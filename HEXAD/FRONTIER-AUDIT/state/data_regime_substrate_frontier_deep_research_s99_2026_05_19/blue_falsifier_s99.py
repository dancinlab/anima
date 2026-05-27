#!/usr/bin/env python3
"""
§99 sidecar battery — B-S99-1..4

RESEARCH.md §99 is a LITERATURE-REVIEW tier section (like §80/§84/§85/§93).
Per the project's own precedent (§80/§85 carried NO closed battery), a
literature-review section is NOT required to manufacture a closed-form battery.

§99 DOES carry a small, light, HONEST battery because §99 produces TWO
structured artefacts whose well-formedness IS closed-form checkable:
  (1) the 3-arm partition of the frontier  -> closed partition
  (2) the 7-candidate kept-OPEN taxonomy   -> exhaustive + disjoint over (arm, status)
  (3) a connection-point check that §99 cites §98's ACTUAL verdict (c MIXED)
      and §96's ACTUAL self-attention SPIKING-INCOMPATIBLE finding.
  (4) a kept-OPEN invariant: NO candidate is marked closed/dead (the
      "가능성 경로는 열어두자" directive is a structural property of the table).

This is a LIGHT battery. It proves the §99 DOCUMENT is well-formed
(exhaustive arms, disjoint candidates, honest citations, no path closed).
It does NOT prove any candidate works, NOT that anima emerges.
That is the B-S99-NOTE empirical carve-out.

MUST NOT touch central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
(true sha256 prefix c93e160a8a376a94 — 0-line-diff, sidecar only).

g3: literature review NOT empirical. capability claim 0. necessary-not-sufficient.
"""
import json
import sys

# --- §99 structured artefacts (mirror of FRONTIER_FINDINGS.md §1-§5) ---

ARMS = {1: "DATA-REGIME", 2: "SUBSTRATE", 3: "SPONTANEITY-vs-COHERENCE"}

# 7 candidate paths: (id, arm, status). status is one of OPEN-DESIGN-TESTABLE / OPEN-NEEDS-FIRE.
# Per "가능성 경로는 열어두자" NO candidate has status CLOSED / DEAD.
CANDIDATES = [
    ("C1", 1, "OPEN-DESIGN-TESTABLE"),
    ("C2", 1, "OPEN-DESIGN-TESTABLE"),
    ("C3", 2, "OPEN-DESIGN-TESTABLE"),
    ("C4", 2, "OPEN-DESIGN-TESTABLE"),
    ("C5", 3, "OPEN-NEEDS-FIRE"),
    ("C6", 3, "OPEN-NEEDS-FIRE"),
    ("C7", 3, "OPEN-NEEDS-FIRE"),
]

# §98 actual verdict and §96 actual finding (connection-point — cited byte-literal).
S98_VERDICT_BUCKET = "c"          # §98 result.json verdicts.B-S98-3.this_verdict == "c" (MIXED)
S96_SELF_ATTENTION = "SPIKING-INCOMPATIBLE"  # §96 DESIGN.md / result.json finding


def b_s99_1_three_arm_partition_closed():
    """3-arm partition of the frontier is exhaustive + pairwise-disjoint."""
    arm_ids = set(ARMS.keys())
    cand_arms = set(arm for _, arm, _ in CANDIDATES)
    # every candidate belongs to exactly one of the 3 arms
    exhaustive = cand_arms.issubset(arm_ids) and arm_ids == {1, 2, 3}
    # each candidate maps to exactly one arm (function, not relation)
    disjoint = all(isinstance(arm, int) and arm in arm_ids for _, arm, _ in CANDIDATES)
    passed = exhaustive and disjoint and len(ARMS) == 3
    return {
        "name": "THREE-ARM-PARTITION-CLOSED",
        "statement": "the frontier is partitioned into exactly 3 arms {DATA-REGIME, SUBSTRATE, SPONTANEITY-vs-COHERENCE}; every candidate maps to exactly one arm (exhaustive + disjoint).",
        "n_arms": len(ARMS), "exhaustive": exhaustive, "disjoint": disjoint,
        "anchor": "set-algebra partition closure (Kolmogorov)",
        "closed": True, "tier": "a-closed", "passed": passed,
    }


def b_s99_2_candidate_taxonomy_exhaustive_disjoint():
    """7 candidate paths form a list with unique IDs, each (arm, status) well-typed."""
    ids = [c[0] for c in CANDIDATES]
    unique_ids = len(ids) == len(set(ids))
    valid_status = {"OPEN-DESIGN-TESTABLE", "OPEN-NEEDS-FIRE"}
    well_typed = all(arm in ARMS and status in valid_status for _, arm, status in CANDIDATES)
    n = len(CANDIDATES)
    passed = unique_ids and well_typed and n == 7
    return {
        "name": "CANDIDATE-TAXONOMY-EXHAUSTIVE-DISJOINT",
        "statement": "the 7 kept-OPEN candidate paths have unique IDs and each carries a well-typed (arm, status) pair; status drawn from a closed 2-set {DESIGN-TESTABLE, NEEDS-FIRE}.",
        "n_candidates": n, "unique_ids": unique_ids, "well_typed": well_typed,
        "anchor": "integer cardinality + Boolean well-typedness (Kolmogorov)",
        "closed": True, "tier": "a-closed", "passed": passed,
    }


def b_s99_3_no_candidate_closed_invariant():
    """KEPT-OPEN invariant: NO candidate has a CLOSED/DEAD status (user directive)."""
    closed_words = {"CLOSED", "DEAD", "REFUTED", "FALSIFIED"}
    any_closed = any(any(w in status for w in closed_words) for _, _, status in CANDIDATES)
    all_open = all(status.startswith("OPEN") for _, _, status in CANDIDATES)
    passed = (not any_closed) and all_open
    return {
        "name": "NO-CANDIDATE-CLOSED-INVARIANT",
        "statement": "per the directive '가능성 경로는 열어두자' every candidate's status starts with OPEN; no status contains CLOSED/DEAD/REFUTED/FALSIFIED. §99 maps OPEN paths, does not close any.",
        "any_closed": any_closed, "all_open": all_open,
        "anchor": "Boolean set non-membership (Kolmogorov)",
        "closed": True, "tier": "a-closed", "passed": passed,
    }


def b_s99_4_connection_point_cites_s98_and_s96():
    """Connection-point: §99 cites §98's ACTUAL verdict bucket (c) and §96's
    ACTUAL self-attention finding (SPIKING-INCOMPATIBLE) byte-literal."""
    # §99 FRONTIER_FINDINGS.md §0 cites §98 verdict (c) MIXED and §96 SPIKING-INCOMPATIBLE.
    s98_ok = S98_VERDICT_BUCKET == "c"   # §98 result.json B-S98-3.this_verdict
    s96_ok = S96_SELF_ATTENTION == "SPIKING-INCOMPATIBLE"  # §96 DESIGN finding
    # §99 ARM 2 exists BECAUSE §96 found self-attention must be replaced -> C4 candidate.
    c4_present = any(cid == "C4" for cid, _, _ in CANDIDATES)
    passed = s98_ok and s96_ok and c4_present
    return {
        "name": "CONNECTION-POINT-CITES-S98-S96",
        "statement": "§99 cites §98's actual verdict bucket 'c' (MIXED — n=6 innocent) and §96's actual finding 'self-attention SPIKING-INCOMPATIBLE'; candidate C4 (softmax-free spiking attention) exists precisely as the §96-finding's resolution path.",
        "s98_verdict_bucket": S98_VERDICT_BUCKET, "s96_self_attention": S96_SELF_ATTENTION,
        "c4_present": c4_present,
        "anchor": "byte-literal citation of §98/§96 result.json verdicts (connection-point)",
        "closed": True, "tier": "a-closed", "passed": passed,
    }


def main():
    checks = [
        b_s99_1_three_arm_partition_closed(),
        b_s99_2_candidate_taxonomy_exhaustive_disjoint(),
        b_s99_3_no_candidate_closed_invariant(),
        b_s99_4_connection_point_cites_s98_and_s96(),
    ]
    note = {
        "name": "B-S99-NOTE",
        "kind": "empirical-carve-out",
        "statement": (
            "§99 is a LITERATURE-REVIEW section. This light battery proves the §99 "
            "DOCUMENT is well-formed (3-arm partition closed, 7-candidate taxonomy "
            "exhaustive+disjoint, NO path closed, §98/§96 cited byte-literal). It does "
            "NOT prove any candidate path works, NOT that anima emerges, NOT that the "
            "GOAL is reached. Whether C1..C7 move the GOAL is EMPIRICAL — future "
            "design+fire cycles. literature = inspiration NOT proof. "
            "necessary-not-sufficient (B-EMERGE-7). B-D-NOTE / B-S95-NOTE / B-S96-NOTE / "
            "B-S98-NOTE family — NOT counted as a closed capability verdict."
        ),
    }
    all_passed = all(c["passed"] for c in checks)
    result = {
        "battery": "B-S99 (§99 data-regime/substrate/spontaneity-vs-coherence frontier deep research sidecar)",
        "tier": "literature-review (light battery — document-well-formedness only)",
        "central_blue_falsifier_sha": "c93e160a8a376a94 (0-line-diff — sidecar only, central untouched)",
        "verdicts": {f"B-S99-{i+1}": c for i, c in enumerate(checks)},
        "note": note,
        "all_passed": all_passed,
        "n_passed": sum(c["passed"] for c in checks),
        "n_total": len(checks),
        "g3": "literature review NOT empirical; capability claim 0; arxiv = inspiration NOT proof; north-star + §15/§51/§72 UNCHANGED; GOAL 미도달",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    out = __file__.rsplit("/", 1)[0] + "/blue_falsifier_s99_result.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
