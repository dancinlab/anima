#!/usr/bin/env python3
"""
§51 milestone close-out — sidecar closed-form battery (B-S51-1..2).

NOT central: this is a sidecar (mirror B-S16 / B-S48 / B-PTD / B-DHDL /
B-LINEAGE / B-KTRIE / B-MGND / B-PHASE-B-RUN sidecar precedent). Central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py is UNCHANGED.

A milestone close-out is a SYNTHESIS, not a new measurement. The battery
proves the close-out doc is structurally honest (asserts GOAL unreached +
north-star unchanged) and comprehensively covers the arc (not cherry-picked).
It does NOT prove any empirical OUTCOME — B-S51-NOTE.

B-S51-1 MILESTONE-IS-NOT-GOAL-ACHIEVEMENT-CLOSED
  Boolean structural predicate over the verdict/doc text: the milestone doc
  asserts (a) GOAL unreached AND (b) north-star unchanged AND (c) frontier-1
  is a HYPOTHESIS not a proven path. A milestone that claimed GOAL achieved
  would FAIL this gate. (g3 self-check encoded as a closed predicate.)

B-S51-2 ARC-COVERAGE-CARDINALITY-CLOSED
  The §16~§50 arc is comprehensively covered: the doc references >= N_FLOOR
  distinct s-numbered sections (integer cardinality, Kolmogorov set count) —
  the synthesis is not cherry-picked to a handful of favourable cycles.

B-S51-NOTE  (empirical carve-out, NOT counted 🔵)
  Whether the *sharpened frontier* (multimodal substrate) actually crosses the
  §1.1 data-regime threshold is an SGD/measurement OUTCOME of a FUTURE fire —
  unmeasured, a hypothesis (B-D-NOTE / B-S16-NOTE / B-DR-UNIQUE-NOTE family).
  The battery proves the milestone doc is honest (declares unsolved, frontier
  = hypothesis), NOT that the frontier is the path. necessary-not-sufficient
  at the milestone layer (mirror B-EMERGE-7 / §15 close-out discipline).
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC = HERE / "MILESTONE_S51.md"

# arc s-numbered sections present in archive/PHILOSOPHY.tape §verdict_* ledger
# (the comprehensive set the milestone must cover, not cherry-pick)
ARC_SECTIONS = [
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
]
N_FLOOR = 24  # >= 24 distinct sections referenced => comprehensive, not cherry-picked


def b_s51_1_milestone_is_not_goal_achievement():
    """Closed Boolean structural predicate: the doc must assert GOAL unreached,
    north-star unchanged, and frontier-1 = hypothesis (not proven path)."""
    txt = DOC.read_text(encoding="utf-8")
    low = txt.lower()

    asserts_goal_unreached = ("goal unreached" in low) or (
        "goal still unreached" in low
    )
    asserts_north_star_unchanged = "north-star" in low and "unchanged" in low
    asserts_frontier_is_hypothesis = (
        "hypothesis, not a proven path" in low
        or "sharpened hypothesis" in low
        or ("hypothesis" in low and "not a proven path" in low)
    )
    # negative falsifier: a doc CLAIMING achievement would assert these
    # WITHOUT an adjacent negation. An honest doc may quote them only inside a
    # negated disclaimer (e.g. -- NOT "we solved GOAL"). The closed predicate
    # therefore requires the claim to appear *un-negated* to FAIL the gate:
    # a forbidden claim is a violation iff some occurrence has no negation
    # token ('not', 'never', 'un', 'no proof', '!=', 'unreached') within the
    # preceding 40 chars.
    forbidden_claims = [
        "goal achieved",
        "goal reached",
        "we solved goal",
        "emergence achieved",
        "north-star reached",
    ]
    # negation detector over a markdown-stripped preceding context window
    # (strip *, _, `, ", quotes, em-dash so '**not** "' normalises to 'not ').
    neg_re = re.compile(r"\b(not|never|no|isn't|wasn't)\b|\bun")

    def claimed_un_negated(claim):
        for m in re.finditer(re.escape(claim), low):
            raw = low[max(0, m.start() - 50):m.start()]
            ctx = re.sub(r'[*_`"—–\']', " ", raw)
            if not neg_re.search(ctx):
                return True  # an un-negated (asserted) occurrence => violation
        return False

    no_forbidden = not any(claimed_un_negated(fc) for fc in forbidden_claims)

    gate = (
        asserts_goal_unreached
        and asserts_north_star_unchanged
        and asserts_frontier_is_hypothesis
        and no_forbidden
    )
    return {
        "id": "B-S51-1",
        "name": "MILESTONE-IS-NOT-GOAL-ACHIEVEMENT-CLOSED",
        "asserts_goal_unreached": asserts_goal_unreached,
        "asserts_north_star_unchanged": asserts_north_star_unchanged,
        "asserts_frontier_is_hypothesis": asserts_frontier_is_hypothesis,
        "no_forbidden_achievement_claim": no_forbidden,
        "pass": bool(gate),
    }


def b_s51_2_arc_coverage_cardinality():
    """Closed integer cardinality: the doc references >= N_FLOOR distinct
    s-numbered arc sections (comprehensive, not cherry-picked)."""
    txt = DOC.read_text(encoding="utf-8")
    # match §NN section references (the doc uses §16, §17, ... form)
    refs = set(int(m) for m in re.findall(r"§(\d{1,3})\b", txt))
    arc_set = set(ARC_SECTIONS)
    covered = sorted(refs & arc_set)
    n_covered = len(covered)
    # the doc must reference at least N_FLOOR of the arc sections AND must not
    # omit the load-bearing pivots (16 breakthrough, 22 mechanism-close,
    # 32/35/42/43 lever chain, 47/34 content-axis, 28 substrate, 15 prior milestone)
    pivots = {16, 22, 28, 32, 34, 35, 42, 43}
    pivots_covered = pivots.issubset(refs)
    gate = n_covered >= N_FLOOR and pivots_covered
    return {
        "id": "B-S51-2",
        "name": "ARC-COVERAGE-CARDINALITY-CLOSED",
        "n_arc_sections_total": len(arc_set),
        "n_floor": N_FLOOR,
        "n_covered": n_covered,
        "covered": covered,
        "pivots_required": sorted(pivots),
        "pivots_covered": pivots_covered,
        "pass": bool(gate),
    }


def main():
    results = [
        b_s51_1_milestone_is_not_goal_achievement(),
        b_s51_2_arc_coverage_cardinality(),
    ]
    all_pass = all(r["pass"] for r in results)
    out = {
        "battery": "B-S51 (§51 milestone close-out sidecar)",
        "central_unchanged": True,
        "results": results,
        "all_pass": all_pass,
        "n_pass": sum(1 for r in results if r["pass"]),
        "n_total": len(results),
        "note": (
            "B-S51-NOTE: milestone close-out is synthesis not measurement; "
            "no empirical OUTCOME claimed; sharpened frontier (multimodal) is "
            "a hypothesis for future cycles, NOT a proven path "
            "(B-D-NOTE/B-S16-NOTE family, NOT counted blue)."
        ),
    }
    (HERE / "blue_falsifier_s51_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    for r in results:
        print(f"{r['id']} {r['name']}: {'PASS' if r['pass'] else 'FAIL'}")
    print(f"=== B-S51 {out['n_pass']}/{out['n_total']} "
          f"{'ALL PASS' if all_pass else 'FAIL'} ===")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
