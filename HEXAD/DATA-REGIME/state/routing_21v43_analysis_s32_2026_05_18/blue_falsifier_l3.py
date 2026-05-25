#!/usr/bin/env python3
"""B-L3-1..3 — closed-form sidecar battery for RESEARCH.md §32 L3.

SIDECAR — central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is
NOT modified (mirror of B-PRIME / B-DIRI / B-EMERGE / B-S16 sidecar precedent).

  B-L3-1 PARTITION-EXHAUSTIVE-DISJOINT
    SUCCESS u FAIL = 64 anchors, SUCCESS n FAIL = empty, integer cardinality
    21 + 43 = 64 (substring grade) AND 17 + 47 = 64 (genuine grade).
    Boolean set algebra, closed.
  B-L3-2 SEPARATION-METRIC-BOUNDED
    The separation statistics live in closed bounded ranges:
    necessary-condition purity, lift in [0,1]; rank-AUC (folded) in
    [0.5, 1.0]; Cohen's-d sign well-defined. sympy / closed-form bounds.
  B-L3-3 ANALYSIS-DETERMINISTIC
    The analysis is a pure function of eval_result_s16.json + anchor SSOT:
    3x bit-identical re-run, AST forbidden-call grep
    {torch, .backward, F.cross_entropy, random.} == 0 over analyze_21v43.py.

  B-L3-NOTE (empirical carve-out, NOT counted blue)
    Whether the separating feature CAUSES routing success vs correlates
    (the §4 curriculum coupling) needs a controlled ablation fire. The
    analysis establishes correlation; causation is empirical.
    B-D-NOTE / B-S16-NOTE / B-CARVE-E6-NOTE family.

f1/f2/f3 + B-IDENTITY-5 safe: Boolean set algebra / sympy interval bounds /
AST structural grep — NO sigma/tau/phi/J2 external derivation; tier = anima
g2 internal-arch carve-out (Knuth Tier, not a lattice number).

$0 Mac CPU, deterministic. NO model forward, NO training, NO GPU.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ANALYZE = HERE / "analyze_21v43.py"
RESULT = HERE / "analysis_result.json"


def _run_analysis():
    """Import + run analyze_21v43.main(), returning its result dict."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("analyze_21v43", ANALYZE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()


# --------------------------------------------------------------------------
# B-L3-1 PARTITION-EXHAUSTIVE-DISJOINT
# --------------------------------------------------------------------------
def b_l3_1(res) -> dict:
    sub = res["partition"]["substring_grade"]
    gen = res["partition"]["genuine_grade"]
    s_succ = set(sub["success_tiers"])
    s_fail = set(sub["fail_tiers"])
    g_succ = set(gen["success_tiers"])
    g_fail = set(gen["fail_tiers"])

    checks = {
        # substring grade: 21 + 43 = 64, disjoint, union complete
        "substr_disjoint": len(s_succ & s_fail) == 0,
        "substr_card": len(s_succ) == 21 and len(s_fail) == 43,
        "substr_union_64": len(s_succ | s_fail) == 64,
        "substr_int_identity": (len(s_succ) + len(s_fail)) == 64,
        # genuine grade: 17 + 47 = 64, disjoint, union complete
        "genuine_disjoint": len(g_succ & g_fail) == 0,
        "genuine_card": len(g_succ) == 17 and len(g_fail) == 47,
        "genuine_union_64": len(g_succ | g_fail) == 64,
        "genuine_int_identity": (len(g_succ) + len(g_fail)) == 64,
        # genuine success is a subset of substring success (artifacts are
        # exactly substring-success that are not genuine)
        "genuine_subset_substr": g_succ <= s_succ,
        "artifact_count_4": len(s_succ - g_succ) == 4,
    }
    # sympy integer identity witness
    a, b = sp.Integer(21), sp.Integer(43)
    c, d = sp.Integer(17), sp.Integer(47)
    checks["sympy_21_43_eq_64"] = bool(sp.Eq(a + b, sp.Integer(64)))
    checks["sympy_17_47_eq_64"] = bool(sp.Eq(c + d, sp.Integer(64)))
    ok = all(checks.values())
    return {"name": "B-L3-1 PARTITION-EXHAUSTIVE-DISJOINT",
            "pass": ok, "checks": checks}


# --------------------------------------------------------------------------
# B-L3-2 SEPARATION-METRIC-BOUNDED
# --------------------------------------------------------------------------
def b_l3_2(res) -> dict:
    checks = {}
    for grade in ("separation_substring_grade", "separation_genuine_grade"):
        feats = res[grade]["features"]
        for fn, r in feats.items():
            nc = r["necessary_condition"]
            tag = f"{grade[11:14]}:{fn}"
            checks[f"{tag}:purity01"] = 0.0 <= nc["purity"] <= 1.0
            checks[f"{tag}:lift01"] = 0.0 <= nc["lift"] <= 1.0
            checks[f"{tag}:excl01"] = 0.0 <= nc["exclusion"] <= 1.0
            # rank-AUC is folded to [0.5, 1.0]
            checks[f"{tag}:auc_folded"] = 0.5 <= r["rank_auc"] <= 1.0 + 1e-9
            # threshold-separation accuracy is a fraction
            checks[f"{tag}:thracc01"] = (
                0.0 <= r["threshold_separation_acc"] <= 1.0)
            # lift <= exclusion at purity 1.0 by construction
            # (lift is exclusion gated on purity==1)
            checks[f"{tag}:lift_le_excl"] = nc["lift"] <= nc["exclusion"] + 1e-9
            # Cohen's d is a finite real (sign well-defined)
            checks[f"{tag}:d_finite"] = isinstance(r["cohens_d"], (int, float))

    # sympy closed-form: necessary-condition lift = |fail excluded| / |fail|
    # is provably in [0,1] since 0 <= excluded <= |fail|.
    n_fail, n_excl = sp.symbols("n_fail n_excl", positive=True)
    lift_expr = n_excl / n_fail
    # bound: with 0 <= n_excl <= n_fail, lift_expr in [0,1]
    checks["sympy_lift_lower_0"] = bool(
        sp.simplify(lift_expr.subs(n_excl, 0)) == 0)
    checks["sympy_lift_upper_1"] = bool(
        sp.simplify(lift_expr.subs(n_excl, n_fail)) == 1)

    # the verdict's top feature lift is reported and bounded
    v = res["verdict"]["necessary_condition"]
    checks["verdict_lift_bounded"] = 0.0 <= v["lift"] <= 1.0
    checks["verdict_purity_bounded"] = 0.0 <= v["purity"] <= 1.0

    ok = all(checks.values())
    return {"name": "B-L3-2 SEPARATION-METRIC-BOUNDED",
            "pass": ok, "n_checks": len(checks),
            "all_bounded": ok}


# --------------------------------------------------------------------------
# B-L3-3 ANALYSIS-DETERMINISTIC
# --------------------------------------------------------------------------
FORBIDDEN_TOKENS = ("torch", "tensorflow", "jax")
FORBIDDEN_ATTR = (".backward", ".grad")
FORBIDDEN_CALLS = ("cross_entropy", "CrossEntropyLoss")
FORBIDDEN_RANDOM = ("random",)  # stdlib random / numpy.random — non-determinism


def _ast_forbidden_grep(src_path: Path) -> dict:
    """AST-level scan: no model-forward / training / unseeded-RNG calls.
    Walks Call / Attribute / Import nodes — comments and docstrings excluded
    by construction (ast drops them)."""
    tree = ast.parse(src_path.read_text())
    hits = {"torch_or_dl": [], "backward_grad": [],
            "cross_entropy": [], "random_rng": []}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = (node.module or "") if isinstance(node, ast.ImportFrom) else ""
            names = [a.name for a in node.names]
            for nm in [mod] + names:
                low = (nm or "").lower()
                if any(t in low.split(".") for t in FORBIDDEN_TOKENS):
                    hits["torch_or_dl"].append(nm)
                if any(low == r or low.endswith("." + r)
                       for r in FORBIDDEN_RANDOM):
                    hits["random_rng"].append(nm)
        if isinstance(node, ast.Attribute):
            if node.attr in ("backward", "grad"):
                hits["backward_grad"].append(node.attr)
        if isinstance(node, ast.Call):
            f = node.func
            name = None
            if isinstance(f, ast.Attribute):
                name = f.attr
            elif isinstance(f, ast.Name):
                name = f.id
            if name in FORBIDDEN_CALLS:
                hits["cross_entropy"].append(name)
            # bare random.* calls (random.random, random.shuffle, ...)
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id == "random":
                    hits["random_rng"].append(f"random.{f.attr}")
    return hits


def b_l3_3(res) -> dict:
    checks = {}
    # (1) AST forbidden-call grep == 0 on the analysis script
    hits = _ast_forbidden_grep(ANALYZE)
    checks["no_torch_dl"] = len(hits["torch_or_dl"]) == 0
    checks["no_backward_grad"] = len(hits["backward_grad"]) == 0
    checks["no_cross_entropy"] = len(hits["cross_entropy"]) == 0
    checks["no_rng"] = len(hits["random_rng"]) == 0

    # (2) 3x bit-identical re-run: serialise result, hash, compare.
    def _hash(d):
        return hashlib.sha256(
            json.dumps(d, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
    h1 = _hash(_run_analysis())
    h2 = _hash(_run_analysis())
    h3 = _hash(_run_analysis())
    checks["rerun_bit_identical"] = (h1 == h2 == h3)
    checks["matches_committed_result"] = (h1 == _hash(res))

    ok = all(checks.values())
    return {"name": "B-L3-3 ANALYSIS-DETERMINISTIC",
            "pass": ok, "checks": checks,
            "forbidden_hits": hits, "rerun_sha256": h1}


def main():
    # run the committed analysis once for B-L3-1/2; B-L3-3 re-runs internally
    res = json.loads(RESULT.read_text()) if RESULT.exists() else _run_analysis()
    if not RESULT.exists():
        _run_analysis()
        res = json.loads(RESULT.read_text())

    b1 = b_l3_1(res)
    b2 = b_l3_2(res)
    b3 = b_l3_3(res)
    battery = [b1, b2, b3]
    n_pass = sum(1 for b in battery if b["pass"])
    all_blue = n_pass == 3

    note = {
        "name": "B-L3-NOTE CAUSATION-EMPIRICAL",
        "counted_blue": False,
        "text": "Whether the separating feature (tier >= 77) CAUSES §16 "
                "routing success, vs correlates via the §16 curriculum "
                "coupling (curriculum_rank weights tier/303 at 0.30) or an "
                "unmeasured cause, needs a controlled ablation fire. The "
                "analysis establishes CORRELATION; causation is empirical. "
                "B-D-NOTE / B-S16-NOTE / B-CARVE-E6-NOTE family — NOT "
                "counted blue.",
    }

    out = {
        "battery": "B-L3-1..3 — RESEARCH.md §32 L3 routing 21-vs-43 analysis",
        "sidecar": True,
        "central_blue_falsifier_modified": False,
        "results": battery,
        "note": note,
        "n_pass": n_pass,
        "n_total": 3,
        "all_blue": all_blue,
        "summary": f"B-L3 {n_pass}/3 "
                   + ("\U0001f535" if all_blue else "FAIL"),
    }
    (HERE / "blue_falsifier_l3_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    for b in battery:
        mark = "\U0001f535 PASS" if b["pass"] else "❌ FAIL"
        print(f"  {b['name']:<42} {mark}")
    print(f"  {note['name']:<42} (empirical carve-out, NOT counted)")
    print(f"\n{out['summary']}")
    if not all_blue:
        raise SystemExit(1)
    return out


if __name__ == "__main__":
    main()
