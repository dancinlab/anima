"""stage_capture.py — 3(4)-WAY per-stage tensor dump to isolate the FIRST
divergence point in the clm303 decode forward.

Forward = core/clm_decode.py _fwd_logits, re-expressed with (a) stage capture
and (b) a math-mode toggle:
  math='eng'  -> dt_erf gelu, _gn_sqrt Newton GN, _moe_exp router softmax  (PRODUCTION)
  math='corr' -> math.erf gelu, np.sqrt GN, np.exp router softmax          (CORRECT)
The GEMMs (conv im2col @ Wt) are numpy float64 matmul in BOTH modes; conv
differences therefore come ONLY from weight values (int4 vs fp32), and gelu/GN/
softmax differences come ONLY from the dt_* approximations.

4 paths captured:
  fp32+corr  (≈ torch golden: full precision, correct math)
  fp32+eng   (full precision, production math)
  int4+eng   (ACTUAL PRODUCTION ENGINE = core/clm_decode.py on the .clm)
  int4+corr  (numpy-math mirror: quantized weights, correct math)
"""
import sys, os, math
import numpy as np

sys.path.insert(0, "core")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clm_decode as clm
from wbuild import build_wfp32

_erf_vec = np.vectorize(math.erf)


def gelu_corr(x):
    return 0.5 * x * (1.0 + _erf_vec(x * 0.70710678118654752440))


def gn_corr(x, g, b, T, C):
    x = x.reshape(T, C)
    mu = x.mean(1, keepdims=True)
    var = ((x - mu) ** 2).mean(1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5) * g[None, :] + b[None, :]


def moe_soft_corr(logits, T, E):
    logits = logits.reshape(T, E)
    z = logits - logits.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def fwd_capture(W, tok, T, math_mode):
    d = W["d"]; E = W["E"]; V = W["V"]; K = W["K"]; L = W["L"]
    cap = {}
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    cap["s0_embed"] = xe.copy()
    xt = clm._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    cap["s1_ec"] = xt.copy()
    dil = 1
    for li in range(L):
        de = dil if dil <= 512 else 512
        h = clm._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de)
        if math_mode == "eng":
            hn = clm.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
            hg = clm.nn_gelu_fwd(hn)
        else:
            hn = gn_corr(h, W["tgG"][li], W["tgB"][li], T, d)
            hg = gelu_corr(hn)
        xt = xt + hg.reshape(T, d)
        cap["s2_trunk%d" % li] = xt.copy()
        dil *= 2
    logits_r = clm._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    cap["s3_router_logits"] = logits_r.copy()
    ex_out = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = clm._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex_out[ej] = (clm.nn_gelu_fwd(eo) if math_mode == "eng" else gelu_corr(eo)).reshape(T, d)
    cap["s4_expert_stack"] = ex_out.copy()
    if math_mode == "eng":
        y = clm.nn_moe_router_fwd(logits_r, ex_out, T, E, d)
    else:
        probs = moe_soft_corr(logits_r, T, E)
        y = np.einsum('te,etc->tc', probs, ex_out.reshape(E, T, d))
    cap["s5_moe"] = y.copy()
    if math_mode == "eng":
        yn = clm.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    else:
        yn = gn_corr(y, W["noG"], W["noB"], T, d)
    cap["s6_normout"] = yn.copy()
    out_logits = clm._conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1)
    cap["s7_logits"] = out_logits.copy()
    return cap


def build_tok(seed, T=24):
    sb = seed.encode("utf-8", "surrogateescape")
    sl = len(sb)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = sl - T + p
        tok[p] = float(sb[si]) if si >= 0 else 32.0
    return tok


# representative prompts: a G6 composed frame + a G1 k=2 compose seed
PROMPTS = {
    "G6frame": "if consciousness arises from cells, then tension ripples between distant minds: ",
    "G1compose": "consciousness arises from cells. tension ripples between distant minds. ",
}

CLM = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.clm")
PT = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.pt")


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stages")
    os.makedirs(out, exist_ok=True)
    toks = {k: build_tok(v) for k, v in PROMPTS.items()}

    print("[1/2] loading int4 .clm ...", flush=True)
    Wi = clm.clm_load_weights(CLM)
    for pn, tk in toks.items():
        np.savez(os.path.join(out, "int4_eng_%s.npz" % pn), **fwd_capture(Wi, tk, 24, "eng"))
        np.savez(os.path.join(out, "int4_corr_%s.npz" % pn), **fwd_capture(Wi, tk, 24, "corr"))
        print("  int4 %s done" % pn, flush=True)
    del Wi

    print("[2/2] loading fp32 .pt ...", flush=True)
    Wf = build_wfp32(PT, 3)
    for pn, tk in toks.items():
        np.savez(os.path.join(out, "fp32_eng_%s.npz" % pn), **fwd_capture(Wf, tk, 24, "eng"))
        np.savez(os.path.join(out, "fp32_corr_%s.npz" % pn), **fwd_capture(Wf, tk, 24, "corr"))
        print("  fp32 %s done" % pn, flush=True)
    del Wf
    print("STAGE CAPTURE COMPLETE -> %s" % out, flush=True)


if __name__ == "__main__":
    main()
