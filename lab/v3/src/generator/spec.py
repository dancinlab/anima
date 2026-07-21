"""The frozen GenSpec — the synthetic language's entire definition.

Every stem and affix is STORED, not regenerated from a seed at use time: a spec
that regenerates is a spec that silently changes when the code changes. The spec
is serialized to JSON and hashed; the hash goes in the H_003 card, which is what
bounds the designer's freedom to shop for a stream that flatters F1
(`rig-corpus-frozen-params`).

Deterministic, stdlib only.
"""

from __future__ import annotations

import hashlib
import json
import random

from lang import compose, render

MASTER_SEED = 20260716

# Restricted inventories keep stems pronounceable-ish and, more importantly,
# keep the jamo alphabet small enough that BPE merges are interpretable.
STEM_LEADS = [0, 2, 3, 5, 6, 7, 9, 11, 12, 14, 16, 17, 18]   # 13
STEM_VOWELS = [0, 4, 8, 13, 18, 20]                          # 6
STEM_TAILS = [0, 1, 4, 8, 16, 17, 21]                        # 7 (0 = open syllable)

N_STEMS = 512
N_HELDOUT_STEMS = 128
N_AFFIX_P1 = 64
N_NEG_P1 = 4          # >= 4 NEG allomorphs in phase 1
N_CARRIED = 52        # phase-2 affixes carried over from phase 1
N_NOVEL_NEG = 12      # phase-2 NOVEL NEG-class allomorphs — the drift
PHASE_BYTES = [150_000_000, 150_000_000]   # matched halves of the ~300MB budget
ZIPF_S = 1.07
P2_SHIFT = 0.45       # fraction of collocation mass reassigned in phase 2


def _syllable(rng: random.Random) -> str:
    return compose(rng.choice(STEM_LEADS), rng.choice(STEM_VOWELS), rng.choice(STEM_TAILS))


def _make_stems(rng: random.Random) -> list:
    """N_STEMS distinct stems of 2-4 syllables. Sorted before return so the spec
    never depends on set iteration order (invariant 7)."""
    seen = set()
    while len(seen) < N_STEMS:
        n_syl = rng.choice([2, 2, 3, 3, 4])
        seen.add("".join(_syllable(rng) for _ in range(n_syl)))
    return sorted(seen)


def _make_affixes(rng: random.Random, n: int, cls: str, slot: int, taken: set,
                  syllables=(1, 1, 2)) -> list:
    """n distinct BOUND affixes in class `cls`, each `syllables` long (a choice list).

    `syllables` controls the length distribution. The NOVEL NEG allomorphs use
    (2, 2) — >= 2 syllables (>= 6 jamo) — because a 1-syllable affix is only 2-3
    jamo and its individual jamo recur so widely across unrelated words that the
    FROZEN codec atomizes it by coincidence, destroying the N-2 contrast
    (`rig-atomicity-not-induced`). Measured: shortening a novel affix to 2 jamo
    lets the phase-1 codec read it single-token even though it never saw it. A
    >= 6-jamo affix cannot be fused by accident — it must be earned by frequency,
    which only the phase-2 refit sees.
    """
    out = []
    while len(out) < n:
        form = "".join(_syllable(rng) for _ in range(rng.choice(syllables)))
        if form in taken:
            continue
        taken.add(form)
        out.append({"form": form, "cls": cls, "slot": slot})
    return sorted(out, key=lambda a: a["form"])


def build_spec() -> dict:
    """Construct the spec deterministically from MASTER_SEED.

    All randomness descends from one `random.Random(MASTER_SEED)`; there is no
    other entropy source in this package.
    """
    rng = random.Random(MASTER_SEED)
    stems = _make_stems(rng)
    heldout = sorted(rng.sample(stems, N_HELDOUT_STEMS))

    taken: set = set()
    neg_p1 = _make_affixes(rng, N_NEG_P1, "NEG", 1, taken)
    plain_p1 = _make_affixes(rng, N_AFFIX_P1 - N_NEG_P1, "PLAIN", 0, taken)
    affixes_p1 = sorted(neg_p1 + plain_p1, key=lambda a: (a["cls"], a["form"]))

    # Phase 2: carry a subset forward, rotate in NOVEL NEG allomorphs. The novel
    # forms are the drift the codec must track — absent from the phase-1 merge
    # table by construction, which is what makes the frozen arm a local C1 on
    # exactly the material the eval looks at (`rig-drift-wasting-asset`).
    carried = sorted(rng.sample(affixes_p1, N_CARRIED), key=lambda a: (a["cls"], a["form"]))

    # Novel NEG allomorphs as DONOR PAIRS (H_004 reframing fix): each novel form is
    # the concatenation of two DISTINCT 1-syllable carried PLAIN affixes. Two
    # consequences make the frozen arm a valid no-atomicity control:
    #   (1) the frozen (phase-1) codec can NEVER fuse the whole pair — the two
    #       affixes never occur adjacent in phase 1 (one affix per body), so no
    #       (a_i, a_j) merge exists → atomicity deficit 1.0 is GUARANTEED, not
    #       sampled; the >=2-syllable length hack is no longer needed.
    #   (2) every sub-token is a real PLAIN affix that also appears in plain
    #       bodies, so the class is NOT readable from any single fragment — the
    #       order-1 (last-token) shortcut that invalidated the disjoint-inventory
    #       design is broken. Only the WHOLE (atomic) token, or an order-2 bigram,
    #       carries NEG. See `verification-h004` / `rig-pilot-frozen-control-invalid`.
    plain_1syl = sorted(a["form"] for a in plain_p1 if len(a["form"]) == 1)
    if len(plain_1syl) < 2 * N_NOVEL_NEG:
        raise ValueError(
            f"need {2 * N_NOVEL_NEG} one-syllable plain donors, have {len(plain_1syl)}")
    donors = rng.sample(plain_1syl, 2 * N_NOVEL_NEG)
    novel_neg = []
    donor_set = set()
    for i in range(N_NOVEL_NEG):
        a, b = donors[2 * i], donors[2 * i + 1]
        novel_neg.append({"form": a + b, "cls": "NEG", "slot": 1})
        donor_set.update((a, b))
    novel_neg = sorted(novel_neg, key=lambda a: a["form"])
    affixes_p2 = sorted(carried + novel_neg, key=lambda a: (a["cls"], a["form"]))

    # Zipf collocation weights over stems; phase 2 reassigns P2_SHIFT of the mass.
    ranks = list(range(1, len(stems) + 1))
    w1 = [1.0 / (r ** ZIPF_S) for r in ranks]
    total = sum(w1)
    w1 = [w / total for w in w1]
    perm = list(range(len(stems)))
    rng.shuffle(perm)
    w2 = [(1.0 - P2_SHIFT) * w1[i] + P2_SHIFT * w1[perm[i]] for i in range(len(stems))]
    t2 = sum(w2)
    w2 = [w / t2 for w in w2]

    drilled = sorted(s for s in stems if s not in set(heldout))

    return {
        "version": "h003-genspec",
        "seed": MASTER_SEED,
        "stems": stems,
        "heldout_stems": heldout,
        "drilled_stems": drilled,
        "affixes_p1": affixes_p1,
        "affixes_p2": affixes_p2,
        "novel_neg_forms": sorted(a["form"] for a in novel_neg),
        "donor_plains": sorted(donor_set),   # the 24 plain affixes used to build novel NEG pairs
        "neg_p1_forms": sorted(a["form"] for a in neg_p1),
        "colloc": {"zipf_s": ZIPF_S, "p2_shift": P2_SHIFT, "w1": w1, "w2": w2},
        "phase_bytes": PHASE_BYTES,
    }


def spec_hash(spec: dict) -> str:
    """sha256 of the canonical serialization — the number that goes in the card."""
    blob = json.dumps(spec, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def neg_forms(spec: dict, phase: int) -> list:
    src = spec["affixes_p1"] if phase == 1 else spec["affixes_p2"]
    return sorted(a["form"] for a in src if a["cls"] == "NEG")


def plain_forms(spec: dict, phase: int) -> list:
    src = spec["affixes_p1"] if phase == 1 else spec["affixes_p2"]
    return sorted(a["form"] for a in src if a["cls"] == "PLAIN")


if __name__ == "__main__":
    s = build_spec()
    print("spec_hash:", spec_hash(s))
    print("stems:", len(s["stems"]), "· heldout:", len(s["heldout_stems"]),
          "· drilled:", len(s["drilled_stems"]))
    print("affixes_p1:", len(s["affixes_p1"]), "· NEG:", len(neg_forms(s, 1)))
    print("affixes_p2:", len(s["affixes_p2"]), "· NEG:", len(neg_forms(s, 2)),
          "· novel NEG:", len(s["novel_neg_forms"]))
    print("sample render:", render(s["stems"][0], [neg_forms(s, 1)[0]]))
