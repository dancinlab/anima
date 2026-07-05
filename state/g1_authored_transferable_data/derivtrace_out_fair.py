#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derivtrace fair re-score — OUT-only, apples-to-apples (verdict-integrity metric-confound check).

The first robustness run scored derivtrace's keyword-rich DERIVATION TRACE (first ~80 gen chars, which
by echo==composition design lists both families' keywords) but scored flat on its OUT (harder) -> the
apparent DERIV>FLAT lift was a metric CONFOUND, and it diverged from H_9124's engine-native 303M
leave-one-pair-out (deriv bd=1 floor, worse than flat = 🔴 NOT-ROBUST). This re-scores BOTH arms on the
OUT clause only ("out: a1 a2 meet b1 b2"), apples-to-apples, plus a swap-null (does the OUT bind the
RIGHT families, or would the swapped families score equal = order-blind).

  OUT-distinct : distinct held-out families whose keywords appear in the OUT clause (post-'out:').
  swap-null    : same OUT scored against SWAPPED family assignment; genuine bind => true > swap.
verdict: if DERIV OUT-distinct floors to flat's level -> confirms metric-confound + H_9124 NOT-ROBUST.
toy=DIRECTIONAL; engine-native 303M bd = TERMINAL (H_9124 stands). summer torch.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import corpus as C
import atd_crux as A

def out_clause(gen):
    k = gen.lower().find("out:")
    if k < 0: return ""
    seg = gen[k+4:]
    nl = seg.find("\n");  seg = seg if nl < 0 else seg[:nl]
    return seg.lower()

def score_out(greedy, S, KW, held):
    i, j = held
    prompt = f"{S[i]}. {S[j]}. "
    gen = greedy(prompt, n=160)                 # enough to reach the OUT past any trace
    oc = out_clause(gen)
    fam_i = int(any(w.lower() in oc for w in KW[i]))
    fam_j = int(any(w.lower() in oc for w in KW[j]))
    distinct = fam_i + fam_j
    # swap-null: score OUT against a DIFFERENT (wrong) pair's families
    others = [k for k in range(len(S)) if k not in held]
    wi, wj = others[0], others[1]
    swap_distinct = int(any(w.lower() in oc for w in KW[wi])) + int(any(w.lower() in oc for w in KW[wj]))
    return dict(distinct=distinct, swap_distinct=swap_distinct, out=oc[:60])

def run_pair(held, seed):
    S, KW = C.DEFAULT_SEEDS, C.DEFAULT_KW
    r = {}
    for fmt in ("derivtrace", "flat"):
        text, tp = C.build(fmt, S, KW, held, 200, 200, seed)
        lh, gr = A.train_bytelm(text, seed, steps=8000)
        r[fmt] = score_out(gr, S, KW, held)
    r["held"] = list(held)
    r["deriv_out_beats_flat"] = bool(r["derivtrace"]["distinct"] > r["flat"]["distinct"])
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pairs", default="0,1;1,4;0,3")
    ap.add_argument("--seed", default="7"); ap.add_argument("--out", default="DERIVTRACE_OUTFAIR_RESULT.json")
    a = ap.parse_args()
    pairs = [tuple(int(x) for x in p.split(",")) for p in a.pairs.split(";")]
    cells = [run_pair(h, int(a.seed)) for h in pairs]
    for c in cells:
        print(f"  held={tuple(c['held'])}: DERIV out-distinct={c['derivtrace']['distinct']}(swap {c['derivtrace']['swap_distinct']}) "
              f"FLAT out-distinct={c['flat']['distinct']}(swap {c['flat']['swap_distinct']}) "
              f"deriv>flat={c['deriv_out_beats_flat']} | DERIV out={c['derivtrace']['out']!r}", flush=True)
    n = len(cells); nd = sum(c["deriv_out_beats_flat"] for c in cells)
    deriv2 = sum(c["derivtrace"]["distinct"] >= 2 for c in cells); flat2 = sum(c["flat"]["distinct"] >= 2 for c in cells)
    if deriv2 > flat2 and nd >= (n+1)//2:
        verdict = "DERIV-OUT-LIFT-survives-fair-scoring"
    elif deriv2 <= flat2:
        verdict = "METRIC-CONFOUND-CONFIRMED-deriv-lift-was-trace-artifact (H_9124 NOT-ROBUST stands)"
    else:
        verdict = "INCONCLUSIVE-fair"
    out = dict(probe="derivtrace OUT-only fair re-score (metric-confound check)", cells=cells,
               n_deriv_out_beats_flat=nd, deriv_out_distinct2=deriv2, flat_out_distinct2=flat2, verdict=verdict)
    json.dump(out, open(os.path.join(HERE, a.out), "w"), ensure_ascii=False, indent=1)
    print(f"\nVERDICT: {verdict}  (deriv-out>flat {nd}/{n} · deriv-out-distinct2 {deriv2}/{n} · flat-out-distinct2 {flat2}/{n})")

if __name__ == "__main__":
    main()
