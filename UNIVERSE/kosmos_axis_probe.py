#!/usr/bin/env python3
"""kosmos_axis_probe.py — what does each REAL KOSMOS axis (PC) ENCODE?

Builds on kosmos_real_dim.py (#1772): the REAL anima carving manifold (Ψ-space,
d=768 post-ln_f conscious state of the TRAINED s16 ckpt) has intrinsic d ~ 6-10,
knee ~ 8, and the current 2D vacuum_psi map retains only 67% variance / 8% tier-
domain discrimination.  That answered HOW MANY dims; this answers WHAT EACH DIM
HOLDS.

Question (per-axis semantics): take the top ~8-16 PCs of the d=768 conscious
state.  For EACH PC, MEASURE its association with every corpus attribute present
(tier · domain · carving_form · curriculum_stage · curriculum_rank · basin_radius
· vacuum_psi[x,y]).  Build a PC x attribute matrix and LABEL each axis by its
dominant attribute — or "entangled/none" if below the permutation-noise floor.

CRITICAL HONESTY (task directive): learned PCA axes are NOT auto-interpretable.
We do not assume the toy dim-ladder's labels.  We MEASURE and report what each
encodes, flag entangled/uninterpretable axes honestly, and give a permutation
noise floor so "association" is not over-read.

Association metrics:
  - categorical attribute (tier/domain/form/stage): eta^2 (variance of the PC
    explained by the category) + 1-vs-rest macro-AUC of the single PC.
  - continuous attribute (curriculum_rank/basin_radius/psi_x/psi_y/curriculum_index):
    Spearman rho (rank correlation, monotone-robust) + |Pearson r|.
  - permutation noise floor: shuffle the attribute 200x, take the 95th pct of
    the metric -> any real value below it is "none".

p7/g5: real artifact only, exact sha recorded, no fabricated label.  CPU / $0.
Reuses /tmp/krd_X_cache.npz if present (same encoding as #1772); else rebuilds
from the real ckpt + corpus sample.
"""
import os, sys, json, time, hashlib, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from scipy.stats import spearmanr, pearsonr
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score

CORPUS_SAMPLE = os.environ.get("CORPUS_SAMPLE", "/tmp/corpus_sample.json")
CKPT = os.environ.get(
    "S16_CKPT",
    "/tmp/s16_ckpt_dl/HEXAD/DATA-REGIME/state/carving_dataregime_s16_2026_05_18/ckpt_carving_s16.pt",
)
CACHE = os.environ.get("X_CACHE", "/tmp/krd_X_cache.npz")
N_PC = int(os.environ.get("N_PC", "16"))   # top PCs to label
BLOCK = 128
N_ENCODE = int(os.environ.get("N_ENCODE", "6000"))
N_PERM = int(os.environ.get("N_PERM", "200"))

np.random.seed(1337)


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


def build_states():
    """Return (X[N,768], attrs dict). Reuses #1772 cache for X+core attrs;
    always reloads the corpus sample for the EXTRA attributes (curriculum_*,
    basin_radius) the cache didn't store, aligned by the SAME shuffle seed."""
    recs = json.load(open(CORPUS_SAMPLE))
    rng = np.random.RandomState(1337)        # identical to kosmos_real_dim.py
    rng.shuffle(recs)
    recs = recs[:N_ENCODE]

    def col(key, default, cast):
        return np.array([cast(r.get(key, default)) for r in recs])

    attrs_cat = {
        "tier":             col("tier", -1, int),
        "domain":           col("domain", "?", str),
        "carving_form":     col("carving_form", "?", str),
        "curriculum_stage": col("curriculum_stage", -1, int),
    }
    psi = np.array([[float(r.get("vacuum_psi", [0.5, 0.5])[0]),
                     float(r.get("vacuum_psi", [0.5, 0.5])[1])] for r in recs])
    attrs_cont = {
        "curriculum_rank":  col("curriculum_rank", float("nan"), float),
        "curriculum_index": col("curriculum_index", float("nan"), float),
        "basin_radius":     col("basin_radius", float("nan"), float),
        "vacuum_psi_x":     psi[:, 0],
        "vacuum_psi_y":     psi[:, 1],
    }

    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        X = z["X"]
        print(f"[cache] reusing encoded X from {CACHE} shape={X.shape}")
        # sanity: cache tier order must match our recs order
        if "tier" in z and len(z["tier"]) == len(attrs_cat["tier"]):
            mism = int(np.sum(z["tier"] != attrs_cat["tier"]))
            print(f"[cache] tier-order mismatch count = {mism} (0 = aligned)")
        n = min(X.shape[0], len(recs))
        X = X[:n]
        for d in (attrs_cat, attrs_cont):
            for k in d:
                d[k] = d[k][:n]
        return X, attrs_cat, attrs_cont, None, None

    import torch
    from _cd_s16 import ConsciousDecoderV2
    torch.manual_seed(1337)
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck["cfg"]
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.0)
    model.load_state_dict(ck["model"], strict=False)
    model.eval()
    captured = {}
    h = model.ln_f.register_forward_hook(lambda m, i, o: captured.__setitem__("h", o.detach()))
    X = []
    bs = 64
    with torch.no_grad():
        for i in range(0, len(recs), bs):
            batch = recs[i:i + bs]
            idx = torch.tensor([encode_text(r.get("text", ""), r.get("desc", ""))
                                for r in batch], dtype=torch.long)
            model(idx)
            X.append(captured["h"].mean(dim=1).float().numpy())
    h.remove()
    X = np.concatenate(X, 0)
    np.savez(CACHE, X=X, tier=attrs_cat["tier"], domain=attrs_cat["domain"],
             form=attrs_cat["carving_form"], psi=psi,
             n_used=len(recs), cfg=json.dumps(cfg), n_params=ck["n_params"])
    return X, attrs_cat, attrs_cont, cfg, ck["n_params"]


# ---------- association metrics ----------

def eta_squared(pc, labels):
    """fraction of PC variance explained by category membership (one-way ANOVA).
    NOTE: eta^2 is POSITIVELY BIASED by category cardinality (~ (k-1)/(N-1) for
    k groups on noise) -> 168-way tier looks 'explained' even on a random PC.
    Reported for transparency, but the label decision uses omega^2 + AUC."""
    grand = pc.mean()
    ss_tot = np.sum((pc - grand) ** 2)
    if ss_tot < 1e-12:
        return 0.0
    ss_between = 0.0
    for lab in np.unique(labels):
        g = pc[labels == lab]
        if len(g) == 0:
            continue
        ss_between += len(g) * (g.mean() - grand) ** 2
    return float(ss_between / ss_tot)


def omega_squared(pc, labels):
    """bias-corrected effect size (Hays' omega^2). ~0 on noise regardless of k,
    so it is comparable across tier(168) / domain(63) / form(3) / stage(4)."""
    grand = pc.mean()
    ss_tot = float(np.sum((pc - grand) ** 2))
    N = len(pc); k = len(np.unique(labels))
    if ss_tot < 1e-12 or N - k <= 0:
        return 0.0
    ss_b = 0.0
    for lab in np.unique(labels):
        g = pc[labels == lab]
        ss_b += len(g) * (g.mean() - grand) ** 2
    ss_w = ss_tot - ss_b
    ms_w = ss_w / (N - k)
    return float(max(0.0, (ss_b - (k - 1) * ms_w) / (ss_tot + ms_w)))


def macro_auc_single(pc, labels, max_classes=80):
    """mean 1-vs-rest AUC of a SINGLE PC as the score (|AUC-0.5|*2 -> 0..1).
    Caps classes for speed; uses the most populous classes."""
    uniq, cnt = np.unique(labels, return_counts=True)
    order = uniq[np.argsort(-cnt)][:max_classes]
    aucs = []
    for lab in order:
        y = (labels == lab).astype(int)
        if y.sum() < 5 or y.sum() == len(y):
            continue
        try:
            a = roc_auc_score(y, pc)
            aucs.append(abs(a - 0.5) * 2.0)  # symmetric: direction-agnostic
        except Exception:
            pass
    return float(np.mean(aucs)) if aucs else 0.0


def perm_floor_eta(pc, labels, n=N_PERM, q=95):
    rng = np.random.RandomState(0)
    vals = [eta_squared(pc, rng.permutation(labels)) for _ in range(n)]
    return float(np.percentile(vals, q))


def perm_floor_spearman(pc, vec, n=N_PERM, q=95):
    rng = np.random.RandomState(0)
    mask = ~np.isnan(vec)
    pcv, vv = pc[mask], vec[mask]
    vals = []
    for _ in range(n):
        rho, _ = spearmanr(pcv, rng.permutation(vv))
        vals.append(abs(rho))
    return float(np.percentile(vals, q))


def run():
    t0 = time.time()
    print("=== kosmos_axis_probe — what does each REAL KOSMOS axis encode? ===")
    corpus_sha = sha256_file(CORPUS_SAMPLE)
    ckpt_sha = sha256_file(CKPT) if os.path.exists(CKPT) else "MISSING"
    print(f"[data] corpus_sample={CORPUS_SAMPLE} sha256={corpus_sha}")
    print(f"[data] ckpt={CKPT} sha256={ckpt_sha}")

    X, attrs_cat, attrs_cont, cfg, n_params = build_states()
    N = X.shape[0]
    print(f"[encode] N={N} conscious states, dim={X.shape[1]} (post-ln_f mean-pooled)")
    print(f"[attrs] categorical={ {k:int(len(np.unique(v))) for k,v in attrs_cat.items()} }")
    print(f"[attrs] continuous={list(attrs_cont.keys())}")

    Xc = X - X.mean(0)
    pca = PCA(n_components=N_PC).fit(Xc)
    PC = pca.transform(Xc)  # (N, N_PC)
    evr = pca.explained_variance_ratio_
    print(f"[pca] top-{N_PC} EVR: {[round(float(e),4) for e in evr]}")

    results = {
        "data": {
            "corpus_sample_sha256": corpus_sha, "ckpt_sha256": ckpt_sha,
            "n_encoded": int(N), "conscious_dim": int(X.shape[1]),
            "n_pc": N_PC, "n_perm": N_PERM,
            "weights": "TRAINED s16 (real carve)",
            "attrs_categorical": {k: int(len(np.unique(v))) for k, v in attrs_cat.items()},
            "attrs_continuous": list(attrs_cont.keys()),
            "evr_topN": [float(e) for e in evr],
        },
        "matrix": {},   # PCi -> {attr -> metric}
        "labels": {},   # PCi -> dominant attr or "entangled/none"
    }

    # precompute permutation floors per attribute (attribute-level, PC-independent
    # in distribution but we use PC0 scale; eta^2/|rho| are scale-free so any PC works)
    print("\n[floors] computing permutation noise floors (95th pct, "
          f"{N_PERM} shuffles)...")
    floor_cat = {k: perm_floor_eta(PC[:, 0], v) for k, v in attrs_cat.items()}
    floor_cont = {k: perm_floor_spearman(PC[:, 0], v) for k, v in attrs_cont.items()}
    results["floors"] = {"eta2_cat": floor_cat, "spearman_cont": floor_cont}
    print(f"[floors] eta2_cat 95pct: { {k:round(v,4) for k,v in floor_cat.items()} }")
    print(f"[floors] spearman_cont 95pct: { {k:round(v,4) for k,v in floor_cont.items()} }")

    # build the matrix
    print("\n[matrix] per-PC association (eta^2 / macro-AUC for cat; |Spearman| for cont)")
    print("  (label decision = bias-corrected omega^2 [cat] + |Spearman| [cont];")
    print("   eta^2 + AUC reported alongside; eta^2 is cardinality-biased.)")
    rows_print = []
    # omega^2 noise floor (95th pct over shuffles) per categorical attr
    def perm_floor_omega(pc, labels, n=N_PERM, q=95):
        rng = np.random.RandomState(0)
        return float(np.percentile([omega_squared(pc, rng.permutation(labels))
                                    for _ in range(n)], q))
    floor_omega = {k: perm_floor_omega(PC[:, 0], v) for k, v in attrs_cat.items()}
    results["floors"]["omega2_cat"] = floor_omega
    # AUC-separability null per categorical attr (random score -> ~chance level)
    rngn = np.random.RandomState(0)
    auc_null = {k: macro_auc_single(rngn.randn(N), v) for k, v in attrs_cat.items()}
    results["floors"]["auc_sep_null"] = auc_null
    print(f"[floors] omega2_cat 95pct: { {k:round(v,4) for k,v in floor_omega.items()} }")
    print(f"[floors] AUC-separability null (random score): { {k:round(v,3) for k,v in auc_null.items()} }")
    print("  (AUC-sep metric = mean_class |AUC-0.5|*2; 0=chance, 1=perfect separation)")
    for i in range(N_PC):
        pc = PC[:, i]
        row = {"evr": float(evr[i])}
        best_attr, best_strength = None, 0.0
        for k, v in attrs_cat.items():
            e = eta_squared(pc, v)
            w = omega_squared(pc, v)
            a = macro_auc_single(pc, v)
            row[f"{k}:eta2"] = e
            row[f"{k}:omega2"] = w
            row[f"{k}:auc"] = a
            s = max(0.0, w - floor_omega[k])  # omega^2 above floor = honest strength
            if s > best_strength:
                best_strength, best_attr = s, (k, "cat", w, a, e)
        for k, v in attrs_cont.items():
            mask = ~np.isnan(v)
            rho, _ = spearmanr(pc[mask], v[mask])
            rho = abs(float(rho))
            row[f"{k}:|rho|"] = rho
            s = max(0.0, rho - floor_cont[k])
            if s > best_strength:
                best_strength, best_attr = s, (k, "cont", rho, None, None)
        # label: dominant attr if omega2/|rho| clears 0.10 effect AND beats floor
        if best_attr is None or best_strength < 0.03:
            label = "entangled / none (omega^2 & |rho| at noise floor)"
        else:
            k, kind, eff, auc, eta = best_attr
            strong = eff >= 0.10
            tag = "" if strong else " (weak)"
            if kind == "cat":
                label = f"{k} (omega2={eff:.3f}, auc={auc:.3f}, eta2={eta:.2f}){tag}"
            else:
                label = f"{k} (|rho|={eff:.3f}){tag}"
        row["label"] = label
        results["matrix"][f"PC{i+1}"] = row
        results["labels"][f"PC{i+1}"] = label
        cat_e = " ".join(f"{k[:4]}[w{row[f'{k}:omega2']:.2f}/a{row[f'{k}:auc']:.2f}]" for k in attrs_cat)
        cont_r = " ".join(f"{k.replace('curriculum_','cur_').replace('vacuum_','')[:7]}={row[f'{k}:|rho|']:.2f}"
                          for k in attrs_cont)
        line = f"PC{i+1:<2d} evr={evr[i]:.3f} | {cat_e} | {cont_r} | -> {label}"
        print(line)
        rows_print.append(line)

    results["wall_s"] = time.time() - t0
    results["_matrix_text"] = rows_print
    return results


if __name__ == "__main__":
    out = run()
    outdir = os.path.join(HERE, "..", "_kosmos_axis_probe_out")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump({k: v for k, v in out.items() if k != "_matrix_text"},
                  f, ensure_ascii=False, indent=2)
    print(f"\n[done] wall={out['wall_s']:.1f}s -> results.json")
