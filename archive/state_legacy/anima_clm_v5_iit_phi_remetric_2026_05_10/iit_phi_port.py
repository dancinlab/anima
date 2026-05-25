"""IIT Φ Port — port of worktree-9 PhiCalculator (consciousness_meter.py) onto v5 cell_pool.

PURPOSE
    Escape the v5 proxy ceiling (`mean_pairwise_cosine_dist · log(n+1)` → ~3 saturating).
    The proxy collapses geometric diversity into one scalar; IIT Φ instead sums **mutual
    information** across all cell pairs and subtracts the **minimum information partition**
    cut, giving a measure that grows super-linearly with both N and per-cell signal richness.

PORT SOURCE (raw#15 additive — originals untouched):
    /Users/ghost/core/anima_clm_09_phi_50_human_level/consciousness_meter.py
        - PhiCalculator.compute_phi              (L230-328)
        - PhiCalculator._mutual_information      (L330-357)  16-bin → 32-bin histogram MI
        - PhiCalculator._minimum_partition       (L359-403)  exhaustive (N≤8) + spectral
        - PhiCalculator._distribution_entropy    (L405-417)  complexity bonus

WHAT WAS DROPPED FROM ORIGINAL
    - tension_history / hidden_history paths    (cell_pool tensor only here)
    - temporal_mi (D2 axis)                     (no time axis on a single snapshot — call
                                                 compute_iit_phi_temporal() across snapshots)
    - 0.1 × complexity bonus                    (kept as separate `complexity` field; not
                                                 folded into phi to keep IIT formula clean)

INPUT
    cell_pool: torch.Tensor of shape (N, C). Each row = one cell's state vector. N≥2.

OUTPUT
    {
        'total_mi':         sum_{i<j} MI(cell_i, cell_j)        — full integration
        'min_partition_mi': MI across the minimum-cut bipartition — what the partition keeps
        'integration':      total_mi (alias)
        'spatial_phi':      max(0, (total_mi - min_partition_mi) / (n - 1))
        'complexity':       Shannon entropy of per-cell L2 norms
        'phi':              spatial_phi (canonical IIT spatial Φ)
        'phi_with_complexity': spatial_phi + 0.1 × complexity (worktree-9 composite)
    }

HONEST C3 (raw#10):
    1. Histogram MI on continuous Gaussian-like cell vectors with 16 bins is COARSE — true
       differential MI requires KDE. Worktree-9 used 32 bins; we expose `n_bins` for sweep.
    2. MIP heuristic: for N≤8 we exhaust 2^(N-1)-1 = 127 bipartitions (exact). For N>8 we
       use Fiedler vector on graph Laplacian (spectral approx) — NOT canonical PyPhi.
    3. The original PhiCalculator divides spatial_phi by (n-1), which makes Φ scale ~O(MI/N).
       To match worktree-9 historical 51.131, we ALSO compute the un-normalized variant
       `total_mi - min_partition_mi` and report both.
    4. No PyPhi cross-validation — this is approximation, not gold-standard. Comparison to
       proxy is shape/scale, not absolute IIT correctness.
"""
from __future__ import annotations

import math
from typing import Dict, Tuple, Optional, List

import numpy as np
import torch


# ─── Mutual information ───────────────────────────────────────────────

def _mutual_information(
    x: np.ndarray, y: np.ndarray, n_bins: int = 16
) -> float:
    """Histogram-based MI(X;Y) = H(X) + H(Y) - H(X,Y).

    Direct port of worktree-9 PhiCalculator._mutual_information (n_bins parameterized).
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    y = np.asarray(y, dtype=np.float64).ravel()
    if x.size == 0 or y.size == 0:
        return 0.0

    x_range = x.max() - x.min()
    y_range = y.max() - y.min()
    x_norm = (x - x.min()) / (x_range + 1e-8)
    y_norm = (y - y.min()) / (y_range + 1e-8)

    joint_hist, _, _ = np.histogram2d(
        x_norm, y_norm, bins=n_bins, range=[[0, 1], [0, 1]]
    )
    joint_hist = joint_hist / (joint_hist.sum() + 1e-8)
    px = joint_hist.sum(axis=1)
    py = joint_hist.sum(axis=0)

    h_x = -np.sum(px * np.log2(px + 1e-10))
    h_y = -np.sum(py * np.log2(py + 1e-10))
    h_xy = -np.sum(joint_hist * np.log2(joint_hist + 1e-10))
    return float(max(0.0, h_x + h_y - h_xy))


# ─── Minimum information partition ────────────────────────────────────

def _minimum_partition(mi_matrix: np.ndarray) -> Tuple[float, List[int], List[int]]:
    """Find the minimum-cut bipartition over the MI graph.

    Returns (min_cut_mi, group_a, group_b).
    """
    n = mi_matrix.shape[0]
    if n <= 1:
        return 0.0, list(range(n)), []

    if n <= 8:
        # Exhaustive: try all 2^(n-1) - 1 non-trivial bipartitions
        min_cut_mi = float("inf")
        best_a: List[int] = []
        best_b: List[int] = []
        # Fix bit 0 in group_a to halve the search (symmetry)
        for mask in range(1, 1 << (n - 1)):
            full_mask = (mask << 1) | 1  # ensure bit 0 set
            group_a = [i for i in range(n) if full_mask & (1 << i)]
            group_b = [i for i in range(n) if not (full_mask & (1 << i))]
            if not group_a or not group_b:
                continue
            cut_mi = sum(mi_matrix[i, j] for i in group_a for j in group_b)
            if cut_mi < min_cut_mi:
                min_cut_mi = cut_mi
                best_a, best_b = group_a, group_b
        if min_cut_mi == float("inf"):
            return 0.0, list(range(n)), []
        return float(min_cut_mi), best_a, best_b

    # Spectral approximation: Fiedler vector of the MI Laplacian
    degree = mi_matrix.sum(axis=1)
    laplacian = np.diag(degree) - mi_matrix
    try:
        eigvals, eigvecs = np.linalg.eigh(laplacian)
        # Second-smallest eigenvalue's eigenvector
        fiedler = eigvecs[:, 1]
        group_a = [i for i in range(n) if fiedler[i] >= 0]
        group_b = [i for i in range(n) if fiedler[i] < 0]
        if not group_a or not group_b:
            group_a = list(range(n // 2))
            group_b = list(range(n // 2, n))
        cut_mi = sum(mi_matrix[i, j] for i in group_a for j in group_b)
        return float(cut_mi), group_a, group_b
    except Exception:
        # Fall back to even split
        group_a = list(range(n // 2))
        group_b = list(range(n // 2, n))
        cut_mi = sum(mi_matrix[i, j] for i in group_a for j in group_b)
        return float(cut_mi), group_a, group_b


# ─── Complexity ──────────────────────────────────────────────────────

def _norm_entropy(values: np.ndarray) -> float:
    """Shannon entropy of L2-norm distribution across cells (worktree-9 complexity)."""
    arr = np.asarray(values, dtype=np.float64).ravel()
    if arr.size < 2:
        return 0.0
    arr = arr - arr.min()
    total = arr.sum()
    if total < 1e-8:
        return 0.0
    probs = arr / total
    return float(-np.sum(probs * np.log2(probs + 1e-10)))


# ─── Public API ──────────────────────────────────────────────────────

def compute_iit_phi(
    cell_pool: torch.Tensor,
    n_bins: int = 16,
    return_matrix: bool = False,
) -> Dict[str, float]:
    """Compute IIT Φ on a (N, C) cell_pool tensor.

    Args:
        cell_pool:     (N, C) torch tensor or numpy array.
        n_bins:        Histogram bins for MI (16 = current spec, 32 = worktree-9 default).
        return_matrix: If True, include 'mi_matrix' (numpy) in output.

    Returns:
        Dict with keys: total_mi, min_partition_mi, integration, spatial_phi,
        spatial_phi_unnormalized, complexity, phi, phi_with_complexity, n_cells, n_bins.
    """
    if isinstance(cell_pool, torch.Tensor):
        cells_np = cell_pool.detach().cpu().numpy()
    else:
        cells_np = np.asarray(cell_pool)

    assert cells_np.ndim == 2, f"cell_pool must be (N, C); got {cells_np.shape}"
    n, c = cells_np.shape

    if n < 2:
        return {
            "total_mi": 0.0,
            "min_partition_mi": 0.0,
            "integration": 0.0,
            "spatial_phi": 0.0,
            "spatial_phi_unnormalized": 0.0,
            "complexity": 0.0,
            "phi": 0.0,
            "phi_with_complexity": 0.0,
            "n_cells": n,
            "n_bins": n_bins,
        }

    # 1. Pairwise MI matrix
    mi_matrix = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(i + 1, n):
            mi = _mutual_information(cells_np[i], cells_np[j], n_bins=n_bins)
            mi_matrix[i, j] = mi
            mi_matrix[j, i] = mi
    total_mi = float(mi_matrix.sum() / 2.0)

    # 2. Minimum information partition
    min_partition_mi, _, _ = _minimum_partition(mi_matrix)

    # 3. Spatial Φ — two variants
    spatial_phi_unnormalized = max(0.0, total_mi - min_partition_mi)
    spatial_phi = spatial_phi_unnormalized / max(n - 1, 1)  # worktree-9 normalization

    # 4. Complexity (norm entropy)
    norms = np.linalg.norm(cells_np, axis=1)
    complexity = _norm_entropy(norms)

    out: Dict[str, float] = {
        "total_mi": total_mi,
        "min_partition_mi": float(min_partition_mi),
        "integration": total_mi,
        "spatial_phi": float(spatial_phi),
        "spatial_phi_unnormalized": float(spatial_phi_unnormalized),
        "complexity": float(complexity),
        "phi": float(spatial_phi),
        "phi_with_complexity": float(spatial_phi + 0.1 * complexity),
        "n_cells": int(n),
        "n_bins": int(n_bins),
    }
    if return_matrix:
        out["mi_matrix"] = mi_matrix  # type: ignore[assignment]
    return out


def compute_iit_phi_temporal(
    cell_pool_now: torch.Tensor,
    cell_pool_prev: torch.Tensor,
    n_bins: int = 16,
) -> float:
    """Temporal MI between two consecutive cell_pool snapshots (cell-aligned by row).

    Returns mean per-cell MI(t, t-1). Cells with mismatched indices (post-split/merge) are
    skipped; only the first min(N_now, N_prev) rows are compared.
    """
    a = cell_pool_now if not isinstance(cell_pool_now, torch.Tensor) else cell_pool_now.detach().cpu().numpy()
    b = cell_pool_prev if not isinstance(cell_pool_prev, torch.Tensor) else cell_pool_prev.detach().cpu().numpy()
    n = min(a.shape[0], b.shape[0])
    if n == 0:
        return 0.0
    mis = [_mutual_information(a[i], b[i], n_bins=n_bins) for i in range(n)]
    return float(sum(mis) / max(n, 1))


# ─── Self-test ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== iit_phi_port self-test ===")
    torch.manual_seed(0)
    for n in [4, 8, 16, 32, 64]:
        cells = torch.randn(n, 12)
        cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        out = compute_iit_phi(cells, n_bins=16)
        print(
            f"  N={n:3d} C=12  total_mi={out['total_mi']:7.3f}  "
            f"min_cut={out['min_partition_mi']:7.3f}  "
            f"spatial_phi={out['spatial_phi']:.4f}  "
            f"unnorm={out['spatial_phi_unnormalized']:7.3f}  "
            f"complexity={out['complexity']:.3f}"
        )
