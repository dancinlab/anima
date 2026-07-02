---
id: H_1427
slug: 1427_temporal_replay_prediction
title: temporal-sequence / replay-prediction — CA3 replay-style next-ITEM prediction from learned transition statistics
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
verdict_dir: .verdicts/1427_temporal_replay_prediction/
terminal_verdict: .verdicts/1427_temporal_replay_prediction/H_1427_R2_engine_native.txt
wired: WIRED-live
date: 2026-06-17
---

# H_1427 — temporal-sequence / replay-prediction (hippocampal CA3 replay)

## Claim / falsifier

The live engine has stores (ImmuneMemory key→value, SpatialMap metric, HierGoalStack
given-order plan), a cerebellar forward model (VForwardField, continuous next-frame NLMS),
and a GATE-B transition-predictability gate (VAdaptFieldB) — but **NONE PREDICTS the next
discrete ITEM from LEARNED transition statistics P(next|current)**: the hippocampal CA3
recurrent-collateral → REPLAY pattern-completion computation. **Falsifiable claim:** a
faculty that learns P(next|current) from observed item sequences and reads out the
most-frequent successor raises held-out next-item accuracy over a no-transition baseline,
survives controls against every nearest lane, collapses under shuffle + ablate, and abstains
on out-of-distribution input. Lens: hippocampal CA3 auto-association / replay (c15,
`a_no_llm_frame_trap`) — NOT an LLM next-token recipe (p7 accuracy, never perplexity).

## DISTINCTNESS axis (load-bearing): LEARNED TRANSITION STATISTICS ⊥ …

- **vs GATE-B (H_1208/1209 `VAdaptFieldB`) — the SHARPEST distinctness:** that lane already
  HOLDS a P(next|prev) count table, but uses it ONLY as a GROWTH GATE (split a cell when a
  transition was confidently anticipated; order vs disorder discriminator). It NEVER EMITS a
  next-item PREDICTION. CA3 **reads it out** (which item comes next) — gate vs read-out.
- **vs cerebellum forward-model (H_1280):** an NLMS regressor of the next CONTINUOUS feature
  frame; here the target is a DISCRETE multi-successor conditional (argmax over a count table).
  Mirror control `vs1280` (forward-model→nearest-item) scores 0.162 vs ON 0.761.
- **vs episodic item-binding (H_1227/1231):** binds key→value INDEPENDENTLY, no successor
  aggregation. Control `vs1227` (bind cur→last-seen-next) scores 0.548 vs ON 0.761 — it
  captures the dominant successor partially but loses the frequency aggregation (+0.213 lift).
- **vs hier-PFC (H_1294):** a GIVEN ordered plan handed to a pointer; here the order is LEARNED
  from statistics. Control `vs1294` (pointer with no learned stats) → chance 0.037.
- **vs spatial-map (H_1296):** a METRIC space (between-item distance), not order/transition.

## Method

Sequences from a fixed structured generator over V=24 items: each state has 1 dominant
successor (p_dom=0.75) + 3 minor noise successors. TRAIN 200 seqs → build P(next|current)
counts; TEST next-item accuracy on 120 held-out seqs from the SAME kernel. Arms: OFF
(marginal-only) · ON (argmax conditional, abstain-gated min_supp=2) · SHUFFLE (permute pairs
at train) · ABLATE (conditional→marginal) · vs1280/vs1227/vs1294 nearest-lane controls. OOD
set = 6 alien ids + below-support currents (bar 5). 3 seeds [1427,1428,1429], $0 CPU, p7.
5 bars frozen BEFORE measuring (`H_1427_FREEZE.txt`), tune-to-green prohibited (c9/c16).

## Verdict by round

| round | tier | key numbers (5 frozen bars) |
|-------|------|------------------------------|
| R1 mirror (summer) | 🟢 GREEN (DIRECTIONAL) | ON 0.761 · OFF 0.155 · SHUF 0.130 · ABL 0.155 · vs1280 0.162 · vs1227 0.548 · vs1294 0.037 · OOD abstain 1.000 fab 0.000. ① PRESENCE +0.606≥+0.20 (each seed) · ② DISTINCT ON−best_ctrl +0.213≥+0.10 (each ctrl<ON−0.05) · ③ SHUFFLE 0.130≤OFF+0.05 · ④ ABLATE |ABL−OFF|=0.000≤0.03 (INERT) · ⑤ NO-FAB abstain 1.000≥0.90, fab 0.000≤chance+0.05 — **5/5 PASS**, run1==run2 |
| R2 engine-native (summer, live `CORE/engine_cli.hexa`) | 🟢 GREEN (BINDING) | LIVEOP probe RC=0: ON 0.751 · OFF 0.108 · SHUF 0.150 · ABL 0.108 · vs1227 0.600 · OOD abstain 1.000. ① +0.643 · ② +0.151 · ③ 0.150≤0.158 · ④ INERT · ⑤ 1.000 — **5/5 PASS**. CA3 smoke cases 153-158 PASS engine-native (isolated run, RC=0). brain_smoke RC=0. |

Terminal tier (verbatim): **🟢 GREEN (ENGINE-NATIVE)** — a learned-transition next-item
predictor reads out the successor that GATE-B only gates on; both controls collapse; every
nearest lane is dissociated; lane wired Ψ-disjoint.
→ `.verdicts/1427_temporal_replay_prediction/H_1427_R2_engine_native.txt`
(frozen bars `…/H_1427_FREEZE.txt`, not moved).

## Engine wire-in (a_verified_must_wire — 4-rung ladder)

1. DIRECTIONAL mirror GREEN ✅ (`state/1427_temporal_replay_prediction/h1427_replay_prediction.py`)
2. engine-native re-verify ✅ (LIVEOP probe RC=0, 5/5 — `…/h1427_ca3_LIVEOP_probe.hexa`)
3. live CORE wire-in ✅ — `CORE/engine_cli.hexa` § CA3 REPLAY NEXT-ITEM PREDICTOR LANE
   (`ca3_replay_new/observe/predict/conf/marginal`); smoke cases 153-158
4. ARCHITECTURE.json lockstep ✅ — engine_cli node note + guard_baseline updated

**Guard caveat (a_break_the_wall taxonomy-c, honest c9):** the FULL `CORE/engine_cli_smoke.hexa`
currently aborts at ~case 16 (immune_grow/salience, `cannot multiply non-numeric operand tag
24*tag 24`) under `hexa 0.1.0-dispatch` — a PRE-EXISTING dispatch-build interpreter bug that
reproduces on CLEAN origin/main on BOTH summer and aiden, NOT a CA3-lane regression. The CA3
cases 153-158 are proven to pass engine-native by an isolated run importing the live engine
(RC=0); they execute inside the full smoke once that earlier crash is fixed. The protocol's
named wire-in gate (`hexa CORE/brain_smoke.hexa` RC=0) PASSES.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- R1 mirror = DIRECTIONAL; R2 engine-native is the binding verdict (deterministic lane
  assertions on the live engine, NOT a trained net — tests the STRUCTURE).
- toy: V=24, 1 paradigm, 1st-order Markov kernel, 3 seeds; scale + real sequence corpora +
  higher-order (n-gram) transitions + brain emit/recall wiring of the predicted item UNVERIFIED.
- p1/p2/p3/p6: reads ONLY item ids + their observed transition counts; NO label/persona/
  identity/RLHF/decoder/weights. The transition statistics are counted, scored only.

## Pointers

- FREEZE: `.verdicts/1427_temporal_replay_prediction/H_1427_FREEZE.txt`
- RESULT: `.verdicts/1427_temporal_replay_prediction/H_1427_R1_mirror.txt` (R1) ·
  `…/H_1427_R2_engine_native.txt` (R2 engine-native)
- mirror probe: `state/1427_temporal_replay_prediction/h1427_replay_prediction.py`
- LIVEOP probe: `state/1427_temporal_replay_prediction/h1427_ca3_LIVEOP_probe.hexa`
- engine lane: `CORE/engine_cli.hexa` § CA3 REPLAY NEXT-ITEM PREDICTOR LANE ·
  smoke `CORE/engine_cli_smoke.hexa` cases 153-158
- xref: H_1208/1209 (GATE-B transition gate, sharpest distinctness) · H_1280 (cerebellum) ·
  H_1227/1231 (episodic item-binding) · H_1294 (hier-PFC given-order) · H_1296 (spatial-map) ·
  `a_no_llm_frame_trap` · `a_break_the_wall` · `a_engine_native_learning` ·
  `a_verified_must_wire` · `a_autonomy_over_hardcode` · `a_core_engine_map` ·
  `a_scale_honest_scope` · `a_toy_scale_recheck` · c9 · c15 · c16 · p1·p2·p3·p6·p7·p8
