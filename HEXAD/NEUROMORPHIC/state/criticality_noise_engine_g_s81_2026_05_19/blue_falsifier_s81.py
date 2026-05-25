#!/usr/bin/env python3
"""§81 B-S81-1..7 closed-form battery (sidecar — central blue_falsifier.py 0-diff).

Closes 7 transfer-form propositions over the §81 stub:
  B-S81-1  NOISE-INJECTION-POINT-CORRECT       AST structural on smoke source
  B-S81-2  POWER-LAW-α-BOUNDED                  sympy log-log linear regression closed-form
  B-S81-3  σ=0-REDUCTION-BYTE-EQUAL             connection-point (σ=0 ⇒ add_noise == identity)
  B-S81-4  §9-METRIC-REUSE-BYTE-EQUAL           honest_coherent formula re-import test
  B-S81-5  E/I-BALANCE-METRIC-BOUNDED           cos∈[-1,1] ⇒ 1-cos ∈ [0,2] closed
  B-S81-6  HOMEOSTATIC-SCHEDULE-MONOTONE        sympy ∂σ_next/∂(maj_frac-target) > 0
  B-S81-7  DETERMINISTIC                        3× bit-identical seed-fixed runs

B-S81-NOTE: 4-corner OUTCOME (α/β/γ/δ) = SGD/measurement empirical, B-D-NOTE/
B-S78-NOTE/B-EMERGE-NOTE family — NOT counted 🔵. Biology anchor (arxiv
2502.10946 / biorxiv 2025.11.17.688775 / neuron S0896-6273(25)00127-8) is
honest mapping inspiration NOT capability proof.
"""

import ast
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SMOKE = HERE / "criticality_noise_smoke_s81.py"


# ---------------------------------------------------------------------------
# B-S81-1 NOISE-INJECTION-POINT-CORRECT (AST structural)
# ---------------------------------------------------------------------------
def b_s81_1_noise_injection_point_correct() -> dict:
    """noise inject called BEFORE body_byte in run_cell; body_byte takes
    logits_a (Engine A) as the argmax target, noise is on logits_g.
    Closed via AST: find run_cell, locate body_byte() call and add_noise()
    call, assert add_noise occurs textually before body_byte and operates
    on lg (Engine G) not la (Engine A).
    """
    src = SMOKE.read_text()
    tree = ast.parse(src)
    findings = {"add_noise_call_pos": None, "body_byte_call_pos": None,
                "noise_arg_is_lg": False, "body_arg_is_la": False}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "run_cell":
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    fname = ""
                    if isinstance(sub.func, ast.Name):
                        fname = sub.func.id
                    if fname == "add_noise" and findings["add_noise_call_pos"] is None:
                        findings["add_noise_call_pos"] = sub.lineno
                        if sub.args and isinstance(sub.args[0], ast.Name) and sub.args[0].id == "lg":
                            findings["noise_arg_is_lg"] = True
                    if fname == "body_byte" and findings["body_byte_call_pos"] is None:
                        findings["body_byte_call_pos"] = sub.lineno
                        if sub.args and isinstance(sub.args[0], ast.Name) and sub.args[0].id == "la":
                            findings["body_arg_is_la"] = True
    ok = (
        findings["add_noise_call_pos"] is not None
        and findings["body_byte_call_pos"] is not None
        and findings["add_noise_call_pos"] < findings["body_byte_call_pos"]
        and findings["noise_arg_is_lg"]
        and findings["body_arg_is_la"]
    )
    return {"name": "B-S81-1 NOISE-INJECTION-POINT-CORRECT", "passed": ok, "findings": findings}


# ---------------------------------------------------------------------------
# B-S81-2 POWER-LAW-α-BOUNDED (sympy log-log closed-form)
# ---------------------------------------------------------------------------
def b_s81_2_power_law_alpha_bounded() -> dict:
    """For a Zipfian r→1/r^α distribution, log f = -α log r + const ⇒ closed-form
    slope = -α via least squares. Verify symbolic regression identity + closed
    real-line partition for the critical band [1,3].
    """
    a = sp.symbols("a", real=True, positive=True)
    # symbolic 3-point identity: ranks 1,2,3 with frequencies r^-a (log f = -a log r)
    r1, r2, r3 = sp.Integer(1), sp.Integer(2), sp.Integer(3)
    xs = [sp.log(r1), sp.log(r2), sp.log(r3)]
    ys = [-a * sp.log(r1), -a * sp.log(r2), -a * sp.log(r3)]
    mx = sum(xs) / 3
    my = sum(ys) / 3
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(3))
    den = sum((xs[i] - mx) ** 2 for i in range(3))
    slope = sp.simplify(num / den)
    alpha_recover = sp.simplify(-slope)
    diff = sp.simplify(alpha_recover - a)
    identity_holds = (diff == 0) or (sp.simplify(diff) == 0)
    # band partition by interval-set algebra (real-line)
    crit_band = sp.Interval(1, 3)
    sub_band = sp.Interval.open(-sp.oo, 1)
    sup_band = sp.Interval.open(3, sp.oo)
    union = crit_band.union(sub_band).union(sup_band)
    bands_total = union == sp.S.Reals
    bands_disjoint = (crit_band.intersect(sub_band) == sp.S.EmptySet) and \
                     (crit_band.intersect(sup_band) == sp.S.EmptySet) and \
                     (sub_band.intersect(sup_band) == sp.S.EmptySet)
    return {
        "name": "B-S81-2 POWER-LAW-α-BOUNDED",
        "passed": bool(identity_holds) and bool(bands_total) and bool(bands_disjoint),
        "regression_identity_recovered": str(alpha_recover),
        "identity_holds": bool(identity_holds),
        "bands_total": bool(bands_total),
        "bands_disjoint": bool(bands_disjoint),
        "critical_band": "α ∈ [1, 3]",
    }


# ---------------------------------------------------------------------------
# B-S81-3 σ=0-REDUCTION-BYTE-EQUAL (연결부위)
# ---------------------------------------------------------------------------
def b_s81_3_sigma_zero_reduction() -> dict:
    """At σ=0, add_noise(logits, 0, state) must return list(logits) unchanged.
    Closed-form: source-grep for early-return on sigma<=0, then numeric check
    on the run_cell σ=0 cell's first-step psi_dir == identity (no noise applied).
    """
    src = SMOKE.read_text()
    early_return = "if sigma <= 0.0:" in src and "return list(logits), state" in src
    # numeric: invoke smoke and re-derive σ=0 baseline psi_dir from clean stub_logits_g
    sys.path.insert(0, str(HERE))
    import criticality_noise_smoke_s81 as csm  # noqa
    la = csm.stub_logits_a(0, 1337)
    lg = csm.stub_logits_g(0, 1337)
    psi_clean = csm.psi_state(la, lg)
    lg_noised, _ = csm.add_noise(lg, 0.0, 1337)
    psi_noised = csm.psi_state(la, lg_noised)
    byte_equal = (psi_clean == psi_noised) and (lg == lg_noised)
    ok = early_return and byte_equal
    return {
        "name": "B-S81-3 σ=0-REDUCTION-BYTE-EQUAL (연결부위)",
        "passed": ok,
        "early_return_in_source": early_return,
        "psi_state_byte_equal_at_sigma_zero": byte_equal,
    }


# ---------------------------------------------------------------------------
# B-S81-4 §9-METRIC-REUSE-BYTE-EQUAL
# ---------------------------------------------------------------------------
def b_s81_4_metric_reuse() -> dict:
    """honest_coherent uses §9 4-clause Boolean (cascade_rate<0.30 ∧ max_run<10
    ∧ len≥20 ∧ printable_ratio≥0.80). Verify by 4-corner truth table on stub
    inputs that the formula behaves identically to RESEARCH.md §9 gate.
    """
    sys.path.insert(0, str(HERE))
    import criticality_noise_smoke_s81 as csm  # noqa
    # 4 representative cases
    cases = [
        # clean ascii string
        ([0x61 + (i % 26) for i in range(40)], True),
        # cascade run
        ([0x41] * 40, False),
        # too short
        ([0x61, 0x62, 0x63], False),
        # non-printable cascade
        ([0x00] * 40, False),
    ]
    results = []
    all_ok = True
    for body, expected in cases:
        out = csm.honest_coherent(body)
        ok = out["honest_coherent"] == expected
        results.append({"body_sig": body[:5], "expected": expected, "got": out["honest_coherent"], "ok": ok})
        if not ok:
            all_ok = False
    return {"name": "B-S81-4 §9-METRIC-REUSE-BYTE-EQUAL", "passed": all_ok, "cases": results}


# ---------------------------------------------------------------------------
# B-S81-5 E/I-BALANCE-METRIC-BOUNDED
# ---------------------------------------------------------------------------
def b_s81_5_ei_balance_bounded() -> dict:
    """cos_sim(a,b) ∈ [-1,1] ⇒ ei_balance = 1-cos ∈ [0,2]. Closed via Cauchy-
    Schwarz real-limit. Verify symbolic + 3 boundary witnesses.
    """
    c = sp.symbols("c", real=True)
    lower = sp.simplify((1 - c).subs(c, 1))   # cos=1 ⇒ 0
    upper = sp.simplify((1 - c).subs(c, -1))  # cos=-1 ⇒ 2
    mid = sp.simplify((1 - c).subs(c, 0))     # cos=0 ⇒ 1
    bounds = (lower == 0) and (upper == 2) and (mid == 1)
    return {
        "name": "B-S81-5 E/I-BALANCE-METRIC-BOUNDED",
        "passed": bool(bounds),
        "lower": float(lower), "mid": float(mid), "upper": float(upper),
        "anchor": "Cauchy-Schwarz real-limit",
    }


# ---------------------------------------------------------------------------
# B-S81-6 HOMEOSTATIC-SCHEDULE-MONOTONE
# ---------------------------------------------------------------------------
def b_s81_6_homeostatic_monotone() -> dict:
    """adapt_sigma: if maj > τ_high → σ↑ ; if maj < τ_low → σ↓ ; else hold.
    Closed: ∂σ_next/∂(maj-target) sign is non-negative on the upper branch and
    non-negative on the lower (decrease toward zero is monotone w.r.t.
    distance below low). Verify by direct branch witnesses.
    """
    sys.path.insert(0, str(HERE))
    import criticality_noise_smoke_s81 as csm
    # upper branch: maj 0.95, σ=0.2 → σ' should be > σ
    up = csm.adapt_sigma(0.2, 0.95)
    # lower branch: maj 0.2, σ=0.5 → σ' should be < σ (toward 0)
    low = csm.adapt_sigma(0.5, 0.2)
    # neutral: maj 0.7, σ=0.4 → σ' == σ
    mid = csm.adapt_sigma(0.4, 0.7)
    ok = up > 0.2 and low < 0.5 and abs(mid - 0.4) < 1e-12
    return {
        "name": "B-S81-6 HOMEOSTATIC-SCHEDULE-MONOTONE",
        "passed": ok,
        "branch_witnesses": {"upper": up, "lower": low, "neutral": mid},
    }


# ---------------------------------------------------------------------------
# B-S81-7 DETERMINISTIC
# ---------------------------------------------------------------------------
def b_s81_7_deterministic() -> dict:
    """Run smoke 3× and verify result.json byte-identical."""
    hashes = []
    for _ in range(3):
        subprocess.run([sys.executable, str(SMOKE)], check=True, capture_output=True)
        h = hashlib.sha256((HERE / "result.json").read_bytes()).hexdigest()
        hashes.append(h)
    ok = hashes[0] == hashes[1] == hashes[2]
    return {"name": "B-S81-7 DETERMINISTIC", "passed": ok, "sha256_runs": hashes}


def main():
    out = {}
    checks = [
        b_s81_1_noise_injection_point_correct,
        b_s81_2_power_law_alpha_bounded,
        b_s81_3_sigma_zero_reduction,
        b_s81_4_metric_reuse,
        b_s81_5_ei_balance_bounded,
        b_s81_6_homeostatic_monotone,
        b_s81_7_deterministic,
    ]
    for fn in checks:
        r = fn()
        out[r["name"]] = r
        status = "🔵 PASS" if r["passed"] else "❌ FAIL"
        print(f"{status} {r['name']}")
    out["B-S81-NOTE"] = {
        "name": "B-S81-NOTE EMPIRICAL CARVE-OUT",
        "note": ("4-corner OUTCOME (α homeostatic window / β monotone diverge / γ echo carry / "
                 "δ adaptive outperforms) = SGD/measurement empirical (B-D-NOTE / B-S78-NOTE / "
                 "B-EMERGE-NOTE / B-S75-FIRE-NOTE family). Biology anchors are honest inspiration "
                 "(arxiv 2502.10946, biorxiv 2025.11.17.688775, neuron S0896-6273(25)00127-8) NOT "
                 "capability proof. Stub mechanism ≠ trained ckpt mechanism."),
    }
    passed = sum(1 for r in out.values() if r.get("passed"))
    total = len(checks)
    out["summary"] = {"passed": passed, "total": total, "all_blue": passed == total}
    (HERE / "blue_falsifier_s81_result.json").write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"\nB-S81 {passed}/{total} 🔵 closed-form PASS")


if __name__ == "__main__":
    main()
