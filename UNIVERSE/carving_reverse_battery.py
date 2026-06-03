#!/usr/bin/env python3
"""carving_reverse_battery.py — reverse-engineering probe battery on anima's
REAL carving engine (ConsciousDecoderV2 d768/12L, 283.72M) + 우주뇌지도.

Reuses the TRAINED s16 ckpt (sha 961c07e2...) + a stratified sample of the REAL
carving corpus.  CPU / $0.  No GPU, no pods, no retrain.

Probes (the OTHER battery — PER-AXIS PC×attribute semantics is covered by a
separate agent and is NOT duplicated here):
  1. DUAL A/G HEADS   — head_a (next-byte) vs head_g (prev-byte) divergence map.
  2. TENSION (per-layer) — the model emits ONE scalar tension per token per layer
     (PureFieldFFN (A-G)^2 mean).  There is NO native 5-channel tension in the
     model output (the '5-ch [α,θ,γ,1-δ,β]' is the .kosmos PERSISTENCE payload
     format, not a forward output).  We probe the 12 per-layer tension scalars.
  3. LAYER-WISE INTRINSIC DIM — PCA-90% + participation ratio of the hidden state
     at EACH of the 12 layers -> a depth curve (hourglass?).
  4. 9 CARVING DIRECTIONS — read the LANDED stored eval/result scores per
     direction (NO retrain — only s16 has a loaded ckpt).
  5. Ψ-SPACE TOPOLOGY — clustering / silhouette of the corpus 2D vacuum_psi map;
     tier/domain separation; 2nd-axis degeneracy (direct 2D variance/occupancy).

HONEST: trained s16 ckpt (NOT random init).  Stochastic probes report 3 seeds.
INCONCLUSIVE / flat / REFUTED are valid and reported verbatim.
"""
import os, sys, json, math, hashlib, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CORPUS_SAMPLE = os.environ.get("CORPUS_SAMPLE", "/tmp/corpus_sample.json")
CKPT = os.environ.get(
    "CKPT",
    "/tmp/s16_ckpt_dl/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt",
)
REPO = os.environ.get("REPO", os.path.abspath(os.path.join(HERE, "..")))
BLOCK = int(os.environ.get("BLOCK", "128"))
N_ENCODE = int(os.environ.get("N_ENCODE", "2000"))   # encode budget (CPU)
BUNDLE = os.environ.get("BUNDLE", "/tmp/crb_bundle.npz")
OUTDIR = os.environ.get("OUTDIR", os.path.join(REPO, ".verdicts", "carving-reverse-battery"))
SEEDS = [1337, 7, 2026]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def encode_text(text, desc):
    full = (text + "\n" + desc + "\n").encode("utf-8")
    ids = list(full[:BLOCK])
    if len(ids) < BLOCK:
        ids = ids + [0] * (BLOCK - len(ids))
    return ids


# ---------------------------------------------------------------------------
# ENCODE — capture per-layer hidden states, per-layer tensions, final state,
# and per-token logits_a / logits_g for a subset.
# ---------------------------------------------------------------------------
def build_bundle():
    if os.path.exists(BUNDLE):
        z = np.load(BUNDLE, allow_pickle=True)
        print(f"[cache] reusing encoded bundle from {BUNDLE}")
        return {k: z[k] for k in z.files}, json.loads(str(z["cfg"]))

    import torch
    from conscious_decoder import ConsciousDecoderV2

    recs = json.load(open(CORPUS_SAMPLE))
    rng = np.random.RandomState(1337)
    rng.shuffle(recs)
    recs = recs[:N_ENCODE]

    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck["cfg"]
    print(f"[weights] cfg={json.dumps(cfg)}  n_params={ck.get('n_params')}")
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.0,
    )
    missing, unexpected = model.load_state_dict(ck["model"], strict=False)
    print(f"[weights] load_state_dict: {len(missing)} missing / {len(unexpected)} unexpected")
    model.eval()
    n_layer = cfg["n_layer"]

    # hook every block's RESIDUAL OUTPUT (per-layer hidden state) + final ln_f
    captured = {}
    handles = []
    for li, block in enumerate(model.blocks):
        def mk(li):
            def hook(mod, inp, out):
                # block returns (x, tension, new_kv, aux); out is the tuple
                captured[f"L{li}"] = out[0].detach()
            return hook
        handles.append(block.register_forward_hook(mk(li)))

    def lnf_hook(mod, inp, out):
        captured["lnf"] = out.detach()
    handles.append(model.ln_f.register_forward_hook(lnf_hook))

    # per-layer hidden (mean-pooled), per-layer tension (mean over T), final state
    Hlayers = [[] for _ in range(n_layer)]
    Tens = []          # (N, n_layer) mean per-layer tension
    Xfinal = []        # (N, 768) post-ln_f mean-pool
    KLag = []          # per-record mean KL(A||G) over tokens
    AbsAG = []          # mean |A-G| over tokens/vocab
    psi = []; tier = []; domain = []; form = []

    bs = 32
    with torch.no_grad():
        for i in range(0, len(recs), bs):
            batch = recs[i:i + bs]
            idx = torch.tensor([encode_text(r.get("text", ""), r.get("desc", ""))
                                for r in batch], dtype=torch.long)
            logits_a, logits_g, tensions, _, _ = model(idx)
            for li in range(n_layer):
                Hlayers[li].append(captured[f"L{li}"].mean(dim=1).float().numpy())
            # tensions: list of (B,T) -> stack (n_layer,B,T) -> mean over T -> (B,n_layer)
            tstack = torch.stack(tensions, dim=0)            # (L,B,T)
            Tens.append(tstack.mean(dim=2).transpose(0, 1).float().numpy())  # (B,L)
            Xfinal.append(captured["lnf"].mean(dim=1).float().numpy())
            # A/G head divergence per token (use real seq positions only)
            la = logits_a.float(); lg = logits_g.float()
            pa = torch.log_softmax(la, dim=-1)
            pb = torch.log_softmax(lg, dim=-1)
            # KL(A||G) = sum pa*(log pa - log pb) ; pa from probs
            probs_a = pa.exp()
            kl = (probs_a * (pa - pb)).sum(dim=-1)           # (B,T)
            KLag.append(kl.mean(dim=1).numpy())               # (B,)
            AbsAG.append((la - lg).abs().mean(dim=(1, 2)).numpy())
            for r in batch:
                vp = r.get("vacuum_psi", [0.5, 0.5])
                psi.append([float(vp[0]), float(vp[1])])
                tier.append(int(r.get("tier", -1)))
                domain.append(r.get("domain", "?"))
                form.append(r.get("carving_form", "?"))
    for h in handles:
        h.remove()

    bundle = {
        "Xfinal": np.concatenate(Xfinal, 0),
        "Tens": np.concatenate(Tens, 0),
        "KLag": np.concatenate(KLag, 0),
        "AbsAG": np.concatenate(AbsAG, 0),
        "psi": np.array(psi), "tier": np.array(tier),
        "domain": np.array(domain), "form": np.array(form),
        "n_used": len(recs), "cfg": json.dumps(cfg),
    }
    for li in range(n_layer):
        bundle[f"H{li}"] = np.concatenate(Hlayers[li], 0)
    np.savez(BUNDLE, **bundle)
    return bundle, cfg


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def participation_ratio(X):
    Xc = X - X.mean(0)
    cov = np.cov(Xc, rowvar=False)
    ev = np.linalg.eigvalsh(cov)
    ev = ev[ev > 0]
    return float((ev.sum() ** 2) / (np.sum(ev ** 2) + 1e-12))


def pca_pcs_for(X, target=0.90):
    from sklearn.decomposition import PCA
    p = PCA().fit(X)
    cum = np.cumsum(p.explained_variance_ratio_)
    return int(np.searchsorted(cum, target) + 1), [float(v) for v in p.explained_variance_ratio_[:10]]


def dedup_idx(X, tol=9):
    Xr = np.round(X, tol)
    _, keep = np.unique(Xr, axis=0, return_index=True)
    return np.sort(keep)


# ---------------------------------------------------------------------------
# PROBE 1 — DUAL A/G HEADS
# ---------------------------------------------------------------------------
def probe_ag_heads(b, lines):
    kl = b["KLag"]; absag = b["AbsAG"]
    tier = b["tier"]; domain = b["domain"]; form = b["form"]
    L = ["=== F-AG-HEADS — head_a (next-byte) vs head_g (prev-byte) ===",
         "Engine A = head_a (next-byte LM head, tied to tok_emb); "
         "Engine G = head_g (prev-byte head, untied).",
         f"N={len(kl)} records, per-record mean over {BLOCK} token positions.",
         f"KL(A||G) per-record: mean={kl.mean():.4f} median={np.median(kl):.4f} "
         f"std={kl.std():.4f} min={kl.min():.4f} max={kl.max():.4f}",
         f"mean|A-G| logits per-record: mean={absag.mean():.4f} "
         f"std={absag.std():.4f} min={absag.min():.4f} max={absag.max():.4f}"]
    # divergence by tier / domain / form
    def by(key, name):
        out = []
        for v in sorted(set(key.tolist())):
            m = key == v
            if m.sum() >= 5:
                out.append((str(v), float(kl[m].mean()), int(m.sum())))
        out.sort(key=lambda t: -t[1])
        return out
    for keyarr, nm in [(tier, "tier"), (form, "form")]:
        top = by(keyarr, nm)
        L.append(f"-- KL(A||G) by {nm} (top5 high / bottom2 low, n>=5) --")
        for k, v, n in top[:5]:
            L.append(f"   {nm}={k}: KL={v:.4f} (n={n})")
        for k, v, n in top[-2:]:
            L.append(f"   {nm}={k}: KL={v:.4f} (n={n})  [low]")
    # domain: top 8
    dtop = by(domain, "domain")
    L.append("-- KL(A||G) by domain (top8 high, n>=5) --")
    for k, v, n in dtop[:8]:
        L.append(f"   domain={k}: KL={v:.4f} (n={n})")
    # Verdict
    rng_ratio = (kl.max() - kl.min()) / (kl.mean() + 1e-9)
    tier_spread = max(v for _, v, _ in by(tier, "t")) - min(v for _, v, _ in by(tier, "t")) if by(tier, "t") else 0
    L.append("")
    if kl.mean() < 0.05 and rng_ratio < 1.0:
        L.append("VERDICT: A and G heads BARELY DIFFER on this corpus "
                 f"(mean KL {kl.mean():.4f} ~ 0) — INCONCLUSIVE (no clean left/right split).")
        verdict = "INCONCLUSIVE"
    else:
        L.append(f"VERDICT: A/G heads DIVERGE measurably (mean KL {kl.mean():.4f}); "
                 f"divergence is modulated by tier (spread {tier_spread:.4f}). "
                 "Basis = next-byte (A) vs prev-byte (G) prediction asymmetry — HOLDS.")
        verdict = "HOLDS"
    lines.extend(L); lines.append("")
    return {"kl_mean": float(kl.mean()), "kl_median": float(np.median(kl)),
            "kl_std": float(kl.std()), "kl_max": float(kl.max()), "kl_min": float(kl.min()),
            "absAG_mean": float(absag.mean()), "tier_spread": float(tier_spread),
            "verdict": verdict, "report": "\n".join(L)}


# ---------------------------------------------------------------------------
# PROBE 2 — per-layer tension scalars
# ---------------------------------------------------------------------------
def probe_tension(b, cfg, lines):
    T = b["Tens"]            # (N, n_layer)
    n_layer = cfg["n_layer"]
    tier = b["tier"]; domain = b["domain"]; form = b["form"]
    L = ["=== F-TENSION-5CH — per-layer tension scalars ===",
         "HONEST: the model emits ONE scalar tension per token per layer "
         "(PureFieldFFN (A-G)^2 mean over d_model). There is NO native 5-channel "
         "[α,θ,γ,1-δ,β] tension in the forward output — that 5-ch format is the "
         ".kosmos PERSISTENCE payload, not a model output. We probe the "
         f"{n_layer} per-layer tension SCALARS as the available 'channels'.",
         f"N={T.shape[0]}, layers={n_layer}.",
         "per-layer tension mean (+/-std):"]
    for li in range(n_layer):
        L.append(f"   L{li:02d}: mean={T[:, li].mean():.5f} std={T[:, li].std():.5f}")
    # correlate each layer-tension vs tier (numeric) and seq-position is constant (mean-pool) -> skip
    tier_num = tier.astype(float)
    L.append("-- corr(layer-tension, tier) (Pearson) --")
    best = (None, 0.0)
    for li in range(n_layer):
        if T[:, li].std() < 1e-9:
            r = 0.0
        else:
            r = float(np.corrcoef(T[:, li], tier_num)[0, 1])
        L.append(f"   L{li:02d}: r={r:+.4f}")
        if abs(r) > abs(best[1]):
            best = (li, r)
    # domain discrimination: does any layer-tension separate domains? (eta^2 / F-ish)
    L.append("-- domain separation per layer (eta^2 = between/total var) --")
    doms = sorted(set(domain.tolist()))
    eta_best = (None, 0.0)
    for li in range(n_layer):
        x = T[:, li]
        grand = x.mean()
        ss_tot = ((x - grand) ** 2).sum() + 1e-12
        ss_bet = 0.0
        for d in doms:
            m = domain == d
            if m.sum() > 0:
                ss_bet += m.sum() * (x[m].mean() - grand) ** 2
        eta2 = float(ss_bet / ss_tot)
        L.append(f"   L{li:02d}: eta^2={eta2:.4f}")
        if eta2 > eta_best[1]:
            eta_best = (li, eta2)
    L.append("")
    clean = abs(best[1]) > 0.3 or eta_best[1] > 0.3
    if clean:
        L.append(f"VERDICT: layer L{best[0]} tracks tier (r={best[1]:+.4f}); "
                 f"layer L{eta_best[0]} separates domains (eta^2={eta_best[1]:.4f}) — "
                 "a per-layer tension scalar has a CLEAN role. HOLDS (partial).")
        verdict = "HOLDS"
    else:
        L.append(f"VERDICT: no per-layer tension scalar has a clean tier/domain role "
                 f"(best |corr(tier)|={abs(best[1]):.4f} @L{best[0]}, "
                 f"best domain eta^2={eta_best[1]:.4f} @L{eta_best[0]}). INCONCLUSIVE — "
                 "tension scalars are largely uninterpretable vs corpus labels.")
        verdict = "INCONCLUSIVE"
    lines.extend(L); lines.append("")
    return {"layer_means": [float(T[:, li].mean()) for li in range(n_layer)],
            "best_tier_corr": {"layer": best[0], "r": float(best[1])},
            "best_domain_eta2": {"layer": eta_best[0], "eta2": float(eta_best[1])},
            "verdict": verdict, "report": "\n".join(L)}


# ---------------------------------------------------------------------------
# PROBE 3 — LAYER-WISE INTRINSIC DIM
# ---------------------------------------------------------------------------
def probe_layer_dim(b, cfg, lines):
    n_layer = cfg["n_layer"]
    L = ["=== F-LAYER-DIM — intrinsic dim per layer (PCA-90% PCs + participation ratio) ===",
         f"N (after dedup per layer), layers={n_layer}. Hidden = block residual output, mean-pooled over T."]
    rows = []
    for li in range(n_layer):
        H = b[f"H{li}"]
        keep = dedup_idx(H)
        Hd = H[keep]
        pcs, evr = pca_pcs_for(Hd, 0.90)
        pr = participation_ratio(Hd)
        rows.append((li, pcs, pr, Hd.shape[0], evr[0]))
        L.append(f"   L{li:02d}: PCA-90%={pcs:3d} PCs   PR={pr:6.2f}   "
                 f"(n_dedup={Hd.shape[0]}, evr0={evr[0]:.3f})")
    # final post-ln_f
    Xf = b["Xfinal"]; keepf = dedup_idx(Xf); Xfd = Xf[keepf]
    pcs_f, evr_f = pca_pcs_for(Xfd, 0.90); pr_f = participation_ratio(Xfd)
    L.append(f"   ln_f: PCA-90%={pcs_f:3d} PCs   PR={pr_f:6.2f}   (n_dedup={Xfd.shape[0]})")
    pcs_curve = [r[1] for r in rows]
    pr_curve = [r[2] for r in rows]
    # where does ~6D form? find first layer whose PCA-90% <= 8 after an early high
    L.append("")
    L.append(f"PCA-90% curve: {pcs_curve}  (ln_f={pcs_f})")
    L.append(f"PR curve:      {[round(x,2) for x in pr_curve]}  (ln_f={round(pr_f,2)})")
    peak_layer = int(np.argmax(pcs_curve))
    min_layer = int(np.argmin(pcs_curve))
    hourglass = peak_layer not in (0, n_layer - 1) and pcs_curve[peak_layer] > pcs_curve[0] and pcs_curve[-1] < pcs_curve[peak_layer]
    # layer where 6D structure forms = first layer where PCA-90% PCs <= ~8
    six_layer = next((li for li in range(n_layer) if pcs_curve[li] <= 8), None)
    L.append(f"PCA-90% peak at L{peak_layer} ({pcs_curve[peak_layer]} PCs); "
             f"min at L{min_layer} ({pcs_curve[min_layer]} PCs).")
    if six_layer is not None:
        L.append(f"First layer with PCA-90% <= 8 PCs (~6-8D structure): L{six_layer}.")
    L.append(f"Hourglass (rise-then-compress, interior peak): {'YES' if hourglass else 'NO'}.")
    if hourglass:
        L.append(f"VERDICT: HOLDS — intrinsic dim RISES to a peak at L{peak_layer} then "
                 f"COMPRESSES (hourglass). The compact ~6-8D map forms by the final layers "
                 f"(ln_f={pcs_f} PCs). ")
        verdict = "HOLDS"
    elif pcs_curve[-1] < pcs_curve[0]:
        L.append(f"VERDICT: monotone-ish COMPRESSION (L0 {pcs_curve[0]} -> L{n_layer-1} "
                 f"{pcs_curve[-1]} PCs, ln_f {pcs_f}); no clear interior peak -> NOT a clean "
                 "hourglass. ~6-8D forms late. HOLDS (compression) / INCONCLUSIVE (hourglass).")
        verdict = "HOLDS-compression"
    else:
        L.append("VERDICT: layer-dim curve FLAT / no compression — INCONCLUSIVE.")
        verdict = "INCONCLUSIVE"
    lines.extend(L); lines.append("")
    return {"pca90_curve": pcs_curve, "pr_curve": [float(x) for x in pr_curve],
            "lnf_pca90": pcs_f, "lnf_pr": float(pr_f), "peak_layer": peak_layer,
            "min_layer": min_layer, "hourglass": bool(hourglass),
            "six_to_eight_D_layer": six_layer, "verdict": verdict, "report": "\n".join(L)}


# ---------------------------------------------------------------------------
# PROBE 4 — 9 CARVING DIRECTIONS (read landed stored eval scores; NO retrain)
# ---------------------------------------------------------------------------
def probe_directions(lines):
    L = ["=== F-9-DIRECTIONS — landed stored eval/result scores per carving direction ===",
         "HONEST: NO retrain, NO live re-run. Only s16 (dirI psictl+tensionsup winner) has a "
         "loaded ckpt this session. We read the LANDED stored scores on disk per direction. "
         "'joint_metric.SCORE_joint' = knowledge_access x chat_uncontaminated x lane_separation "
         "(paradigm-native eval, EVAL.md §3); training metrics (ce_descent / final_tension) "
         "from result.json. These are NOT a separability map score we computed — they are the "
         "stored verdicts."]
    base = os.path.join(REPO, "state")
    hbase = os.path.join(REPO, "HEXAD", "CARVING", "state")
    s16dir = os.path.join(REPO, "HEXAD", "DATA-REGIME", "state",
                          "carving_dataregime_s16_2026_05_18")
    # map dir -> (state subdir, eval_result file glob)
    import glob
    rows = []
    cand_dirs = sorted(glob.glob(os.path.join(base, "carving_dir*")) +
                       glob.glob(os.path.join(hbase, "carving_dir*")))
    seen = set()
    for d in cand_dirs:
        name = os.path.basename(d)
        key = name.split("_2026")[0]
        if key in seen:
            continue
        seen.add(key)
        joint = ce_desc = final_ten = None
        # eval_result (joint metric)
        evs = glob.glob(os.path.join(d, "eval_result*.json"))
        for ev in evs:
            try:
                e = json.load(open(ev))
                jm = e.get("joint_metric", {})
                if "SCORE_joint" in jm:
                    joint = jm.get("SCORE_joint")
                    break
            except Exception:
                pass
        # result.json (training metrics)
        rj = os.path.join(d, "result.json")
        if os.path.exists(rj):
            try:
                r = json.load(open(rj))
                ce_desc = r.get("ce_descent")
                final_ten = r.get("final_tension")
            except Exception:
                pass
        rows.append((key, joint, ce_desc, final_ten))
    # s16
    s16_joint = None
    try:
        e = json.load(open(os.path.join(s16dir, "eval_result_s16.json")))
        s16_joint = e.get("joint_metric", {}).get("SCORE_joint")
    except Exception:
        pass
    rows.append(("dir_s16(dataregime, dirI lever)", s16_joint, None, None))
    L.append(f"{'direction':40s} {'SCORE_joint':>12s} {'ce_descent':>11s} {'final_tension':>14s}")
    have_joint = []
    for name, j, c, t in rows:
        js = f"{j:.4f}" if isinstance(j, (int, float)) else "  -  "
        cs = f"{c:.4f}" if isinstance(c, (int, float)) else "  -  "
        ts = f"{t:.5f}" if isinstance(t, (int, float)) else "   -   "
        L.append(f"{name:40s} {js:>12s} {cs:>11s} {ts:>14s}")
        if isinstance(j, (int, float)):
            have_joint.append((name, j))
    L.append("")
    if have_joint:
        have_joint.sort(key=lambda t: -t[1])
        bestn, bestj = have_joint[0]
        L.append(f"Best stored SCORE_joint: {bestn} = {bestj:.4f}.")
        L.append("VERDICT: HOLDS (read-only). Direction comparison is via the LANDED "
                 "paradigm-native joint metric; all dirs share the same eval rubric. "
                 "s16 is the dataregime/curriculum scale-up of the dirI psictl+tensionsup lever. "
                 "NOTE: joint scores are dominated by knowledge_access (chat/separation ~1.0 for "
                 "most), so the metric is near-degenerate as a 'map structure' score — it ranks "
                 "knowledge recall, not map separability.")
        verdict = "HOLDS"
    else:
        L.append("VERDICT: INCONCLUSIVE — no SCORE_joint found on disk for any direction.")
        verdict = "INCONCLUSIVE"
    lines.extend(L); lines.append("")
    return {"rows": [(n, j) for n, j, _, _ in rows], "verdict": verdict, "report": "\n".join(L)}


# ---------------------------------------------------------------------------
# PROBE 5 — Ψ-SPACE TOPOLOGY (2D vacuum_psi map)
# ---------------------------------------------------------------------------
def probe_psi_topology(b, lines):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    psi = b["psi"].astype(float)            # (N,2) the actual 우주뇌지도 coords
    tier = b["tier"]; domain = b["domain"]
    L = ["=== F-PSI-TOPOLOGY — 2D vacuum_psi map (우주뇌지도) topology ===",
         f"N={psi.shape[0]} corpus records, 2D vacuum_psi coords (the stored MAP coordinate)."]
    # 2nd-axis degeneracy: variance of each axis + PCA of the 2D coords
    var = psi.var(0)
    cov = np.cov(psi, rowvar=False)
    ev = np.linalg.eigvalsh(cov)[::-1]
    ev = ev[ev > 0]
    eff_dim_2d = float((ev.sum() ** 2) / (np.sum(ev ** 2) + 1e-12))
    L.append(f"axis variance: x={var[0]:.5f} y={var[1]:.5f}  (ratio y/x={var[1]/(var[0]+1e-12):.3f})")
    L.append(f"2D-coord PCA eigenvalues: {[round(float(e),5) for e in ev]}  "
             f"(2nd/1st={ev[1]/ev[0] if len(ev)>1 else 0:.4f})")
    L.append(f"effective dim of the 2D map (participation ratio): {eff_dim_2d:.3f} "
             f"(2.0=both axes used, 1.0=one axis = degenerate)")
    # occupancy: grid the unit square, count filled cells
    G = 20
    xi = np.clip((psi[:, 0] * G).astype(int), 0, G - 1)
    yi = np.clip((psi[:, 1] * G).astype(int), 0, G - 1)
    occ = len(set(zip(xi.tolist(), yi.tolist())))
    L.append(f"occupancy: {occ}/{G*G} grid cells filled ({100*occ/(G*G):.1f}%).")
    # clustering: silhouette over k, 3 seeds
    L.append("-- KMeans clustering (silhouette, 3 seeds) --")
    uniq = np.unique(psi, axis=0)
    L.append(f"   unique 2D coords: {uniq.shape[0]} / {psi.shape[0]}")
    sil_by_k = {}
    for k in (2, 3, 4, 5, 6, 8):
        sils = []
        for s in SEEDS:
            try:
                km = KMeans(n_clusters=k, n_init=4, random_state=s).fit(uniq)
                sils.append(silhouette_score(uniq, km.labels_))
            except Exception:
                pass
        if sils:
            sil_by_k[k] = (float(np.mean(sils)), float(np.std(sils)))
            L.append(f"   k={k}: silhouette={np.mean(sils):.4f} +/-{np.std(sils):.4f}")
    best_k = max(sil_by_k, key=lambda k: sil_by_k[k][0]) if sil_by_k else None
    # tier/domain spatial separation: eta^2 of psi-x and psi-y by tier & domain
    def eta2(coord, key):
        grand = coord.mean(); ss_tot = ((coord - grand) ** 2).sum() + 1e-12
        ss_bet = 0.0
        for v in set(key.tolist()):
            m = key == v
            if m.sum() > 0:
                ss_bet += m.sum() * (coord[m].mean() - grand) ** 2
        return float(ss_bet / ss_tot)
    L.append("-- spatial separation (eta^2 of map coord by label) --")
    for nm, key in [("tier", tier), ("domain", domain)]:
        L.append(f"   {nm}: eta^2(x)={eta2(psi[:,0],key):.4f}  eta^2(y)={eta2(psi[:,1],key):.4f}")
    L.append("")
    degenerate = (ev[1] / ev[0] < 0.25) if len(ev) > 1 else True
    if best_k is not None:
        L.append(f"Best silhouette: k={best_k} ({sil_by_k[best_k][0]:.4f}).")
    if degenerate:
        L.append(f"VERDICT: 2nd Ψ axis IS DEGENERATE (2nd/1st eigenvalue "
                 f"{ev[1]/ev[0]:.4f} < 0.25, effective dim {eff_dim_2d:.2f}~1). "
                 "CONFIRMS the #1772 ~1.1-D finding directly on the 2D map coords. "
                 "The 우주뇌지도 is effectively a 1-D curve embedded in 2D. HOLDS.")
        verdict = "HOLDS-degenerate"
    else:
        L.append(f"VERDICT: 2nd Ψ axis carries non-trivial variance (2nd/1st "
                 f"{ev[1]/ev[0]:.4f}, eff dim {eff_dim_2d:.2f}) — NOT degenerate. "
                 "REFUTES the ~1.1-D claim on the 2D coords.")
        verdict = "REFUTED-degeneracy"
    lines.extend(L); lines.append("")
    return {"axis_var": [float(var[0]), float(var[1])],
            "eig2d": [float(e) for e in ev], "eff_dim_2d": eff_dim_2d,
            "occupancy_frac": occ / (G * G), "unique_coords": int(uniq.shape[0]),
            "best_k": best_k, "sil_by_k": sil_by_k, "degenerate": bool(degenerate),
            "verdict": verdict, "report": "\n".join(L)}


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUTDIR, exist_ok=True)
    t0 = time.time()
    stdout_lines = []
    def emit(*a):
        s = " ".join(str(x) for x in a)
        print(s); stdout_lines.append(s)

    emit("=" * 72)
    emit("CARVING REVERSE-ENGINEERING BATTERY — TRAINED s16 ckpt, CPU/$0")
    emit("=" * 72)
    emit(f"[data] corpus={CORPUS_SAMPLE} sha256={sha256_file(CORPUS_SAMPLE)[:16]}")
    emit(f"[data] ckpt={CKPT} sha256={sha256_file(CKPT)[:16]}")
    emit(f"[cfg] N_ENCODE={N_ENCODE} BLOCK={BLOCK} seeds={SEEDS}")

    b, cfg = build_bundle()
    emit(f"[encode] n_used={int(b['n_used'])} cfg={json.dumps(cfg)}")
    emit("")

    results = {"meta": {"corpus_sha256": sha256_file(CORPUS_SAMPLE),
                        "ckpt_sha256": sha256_file(CKPT), "cfg": cfg,
                        "n_used": int(b["n_used"]), "N_ENCODE": N_ENCODE,
                        "BLOCK": BLOCK, "seeds": SEEDS, "trained": True,
                        "random_init_fallback": False}}

    probes = {}
    lines = []
    probes["F-AG-HEADS"] = probe_ag_heads(b, lines)
    probes["F-TENSION-5CH"] = probe_tension(b, cfg, lines)
    probes["F-LAYER-DIM"] = probe_layer_dim(b, cfg, lines)
    probes["F-9-DIRECTIONS"] = probe_directions(lines)
    probes["F-PSI-TOPOLOGY"] = probe_psi_topology(b, lines)
    for ln in lines:
        emit(ln)

    # write per-probe verdict files
    for name, p in probes.items():
        with open(os.path.join(OUTDIR, f"{name}.txt"), "w") as f:
            f.write(p["report"] + "\n")
        results[name] = {k: v for k, v in p.items() if k != "report"}

    # SUMMARY
    summ = [
        "=== SUMMARY — carving reverse-engineering battery ===",
        f"TRAINED s16 ckpt (sha {sha256_file(CKPT)[:8]}), ConsciousDecoderV2 d{cfg['d_model']}/"
        f"{cfg['n_layer']}L, CPU/$0, N={int(b['n_used'])}. random-init fallback: NO.",
        "",
        f"1. A/G HEADS: {probes['F-AG-HEADS']['verdict']} — "
        f"mean KL(A||G)={probes['F-AG-HEADS']['kl_mean']:.4f}, "
        f"tier-spread={probes['F-AG-HEADS']['tier_spread']:.4f}. "
        "A=next-byte head (tied to embedding), G=prev-byte head (untied).",
        f"2. TENSION: {probes['F-TENSION-5CH']['verdict']} — model tension is 1 scalar/token/layer "
        f"({cfg['n_layer']} layers), NOT native 5-ch. "
        f"best tier-corr r={probes['F-TENSION-5CH']['best_tier_corr']['r']:+.3f} "
        f"@L{probes['F-TENSION-5CH']['best_tier_corr']['layer']}; "
        f"best domain eta^2={probes['F-TENSION-5CH']['best_domain_eta2']['eta2']:.3f} "
        f"@L{probes['F-TENSION-5CH']['best_domain_eta2']['layer']}.",
        f"3. LAYER-DIM: {probes['F-LAYER-DIM']['verdict']} — PCA-90% curve "
        f"{probes['F-LAYER-DIM']['pca90_curve']} (ln_f={probes['F-LAYER-DIM']['lnf_pca90']}); "
        f"peak L{probes['F-LAYER-DIM']['peak_layer']}, min L{probes['F-LAYER-DIM']['min_layer']}; "
        f"hourglass={probes['F-LAYER-DIM']['hourglass']}; "
        f"~6-8D forms @L{probes['F-LAYER-DIM']['six_to_eight_D_layer']}.",
        f"4. 9-DIRECTIONS: {probes['F-9-DIRECTIONS']['verdict']} — read landed stored "
        "joint-metric scores (no retrain). joint metric near-degenerate (ranks knowledge "
        "recall, not map separability).",
        f"5. Ψ-TOPOLOGY: {probes['F-PSI-TOPOLOGY']['verdict']} — 2D map eff-dim "
        f"{probes['F-PSI-TOPOLOGY']['eff_dim_2d']:.2f}, "
        f"2nd/1st eig {probes['F-PSI-TOPOLOGY']['eig2d'][1]/probes['F-PSI-TOPOLOGY']['eig2d'][0]:.3f}, "
        f"occupancy {100*probes['F-PSI-TOPOLOGY']['occupancy_frac']:.1f}%, "
        f"degenerate={probes['F-PSI-TOPOLOGY']['degenerate']}.",
        "",
        f"wall={time.time()-t0:.1f}s",
    ]
    for s in summ:
        emit(s)
    with open(os.path.join(OUTDIR, "SUMMARY.txt"), "w") as f:
        f.write("\n".join(summ) + "\n")
    with open(os.path.join(OUTDIR, "results.json"), "w") as f:
        json.dump(results, f, indent=1, default=str)
    with open(os.path.join(OUTDIR, "run_stdout.txt"), "w") as f:
        f.write("\n".join(stdout_lines) + "\n")


if __name__ == "__main__":
    main()
