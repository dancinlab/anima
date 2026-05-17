#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
# judge_3way.py — RESEARCH.md §18 3-way re-score + combined metric
#
#   lenient V-SPONT (§8.2)  vs  honest cascade-rate (§9, NECESSARY)
#                           vs  LLM-judge rubric (§18, SUFFICIENT-as-rubric)
#
#   combined(probe) = honest_coherent(§9) AND judge_coherent(§18)
#                   = cascade-free  AND  rubric coherent+correct+spontaneous
#
#   $0 — no GPU, no model forward, no new fire. Reads:
#     - §9 rescore_result.json (lenient + honest cascade per probe)
#     - §18 judge_scores.json  (this dir; LLM-judge per probe, hand-applied)
#
#   HONESTY (g3): the §9 side is closed (B-EMERGE-1..7 sympy/Boolean).
#   The §18 judge side is EMPIRICAL — subjective + non-deterministic.
#   No closed verdict is claimed for the judge. Passing combined is NOT a
#   capability proof; it means "cascade-free AND rubric-coherent" only.
# ──────────────────────────────────────────────────────────────────────
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RESCORE = os.path.join(ROOT, "state/verify_emergence_metric_2026_05_18/rescore_result.json")
JUDGE = os.path.join(HERE, "judge_scores.json")

# fire-name reconciliation: §9 rescore uses "UBM-E6 α (alpha)" etc.;
# §18 judge_scores uses ASCII keys. Map §9 -> §18.
N9_TO_N18 = {
    "UBM-E6 α (alpha)": "UBM-E6 alpha",
    "UBM-E6 β (beta)":  "UBM-E6 beta",
    "UBM-E6 γ (gamma)": "UBM-E6 gamma",
    "UBM-E6 weave":     "UBM-E6 weave",
    "UBM-E7 α":         "UBM-E7 alpha",
    "Dir-A tension":    "Dir-A tension",
    "Dir-B intuitor":   "Dir-B intuitor",
    "Dir-C prime":      None,                 # no V-SPONT probe
    "Dir-D cde":        "Dir-D cde",
    "Dir-E superpos":   "Dir-E superpos",
    "Dir-F abstractcot":"Dir-F abstractcot",
    "Dir-G psi_ctl":    "Dir-G psi_ctl",
    "Dir-H tension_sup":"Dir-H tension_sup",
    "Dir-I psictl":     "Dir-I psictl",
    "Dir-I diverse (§8)":"Dir-I diverse (§8)",
}


def main():
    r9 = json.load(open(RESCORE))
    j18 = json.load(open(JUDGE))["per_fire"]

    # index §9 per-probe by fire
    pp9 = r9["per_probe"]

    rows = []
    tot_l = tot_h = tot_j = tot_c = tot_n = 0
    tot_judge_pass_among_honest = 0   # of probes §9 passes, how many judge passes
    tot_honest_pass = 0
    for r in r9["rescore_table"]:
        fire = r["fire"]
        if "lenient_n" not in r:           # Dir-C / missing
            rows.append({"fire": fire, "lenient": r["lenient"],
                         "honest": r["honest"], "judge": "N/A",
                         "combined": "N/A", "note": r.get("note", "")})
            continue
        n18key = N9_TO_N18.get(fire)
        jp = j18.get(n18key, [])
        probes9 = pp9[fire]
        n = len(probes9)
        ln = r["lenient_n"]
        hn = r["honest_n"]
        jn = sum(p["judge"] for p in jp)
        cn = 0
        for i in range(n):
            h_ok = probes9[i]["honest_coherent"]
            j_ok = bool(jp[i]["judge"]) if i < len(jp) else False
            if h_ok:
                tot_honest_pass += 1
                if j_ok:
                    tot_judge_pass_among_honest += 1
            if h_ok and j_ok:
                cn += 1
        rows.append({"fire": fire, "lenient": f"{ln}/{n}",
                     "honest": f"{hn}/{n}", "judge": f"{jn}/{n}",
                     "combined": f"{cn}/{n}",
                     "lenient_n": ln, "honest_n": hn, "judge_n": jn,
                     "combined_n": cn, "total": n})
        tot_l += ln; tot_h += hn; tot_j += jn; tot_c += cn; tot_n += n

    out = {
        "metric": "RESEARCH.md §18 — 3-way (lenient/§9 honest/§18 judge) + combined",
        "judge_is_empirical": True,
        "combined_def": "honest_coherent (§9, necessary, closed) AND judge_coherent (§18, sufficient-as-rubric, empirical)",
        "rescore_3way": rows,
        "totals": {
            "lenient": f"{tot_l}/{tot_n}",
            "honest_cascade": f"{tot_h}/{tot_n}",
            "llm_judge": f"{tot_j}/{tot_n}",
            "combined": f"{tot_c}/{tot_n}",
        },
        "sufficiency_gap": {
            "honest_cascade_pass_probes": tot_honest_pass,
            "of_which_judge_pass": tot_judge_pass_among_honest,
            "of_which_judge_fail": tot_honest_pass - tot_judge_pass_among_honest,
            "interpretation": (
                f"§9 cascade-gate passes {tot_honest_pass} probes; the LLM-judge "
                f"finds only {tot_judge_pass_among_honest} of them coherent+correct+"
                f"spontaneous. {tot_honest_pass - tot_judge_pass_among_honest} §9-pass "
                f"probes are word-mangled / fragmentary / header-dumps that are NOT "
                f"cascades — this is the §9.3(3) necessary-not-sufficient gap, "
                f"quantified."
            ),
        },
        "honest_c3": [
            "judge is EMPIRICAL not closed — subjective + non-deterministic; "
            "calibration = explicit rubric + pinned exemplars + per-probe rationale.",
            "every combined-pass probe is flagged memorized=true (verbatim corpus "
            "continuation) — sufficient-as-rubric, NOT novel emergence.",
            "over-claim 0: combined pass is 'cascade-free AND rubric-coherent', "
            "not a GOAL capability proof; held-out generalization still unmeasured ($0).",
        ],
    }
    json.dump(out, open(os.path.join(HERE, "judge_3way_result.json"), "w"),
              ensure_ascii=False, indent=2)

    print("=== RESEARCH.md §18 — 3-way re-score (lenient / §9 honest / §18 judge / combined) ===")
    print(f"{'fire':<22}{'lenient':>9}{'honest':>9}{'judge':>9}{'combined':>10}")
    print("-" * 59)
    for r in rows:
        print(f"{r['fire']:<22}{r['lenient']:>9}{r['honest']:>9}"
              f"{r['judge']:>9}{r['combined']:>10}"
              + (("   " + r['note']) if r.get('note') else ""))
    print("-" * 59)
    print(f"{'TOTAL (scored)':<22}{out['totals']['lenient']:>9}"
          f"{out['totals']['honest_cascade']:>9}{out['totals']['llm_judge']:>9}"
          f"{out['totals']['combined']:>10}")
    print()
    print(out["sufficiency_gap"]["interpretation"])
    print(f"\nwrote judge_3way_result.json")


if __name__ == "__main__":
    main()
