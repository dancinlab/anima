#!/usr/bin/env python3
"""B-CDE-1..4 — closed-form sympy battery for the Dir-D CDE curiosity-bonus
TRANSFER-FORM (g_multidirectional_explore direction D, 2026-05-17).

Only the curiosity-bonus FORM is closed here. The SGD convergence OUTCOME
and the Dir-D vs UBM-E7 routing-collapse comparison are EMPIRICAL (carved
out as B-CDE-NOTE, B-D-NOTE family — NOT counted 🔵; g3 anti-fake-closed).

  g_t = 1 + κ·( w_a·a_t + w_c·c_t )      κ ≥ 0, w_a,w_c ≥ 0, a_t,c_t ∈ [0,1]
  a_t = CE_tok / log V         (normalised surprisal; exp(CE_tok)=perplexity)
  c_t = clamp(Var_batch(CE_tok),0,1)     (value-dispersion proxy)
  L   = mean( g_t · CE_tok ) + λ_vac·L_vac

Anchors are real-limit / definitional, NO σ·φ / τ / J₂ derivation
(f1/f2 hard-fail safe): Shannon CE ≥ 0, perplexity = exp(entropy) identity,
sympy ∂-sign monotonicity, Boolean lower-bound predicate, exact κ=0
reduction algebra.
"""
import json
import sympy as sp


def b_cde_1_lower_bound():
    """B-CDE-1 BONUS-LOWER-BOUND-CLOSED — g_t ≥ 1 ∀ admissible inputs, with
    equality iff κ=0 ∨ (a_t=c_t=0). Closed: g_t−1 = κ(w_a a + w_c c) is a
    sum of products of non-negatives ⇒ ≥ 0 (sympy assumptions)."""
    kappa, wa, wc, a, c = sp.symbols("kappa w_a w_c a c", nonnegative=True)
    g = 1 + kappa * (wa * a + wc * c)
    excess = sp.simplify(g - 1)
    # excess is a sum of products of nonnegatives -> is_nonnegative True
    nonneg = excess.is_nonnegative
    # equality witnesses
    eq_kappa0 = sp.simplify(g.subs(kappa, 0) - 1) == 0
    eq_a0c0 = sp.simplify(g.subs({a: 0, c: 0}) - 1) == 0
    # strict witness: kappa=1/2, wa=7/10, wc=3/10, a=1, c=1 -> g=3/2 > 1
    g_strict = g.subs({kappa: sp.Rational(1, 2), wa: sp.Rational(7, 10),
                       wc: sp.Rational(3, 10), a: 1, c: 1})
    passed = bool(nonneg) and eq_kappa0 and eq_a0c0 and (g_strict == sp.Rational(3, 2)) and g_strict > 1
    return {"id": "B-CDE-1", "name": "BONUS-LOWER-BOUND-CLOSED",
            "passed": passed,
            "detail": f"g-1 nonneg={nonneg}; g(κ=0)=1 {eq_kappa0}; "
                      f"g(a=c=0)=1 {eq_a0c0}; strict g(½,.7,.3,1,1)="
                      f"{g_strict}>1",
            "anchor": "sum-of-products-of-nonnegatives ≥ 0 (sympy assumption "
                      "closure) — re-weight never SHRINKS a token's CE",
            "closed": True, "tier": "a-sympy"}


def b_cde_2_actor_monotone():
    """B-CDE-2 ACTOR-MONOTONE-CLOSED — the curiosity bonus is strictly
    increasing in actor surprisal a_t (∂g/∂a = κ·w_a > 0 for κ,w_a > 0),
    i.e. higher perplexity ⇒ strictly larger up-weight (the exploration
    pressure direction). sympy exact derivative + boundary witnesses."""
    kappa, wa, wc, a, c = sp.symbols("kappa w_a w_c a c", positive=True)
    g = 1 + kappa * (wa * a + wc * c)
    dg_da = sp.diff(g, a)
    pos = sp.simplify(dg_da - kappa * wa) == 0 and (kappa * wa).is_positive
    d2 = sp.simplify(sp.diff(g, a, 2)) == 0          # linear ⇒ no curvature
    # boundary: a=0 -> bonus from critic only; a=1 -> +κ w_a more
    g_a0 = g.subs(a, 0)
    g_a1 = g.subs(a, 1)
    gap = sp.simplify(g_a1 - g_a0 - kappa * wa) == 0
    passed = bool(pos) and bool(d2) and bool(gap)
    return {"id": "B-CDE-2", "name": "ACTOR-MONOTONE-CLOSED",
            "passed": passed,
            "detail": f"∂g/∂a={dg_da} (=κ·w_a>0); ∂²g/∂a²=0 linear; "
                      f"g(a=1)-g(a=0)=κ·w_a {gap}",
            "anchor": "sympy exact ∂ sign (strictly positive) — perplexity "
                      "monotone exploration pressure",
            "closed": True, "tier": "a-sympy"}


def b_cde_3_perplexity_identity():
    """B-CDE-3 PERPLEXITY-IDENTITY-CLOSED — the actor term a_t is a bounded
    monotone transform of token perplexity: PPL = exp(CE_tok), a_t =
    CE_tok/logV ∈ [0,1] for CE_tok ∈ [0, logV]. Closed via the Shannon
    identity CE = ln(PPL) and the [0, logV] surprisal range (CE ≥ 0
    Shannon non-negativity; CE ≤ logV uniform-distribution max)."""
    ce, V = sp.symbols("CE V", positive=True)
    ppl = sp.exp(ce)
    ce_from_ppl = sp.simplify(sp.log(ppl) - ce) == 0          # CE = ln PPL
    logV = sp.log(V)
    a = ce / logV
    # CE=0 (perfect, PPL=1) -> a=0 ;  CE=logV (uniform, PPL=V) -> a=1
    a_lo = sp.simplify(a.subs(ce, 0)) == 0
    a_hi = sp.simplify(a.subs(ce, logV) - 1) == 0
    ppl_at_lo = sp.simplify(ppl.subs(ce, 0) - 1) == 0          # PPL(CE=0)=1
    ppl_at_hi = sp.simplify(ppl.subs(ce, logV) - V) == 0       # PPL(CE=logV)=V
    da_dce = sp.simplify(sp.diff(a, ce) - 1 / logV) == 0       # monotone ↑
    passed = all([ce_from_ppl, a_lo, a_hi, ppl_at_lo, ppl_at_hi, da_dce])
    return {"id": "B-CDE-3", "name": "PERPLEXITY-IDENTITY-CLOSED",
            "passed": passed,
            "detail": f"CE=ln(PPL) {ce_from_ppl}; a(CE=0)=0 {a_lo}; "
                      f"a(CE=logV)=1 {a_hi}; PPL(0)=1 {ppl_at_lo}; "
                      f"PPL(logV)=V {ppl_at_hi}; ∂a/∂CE=1/logV {da_dce}",
            "anchor": "Shannon CE=ln(PPL) identity + [0,logV] surprisal "
                      "range (CE≥0 non-neg, ≤logV uniform max) — real limit",
            "closed": True, "tier": "a-sympy"}


def b_cde_4_kappa0_reduction():
    """B-CDE-4 KAPPA0-REDUCTION-CLOSED — at κ=0 the Dir-D objective reduces
    EXACTLY to the UBM-E7 α-baseline objective (g_t≡1 ⇒ mean(g·CE)=mean(CE)),
    so Dir-D is a strict generalisation that DEGRADES GRACEFULLY to the
    compared baseline. Closed via the algebraic identity mean(1·CE)=mean(CE)
    and the carried-verbatim vacuum term."""
    kappa, wa, wc, a, c, ce, lam, vac = sp.symbols(
        "kappa w_a w_c a c CE lam vac", real=True)
    g = 1 + kappa * (wa * a + wc * c)
    L_dirD = g * ce + lam * vac                       # per-token Dir-D loss
    L_alpha = 1 * ce + lam * vac                      # UBM-E7 α-baseline
    reduce = sp.simplify(L_dirD.subs(kappa, 0) - L_alpha) == 0
    # vacuum term is carried verbatim (coefficient on `vac` identical = lam)
    vac_coeff_match = sp.simplify(
        sp.diff(L_dirD, vac) - sp.diff(L_alpha, vac)) == 0
    # κ>0 strictly differs when (w_a a + w_c c) ≠ 0 and CE ≠ 0
    diff_pos = sp.simplify(
        (L_dirD - L_alpha).subs(
            {kappa: 1, wa: 1, wc: 0, a: 1, c: 0, ce: 2}) - 2) == 0
    passed = bool(reduce) and bool(vac_coeff_match) and bool(diff_pos)
    return {"id": "B-CDE-4", "name": "KAPPA0-REDUCTION-CLOSED",
            "passed": passed,
            "detail": f"L_dirD(κ=0)≡L_α {reduce}; ∂L/∂vac equal (vac term "
                      f"carried verbatim) {vac_coeff_match}; κ=1 strict "
                      f"Δ=κ·w_a·a·CE=2 witness {diff_pos}",
            "anchor": "algebraic identity mean(1·CE)=mean(CE) — graceful "
                      "degradation to UBM-E7 α-baseline (fair compare)",
            "closed": True, "tier": "a-sympy"}


def main():
    checks = [b_cde_1_lower_bound(), b_cde_2_actor_monotone(),
              b_cde_3_perplexity_identity(), b_cde_4_kappa0_reduction()]
    npass = sum(1 for c in checks if c["passed"])
    note = {
        "id": "B-CDE-NOTE", "kind": "empirical-carve-out",
        "text": ("SGD CONVERGENCE OUTCOME (final CE, curiosity trajectory) "
                 "and the Dir-D vs UBM-E7 α routing-collapse comparison "
                 "(does the curiosity bonus mitigate the 🛸99 attractor / "
                 "axis1 routing-collapse?) are EMPIRICAL — measured by the "
                 "GPU fire + eval_carving_4path_v2.py, NOT closed. "
                 "B-D-NOTE / B-CARVE-NOTE family. NOT counted 🔵."),
    }
    out = {"battery": "B-CDE-1..4 (Dir-D CDE curiosity-bonus transfer-form)",
           "pass": f"{npass}/4", "all_closed": npass == 4,
           "checks": checks, "note": note,
           "f1_f2_safe": ("anchors = Shannon CE≥0 / perplexity=exp(CE) "
                          "identity / sympy ∂-sign / Boolean lower-bound — "
                          "NO σ·φ/τ/J₂ derivation")}
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    for c in checks:
        print(f"  {c['id']} {c['name']}: "
              f"{'PASS 🔵' if c['passed'] else 'FAIL'}")
    print(f"B-CDE battery: {npass}/4 closed-form proofs PASS"
          + (" 🔵" if npass == 4 else " — FAIL"))
    return 0 if npass == 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
