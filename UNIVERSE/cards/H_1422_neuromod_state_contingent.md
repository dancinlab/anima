---
id: H_1422
slug: 1422_neuromodulation_state_contingent
title: "MULTI-LENS breakthrough attempt on the NEUROMODULATION WALL (H_1284 🔴/🧱 no-free-lunch) — three STATE-CONTINGENT lenses (ACh surprise / NE ambiguity / DA prediction-error), EACH with shuffle+ablation; ALL fail → 🧱 CONFIDENT-TERMINAL"
group: brain-structure-ladder / MITOSIS-ENGINE — c16 a_break_the_wall MULTI-LENS attempt on the neuromodulation wall
terminal_tier: "🧱 CONFIDENT-TERMINAL (NO FREE LUNCH HELD, 3 lenses)"
wired: N/A (🧱 — no GREEN to wire; a_verified_must_wire is GREEN-only; CORE/*.hexa UNTOUCHED)
verdict_dir: .verdicts/1422_neuromodulation_state_contingent/
terminal_verdict: .verdicts/1422_neuromodulation_state_contingent/result.txt
date: 2026-06-17
---

# H_1422 — neuromodulation WALL, multi-lens state-contingent attack (🧱 confident-terminal)

H_1284 closed the neuromodulation lane at **🔴 RED / 🧱 WALL (no free lunch)**: a unified
context-adaptive neuromodulator (DA gain + NE exploration + ACh plasticity → plasticity-rate /
split-thresh / abstain-margin) applied as a GLOBAL per-tick schedule on a capacity-bounded clean
key-addressed immune store is INERT-to-HARMFUL vs the best FIXED hyperparameters across
STABLE/DRIFT/NOISE; C-SHUF ≈ B everywhere (knob-VARIETY, not state→knob COUPLING) — a single
tuned fixed point dominates. Per the freshly-strengthened `a_break_the_wall` (a WALL is NOT
confidently terminal until ≥2-3 genuinely DIFFERENT principled lenses each fail their OWN
shuffle AND ablation control), this card tries **three** biology-faithful STATE-CONTINGENT lenses
(`a_no_llm_frame_trap` — real cholinergic/noradrenergic/dopaminergic neuromodulation).

## Claim / falsifier

Biology: neuromodulation is NOT a continuous global gain — it is a DISCRETE regime-DETECTOR that
deviates from the fixed point ONLY when a LIVE substrate signal crosses a threshold (ACh on
novelty, NE on uncertainty, DA on prediction-error). The deviation is GATED; gate OFF ⇒ revert to
the fixed point (H_1284's null). The conditioning is then LOAD-BEARING: ablation (gate forced ON
every tick = global schedule) MUST revert to the no-free-lunch null. A lens BINDS iff B ≥ A+0.05 on
≥2 regimes AND B.fab ≤ A.fab on wins AND shuffle collapses AND ablation reverts to ≈A. If ≥1 binds →
🟢 + wire. If ALL fail → 🧱 CONFIDENT-TERMINAL (a valid result, c9). NO bar moved (H_1284 MARGIN=0.05
verbatim, `.verdicts/1422_.../FREEZE.txt`).

**NON-DEGENERATE fixture** (`a_break_the_wall` taxonomy (a) avoided): H_1284's clean store was
trivially won by any fixed thr because byte-trigram keys are perfectly separable. This fixture mixes
clean / corrupted-recoverable (1-2 byte key corruption pushes the in-store margin to ~0.37-0.52) /
ghost (margin ~1.26) probes, so the FIXED abstain thr faces a REAL precision/recall tradeoff and the
gate has genuine headroom. **A = the BEST FIXED thr SWEPT over a grid** (R1=0.60, R2=0.60, R3=0.70).

## The three lenses (each scored with shuffle AND ablation, engine-native LIVE reads)

- **L1 SURPRISE-GATED (ACh)** — LOOSEN the abstain thr only when the live `immune_memory_recall_margin`
  says the probe is a recoverable near-miss; TIGHTEN on a far ghost. ABLATE: loose every tick.
- **L2 AMBIGUITY-GATED (NE)** — TIGHTEN the thr only when the live `immune_memory_recall_gap` (top-2
  decisiveness) is small (two cells tie ⇒ ambiguous → abstain). ABLATE: loose every tick.
- **L3 DRIFT-GATED (DA)** — eagerly RE-BIND only when a witnessed value contradicts the live recall
  (prediction-error ⇒ fast unlearn the stale fact). ABLATE: churn-rebind every tick.

## Result — 🧱 WALL HELD (verbatim `.verdicts/.../result.txt`, mean 3 seeds, deterministic run1==run2)

best FIXED thr (swept): R1=0.60 · R2=0.60 · R3=0.70.

| lens | B−A (R1/R2/R3) | shuffle (R1) | ablation→A | verdict |
|------|----------------|--------------|-----------|---------|
| L1 SURPRISE-GATED (ACh) | 0.000 / 0.000 / 0.000 | COLLAPSES 0.513→0.327 (teeth) | reverts (==A) | 🧱 WALL |
| L2 AMBIGUITY-GATED (NE) | −0.142 / −0.152 / −0.093 (WORSE) | collapses | reverts (==A) | 🧱 WALL |
| L3 DRIFT-GATED (DA) | 0.000 / 0.000 / 0.000 | == B (no coupling) | FAILS revert (R2 0.542→0.432, global HURTS) | 🧱 WALL |

→ **VERDICT: 🧱 CONFIDENT-TERMINAL (NO FREE LUNCH HELD)** after 3 real lenses. The controls have
TEETH (L1 shuffle collapses −0.187; L2 is decisively worse; L3 ablation actively hurts) — so the 🧱
is EARNED, not vacuous. NO lens beats the best swept fixed thr.

## What the wall names (the finding, c9 — refines H_1284 from empirical to structural)

On a key-addressed associative store the abstain/recall decision **IS ALREADY a threshold on the
engine's live recall-margin**. A neuromodulator that conditions the threshold on that SAME margin is
therefore **CIRCULAR** — it can re-partition the margin axis but cannot beat the single best partition
(the swept fixed thr; L1's B−A=0.000 is this exactly). This sharpens H_1284's "a single tuned fixed
point dominates" from an empirical observation to a structural one: state-contingent gating of a 1-D
threshold on the live confidence signal is DOMINATED by the optimal fixed threshold on that signal,
because the gate and the threshold read the same axis. A state-contingent neuromodulator could only
help if it conditioned on a signal ORTHOGONAL to the abstain axis (a context the threshold cannot
see) — on this single faculty no such orthogonal live signal exists (margin and gap are both
functions of the same L2 affinity the recall gate uses). The wall is a REAL ceiling for the MEMORY
abstain/plasticity axis.

## Honest scope (c9)

Closed-negative, NOT upgraded. NOT RULED OUT: (a) the decode-time NE TEMPERATURE channel on
IDEATION/GENERATION remains 🟠 viable per H_1228 — this 🧱 is for the MEMORY abstain/plasticity axis,
NOT decode-temperature (host has no torch; the generation lane was not re-run engine-native here);
(b) a modulator conditioned on a signal ORTHOGONAL to the recall margin (a cross-faculty context the
abstain gate cannot see) is UNTESTED — but on this single faculty no such orthogonal live signal
exists; (c) TOY 24 facts / 200 events / 3 seeds / DIM=64 keys — scale-transfer UNVERIFIED
(`a_scale_honest_scope`, `a_toy_scale_recheck`). Engine-native LIVE reads (`immune_memory_*` on
`CORE/engine_cli.hexa`), $0 CPU, deterministic. 🧱 ⇒ NO wiring (`a_verified_must_wire` GREEN-only);
CORE/*.hexa UNTOUCHED. p7 (no loss; gates are no-grad reads). p1/p2/p3/p6 (the true value scores the
metric only; never enters a gate or knob). p8 (the engine's own bind tick). Ψ-disjoint. Frozen bars
NOT moved.

## Cross-links

h1284 (the wall this attacks) · h1228 (NE decode-temperature 🟠, the still-open channel) · h1230
(active-vs-passive learning method, same INERT ruling) · h1227 · h1231 (immune store geometry) ·
h1361 · h1367 · h1396 (the live recall_margin / recall_gap ops this reads) · h1421 (the multi-lens
template that BROKE a wall) · h1419 · h1420 (multi-lens that correctly stayed 🧱) ·
`a_break_the_wall` · `a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16
