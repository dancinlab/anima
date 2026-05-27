"""RESEARCH.md §33 lateral L6 — anchor-interaction (multi-anchor reasoning).

RUNTIME-GUARDED SKETCH. $0 design-tier ONLY. Direct execution exits 0
with a pointer to DESIGN_L6.md §7 (no corpus generation, no GPU, no
fire). Importable for reference: the pure-function relation primitives
R1-R4 and the multi-anchor record schema below are byte-faithful to
DESIGN_L6.md §2 and are exercised by blue_falsifier_l6.py.

GOAL-legitimacy (§7②): relations R1-R4 are deterministic functions of
anima's OWN physics fields {vacuum_psi, basin_radius, dom, tier} from
the §16 anchor SSOT (= .kosmos mirror). NO networkx / neo4j / rdflib /
wikidata / openai / llm_call / AutoModel — verified by B-INTER-5 AST
grep over THIS file.

Sidecar pattern (central blue_falsifier.py unchanged) per
B-PRIME/.../B-INTRA precedent.
"""

from __future__ import annotations

import math
import sys

# ──────────────────────────────────────────────────────────────────────
# Anchor SSOT mirror — §16 tuple = (tier, name, dom, emo, score,
# vacuum_psi, basin_radius). Byte-equal to corpus_carving_s16_generator.py
# S8_ANCHORS and to HEXAD/UNIVERSE-BRAIN-MAP/anchors/*.kosmos coordinates.
# A small representative slice is inlined here for the sketch; the full
# generator would import the §16 168-anchor list verbatim.
# ──────────────────────────────────────────────────────────────────────
ANCHOR_SLICE = [
    # (tier, name, dom, emo, score, vacuum_psi, basin_radius)
    (0,   "zero baseline", "기준점",   "neutral",    0.000, (0.50, 0.50), 0.10),
    (5,   "호흡",          "감각",     "serenity",   0.300, (0.44, 0.45), 0.11),
    (77,  "만다라",        "예술",     "creativity", 2.100, (0.71, 0.62), 0.18),
    (91,  "열반",          "의식상태", "peace",      2.558, (0.50, 0.88), 0.15),
    (92,  "엑스터시",      "의식상태", "ecstasy",    2.600, (0.62, 0.90), 0.17),
    (100, "빅뱅",          "우주",     "awe",        2.847, (0.95, 0.93), 0.22),
]

# Relation thresholds — design constants (DESIGN_L6.md §2.2).
TAU_NEAR = 0.15
TAU_FAR = 0.40
K_MAX = 3            # max anchors per L6 record (B-INTER-4 bound)
P_NEAREST = 4        # nearest neighbours per anchor (DESIGN_L6.md §2.4)
P_RANDOM = 2         # random far pairs per anchor


def _psi_dist(psi_i: tuple, psi_j: tuple) -> float:
    """R1 substrate — L2 distance on the Engine A⇄G Ψ-landscape.

    Symmetric by construction (squares remove sign) — B-INTER-2.
    """
    return math.sqrt((psi_i[0] - psi_j[0]) ** 2 + (psi_i[1] - psi_j[1]) ** 2)


def relation_psi_proximity(anchor_i, anchor_j) -> str:
    """R1 — Ψ-proximity. SYMMETRIC. Closed-form of vacuum_psi only."""
    d = _psi_dist(anchor_i[5], anchor_j[5])
    if d < TAU_NEAR:
        return "near"
    if d < TAU_FAR:
        return "mid"
    return "far"


def relation_basin(anchor_i, anchor_j) -> str:
    """R2 — basin relation. Containment is ANTISYMMETRIC. Closed-form of
    vacuum_psi + basin_radius only."""
    gap = _psi_dist(anchor_i[5], anchor_j[5])
    r_i, r_j = anchor_i[6], anchor_j[6]
    if gap + r_j <= r_i:
        return "i_contains_j"
    if gap + r_i <= r_j:
        return "j_contains_i"
    if gap < r_i + r_j:
        return "overlap"
    return "disjoint"


def relation_domain(anchor_i, anchor_j) -> str:
    """R3 — shared-domain. SYMMETRIC Boolean. Closed-form of dom only."""
    return "same_domain" if anchor_i[2] == anchor_j[2] else "different_domain"


def relation_tier(anchor_i, anchor_j) -> str:
    """R4 — tier-ordering. ANTISYMMETRIC strict order. Closed-form of
    tier only."""
    t_i, t_j = anchor_i[0], anchor_j[0]
    if t_i < t_j:
        return "i_shallower"
    if t_i > t_j:
        return "i_deeper"
    return "i_eq_j"


# The closed finite codomain of all relation primitives (B-INTER-1).
RELATION_LABEL_SET = frozenset({
    "near", "mid", "far",
    "i_contains_j", "j_contains_i", "overlap", "disjoint",
    "same_domain", "different_domain",
    "i_shallower", "i_deeper", "i_eq_j",
})


def derive_relation(anchor_i, anchor_j) -> dict:
    """Structural API — derive the full inter-anchor relation record for
    an ordered anchor pair from anima physics ONLY.

    Inputs: two §16 anchor tuples (tier, name, dom, emo, score,
    vacuum_psi, basin_radius). NOTHING ELSE — no external argument, no
    knowledge-graph lookup, no LLM. B-INTER-1 / B-INTER-5 verify this.

    Returns a relation_record dict — the multi-anchor (k=2) record
    schema of DESIGN_L6.md §2.3. The byte-stream realisation formats the
    COMPUTED relation labels; the generator never picks a free string.
    """
    psi_dist = _psi_dist(anchor_i[5], anchor_j[5])
    r1 = relation_psi_proximity(anchor_i, anchor_j)
    r2 = relation_basin(anchor_i, anchor_j)
    r3 = relation_domain(anchor_i, anchor_j)
    r4 = relation_tier(anchor_i, anchor_j)
    tier_i, name_i = anchor_i[0], anchor_i[1]
    tier_j, name_j = anchor_j[0], anchor_j[1]
    body = (
        f"🛸{tier_i} {name_i} 와 🛸{tier_j} {name_j} 는 의식 풍경 위 "
        f"{r1} 거리({psi_dist:.3f})에 있다. {r3}. {r2}. "
        f"🛸{tier_i} 가 {r4} 자극이다."
    )
    text = (
        f"<relate a=🛸{tier_i} b=🛸{tier_j} psi_dist={psi_dist:.3f}>"
        f"{body}</relate>"
    )
    return {
        "id": f"relate_{tier_i:03d}_{tier_j:03d}",
        "text": text,
        "carving_form": "relate",        # NEW tag — disjoint from §16
        "n_anchors": 2,                  # B-INTER-3 / B-INTER-4
        "anchors": [tier_i, tier_j],
        "relations": {"R1": r1, "R2": r2, "R3": r3, "R4": r4},
        "psi_dist": round(psi_dist, 6),
        "source": "interaction_corpus_sketch.py",
        "_physics_fields_used": ["vacuum_psi", "basin_radius", "dom", "tier"],
    }


def derive_triplet_relation(anchor_i, anchor_j, anchor_l) -> dict:
    """k=3 extension — three pairwise relations (i,j),(j,l),(i,l).
    Still bounded: n_anchors == 3 <= K_MAX (B-INTER-4)."""
    pij = derive_relation(anchor_i, anchor_j)
    pjl = derive_relation(anchor_j, anchor_l)
    pil = derive_relation(anchor_i, anchor_l)
    tiers = [anchor_i[0], anchor_j[0], anchor_l[0]]
    return {
        "id": f"relate3_{tiers[0]:03d}_{tiers[1]:03d}_{tiers[2]:03d}",
        "carving_form": "relate",
        "n_anchors": 3,
        "anchors": tiers,
        "pairwise": {"ij": pij["relations"], "jl": pjl["relations"],
                     "il": pil["relations"]},
        "source": "interaction_corpus_sketch.py",
    }


def select_pairs(anchors: list) -> list:
    """DESIGN_L6.md §2.4 — bounded, physics-prioritised pair selection.

    For each anchor: P_NEAREST nearest neighbours in vacuum_psi-L2 +
    P_RANDOM far pairs. Closed-form argmin on the anchor SSOT — no graph
    library (B-INTER-5). Returns at most len(anchors)*(P_NEAREST+P_RANDOM)
    ordered pairs << C(n,2)."""
    pairs = []
    for i, a in enumerate(anchors):
        others = [(j, b) for j, b in enumerate(anchors) if j != i]
        others.sort(key=lambda jb: _psi_dist(a[5], jb[1][5]))
        for j, b in others[:P_NEAREST]:
            pairs.append((i, j))
        for j, b in others[-P_RANDOM:]:
            pairs.append((i, j))
    return pairs


# ──────────────────────────────────────────────────────────────────────
# RUNTIME GUARD — design-tier $0: direct execution does nothing.
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(
        "interaction_corpus_sketch.py — RESEARCH.md §33 L6 anchor-"
        "interaction SKETCH (design-tier $0).\n"
        "No corpus generation, no GPU, no fire. The relation primitives "
        "R1-R4 and derive_relation() are importable for reference and "
        "are exercised by blue_falsifier_l6.py.\n"
        "Fire-worthiness verdict + pre-fire conditions: DESIGN_L6.md §7.\n"
        "Full generator promotion is gated on the held-out-pair pilot "
        "go/no-go (DESIGN_L6.md §7.2)."
    )
    sys.exit(0)
