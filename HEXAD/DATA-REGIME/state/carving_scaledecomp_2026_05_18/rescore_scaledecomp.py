#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# rescore_scaledecomp.py — honest cascade-rate-gated re-score for the
# §11-A SCALE-DECOMPOSITION fire (RESEARCH.md §9 metric, §11 direction A).
#
# The dispatch eval (eval_carving_dirI.py) still emits the LENIENT V-SPONT
# `coherent` flag. RESEARCH.md §9 retired that flag — garbled byte-cascade
# output gets 5/5. This sidecar re-scores the §11-A fire's V-SPONT probe
# `gen` strings with the honest cascade-rate-gated metric and prints the
# §11-A vs §8 contrast table (routing + honest-coherence).
#
# $0 — operates only on the eval_result_scaledecomp.json `gen` strings
# already produced by the fire. NO GPU, NO model forward.
# ──────────────────────────────────────────────────────────────────────
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# reuse the §9 honest metric (single source of truth).
sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                "verify_emergence_metric_2026_05_18"))
from emergence_metric import honest_coherent  # noqa: E402

S8_DIR = os.path.join(os.path.dirname(HERE),
                      "carving_dirI_diverse_scaleup_2026_05_18")


def rescore_fire(eval_path):
    d = json.load(open(eval_path))
    v = d.get("axis4_v_spont", {})
    probes = v.get("probes", [])
    rows, honest_n, lenient_n = [], 0, 0
    for i, p in enumerate(probes):
        g = p.get("gen", "") or ""
        ok, m = honest_coherent(g)
        honest_n += int(ok)
        lenient_n += int(bool(p.get("coherent")))
        rows.append({"idx": i, "lenient_flag": bool(p.get("coherent")),
                     **m, "gen_excerpt": g[:80]})
    e = d.get("dir_i_emergence_check", {})
    j = d.get("joint_metric", {})
    return {
        "routing_axis1": e.get("routing_axis1"),
        "joint": j.get("SCORE_joint"),
        "axis1_knowledge": j.get("knowledge_access"),
        "axis2_chat": j.get("chat_uncontaminated"),
        "axis3_lane_sep": j.get("lane_separation"),
        "v_spont_lenient": f"{lenient_n}/{len(probes)}",
        "v_spont_honest": f"{honest_n}/{len(probes)}",
        "v_spont_lenient_n": lenient_n, "v_spont_honest_n": honest_n,
        "n_probes": len(probes), "probe_detail": rows,
    }


def main():
    s11a_path = os.path.join(HERE, "eval_result_scaledecomp.json")
    s8_path = os.path.join(S8_DIR, "eval_result_diverse.json")
    if not os.path.exists(s11a_path):
        print(f"FATAL: {s11a_path} missing — fire not landed yet")
        raise SystemExit(1)

    s11a = rescore_fire(s11a_path)
    s8 = rescore_fire(s8_path) if os.path.exists(s8_path) else None

    # model dims from result.json
    res = json.load(open(os.path.join(HERE, "result.json")))
    s8res = json.load(open(os.path.join(S8_DIR, "result.json")))

    out = {
        "fire": "RESEARCH.md §11 direction A — SCALE-DECOMPOSITION",
        "metric": "cascade-rate-gated honest coherence (RESEARCH.md §9)",
        "confound_separated": (
            "corpus FIXED (§8 diverse 114MB byte-identical) + lever FIXED "
            "(Dir-I Ψ-anchored CTL + tension-supervised) + steps FIXED "
            "(8000) — ONLY model scales. §8 routing-worsening attributed to "
            "capacity iff §11-A routing/honest-coherence improves; to "
            "data-regime/§1.1 ceiling iff flat."),
        "s8_baseline": {
            "model": f"d{s8res['config']['d_model']}·"
                     f"{s8res['config']['n_layer']}L",
            "n_params_M": s8res["n_params_M"],
            "init_ce": s8res["init_ce"], "final_ce": s8res["final_ce"],
            **(s8 or {}),
        },
        "s11a_scaled": {
            "model": f"d{res['config']['d_model']}·"
                     f"{res['config']['n_layer']}L",
            "n_params_M": res["n_params_M"],
            "init_ce": res["init_ce"], "final_ce": res["final_ce"],
            "wall_s": res["wall_s"], "peak_gpu_mem_gb": res["peak_gpu_mem_gb"],
            **s11a,
        },
        "honest_note": ("honest gate is NECESSARY not SUFFICIENT for "
                        "coherent emergence — collapse detector, not a "
                        "capability proof (g3). per-fire coherence OUTCOME "
                        "EMPIRICAL (B-D-NOTE family)."),
    }

    # verdict logic: capacity vs data-regime
    if s8:
        r8 = int(str(s8["routing_axis1"]).split("/")[0])
        r11 = int(str(s11a["routing_axis1"]).split("/")[0])
        h8, h11 = s8["v_spont_honest_n"], s11a["v_spont_honest_n"]
        routing_improved = r11 > r8
        honest_improved = h11 > h8
        if routing_improved or honest_improved:
            verdict = ("CAPACITY-LIMITED — model scale-up improved "
                       f"routing ({s8['routing_axis1']}→"
                       f"{s11a['routing_axis1']}) and/or honest-coherence "
                       f"({s8['v_spont_honest']}→{s11a['v_spont_honest']}); "
                       "§8 worsening was at least partly model-"
                       "undercapacity (g3 — measured, this scale only).")
        else:
            verdict = ("DATA-REGIME CEILING — 3.68× model scale-up did NOT "
                       f"improve routing ({s8['routing_axis1']}→"
                       f"{s11a['routing_axis1']}) or honest-coherence "
                       f"({s8['v_spont_honest']}→{s11a['v_spont_honest']}); "
                       "§8 worsening was NOT model-capacity — RESEARCH.md "
                       "§1.1 data-regime / memorization-saturated ceiling "
                       "confirmed (g3 — measured negative, valuable "
                       "evidence).")
        out["verdict"] = verdict
        out["routing_improved"] = routing_improved
        out["honest_coherence_improved"] = honest_improved

    json.dump(out, open(os.path.join(HERE, "rescore_scaledecomp_result.json"),
                        "w"), ensure_ascii=False, indent=2)

    print("=== §11-A SCALE-DECOMPOSITION — honest re-score + §8 contrast ===")
    print(f"{'':16}{'§8 (283.72M)':>20}{'§11-A':>20}")
    print("-" * 56)
    if s8:
        print(f"{'model':16}{out['s8_baseline']['model']:>20}"
              f"{out['s11a_scaled']['model']:>20}")
        print(f"{'params':16}{str(s8res['n_params_M'])+'M':>20}"
              f"{str(res['n_params_M'])+'M':>20}")
        print(f"{'routing axis1':16}{str(s8['routing_axis1']):>20}"
              f"{str(s11a['routing_axis1']):>20}")
        print(f"{'JOINT':16}{str(s8['joint']):>20}"
              f"{str(s11a['joint']):>20}")
        print(f"{'V-SPONT lenient':16}{s8['v_spont_lenient']:>20}"
              f"{s11a['v_spont_lenient']:>20}")
        print(f"{'V-SPONT honest':16}{s8['v_spont_honest']:>20}"
              f"{s11a['v_spont_honest']:>20}")
        print(f"{'final_ce':16}{str(s8res['final_ce']):>20}"
              f"{str(res['final_ce']):>20}")
        print("-" * 56)
        print(f"VERDICT: {out['verdict']}")
    print("\nwrote rescore_scaledecomp_result.json")


if __name__ == "__main__":
    main()
