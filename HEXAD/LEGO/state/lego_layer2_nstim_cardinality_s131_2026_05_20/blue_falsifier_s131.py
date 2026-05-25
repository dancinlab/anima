#!/usr/bin/env python3
"""§131 STIMULUS-CARDINALITY battery — 7 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
CANONICAL_ENGINE = ANIMA / "HEXAD" / "LEGO" / "lego_engine.py"
S131_RESULT = HERE / "result.json"
S131_PROBE = HERE / "probe_nstim.py"


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s131_1_eta_bounded():
    r = json.loads(S131_RESULT.read_text())
    all_in = all(0.0 <= m["eta_squared"] <= 1.0 for m in r["per_nstim_measurements"])
    return {"name": "B-S131-1 ETA-BOUNDED-ALL-NSTIM-POINTS",
            "passed": bool(all_in),
            "evidence": {"eta_values": [m["eta_squared"] for m in r["per_nstim_measurements"]],
                          "all_in_unit_interval": all_in}}


def b_s131_2_range_ratio_3_bucket_partition():
    """3-bucket classification {STRONGLY / MILDLY / INVARIANT} over ratio η²_max/η²_min ∈ (0,∞).
    Partition (by first-satisfied):
      ratio > 1.50            → STRONGLY-NSTIM-DEPENDENT
      1.10 ≤ ratio ≤ 1.50      → MILDLY-NSTIM-DEPENDENT
      ratio < 1.10            → NSTIM-INVARIANT
    """
    r = sp.Symbol("r", positive=True)
    intervals = {
        "STRONGLY": sp.Interval.open(sp.Rational(3, 2), sp.oo),
        "MILDLY": sp.Interval(sp.Rational(11, 10), sp.Rational(3, 2)),
        "INVARIANT": sp.Interval.Lopen(0, sp.Rational(11, 10)),
    }
    union = sp.Union(*intervals.values())
    exhaustive = union == sp.Interval.open(0, sp.oo)
    pairs = list(intervals.items())
    disjoint = True
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[i][1].intersect(pairs[j][1]).measure != 0:
                disjoint = False
    result = json.loads(S131_RESULT.read_text())
    ratio = result["eta_range_ratio"]
    if ratio > 1.50:
        reclass = "STRONGLY-NSTIM-DEPENDENT"
    elif 1.10 <= ratio <= 1.50:
        reclass = "MILDLY-NSTIM-DEPENDENT"
    else:
        reclass = "NSTIM-INVARIANT"
    matches = (result["verdict"] == reclass)
    passed = bool(exhaustive and disjoint and matches)
    return {"name": "B-S131-2 RANGE-RATIO-3-BUCKET-CLOSED-PARTITION",
            "passed": passed,
            "evidence": {"exhaustive": exhaustive, "disjoint": disjoint,
                          "ratio": ratio, "reclass": reclass,
                          "recorded": result["verdict"], "match": matches}}


def b_s131_3_ss_decomposition_all_nstim():
    """ANOVA identity SS_total = SS_between + SS_within holds at every n_stim point."""
    r = json.loads(S131_RESULT.read_text())
    all_hold = True
    diagnostics = []
    for m in r["per_nstim_measurements"]:
        ssb, ssw, sst = m["ss_between"], m["ss_within"], m["ss_total"]
        identity = abs((ssb + ssw) - sst) < 1e-6 * max(abs(sst), 1.0)
        diagnostics.append({"n_stim": m["n_stim"], "identity_holds": identity})
        if not identity:
            all_hold = False
    return {"name": "B-S131-3 SS-DECOMPOSITION-IDENTITY-CLOSED-ALL-NSTIM",
            "passed": bool(all_hold),
            "evidence": {"per_nstim_anova_identity": diagnostics, "all_hold": all_hold}}


def b_s131_4_engine_is_canonical_lego_lib():
    """§131 uses the post-§129 canonical engine SSOT at HEXAD/LEGO/lego_engine.py
    (NOT importlib of state/s117/lego_sim.py). AST: `import lego_engine` present
    AND `importlib` NOT used in §131 probe."""
    src = S131_PROBE.read_text()
    tree = ast.parse(src)
    imports = set()
    importlib_used = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for nm in n.names:
                imports.add(nm.name.split(".")[0].lower())
                if "importlib" in nm.name:
                    importlib_used = True
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                imports.add(n.module.split(".")[0].lower())
                if "importlib" in n.module:
                    importlib_used = True
    canonical_imported = "lego_engine" in imports
    canonical_lib_exists = CANONICAL_ENGINE.exists()
    canonical_sha = sha16(CANONICAL_ENGINE) if canonical_lib_exists else None
    passed = canonical_imported and (not importlib_used) and canonical_lib_exists
    return {"name": "B-S131-4 ENGINE-IS-CANONICAL-LEGO-LIB-POST-§129",
            "passed": bool(passed),
            "evidence": {"canonical_engine_imported": canonical_imported,
                          "importlib_NOT_used": not importlib_used,
                          "canonical_engine_exists": canonical_lib_exists,
                          "canonical_engine_sha16": canonical_sha}}


def b_s131_5_axis_orthogonality():
    """N held fixed at 256 (n_a=96, n_g=96, n_rec=64) across all n_stim points —
    measurement axis orthogonal to §125/§126/§127 N axis. Structural Boolean."""
    r = json.loads(S131_RESULT.read_text())
    m = r["method"]
    N_fixed = (m["N_total_fixed"] == 256) and (m["n_a"] == 96) and (m["n_g"] == 96) and (m["n_rec"] == 64)
    nstim_varies = (len(set(m["nstim_points"])) == len(m["nstim_points"]))
    passed = N_fixed and nstim_varies
    return {"name": "B-S131-5 N-FIXED-NSTIM-VARIES-ORTHOGONALITY-CLOSED",
            "passed": bool(passed),
            "evidence": {"N_total_fixed_256": N_fixed,
                          "nstim_points": m["nstim_points"], "nstim_varies": nstim_varies}}


def b_s131_6_peak_at_low_nstim():
    """§131 measures η² peak at the LOWEST n_stim point (n_stim=4). closed Boolean."""
    r = json.loads(S131_RESULT.read_text())
    peak = r["peak_n_stim"]
    min_nstim = min(r["method"]["nstim_points"])
    return {"name": "B-S131-6 ETA-PEAK-AT-MIN-NSTIM-MEASURED",
            "passed": bool(peak == min_nstim),
            "evidence": {"peak_n_stim": peak, "min_n_stim_in_range": min_nstim,
                          "peak_at_min": peak == min_nstim}}


def b_s131_7_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    forbidden_calls = {"backward", "cross_entropy", "CrossEntropyLoss",
                       "podFindAndDeployOnDemand", "create_pod"}
    ih, ch = set(), set()
    for p in [S131_PROBE, Path(__file__), CANONICAL_ENGINE]:
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
    return {"name": "B-S131-7 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-CALL-AST",
            "passed": bool(central_ok and ast_ok),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports_hit": sorted(ih),
                          "forbidden_calls_hit": sorted(ch)}}


def b_s131_note():
    return {"name": "B-S131-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "4-cardinality-point-measurement",
            "family": "B-EMERGE-7 / B-S125-NOTE / B-S126-NOTE / B-S127-NOTE / B-S124-NOTE",
            "honest_scope": ("η² peak at n_stim=4 OUTCOME is measured on §117's specific "
                             "LIF parametrisation (N=256). 4 n_stim points (4/12/24/48) — "
                             "fewer than would be needed to fit a continuous η²(n_stim) "
                             "curve; geometric step ×~2 spans 12× cardinality range. The "
                             "η² range ratio 2.199× is the measured magnitude of n_stim "
                             "modulation at this parametrisation; whether the peak shifts "
                             "or shape changes at different N values is unanswered. "
                             "Necessary-not-sufficient (B-EMERGE-7); GOAL 미도달; "
                             "north-star + §15/§51/§72 milestones UNCHANGED.")}


def main():
    results = {
        "preconditions": [b_s131_7_central_and_ast()],
        "closed_propositions": [
            b_s131_1_eta_bounded(),
            b_s131_2_range_ratio_3_bucket_partition(),
            b_s131_3_ss_decomposition_all_nstim(),
            b_s131_4_engine_is_canonical_lego_lib(),
            b_s131_5_axis_orthogonality(),
            b_s131_6_peak_at_low_nstim(),
            b_s131_7_central_and_ast(),
        ],
        "empirical_carve_out": b_s131_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    closed_count = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])

    r = json.loads(S131_RESULT.read_text())
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{closed_count}/{total}",
        "all_closed_pass": all_props,
        "eta_values_by_nstim": [(m["n_stim"], m["eta_squared"]) for m in r["per_nstim_measurements"]],
        "eta_range_ratio": r["eta_range_ratio"],
        "peak_n_stim": r["peak_n_stim"],
        "probe_verdict": r["verdict"],
        "battery_verdict": (f"{r['verdict']}-{closed_count}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "necessary_not_sufficient_B_EMERGE_7": True,
        "north_star_unchanged": True,
        "goal_unreached": True,
    }
    results["summary"] = summary

    out = HERE / "blue_falsifier_s131_result.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
