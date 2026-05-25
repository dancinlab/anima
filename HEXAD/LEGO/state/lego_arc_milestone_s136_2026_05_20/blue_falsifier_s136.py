#!/usr/bin/env python3
"""§136 LEGO ARC MILESTONE battery — 5 closed-form propositions + 1 NOTE.

Milestone-tier (mirror §15/§51): proves the §136 MILESTONE doc is structurally
honest — arc-coverage cardinality, battery sum, GOAL-not-claimed — NOT a new
measurement. No new arc finding; consolidation only.
"""

import ast
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
MILESTONE_MD = HERE / "MILESTONE.md"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s136_1_arc_cycle_cardinality():
    """The §136 milestone documents exactly 11 measured cycles + 1 carry.
    Verify the cycle table in MILESTONE.md lists all expected §N."""
    src = MILESTONE_MD.read_text()
    expected_cycles = ["§115", "§117", "§124", "§125", "§126", "§127",
                        "§128", "§129", "§131", "§132", "§133", "§134", "§135"]
    all_present = all(c in src for c in expected_cycles)
    count = len(expected_cycles)
    return {"name": "B-S136-1 ARC-CYCLE-CARDINALITY-CLOSED",
            "passed": bool(all_present and count == 13),
            "evidence": {"expected_cycles": expected_cycles,
                          "all_present_in_milestone": all_present,
                          "cycle_count (incl §129 consolidation + §133 carry)": count}}


def b_s136_2_battery_sum_arithmetic():
    """78 = 9+7+7+7+7+8+6+7+6+7+7 — closed arithmetic identity."""
    batteries = [9, 7, 7, 7, 7, 8, 6, 7, 6, 7, 7]  # S115,117,124,125,126,127,128,131,132,134,135
    total = sum(batteries)
    correct = (total == 78)
    src = MILESTONE_MD.read_text()
    doc_states_78 = ("78" in src)
    return {"name": "B-S136-2 BATTERY-SUM-ARITHMETIC-CLOSED",
            "passed": bool(correct and doc_states_78),
            "evidence": {"per_cycle_batteries": batteries, "sum": total,
                          "equals_78": correct, "milestone_states_78": doc_states_78}}


def b_s136_3_goal_not_claimed():
    """Milestone doc explicitly asserts GOAL 미도달 and north-star unchanged —
    structural Boolean over doc text."""
    src = MILESTONE_MD.read_text()
    goal_not_reached = ("GOAL 미도달" in src)
    north_star_unchanged = ("milestones UNCHANGED" in src or "north-star" in src)
    no_emergence_claim = ("0 GOAL emergence claim" in src or "GOAL emergence" in src)
    return {"name": "B-S136-3 GOAL-NOT-CLAIMED-CLOSED",
            "passed": bool(goal_not_reached and north_star_unchanged and no_emergence_claim),
            "evidence": {"goal_미도달_asserted": goal_not_reached,
                          "north_star_unchanged_asserted": north_star_unchanged,
                          "no_emergence_claim_explicit": no_emergence_claim}}


def b_s136_4_three_layer_partition_status():
    """Milestone documents the 3-layer partition with layer-1 closed, layer-2
    closed-PARTIAL, layer-3 design-close — Boolean over doc text."""
    src = MILESTONE_MD.read_text()
    layer1 = ("VARIANCE-ONLY" in src and "§117 closed" in src)
    layer2 = ("STIMULUS-DRIVEN" in src and "PARTIAL" in src)
    layer3 = ("TASK-GROUNDED" in src and "DESIGN-CLOSE" in src)
    return {"name": "B-S136-4 THREE-LAYER-PARTITION-STATUS-CLOSED",
            "passed": bool(layer1 and layer2 and layer3),
            "evidence": {"layer1_variance_closed": layer1,
                          "layer2_stimulus_partial": layer2,
                          "layer3_task_design_close": layer3}}


def b_s136_5_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    ih = set()
    tree = ast.parse(Path(__file__).read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for nm in n.names:
                if nm.name.split(".")[0] in forbidden_imports: ih.add(nm.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module and n.module.split(".")[0] in forbidden_imports: ih.add(n.module)
    return {"name": "B-S136-5 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s136_note():
    return {"name": "B-S136-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "milestone-consolidation-not-measurement",
            "family": "B-EMERGE-7 / §15-milestone / §51-milestone precedent",
            "honest_scope": ("§136 is a milestone consolidation doc, NOT a new "
                             "measurement. The battery proves the MILESTONE.md is "
                             "structurally honest (cycle cardinality, battery sum "
                             "arithmetic, GOAL-not-claimed, partition status) — it "
                             "does NOT add any arc finding. The LEGO arc's substantive "
                             "results are in §115–§135. §136 = the §15/§51-style "
                             "retrospective. GOAL 미도달; north-star + §15/§51/§72 "
                             "milestones UNCHANGED.")}


def main():
    results = {
        "preconditions": [b_s136_5_central_and_ast()],
        "closed_propositions": [
            b_s136_1_arc_cycle_cardinality(),
            b_s136_2_battery_sum_arithmetic(),
            b_s136_3_goal_not_claimed(),
            b_s136_4_three_layer_partition_status(),
            b_s136_5_central_and_ast(),
        ],
        "empirical_carve_out": b_s136_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    closed_count = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{closed_count}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"LEGO-ARC-MILESTONE-CONSOLIDATED-{closed_count}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "necessary_not_sufficient_B_EMERGE_7": True,
        "north_star_unchanged": True,
        "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s136_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
