#!/usr/bin/env python3
"""retro303m_en_train.py — train anima-303M-RETRO from scratch (H_1129 303M ByteGPT backbone
+ the H_1147 RETRO copy/cross-attention head over a PRIOR-WINDOW retrieved-anchor stream),
coherence-first, scoring a303m_pass G0/G1/G2 with the FROZEN H_1129 evaluators + a G5
non-fabrication probe.

MODEL.md BUILD ORDER step 2. Lane-G torch REFERENCE mouth (a_clm_gen_pipeline). seed 7, p7
deterministic (NOT perplexity). nohup-detached (survives SSH drop); one ledger JSONL row per
eval (crash-recovery). The RECIPE (dropout/wd/lr/warmup) is read from the ByteGPT sweep winner
ledger (best G0/G1/G2) OR passed explicitly via --dropout/--wd/--lr/--warmup.

ANCHOR SOURCE (--anchor, default=semantic):
  semantic (v2, H_1148 🟢) = byte-trigram TF-cosine retrieval over a RING of recent prior
    windows; the anchor for a target span is the MOST content-similar prior window (not the
    fixed positional one). H_1148 proved the RETRO copy head is RETRIEVAL-limited not capacity-
    limited (copy-acc 0.218 prior-window -> 1.000 semantic = oracle). Index-free, $0, gap=64
    causal no-leak, NO external RAG (a_kosmos). This is the PRIMARY RETRO-303M run.
  prior_window (v1 baseline) = the preceding [i-La-gap : i-gap] window picked by POSITION; kept
    as the labelled BASELINE arm for an honest G5 A/B (a_completeness_over_cheap).
At inference both reduce to the retrieved KOSMOS anchor via generator_read_anchors (kosmos_io->
brain, single-entry a_core_engine_map) scored by the SAME byte-trigram cosine.
"""
from __future__ import annotations
import argparse, json, math, os, sys, time

THIS = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.normpath(os.path.join(THIS, "..", "model"))
sys.path.insert(0, MODEL_DIR)
import retro303m_en as R  # noqa: E402
import torch  # noqa: E402


def pick_winner(sweep_ledger):
    """Read the ByteGPT sweep winner from state/sweep_303m_en/ledger.jsonl — the status=done
    config with the best (G0_pass, G1, G2, lowest val). Returns (cfg_label, axes) or None."""
    best = None
    if not os.path.exists(sweep_ledger):
        return None
    for l in open(sweep_ledger):
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("status") != "done":
            continue
        g0 = r.get("G0_kwr") or 0.0
        g1 = 1 if (r.get("G1") or {}).get("emergent") else 0
        g2 = 1 if (r.get("G2") or {}).get("pass") else 0
        val = r.get("val") if r.get("val") is not None else 1e9
        # rank: maximize (g0>=0.5, g1, g2), then minimize val
        key = (int(g0 >= 0.50), g1, g2, -val)
        if best is None or key > best[0]:
            best = (key, r.get("config"), r.get("axes", {}))
    if best is None:
        return None
    return best[1], best[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--sweep_universe", required=True,
                    help="dir with h1129_midcap_broad_converged_recombination.py")
    ap.add_argument("--cfg", default="retro303m_en")
    ap.add_argument("--host", default="aiden")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--sweep_ledger", default=None,
                    help="ByteGPT sweep ledger to read the winning recipe from")
    # H_1129 base arch (frozen)
    ap.add_argument("--d", type=int, default=1024)
    ap.add_argument("--n_layer", type=int, default=24)
    ap.add_argument("--n_head", type=int, default=16)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=12000)
    # RETRO anchor
    ap.add_argument("--anchor_len", type=int, default=256)
    ap.add_argument("--anchor_gap", type=int, default=64)
    # anchor SOURCE: semantic (H_1148 v2, default) | prior_window (v1 baseline arm, honest A/B)
    ap.add_argument("--anchor", choices=["semantic", "prior_window"], default="semantic",
                    help="anchor retrieval policy: semantic=byte-trigram cosine over a ring of "
                         "recent prior windows (H_1148 v2 GREEN); prior_window=v1 positional baseline")
    ap.add_argument("--anchor_ring", type=int, default=8,
                    help="semantic: # of recent prior windows scored per target (ring size)")
    ap.add_argument("--anchor_qhead", type=int, default=64,
                    help="semantic: leading query bytes used to build the retrieval profile")
    # recipe (overridden by sweep winner unless given)
    ap.add_argument("--dropout", type=float, default=None)
    ap.add_argument("--weight_decay", type=float, default=None)
    ap.add_argument("--lr", type=float, default=None)
    ap.add_argument("--warmup", type=int, default=None)
    ap.add_argument("--grad_ckpt", action="store_true")
    ap.add_argument("--eval_every", type=int, default=500)
    a = ap.parse_args()

    H = R._import_h1129(a.sweep_universe)

    # resolve recipe: explicit flags > sweep winner > H_1129 reference defaults
    win = pick_winner(a.sweep_ledger) if a.sweep_ledger else None
    rec = {"dropout": 0.0, "weight_decay": 0.1, "lr": 3e-4, "warmup": 300}
    win_cfg = None
    if win:
        win_cfg, win_axes = win
        for k in ("dropout", "weight_decay", "lr", "warmup"):
            if k in win_axes and win_axes[k] is not None:
                rec[k] = win_axes[k]
    if a.dropout is not None: rec["dropout"] = a.dropout
    if a.weight_decay is not None: rec["weight_decay"] = a.weight_decay
    if a.lr is not None: rec["lr"] = a.lr
    if a.warmup is not None: rec["warmup"] = a.warmup

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    if dev == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)}", flush=True)
    print(f"[recipe] winner_cfg={win_cfg} -> {rec}", flush=True)

    data = H.load_bytes(a.corpus)
    n = data.numel(); ntr = int(n * 0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] {a.corpus} total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB",
          flush=True)

    # anchor SOURCE dispatch (H_1148 v2): semantic byte-trigram-cosine retrieval (default)
    # vs the v1 prior-window positional baseline. SAME (x,y) target stream + SAME La/gap; only
    # WHICH window fills the anchor slot changes (cf a_completeness_over_cheap honest A/B).
    if a.anchor == "semantic":
        print(f"[anchor] SEMANTIC (H_1148 v2) ring={a.anchor_ring} qhead={a.anchor_qhead} "
              f"gap={a.anchor_gap} — byte-trigram cosine over recent prior windows", flush=True)
        def anchor_batch(d):
            return R.semantic_anchor_batch(d, a.block, a.anchor_len, a.anchor_gap, a.bs, dev,
                                           ring=a.anchor_ring, q_head=a.anchor_qhead)
        anchor_source_tag = "semantic_byte_trigram_cosine_v2"
    else:
        print(f"[anchor] PRIOR_WINDOW (v1 baseline) gap={a.anchor_gap} — positional surrogate",
              flush=True)
        def anchor_batch(d):
            return R.prior_window_batch(d, a.block, a.anchor_len, a.anchor_gap, a.bs, dev)
        anchor_source_tag = "prior_window_self_retrieval"

    m = R.RetroByteGPT(H, d=a.d, n_layer=a.n_layer, n_head=a.n_head, block=a.block,
                       p=rec["dropout"], grad_ckpt=a.grad_ckpt).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    nback = sum(p.numel() for p in m.backbone.parameters())
    nextra = m.n_extra_params()
    print(f"[model] anima-303M-RETRO PARAM COUNT = {nparam:,} ({nparam/1e6:.1f}M) "
          f"= backbone {nback:,} + retro {nextra:,}", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=rec["lr"], betas=(0.9, 0.95),
                            weight_decay=rec["weight_decay"])

    # OOM-guard fit probe (one fwd+bwd with anchor at full batch)
    m.train()
    x, y, anc, amask = anchor_batch(tr)
    if dev == "cuda":
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            _, loss = m(x, anc, targets=y, anchor_mask=amask)
    else:
        _, loss = m(x, anc, targets=y, anchor_mask=amask)
    loss.backward(); opt.zero_grad(set_to_none=True)
    if dev == "cuda":
        print(f"[fit] OK peak={torch.cuda.max_memory_allocated()/1e9:.2f}GB / 12GB", flush=True)
        torch.cuda.reset_peak_memory_stats()

    @torch.no_grad()
    def eval_ce(d, iters=30):
        m.eval(); tot = 0.0
        for _ in range(iters):
            x, y, anc, amask = anchor_batch(d)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, l = m(x, anc, targets=y, anchor_mask=amask)
            else:
                _, l = m(x, anc, targets=y, anchor_mask=amask)
            tot += l.item()
        m.train(); return tot / iters

    os.makedirs(os.path.dirname(a.ledger), exist_ok=True)

    def ledger_row(status, step, vce, g0=None, g1=None, g2=None, g5=None):
        val = round(vce, 4) if vce != float("inf") else None
        row = {"config": a.cfg, "host": a.host, "step": step, "val": val,
               "G0_kwr": (round(g0, 3) if g0 is not None else None),
               "G1": g1, "G2": g2, "G5": g5, "status": status, "ckpt_path": a.ckpt,
               "nparam": nparam, "nparam_backbone": nback, "nparam_retro": nextra,
               "winner_cfg": win_cfg, "anchor_source": anchor_source_tag,
               "anchor_policy": a.anchor,
               "axes": {**rec, "steps": a.steps, "anchor_len": a.anchor_len,
                        "anchor_gap": a.anchor_gap, "anchor_ring": a.anchor_ring,
                        "anchor_qhead": a.anchor_qhead},
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(a.ledger, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    ledger_row("started", 0, float("inf"))
    print(f"\n[train] {a.steps} steps bs={a.bs} accum={a.accum} anchor_len={a.anchor_len} "
          f"gap={a.anchor_gap}", flush=True)
    best_val = float("inf"); t0 = time.time(); m.train()
    for st in range(a.steps):
        if st < rec["warmup"]:
            lr_t = rec["lr"] * (st + 1) / rec["warmup"]
        else:
            prog = min(1.0, (st - rec["warmup"]) / max(1, a.steps - rec["warmup"]))
            lr_t = rec["lr"] * 0.5 * (1 + math.cos(math.pi * prog))
        for g in opt.param_groups:
            g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y, anc, amask = anchor_batch(tr)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, loss = m(x, anc, targets=y, anchor_mask=amask)
            else:
                _, loss = m(x, anc, targets=y, anchor_mask=amask)
            (loss / a.accum).backward(); acc_loss += loss.item() / a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % a.eval_every == 0 or st == a.steps - 1:
            vce = eval_ce(va); dt = time.time() - t0
            print(f"  step {st:5d} train_ce={acc_loss:.4f} val_ce={vce:.4f} lr={lr_t:.2e} {dt/60:.1f}min",
                  flush=True)
            if vce < best_val:
                best_val = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab": 256, "d": a.d, "n_layer": a.n_layer,
                                       "n_head": a.n_head, "block": a.block,
                                       "anchor_len": a.anchor_len, "anchor_gap": a.anchor_gap,
                                       "retro": True},
                            "val_ce": vce, "step": st, "nparam": nparam,
                            "recipe": rec, "winner_cfg": win_cfg}, a.ckpt)
            ledger_row("training", st, vce)
    print(f"[train] done best_val_ce={best_val:.4f} ckpt={a.ckpt} wall={(time.time()-t0)/60:.1f}min",
          flush=True)

    # ── reload best, run the FROZEN H_1129 evaluators (anchor-fallback gen) + G5 fab probe ──
    ck = torch.load(a.ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"]); m.backbone.grad_ckpt = False; m.eval()
    print(f"[ladder] best ckpt step={ck['step']} val_ce={ck['val_ce']:.4f}", flush=True)

    @torch.no_grad()
    def retro_gen(seed, mx, anchor_bytes=None):
        idx = torch.tensor([list(seed.encode("utf-8"))[-a.block:]], dtype=torch.long, device=dev)
        if anchor_bytes is None:
            anc = torch.full((1, a.anchor_len), 32, dtype=torch.long, device=dev)
            amask = torch.zeros(1, a.anchor_len, dtype=torch.long, device=dev)  # vocab fallback
        else:
            ab = list(anchor_bytes.encode("utf-8"))[-a.anchor_len:]
            pad = a.anchor_len - len(ab)
            anc = torch.tensor([[32] * pad + ab], dtype=torch.long, device=dev)
            amask = torch.tensor([[0] * pad + [1] * len(ab)], dtype=torch.long, device=dev)
        out = []
        for _ in range(mx):
            ctx = idx[:, -a.block:]
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    probs, _ = m(ctx, anc, anchor_mask=amask)
            else:
                probs, _ = m(ctx, anc, anchor_mask=amask)
            nb = int(probs[0, -1].argmax().item()); out.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        return bytes(out).decode("utf-8", "ignore").strip()

    # G0
    single_gens = [retro_gen(f"{c}. ", 80) for c, _ in H.CONCEPTS]
    g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)
    g0_pass = g0_kwr >= 0.50
    for i, (c, _) in enumerate(H.CONCEPTS):
        print(f"  [G0 {i}] kwr={H.known_word_ratio(single_gens[i]):.2f} :: {single_gens[i][:90]}",
              flush=True)

    # G1 recombination ladder (anchor-fallback gen; uses H_1129 coverage machinery)
    max_single = max(len(H.coverage(g)) for g in single_gens)
    g1_emergent = False; ladder = {}
    for k in (2, 3, 4, 5):
        seed = ". ".join(c for c, _ in H.CONCEPTS[:k]) + ". "
        o = retro_gen(seed, 120)
        cc = H.coverage(o); kwr = H.known_word_ratio(o); coh = kwr >= 0.50
        clears = (len(cc) >= 2 and len(cc) > max_single and coh)
        g1_emergent = g1_emergent or clears
        ladder[k] = {"composed_distinct": len(cc), "kwr": round(kwr, 3), "clears": clears,
                     "text": o}
        print(f"  [G1 k={k}] cd={len(cc)} kwr={kwr:.2f} clears={clears} :: {o[:120]}", flush=True)

    # G2 novelty
    corpus_text = bytes(data[: min(data.numel(), 40 * 1024 * 1024)].tolist()).decode("utf-8", "ignore")

    def novelty_count(gens, n=4):
        cg = set(); cw = H.words(corpus_text)
        for i in range(len(cw) - n + 1):
            cg.add(tuple(cw[i:i + n]))
        novel = 0; seen = set()
        for g in gens:
            gw = H.words(g)
            for i in range(len(gw) - n + 1):
                gram = tuple(gw[i:i + n])
                if gram in seen: continue
                seen.add(gram)
                if not all(w in H.KNOWN for w in gram): continue
                if gram not in cg: novel += 1
        return novel
    comp_gens = [ladder[k]["text"] for k in (2, 3, 4, 5)]
    g2_novel = novelty_count(comp_gens)
    g2_ctrl = novelty_count([corpus_text[:400]])
    g2_pass = (g2_novel >= 3 and g2_ctrl == 0)

    # G5 NON-FABRICATION probe (the RETRO axis): held-out must-copy entities via the anchor.
    #   Build (query, anchor) pairs whose answer entity is a rare token present ONLY in the
    #   anchor; with anchor present the trained copy head should emit it (low fab); with the
    #   anchor MASKED it must collapse (control). Reuses the H_1147 fab-rate metric idea.
    @torch.no_grad()
    def g5_fab(masked=False, trials=40):
        fab = 0; rng = torch.Generator().manual_seed(7)
        for _ in range(trials):
            E = int(torch.randint(65, 90, (1,), generator=rng).item())
            ab = [32] * (a.anchor_len)
            ab[a.anchor_len // 2] = E
            anc = torch.tensor([ab], dtype=torch.long, device=dev)
            amask = (torch.zeros if masked else torch.ones)(1, a.anchor_len, dtype=torch.long,
                                                            device=dev)
            q = torch.tensor([[ord("?")] * a.block], dtype=torch.long, device=dev)
            probs, _ = m(q, anc, anchor_mask=amask)
            pred = int(probs[0, -1].argmax().item())
            fab += int(pred != E)
        return fab / trials
    g5_present = g5_fab(masked=False)
    g5_masked = g5_fab(masked=True)
    g5_l1_pass = g5_present <= 0.30
    g5_l2_pass = g5_present <= 0.20
    g5_grounds = (g5_masked - g5_present) >= 0.40  # copies only with anchor present

    print("\n=== a303m_pass SCORES (frozen p7) ===", flush=True)
    print(f"  G0_kwr={g0_kwr:.3f} pass={g0_pass}", flush=True)
    print(f"  G1 emergent={g1_emergent}", flush=True)
    print(f"  G2 novel={g2_novel} ctrl={g2_ctrl} pass={g2_pass}", flush=True)
    print(f"  G5 fab(anchor)={g5_present:.3f} fab(masked)={g5_masked:.3f} "
          f"L1<=0.30={g5_l1_pass} L2<=0.20={g5_l2_pass} grounds={g5_grounds}", flush=True)

    g5 = {"fab_anchor": g5_present, "fab_masked": g5_masked,
          "L1_pass": g5_l1_pass, "L2_pass": g5_l2_pass, "grounds": g5_grounds}
    ledger_row("done", ck["step"], best_val, g0=g0_kwr,
               g1={"emergent": g1_emergent, "max_single": max_single,
                   "ladder": {k: {"composed_distinct": ladder[k]["composed_distinct"],
                                  "kwr": ladder[k]["kwr"], "clears": ladder[k]["clears"]}
                              for k in (2, 3, 4, 5)}},
               g2={"novel": g2_novel, "control": g2_ctrl, "pass": g2_pass}, g5=g5)
    json.dump({"config": a.cfg, "nparam": nparam, "nparam_backbone": nback, "nparam_retro": nextra,
               "best_val_ce": best_val, "G0_kwr": g0_kwr, "G0_pass": g0_pass,
               "G1_emergent": g1_emergent, "G2_novel": g2_novel, "G2_pass": g2_pass,
               "G5": g5, "winner_cfg": win_cfg, "recipe": rec,
               "anchor_source": anchor_source_tag, "anchor_policy": a.anchor},
              open(a.ckpt + ".result.json", "w"), ensure_ascii=False, indent=2)
    print(f"[done] {a.ckpt}.result.json", flush=True)


if __name__ == "__main__":
    main()
