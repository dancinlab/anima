#!/usr/bin/env python3
"""H_9124 lever#1 — derivation-trace procedural corpus generator (2-arm control).

PARAMETERIZED leave-one-pair-out variant of the H_9124 canonical generator
(byte-identical logic to the prior fire's embedded generator; the ONLY change is
HELDOUT_PAIR + SEED are now argv so we can sweep >=4 held pairs).

  anima corpus derivtrace|flat  ==  this script, held pair {I,J}, seed S.

Emits TWO byte corpora that are CONTENT-MATCHED and differ ONLY in target format:
  DERIV : composite prompt -> explicit derivation trace -> final OUT passage
  FLAT  : composite prompt -> final OUT passage only

Both arms come from the SAME instance stream (same pairs, keyword fills, RNG order);
FLAT = DERIV with the derivation middle removed. Only data-format is the varied
(controlled) variable; the held pair {I,J} is never trained (both orderings), so the
G1 gate composite on {I,J} is a memorization-free pair-generalization test.

usage:  derivtrace_corpus.py <outdir> <held_i> <held_j> <seed>
"""
import random, sys

# concept seed sentences (EXACTLY cz[] from core/g6_ideation._g6_concepts)
S = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
# per-family EXACT detector words (real English -> kwr-safe; each hits its family)
KW = [
    ["consciousness", "cells", "mind", "aware"],
    ["tension", "distant", "between"],
    ["memory", "meaning", "new"],
    ["silence", "information", "quiet", "carries"],
    ["engine", "alone", "dream"],
]

DERIVE_LEAD = ["derive", "steps", "unfold", "trace"]
BIND = ["bind", "join", "weave", "link"]
CLOSE = ["new meaning arises", "meaning composes anew",
         "a new whole arises", "they compose into meaning"]


def two(rng, fam):
    ks = KW[fam][:]
    rng.shuffle(ks)
    return ks[0], ks[1 % len(ks)]


def instance(rng, i, j):
    a1, a2 = two(rng, i)
    b1, b2 = two(rng, j)
    prompt = f"{S[i]}. {S[j]}. "
    out = f"out: {a1} {a2} meet {b1} {b2}, {rng.choice(CLOSE)}.\n"
    deriv_mid = (f"{rng.choice(DERIVE_LEAD)}: take {a1} and {a2}; "
                 f"take {b1} and {b2}; {rng.choice(BIND)} {a1} with {b1}. ")
    return prompt + deriv_mid + out, prompt + out


def single(rng, i):
    a1, a2 = two(rng, i)
    return f"{S[i]}. here {a1} and {a2} stand alone; {a1} holds {a2}.\n"


def build(rng, train_pairs, n_comp_per_pair, n_single_per_concept):
    deriv, flat = [], []
    stream = []
    for _ in range(n_comp_per_pair):
        for (i, j) in train_pairs:
            stream.append(("comp", i, j))
    for _ in range(n_single_per_concept):
        for i in range(5):
            stream.append(("sing", i, None))
    rng.shuffle(stream)
    for kind, i, j in stream:
        if kind == "comp":
            d, f = instance(rng, i, j)
            deriv.append(d); flat.append(f)
        else:
            s = single(rng, i)
            deriv.append(s); flat.append(s)
    return "".join(deriv), "".join(flat)


if __name__ == "__main__":
    outdir = sys.argv[1]
    held_i = int(sys.argv[2]); held_j = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    rng = random.Random(seed)

    HELDOUT_PAIR = frozenset((held_i, held_j))
    train_pairs = []
    for i in range(5):
        for j in range(5):
            if i == j:
                continue
            if frozenset((i, j)) == HELDOUT_PAIR:
                continue
            train_pairs.append((i, j))

    deriv, flat = build(rng, train_pairs, n_comp_per_pair=280, n_single_per_concept=300)
    with open(f"{outdir}/deriv.txt", "w") as fh:
        fh.write(deriv)
    with open(f"{outdir}/flat.txt", "w") as fh:
        fh.write(flat)
    print(f"held_pair={{{held_i},{held_j}}} seed={seed} "
          f"train_pairs={len(train_pairs)} (18 = 20 ordered - 2 held orderings)")
    print(f"DERIV bytes={len(deriv.encode())} FLAT bytes={len(flat.encode())}")
    print("--- DERIV sample head ---")
    print(deriv[:400])
    print("--- FLAT sample head ---")
    print(flat[:280])
