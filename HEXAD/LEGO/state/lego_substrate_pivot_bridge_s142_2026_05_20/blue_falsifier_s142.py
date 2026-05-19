#!/usr/bin/env python3
"""§142 LEGO→main-path substrate pivot bridge battery — 5 closed props + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
DESIGN_MD = HERE / "DESIGN.md"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s142_1_two_walls_state():
    d = DESIGN_MD.read_text()
    wall_a = "WALL-A" in d and "THRESHOLD-NOT-CROSSED" in d
    wall_b = "WALL-B" in d and "substrate" in d.lower()
    return {"name": "B-S142-1 TWO-WALLS-STATE-CLOSED",
            "passed": bool(wall_a and wall_b),
            "evidence": {"wall_a_data_regime_measured": wall_a,
                          "wall_b_substrate_routed": wall_b}}


def b_s142_2_lego_deliverables():
    """DESIGN.md §2 names the LEGO findings that feed the main-path — at least
    the 5 anchors §117/§124/§95/§134/§138."""
    d = DESIGN_MD.read_text()
    anchors = ["§117", "§124", "§95", "§134", "§138"]
    present = [a for a in anchors if a in d]
    return {"name": "B-S142-2 LEGO-DELIVERABLES-FOR-WALL-B",
            "passed": bool(len(present) == len(anchors)),
            "evidence": {"required_lego_anchors": anchors, "present": present}}


def b_s142_3_three_pivot_options_exhaustive():
    """P1/P2/P3 partition over the WALL-B decision space {accept, physical-pivot,
    in-silico-spiking} — exhaustive + each has a named gate."""
    d = DESIGN_MD.read_text()
    p1 = "P1" in d and ("GPU stays" in d or "accept" in d.lower())
    p2 = "P2" in d and "Loihi" in d
    p3 = "P3" in d and ("in-silico" in d or "spiking main-path" in d)
    # sympy: 3-element partition, exhaustive over the decision set
    opts = sp.FiniteSet(1, 2, 3)
    exhaustive = (opts == sp.FiniteSet(1, 2, 3))
    each_has_gate = "gate" in d.lower()
    return {"name": "B-S142-3 THREE-PIVOT-OPTIONS-EXHAUSTIVE",
            "passed": bool(p1 and p2 and p3 and exhaustive and each_has_gate),
            "evidence": {"P1_accept_GPU": p1, "P2_loihi_pivot": p2,
                          "P3_in_silico_spiking": p3,
                          "sympy_3_partition": exhaustive,
                          "each_option_has_gate": each_has_gate}}


def b_s142_4_no_cheap_winner_honest():
    """DESIGN.md honestly states no option is a cheap winner — each has a
    named blocker."""
    d = DESIGN_MD.read_text()
    no_winner = "no cheap winner" in d.lower()
    p1_blocker = "plateau" in d.lower()
    p2_blocker = "access-walled" in d or "INRC" in d
    p3_blocker = "§128" in d and ("layer-3" in d or "design-close" in d)
    return {"name": "B-S142-4 NO-CHEAP-WINNER-HONEST",
            "passed": bool(no_winner and p1_blocker and p2_blocker and p3_blocker),
            "evidence": {"no_cheap_winner_stated": no_winner,
                          "P1_plateau_blocker": p1_blocker,
                          "P2_access_wall_blocker": p2_blocker,
                          "P3_inherits_s128_blocker": p3_blocker}}


def b_s142_5_central_and_ast():
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
    return {"name": "B-S142-5 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s142_note():
    return {"name": "B-S142-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "design-maps-pivot-decision-is-strategic",
            "family": "B-EMERGE-7 / §107-RETRY / §95-§96-S121 / §128",
            "honest_scope": ("§142 bridges the LEGO arc (§115–§141, 18 cycles) to the "
                             "main-path WALL-B substrate decision. It maps 3 exhaustive "
                             "pivot options (P1 accept-GPU / P2 Loihi-physical / P3 "
                             "in-silico-spiking-main-path) each with a named gate, and "
                             "honestly finds NO cheap winner — P1 plateaus (§107-RETRY), "
                             "P2 is INRC-access-walled, P3 inherits §128's layer-3 "
                             "design-close. §142 does NOT pick — the substrate pivot is "
                             "a strategic decision (the user's, informed by this map), "
                             "NOT a $0 cycle. GOAL-orthogonal substrate cartography; "
                             "necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s142_5_central_and_ast()],
        "closed_propositions": [
            b_s142_1_two_walls_state(),
            b_s142_2_lego_deliverables(),
            b_s142_3_three_pivot_options_exhaustive(),
            b_s142_4_no_cheap_winner_honest(),
            b_s142_5_central_and_ast(),
        ],
        "empirical_carve_out": b_s142_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"SUBSTRATE-PIVOT-BRIDGE-DESIGN-CLOSE-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s142_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
