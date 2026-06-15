---
id: H_1282
slug: 1282_working_memory_buffer
title: working memory — PFC gated leaky active-maintenance buffer (capacity ~K)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
verdict_dir: .verdicts/1282_working_memory_buffer/
terminal_verdict: .verdicts/1282_working_memory_buffer/H_1282_R3.txt
date: 2026-06-15
---

# H_1282 — working memory: gated leaky active-maintenance buffer

## Claim / falsifier

anima has long-term episodic memory (immune/clonal cells, H_1227→H_1231: persistent,
grows with #facts, no decay) and the decoder's fixed last-W context — but NO gated
SHORT-TERM active-maintenance buffer (PFC working memory: a few items held ACTIVE
across distractor steps, VOLATILE, CAPACITY-LIMITED ~K slots, distractor-vulnerable).
**Falsifiable claim:** a gated leaky-activation WM-buffer lane holds a cue across
distractors, discriminates a delayed-match probe above flat-context baseline, decays
monotonically, and caps capacity at ~K. Lens: c15 ladder, NOT an LLM recipe.

## Method

- DMS (delayed-match-to-sample) trials, synthetic DIM=16 tokens, seeds [1282,1283,1284].
- R3 (binding): `WorkMemBuffer` lane added to live `CORE/engine_cli.hexa`
  (K=4 slots, λ=0.85 leak, weakest-slot displacement, graded probe score); probe
  `CORE/h1282_wm_buffer_engine_probe.hexa`, export `UNIVERSE/h1282_wm_engine_export.py`.
- AUROC discrimination metric (p7, NOT perplexity), $0 CPU.

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 | 🔴 RED | readout + horizon artifact (NOT a real failure — instrument issue) |
| R2 mirror | 🟢 GREEN (DIRECTIONAL) | margin +0.244 |
| R3 engine-native | 🟢 GREEN (binding) | re-clears all 4 frozen R2 bars on the live lane: margin +0.245 over N≥4, AUROC 1.000 at N=6 (flat-context collapses to 0.506), monotonic decay, capacity caps ~K |

Terminal tier (verbatim): **🟢 GREEN (ENGINE-NATIVE) — the R2 GREEN reproduces on the LIVE engine**
→ `.verdicts/1282_working_memory_buffer/H_1282_R3.txt`

## Honest scope

R2 mirror DIRECTIONAL. Buffer holds TASK ACTIVATION only — no decoder weights, no
persona/identity/ethics (p1-p8). It is SUBSTRATE-CONFIG active maintenance, NOT an
emit/silence gate (returns slots + graded score, never an emit decision —
`a_autonomy_over_hardcode` · p5). Wiring into `brain_decide` context/recall path =
explicit R4 follow-on. Toy DIM=16 synthetic, 3 seeds, scale-transfer UNVERIFIED.

## Cross-links

h1280 · h1281 · h1227 · h1231 · h1199 · h1205 ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_autonomy_over_hardcode` · `a_substrate_native_speak` · `a_scale_honest_scope` ·
`a_toy_scale_recheck` · p1·p2·p3·p5·p6·p7·p8·c1·c2·c9·c15
