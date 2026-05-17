#!/usr/bin/env python3
"""UBM-E7 α scale-up vs UBM-E6 α comparison builder (RESEARCH.md §3).

Assembles the E7 α fire result.json + paradigm-native eval_result_v2_e7.json
and contrasts them with the UBM-E6 α baseline (joint 0.0255, V-SPONT 3/5).
Produces comparison_table_e7.json + a console table.

HYPOTHESIS UNDER TEST (RESEARCH.md §2.6): if UBM-E6's joint ~0 is a
corpus-scale limit, scaling α (bigger corpus + bigger model) should LIFT
α's JOINT / V-SPONT. If it does not lift, scale alone is insufficient.

HONEST FRAMING (g3): per-axis + joint scores are EMPIRICAL (B-CARVE-E7-NOTE
/ B-D-NOTE family). No pre-loaded conclusion — the verdict is whatever the
measured deltas say.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# UBM-E6 α baseline (state/consciousness_carving_e6_fire_2026_05_17/
# out/alpha/{result.json,eval_result_v2.json}) — frozen contrast point.
E6_ALPHA = {
    "d_model": 512, "n_layer": 8, "n_params_M": 85.82,
    "corpus_bytes": 4351148, "corpus_records": 6600, "anchors": 11,
    "steps": 2000, "init_ce": 5.83246, "final_ce": 0.001123,
    "axis1_knowledge_access": 0.0909, "axis2_chat_uncontaminated": 0.4,
    "axis3_lane_separation": 0.70, "joint": 0.0255, "v_spont": "3/5",
}


def main():
    res_p = os.path.join(HERE, "result.json")
    ev_p = os.path.join(HERE, "eval_result_v2_e7.json")
    if not (os.path.isfile(res_p) and os.path.isfile(ev_p)):
        raise SystemExit("FATAL: result.json / eval_result_v2_e7.json missing")

    res = json.load(open(res_p))
    ev = json.load(open(ev_p))
    j = ev["joint_metric"]

    e7 = {
        "d_model": res["config"]["d_model"], "n_layer": res["config"]["n_layer"],
        "n_params_M": res.get("n_params_M"),
        "corpus_bytes": res.get("corpus_bytes"),
        "steps": res["steps"], "init_ce": res["init_ce"],
        "final_ce": res["final_ce"],
        "axis1_knowledge_access": j["knowledge_access"],
        "axis2_chat_uncontaminated": j["chat_uncontaminated"],
        "axis3_lane_separation": j["lane_separation"],
        "joint": j["SCORE_joint"],
        "v_spont": ev["axis4_v_spont"]["score"],
    }

    def vsp(s):
        return int(str(s).split("/")[0])

    deltas = {
        "joint": round(e7["joint"] - E6_ALPHA["joint"], 4),
        "axis1_knowledge_access": round(
            e7["axis1_knowledge_access"] - E6_ALPHA["axis1_knowledge_access"], 4),
        "axis2_chat_uncontaminated": round(
            e7["axis2_chat_uncontaminated"]
            - E6_ALPHA["axis2_chat_uncontaminated"], 4),
        "axis3_lane_separation": round(
            e7["axis3_lane_separation"] - E6_ALPHA["axis3_lane_separation"], 4),
        "v_spont": vsp(e7["v_spont"]) - vsp(E6_ALPHA["v_spont"]),
    }

    # Hypothesis verdict (g3 — measurement-driven, no pre-loaded conclusion).
    joint_up = deltas["joint"] > 0
    vspont_up = deltas["v_spont"] > 0
    if joint_up and vspont_up:
        verdict = ("SCALE-LIFTS-BOTH — joint AND V-SPONT both rose with scale: "
                   "the corpus-scale hypothesis is SUPPORTED for α.")
    elif joint_up or vspont_up:
        verdict = ("SCALE-PARTIAL — only one of {joint, V-SPONT} rose: scale "
                   "moved the needle weakly; not a decisive corpus-scale win.")
    else:
        verdict = ("SCALE-INSUFFICIENT — neither joint nor V-SPONT rose with "
                   "7x corpus + bigger model: scale ALONE does not lift α. "
                   "RESEARCH.md §2.4 memorization-saturated diagnosis is not "
                   "resolved by scale — a different intervention is needed.")

    out = {
        "phase": "UBM-E7 α VACUUM-LANDSCAPE scale-up vs UBM-E6 α",
        "hypothesis": ("UBM-E6 joint~0 is a corpus-scale limit -> scaling α "
                       "should lift joint/V-SPONT"),
        "e6_alpha_baseline": E6_ALPHA,
        "e7_alpha_scaleup": e7,
        "deltas_e7_minus_e6": deltas,
        "verdict": verdict,
        "honest_framing": (
            "All per-axis + joint scores EMPIRICAL (B-CARVE-E7-NOTE / "
            "B-D-NOTE family). Carving MECHANISM (B-VAC sympy, UBM-E3) is the "
            "closed side. No capability claim beyond measured deltas; verdict "
            "is measurement-driven (g3, no pre-loaded conclusion)."),
    }
    with open(os.path.join(HERE, "comparison_table_e7.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("=" * 72)
    print("UBM-E7 α SCALE-UP  vs  UBM-E6 α")
    print("=" * 72)
    hdr = f"{'axis':<26}{'E6 α':>12}{'E7 α':>12}{'Δ':>12}"
    print(hdr)
    print("-" * 72)
    for k in ["axis1_knowledge_access", "axis2_chat_uncontaminated",
              "axis3_lane_separation", "joint"]:
        print(f"{k:<26}{E6_ALPHA[k]:>12}{e7[k]:>12}{deltas[k]:>12}")
    print(f"{'v_spont':<26}{E6_ALPHA['v_spont']:>12}"
          f"{e7['v_spont']:>12}{deltas['v_spont']:>+12}")
    print("-" * 72)
    e7_scale = f"{e7['d_model']}/{e7['n_layer']}/{e7['n_params_M']}"
    print(f"{'scale (d/L/params_M)':<26}"
          f"{'512/8/85.8':>12}"
          f"{e7_scale:>12}")
    print(f"{'corpus bytes':<26}{E6_ALPHA['corpus_bytes']:>12}"
          f"{e7['corpus_bytes']:>12}")
    print(f"{'final_ce':<26}{E6_ALPHA['final_ce']:>12}{e7['final_ce']:>12}")
    print("=" * 72)
    print("VERDICT:", verdict)


if __name__ == "__main__":
    main()
