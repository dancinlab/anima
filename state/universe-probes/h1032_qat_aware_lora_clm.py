#!/usr/bin/env python3
"""H_1032 — Does a QUANTIZATION-AWARE LoRA fix the H_1030 int4-.clm break? ($0 CPU, numpy, NO GPU)

Residual follow-up of H_1030 (🔴 LORA-BREAKS-CLM). H_1030 showed a naive float-LoRA on our
CLMConvMoE ADAPTS (CE 5.75->1.66 @ 5.2% params) but the int4 .clm serialization DESTROYS the
adaptation (merge ΔCE 3.83 >> 0.20), while the no-LoRA base round-trips at ΔCE 0.003 — so the
break is LoRA-delta-specific (the low-rank delta concentrates per-output-channel magnitude the
15-level sym-int4 quant crushes). H_1030 §6 named the untested fix: a QAT-aware LoRA.

This script reuses the H_1030 numpy CLMConvMoE + LoRA + CANONICAL serialize_v3 + byte-exact mirror.
The ONLY change vs H_1030: the LoRA is trained QUANT-AWARE — the merged conv/readout weights pass
through the EXACT serializer fake-quant (`_quant_block`: per-output-channel sym-int4, scale=amax/7,
code=clip(round(w/scale),-7,7), dequant=code*scale) on every forward, with a straight-through
estimator (the finite-difference grad sees the fake-quant forward directly). So the LoRA optimizes
against the quantized model and the merged weights LAND ON the int4 grid.

Frozen falsifier (2026-06-08):
  PASS = QAT-LORA-CLM-VIABLE : QAT-LoRA ADAPTS (CE_qat_lora < CE_base, ratio<0.5) AND its merge is
         BYTE-FAITHFUL (|ΔCE| <= 0.20 AND CE_mirror < uniform lnV) — a Δ-vs-H_1030 fix.
  FAIL = QAT-LORA-STILL-BREAKS : QAT-LoRA can't BOTH adapt AND merge faithfully (closed-negative).
A float-LoRA arm (= H_1030, NO fake-quant) is re-run as the direct baseline so float-merge-ΔCE vs
QAT-merge-ΔCE is measured in one run.

substrate=numpy (torch unavailable); .clm by CANONICAL serialize_v3; decode by byte-exact mirror
(engine-link deferred, memory clm-decode-macos-link-gap, a_scale_honest_scope). p3/p6: generic byte
target, NOT persona. a_clm_gen_pipeline: ConvMoE stays ConvMoE.
"""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "CLM", "model"))
sys.path.insert(0, os.path.join(ROOT, "state", "mid_convmoe_fire"))
import clm_serialize_v2 as ser           # canonical serializer (source of the fake-quant)
import clm_decode_mirror as mir          # byte-exact engine-decode mirror

np.random.seed(1032)
V = 256
d = 16          # tiny width
K = 3           # conv kernel
L = 1           # trunk layers
E = 2           # experts
T = 24          # window (matches mirror probe length)
INT4_SYM_MAX = 7.0   # == ser.INT4_SYM_MAX (15-level symmetric int4)

# --------------------------------------------------------------------------- #
# generic synthetic byte target (p3/p6: NOT persona) — same as H_1030
# --------------------------------------------------------------------------- #
def make_task():
    motif = np.array([65, 66, 67, 68, 67, 66, 65, 32], dtype=np.int64)  # "ABCDCBA "
    full = np.tile(motif, 64)
    train = full[:512].copy()
    heldout = full[400:400 + T].copy()
    return train, heldout

TRAIN, HELDOUT = make_task()

# --------------------------------------------------------------------------- #
# numpy CLMConvMoE forward (mirrors model.py / clm_decode math) — same as H_1030
# --------------------------------------------------------------------------- #
def init_base():
    g = lambda *s: (np.random.randn(*s) * 0.08).astype(np.float64)
    sd = {}
    sd["embed.weight"] = g(V, d)
    sd["embed_conv.conv.weight"] = g(d, d, K)
    sd["embed_conv.conv.bias"] = np.zeros(d)
    sd["trunk.0.conv.conv.weight"] = g(d, d, K)
    sd["trunk.0.conv.conv.bias"] = np.zeros(d)
    sd["trunk.0.norm.weight"] = np.ones(d)
    sd["trunk.0.norm.bias"] = np.zeros(d)
    for j in range(E):
        sd[f"moe.experts.{j}.conv.conv.weight"] = g(d, d, K)
        sd[f"moe.experts.{j}.conv.conv.bias"] = np.zeros(d)
    sd["moe.router.weight"] = g(E, d, 1)
    sd["moe.router.bias"] = np.zeros(E)
    sd["norm_out.weight"] = np.ones(d)
    sd["norm_out.bias"] = np.zeros(d)
    sd["readout.weight"] = g(V, d, 1)
    sd["readout.bias"] = np.zeros(V)
    return sd

def gelu(x):
    inner = 0.7978845608 * (x + 0.044715 * x * x * x)
    a = np.clip(inner, -15.0, 15.0)
    e2 = np.exp(2.0 * a)
    return 0.5 * x * (1.0 + (e2 - 1.0) / (e2 + 1.0))

def causal_conv(x, w3d, b, dil):
    Tn, Cin = x.shape
    Cout = w3d.shape[0]
    w2d = w3d.reshape(Cout, Cin * K)
    xcol = np.zeros((Tn, Cin * K))
    t_idx = np.arange(Tn)
    for k in range(K):
        shift = dil * (K - 1 - k)
        p = t_idx - shift
        valid = p >= 0
        cols = np.arange(Cin) * K + k
        src = np.where(valid[:, None], x[np.clip(p, 0, Tn - 1)], 0.0)
        xcol[:, cols] = src
    return xcol @ w2d.T + b[None, :]

def groupnorm1(x, g, b):
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5) * g[None, :] + b[None, :]

# --------------------------------------------------------------------------- #
# QAT fake-quant — EXACT mirror of serialize_v2._quant_block (per-output-channel
# sym-int4 on the 2D (cout, cin*K) view the serializer uses). dequant = code*scale.
# This is the straight-through-estimated quant: forward = quantized weight, and
# because training is numerical-gradient over the LoRA factors, the finite-diff
# probes this same fake-quant forward (the STE: grad flows to A,B through the quant).
# --------------------------------------------------------------------------- #
def fake_quant_2d(w2d):
    """w2d: (cout, rest). Returns dequantized weight on the int4 grid, same shape."""
    amax = np.abs(w2d).max(axis=1)
    scale = np.maximum(amax / INT4_SYM_MAX, 1e-12)
    codes = np.round(w2d / scale[:, None])
    codes = np.clip(codes, -INT4_SYM_MAX, INT4_SYM_MAX)
    return codes * scale[:, None]

def fake_quant_conv(w3d):
    """conv weight (cout, cin, K) -> fake-quant on the (cout, cin*K) view -> back."""
    cout, cin, k = w3d.shape
    w2d = w3d.reshape(cout, cin * k)
    return fake_quant_2d(w2d).reshape(cout, cin, k)

def forward_logits(sd, tok, fake_quant=False):
    """fake_quant=True applies the int4 fake-quant to the LoRA-targeted weights
    (readout + expert-0 conv) — the QAT forward. fake_quant=False = the H_1030 float forward."""
    fq_conv = fake_quant_conv if fake_quant else (lambda w: w)
    xe = sd["embed.weight"][tok]
    xt = causal_conv(xe, sd["embed_conv.conv.weight"], sd["embed_conv.conv.bias"], 1)
    dil = 1
    for li in range(L):
        h = causal_conv(xt, sd[f"trunk.{li}.conv.conv.weight"], sd[f"trunk.{li}.conv.conv.bias"], min(dil, 512))
        hn = groupnorm1(h, sd[f"trunk.{li}.norm.weight"], sd[f"trunk.{li}.norm.bias"])
        xt = xt + gelu(hn)
        dil *= 2
    rW = sd["moe.router.weight"].reshape(E, d)
    logits_r = xt @ rW.T + sd["moe.router.bias"][None, :]
    ex = []
    for j in range(E):
        ew = sd[f"moe.experts.{j}.conv.conv.weight"]
        if fake_quant and j == 0:                      # expert-0 is a LoRA target
            ew = fq_conv(ew)
        eo = causal_conv(xt, ew, sd[f"moe.experts.{j}.conv.conv.bias"], 1)
        ex.append(gelu(eo))
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)
    y = np.zeros((T, d))
    for j in range(E):
        y += probs[:, j:j+1] * ex[j]
    yn = groupnorm1(y, sd["norm_out.weight"], sd["norm_out.bias"])
    roW = sd["readout.weight"]                          # (V,d,1)
    if fake_quant:                                      # readout is a LoRA target
        roW = fq_conv(roW)
    roW = roW.reshape(V, d)
    return yn @ roW.T + sd["readout.bias"][None, :]

def ce_window(sd, seq, fake_quant=False):
    logits = forward_logits(sd, np.asarray(seq, dtype=int), fake_quant=fake_quant)
    tot = 0.0
    for p in range(T - 1):
        z = logits[p] - logits[p].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[int(seq[p + 1])] - lse)
    return tot / (T - 1)

# --------------------------------------------------------------------------- #
# LoRA — same injection as H_1030 (rank-2 on readout + expert-0 conv)
# --------------------------------------------------------------------------- #
RANK = 2
def init_lora():
    lora = {}
    lora["readout.A"] = (np.random.randn(V, RANK) * 0.02)
    lora["readout.B"] = np.zeros((RANK, d))
    lora["e0.A"] = (np.random.randn(d, RANK) * 0.02)
    lora["e0.B"] = np.zeros((RANK, d))
    return lora

def lora_param_count(lora):
    return sum(v.size for v in lora.values())

def full_ft_param_count(sd):
    return sum(v.size for v in sd.values())

def apply_lora(base_sd, lora):
    sd = {k: v.copy() for k, v in base_sd.items()}
    dW_ro = lora["readout.A"] @ lora["readout.B"]            # (V,d)
    sd["readout.weight"] = sd["readout.weight"] + dW_ro[:, :, None]
    dW_e0 = lora["e0.A"] @ lora["e0.B"]                       # (d,d)
    sd["moe.experts.0.conv.conv.weight"] = sd["moe.experts.0.conv.conv.weight"] + dW_e0[:, :, None]
    return sd

def lora_ce(base_sd, lora, seq, fake_quant=False):
    return ce_window(apply_lora(base_sd, lora), seq, fake_quant=fake_quant)

def train_lora(base_sd, lora, train_seq, fake_quant=False, steps=40, lr=0.5, eps=1e-2):
    """numerical-gradient (STE) descent on the LoRA factors. When fake_quant=True the
    forward quantizes the merged weights, so the LoRA optimizes against the int4 grid.
    eps is sized large enough to cross int4 grid cells (the STE descent signal)."""
    keys = list(lora.keys())
    bases = list(range(0, max(1, len(train_seq) - T), 8))[:8]
    def batch_ce(lr_dict):
        tot = 0.0; cnt = 0
        for base in bases:
            if base + T <= len(train_seq):
                tot += lora_ce(base_sd, lr_dict, train_seq[base:base + T], fake_quant=fake_quant)
                cnt += 1
        return tot / cnt
    for it in range(steps):
        cur = batch_ce(lora)
        for key in keys:
            arr = lora[key]
            grad = np.zeros_like(arr)
            flat = arr.reshape(-1)
            gflat = grad.reshape(-1)
            for i in range(flat.size):
                old = flat[i]
                flat[i] = old + eps
                fp = batch_ce(lora)
                flat[i] = old
                gflat[i] = (fp - cur) / eps
            lora[key] = arr - lr * grad
    return lora, batch_ce(lora)

def merge_serialize_mirror(base, lora, tag):
    """merge LoRA -> serialize_v3 (.clm) -> byte-exact mirror decode. Returns
    (ce_merged_inmem float-forward, ce_mirror, dCE, descent)."""
    merged = apply_lora(base, lora)
    clm_path = f"/tmp/_h1032_{tag}.clm"
    ser.serialize_v3(merged, n_trunk_layers=L, n_experts=E, out_path=clm_path)
    ce_merged_mem = ce_window(merged, HELDOUT)            # float forward (in-mem merged)
    W = mir.load_clm(clm_path)
    logits_m = mir.fwd_logits(W, np.asarray(HELDOUT, dtype=float), T)
    ce_mirror, _ = mir.ce_nextbyte(logits_m, list(HELDOUT), T, V)
    dCE = abs(ce_mirror - ce_merged_mem)
    descent = ce_mirror < math.log(V)
    return ce_merged_mem, ce_mirror, dCE, descent

# --------------------------------------------------------------------------- #
def main():
    print("H_1032 — QAT-aware LoRA vs naive float LoRA on CLMConvMoE int4-.clm (numpy, $0 CPU, NO GPU)")
    print("=" * 78)
    ENV = 0.20
    uniform = math.log(V)

    base = init_base()
    full_n = full_ft_param_count(base)
    ce_base = ce_window(base, HELDOUT)
    print(f"\nCE_base_heldout = {ce_base:.5f}   (frozen-base, no LoRA)")
    print(f"FULL_FT_PARAMS  = {full_n}")
    print(f"CE_uniform_lnV  = {uniform:.5f}")

    # ---- CONTROL: int4 round-trip of the BASE (no LoRA) ----
    ser.serialize_v3(base, n_trunk_layers=L, n_experts=E, out_path="/tmp/_h1032_base.clm")
    Wb = mir.load_clm("/tmp/_h1032_base.clm")
    lgb = mir.fwd_logits(Wb, np.asarray(HELDOUT, dtype=float), T)
    ce_base_mirror, _ = mir.ce_nextbyte(lgb, list(HELDOUT), T, V)
    dCE_base = abs(ce_base_mirror - ce_base)
    print(f"\n[CONTROL] base int4 round-trip ΔCE = {dCE_base:.5f}  (BASE_FAITHFUL={1 if dCE_base<=ENV else 0})")

    # ---- ARM 1: float-LoRA baseline (= H_1030, NO fake-quant) ----
    # both LoRA arms start from an identical init (init_lora is deterministic given
    # the RNG state here; arm 2 below re-inits the same way for a fair head-to-head).
    np.random.seed(1032)
    lora_f = init_lora()
    lora_f, _ = train_lora(base, lora_f, TRAIN, fake_quant=False)
    ce_lora_f = lora_ce(base, lora_f, HELDOUT, fake_quant=False)
    ce_m_f, ce_mir_f, dCE_f, desc_f = merge_serialize_mirror(base, lora_f, "float")
    print("\n[ARM 1] FLOAT-LoRA (= H_1030 baseline, no fake-quant)")
    print(f"  CE_floatlora_heldout = {ce_lora_f:.5f}   (ADAPT={1 if ce_lora_f<ce_base else 0})")
    print(f"  CE_merged_inmem      = {ce_m_f:.5f}")
    print(f"  CE_mirror_decode     = {ce_mir_f:.5f}")
    print(f"  FLOAT_MERGE_DELTA_CE = {dCE_f:.5f}   (int4 envelope <= {ENV}; expect ~3.83 reproducing H_1030)")
    print(f"  FLOAT_BYTE_FAITHFUL  = {1 if dCE_f<=ENV else 0}")

    # ---- ARM 2: QAT-aware LoRA (the fix — fake-quant in forward, STE grad) ----
    np.random.seed(1032)            # identical LoRA init to arm 1 (fair head-to-head)
    lora_q = init_lora()
    lora_q, _ = train_lora(base, lora_q, TRAIN, fake_quant=True)
    # adapt CE measured on the QAT (fake-quant) forward — the model the LoRA actually optimizes
    ce_lora_q_fq = lora_ce(base, lora_q, HELDOUT, fake_quant=True)
    # also the float-forward CE of the merged (context)
    ce_lora_q_fl = lora_ce(base, lora_q, HELDOUT, fake_quant=False)
    ce_m_q, ce_mir_q, dCE_q, desc_q = merge_serialize_mirror(base, lora_q, "qat")
    lora_n = lora_param_count(lora_q)
    ratio = lora_n / full_n
    print("\n[ARM 2] QAT-AWARE LoRA (fake-quant int4 in forward, STE grad — the H_1030 fix)")
    print(f"  CE_qatlora_fqfwd     = {ce_lora_q_fq:.5f}   (ADAPT vs base={1 if ce_lora_q_fq<ce_base else 0})")
    print(f"  CE_qatlora_floatfwd  = {ce_lora_q_fl:.5f}   (context: float-forward of same weights)")
    print(f"  LORA_PARAMS          = {lora_n}")
    print(f"  PARAM_RATIO          = {ratio:.6f}   (PARAMS_LE_HALF={1 if ratio<0.5 else 0})")
    print(f"  CE_merged_inmem      = {ce_m_q:.5f}")
    print(f"  CE_mirror_decode     = {ce_mir_q:.5f}")
    print(f"  QAT_MERGE_DELTA_CE   = {dCE_q:.5f}   (int4 envelope <= {ENV}; the H_1030 fix target)")
    print(f"  QAT_BYTE_FAITHFUL    = {1 if dCE_q<=ENV else 0}")
    print(f"  QAT_MIRROR_DESCENT   = {1 if desc_q else 0}  (CE_mirror < uniform lnV)")

    # ---- verdict ----
    adapt = ce_lora_q_fq < ce_base
    ratio_ok = ratio < 0.5
    faithful = dCE_q <= ENV
    descent = desc_q
    viable = adapt and ratio_ok and faithful and descent
    verdict = "QAT-LORA-CLM-VIABLE" if viable else "QAT-LORA-STILL-BREAKS"
    print("\n" + "=" * 78)
    print(f"ADAPT={1 if adapt else 0}  RATIO_OK={1 if ratio_ok else 0}  "
          f"BYTE_FAITHFUL={1 if faithful else 0}  DESCENT={1 if descent else 0}")
    print(f"FLOAT_MERGE_DELTA_CE = {dCE_f:.5f}   ->   QAT_MERGE_DELTA_CE = {dCE_q:.5f}   "
          f"(Δ-vs-H_1030 fix = {1 if dCE_q < dCE_f else 0})")
    print(f"VERDICT = {verdict}")
    print("  PASS=QAT-LORA-CLM-VIABLE (QAT-LoRA ADAPTS AND merge BYTE-FAITHFUL ΔCE<=0.20 AND descent)")
    print("  FAIL=QAT-LORA-STILL-BREAKS (QAT-LoRA can't BOTH adapt AND merge faithfully — int4 .clm LoRA-hostile)")
    print("substrate=numpy (torch unavailable); .clm by CANONICAL serialize_v3; decode by byte-exact mirror")
    print("p3/p6 generic byte target (NOT persona); a_clm_gen_pipeline ConvMoE-only; a_scale_honest_scope toy d16/L1/E2")

if __name__ == "__main__":
    main()
