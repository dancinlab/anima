"""ablate.py — SELF-CONSISTENT quantization + dt-math ablation on clm303_clean.

Because the .pt and .clm express the same model in DIFFERENT hidden-channel bases
(network symmetry; confirmed: fastmirror.clm CE 1.69 ~ torch_golden.pt CE 1.74,
yet element-wise weights uncorrelated), we CANNOT diff .pt vs .clm per-stage.
Instead we take the .pt fp32 weights (one basis) and ablate WITHIN that basis:

  A fp32_eng  : fp32 weights,  engine dt_* math (gelu=dt_erf, GN=_gn_sqrt, softmax=dt_exp/_moe_exp)
  B int4_eng  : int4-quantized (OUR quant, same int4-sym per-out-channel scheme), engine math
  C fp32_corr : fp32 weights,  correct math (np.exp/np.erf/np.sqrt)  [monkeypatched]
  D int4_corr : int4 weights,  correct math

A vs B  = PURE quantization effect (same basis, same math)   -> does int4 kill G1/G6?
A vs C  = PURE dt-math effect     (same weights)             -> does dt_* kill G1/G6?
The real production .clm (separate basis) is measured separately as a cross-check.

Quantization replicates core clm serializer dequant  w=(nibble-8)*scale  (nibble 0..15,
levels -8..7), per OUTPUT-channel scale, applied ONLY to conv weights (embed/biases/
GN are fp32 ext in the .clm too).
"""
import sys, os, math, time, copy
import numpy as np

sys.path.insert(0, "core")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "state/clm303_g6/tools")
import clm_decode as clm
import g_gates as gg
from wbuild import build_wfp32

CLM = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.clm")
PT = os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.pt")


# ── int4-sym per-output-channel quant on conv weights stored Wt[Kdim, Cout] ──
def q_col(Wt):
    Wt = np.asarray(Wt, dtype=np.float64)
    scale = np.abs(Wt).max(axis=0, keepdims=True) / 7.0   # per output channel (col)
    scale = np.where(scale <= 0, 1.0, scale)
    nib = np.clip(np.round(Wt / scale) + 8, 0, 15)
    return (nib - 8) * scale


def quantize_W(W):
    Wq = dict(W)
    Wq["ecWt"] = q_col(W["ecWt"])
    Wq["tcWt"] = [q_col(w) for w in W["tcWt"]]
    Wq["eWt"] = [q_col(w) for w in W["eWt"]]
    Wq["rWt"] = q_col(W["rWt"])
    Wq["roWt"] = q_col(W["roWt"])
    return Wq


# ── correct-math monkeypatch (flips ALL engine dt_* to numpy-correct) ──
_erf_vec = np.vectorize(math.erf)
_ORIG = {}


def patch_correct():
    _ORIG["dt_exp"] = clm.dt_exp
    _ORIG["dt_ln"] = clm.dt_ln
    _ORIG["dt_erf"] = clm.dt_erf
    _ORIG["_moe_exp"] = clm._moe_exp
    _ORIG["_gn_sqrt"] = clm._gn_sqrt
    clm.dt_exp = lambda x: np.exp(np.asarray(x, dtype=np.float64))
    clm.dt_ln = lambda x: np.log(np.asarray(x, dtype=np.float64))
    clm.dt_erf = lambda x: _erf_vec(np.asarray(x, dtype=np.float64))
    clm._moe_exp = lambda x: np.exp(np.asarray(x, dtype=np.float64))
    clm._gn_sqrt = lambda x: math.sqrt(x) if x > 0 else 0.0


def unpatch():
    for k, v in _ORIG.items():
        setattr(clm, k, v)


class WMouth:
    """g_gates mouth over a preloaded clm W dict (basis-consistent ablation)."""
    kind = "clm"

    def __init__(self, W):
        self.W = W

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        return clm.clm_decode_topk_sampled_W(self.W, seed, gen, top_k, temp, seed_rng)["text"]


def run_gates(tag, mouth, known, gen, corpus_paths):
    t = time.time()
    r0 = gg.g_eval_g0(mouth, gen, known)
    r1 = gg.g_eval_g1(mouth, gen, known)
    r6 = gg.g_eval_g6(mouth, gen, known)
    dt = time.time() - t
    line = ("[%s] G0 n_coh=%d/5 pass=%s | G1 max_single=%d best_distinct=%d pass=%s | "
            "G6 dist=%d fals=%d coh=%d pass=%s  (%.0fs)") % (
        tag, r0["n_coherent"], r0["pass"], r1["max_single"], r1["best_distinct"], r1["pass"],
        r6["dist"], r6["fals"], r6["coherent"], r6["pass"], dt)
    print(line, flush=True)
    # G1 ladder detail
    lad = " ".join("k%d:d%d/kwr%.2f/%s" % (x["k"], x["distinct"], x["kwr"], "clr" if x["clears"] else "no")
                   for x in r1["ks"])
    print("    G1 ladder: " + lad, flush=True)
    return {"tag": tag, "g0": r0, "g1": r1, "g6": r6}


def main():
    gen = 40   # match the existing int4 baseline (state/clm303_clean_corpus/g0g6_py.txt)
    known = gg._g6_dict_load()
    corpus = []
    print("=== loading fp32 .pt -> Wf (basis F) ===", flush=True)
    Wf = build_wfp32(PT, 3)
    print("=== quantizing Wf -> Wq (int4-sym per-out-channel) ===", flush=True)
    Wq = quantize_W(Wf)
    # quick CE sanity (engine math) so quant didn't break the model
    rb = np.frombuffer(open("state/clm303_clean_corpus/gen_en.txt", "rb").read(), np.uint8)
    def ce(W, n=6):
        T = 24; st = max(1, (len(rb) - T - 1) // n); s = 0.0; c = 0
        for i in range(n):
            b = i * st
            tk = rb[b:b+T].astype(np.float64); tg = rb[b+1:b+T+1].astype(int)
            lg = clm._fwd_logits(W, tk, T); z = lg - lg.max(1, keepdims=True)
            s += float((-(z[np.arange(T), tg] - np.log(np.exp(z).sum(1)))).sum()/T); c += 1
        return s/c
    print("    CE(math.log) fp32=%.4f int4=%.4f  (uniform=%.4f)" % (ce(Wf), ce(Wq), math.log(256)), flush=True)

    res = []
    print("\n=== A: fp32_eng (full precision, engine dt_* math) ===", flush=True)
    res.append(run_gates("A_fp32_eng", WMouth(Wf), known, gen, corpus))
    print("\n=== B: int4_eng (OUR int4 quant, engine dt_* math) — quant ablation vs A ===", flush=True)
    res.append(run_gates("B_int4_eng", WMouth(Wq), known, gen, corpus))
    print("\n=== C: fp32_corr (full precision, CORRECT math) — dt-math ablation vs A ===", flush=True)
    patch_correct()
    try:
        res.append(run_gates("C_fp32_corr", WMouth(Wf), known, gen, corpus))
        res.append(run_gates("D_int4_corr", WMouth(Wq), known, gen, corpus))
    finally:
        unpatch()
    print("\n=== E: REAL .clm via production clm_decode (separate basis, cross-check) ===", flush=True)
    res.append(run_gates("E_realclm_eng", gg._Mouth(CLM), known, gen, corpus))

    print("\n================ SUMMARY (G1 best_distinct / G6 fals) ================", flush=True)
    for r in res:
        print("  %-14s G1.best_distinct=%d G1.pass=%s | G6.dist=%d G6.fals=%d G6.pass=%s" % (
            r["tag"], r["g1"]["best_distinct"], r["g1"]["pass"],
            r["g6"]["dist"], r["g6"]["fals"], r["g6"]["pass"]), flush=True)


if __name__ == "__main__":
    main()
