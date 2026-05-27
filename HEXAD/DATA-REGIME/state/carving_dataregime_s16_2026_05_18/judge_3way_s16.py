#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# judge_3way_s16.py — RESEARCH.md §16 V-SPONT 3-way re-score + combined
#
#   lenient V-SPONT (§8.2)  vs  honest cascade-rate (§9, NECESSARY, closed)
#                           vs  LLM-judge rubric  (§18, SUFFICIENT-as-rubric,
#                                                   EMPIRICAL)
#
#   combined(probe) = honest_coherent(§9) AND judge_coherent(§18)
#
#   $0 — no GPU, no model forward, no new fire. Reads only:
#     - eval_result_s16.json   (lenient flag + gen strings)
#     - §9 emergence_metric.py (cascade-rate honest, single SSOT import)
#     - judge_scores_s16.json  (this dir; §18 LLM-judge, hand-applied)
#
#   HONESTY (g3): §9 side is closed (B-EMERGE-1..7 sympy/Boolean). §18
#   judge side is EMPIRICAL — subjective + non-deterministic. combined
#   pass is "cascade-free AND rubric-coherent", NOT a GOAL capability
#   proof; held-out generalization unmeasured.
# ──────────────────────────────────────────────────────────────────────
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(
    ROOT, "state", "verify_emergence_metric_2026_05_18"))
from emergence_metric import honest_coherent  # §9 SSOT — no re-impl

# §8 / §11-A 3-way baselines (from the 14-way §18 pass —
# state/verify_llm_judge_metric_2026_05_18/judge_3way_result.json).
S8 = {"label": "§8 Dir-I diverse (114MB / 283.72M / 64-anchor)",
      "routing": "2/64", "lenient": "5/5", "honest": "2/5", "judge": "0/5",
      "combined": "0/5"}
S11A = {"label": "§11-A SCALE-DECOMP (114MB / 1044.46M 3.68×)",
        "routing": "1/64", "lenient": "1/5", "honest": "2/5",
        "judge": "0/5", "combined": "0/5"}


def main():
    ev = json.load(open(os.path.join(HERE, "eval_result_s16.json")))
    js = json.load(open(os.path.join(HERE, "judge_scores_s16.json")))
    jp = js["per_fire"]["S16 dataregime curriculum"]

    probes = ev["axis4_v_spont"]["probes"]
    n = len(probes)
    lenient_n = honest_n = judge_n = combined_n = 0
    rows = []
    for i, p in enumerate(probes):
        g = p.get("gen", "") or ""
        h_ok, m = honest_coherent(g)
        len_ok = bool(p.get("coherent"))
        j_ok = bool(jp[i]["judge"]) if i < len(jp) else False
        c_ok = h_ok and j_ok
        lenient_n += int(len_ok)
        honest_n += int(h_ok)
        judge_n += int(j_ok)
        combined_n += int(c_ok)
        rows.append({
            "idx": i, "prompt": p.get("prompt"),
            "lenient": len_ok, "honest_cascade": h_ok,
            "llm_judge": j_ok, "combined": c_ok,
            "cascade_rate": m["cascade_rate"], "max_run": m["max_run"],
            "judge_why": jp[i]["why"], "gen_excerpt": g[:80]})

    out = {
        "fire": "RESEARCH.md §16 — GOAL-legitimate LARGE-SCALE "
                "DATA-REGIME + CURRICULUM (Dir-I lever)",
        "metric": "RESEARCH.md §18 3-way: lenient V-SPONT (§8.2) / "
                  "§9 honest cascade-rate (closed) / §18 LLM-judge "
                  "(empirical) + combined",
        "judge": "Claude Opus 4.7 (1M context) — same judge as 14-way "
                 "§18 pass; EMPIRICAL not closed",
        "combined_def": "honest_coherent (§9, necessary, closed) AND "
                        "judge_coherent (§18, sufficient-as-rubric, "
                        "empirical)",
        "s8_baseline_3way": S8,
        "s11a_baseline_3way": S11A,
        "s16_3way": {
            "label": "§16 (~603MB file / ~360MB carving stream / "
                     "283.72M / 168-anchor + §12.1 Q1-c curriculum)",
            "routing_axis1": ev["axis1_knowledge_access"][
                "routing_accuracy"],
            "joint": ev["joint_metric"]["SCORE_joint"],
            "lenient": f"{lenient_n}/{n}",
            "honest_cascade": f"{honest_n}/{n}",
            "llm_judge": f"{judge_n}/{n}",
            "combined": f"{combined_n}/{n}",
        },
        "per_probe": rows,
        "verdict": (
            "ROUTING-POSITIVE, V-SPONT NEGATIVE-3-WAY — §16 ~5× data + "
            "curriculum moved axis-1 routing 2/64→21/64 (the first large "
            "break of the 13-way+§8+§11 universal-FLAT 1/31~2/64), but "
            "the V-SPONT spontaneous-emission axis is honest 1/5 (BELOW "
            "§8/§11-A honest 2/5) and LLM-judge 0/5 / combined 0/5 — "
            "every §16 V-SPONT probe is either a char/digit-cascade "
            "(§9 rejects 4/5) or a §9-pass-but-fragmentary memorized-"
            "template shard the §18 judge rejects (1/5). routing↑ is a "
            "measured data-regime positive; spontaneous coherent "
            "emergence is NOT (g3 — over-claim 0, B-S16-NOTE empirical)."),
        "honest_c3": [
            "judge is EMPIRICAL not closed — subjective + "
            "non-deterministic; calibration = §18 rubric + pinned "
            "exemplars + per-probe rationale.",
            "§16 combined = 0/5 — no V-SPONT probe is both cascade-free "
            "AND rubric-coherent; the routing-axis movement does NOT "
            "transfer to the spontaneous-emission axis at this scale.",
            "the lone §9-honest §16 probe (idx 2) is the §9.3(3) "
            "necessary-not-sufficient gap: `자도이`-mangled memorized "
            "template fragment ending in `�` corruption — §9 passes it, "
            "§18 rejects D1.",
            "over-claim 0: routing 21/64 (17 genuine exact-tier, 4 "
            "substring-artifact) ≠ GOAL emergence; V-SPONT 3-way is the "
            "honest counter-evidence that capability ≠ GOAL distance.",
        ],
    }
    op = os.path.join(HERE, "judge_3way_s16_result.json")
    json.dump(out, open(op, "w"), ensure_ascii=False, indent=2)

    print("=== RESEARCH.md §16 — V-SPONT 3-way (lenient / §9 honest / "
          "§18 judge / combined) ===")
    print(f"{'fire':<44}{'routing':>8}{'lenient':>9}{'honest':>8}"
          f"{'judge':>7}{'combined':>10}")
    print("-" * 86)
    for b in (S8, S11A):
        print(f"{b['label']:<44}{b['routing']:>8}{b['lenient']:>9}"
              f"{b['honest']:>8}{b['judge']:>7}{b['combined']:>10}")
    s = out["s16_3way"]
    print(f"{'§16 (~5× data + §12.1 Q1-c curriculum)':<44}"
          f"{str(s['routing_axis1']):>8}{s['lenient']:>9}"
          f"{s['honest_cascade']:>8}{s['llm_judge']:>7}"
          f"{s['combined']:>10}")
    print("-" * 86)
    print(f"VERDICT: {out['verdict']}")
    print(f"wrote {os.path.basename(op)}")


if __name__ == "__main__":
    main()
