#!/usr/bin/env python3
"""alpha_v2 — A2 binned ΔΦ-rate vs n_cells α metric (V2) with Candidate-E gate wrapper.

Design SSOT: docs/anima_clm_v5_alpha_metric_v2_design_2026_05_10.md (§3, §7).

`compute_alpha_v2(snapshots, ...)` returns dict with keys:
  - alpha:    OLS slope (or None when UNRELIABLE)
  - CI95:     bootstrap 95% CI tuple (lo, hi) (or None)
  - bins:     {bin_mid: mean_rate} dict (kept positives only)
  - n_bins:   number of bins that survived all gates
  - x_range:  log-x range across surviving bins
  - verdict:  "OK" | "UNRELIABLE_INSUFFICIENT_BINS(n)" | "UNRELIABLE_X_RANGE"

Default bin edges {2,4,8,16,32,64,128} target the toy max_cells=64 substrate +
historical Cells 2-64 sweep (CLM v2 stage 8).  All cost is local CPU, $0.

Honest C3:
- Bin midpoint = geometric mean of [lo, hi); biased toward lower for asym bins.
- Single-pair bin can pass only if n_cells_pre is unique to that bin (toy 8→41
  jump leaves [16,32) empty by construction).
- Post-cap bin [64,128) tends to noise-dominated mean; eps=1e-6 filter cuts most
  but a few may slip through under accumulated Lorenz drift on long trajectories.
"""

from __future__ import annotations

import math
import random
from typing import Iterable, Sequence


def compute_alpha_v2(
    snapshots: Sequence[dict],
    phi_field: str = "phi",
    n_cells_field: str = "n_cells",
    bin_edges: Iterable[int] = (2, 4, 8, 16, 32, 64, 128),
    min_bins: int = 3,
    min_x_range: float = 0.5,
    min_rate: float = 1e-6,
    n_bootstrap: int = 200,
    seed: int = 42,
) -> dict:
    """A2 binned ΔΦ-rate vs n_cells regression with E-wrapper gate.

    Args:
        snapshots: ordered list of {turn, n_cells, phi, ...}.
        phi_field: key for Φ value (e.g. "phi", "proxy_phi", "iit_phi_unnorm_b16").
        n_cells_field: key for cell count.
        bin_edges: monotone increasing ints, half-open intervals [edge_i, edge_{i+1}).
        min_bins: gate — require ≥this many surviving bins.
        min_x_range: gate — log-x range across surviving bins must reach this.
        min_rate: floor — bins with mean_rate ≤ this are dropped (cannot log).
        n_bootstrap: bootstrap iters for CI95.
        seed: bootstrap RNG seed for reproducibility.

    Returns:
        dict (see module docstring).
    """
    bin_edges = list(bin_edges)

    # Step 1 — per-pair rate r_i = ΔΦ/Δturn, keyed by n_cells_pre.
    pairs: list[tuple[int, float]] = []
    for s1, s2 in zip(snapshots[:-1], snapshots[1:]):
        dt = s2["turn"] - s1["turn"]
        if dt <= 0:
            continue
        if phi_field not in s1 or phi_field not in s2:
            continue
        rate = (s2[phi_field] - s1[phi_field]) / dt
        n_pre = s1[n_cells_field]
        pairs.append((n_pre, rate))

    # Step 2 — bin by n_cells_pre, mean rate, drop non-positive bins.
    bins: dict[float, float] = {}
    bin_pair_counts: dict[float, int] = {}
    for i in range(len(bin_edges) - 1):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        in_bin = [r for n, r in pairs if lo <= n < hi]
        if not in_bin:
            continue
        mean_rate = sum(in_bin) / len(in_bin)
        if mean_rate <= min_rate:
            continue
        mid = math.sqrt(lo * hi)  # geometric midpoint
        bins[mid] = mean_rate
        bin_pair_counts[mid] = len(in_bin)

    valid_bins = sorted(bins.items())
    n_valid = len(valid_bins)

    # Step 3 — gate: min_bins.
    if n_valid < min_bins:
        return {
            "alpha": None,
            "CI95": None,
            "bins": bins,
            "bin_pair_counts": bin_pair_counts,
            "n_bins": n_valid,
            "x_range": None,
            "verdict": f"UNRELIABLE_INSUFFICIENT_BINS({n_valid})",
        }

    xs = [math.log(m) for m, _ in valid_bins]
    ys = [math.log(r) for _, r in valid_bins]
    x_range = max(xs) - min(xs)

    # Step 4 — gate: min_x_range.
    if x_range < min_x_range:
        return {
            "alpha": None,
            "CI95": None,
            "bins": bins,
            "bin_pair_counts": bin_pair_counts,
            "n_bins": n_valid,
            "x_range": x_range,
            "verdict": "UNRELIABLE_X_RANGE",
        }

    def _ols(xs_: list[float], ys_: list[float]) -> float | None:
        n = len(xs_)
        mx = sum(xs_) / n
        my = sum(ys_) / n
        num = sum((xs_[i] - mx) * (ys_[i] - my) for i in range(n))
        den = sum((xs_[i] - mx) ** 2 for i in range(n))
        if den <= 0:
            return None
        return num / den

    alpha = _ols(xs, ys)

    # Step 5 — bootstrap CI95.
    rng = random.Random(seed)
    boot: list[float] = []
    n = len(valid_bins)
    for _ in range(n_bootstrap):
        sampled = [rng.choice(valid_bins) for _ in range(n)]
        bxs = [math.log(m) for m, _ in sampled]
        bys = [math.log(r) for _, r in sampled]
        a = _ols(bxs, bys)
        if a is not None:
            boot.append(a)
    boot.sort()
    ci_low = boot[int(0.025 * len(boot))] if boot else None
    ci_high = boot[int(0.975 * len(boot))] if boot else None

    return {
        "alpha": alpha,
        "CI95": (ci_low, ci_high),
        "bins": bins,
        "bin_pair_counts": bin_pair_counts,
        "n_bins": n_valid,
        "x_range": x_range,
        "verdict": "OK",
    }


def alpha_v1_ols(snapshots: Sequence[dict], phi_field: str = "phi",
                 n_cells_field: str = "n_cells") -> float | None:
    """V1: OLS slope of log(Φ) vs log(n_cells) over every snapshot.

    Replicates the historical α_exponent emitted by run.py prior to V2.
    """
    xs, ys = [], []
    for s in snapshots:
        n = s.get(n_cells_field, 0)
        p = s.get(phi_field, 0.0)
        if n is None or n <= 0 or p is None or p <= 0:
            continue
        xs.append(math.log(n))
        ys.append(math.log(p))
    if len(xs) < 2:
        return None
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den <= 0:
        return None
    return num / den
