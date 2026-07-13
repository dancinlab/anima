"""Is the observed Phi even ABOVE its own null? — the pedestal ENSEMBLE, not one draw.

bias_pedestal.py used ONE permutation, so its 1.813 is a single noisy draw from the null
distribution (H_9260's P0 measured that noise at sd ~0.30). The sharper question is where the
arms sit relative to the null MEAN. If E[Phi(null)] >= Phi(arm), then the arms carry no
integration the estimator can see at all — the entire reading is pedestal, and the arm-to-arm
gaps H_1283 cemented verdicts on were differences between two noise draws.

Null construction (true Phi = 0 by construction, marginals byte-identical): per-module
independent time permutation of the arm's own trajectory. Module 0 held at identity — MI is
invariant to a common relabelling of t, so permuting modules 1..n-1 already gives an independent
joint. K draws per arm, Fisher-Yates from a dedicated arm-independent LCG stream (common random
numbers across arms → the arm contrast is paired, not two independent noises).

Reported per arm at the FROZEN T=64, over the FROZEN seeds [3..11]:
    Phi_obs           the arm as H_1283/H_9260 read it
    E[Phi_null]       the pedestal's ensemble mean
    Phi* = obs - E[null]   the pedestal-subtracted quantity (this is what Phi SHOULD have been)
    z = Phi* / sd(null)    how many null-sd's the observation sits above its own null
"""

from __future__ import annotations

import json

import numpy as np

from faithful_phi import faithful_phi
from substrate import (
    A_DIRECT, B_MULTI, DIM, NBINS, N_MOD, N_SELF, R_CHORD, T_TICKS, X_SHARED, Lcg,
    gen_traj, rank_uniform,
)

SEEDS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
K = 32                      # null draws per (arm, seed)
NULL_STREAM = 0x5EED_0000   # arm-independent → common random numbers → paired contrast
ARMS = [("A", A_DIRECT), ("B", B_MULTI), ("X", X_SHARED), ("N", N_SELF), ("R", R_CHORD)]


def perm_indices(rng: Lcg, t: int) -> np.ndarray:
    idx = np.arange(t)
    for k in range(t - 1, 0, -1):
        j = int(abs(rng.gauss()) * 1e6) % (k + 1)
        idx[k], idx[j] = idx[j], idx[k]
    return idx


def null_phis(traj: np.ndarray, k: int) -> np.ndarray:
    """K draws of Phi under 'same marginals, zero cross-module information'."""
    rng = Lcg(NULL_STREAM)
    t = traj.shape[1]
    out = np.empty(k, dtype=np.float64)
    for d in range(k):
        nul = traj.copy()
        for i in range(1, traj.shape[0]):
            nul[i] = traj[i][perm_indices(rng, t)]
        out[d] = faithful_phi(rank_uniform(nul).reshape(-1), N_MOD, t, NBINS)
    return out


def main() -> int:
    rows = []
    print(f"FROZEN T={T_TICKS} · seeds {SEEDS} · K={K} null draws per (arm, seed) "
          f"· faithful IIT-4 exact MIP-EI")
    print(f"{'arm':>5} | {'Phi_obs':>9} {'E[Phi_null]':>12} {'sd(null)':>9} | "
          f"{'Phi*=obs-null':>13} {'z':>7} | obs > E[null] on")
    print("-" * 84)
    for name, mode in ARMS:
        obs_l, mu_l, sd_l, star_l, z_l, wins = [], [], [], [], [], 0
        for s in SEEDS:
            traj = gen_traj(s, mode)
            obs = faithful_phi(rank_uniform(traj).reshape(-1), N_MOD, T_TICKS, NBINS)
            nul = null_phis(traj, K)
            mu, sd = float(nul.mean()), float(nul.std(ddof=1))
            star = obs - mu
            obs_l.append(obs); mu_l.append(mu); sd_l.append(sd); star_l.append(star)
            z_l.append(star / sd if sd > 0 else 0.0)
            wins += int(obs > mu)
        rows.append({"arm": name, "phi_obs": obs_l, "null_mean": mu_l, "null_sd": sd_l,
                     "phi_star": star_l, "z": z_l, "obs_gt_null": wins})
        print(f"{name:>5} | {np.mean(obs_l):9.4f} {np.mean(mu_l):12.4f} {np.mean(sd_l):9.4f} | "
              f"{np.mean(star_l):+13.4f} {np.mean(z_l):+7.2f} | {wins}/9 seeds")

    b = next(r for r in rows if r["arm"] == "B")
    x = next(r for r in rows if r["arm"] == "X")
    a = next(r for r in rows if r["arm"] == "A")
    print()
    print("the H_1283 R6 claim, re-read against the arms' OWN nulls:")
    print(f"   Phi*(B) = {np.mean(b['phi_star']):+.4f}  (B carries {'MORE' if np.mean(b['phi_star'])>0 else 'LESS'} "
          f"integration than a zero-integration system with B's marginals)")
    star_bx = np.array(b["phi_star"]) - np.array(x["phi_star"])
    star_ba = np.array(b["phi_star"]) - np.array(a["phi_star"])
    print(f"   Phi*(B) - Phi*(X) = {star_bx.mean():+.4f}  (the disjointness claim · frozen bar +0.02 · "
          f"every-seed {int((star_bx >= 0.02).sum())}/9)")
    print(f"   Phi*(B) - Phi*(A) = {star_ba.mean():+.4f}  (every-seed {int((star_ba >= 0.02).sum())}/9)")
    json.dump(rows, open("pedestal_ensemble.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
