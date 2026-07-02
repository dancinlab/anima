---
id: H_1281
slug: 1281_basal_ganglia_gating
title: basal ganglia — reinforcement-gated go/no-go action SELECTION
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED
verdict_dir: .verdicts/1281_basal_ganglia_gating/
terminal_verdict: .verdicts/1281_basal_ganglia_gating/H_1281_R3.txt
date: 2026-06-15
---

# H_1281 — basal ganglia: go/no-go action selection

## Claim / falsifier

`CORE/brain.hexa::brain_decide` gates emit/silence with a FIXED 8-weight linear
`motivation_score` and a FIXED 0.30 threshold — a single-candidate, fixed-map,
fixed-threshold gate with NO competition, NO disinhibition, NO outcome-learning.
**Falsifiable claim:** a basal-ganglia go/no-go SELECTION lane (among COMPETING
candidate emits, release the best / suppress the rest; learn the gate gradient-free
from a GROUNDING OUTCOME reward only) beats anima's faithful untuned fixed engine_g
gate on emit-appropriateness, with the lift reward-driven (shuffled-reward control
collapses). Lens: c15 missing-brain-structure ladder, NOT an LLM recipe.

## Method

- K=4 competing candidates/step, D=6 noisy-correlate features (P_grounded 0.45).
- ARM A = live fixed gate vs ARM B = BG go/no-go (learned go-value vs learned NO-GO/abstain
  argmax; grounding reward grounded +1 / fab −1, outcome-only, gradient-free).
- R3 (binding): engine-native `VBasalGate` lane added to `CORE/brain.hexa`, wired into
  `brain_decide` via `brain_decide_bg`. Smoke `CORE/h1281_basal_ganglia_smoke.hexa`.
- seeds [7,8,9], $0 CPU, p7 (G5 abstain / H_1202 meta-d′ appropriateness metric).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 | 🟠 AMBER / baseline-conditional | frozen oracle-A bars RED (Δ−0.057) verbatim; diagnostic vs faithful untuned A → B +0.236 (FREEZE underdetermined the baseline) |
| R2 mirror | 🟢 GREEN (DIRECTIONAL) | learned weights align to true grounding cos≈+0.76, shuffled→0.12 collapse |
| R3 engine-native + wired | 🟢 GREEN (binding) | VBasalGate beats faithful untuned fixed engine_g gate by +0.195 mean (every seed clears +0.05); shuffled-reward control 0.128 ≪ A+0.02; live weights cos +0.84..+0.91 |

Terminal tier (verbatim): **🟢 GREEN — the R1/R2 numpy-MIRROR result is REPRODUCED ON THE LIVE ENGINE**
→ `.verdicts/1281_basal_ganglia_gating/H_1281_R3.txt`

## Honest scope

R1/R2 mirror DIRECTIONAL; R1 frozen oracle-A bars honored verbatim (no tune-to-green,
c9). Gate learns ONLY from grounding outcome — no external do/dont, no persona/ethics
(`a_autonomy_over_hardcode`, p6). Toy scale, scale-transfer UNVERIFIED.

## Cross-links

h1280 · h1282 · h1231 · h1199 · h1205 · h1227 · h1202 · h1165 ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_autonomy_over_hardcode` ·
`a_core_engine_map` · `a_no_llm_frame_trap` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c1·c9·c15
