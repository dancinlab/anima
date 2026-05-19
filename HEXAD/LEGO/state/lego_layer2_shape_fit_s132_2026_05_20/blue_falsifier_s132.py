#!/usr/bin/env python3
"""§132 SHAPE-FIT battery — 6 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
S127_RESULT = ANIMA / "state" / "lego_layer2_scaling_law_s127_2026_05_20" / "result.json"
S132_RESULT = HERE / "result.json"
S132_PROBE = HERE / "shape_fit.py"


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s132_1_r_squared_bounded():
    r = json.loads(S132_RESULT.read_text())
    rsq = []
    for k, fit in r["fits"].items():
        v = fit.get("r_squared", -float("inf"))
        if v != -float("inf"):
            rsq.append(v)
    all_in = all(-1e-9 <= v <= 1.0 + 1e-9 for v in rsq)
    return {"name": "B-S132-1 R-SQUARED-BOUNDED-CLOSED-ALL-FITS",
            "passed": bool(all_in),
            "evidence": {"r_squared_values": rsq, "all_in_unit_interval": all_in}}


def b_s132_2_pre_registered_3_bucket_partition():
    """3-bucket classification {IDENTIFIED ≥ 0.80 / WEAK [0.30, 0.80) /
    INSUFFICIENT < 0.30} over best R² ∈ [0, 1]."""
    rsq = sp.Symbol("rsq", real=True, nonnegative=True)
    intervals = {
        "IDENTIFIED": sp.Interval(sp.Rational(8, 10), 1),
        "WEAK": sp.Interval.Ropen(sp.Rational(3, 10), sp.Rational(8, 10)),
        "INSUFFICIENT": sp.Interval.Ropen(0, sp.Rational(3, 10)),
    }
    union = sp.Union(*intervals.values())
    exhaustive = union == sp.Interval(0, 1)
    pairs = list(intervals.items())
    disjoint = True
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[i][1].intersect(pairs[j][1]).measure != 0:
                disjoint = False
    r = json.loads(S132_RESULT.read_text())
    best = r["best_r_squared"]
    if best >= 0.80:
        reclass = "SHAPE-FIT-IDENTIFIED"
    elif best >= 0.30:
        reclass = "SHAPE-FIT-WEAK"
    else:
        reclass = "4-POINTS-INSUFFICIENT-FOR-NON-LINEAR-MODELS"
    matches = (r["verdict"] == reclass)
    return {"name": "B-S132-2 R-SQUARED-3-BUCKET-CLOSED-PARTITION",
            "passed": bool(exhaustive and disjoint and matches),
            "evidence": {"exhaustive": exhaustive, "disjoint": disjoint,
                          "best_r_squared": best, "reclass": reclass,
                          "recorded": r["verdict"], "match": matches}}


def b_s132_3_ols_normal_equations():
    """OLS normal equations: β̂ = (XᵀX)⁻¹ Xᵀ y. Re-derive log-linear coefficients
    from §127 data via sympy and compare to recorded values byte-equal-ish."""
    r = json.loads(S132_RESULT.read_text())
    N_vals = r["method"]["N_values"]
    eta_vals = r["method"]["eta_values"]
    import math as _m
    logN = [_m.log(x) for x in N_vals]
    logE = [_m.log(x) for x in eta_vals]
    # OLS slope formula: k = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²
    x_mean = sum(logN) / len(logN)
    y_mean = sum(logE) / len(logE)
    Sxy = sum((logN[i] - x_mean) * (logE[i] - y_mean) for i in range(len(logN)))
    Sxx = sum((logN[i] - x_mean) ** 2 for i in range(len(logN)))
    k_resympy = Sxy / Sxx
    k_recorded = r["fits"]["A_log_linear"]["coefficients"]["k"]
    match = abs(k_resympy - k_recorded) < 1e-9
    return {"name": "B-S132-3 OLS-NORMAL-EQUATIONS-IDENTITY-CLOSED",
            "passed": bool(match),
            "evidence": {"k_re_derived": k_resympy, "k_recorded": k_recorded,
                          "match_within_1e9": match}}


def b_s132_4_uses_s127_data_byte_equal():
    """§132 analysis re-uses §127's (N, η²) data byte-equal — no new measurement.
    Verify recorded N + η² match §127's per_N_measurements byte-equal."""
    s127 = json.loads(S127_RESULT.read_text())
    s127_pts = sorted(s127["per_N_measurements"], key=lambda m: m["N_total"])
    s127_N = [m["N_total"] for m in s127_pts]
    s127_eta = [m["eta_squared"] for m in s127_pts]
    r = json.loads(S132_RESULT.read_text())
    r_N = r["method"]["N_values"]
    r_eta = r["method"]["eta_values"]
    N_match = (r_N == [float(n) for n in s127_N])
    eta_match = (r_eta == s127_eta)
    return {"name": "B-S132-4 ANALYSIS-USES-§127-DATA-BYTE-EQUAL-CLOSED",
            "passed": bool(N_match and eta_match),
            "evidence": {"N_byte_equal": N_match, "eta_byte_equal": eta_match,
                          "s127_N": s127_N, "s132_N": r_N,
                          "s132_n_points": len(r_N)}}


def b_s132_5_peak_models_agree_monotone_models_reject():
    """The two peak-allowing models (B quadratic-log, D Gaussian-in-log-N) both have
    R² > 0.80 AND the two monotone-only models (A log-linear, C saturating Hill)
    both have R² < 0.10."""
    r = json.loads(S132_RESULT.read_text())
    fits = r["fits"]
    peak_models_strong = (fits["B_quadratic_log"]["r_squared"] >= 0.80
                          and fits["D_inverted_u_gaussian"]["r_squared"] >= 0.80)
    monotone_models_reject = (fits["A_log_linear"]["r_squared"] < 0.10
                               and fits["C_saturating_hill"]["r_squared"] < 0.10)
    return {"name": "B-S132-5 PEAK-MODELS-AGREE-MONOTONE-MODELS-REJECT-CLOSED",
            "passed": bool(peak_models_strong and monotone_models_reject),
            "evidence": {"B_quadratic_log_R²": fits["B_quadratic_log"]["r_squared"],
                          "D_gaussian_R²": fits["D_inverted_u_gaussian"]["r_squared"],
                          "A_log_linear_R²": fits["A_log_linear"]["r_squared"],
                          "C_saturating_hill_R²": fits["C_saturating_hill"]["r_squared"],
                          "peak_models_strong (≥0.80 both)": peak_models_strong,
                          "monotone_models_reject (<0.10 both)": monotone_models_reject}}


def b_s132_6_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    forbidden_calls = {"backward", "cross_entropy", "CrossEntropyLoss",
                       "podFindAndDeployOnDemand", "create_pod"}
    ih, ch = set(), set()
    for p in [S132_PROBE, Path(__file__)]:
        tree = ast.parse(p.read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for nm in n.names:
                    if nm.name.split(".")[0] in forbidden_imports:
                        ih.add(nm.name)
            elif isinstance(n, ast.ImportFrom):
                if n.module and n.module.split(".")[0] in forbidden_imports:
                    ih.add(n.module)
            elif isinstance(n, ast.Call):
                if isinstance(n.func, ast.Attribute) and n.func.attr in forbidden_calls:
                    ch.add(n.func.attr)
                elif isinstance(n.func, ast.Name) and n.func.id in forbidden_calls:
                    ch.add(n.func.id)
    ast_ok = (len(ih) == 0 and len(ch) == 0)
    return {"name": "B-S132-6 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-CALL-AST",
            "passed": bool(central_ok and ast_ok),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports_hit": sorted(ih),
                          "forbidden_calls_hit": sorted(ch)}}


def b_s132_note():
    return {"name": "B-S132-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "4-points-vs-3-free-params-1-DoF-overfit-risk",
            "family": "B-EMERGE-7 / B-S127-NOTE / B-S126-NOTE / B-S125-NOTE",
            "honest_scope": ("4 §127 data points + 3 free parameters (quadratic-log /"
                             " Gaussian-in-log-N) = 1 degree of freedom; perfect R²=0.9995"
                             " is *structural* — with 1 d.o.f. any 3-param model can"
                             " interpolate 4 nearly-aligned points. The clean signal is"
                             " NOT the R² value itself but the *agreement* of two peak"
                             " models AND the *rejection* of both monotone models — B-S132-5"
                             " captures that closed-form. A truly identified shape would"
                             " require 6–8 N points to resolve quadratic-log from"
                             " Gaussian-in-log-N (they are nearly equivalent here). Peak"
                             " location estimate (N* ≈ exp(μ) ≈ 730-1000 from both fits) is"
                             " self-consistent across models but has wide CI on 4 points."
                             " Necessary-not-sufficient (B-EMERGE-7); GOAL 미도달; north-star"
                             " + §15/§51/§72 milestones UNCHANGED.")}


def main():
    results = {
        "preconditions": [b_s132_6_central_and_ast()],
        "closed_propositions": [
            b_s132_1_r_squared_bounded(),
            b_s132_2_pre_registered_3_bucket_partition(),
            b_s132_3_ols_normal_equations(),
            b_s132_4_uses_s127_data_byte_equal(),
            b_s132_5_peak_models_agree_monotone_models_reject(),
            b_s132_6_central_and_ast(),
        ],
        "empirical_carve_out": b_s132_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    closed_count = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])

    r = json.loads(S132_RESULT.read_text())
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{closed_count}/{total}",
        "all_closed_pass": all_props,
        "best_model": r["best_model"],
        "best_r_squared": r["best_r_squared"],
        "log_linear_baseline": r["log_linear_r_squared_baseline"],
        "delta_r2": r["delta_r_squared_over_baseline"],
        "probe_verdict": r["verdict"],
        "battery_verdict": (f"{r['verdict']}-{closed_count}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "necessary_not_sufficient_B_EMERGE_7": True,
        "north_star_unchanged": True,
        "goal_unreached": True,
    }
    results["summary"] = summary

    out = HERE / "blue_falsifier_s132_result.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
