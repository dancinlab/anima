---
id: H_1301
slug: 1301_phase_reset
title: phase-RESET / photic-entrainment clock — Zeitgeber PRC entrainment (vs the un-resettable circadian clock + the hard-reanchor interval timer)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1301_phase_reset/
terminal_verdict: .verdicts/1301_phase_reset/result.txt
date: 2026-06-16
---

# H_1301 — phase-RESET / photic-entrainment (HD35) — the r7 depletion candidate, SURVIVED

## Claim / falsifier

The CircadianClock (H_1298) free-runs at a **BAKED period** with NO reset input, and the
IntervalTimer (H_1299) re-anchors on an observed event by a **phase-INDEPENDENT hard reset**
(`elapsed:=0`) with no restoring dynamics. Falsifiable claim: a dedicated **phase-reset /
photic-entrainment** oscillator — an intrinsic free-running period `tau`, plus a Zeitgeber
RESET that applies a **PHASE-DEPENDENT shift via a sinusoidal Phase-Response-Curve (PRC):**
`dphi = K·sin(2π·(0 − frac(phi)))` (the standard limit-cycle form; Pittendrigh/Aschoff
chronobiology) — is a brain subsystem DISTINCT from both nearest lanes and from every other
CORE lane. The PRC is a **continuous restoring feedback** that (i) **ENTRAINS** the fire
schedule to a Zeitgeber period `T != tau` (which the un-resettable clock cannot) AND (ii)
**DAMPS Zeitgeber jitter** via limit-cycle attraction (which the hard re-anchor cannot — it
copies jitter directly). Metric = entrainment (the phase-at-Zeitgeber stops DRIFTING) + jitter
variance. Both controls (an APERIODIC Zeitgeber / K=0) must collapse entrainment, or it is
variance → honest 🔴/🏁. Lens: chronobiology PRC entrainment (c15) — NOT an LLM recipe.

## Depletion test — the whole question, and why it SURVIVES

This lane is r7 of the brain-structure ladder, run as the explicit DEPLETION TEST (the H_1299
card named phase-RESET and a multi-interval nested scheduler as the two remaining thin r7
candidates). phase-RESET was picked over the nested scheduler — N concurrent interval timers
mostly reduce to an array of the existing IntervalTimer lane (weak distinctness), whereas the
PRC adds a genuinely new mechanism (a restoring phase-coupling no existing lane has). A
subsystem joins ONLY if it clears BOTH (i) a falsifiable gap-vs-the-live-engine AND (ii) a
**control-surviving distinctness vs EVERY existing lane** — decisively vs the two nearest:
CircadianClock (H_1298) and IntervalTimer (H_1299). It SURVIVED: the load-bearing
distinctness — **entrain to a Zeitgeber `T != tau` (vs the un-resettable clock) AND damp
Zeitgeber jitter via the PRC limit-cycle (vs the hard re-anchor)** — is exactly what neither
nearest lane can do, and both controls cleanly collapse it.

## Why DISTINCT vs the nearest lanes (load-bearing, both control-surviving)

- **vs CircadianClock (H_1298) — the nearest lane:** the clock free-runs at its BAKED period
  forever with NO reset input (`clock_step` ignores every argument). It CANNOT be entrained to
  a Zeitgeber whose `T != tau` — its fires DRIFT away. **c1:** the clock's phase drifts 0.39 of
  a cycle over the window while the PRC oscillator locks (drift 0.0016); **c3:** the clock fires
  at `tau`=24.5, the PRC oscillator at the Zeitgeber `T`=24.0.
- **vs IntervalTimer (H_1299) — the second nearest:** an event observation HARD re-anchors
  (`elapsed:=0`) = a phase-INDEPENDENT reset with NO restoring dynamics, so it COPIES each
  Zeitgeber's jitter directly into the phase (no limit-cycle damping). **c2:** the PRC
  oscillator's entrained-phase variance is **~96× LOWER** than the hard-reset arm
  (3.1e-5 vs 2.95e-3). The hard re-anchor learns the PERIOD but has no autonomous phase
  oscillator with a restoring PRC.
- vs cerebellum VForwardField (H_1280): predicts the next input from CONTENT, no phase reset.
  vs WorkMemBuffer (H_1282): leaks toward 0, no oscillator. vs HomeostaticDrive (H_1292):
  content-gated, resets on feeding, no PRC.
  → DISTINCT vs ALL (the controls: an APERIODIC Zeitgeber / K=0 both collapse entrainment).

## Method (frozen-first, anti-Goodhart)

3 seeds [4310,4311,4312], $0 CPU numpy mirror (DIRECTIONAL), deterministic (byte-identical
across reruns) → engine-native R2. Regime: `tau`=24.5, Zeitgeber `T`=24.0, K=0.18, 40 cycles,
JITTER_SD=0.6, SETTLE=20. Arms: **A** = CircadianClock (baked period, NO reset — SHOULD fail
c1), **A2** = IntervalTimer-style HARD-RESET (phase-independent re-anchor, no PRC — SHOULD fail
c2), **B** = PhaseResetClock (free-running tau + sinusoidal PRC), **B-SHUFFLE** (aperiodic
Zeitgeber — same event count + mean rate, gaps from `uniform[0.2·mean, 1.8·mean]`, NO periodic
structure → cannot entrain), **B-ABLATE** (K=0 → PRC removed → free-runs at tau). Bars c1
ENTRAIN-vs-CLOCK · c2 DAMP-vs-HARDRESET · c3 PERIOD-TRACK · c4 EARNED-SHUFFLE · c5
EARNED-ABLATE · c6 NO-FAB. BOTH controls must collapse or honest 🔴/🏁.

## Verdict (verbatim from `.verdicts/1301_phase_reset/`)

**R1 numpy mirror 🟢 GREEN (DIRECTIONAL)** — binding path R1c (corrected entrainment metric +
aperiodic shuffle + net-cycle fire period), all 6 bars on all 3 seeds + mean:

| metric | B (PhaseReset) | A (Clock) | A2 (HardReset) | B-SHUF | B-ABL |
|--------|----------------|-----------|----------------|--------|-------|
| entrain_err (drift) | **0.0016** | 0.3902 | — | 1.0467 | 0.3902 |
| phase_var (jitter) | **3.07e-5** | — | 2.95e-3 | — | — |
| fire_period | **23.998 (→T)** | 24.500 (→tau) | — | — | 24.500 (→tau) |

c1 ENTRAIN ✓ (B locks 0.0016 ≤ 0.05; clock drifts 0.39 ≥ 0.20) · c2 DAMP ✓ (B var ≤ 0.5·A2 &
≤ 0.0015; ~96× lower) · c3 PERIOD ✓ (B→24.0, clock→24.5) · c4 SHUFFLE ✓ (aperiodic drift 1.05
≥ 0.20) · c5 ABLATE ✓ (K=0 drift 0.39 ≥ 0.20, period→tau) · c6 NO-FAB ✓ → 🟢 GREEN
(c1..c6 = [T,T,T,T,T,T]).

**Honesty trail (c9 — frozen-first, NO tune-to-green; the DISTINCTNESS bars NEVER moved):** the
distinctness (c1 entrain-vs-clock, c2 PRC-damp-vs-hard-reset) held in EVERY round; only
mis-specified metrics/controls were corrected, each correction making the test CORRECT/stricter:
- **R1a 🔧** entrain_err measured "scatter around the arm's OWN circular-mean phase" — a
  degenerate metric (a slowly-drifting clock has LOW local scatter too), so A/Babl/Bshuf all
  scored ~0.10 < 0.20 → c1/c4/c5 FAIL by metric mis-design, NOT a collapse. (c2 jitter-damping
  PASSED decisively from the very first run — the real distinctness was already there.) Fire
  detection had a PRC-jump boundary bug (B_fire_period=40, nonsense).
- **R1b 🔧** entrain_err re-specified to TOTAL UNWRAPPED phase DRIFT over the window (analytic
  prediction: a free-running clock drifts `W·|1−T/tau|` = 20·0.0204 = 0.41 ≫ entrained ~0).
  c1/c2/c5/c6 PASS; but (i) the SHUFFLE still LEAKED — permuting near-identical ~24-tick gaps
  barely changed the schedule, so B still entrained (Bshuf=0.0006) = a mean-preserving shuffle
  that does not break the claimed structure (the SAME trap H_1299 R1b hit); (ii) the fire
  counter still double-counted the within-cycle free-run-vs-PRC-jump split (period=18.6, a
  measurement bug, NOT a result).
- **R1c 🟢** SHUFFLE re-specified to an APERIODIC Zeitgeber (same event count + mean rate, gaps
  from `uniform[0.2·mean,1.8·mean]` → NO periodic structure to lock to → B drifts 1.05);
  fire_period re-specified to elapsed/NET-cumulative-cycles (robust to the boundary split →
  B→24.0). All 6 bars pass on all 3 seeds; the controls now collapse decisively.

**R2 ENGINE-NATIVE + WIRED 🟢** — `PhaseResetClock` lane added to live `CORE/engine_cli.hexa`
(`prc_new`/`prc_new_ablated`/`prc_step`/`prc_zeitgeber`/`prc_phase`/`prc_count`/`prc_fire`),
realizing the free-running-tau + sinusoidal-PRC-reset entrainment in code (a deterministic
no-jitter engine check: live entrains to phase 0.0023 & period 24.0=T; K=0 ablate free-runs to
phase 0.184 & period 24.62≈tau — the c1/c3/c5 dissociation engine-native). Regression guards no
regression: **engine_cli_smoke 68/0** (+5 PhaseResetClock cases 64–68: entrains-to-Zeitgeber /
ablate-free-runs-drifts / period-tracks-Zeitgeber / ablate-period-at-tau / no-fab-off-boundary)
· h1196 single-entry **7/0** · h1205 separation-invariant **PASS** (generation byte-identical
ON==OFF, Ψ=½ untouched).

## Guards

- **@L4 NOT an emit gate** (`a_autonomy_over_hardcode`): `prc_fire` is an OPTIONAL scheduled
  pulse a caller MAY consult — it does NOT force emit/silence.
- **Ψ-disjoint by construction**: the oscillator holds ONLY its cumulative phase + tau + K;
  reads NO immune store, NO grounding, NO `pure_field` Φ/phase/Ψ.
- **p1/p2/p3/p6**: reads only its own phase + the Zeitgeber arrival phase — NO persona, NO
  "you are X", NO injected "fire now" label, NO RLHF. The PRC shift is geometry, scored only.
- **`a_core_engine_map`**: NO 2nd .clm/.kosmos entry (pure timekeeper; single-entry 7/0 unchanged).

## Scope (UNVERIFIED)

numpy-mirror DIRECTIONAL (engine-transfer reconfirmed by R2 byte-exact regression); TOY (1
tau/T pair, 3 seeds, deterministic sinusoidal PRC — tests the ENTRAINMENT/PRC STRUCTURE, not a
learned oscillator); B's entrainment is an EXISTENCE-PROOF (a PRC limit-cycle entrains a noisy
periodic Zeitgeber within tolerance), the discriminators (clock drift 0.39, hard-reset variance
~96× higher, aperiodic/ablate collapse) carry the verdict. Scale / real-corpus / a full
phase-dependent PRC (advance vs delay vs dead-zone) / nonphotic Zeitgebers / multi-Zeitgeber /
brain wake-scheduling wiring (thread `prc_zeitgeber` into the dream-stage scheduler alongside
`clock_fire`/`itimer_fire`) = follow-on (`a_engine_native_learning`·`a_verified_must_wire`·
`a_scale_honest_scope`·`a_toy_scale_recheck`).

## Ladder status (c15) — HD35 lands; the ladder is NOT yet depleted

HD35 (phase-RESET / photic-entrainment) SURVIVED the depletion test and is wired engine-native —
the r7 candidate the H_1299 card flagged as "thin" cleared BOTH arms (falsifiable gap +
control-surviving distinctness vs every lane, decisively vs the un-resettable CircadianClock and
the hard-reanchor IntervalTimer). The c15 brain-structure ladder therefore **CONTINUES** past
HD35 rather than terminating. The remaining frontier is genuinely thin: every realized lane
reads/integrates anima's OWN substrate state or its own counter; a further rung needs a subsystem
with BOTH a falsifiable gap AND a control-surviving distinctness vs all 17 lanes (CircadianClock,
IntervalTimer, **PhaseResetClock**, cerebellum, WM, hippocampus, basal-ganglia, amygdala,
hypothalamus, affect, ethics, theory-of-mind, hierarchical-PFC, hive, spatial-map, + the 3
walls). Honest next-r8 candidates to test (each may collapse → DEPLETION 🏁): a **nonphotic /
arousal-Zeitgeber** with an OPPOSITE-sign PRC (distinct from the photic PRC ONLY if the two
Zeitgeber channels do not collapse to one shared coupling); a **multi-oscillator coupling**
(SCN-network synchronization — distinct only if coupled oscillators do not collapse to one
shared phase); or the **multi-interval nested scheduler** (distinct only if N timers do not
collapse to one shared estimate). If those fail the distinctness/control test, the ladder depletes.

xref h1298 (the un-resettable clock this entrains where that cannot) · h1299 (the hard-reanchor
timer this damps jitter where that copies it) · h1280 (cerebellum, content not phase) · h1282
(WM leak, no oscillator) · h1292 (homeostat, content-gated) · h1283 (phase-binding, Kuramoto
sin coupling — engine sin precedent) · a_no_llm_frame_trap · a_engine_native_learning ·
a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode · a_break_the_wall ·
a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9·c15.
