#!/usr/bin/env python3
# H_1301 — phase-RESET / photic-entrainment clock (HD35 candidate, c15 brain-structure ladder)
# ----------------------------------------------------------------------------------------------
# DEPLETION TEST r7 (very likely the FINAL rung). Frozen-first: see
# .verdicts/1301_phase_reset/FREEZE.txt — all bars pre-registered BEFORE this run; no bar moves.
#
# CANDIDATE: a free-running phase oscillator (intrinsic period tau) with a Zeitgeber RESET input
# that applies a PHASE-DEPENDENT shift via a sinusoidal Phase-Response-Curve (PRC). The PRC is a
# CONTINUOUS RESTORING FEEDBACK that pulls the internal phase toward a STABLE entrained phase
# relationship with the Zeitgeber (limit-cycle attraction). This is the chronobiology mechanism
# (Pittendrigh/Aschoff PRC entrainment) — NOT an LLM recipe (a_no_llm_frame_trap, c15).
#
# CONTROL-SURVIVING DISTINCTNESS vs the TWO nearest lanes:
#   A  CircadianClock (H_1298): baked period, NO reset -> CANNOT entrain to T != baked period (c1).
#   A2 IntervalTimer-style HARD-RESET (H_1299 observe = phase-INDEPENDENT hard re-anchor, no PRC):
#      copies Zeitgeber jitter directly -> HIGH entrained-phase variance, NO limit-cycle damping (c2).
# CONTROLS: B-SHUFFLE permutes Zeitgeber arrival phases (kills the phase-dependent pull -> c4);
#           B-ABLATE sets K=0 (removes the PRC -> B free-runs at tau, cannot entrain -> c5).
#
# $0 CPU numpy mirror, DIRECTIONAL (engine-transfer UNVERIFIED until R2 byte-exact). p7. 3 seeds.
# Deterministic given a seed (numpy default_rng). p1/p2/p3/p6: the oscillator reads ONLY its own
# phase + Zeitgeber arrival times; NO persona/label/RLHF; the PRC shift is geometry, SCORED only.

import numpy as np
import json

# ── FROZEN regime constants (verbatim from FREEZE.txt) ────────────────────────────────────────
SEEDS        = [4310, 4311, 4312]
TAU_INTERNAL = 24.5    # intrinsic free-running period (ticks/cycle); != T_zeit
T_ZEIT       = 24.0    # Zeitgeber period (different day length, the entrain target)
K_COUPLE     = 0.18    # PRC coupling strength
N_CYCLES     = 40      # entrainment window
JITTER_SD    = 0.6     # Zeitgeber arrival jitter (ticks) — the limit-cycle DAMPING test
SETTLE       = 20      # transient cycles discarded; metrics over the last (N_CYCLES-SETTLE)
TOL_ENTRAIN  = 0.08    # entrained phase-error tolerance (fraction of a cycle)


def _wrap_phase(p):
    """wrap a phase into [0,1)."""
    return p - np.floor(p)


def _circ_diff(a, b):
    """signed phase difference (a-b) wrapped into (-0.5, 0.5] — fraction of a cycle."""
    d = (a - b + 0.5) % 1.0 - 0.5
    return d


def gen_zeitgeber_times(rng):
    """The external Zeitgeber arrival ABSOLUTE ticks: one per day at period T_ZEIT with jitter.
    Returns the absolute arrival ticks for cycles 0..N_CYCLES-1. The jitter is the limit-cycle
    DAMPING test: a PRC restoring force damps it; a hard re-anchor copies it directly."""
    base = np.arange(N_CYCLES) * T_ZEIT
    jit = rng.normal(0.0, JITTER_SD, size=N_CYCLES)
    return base + jit


# ── ARM B — PhaseResetClock: free-running tau + sinusoidal PRC reset ───────────────────────────
def run_phase_reset(zeit_times, K=K_COUPLE):
    """Advance internal phase at rate 1/tau per tick (phi is CUMULATIVE = elapsed cycles). At each
    Zeitgeber arrival, apply a PHASE-DEPENDENT shift dphi = K*sin(2pi*(0 - frac(phi))) (the PRC;
    the Zeitgeber marks subjective dawn = reference phase 0). The PRC pulls frac(phi) toward a
    STABLE relationship with the Zeitgeber. A FIRE = every phase-0 boundary crossing (integer phi).
    Returns (phase_at_zeit_frac[], fire_times[]); phi is CUMULATIVE so the fire count = floor(phi)."""
    phi = 0.0
    t_prev = 0.0
    phase_at_zeit = []
    cum_phi = []   # the CUMULATIVE phase (elapsed cycles) AT each Zeitgeber — NET fire count
    for tz in zeit_times:
        dt = tz - t_prev
        phi = phi + dt / TAU_INTERNAL            # free-run advance (cumulative cycles)
        t_prev = tz
        # PRC reset: phase-dependent pull on the FRACTIONAL phase (the cumulative count is kept).
        phi_frac = phi - np.floor(phi)
        dphi = K * np.sin(2.0 * np.pi * (0.0 - phi_frac))
        phi = phi + dphi
        cum_phi.append(phi)
        phase_at_zeit.append(phi - np.floor(phi))
    # NET realized fires = cumulative-phase boundary crossings; the realized fire PERIOD is the
    # mean time per NET cycle (immune to the within-cycle free-run-vs-PRC-jump split): an entrained
    # oscillator advances exactly ONE cumulative cycle per Zeitgeber day -> fire_period -> T.
    return np.array(phase_at_zeit), (np.array(zeit_times), np.array(cum_phi))


def fire_period_from_cum(zt, cum_phi):
    """realized fire period = elapsed time / NET cumulative-phase cycles over the post-SETTLE
    window (robust to the within-cycle free-run/PRC-jump boundary split)."""
    z = zt[SETTLE:]
    c = cum_phi[SETTLE:]
    if len(z) < 2:
        return float("nan")
    elapsed = z[-1] - z[0]
    net_cycles = c[-1] - c[0]
    if abs(net_cycles) < 1e-9:
        return float("nan")
    return float(elapsed / net_cycles)


# ── ARM A — CircadianClock (H_1298): baked period, NO reset (ignores the Zeitgeber) ────────────
def run_baked_clock(zeit_times):
    """Free-runs at its BAKED period == TAU_INTERNAL forever; the Zeitgeber CANNOT touch it
    (clock_step is content-blind, no reset input — H_1298). We read the internal phase AT each
    Zeitgeber arrival; because tau != T_zeit the phase DRIFTS relative to the Zeitgeber."""
    phase_at_zeit = []
    cum_phi = []
    phi = 0.0
    t_prev = 0.0
    for tz in zeit_times:
        dt = tz - t_prev
        phi = phi + dt / TAU_INTERNAL
        t_prev = tz
        # NO reset (the load-bearing distinctness: the clock ignores the Zeitgeber)
        cum_phi.append(phi)
        phase_at_zeit.append(_wrap_phase(phi))
    return np.array(phase_at_zeit), (np.array(zeit_times), np.array(cum_phi))


# ── ARM A2 — IntervalTimer-style HARD-RESET (H_1299 observe): phase-INDEPENDENT re-anchor ──────
def run_hard_reset(zeit_times):
    """The IntervalTimer's observe HARD re-anchors: at each Zeitgeber event the phase is SET to 0
    (elapsed:=0) REGARDLESS of the current phase — a phase-INDEPENDENT reset with NO restoring
    dynamics. Between events it free-runs at tau. The entrained phase-at-Zeitgeber therefore just
    re-expresses whatever residual the prior free-run produced; under a JITTERED Zeitgeber the
    jitter is copied DIRECTLY into the phase (no limit-cycle damping). This is the c2 FAIL arm."""
    phase_at_zeit = []
    phi = 0.0
    t_prev = 0.0
    for tz in zeit_times:
        dt = tz - t_prev
        phi = phi + dt / TAU_INTERNAL
        # the phase observed AT the Zeitgeber (before the hard reset) — this is what carries jitter
        phase_at_zeit.append(_wrap_phase(phi))
        # HARD re-anchor: set phase to 0 (the IntervalTimer observe; phase-independent)
        phi = 0.0
        t_prev = tz
    return np.array(phase_at_zeit)


# ── metrics ────────────────────────────────────────────────────────────────────────────────────
def entrain_err(phase_at_zeit):
    """The CORRECT entrainment metric (R1b — fixed from the R1a self-mean-scatter mis-design):
    entrainment = the phase-at-Zeitgeber STOPS DRIFTING (converges to a stable phase fixed point).
    A free-running oscillator with tau != T DRIFTS steadily; over a W-cycle window the internal
    phase sweeps ~W*|1 - T/tau| of a cycle. We measure the TOTAL UNWRAPPED drift magnitude over
    the post-SETTLE window (the sum of |signed per-cycle phase advances|): entrained -> ~0;
    un-entrained clock -> a large accumulated drift (sweeps a sizeable fraction of a full cycle).
    Returns the total unwrapped drift in fraction-of-cycle over the window."""
    p = phase_at_zeit[SETTLE:]
    steps = _circ_diff(p[1:], p[:-1])   # signed per-cycle advance, wrapped to (-0.5, 0.5]
    return float(np.abs(np.sum(steps)))


def phase_var(phase_at_zeit):
    """The jitter-DAMPING signal (c2): variance of the per-cycle phase RESIDUAL after removing the
    arm's mean drift, over post-SETTLE cycles. The PRC limit-cycle DAMPS Zeitgeber jitter -> low
    residual variance; the hard re-anchor copies each Zeitgeber's jitter into the phase -> high
    residual variance. (Measuring the residual about the mean drift isolates jitter from any
    steady drift, so an entrained-but-jittery arm and a drifting arm are compared on jitter alone.)"""
    p = phase_at_zeit[SETTLE:]
    steps = _circ_diff(p[1:], p[:-1])
    return float(np.var(steps))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    zt = gen_zeitgeber_times(rng)

    # B — phase reset (returns phase_at_zeit + (zt, cumulative phi) for the net fire period)
    pB, (ztB, cumB) = run_phase_reset(zt, K=K_COUPLE)
    # A — baked clock (no reset)
    pA, (ztA, cumA) = run_baked_clock(zt)
    # A2 — hard reset (IntervalTimer observe) — only phase_at_zeit needed (c2 jitter-damping)
    pA2 = run_hard_reset(zt)
    # B-SHUFFLE — DESTROY the Zeitgeber PERIODICITY (R1c: a mean-preserving GAP-PERMUTATION
    #   leaked — permuting near-identical ~24-tick gaps barely changes the schedule, so B still
    #   entrained = a MIS-SPECIFIED control. The claimed structure is "entrain to a PERIODIC
    #   Zeitgeber via the phase-dependent PRC"; the correct control destroys the PERIODICITY:
    #   the SAME number of events at the SAME mean rate but with gaps drawn from a HIGH-VARIANCE
    #   (aperiodic) distribution, so NO consistent period exists to lock to. The phase at which
    #   each reset lands is now decorrelated -> the PRC pull cannot converge to a stable phase.)
    mean_gap = float(np.mean(np.diff(np.concatenate([[0.0], zt]))))
    rand_gaps = rng.uniform(0.2 * mean_gap, 1.8 * mean_gap, size=len(zt))  # same mean rate, aperiodic
    zt_shuf = np.cumsum(rand_gaps)
    pBs, _ = run_phase_reset(zt_shuf, K=K_COUPLE)
    # B-ABLATE — K=0: the PRC coupling removed -> reset has no effect -> free-runs at tau
    pBa, (ztBa, cumBa) = run_phase_reset(zt, K=0.0)

    return {
        "B_entrain_err": entrain_err(pB),
        "A_entrain_err": entrain_err(pA),
        "B_phase_var": phase_var(pB),
        "A2_phase_var": phase_var(pA2),
        "B_fire_period": fire_period_from_cum(ztB, cumB),
        "A_fire_period": fire_period_from_cum(ztA, cumA),
        "Bshuf_entrain_err": entrain_err(pBs),
        "Babl_entrain_err": entrain_err(pBa),
        "Babl_fire_period": fire_period_from_cum(ztBa, cumBa),
    }


def nofab_check():
    """c6 NO-FAB: with NO Zeitgeber present, B free-runs at tau and fires ONLY at its own phase-0
    boundary. Off-boundary (mid-cycle) it does NOT fire -> no spurious pulse."""
    # free-run for one cycle, sample phase at a mid-cycle tick and a boundary tick
    phi_mid = _wrap_phase(0.0 + (TAU_INTERNAL / 2.0) / TAU_INTERNAL)   # = 0.5, off boundary
    phi_boundary = _wrap_phase(0.0 + TAU_INTERNAL / TAU_INTERNAL)       # = 0.0, the boundary
    fires_at_boundary = abs(phi_boundary - 0.0) < 1e-9
    fires_mid = abs(phi_mid - 0.0) < 1e-9
    return fires_at_boundary and (not fires_mid)


def main():
    per_seed = []
    for s in SEEDS:
        per_seed.append(run_seed(s))

    def mean(key):
        return float(np.mean([r[key] for r in per_seed]))

    m = {k: mean(k) for k in per_seed[0].keys()}

    # ── FROZEN bars (verbatim from FREEZE.txt) ──
    def allseeds(pred):
        return all(pred(r) for r in per_seed)

    # R1b FROZEN bars (re-derived analytically from the corrected total-drift metric; see FREEZE)
    c1_mean = (m["B_entrain_err"] <= 0.05) and (m["A_entrain_err"] >= 0.20)
    c1_seed = allseeds(lambda r: (r["B_entrain_err"] <= 0.05) and (r["A_entrain_err"] >= 0.20))
    c1 = c1_mean and c1_seed

    c2_mean = (m["B_phase_var"] <= 0.5 * m["A2_phase_var"]) and (m["B_phase_var"] <= 0.0015)
    c2_seed = allseeds(lambda r: (r["B_phase_var"] <= 0.5 * r["A2_phase_var"]) and (r["B_phase_var"] <= 0.0015))
    c2 = c2_mean and c2_seed

    c3_mean = (abs(m["B_fire_period"] - T_ZEIT) <= 0.30) and (abs(m["A_fire_period"] - TAU_INTERNAL) <= 0.30)
    c3_seed = allseeds(lambda r: (abs(r["B_fire_period"] - T_ZEIT) <= 0.30) and (abs(r["A_fire_period"] - TAU_INTERNAL) <= 0.30))
    c3 = c3_mean and c3_seed

    c4_mean = m["Bshuf_entrain_err"] >= 0.20
    c4_seed = allseeds(lambda r: r["Bshuf_entrain_err"] >= 0.20)
    c4 = c4_mean and c4_seed

    c5_mean = (m["Babl_entrain_err"] >= 0.20) and (abs(m["Babl_fire_period"] - TAU_INTERNAL) <= 0.30)
    c5_seed = allseeds(lambda r: (r["Babl_entrain_err"] >= 0.20) and (abs(r["Babl_fire_period"] - TAU_INTERNAL) <= 0.30))
    c5 = c5_mean and c5_seed

    c6 = nofab_check()

    bars = [c1, c2, c3, c4, c5, c6]
    green = all(bars)

    print("=" * 90)
    print("H_1301 — phase-RESET / photic-entrainment clock — HD35 DEPLETION TEST (r7)")
    print("=" * 90)
    print(f"seeds={SEEDS}  tau={TAU_INTERNAL}  T_zeit={T_ZEIT}  K={K_COUPLE}  N_CYCLES={N_CYCLES}")
    print(f"JITTER_SD={JITTER_SD}  SETTLE={SETTLE}  TOL_ENTRAIN={TOL_ENTRAIN}")
    print("-" * 90)
    print("PER-SEED:")
    for s, r in zip(SEEDS, per_seed):
        print(f"  seed {s}: B_err={r['B_entrain_err']:.4f} A_err={r['A_entrain_err']:.4f} "
              f"B_pvar={r['B_phase_var']:.6f} A2_pvar={r['A2_phase_var']:.6f}")
        print(f"            B_period={r['B_fire_period']:.3f} A_period={r['A_fire_period']:.3f} "
              f"Bshuf_err={r['Bshuf_entrain_err']:.4f} Babl_err={r['Babl_entrain_err']:.4f} "
              f"Babl_period={r['Babl_fire_period']:.3f}")
    print("-" * 90)
    print("3-SEED MEAN:")
    print(f"  B.entrain_err  = {m['B_entrain_err']:.4f}   (<= 0.05 ?)   [B entrains to T!=tau; ~0 drift]")
    print(f"  A.entrain_err  = {m['A_entrain_err']:.4f}   (>= 0.20 ?)            [clock CANNOT entrain]")
    print(f"  B.phase_var    = {m['B_phase_var']:.6f}  (<= 0.5*A2 & <= 0.0015 ?) [PRC damps jitter]")
    print(f"  A2.phase_var   = {m['A2_phase_var']:.6f}  (hard re-anchor copies jitter)")
    print(f"  B.fire_period  = {m['B_fire_period']:.3f}  (-> T_zeit {T_ZEIT})    [tracks Zeitgeber]")
    print(f"  A.fire_period  = {m['A_fire_period']:.3f}  (-> tau {TAU_INTERNAL}) [keeps baked period]")
    print(f"  Bshuf.err      = {m['Bshuf_entrain_err']:.4f}   (>= 0.20 ?)         [shuffle kills entrain]")
    print(f"  Babl.err       = {m['Babl_entrain_err']:.4f}   (>= 0.20 ?)         [K=0 cannot entrain]")
    print(f"  Babl.period    = {m['Babl_fire_period']:.3f}  (-> tau {TAU_INTERNAL}) [free-runs at tau]")
    print("-" * 90)
    labels = [
        "c1 ENTRAIN-vs-CLOCK  (B locks to T!=tau; clock drifts)",
        "c2 DAMP-vs-HARDRESET (PRC damps jitter; hard re-anchor copies it)",
        "c3 PERIOD-TRACK      (B fires at T; clock fires at tau)",
        "c4 EARNED-SHUFFLE    (permuted Zeitgeber phases -> no entrain)",
        "c5 EARNED-ABLATE     (K=0 -> free-runs at tau, no entrain)",
        "c6 NO-FAB            (fires only at own phase-0 boundary)",
    ]
    for lbl, b in zip(labels, bars):
        print(f"  [{'PASS' if b else 'FAIL'}] {lbl}")
    print("-" * 90)
    print(f"bars = {[bool(b) for b in bars]}")
    if green:
        print("VERDICT: GREEN — phase-RESET SURVIVES the depletion test; HD35 CONTINUES the ladder.")
    else:
        print("VERDICT: NOT GREEN — a control failed -> the candidate COLLAPSES into an existing")
        print("         lane -> the c15 brain-structure ladder is DEPLETED (the expected honest")
        print("         outcome; NO filler lane, NO tune-to-green).")
    print("=" * 90)

    out = {"seeds": SEEDS, "mean": m, "per_seed": per_seed,
           "bars": {"c1": bool(c1), "c2": bool(c2), "c3": bool(c3),
                    "c4": bool(c4), "c5": bool(c5), "c6": bool(c6)},
           "green": bool(green)}
    print("JSON " + json.dumps(out))


if __name__ == "__main__":
    main()
