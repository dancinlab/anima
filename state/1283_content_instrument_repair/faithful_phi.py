"""faithful IIT-4 Phi (small-N exact MIP-EI) — byte-faithful Python port.

Reference (open source, `reference-match`): hexa-lang
`stdlib/consciousness/iit4/faithful_phi.hexa` (411 lines). This module is a 1:1
port of that file's exact path, kept numerically identical so a py-channel probe
may cement a tier under `a_phi_iit4_tool` (the mandated estimator, not a proxy).

Parity is not asserted by argument — it is measured against the hexa run of the
H_9260 probe (10 arms x 9 seeds, both readouts) by `parity_check.py`.

Ported quirks that are SPEC, not bugs (do not "fix" — they change Phi):
  * `_bin_values` all-identical guard uses the Rust f32::EPSILON literal
    (1.19209290e-7) even though the pipeline is f64 throughout.
  * `_entropy` divides by `total + 1e-8` and takes `log2(p + 1e-10)`.
  * The MIP enumeration starts at mask=1, so the bipartition {0} | {1..n-1}
    is NEVER evaluated (mask=0 is skipped). Every other bipartition is.
"""

from __future__ import annotations

import math

import numpy as np

F32_EPS = 1.19209290e-7
LOG2 = math.log(2.0)


def bin_values(values: np.ndarray, n_bins: int) -> np.ndarray:
    """Min-max bin a 1-D f64 array into [0, n_bins-1]. Mirrors `_iit4_bin_values`."""
    n = values.shape[0]
    if n <= 0 or n_bins <= 0:
        return np.zeros(max(n, 0), dtype=np.int64)
    mn = float(values.min())
    mx = float(values.max())
    rng = mx - mn
    if rng < F32_EPS:
        return np.zeros(n, dtype=np.int64)
    bw = rng / n_bins
    b = np.floor((values - mn) / bw).astype(np.int64)
    np.clip(b, 0, n_bins - 1, out=b)
    return b


def _entropy(counts: np.ndarray, total: int) -> float:
    """Shannon entropy over ALL k bins. Mirrors `_iit4_entropy` (incl. the epsilons)."""
    if total == 0:
        return 0.0
    t = total + 1.0e-8
    p = counts / t
    return float(np.sum(-p * (np.log(p + 1.0e-10) / LOG2)))


def mi_pair(a: np.ndarray, b: np.ndarray, n_bins: int) -> float:
    """MI(A;B) = max(H(A) + H(B) - H(A,B), 0). Mirrors `_iit4_mi_pair`."""
    n = a.shape[0]
    if n <= 0 or n_bins <= 0:
        return 0.0
    ba = bin_values(a, n_bins)
    bb = bin_values(b, n_bins)
    ca = np.bincount(ba, minlength=n_bins).astype(np.float64)
    cb = np.bincount(bb, minlength=n_bins).astype(np.float64)
    jo = np.bincount(ba * n_bins + bb, minlength=n_bins * n_bins).astype(np.float64)
    mi = _entropy(ca, n) + _entropy(cb, n) - _entropy(jo, n)
    return 0.0 if mi < 0.0 else mi


def build_mi_matrix(state: np.ndarray, n: int, dim: int, n_bins: int) -> np.ndarray:
    """Pairwise MI matrix over the dim-step trajectories. Mirrors `iit4_build_mi_matrix`."""
    s = state.reshape(n, dim)
    mi = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(i + 1, n):
            v = mi_pair(s[i], s[j], n_bins)
            mi[i, j] = v
            mi[j, i] = v
    return mi


def faithful_phi_from_mi(mi: np.ndarray, n: int) -> float:
    """Exact MIP-EI over an n x n MI matrix. Mirrors `iit4_faithful_phi_from_mi`.

    Enumerates masks 1 .. 2^(n-1)-1 (cell 0 pinned to side A; bit b set => cell
    b+1 in A), skipping any mask that leaves side B empty. mask=0 — the
    {0} | {1..n-1} cut — is outside the loop in the reference and stays so here.
    """
    if n <= 1:
        return 0.0
    if n == 2:
        return float(mi[0, 1])

    max_mask = 1 << (n - 1)
    best_cut = 1.0e308
    best_norm = 1.0
    found = False
    for mask in range(1, max_mask):
        in_a = np.zeros(n, dtype=bool)
        in_a[0] = True
        for b in range(n - 1):
            if (mask >> b) & 1:
                in_a[b + 1] = True
        sa = int(in_a.sum())
        sb = n - sa
        if sb < 1:
            continue
        cut = float(mi[np.ix_(in_a, ~in_a)].sum())
        if (not found) or (cut < best_cut):
            best_cut = cut
            best_norm = float(min(sa, sb))
            found = True
    if best_norm < 1.0:
        best_norm = 1.0
    phi = best_cut / best_norm
    return 0.0 if phi < 0.0 else phi


def faithful_phi(state: np.ndarray, n: int, dim: int, n_bins: int) -> float:
    """faithful Phi* over a flat row-major n x dim state. Mirrors `iit4_faithful_phi`."""
    if n <= 1 or dim <= 0 or n_bins <= 0:
        return 0.0
    if n > 8:
        raise ValueError("faithful_phi: n > 8 not supported (exact MIP-EI is n<=8)")
    return faithful_phi_from_mi(build_mi_matrix(state, n, dim, n_bins), n)
