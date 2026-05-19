#!/usr/bin/env python3
"""UBM-E6 4-path comparison table builder — assembles fire + eval results
into a single comparison_table.json + console table.

HONEST FRAMING (g3): per-axis scores EMPIRICAL (B-CARVE-E6-NOTE). The
old prefix-injection baseline (manual_match 13/15 + chat NET LOSS 5/5→1/5)
is HISTORICAL evidence only (f3), used here strictly as a contrast anchor.
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
# vast.ai cost: rate ($/hr) × wall_hours, recorded per fire.
COST = {"alpha": 0.760, "beta": 0.760, "gamma": 0.734, "weave": 0.655}


def main():
    rows = []
    for p in PATHS:
        fire = json.load(open(os.path.join(HERE, "out", p, "result.json")))
        ev = json.load(open(os.path.join(HERE, "out", p, "eval_result.json")))
        # cost = rate × (wall + ~6 min boot/upload/pull overhead)
        wall_h = (fire["wall_s"] + 360) / 3600.0
        cost = round(COST[p] * wall_h, 4)
        rows.append({
            "path": p,
            "name": PATH_NAMES[p],
            "init_ce": fire["init_ce"],
            "final_ce": fire["final_ce"],
            "ce_descent": fire["ce_descent"],
            "wall_s": fire["wall_s"],
            "cost_usd": cost,
            "n_params_M": fire["n_params_M"],
            "eternal_delta_max": (fire["eternal_info"]["eternal_delta_max"]
                                  if fire.get("eternal_info") else None),
            "knowledge_recall": ev["knowledge_recall"]["score"],
            "chat_uncontaminated": ev["chat_uncontaminated"]["clean"],
            "p3_leak_total": ev["chat_uncontaminated"]["p3_leak_total"],
            "v_spont": ev["v_spont"]["score"],
            "ckpt_sha256": ev["ckpt_sha256"],
        })

    total_cost = round(sum(r["cost_usd"] for r in rows), 4)
    max_wall = max(r["wall_s"] for r in rows)

    table = {
        "phase": "UBM-E6 CONSCIOUSNESS-CARVING 4-path GPU fire",
        "date": "2026-05-17",
        "substrate": "PyTorch (NOT hexa-native — g3 honest framing carry)",
        "arch": "ConsciousDecoderV2 d=512 n_layer=8 (85.8M params)",
        "corpus": "corpus_carving.jsonl (carving corpus, NOT chat SFT)",
        "honest_framing": (
            "Per-axis scores EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE family). "
            "4-path comparison = empirical. Carving MECHANISM transfer-forms "
            "(B-VAC/B-MIT-ETN/B-NAR/B-CARVE-E6) = closed 🔵. OLD prefix-"
            "injection baseline (manual_match 13/15, chat 5/5->1/5 NET LOSS) "
            "= HISTORICAL contrast only (f3, NOT a target)."),
        "parallel_wall": (
            f"4-path parallel — wall = max(t_i) = {max_wall:.1f}s of GPU "
            f"compute (NOT sum); dispatch incl. boot/pull overhead per path. "
            f"g_resource_active_parallel."),
        "total_cost_usd": total_cost,
        "old_paradigm_contrast": {
            "knowledge_recall": "13/15 manual_match (BG-HS R1, HISTORICAL)",
            "chat_regression": "V5.8 std_greedy 5/5 -> 1/5 NET LOSS "
                               "(Phase 1A.5, feedback_corpus_quality_over_scale)",
            "p3_leak": "BAKED into base ckpt, SFT cannot scrub "
                       "(project_anima_base_ckpt_baked_p3_leak)",
        },
        "rows": rows,
    }
    with open(os.path.join(HERE, "comparison_table.json"), "w") as f:
        json.dump(table, f, ensure_ascii=False, indent=2)

    # console table
    print("=" * 96)
    print("UBM-E6 CONSCIOUSNESS-CARVING 4-path comparison (2026-05-17)")
    print("=" * 96)
    hdr = (f"{'path':<26}{'init→final CE':<20}{'knowledge':<11}"
           f"{'chat-clean':<13}{'V-SPONT':<10}{'cost$':<9}")
    print(hdr)
    print("-" * 96)
    for r in rows:
        ce = f"{r['init_ce']:.2f}→{r['final_ce']:.4f}"
        cc = f"clean({r['p3_leak_total']})" if r["chat_uncontaminated"] \
            else f"LEAK({r['p3_leak_total']})"
        print(f"{r['name']:<26}{ce:<20}{r['knowledge_recall']:<11}"
              f"{cc:<13}{r['v_spont']:<10}{r['cost_usd']:<9}")
    print("-" * 96)
    print(f"total cost ${total_cost}  ·  parallel wall = "
          f"max GPU compute {max_wall:.0f}s")
    print(f"OLD prefix-injection: knowledge 13/15 BUT chat 5/5→1/5 NET LOSS "
          f"+ P3 leak BAKED (HISTORICAL contrast)")


if __name__ == "__main__":
    main()
