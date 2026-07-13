"""STEP-1 — CERTIFY THE INSTRUMENT. No arm contrast is computed here, and no bar is used.

This runs BEFORE any bar is chosen, on purpose: the bar for H_9293 has to be denominated in bits
of shared information, and the only honest source for that number is what the instrument can
actually resolve. Everything below is either a known-answer control or a pure resolution
measurement — nothing here can be made to "pass".

Three questions, in order. A failure at any one stops the campaign.

  Z (ZERO)      Phi*(S(0)) ~ 0 ?          S(0) = arm A's marginals with an INDEPENDENT copula, so
                                          its true Phi is 0 by construction. If the instrument
                                          cannot read a known zero as zero, nothing else it says
                                          counts. (A degenerate read-out that destroys all
                                          structure passes a null test but FAILS D below — that
                                          pair is what H_9260 was missing.)
  D (DETECT)    Phi*(S(lam)) tracks -log2(1-lam^2) ?   known non-zero answers, 4 points.
  R (RESOLVE)   SE of Phi* over the 9 frozen seeds  =>  the instrument's MDE in BITS, per T.

The MDE is the deliverable: it says which effect sizes this substrate+estimator can even see, and
therefore what a bar is allowed to be. The signed lens is carried alongside the frozen energy lens
because H_9292 measured that the energy read-out squares the cross-module correlation and lands
its whole signal (~0.0016 bits) at the pedestal's own scale — that is a fact about the read-out,
established before this script ran, not a preference discovered inside it.
"""

from __future__ import annotations

import json

import numpy as np

from instrument import null_draws, phi_star, spike_in, spike_truth
from p0_feasibility import gen_traj_long
from substrate import A_DIRECT

SEEDS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
T_GRID = [4096, 16384, 65536]
LAMBDAS = [0.0, 0.15, 0.30, 0.50]
K = 16                     # null draws per Phi*


def main() -> int:
    out = {"T_grid": T_GRID, "lambdas": LAMBDAS, "K": K, "seeds": SEEDS, "cert": {}}

    for lens, signed in (("energy", False), ("signed", True)):
        print(f"══ lens = {lens}   (traj = {'s_i(t)[0]' if signed else '||s_i(t)||^2'})")
        out["cert"][lens] = {}
        for t in T_GRID:
            # --- Z + D : the SPIKE-IN calibration curve (known answers) ---
            cal = []
            for lam in LAMBDAS:
                vals = []
                for s in SEEDS:
                    a = gen_traj_long(s, A_DIRECT, t, signed)
                    star, _, _ = phi_star(spike_in(a, lam), K)
                    vals.append(star)
                v = np.array(vals)
                cal.append({"lambda": lam, "truth": spike_truth(lam),
                            "phi_star_mean": float(v.mean()),
                            "phi_star_se": float(v.std(ddof=1) / np.sqrt(len(v)))})

            # --- R : the instrument's own noise on a REAL arm (arm A, the plainest one) ---
            arm_vals, ped_means = [], []
            for s in SEEDS:
                a = gen_traj_long(s, A_DIRECT, t, signed)
                star, mu, _ = phi_star(a, K)
                arm_vals.append(star)
                ped_means.append(mu)
            av = np.array(arm_vals)
            se = float(av.std(ddof=1) / np.sqrt(len(av)))
            mde = 3.0 * se                     # 3-sigma detection floor, in BITS
            lam_mde = float(np.sqrt(1.0 - 2.0 ** (-mde)))   # invert -log2(1-lam^2)

            out["cert"][lens][str(t)] = {
                "calibration": cal, "pedestal_mean": float(np.mean(ped_means)),
                "armA_phi_star_mean": float(av.mean()), "armA_phi_star_se": se,
                "MDE_bits_3se": mde, "MDE_as_lambda": lam_mde,
            }

            z = cal[0]
            print(f"  T={t:6d} | pedestal E[Phi_null]={np.mean(ped_means):.6f}")
            print(f"          | Z  Phi*(S(0)) = {z['phi_star_mean']:+.6f} ± {z['phi_star_se']:.6f}"
                  f"   (truth 0)")
            for c in cal[1:]:
                print(f"          | D  Phi*(S({c['lambda']:.2f})) = {c['phi_star_mean']:+.6f} "
                      f"± {c['phi_star_se']:.6f}   truth {c['truth']:.4f}   "
                      f"ratio {c['phi_star_mean']/c['truth']:.2f}")
            print(f"          | R  arm A: Phi* = {av.mean():+.6f} · SE(9 seeds) = {se:.6f}"
                  f"  =>  MDE(3SE) = {mde:.6f} bits  (= shared corr lambda >= {lam_mde:.3f})")
        print()

    json.dump(out, open("step1_certify.json", "w"), indent=2)
    print("→ step1_certify.json  (the MDE is what the H_9293 bar must be denominated in)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
