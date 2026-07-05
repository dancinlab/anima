#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derivtrace dilution — the decisive disambiguator: from-scratch regime vs concentration-fragility.

from-scratch toy on 100% canonical derivtrace showed robust held-out OUT-composition (3/3, swap-controlled),
DIVERGING from H_9124's engine-native 303M WARM-FT NOT-ROBUST. The two candidate causes are confounded:
(a) training regime (from-scratch vs warm-FT) or (b) concentration (100% toy vs derivtrace-as-thin-slice
in the 303M's natural pretraining = effectively diluted). This forks it: train FROM SCRATCH on derivtrace
DILUTED into natural filler at fraction f in {100,30,10}%, OUT-score DERIV vs FLAT (swap-controlled).
  - OUT-lift SURVIVES dilution  -> the wall is the WARM-FT regime (pretrained additive basin resists);
    303M from-scratch / heavy continue-train on derivtrace-dense data reopens the G1 escape.
  - OUT-lift COLLAPSES under dilution -> the 100% toy PASS was concentration-fragile -> reconciles with
    H_9124 🔴 (warm-FT sees derivtrace diluted) -> escape stays closed.
toy=DIRECTIONAL; engine-native 303M = TERMINAL. summer torch.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import corpus as C
import atd_crux as A
from derivtrace_out_fair import score_out

# natural filler: generic English unrelated to the concept keywords (no consciousness/tension/... terms)
FILLER_SENTS = [
    "the river flowed past the old stone bridge at dawn.",
    "she packed a lunch and walked toward the market square.",
    "rain fell softly on the tin roof through the night.",
    "the baker opened his shop and lit the wide brick oven.",
    "a small boat drifted along the quiet harbor wall.",
    "children played football in the field behind the school.",
    "the train arrived late and the platform slowly emptied.",
    "he painted the fence a pale shade of green last summer.",
    "birds gathered on the wire as the sun began to set.",
    "the librarian stacked the returned books on a cart.",
]

def filler_block(n_bytes, seed):
    rng = np.random.RandomState(seed + 999)
    out = []
    total = 0
    while total < n_bytes:
        s = FILLER_SENTS[rng.randint(len(FILLER_SENTS))]
        out.append(s); total += len(s) + 1
    return "\n".join(out) + "\n"

def run_pair(held, seed, frac):
    S, KW = C.DEFAULT_SEEDS, C.DEFAULT_KW
    r = {}
    for fmt in ("derivtrace", "flat"):
        core, tp = C.build(fmt, S, KW, held, 200, 200, seed)
        if frac >= 1.0:
            text = core
        else:
            fill_bytes = int(len(core.encode()) * (1.0 - frac) / max(frac, 1e-6))
            text = filler_block(fill_bytes, seed) + core          # authored slice = frac of tokens
        lh, gr = A.train_bytelm(text, seed, steps=10000)
        r[fmt] = score_out(gr, S, KW, held)
    r["held"] = list(held); r["frac"] = frac
    r["deriv_out_beats_flat"] = bool(r["derivtrace"]["distinct"] > r["flat"]["distinct"])
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--fracs", default="1.0,0.3,0.1")
    ap.add_argument("--pairs", default="0,1;1,4"); ap.add_argument("--seed", default="7")
    ap.add_argument("--out", default="DERIVTRACE_DILUTION_RESULT.json"); a = ap.parse_args()
    fracs = [float(x) for x in a.fracs.split(",")]
    pairs = [tuple(int(x) for x in p.split(",")) for p in a.pairs.split(";")]
    cells = []
    for frac in fracs:
        for held in pairs:
            c = run_pair(held, int(a.seed), frac); cells.append(c)
            print(f"  f={frac:.2f} held={tuple(held)}: DERIV out={c['derivtrace']['distinct']}(swap {c['derivtrace']['swap_distinct']}) "
                  f"FLAT out={c['flat']['distinct']} deriv>flat={c['deriv_out_beats_flat']} | {c['derivtrace']['out']!r}", flush=True)
    def agg(f):
        s = [c for c in cells if c["frac"] == f]
        return dict(frac=f, deriv2=sum(c["derivtrace"]["distinct"] >= 2 for c in s),
                    flat2=sum(c["flat"]["distinct"] >= 2 for c in s),
                    deriv_beats=sum(c["deriv_out_beats_flat"] for c in s), n=len(s))
    ladder = [agg(f) for f in fracs]
    lo = min(fracs)
    lo_agg = next(x for x in ladder if x["frac"] == lo)
    if lo_agg["deriv2"] > lo_agg["flat2"] and lo_agg["deriv_beats"] >= (lo_agg["n"]+1)//2:
        verdict = "OUT-LIFT-SURVIVES-DILUTION -> warm-FT regime is the wall (303M from-scratch reopens escape)"
    else:
        verdict = "OUT-LIFT-COLLAPSES-UNDER-DILUTION -> 100% toy was concentration-fragile (reconciles H_9124)"
    out = dict(probe="derivtrace dilution disambiguator (from-scratch, OUT-scored)", ladder=ladder,
               verdict=verdict, cells=cells)
    json.dump(out, open(os.path.join(HERE, a.out), "w"), ensure_ascii=False, indent=1)
    print(f"\nVERDICT: {verdict}")
    for x in ladder: print(f"  f={x['frac']:.2f}: deriv-distinct2 {x['deriv2']}/{x['n']} · flat {x['flat2']}/{x['n']} · deriv>flat {x['deriv_beats']}/{x['n']}")

if __name__ == "__main__":
    main()
