---
id: H_1509
slug: 1509_allosteric_buffer
title: "ALLOSTERIC-BUFFER — tension-gated resistance-to-deviation (external proposal, Amoeba Protocol μ_t) reopens the neuromodulation WALL (H_1284) via a_break_the_wall(d); engine-native — WALL HELD 🧱"
group: brain-structure-ladder / MITOSIS-ENGINE — a_break_the_wall(d) NEW-lever attempt on the neuromodulation wall
source: external proposal — Amoeba Protocol (@qingkong66) μ_t allosteric buffer
terminal_tier: "🧱 WALL-HELD (engine-native, byte-exact to R1 mirror) — neuromodulation ceiling holds vs the buffering/resistance lever"
wired: engine-native (§AllostericBuffer ops LIVE in core/engine_cli.hexa + 5 smoke cases 318-322; 🧱 ⇒ NO live emit/decision wiring — a_verified_must_wire is GREEN-only)
verdict_dir: state/verdicts/1509_allosteric_buffer/
terminal_verdict: state/verdicts/1509_allosteric_buffer/R2_engine_native.txt
date: 2026-06-21
---

# H_1509 — allosteric buffer μ_t (Amoeba Protocol) on the neuromodulation wall (🧱 wall held)

**SOURCE: external proposal — Amoeba Protocol (@qingkong66), the μ_t allosteric buffer.**

## The wall this reopens (a_break_the_wall lens d)

H_1284 closed the neuromodulation lane at **🔴 RED / 🧱 WALL (no free lunch)**: a state-driven
neuromodulator that modulates a GLOBAL GAIN against a FIXED operating point is DOMINATED by the
single best fixed operating point. H_1422 (3 state-contingent lenses, each shuffle+ablation) and
H_1425 (orthogonal ideation-temperature channel) both confirmed the ceiling as STRUCTURAL — "a
single tuned fixed point dominates the controller."

The proposal is a genuinely DIFFERENT lever (so per `a_break_the_wall(d)` it legitimately reopens
the wall): do NOT modulate global gain on an operating point — modulate the **RESISTANCE-to-
DEVIATION** from the fixed point Ψ=1/2. Let τ_t = |A−G| = the live A⇄G tension (the emit/silence
balance; Ψ=1/2 ideal). The allosteric modulator

    μ_t = 1 + λ · (1 − exp(−(τ_t − 0.5)² / (2σ²)))

acts as a biochemical buffer (like bicarbonate defending blood pH): μ≈1 near the fixed point (no
extra resistance when balanced), μ→1+λ on large excursions — tightening the restoring force ONLY
when tension drifts far from Ψ=1/2.

## Frozen bars (MARGIN = 0.05 verbatim from H_1284; set BEFORE running, c9, no tune-to-green)

RMS(arm) = sqrt(mean_t (b_t − 0.5)²) under a fixed perturbation (sinusoid amp 0.30 period 17 + a
held step shock +0.35 at t=100 for 20 ticks), lower = tighter defense of Ψ=1/2. 3 seeds, deterministic.

- **(A WALL-CROSS)** μ defends Ψ=1/2 better than the BEST swept fixed gain: RMS(A) − RMS(B) ≥ 0.05.
- **(B vs BASELINE)** RMS(B) < RMS(A) on all 3 seeds (the walled global-gain approach is ARM A).
- **(C EARNED ablate λ=0)** μ≡1 collapses to the global gain @g0 (|RMS(C)−gain@g0| ≤ 0.01) AND the
  buffer is load-bearing vs its base (RMS(C) − RMS(B) ≥ 0.05).
- **(D EARNED shuffle)** permuting τ→μ decorrelates the defense: RMS(D) − RMS(B) ≥ 0.05.

WALL-BROKEN 🟢 iff A∧B∧C∧D · otherwise WALL-HELD 🧱 (honest multi-lens confirmation, c9).

## Result — 🧱 WALL HELD (engine-native, byte-identical to the R1 mirror, mean 3 seeds [1509/1510/1511])

| arm | RMS (mean) | meaning |
|-----|-----------|---------|
| A best swept FIXED gain | **0.2680** (g*=0.80) | the H_1284 strongest baseline |
| B allosteric μ (g0=0.40) | **0.2741** | the buffer — does NOT beat A |
| C ablate λ=0 (== gain@g0) | 0.3827 | μ≡1 collapse |
| D shuffle τ→μ | 0.3002 | coupling broken |

- **(A WALL-CROSS) FAIL** — RMS(A)−RMS(B) = **−0.0061** < 0.05. **B does NOT cross the bar the
  global-gain lever could not.** The wall holds.
- **(B vs BASELINE) FAIL** — RMS(B) > RMS(A) on all 3 seeds: the best swept fixed gain (g=0.80)
  dominates the buffer, exactly as H_1284 predicts.
- **(C EARNED ablate) PASS** — λ=0 collapses to gain@g0 (|Δ|=0.0000) AND the buffer is load-bearing
  vs that base (+0.109). So the buffer IS a real, coupled mechanism — it does something.
- **(D EARNED shuffle) FAIL (sub-margin)** — shuffle hurts B by only +0.026 (< 0.05). The τ→μ
  coupling has SOME teeth but is too weak to break the wall.

### The honest finding (gain-matched diagnostic, non-gating, c9)

The buffer's allosteric SHAPE — concentrating resistance on large excursions — DOES beat a
**gain-matched** uniform fixed gain by +0.026 (RMS_B 0.2741 vs gain-matched 0.2997). So the shape
is genuinely a better-positioned controller *per unit of restoring effort*. **But** (i) that
advantage is sub-margin (<0.05), and (ii) it is DOMINATED outright by simply turning the uniform
fixed gain up to g=0.80 (RMS 0.2680). This is H_1284's structural result reproduced on a NEW lever:
the controller has real coupling, yet **a single tuned fixed point still wins.** The buffer's
average effective gain (0.69) is merely a worse-positioned fixed gain than the best swept one.

## Measurement-validity note (a_break_the_wall taxonomy (a), bar UNMOVED)

The first R1 roll had a SIGN error (b+d−restoring → anti-restoring → clamp-saturated degenerate
oscillation). Corrected to b+d+g·μ·(0.5−b) so the force actually DEFENDS Ψ=1/2 — a measurement fix,
NOT tune-to-green (metric, MARGIN=0.05, arm definitions, A=best-swept-gain, verdict logic all
unchanged). With corrected dynamics the test is non-degenerate (RMS 0.27–0.38, off the clamp).

## Engine-native wiring (R2)

§AllostericBuffer ops LIVE in `core/engine_cli.hexa` — `allo_mu` (the buffer), `allo_defend`
(roll the balance, read live τ, return RMS; mode_shuf=1 = ARM D), `allo_best_fixed_gain` (ARM A
grid sweep). Ψ-disjoint by construction (owns only its own scalar balance; NEVER touches
pure_field's Φ/phase/Ψ; READ-ONLY over every other faculty; returns a stability scalar, never an
emit decision — a_autonomy_over_hardcode, a_core_engine_map). Re-scored byte-exact via
`core/engine_cli_smoke.hexa` cases 318-322 (full smoke 0 fail, deterministic ×3). 🧱 ⇒ NO live
emit/decision wiring (a_verified_must_wire is GREEN-only; the Ψ field stays substrate-decided).
ARCHITECTURE.json §AllostericBuffer node added in lockstep.

## Honest scope (c9)

Wall HELD, NOT a free-lunch lift. Engine-native (LIVE §AllostericBuffer ops, byte-identical to R1
mirror), $0 CPU, deterministic run1==run2. p7 (no loss; pure deterministic dynamics; the bar is
the RMS excursion, not perplexity). p1/p2/p3/p6 (no injected label/RLHF/persona; the buffer reads
only the live tension scalar). p8. Ψ-disjoint. TOY: 200 ticks / 1 perturbation schedule / 3 seeds
/ 1-D balance scalar — scale, real A⇄G emit dynamics, alternative perturbation spectra, and
engine-transfer to the live emit loop are UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`).
This is the FOURTH independent lens to confirm the neuromodulation ceiling (after H_1284 global-gain,
H_1422 three state-contingent lenses, H_1425 orthogonal ideation-temperature) — a strong multi-lens
WALL. NOT RULED OUT: a buffer conditioned on a signal genuinely ORTHOGONAL to the balance axis (a
cross-faculty context the restoring force cannot already see) remains untested — but on this single
Ψ-stability axis no such orthogonal live signal exists (τ IS the axis the buffer defends).

## Cross-links

h1284 (the wall this attacks) · h1422 (3 state-contingent lenses, same 🧱) · h1425 (orthogonal
ideation-temperature, same 🧱) · h1292 (HomeostaticDrive — the setpoint-controller idiom this reuses,
S*=0.5=Ψ midpoint) · h1290 (affect) · `a_break_the_wall` (lens d, NEW lever; taxonomy (a) measurement
fix; taxonomy (b) gain-matched control) · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` (GREEN-only, so 🧱 = no emit wiring) · `a_core_engine_map` (Ψ-disjoint) ·
`a_autonomy_over_hardcode` · `a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16
