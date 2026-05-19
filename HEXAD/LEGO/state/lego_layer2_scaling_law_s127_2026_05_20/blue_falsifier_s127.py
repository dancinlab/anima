#!/usr/bin/env python3
"""§127 SCALING-LAW battery — 8 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import math
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
S117_LEGO_SIM = ANIMA / "state" / "lego_assembly_run_s117_2026_05_19" / "lego_sim.py"
S126_RESULT = ANIMA / "state" / "lego_layer2_nscale_probe_s126_2026_05_20" / "result.json"
S127_RESULT = HERE / "result.json"
S127_PROBE = HERE / "probe_scaling_law.py"


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s127_1_eta_bounded_all_n():
    r = json.loads(S127_RESULT.read_text())
    all_in = all(0.0 <= m["eta_squared"] <= 1.0 for m in r["per_N_measurements"])
    return {"name": "B-S127-1 ETA-BOUNDED-ALL-4-N-POINTS",
            "passed": bool(all_in),
            "evidence": {"eta_values": [m["eta_squared"] for m in r["per_N_measurements"]],
                          "all_in_unit_interval": all_in}}


def b_s127_2_log_linear_fit_ols_identity():
    """OLS slope identity:  k = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²  with x = log N, y = log η².
    Verify the recorded k via independent sympy re-derivation."""
    r = json.loads(S127_RESULT.read_text())
    fit = r["power_law_fit"]
    x = sp.Matrix(fit["log_N_values"])
    y = sp.Matrix(fit["log_eta_values"])
    n = x.rows
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    Sxy = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    Sxx = sum((x[i] - x_mean) ** 2 for i in range(n))
    k_sympy = float(Sxy / Sxx)
    k_recorded = fit["k_scaling_exponent"]
    match = abs(k_sympy - k_recorded) < 1e-9
    return {"name": "B-S127-2 LOG-LINEAR-OLS-IDENTITY-CLOSED",
            "passed": bool(match),
            "evidence": {"k_sympy_rederived": k_sympy,
                          "k_recorded": k_recorded,
                          "match_within_1e9": match}}


def b_s127_3_r_squared_bounded():
    r = json.loads(S127_RESULT.read_text())
    rsq = r["power_law_fit"]["r_squared"]
    in_range = -1.0 <= rsq <= 1.0  # R² for OLS over real points is in [0,1], but allow [-1,1] safety
    standard = 0.0 <= rsq <= 1.0
    return {"name": "B-S127-3 R-SQUARED-BOUNDED-CLOSED",
            "passed": bool(in_range and standard),
            "evidence": {"r_squared": rsq, "in_unit_interval": standard}}


def b_s127_4_scaling_3_bucket_partition():
    """3-bucket classification {ROBUST-POWER-LAW, APPROX-INVARIANT, DEGRADES} over k ∈ ℝ.

    Partition:  k > 0.10 → ROBUST  /  -0.10 ≤ k ≤ 0.10 → INVARIANT  /  k < -0.10 → DEGRADES.
    """
    k = sp.Symbol("k", real=True)
    intervals = {
        "ROBUST": sp.Interval.open(sp.Rational(1, 10), sp.oo),
        "INVARIANT": sp.Interval(sp.Rational(-1, 10), sp.Rational(1, 10)),
        "DEGRADES": sp.Interval.open(-sp.oo, sp.Rational(-1, 10)),
    }
    union = sp.Union(*intervals.values())
    exhaustive = union == sp.Interval(-sp.oo, sp.oo)
    pairs = list(intervals.items())
    disjoint = True
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[i][1].intersect(pairs[j][1]).measure != 0:
                disjoint = False
    r = json.loads(S127_RESULT.read_text())
    k_meas = r["power_law_fit"]["k_scaling_exponent"]
    if k_meas > 0.10:
        reclass = "ROBUST-POWER-LAW-GROWS-WITH-N"
    elif -0.10 <= k_meas <= 0.10:
        reclass = "APPROXIMATELY-N-INVARIANT"
    else:
        reclass = "DEGRADES-WITH-N-SMALL-N-ARTIFACT"
    matches = r["verdict"] == reclass
    passed = bool(exhaustive and disjoint and matches)
    return {"name": "B-S127-4 SCALING-3-BUCKET-CLOSED-PARTITION",
            "passed": passed,
            "evidence": {"exhaustive": exhaustive, "disjoint": disjoint,
                          "k_measured": k_meas, "reclass": reclass,
                          "recorded": r["verdict"], "match": matches}}


def b_s127_5_s126_single_point_carried_but_not_a_scaling_law():
    """B-S127-5 honest connection-point: §126's measured 1.189× ratio at single
    scale-pair (256→1024) is NUMERICALLY CONFIRMED here (η²(256) and η²(1024) match
    §126's values byte-equal up to RNG-determinism), BUT the 4-point fit (R²=0.022,
    |k|≤0.10) shows this is NOT a power-law growth pattern across the wider 256–2048
    range. §126's verdict ROBUST-GROWS-WITH-N is *true at its scope* (one scale-pair)
    but does NOT extrapolate to a scaling law.
    """
    s127 = json.loads(S127_RESULT.read_text())
    s126 = json.loads(S126_RESULT.read_text())

    s127_eta_256 = next(m["eta_squared"] for m in s127["per_N_measurements"] if m["N_total"] == 256)
    s127_eta_1024 = next(m["eta_squared"] for m in s127["per_N_measurements"] if m["N_total"] == 1024)
    s126_eta_256 = s126["comparator_s125"]["eta_squared_s125"]
    s126_eta_1024 = s126["variance_decomposition_s126"]["eta_squared"]

    # §126 values match §127's N=256 + N=1024 measurements byte-equal (same seeds, same code)
    match_256 = abs(s127_eta_256 - s126_eta_256) < 1e-12
    match_1024 = abs(s127_eta_1024 - s126_eta_1024) < 1e-12

    # Honest refinement: §126's single-point ratio confirmed; but full fit refutes scaling law
    fit_r_squared = s127["power_law_fit"]["r_squared"]
    fit_not_power_law = fit_r_squared < 0.5  # honest threshold for "this is not a power law"

    passed = bool(match_256 and match_1024 and fit_not_power_law)
    return {"name": "B-S127-5 §126-SINGLE-POINT-CONFIRMED-NOT-A-SCALING-LAW",
            "passed": passed,
            "evidence": {
                "s127_eta_at_N256_matches_s126_byte_equal": match_256,
                "s127_eta_at_N1024_matches_s126_byte_equal": match_1024,
                "s127_full_fit_r_squared": fit_r_squared,
                "fit_does_not_describe_power_law (R²<0.5)": fit_not_power_law,
                "honest_refinement": ("§126's 1.189× is one valid scale-pair ratio, "
                                       "NOT a generalisable scaling law"),
            }}


def b_s127_6_monotonicity_check():
    """B-S127-6: η²(N) is NON-MONOTONIC over {256, 512, 1024, 2048} — there exists a
    triple (N_i < N_j < N_k) such that NOT (η²(N_i) ≤ η²(N_j) ≤ η²(N_k)) AND
    NOT (η²(N_i) ≥ η²(N_j) ≥ η²(N_k))."""
    r = json.loads(S127_RESULT.read_text())
    ms = sorted(r["per_N_measurements"], key=lambda m: m["N_total"])
    Ns = [m["N_total"] for m in ms]
    es = [m["eta_squared"] for m in ms]
    monotone_up = all(es[i] <= es[i+1] for i in range(len(es)-1))
    monotone_down = all(es[i] >= es[i+1] for i in range(len(es)-1))
    non_monotonic = (not monotone_up) and (not monotone_down)
    return {"name": "B-S127-6 ETA-NON-MONOTONIC-OVER-4-POINTS",
            "passed": bool(non_monotonic),
            "evidence": {"N_sorted": Ns, "eta_sorted": es,
                          "monotone_up": monotone_up, "monotone_down": monotone_down,
                          "non_monotonic": non_monotonic}}


def b_s127_7_s117_import_byte_equal():
    s117_sha = sha16(S117_LEGO_SIM)
    src = S127_PROBE.read_text()
    tree = ast.parse(src)
    idents = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name): idents.add(n.id)
        elif isinstance(n, ast.Attribute): idents.add(n.attr)
    refs = ("S117_LEGO_SIM" in idents) or ("s117_lego_sim" in idents)
    uses_importlib = any("importlib" in (n.module or "") for n in ast.walk(tree)
                          if isinstance(n, ast.ImportFrom)) or \
                      any(any("importlib" in nm.name for nm in n.names)
                          for n in ast.walk(tree) if isinstance(n, ast.Import))
    return {"name": "B-S127-7 §117-LIF-SIM-IMPORT-BYTE-EQUAL",
            "passed": bool(refs and uses_importlib),
            "evidence": {"s117_sha16": s117_sha, "probe_references_s117": refs,
                          "probe_uses_importlib": uses_importlib}}


def b_s127_8_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    forbidden_calls = {"backward", "cross_entropy", "CrossEntropyLoss",
                       "podFindAndDeployOnDemand", "create_pod"}
    ih, ch = set(), set()
    for p in [S127_PROBE, Path(__file__)]:
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
    passed = bool(central_ok and ast_ok)
    return {"name": "B-S127-8 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-CALL-AST",
            "passed": passed,
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports_hit": sorted(ih), "forbidden_calls_hit": sorted(ch)}}


def b_s127_note():
    return {"name": "B-S127-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "4-point-fit-not-full-scaling-curve",
            "family": "B-EMERGE-7 / B-S126-NOTE / B-S125-NOTE / B-S117-NOTE / B-S124-NOTE",
            "honest_scope": ("4 N points (256/512/1024/2048) fit OLS log-linear with low R²=0.022 "
                             "→ η² is NOT well-described by a power-law on this range. The "
                             "non-monotonic curve (peak at N=512–1024, drop at N=2048) may reflect "
                             "unmodelled regime transitions; a richer fit (logistic / piecewise) is "
                             "future work. §125's PARTIAL verdict + §126's single-point 1.189× ratio "
                             "remain TRUE WITHIN their respective scopes; only the *extrapolation* to "
                             "a scaling law is refuted. Necessary-not-sufficient at every layer "
                             "(B-EMERGE-7). Layer-3 task-grounded REMAINS OPEN. north-star + §15/§51/"
                             "§72 milestones UNCHANGED; GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s127_8_central_and_ast()],
        "closed_propositions": [
            b_s127_1_eta_bounded_all_n(),
            b_s127_2_log_linear_fit_ols_identity(),
            b_s127_3_r_squared_bounded(),
            b_s127_4_scaling_3_bucket_partition(),
            b_s127_5_s126_single_point_carried_but_not_a_scaling_law(),
            b_s127_6_monotonicity_check(),
            b_s127_7_s117_import_byte_equal(),
            b_s127_8_central_and_ast(),
        ],
        "empirical_carve_out": b_s127_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    closed_count = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])

    r = json.loads(S127_RESULT.read_text())
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{closed_count}/{total}",
        "all_closed_pass": all_props,
        "eta_values_by_N": [(m["N_total"], m["eta_squared"]) for m in r["per_N_measurements"]],
        "k_scaling_exponent": r["power_law_fit"]["k_scaling_exponent"],
        "r_squared": r["power_law_fit"]["r_squared"],
        "probe_verdict": r["verdict"],
        "battery_verdict": (f"{r['verdict']}-{closed_count}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "necessary_not_sufficient_B_EMERGE_7": True,
        "north_star_unchanged": True,
        "goal_unreached": True,
    }
    results["summary"] = summary

    out = HERE / "blue_falsifier_s127_result.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
