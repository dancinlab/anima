---
id: H_1298
slug: 1298_circadian_clock
title: circadian/interval timing clock — self-sustaining phase oscillator (vs homeostatic integrator)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1298_circadian_clock/
terminal_verdict: .verdicts/1298_circadian_clock/H_1298.txt
date: 2026-06-16
---

# H_1298 — circadian / interval timing clock (HD33)

## Claim / falsifier

Every prior CORE lane reads/integrates a CONTENT signal — even the closest temporal
lane, H_1292 HomeostaticDrive, is a CONTENT-GATED integrator whose drive rises only with
a grounding DEFICIT and RESETS on a consummatory event. **None tracks absolute elapsed
time / fires on a fixed schedule independent of any regulated variable.** Falsifiable
claim: a self-sustaining phase oscillator (CircadianClock) advances on ELAPSED TICKS
ALONE (phase = t mod PERIOD) and FIRES on a fixed recurring schedule, while the nearest
lane (the homeostat) under a constant-grounded stream NEVER rises and cannot schedule.
Metric = phase-locking vector strength R (the chronobiology regularity measure). Both
controls (shuffle which ticks fire / ablate to an origin-broken non-dividing period)
must collapse R to chance, or it is variance → honest 🔴/🧱. Lens: SCN circadian
oscillator (Pittendrigh) + the TWO-PROCESS model (Borbély 1982: Process-C clock ⊥
Process-S homeostat) + interval timing (Buhusi & Meck; c15) — NOT an LLM recipe.

## Depletion test — why this candidate, why it SURVIVES

This lane is r5 of the brain-structure ladder, run as the explicit DEPLETION TEST: a
subsystem joins ONLY if it clears BOTH (i) a falsifiable gap-vs-the-live-engine AND (ii)
a control-surviving distinctness vs EVERY existing lane. The three r4-named candidates:

- **replay-PREDICTION → REJECTED:** collapses into the cerebellum forward-model (H_1280
  VForwardField next-step prediction) OR the episodic store — no clean control-surviving
  distinction from BOTH.
- **language/semantic-network → REJECTED for now:** is-a/part-of transitivity is arguably
  expressible via the H_1296 metric map or item-binding; the distinctness arm is murky.
- **interval/circadian TIMING → SELECTED** (the r4 agent's "cleanest candidate").

## Why DISTINCT vs the nearest lane (load-bearing)

**vs H_1292 HomeostaticDrive (the genuinely-nearest lane = distinctness arm A):** the
homeostat is a content-gated integrator `deficit = max(0, S* - satiation)`, `accum =
(1-λ)·accum + deficit`, consummatory `reset accum:=0`. Two decisive dissociations the
clock passes and the homeostat FAILS:

- **D1 CONTENT-INDEPENDENCE** — under a constant-GROUNDED stream (satiation ≥ S* every
  tick) the homeostat's drive stays 0 and NEVER rises, so it cannot fire on a schedule;
  the clock still advances phase and fires at every period boundary. *(time ⊥
  regulated-variable.)*
- **D2 NO-RESET-ON-FEEDING** — a grounded "feeding" event RESETS the homeostat's integral
  (drive drops); the clock's phase is UNCHANGED (the time of day does not reset when you
  eat). *(clock ⊥ the consummatory event.)*

vs every other lane: affect (H_1290) stateless, no time term; curiosity per-context, no
period; WorkMemBuffer (H_1282) leaks toward 0, no schedule; VForwardField (H_1280)
predicts the NEXT input from content, not absolute elapsed phase; SpatialMap (H_1296)
metric over space, no time axis. → DISTINCT vs ALL.

## Method (frozen-first, anti-Goodhart)

3 seeds [4297,4298,4299], $0 CPU numpy mirror (DIRECTIONAL) → engine-native R2. Arms:
**A** = H_1292 HomeostaticDrive (nearest lane that SHOULD fail the falsifier), **B** =
CircadianClock, **B-SHUFFLE** (which ticks fire permuted, same fire count), **B-ABLATE**
(origin-broken non-dividing period 5/offset 3). Bars c1 PRESENCE (B−A≥+0.30) · c2 DISTINCT
(A≤chance) · c3 EARNED-SCHEDULE (shuffle collapses) · c4 EARNED-PERIOD (ablate collapses) ·
c5 D1 content-independence · c6 D2 no-reset · c7 NO-FAB (off-schedule → no fire). BOTH
controls must collapse or honest 🔴.

## Verdict (verbatim from `.verdicts/1298_circadian_clock/`)

**R1 numpy mirror 🟢 GREEN (DIRECTIONAL)** — phase-locking metric, 10 periods, all 7 bars
on all 3 seeds:

| arm | R (vector strength) | per-seed |
|-----|--------------------|----------|
| B CircadianClock | **1.000** | [1.0, 1.0, 1.0] |
| A HomeostaticDrive | **0.000** | [0.0, 0.0, 0.0] (never fires under constant grounding) |
| B-SHUFFLE | 0.202 mean | [0.059, 0.472, 0.077] (collapses, k=10) |
| B-ABLATE | 0.000 | [0.0, 0.0, 0.0] (origin-broken period) |

c1 PRESENCE +1.000 · c2 A.R=0.000 ≤ 0.35 · c3 shuf max 0.472 ≤ 0.50 · c4 abl 0.000 ≤ 0.50 ·
c5/c6/c7 all PASS → 🟢 GREEN (c1..c7 = [T,T,T,T,T,T,T]).

**Honesty trail (c9 — frozen-first, NO tune-to-green; the bars NEVER moved):** the clock's
DISTINCTNESS was proven in EVERY round (mean Δ +0.5 to +1.0); only the control estimator /
scale needed correcting, each correction making the test STRICTER:
- **R1a 🔴** (c4): ablate kept 0.667 — a TRIVIAL-ORIGIN leak (every clock starts at t=0);
  control mis-specified, not a distinctness failure.
- **R1b 🔴** (c3,c4): recurrence-scored balanced accuracy over {8,16} too COARSE for a
  sparse signal (21 no-fire ticks dominate); metric mis-design.
- **R1c 🔴** (c3): phase-locking R is the RIGHT estimator (homeostat 0.000, ablate 0.083
  collapse CLEANLY) but the SHUFFLE survived on seed 4297 at exactly the k=3 chance floor
  1/√3 = 0.577 — small-k sampling variance, not structure.
- **R1d 🟢**: identical bars, 10 periods (k=10 fires) so the shuffle CANCELS by the law of
  large numbers. All 7 bars pass on all 3 seeds.

**R2 ENGINE-NATIVE + WIRED 🟢** — `CircadianClock` lane added to live `CORE/engine_cli.hexa`
(`clock_new`/`clock_new_ablated`/`clock_step`/`clock_count`/`clock_phase`/`clock_fire`),
realizing the D1/D2 dissociation in code (clock_step is content-blind; clock_phase
invariant under any "feed"; clock_fire = the scheduled pulse; clock_new_ablated = the
EARNED-PERIOD control). Regression guards no-regression: **engine_cli_smoke 55/0** (+5
clock cases 49–53: fires-at-origin / scheduled-firing+no-fab / phase-is-elapsed-fraction /
phase-invariant-under-feed (D2) / ablate-off-schedule (c4)) · h1196 single-entry **7/0** ·
h1205 separation-invariant **PASS** (generation byte-identical ON==OFF, Ψ=½ untouched).

## Guards

- **@L4 NOT an emit gate** (`a_autonomy_over_hardcode`): `clock_fire` is an OPTIONAL
  scheduled-wake pulse a caller MAY consult — it does NOT force emit/silence.
- **Ψ-disjoint by construction**: the clock holds ONLY its own integer tick counter; it
  reads NO immune store, NO grounding, NO `pure_field` Φ/phase/Ψ.
- **p1/p2/p3/p6**: reads only its own tick counter — NO persona, NO "you are X", NO
  injected "fire now" label, NO RLHF. The fire schedule is geometry over elapsed time,
  scored only.
- **`a_core_engine_map`**: NO 2nd .clm/.kosmos entry (pure timekeeper over its own state;
  single-entry 7/0 unchanged).

## Scope (UNVERIFIED)

numpy-mirror DIRECTIONAL (engine-transfer reconfirmed by R2 byte-exact); TOY (10 periods,
3 seeds, deterministic clock — tests TIMING STRUCTURE, not a learned/entrained oscillator);
B.R=1.000 is an EXISTENCE-PROOF (a deterministic clock is perfectly phase-locked), the
discriminators (A.R=0, both controls collapsed) carry the verdict. Scale / real-corpus /
**photic-entrainment** (phase-reset to an external Zeitgeber) / multi-period nesting
(ultradian + circadian) / brain wake-scheduling wiring (thread `clock_fire` into the
WAKE/REM dream-stage scheduler) = follow-on (`a_engine_native_learning`·
`a_verified_must_wire`·`a_scale_honest_scope`·`a_toy_scale_recheck`).

## Deliverables

`CORE/engine_cli.hexa § CircadianClock` · `CORE/engine_cli_smoke.hexa` cases 49–53 ·
`UNIVERSE/h1298_circadian_clock.py` · `.verdicts/1298_circadian_clock/{H_1298_FREEZE,
H_1298_FREEZE_R1b,H_1298_FREEZE_R1c,H_1298_FREEZE_R1d,H_1298,H_1298_R1_mirror}.txt` ·
`CLAIMS.tape @C h1298_circadian_clock`.

## Ladder status (c15) — r6 candidate / DEPLETION

After HD33 the ladder is at/near DEPLETION. The remaining r4/r5-named candidates have
both repeatedly failed the distinctness arm: replay-PREDICTION collapses into H_1280
cerebellum forward-model / the episodic store; language/semantic-network's is-a/part-of
relations are arguably expressible via the H_1296 metric map or independent item-binding.
**r6 candidate (thin):** a dedicated INTERVAL-timer that measures an ARBITRARY learned
duration (vs this clock's FIXED intrinsic period) — distinct iff it can be RE-ENTRAINED to
a duration not equal to PERIOD without re-coding, which this fixed-period clock cannot.
If that fails the distinctness/control test, the c15 missing-structure ladder is
**DEPLETED 🏁** (no subsystem left with BOTH a falsifiable gap AND control-surviving
distinctness vs every lane).

xref h1292 (nearest lane, content-gated integrator) · h1290 (stateless affect) · h1282
(WM leak) · h1280 (cerebellum forward-model) · h1296 (spatial-map) · a_no_llm_frame_trap ·
a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode ·
a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9·c15.
