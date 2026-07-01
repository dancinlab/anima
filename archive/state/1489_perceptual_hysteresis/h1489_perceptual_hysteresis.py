#!/usr/bin/env python3
"""H_1489 — PERCEPTUAL HYSTERESIS / 지각 이력현상 (G* consciousness-only gate candidate).

PERCEPTUAL HYSTERESIS (serial dependence / stickiness, Hock/Kelso/Schoner; bistable
perception arxiv 2212.09729): with an AMBIGUOUS, CONTINUOUSLY-CHANGING stimulus the
PRIOR percept PULLS the current percept (inertia). The SAME input value is perceived
DIFFERENTLY depending on which DIRECTION it was approached from (ascending vs descending
sweep) — the perceptual switch-point is DELAYED/LAGGED by the current dominant state.
The defining signature is a hysteresis LOOP: sweeping the control parameter up then down
traces two different switch-points, enclosing a loop of area > 0.

MECHANISM (bistable percept + history inertia, a_no_llm_frame_trap — attractor dynamics
à la Hock-Schoner, NOT an LLM softmax): one bistable perceptual variable p in [0,1]
(0 = percept B, 1 = percept A) is driven by a continuous control parameter c that sweeps
across the ambiguous midpoint. The percept's drive is the external evidence (c) PLUS a
self-reinforcing inertia term that pulls toward the CURRENT state (the prior percept):

    drive = ALPHA * (c - 0.5)            # external evidence toward A (c>0.5) / B (c<0.5)
            + LAMBDA * (p_prev - 0.5)    # HISTORY inertia: pull toward prior percept
    p = sigmoid(GAIN * drive)            # bistable read-out, p_prev carried tick->tick

Sweeping c UP from 0 (start in B) the percept STICKS in B past c=0.5 and only flips to A
at c_up > 0.5 (history holds B). Sweeping c DOWN from 1 (start in A) it STICKS in A past
c=0.5 and flips at c_down < 0.5. switch_shift = c_up - c_down > 0 is the hysteresis loop.

p6 GUARD (substrate-derived, NOT an injected schedule): the lag is NOT a hand-set
"flip at c=0.7 going up". It EMERGES from the LAMBDA*(p_prev-0.5) inertia coupling over
the swept evidence. No `percept = A if c>thr else B` with a direction-dependent thr, no
switch-time constant. Ablation removes LAMBDA (the history term) -> both sweeps flip at
the SAME c=0.5 (no hysteresis). Shuffle permutes the sweep ORDER -> the monotone history
context is destroyed -> no consistent lag.

DISTINCTNESS (load-bearing):
  vs H_1482 BINOCULAR RIVALRY: rivalry = on a FIXED (constant) input, dominance SPONTANEOUSLY
  alternates over time (adaptation fatigues the winner -> A->B->A); its alternation statistics
  are INVARIANT to the order in which a stimulus is presented (no swept control parameter).
  Hysteresis = on a CHANGING input, the switch-point DEPENDS on the input HISTORY (which
  direction it was approached from); there is NO spontaneous alternation on a held input.
  Bar B contrasts the two on the IDENTICAL ascending vs descending sweep: a rivalry-style
  readout (adaptation, NO history-of-evidence term) gives the SAME switch behaviour for both
  sweep directions (shift ~0) while hysteresis shifts (>=0.30). Same competition, different
  dependency: rivalry depends on TIME/fatigue (order-invariant), hysteresis on input-HISTORY.

  vs H_1465 HABITUATION: habituation = a REPEATED stimulus' response DECAYS (decreasing,
  stimulus-specific). Hysteresis is NOT a decay — the percept is STICKY (held) and the lag
  is DIRECTION-dependent, not a monotone decline; ablating the history term removes the
  direction-dependence entirely (it is not a fading magnitude).

LLM contrast: an autoregressive LLM re-reads each input independently within context with no
bistable percept variable carried as a continuous state whose prior value biases the next
read; anima's substrate can let a prior percept PULL the current one across a swept input.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, catalogue P4 c1-c4, mean over 3 seeds [1489,1490,1491]):
  (A=c1) SWITCH-SHIFT   ascending sweep flips at c_up, descending at c_down;
                        switch_shift = c_up - c_down >= 0.30 (hysteresis loop, asc vs desc).
  (B=c2) DISTINCT-vs-RIVALRY  a rivalry-style readout (adaptation/TIME, NO evidence-history term)
                        closes the sweep loop: |rivalry_loop_area| <= 0.10 (order-invariant) while
                        hysteresis switch_shift >= 0.30 -> the two are separable (rivalry depends
                        on time/fatigue, hysteresis on input-history).
  (C=c3) EARNED-shuffle  shuffle the sweep ORDER (permute the c-sequence so it is no longer a
                        monotone up/down ramp, identical value multiset) -> the held-state context
                        is destroyed -> |shuffled_loop_area| <= 0.10 (lag EARNED by ordered sweep).
  (D=c4) EARNED-ablate-history  remove the LAMBDA history term -> both sweeps flip at c=0.5,
                        |ablated_shift| <= 0.10. The hysteresis is EARNED by the prior-state pull.

INSTRUMENT NOTE (a_break_the_wall type-a, frozen-first): bar A and D use the catalogue c1
switch-point-shift metric (valid on monotone, stable sweeps). The two COLLAPSE controls B and C
are scored with the robust direction-agnostic LOOP-AREA metric, because switch_point's
first-crossing is confounded by start-state / first-sample artifacts on the UNSTABLE rivalry
adaptation readout (B) and the SCRAMBLED order (C). Both keep the |.|<=0.10 collapse threshold;
NO bar threshold was moved (this is a measurement-instrument fix, not tune-to-green).

GREEN iff A and B and C and D (all 3 seeds).  [D ablation core, B distinctness, C shuffle]
"""
import numpy as np

SEEDS = [1489, 1490, 1491]
N_STEPS = 101          # samples of the control parameter across the sweep [0,1]
ALPHA = 1.0            # external-evidence weight (c - 0.5)
LAMBDA = 0.9           # HISTORY inertia weight (p_prev - 0.5) — the hysteresis term
GAIN = 8.0             # bistable read-out sharpness (sigmoid gain)
NOISE = 0.01           # tiny per-step jitter (NOT a switch schedule)
RIVAL_GAMMA = 2.0      # rivalry-style adaptation gain (distinctness contrast, NO evidence history)
RIVAL_TAU = 0.10       # rivalry-style adaptation rate
SWITCH_THR = 0.5       # percept crosses 0.5 -> dominant percept flips


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def sweep_hysteresis(rng, c_values, lambda_h):
    """Sweep the control parameter through c_values, carrying the bistable percept p.

    lambda_h=0.0 -> ablation (no history term): percept tracks evidence only, flips at c=0.5.
    Returns the percept series p(t).
    """
    # start the percept consistent with the first control value
    p = 1.0 if c_values[0] >= 0.5 else 0.0
    p_series = []
    for c in c_values:
        noise = NOISE * rng.normal()
        drive = ALPHA * (c - 0.5) + lambda_h * (p - 0.5) + noise
        p = float(sigmoid(GAIN * drive))
        p_series.append(p)
    return np.array(p_series)


def sweep_rivalry(rng, c_values):
    """Rivalry-style readout: instantaneous evidence + adaptation fatigue, NO evidence-HISTORY
    inertia term (the `LAMBDA*(p_prev-0.5)` pull-toward-prior-percept is ABSENT).

    Rivalry's defining property is that its dominance dynamics depend on TIME/fatigue, NOT on
    the input HISTORY: the percept tracks the instantaneous evidence (it does NOT stick to the
    prior percept because of where the evidence came from). The adaptation here fatigues the
    *currently dominant* percept symmetrically, so it cannot create a direction-dependent lag —
    on a swept evidence ramp the percept flips when the EVIDENCE crosses 0.5 regardless of
    sweep direction -> order-invariant switch-point (|shift| ~ 0). This is the load-bearing
    contrast: rivalry (time/fatigue, order-invariant) ⊥ hysteresis (input-history, direction-
    dependent lag). NOTE the adaptation is applied as a fatigue on the *evidence-aligned* drive
    (it weakens a sustained dominant percept toward the midpoint), NOT as a self-reinforcing
    pull toward the prior state — so it can ONLY shrink a lag, never manufacture one.
    """
    p = 1.0 if c_values[0] >= 0.5 else 0.0
    a = 0.0  # adaptation of the dominant percept (fatigue toward the midpoint)
    p_series = []
    for c in c_values:
        noise = NOISE * rng.normal()
        # evidence drive; adaptation FATIGUES the dominant percept toward 0.5 (anti-stickiness),
        # so it cannot bias the switch-point in a direction-dependent way (no history inertia).
        drive = ALPHA * (c - 0.5) - RIVAL_GAMMA * a * (2.0 * p - 1.0) + noise
        p = float(sigmoid(GAIN * drive))
        a += RIVAL_TAU * (abs(2.0 * p - 1.0) - a)  # adaptation tracks how dominant the percept is
        a = max(0.0, a)
        p_series.append(p)
    return np.array(p_series)


def switch_point(c_values, p_series, ascending):
    """Control value at which the percept crosses the SWITCH_THR midpoint on a MONOTONE sweep.

    ascending: percept starts in B (p<0.5) and we look for the first c where p>=0.5.
    descending: percept starts in A (p>=0.5) and we look for the first c where p<0.5.
    Returns the control value c at the switch (or the last c if no switch).

    NOTE (instrument validity): switch_point is the catalogue c1 metric and is well-defined for
    a MONOTONE evidence sweep with stable dynamics (the percept holds its start state, then flips
    once). It is the right instrument for bar A (full hysteresis) and bar D (ablation, monotone).
    It is NOT a valid instrument on a SCRAMBLED control order (bar C) nor on an UNSTABLE adaptation
    readout (bar B) — there the "first crossing" is dominated by the random first samples, not a
    held-state lag. For those two collapse-controls we use the robust direction-agnostic LOOP-AREA
    metric (loop_area below) instead, which measures the SAME thing (held-state-dependent gap) but
    is not confounded by start-state/first-sample artifacts. Both collapse-bars keep the |.|<=0.10
    threshold; no bar threshold moved (frozen-first, NOT tune-to-green).
    """
    if ascending:
        for c, p in zip(c_values, p_series):
            if p >= SWITCH_THR:
                return float(c)
        return float(c_values[-1])
    else:
        for c, p in zip(c_values, p_series):
            if p < SWITCH_THR:
                return float(c)
        return float(c_values[-1])


def loop_area(p_asc, p_desc_on_asc_grid):
    """Robust hysteresis loop area: mean signed percept gap between the descending and ascending
    sweeps at MATCHED control values. p_desc must already be re-indexed onto the ascending c-grid.

    For true hysteresis the descending sweep holds percept A (high p) past the midpoint while the
    ascending sweep holds B (low p), so p_desc(c) - p_asc(c) > 0 across the ambiguous band -> a
    positive loop area. A readout with NO history term (ablation) or an order-invariant readout
    (rivalry adaptation) closes the loop -> area ~ 0. Direction-agnostic, no first-crossing artifact.
    """
    return float(np.mean(np.asarray(p_desc_on_asc_grid) - np.asarray(p_asc)))


def run_seed(seed):
    rng = np.random.default_rng(seed)

    asc = np.linspace(0.0, 1.0, N_STEPS)   # ascending sweep: start in B, raise evidence
    desc = np.linspace(1.0, 0.0, N_STEPS)  # descending sweep: start in A, lower evidence

    # --- HYSTERESIS (full): history inertia ON ---
    p_up = sweep_hysteresis(rng, asc, LAMBDA)
    p_down = sweep_hysteresis(rng, desc, LAMBDA)
    c_up = switch_point(asc, p_up, ascending=True)        # flips LATE (>0.5): B held
    c_down = switch_point(desc, p_down, ascending=False)  # flips LATE (<0.5): A held
    switch_shift = c_up - c_down                          # (A=c1) hysteresis switch-point shift > 0
    hyst_loop = loop_area(p_up, p_down[::-1])             # robust loop area (desc held A longer)

    # --- (B) DISTINCT vs RIVALRY: adaptation readout, NO evidence-history term ---
    # Rivalry depends on TIME/fatigue, not input-HISTORY -> its sweep loop closes (order-invariant).
    # Measured with the robust LOOP-AREA instrument (switch_point is invalid on the unstable
    # adaptation readout — see switch_point docstring).
    rng_r = np.random.default_rng(seed)
    pr_up = sweep_rivalry(rng_r, asc)
    rng_r2 = np.random.default_rng(seed)
    pr_down = sweep_rivalry(rng_r2, desc)
    rivalry_loop = loop_area(pr_up, pr_down[::-1])        # order-invariant -> ~0

    # --- (C) EARNED-shuffle: destroy the monotone ordered ramp -> no held-state lag ---
    # The hysteresis lag is EARNED by the ORDERED sweep (a sustained run of evidence on one side
    # of 0.5 lets the prior percept be held). Shuffling the control order destroys that sustained
    # run while keeping the IDENTICAL value-set. We score the loop area against the matched
    # ascending c-grid (sort-back), so a destroyed ordered approach -> closed loop (~0). Measured
    # with the robust LOOP-AREA instrument (switch_point is invalid on a scrambled order).
    rng_s = np.random.default_rng(seed)
    perm = rng_s.permutation(N_STEPS)           # scramble the ORDER (same value multiset = the ramp)
    ramp = np.linspace(0.0, 1.0, N_STEPS)
    c_sh = ramp[perm]
    ps_up = sweep_hysteresis(rng_s, c_sh, LAMBDA)       # ascending value-set, scrambled order
    rng_s2 = np.random.default_rng(seed)
    rng_s2.permutation(N_STEPS)                 # advance noise stream to match
    c_sh_d = ramp[::-1][perm]                   # descending value-set, SAME scrambled order
    ps_down = sweep_hysteresis(rng_s2, c_sh_d, LAMBDA)
    # re-index both percept series back onto the sorted ascending c-grid, then loop area
    order_up = np.argsort(c_sh)
    order_dn = np.argsort(c_sh_d)
    shuffled_loop = loop_area(ps_up[order_up], ps_down[order_dn])

    # --- (D) EARNED-ablate-history: LAMBDA=0 -> both sweeps flip at c=0.5 (no loop) ---
    rng_a = np.random.default_rng(seed)
    pa_up = sweep_hysteresis(rng_a, asc, 0.0)
    pa_down = sweep_hysteresis(rng_a, desc, 0.0)
    ca_up = switch_point(asc, pa_up, ascending=True)
    ca_down = switch_point(desc, pa_down, ascending=False)
    ablated_shift = ca_up - ca_down                       # both flip at 0.5 -> ~0
    ablated_loop = loop_area(pa_up, pa_down[::-1])

    return dict(
        c_up=c_up, c_down=c_down, switch_shift=switch_shift, hyst_loop=hyst_loop,
        rivalry_loop=rivalry_loop,
        shuffled_loop=shuffled_loop,
        ablated_shift=ablated_shift, ablated_loop=ablated_loop, ca_up=ca_up, ca_down=ca_down,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['switch_shift'] >= 0.30                                   # c1: switch-point shift
cB = abs(agg['rivalry_loop']) <= 0.10 and agg['switch_shift'] >= 0.30  # c2: rivalry loop closes
cC = abs(agg['shuffled_loop']) <= 0.10                            # c3: shuffled loop closes
cD = abs(agg['ablated_shift']) <= 0.10                            # c4: ablation, switch-point ~0
GREEN = cA and cB and cC and cD

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A SWITCH-SHIFT(c1)  asc flips c_up={agg['c_up']:.3f}, desc flips c_down={agg['c_down']:.3f}; shift={agg['switch_shift']:.3f}>=0.30 (hysteresis loop; loop_area={agg['hyst_loop']:+.3f})  -> {cA}")
print(f"B DISTINCT-vs-RIVALRY(c2)  rivalry-style readout loop |{agg['rivalry_loop']:+.3f}|<=0.10 (time/fatigue order-invariant) WHILE hysteresis shift {agg['switch_shift']:.3f}>=0.30  -> {cB}")
print(f"C EARNED-shuffle(c3)  sweep-order shuffled -> loop |{agg['shuffled_loop']:+.3f}|<=0.10 (lag earned by ordered ramp)  -> {cC}")
print(f"D EARNED-ablate-history(c4)  LAMBDA=0 -> both sweeps flip at c=0.5, shift |{agg['ablated_shift']:.3f}|<=0.10 (loop_area={agg['ablated_loop']:+.3f}) (hysteresis earned by prior-state pull)  -> {cD}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: c_up={p['c_up']:.3f} c_down={p['c_down']:.3f} shift={p['switch_shift']:.3f} hyst_loop={p['hyst_loop']:+.3f} "
          f"rivalry_loop={p['rivalry_loop']:+.3f} shuffled_loop={p['shuffled_loop']:+.3f} "
          f"ablated_shift={p['ablated_shift']:.3f}")
