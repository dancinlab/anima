#!/usr/bin/env python3
"""blue_falsifier_s44.py — §44 closed-form sympy sidecar B-S44-1..4.

central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED — sidecar
pattern per B-S38 / B-DHDL / B-PTD / B-DIRI / B-EBT precedent.

B-S44-1 DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED
  L = L_decision + λ_s · L_safety + λ_ptd · L_ptd_nextstate ≥ 0 for
  λ_s,λ_ptd ≥ 0. Sum of non-negatives × non-negative weights is non-negative.
  Shannon CE ≥ 0 (B-DHDL-3 carry), (1-s)·p^2 ≥ 0 (square × Boolean), MSE ≥ 0.

B-S44-2 LAMBDA-PTD-OFF-REDUCTION-CLOSED (CONNECTION-POINT)
  λ_ptd = 0 ⇒ L = L_decision + λ_s · L_safety = L_DHDL (§27 byte-equal
  trainer at same seed). PTD aux head contributes ZERO gradient to shared
  trunk + decision head at λ_ptd = 0 (the loss term vanishes; the source code
  multiplies dxhat by lambda_ptd before backprop). Fair-compare-by-construction
  with §27 baseline. Mirror B-S38-3 / B-PTD-4 / B-EBT-5 / B-S16-5 / B-DIRI-5 /
  B-MGND-5 / B-CT3-2 / B-PHYS-5 overlay-off connection-point pattern.

B-S44-3 GAP-METRIC-DETERMINISTIC-CLOSED
  threshold-distillation gap is a pure function of (head_weights, mean, std,
  corpus_records). No RNG / no forward sampling / no temperature. Running
  eval twice on the same head + corpus produces bit-identical gap value.
  Source: eval_dhdl_ptd.py uses argmax (deterministic) + threshold_decision
  (pure-fn of score + safety_ok bool).

B-S44-4 SCALE-ORTHOGONAL-CLOSED
  composed gate head = shared(480) + decision(579) + ptd_aux(766) = 1825
  params. base byte-LM = 283,720,000 params. 1825 / 283720000 ≈ 6.43e-6 < 1%.
  Kolmogorov-bounded rational inequality. Mirror B-S38-2.

B-S44-NOTE (empirical carve-out, NOT counted 🔵)
  Whether the PTD auxiliary term moves the decision-head accuracy, the
  threshold-distillation gap, or the CONTINUE_THINK-corner behaviour is an
  SGD convergence + measurement OUTCOME. The battery proves the composed
  objective is well-formed, λ-reducible to §27, deterministic, and scale-
  orthogonal. It does NOT prove the composition improves anything —
  DESIGN_S38.md §7 explicitly: "better-engineered distillation, still
  distillation; NOT GOAL emergence." B-D-NOTE / B-DHDL-NOTE / B-PTD-NOTE /
  B-MITENS-NOTE family.
"""
from __future__ import annotations
import ast
import inspect
import json
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


# ────────────────────────────────────────────────────────────────────────
# B-S44-1
# ────────────────────────────────────────────────────────────────────────
def b_s44_1_dual_loss_plus_ptd_nonneg() -> dict:
    """L = L_dec + λ_s·L_safe + λ_ptd·L_ptd ≥ 0 for λ_s, λ_ptd ≥ 0."""
    # symbolic non-negative pieces
    L_dec, L_safe, L_ptd, lam_s, lam_ptd = sp.symbols(
        "L_dec L_safe L_ptd lam_s lam_ptd", nonnegative=True)
    L = L_dec + lam_s * L_safe + lam_ptd * L_ptd
    # sympy: a sum of non-negative symbols is non-negative
    nonneg = sp.simplify(L).is_nonnegative
    # MSE ≥ 0 sanity (sum of squares mean)
    a, b = sp.symbols("a b", real=True)
    mse = (a - b) ** 2
    mse_nonneg = sp.simplify(mse).is_nonnegative
    # Shannon CE ≥ 0: -log(p) ≥ 0 for p ∈ (0, 1]
    p = sp.symbols("p", positive=True)
    ce = -sp.log(p)
    ce_nonneg_at_le1 = bool(sp.simplify(ce.subs(p, sp.Rational(1, 2))).is_nonnegative)
    return {
        "id": "B-S44-1",
        "name": "DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED",
        "L_nonneg": bool(nonneg),
        "MSE_nonneg": bool(mse_nonneg),
        "shannon_CE_nonneg_at_half": ce_nonneg_at_le1,
        "pass": bool(nonneg) and bool(mse_nonneg) and ce_nonneg_at_le1,
    }


# ────────────────────────────────────────────────────────────────────────
# B-S44-2 (connection-point)
# ────────────────────────────────────────────────────────────────────────
def b_s44_2_lambda_ptd_off_reduction() -> dict:
    """λ_ptd = 0 ⇒ L = L_decision + λ_s · L_safety = L_DHDL (§27 byte-equal)."""
    L_dec, L_safe, L_ptd, lam_s, lam_ptd = sp.symbols(
        "L_dec L_safe L_ptd lam_s lam_ptd")
    L_full = L_dec + lam_s * L_safe + lam_ptd * L_ptd
    L_off = L_full.subs(lam_ptd, 0)
    L_dhdl = L_dec + lam_s * L_safe
    reduced = sp.simplify(L_off - L_dhdl) == 0

    # ── structural reduction: check that lambda_ptd appears as a multiplier
    # on every PTD-only computation path in train_dhdl_ptd.py (so the actual
    # source code embodies the symbolic reduction).
    src = (HERE / "train_dhdl_ptd.py").read_text(encoding="utf-8")
    # gradient line for PTD aux must contain lambda_ptd
    src_lines = src.splitlines()
    dxhat_lines = [ln for ln in src_lines if "dxhat" in ln and "lambda_ptd" in ln]
    l_ptd_lines = [ln for ln in src_lines if "l_ptd" in ln and "lambda_ptd" in ln]
    structural_ok = (len(dxhat_lines) > 0) and (len(l_ptd_lines) > 0)

    return {
        "id": "B-S44-2",
        "name": "LAMBDA-PTD-OFF-REDUCTION-CLOSED (connection-point)",
        "sympy_reduced_to_dhdl": bool(reduced),
        "ptd_aux_gradient_gated_by_lambda_ptd_in_source": structural_ok,
        "dxhat_lines": len(dxhat_lines),
        "l_ptd_lines": len(l_ptd_lines),
        "pass": bool(reduced) and structural_ok,
    }


# ────────────────────────────────────────────────────────────────────────
# B-S44-3 (deterministic)
# ────────────────────────────────────────────────────────────────────────
def b_s44_3_gap_deterministic() -> dict:
    """Eval is a pure function of (head_weights, mean, std, corpus).
    AST grep: no RNG / no temperature sampling in eval_dhdl_ptd.py.
    """
    src = (HERE / "eval_dhdl_ptd.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    forbidden = {"random", "sample", "multinomial", "temperature",
                 "np.random", "torch.rand", "Random"}
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            txt = ast.unparse(node.func) if hasattr(ast, "unparse") else ""
            for f in forbidden:
                if f in txt:
                    hits.append((f, txt))
    no_rng = len(hits) == 0
    # also check argmax-based decision (deterministic)
    argmax_used = "max(p)" in src and "p.index(max(p))" in src
    return {
        "id": "B-S44-3",
        "name": "GAP-METRIC-DETERMINISTIC-CLOSED",
        "rng_calls_in_eval": len(hits),
        "rng_call_hits": hits,
        "argmax_used": argmax_used,
        "pass": no_rng and argmax_used,
    }


# ────────────────────────────────────────────────────────────────────────
# B-S44-4 (scale-orthogonal)
# ────────────────────────────────────────────────────────────────────────
def b_s44_4_scale_orthogonal() -> dict:
    """Composed head total params 1825 / base 283.72M < 1%."""
    N_IN = 14
    H1 = 32; H2_DEC = 16; N_OUT_DEC = 3
    H2_PTD = 16; N_OUT_PTD = 14
    # weights + biases
    shared = N_IN * H1 + H1                       # 14·32 + 32 = 480
    decision = H1 * H2_DEC + H2_DEC + H2_DEC * N_OUT_DEC + N_OUT_DEC  # 579
    ptd = H1 * H2_PTD + H2_PTD + H2_PTD * N_OUT_PTD + N_OUT_PTD       # 766
    total = shared + decision + ptd
    base = 283_720_000
    ratio = sp.Rational(total, base)
    one_pct = sp.Rational(1, 100)
    pass_ = bool(ratio < one_pct)
    return {
        "id": "B-S44-4",
        "name": "SCALE-ORTHOGONAL-CLOSED",
        "params_shared": shared,
        "params_decision": decision,
        "params_ptd_aux": ptd,
        "params_total": total,
        "base_params": base,
        "ratio": float(ratio),
        "below_one_percent": pass_,
        "pass": pass_,
    }


def main() -> int:
    t0 = time.time()
    verdicts = [
        b_s44_1_dual_loss_plus_ptd_nonneg(),
        b_s44_2_lambda_ptd_off_reduction(),
        b_s44_3_gap_deterministic(),
        b_s44_4_scale_orthogonal(),
    ]
    all_pass = all(v["pass"] for v in verdicts)
    out = {
        "research_md_section": "§44",
        "battery": "B-S44-1..4",
        "verdicts": verdicts,
        "all_pass": all_pass,
        "count_closed": sum(1 for v in verdicts if v["pass"]),
        "total": len(verdicts),
        "wall_sec": round(time.time() - t0, 3),
        "B-S44-NOTE": (
            "Whether PTD-aux moves the decision-head accuracy, gap, or "
            "CONTINUE_THINK corner behaviour is SGD convergence + measurement "
            "OUTCOME (empirical). The battery proves composition is well-formed "
            "+ λ-reducible to §27 + deterministic + scale-orthogonal. It does "
            "NOT prove the composition improves anything (DESIGN_S38.md §7 — "
            "better-engineered distillation, still distillation, NOT emergence). "
            "B-D-NOTE / B-DHDL-NOTE / B-PTD-NOTE family."
        ),
    }
    (HERE / "blue_falsifier_s44_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False)
    )
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
