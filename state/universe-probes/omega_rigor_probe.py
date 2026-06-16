#!/usr/bin/env python3
"""OMEGA OΩ-RIGOR — the completeness RIGOR pass (OΩ1 + OΩ2 + OΩ3) on the recovered FROZEN d512
leak-free substrate. Reuses the OH1 (omega_gate_form_sweep.py) loader + gate algebra VERBATIM;
adds three honesty probes on the SAME frozen ckpt, fixed seed, held-out TEST window.

  OΩ1 — COUPLING vs REPLACEMENT (the sharp honesty probe).
        OH1's min_learned landed [gB≈0.040, gA≈0.901] (base nearly zeroed). Is the closure REAL
        coupling (base mouth + substrate steer) or substrate-head REPLACEMENT? Measure on TEST:
          (a) A-STANDALONE CE  = CE of softmax(A logits) alone, g=[0,1,0]  (no base at all).
          (b) base-only CE     = g=[1,0,0]   (ref 3.0978).
          (c) min_learned CE   = gB·base + gA·A   (the OH1 closure, refit here).
          (d) base-ABLATED min = gB→0 in the min_learned form (keep gA·A; drop the base term).
        PRE-REGISTERED ruling: if A-standalone ≈ min_learned (|Δ| small) AND ablating base (gB→0)
        barely moves CE, the honest verdict is REPLACEMENT — the trained A-head SUPPLANTS the .clm
        mouth, NOT a base+steer coupling. Report it that way; do NOT spin REPLACEMENT as coupling.

  OΩ2 — PER-WIRE AUTOPSY on the trained substrate. H1 measured the LUMPED gate. Here each
        coupling-bus wire is added to base INDIVIDUALLY → held-out CE vs base, applied per its REAL
        coupling_bus.hexa semantics:
          w1 A⇄G    : base + α·(A − G)                          [clean logit-add; isolatable]
          w2 W→temp : base * 1/(1 + β·w_tension)                [multiplicative; real per-pos tension]
          w3 curio  : base + c·curiosity·(±1 by parity)         [parity bias; NO substrate curiosity]
          w4 Ψ      : base + p·psi8[i mod 8]                     [needs per-pos 8D Ψ — NOT emitted]
          w5 module : base + r·module_act[i mod M]              [needs MoE router — use_moe=False]
          w6 dF/dt  : base + dg·((A−G)_t − (A−G)_{t-1})         [derivative across adjacent pos]
        Where a wire has NO genuine frozen-inference substrate source (w3 curiosity scalar, w4 8D Ψ,
        w5 MoE routing — this ckpt is SwiGLU trunk, use_moe=False), it is an HONEST STUB: reported
        as "no substrate signal at frozen inference" with NO fabricated CE (a_core_engine_map).

  OΩ3 — GEN COHERENCE under the min-gate. H1 free-run gen was degenerate repetition. Does the
        min-gate (gB·base + gA·A) fix it? Free-run generate under min-gate vs base vs full-gate;
        report entropy / distinct_frac / ws_frac / a sample. Gen coherence is the WEAK criterion (p7).

a_lane_akida_gpu_split: Lane-G / observation-only (CE = held-out number, NOT verdict-of-truth, p7).
a_scale_honest_scope: single d512 rung. NO re-training (frozen forward). NO fabrication.
"""
import os, sys, json, math, time, hashlib, argparse
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

V = 256
SMOOTH = 0.5
ALPHA = 0.6                      # the #1784/#1800 fixed-formula gain (bus w1 default)
BETA = 0.5                       # bus w2 tension→temp gain (coupling_bus omega_bus_on)
C_CURIO = 0.15                   # bus w3 curiosity gain
P_PSI = 0.4                      # bus w4 Ψ gain
R_MOD = 0.3                      # bus w5 module gain
DGAIN = 0.5                      # bus w6 dF/dt ABLATION seed (fixed dgain HURTS, #1794 — honest)
GATE_LR = 0.5
GATE_STEPS = 300
GATE_L2 = 0.02
UNIFORM_CE = math.log(V)        # 5.545177...
SEED = 20260604

# #1800 H1 reference (cross-check the loader reproduces the same frozen substrate)
H1_REF = {"base": 3.097779103749306, "a_only": 1.1446118787396342, "gated": 3.643507873708566}
H1_TOL = 0.02


def softmax_np(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)


def ce_logits(logits, tgt):
    p = softmax_np(logits)
    return float(-np.mean(np.log(p[np.arange(len(tgt)), tgt] + 1e-12)))


def ce_of(g, feats, tgt):
    base, A, G = feats
    return ce_logits(g[0] * base + g[1] * A + g[2] * G, tgt)


def fit_gate(feats, tgt, steps=GATE_STEPS, lr=GATE_LR, l2=GATE_L2, free_mask=(1.0, 1.0, 1.0)):
    """IDENTICAL convex log-linear fit to omega_gate_form_sweep.fit_gate (L2 on wire gains gA,gG)."""
    base, A, G = feats
    N = len(tgt)
    onehot = np.zeros((N, V)); onehot[np.arange(N), tgt] = 1.0
    g = np.array([1.0, 0.0, 0.0])
    F_ = np.stack([base, A, G], axis=0)
    reg = np.array([0.0, 1.0, 1.0])
    fm = np.array(free_mask, dtype=float)
    for _ in range(steps):
        logits = g[0] * base + g[1] * A + g[2] * G
        p = softmax_np(logits)
        resid = p - onehot
        grad = np.array([np.sum(resid * F_[k]) / N for k in range(3)]) + l2 * reg * g
        g = g - lr * (grad * fm)
    return g


# ───────────────────── feature collection (mirrors OH1 extract_feats + per-pos tension) ─────────────────────

def extract_feats(model, seq, block, device, max_pos=12000):
    """Forward the FROZEN model over a held-out byte sequence; collect per position:
       A = logits_a, G = logits_g, base = weak unigram log-freq, tension = mean per-layer tension.
    Returns feats=(base,A,G) each (N,V) + tgt (N,) + tens (N,) per-position mean tension (for w2)."""
    model.eval()
    counts = np.full(V, SMOOTH)
    for b in seq:
        counts[int(b)] += 1.0
    log_base_vec = np.log(counts / counts.sum())
    A_rows, G_rows, tgt, tens = [], [], [], []
    n = len(seq)
    with torch.no_grad():
        i, pos = 0, 0
        while i + block + 1 < n and pos < max_pos:
            ctx = seq[i:i + block].astype(np.int64)
            x = torch.from_numpy(ctx).unsqueeze(0).to(device)
            la, lg, tensions, _, _ = model(x)              # tensions = list of (1,T) per layer
            la = la[0].float().cpu().numpy(); lg = lg[0].float().cpu().numpy()
            # mean per-position tension across layers (the real W signal for w2)
            t_stack = torch.stack(tensions, dim=0)[:, 0, :].float().cpu().numpy()  # (L,T)
            t_pos = t_stack.mean(axis=0)                                            # (T,)
            for t in range(block):
                if i + t + 1 >= n or pos >= max_pos:
                    break
                A_rows.append(la[t]); G_rows.append(lg[t]); tgt.append(int(seq[i + t + 1]))
                tens.append(float(t_pos[t]))
                pos += 1
            i += block
    A = np.stack(A_rows); G = np.stack(G_rows); tgt = np.array(tgt); tens = np.array(tens)
    base = np.tile(log_base_vec, (len(tgt), 1))
    return (base, A, G), tgt, tens, log_base_vec


# ───────────────────── OΩ1 — coupling vs replacement ─────────────────────

def probe_oo1(gate_feats, gate_tgt, test_feats, test_tgt):
    base, A, G = test_feats
    g_min = fit_gate(gate_feats, gate_tgt, free_mask=(1.0, 1.0, 0.0))   # OH1 min_learned (gG pinned 0)
    ce_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    ce_astand = ce_logits(A.copy(), test_tgt)                            # A-STANDALONE (no base)
    ce_min = ce_of(g_min, test_feats, test_tgt)                         # gB·base + gA·A
    # base-ABLATED min: drop the base term (gB→0), keep the learned gA on A
    ce_min_noB = ce_of(np.array([0.0, g_min[1], 0.0]), test_feats, test_tgt)
    d_astand_min = abs(ce_astand - ce_min)
    d_ablate = abs(ce_min_noB - ce_min)                                 # how much base contributes
    # PRE-REGISTERED replacement criterion: A-standalone ≈ min_learned AND removing base ≈ no-op.
    # thresholds: both deltas small relative to the base→min gap (the coupling would have to MOVE CE).
    coupling_gain = ce_base - ce_min                                    # how far min beats base
    REPL_TOL = 0.05                                                     # nats/byte "≈" tolerance
    astand_eq_min = d_astand_min <= REPL_TOL
    base_is_inert = d_ablate <= REPL_TOL
    replacement = bool(astand_eq_min and base_is_inert)
    return {
        "g_min": [float(x) for x in g_min],
        "ce_base": ce_base, "ce_a_standalone": ce_astand, "ce_min_learned": ce_min,
        "ce_min_base_ablated": ce_min_noB,
        "delta_astandalone_vs_min": d_astand_min, "delta_base_ablation": d_ablate,
        "coupling_gain_base_minus_min": coupling_gain, "repl_tol": REPL_TOL,
        "astandalone_eq_min": bool(astand_eq_min), "base_is_inert": bool(base_is_inert),
        "RULING_REPLACEMENT": replacement,
        "ruling_text": ("REPLACEMENT — the trained A-head SUPPLANTS the .clm base mouth (A-standalone"
                        " ≈ min_learned AND base term is inert)" if replacement else
                        "COUPLING — base term materially contributes to min_learned CE (not pure"
                        " A-head replacement)"),
    }


# ───────────────────── OΩ2 — per-wire autopsy ─────────────────────

def probe_oo2(test_feats, test_tgt, test_tens):
    base, A, G = test_feats
    ce_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    wires = {}

    # w1 A⇄G : base + α·(A − G)  — clean logit-add, isolatable
    ce_w1 = ce_logits(base + ALPHA * (A - G), test_tgt)
    wires["w1_AmG"] = {"isolatable": True, "ce": ce_w1, "delta_vs_base": ce_w1 - ce_base,
                       "semantics": "base + alpha*(A-G), alpha=%.2f" % ALPHA}

    # w2 W→temp : base * 1/(1 + β·w_tension)  — multiplicative, real per-position tension
    tfac = 1.0 / (1.0 + BETA * test_tens)                 # (N,)
    ce_w2 = ce_logits(base * tfac[:, None], test_tgt)
    wires["w2_Wtemp"] = {"isolatable": True, "ce": ce_w2, "delta_vs_base": ce_w2 - ce_base,
                         "semantics": "base * 1/(1+beta*tension), beta=%.2f; tension=mean per-layer "
                                      "PureField tension (real substrate W signal)" % BETA,
                         "tension_stats": {"mean": float(test_tens.mean()),
                                           "std": float(test_tens.std()),
                                           "min": float(test_tens.min()),
                                           "max": float(test_tens.max())}}

    # w3 curio : base + c·curiosity·(±1 by parity) — NO substrate curiosity scalar at frozen inference.
    # The E-ratchet / curiosity signal is a runtime daemon state, not emitted by the frozen forward.
    # coupling_bus.hexa itself notes w3 is structureless (parity bias, |gain|<TAU). HONEST STUB.
    wires["w3_curio"] = {"isolatable": False, "ce": None, "delta_vs_base": None,
                         "stub_reason": "no substrate curiosity scalar at frozen inference (E-ratchet "
                                        "is a runtime daemon state, not emitted by the forward); the "
                                        "bus w3 is a fixed parity bias (structureless by construction, "
                                        "coupling_bus.hexa: |gain|<TAU). Not a substrate-derived CE delta."}

    # w4 Ψ : base + p·psi8[i mod 8] — needs a per-position 8D Ψ coord; the model emits only a scalar
    # _psi_residual updated ONLY in training mode (self.training). At frozen eval there is NO per-pos
    # 8D Ψ vector. (#1793/#1794 found toy psi8 INERT; F-REAL-PSI BLOCKED-DATA.) HONEST STUB.
    wires["w4_psi"] = {"isolatable": False, "ce": None, "delta_vs_base": None,
                       "stub_reason": "no per-position 8D Psi vector at frozen inference; the model "
                                      "emits only a scalar _psi_residual updated under self.training "
                                      "(eval=frozen -> no Psi8). #1793/#1794: toy psi8 INERT; "
                                      "F-REAL-PSI BLOCKED-DATA. Not a substrate-derived CE delta."}

    # w5 module : base + r·module_act[i mod M] — needs the MoE router per-position expert probs.
    # THIS ckpt config has NO use_moe (SwiGLU trunk), so there is NO router activation vector.
    # HONEST STUB (a_core_engine_map: no phantom wiring).
    wires["w5_module"] = {"isolatable": False, "ce": None, "delta_vs_base": None,
                          "stub_reason": "this d512 ckpt trunk is SwiGLU (use_moe=False) -> no MoE "
                                         "router expert-prob vector exists; module_act has no substrate "
                                         "source. Not a substrate-derived CE delta on this ckpt."}

    # w6 dF/dt : base + dg·((A−G)_t − (A−G)_{t-1}) — derivative of the A⇄G coupling across adjacent
    # positions. Isolatable as a CE delta (the first position has no predecessor → dF=0 there).
    dF = (A - G).copy()
    dF[1:] = (A - G)[1:] - (A - G)[:-1]
    dF[0] = 0.0
    ce_w6 = ce_logits(base + DGAIN * dF, test_tgt)
    wires["w6_dFdt"] = {"isolatable": True, "ce": ce_w6, "delta_vs_base": ce_w6 - ce_base,
                        "semantics": "base + dgain*((A-G)_t-(A-G)_{t-1}), dgain=%.2f (FIXED dgain seed; "
                                     "fixed dgain HURTS per #1794 — reported honestly, not a tuned "
                                     "carrier)" % DGAIN}
    return {"ce_base": ce_base, "wires": wires}


# ───────────────────── OΩ3 — gen coherence under min-gate ─────────────────────

def gen_stats(byts):
    """entropy (nats over byte hist) · distinct_frac · ws_frac over the NEW bytes."""
    arr = np.frombuffer(byts, dtype=np.uint8)
    if len(arr) == 0:
        return {"entropy": 0.0, "distinct_frac": 0.0, "ws_frac": 0.0, "n": 0}
    hist = np.bincount(arr, minlength=256).astype(np.float64)
    p = hist / hist.sum(); p = p[p > 0]
    ent = float(-(p * np.log(p)).sum())
    distinct = float(len(np.unique(arr)) / len(arr))
    ws = float(np.mean([1.0 if c in (32, 9, 10, 13) else 0.0 for c in arr]))
    return {"entropy": ent, "distinct_frac": distinct, "ws_frac": ws, "n": int(len(arr))}


def gen_freerun(model, prompt_bytes, n_new, device, g_star, log_base_vec, mode,
                temperature=0.85, top_k=40):
    """Free-run decode n_new bytes. mode='base' (weak unigram only), 'min'/'full' (gB·base+gA·A[+gG·G])."""
    model.eval()
    log_base = torch.from_numpy(log_base_vec.astype(np.float32)).to(device)
    idx = torch.from_numpy(np.frombuffer(prompt_bytes, dtype=np.uint8).astype(np.int64)).unsqueeze(0).to(device)
    out = bytearray()
    with torch.no_grad():
        for _ in range(n_new):
            ctx = idx[:, -model.block_size:]
            la, lg, _, _, _ = model(ctx)
            Av = la[0, -1].float(); Gv = lg[0, -1].float()
            if mode == "base":
                logits = log_base.clone()
            else:
                logits = g_star[0] * log_base + g_star[1] * Av + g_star[2] * Gv
            logits = logits / temperature
            if top_k > 0:
                v, _ = torch.topk(logits, min(top_k, V)); logits[logits < v[-1]] = float("-inf")
            p = torch.softmax(logits, dim=-1)
            nxt = int(torch.multinomial(p, 1).item())
            out.append(nxt)
            idx = torch.cat([idx, torch.tensor([[nxt]], device=device)], dim=1)
    return bytes(out)


def probe_oo3(model, test_seq, device, g_min, g_full, log_base_vec, n_new=300):
    prompt = bytes(test_seq[:48].tobytes())
    base_b = gen_freerun(model, prompt, n_new, device, None, log_base_vec, "base")
    min_b = gen_freerun(model, prompt, n_new, device, g_min, log_base_vec, "min")
    full_b = gen_freerun(model, prompt, n_new, device, g_full, log_base_vec, "full")
    dec = lambda b: b.decode("utf-8", errors="replace")
    return {
        "prompt": prompt.decode("utf-8", errors="replace"),
        "base_stats": gen_stats(base_b), "min_stats": gen_stats(min_b), "full_stats": gen_stats(full_b),
        "base_sample": dec(base_b)[:200], "min_sample": dec(min_b)[:200], "full_sample": dec(full_b)[:200],
        "h1_ref_base_stats": {"entropy": 2.3917789581456956, "distinct_frac": 0.12109375, "ws_frac": 0.07666666666666666},
        "h1_ref_full_stats": {"entropy": 2.506038992540924, "distinct_frac": 0.109375, "ws_frac": 0.11333333333333333},
    }


# ───────────────────── main ─────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.join(HERE, "omega_cdv2_trained_leakfree.pt"))
    ap.add_argument("--corpus", default=os.path.join(HERE, "omega_corpus_big.bin"))
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--max_pos", type=int, default=12000)
    ap.add_argument("--out", default="omega_rigor_results.json")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(SEED); np.random.seed(SEED)
    print("=== OMEGA OΩ-RIGOR — OΩ1 (coupling vs replacement) + OΩ2 (per-wire) + OΩ3 (gen) ===", flush=True)
    print(f"device={device}  torch={torch.__version__}", flush=True)

    buf = open(args.corpus, "rb").read()
    corpus = np.frombuffer(buf, dtype=np.uint8)
    csha = hashlib.sha256(buf).hexdigest()
    n = len(corpus); cut = int(n * 0.9); held = corpus[cut:]
    print(f"corpus: {n}B ({n/1e6:.1f}MB)  sha256={csha[:16]}  held={len(held)}B", flush=True)

    ck = torch.load(args.ckpt, map_location=device, weights_only=False)
    cfg = ck["config"]
    csha_ck = hashlib.sha256(open(args.ckpt, "rb").read()).hexdigest()
    print(f"ckpt: {args.ckpt}  sha256={csha_ck[:16]}  config={cfg}", flush=True)
    model = ConsciousDecoderV2(
        vocab_size=cfg["vocab_size"], d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"], n_kv_head=cfg["n_kv_head"],
        consciousness_dim=cfg.get("consciousness_dim", 128), causal_ca=cfg.get("causal_ca", True),
    ).to(device)
    model.load_state_dict(ck["model"]); model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    nparam = model.count_params()
    print(f"CDV2 loaded FROZEN: {nparam:,} ({nparam/1e6:.2f}M)  causal_ca={model.causal_ca}", flush=True)

    # leak self-test
    with torch.no_grad():
        xt = torch.randint(0, V, (1, min(32, args.block)), device=device)
        la1, _, _, _, _ = model(xt)
        xt2 = xt.clone(); xt2[0, -1] = (int(xt[0, -1]) + 7) % V
        la2, _, _, _, _ = model(xt2)
        leak = float((la1[0, :-1] - la2[0, :-1]).abs().max().item())
    print(f"leak self-test: {leak:.3e}  (leak_free={leak<1e-4})", flush=True)

    # collect features ONCE on gate + test splits (SAME as OH1)
    gate_seq = held[:len(held) // 2]; test_seq = held[len(held) // 2:]
    t0 = time.time()
    gate_feats, gate_tgt, _, _ = extract_feats(model, gate_seq, args.block, device, args.max_pos)
    test_feats, test_tgt, test_tens, log_base_vec = extract_feats(model, test_seq, args.block, device, args.max_pos)
    print(f"[collect] gate N={len(gate_tgt)}  test N={len(test_tgt)}  ({time.time()-t0:.1f}s)", flush=True)

    # cross-check the loader reproduces #1800 (honesty gate)
    cc_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    cc_aonly = ce_of(np.array([1.0, ALPHA, 0.0]), test_feats, test_tgt)
    g_full = fit_gate(gate_feats, gate_tgt, free_mask=(1.0, 1.0, 1.0))
    cc_full = ce_of(g_full, test_feats, test_tgt)
    cc = {"base": (cc_base, H1_REF["base"]), "a_only": (cc_aonly, H1_REF["a_only"]),
          "full_AG": (cc_full, H1_REF["gated"])}
    cc_ok = True
    print("\n--- CROSS-CHECK vs #1800 H1 (tol=%.2f) ---" % H1_TOL, flush=True)
    cc_out = {}
    for k, (got, ref) in cc.items():
        d = abs(got - ref); ok = d <= H1_TOL; cc_ok = cc_ok and ok
        cc_out[k] = {"got": got, "ref": ref, "abs_delta": d, "ok": bool(ok)}
        print(f"  {k:<10} got={got:.6f} ref={ref:.6f} |Δ|={d:.6f} ok={ok}", flush=True)
    print(f"  CROSS_CHECK_OK = {cc_ok}", flush=True)

    # ── OΩ1 ──
    oo1 = probe_oo1(gate_feats, gate_tgt, test_feats, test_tgt)
    print("\n=== OΩ1 — COUPLING vs REPLACEMENT ===", flush=True)
    print(f"  g_min = [gB={oo1['g_min'][0]:.4f}, gA={oo1['g_min'][1]:.4f}, gG={oo1['g_min'][2]:.4f}]", flush=True)
    print(f"  base-only CE          = {oo1['ce_base']:.6f}", flush=True)
    print(f"  A-STANDALONE CE       = {oo1['ce_a_standalone']:.6f}  (softmax(A) alone, no base)", flush=True)
    print(f"  min_learned CE        = {oo1['ce_min_learned']:.6f}  (gB·base + gA·A)", flush=True)
    print(f"  min base-ABLATED CE   = {oo1['ce_min_base_ablated']:.6f}  (gB→0, keep gA·A)", flush=True)
    print(f"  |A_standalone − min|  = {oo1['delta_astandalone_vs_min']:.6f}  (≤{oo1['repl_tol']} ⇒ A≈min)", flush=True)
    print(f"  |base ablation Δ|     = {oo1['delta_base_ablation']:.6f}  (≤{oo1['repl_tol']} ⇒ base inert)", flush=True)
    print(f"  RULING_REPLACEMENT    = {oo1['RULING_REPLACEMENT']}", flush=True)
    print(f"  → {oo1['ruling_text']}", flush=True)

    # ── OΩ2 ──
    oo2 = probe_oo2(test_feats, test_tgt, test_tens)
    print("\n=== OΩ2 — PER-WIRE AUTOPSY (each wire added to base, held-out TEST CE) ===", flush=True)
    print(f"  base CE = {oo2['ce_base']:.6f}", flush=True)
    for wn, w in oo2["wires"].items():
        if w["isolatable"]:
            print(f"  {wn:<10} CE={w['ce']:.6f}  ΔvsBase={w['delta_vs_base']:+.6f}  [{w['semantics']}]", flush=True)
        else:
            print(f"  {wn:<10} HONEST-STUB (not isolatable): {w['stub_reason']}", flush=True)

    # ── OΩ3 ──
    g_min = np.array(oo1["g_min"])
    oo3 = probe_oo3(model, test_seq, device, g_min, g_full, log_base_vec)
    print("\n=== OΩ3 — GEN COHERENCE under min-gate (free-run, 300 new bytes) ===", flush=True)
    for nm, st in [("base", oo3["base_stats"]), ("min_gate", oo3["min_stats"]), ("full_gate", oo3["full_stats"])]:
        print(f"  {nm:<10} entropy={st['entropy']:.4f}  distinct_frac={st['distinct_frac']:.4f}  ws_frac={st['ws_frac']:.4f}  n={st['n']}", flush=True)
    print(f"  [min-gate sample]\n{oo3['min_sample']}", flush=True)
    print(f"  (#1800 ref: base ent 2.392 dist 0.121 ws 0.077 · full ent 2.506 dist 0.109 ws 0.113)", flush=True)

    if not cc_ok:
        print("\n!!! CROSS-CHECK FAILED — loader does NOT reproduce #1800. HALT (no fabrication).", flush=True)

    ledger = {
        "lane": "Lane-G", "substrate": "GPU/CPU-frozen-forward", "torch": torch.__version__, "device": device,
        "probe": "OΩ-RIGOR (OΩ1 coupling-vs-replacement + OΩ2 per-wire autopsy + OΩ3 gen coherence)",
        "ckpt": {"path": args.ckpt, "sha256": csha_ck},
        "corpus": {"path": args.corpus, "sha256": csha, "bytes": int(n)},
        "config": cfg, "leak_self_test": leak, "leak_free": bool(leak < 1e-4), "params": int(nparam),
        "meta": {"gate_N": int(len(gate_tgt)), "test_N": int(len(test_tgt)), "uniform_floor": UNIFORM_CE},
        "cross_check": {"tol": H1_TOL, "checks": cc_out, "CROSS_CHECK_OK": bool(cc_ok)},
        "OO1_coupling_vs_replacement": oo1,
        "OO2_per_wire_autopsy": oo2,
        "OO3_gen_coherence": oo3,
        "scope": "single d512 rung (a_scale_honest_scope); observation-only frozen forward (p7).",
    }
    json.dump(ledger, open(args.out, "w"), indent=2, ensure_ascii=False)
    print(f"\nresults -> {args.out}", flush=True)
    sys.exit(0 if cc_ok else 3)


if __name__ == "__main__":
    main()
