"""Generate the four frozen trajectories per seed and score them with the new DVs.

Trajectories (all inherited frozen -- nothing is refit here):
    B_gated   gen(s, B_MULTI,  T, gated=True)                    <- the "gated" arm
    LSHIFT    same substrate, same gate series, circularly shifted (l_shift_pair)  <- positive ctrl
    Xp_gated  gen(s, X_SHARED, T, gated=True,  w_relay=0.90)     <- strength-matched X'
    B_lin     gen(s, B_MULTI,  T, gated=False)
    Xp_lin    gen(s, X_SHARED, T, gated=False, w_relay=0.90)

beta / w* / seeds / substrate all come from H_9295's frozen record.  Usage:
    python3 run_arms.py <tag> <seed> [<seed> ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

H9295 = Path(__file__).resolve().parents[1] / "1283_content_instrument_repair"
sys.path.insert(0, str(H9295))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from faithful_phi import build_mi_matrix
from gated import calibrate_beta, gen, l_shift_pair
from substrate import B_MULTI, NBINS, N_MOD, X_SHARED, rank_uniform

from estimators import DV_NAMES, dv_star

T = 65536
K = 32
W_STAR = 0.90                       # inherited: step3/step4 `w_star`, match_pass=True
BETA_SEEDS = [4, 5, 6, 7, 8, 9, 10, 11]
ADJ = [(0, 1), (1, 2), (2, 3), (3, 0)]
DIAG = [(0, 2), (1, 3)]
ARMS = ["B_gated", "LSHIFT", "Xp_gated", "B_lin", "Xp_lin"]


def s_tot(traj: np.ndarray) -> float:
    """Total pairwise MI -- the covariate the strength-match was built on (H_9294)."""
    mi = build_mi_matrix(rank_uniform(traj).reshape(-1), N_MOD, traj.shape[1], NBINS)
    return float(sum(mi[i, j] for i, j in ADJ + DIAG))


def main() -> int:
    tag, seeds = sys.argv[1], [int(x) for x in sys.argv[2:]]
    beta, mu, sd = calibrate_beta(BETA_SEEDS, 4096)      # arm A alone, frozen -> 0.98847546...
    out: dict = {"tag": tag, "T": T, "K": K, "w_star": W_STAR, "beta": beta, "seeds": seeds,
                 "star": {a: {d: [] for d in DV_NAMES} for a in ARMS},
                 "raw": {a: {d: [] for d in DV_NAMES} for a in ARMS},
                 "s_tot": {a: [] for a in ARMS},
                 "null_abs_q975": {a: {d: [] for d in DV_NAMES} for a in ARMS}}

    for s in seeds:
        g, ls = l_shift_pair(s, B_MULTI, T, beta, mu, sd)
        trajs = {
            "B_gated": g,
            "LSHIFT": ls,
            "Xp_gated": gen(s, X_SHARED, T, gated=True, beta=beta, mu=mu, sd=sd, w_relay=W_STAR),
            "B_lin": gen(s, B_MULTI, T, gated=False),
            "Xp_lin": gen(s, X_SHARED, T, gated=False, w_relay=W_STAR),
        }
        for a in ARMS:
            star, raw, null = dv_star(trajs[a], s, K)
            for d in DV_NAMES:
                out["star"][a][d].append(star[d])
                out["raw"][a][d].append(raw[d])
                out["null_abs_q975"][a][d].append(float(np.quantile(np.abs(null[d]), 0.975)))
            out["s_tot"][a].append(s_tot(trajs[a]))
        print(f"seed {s} done: " + "  ".join(
            f"{d}(B_gated)={out['star']['B_gated'][d][-1]:+.6f}" for d in DV_NAMES), flush=True)

    json.dump(out, open(Path(__file__).resolve().parent / f"arms_{tag}.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
