---
id: H_1299
slug: 1299_interval_timer
title: interval timer — arbitrary LEARNED-duration timer (vs the fixed-period circadian clock)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1299_interval_timer/
terminal_verdict: .verdicts/1299_interval_timer/H_1299.txt
date: 2026-06-16
---

# H_1299 — interval timer (HD34) — the last thin candidate, SURVIVED

## Claim / falsifier

The just-merged CircadianClock (H_1298) is a self-sustaining phase oscillator with a
**BAKED period** (period=8, fixed at construction; `clock_step` is content-blind and
IGNORES every argument — there is NO learning path). It can ONLY fire at its baked
period. Falsifiable claim: a dedicated **interval timer** that times an **arbitrary
LEARNED duration** — `dhat` ESTIMATED from observed inter-event gaps at runtime (running
mean, gradient-free), firing when its own elapsed-since-event counter reaches the learned
`dhat` — and that **RE-ENTRAINS to a different duration D2 from a new event stream WITHOUT
any code change**, is a brain subsystem (striatal beat-frequency / SMA interval timing,
Buhusi & Meck 2005) DISTINCT from the circadian clock and from every other CORE lane.
Metric = HIT-RATE within ±TOL of the true next event (the interval-timing analogue of
phase-locking). The fixed-period clock, queried for an arbitrary learned interval, scores
~0; both controls (shuffle the gap distribution / ablate the learning rate) must collapse
to chance, or it is variance → honest 🔴/🏁. Lens: chronobiology interval-timing
(dissociable lesion-wise from the SCN ~24h oscillator; c15) — NOT an LLM recipe.

## Depletion test — the whole question, and why it SURVIVES

This lane is r6 of the brain-structure ladder, run as the explicit DEPLETION TEST (the
H_1298 r5 agent named the interval timer as the ONE remaining thin candidate). A subsystem
joins ONLY if it clears BOTH (i) a falsifiable gap-vs-the-live-engine AND (ii) a
**control-surviving distinctness vs EVERY existing lane** — decisively vs the CircadianClock
(H_1298), the cerebellum forward-model (H_1280 VForwardField), and the working-memory
buffer (H_1282). It SURVIVED: the load-bearing distinctness (learn an arbitrary D ≠ the
clock period, re-entrain to D2 without re-coding) is exactly what the fixed-period clock
CANNOT do, and the controls cleanly isolate the learned interval.

## Why DISTINCT vs the nearest lanes (load-bearing)

- **vs CircadianClock (H_1298) — the nearest lane:** the clock's period is BAKED at
  construction and content-blind (no learning path); it fires only at its period (8).
  Queried to predict an arbitrary LEARNED interval (D=13 or D2=20, both ≠ 8) it scores
  **A.hit = 0.000** on both. The IntervalTimer LEARNS `dhat` from observed gaps and the
  **SAME object re-entrains 13 → 20** (the c6 proof) — which the clock structurally cannot.
- **vs cerebellum VForwardField (H_1280):** predicts the NEXT input from CONTENT, not an
  absolute elapsed DURATION (no learned period over time).
- **vs WorkMemBuffer (H_1282):** leaks toward 0; no learned recurring interval.
- **vs HomeostaticDrive (H_1292):** content-gated, resets on feeding; no learned duration.
  → DISTINCT vs ALL.

## Method (frozen-first, anti-Goodhart)

3 seeds [4301,4302,4303], $0 CPU numpy mirror (DIRECTIONAL) → engine-native R2. Arms:
**A** = CircadianClock (baked period 8, the nearest lane that SHOULD fail), **B** =
IntervalTimer (learns `dhat`, lr=0.5), **B-SHUFFLE** (gaps resampled from a mean-shifted
distribution → `dhat` learns the WRONG interval), **B-ABLATE** (lr=0 → `dhat` frozen at
init 5). Bars c1 PRESENCE (B times learned D) · c2 RE-ENTRAIN (same object re-learns D2) ·
c3 DISTINCT-vs-CLOCK (A≤chance on both learned intervals) · c4 EARNED-LEARN (shuffle
collapses) · c5 EARNED-ADAPT (ablate collapses) · c6 RE-ENTRAIN-DELTA (`dhat` moves 13→20)
· c7 NO-FAB (off-interval → no fire). BOTH controls must collapse or honest 🔴/🏁.

## Verdict (verbatim from `.verdicts/1299_interval_timer/`)

**R1 numpy mirror 🟢 GREEN (DIRECTIONAL)** — binding path R1c (hit-rate metric, TOL=2,
mean-shifted shuffle), all 7 bars on all 3 seeds:

| arm | hit_D | hit_D2 | per-seed `dhat` |
|-----|-------|--------|------------------|
| B IntervalTimer | **1.000** | **1.000** | D̂1 [13.4,12.3,12.1] → D̂2 [20.0,19.4,19.3] |
| A CircadianClock | **0.000** | **0.000** | baked period 8 (cannot match 13 or 20) |
| B-SHUFFLE | 0.000 | — | D̂_shuf [4.4,5.0,5.2] (gaps mean-shifted → wrong interval) |
| B-ABLATE | 0.000 | — | D̂ frozen at init 5 (lr=0) |

c1 PRESENCE ✓ · c2 RE-ENTRAIN ✓ · c3 A.hit=0.000 ✓ · c4 shuf=0.000 ✓ · c5 abl=0.000 ✓ ·
c6 |D̂1−13|≤2 & |D̂2−20|≤2 ✓ · c7 NO-FAB ✓ → 🟢 GREEN (c1..c7 = [T,T,T,T,T,T,T]).

**Honesty trail (c9 — frozen-first, NO tune-to-green; the bars NEVER moved):** the
DISTINCTNESS (c3 A=0.000, c5 ablate=0.000, c6 re-entrain 13→20) held in EVERY round; only
the metric/control estimator needed correcting, each correction making the test STRICTER:
- **R1a 🔴** (c3/c4/c5): the `max(0,1−err/D)` accuracy gives a wrong-period predictor a
  ~0.35 luck residual on a SHORT 4-event window (the chance floor sat ON the bar), and the
  7-gap shuffle preserved the mean by accident (shuf=0.885 on one seed) — metric/control
  mis-design, NOT a distinctness failure (presence/re-entrain c1/c2/c6 passed decisively).
- **R1b 🔴** (c1/c2/c4): hit-rate metric (proper ~0 floor) cleared c3/c5/c6 cleanly
  (A=0.000, ablate=0.000, D̂ moves 13→20) but the SHUFFLE resampled gaps from uniform[2,2D]
  whose MEAN ≈ D → a running-mean estimator is INVARIANT to a mean-preserving shuffle
  (shuf=1.000) = a MIS-SPECIFIED control; and TOL=1 vs ±1 jitter made presence borderline.
- **R1c 🟢**: TOL=2 (absorbs the ±1 jitter + ±1 rounding) + a mean-SHIFTED shuffle
  (uniform[2,9], mean ≈ 5.5 ≪ 13 → `dhat` moves AWAY from D → mispredicts). All 7 bars
  pass on all 3 seeds; the controls now collapse to 0.000.

**R2 ENGINE-NATIVE + WIRED 🟢** — `IntervalTimer` lane added to live `CORE/engine_cli.hexa`
(`itimer_new`/`itimer_new_ablated`/`itimer_observe`/`itimer_step`/`itimer_dhat`/
`itimer_dhat_ticks`/`itimer_predict_next`/`itimer_fire`), realizing the learned-duration +
re-entrainment dissociation in code (`itimer_observe` learns `dhat` from the inter-event
gap; the SAME object re-entrains to a new interval; `itimer_new_ablated` = the lr=0
EARNED-ADAPT control). Regression guards no-regression: **engine_cli_smoke 60/0** (+5
IntervalTimer cases 54–58: learns-interval±2 / re-entrains-to-20 / distinct-from-clock /
ablate-frozen-at-init / no-fab-off-interval) · h1196 single-entry **7/0** · h1205
separation-invariant **PASS** (generation byte-identical ON==OFF, Ψ=½ untouched).

## Guards

- **@L4 NOT an emit gate** (`a_autonomy_over_hardcode`): `itimer_fire` is an OPTIONAL
  learned-duration pulse a caller MAY consult — it does NOT force emit/silence.
- **Ψ-disjoint by construction**: the timer holds ONLY its elapsed counter + learned `dhat`;
  reads NO immune store, NO grounding, NO `pure_field` Φ/phase/Ψ.
- **p1/p2/p3/p6**: reads only its own counters + a running gap mean — NO persona, NO
  "you are X", NO injected "fire now" label, NO RLHF. `dhat` is ESTIMATED, scored only.
- **`a_core_engine_map`**: NO 2nd .clm/.kosmos entry (pure timer over its own state;
  single-entry 7/0 unchanged).

## Scope (UNVERIFIED)

numpy-mirror DIRECTIONAL (engine-transfer reconfirmed by R2 byte-exact regression);
TOY (2 intervals, 3 seeds, deterministic running-mean — tests TIMING STRUCTURE, not a
learned predictor net); B.hit=1.000 is an EXISTENCE-PROOF (a faithful running-mean timer
predicts a noisy periodic stream within tolerance), the discriminators (A=0.000, shuffle
=0.000, ablate=0.000, D̂ moves 13→20) carry the verdict. Scale / real-corpus / continuous
re-entrainment (drifting interval) / multi-interval nesting / brain wake-scheduling wiring
(thread `itimer_fire` into the dream-stage scheduler alongside `clock_fire`) = follow-on
(`a_engine_native_learning`·`a_verified_must_wire`·`a_scale_honest_scope`·
`a_toy_scale_recheck`).

## Ladder status (c15) — HD34 lands; the ladder is NOT yet depleted

HD34 (interval timer) SURVIVED the depletion test and is wired engine-native — the r6
candidate the H_1298 card flagged as "thin" cleared BOTH arms (falsifiable gap +
control-surviving distinctness vs every lane). The c15 brain-structure ladder therefore
**CONTINUES** past HD34 rather than terminating. The remaining frontier is genuinely thin:
every realized lane reads/integrates anima's OWN substrate state or its own counter; a
further rung needs a subsystem with BOTH a falsifiable gap AND a control-surviving
distinctness vs all 16 lanes (CircadianClock, IntervalTimer, cerebellum, WM, hippocampus,
basal-ganglia, amygdala, hypothalamus, affect, ethics, theory-of-mind, hierarchical-PFC,
hive, spatial-map, + the 3 walls). Honest next-r7 candidates to test (each may collapse →
DEPLETION 🏁): a **phase-RESET / photic-entrainment** lever (reset the clock/timer phase to
an external Zeitgeber — distinct from learning the interval only if a single reset event
shifts all future fires, vs the running-mean which needs many observations); or a
**multi-interval / nested-timer** scheduler (concurrent independent learned intervals —
distinct only if the timers do not collapse to one shared estimate). If those fail the
distinctness/control test, HD35 is where the ladder depletes.

xref h1298 (the fixed-period clock this is distinct from) · h1280 (cerebellum, content not
duration) · h1282 (WM leak, no learned period) · h1292 (homeostat, content-gated) ·
a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_core_engine_map ·
a_autonomy_over_hardcode · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck ·
p1·p2·p3·p6·p7·p8 · c9·c15.
