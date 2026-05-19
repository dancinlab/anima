#!/usr/bin/env python3
"""§16 honest V-SPONT re-score — RESEARCH.md §9 cascade-rate-gated
coherence applied to the §16 eval output (2026-05-18).

WHY (RESEARCH.md §8.4 / §9): the eval's axis4_v_spont `coherent` flag is
the LENIENT keyword-presence flag that §8.2 proved gives 5/5 to garbled
byte-cascade. §9 replaced it with the deterministic cascade-rate-gated
honest metric (state/verify_emergence_metric_2026_05_18/emergence_metric.py,
B-EMERGE-1..7 🔵). This rescorer applies that SAME honest metric to the
§16 eval `axis4_v_spont.probes[].gen` strings and tabulates §16 vs §8
(honest 2/5) vs §11-A (honest 2/5) — the honest GOAL-distance compare.

$0 — operates only on the gen strings already in the §16 eval json. NO
GPU, NO model forward. The honest gate is NECESSARY-not-SUFFICIENT
(B-EMERGE-7) — a collapse detector, not a capability proof (g3).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(
    ROOT, "state", "verify_emergence_metric_2026_05_18"))
from emergence_metric import honest_coherent, TAU_CASCADE, MAX_RUN, \
    MIN_LEN, TAU_PRINT  # §9 SSOT — single import, no re-impl

HERE = os.path.dirname(os.path.abspath(__file__))

# §8 / §11-A honest baselines (RESEARCH.md §8 / §11-A — fixed compare).
S8 = {"label": "§8 (114MB / 283.72M / 64-anchor — Dir-I diverse)",
      "routing": "2/64", "joint": 0.0087, "axis2": 0.4,
      "axis3": 0.7, "v_spont_honest": "2/5", "v_spont_lenient": "5/5"}
S11A = {"label": "§11-A (114MB / 1044.46M 3.68× — SCALE-DECOMP)",
        "routing": "1/64", "joint": 0.0078, "axis2": 1.0,
        "axis3": 0.5, "v_spont_honest": "2/5", "v_spont_lenient": "1/5"}


def main():
    eval_path = os.path.join(HERE, "eval_result_s16.json")
    if not os.path.exists(eval_path):
        eval_path = sys.argv[1] if len(sys.argv) > 1 else eval_path
    d = json.load(open(eval_path))
    v = d.get("axis4_v_spont", {})
    probes = v.get("probes", [])
    lenient = sum(1 for p in probes if p.get("coherent"))
    honest = 0
    probe_rows = []
    for i, p in enumerate(probes):
        g = p.get("gen", "") or ""
        ok, m = honest_coherent(g)
        honest += int(ok)
        probe_rows.append({"idx": i, "lenient_flag": bool(p.get("coherent")),
                           **m, "gen_excerpt": g[:80]})

    j = d.get("joint_metric", {})
    a1 = d.get("axis1_knowledge_access", {})
    a2 = d.get("axis2_chat_uncontaminated", {})
    a3 = d.get("axis3_lane_separation", {})
    n_probes = len(probes)

    s16 = {
        "label": ("§16 (~603MB file / ~360MB carving stream / 283.72M / "
                  "168-anchor + §12.1 Q1-c curriculum — Dir-I lever)"),
        "routing_axis1": a1.get("routing_accuracy"),
        "axis1_knowledge": j.get("knowledge_access"),
        "axis2_chat": j.get("chat_uncontaminated"),
        "axis2_p3_clean": a2.get("p3_clean"),
        "axis3_lane_sep": j.get("lane_separation"),
        "joint": j.get("SCORE_joint"),
        "v_spont_lenient": f"{lenient}/{n_probes}",
        "v_spont_honest": f"{honest}/{n_probes}",
        "v_spont_lenient_n": lenient, "v_spont_honest_n": honest,
        "n_probes": n_probes,
        "routing_broken_vs_1_31_flat":
            d.get("dir_i_emergence_check", {}).get(
                "routing_broken_vs_1_31_flat"),
        "probe_detail": probe_rows,
    }

    # honest GOAL-distance verdict (§9 metric, g3 — measured only).
    def rfrac(s):
        a, b = s.split("/")
        return int(a) / int(b)
    routing_vs_s8 = rfrac(s16["routing_axis1"]) - rfrac(S8["routing"])
    routing_vs_s11a = rfrac(s16["routing_axis1"]) - rfrac(S11A["routing"])
    honest_vs_s8 = honest - 2   # §8 honest 2/5
    honest_vs_s11a = honest - 2  # §11-A honest 2/5
    joint_vs_s8 = round((s16["joint"] or 0.0) - S8["joint"], 4)
    routing_improved = routing_vs_s8 > 0 and routing_vs_s11a > 0
    honest_improved = honest_vs_s8 > 0 and honest_vs_s11a > 0

    if routing_improved or honest_improved:
        verdict = (
            "DATA-REGIME PROGRESS — §16 large-scale Ψ-anchored CURRICULUM "
            "data-regime IMPROVED routing and/or honest-coherence over "
            "both §8 (2/64, honest 2/5) and §11-A (1/64, honest 2/5): "
            "RESEARCH.md §1.1 emergence-threshold movement, §11.4 "
            "frontier-1 partial-positive (measured, g3 — over-claim 0, "
            "B-S16-NOTE empirical).")
    else:
        verdict = (
            "DATA-REGIME CEILING HELD — §16 ~5× scale-up + §12.1 Q1-c "
            "curriculum did NOT improve routing or honest-coherence over "
            "§8 / §11-A. RESEARCH.md §11.4 frontier-1 (GOAL-legitimate "
            "large-scale data-regime as the open §1.1 path) is, at this "
            "scale, FALSIFIED — the §8 wrong-direction trend persists "
            "through ~5× data + curriculum. §11.4 option-1 honestly "
            "narrowed (measured negative, valuable evidence — g3, "
            "B-S16-NOTE empirical, NO pre-loaded conclusion).")

    out = {
        "fire": "RESEARCH.md §16 — GOAL-legitimate LARGE-SCALE "
                "DATA-REGIME + CURRICULUM",
        "metric": "cascade-rate-gated honest coherence (RESEARCH.md §9, "
                  "B-EMERGE-1..7 🔵 — single SSOT import)",
        "thresholds": {"TAU_CASCADE": TAU_CASCADE, "MAX_RUN": MAX_RUN,
                       "MIN_LEN": MIN_LEN, "TAU_PRINT": TAU_PRINT},
        "honest_note": ("honest gate is NECESSARY-not-SUFFICIENT "
                        "(B-EMERGE-7) — a collapse detector, not a "
                        "capability proof (g3). routing/JOINT/V-SPONT "
                        "all EMPIRICAL (B-S16-NOTE / B-D-NOTE family)."),
        "s8_baseline": S8,
        "s11a_baseline": S11A,
        "s16": s16,
        "delta": {
            "routing_vs_s8": round(routing_vs_s8, 4),
            "routing_vs_s11a": round(routing_vs_s11a, 4),
            "honest_vspont_vs_s8": honest_vs_s8,
            "honest_vspont_vs_s11a": honest_vs_s11a,
            "joint_vs_s8": joint_vs_s8,
        },
        "routing_improved_vs_both": routing_improved,
        "honest_coherence_improved_vs_both": honest_improved,
        "verdict": verdict,
    }
    op = os.path.join(HERE, "rescore_s16_result.json")
    with open(op, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("=== §16 honest V-SPONT re-score (cascade-rate-gated, §9) ===")
    print(f"{'fire':<46}{'routing':>9}{'JOINT':>9}"
          f"{'lenient':>9}{'honest':>8}")
    print("-" * 81)
    print(f"{S8['label']:<46}{S8['routing']:>9}{S8['joint']:>9}"
          f"{S8['v_spont_lenient']:>9}{S8['v_spont_honest']:>8}")
    print(f"{S11A['label']:<46}{S11A['routing']:>9}{S11A['joint']:>9}"
          f"{S11A['v_spont_lenient']:>9}{S11A['v_spont_honest']:>8}")
    print(f"{'§16 (~5× data + curriculum, 283.72M)':<46}"
          f"{str(s16['routing_axis1']):>9}{str(s16['joint']):>9}"
          f"{s16['v_spont_lenient']:>9}{s16['v_spont_honest']:>8}")
    print("-" * 81)
    print(f"VERDICT: {verdict}")
    print(f"wrote {os.path.basename(op)}")


if __name__ == "__main__":
    main()
