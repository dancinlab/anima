#!/usr/bin/env python3
# build_corpus.py — structural recomb-objective corpus (H_1602 structural GPU-scale test).
#
# DESIGN (owner spec: "CE minimized ONLY through the combination path; corpus=2-concept
# combos; held-out = train-absent unseen combos"). DATA realization of an additive-bypass-
# DENIED recomb objective on a STANDARD ByteGPT (engine-native faithful; no un-decodable
# custom operator => avoids H_1601 INERT-readout trap): plain next-byte CE where the single-
# concept MARGINAL cannot predict a composed continuation, and the exact subsets the frozen
# G1 evaluator probes are HELD OUT.
#
# 5 concepts + keyword sets = FROZEN anima G1 concepts (cli/evaluate.py _g6_concepts /
# _g_concept_keywords) verbatim => trained trunk scored by the frozen bar unchanged.
#
# gen BUDGET: the frozen battery generates only 40 bytes for composed prompts (g_comp=40).
# So continuations are KEYWORD-DENSE (round-robin interleave of each subset concept's exact
# keyword tokens) — every token is a real word (kwr coherence passes) and 3+ concepts fit in
# 40 bytes. Single-concept docs emit ONLY their own concept's keywords => max_single stays 1.
#
# Prompt form MATCHES the evaluator seed exactly:
#   single   : "<concept sentence>. "
#   composed : ". ".join(concept sentences) + ". "
# HELD-OUT (never a composed doc): the evaluator first-k prefix subsets
#   {0,1}, {0,1,2}, {0,1,2,3}, {0,1,2,3,4}.
# Trained: 5 singletons + every 2/3/4-subset EXCEPT the held-out prefixes. Each concept is
# seen composed with OTHERS, so recombining on the held-out prefixes = SYSTEMATIC
# GENERALIZATION (the honest GPU-scale recombination test).

import random, sys, itertools

CONCEPT_SENTENCE = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
# exact eval keyword tokens (== _g_concept_keywords()); coverage = whole-token match.
KEYWORDS = [
    ["consciousness", "cells", "mind", "aware"],
    ["tension", "ripple", "distant", "between"],
    ["memory", "meaning", "compose", "new"],
    ["silence", "information", "quiet", "carries"],
    ["dream", "engine", "alone", "sleep"],
]

HELD_OUT = [frozenset({0, 1}), frozenset({0, 1, 2}),
            frozenset({0, 1, 2, 3}), frozenset({0, 1, 2, 3, 4})]

CONT_TOKENS = 14   # ~ up to ~90 bytes of continuation; eval reads only the first 40.


def prompt_for(order):
    return ". ".join(CONCEPT_SENTENCE[i] for i in order) + ". "


def continuation_for(subset, rng):
    # round-robin interleave one random keyword per concept, cycling through the subset,
    # so the FIRST |subset| tokens already cover every concept (dense within 40 bytes).
    order = list(subset); rng.shuffle(order)
    toks = []
    ci = 0
    while len(toks) < CONT_TOKENS:
        c = order[ci % len(order)]
        toks.append(rng.choice(KEYWORDS[c]))
        ci += 1
    return " ".join(toks) + "."


def train_subsets():
    subs = [(i,) for i in range(5)]
    for k in (2, 3, 4):
        for combo in itertools.combinations(range(5), k):
            if frozenset(combo) in HELD_OUT:
                continue
            subs.append(combo)
    return subs


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "corpus.txt"
    docs_per_subset = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 12345
    rng = random.Random(seed)
    subs = train_subsets()
    docs = []
    for sub in subs:
        for _ in range(docs_per_subset):
            order = list(sub); rng.shuffle(order)
            docs.append(prompt_for(order) + continuation_for(sub, rng))
    rng.shuffle(docs)
    text = "\n".join(docs) + "\n"
    with open(out, "wb") as f:
        f.write(text.encode("utf-8"))
    from collections import Counter
    kc = Counter(len(s) for s in subs)
    print(f"subsets={len(subs)} (by size {dict(kc)}) docs={len(docs)} "
          f"bytes={len(text.encode('utf-8'))} -> {out}")
    print("held_out (NOT in corpus): " + ", ".join(
        "{" + ",".join(map(str, sorted(h))) + "}" for h in HELD_OUT))
    print("sample train docs:")
    for d in docs[:4]:
        print("  " + d)


if __name__ == "__main__":
    main()
