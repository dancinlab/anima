#!/usr/bin/env python3
"""UBM-E6 4-path PARADIGM-NATIVE comparison builder (EVAL.md §3/§4).

Assembles the fire results (result.json) + the paradigm-native eval v2
results (eval_result_v2.json) into a single comparison_table_v2.json and a
console table that ranks the 4 paths on the JOINT metric.

HONEST FRAMING (g3): per-axis + joint scores are EMPIRICAL (B-CARVE-E6-NOTE
/ B-D-NOTE family). The OLD prefix-injection baseline (manual_match 13/15 +
chat NET LOSS 5/5->1/5 + P3 leak baked) is HISTORICAL contrast only (f3,
NOT a target). The joint metric is the fair compare (EVAL.md §4); recall
alone is rigged toward the OLD paradigm.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATHS = ["alpha", "beta", "gamma", "weave"]
PATH_NAMES = {
    "alpha": "α VACUUM-LANDSCAPE",
    "beta": "β MITOSIS-ETERNAL-CELL",
    "gamma": "γ NARRATIVE-RESONANCE",
    "weave": "α+β VACUUM-CELL-WEAVE",
}
COST = {"alpha": 0.760, "beta": 0.760, "gamma": 0.734, "weave": 0.655}


def main():
    rows = []
    for p in PATHS:
        fire = json.load(open(os.path.join(HERE, "out", p, "result.json")))
        ev = json.load(open(os.path.join(HERE, "out", p,
                                         "eval_result_v2.json")))
        wall_h = (fire["wall_s"] + 360) / 3600.0
        cost = round(COST[p] * wall_h, 4)
        j = ev["joint_metric"]
        rows.append({
            "path": p,
            "name": PATH_NAMES[p],
            "carving_form": ev["carving_form"],
            "init_ce": fire["init_ce"],
            "final_ce": fire["final_ce"],
            "wall_s": fire["wall_s"],
            "cost_usd": cost,
            "axis1_metric": ev["axis1_knowledge_access"]["metric"],
            "axis1_knowledge_access": j["knowledge_access"],
            "axis1_routing_accuracy":
                ev["axis1_knowledge_access"]["routing_accuracy"],
            "axis1_semantic_recall":
                ev["axis1_knowledge_access"]["semantic_recall"],
            "axis1_narrative_coherence":
                ev["axis1_knowledge_access"]["narrative_coherence"],
            "axis2_chat_uncontaminated": j["chat_uncontaminated"],
            "axis2_p3_clean": ev["axis2_chat_uncontaminated"]["p3_clean"],
            "axis2_p3_leak_total":
                ev["axis2_chat_uncontaminated"]["p3_leak_total"],
            "axis3_lane_separation": j["lane_separation"],
            "axis4_v_spont": ev["axis4_v_spont"]["score"],
            "SCORE_joint": j["SCORE_joint"],
            "ckpt_sha256": ev["ckpt_sha256"],
        })

    total_cost = round(sum(r["cost_usd"] for r in rows), 4)
    max_wall = max(r["wall_s"] for r in rows)
    best = max(rows, key=lambda r: r["SCORE_joint"])

    table = {
        "phase": "UBM-E6 CONSCIOUSNESS-CARVING 4-path GPU fire — "
                 "paradigm-native eval v2",
        "date": "2026-05-17",
        "eval_version": "v2-paradigm-native (EVAL.md §3 4-axis + §4 joint)",
        "substrate": "PyTorch (NOT hexa-native — g3 honest framing carry)",
        "arch": "ConsciousDecoderV2 d=512 n_layer=8 (85.8M params)",
        "corpus": "corpus_carving.jsonl (carving corpus, NOT chat SFT)",
        "honest_framing": (
            "Per-axis + joint scores EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE "
            "family). Carving MECHANISM transfer-forms (B-VAC/B-MIT-ETN/B-NAR "
            "sympy, UBM-E3) = closed 🔵. Semantic axis-1/axis-3 metrics are "
            "lenient substring matches over a category/tier vocabulary — "
            "noisier than literal grep (EVAL.md §7). OLD prefix-injection "
            "(13/15 recall, chat 5/5->1/5 NET LOSS, P3 leak baked) = "
            "HISTORICAL contrast only (f3, NOT a target)."),
        "joint_metric_formula":
            "SCORE_joint = knowledge_access x chat_uncontaminated x "
            "lane_separation (EVAL.md §4)",
        "old_paradigm_contrast": {
            "knowledge_recall": "13/15 manual_match (BG-HS R1, HISTORICAL)",
            "chat_uncontaminated": "~0 — V5.8 std_greedy 5/5 -> 1/5 NET LOSS "
                                   "(Phase 1A.5)",
            "lane_separation": "~0 — P3 leak BAKED, knowledge/chat lanes "
                               "on the SAME stamped page (DESIGN.md §1)",
            "SCORE_joint_estimate": "high x ~0 x ~0 ~= 0 — recall-only "
                                    "compare is rigged toward OLD (EVAL.md §4)",
        },
        "parallel_wall": (
            f"4-path parallel — wall = max(t_i) = {max_wall:.1f}s GPU "
            f"compute (NOT sum). g_resource_active_parallel."),
        "total_cost_usd": total_cost,
        "best_joint": {"path": best["path"], "name": best["name"],
                       "SCORE_joint": best["SCORE_joint"]},
        "rows": rows,
    }
    with open(os.path.join(HERE, "comparison_table_v2.json"), "w") as f:
        json.dump(table, f, ensure_ascii=False, indent=2)

    print("=" * 100)
    print("UBM-E6 CONSCIOUSNESS-CARVING 4-path — PARADIGM-NATIVE eval v2 "
          "(2026-05-17)")
    print("=" * 100)
    hdr = (f"{'path':<26}{'ax1 know':<11}{'ax2 chat':<11}"
           f"{'ax3 sep':<10}{'ax4 spont':<11}{'JOINT':<9}{'cost$':<8}")
    print(hdr)
    print("-" * 100)
    for r in rows:
        print(f"{r['name']:<26}{r['axis1_knowledge_access']:<11}"
              f"{r['axis2_chat_uncontaminated']:<11}"
              f"{r['axis3_lane_separation']:<10}{r['axis4_v_spont']:<11}"
              f"{r['SCORE_joint']:<9}{r['cost_usd']:<8}")
    print("-" * 100)
    print(f"best JOINT: {best['name']} = {best['SCORE_joint']}  ·  "
          f"total cost ${total_cost}  ·  parallel wall {max_wall:.0f}s")
    print(f"OLD prefix-injection JOINT ~= 0 (recall 13/15 BUT chat ~0 + "
          f"separation ~0) — HISTORICAL contrast, EVAL.md §4")


if __name__ == "__main__":
    main()
