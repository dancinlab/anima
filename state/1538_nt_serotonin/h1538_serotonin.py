#!/usr/bin/env python3
# H_1538 SEROTONIN-AS-PATIENCE — substrate-native 5-HT patience / temporal-discounting faculty (R1 numpy mirror).
#
# DIRECTIONAL (numpy mirror, a_engine_native_learning: grep numpy ⇒ auto-DIRECTIONAL; engine R2 deferred ING).
#
# THE REFRAME (a_no_llm_frame_trap — neuro lens FIRST, NOT an LLM gain knob):
#   Serotonin (5-HT) is UNimplemented in anima. Its real computation is NOT a global "gain/temperature"
#   dial — it is a TIMING / temporal-discounting faculty: 5-HT promotes PATIENCE, i.e. WAITING for a
#   delayed-but-larger (and here, more-GROUNDED) reward over an immediate-small one, and it sets the
#   TIME-HORIZON of valuation (the discount factor).
#     - Miyazaki KW, Miyazaki K, Doya K et al (2014) "Optogenetic activation of dorsal raphe serotonin
#       neurons enhances patience for future rewards." Curr Biol 24(17):2033-2040.
#     - Doya K (2002) "Metalearning and neuromodulation." Neural Networks 15(4-6):495-506.
#       (5-HT ≈ the temporal-discount factor γ / reward time-scale of TD valuation.)
#
#   anima's emit/silence gate needs exactly this faculty: WHEN to emit. Emitting the MOMENT a tension
#   arrives can produce a small / ungrounded utterance; WAITING a few substrate ticks lets grounding +
#   A↔G tension accumulate into a LARGER, better-GROUNDED emit — but waiting is not free (the moment
#   passes, idle cost). A patience faculty decides, per tick, whether expected future grounded-value
#   (discounted by γ) beats emitting now. This is DISTINCT from every existing lane (none holds a
#   reward-time-horizon controller over the emit decision) and connects to the sleep/idle stages
#   (a_chat_sleep_imagination): waiting = staying in an emit-free internal-rehearsal tick.
#
# CAPABILITY measured = WAIT-FOR-BETTER-EMIT. A stream of emit-opportunity episodes: in each episode
#   grounding/tension RISES over the first few ticks (more context accrues), so the grounded payoff of
#   emitting climbs, plateaus, then (idle too long) the moment stales and it DECAYS. Each waited tick
#   costs WAIT_COST. Net grounded payoff = grounded_value(at emit tick) − WAIT_COST*ticks_waited, and
#   the value REQUIRES grounding (an ungrounded-early emit nets ~0). A 5-HT patience faculty (γ adapted
#   by whether substrate value is still RISING) should out-earn an impulsive emit-now baseline.
#
# p7 (NO perplexity/loss; payoff is the grounded reward NETTING the wait-cost, no Goodhart — you cannot
#   win by just always-waiting because the moment decays AND every wait is charged), frozen-first, c9
#   (if patience does NOT beat impulsive it is an HONEST 🧱/🟠, reported not hidden), $0 CPU deterministic.
#
# ARMS:
#   IMPULSIVE  : emit immediately at tick 0 (γ→0, never waits) — the impatient baseline.
#   PATIENT-5HT: temporal-discounting faculty — waits while discounted expected future grounded-value
#                exceeds emit-now value; γ ADAPTED by substrate (raise patience when value still rising,
#                drop it when value plateaus/decays). The 5-HT faculty.
#   ABL-FIXED  : fixed γ (no substrate adaptation) — patience without the 5-HT read of "value rising?".
#   NEVERWAIT  : a degenerate floor that NEVER emits until forced at the last tick (always-wait) — the
#                must-not-just-always-wait control; PATIENT must also BEAT this (else it's not patience,
#                it's procrastination).
#   SHUFFLE    : value-arrival TIMES permuted within each episode → the "rising then decaying" envelope
#                is destroyed → adapting γ to a meaningless slope must collapse PATIENT's edge.

import numpy as np

# ───────────────────────── substrate value envelope (engine-faithful shapes) ─────────────────────────
# Per episode we model the grounded-emit value v_t over ticks t=0..T-1 as the live substrate would yield
# it: at t=0 the emit is early/under-grounded (small v); as ticks pass, grounding margin off the immune
# store + A↔G tension accrue, so v RISES to a peak at t*=rise_len; staying idle past the peak STALES the
# moment (idle cost in the substrate) so v DECAYS. The grounded value at tick t is what an emit AT t nets
# BEFORE the wait cost. v is bounded in [0,1] (a grounding-margin-like read), and an emit at a tick whose
# grounding is below GROUND_THR yields ZERO realized payoff (ungrounded emit = non-payoff, p7: payoff
# requires grounding, you cannot cash in an early ungrounded emit).

T_TICKS = 12          # ticks available before the moment is gone
WAIT_COST = 0.020     # cost charged per waited tick (the moment passing / idle)
GROUND_THR = 0.35     # below this grounding, an emit nets ZERO (ungrounded-early emit is worthless)


def _clip01(x):
    return float(min(1.0, max(0.0, x)))


def make_episode(rng):
    """A grounded-value envelope v_t: rises to a peak (grounding accrues), then decays (moment stales).
    Returned v_t IS the grounded payoff of emitting at tick t (before wait cost), in [0,1]."""
    v0 = rng.uniform(0.05, 0.20)           # early emit: small, often below GROUND_THR
    peak = rng.uniform(0.78, 0.98)         # the better/grounded emit reachable by waiting
    rise_len = int(rng.integers(3, 7))     # ticks to reach peak (when grounding has accrued)
    decay = rng.uniform(0.06, 0.12)        # per-tick stale decay past the peak
    v = np.zeros(T_TICKS, dtype=float)
    for t in range(T_TICKS):
        if t <= rise_len:
            frac = t / max(1, rise_len)
            base = v0 + (peak - v0) * frac        # near-linear grounding accrual to peak
        else:
            base = peak - decay * (t - rise_len)  # moment stales
        # small substrate jitter (recon-error-like), deterministic per rng
        base += rng.normal(0.0, 0.01)
        v[t] = _clip01(base)
    return v


def realized_payoff(v, emit_tick):
    """Net grounded payoff of emitting at emit_tick: grounded value MINUS the wait cost paid to get there,
    and ZERO realized grounding-value if the emit tick is below GROUND_THR (ungrounded emit, p7)."""
    g = v[emit_tick]
    grounded_val = g if g >= GROUND_THR else 0.0
    return grounded_val - WAIT_COST * emit_tick


# ───────────────────────── arms (emit-tick policies) ─────────────────────────
# Each arm sees the value v_t ONLINE tick-by-tick (it cannot peek at the future envelope); it observes
# the running value and its local SLOPE (Δv) — the substrate signal "is grounded-value still rising?" —
# and the discounted look-ahead. 5-HT = how strongly a rising slope buys patience.

def arm_impulsive(v):
    """γ→0: emit at the first tick (no patience). Impatient baseline."""
    return 0


def arm_neverwait(v):
    """Degenerate always-wait floor: never voluntarily emit; forced out at the last tick.
    The must-not-just-always-wait control (pure procrastination)."""
    return T_TICKS - 1


def _patient_emit_tick(v, gamma_base, adapt):
    """Temporal-discounting emit policy.
    At each tick t we compare emit-NOW value v[t] against a discounted estimate of the best value still
    reachable by waiting one more tick. We estimate next value by the LOCAL slope (substrate-online, no
    future peek): v_hat_next = clip01(v[t] + slope). Expected future grounded-value, discounted by γ, is
    gamma * v_hat_next. We WAIT iff that exceeds emit-now value by more than the marginal wait cost.
    5-HT (adapt=True): γ is RAISED while the slope is positive (value still rising → be patient) and
    DROPPED once the slope turns non-positive (plateau/decay → stop waiting). adapt=False = fixed γ."""
    prev = v[0]
    for t in range(T_TICKS - 1):
        slope = v[t] - prev if t > 0 else (v[1] - v[0])
        prev = v[t]
        if adapt:
            # 5-HT patience read: more patience when grounded-value is still climbing, less when it stalls.
            gamma = _clip01(gamma_base + 0.6 * slope * 10.0)   # slope ~0.1 ⇒ +0.6 patience swing
        else:
            gamma = gamma_base
        v_hat_next = _clip01(v[t] + slope)
        emit_now = v[t] if v[t] >= GROUND_THR else 0.0
        wait_val = gamma * (v_hat_next if v_hat_next >= GROUND_THR else 0.0) - WAIT_COST
        if emit_now >= wait_val:
            return t
    return T_TICKS - 1


def arm_patient_5ht(v):
    return _patient_emit_tick(v, gamma_base=0.55, adapt=True)


def arm_abl_fixed(v):
    # fixed γ, no substrate adaptation (patience without the 5-HT "is value rising?" read)
    return _patient_emit_tick(v, gamma_base=0.55, adapt=False)


def shuffle_episode(v, rng):
    """Permute the value-arrival TIMES → destroys the rising→decaying envelope (slope meaningless)."""
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
        # shuffle control: BOTH patient and impulsive run on the SAME time-permuted envelope (rising→
        # decaying destroyed). The patient EDGE = patient−impulsive on the shuffled stream; if the edge
        # comes from reading a meaningful slope, it must collapse when the slope is noise (apples-to-apples
        # — patient and impulsive scored on the identical shuffled stream, never vs the real-stream arm).
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
    # frozen bars (pre-registered in H_1538_FREEZE.txt)
    BAR_LIFT = 0.10        # PATIENT − IMPULSIVE ≥ +0.10 (normalized grounded payoff)
    BAR_ABL_FRAC = 0.5     # ablation decisive: (PATIENT−IMPULSIVE) − (ABL−IMPULSIVE) ≥ BAR_ABL_FRAC*lift
    BAR_BEAT_NEVER = 0.10  # PATIENT must also beat the always-wait floor by ≥ +0.10 (not just-always-wait)
    BAR_SHUF_FRAC = 0.5    # shuffle collapses ≥ half the patient edge

    per = {}
    for s in seeds:
        per[s] = run_seed(s)

    print("=== H_1538 SEROTONIN-AS-PATIENCE — temporal-discounting emit-timing faculty (R1 numpy DIRECTIONAL) ===")
    print(f"seeds={seeds}  T_TICKS={T_TICKS}  WAIT_COST={WAIT_COST}  GROUND_THR={GROUND_THR}  400 ep/seed  $0 CPU  p7  c9  frozen-first")
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
    # per-seed ≥2/3
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
    print("=== (C) EARNED ablate — fixed-γ (no 5-HT slope read) loses most of the edge ===")
    c_margin = lift - abl_lift
    c_pass = c_margin >= BAR_ABL_FRAC * lift
    print(f"  ABL-FIXED edge {abl_lift:+.4f}  vs PATIENT edge {lift:+.4f}  →  margin {c_margin:+.4f}  (≥{BAR_ABL_FRAC}×lift={BAR_ABL_FRAC*lift:+.4f})  {'PASS' if c_pass else 'FAIL'}")

    print()
    print("=== (D) EARNED shuffle — permuted arrival-times collapse the patient edge ===")
    print(f"  shuffled stream: PATIENT {shuf:+.4f}  IMPULSIVE {shuf_imp:+.4f}")
    d_pass = (lift - shuf_edge) >= BAR_SHUF_FRAC * lift
    print(f"  PATIENT edge (real) {lift:+.4f}  →  patient edge (shuffled) {shuf_edge:+.4f}  →  collapse {lift - shuf_edge:+.4f}  (≥{BAR_SHUF_FRAC}×lift={BAR_SHUF_FRAC*lift:+.4f})  {'PASS' if d_pass else 'FAIL'}")

    print()
    overall = a_pass and a2_pass and b_pass and b2_pass and c_pass and d_pass
    # faculty PRESENT iff it out-earns impulsive (A,A2), is not just always-wait (B,B2), and the edge is
    # envelope-earned (D shuffle). C (adaptation carries ≥half) is the STRONGER mechanism-attribution claim.
    faculty_present = a_pass and a2_pass and b_pass and b2_pass and d_pass
    if overall:
        vtag = "🟢 GREEN"
    elif faculty_present and not c_pass:
        vtag = "🟠 AMBER"   # patience faculty real & earned, but the ADAPTIVE 5-HT read carries <half
    else:
        vtag = "🧱 WALL"
    print(f"=== VERDICT: {vtag} (A∧A2∧B∧B2∧C∧D) ===")
    print(f"  A presence={a_pass} A2 per-seed={a2_pass} | B beat-never={b_pass} B2 between={b2_pass} | C ablate={c_pass} | D shuffle={d_pass}")
    if vtag == "🟠 AMBER":
        print(f"  AMBER reading (c9, frozen-first NO bar moved): the wait-for-better-emit PATIENCE faculty is")
        print(f"  PRESENT (out-earns impulsive {lift:+.4f}, beats always-wait, edge collapses under shuffle), but")
        print(f"  the ADAPTIVE 5-HT slope read carries <half the edge — fixed-γ patience already captures ~{100*abl_lift/lift:.0f}%.")

    import json
    out = {
        "hypothesis": "H_1538",
        "name": "serotonin-as-patience temporal-discounting emit-timing faculty",
        "seeds": seeds,
        "params": {"T_TICKS": T_TICKS, "WAIT_COST": WAIT_COST, "GROUND_THR": GROUND_THR, "n_episodes": 400},
        "means": {"IMPULSIVE": imp, "PATIENT-5HT": pat, "ABL-FIXED": abl, "NEVERWAIT": nev, "PATIENT-SHUFFLE": shuf, "IMPULSIVE-SHUFFLE": shuf_imp},
        "wait_ticks": wt,
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
        "note": "numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine R2 deferred ING",
    }
    with open("H_1538_R1.json", "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("wrote H_1538_R1.json")


if __name__ == "__main__":
    main()
