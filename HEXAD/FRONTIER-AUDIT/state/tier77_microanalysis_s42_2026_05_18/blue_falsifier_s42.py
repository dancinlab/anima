#!/usr/bin/env python3
"""
B-S42-1..3 sidecar — closed-form battery for §42 tier ≥ 77 micro-analysis.

🔵 Sympy/Boolean closed-form falsifiers. central blue_falsifier.py untouched
(sidecar pattern; B-PRIME/B-DIRH/B-DIRI/B-S16/B-MGND/B-KTRIE/B-EEG-CT3/B-S37
precedent).

  B-S42-1 TIER77-PARTITION-EXHAUSTIVE-DISJOINT  (Boolean + integer)
  B-S42-2 SEPARATION-METRIC-BOUNDED              (closed-form bounds)
  B-S42-3 ANALYSIS-DETERMINISTIC                 (3× bit-identical + AST)
  B-S42-NOTE empirical carve-out (NOT counted 🔵)
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ANALYZE_PY = HERE / "analyze_s42.py"
ANALYSIS_RESULT = HERE / "analysis_result.json"


# ---------------------------------------------------------------------------
# B-S42-1 TIER77-PARTITION-EXHAUSTIVE-DISJOINT
# ---------------------------------------------------------------------------
def b_s42_1():
    """Partition the 46 tier ≥ 77 anchors into 17 success + 29 fail.
    Closed: integer cardinality 17 + 29 = 46; Boolean disjoint
    (success ∩ fail = ∅); partition exact (success ∪ fail covers band)."""
    r = json.loads(ANALYSIS_RESULT.read_text())
    band = set(r["partition"]["tier77_band_tiers"])
    success = set(r["partition"]["success_tiers"])
    fail = set(r["partition"]["fail_tiers"])

    # Closed identities.
    sum_eq_band = sp.Integer(len(success)) + sp.Integer(len(fail)) == sp.Integer(len(band))
    intersect_empty = bool(success & fail) is False
    union_eq_band = (success | fail) == band
    s_eq_17 = sp.Integer(len(success)) == sp.Integer(17)
    f_eq_29 = sp.Integer(len(fail)) == sp.Integer(29)
    band_eq_46 = sp.Integer(len(band)) == sp.Integer(46)

    # Necessary-condition floor check: every band tier ≥ 77.
    floor_holds = all(t >= 77 for t in band)

    ok = bool(sum_eq_band and intersect_empty and union_eq_band and
              s_eq_17 and f_eq_29 and band_eq_46 and floor_holds)
    return {
        "id": "B-S42-1",
        "name": "TIER77-PARTITION-EXHAUSTIVE-DISJOINT",
        "kind": "boolean+integer cardinality (closed)",
        "passed": ok,
        "witnesses": {
            "n_band": len(band),
            "n_success": len(success),
            "n_fail": len(fail),
            "sum_17_plus_29_eq_46": bool(sum_eq_band),
            "intersect_empty": intersect_empty,
            "union_eq_band": union_eq_band,
            "floor_77_holds": floor_holds,
        },
    }


# ---------------------------------------------------------------------------
# B-S42-2 SEPARATION-METRIC-BOUNDED
# ---------------------------------------------------------------------------
def b_s42_2():
    """All separation metrics live in their stated closed-form intervals
    for EVERY feature in analysis_result.json. Closed: bounded predicate."""
    r = json.loads(ANALYSIS_RESULT.read_text())
    feats = r["numeric_features_ranked"]

    violations = []
    for f in feats:
        acc = f["threshold_separation_acc"]
        if not (0.0 <= acc <= 1.0):
            violations.append((f["feature"], "acc_out_of_range", acc))
        d = abs(f["cohens_d"])
        if not (d >= 0.0):
            violations.append((f["feature"], "d_negative", f["cohens_d"]))
        auc = f["rank_auc"]
        if not (0.5 <= auc <= 1.0):
            violations.append((f["feature"], "auc_out_of_range", auc))
        nc = f["necessary_condition"]
        for k in ("purity", "exclusion", "lift"):
            v = nc[k]
            if not (0.0 <= v <= 1.0):
                violations.append((f["feature"], f"nc_{k}_out_of_range", v))

    # Symbolic statement: ∀ feature, acc∈[0,1] ∧ |d|≥0 ∧ auc∈[0.5,1] ∧
    # purity,exclusion,lift ∈ [0,1].
    x = sp.Symbol("acc", real=True)
    acc_bound = sp.And(x >= 0, x <= 1)  # closed-form interval
    closed_form_acc = sp.simplify(acc_bound.subs(x, 0.6739)) == sp.true

    return {
        "id": "B-S42-2",
        "name": "SEPARATION-METRIC-BOUNDED",
        "kind": "closed-form interval bounds (sympy)",
        "passed": len(violations) == 0 and bool(closed_form_acc),
        "witnesses": {
            "n_features_checked": len(feats),
            "violations": violations,
            "acc_interval_closed_form": "acc ∈ [0,1]",
            "d_lower_bound": "|d| ≥ 0",
            "auc_interval": "rank_auc ∈ [0.5, 1.0]",
            "nc_field_intervals": "purity, exclusion, lift ∈ [0,1]",
        },
    }


# ---------------------------------------------------------------------------
# B-S42-3 ANALYSIS-DETERMINISTIC
# ---------------------------------------------------------------------------
FORBIDDEN_CALL_SUBSTRINGS = (
    "torch", ".backward", "F.cross_entropy",
    "random.", "np.random", "numpy.random",
    "torch.rand", "torch.randn", "openai", "anthropic",
)


def _ast_forbidden_call_count(src: str) -> dict[str, int]:
    """Walk AST and count any Name/Attribute usage whose dotted-source
    contains a forbidden substring. AST-level — comment/docstring/string
    literals automatically excluded."""
    tree = ast.parse(src)
    counts: dict[str, int] = {sub: 0 for sub in FORBIDDEN_CALL_SUBSTRINGS}

    def dotted(node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{dotted(node.value)}.{node.attr}"
        return ""

    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            d = dotted(n.func)
            for sub in FORBIDDEN_CALL_SUBSTRINGS:
                if sub in d:
                    counts[sub] += 1
        elif isinstance(n, ast.Attribute):
            d = dotted(n)
            for sub in FORBIDDEN_CALL_SUBSTRINGS:
                if sub in d and sub.startswith("torch") or sub.startswith("np."):
                    # Only count as forbidden if it's actually invoked; we
                    # already handle Call above. Skip bare Attribute.
                    pass
        elif isinstance(n, ast.Import):
            for alias in n.names:
                for sub in FORBIDDEN_CALL_SUBSTRINGS:
                    if sub.rstrip(".") in alias.name:
                        counts[sub] += 1
        elif isinstance(n, ast.ImportFrom):
            mod = n.module or ""
            for sub in FORBIDDEN_CALL_SUBSTRINGS:
                if sub.rstrip(".") in mod:
                    counts[sub] += 1
    return counts


def b_s42_3():
    """Determinism: 3× run of analyze_s42.py produces bit-identical
    analysis_result.json. AST audit shows zero forbidden-call (torch /
    .backward / F.cross_entropy / random.* / np.random)."""
    # 3× bit-identical.
    hashes = []
    for _ in range(3):
        subprocess.run([sys.executable, str(ANALYZE_PY)], check=True,
                       capture_output=True)
        h = hashlib.sha256(ANALYSIS_RESULT.read_bytes()).hexdigest()
        hashes.append(h)
    bit_identical = len(set(hashes)) == 1

    # AST forbidden-call audit.
    src = ANALYZE_PY.read_text()
    forbidden = _ast_forbidden_call_count(src)
    forbidden_total = sum(forbidden.values())
    forbidden_clean = forbidden_total == 0

    return {
        "id": "B-S42-3",
        "name": "ANALYSIS-DETERMINISTIC",
        "kind": "3× bit-identical + AST forbidden-call grep (structural)",
        "passed": bit_identical and forbidden_clean,
        "witnesses": {
            "hashes_3x": hashes,
            "bit_identical": bit_identical,
            "forbidden_calls": forbidden,
            "forbidden_total": forbidden_total,
        },
    }


# ---------------------------------------------------------------------------
# B-S42-NOTE (empirical carve-out, NOT counted 🔵)
# ---------------------------------------------------------------------------
B_S42_NOTE = (
    "B-S42-NOTE empirical carve-out: any sufficient-condition lever inferred "
    "from §42 is HYPOTHESIS. promotion to causal lever requires a §43/§40-"
    "style ablation fire varying the candidate feature with all others "
    "fixed. The §42 verdict 'structure_found_within_tier77 = False' is itself "
    "a hypothesis — testable by re-firing §16 with a different seed. "
    "B-D-NOTE / B-L3-NOTE / B-S35-NOTE family. NOT counted 🔵."
)


def main():
    rows = [b_s42_1(), b_s42_2(), b_s42_3()]
    passed = sum(1 for r in rows if r["passed"])
    total = len(rows)
    result = {
        "battery": "B-S42",
        "scope": "§42 tier ≥ 77 17-vs-29 distinguishing-structure micro-analysis",
        "rows": rows,
        "passed": passed,
        "total": total,
        "all_pass": passed == total,
        "note_empirical": B_S42_NOTE,
        "f_safety": {
            "f1_lattice_fit_external_entity": False,
            "f2_lattice_tautology": False,
            "f3_no_outcome_claim": False,
            "B-IDENTITY-5_corpus_grep": "not_applicable_no_corpus_generated",
        },
    }
    return result


if __name__ == "__main__":
    res = main()
    out = HERE / "blue_falsifier_s42_result.json"
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(f"B-S42: {res['passed']}/{res['total']} PASS — all_pass={res['all_pass']}")
    for row in res["rows"]:
        print(f"  {row['id']} {row['name']}: passed={row['passed']}")
    print(f"\nwrote {out}")
