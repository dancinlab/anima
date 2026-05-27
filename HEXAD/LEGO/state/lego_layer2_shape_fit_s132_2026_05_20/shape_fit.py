"""
§132 LEGO LAYER-2 NON-MONOTONIC SHAPE FIT
==========================================

§127 OLS log-linear fit gave k=-0.0198, R²=0.022 → APPROXIMATELY-N-INVARIANT,
honest residual: "logistic / piecewise / saturating fits = future work."

§132 closes that residual: re-fit §127's 4 (N, η²) points with three candidate
non-linear models, compare R², pick the best.

Models (all OLS-fittable on transformed coordinates or numpy.polyfit):
  (A) log-linear  (§127 baseline)   log η² = log a + k · log N
  (B) quadratic-in-logN              log η² = c0 + c1 · logN + c2 · logN²   (peaked curve)
  (C) saturating Hill / Michaelis    η² = η_max · N / (N + K)               (monotone saturation)
  (D) inverted-U Gaussian-in-logN    log η² = c0 − ((logN − μ) / σ)² / 2     (peaked, symmetric)

Compare R² values; highest R² wins. Pre-registered classification:
  if best R² ≥ 0.80         → SHAPE-FIT-IDENTIFIED
  if 0.30 ≤ best R² < 0.80   → SHAPE-FIT-WEAK
  if best R² < 0.30          → 4-POINTS-INSUFFICIENT-FOR-NON-LINEAR-MODELS

Honest: 4 points and 3 free parameters (quadratic) = 1 d.o.f.; 4-parameter
models (Gaussian) = 0 d.o.f. R² overfits in low-d.o.f. regime — closure
classification *requires* R² ≥ 0.80 to call a shape "identified."
"""

import json
import math
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
S127_RESULT = ANIMA / "state" / "lego_layer2_scaling_law_s127_2026_05_20" / "result.json"


def fit_log_linear(logN, logE):
    """OLS log η² = a + k logN; §127 baseline."""
    A = np.vstack([np.ones_like(logN), logN]).T
    coef, *_ = np.linalg.lstsq(A, logE, rcond=None)
    pred = A @ coef
    ss_res = ((logE - pred) ** 2).sum()
    ss_tot = ((logE - logE.mean()) ** 2).sum()
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {"model": "log_linear", "n_params": 2,
            "coefficients": {"log_a": float(coef[0]), "k": float(coef[1])},
            "log_eta_predicted": pred.tolist(),
            "r_squared": float(r_sq),
            "fits_peak_or_drop": False}


def fit_quadratic_log(logN, logE):
    """OLS log η² = c0 + c1·logN + c2·logN²; admits peak shape."""
    A = np.vstack([np.ones_like(logN), logN, logN ** 2]).T
    coef, *_ = np.linalg.lstsq(A, logE, rcond=None)
    pred = A @ coef
    ss_res = ((logE - pred) ** 2).sum()
    ss_tot = ((logE - logE.mean()) ** 2).sum()
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    # Peak location (if c2<0 there's a maximum at logN* = -c1/(2c2))
    has_max = coef[2] < 0
    peak_logN = float(-coef[1] / (2.0 * coef[2])) if abs(coef[2]) > 1e-12 else float("nan")
    peak_N = float(math.exp(peak_logN)) if has_max and math.isfinite(peak_logN) else float("nan")
    return {"model": "quadratic_log", "n_params": 3,
            "coefficients": {"c0": float(coef[0]), "c1": float(coef[1]), "c2": float(coef[2])},
            "log_eta_predicted": pred.tolist(),
            "r_squared": float(r_sq),
            "fits_peak_or_drop": True,
            "has_max": bool(has_max),
            "peak_log_N": peak_logN,
            "peak_N_estimate": peak_N}


def fit_saturating_hill(N, eta):
    """Iterative fit η² = η_max · N / (N + K). Linearise via 1/η = 1/η_max + (K/η_max)·(1/N)."""
    inv_eta = 1.0 / eta
    inv_N = 1.0 / N
    A = np.vstack([np.ones_like(inv_N), inv_N]).T
    coef, *_ = np.linalg.lstsq(A, inv_eta, rcond=None)
    inv_eta_max = coef[0]
    K_over_eta_max = coef[1]
    eta_max = float(1.0 / inv_eta_max)
    K = float(K_over_eta_max * eta_max)
    pred_eta = eta_max * N / (N + K)
    ss_res = ((eta - pred_eta) ** 2).sum()
    ss_tot = ((eta - eta.mean()) ** 2).sum()
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {"model": "saturating_hill", "n_params": 2,
            "coefficients": {"eta_max": eta_max, "K": K},
            "eta_predicted": pred_eta.tolist(),
            "r_squared": float(r_sq),
            "fits_peak_or_drop": False}


def fit_inverted_u_gaussian(logN, logE):
    """log η² = a − ((logN − μ) / σ)² / 2. Same DoF as quadratic-log."""
    A = np.vstack([np.ones_like(logN), logN, logN ** 2]).T
    coef, *_ = np.linalg.lstsq(A, logE, rcond=None)
    # Re-parameterise: if c2 = -1/(2σ²) and c1 = μ/σ², then σ²=-1/(2c2), μ=c1·σ², a=c0+μ²/(2σ²)
    if coef[2] >= 0:
        return {"model": "inverted_u_gaussian", "n_params": 3,
                "fit_failed_because": "c2 ≥ 0 (no upward-curving Gaussian)",
                "r_squared": -float("inf"),
                "fits_peak_or_drop": False}
    sigma_sq = -1.0 / (2.0 * coef[2])
    mu = coef[1] * sigma_sq
    a = coef[0] + (mu ** 2) / (2.0 * sigma_sq)
    pred = a - ((logN - mu) ** 2) / (2.0 * sigma_sq)
    ss_res = ((logE - pred) ** 2).sum()
    ss_tot = ((logE - logE.mean()) ** 2).sum()
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return {"model": "inverted_u_gaussian", "n_params": 3,
            "coefficients": {"log_eta_peak": float(a), "log_N_peak": float(mu),
                              "sigma": float(math.sqrt(sigma_sq))},
            "log_eta_predicted": pred.tolist(),
            "r_squared": float(r_sq),
            "fits_peak_or_drop": True,
            "peak_N_estimate": float(math.exp(mu))}


def classify(best_r_sq: float) -> dict:
    if best_r_sq >= 0.80:
        v = "SHAPE-FIT-IDENTIFIED"
        n = f"best R² {best_r_sq:.3f} ≥ 0.80 — a non-linear model fits η²(N) at this resolution."
    elif 0.30 <= best_r_sq < 0.80:
        v = "SHAPE-FIT-WEAK"
        n = f"best R² {best_r_sq:.3f} — model captures some structure but cannot be called identified at this scope."
    else:
        v = "4-POINTS-INSUFFICIENT-FOR-NON-LINEAR-MODELS"
        n = f"best R² {best_r_sq:.3f} < 0.30 — 4 points cannot distinguish non-linear models from §127 baseline noise."
    return {"verdict": v, "note": n}


def main():
    s127 = json.loads(S127_RESULT.read_text())
    pts = sorted(s127["per_N_measurements"], key=lambda m: m["N_total"])
    N = np.array([m["N_total"] for m in pts], dtype=np.float64)
    eta = np.array([m["eta_squared"] for m in pts], dtype=np.float64)
    logN = np.log(N)
    logE = np.log(eta)

    fits = {
        "A_log_linear": fit_log_linear(logN, logE),
        "B_quadratic_log": fit_quadratic_log(logN, logE),
        "C_saturating_hill": fit_saturating_hill(N, eta),
        "D_inverted_u_gaussian": fit_inverted_u_gaussian(logN, logE),
    }
    # Find best by R²
    best = max(fits.items(), key=lambda kv: kv[1].get("r_squared", -float("inf")))
    best_name, best_fit = best
    cls = classify(best_fit["r_squared"])

    # honest baseline comparison
    log_linear_r2 = fits["A_log_linear"]["r_squared"]
    delta_r2 = best_fit["r_squared"] - log_linear_r2

    result = {
        "section": "§132",
        "title": "LEGO LAYER-2 NON-MONOTONIC SHAPE FIT",
        "tier": "analysis-tier (re-fit of §127 data)",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§127 4-point η²(N) fit (OLS log-linear R²=0.022 → APPROXIMATELY-N-INVARIANT)",
            "§127 honest residual: 'logistic / piecewise / saturating = future work'",
        ],
        "method": {
            "n_points": int(len(N)),
            "N_values": N.tolist(),
            "eta_values": eta.tolist(),
            "candidate_models": ["A_log_linear", "B_quadratic_log",
                                  "C_saturating_hill", "D_inverted_u_gaussian"],
        },
        "fits": fits,
        "best_model": best_name,
        "best_r_squared": best_fit["r_squared"],
        "log_linear_r_squared_baseline": log_linear_r2,
        "delta_r_squared_over_baseline": float(delta_r2),
        "verdict": cls["verdict"],
        "verdict_note": cls["note"],
        "g3": "analysis ≠ measurement ≠ fire ≠ emergence; capability claim 0; GOAL 미도달.",
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    summary = {
        "best_model": best_name,
        "best_r_squared": round(best_fit["r_squared"], 4),
        "log_linear_baseline_r2": round(log_linear_r2, 4),
        "delta_r2_over_baseline": round(delta_r2, 4),
        "verdict": cls["verdict"],
        "all_r_squared": {k: round(v.get("r_squared", -float("inf")), 4)
                           for k, v in fits.items()},
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
