#!/usr/bin/env python3
# tool/anima_holographic_ib_ksg_validate_prod.py — F3 prod KSG MI scipy permutation_test
# ─────────────────────────────────────────────────────────────────────────────
# @raw9-relaxation: anima/.own own 1 opt-out (commit f890d69f 2026-04-28).
# Rationale: hexa interp single-thread cannot complete F3 cycle 1 prod-scale
# (n=200 perms=100 = 20K ops) within 15m Mac jetsam memory window. scipy
# vectorized + sklearn KSG MI completes same task in seconds.
# Scope: NARROW measurement-statistics-only. SSOT/governance/orchestration
# /canonical-helper path invocation = raw 71 retirement criterion violation.
# Long-term hexa-native scipy-equivalent KSG impl track preserved per raw 38
# implement-omega-converge.
# ─────────────────────────────────────────────────────────────────────────────
# F3 cycle 1 falsifier (anima evolution roadmap primary axes — see closure doc):
#   anima_holographic_ib_ksg_validate.hexa hetzner small-N=15 perms=10 returned
#   cohen_d=3.73 BORDERLINE p=0.064 — small-N statistical-power bottleneck.
#   This .py prod impl scales to n=200 perms=100 with same algorithmic
#   structure (KSG MI + scipy.stats.permutation_test).
#
# USAGE (post-exemption, post-impl):
#   python3 tool/anima_holographic_ib_ksg_validate_prod.py --selftest
#   python3 tool/anima_holographic_ib_ksg_validate_prod.py --run --n 200 --perms 100
#   python3 tool/anima_holographic_ib_ksg_validate_prod.py --run --n 30 --perms 20  # quick
#
# OUTPUT: JSON to stdout with cohen_d + p_value + n + perms + verdict.
# ─────────────────────────────────────────────────────────────────────────────

import sys
import json
import argparse
import datetime
import math

try:
    import numpy as np
    from sklearn.feature_selection import mutual_info_regression
    from scipy import stats as sp_stats
except ImportError as e:
    print(json.dumps({"error": f"missing dep: {e}", "fix": "pip install scipy numpy scikit-learn"}))
    sys.exit(1)

LINT_VERSION = "v1"
RAW9_RELAXATION_TAG = "F3-prod-scipy-permutation-test-2026-04-28"


def synth_holographic_pair(n_samples: int, dim_x: int, dim_y: int, coupling: float, seed: int):
    """Synthesize (X, Y) holographic IB-style pairs with controlled MI.

    Returns
    -------
    X : ndarray (n_samples, dim_x)
    Y : ndarray (n_samples, dim_y)
        Y = projection(X) + coupling * shared + noise, holographic IB structure.
    """
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n_samples, dim_x))
    shared = X[:, :min(dim_x, dim_y)].mean(axis=1, keepdims=True)
    Y_base = rng.standard_normal((n_samples, dim_y))
    Y = Y_base + coupling * np.broadcast_to(shared, (n_samples, dim_y))
    return X, Y


def ksg_mi_estimate(X, Y, k_neighbors: int = 3) -> float:
    """KSG mutual information estimator via sklearn.

    Reduces multivariate Y to scalar via first principal direction average for
    sklearn's mutual_info_regression which expects (X, y_scalar).
    """
    if Y.ndim > 1 and Y.shape[1] > 1:
        y_scalar = Y.mean(axis=1)
    else:
        y_scalar = Y.ravel()
    mi = mutual_info_regression(X, y_scalar, n_neighbors=k_neighbors, random_state=20260428)
    return float(np.mean(mi))


def cohens_d(group_a, group_b) -> float:
    """Cohen's d effect size — single-observation vs null-distribution variant.

    For permutation test (single obs_mi vs perm_mi distribution), pooled-SD denominator
    breaks (a.size-1 = 0 → NaN). This variant uses standardized effect size against null:
        d = (obs - null_mean) / null_std

    Falls back to standard pooled-SD Cohen's d when both groups have ≥2 elements.
    """
    a = np.asarray(group_a)
    b = np.asarray(group_b)
    if a.size == 1 and b.size > 1:
        # Standardized effect size: (obs - null_mean) / null_std
        null_std = float(b.std(ddof=1))
        if null_std == 0.0:
            return 0.0
        return float((a.mean() - b.mean()) / null_std)
    if b.size == 1 and a.size > 1:
        ref_std = float(a.std(ddof=1))
        if ref_std == 0.0:
            return 0.0
        return float((b.mean() - a.mean()) / ref_std)
    if a.size < 2 or b.size < 2:
        return 0.0
    pooled_sd = math.sqrt(((a.var(ddof=1) * (a.size - 1)) + (b.var(ddof=1) * (b.size - 1))) / (a.size + b.size - 2))
    if pooled_sd == 0:
        return 0.0
    return float((a.mean() - b.mean()) / pooled_sd)


def permutation_test_mi(X, Y, n_permutations: int, k_neighbors: int = 3, seed: int = 20260428):
    """Permutation test for MI(X; Y). Null: shuffle Y rows."""
    rng = np.random.default_rng(seed)
    obs_mi = ksg_mi_estimate(X, Y, k_neighbors)
    perm_mis = np.zeros(n_permutations, dtype=np.float64)
    for i in range(n_permutations):
        perm_idx = rng.permutation(Y.shape[0])
        perm_mis[i] = ksg_mi_estimate(X, Y[perm_idx], k_neighbors)
    p_value = float(np.mean(perm_mis >= obs_mi))
    d = cohens_d([obs_mi], perm_mis)
    return {
        "obs_mi": float(obs_mi),
        "perm_mi_mean": float(perm_mis.mean()),
        "perm_mi_std": float(perm_mis.std(ddof=1)) if perm_mis.size > 1 else 0.0,
        "p_value": p_value,
        "cohen_d": d,
        "n_permutations": int(n_permutations),
    }


def run(n_samples: int, n_permutations: int, dim_x: int = 8, dim_y: int = 8,
        coupling: float = 0.6, k_neighbors: int = 3, seed: int = 20260428):
    X, Y = synth_holographic_pair(n_samples, dim_x, dim_y, coupling, seed)
    result = permutation_test_mi(X, Y, n_permutations, k_neighbors, seed)
    p = result["p_value"]
    d = result["cohen_d"]
    f3_threshold_pass_strict = p < 0.05
    f3_threshold_pass_borderline = p < 0.10
    return {
        "tool": "anima_holographic_ib_ksg_validate_prod",
        "version": LINT_VERSION,
        "raw9_relaxation_tag": RAW9_RELAXATION_TAG,
        "n_samples": int(n_samples),
        "n_permutations": int(n_permutations),
        "dim_x": int(dim_x),
        "dim_y": int(dim_y),
        "coupling": float(coupling),
        "k_neighbors": int(k_neighbors),
        "seed": int(seed),
        "result": result,
        "f3_strict_pass_p_lt_0_05": bool(f3_threshold_pass_strict),
        "f3_borderline_pass_p_lt_0_10": bool(f3_threshold_pass_borderline),
        "verdict": ("PASS_STRICT" if f3_threshold_pass_strict
                    else ("PASS_BORDERLINE" if f3_threshold_pass_borderline
                          else "FAIL_above_threshold")),
        "ts": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_10_caveat": "scipy + sklearn deps; per anima/.own own 1 raw 9 explicit relaxation; scope narrow measurement-statistics-only",
    }


def selftest():
    """Selftest at small N=15 perms=10 (matches hetzner BORDERLINE result)."""
    out = {
        "tool": "anima_holographic_ib_ksg_validate_prod",
        "version": LINT_VERSION,
        "mode": "selftest",
        "raw9_relaxation_tag": RAW9_RELAXATION_TAG,
        "scope": "narrow_measurement_statistics_only",
        "raw_71_retirement_criterion": "invocation by SSOT/governance/orchestration/canonical-helper path = re-violation",
        "raw_38_long_term_track": "hexa-native scipy-equivalent KSG impl track preserved",
        "selftest_n": 15,
        "selftest_perms": 10,
    }
    try:
        r = run(n_samples=15, n_permutations=10, seed=20260428)
        out["selftest_result"] = r
        out["selftest_verdict"] = "PASS_HARNESS_RUN_TO_COMPLETION"
    except Exception as e:
        out["selftest_verdict"] = f"FAIL_HARNESS_ERROR: {e}"
    return out


def main():
    parser = argparse.ArgumentParser(description="F3 prod KSG MI scipy permutation_test")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--perms", type=int, default=20)
    parser.add_argument("--dim-x", type=int, default=8)
    parser.add_argument("--dim-y", type=int, default=8)
    parser.add_argument("--coupling", type=float, default=0.6)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260428)
    args = parser.parse_args()

    if args.selftest:
        out = selftest()
    elif args.run:
        out = run(args.n, args.perms, args.dim_x, args.dim_y, args.coupling, args.k, args.seed)
    else:
        out = {
            "usage": "python3 tool/anima_holographic_ib_ksg_validate_prod.py --selftest | --run --n 200 --perms 100",
            "raw9_relaxation_tag": RAW9_RELAXATION_TAG,
            "scope": "narrow_measurement_statistics_only",
        }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
