#!/usr/bin/env python3
"""strict-G1 window-confound BYPASS-A, CANONICAL gen=40 (gen-guard #2821).

Reuses the CANONICAL cli/evaluate.py g_eval_g1 VERBATIM (frozen gate:
composed_distinct>=2 AND >max_single AND coherent). The ONLY change is the
decode window T, swept as a free parameter — subclass _Mouth so ideate() calls
a T-parameterized twin of clm_decode_topk_sampled_W (identical logic, only T
changed from the hardcoded 24). gen stays CANONICAL 40 (=> g_eval_g1 sets
g_single=40, g_comp=40 since 40<80 and 40<120). max_single re-measured at same T.

RATIONALE: CLMConvMoE has NO positional embedding (RF~513, dilated causal conv),
trained at seq_len=1024 => T is a free decode param, not a block_size. At T=24 a
k=2 composed seed (~72B) has concept-1 OUT of window. Expanding T (still <<1024,
<<513 RF) lets both concepts co-exist. MEASUREMENT-PHYSICS fix, bar UNCHANGED.

usage: python3 g1_canonical_windowsweep.py <ckpt.clm> <T1,T2,...>
"""
import os, sys, json, time
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "core"))
sys.path.insert(0, os.path.join(_HERE, "cli"))
import numpy as np
import decode as D
import evaluate as EV
from g6_ideation import _g6_dict_load

CKPT = sys.argv[1]
TSET = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [24, 48, 96, 192]
GEN = 40  # CANONICAL (gen-guard #2821)


class _MouthT(EV._Mouth):
    """canonical _Mouth but decode window T is configurable (was hardcoded 24)."""
    def __init__(self, ckpt, T):
        super().__init__(ckpt)
        self.T = T

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        assert self.kind == "clm", "bypass sweep is clm-mouth only"
        return _clm_decode_T(self.W, seed, gen, top_k, temp, seed_rng, self.T)


def _clm_decode_T(W, seed, gen, top_k, temp, seed_rng, T):
    """T-parameterized twin of decode.clm_decode_topk_sampled_W — IDENTICAL logic,
    only T (was 24). Right-align seed, pad-left byte 32, slide window during gen."""
    V = W["V"]
    seed_b = seed.encode("utf-8", "surrogateescape")
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    rng = D._mix32(seed_rng)
    for _ in range(gen):
        logits = D._fwd_logits(W, tok, T)
        nb, rng = D._topk_sample(logits[T - 1], V, top_k, temp, rng)
        out.append(nb)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(nb)
    return {"ok": True, "text": out.decode("utf-8", "surrogateescape")}["text"]


def main():
    t0 = time.time()
    known = _g6_dict_load()
    out = {"ckpt": CKPT, "gen_CANONICAL": GEN,
           "engine": "canonical cli/evaluate.py g_eval_g1 VERBATIM (frozen: composed>=2 AND >max_single AND coherent); _Mouth subclassed to sweep decode window T only.",
           "gen_guard": "#2821 canonical gen=40 => g_single=40 g_comp=40 (both <80/<120).",
           "note": "CLMConvMoE no-posemb RF~513, train seq_len=1024 => T free decode param not block_size.",
           "sweep": []}
    for T in TSET:
        tt = time.time()
        m = _MouthT(CKPT, T)
        r = EV.g_eval_g1(m, GEN, known)
        r_out = {"T": T, "pass_strict": r["pass"], "max_single": r["max_single"],
                 "best_distinct": r["best_distinct"], "best_k": r["best_k"],
                 "ks": r["ks"], "wall_s": round(time.time() - tt, 1)}
        out["sweep"].append(r_out)
        print("[T=%d] gen40 max_single=%d best_distinct=%d best_k=%d STRICT_PASS=%s (%.1fs)" % (
            T, r["max_single"], r["best_distinct"], r["best_k"], r["pass"], r_out["wall_s"]), flush=True)
    out["total_wall_s"] = round(time.time() - t0, 1)
    out["strict_PASS_any_T"] = any(s["pass_strict"] for s in out["sweep"])
    print("STRICT_PASS_ANY_T=%s" % out["strict_PASS_any_T"], flush=True)
    with open(os.path.join(_HERE, "g1_canonical_windowsweep_result.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
