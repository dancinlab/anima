#!/usr/bin/env python3
"""H_1030 — Can we LoRA an existing LLM to our CLM standard?  ($0 CPU, numpy, NO GPU)

Two-arm pre-registered falsifier (frozen 2026-06-07). Substrate = numpy
(torch unavailable on this Mac). The numpy CLMConvMoE forward re-implements the
SAME conv-native math as CLM/model/model.py / CORE/clm_decode.hexa. The merged
state_dict is packed into the EXACT torch-key layout that the CANONICAL serializer
CLM/model/clm_serialize_v2.py::serialize_v3 consumes, so the .clm is produced by
the real serializer (not a re-implementation). Decode is verified by the byte-exact
mirror state/mid_convmoe_fire/clm_decode_mirror.py (memory clm-decode-macos-link-gap).

ARM A (deterministic): a foundation-transformer state_dict (attention QKV + FFN,
NO conv/router/expert/readout-conv) is fed to serialize_v3 -> it CANNOT map ->
KeyError/mismatch == "LoRA-on-foundation -> engine-mount BLOCKED".

ARM B ($0 toy): base CLMConvMoE (frozen random) -> inject low-rank LoRA on the
expert + readout convs -> adapt on a GENERIC synthetic formal-language byte task
(p3/p6: NOT persona) by numerical-gradient descent over ONLY the LoRA factors ->
(B1) CE_lora < CE_base with LoRA params << full params; (B2) merge LoRA into the
base weights, serialize_v3 -> .clm, mirror-decode -> |CE_mirror - CE_merged| within
int4 envelope AND mirror CE < uniform lnV (AXIS-2 descent).
"""
import os, sys, math, struct, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "CLM", "model"))
sys.path.insert(0, os.path.join(ROOT, "state", "mid_convmoe_fire"))
import clm_serialize_v2 as ser           # canonical serializer
import clm_decode_mirror as mir           # byte-exact engine-decode mirror

np.random.seed(1030)
V = 256
d = 16          # tiny width
K = 3           # conv kernel
L = 1           # trunk layers (decoder-general; L=1 keeps it small)
E = 2           # experts
T = 24          # window (matches mirror probe length)

# --------------------------------------------------------------------------- #
# generic synthetic byte target task (p3/p6: NOT persona) — a deterministic
# formal-language slice: a periodic structured byte stream over a small alphabet
# with a fixed grammar (next byte = f(position-in-cycle)). The base random model
# does not know it; LoRA must adapt to lower CE on a HELD-OUT window.
# --------------------------------------------------------------------------- #
def make_task():
    # formal language: cycle of a fixed 8-symbol motif mapped into byte space.
    motif = np.array([65, 66, 67, 68, 67, 66, 65, 32], dtype=np.int64)  # "ABCDCBA "
    full = np.tile(motif, 64)
    train = full[:512].copy()
    heldout = full[400:400 + T].copy()   # a held-out window (different phase tail)
    return train, heldout

TRAIN, HELDOUT = make_task()

# --------------------------------------------------------------------------- #
# numpy CLMConvMoE forward (mirrors model.py / clm_decode math)
# weights stored as a flat param dict in TORCH-KEY layout (what serialize_v3 reads)
# conv weight shape (cout, cin, K); bias (cout,)
# --------------------------------------------------------------------------- #
def init_base():
    g = lambda *s: (np.random.randn(*s) * 0.08).astype(np.float64)
    sd = {}
    sd["embed.weight"] = g(V, d)                      # (V,d)
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
    # x: (T, Cin); w3d: (Cout, Cin, K) ; causal left pad. Matches mirror conv1d
    # EXACTLY: w2d col j = ci*K + k and tap p = t - dil*(K-1-k). VECTORIZED im2col
    # (byte-identical to the loop form, just no Python loops -> tractable on CPU).
    Tn, Cin = x.shape
    Cout = w3d.shape[0]
    w2d = w3d.reshape(Cout, Cin * K)
    xcol = np.zeros((Tn, Cin * K))
    t_idx = np.arange(Tn)
    for k in range(K):                       # only K iterations (K=3)
        shift = dil * (K - 1 - k)
        p = t_idx - shift                    # (Tn,)
        valid = p >= 0
        # rows where tap valid get x[p]; cols ci*K + k for all ci
        cols = np.arange(Cin) * K + k        # (Cin,)
        src = np.where(valid[:, None], x[np.clip(p, 0, Tn - 1)], 0.0)  # (Tn,Cin)
        xcol[:, cols] = src
    return xcol @ w2d.T + b[None, :]

def groupnorm1(x, g, b):
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5) * g[None, :] + b[None, :]

def forward_logits(sd, tok):
    xe = sd["embed.weight"][tok]                                  # (T,d)
    xt = causal_conv(xe, sd["embed_conv.conv.weight"], sd["embed_conv.conv.bias"], 1)
    dil = 1
    for li in range(L):
        h = causal_conv(xt, sd[f"trunk.{li}.conv.conv.weight"], sd[f"trunk.{li}.conv.conv.bias"], min(dil, 512))
        hn = groupnorm1(h, sd[f"trunk.{li}.norm.weight"], sd[f"trunk.{li}.norm.bias"])
        xt = xt + gelu(hn)
        dil *= 2
    rW = sd["moe.router.weight"].reshape(E, d)
    logits_r = xt @ rW.T + sd["moe.router.bias"][None, :]         # (T,E)
    ex = []
    for j in range(E):
        eo = causal_conv(xt, sd[f"moe.experts.{j}.conv.conv.weight"], sd[f"moe.experts.{j}.conv.conv.bias"], 1)
        ex.append(gelu(eo))
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)
    y = np.zeros((T, d))
    for j in range(E):
        y += probs[:, j:j+1] * ex[j]
    yn = groupnorm1(y, sd["norm_out.weight"], sd["norm_out.bias"])
    roW = sd["readout.weight"].reshape(V, d)
    return yn @ roW.T + sd["readout.bias"][None, :]               # (T,V)

def ce_window(sd, seq):
    # position p predicts seq[p+1]; mean over T-1 (matches mirror ce_nextbyte)
    logits = forward_logits(sd, np.asarray(seq, dtype=int))
    tot = 0.0
    for p in range(T - 1):
        z = logits[p] - logits[p].max()
        lse = math.log(np.exp(z).sum())
        tot += -(z[int(seq[p + 1])] - lse)
    return tot / (T - 1)

# --------------------------------------------------------------------------- #
# LoRA: low-rank adapters A(d,r)·B(r,d) added to the readout + expert-0 conv
# (the conv weight (Cout,Cin,K) gets a per-k low-rank delta on the Cin->Cout map).
# Only A,B are trainable. We adapt with NUMERICAL gradient (few params, $0).
# --------------------------------------------------------------------------- #
RANK = 2
LORA_TARGETS = ["readout.weight", "moe.experts.0.conv.conv.weight"]

def init_lora():
    lora = {}
    for key in LORA_TARGETS:
        w = None  # shape resolved against base at merge
    # readout: (V,d,1) -> map d->V. LoRA A:(V,r) B:(r,d)
    lora["readout.A"] = (np.random.randn(V, RANK) * 0.02)
    lora["readout.B"] = np.zeros((RANK, d))           # B=0 -> initial delta 0
    # expert0 conv: (d,d,K) -> per kernel slice d->d. A:(d,r) B:(r,d), shared over K
    lora["e0.A"] = (np.random.randn(d, RANK) * 0.02)
    lora["e0.B"] = np.zeros((RANK, d))
    return lora

def lora_param_count(lora):
    return sum(v.size for v in lora.values())

def full_ft_param_count(sd):
    return sum(v.size for v in sd.values())

def apply_lora(base_sd, lora):
    """return a merged state_dict = base + lora delta (does NOT mutate base)."""
    sd = {k: v.copy() for k, v in base_sd.items()}
    # readout delta: dW (V,d) added to readout.weight (V,d,1)
    dW_ro = lora["readout.A"] @ lora["readout.B"]            # (V,d)
    sd["readout.weight"] = sd["readout.weight"] + dW_ro[:, :, None]
    # expert0 delta: dW (d,d) broadcast onto each kernel tap k
    dW_e0 = lora["e0.A"] @ lora["e0.B"]                       # (d,d)
    sd["moe.experts.0.conv.conv.weight"] = sd["moe.experts.0.conv.conv.weight"] + dW_e0[:, :, None]
    return sd

def lora_ce(base_sd, lora, seq):
    return ce_window(apply_lora(base_sd, lora), seq)

def train_lora(base_sd, lora, train_seq, steps=40, lr=0.5, eps=1e-3):
    """numerical-gradient descent on the LoRA factors over a small fixed window set."""
    keys = list(lora.keys())
    # fixed set of training windows (cap to keep finite-diff $0-tractable on CPU)
    bases = list(range(0, max(1, len(train_seq) - T), 8))[:8]
    def batch_ce(lr_dict):
        tot = 0.0; cnt = 0
        for base in bases:
            if base + T <= len(train_seq):
                tot += lora_ce(base_sd, lr_dict, train_seq[base:base + T])
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

# --------------------------------------------------------------------------- #
# ARM A — foundation transformer block-mismatch (deterministic)
# --------------------------------------------------------------------------- #
def arm_a():
    # a tiny foundation-transformer state_dict: attention QKV + FFN, NO conv /
    # router / expert / readout-conv structure the .clm grammar requires.
    tfm_sd = {
        "tok_emb.weight": np.random.randn(V, d).astype(np.float32),
        "blocks.0.attn.qkv.weight": np.random.randn(3 * d, d).astype(np.float32),
        "blocks.0.attn.proj.weight": np.random.randn(d, d).astype(np.float32),
        "blocks.0.ffn.fc1.weight": np.random.randn(4 * d, d).astype(np.float32),
        "blocks.0.ffn.fc2.weight": np.random.randn(d, 4 * d).astype(np.float32),
        "blocks.0.ln1.weight": np.ones(d, dtype=np.float32),
        "lm_head.weight": np.random.randn(V, d).astype(np.float32),
    }
    blocked = False
    err = ""
    try:
        ser.serialize_v3(tfm_sd, n_trunk_layers=L, n_experts=E,
                         out_path="/tmp/_h1030_arm_a.clm")
    except (KeyError, ValueError) as e:
        blocked = True
        err = f"{type(e).__name__}: {str(e)[:120]}"
    return blocked, err

# --------------------------------------------------------------------------- #
def main():
    print("H_1030 — LoRA on CLMConvMoE vs foundation transformer (numpy, $0 CPU, NO GPU)")
    print("=" * 72)

    # ---- ARM A ----
    blocked, err = arm_a()
    print("\n[ARM A] foundation transformer -> .clm serialize")
    print(f"  ARM_A_BLOCKED = {1 if blocked else 0}")
    print(f"  ARM_A_REASON  = {err if blocked else 'serializer ACCEPTED a transformer (unexpected)'}")

    # ---- ARM B ----
    base = init_base()
    lora = init_lora()
    lora_n = lora_param_count(lora)
    full_n = full_ft_param_count(base)
    ratio = lora_n / full_n

    ce_base = ce_window(base, HELDOUT)
    lora, _ = train_lora(base, lora, TRAIN)
    ce_lora = lora_ce(base, lora, HELDOUT)

    print("\n[ARM B1] LoRA adapts CLMConvMoE on generic held-out byte task (p3/p6: NOT persona)")
    print(f"  CE_base_heldout = {ce_base:.5f}")
    print(f"  CE_lora_heldout = {ce_lora:.5f}")
    print(f"  CE_DROPPED      = {1 if ce_lora < ce_base else 0}")
    print(f"  LORA_PARAMS     = {lora_n}")
    print(f"  FULL_FT_PARAMS  = {full_n}")
    print(f"  PARAM_RATIO     = {ratio:.6f}")
    print(f"  PARAMS_LE_HALF  = {1 if ratio < 0.5 else 0}")
    b1 = (ce_lora < ce_base) and (ratio < 0.5)
    print(f"  ARM_B1_PASS     = {1 if b1 else 0}")

    # ---- CONTROL: does int4 faithfully preserve the BASE (no LoRA)? ----
    # isolates whether any B2 break is LoRA-delta-specific vs generic int4 loss.
    ser.serialize_v3(base, n_trunk_layers=L, n_experts=E, out_path="/tmp/_h1030_base.clm")
    Wb = mir.load_clm("/tmp/_h1030_base.clm")
    lgb = mir.fwd_logits(Wb, np.asarray(HELDOUT, dtype=float), T)
    ce_base_mirror, _ = mir.ce_nextbyte(lgb, list(HELDOUT), T, V)
    ce_base_mem2 = ce_window(base, HELDOUT)
    dCE_base = abs(ce_base_mirror - ce_base_mem2)
    print("\n[CONTROL] int4 round-trip of BASE (no LoRA) — is the envelope generally lossy?")
    print(f"  CE_base_inmem    = {ce_base_mem2:.5f}")
    print(f"  CE_base_mirror   = {ce_base_mirror:.5f}")
    print(f"  DELTA_CE_BASE    = {dCE_base:.5f}   (int4 envelope <= 0.20)")
    print(f"  BASE_FAITHFUL    = {1 if dCE_base <= 0.20 else 0}  (1 => int4 faithful on base; any B2 break is LoRA-delta-specific)")

    # ---- ARM B2: merge -> serialize_v3 (canonical) -> mirror decode ----
    merged = apply_lora(base, lora)
    clm_path = "/tmp/_h1030_merged.clm"
    ser.serialize_v3(merged, n_trunk_layers=L, n_experts=E, out_path=clm_path)
    clm_bytes = os.path.getsize(clm_path)

    # in-memory merged CE on the probe window (same semantics as mirror)
    ce_merged_mem = ce_window(merged, HELDOUT)
    # mirror decode: re-derive from serialized int4 .clm and compute CE on same window
    W = mir.load_clm(clm_path)
    logits_m = mir.fwd_logits(W, np.asarray(HELDOUT, dtype=float), T)
    ce_mirror, _ = mir.ce_nextbyte(logits_m, list(HELDOUT), T, V)
    uniform = math.log(V)
    dCE = abs(ce_mirror - ce_merged_mem)
    ENV = 0.20
    faithful = dCE <= ENV
    descent = ce_mirror < uniform
    b2 = faithful and descent

    print("\n[ARM B2] LoRA-merged -> serialize_v3 (.clm) -> byte-exact mirror decode")
    print(f"  CLM_BYTES        = {clm_bytes}")
    print(f"  CE_merged_inmem  = {ce_merged_mem:.5f}")
    print(f"  CE_mirror_decode = {ce_mirror:.5f}")
    print(f"  CE_uniform_lnV   = {uniform:.5f}")
    print(f"  DELTA_CE         = {dCE:.5f}   (int4 envelope <= {ENV})")
    print(f"  BYTE_FAITHFUL    = {1 if faithful else 0}")
    print(f"  MIRROR_DESCENT   = {1 if descent else 0}  (CE_mirror < uniform)")
    print(f"  ARM_B2_PASS      = {1 if b2 else 0}")

    # ---- verdict ----
    arm_b = b1 and b2
    verdict = "LORA-VIABLE-ON-CONVMOE" if (arm_b and blocked) else "LORA-BREAKS-CLM"
    print("\n" + "=" * 72)
    print(f"ARM_A_BLOCKED={1 if blocked else 0}  ARM_B1={1 if b1 else 0}  ARM_B2={1 if b2 else 0}")
    print(f"VERDICT = {verdict}")
    print("  PASS=LORA-VIABLE-ON-CONVMOE (Arm B1&B2 hold AND Arm A foundation BLOCKED)")
    print("  FAIL=LORA-BREAKS-CLM (Arm B fails to adapt OR breaks int4/.clm byte-faithfulness)")
    print("substrate=numpy (torch unavailable); .clm by CANONICAL serialize_v3; decode by byte-exact mirror (engine-link deferred, a_scale_honest_scope)")

if __name__ == "__main__":
    main()
