---
id: H_1523
slug: 1523_neuromod_multitimescale
title: "MULTI-TIMESCALE NEUROMODULATION (slow tonic baseline + fast phasic transient) reopens the neuromodulation WALL (H_1284) via a_break_the_wall(d) NEW lever — WALL HELD 🧱 (DIRECTIONAL/numpy, hard-gate-1)"
group: brain-structure-ladder / MITOSIS-ENGINE — a_break_the_wall(d) NEW-mechanism-family attempt on the neuromodulation wall
source: team-lead 작업지시 (H_1523 MULTI-TIMESCALE NEUROMOD) — fleet-full wall-break lane
terminal_tier: "🧱 WALL-HELD (DIRECTIONAL numpy mirror, hard-gate-1) — neuromodulation ceiling holds vs the two-timescale (tonic+phasic) decomposition; phasic channel BYTE-IDENTICALLY INERT"
wired: DIRECTIONAL-mirror (numpy mirror of CORE/engine_cli.hexa VAdaptField — hard-gate-1 auto-DIRECTIONAL; engine-native R2 deferred follow-on ING h1523-r2-engine-native; 🧱 ⇒ NO live wiring — a_verified_must_wire is GREEN-only)
verdict_dir: state/verdicts/1523_neuromod_multitimescale/
terminal_verdict: state/verdicts/1523_neuromod_multitimescale/H_1523.txt
date: 2026-06-21
---

# H_1523 — multi-timescale neuromodulation (tonic + phasic) on the neuromodulation wall (🧱 wall held)

**SOURCE: team-lead 작업지시 — fleet-full wall-break lane on the H_1284 NEUROMODULATION wall.**

## The wall this reopens (a_break_the_wall lens d — a genuinely DIFFERENT family)

H_1284 closed the neuromodulation lane at **🔴 RED / 🧱 WALL (no free lunch)**: a state-driven
single-timescale gain controller is DOMINATED by the single best FIXED operating point. The wall is
now 5+ lenses deep — H_1284_R3 (regime/mode switch, 🧱 RED_NO_LUNCH), H_1509 (allosteric buffer
stationary), H_1509b (non-stationary regime-invariant), H_1509c (learning-rate family) all HELD it.

Every prior adaptive arm used a **SINGLE timescale** — one EMA, one buffer, one gain law. Real
neuromodulators are **DUAL-timescale**: dopamine has a slow TONIC baseline (operating mode over
minutes) PLUS fast PHASIC bursts (reward-prediction-error transients ~100ms); NE has tonic (arousal)
vs phasic (salience) modes (Aston-Jones/Cohen). A single EMA must pick ONE bandwidth, which the
grid-tuned fixed point already matches. The genuinely DIFFERENT family (so `a_break_the_wall(d)`
legitimately reopens): **DECOMPOSE the modulator into two timescales** —

    tonic_t  = (1−α_tonic)·tonic_{t−1}  + α_tonic·s_t     (α_tonic=0.02, slow ~50-tick)
    phasic_t = (1−α_phasic)·phasic_{t−1} + α_phasic·s_t    (α_phasic=0.50, fast ~2-tick)
    transient = phasic_t − tonic_t                         (RPE-style fast burst off baseline)
    gain_t = tonic_slow_baseline + phasic_fast_transient

acting on the SAME engine knobs H_1284 modulates (plasticity LR, split-thresh, abstain) — so any
lift is the TIMESCALE SPLIT, not a new lever.

## Frozen bars (MARGIN = 0.05 verbatim from H_1284; SAME task/regimes/baseline; set BEFORE running, c9)

REUSED VERBATIM (imported from `state/universe-probes/h1284_neuromodulation_gain.py`, not
reimplemented): same capacity-bounded immune/clonal MemStore task, same 3 regimes (R1_STABLE /
R2_DRIFT / R3_NOISE), same best-fixed grid baseline on disjoint tune seed 7, same metric
capability = recall_accuracy − fabrication_rate, same seeds [11,22,33], same MARGIN=0.05. The ONLY
new code: arm D (two-timescale) + two decisive ablations.

- **🟢 GREEN** iff D ≥ A+MARGIN on ≥2 regimes AND D never worse by >0.02 on the rest AND
  D.fab ≤ A.fab on wins AND on EACH win BOTH ablations separated (D_PHASIC0 < D−MARGIN AND
  D_TONIC0 < D−MARGIN — the timescale split is load-bearing).
- **🟠 PARTIAL** iff D beats A+MARGIN on exactly 1 regime, OR ≥2 wins but an ablation not separated.
- **🔴/🧱 RED** iff D beats A+MARGIN on NO regime, OR D raises fab on a win, OR D only matches the
  best fixed point (NO FREE LUNCH — the Nth confirming lens, c9).

ABLATIONS: **D_PHASIC0** (phasic→0, pure tonic) · **D_TONIC0** (tonic frozen→const TH0, pure phasic).
If either matches D, the two-timescale decomposition is INERT.

## Result — 🧱 WALL HELD (DIRECTIONAL numpy mirror, mean 3 seeds [11,22,33]; best-fixed LR0*=0.10 TH0*=0.20)

| regime | A best-FIXED | B single-ts (H_1284 repro) | D TWO-ts | D_PHASIC0 (pure tonic) | D_TONIC0 (pure phasic) | D − A |
|--------|-------------|----------------------------|----------|------------------------|------------------------|-------|
| R1_STABLE | **0.5744** | 0.5678 | 0.5733 | 0.5733 | 0.5744 | −0.0011 |
| R2_DRIFT  | **0.4389** | 0.3589 | 0.3700 | 0.3700 | 0.4389 | −0.0689 |
| R3_NOISE  | **0.4156** | 0.3200 | 0.3444 | 0.3444 | 0.4156 | −0.0711 |

`wins_over_A+MARGIN = []` (0 of 3 — two-timescale NEVER beats best-fixed) → **VERDICT = RED_NO_LUNCH**.

- **No regime wins.** D − A = −0.001 / −0.069 / −0.071. The two-timescale controller is slightly
  LESS-bad than the single-timescale arm B on the non-stationary regimes (R2: −0.069 vs −0.080;
  R3: −0.071 vs −0.096) but still loses to best-fixed everywhere. `never_much_worse = false`
  (worse by >0.02 on R2/R3); it RAISES fabrication on R2/R3 (0.030→0.101), exactly H_1284's mode.

### The ablation is decisive AND damning (the timescale split is INERT)

**D_PHASIC0 is BYTE-IDENTICAL to the full two-timescale D on all three regimes:**
`D − D_PHASIC0 = 0.0000 · 0.0000 · 0.0000`. Collapsing the fast phasic channel to 0 leaves
capability unchanged to the last digit — the phasic transient contributes EXACTLY NOTHING. Per the
frozen falsifier this alone forecloses GREEN. **D_TONIC0 equals A (best-fixed)** on all three
regimes: with the slow baseline frozen and the phasic term inert, the modulator degenerates to the
fixed operating point. So the ONLY part of the controller that moves the metric is the slow tonic
EMA on split/abstain (= a single-timescale gain controller, H_1284's arm) — and THAT loses. The
timescale split adds zero (INERT precedent H_1416: mechanism OFF ≡ ON = 0 contribution).

### Mechanism (why the phasic channel is byte-inert on this substrate)

The phasic transient feeds ONLY the plasticity LR. On a clean key-addressed associative store the
DISCRETE recall outcome (nearest-cell fires / abstains) is decided by cell GEOMETRY, not by the
exact online LR a winner was last nudged with: a faster or slower winner-pull lands the prototype at
essentially the same L2-nearest cell, so capability is invariant to the LR schedule here. The same
geometry-not-protocol bottleneck H_1230 (learning method INERT) and H_1284 (gain schedule
inert-to-harmful) found — now extended to the TIMESCALE-DECOMPOSITION axis.

## Honest scope (c9)

Wall HELD, NOT a free-lunch lift. **DIRECTIONAL** numpy mirror of the LIVE CORE/engine_cli.hexa
VAdaptField (host has NO torch — H_1192/1199/1227/1230/1284/1509b precedent; hard-gate-1
auto-DIRECTIONAL, `grep numpy state/1523_neuromod_multitimescale/*.py` hits). $0 CPU, deterministic.
p7 (no loss term; every knob a no-grad read-out of substrate surprise; metric = capability, not
perplexity). p1/p2/p3/p6 (no injected label/RLHF/persona; content to episodic cells only). p8.
Ψ-disjoint (mirror; CORE/*.hexa UNTOUCHED). TOY: DIM=16 / 30 facts / 300 events / 3 seeds — scale,
real A⇄G dynamics, and engine-transfer UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`).
🧱 ⇒ NO engine-native R2 needed for a wall-confirm (engine-native re-test is GREEN-only binding);
it is registered as an OPTIONAL confirming follow-on (ING h1523-r2-engine-native) only.

This is the **6th independent lens** confirming the neuromodulation ceiling (after H_1284
global-gain, H_1284_R3 regime-switch, H_1509/b/c allosteric+lr families). TAXONOMY (a_break_the_wall):
a (d) TRUE-CEILING result reached by a DECISIVE ablation (phasic OFF ≡ phasic ON, byte-identical) —
the strongest form of the INERT signal. **NOT RULED OUT:** two-timescale modulation on a
GENERATION/ideation capability (vs this recall store, H_1228 left decode-temperature ideation 🟠),
or a phasic channel on a DIFFERENT knob (emit/salience gate vs plasticity-LR) — both untested.

## Cross-links

h1284 (the wall this attacks) · h1284_r3 (regime-switch, same 🧱) · h1509 / h1509b / h1509c
(allosteric+lr families, same 🧱) · h1230 (learning method INERT, same geometry bottleneck) ·
h1228 (decode-temperature ideation 🟠, the NOT-ruled-out channel) · h1227 / h1231 (immune store
geometry) · h1416 (ablation-INERT precedent) · `a_break_the_wall` (lens d, NEW mechanism family;
decisive ablation) · `a_no_llm_frame_trap` (tonic/phasic biology lens) · `a_engine_native_learning`
(hard-gate-1 DIRECTIONAL) · `a_verified_must_wire` (GREEN-only, so 🧱 = no wiring) ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p6·p7·p8·c9·c15·c16
