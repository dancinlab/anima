#!/usr/bin/env python3
"""PURE-PHYSICS (no-CE) eval — paradigm-native 4-axis + HONEST cascade-rate
metric  (RESEARCH.md §11-B).

Runs the paradigm-native 64-anchor eval (eval_carving_dirI.py — 4 axes +
JOINT + routing-broken) on the no-CE ckpt, THEN re-scores the V-SPONT
probe `gen` strings with the HONEST cascade-rate-gated coherence metric
(emergence_metric.py, RESEARCH.md §9). The lenient V-SPONT `coherent`
flag is recorded but NOT trusted — §8.2/§9 proved it gives garbled
byte-cascade 5/5. The honest metric is the GOAL-distance standard.

The §8 CE-trained Dir-I diverse baseline (honest 2/5, lenient 5/5) is the
direct comparison. The verdict question (RESEARCH.md §11-B): is pure-
physics (i) producing a coherent signal on the honest metric, (ii)
degenerate, (iii) a DIFFERENT failure mode than CE-trained byte-cascade?

$0 for the honest re-score (deterministic ops on `gen` strings). The
4-axis eval requires one model forward pass on the ckpt.
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emergence_metric import honest_coherent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--max-new", type=int, default=90)
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    paradigm_out = os.path.join(os.path.dirname(args.output),
                                "eval_paradigm_native.json")

    # ── step 1: paradigm-native 4-axis eval (one model forward) ─────────
    rc = subprocess.call([sys.executable,
                          os.path.join(here, "eval_carving_dirI.py"),
                          "--ckpt", args.ckpt, "--output", paradigm_out,
                          "--device", args.device,
                          "--max-new", str(args.max_new)])
    if rc != 0 or not os.path.exists(paradigm_out):
        print(json.dumps({"FATAL": "paradigm-native eval failed",
                          "rc": rc}), flush=True)
        sys.exit(5)
    pn = json.load(open(paradigm_out))

    # ── step 2: HONEST cascade-rate re-score of V-SPONT probes ──────────
    v = pn.get("axis4_v_spont", {})
    probes = v.get("probes", [])
    honest_rows = []
    honest_n = lenient_n = 0
    for i, p in enumerate(probes):
        g = p.get("gen", "") or ""
        ok, m = honest_coherent(g)
        honest_n += int(ok)
        lenient_n += int(bool(p.get("coherent")))
        honest_rows.append({"idx": i, "prompt": p.get("prompt", ""),
                            "lenient_flag": bool(p.get("coherent")),
                            "honest_coherent": ok, **m,
                            "gen_excerpt": g[:80]})

    # ── §8 CE-trained Dir-I diverse baseline (the direct comparison) ────
    # honest re-score from state/verify_emergence_metric_2026_05_18 §9.2
    # table: Dir-I diverse (§8) lenient 5/5 -> honest 2/5.
    s8_baseline = {"fire": "Dir-I diverse (§8, CE-trained)",
                   "v_spont_lenient": "5/5", "coherence_honest": "2/5",
                   "final_ce": 0.000169,
                   "note": ("§8 CE-trained: deep memorization (final_ce "
                            "0.000169) + byte-cascade collapse; honest "
                            "metric rejects 3/5 V-SPONT probes as "
                            "digit-cascade (max_run 21/16/11 ≥ 10).")}

    n_probes = max(1, len(probes))
    result = {
        "eval_version": "purephysics-noce-honest-v1",
        "direction": "RESEARCH.md §11-B PURE-PHYSICS (no-CE)",
        "ckpt": os.path.abspath(args.ckpt),
        "ckpt_sha256": pn.get("ckpt_sha256"),
        "honest_framing": (
            "V-SPONT lenient `coherent` flag is RECORDED but NOT trusted "
            "(§8.2/§9 proved it gives garbled byte-cascade 5/5). The "
            "HONEST cascade-rate-gated metric (emergence_metric.py, "
            "RESEARCH.md §9, B-EMERGE 7/7 🔵) is the GOAL-distance "
            "standard. honest_coherent is NECESSARY-NOT-SUFFICIENT — a "
            "collapse detector, not a capability proof (g3)."),
        "paradigm_native_4axis": {
            "axis1_knowledge_access":
                pn.get("axis1_knowledge_access", {}).get("primary_score"),
            "axis1_routing": pn.get("axis1_knowledge_access", {})
                .get("routing_accuracy"),
            "axis2_chat_uncontaminated":
                pn.get("axis2_chat_uncontaminated", {}).get("score"),
            "axis3_lane_separation":
                pn.get("axis3_lane_separation", {}).get("score"),
            "axis4_v_spont_lenient":
                pn.get("axis4_v_spont", {}).get("score"),
            "JOINT": pn.get("joint_metric", {}).get("SCORE_joint"),
            "routing_broken_vs_flat":
                pn.get("dir_i_emergence_check", {})
                .get("routing_broken_vs_1_31_flat")},
        "honest_emergence_metric": {
            "metric": "cascade-rate-gated coherence (RESEARCH.md §9)",
            "v_spont_lenient": f"{lenient_n}/{n_probes}",
            "v_spont_honest_coherent": f"{honest_n}/{n_probes}",
            "delta_lenient_to_honest": honest_n - lenient_n,
            "per_probe": honest_rows},
        "ce_baseline_comparison": s8_baseline,
        "honest_note": (
            "honest coherence counts byte-cascade-free probes only — it "
            "is NOT a count of correct emergence (B-EMERGE-7 necessary-"
            "not-sufficient). pure-physics may be DEGENERATE; that is an "
            "honest result confirming CE is load-bearing (g3, no "
            "over-claim)."),
    }
    with open(args.output, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("EVAL_RESULT_WRITTEN", flush=True)
    print(json.dumps({
        "direction": "purephysics_noce",
        "axis1_routing": result["paradigm_native_4axis"]["axis1_routing"],
        "JOINT": result["paradigm_native_4axis"]["JOINT"],
        "v_spont_lenient": f"{lenient_n}/{n_probes}",
        "v_spont_honest": f"{honest_n}/{n_probes}",
        "ce_baseline_honest": s8_baseline["coherence_honest"]},
        ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
