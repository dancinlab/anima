"""STAGE-1 metric fix (@L1) — re-measure the round-1 DISSOLVE sweep with Pielou J.

ROUND-1 verdict (H_852, dissolve_sweep_2026_05_30): the uniform-null z-score
COLLAPSED as E grew (mean_z 0.53 -> -7.61 over E=4..64), so DISSOLVE was ruled
red. ROUND-2 mining (CLM.breakthrough.mining.md) found that this is a RULER
ARTIFACT: the z metric measures (H_obs - null_mu) / null_sigma, but BOTH the
uniform ceiling ln(E) AND null_mu grow with E, so even though the raw dispatch
entropy H_obs RISES (1.19 -> 3.17 nats), the gap to the ever-higher uniform
ceiling shrinks and z plunges.

The fix (@L1) replaces the ruler with the ecological evenness index
**Pielou's J = H / ln(E)**, which DIVIDES OUT the ln(E) ceiling growth directly.
J in [0, 1] (1 = perfectly balanced dispatch). The question becomes:

    is J monotone non-decreasing over E = 4 -> 64?  (does DISSOLVE flip?)

We re-measure the EXISTING round-1 data (no model change, no re-run, $0) by
reading dissolve_sweep_2026_05_30.json's per_run H_obs values and recomputing
J = H_obs / ln(E) per (E, seed). The frozen falsifier threshold is NOT touched
(@L5); a non-monotone J is reported honestly as a valid finding.

Run:  python3 CLM/model/measure_pielou.py [--src <dissolve.json>]
Env:  PIELOU_TXT to persist the stdout verbatim.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Dict, List

# frozen STAGE-1 re-measure falsifier (mirrors round-1 mono semantics, @L5)
MONO_TOL = 0.02   # J is in [0,1]; allow a 0.02 evenness dip as "non-decreasing"
MIN_RISE = 0.0    # DISSOLVE-flip = J(E64) >= J(E4) within tol (escape scales)


def pielou_j(h_nats: float, n_experts: int) -> float:
    """Pielou's evenness J = H / ln(E). E<=1 -> 0 by convention."""
    return h_nats / math.log(n_experts) if n_experts > 1 else 0.0


def remeasure(src_path: str) -> Dict:
    data = json.load(open(src_path))
    per_run = data["per_run"]
    axis = data["frozen"]["axis"]

    # group J by E (using the round-1 raw H_obs — no re-run)
    by_e: Dict[int, List[float]] = {e: [] for e in axis}
    rows: List[Dict] = []
    for r in per_run:
        e = int(r["n_experts"])
        j = pielou_j(float(r["H_obs"]), e)
        by_e[e].append(j)
        rows.append({
            "n_experts": e, "seed": r["seed"], "H_obs": r["H_obs"],
            "z_round1": r["z"], "pielou_J": round(j, 5),
        })

    mean_j = [round(sum(by_e[e]) / len(by_e[e]), 5) for e in axis]

    # monotone non-decreasing (within MONO_TOL) over the E axis
    mono = all(mean_j[i + 1] >= mean_j[i] - MONO_TOL for i in range(len(mean_j) - 1))
    rise = round(mean_j[-1] - mean_j[0], 5)
    # the round-1 z sweep for the same data (for the cross-check table)
    mean_z = [data["per_E"][str(e)]["mean_z"] for e in axis]

    passed = bool(mono and rise >= MIN_RISE - MONO_TOL)
    return {
        "src": os.path.basename(src_path),
        "metric": "Pielou J = H / ln(E) (ecological evenness, ln(E) ceiling divided out)",
        "frozen": {
            "axis": axis, "seeds": data["frozen"]["seeds"],
            "mono_tol": MONO_TOL, "min_rise": MIN_RISE,
            "falsifier": ("F-CLM-PIELOU-DISSOLVE: Pielou J monotone non-decreasing "
                          "(within mono_tol) over E AND J(E64) >= J(E4) (escape "
                          "scales with chip count under the ln(E)-corrected ruler)"),
        },
        "per_run": rows,
        "axis": axis,
        "mean_pielou_J": mean_j,
        "mean_z_round1": mean_z,
        "J_monotone_non_decr": mono,
        "J_rise_E64_minus_E4": rise,
        "round1_z_monotone": data.get("monotone_non_decr", False),
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("\U0001f7e2 SUPPORTED-NUMERICAL" if passed else "\U0001f534 CLOSED-NEGATIVE"),
        "scale_scope": ("toy expert-count sweep (d64/L2, toy two-lane) re-measured "
                        "from round-1 H_obs -- a_scale_honest_scope (toy != production)"),
    }


def fmt(res: Dict) -> str:
    L = ["F-CLM-PIELOU-DISSOLVE -- DISSOLVE re-measured with Pielou J = H/ln(E)",
         "=" * 72,
         f"source        : {res['src']} (round-1 raw H_obs, no re-run, $0)",
         f"metric        : {res['metric']}",
         "",
         "FROZEN (@L5, ruler swapped, thresholds not tampered):"]
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'E':>4} {'seed':>5} {'H_obs':>9} {'z_round1':>9} {'Pielou_J':>9}")
    for r in res["per_run"]:
        L.append(f"{r['n_experts']:>4} {r['seed']:>5} {r['H_obs']:>9.4f} "
                 f"{r['z_round1']:>9.4f} {r['pielou_J']:>9.4f}")
    L.append("")
    L.append(f"axis (E)            : {res['axis']}")
    L.append(f"mean Pielou J       : {res['mean_pielou_J']}")
    L.append(f"mean z (round-1)    : {res['mean_z_round1']}")
    L.append(f"J monotone non-decr : {res['J_monotone_non_decr']} (tol {res['frozen']['mono_tol']})")
    L.append(f"J rise (E64 - E4)   : {res['J_rise_E64_minus_E4']} (threshold >= {res['frozen']['min_rise']})")
    L.append(f"round-1 z monotone  : {res['round1_z_monotone']} (the artifact verdict)")
    L.append(f"scale scope         : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    L.append("")
    L.append("READING: raw dispatch entropy H_obs RISES with E (1.19 -> 3.17 nats),")
    L.append("but Pielou J (evenness) does NOT improve -- so the ln(E) ceiling was")
    L.append("only PART of the round-1 z-collapse. The router's per-expert balance")
    L.append("stays ~flat/slightly down as E grows: experts proliferate but evenness")
    L.append("does not scale. See verdict tier for the honest ruling.")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    default_src = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".verdicts", "clm-mitosis-array", "dissolve_sweep_2026_05_30.json",
    )
    ap.add_argument("--src", default=default_src)
    a = ap.parse_args()
    if not os.path.exists(a.src):
        print(f"ERROR: dissolve sweep JSON not found: {a.src}", file=sys.stderr)
        sys.exit(2)
    res = remeasure(a.src)
    txt = fmt(res)
    print(txt, flush=True)
    if os.environ.get("PIELOU_TXT"):
        open(os.environ["PIELOU_TXT"], "w").write(txt)
    if os.environ.get("PIELOU_JSON"):
        json.dump(res, open(os.environ["PIELOU_JSON"], "w"), indent=2)


if __name__ == "__main__":
    main()
