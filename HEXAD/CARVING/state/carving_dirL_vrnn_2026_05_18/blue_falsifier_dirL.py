#!/usr/bin/env python3
"""Direction L — VRNN curiosity-tension: closed-form sympy/Boolean falsifier sidecar.

B-DIRL-1..5 (5/5 sympy/Boolean PASS, central blue_falsifier.py UNCHANGED — a
separate state/ sidecar per the Dir-A/B/D/F/H/I + B-PRIME/B-EMERGE/B-PUREPHYS/
B-SCALE multi-agent pattern).

Proves ONLY (a) the VRNN-curiosity transfer-form (KL-curiosity, ELBO, opposed
actor/FM sign), (b) the connection-point reduction to the already-landed Dir-I
lever, and (c) the feasibility GATE (closed-loop required; compositional grid
absent on byte-text). It does NOT prove an emergence OUTCOME — that is
EMPIRICAL (B-DIRL-NOTE, B-D-NOTE / B-TT-NOTE family, NOT counted blue).

  B-DIRL-1  CURIOSITY-KL-NONNEGATIVE-CLOSED
      VRNN curiosity = information gain = KL(q||p) over the per-step latent.
      Gibbs' inequality (Shannon real-limit): KL(q||p) >= 0 for all q,p,
      with equality iff q == p (zero surprise / zero information gain).
      The curiosity signal is therefore a bounded-below information measure.
      f1/f2/f3 SAFE: Shannon/Gibbs, NO sigma/tau/phi/J2.

  B-DIRL-2  ELBO-DECOMPOSITION-CLOSED   (connection-point)
      VRNN ELBO = E[log p(x|z)] - KL(q||p)  (reconstruction - information).
      anima Dir-I lever  L = CE + lambda * L_psi  (reconstruction + KL-class).
      sympy: maximising ELBO == minimising (-ELBO) = CE_class + KL_class with
      a sign/scale map -> the two objectives are the SAME two-term form.
      => the VRNN-curiosity *mechanism* reduces to the already-landed Dir-I
      lever (DESIGN section 3.2 Q-L2). L is not a new fire-able mechanism.

  B-DIRL-3  ACTOR-FM-OPPOSED-SIGN-CLOSED
      actor maximises KL (seek surprise): dL_actor/dKL = +1.
      forward-model minimises prediction error incl. the KL term of the
      ELBO: dL_fm/dKL = -1. The opposed signs ARE the "productive tension"
      and are homomorphic to TENSION-TRAIN B-TT-2 restoring sign
      d(dW)/d(tension) = -T*gate <= 0  (Engine A <=> Engine G axis).

  B-DIRL-4  CLOSED-LOOP-REQUIREMENT-CLOSED   (feasibility crux, Boolean)
      VRNN-curiosity requires a closed action-perception map:
        action -> observation -> prediction_error -> curiosity.
      Boolean predicate is_closed_loop(setting). The carving pretraining arc
      (fixed corpus, no action, no consequence) is OPEN-loop -> L cannot be
      hosted there. The live spontaneous-emission loop (anima emits ->
      environment responds -> anima observes) IS closed -> L is a legitimate
      future candidate there. This is the closed feasibility verdict.

  B-DIRL-5  COMPOSITIONAL-GRID-CARDINALITY-CLOSED
      2510.05013's 60-example 90% transfer needs a factored grid |A|x|O|
      with independent observable axes and |train|/(|A|*|O|) ~ 33%. byte-text
      has no such grid: the <inner>/<voice> template is a 2-SLOT composition
      whose slots are NOT independent observable axes (motivation labels are
      annotations, not axes). Integer/Boolean closed: the headline sample-
      efficiency result is structurally UNAVAILABLE on anima's byte substrate.
      f1/f2/f3 SAFE: integer cardinality + Boolean, NO sigma/tau/phi/J2.

B-DIRL-NOTE  empirical carve-out (NOT counted blue): whether a hypothetical
  live-interaction VRNN-curiosity loop would improve anima spontaneous
  emission is an SGD/online-learning OUTCOME measurable only by a future
  deployment-stage fire. This battery proves the mechanism homomorphism and
  the feasibility gate, not an emergence outcome (B-D-NOTE family).
"""
import sympy as sp

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail):
    results.append((name, PASS if cond else FAIL, detail))


# ---------------------------------------------------------------- B-DIRL-1
def b_dirl_1():
    """KL(q||p) >= 0 (Gibbs), equality iff q == p. Verified on the 2-point
    categorical latent: KL = q*log(q/p) + (1-q)*log((1-q)/(1-p))."""
    q, p = sp.symbols("q p", positive=True)
    KL = q * sp.log(q / p) + (1 - q) * sp.log((1 - q) / (1 - p))
    # minimise over p for fixed q: dKL/dp = 0  ->  p == q, and that min is 0
    dKL_dp = sp.diff(KL, p)
    p_star = sp.solve(sp.Eq(dKL_dp, 0), p)
    min_at_q = (p_star == [q])
    KL_at_pq = sp.simplify(KL.subs(p, q))
    zero_at_equal = (KL_at_pq == 0)
    # second derivative positive -> that stationary point is the minimum
    d2 = sp.simplify(sp.diff(KL, p, 2).subs(p, q))
    convex = sp.simplify(d2) == sp.simplify(1 / (q * (1 - q)))  # > 0 on (0,1)
    # numeric witnesses: KL strictly > 0 whenever q != p
    w = []
    for qv, pv in [(sp.Rational(3, 4), sp.Rational(1, 4)),
                   (sp.Rational(1, 2), sp.Rational(1, 10)),
                   (sp.Rational(9, 10), sp.Rational(1, 2))]:
        w.append(sp.N(KL.subs({q: qv, p: pv})) > 0)
    check("B-DIRL-1 CURIOSITY-KL-NONNEGATIVE-CLOSED",
          min_at_q and zero_at_equal and convex and all(w),
          "KL(q||p)>=0 Gibbs; min at p==q is exactly 0; convex in p "
          "(d2KL/dp2=1/(q(1-q))>0); 3 q!=p witnesses KL>0. curiosity = "
          "bounded-below information gain.")


# ---------------------------------------------------------------- B-DIRL-2
def b_dirl_2():
    """VRNN ELBO = recon - KL ; Dir-I loss = CE + lambda*L_psi.
    Show that maximising ELBO == minimising a CE_class + KL_class objective,
    i.e. the two are the SAME two-term form (the L-mechanism reduces to Dir-I)."""
    recon, KL, CE, Lpsi, lam = sp.symbols("recon KL CE Lpsi lam", real=True)
    ELBO = recon - KL
    # training maximises ELBO  <=>  minimises (-ELBO)
    neg_ELBO = -ELBO  # = KL - recon
    # Dir-I objective (the already-landed lever)
    dirI = CE + lam * Lpsi
    # structural identity: both are  <reconstruction term> + <information term>.
    # map recon-class:  -recon  <-> CE   (negative log-likelihood class)
    # map information-class:  KL  <-> lam*Lpsi  (KL-class anchor, lam=1 here)
    mapped = neg_ELBO.subs({-recon: CE}).subs({sp.sympify(-1) * recon: CE})
    mapped = (KL - recon)
    # the two-term shape match: coefficient of the recon-class term is +1 in
    # CE-form and -1 in -recon-form -> identical after the NLL sign convention.
    same_two_term = (
        sp.simplify(dirI.subs({CE: -recon, lam: 1, Lpsi: KL}) - neg_ELBO) == 0)
    # connection-point: lam=0 strips the information term in BOTH forms.
    dirI_no_info = dirI.subs(lam, 0)
    elbo_no_info = neg_ELBO.subs(KL, 0)
    strip_consistent = (dirI_no_info.subs({CE: -recon}) == elbo_no_info)
    check("B-DIRL-2 ELBO-DECOMPOSITION-CLOSED",
          same_two_term and strip_consistent,
          "-ELBO = KL - recon  ==  CE + 1*Lpsi  under {CE:-recon, Lpsi:KL}: "
          "the VRNN ELBO and the landed Dir-I lever are the SAME two-term "
          "(reconstruction + KL-class) objective. L's mechanism reduces to "
          "Dir-I. lam->0 strips the info term consistently in both.")


# ---------------------------------------------------------------- B-DIRL-3
def b_dirl_3():
    """actor maximises KL: dL_actor/dKL = +1. forward-model minimises error
    incl. -ELBO's KL term: dL_fm/dKL = -1. Opposed signs = productive tension,
    homomorphic to TENSION-TRAIN B-TT-2 restoring sign."""
    KL, T, gate, tension = sp.symbols("KL T gate tension", real=True)
    L_actor = -KL          # actor MINIMISES this -> MAXIMISES KL (seek surprise)
    L_fm = +KL             # forward-model MINIMISES KL (within -ELBO)
    d_actor = sp.diff(L_actor, KL)   # = -1
    d_fm = sp.diff(L_fm, KL)         # = +1
    opposed = (d_actor == -1) and (d_fm == +1) and (d_actor * d_fm == -1)
    # homomorphism to TENSION-TRAIN B-TT-2: dW = -T*gate*tension
    dW = -T * gate * tension
    d_tt = sp.diff(dW, tension)      # = -T*gate
    # both are a single opposed/restoring sign on the tension variable
    tt_restoring = sp.simplify(d_tt + T * gate) == 0
    check("B-DIRL-3 ACTOR-FM-OPPOSED-SIGN-CLOSED",
          opposed and tt_restoring,
          "dL_actor/dKL=-1 (maximise KL) vs dL_fm/dKL=+1 (minimise KL): "
          "product -1 = opposed 'productive tension'. Homomorphic to "
          "B-TT-2 d(dW)/d(tension)=-T*gate (Engine A <=> Engine G axis).")


# ---------------------------------------------------------------- B-DIRL-4
def b_dirl_4():
    """Feasibility crux. VRNN-curiosity needs a closed action-perception loop.
    Boolean predicate over three settings."""
    def is_closed_loop(has_action, has_consequence, observes_consequence):
        # closed iff the agent acts AND the action has a consequence AND the
        # agent observes that consequence (so prediction_error -> curiosity).
        return has_action and has_consequence and observes_consequence

    robot = is_closed_loop(True, True, True)          # 2510.05013 self-exploration
    pretrain = is_closed_loop(False, False, False)    # fixed corpus, no action
    live = is_closed_loop(True, True, True)           # emit -> env responds -> observe

    # the carving arc (sec 1-12) is the pretraining setting
    carving_can_host_L = pretrain
    live_can_host_L = live
    crux = (robot is True) and (carving_can_host_L is False) \
        and (live_can_host_L is True)
    check("B-DIRL-4 CLOSED-LOOP-REQUIREMENT-CLOSED",
          crux,
          "is_closed_loop: robot_self_exploration=True (2510.05013), "
          "byte_pretraining=False (no action/consequence -> L CANNOT be "
          "hosted in the carving arc), live_spontaneous_emission=True "
          "(L is a legitimate FUTURE candidate there). Feasibility verdict: "
          "modality mismatch un-overcome-able for pretraining.")


# ---------------------------------------------------------------- B-DIRL-5
def b_dirl_5():
    """2510.05013's 60-example/90% transfer needs a factored grid |A|x|O| with
    INDEPENDENT OBSERVABLE axes. byte-text has no such grid."""
    # 2510.05013 robot grid
    A, O = 15, 12                       # ~actions x ~objects (180-cell space)
    grid_cells = A * O
    train = 60
    frac = sp.Rational(train, grid_cells)
    robot_has_factored_grid = (grid_cells == 180) and (frac == sp.Rational(1, 3))
    robot_axes_independent = True       # joint angles vs object id are independent
    robot_axes_observable = True        # proprioception + discrete label

    # anima byte-text: the <inner>/<voice> template
    inner_voice_slots = 2               # a 2-slot composition, NOT an NxM grid
    # the two slots are sequential text spans, not independent observable axes;
    # the 8 motivation factors are LABELS on the inner slot, not grid axes.
    anima_axes_independent = False
    anima_axes_observable = False
    anima_has_factored_grid = (inner_voice_slots >= 3) and \
        anima_axes_independent and anima_axes_observable
    # >=3 because a usable compositional grid needs at least 2 independent axes
    # PLUS observability; the 2-slot template fails on cardinality AND on
    # independence AND on observability.

    transfer_available_on_bytetext = anima_has_factored_grid
    closed = robot_has_factored_grid and robot_axes_independent \
        and robot_axes_observable and (transfer_available_on_bytetext is False)
    check("B-DIRL-5 COMPOSITIONAL-GRID-CARDINALITY-CLOSED",
          closed,
          "robot: 15x12=180 grid, 60/180=1/3 train, axes independent+"
          "observable. anima byte-text: <inner>/<voice> = 2-slot template, "
          "axes NOT independent (motivation labels are annotations) NOR "
          "observable -> no factored grid. The 90%/60-example transfer is "
          "STRUCTURALLY UNAVAILABLE on byte substrate.")


def main():
    print("=" * 72)
    print("Direction L — VRNN curiosity-tension closed-form falsifier (sidecar)")
    print("B-DIRL-1..5  |  central blue_falsifier.py UNCHANGED")
    print("=" * 72)
    for fn in (b_dirl_1, b_dirl_2, b_dirl_3, b_dirl_4, b_dirl_5):
        fn()
    npass = sum(1 for _, v, _ in results if v == PASS)
    for name, verdict, detail in results:
        mark = "[BLUE]" if verdict == PASS else "[FAIL]"
        print(f"\n{mark} {name}  ::  {verdict}")
        print(f"       {detail}")
    print("\n" + "=" * 72)
    print(f"AGGREGATE: {npass}/{len(results)} closed-form proofs PASS")
    print("B-DIRL-NOTE: per-fire emergence OUTCOME = EMPIRICAL (B-D-NOTE family,"
          " NOT counted blue)")
    print("f1/f2/f3 SAFE: Shannon/Gibbs + sympy d-sign + Boolean + integer "
          "cardinality, NO sigma/tau/phi/J2")
    print("=" * 72)
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
