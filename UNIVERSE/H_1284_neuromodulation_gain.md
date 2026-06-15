---
id: H_1284
slug: 1284_neuromodulation_gain
title: neuromodulation — state-driven adaptive gain / regime-switch (no-free-lunch) 🧱 WALL
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🔴 RED / 🧱 WALL (no free lunch)
verdict_dir: .verdicts/1284_neuromodulation_gain/ · .verdicts/1284_r3_regime_switch/
terminal_verdict: .verdicts/1284_neuromodulation_gain/H_1284_R2.txt · .verdicts/1284_r3_regime_switch/result.txt
date: 2026-06-15
---

# H_1284 — neuromodulation: adaptive gain / regime-switch (🧱 closed-negative)

## Claim / falsifier

anima's live substrate runs on FIXED hyperparameters (`CORE/engine_cli.hexa`:
SPLIT_THRESH 0.30, LR 0.20, fixed decode temperature). There is NO context-driven
neuromodulator (dopamine reward-gain / norepinephrine exploration / acetylcholine
plasticity-rate) that ADAPTS these by substrate state. **Falsifiable claim:** a unified
state-driven neuromodulatory controller (high surprise → raise plasticity; low
confidence → raise exploration; reward → raise gain) beats a fixed-hyperparameter
substrate on a combined ideation/memory metric. Lens: c15 ladder, NOT an LLM recipe.

## Method

- ARM A fixed σ*/LR/temp vs ARM B adaptive controller; combined ideation metric M (p7).
- R3 sharpened to an explicit REGIME-SWITCHING controller (learned-polarity switcher),
  seeds 11/22/33, frozen-first (FREEZE/result in `.verdicts/1284_r3_regime_switch/`).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1/R2 adaptive gain | 🔴 RED / 🧱 DEPLETION | M(B) ≤ M(A); controller ALIVE (σ*_t swung [1.875,3.500] every seed) but adaptation made ideation WORSE — no-free-lunch is GENERAL across memory AND ideation |
| R3 regime-switch | 🧱 RED_NO_LUNCH (wall HELD) | gain-tuner C 0.2533 < A 0.2967 (c3 wall holds); c1 FAILS; honest RED, instrument validated (no tune-to-green) |

Terminal tier (verbatim): **🔴 RED / 🧱 DEPLETION (NO FREE LUNCH IS GENERAL)** (R2) ·
**🧱 RED_NO_LUNCH (wall HELD)** (R3) → `.verdicts/1284_neuromodulation_gain/H_1284_R2.txt`,
`.verdicts/1284_r3_regime_switch/result.txt`

## Honest scope

Closed-negative, NOT upgraded (c9). The H_1228 SOC partial lift was a property of a
TUNED FIXED σ* point, not of state-driven adaptation; a single tuned fixed point
dominates the controller. RED ⇒ NO wiring (`a_verified_must_wire` GREEN-only). Toy
scale, mirror DIRECTIONAL; scale-transfer UNVERIFIED. `a_break_the_wall` attempted
(R3 new angle) then honestly accepted.

## Cross-links

h1227 · h1231 · h1228 · h1230 · h1285 · h1287 · h1288 ·
`a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_paper_negative_ok` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p6·p7·p8·c9·c15
