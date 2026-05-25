#!/usr/bin/env python3
"""RESEARCH.md §43 — L8 routing-via-relation: fingerprint builder.

Reformulates ROUTING (the §16 axis1 single-anchor pick) as fingerprint
prediction + 1-NN lookup. The fingerprint of an anchor X is the stacked
encoded vector of its four §37/§33-L6 relation primitives R1-R4 to every
OTHER anchor in the 64-anchor SSOT. That is, anchor X's identity =
its relation profile to the rest of the landscape — anima OWN physics
(coord, radius, dom, tier), NO external knowledge graph, NO LLM, NO
surface text.

Routing-via-relation contract:
  1. fingerprint(X) = vector(R1(X,Y), R2(X,Y), R3(X,Y), R4(X,Y))
                      over all Y != X, in fixed tier-sorted order.
     dim = 63 * 4 = 252 categorical labels per anchor.
  2. lookup(query_fingerprint) = argmin_X  Euclidean distance between
     query and table[X] (one-hot encoded labels).
  3. routing decision falls out of (1) and (2), deterministic.
  4. anima's task at FIRE time: predict fingerprint(X) from anima's own
     state when prompted about X. The byte → 🛸X surface routing token
     is then a closed-form deterministic 1-NN lookup, NOT a memorised
     string.

This file = the FINGERPRINT TABLE BUILDER. It imports the §37 relation
primitives R1-R4 by direct path (anima OWN physics SSOT) and emits a
deterministic 64 x 252 fingerprint matrix + identity-lookup function.

NO external KG, NO LLM. Deterministic — no SGD, no RNG. Pure-fn over the
§16 / §37 anchor SSOT. Output: fingerprint_table.json (the closed-form
artefact) and a verify_distinguishable() check (B-S43-4).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Import §37 relation primitives via direct path (sibling state dir is
# read-only and on the same anima repo). This keeps the relation SSOT
# single-source-of-truth and AST-traceable for B-S43-3.
S37_DIR = HERE.parent / "l6_pilot_s37_2026_05_18"
RELATION_CORPUS = S37_DIR / "relation_corpus.py"
assert RELATION_CORPUS.exists(), f"missing §37 SSOT: {RELATION_CORPUS}"

_spec = importlib.util.spec_from_file_location("rc_s37", RELATION_CORPUS)
_rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rc)

S8_ANCHORS = _rc.S8_ANCHORS                 # 64-anchor SSOT
RELATION_LABEL_SET = _rc.RELATION_LABEL_SET # closed finite set, |·| = 12
r1_proximity = _rc.r1_proximity
r2_basin = _rc.r2_basin
r3_domain = _rc.r3_domain
r4_tier = _rc.r4_tier

assert len(S8_ANCHORS) == 64, len(S8_ANCHORS)


# Each relation has its own closed label codomain (same as §37 RELATIONS).
R1_LABELS = ["near", "mid", "far"]                                 # |=3
R2_LABELS = ["i_contains_j", "j_contains_i", "overlap", "disjoint"]# |=4
R3_LABELS = ["same_domain", "different_domain"]                    # |=2
R4_LABELS = ["i_shallower", "i_deeper", "i_eq_j"]                  # |=3

# Per-pair one-hot encoding dim per relation; total per (X,Y) = 12
_PER_PAIR_DIM = len(R1_LABELS) + len(R2_LABELS) + len(R3_LABELS) + len(R4_LABELS)
assert _PER_PAIR_DIM == 12, _PER_PAIR_DIM
# Fingerprint dim per anchor = 63 partners * 12 labels = 756 one-hot floats
FINGERPRINT_DIM = 63 * _PER_PAIR_DIM
assert FINGERPRINT_DIM == 756, FINGERPRINT_DIM


def _one_hot(label: str, labels: list[str]) -> list[int]:
    return [1 if label == L else 0 for L in labels]


def _anchor_order() -> list[int]:
    """Stable tier-sorted ordering of all 64 anchor indices. The
    fingerprint format ALWAYS uses this same order for the 63 partners,
    so two anchors' fingerprints are comparable element-wise (B-S43-1).
    """
    pairs = sorted(range(len(S8_ANCHORS)), key=lambda i: S8_ANCHORS[i][0])
    return pairs


def build_fingerprint(x_idx: int, order: list[int]) -> list[int]:
    """anchor X's fingerprint = R1..R4 (one-hot) to every other anchor Y,
    Y in tier-sorted order, Y != X. Deterministic pure-fn of S8_ANCHORS.
    Returns a flat list of FINGERPRINT_DIM = 756 ints in {0,1}.
    """
    X = S8_ANCHORS[x_idx]
    out: list[int] = []
    for y_idx in order:
        if y_idx == x_idx:
            continue
        Y = S8_ANCHORS[y_idx]
        out.extend(_one_hot(r1_proximity(X, Y), R1_LABELS))
        out.extend(_one_hot(r2_basin(X, Y),     R2_LABELS))
        out.extend(_one_hot(r3_domain(X, Y),    R3_LABELS))
        out.extend(_one_hot(r4_tier(X, Y),      R4_LABELS))
    assert len(out) == FINGERPRINT_DIM, len(out)
    return out


def build_table() -> dict:
    """Build the 64 x 756 fingerprint table. Deterministic.
    Returns a JSON-serialisable dict with table, tiers, order, sha256."""
    order = _anchor_order()
    tiers = [S8_ANCHORS[i][0] for i in order]
    # one fingerprint per anchor (anchor's row in the table)
    fps: list[list[int]] = []
    for x_idx in range(len(S8_ANCHORS)):
        fps.append(build_fingerprint(x_idx, order))

    # canonical JSON for sha256
    canonical = json.dumps({
        "order_tiers": tiers,
        "fingerprint_dim": FINGERPRINT_DIM,
        "table": fps,
    }, ensure_ascii=False, sort_keys=True).encode("utf-8")
    sha = hashlib.sha256(canonical).hexdigest()

    return {
        "n_anchors": len(S8_ANCHORS),
        "fingerprint_dim": FINGERPRINT_DIM,
        "per_pair_dim": _PER_PAIR_DIM,
        "n_partners_per_anchor": 63,
        "order_tiers": tiers,
        "anchor_tiers": [S8_ANCHORS[i][0] for i in range(len(S8_ANCHORS))],
        "table": fps,
        "table_sha256": sha,
    }


def euclidean_sq(u: list[int], v: list[int]) -> int:
    """Squared L2 between two one-hot vectors — integer arithmetic, NO
    floating point. For one-hot vectors of equal dim, ‖u-v‖² is an
    integer in [0, 2*FINGERPRINT_DIM/PER_PAIR_DIM] (each disagreeing
    one-hot adds exactly 2). Deterministic, no RNG."""
    s = 0
    for a, b in zip(u, v):
        d = a - b
        s += d * d
    return s


def lookup_identity(query: list[int], table: list[list[int]]) -> tuple[int, int]:
    """1-NN argmin over the table — returns (anchor_idx, distance_sq).
    Closed-form Euclidean. Deterministic tie-break = lowest anchor_idx."""
    best_idx, best_d = -1, 10**18
    for idx, row in enumerate(table):
        d = euclidean_sq(query, row)
        if d < best_d:
            best_d, best_idx = d, idx
    return best_idx, best_d


def verify_self_lookup(table: list[list[int]]) -> tuple[bool, int]:
    """For each anchor X, lookup_identity(table[X]) must return X (since
    table[X] is at distance 0 from itself, and all other table rows are
    >0 away — by pairwise-distinct fingerprints, B-S43-4). Returns
    (all_match, n_match)."""
    n_match = 0
    for x, row in enumerate(table):
        idx, dsq = lookup_identity(row, table)
        if idx == x and dsq == 0:
            n_match += 1
    return n_match == len(table), n_match


def pairwise_distinct(table: list[list[int]]) -> tuple[bool, int, int]:
    """All C(64, 2) = 2016 pairs of fingerprints distinct.
    Returns (all_distinct, n_distinct_pairs, min_pair_distance_sq)."""
    n = len(table)
    distinct_pairs = 0
    min_d = 10**18
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_sq(table[i], table[j])
            if d > 0:
                distinct_pairs += 1
            if d < min_d:
                min_d = d
    total = n * (n - 1) // 2
    return (distinct_pairs == total), distinct_pairs, min_d


def main() -> int:
    art = build_table()

    # B-S43-4 verification surfaces (closed-form Boolean checks).
    fps = art["table"]
    all_self_ok, n_self = verify_self_lookup(fps)
    all_distinct, n_distinct_pairs, min_pair_d = pairwise_distinct(fps)
    total_pairs = 64 * 63 // 2

    art_out = {k: art[k] for k in
               ("n_anchors", "fingerprint_dim", "per_pair_dim",
                "n_partners_per_anchor", "order_tiers", "anchor_tiers",
                "table_sha256")}
    art_out["table_summary"] = {
        "self_lookup_all_match": all_self_ok,
        "self_lookup_n_match": n_self,
        "pairwise_distinct_all": all_distinct,
        "pairwise_distinct_count": n_distinct_pairs,
        "pairwise_total": total_pairs,
        "min_pairwise_distance_sq": min_pair_d,
    }

    (HERE / "fingerprint_table.json").write_text(
        json.dumps({"meta": art_out,
                    "table": fps}, ensure_ascii=False, indent=2))
    (HERE / "fingerprint_table_meta.json").write_text(
        json.dumps(art_out, ensure_ascii=False, indent=2))

    print(json.dumps(art_out, ensure_ascii=False, indent=2))
    print(f"\n[§43] fingerprint_dim={art['fingerprint_dim']} sha256="
          f"{art['table_sha256'][:16]}…  self-lookup {n_self}/64  "
          f"pairwise-distinct {n_distinct_pairs}/{total_pairs}  "
          f"min_pair_d²={min_pair_d}")
    return 0 if (all_self_ok and all_distinct) else 1


if __name__ == "__main__":
    sys.exit(main())
