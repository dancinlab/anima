"""STRENGTH-CONFOUND audit -- the control that can kill this experiment's own positive.

H_9294's lesson (memory `control-must-match-mediating-covariate`): a control matched on NOMINAL
capacity is not a control; you must match (or regress out) the covariate that actually mediates the
outcome.  The B vs X' pair was matched on S_tot (total pairwise MI) because S_tot mediates Phi*.
It does NOT follow that S_tot mediates Omega -- and the residual match gap is not exactly 0
(0.13% gated / 0.50% linear).

So: measure dOmega*/dS_tot directly, by sweeping X's W_RELAY over a grid, and ask whether the
residual S_tot gap ALONE predicts the observed Delta.  If it does, the "structure" signal is a
strength artifact and dies.  Running this can only hurt the positive claim, which is why it runs.

    python3 slope_audit.py <seed> [<seed> ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "1283_content_instrument_repair"))
sys.path.insert(0, str(HERE))

from gated import calibrate_beta, gen
from substrate import X_SHARED

from estimators import DV_NAMES, dv_star
from run_arms import BETA_SEEDS, K, T, s_tot

W_GRID = [0.70, 0.80, 0.90, 1.00, 1.10]


def main() -> int:
    seeds = [int(x) for x in sys.argv[1:]]
    beta, mu, sd = calibrate_beta(BETA_SEEDS, 4096)
    out: dict = {"seeds": seeds, "w_grid": W_GRID, "gated": {}, "linear": {}}

    for sub in ("gated", "linear"):
        rows = {w: {"s_tot": [], **{d: [] for d in DV_NAMES}} for w in W_GRID}
        for s in seeds:
            for w in W_GRID:
                tr = (gen(s, X_SHARED, T, gated=True, beta=beta, mu=mu, sd=sd, w_relay=w)
                      if sub == "gated" else
                      gen(s, X_SHARED, T, gated=False, w_relay=w))
                star, _, _ = dv_star(tr, s, K)
                rows[w]["s_tot"].append(s_tot(tr))
                for d in DV_NAMES:
                    rows[w][d].append(star[d])
            print(f"{sub} seed {s} done", flush=True)
        # slope dDV*/dS_tot from the within-seed grid (paired: same seed across w)
        xs = np.array([np.mean(rows[w]["s_tot"]) for w in W_GRID])
        res = {"s_tot_by_w": {str(w): float(np.mean(rows[w]["s_tot"])) for w in W_GRID}, "slope": {}}
        for d in DV_NAMES:
            ys = np.array([np.mean(rows[w][d]) for w in W_GRID])
            A = np.column_stack([np.ones_like(xs), xs])
            coef = np.linalg.lstsq(A, ys, rcond=None)[0]
            res["slope"][d] = float(coef[1])
            res.setdefault("dv_by_w", {})[d] = {str(w): float(np.mean(rows[w][d])) for w in W_GRID}
        out[sub] = res
        print(f"[{sub}] slopes dDV*/dS_tot = "
              + "  ".join(f"{d}={res['slope'][d]:+.5f}" for d in DV_NAMES))

    json.dump(out, open(HERE / "slope_audit.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
