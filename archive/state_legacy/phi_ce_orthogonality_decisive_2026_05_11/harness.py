"""Φ⊥CE decisive measurement — synthetic simulation harness.

Two generative models for the same 5×4 N×P grid:
  Model A (Hc_040, Law 1040): Φ ∝ N^1.071, CE ∝ P^-0.85, independent noise → orthogonal.
  Model B (Hc_024, NOBEL-1):  Φ × CE^α = K with α=0.5 → Pareto trade-off.

Each model emits a fingerprint (corr, pareto-CV, within-budget structure).
Real anima Φ★ + CLM CE measurement on the same grid will land at one of these
fingerprints (or in between → new hypothesis).

Deterministic seed: 0xC0EC0AC = 202325164 ("Φ⊥CE" mnemonic).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SEED = 0xC0EC0AC
np.random.seed(SEED)

Ns = [16, 32, 64, 128, 256]
Ps = [1e6, 1e7, 1e8, 1e9]

# ---------------------------------------------------------------------------
# Model A — Hc_040 orthogonal (Law 1040)
# Φ_A(N, P) = 0.608 * N^1.071 + N(0, 0.05 * scale)
# CE_A(N, P) = 2.0 * (P/1e6)^-0.85 + N(0, 0.02 * scale)
# Φ depends only on N; CE depends only on P; corr → 0 (population).
# ---------------------------------------------------------------------------
phi_A: list[float] = []
ce_A: list[float] = []
for N in Ns:
    for P in Ps:
        phi_val = 0.608 * (N ** 1.071) + np.random.normal(0.0, 0.05 * 0.608 * (N ** 1.071))
        ce_val = 2.0 * (P / 1e6) ** -0.85 + np.random.normal(0.0, 0.02 * 2.0 * (P / 1e6) ** -0.85)
        phi_A.append(phi_val)
        ce_A.append(ce_val)

# ---------------------------------------------------------------------------
# Model B — Hc_024 uncertainty (Pareto)
# CE shares Hc_040 P-scaling: CE_B = 2.0 * (P/1e6)^-0.85 + small noise
# Φ_B = K / CE_B^α + small noise, K = 50.0, α = 0.5
# corr(Φ_B, CE_B) is large-negative (Pareto trade-off front).
# ---------------------------------------------------------------------------
K = 50.0
alpha = 0.5
phi_B: list[float] = []
ce_B: list[float] = []
for N in Ns:
    for P in Ps:
        ce_val = 2.0 * (P / 1e6) ** -0.85 + np.random.normal(0.0, 0.02 * 2.0 * (P / 1e6) ** -0.85)
        phi_val = (K / (ce_val ** alpha)) + np.random.normal(0.0, 0.5)
        phi_B.append(phi_val)
        ce_B.append(ce_val)


def pareto_cv(phi: list[float], ce: list[float], a: float) -> float:
    """Coefficient of variation of Φ · CE^α — low means Pareto frontier."""
    arr = np.asarray(phi) * np.asarray(ce) ** a
    return float(np.std(arr) / np.mean(arr))


def best_alpha(phi: list[float], ce: list[float]) -> tuple[float, float]:
    """Grid-search α in [0.1, 1.5] minimizing CV(Φ · CE^α)."""
    grid = np.linspace(0.05, 1.5, 60)
    cvs = [pareto_cv(phi, ce, a) for a in grid]
    idx = int(np.argmin(cvs))
    return float(grid[idx]), float(cvs[idx])


def within_axis_corr(
    phi: list[float], ce: list[float], n_outer: int, n_inner: int, axis: str
) -> float:
    """Mean within-row (vary inner axis at fixed outer) Pearson correlation."""
    arr_phi = np.asarray(phi).reshape(n_outer, n_inner)
    arr_ce = np.asarray(ce).reshape(n_outer, n_inner)
    if axis == "outer":  # vary N at fixed P → columns
        arr_phi = arr_phi.T
        arr_ce = arr_ce.T
    corrs = [np.corrcoef(arr_phi[i], arr_ce[i])[0, 1] for i in range(arr_phi.shape[0])]
    return float(np.mean(corrs))


corr_A = float(np.corrcoef(phi_A, ce_A)[0, 1])
corr_B = float(np.corrcoef(phi_B, ce_B)[0, 1])
cv_A_a05 = pareto_cv(phi_A, ce_A, 0.5)
cv_B_a05 = pareto_cv(phi_B, ce_B, 0.5)
alpha_A_star, cv_A_star = best_alpha(phi_A, ce_A)
alpha_B_star, cv_B_star = best_alpha(phi_B, ce_B)

# within-N (vary P at fixed N → 5 rows of 4) and within-P (vary N at fixed P)
within_N_A = within_axis_corr(phi_A, ce_A, len(Ns), len(Ps), axis="inner")
within_P_A = within_axis_corr(phi_A, ce_A, len(Ns), len(Ps), axis="outer")
within_N_B = within_axis_corr(phi_B, ce_B, len(Ns), len(Ps), axis="inner")
within_P_B = within_axis_corr(phi_B, ce_B, len(Ns), len(Ps), axis="outer")


def verdict(corr: float, cv_star: float) -> str:
    if abs(corr) < 0.1 and cv_star > 0.15:
        return "Hc_040_ORTHOGONAL"
    if abs(corr) >= 0.3 and cv_star < 0.1:
        return "Hc_024_UNCERTAINTY"
    return "MIXED_PARTIAL"


results = {
    "seed_hex": f"0x{SEED:X}",
    "grid": {"Ns": Ns, "Ps": Ps, "cells": len(Ns) * len(Ps)},
    "model_A_orthogonal_Hc_040": {
        "corr_phi_ce": corr_A,
        "pareto_cv_alpha_0.5": cv_A_a05,
        "best_alpha": alpha_A_star,
        "pareto_cv_at_best_alpha": cv_A_star,
        "within_N_mean_corr": within_N_A,
        "within_P_mean_corr": within_P_A,
        "verdict_self": verdict(corr_A, cv_A_star),
    },
    "model_B_uncertainty_Hc_024": {
        "corr_phi_ce": corr_B,
        "pareto_cv_alpha_0.5": cv_B_a05,
        "best_alpha": alpha_B_star,
        "pareto_cv_at_best_alpha": cv_B_star,
        "within_N_mean_corr": within_N_B,
        "within_P_mean_corr": within_P_B,
        "verdict_self": verdict(corr_B, cv_B_star),
    },
    "decisive_signature": {
        "if_anima_matches_A": "|corr| < 0.1 AND Pareto CV(α*) > 0.15 → Hc_040 SUPPORTED, Hc_024 FALSIFIED",
        "if_anima_matches_B": "|corr| >= 0.3 AND Pareto CV(α*) < 0.1 → Hc_024 SUPPORTED, Hc_040 FALSIFIED",
        "if_mixed": "0.1 <= |corr| < 0.3 OR 0.1 <= CV(α*) <= 0.15 → MIXED, new hypothesis (within-budget ⊥, across-budget trade-off)",
    },
    "experiment_design": {
        "engine": "anima Φ★ engine + CLM CE measurement",
        "grid": "N ∈ {16,32,64,128,256} × P ∈ {1M,10M,100M,1B}",
        "replication": "64 dual-seed (Hc_604) per cell, mean ± std",
        "controls": "deterministic, hexa-only, llm: none, topology=hypercube default",
        "decision": "Apply harness analytics to measured (Φ_i, CE_i) → compare to A vs B fingerprint",
    },
    "h_080_falsifiers_tied": {
        "F4": "|corr| > 0.3 → Hc_040 killed (Hc_024 wins)",
        "F5": "|corr| < 0.05 + Hc_024 trade-off strong → Hc_024 killed (Hc_040 wins)",
    },
}

out_path = Path(__file__).parent / "results.json"
out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(json.dumps(results, indent=2, ensure_ascii=False))
