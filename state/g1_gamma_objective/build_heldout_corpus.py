#!/usr/bin/env python3
"""build_heldout_corpus.py — held-out compositional split byte-corpus for the γ
recomb-objective (DESIGN §(b)). Emits a raw UTF-8 byte file that cli/train.py's
ByteCell reads directly (V=256 mouth), plus a sidecar JSON with the SEEN/HELD split
+ per-window pair metadata (A/B/D keyword bytes) the recomb-objective consumes.

DISJOINT-VOCAB INVARIANT (false-GREEN guard, DESIGN §(b)): the concept vocabulary here
MUST NOT overlap the anima G1 metric's 5 concepts (evaluate.py _g_concept_keywords:
consciousness/cells·tension/ripple·memory/meaning·silence/information·dream/engine).
The anima G1 bar stays a pure TRANSFER test never seen in training. A guard asserts ∅.

⚠️ DESIGN ARTIFACT. cheap (CPU, mini-ok). Run as the first cost-gated follow-on step.
"""
from __future__ import annotations
import json, os, argparse
import numpy as np

# ── disjoint concept vocab (32 concepts × 4 keywords). NONE overlaps the anima G1 5. ──
# natural-world / motion / emotion domains, deliberately away from anima's consciousness set.
CONCEPTS = {
    "river":   ["river", "current", "flow", "delta"],
    "mountain":["mountain", "peak", "ridge", "summit"],
    "forest":  ["forest", "canopy", "grove", "thicket"],
    "desert":  ["desert", "dune", "sand", "arid"],
    "ocean":   ["ocean", "tide", "wave", "abyss"],
    "storm":   ["storm", "thunder", "lightning", "gale"],
    "ember":   ["ember", "flame", "spark", "cinder"],
    "frost":   ["frost", "ice", "chill", "glacier"],
    "meadow":  ["meadow", "grass", "bloom", "clover"],
    "cavern":  ["cavern", "cave", "hollow", "grotto"],
    "harbor":  ["harbor", "dock", "pier", "wharf"],
    "orchard": ["orchard", "apple", "harvest", "blossom"],
    "falcon":  ["falcon", "hawk", "talon", "swoop"],
    "otter":   ["otter", "sleek", "dive", "holt"],
    "beetle":  ["beetle", "carapace", "burrow", "chitin"],
    "willow":  ["willow", "branch", "weep", "sway"],
    "copper":  ["copper", "patina", "wire", "verdigris"],
    "marble":  ["marble", "vein", "chisel", "polish"],
    "lantern": ["lantern", "glow", "wick", "flicker"],
    "compass": ["compass", "needle", "bearing", "north"],
    "anchor":  ["anchor", "chain", "moor", "ballast"],
    "loom":    ["loom", "weave", "thread", "shuttle"],
    "kiln":    ["kiln", "fire", "clay", "glaze"],
    "quarry":  ["quarry", "stone", "hew", "slab"],
    "gale":    ["squall", "bluster", "howl", "sweep"],
    "brook":   ["brook", "trickle", "pebble", "babble"],
    "thicket": ["bramble", "briar", "tangle", "hedge"],
    "prairie": ["prairie", "plain", "expanse", "range"],
    "fjord":   ["fjord", "inlet", "cliff", "narrows"],
    "reef":    ["reef", "coral", "shoal", "atoll"],
    "tundra":  ["tundra", "permafrost", "lichen", "bleak"],
    "vale":    ["vale", "valley", "glen", "dell"],
}

# anima G1 metric's concept keywords — the DISJOINT guard set (must not intersect).
ANIMA_G1_KW = {"consciousness","cells","mind","aware","tension","ripple","distant","between",
               "memory","meaning","compose","new","silence","information","quiet","carries",
               "dream","engine","alone","sleep"}

TEMPLATES = [
    "if {A}, then {B}: {C}.",
    "when {A}, {B} follows and {C}.",
    "{A}. therefore {B}. {C}.",
    "given {A} and {B}, {C}.",
]


def _guard_disjoint():
    allkw = {k for kws in CONCEPTS.values() for k in kws}
    overlap = allkw & ANIMA_G1_KW
    assert not overlap, f"DISJOINT-VOCAB VIOLATED (false-GREEN risk): {overlap}"


def phrase(name):        # a concept's descriptive seed phrase
    kw = CONCEPTS[name]
    return f"the {kw[0]} {kw[1]}"


def compose(a, b):       # NOVEL relation joining A & B keywords (the recombination target)
    ka, kb = CONCEPTS[a], CONCEPTS[b]
    return (f"the {ka[0]} {ka[2]} meets the {kb[0]} {kb[2]} so {ka[1]} and {kb[1]} "
            f"become one {ka[3]} {kb[3]}")


def build(out_bytes, out_meta, held_frac=0.15, reps=300, seed=7):
    _guard_disjoint()
    names = list(CONCEPTS)
    N = len(names)
    rng = np.random.default_rng(seed)
    pairs = [(a, b) for a in names for b in names if a != b]
    rng.shuffle(pairs)
    n_held = int(len(pairs) * held_frac)
    HELD = set(map(tuple, pairs[:n_held]))
    SEEN = [p for p in pairs if p not in HELD]

    lines, meta = [], []
    for _ in range(reps):
        # TRACK 1: PAIR-COMPOSED (SEEN pairs only — HELD compose sentences NEVER appear)
        for (a, b) in SEEN:
            c = compose(a, b)
            t = TEMPLATES[rng.integers(len(TEMPLATES))].format(A=phrase(a), B=phrase(b), C=c)
            lines.append(t)
            # distractor D ∉ {a,b} for the shuffle-control baseline
            d = names[rng.integers(N)]
            while d in (a, b):
                d = names[rng.integers(N)]
            meta.append({"line_kind": "composed", "a": a, "b": b, "d": d})
        # TRACK 2: SINGLETON (every concept individually seen — incl. HELD concepts)
        for a in names:
            kw = CONCEPTS[a]
            lines.append(f"{phrase(a)}. {kw[0]} means {kw[1]}.")
            meta.append({"line_kind": "singleton", "a": a})
    # (TRACK 3 register anchor is added at TRAIN time via extra --corpus cells, DESIGN §(b))

    order = rng.permutation(len(lines))
    text = "\n".join(lines[i] for i in order) + "\n"
    with open(out_bytes, "wb") as f:
        f.write(text.encode("utf-8"))
    split = {
        "n_concepts": N, "held_frac": held_frac, "n_pairs": len(pairs),
        "n_held": len(HELD), "n_seen": len(SEEN), "seed": seed,
        "HELD": sorted(list(HELD)), "SEEN": SEEN,
        "concepts": CONCEPTS, "disjoint_from_anima_g1": True,
        "note": "TRACK1 composed(SEEN only) + TRACK2 singleton(all). HELD pair compose "
                "sentences absent → held-out systematic-generalization test. "
                "byte-window pair_ctx (A/B/D keyword bytes) derived at train time from "
                "the composed-line boundary; see recomb_objective.py.",
    }
    with open(out_meta, "w") as f:
        json.dump(split, f, ensure_ascii=False, indent=2)
    print(f"[built] {out_bytes} bytes={os.path.getsize(out_bytes)}  "
          f"concepts={N} seen={len(SEEN)} held={len(HELD)}  meta={out_meta}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-bytes", default="state/g1_gamma_objective/heldout_composed.bytes")
    ap.add_argument("--out-meta",  default="state/g1_gamma_objective/heldout_split.json")
    ap.add_argument("--held-frac", type=float, default=0.15)
    ap.add_argument("--reps", type=int, default=300)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    build(a.out_bytes, a.out_meta, a.held_frac, a.reps, a.seed)
