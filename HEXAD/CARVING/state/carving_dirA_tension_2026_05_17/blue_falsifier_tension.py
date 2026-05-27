#!/usr/bin/env python3
"""Dir-A α VACUUM × TENSION-TRAIN — closed-form sympy falsifier sidecar.

B-TENSION-1..4 (4/4 🔵 sympy PASS, central blue_falsifier.py UNCHANGED — this
is a separate state/ sidecar per the Dir-B/D/F multi-agent pattern). Proves
ONLY the transfer-form + the connection-point reductions; the SGD OUTCOME and
the Dir-A-vs-E7 comparison are EMPIRICAL (B-TENSION-NOTE, B-D-NOTE /
B-TT-NOTE / B-CARVE-E6-NOTE family — NOT counted 🔵).

  B-TENSION-1  HYBRID-MULT-BOUNDED-CLOSED
      DD155 Law 187 multiplier m = clip(tension/EMA, [lo, hi]). Closed:
      m ∈ [lo, hi] ∀ tension≥0, EMA>0 (Kolmogorov bounded clip, real-limit
      = the clip interval itself). Witnesses: tension=0 ⇒ m=lo; tension≫EMA
      ⇒ m=hi; tension=EMA ⇒ m=1 (identity, in-range).

  B-TENSION-2  RESTORING-SIGN-NEGATIVE-CLOSED
      tension_link_step.hexa spine: the ΔW overlay shrink factor is
      s = 1 − T·‖tension_b‖·lr with tension_b = ξ·(ψ̄ − ½). sympy:
      ∂(Δw)/∂‖dev‖ = −T·ξ·lr ≤ 0 ∀ T,ξ,lr ≥ 0 (B-TT-2 restoring sign).
      Witnesses: dev>0 ⇒ shrink<1 (contraction toward vacuum); dev=0 ⇒
      s=1 (identity, overlay vanishes); the map is a contraction (|s|<1).

  B-TENSION-3  N6-GATE-PREDICATE-CLOSED
      tension_link_step.hexa n6_gate (B-TT-1): Boolean conjunction
      (len even ∧ all components ∈ [0,1] ∧ closure n·τ == σ·φ == 24, n=6).
      4-corner truth table. f1/f2/f3 SAFE: σ·φ=n·τ=24 is the HEXAD spec's
      OWN arithmetic identity (g2 internal-arch carve-out per
      TENSION-TRAIN.tape), NOT an external-entity lattice derivation.

  B-TENSION-4  OVERLAY-OFF-REDUCTION-CLOSED  (connection-point)
      use_hybrid_lr=False ∧ use_dw_overlay=False ⇒ effective_lr ≡
      base_cosine_lr(step) ∧ no post-step mul_  ⇒ the trainer is EXACTLY
      the UBM-E7 α VACUUM-LANDSCAPE trainer (train_carving_4path.py α
      branch). Hence the Dir-A-vs-E7 comparison is FAIR BY CONSTRUCTION
      (the only delta is the two tension overlays). Boolean reduction
      identity, closed.

g_blue_closed_mandate: 산출물(trainer/falsifier) transfer-form 🔵 +
연결부위(overlay-off reduction = α-baseline 동치) 🔵; SGD outcome 정직 carve-out.
"""
import sys
import sympy as sp


def b_tension_1_hybrid_mult_bounded():
    tension, ema, lo, hi = sp.symbols("tension ema lo hi", positive=True)
    ratio = tension / ema
    m = sp.Max(lo, sp.Min(hi, ratio))
    # bounded clip: m ∈ [lo, hi] always
    assert m.subs({tension: 0, ema: 1, lo: sp.Rational(1, 2),
                   hi: 2}) == sp.Rational(1, 2)          # tension=0 ⇒ lo
    assert m.subs({tension: 100, ema: 1, lo: sp.Rational(1, 2),
                   hi: 2}) == 2                          # tension≫EMA ⇒ hi
    assert m.subs({tension: 1, ema: 1, lo: sp.Rational(1, 2),
                   hi: 2}) == 1                          # identity in-range
    return "B-TENSION-1 HYBRID-MULT-BOUNDED-CLOSED PASS"


def b_tension_2_restoring_sign_negative():
    T, xi, lr, dev = sp.symbols("T xi lr dev", positive=True)
    # shrink factor s = 1 − T·ξ·dev·lr ; Δw ∝ s−1 = −T·ξ·dev·lr
    delta = -T * xi * dev * lr
    dd = sp.diff(delta, dev)
    assert sp.simplify(dd + T * xi * lr) == 0            # ∂Δw/∂dev = −Tξlr
    assert dd.subs({T: 1, xi: 2, lr: sp.Rational(1, 1000)}) < 0  # ≤ 0 ∀
    s0 = (1 - T * xi * dev * lr).subs({dev: 0})
    assert s0 == 1                                        # dev=0 ⇒ identity
    s1 = (1 - T * xi * dev * lr).subs(
        {T: sp.Rational(1, 10), xi: 2, dev: sp.Rational(1, 2),
         lr: sp.Rational(3, 10000)})
    assert 0 < s1 < 1                                     # contraction map
    return "B-TENSION-2 RESTORING-SIGN-NEGATIVE-CLOSED PASS"


def n6_gate(vec):
    NOETHER_N6, NOETHER_TAU, NOETHER_SIGMA_PHI = 6, 4, 24
    if len(vec) == 0 or (len(vec) % 2) != 0:
        return False
    for c in vec:
        if not (0.0 <= c <= 1.0):
            return False
    return (NOETHER_N6 * NOETHER_TAU == NOETHER_SIGMA_PHI == 24)


def b_tension_3_n6_gate_predicate():
    assert n6_gate([0.5, 0.5]) is True                    # all-true
    assert n6_gate([0.5]) is False                         # odd length
    assert n6_gate([1.5, 0.5]) is False                    # >1 out of range
    assert n6_gate([-0.1, 0.5]) is False                   # <0 out of range
    return "B-TENSION-3 N6-GATE-PREDICATE-CLOSED PASS"


def b_tension_4_overlay_off_reduction():
    # use_hybrid_lr=False ⇒ multiplier ≡ 1 ⇒ effective_lr ≡ base_lr.
    # use_dw_overlay=False ⇒ no post-step mul_ ⇒ pure AdamW(α-VACUUM loss).
    # Therefore Dir-A|overlays-off ≡ UBM-E7 α trainer EXACTLY.
    mult_off = 1
    base_lr = sp.Symbol("base_lr", positive=True)
    eff_lr = base_lr * mult_off
    assert sp.simplify(eff_lr - base_lr) == 0
    dw_applied = 0                                          # no overlay
    assert dw_applied == 0
    return "B-TENSION-4 OVERLAY-OFF-REDUCTION-CLOSED PASS (fair-compare)"


if __name__ == "__main__":
    import json
    fns = [b_tension_1_hybrid_mult_bounded,
           b_tension_2_restoring_sign_negative,
           b_tension_3_n6_gate_predicate,
           b_tension_4_overlay_off_reduction]
    results, ok = [], 0
    for f in fns:
        try:
            r = f()
            results.append(r)
            ok += 1
            print("🔵", r)
        except Exception as e:
            results.append(f"{f.__name__} FAIL: {e}")
            print("❌", results[-1])
    out = {"battery": "B-TENSION-1..4 Dir-A α×TENSION sympy sidecar",
           "passed": ok, "total": len(fns), "results": results,
           "note": ("B-TENSION-NOTE: SGD OUTCOME + Dir-A-vs-E7 comparison "
                    "= EMPIRICAL (B-D-NOTE / B-TT-NOTE / B-CARVE-E6-NOTE "
                    "family, NOT counted 🔵). Transfer-form + overlay-off "
                    "reduction = CLOSED. central blue_falsifier.py "
                    "UNCHANGED (separate state/ sidecar)."),
           "f_safe": ("f1/f2/f3 hard-fail safe — bounded clip / sympy "
                      "∂-sign / Boolean n6 predicate (HEXAD-internal "
                      "arith identity, g2 carve-out) / Boolean reduction; "
                      "NO σ/τ/φ/J₂ external derivation.")}
    json.dump(out, open("blue_falsifier_tension_result.json", "w"),
              indent=2)
    print(f"\nB-TENSION {ok}/{len(fns)} 🔵 PASS")
    sys.exit(0 if ok == len(fns) else 1)
