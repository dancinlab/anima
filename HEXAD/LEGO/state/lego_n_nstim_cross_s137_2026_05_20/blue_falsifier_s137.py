#!/usr/bin/env python3
"""§137 (N,n_stim) CROSS-MATRIX battery — 5 closed-form propositions + 1 NOTE."""

import ast
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
CENTRAL_BLUE = ANIMA / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
S137_RESULT = HERE / "result.json"
S137_PROBE = HERE / "probe_cross.py"


def sha16(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def b_s137_1_eta_bounded():
    r = json.loads(S137_RESULT.read_text())
    etas = [c["eta_squared"] for c in r["cells"]]
    all_in = all(0 <= v <= 1 for v in etas)
    return {"name": "B-S137-1 ETA-BOUNDED-ALL-6-CELLS",
            "passed": bool(all_in and len(etas) == 6),
            "evidence": {"eta_values": etas, "cell_count": len(etas),
                          "all_in_unit_interval": all_in}}


def b_s137_2_peak_n_stim_invariant():
    r = json.loads(S137_RESULT.read_text())
    peak_by_N = r["peak_by_N"]
    peaks = [peak_by_N[N]["peak_n_stim"] for N in peak_by_N]
    invariant = (len(set(peaks)) == 1)
    return {"name": "B-S137-2 PEAK-N-STIM-INVARIANT-CLOSED",
            "passed": bool(invariant and r["verdict"] == "PEAK-N-STIM-N-INVARIANT"),
            "evidence": {"peak_n_stim_per_N": peaks, "invariant": invariant,
                          "recorded_verdict": r["verdict"]}}


def b_s137_3_nstim_gradient_steepens():
    """The n_stim range ratio (η²_max/η²_min over n_stim) is LARGER at N=1024
    than at N=256 — closed real-number inequality."""
    r = json.loads(S137_RESULT.read_text())
    cells = r["cells"]
    def range_ratio_at_N(N):
        N_etas = [c["eta_squared"] for c in cells if c["N"] == N]
        return max(N_etas) / min(N_etas)
    ratio_256 = range_ratio_at_N(256)
    ratio_1024 = range_ratio_at_N(1024)
    steepens = ratio_1024 > ratio_256
    return {"name": "B-S137-3 NSTIM-GRADIENT-STEEPENS-WITH-N-CLOSED",
            "passed": bool(steepens),
            "evidence": {"range_ratio_N256": ratio_256, "range_ratio_N1024": ratio_1024,
                          "gradient_steepens_with_N": steepens}}


def b_s137_4_engine_canonical():
    src = S137_PROBE.read_text()
    tree = ast.parse(src)
    imports_lego_engine = any(
        (isinstance(n, ast.Import) and any(nm.name == "lego_engine" for nm in n.names))
        or (isinstance(n, ast.ImportFrom) and n.module == "lego_engine")
        for n in ast.walk(tree))
    return {"name": "B-S137-4 ENGINE-CANONICAL-POST-S134",
            "passed": bool(imports_lego_engine),
            "evidence": {"imports_canonical_lego_engine": imports_lego_engine}}


def b_s137_5_central_and_ast():
    prefix = sha16(CENTRAL_BLUE)
    central_ok = (prefix == "c93e160a8a376a94")
    forbidden_imports = {"torch", "runpod", "vastai", "anthropic", "openai"}
    forbidden_calls = {"backward", "cross_entropy", "CrossEntropyLoss",
                       "podFindAndDeployOnDemand", "create_pod"}
    ih, ch = set(), set()
    for p in [S137_PROBE, Path(__file__)]:
        tree = ast.parse(p.read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for nm in n.names:
                    if nm.name.split(".")[0] in forbidden_imports: ih.add(nm.name)
            elif isinstance(n, ast.ImportFrom):
                if n.module and n.module.split(".")[0] in forbidden_imports: ih.add(n.module)
            elif isinstance(n, ast.Call):
                if isinstance(n.func, ast.Attribute) and n.func.attr in forbidden_calls:
                    ch.add(n.func.attr)
                elif isinstance(n.func, ast.Name) and n.func.id in forbidden_calls:
                    ch.add(n.func.id)
    return {"name": "B-S137-5 CENTRAL-0-DIFF-AND-NO-FORBIDDEN-CALL-AST",
            "passed": bool(central_ok and len(ih) == 0 and len(ch) == 0),
            "evidence": {"central_sha16": prefix, "central_match": central_ok,
                          "forbidden_imports": sorted(ih), "forbidden_calls": sorted(ch)}}


def b_s137_note():
    return {"name": "B-S137-NOTE EMPIRICAL-CARVE-OUT (NOT counted 🔵)",
            "carve_out_kind": "2x3-grid-M3-not-full-surface",
            "family": "B-EMERGE-7 / B-S127-NOTE / B-S131-NOTE / B-S135-NOTE",
            "honest_scope": ("§137 measured a 2×3 (N, n_stim) cross-matrix at M=3 "
                             "(reduced from §125–§135's M=5 for speed — wider SE). "
                             "Peak n_stim=4 invariant at both N; n_stim-gradient "
                             "steepens 1.05×→2.39× from N=256→N=1024 = N and n_stim "
                             "interact, not separable axes. A full (N, n_stim) surface "
                             "would need a 4×5 grid (not pursued, diminishing ROI). "
                             "Qualitative verdict robust to M; exact η² has wider CI. "
                             "GOAL-orthogonal layer-2 geometry; necessary-not-sufficient "
                             "(B-EMERGE-7); GOAL 미도달.")}


def main():
    results = {
        "preconditions": [b_s137_5_central_and_ast()],
        "closed_propositions": [
            b_s137_1_eta_bounded(),
            b_s137_2_peak_n_stim_invariant(),
            b_s137_3_nstim_gradient_steepens(),
            b_s137_4_engine_canonical(),
            b_s137_5_central_and_ast(),
        ],
        "empirical_carve_out": b_s137_note(),
    }
    all_pre = all(p["passed"] for p in results["preconditions"])
    all_props = all(p["passed"] for p in results["closed_propositions"])
    cc = sum(1 for p in results["closed_propositions"] if p["passed"])
    total = len(results["closed_propositions"])
    summary = {
        "preconditions_passed": all_pre,
        "closed_propositions_passed": f"{cc}/{total}",
        "all_closed_pass": all_props,
        "battery_verdict": (f"PEAK-N-STIM-N-INVARIANT-{cc}-{total}-🔵"
                            if (all_pre and all_props) else "BATTERY-INCOMPLETE"),
        "empirical_carve_out_NOT_counted_🔵": True,
        "north_star_unchanged": True, "goal_unreached": True,
    }
    results["summary"] = summary
    (HERE / "blue_falsifier_s137_result.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    sys.exit(0 if (all_pre and all_props) else 1)


if __name__ == "__main__":
    main()
