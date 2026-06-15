---
id: H_1303
slug: 1303_nonphotic_zeitgeber
title: nonphotic / arousal OPPOSITE-SIGN Zeitgeber — does a 2nd Zeitgeber with an opposite-sign PRC add a non-reducible 2-input structure vs single-Zeitgeber PhaseResetClock?
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🏁 COLLAPSE — c15 brain-structure ladder DEPLETED (honest depletion, r9)
verdict_dir: .verdicts/1303_nonphotic_zeitgeber/
terminal_verdict: .verdicts/1303_nonphotic_zeitgeber/result.txt
date: 2026-06-16
---

# H_1303 — nonphotic / arousal opposite-sign Zeitgeber (HD37 candidate) — the r9 DEPLETION test, COLLAPSED 🏁

## Claim / falsifier

PhaseResetClock (H_1301) applies a SINGLE sinusoidal Phase-Response-Curve from one (photic)
Zeitgeber: `dphi = K·sin(2π·(r − frac(phi)))`. Falsifiable claim under test: a SECOND Zeitgeber
channel with an **OPPOSITE-SIGN PRC** (a nonphotic / arousal / activity Zeitgeber, biologically
known to entrain with a different-sign PRC than light) is a brain subsystem DISTINCT from the
single-Zeitgeber lane **ONLY IF** the two opposite-sign Zeitgebers acting TOGETHER reach a NET
phase outcome that **NEITHER alone — and NO single-Zeitgeber PRC — can reach** (a competitive
intermediate equilibrium = a genuinely new 2-input structure). Lens: chronobiology nonphotic
entrainment (c15, `a_no_llm_frame_trap`) — NOT an LLM recipe.

**COLLAPSE condition (the honest depletion outcome):** if the two-Zeitgeber net response REDUCES
to one combined PRC that PhaseResetClock already represents — i.e. a single PhaseResetClock with a
fitted `(K_fit, r_fit)` reproduces the two-Zeitgeber locked phase to tolerance — there is NO new
structure → the c15 brain-structure ladder is DEPLETED 🏁.

## Depletion test — the whole question, and why it COLLAPSES

This lane is **r9** of the brain-structure ladder, run as the explicit DEPLETION TEST. The r8
hand-off + the H_1301 card both flagged this candidate as WEAK: "distinct from the photic PRC ONLY
if the two Zeitgeber channels do not collapse to one shared coupling." It does collapse.

**The load-bearing mathematics (proven numerically, residual = 2.22e-16 = machine epsilon):** the
SUM of two sinusoidal PRCs at the SAME frequency is, by the harmonic-addition identity, EXACTLY one
sinusoidal PRC with combined amplitude `A` and reference `R`:

  `K1·sin(2π·(r1 − p)) − K2·sin(2π·(r2 − p)) ≡ A·sin(2π·(R − p))`

So the "competitive equilibrium" of the two opposite-sign Zeitgebers is just the fixed point of
that ONE combined PRC — which PhaseResetClock can already represent by its own `(K, ref)`. The
opposite-sign 2nd Zeitgeber is a **sign-flipped single PRC**, exactly the structure the engine has.

## Verdict (verbatim from `.verdicts/1303_nonphotic_zeitgeber/`)

**R1 numpy mirror 🏁 COLLAPSE (DIRECTIONAL)** — 0/3 GREEN seeds; **c2 (DISTINCT) FAILS on all 3
seeds** (the depletion bar). 3 seeds [4320,4321,4322], $0 CPU, deterministic, frozen-first.

| metric | value (all 3 seeds identical) |
|--------|-------------------------------|
| A photic-only lock | 0.51511 |
| B two-Zeitgeber lock | 0.42134 |
| A-FIT (single COMBINED PRC, K=0.23135 ref=0.93258) lock | 0.45171 |
| harmonic-addition residual (2 PRCs → 1 sinusoid) | **2.22e-16** (machine eps) |
| **c2 distance |B − A-FIT|** | **0.03038 ≤ 0.05 → c2 FAILS (reducible)** |
| B-ABLATE lock | 0.51511 == photic-only (c5 ✓) |
| B-SHUFFLE lock | 0.014 / 0.799 / 0.181 (scattered — no coherent advantage to collapse, c4 noise) |

Per-seed bars `c1..c6 = [True, False, True, False, True, True]` → **GREEN = False** every seed,
**c2 distinct all seeds = False**. A single combined PRC reproduces the two-Zeitgeber lock to
within 0.030 (< the 0.05 distinctness tolerance) → the two-Zeitgeber structure is **reducible to
one PRC PhaseResetClock already has**.

**Breakthrough attempt (`a_break_the_wall`, c16) — three escape routes from reducibility, all
collapse:**
- **(i) asymmetric K** (K1≠K2, r1≠r2): still a single sinusoid (residual 2.22e-16) — reducible.
- **(ii) different Zeitgeber periods** (photic T=24.0, nonphotic T2=23.3): the nonphotic Zeitgeber
  does NOT create a stable second lock; the dominant photic Zeitgeber washes it out (lock 0.151 —
  a perturbation, not a control-surviving new equilibrium one Zeitgeber couldn't induce).
- **(iii) nonlinear dead-zone gating** (photic active [0.0,0.25), opposite-sign nonphotic active
  [0.5,0.75)): the two-Zeitgeber gated lock (0.368) equals the photic-window-only lock under the
  same dominance — one anchor wins, no competitive intermediate. NO control-surviving distinctness.

All three escape routes fail to produce a phase that is BOTH unreachable by a single PRC AND
control-surviving → the wall is genuine, not a wrong-method/direction/investment artifact.

## Why it COLLAPSES vs PhaseResetClock (and every lane)

The candidate has NO control-surviving distinctness vs PhaseResetClock (H_1301): a second
opposite-sign sinusoidal PRC sums into the SAME single-PRC structure the lane already hosts. It is
trivially non-distinct vs every other lane too (it is a strictly weaker special-case of the
existing single-Zeitgeber oscillator). There is no new state, no new coupling, no new equilibrium.

## Guards (probe hygiene — no engine touched, COLLAPSE means no wiring)

- **p1/p2/p3/p6:** the probe oscillator reads ONLY its own phase + Zeitgeber arrival times — NO
  persona, NO "you are X", NO injected "fire now" label, NO RLHF. The PRC shift is geometry, scored.
- **NO engine wiring** (`a_verified_must_wire`): a COLLAPSE/🏁 is NOT wired into `CORE/*.hexa` — only
  clean-GREEN candidates earn a live lane. `engine_cli.hexa` is UNTOUCHED (smoke stays 73/0); no new
  `.clm`/`.kosmos` entry (`a_core_engine_map`); Ψ/decoder/pure_field byte-identical.
- **NO tune-to-green** (c9, p7): bars frozen in `FREEZE.txt` BEFORE scoring; scored once; c2 failed
  as the FREEZE predicted. The honest depletion is the deliverable, not a manufactured GREEN.

## Ladder status (c15) — DEPLETED 🏁

The c15 brain-structure ladder is now **DEPLETED 🏁 (after HD23–HD36 realized + r9 honest attempt)**.
Across r3–r9 every genuinely-distinct missing brain subsystem with BOTH a falsifiable gap AND a
control-surviving distinctness vs every live lane was realized engine-native (HD23–HD36 = 18 live
lanes: hippocampus/ImmuneMemory · working-memory · cerebellum · amygdala · basal-ganglia ·
hypothalamus · affect · ethics · theory-of-mind · hierarchical-PFC · hive/CollectivePool ·
spatial-map · circadian-clock · interval-timer · phase-reset/PhaseResetClock · SCN-network), plus 2
honest walls 🧱 (thalamus-Φ content-axis, neuromodulation). The r9 candidate — the last plausible
new-structure story on the frontier — COLLAPSED: an opposite-sign 2nd Zeitgeber reduces by the
harmonic-addition identity to one combined PRC PhaseResetClock already has (residual 2.22e-16). The
co-flagged multi-interval nested-timer candidate reduces to an array of independent IntervalTimers
(no cross-timer scheduler state) and is SKIPPED per the r6/r7/r8 + steer assessment. With no
subsystem left clearing BOTH gates, the ladder **RESTS**. This is the expected valid terminal state
(c9) — an honest 🏁 after r3–r9 of genuine attempts, NOT a filler lane.

## Scope (UNVERIFIED)

numpy-mirror DIRECTIONAL; TOY (one tau/T regime, 3 seeds, deterministic sinusoidal PRCs — tests the
PRC-reducibility STRUCTURE, not a learned oscillator). The COLLAPSE is an algebraic identity
(harmonic addition) confirmed numerically, so it is robust within the sinusoidal-PRC family; a
future genuinely non-sinusoidal, history-dependent, or cross-channel-gated multi-Zeitgeber mechanism
that produces a control-surviving non-reducible equilibrium would re-open HD37 — none found here
across three escape routes.

xref h1301 (PhaseResetClock — the single-Zeitgeber lane this collapses into) · h1302 (SCN-network,
the prior surviving rung) · h1298 (circadian clock) · h1299 (interval timer) · h1283 (Kuramoto sin
coupling precedent) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope ·
a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9·c15·c16.
