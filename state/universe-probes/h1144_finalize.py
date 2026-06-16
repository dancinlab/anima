#!/usr/bin/env python3
"""h1144_finalize.py — assemble the H_1144 terminal verdict from the pulled pod
artifacts (state/h1144_grounding/). Computes the slope decision, the converged
fab-rate (if greenlit), the FULL a7b_pass tally, prints a verdict block to stdout
(captured into .verdicts/1144_grounding_train/H_1144.txt by the caller). Read-only
on the artifacts; deterministic. NOT perplexity, NOT LLM.
"""
import json, os, sys

ART = "/Users/mini/dancinlab/anima/.claude/worktrees/agent-ac7bce10c6e042622/state/h1144_grounding"
R0 = 0.2469
BAR = 0.20


def load(name):
    p = os.path.join(ART, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    probe_fab = load("h1144_fabrate_probe.json")
    conv_fab = load("h1144_fabrate_converge.json")
    curve_probe = load("h1144_curve_probe.json")
    curve_conv = load("h1144_curve_converge.json")
    battery_probe = load("h1144_battery_probe.json")
    battery_conv = load("h1144_battery_converge.json")
    manifest = load("h1144_final_manifest.json")

    print("H_1144 GROUNDING CONTINUE-TRAIN — assembled artifacts:")
    if probe_fab:
        print(f"  PROBE fab-rate = {probe_fab['fabricated_entity_rate']} "
              f"(n_fab {probe_fab['n_fabricated']}/{probe_fab['n_entities_total']})  "
              f"new_L2_pass={probe_fab['new_L2_pass']}")
    if curve_probe:
        print(f"  PROBE train: base_val={curve_probe.get('baseline_val_on_grounding_corpus')} "
              f"best_val={curve_probe.get('best_val_ce')} @step{curve_probe.get('best_step')} "
              f"improved={curve_probe.get('improved_vs_baseline')}")
    greenlit = bool(conv_fab) or (manifest and manifest.get("slope_rc") == 0)
    print(f"  SLOPE: greenlit_to_converge={greenlit}")
    if conv_fab:
        print(f"  CONVERGED fab-rate = {conv_fab['fabricated_entity_rate']} "
              f"new_L2_pass={conv_fab['new_L2_pass']}")
    if curve_conv:
        print(f"  CONVERGE train: best_val={curve_conv.get('best_val_ce')} @step{curve_conv.get('best_step')}")

    final_fab = conv_fab or probe_fab
    final_battery = battery_conv or battery_probe
    if final_fab:
        r = final_fab["fabricated_entity_rate"]
        l2_pass = final_fab["new_L2_pass"]
        print(f"\nFINAL fab-rate = {r}  (bar {BAR})  L2-new = {'PASS' if l2_pass else 'FAIL'}")
        # full a7b_pass tally
        if final_battery:
            g0 = final_battery.get("G0", {}).get("pass")
            g1 = final_battery.get("G1", {}).get("pass")
            g2 = final_battery.get("G2", {}).get("pass")
            g3 = final_battery.get("G3", {}).get("pass")
            l1 = None
            # G5-L1 is in the g5_result json
            g5r = load("g5_result_converge.json") or load("g5_result_probe.json")
            if g5r:
                l1 = g5r.get("G5_L1", {}).get("pass")
            g5 = (l1 is True) and (l2_pass is True)
            a7b = all(x is True for x in (g0, g1, g2, g3, l1, l2_pass))
            print(f"\na7b_pass TALLY: G0={g0} G1={g1} G2={g2} G3={g3} G4=(provenance) "
                  f"G5=(L1={l1} ∧ L2={l2_pass})={g5}")
            print(f"a7b_pass = {a7b}")
    if manifest:
        print(f"\nFINAL ckpt: {manifest.get('final_ckpt')} tag={manifest.get('final_tag')} "
              f"sha256={manifest.get('sha256')} size={manifest.get('size')}")


if __name__ == "__main__":
    main()
