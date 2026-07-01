#!/usr/bin/env python3
# H_1540 SEROTONIN-AS-PATIENCE — REGIME-SHIFTING-HORIZON RETRY of H_1538 🟠 (R1 numpy mirror).
#
# DIRECTIONAL (numpy mirror, a_engine_native_learning: grep numpy ⇒ auto-DIRECTIONAL; engine R2 deferred ING).
#
# WHY THE RETRY (the H_1538 lane's OWN identified gap, NOT tune-to-green):
#   H_1538 found the wait-for-better-emit PATIENCE faculty PRESENT + EARNED (out-earns impulsive +0.1911,
#   beats always-wait +0.2419, edge collapses under shuffle) — only the STRONG mechanism-attribution bar C
#   FAILED: a FIXED γ already captured ~51% of the patience value, so the substrate-ADAPTIVE 5-HT slope read
#   was real but a MINORITY lever (+0.0942 vs bar +0.0956). The reason a fixed γ sufficed: in H_1538 EVERY
#   episode had the SAME value-arrival timescale (rise_len ∈ [3,7], one regime) → one constant discount
#   horizon was near-optimal for all episodes, so adaptation added little.
#
#   THE ONE CHANGE (pre-registered): a REGIME-SHIFTING HORIZON. The OPTIMAL patience / time-horizon now
#   genuinely SHIFTS across contexts: some contexts reward waiting (the grounded value arrives LATE —
#   SLOW-grounding regime → LONG optimal wait), others punish it (the value arrives EARLY then decays —
#   FAST-grounding regime → SHORT optimal wait). A SINGLE fixed γ CANNOT serve both regimes; the context
#   is INFERABLE FROM SUBSTRATE STATE (the early local slope: a steep early climb signals the fast/early-peak
#   regime, a shallow early climb signals the slow/late-peak regime). Under this regime-shifting horizon the
#   substrate-state-gated (adaptive-γ) read SHOULD become the MAJORITY lever — this is exactly the condition
#   under which 5-HT-as-adaptive-discounting earns its keep.
#     - Doya K (2002) "Metalearning and neuromodulation." Neural Networks 15(4-6):495-506: 5-HT sets the
#       TIME-SCALE of reward integration — which SHOULD be context-adaptive, not a single constant.
#     - Miyazaki KW, Miyazaki K, Doya K et al (2014) Curr Biol 24(17):2033: dorsal-raphe 5-HT enhances
#       patience for delayed rewards (waiting buys the larger/later reward when the context warrants it).
#
# FRAMING: faculty-building (a NEW timing faculty for the emit gate), NOT the H_1284 recall wall.
#
# BARS ARE FROZEN IDENTICALLY to H_1538 (frozen-first, NO tune-to-green). In particular bar C UNCHANGED:
#   EARNED ablate: (PATIENT−IMPULSIVE) − (ABL-FIXED-γ − IMPULSIVE) ≥ 0.5×lift  (adaptation carries ≥ HALF).
#   The HYPOTHESIS is that under regime-shifting horizon the adaptive γ now CLEARS bar C (carries majority)
#   while every other bar still PASSES. HONEST (c9): if a fixed γ STILL captures ≥half even under shifting
#   horizon, 5-HT-adaptive is genuinely minority → HONEST 🟠, reported not hidden, NO bar moved.
#
# p7 (NO perplexity/loss; payoff is the grounded reward NETTING the wait-cost — you cannot win by just
#   always-waiting because the moment decays AND every wait is charged), frozen-first, c9, $0 CPU determ.
#
# ARMS (identical roster to H_1538):
#   IMPULSIVE  : emit at tick 0 (γ→0, never waits) — the impatient baseline.
#   PATIENT-5HT: temporal-discounting faculty — γ ADAPTED by substrate slope (the regime read).
#   ABL-FIXED  : fixed γ=0.55 (no substrate adaptation) — patience WITHOUT the 5-HT "is value rising?" read.
#                Under a SINGLE-regime world (H_1538) a fixed γ nearly matches; under regime-SHIFTING it
#                cannot serve both fast & slow regimes → it loses the majority of the edge (the bar-C test).
#   NEVERWAIT  : always-wait floor (emit only at last tick) — the must-not-just-always-wait control.
#   SHUFFLE    : value-arrival TIMES permuted → rising→decaying envelope destroyed → slope meaningless.

import numpy as np

# ───────────────────────── substrate value envelope (engine-faithful shapes) ─────────────────────────
T_TICKS = 12          # ticks available before the moment is gone           (H_1538 frozen)
WAIT_COST = 0.020     # cost charged per waited tick (the moment passing)    (H_1538 frozen)
GROUND_THR = 0.35     # below this grounding, an emit nets ZERO              (H_1538 frozen)


def _clip01(x):
    return float(min(1.0, max(0.0, x)))


def make_episode(rng):
    """A grounded-value envelope v_t: rises to a peak (grounding accrues), then decays (moment stales).
    Returned v_t IS the grounded payoff of emitting at tick t (before wait cost), in [0,1].

    THE ONE CHANGE vs H_1538 — REGIME-SHIFTING HORIZON: each episode is drawn from one of TWO regimes
    with the OPTIMAL wait genuinely DIFFERENT (and the regime inferable from substrate state = the early
    slope). The mix is 50/50; which regime is drawn is hidden from the policy (only the substrate signal
    leaks it).
      FAST regime  : peak arrives EARLY (rise_len 1-2) then DECAYS HARD → optimal wait SHORT; waiting is
                     PUNISHED (the moment stales fast).  → early slope is STEEP.
      SLOW regime  : peak arrives LATE (rise_len 7-9) and decays gently → optimal wait LONG; waiting is
                     REWARDED.  → early slope is SHALLOW.
    A SINGLE fixed γ is a compromise that is wrong in BOTH regimes (too patient for FAST → over-waits into
    the decay; too impatient for SLOW → emits before the late peak). The substrate-adaptive read can tell
    them apart from the slope and set the horizon per-regime."""
    fast = (rng.uniform() < 0.5)
    v0 = rng.uniform(0.05, 0.20)               # early emit: small, often below GROUND_THR
    peak = rng.uniform(0.78, 0.98)             # the better/grounded emit reachable by waiting
    if fast:
        rise_len = int(rng.integers(1, 3))     # FAST: peak EARLY (1-2 ticks) → short optimal wait
        decay = rng.uniform(0.14, 0.22)        # FAST: decays HARD past the peak (waiting punished)
    else:
        rise_len = int(rng.integers(7, 10))    # SLOW: peak LATE (7-9 ticks) → long optimal wait
        decay = rng.uniform(0.04, 0.08)        # SLOW: decays gently (waiting rewarded)
    v = np.zeros(T_TICKS, dtype=float)
    for t in range(T_TICKS):
        if t <= rise_len:
            frac = t / max(1, rise_len)
            base = v0 + (peak - v0) * frac     # near-linear grounding accrual to peak
        else:
            base = peak - decay * (t - rise_len)   # moment stales (regime-dependent rate)
        base += rng.normal(0.0, 0.01)          # small substrate jitter (recon-error-like)
        v[t] = _clip01(base)
    return v


def realized_payoff(v, emit_tick):
    """Net grounded payoff of emitting at emit_tick: grounded value MINUS the wait cost paid to get there,
    and ZERO realized grounding-value if the emit tick is below GROUND_THR (ungrounded emit, p7)."""
    g = v[emit_tick]
    grounded_val = g if g >= GROUND_THR else 0.0
    return grounded_val - WAIT_COST * emit_tick


# ───────────────────────── arms (emit-tick policies) ─────────────────────────
# Each arm sees v_t ONLINE tick-by-tick (no future peek); it observes the running value and its local
# SLOPE (Δv) — the substrate signal "is grounded-value still rising, and how fast?" The slope ALSO leaks
# the regime (steep early slope ⇒ FAST/early-peak ⇒ be impatient; shallow ⇒ SLOW/late-peak ⇒ be patient).

def arm_impulsive(v):
    """γ→0: emit at the first tick (no patience). Impatient baseline."""
    return 0


def arm_neverwait(v):
    """Degenerate always-wait floor: never voluntarily emit; forced out at the last tick.
    The must-not-just-always-wait control (pure procrastination)."""
    return T_TICKS - 1


def _patient_emit_tick(v, gamma_base, adapt):
    """Temporal-discounting emit policy.
    At each tick t compare emit-NOW value v[t] against a discounted estimate of the best value still
    reachable by waiting one more tick (v_hat_next = clip01(v[t]+slope), discounted by γ). WAIT iff that
    exceeds emit-now by more than the marginal wait cost.

      adapt=True (5-HT, the REGIME read): γ is the substrate-state-gated reward-TIME-HORIZON (Doya 2002:
        5-HT sets the time-scale of reward integration, context-adaptive). The regime is INFERRED FROM
        SUBSTRATE STATE = the EARLY-slope steepness over the first ticks: a STEEP early climb signals the
        FAST/early-peak regime (peak imminent, decay hard → SHORT horizon → LOW γ, emit soon); a SHALLOW
        early climb signals the SLOW/late-peak regime (peak far off, gentle decay → LONG horizon → HIGH
        γ, keep waiting). γ is set ONCE from this early-slope regime estimate (a steep regime → impatient,
        a shallow regime → patient) — NOT from the instantaneous local slope (that conflates "rising now"
        with "long horizon", which is exactly backwards in the FAST regime). early_slope is the per-tick
        rise over the first OBSERVE ticks; γ = clip01(gamma_base + REGIME_GAIN*(SLOPE_REF − early_slope))
        → shallow (early_slope<ref) ⇒ γ↑ patient; steep (early_slope>ref) ⇒ γ↓ impatient.
      adapt=False: fixed γ = gamma_base for every tick & every regime (a single compromise horizon)."""
    OBSERVE = 2          # ticks of early slope used to read the regime (substrate-state inference)
    SLOPE_REF = 0.30     # reference early-slope (between FAST ~0.5+ and SLOW ~0.1) — the regime midpoint
    REGIME_GAIN = 1.2    # how strongly the inferred regime moves the horizon γ
    if adapt:
        early_slope = (v[OBSERVE] - v[0]) / OBSERVE            # mean per-tick early climb (regime signal)
        gamma_eff = _clip01(gamma_base + REGIME_GAIN * (SLOPE_REF - early_slope))
    # CONSTRUCTION (a_break_the_wall type-a, frozen-first — bars UNCHANGED): the wait decision uses a
    # γ-HORIZON multi-step look-ahead, NOT a myopic one-tick peek. A one-step peek (v_hat_next = v[t]+slope)
    # cannot SEE a grounded peak several ticks away — in the SLOW/late-peak regime the next tick is still
    # ungrounded, so a one-step rule force-emits an ungrounded tick-0 and SLOW degenerates to 0 for ALL
    # arms (no differential for the horizon lever — a faulty CONTROL WIRING, not a bar). Instead, γ IS the
    # reward-time-scale (Doya 2002): we estimate the best grounded value reachable by waiting k more ticks
    # along the LOCAL slope (substrate-online, no future peek beyond extrapolating the current slope),
    # geometrically discounted by γ^k, and WAIT iff that discounted future beats emit-now net of the k wait
    # costs. A LARGER γ literally looks FARTHER ahead — so the substrate-state-gated γ (the 5-HT regime
    # read) controls the integration horizon, the mechanism a fixed γ cannot match across regimes.
    HORIZON = T_TICKS         # max ticks the look-ahead may extrapolate
    for t in range(T_TICKS - 1):
        slope = (v[t] - v[t - 1]) if t > 0 else (v[1] - v[0])
        gamma = gamma_eff if adapt else gamma_base
        grounded_now = v[t] >= GROUND_THR
        emit_now = v[t] if grounded_now else 0.0
        # best γ-discounted grounded value reachable by waiting k=1..K more ticks (extrapolate local slope),
        # net of the k wait-costs paid to get there. γ^k = the integration horizon (5-HT time-scale).
        best_wait = -1e9
        for k in range(1, HORIZON - t):
            v_k = _clip01(v[t] + slope * k)              # slope-extrapolated value k ticks ahead
            g_k = v_k if v_k >= GROUND_THR else 0.0       # grounded only
            disc = (gamma ** k) * g_k - WAIT_COST * k     # γ-discounted future minus k wait-costs
            if disc > best_wait:
                best_wait = disc
        # emit now iff emitting now (grounded) is at least as good as the best discounted waited future;
        # if now is ungrounded (emit_now=0) we only emit when even the best waited future is non-positive.
        if emit_now >= best_wait:
            return t
    return T_TICKS - 1


def arm_patient_5ht(v):
    return _patient_emit_tick(v, gamma_base=0.55, adapt=True)


def arm_abl_fixed(v):
    # fixed γ, no substrate adaptation (patience without the 5-HT "is value rising?" / regime read)
    return _patient_emit_tick(v, gamma_base=0.55, adapt=False)


def shuffle_episode(v, rng):
    """Permute the value-arrival TIMES → destroys the rising→decaying envelope (slope/regime meaningless)."""
    perm = rng.permutation(T_TICKS)
    return v[perm]


# ───────────────────────── experiment ─────────────────────────

def run_seed(seed, n_episodes=400):
    rng = np.random.default_rng(seed)
    arms = {
        "IMPULSIVE": arm_impulsive,
        "PATIENT-5HT": arm_patient_5ht,
        "ABL-FIXED": arm_abl_fixed,
        "NEVERWAIT": arm_neverwait,
    }
    sums = {k: 0.0 for k in arms}
    sums_shuf_patient = 0.0
    sums_shuf_imp = 0.0
    waited = {k: 0.0 for k in arms}
    for _ in range(n_episodes):
        v = make_episode(rng)
        for name, fn in arms.items():
            et = fn(v)
            sums[name] += realized_payoff(v, et)
            waited[name] += et
        # shuffle control: BOTH patient and impulsive run on the SAME time-permuted envelope (apples-to-
        # apples — the H_1538 fix). If the edge comes from reading a meaningful slope/regime, it collapses
        # when the slope is noise.
        vs = shuffle_episode(v, rng)
        et_s = arm_patient_5ht(vs)
        et_si = arm_impulsive(vs)
        sums_shuf_patient += realized_payoff(vs, et_s)
        sums_shuf_imp += realized_payoff(vs, et_si)
    res = {k: sums[k] / n_episodes for k in arms}
    res["PATIENT-SHUFFLE"] = sums_shuf_patient / n_episodes
    res["IMPULSIVE-SHUFFLE"] = sums_shuf_imp / n_episodes
    res["_wait_ticks"] = {k: waited[k] / n_episodes for k in arms}
    return res


def main():
    seeds = [1538, 1539, 1540]
    # frozen bars — IDENTICAL to H_1538 (frozen-first, NO tune-to-green)
    BAR_LIFT = 0.10        # PATIENT − IMPULSIVE ≥ +0.10 (normalized grounded payoff)
    BAR_ABL_FRAC = 0.5     # bar C: (PATIENT−IMPULSIVE) − (ABL−IMPULSIVE) ≥ BAR_ABL_FRAC*lift  (UNCHANGED)
    BAR_BEAT_NEVER = 0.10  # PATIENT must also beat the always-wait floor by ≥ +0.10 (not just-always-wait)
    BAR_SHUF_FRAC = 0.5    # shuffle collapses ≥ half the patient edge

    per = {}
    for s in seeds:
        per[s] = run_seed(s)

    print("=== H_1540 SEROTONIN-AS-PATIENCE — REGIME-SHIFTING-HORIZON retry (R1 numpy DIRECTIONAL) ===")
    print(f"seeds={seeds}  T_TICKS={T_TICKS}  WAIT_COST={WAIT_COST}  GROUND_THR={GROUND_THR}  400 ep/seed  $0 CPU  p7  c9  frozen-first")
    print("regime-shifting horizon: FAST(peak 1-2,decay 0.14-0.22,short opt wait) vs SLOW(peak 7-9,decay 0.04-0.08,long opt wait), 50/50, regime hidden (only early slope leaks it)")
    print()
    print("--- mean net grounded payoff per arm (per seed) ---")
    hdr = "  seed    IMPULSIVE  PATIENT-5HT  ABL-FIXED  NEVERWAIT  PAT-SHUFFLE"
    print(hdr)
    for s in seeds:
        r = per[s]
        print(f"  {s}   {r['IMPULSIVE']:+8.4f}   {r['PATIENT-5HT']:+8.4f}   {r['ABL-FIXED']:+8.4f}  {r['NEVERWAIT']:+8.4f}   {r['PATIENT-SHUFFLE']:+8.4f}")

    def mean(key):
        return float(np.mean([per[s][key] for s in seeds]))

    imp = mean("IMPULSIVE"); pat = mean("PATIENT-5HT"); abl = mean("ABL-FIXED")
    nev = mean("NEVERWAIT"); shuf = mean("PATIENT-SHUFFLE"); shuf_imp = mean("IMPULSIVE-SHUFFLE")
    lift = pat - imp
    abl_lift = abl - imp
    beat_never = pat - nev
    shuf_edge = shuf - shuf_imp   # patient EDGE over impulsive on the SAME shuffled stream

    print()
    print("--- mean wait-ticks per arm (must-not-always-wait sanity) ---")
    wt = {k: float(np.mean([per[s]['_wait_ticks'][k] for s in seeds])) for k in per[seeds[0]]['_wait_ticks']}
    print(f"  IMPULSIVE={wt['IMPULSIVE']:.2f}  PATIENT-5HT={wt['PATIENT-5HT']:.2f}  ABL-FIXED={wt['ABL-FIXED']:.2f}  NEVERWAIT={wt['NEVERWAIT']:.2f}  (PATIENT must be strictly between)")

    print()
    print("=== (A) PRESENCE — PATIENT-5HT out-earns IMPULSIVE ===")
    a_pass = lift >= BAR_LIFT
    print(f"  PATIENT {pat:+.4f} − IMPULSIVE {imp:+.4f} = lift {lift:+.4f}  (≥{BAR_LIFT})  {'PASS' if a_pass else 'FAIL'}")
    seed_lifts = [per[s]['PATIENT-5HT'] - per[s]['IMPULSIVE'] for s in seeds]
    n_seed_pass = sum(1 for x in seed_lifts if x >= BAR_LIFT)
    a2_pass = n_seed_pass >= 2
    print(f"  per-seed lifts {[f'{x:+.4f}' for x in seed_lifts]}  ≥{BAR_LIFT} on {n_seed_pass}/3  (≥2/3)  {'PASS' if a2_pass else 'FAIL'}")

    print()
    print("=== (B) NOT-JUST-ALWAYS-WAIT — PATIENT beats the always-wait floor too ===")
    b_pass = beat_never >= BAR_BEAT_NEVER
    print(f"  PATIENT {pat:+.4f} − NEVERWAIT {nev:+.4f} = {beat_never:+.4f}  (≥{BAR_BEAT_NEVER})  {'PASS' if b_pass else 'FAIL'}")
    b2_pass = (wt['IMPULSIVE'] < wt['PATIENT-5HT'] < wt['NEVERWAIT'])
    print(f"  wait-ticks IMPULSIVE {wt['IMPULSIVE']:.2f} < PATIENT {wt['PATIENT-5HT']:.2f} < NEVERWAIT {wt['NEVERWAIT']:.2f}  (strictly between)  {'PASS' if b2_pass else 'FAIL'}")

    print()
    print("=== (C) EARNED ablate — fixed-γ (no 5-HT slope/regime read) loses ≥HALF the edge ===")
    c_margin = lift - abl_lift
    c_pass = c_margin >= BAR_ABL_FRAC * lift
    print(f"  ABL-FIXED edge {abl_lift:+.4f}  vs PATIENT edge {lift:+.4f}  →  margin {c_margin:+.4f}  (≥{BAR_ABL_FRAC}×lift={BAR_ABL_FRAC*lift:+.4f})  {'PASS' if c_pass else 'FAIL'}")
    frac_fixed = (100*abl_lift/lift) if lift != 0 else float('nan')
    print(f"  → fixed-γ captures {frac_fixed:.0f}% of the patient edge; adaptive-γ (5-HT regime read) carries {100-frac_fixed:.0f}%")

    print()
    print("=== (D) EARNED shuffle — permuted arrival-times collapse the patient edge ===")
    print(f"  shuffled stream: PATIENT {shuf:+.4f}  IMPULSIVE {shuf_imp:+.4f}")
    d_pass = (lift - shuf_edge) >= BAR_SHUF_FRAC * lift
    print(f"  PATIENT edge (real) {lift:+.4f}  →  patient edge (shuffled) {shuf_edge:+.4f}  →  collapse {lift - shuf_edge:+.4f}  (≥{BAR_SHUF_FRAC}×lift={BAR_SHUF_FRAC*lift:+.4f})  {'PASS' if d_pass else 'FAIL'}")

    print()
    overall = a_pass and a2_pass and b_pass and b2_pass and c_pass and d_pass
    faculty_present = a_pass and a2_pass and b_pass and b2_pass and d_pass
    if overall:
        vtag = "🟢 GREEN"
    elif faculty_present and not c_pass:
        vtag = "🟠 AMBER"
    else:
        vtag = "🧱 WALL"
    print(f"=== VERDICT: {vtag} (A∧A2∧B∧B2∧C∧D) ===")
    print(f"  A presence={a_pass} A2 per-seed={a2_pass} | B beat-never={b_pass} B2 between={b2_pass} | C ablate={c_pass} | D shuffle={d_pass}")
    if vtag == "🟢 GREEN":
        print(f"  GREEN reading (c9, frozen-first NO bar moved): under REGIME-SHIFTING horizon the substrate-")
        print(f"  ADAPTIVE 5-HT γ read now carries the MAJORITY of the edge ({100-frac_fixed:.0f}%) — a single fixed γ")
        print(f"  cannot serve both the FAST (short-wait) and SLOW (long-wait) regimes → bar C CLEARS. 5-HT-as-")
        print(f"  adaptive-discounting is a real MAJORITY faculty (Doya 2002: context-adaptive reward time-scale).")
    elif vtag == "🟠 AMBER":
        print(f"  AMBER reading (c9, frozen-first NO bar moved): the PATIENCE faculty is PRESENT+EARNED, but even")
        print(f"  under regime-shifting horizon a fixed γ STILL captures ≥half ({frac_fixed:.0f}%) → 5-HT-adaptive")
        print(f"  is genuinely a minority lever (honest, Miyazaki 2014 / Doya 2002).")

    import json
    out = {
        "hypothesis": "H_1540",
        "name": "serotonin-as-patience REGIME-SHIFTING-HORIZON retry of H_1538",
        "seeds": seeds,
        "params": {"T_TICKS": T_TICKS, "WAIT_COST": WAIT_COST, "GROUND_THR": GROUND_THR, "n_episodes": 400},
        "regime": {"mix": "50/50 FAST vs SLOW, hidden (early slope leaks it)",
                   "FAST": "rise_len 1-2, decay 0.14-0.22, short optimal wait",
                   "SLOW": "rise_len 7-9, decay 0.04-0.08, long optimal wait"},
        "means": {"IMPULSIVE": imp, "PATIENT-5HT": pat, "ABL-FIXED": abl, "NEVERWAIT": nev, "PATIENT-SHUFFLE": shuf, "IMPULSIVE-SHUFFLE": shuf_imp},
        "wait_ticks": wt,
        "fixed_gamma_captures_pct": frac_fixed,
        "bars": {
            "A_presence_lift": {"lift": lift, "bar": BAR_LIFT, "pass": bool(a_pass)},
            "A2_per_seed": {"n_pass": n_seed_pass, "bar": 2, "pass": bool(a2_pass)},
            "B_beat_neverwait": {"margin": beat_never, "bar": BAR_BEAT_NEVER, "pass": bool(b_pass)},
            "B2_wait_between": {"pass": bool(b2_pass)},
            "C_ablate": {"margin": c_margin, "bar": BAR_ABL_FRAC * lift, "pass": bool(c_pass)},
            "D_shuffle": {"patient_edge_shuffled": shuf_edge, "collapse": lift - shuf_edge, "bar": BAR_SHUF_FRAC * lift, "pass": bool(d_pass)},
        },
        "verdict": "GREEN" if overall else ("AMBER" if faculty_present else "WALL"),
        "faculty_present": bool(faculty_present),
        "directional": True,
        "note": "numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine R2 deferred ING; bars IDENTICAL to H_1538 (frozen-first)",
    }
    with open("H_1540_R1.json", "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("wrote H_1540_R1.json")


if __name__ == "__main__":
    main()
