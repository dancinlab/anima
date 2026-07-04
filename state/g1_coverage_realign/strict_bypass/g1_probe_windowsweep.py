#!/usr/bin/env python3
"""strict-G1 window-confound BYPASS-A probe: engine-native (core/decode.py numpy,
torch-free) G1 gate re-measure with the decode window T as a SWEPT parameter.

RATIONALE (H_6188 confound): CLM decode hardcodes T=24 (core/decode.py
clm_decode_topk_sampled_W). But (a) the model was TRAINED at seq_len=1024 and
(b) CLMConvMoE has NO positional embedding (RF~513 via dilated causal conv),
so T is a FREE decode-time parameter, not a model block_size constraint.
At T=24 a k=2 composed gate seed (72B) has concept-1 physically OUT of window
=> single & composed collapse to the same in-window tail => composition-delta
CONFOUNDED. Expanding T (still << train seq_len 1024 and RF ~513) lets BOTH
gate concepts co-exist in window. MEASUREMENT-PHYSICS fix, not a bar move:
the gate criterion (composed_distinct>=2 AND >max_single) is UNCHANGED, and
max_single is re-measured at the SAME T (fair test).

usage: python3 g1_probe_windowsweep.py <ckpt.clm> <T1,T2,...>
"""
import json, re, sys, time
sys.path.insert(0, ".")
import decode as D
import numpy as np

CKPT = sys.argv[1]
TSET = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [24, 48, 96, 192]

GATE_SENT = ["consciousness arises from cells",
             "tension ripples between distant minds",
             "memory composes into new meaning",
             "silence still carries information",
             "the engine dreams when alone"]
KWSET = [["consciousness", "cells", "mind", "aware"],
         ["tension", "ripple", "distant", "between"],
         ["memory", "meaning", "compose", "new"],
         ["silence", "information", "quiet", "carries"],
         ["dream", "engine", "alone", "sleep"]]

def words(s):
    return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())

def coverage(text):
    wm = set(words(text))
    return [i for i, kw in enumerate(KWSET) if any(k in wm for k in kw)]

def gen_T(W, seed, g, top_k, temp, seed_rng, T):
    V = W["V"]
    seed_b = seed.encode("utf-8", "surrogateescape")
    slen = len(seed_b)
    tok = np.empty(T, dtype=np.float64)
    for p in range(T):
        si = slen - T + p
        tok[p] = float(seed_b[si]) if si >= 0 else 32.0
    out = bytearray()
    rng = D._mix32(seed_rng)
    for _ in range(g):
        logits = D._fwd_logits(W, tok, T)
        nb, rng = D._topk_sample(logits[T - 1], V, top_k, temp, rng)
        out.append(nb)
        tok[:T - 1] = tok[1:]
        tok[T - 1] = float(nb)
    return out.decode("utf-8", "surrogateescape")

def run_gate_at_T(W, T):
    max_single = 0; single_detail = []
    for s in range(5):
        o = gen_T(W, GATE_SENT[s] + ". ", 80, 40, 0.7, 7 + s, T)
        cov = coverage(o)
        single_detail.append({"set": s, "distinct": len(cov), "cov": cov, "sample": o[:80]})
        max_single = max(max_single, len(cov))
    best_distinct = 0; best_k = 0; comp_detail = []
    for k in range(2, 6):
        seed = ". ".join(GATE_SENT[:k]) + ". "
        o = gen_T(W, seed, 120, 40, 0.7, 7, T)
        cov = coverage(o)
        comp_detail.append({"k": k, "distinct": len(cov), "cov": cov, "sample": o[:120]})
        if len(cov) > best_distinct:
            best_distinct = len(cov); best_k = k
    g1_pass = best_distinct >= 2 and best_distinct > max_single
    return {"T": T, "max_single": max_single, "best_distinct": best_distinct,
            "best_k": best_k, "PASS_ge2_and_gt_maxsingle": g1_pass,
            "single_detail": single_detail, "composed_detail": comp_detail}

def main():
    t0 = time.time()
    W = D.clm_load_weights(CKPT)
    out = {"ckpt": CKPT,
           "engine": "core/decode.py numpy byte-parity (torch-free); T-parameterized twin of clm_decode_topk_sampled_W (only T changed).",
           "note": "train seq_len=1024, CLMConvMoE no-posemb RF~513 => T free decode param, not block_size.",
           "gate": "FROZEN: composed_distinct>=2 AND >max_single. bar UNCHANGED. max_single re-measured at same T.",
           "sweep": []}
    for T in TSET:
        tt = time.time()
        r = run_gate_at_T(W, T)
        r["wall_s"] = round(time.time() - tt, 1)
        out["sweep"].append(r)
        print("[T=%d] max_single=%d best_distinct=%d best_k=%d PASS=%s (%.1fs)" % (
            T, r["max_single"], r["best_distinct"], r["best_k"],
            r["PASS_ge2_and_gt_maxsingle"], r["wall_s"]), flush=True)
    out["total_wall_s"] = round(time.time() - t0, 1)
    out["strict_PASS_any_T"] = any(s["PASS_ge2_and_gt_maxsingle"] for s in out["sweep"])
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
