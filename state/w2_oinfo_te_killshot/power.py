"""PREREG §6 -- power, computed on the PILOT seeds BEFORE any confirm seed is generated.

    MDE   = 3 x q97.5(|pedestal null|)                      (dossier card 1)
    N_REQ = ceil( ((z.95 + z.90) * sd_hat / MDE)^2 ), >= 8, and > 40 => NOT-POWERED
    d_eq  = |pilot positive-control effect| / 10            (TOST margin, fixed pre-confirm)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
Z = 1.6448536269514722 + 1.2815515655446004      # z(.95) + z(.90) = 2.9264
CAP = 40
CONTRASTS = {"C1_positive": ("B_gated", "LSHIFT"),
             "C2G_headline": ("B_gated", "Xp_gated"),
             "C2L_headline": ("B_lin", "Xp_lin")}


def main() -> int:
    a = json.load(open(HERE / "arms_pilot.json"))
    dvs = list(a["star"]["B_gated"].keys())
    out: dict = {"contrasts": {}, "s_tot": {k: float(np.mean(v)) for k, v in a["s_tot"].items()}}

    b, x = out["s_tot"]["B_gated"], out["s_tot"]["Xp_gated"]
    bl, xl = out["s_tot"]["B_lin"], out["s_tot"]["Xp_lin"]
    out["match_gap_gated"] = abs(x - b) / b
    out["match_gap_linear"] = abs(xl - bl) / bl

    for cname, (p, q) in CONTRASTS.items():
        row = {}
        for d in dvs:
            diff = np.array(a["star"][p][d]) - np.array(a["star"][q][d])
            # MDE from the pedestal null of BOTH arms in the contrast (paired difference of two
            # pedestal-subtracted values -> combine the two arms' null spreads)
            nq = math.hypot(float(np.mean(a["null_abs_q975"][p][d])),
                            float(np.mean(a["null_abs_q975"][q][d])))
            mde = 3.0 * nq
            sd = float(diff.std(ddof=1))
            n_req = max(8, math.ceil((Z * sd / mde) ** 2)) if mde > 0 else 10 ** 9
            row[d] = {"pilot_mean": float(diff.mean()), "pilot_sd": sd, "mde": mde,
                      "n_req": int(n_req), "powered": bool(n_req <= CAP)}
        out["contrasts"][cname] = row

    # TOST margin = |positive-control pilot effect| / 10, per DV
    out["d_eq"] = {d: abs(out["contrasts"]["C1_positive"][d]["pilot_mean"]) / 10.0 for d in dvs}
    n_need = [out["contrasts"][c][d]["n_req"] for c in CONTRASTS for d in dvs]
    out["N_CONFIRM"] = int(min(CAP, max(8, max(n_need))))
    out["confirm_seeds"] = list(range(12, 12 + out["N_CONFIRM"]))

    print(f"S_tot match: gated gap {out['match_gap_gated']*100:.2f}%  "
          f"linear gap {out['match_gap_linear']*100:.2f}%")
    for c in CONTRASTS:
        print(f"\n[{c}]")
        for d in dvs:
            r = out["contrasts"][c][d]
            print(f"  {d:12s} mean={r['pilot_mean']:+.6f} sd={r['pilot_sd']:.6f} "
                  f"MDE={r['mde']:.6f} N_REQ={r['n_req']:4d} "
                  f"{'POWERED' if r['powered'] else 'NOT-POWERED(>40)'}")
    print(f"\nd_eq (TOST) = { {k: round(v, 7) for k, v in out['d_eq'].items()} }")
    print(f"N_CONFIRM = {out['N_CONFIRM']}  seeds {out['confirm_seeds'][0]}..{out['confirm_seeds'][-1]}")
    json.dump(out, open(HERE / "power.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
