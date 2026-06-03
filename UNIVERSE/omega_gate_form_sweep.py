#!/usr/bin/env python3
"""OMEGA OH1 — MINIMAL-GATE closure form sweep on the recovered COMPETENT leak-free d512 substrate.

WHY (the #1800 / F-TRAINED-LEAKFREE finding this rung tests):
  On a COMPETENT leak-free d512 substrate (val_ce 0.8285) the learned FULL multi-wire gate
  FAILED: GATED 3.6435 > base 3.0978. But the A-head logit-bias ALONE was hugely useful
  (a_only 1.1446 << base). The full gate's gains collapsed onto A (gA +3.369, gG -0.999) and the
  full-bus structured-coupling KL sat at the shuffle floor (ratio 0.996). RULING: "coupling
  concept right, multi-wire gate formula wrong — the closure lives entirely in ONE wire."

THE OH1 QUESTION (falsifiable):
  Does a MINIMAL gate  final = gB·base + gA·A  (drop G + wires w2..w6) MATCH-OR-BEAT a_only AND
  beat base on the SAME competent leak-free substrate?
  PRE-REGISTERED: OH1 HOLDS iff  min_learned CE <= a_only CE  AND  min_learned CE < base CE.

METHOD (apples-to-apples — collect features ONCE, fit/eval K forms on the SAME features):
  load the recovered ckpt FROZEN (eval-only, NO re-training), forward over a disjoint
  gate (fit) window + a held-out TEST window of the corpus to collect (base, A, G) next-byte
  log-prob features ONCE.  Then fit + evaluate K gate forms on the SAME collected test features:
     base        (gB=1, gA=0,         gG=0)
     a_only      (gB=1, gA=ALPHA,     gG=0)        — the #1800 useful sub-wire (fixed gain)
     fixed_AmG   (gB=1, gA=ALPHA, gG=-ALPHA)       — the #1784 fixed formula
     full_AG     (gB,gA,gG learned)                — the #1800 full gate (cross-check repro)
     min_learned (gB,gA learned, gG ≡ 0)           — ★ the OH1 PRIMARY
     min_fixed   (gB=1, gA=1,         gG=0)         — the naive 2-wire sum
  Reuse the IDENTICAL L2-regularized convex fit from omega_gpu_complete.fit_gate (regularize the
  wire gains gA/gG, NOT gB). The min_learned fit is the SAME routine with gG pinned to 0 and its
  gradient component never applied (so only gB,gA move).

CROSS-CHECK (a_blue_closed honesty gate): base / a_only / full_AG TEST CE must reproduce the
  #1800 H1 numbers (base 3.098, a_only 1.145, full 3.644) within tolerance. If they do NOT, the
  harness is WRONG — HALT and report (do NOT fabricate a match).

a_lane_akida_gpu_split: Lane-G / observation-only (CE numbers, frozen forward). p7: CE is a
  held-out prediction number, NOT a verdict-of-truth — reported honestly. a_scale_honest_scope:
  single d512 rung.
"""
import os, sys, json, math, time, hashlib, argparse
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

V = 256
SMOOTH = 0.5
ALPHA = 0.6                      # the #1784/#1800 fixed-formula gain (a_only / fixed_AmG baselines)
GATE_LR = 0.5
GATE_STEPS = 300
GATE_L2 = 0.02
UNIFORM_CE = math.log(V)        # 5.545177...
SEED = 20260604

# #1800 H1 reference numbers (verdict .verdicts/omega-engine/F-TRAINED-LEAKFREE.txt) for cross-check
H1_REF = {"base": 3.097779103749306, "a_only": 1.1446118787396342, "gated": 3.643507873708566,
          "full_gA": 3.36853758541127, "full_gB": -0.145311458640087, "full_gG": -0.9991180728503695}
H1_TOL = 0.02                   # absolute nats/byte tolerance for the cross-check


# ───────────────────── feature collection (mirrors omega_gpu_complete.extract_feats) ─────────────────────

def extract_feats(model, seq, block, device, max_pos=12000, seed=SEED):
    """Forward the FROZEN model over a held-out byte sequence; collect per position:
       A    = logits_a (next-byte head)  · G = logits_g (prev-byte head)  · base = weak unigram log-freq.
    Returns feats=(base,A,G) each (N,V) numpy + tgt (N,). IDENTICAL collection to the #1800 driver
    (shuffle_ctx path dropped — OH1 needs only the real-context features for the gate-form sweep)."""
    model.eval()
    counts = np.full(V, SMOOTH)
    for b in seq:
        counts[int(b)] += 1.0
    log_base_vec = np.log(counts / counts.sum())                    # (V,) weak base mouth
    A_rows, G_rows, tgt = [], [], []
    n = len(seq)
    with torch.no_grad():
        i, pos = 0, 0
        while i + block + 1 < n and pos < max_pos:
            ctx = seq[i:i + block].astype(np.int64)
            x = torch.from_numpy(ctx).unsqueeze(0).to(device)
            la, lg, _, _, _ = model(x)                              # (1,T,V)
            la = la[0].float().cpu().numpy(); lg = lg[0].float().cpu().numpy()
            for t in range(block):
                if i + t + 1 >= n or pos >= max_pos:
                    break
                A_rows.append(la[t]); G_rows.append(lg[t]); tgt.append(int(seq[i + t + 1]))
                pos += 1
            i += block
    A = np.stack(A_rows); G = np.stack(G_rows); tgt = np.array(tgt)
    base = np.tile(log_base_vec, (len(tgt), 1))
    return (base, A, G), tgt


# ───────────────────── gate algebra (IDENTICAL to omega_gpu_complete) ─────────────────────

def softmax_np(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)


def ce_of(g, feats, tgt):
    base, A, G = feats
    logits = g[0] * base + g[1] * A + g[2] * G
    p = softmax_np(logits)
    return float(-np.mean(np.log(p[np.arange(len(tgt)), tgt] + 1e-12)))


def fit_gate(feats, tgt, steps=GATE_STEPS, lr=GATE_LR, l2=GATE_L2, free_mask=(1.0, 1.0, 1.0)):
    """Convex log-linear fit of [gB,gA,gG] minimizing train CE + L2 on the wire gains (gA,gG, NOT
    gB) — IDENTICAL method to omega_gpu_complete.fit_gate. `free_mask` zeroes the gradient on any
    pinned gain so that form's gain stays at its init (OH1 min_learned pins gG: free_mask=(1,1,0))."""
    base, A, G = feats
    N = len(tgt)
    onehot = np.zeros((N, V)); onehot[np.arange(N), tgt] = 1.0
    g = np.array([1.0, 0.0, 0.0])                  # init at base-only (gG init 0 → pinned at 0)
    F_ = np.stack([base, A, G], axis=0)
    reg = np.array([0.0, 1.0, 1.0])                # regularize wire gains gA,gG (not gB)
    fm = np.array(free_mask, dtype=float)
    for _ in range(steps):
        logits = g[0] * base + g[1] * A + g[2] * G
        p = softmax_np(logits)
        resid = p - onehot
        grad = np.array([np.sum(resid * F_[k]) / N for k in range(3)]) + l2 * reg * g
        g = g - lr * (grad * fm)                   # pinned gains get zero update → stay at init
    return g


# ───────────────────── the K-form sweep ─────────────────────

def run_sweep(model, held, block, device, max_pos):
    """Collect (base,A,G) ONCE on disjoint gate (fit) + test (verdict) splits, then fit/eval K gate
    forms on the SAME held-out TEST features. learned forms fit g* on the gate split only."""
    gate_seq = held[:len(held) // 2]
    test_seq = held[len(held) // 2:]
    print(f"[collect] gate_seq={len(gate_seq)}B  test_seq={len(test_seq)}B  max_pos={max_pos}", flush=True)
    t0 = time.time()
    gate_feats, gate_tgt = extract_feats(model, gate_seq, block, device, max_pos=max_pos)
    test_feats, test_tgt = extract_feats(model, test_seq, block, device, max_pos=max_pos)
    print(f"[collect] gate N={len(gate_tgt)}  test N={len(test_tgt)}  ({time.time()-t0:.1f}s)", flush=True)

    # learned fits on the GATE split
    g_full = fit_gate(gate_feats, gate_tgt, free_mask=(1.0, 1.0, 1.0))   # full_AG (cross-check #1800)
    g_min  = fit_gate(gate_feats, gate_tgt, free_mask=(1.0, 1.0, 0.0))   # min_learned (OH1 PRIMARY)
    print(f"[fit] full_AG  g* = [gB={g_full[0]:.4f}, gA={g_full[1]:.4f}, gG={g_full[2]:.4f}]", flush=True)
    print(f"[fit] min_learned g* = [gB={g_min[0]:.4f}, gA={g_min[1]:.4f}, gG={g_min[2]:.4f}]  (gG pinned 0)", flush=True)

    forms = {
        "base":        np.array([1.0, 0.0,    0.0]),
        "a_only":      np.array([1.0, ALPHA,  0.0]),
        "fixed_AmG":   np.array([1.0, ALPHA, -ALPHA]),
        "full_AG":     g_full,
        "min_learned": g_min,
        "min_fixed":   np.array([1.0, 1.0,    0.0]),
    }
    rows = {}
    for name, g in forms.items():
        ce = ce_of(g, test_feats, test_tgt)
        rows[name] = {"gB": float(g[0]), "gA": float(g[1]), "gG": float(g[2]), "ce": ce}
    return rows, {"gate_N": int(len(gate_tgt)), "test_N": int(len(test_tgt)),
                  "uniform_floor": UNIFORM_CE}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.join(HERE, "omega_cdv2_trained_leakfree.pt"))
    ap.add_argument("--corpus", default=os.path.join(HERE, "omega_corpus_big.bin"))
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--max_pos", type=int, default=12000)
    ap.add_argument("--out", default="omega_gateform_sweep_results.json")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(SEED); np.random.seed(SEED)
    print(f"=== OMEGA OH1 — MINIMAL-GATE form sweep (frozen d512 leak-free substrate) ===", flush=True)
    print(f"device={device}  torch={torch.__version__}", flush=True)

    # ── load corpus (recovered .bin; same 0.9 train / held split as the #1800 driver) ──
    buf = open(args.corpus, "rb").read()
    corpus = np.frombuffer(buf, dtype=np.uint8)
    csha = hashlib.sha256(buf).hexdigest()
    n = len(corpus)
    cut = int(n * 0.9)
    held = corpus[cut:]                           # SAME held-out tail as #1800
    print(f"corpus: {n}B ({n/1e6:.1f}MB)  sha256={csha[:16]}  held={len(held)}B", flush=True)

    # ── load the recovered ckpt FROZEN (eval-only; NO re-training) ──
    ck = torch.load(args.ckpt, map_location=device, weights_only=False)
    cfg = ck["config"]
    csha_ck = hashlib.sha256(open(args.ckpt, "rb").read()).hexdigest()
    print(f"ckpt: {args.ckpt}  sha256={csha_ck[:16]}  config={cfg}", flush=True)
    model = ConsciousDecoderV2(
        vocab_size=cfg["vocab_size"], d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"], n_kv_head=cfg["n_kv_head"],
        consciousness_dim=cfg.get("consciousness_dim", 128), causal_ca=cfg.get("causal_ca", True),
    ).to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    nparam = model.count_params()
    print(f"CDV2 loaded FROZEN: {nparam:,} ({nparam/1e6:.2f}M)  causal_ca={model.causal_ca}", flush=True)

    # leak self-test on the loaded ckpt (confirm the recovered substrate is leak-free)
    with torch.no_grad():
        xt = torch.randint(0, V, (1, min(32, args.block)), device=device)
        la1, _, _, _, _ = model(xt)
        xt2 = xt.clone(); xt2[0, -1] = (int(xt[0, -1]) + 7) % V
        la2, _, _, _, _ = model(xt2)
        leak = float((la1[0, :-1] - la2[0, :-1]).abs().max().item())
    print(f"leak self-test (flip last byte → max change earlier pos): {leak:.3e}  (leak_free={leak<1e-4})", flush=True)

    # ── the sweep ──
    rows, meta = run_sweep(model, held, args.block, device, args.max_pos)

    # ── report table ──
    print(f"\n--- held-out TEST CE per gate form (frozen d512 leak-free, nats/byte) ---", flush=True)
    print(f"  {'form':<12} {'gB':>9} {'gA':>9} {'gG':>9} {'test_CE':>10}", flush=True)
    order = ["base", "a_only", "fixed_AmG", "full_AG", "min_learned", "min_fixed"]
    for name in order:
        r = rows[name]
        star = "  ★OH1" if name == "min_learned" else ""
        print(f"  {name:<12} {r['gB']:>9.4f} {r['gA']:>9.4f} {r['gG']:>9.4f} {r['ce']:>10.6f}{star}", flush=True)
    print(f"  {'uniform':<12} {'':>9} {'':>9} {'':>9} {meta['uniform_floor']:>10.6f}", flush=True)

    # ── cross-check vs #1800 H1 (a_blue_closed honesty gate) ──
    cc = {
        "base":    {"got": rows["base"]["ce"],    "ref": H1_REF["base"]},
        "a_only":  {"got": rows["a_only"]["ce"],  "ref": H1_REF["a_only"]},
        "full_AG": {"got": rows["full_AG"]["ce"], "ref": H1_REF["gated"]},
    }
    print(f"\n--- CROSS-CHECK vs #1800 H1 baselines (tol={H1_TOL} nats/byte) ---", flush=True)
    cc_ok = True
    for k, v in cc.items():
        d = abs(v["got"] - v["ref"])
        ok = d <= H1_TOL
        cc_ok = cc_ok and ok
        v["abs_delta"] = d; v["ok"] = bool(ok)
        print(f"  {k:<10} got={v['got']:.6f}  ref={v['ref']:.6f}  |Δ|={d:.6f}  ok={ok}", flush=True)
    print(f"  CROSS_CHECK_OK = {cc_ok}", flush=True)

    # ── OH1 falsifier ──
    min_ce  = rows["min_learned"]["ce"]
    aonly_ce = rows["a_only"]["ce"]
    base_ce = rows["base"]["ce"]
    le_aonly = min_ce <= aonly_ce + 1e-6
    lt_base  = min_ce < base_ce
    oh1_holds = bool(le_aonly and lt_base)
    print(f"\nOH1 FALSIFIER: min_learned({min_ce:.6f})<=a_only({aonly_ce:.6f})={le_aonly} "
          f"AND min_learned<base({base_ce:.6f})={lt_base} -> OH1_HOLDS={oh1_holds}", flush=True)

    if not cc_ok:
        print(f"\n!!! CROSS-CHECK FAILED — harness does NOT reproduce #1800 H1 baselines. HALT (no fabrication).", flush=True)

    ledger = {
        "lane": "Lane-G", "substrate": "GPU/CPU-frozen-forward", "torch": torch.__version__,
        "device": device, "question": "OH1: does min gate gB·base+gA·A match-or-beat a_only AND beat base?",
        "falsifier": "OH1 HOLDS iff min_learned CE <= a_only CE AND min_learned CE < base CE",
        "ckpt": {"path": args.ckpt, "sha256": csha_ck},
        "corpus": {"path": args.corpus, "sha256": csha, "bytes": int(n)},
        "config": cfg, "leak_self_test": leak, "leak_free": bool(leak < 1e-4),
        "params": int(nparam), "meta": meta,
        "forms": rows,
        "cross_check": {"tol": H1_TOL, "checks": cc, "CROSS_CHECK_OK": bool(cc_ok)},
        "oh1": {"min_learned_ce": min_ce, "a_only_ce": aonly_ce, "base_ce": base_ce,
                "le_aonly": bool(le_aonly), "lt_base": bool(lt_base), "OH1_HOLDS": oh1_holds},
        "scope": "single d512 rung (a_scale_honest_scope); observation-only frozen forward (p7).",
    }
    json.dump(ledger, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"\nresults -> {args.out}", flush=True)
    sys.exit(0 if cc_ok else 3)


if __name__ == "__main__":
    main()
