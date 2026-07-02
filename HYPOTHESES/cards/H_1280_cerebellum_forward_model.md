---
id: H_1280
slug: 1280_cerebellum_forward_model
title: cerebellum — internal forward-model (predict-next-substrate-state + NLMS error-correct)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
verdict_dir: .verdicts/1280_cerebellum_forward_model/
terminal_verdict: .verdicts/1280_cerebellum_forward_model/H_1280_R2.txt
date: 2026-06-15
---

# H_1280 — cerebellum: internal forward-model

## Claim / falsifier

anima's Engine A (CE-trained byte generation) and Engine G (fixed 8-weight closed-form
motivation/emit score) are NEITHER a cerebellum: an internal FORWARD MODEL that PREDICTS
the next substrate state and LEARNS from prediction error (supervised delta-rule /
NLMS correction). **Falsifiable claim:** adding a forward-model lane that predicts the
next feature frame and corrects via a learned regressor raises held-out coherence and
reduces prediction error, beats a shuffled-context control, and is DISTINCT from Engine G.
Lens: neuroscience missing-brain-structure ladder (c15, `a_no_llm_frame_trap`) — NOT an LLM recipe.

## Method

- R1: numpy MIRROR (host has no torch → DIRECTIONAL only), seeds [7,8,9], frozen-first, $0 CPU.
- R2 (binding): engine-native realization. The live engine could not express a forward
  model with existing surfaces (VAdaptField/VAdaptFieldB/ImmuneMemory carry no
  L·DIM→DIM weight matrix, no delta-rule, no smoothing readout), so R2 EXTENDS the engine
  with a NEW additive Ψ-disjoint lane `VForwardField` in `CORE/engine_cli.hexa`
  (engine-transform-to-fit-the-learning, c1 — precedent H_1199). Probe
  `CORE/h1280_live_cerebellum_probe.hexa`; export `UNIVERSE/h1280_live_feature_export.py`.

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror | 🟢 GREEN (DIRECTIONAL) | held-out coherence +0.048, pred-error falls ~23%, 3 seeds, beats shuffled-context control, distinct from Engine G |
| R2 engine-native | 🟢 GREEN LIVE-CEREBELLUM (binding) | same mechanism on live `VForwardField`; emit-wiring into `CORE/brain.hexa` tracked as R3 follow-on (GREEN-but-emit-unwired) |

Terminal tier (verbatim): **🟢 GREEN LIVE-CEREBELLUM (engine-native — BINDING, not a mirror)**
→ `.verdicts/1280_cerebellum_forward_model/H_1280_R2.txt`

## Honest scope

R1 mirror DIRECTIONAL (engine-transfer was unverified until R2). Toy scale, geometric
coherence + L2 error metric (p7, never perplexity). Forward model corrects SUBSTRATE
DYNAMICS only — no persona/identity/ethics (p2/p3/p6). Scale-transfer UNVERIFIED
(`a_scale_honest_scope` · `a_toy_scale_recheck`).

## Cross-links

h1199 · h1209 · h1205 · h1227 · h1231 · h1281 · h1282 ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_core_engine_map` ·
`a_no_llm_frame_trap` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c1·c2·c9·c15
