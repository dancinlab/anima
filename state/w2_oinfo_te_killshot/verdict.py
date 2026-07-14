"""PREREG §7 -- the frozen decision rules, applied to the CONFIRM sample (fresh seeds 12..51).

    PASS (structure detected) : 90% CI excludes 0  AND  |Delta| > MDE
    FAIL (equivalent)         : 90% CI  contained in (-d_eq, +d_eq)          [TOST]
    else                      : INCONCLUSIVE
    C1 (positive control) not detected for a DV  ->  that DV is a DEAD TOOL -> INVALID, not FAIL
    N_REQ > 40                                   ->  NOT-POWERED for MDE-sized effects

Paired-t throughout.  No max(controls) anywhere (that order statistic flipped 7/11 past verdicts).
MDE and d_eq are read from power.json, which was written from the PILOT before these seeds existed.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
CONTRASTS = {"C1_positive": ("B_gated", "LSHIFT"),
             "C2G_headline": ("B_gated", "Xp_gated"),
             "C2L_headline": ("B_lin", "Xp_lin")}


def merge() -> dict:
    arms: dict = {}
    seeds: list[int] = []
    for f in sorted(HERE.glob("arms_confirm*.json")):
        a = json.load(open(f))
        seeds += a["seeds"]
        for k in ("star", "raw", "s_tot"):
            arms.setdefault(k, {})
            for arm, v in a[k].items():
                if isinstance(v, dict):
                    arms[k].setdefault(arm, {})
                    for d, vals in v.items():
                        arms[k][arm].setdefault(d, []).extend(vals)
                else:
                    arms[k].setdefault(arm, []).extend(v)
    arms["seeds"] = seeds
    return arms


def main() -> int:
    a = merge()
    p = json.load(open(HERE / "power.json"))
    n = len(a["seeds"])
    dvs = list(a["star"]["B_gated"].keys())
    tcrit = float(stats.t.ppf(0.95, n - 1))
    out: dict = {"n": n, "seeds": a["seeds"], "contrasts": {},
                 "s_tot": {k: float(np.mean(v)) for k, v in a["s_tot"].items()}}
    out["match_gap_gated"] = abs(out["s_tot"]["Xp_gated"] - out["s_tot"]["B_gated"]) / out["s_tot"]["B_gated"]
    out["match_gap_linear"] = abs(out["s_tot"]["Xp_lin"] - out["s_tot"]["B_lin"]) / out["s_tot"]["B_lin"]
    out["s_tot_gap_abs"] = {"gated": out["s_tot"]["B_gated"] - out["s_tot"]["Xp_gated"],
                            "linear": out["s_tot"]["B_lin"] - out["s_tot"]["Xp_lin"]}

    print(f"n = {n} fresh seeds ({a['seeds'][0]}..{a['seeds'][-1]})   t.95 = {tcrit:.4f}")
    print(f"S_tot match: gated {out['match_gap_gated']*100:.2f}%  linear {out['match_gap_linear']*100:.2f}%\n")

    for c, (u, v) in CONTRASTS.items():
        row = {}
        print(f"[{c}]  {u} - {v}")
        for d in dvs:
            diff = np.array(a["star"][u][d]) - np.array(a["star"][v][d])
            m = float(diff.mean())
            se = float(diff.std(ddof=1) / np.sqrt(n))
            lo, hi = m - tcrit * se, m + tcrit * se
            t = m / se if se > 0 else 0.0
            pv = float(2 * stats.t.sf(abs(t), n - 1))
            mde = p["contrasts"][c][d]["mde"]
            deq = p["d_eq"][d]
            detect = bool((lo > 0 or hi < 0) and abs(m) > mde)
            equiv = bool(lo > -deq and hi < deq)
            row[d] = {"mean": m, "se": se, "ci90": [lo, hi], "t": t, "p": pv,
                      "mde": mde, "d_eq": deq, "detect": detect, "tost_equiv": equiv,
                      "n_req_pilot": p["contrasts"][c][d]["n_req"],
                      "powered_for_mde": p["contrasts"][c][d]["powered"]}
            flag = ("DETECT" if detect else ("TOST-EQUIV" if equiv else "INCONCLUSIVE"))
            if detect and equiv:
                flag = "DETECT+below-d_eq"
            print(f"  {d:12s} {m:+.6f}  90%CI [{lo:+.6f},{hi:+.6f}]  t={t:+7.2f} p={pv:.2e}  "
                  f"MDE={mde:.6f} d_eq={deq:.6f}  -> {flag}")
        out["contrasts"][c] = row
        print()

    json.dump(out, open(HERE / "verdict.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
