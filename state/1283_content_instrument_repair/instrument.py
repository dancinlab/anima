"""The repaired instrument — Phi* (pedestal-subtracted) + the SPIKE-IN arm with a KNOWN answer.

H_9292 established that a raw Phi is unreadable on this axis: after rank-uniformisation the plugin
bias depends only on (T, n_bins), not on the arm, so every arm carries the same pedestal and the
raw value is ~all pedestal. The repair is not a new read-out — it is to stop reading a raw value:

    Phi*(arm) = Phi(RU(traj)) - E[ Phi(RU(pi_k(traj))) ]      k = 1..K

pi_k = per-module independent time permutation (marginals byte-identical, cross-module joint
destroyed => true Phi of the null is 0 by construction). The subtraction is what "signal = a
collapse-Delta against controls, never a raw value" means for this estimator.

SPIKE-IN — the only arm in this file whose answer is known before it is measured. Build a
trajectory with the SAME marginals as arm A but a gaussian copula of correlation lambda:

    g[t] ~ N(0,1)                       common latent factor  (arm-independent LCG stream)
    e_i[t] ~ N(0,1)                     independent per module
    y_i[t] = sqrt(lambda)*g + sqrt(1-lambda)*e_i          => Corr(y_i, y_j) = lambda exactly
    traj_S[i,t] = sort(traj_A[i,:])[ rank of y_i[t] ]     => marginal of A, copula of y

All 6 pairs then share one MI c = -0.5*log2(1 - lambda^2), so the exact MIP over the estimator's
own enumeration (masks 1..6; the {0}|{1,2,3} cut is outside the reference loop) is the 2|2 cut at
4c/2, giving the closed form

    Phi_pop(S(lambda)) = -log2(1 - lambda^2)          0.15 -> 0.0328 · 0.30 -> 0.1361 · 0.50 -> 0.4150

That closed form is what turns the instrument's own resolution into a number in BITS — which is
what a bar has to be denominated in, instead of being inherited from another axis.

SURROGATE RNG — deliberately NOT the engine LCG (Fable design §1.3, adopted):
the engine's `x -> (1103515245x + 12345) mod 2^31` is full-period, so it has exactly ONE cycle.
Different hash-derived seeds are therefore different OFFSETS ON THE SAME CYCLE, not independent
streams — K surrogates or R realisations drawn that way can silently share random numbers, and
then a block-mean's SE does not shrink like 1/sqrt(K) even though the arithmetic says it does.
Surrogates use counter-based Philox (genuinely independent, still fully deterministic). The
SUBSTRATE keeps the engine LCG untouched — that is where byte-parity with hexa must hold, and it
does (PARITY.txt). Nothing about the substrate moves here.
"""

from __future__ import annotations

import numpy as np

from faithful_phi import faithful_phi
from substrate import NBINS, N_MOD, rank_uniform

NULL_KEY = 0x5EED_0000   # pi_k draws  — arm-independent (common random numbers => paired contrast)
SPIKE_KEY = 0x5A17_0000  # spike-in g/e draws — arm-independent


def _rng(key: int) -> np.random.Generator:
    return np.random.Generator(np.random.Philox(key=key))


def null_draws(traj: np.ndarray, k: int, key: int = NULL_KEY) -> np.ndarray:
    """K draws of Phi under 'same marginals, zero cross-module information'.

    Per-module independent time permutation; module 0 held at identity (MI is invariant to a
    common relabelling of t, so permuting modules 1..n-1 already gives an independent joint).
    """
    rng = _rng(key)
    t = traj.shape[1]
    out = np.empty(k, dtype=np.float64)
    for d in range(k):
        nul = traj.copy()
        for i in range(1, traj.shape[0]):
            nul[i] = traj[i][rng.permutation(t)]
        out[d] = faithful_phi(rank_uniform(nul).reshape(-1), N_MOD, t, NBINS)
    return out


def phi_star(traj: np.ndarray, k: int) -> tuple[float, float, float]:
    """(Phi*, E[Phi_null], sd(Phi_null)) — the pedestal-subtracted quantity and its null spread."""
    t = traj.shape[1]
    obs = faithful_phi(rank_uniform(traj).reshape(-1), N_MOD, t, NBINS)
    nul = null_draws(traj, k)
    return obs - float(nul.mean()), float(nul.mean()), float(nul.std(ddof=1))


def spike_in(traj_a: np.ndarray, lam: float, key: int = SPIKE_KEY) -> np.ndarray:
    """Arm A's marginals + a gaussian copula of correlation `lam`. True Phi = -log2(1-lam^2)."""
    n, t = traj_a.shape
    rng = _rng(key)
    g = rng.standard_normal(t)
    out = np.empty_like(traj_a)
    for i in range(n):
        y = np.sqrt(lam) * g + np.sqrt(1.0 - lam) * rng.standard_normal(t)
        rk = np.empty(t, dtype=np.int64)
        rk[np.argsort(y, kind="stable")] = np.arange(t)
        out[i] = np.sort(traj_a[i])[rk]
    return out


def spike_truth(lam: float) -> float:
    """Closed-form population Phi of the SPIKE-IN arm (independently re-derived, see module docstring)."""
    return float(-np.log2(1.0 - lam * lam))
