"""New observables that live OUTSIDE faithful_phi's estimator class.

faithful_phi (verified by reading the code, not the docstring):
    build_mi_matrix  -> same-time pairwise MI matrix, 8-bin plug-in, EVEN in rho (sign lost)
    faithful_phi_from_mi -> bipartition min-cut of that matrix / min(|A|,|B|)
=> Phi* = f(same-time pairwise MI matrix).  Time direction, 3rd-order synergy and the
   coupling MECHANISM are invisible BY CONSTRUCTION.

This module implements four DVs that are not functions of that statistic:
    D1 Omega_gauss  gaussian-copula O-information            (2nd order, but logdet + sign)
    D2 Omega_disc   discrete plug-in O-information           (CAN see 3rd-order synergy)
    D3 TE_tot       lag-1 gaussian transfer entropy, total   (lagged -> outside same-time class)
    D4 TE_asym      ring circulation asymmetry               (directed; true value 0 on a ring)

Every DV is pedestal-subtracted against K circular-shift surrogates (marginals byte-identical,
autocorrelation preserved, cross-module alignment destroyed => true value 0 by construction).
No max(controls) anywhere: contrasts are paired per seed.
"""

from __future__ import annotations

import numpy as np
from scipy.special import ndtri

LOG2 = np.log(2.0)
RING = [(0, 1), (1, 2), (2, 3), (3, 0)]
SURR_KEY = 0x0E1F_0000          # arm-independent -> common random numbers across arms


# ---------------------------------------------------------------- readouts
def normal_scores(traj: np.ndarray) -> np.ndarray:
    """Per-row rank -> (r+0.5)/T -> Phi^-1.  The gaussian-copula transform.

    Rank is invariant to any strictly monotone lens, and it is EQUIVARIANT to a circular time
    shift, which is what makes the surrogate cheap and exact.
    """
    n, t = traj.shape
    order = np.argsort(traj, axis=1, kind="stable")
    ranks = np.empty((n, t), dtype=np.float64)
    rows = np.arange(n)[:, None]
    ranks[rows, order] = np.arange(t, dtype=np.float64)[None, :]
    return ndtri((ranks + 0.5) / t)


def equal_freq_bins(traj: np.ndarray, n_bins: int) -> np.ndarray:
    """Per-row rank -> equal-frequency bin index. Marginals are exactly uniform by construction."""
    n, t = traj.shape
    order = np.argsort(traj, axis=1, kind="stable")
    ranks = np.empty((n, t), dtype=np.int64)
    rows = np.arange(n)[:, None]
    ranks[rows, order] = np.arange(t)[None, :]
    return np.minimum((ranks * n_bins) // t, n_bins - 1)


# ---------------------------------------------------------------- D1 gaussian-copula Omega
def omega_gauss(z: np.ndarray) -> float:
    """O-information of a gaussian copula, in bits.

        Omega = (n-2) H(X) + sum_j [ H(X_j) - H(X_-j) ]

    With H = 1/2 log((2 pi e)^d det Sigma), every (2 pi e) constant cancels identically
    ((n-2)n + n - n(n-1) = 0), so Omega is a pure log-determinant functional.
    Omega > 0 redundancy-dominated; Omega < 0 synergy-dominated.
    """
    n = z.shape[0]
    c = np.corrcoef(z)
    sign, ld = np.linalg.slogdet(c)
    if sign <= 0:
        return float("nan")
    tot = (n - 2) * ld
    for j in range(n):
        idx = [i for i in range(n) if i != j]
        s2, ld2 = np.linalg.slogdet(c[np.ix_(idx, idx)])
        tot += np.log(c[j, j]) - ld2
    return float(0.5 * tot / LOG2)


# ---------------------------------------------------------------- D2 discrete plug-in Omega
def _entropy_counts(codes: np.ndarray, n_states: int) -> float:
    cnt = np.bincount(codes, minlength=n_states).astype(np.float64)
    t = codes.shape[0]
    p = cnt[cnt > 0] / t
    return float(-np.sum(p * np.log(p)) / LOG2)


def omega_disc(b: np.ndarray, n_bins: int) -> float:
    """Plug-in O-information over discretised modules, in bits.

    This is the ONLY DV here that can carry 3rd-order synergy (an XOR triplet has every pairwise
    MI = 0 while its O-information is not 0).  The plug-in bias is arm-independent given the same
    (T, n, n_bins) and exactly-uniform marginals, and it is removed by the pedestal subtraction.
    """
    n = b.shape[0]
    pw = n_bins ** np.arange(n)
    full = (b * pw[:, None]).sum(axis=0)
    h_full = _entropy_counts(full, n_bins ** n)
    tot = (n - 2) * h_full
    for j in range(n):
        idx = [i for i in range(n) if i != j]
        h_j = _entropy_counts(b[j], n_bins)
        codes = (b[idx] * (n_bins ** np.arange(n - 1))[:, None]).sum(axis=0)
        h_rest = _entropy_counts(codes, n_bins ** (n - 1))
        tot += h_j - h_rest
    return float(tot)


# ---------------------------------------------------------------- D3/D4 transfer entropy
def te_pair(src: np.ndarray, dst: np.ndarray) -> float:
    """lag-1 gaussian TE(src -> dst) in bits: 1/2 log2( var(d_t|d_-1) / var(d_t|d_-1, s_-1) )."""
    y = dst[1:]
    x1 = np.column_stack([np.ones_like(y), dst[:-1]])
    x2 = np.column_stack([np.ones_like(y), dst[:-1], src[:-1]])
    r1 = y - x1 @ np.linalg.lstsq(x1, y, rcond=None)[0]
    r2 = y - x2 @ np.linalg.lstsq(x2, y, rcond=None)[0]
    v1, v2 = float(r1 @ r1), float(r2 @ r2)
    if v2 <= 0 or v1 <= 0:
        return 0.0
    return float(0.5 * np.log(v1 / v2) / LOG2)


def te_stats(z: np.ndarray) -> tuple[float, float]:
    """(TE_tot, TE_asym) over the 8 ordered ring-adjacent pairs."""
    fwd = sum(te_pair(z[a], z[b]) for a, b in RING)
    bwd = sum(te_pair(z[b], z[a]) for a, b in RING)
    return fwd + bwd, fwd - bwd


# ---------------------------------------------------------------- DV bundle + pedestals
DV_NAMES = ["omega_gauss", "omega_disc", "te_tot", "te_asym"]
N_BINS_DISC = 4


def dv_from_readouts(z: np.ndarray, b: np.ndarray) -> dict[str, float]:
    tt, ta = te_stats(z)
    return {"omega_gauss": omega_gauss(z), "omega_disc": omega_disc(b, N_BINS_DISC),
            "te_tot": tt, "te_asym": ta}


def dv_raw(traj: np.ndarray) -> dict[str, float]:
    return dv_from_readouts(normal_scores(traj), equal_freq_bins(traj, N_BINS_DISC))


def _shifts(seed: int, k: int, n: int, t: int) -> np.ndarray:
    """Per-(surrogate, module) circular lags in the middle half of the record (Philox)."""
    rng = np.random.Generator(np.random.Philox(key=SURR_KEY + seed))
    return rng.integers(t // 4, 3 * t // 4, size=(k, n))


def pedestal_circ(traj: np.ndarray, seed: int, k: int) -> list[dict[str, float]]:
    """K circular-shift surrogate DV draws.  True value of every DV is 0 by construction.

    rank (hence normal score and bin index) commutes with a circular shift, so the surrogate
    readouts are exact rolls of the arm's own readouts -- no re-ranking, no approximation.
    """
    z = normal_scores(traj)
    b = equal_freq_bins(traj, N_BINS_DISC)
    n, t = traj.shape
    lags = _shifts(seed, k, n, t)
    out = []
    for j in range(k):
        zs = np.stack([np.roll(z[i], int(lags[j, i])) for i in range(n)])
        bs = np.stack([np.roll(b[i], int(lags[j, i])) for i in range(n)])
        out.append(dv_from_readouts(zs, bs))
    return out


def pedestal_phase(traj: np.ndarray, seed: int, k: int) -> list[dict[str, float]]:
    """K phase-randomised surrogate DV draws (2nd pedestal): spectrum kept, coupling destroyed."""
    n, t = traj.shape
    rng = np.random.Generator(np.random.Philox(key=SURR_KEY ^ 0xBEEF + seed))
    f = np.fft.rfft(traj, axis=1)
    mag = np.abs(f)
    out = []
    for _ in range(k):
        ph = rng.uniform(0, 2 * np.pi, size=f.shape)
        ph[:, 0] = 0.0
        if t % 2 == 0:
            ph[:, -1] = 0.0
        sur = np.fft.irfft(mag * np.exp(1j * ph), n=t, axis=1)
        out.append(dv_raw(sur))
    return out


def dv_star(traj: np.ndarray, seed: int, k: int = 32) -> tuple[dict, dict, dict]:
    """(DV*, DV_raw, pedestal-null spread) -- DV* = raw - mean(K circular-shift pedestal draws)."""
    raw = dv_raw(traj)
    ped = pedestal_circ(traj, seed, k)
    star, null = {}, {}
    for nm in DV_NAMES:
        vals = np.array([p[nm] for p in ped])
        star[nm] = float(raw[nm] - vals.mean())
        null[nm] = vals - vals.mean()          # centred pedestal draws -> the MDE null
    return star, raw, null
