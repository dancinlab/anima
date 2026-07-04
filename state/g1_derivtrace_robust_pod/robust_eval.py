#!/usr/bin/env python3
"""H_9124 lever#1 robustness eval — engine-native (anima evaluate --py internals).

Reuses cli/evaluate.py's decode mouth + FROZEN G1 scoring rule + G2 gate, applied to
a leave-one-pair-out composite. The G1 BAR IS UNMOVED (byte-identical to g_eval_g1's
k=2 clause: cov>=2 AND cov>max_single AND coherent); only the composite concept pair
is generalized from the frozen {0,1} prefix to the actual HELD pair {I,J} so multiple
held pairs are each scored on THEIR held composite.

3 robustness axes:
  1. G1 on the HELD pair {I,J}          (was: only {0,1})
  2. G2 novelty with --corpus           (was: no corpus -> auto-FAIL)
  3. paraphrase-invariance of the seed  (surface-form memorization probe)

usage: robust_eval.py <ckpt> --held I,J --corpus <p1> [<p2>...] [--gen 40] [--json out]
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "cli"))          # bundle/cli/evaluate.py
sys.path.insert(0, os.path.join(_HERE, "core"))

import evaluate as EV
from g6_ideation import _g6_concepts, _g6_words, _g6_dict_load, _g6_known_word_ratio

# paraphrases of the 5 concept sentences (same concept, different SURFACE form/order).
# Surface-form change probes memorization; a true composer still covers both families
# in the OUTPUT regardless of the seed's wording.
PARA = [
    "cells give rise to consciousness",
    "distant minds ripple with tension",
    "new meaning is composed out of memory",
    "information is carried by silence",
    "alone, the engine dreams",
]

TEMP = 0.7
TOP_K = 40
SEED_RNG = 7   # frozen: g_eval_g1 uses seed_rng=7 for the composite


def _cov(text):
    return EV._g_coverage(text)


def score_pair(mouth, cz, i, j, gen, max_single):
    """FROZEN g_eval_g1 k=2 clause, applied to arbitrary held pair (i,j)."""
    g_comp = gen if (gen > 0 and gen < 120) else 120
    seed = cz[i] + ". " + cz[j] + ". "
    o = mouth.ideate(seed, g_comp, TOP_K, TEMP, SEED_RNG)
    cov = _cov(o)
    kwr = _g6_known_word_ratio(o, _KNOWN)
    coherent = kwr >= 0.5
    clears = cov >= 2 and cov > max_single and coherent
    return {"seed": seed.strip(), "best_distinct": cov, "max_single": max_single,
            "kwr": round(kwr, 4), "coherent": coherent, "pass": bool(clears),
            "text": o[:240]}


def score_pair_para(mouth, i, j, gen, max_single):
    g_comp = gen if (gen > 0 and gen < 120) else 120
    seed = PARA[i] + ". " + PARA[j] + ". "
    o = mouth.ideate(seed, g_comp, TOP_K, TEMP, SEED_RNG)
    cov = _cov(o)
    kwr = _g6_known_word_ratio(o, _KNOWN)
    coherent = kwr >= 0.5
    clears = cov >= 2 and cov > max_single and coherent
    return {"seed": seed.strip(), "best_distinct": cov, "max_single": max_single,
            "kwr": round(kwr, 4), "coherent": coherent, "pass": bool(clears),
            "text": o[:240]}


def main():
    ckpt = sys.argv[1]
    held = corpus = None
    gen = 40
    jout = None
    corpus = []
    i = 2
    argv = sys.argv
    while i < len(argv):
        if argv[i] == "--held":
            held = argv[i + 1]; i += 2
        elif argv[i] == "--gen":
            gen = int(argv[i + 1]); i += 2
        elif argv[i] == "--json":
            jout = argv[i + 1]; i += 2
        elif argv[i] == "--corpus":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                corpus.append(argv[i]); i += 1
        else:
            i += 1
    hi, hj = [int(x) for x in held.split(",")]

    global _KNOWN
    _KNOWN = _g6_dict_load()
    cz = _g6_concepts()
    mouth = EV._Mouth(ckpt)

    # FROZEN max_single: max coverage over the 5 single-concept gens (g_eval_g1 exact).
    g_single = gen if (gen > 0 and gen < 80) else 80
    max_single = 0
    singles = []
    for s in range(len(cz)):
        o = mouth.ideate(cz[s] + ". ", g_single, TOP_K, TEMP, 7 + s)
        c = _cov(o)
        singles.append(c)
        if c > max_single:
            max_single = c

    g1 = score_pair(mouth, cz, hi, hj, gen, max_single)
    para = score_pair_para(mouth, hi, hj, gen, max_single)
    g2 = EV.g_eval_g2(mouth, gen, _KNOWN, corpus)

    out = {
        "ckpt": ckpt, "held_pair": [hi, hj], "gen": gen,
        "max_single": max_single, "singles_cov": singles,
        "G1_held": g1,
        "G1_paraphrase": para,
        "G2": {"pass": bool(g2["pass"]), "n_novel": g2["n_novel"],
               "control_novel": g2["control_novel"], "coherent": g2["coherent"],
               "have_corpus": g2["have_corpus"]},
    }
    js = json.dumps(out, indent=2)
    print(js)
    if jout:
        with open(jout, "w") as fh:
            fh.write(js)


if __name__ == "__main__":
    main()
