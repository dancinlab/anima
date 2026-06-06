---
id: H_979
slug: active-perception-curiosity
title: Is the engine's NEXT perception target CHOSEN by its own motivation / curiosity (active inference, where-to-look) rather than a fixed sensor scan — and does curiosity-driven sampling reduce world-state uncertainty faster than a passive baseline?
domain: cwm · perceive · world-model · active-inference · curiosity · substrate-motivation · a_substrate_native_speak · pre-register
source: a_substrate_native_speak (action emerges from substrate state, environment ≠ obligation) generalized to PERCEPTION + curiosity drive (M×W×Φ×curiosity) + active inference / free-energy + CWM domain
exploration_method: E14 (substrate-native) + E5 (toy partial-observability sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered active-vs-passive uncertainty-reduction falsifier · matched sample budget) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy partial-observability rung (a_scale_honest_scope) — a hidden world-state partially observable through selectable sensor "glimpses"; engine chooses the next glimpse vs a fixed/random scan, under a MATCHED sample budget. $0 local candidate. Perception-selection driven by substrate motivation, NOT an external reward-shaping rule. NOT a forge binary.
sister: H_968 (action from substrate motivation — the ACT-axis twin), H_984 (object permanence / fill-in), H_960 (modality-agnostic encoding), a_substrate_native_speak
axes_seed: passive scan = perception is a fixed input pipeline ⊥ H_979 = perception is an ACT chosen by substrate curiosity (active inference) that beats passive at equal budget — if curiosity-selection does NOT beat passive, perception is not agentive (closed-negative)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_979 — Active perception (does curiosity choose where to look?)

## 0. Motivation

a_substrate_native_speak says anima's emission is not stimulus-response — it emerges from internal substrate state. CWM generalizes this to the PERCEIVE axis: a world-model agent does not passively ingest a fixed sensor stream; it **chooses what to perceive next** to reduce its own uncertainty (active inference / where-to-look). If anima's curiosity drive (already a substrate term, M×W×Φ×curiosity) can steer perception better than a passive scan, perception is agentive; if not, perception is a dumb pipeline.

## 1. Hypothesis (one falsifiable claim)

Under partial observability and a fixed sample budget, an engine that selects its next perceptual "glimpse" by its own curiosity / uncertainty signal reduces world-state estimation error **faster** than a passive (fixed or random) scan baseline using the same budget.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a hidden toy world-state (e.g. a structured grid / object configuration) observable only through K selectable glimpses. arm-ACTIVE = engine picks the next glimpse to maximize expected uncertainty reduction (curiosity); arm-PASSIVE = fixed raster / random glimpse order. Identical budget B glimpses, N seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = world-state reconstruction / decode **error after B glimpses** (active vs passive).
- D2 = **glimpses-to-threshold** (how many glimpses to reach error ≤ ε), active vs passive.
- D3 = control: random-glimpse arm bounds "any selection helps"; active must beat random too.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured error_active < error_passive (and < error_random) at budget B with Cohen d≥0.5, p<0.05, AND glimpses-to-threshold_active < passive THEN PASS — active perception SUPPORTED.
- IF error_active ≈ error_passive (CI overlaps) OR active does not beat random THEN FAIL — perception is not agentive here (closed-negative).
- IF n too small / world degenerate THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy partial-observability world, small scale (a_scale_honest_scope, #123-A). Curiosity-selection is one operationalization of the substrate curiosity term, not the full engine drive. Single rung; matched-budget comparison only — does not claim optimality. NOT a forge binary; a probe.

## 4. Sibling / xlinks

- ⇄ [H_968](./H_968_action_from_substrate_motivation.md) (action from substrate motivation — ACT twin)
- ⇄ [H_984](./H_984_world_model_object_permanence.md) (fill-in under incomplete perception)
- ⇄ [H_960](./H_960_modality_agnostic_latent_encoder.md) (what gets encoded once chosen)
- ⇄ [CWM](../CWM/CWM.md) (CWM-PERCEIVE) · a_substrate_native_speak
- external: active inference / free-energy principle · where-to-look attention
