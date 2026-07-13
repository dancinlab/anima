"""The pedestal receipt — what does the frozen T=64 estimator report for ZERO integration?

P0' showed the population Phi of every content arm is ~0.0016 bits, while the frozen T=64
read-out reports ~1.8-2.2 and arm-to-arm gaps of +-0.1..0.5. Two readings cannot both be the
system's integration. This script settles which is the estimator and which is the substrate:

  * PEDESTAL — an arm whose TRUE cross-module information is exactly zero by construction
    (each module's time series independently permuted => marginals byte-identical, joint
    destroyed). Its Phi must be 0. Whatever the estimator reports instead IS the bias.
  * SWEEP — Phi(T) for A, B and PEDESTAL as T grows 64 -> 65536.

If Phi_T64(PEDESTAL) lands next to Phi_T64(A) and Phi_T64(B), then at T=64 the estimator is
reporting its own plugin bias, the arms are indistinguishable from a zero-integration system,
and every content-axis tier ever cemented at T=64 — R6's green and the wall alike — was noise
on top of that pedestal. Nothing is tuned here: same substrate, same hypers, same estimator.
"""

from __future__ import annotations

import json

import numpy as np

from faithful_phi import faithful_phi
from p0_feasibility import gen_traj_long
from substrate import A_DIRECT, B_MULTI, NBINS, N_MOD, X_SHARED, Lcg, rank_uniform

T_GRID = [64, 256, 1024, 4096, 16384, 65536]
SEED = 3
PERM_STREAM = 0x5EED_0000  # dedicated LCG stream — arm-independent, never touches a trajectory


def pedestal_permute(traj: np.ndarray) -> np.ndarray:
    """Per-module independent time permutation: marginals exact, cross-module joint destroyed.

    Module 0 is held at identity (MI is invariant to a common relabelling of t, so permuting
    modules 1..n-1 already gives an independent joint). Fisher-Yates from the engine LCG.
    """
    out = traj.copy()
    t = traj.shape[1]
    rng = Lcg(PERM_STREAM)
    for i in range(1, traj.shape[0]):
        idx = np.arange(t)
        for k in range(t - 1, 0, -1):
            j = int(abs(rng.gauss()) * 1e6) % (k + 1)
            idx[k], idx[j] = idx[j], idx[k]
        out[i] = traj[i][idx]
    return out


def phi_at(mode: int, t: int, pedestal: bool) -> float:
    traj = gen_traj_long(SEED, mode, t, signed=False)
    if pedestal:
        traj = pedestal_permute(traj)
    return faithful_phi(rank_uniform(traj).reshape(-1), N_MOD, t, NBINS)


def main() -> int:
    rows = []
    print("Phi vs T — same substrate, same hypers, same faithful IIT-4 estimator, RU read-out")
    print(f"{'T':>7} | {'A':>9} {'B':>9} {'X':>9} | {'PEDESTAL':>9}  (true Phi = 0 by construction)")
    print("-" * 66)
    for t in T_GRID:
        a = phi_at(A_DIRECT, t, False)
        b = phi_at(B_MULTI, t, False)
        x = phi_at(X_SHARED, t, False)
        p = phi_at(B_MULTI, t, True)
        rows.append({"T": t, "A": a, "B": b, "X": x, "pedestal": p, "B_minus_X": b - x})
        print(f"{t:7d} | {a:9.6f} {b:9.6f} {x:9.6f} | {p:9.6f}")

    t64 = rows[0]
    tinf = rows[-1]
    print()
    print(f"at the FROZEN T=64:  pedestal (zero integration) reads Phi = {t64['pedestal']:.4f}, "
          f"vs B = {t64['B']:.4f}")
    print(f"   => the arms sit {abs(t64['B'] - t64['pedestal']):.4f} from a system with NO "
          f"integration at all, while the frozen bar is 0.02")
    print(f"   => B - X at T=64 is {t64['B_minus_X']:+.4f}, at T=65536 it is "
          f"{tinf['B_minus_X']:+.6f} ({abs(t64['B_minus_X'] / tinf['B_minus_X']):.0f}x inflated)")
    json.dump(rows, open("bias_pedestal.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
