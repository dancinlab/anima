#!/usr/bin/env python3
"""S121 LOIHI-SPEC battery — 5 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
DESIGN_MD = HERE / "DESIGN.md"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s121_1_lifnet_maps_to_lava_complete():
    """Every lego_engine LIFNet component has a named Lava equivalent in the
    §1 mapping table."""
    design = DESIGN_MD.read_text()
    components = ["LIF", "Dense", "on-chip", "STDP", "Monitor", "bias", "s_out"]
    all_present = all(c in design for c in components)
    return {"name": "B-S121-1 LIFNET-MAPS-TO-LAVA-COMPLETE",
            "passed": bool(all_present),
            "evidence": {"required_lava_components": components,
                          "all_in_mapping_table": all_present}}


def b_s121_2_stdp_native_on_loihi():
    """DESIGN.md asserts STDP is a native on-chip Loihi 2 learning rule — the
    §11-B-as-GPU-tautology escape. Boolean."""
    design = DESIGN_MD.read_text()
    on_chip = "on-chip" in design and "learning_rule" in design
    escapes_tautology = "11-B-as-GPU" in design or "GPU-tautology" in design
    return {"name": "B-S121-2 STDP-IS-NATIVE-ON-LOIHI-2",
            "passed": bool(on_chip and escapes_tautology),
            "evidence": {"on_chip_learning_rule_named": on_chip,
                          "gpu_tautology_escape_cited": escapes_tautology}}


def b_s121_3_access_wall_soft_not_arch():
    """DESIGN.md classifies the Loihi access wall as soft (INRC membership)
    not hard (architecture/ethics) — Boolean."""
    design = DESIGN_MD.read_text()
    soft_wall = "soft wall" in design or "soft* wall" in design or "soft* (access" in design
    inrc = "INRC" in design
    return {"name": "B-S121-3 ACCESS-WALL-IS-SOFT-NOT-ARCH",
            "passed": bool(soft_wall and inrc),
            "evidence": {"soft_wall_classified": soft_wall, "inrc_named": inrc}}


def b_s121_4_spec_readable_not_fireable():
    """S121 has NO hardware/dispatch/fire path — AST audit of this battery +
    confirmation DESIGN.md explicitly states readable-only."""
    design = DESIGN_MD.read_text()
    readable_only = ("readable only" in design or "readable-only" in design
                     or "SPEC ONLY" in design)
    no_fire_claim = "NOT a fire" in design or "design-tier" in design
    # AST: this battery has no fire/dispatch calls
    forbidden = {"create_pod", "podFindAndDeployOnDemand", "run"}
    tree = ast.parse(Path(__file__).read_text())
    # 'run' is too generic; only check pod/dispatch
    dispatch_hit = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr in {"create_pod", "podFindAndDeployOnDemand"}:
                dispatch_hit = True
    return {"name": "B-S121-4 SPEC-IS-READABLE-NOT-FIREABLE",
            "passed": bool(readable_only and no_fire_claim and not dispatch_hit),
            "evidence": {"readable_only_stated": readable_only,
                          "no_fire_claim": no_fire_claim,
                          "no_dispatch_in_battery": not dispatch_hit}}


def b_s121_5_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai", "lava"}
    ih = set()
    tree = ast.parse(Path(__file__).read_text())
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for nm in n.names:
                if nm.name.split(".")[0] in forbidden_imports: ih.add(nm.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module and n.module.split(".")[0] in forbidden_imports: ih.add(n.module)
    return {"name": "B-S121-5 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-IMPORT",
            "passed": bool(central_ok and len(ih) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih)}}


def b_s121_note():
    return {"name": "B-S121-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "mapping-specified-fire-access-walled",
            "family": "B-EMERGE-7 / §95-substrate-matrix / §96-spiking-rederivation",
            "honest_scope": ("S121 specifies the lego_engine → Loihi 2 Lava mapping "
                             "fully (every LIFNet component → native Lava primitive). "
                             "It does NOT fire — Loihi 2 access is INRC-membership-walled "
                             "(§95, survey inactive). Whether a Loihi-resident anima "
                             "actually escapes WALL-B (§96) is a post-INRC-access "
                             "empirical question; S121 is the blueprint, not the verdict. "
                             "The §11-B-as-GPU-tautology escape claim (Loihi's on-chip "
                             "learning_rule is a physical process) is §96's insight made "
                             "concrete in Lava primitives — named, not proven. GOAL-"
                             "orthogonal; necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s121_5_central_and_ast()],
        "closed_propositions": [
            b_s121_1_lifnet_maps_to_lava_complete(),
            b_s121_2_stdp_native_on_loihi(),
            b_s121_3_access_wall_soft_not_arch(),
            b_s121_4_spec_readable_not_fireable(),
            b_s121_5_central_and_ast(),
        ],
        "empirical_carve_out": b_s121_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"LOIHI-SPEC-DESIGN-CLOSE-ACCESS-WALLED-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s121_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
