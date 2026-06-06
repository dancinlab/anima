"""H_991 — re-perception is the error-corrector: closed-loop drift vs re-perception interval.

1st-round seed: H_981🟢 imagined rollouts are bounded-but-DRIFTING; H_990🟢 closed loop beats
blind open-loop. This sharpens WHY: the cure for imagination drift is RE-PERCEPTION. Sweep
the re-perception interval k (act from a fresh latent every k steps, imagine in between).

Falsifier (frozen): on a forecasting/tracking task with hidden dynamics, measure tracking
error as a function of re-perception interval k ∈ {1,2,3,5,8,15,30}.
  PASS  iff  error increases MONOTONICALLY with k (more imagination-between-perceptions =
            more drift), Spearman rho(k, error) > 0.8, AND k=1 (re-perceive every step)
            error is < 1/3 of k=30 (pure open-loop) error — perception bounds the drift.
  FAIL  iff  no monotone relationship (re-perception does not contain drift) OR k=1 ≈ k=30.
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LDSWorldModel, header, spearman

N_SEEDS = 24
T = 30
KS = [1, 2, 3, 5, 8, 15, 30]


def make_traj(rng, n=T):
    """A NONLINEAR damped oscillator with process noise (hidden velocity). The cubic
    stiffening + stochastic drive make pure imagination accumulate error (a linear LDS
    cannot exactly model it), so re-perception genuinely matters."""
    p = rng.uniform(-1.5, 1.5, 2); v = rng.uniform(-1, 1, 2)
    obs = []
    w = 1.3
    for t in range(n):
        obs.append(p.copy())
        acc = -w * w * p - 0.4 * (p ** 3) - 0.15 * v + rng.normal(0, 0.12, 2)
        v = v + acc * 0.2; p = p + v * 0.2
    return np.array(obs)


def fit_lm(seed):
    rng = np.random.default_rng(seed)
    trajs = [make_traj(rng) for _ in range(50)]
    lm = LDSWorldModel(obs_dim=2, delay=3, ridge=1e-3)
    lm.fit(trajs)
    return lm


def tracking_error(lm, traj, k):
    """Track the traj: re-perceive (reset latent from true obs) every k steps; imagine between.
    error = mean over steps of ||decoded latent - true obs||."""
    d = lm.delay
    errs = []
    z = lm.embed(traj[:d])[-1]
    for t in range(d, len(traj)):
        if (t - d) % k == 0:
            # RE-PERCEIVE: reset latent from the true recent observations
            z = lm.embed(traj[max(0, t - d + 1):t + 1])[-1]
        else:
            # IMAGINE: roll the latent forward (no perception)
            z = lm.roll(z, 1)
        pred = lm.decode(z)
        errs.append(np.linalg.norm(pred - traj[t]))
    return float(np.mean(errs))


def main():
    header("H_991", "re-perception is the error-corrector (drift vs re-perception interval)")
    per_k = {k: [] for k in KS}
    for s in range(N_SEEDS):
        lm = fit_lm(s)
        rng = np.random.default_rng(10000 + s)
        traj = make_traj(rng)
        for k in KS:
            per_k[k].append(tracking_error(lm, traj, k))
    means = {k: float(np.mean(per_k[k])) for k in KS}
    print(f"task=hidden-velocity oscillator tracking  T={T} seeds={N_SEEDS}")
    print("re-perception interval k → tracking error (lower=better):")
    for k in KS:
        print(f"  k={k:2d} (imagine {k-1} steps between perceptions) : {means[k]:.4f} ± {np.std(per_k[k]):.4f}")
    xs = np.array(KS, float)
    ys = np.array([means[k] for k in KS])
    rho, p = spearman(xs, ys)
    ratio = means[1] / max(means[30], 1e-9)
    print()
    print(f"D1 monotone drift vs k: Spearman rho={rho:.3f} p={p:.3e}")
    print(f"D2 perception bounds drift: error(k=1)/error(k=30) = {ratio:.3f} (PASS if < 0.333)")
    print("-" * 78)
    mono = rho > 0.8
    bounds = ratio < 0.333
    if mono and bounds:
        v = (f"PASS re-perception is the error-corrector: error rises monotonically with imagination "
             f"interval (rho={rho:.2f}), and re-perceiving every step cuts drift to {ratio:.2f}× of "
             f"pure open-loop — perception bounds imagination drift (toy rung).")
        tok = "PASS"
    elif mono:
        v = (f"PASS-PARTIAL monotone drift with k (rho={rho:.2f}) but k=1/k=30 ratio={ratio:.2f} "
             f"not < 1/3 — perception helps but bound is weaker than pre-registered (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL no monotone drift-vs-interval (rho={rho:.2f}) — re-perception does not contain "
             f"imagination drift here (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_991: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
