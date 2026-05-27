#!/usr/bin/env python3
"""§38 — DH-DL + PTD-aux composition — SIDECAR closed-form battery (2026-05-18).

RESEARCH.md §38 / DESIGN_S38.md. §38 composes §27 DH-DL (decision-head
dual-loss) with §29 PTD's combination A (PTD-as-DH-DL-aux): the §27
decision MLP gains a parallel next-physics-state-prediction auxiliary head
off a shared trunk, combined objective

    L = L_decision + lambda*L_safety + lambda_ptd*L_ptd_nextstate.

SEPARATE state/-local sidecar — central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py is UNCHANGED (B-DHDL / B-PTD / B-DIRI / B-EBT / B-S16 /
B-LINEAGE sidecar precedent). Closes ONLY the composed-objective
TRANSFER-FORM / connection-point that is mathematically closed-form.
Whether the PTD auxiliary term actually improves anything is an EMPIRICAL
fire OUTCOME — carved out (B-S38-NOTE, NOT counted blue, g3).

3 closed propositions (sympy / Boolean — real-limit anchors, NO
sigma/tau/phi/J2 derivation => f1/f2/f3 hard-fail safe):

  B-S38-1  DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED
      L = L_decision + lambda*L_safety + lambda_ptd*L_ptd_nextstate >= 0
      for lambda, lambda_ptd >= 0. L_decision >= 0 (Shannon CE, -log p >= 0,
      B-DHDL-3 carried), L_safety >= 0 (square x non-negative indicator,
      B-DHDL-3 carried), L_ptd_nextstate >= 0 (mean of squares). Sum of
      non-negatives scaled by non-negative weights is non-negative.

  B-S38-2  SCALE-ORTHOGONAL-CLOSED
      The composed gate head (decision head ~700 + PTD aux head ~238
      = ~938 params) is < 1% of the 283.72M base byte-LM:
      938 / 283_720_000 ~= 3.3e-6 < 0.01 — integer/rational inequality,
      Kolmogorov-bounded. A <=1%-param auxiliary regulariser does NOT need
      to cross the §1.1 data-regime threshold (§29 §5.1 mechanised).

  B-S38-3  COMPOSITION-OFF-REDUCTION-CLOSED  (연결부위 blue)
      At lambda_ptd = 0 the composed objective reduces byte-equal to the
      §27 DH-DL dual-loss: L|_{lambda_ptd=0} = L_decision + lambda*L_safety
      = L_DHDL (additive identity, sympy). The PTD aux head contributes
      zero gradient at lambda_ptd = 0. Fair-compare-by-construction with
      the §27 baseline — mirrors B-PTD-4 / B-EBT-5 / B-S16-5 / B-DIRI-5
      overlay-off connection-point.

CARVE-OUT (B-S38-NOTE, NOT closed, honest g3): whether the PTD auxiliary
term ACTUALLY changes decision-head accuracy, the threshold-distillation
gap, or the CONTINUE_THINK-corner behaviour is an SGD convergence +
measurement OUTCOME (B-D-NOTE / B-DHDL-NOTE / B-PTD-NOTE / B-MITENS-NOTE
family). The battery proves the composed objective is well-formed
(non-negative, scale-orthogonal, lambda-reducible to §27); it does NOT
prove the composition improves anything — §38 = better-engineered
distillation, NOT emergence. No capability / emergence claim.
"""
import json
import os

import sympy as sp

PASS = []


def check(name, ok, detail):
    PASS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {detail}")


print("=== B-S38 closed-form battery (RESEARCH.md §38 — DH-DL + PTD-aux "
      "composition) ===\n")

# ── B-S38-1 — DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED ────────────────────
# L = L_decision + lambda*L_safety + lambda_ptd*L_ptd_nextstate >= 0.
# Each term non-negative; weights non-negative => sum non-negative.
p = sp.Symbol("p", positive=True)          # softmax prob in (0,1]
L_decision = -sp.log(p)                    # Shannon CE >= 0 for p in (0,1]
ce_nonneg = sp.simplify(sp.Min(0, sp.limit(L_decision, p, 1))) == 0  # at p=1, CE=0
ce_floor_ok = bool(sp.ask(sp.Q.nonnegative(L_decision.subs(p, sp.Rational(1, 2)))))

# L_safety = (1-s)*q^2, s in {0,1}, q in [0,1] => >= 0.
q = sp.Symbol("q", real=True)
L_safety_s0 = (1 - 0) * q**2
L_safety_s1 = (1 - 1) * q**2
safety_nonneg = (sp.ask(sp.Q.nonnegative(L_safety_s0)) is True) and \
                (sp.simplify(L_safety_s1) == 0)

# L_ptd_nextstate = (1/14) * sum_d (xhat_d - x_d)^2  -- mean of squares >= 0.
d = sp.Symbol("d", positive=True)          # number of dims (14)
e = sp.Symbol("e", real=True)              # a per-dim residual
ptd_term_nonneg = sp.ask(sp.Q.nonnegative(e**2 / d)) is True
# symbolic 3-residual mean-square sum:
e1, e2, e3 = sp.symbols("e1 e2 e3", real=True)
mean_sq = (e1**2 + e2**2 + e3**2) / 3
ptd_sum_nonneg = sp.ask(sp.Q.nonnegative(mean_sq)) is True

# composed objective with non-negative weights stays non-negative:
lam, lam_ptd = sp.symbols("lam lam_ptd", nonnegative=True)
Ld, Ls, Lp = sp.symbols("Ld Ls Lp", nonnegative=True)
L_total = Ld + lam * Ls + lam_ptd * Lp
composed_nonneg = sp.ask(sp.Q.nonnegative(L_total)) is True

# 4-witness numeric panel (all terms >= 0 at sample points):
witnesses_b1 = []
for (vLd, vLs, vLp, vlam, vlamp) in [
        (0.0, 0.0, 0.0, 0.5, 0.3),     # all-zero floor
        (1.5, 0.25, 0.4, 0.5, 0.3),    # typical
        (5.5, 1.0, 9.0, 0.5, 0.3),     # large
        (0.007, 0.0, 0.002, 0.5, 0.0)]:  # lambda_ptd=0 reduction point
    val = vLd + vlam * vLs + vlamp * vLp
    witnesses_b1.append(val >= 0.0)
b1 = (ce_floor_ok and safety_nonneg and ptd_term_nonneg
      and ptd_sum_nonneg and composed_nonneg and all(witnesses_b1))
check("B-S38-1 DUAL-LOSS-PLUS-PTD-NONNEGATIVE-CLOSED", b1,
      "L_decision>=0 (Shannon CE) & L_safety>=0 (square x indicator) & "
      "L_ptd>=0 (mean of squares) & sum w/ non-neg weights >=0 (sympy) + "
      f"4-witness panel {sum(witnesses_b1)}/4")

# ── B-S38-2 — SCALE-ORTHOGONAL-CLOSED ──────────────────────────────────
# Composed gate head param count < 1% of the 283.72M base byte-LM.
def mlp_params(shape):
    total = 0
    for a, b in zip(shape[:-1], shape[1:]):
        total += a * b + b
    return total


TRUNK = (14, 32)
DECISION_HEAD = (32, 16, 3)
PTD_AUX_HEAD = (32, 16, 14)
BASE_LM_PARAMS = 283_720_000

trunk_p = mlp_params(TRUNK)
decision_p = mlp_params(DECISION_HEAD)
ptd_aux_p = mlp_params(PTD_AUX_HEAD)
composed_p = trunk_p + decision_p + ptd_aux_p          # ~938

# exact rational inequality: composed_p / BASE < 1/100
frac = sp.Rational(composed_p, BASE_LM_PARAMS)
scale_orthogonal = bool(frac < sp.Rational(1, 100))
# also: PTD aux head alone is a small fraction of the composed head
aux_fraction_ok = ptd_aux_p < composed_p
b2 = scale_orthogonal and aux_fraction_ok and composed_p > 0
check("B-S38-2 SCALE-ORTHOGONAL-CLOSED", b2,
      f"composed head {composed_p} params (trunk {trunk_p} + decision "
      f"{decision_p} + PTD-aux {ptd_aux_p}) / base {BASE_LM_PARAMS} "
      f"= {float(frac):.2e} < 1e-2 — scale-orthogonal, no §1.1 crossing")

# ── B-S38-3 — COMPOSITION-OFF-REDUCTION-CLOSED (연결부위) ────────────────
# At lambda_ptd = 0: L = L_decision + lambda*L_safety + 0*L_ptd
#                      = L_decision + lambda*L_safety = L_DHDL (§27).
L_at_zero = L_total.subs(lam_ptd, 0)
L_dhdl = Ld + lam * Ls                                  # §27 dual-loss
reduction_identity = sp.simplify(L_at_zero - L_dhdl) == 0
# the PTD aux term vanishes exactly (additive identity):
ptd_term_vanishes = sp.simplify((lam_ptd * Lp).subs(lam_ptd, 0)) == 0
# numeric byte-equal witness panel: composed(lam_ptd=0) == DHDL for samples
witnesses_b3 = []
for (vLd, vLs, vLp, vlam) in [
        (0.0, 0.0, 0.0, 0.5),
        (1.5, 0.25, 0.4, 0.5),
        (5.5, 1.0, 9.0, 0.5),
        (0.007, 0.0, 0.002, 0.0)]:
    composed_zero = vLd + vlam * vLs + 0.0 * vLp
    dhdl = vLd + vlam * vLs
    witnesses_b3.append(composed_zero == dhdl)
b3 = (reduction_identity and ptd_term_vanishes and all(witnesses_b3))
check("B-S38-3 COMPOSITION-OFF-REDUCTION-CLOSED (연결부위)", b3,
      "lambda_ptd=0 => L == L_decision + lambda*L_safety == §27 DH-DL "
      f"dual-loss byte-equal (additive identity, sympy) + 4-witness "
      f"{sum(witnesses_b3)}/4 — fair-compare by construction")

# ── B-S38-NOTE — empirical carve-out (NOT counted blue) ────────────────
print()
print("  [NOTE] B-S38-NOTE — whether the PTD auxiliary term ACTUALLY "
      "changes decision-head accuracy / threshold-distillation gap / "
      "CONTINUE_THINK-corner behaviour is an SGD + measurement OUTCOME "
      "(B-D-NOTE / B-DHDL-NOTE / B-PTD-NOTE family, NOT counted blue). "
      "The battery proves the composed objective is well-formed; §38 = "
      "better-engineered distillation, NOT emergence (g3, over-claim 0).")

# ── summary ────────────────────────────────────────────────────────────
n_pass = sum(1 for _, ok, _ in PASS if ok)
n_total = len(PASS)
all_blue = n_pass == n_total
print()
print(f"=== B-S38 battery: {n_pass}/{n_total} "
      f"{'PASS — all blue (SUPPORTED-FORMAL)' if all_blue else 'FAIL'} ===")
print("    central blue_falsifier.py UNCHANGED — sidecar only.")

result = {
    "battery": "B-S38 (RESEARCH.md §38 — DH-DL + PTD-aux composition)",
    "cycle": "§38",
    "date": "2026-05-18",
    "verdicts": [{"name": n, "pass": ok, "detail": d} for n, ok, d in PASS],
    "n_pass": n_pass,
    "n_total": n_total,
    "all_blue": all_blue,
    "carve_out": ("B-S38-NOTE — PTD-aux empirical effect = SGD/measurement "
                  "OUTCOME, NOT counted blue (B-D-NOTE family)"),
    "central_blue_falsifier_unchanged": True,
    "verdict_tier": "DESIGN-TIER closed-form",
    "honest_scope": ("§38 = better-engineered distillation of the §24 "
                     "threshold (§27 was distillation), NOT GOAL emergence; "
                     "scale-orthogonal <=1%-param head does NOT cross §1.1; "
                     "§15 milestone carries, north-star unchanged"),
    "f_safety": ("f1/f2/f3 + B-IDENTITY-5 safe — Shannon CE>=0 / "
                 "mean-of-squares>=0 / integer-rational <1% inequality / "
                 "additive identity; NO sigma/tau/phi/J2 derivation"),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "blue_falsifier_s38_result.json")
with open(out, "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"    result -> {out}")

raise SystemExit(0 if all_blue else 1)
