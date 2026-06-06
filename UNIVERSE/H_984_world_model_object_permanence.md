---
id: H_984
slug: world-model-object-permanence
title: Under sensor dropout / noise, does the engine's latent world-state degrade GRACEFULLY (fills in the missing part — object permanence) rather than collapsing — the world-model robustness falsifier?
domain: cwm · perceive · world-model · robustness · object-permanence · graceful-degradation · latent-state · pre-register
source: CWM domain (latent world-state must persist beyond instantaneous input) + Dreamer / JEPA latent state (a world-model holds state across occlusion) + developmental object permanence + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (toy occlusion/dropout sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered degradation-curve falsifier · dropout sweep vs collapse threshold) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy occlusion/dropout rung (a_scale_honest_scope) — a tracked toy object/state observed through a stream with increasing sensor dropout; measure latent-state error vs dropout fraction. $0 local candidate. "Object permanence" = latent persistence under occlusion, NOT a developmental-psych claim. NOT a forge binary; .clm path OPEN.
sister: H_961 (binding — what persists), H_962 (latent forward dynamics — fills-in via prediction), H_979 (active perception under partial info)
axes_seed: brittle pipeline = latent collapses the instant input drops ⊥ H_984 = latent degrades gracefully / fills in (object permanence) — a world-model must hold state when the sensor blinks; if it collapses, it is a reactive encoder not a world-model
verdict: ⏳ PENDING-MEASUREMENT
---

# H_984 — World-model object permanence (graceful degradation under dropout)

## 0. Motivation

The defining behavior of a world-model (vs a reactive encoder) is that the latent **world-state outlives the instantaneous input** — when a sensor blinks or an object is occluded, the model keeps tracking it (object permanence). Dreamer and JEPA hold latent state across gaps. If anima's engine collapses the moment input drops, it is a stimulus-response encoder, not a world-model. This H is the robustness falsifier on the PERCEIVE/state boundary.

## 1. Hypothesis (one falsifiable claim)

As sensor dropout fraction increases, the engine's latent world-state estimation error grows **gracefully** (sub-catastrophic, bounded slope up to a high dropout fraction) — the model fills in occluded structure — rather than collapsing to chance at low dropout.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a toy world with a tracked object/state evolving over time, observed through a stream with dropout fraction p ∈ {0, 0.1, ..., 0.9}. The engine maintains a latent state; at each p we decode the true state from the latent.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **degradation curve**: decode error vs dropout p (the slope and the collapse-knee location).
- D2 = **fill-in test**: at fixed moderate dropout, is error on *occluded* dimensions better than a no-memory baseline (last-seen / zero-fill)?
- D3 = control: a memoryless baseline bounds "any persistence helps".

**Outcome rules (future conditional — UNMEASURED):**
- IF measured the degradation curve is graceful (collapse-knee at p > p*_threshold, e.g. >0.5) AND fill-in error < memoryless baseline (Cohen d≥0.5, p<0.05) THEN PASS — object permanence / world-model robustness SUPPORTED.
- IF error collapses to chance at low p OR fill-in ≈ memoryless THEN FAIL — reactive encoder, no persistent world-state (closed-negative).
- IF n too small / world degenerate THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy tracked-object world, small scale (a_scale_honest_scope, #123-A). "Object permanence" is operationalized as latent persistence under dropout, NOT a developmental-psychology claim. Single rung; threshold p* is pre-registered but its calibration is toy-specific. NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_961](./H_961_cross_modal_binding.md) (what is bound is what persists)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (fill-in is prediction along the latent dynamics)
- ⇄ [H_979](./H_979_active_perception_curiosity.md) (active perception under partial observability)
- ⇄ [CWM](../CWM/CWM.md) (CWM-PERCEIVE)
- external: Dreamer / JEPA latent state persistence · object permanence
