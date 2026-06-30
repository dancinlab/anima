"""H_981 — Imagination self-consistency (stochastic rollouts stay grounded, not hallucinate).

FROZEN FALSIFIER (honored):
  fix a latent state; launch K stochastic rollouts (entropy/seed varied). Measure pairwise
  divergence of the rollout latents at each horizon step. N start-states x seeds.
  D1 = cross-rollout divergence curve (mean pairwise latent distance vs horizon h).
  D2 = drift-knee: horizon at which divergence reaches a fraction f of the unconditioned-
       latent baseline distance.
  D3 = the unconditioned (no-start-state) latent spread bounds maximal hallucination.
  PASS: divergence curve bounded/sub-linear AND drift-knee horizon > h_threshold (rollouts
        stay well below unconditioned spread up to a meaningful horizon).
  FAIL: divergence reaches the unconditioned spread at low horizon (immediate hallucination).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, header, verdict_line

ODIM = 2
T = 30
N_TRAIN = 300
K_ROLLOUTS = 12
N_START = 60
HMAX = 20
ENTROPY = 0.05        # stochastic rollout noise (qentropy-style seed-point entropy,
                      # matched to the world's intrinsic dynamics noise scale ~0.02-0.05;
                      # NOT a large perturbation -- imagination samples near the dynamics)
F_KNEE = 0.5
H_THRESHOLD = 5


def make_traj(rng):
    theta = 0.4
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    pos = rng.standard_normal(2); v = rng.standard_normal(2) * 0.5
    out = [pos.copy()]
    for _ in range(T - 1):
        v = R @ v; pos = pos + 0.3 * v + 0.02 * rng.standard_normal(2); out.append(pos.copy())
    return np.array(out)


def stochastic_roll(m, z0, h, rng, entropy):
    z = z0.copy()
    for _ in range(h):
        z = m.roll(z, 1) + entropy * rng.standard_normal(len(z))
    return z


def main():
    header("H_981", "Imagination self-consistency (grounded rollouts, not hallucination)")
    print(f"K={K_ROLLOUTS} stochastic rollouts/state, entropy={ENTROPY}, Hmax={HMAX}, N_start={N_START}\n")
    rng = np.random.default_rng(0)
    trs = [make_traj(rng) for _ in range(N_TRAIN)]
    m = LDSWorldModel(ODIM, delay=3).fit(trs)

    # unconditioned spread (D3): pairwise distance of latents from random start states
    rng_u = np.random.default_rng(5)
    uncond = np.array([m.embed(make_traj(rng_u))[10] for _ in range(200)])
    uncond_spread = np.mean([np.linalg.norm(uncond[i] - uncond[j])
                             for i in range(0, 200, 2) for j in range(1, 200, 2)])
    print(f"D3 unconditioned latent spread (max-hallucination bound) = {uncond_spread:.4f}\n")

    div_curve = np.zeros(HMAX)
    for s in range(N_START):
        rng_s = np.random.default_rng(1000 + s)
        z0 = m.embed(make_traj(rng_s))[5]
        for h in range(1, HMAX + 1):
            rolls = np.array([stochastic_roll(m, z0, h, np.random.default_rng(s * 100 + k), ENTROPY)
                              for k in range(K_ROLLOUTS)])
            d = np.mean([np.linalg.norm(rolls[i] - rolls[j])
                         for i in range(K_ROLLOUTS) for j in range(i + 1, K_ROLLOUTS)])
            div_curve[h - 1] += d
    div_curve /= N_START

    print("D1 cross-rollout divergence vs horizon:")
    for h in [1, 2, 4, 8, 12, 16, 20]:
        print(f"  h={h:2d}: divergence={div_curve[h-1]:.4f}  ({div_curve[h-1]/uncond_spread*100:.1f}% of uncond)")

    # D2 drift-knee = first h where divergence >= F_KNEE * uncond_spread
    knee = next((h for h in range(1, HMAX + 1) if div_curve[h - 1] >= F_KNEE * uncond_spread), HMAX + 1)
    print(f"\nD2 drift-knee ({int(F_KNEE*100)}% of uncond) at h={knee} (threshold > {H_THRESHOLD})")
    # sub-linear check: divergence growth decelerates
    diffs = np.diff(div_curve)
    sublinear = np.mean(diffs[HMAX//2:]) <= np.mean(diffs[:HMAX//2]) + 1e-9
    print(f"D1 sub-linear (growth decelerates): {sublinear}")

    if knee > H_THRESHOLD and sublinear:
        verdict_line("H_981", "PASS",
                     f"divergence bounded/sub-linear, drift-knee h={knee}>{H_THRESHOLD} "
                     f"(rollouts stay <{int(F_KNEE*100)}% of unconditioned spread to h={knee}) — "
                     f"imagination self-consistency (toy).")
    elif knee <= 2:
        verdict_line("H_981", "FAIL",
                     f"divergence reaches unconditioned spread at low horizon (knee h={knee}) — "
                     f"immediate hallucination, not grounded (closed-negative).")
    else:
        verdict_line("H_981", "INCOMPLETE", f"knee h={knee} sublinear={sublinear} marginal; toy C3.")


if __name__ == "__main__":
    main()
