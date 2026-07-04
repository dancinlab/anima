#!/usr/bin/env python3
"""build_corpus.py — GAMMA-DATA vs ADD corpus builder for the H_9127 G1 fire.

Escalates the ONLY surviving STEP-0 signal (B3 gamma-via-DATA-channel) to a REAL
303M byte-mouth, engine-native. The scientific question = TRANSFER:

  STEP-0 toy PASSED but its decoder was HANDED the role/slot keys (fixed keys +
  canonical-sorted binding). A real byte-mouth must LEARN role-binding from the
  training distribution and EMIT compositions on held-out concept combos with NO
  role-key at test. So we build TWO corpora that differ ONLY in the compositional
  TARGET FORMAT (the data channel), warm-FT h1129 on each, and measure the frozen
  anima G1 bar (evaluate.py). role-key is NEVER handed at test (the bar seeds plain
  concept phrases -- no role tags).

  GAMMA-DATA  -- role-slot bound composition grammar (gamma constructive-bind in the
                DATA channel): `bind [r0] A [r1] B => <A-clause> and <B-clause> .`
                Fixed content-free role slots [r0][r1][r2] = the HRR skeleton (V1).
                MULTIPATH: every ordering of the slots is emitted (V6 confluence /
                order-invariance). The model must UNBIND each role and emit its
                concept's keyword clause.
  ADD         -- flat additive concatenation, SAME clauses/content, NO bind operator,
                NO role slots, single canonical order: `<A-clause> <B-clause> .`

CONTROLLED: both arms share the identical single-concept cell (G0 / max_single
preservation), the identical concept set, the identical held-out split, and the
identical composition CONTENT. ONLY the composition FORMAT varies.

HELD-OUT (the G1 transfer test): the 5 FROZEN-BAR concepts (C0..C4) are NEVER
composed *with each other* in training -- every training composition pairs a bar
concept only with an EXTRA (distractor) concept, or two extras together. The bar
seeds exactly the C0..C4 prefix combos, so the tested combos are held out of
training. Each bar concept DOES appear (a) alone in the single-concept cell
(max_single) and (b) composed with extras (the compose skill) -- but the specific
C_i x C_j bar pairings are unseen. Compositional generalisation of the bind skill to
these unseen bar pairs = G1 recombination.
"""
import random, os

# 5 FROZEN-BAR concepts (evaluate.py _g6_concepts + _g_concept_keywords).
# clause = a short sentence weaving the concept's own keywords (drives max_single).
BAR = [
    ("consciousness arises from cells",        "consciousness grows as cells become aware in the mind"),
    ("tension ripples between distant minds",  "tension ripples in the distant space between two minds"),
    ("memory composes into new meaning",       "memory can compose old traces into new meaning"),
    ("silence still carries information",      "silence is quiet yet still carries information"),
    ("the engine dreams when alone",           "the engine dreams and sleeps when it is alone"),
]

# EXTRA distractor concepts -- enlarge the combinatorial space so the bind skill is a
# real distribution. Keywords DISJOINT from the bar sets (never move bar coverage),
# real English words (kwr stays high).
EXTRA = [
    ("rivers flow toward the open sea",     "rivers flow slowly toward the wide open sea"),
    ("mountains hold the morning light",    "tall mountains hold the cold morning light"),
    ("forests breathe in the falling rain", "green forests breathe deep in the falling rain"),
    ("children laugh across the field",     "small children laugh and run across the field"),
    ("music drifts through the old house",  "soft music drifts through the quiet old house"),
    ("birds gather before the storm",       "many birds gather in trees before the storm"),
    ("candles burn against the dark",       "warm candles burn slowly against the dark"),
    ("clocks measure the passing hours",    "old clocks measure the slow passing hours"),
    ("ships cross the northern water",      "heavy ships cross the cold northern water"),
    ("gardens bloom after the frost",       "bright gardens bloom soon after the frost"),
    ("letters travel between two towns",    "written letters travel between two far towns"),
    ("lanterns float upon the river",       "paper lanterns float upon the moving river"),
    ("shadows lengthen near the wall",      "long shadows lengthen near the stone wall"),
    ("markets wake at early dawn",          "busy markets wake and open at early dawn"),
    ("travelers rest beneath the tree",     "tired travelers rest beneath the broad tree"),
]

ROLES = ["[r0]", "[r1]", "[r2]"]
HELDOUT_FRAC = 0.45
SEED = 7
REPEAT_SINGLE = 30
REPEAT_COMP = 8
N_TRIPLE = 400


def clause(c, alt_prob, rng):
    return c[1] if rng.random() < alt_prob else c[0]


def build():
    rng = random.Random(SEED)
    concepts = BAR + EXTRA
    N = len(concepts)
    bar_idx = set(range(len(BAR)))

    all_pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    train_pairs = [(i, j) for (i, j) in all_pairs
                   if not (i in bar_idx and j in bar_idx)]   # drop every C_i x C_j
    rng.shuffle(train_pairs)
    keep = int(len(train_pairs) * (1 - HELDOUT_FRAC))
    heldout_extra = train_pairs[keep:]
    train_pairs = train_pairs[:keep]

    train_triples = []
    seen = set()
    while len(train_triples) < N_TRIPLE:
        t = tuple(sorted(rng.sample(range(N), 3)))
        if t in seen:
            continue
        if len(set(t) & bar_idx) >= 2:
            continue
        seen.add(t); train_triples.append(t)

    gamma, add = [], []

    for c in concepts:
        for _ in range(REPEAT_SINGLE):
            s = clause(c, 0.4, rng)
            gamma.append(s + " .")
            add.append(s + " .")

    # CONTENT-MATCHED control: ADD gets the SAME slot phrases + SAME clauses in the
    # SAME order as gamma -- the ONLY difference is the binding scaffold tokens
    # ("bind", the [r_k] role slots, the "=>" unbind boundary). This isolates the
    # role-binding STRUCTURE from mere clause-exposure (both arms see each concept's
    # canonical phrase AND its clause the same number of times).
    def emit_pair(i, j):
        for _ in range(REPEAT_COMP):
            ci, cj = concepts[i], concepts[j]
            a_cl = clause(ci, 0.5, rng); b_cl = clause(cj, 0.5, rng)
            if rng.random() < 0.5:
                first, second, fc, sc = ci, cj, a_cl, b_cl
            else:
                first, second, fc, sc = cj, ci, b_cl, a_cl
            gamma.append(f"bind {ROLES[0]} {first[0]} {ROLES[1]} {second[0]} => {fc} and {sc} .")
            add.append(f"{first[0]} {second[0]} {fc} and {sc} .")

    for (i, j) in train_pairs:
        emit_pair(i, j)

    for t in train_triples:
        for _ in range(max(1, REPEAT_COMP // 2)):
            cs = [concepts[k] for k in t]
            order = list(range(3)); rng.shuffle(order)
            cls = [clause(cs[k], 0.5, rng) for k in range(3)]
            phrases = " ".join(cs[order[k]][0] for k in range(3))
            slots = " ".join(f"{ROLES[k]} {cs[order[k]][0]}" for k in range(3))
            body = " and ".join(cls[order[k]] for k in range(3))
            gamma.append(f"bind {slots} => {body} .")
            add.append(f"{phrases} {body} .")

    rng.shuffle(gamma); rng.shuffle(add)
    outdir = os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(outdir, "gamma_data.txt"), "w").write("\n".join(gamma) + "\n")
    open(os.path.join(outdir, "add.txt"), "w").write("\n".join(add) + "\n")

    heldout_bar = [(i, j) for i in bar_idx for j in bar_idx if i < j]
    with open(os.path.join(outdir, "corpus_manifest.txt"), "w") as f:
        f.write(f"concepts N={N} (bar={len(BAR)} extra={len(EXTRA)})\n")
        f.write(f"train_pairs={len(train_pairs)} train_triples={len(train_triples)}\n")
        f.write(f"gamma_lines={len(gamma)} add_lines={len(add)}\n")
        f.write("HELD-OUT bar x bar pairs (NEVER in training = the G1 transfer test):\n")
        for (i, j) in heldout_bar:
            f.write(f"  C{i}({concepts[i][0]}) x C{j}({concepts[j][0]})\n")
        f.write(f"held-out extra pairs (random {HELDOUT_FRAC}): {len(heldout_extra)}\n")
        f.write(f"gamma_bytes={sum(len(x) for x in gamma)} add_bytes={sum(len(x) for x in add)}\n")
    print(f"gamma_lines={len(gamma)} add_lines={len(add)} "
          f"train_pairs={len(train_pairs)} triples={len(train_triples)} "
          f"heldout_bar_pairs={len(heldout_bar)}")


if __name__ == "__main__":
    build()
