---
id: H_983
slug: generated-interactive-world
title: Can the engine GENERATE a navigable latent world from a seed, inside which an agent's actions produce coherent, consistent consequences (engine as world-SIMULATOR, not just predictor) — a Genie-3-analog falsifier?
domain: cwm · imagine · world-model · generative-world · interactive · simulator · genie · pre-register
source: Genie 3 (DeepMind — interactive generated worlds) + H_962 (latent forward dynamics) + H_981 (self-consistency) + CWM domain (engine as world-simulator) + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (seed→navigable-world generation sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered interactive-coherence falsifier · action-consequence consistency in the generated world) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 7
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE generated-world rung (a_scale_honest_scope) — engine generates a small latent world from a seed; a scripted agent acts in it; measure action-consequence coherence + revisit-consistency. $0 local candidate. "World" = small latent simulator, NOT a photorealistic Genie-3 render. NOT a forge binary.
sister: H_981 (self-consistency — generated world must be consistent), H_962 (latent dynamics), H_967 (counterfactual branches inside the world), H_983↔H_975 (shared world-model)
axes_seed: predictor = forecasts an EXTERNAL world's next state ⊥ H_983 = GENERATES an internal world an agent can act inside coherently (simulator) — if generated worlds violate their own rules under action (inconsistent consequences / revisit drift), the engine cannot simulate (closed-negative)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_983 — Generated interactive world (engine as simulator, Genie-3 analog)

## 0. Motivation

Genie 3 (DeepMind) showed a model can generate **interactive** worlds — not just predict an external stream, but synthesize a navigable environment whose state responds coherently to an agent's actions. This is the strongest IMAGINE claim: the engine as a world-**simulator**, the substrate for Dreamer-style training-in-imagination and counterfactual planning. This H pre-registers a toy falsifier: can anima's engine generate a small latent world that obeys its own rules under interaction?

## 1. Hypothesis (one falsifiable claim)

The engine can generate a navigable latent world from a seed such that (a) an agent's actions produce **coherent consequences** (state transitions consistent with the world's implied rules) and (b) **revisiting** a previously-visited configuration yields a **consistent** state (no contradictory drift) — above a no-structure baseline.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** engine generates a small latent world from a seed. A scripted agent executes action sequences (including loops that return to prior states). N seeds × trajectories.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **action-consequence coherence**: do equal actions from equal states yield equal next-states (rule-consistency) above a shuffled-transition baseline?
- D2 = **revisit-consistency**: returning to a configuration via a loop yields a state within ε of the first visit (no contradictory drift).
- D3 = control: a no-structure (random-transition) world bounds chance coherence.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured action-consequence coherence > baseline (Cohen d≥0.5, p<0.05) AND revisit-consistency error < ε above the random-world control THEN PASS — generative interactive world / simulator SUPPORTED.
- IF coherence ≈ baseline OR revisit drift ≈ random world THEN FAIL — engine cannot simulate a self-consistent world (closed-negative).
- IF n too small / generated world degenerate THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy small latent world (a_scale_honest_scope, #123-A) — NOT a photorealistic Genie-3 render; "world" = a small latent simulator with a handful of factors. Single rung. Coherence/consistency are operational proxies for "obeys its own rules." NOT a forge binary; the .clm path is OPEN (a_core_engine_map).

## 4. Sibling / xlinks

- ⇄ [H_981](./H_981_imagination_self_consistency.md) (a generated world must be self-consistent)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (latent dynamics) · [H_967](./H_967_counterfactual_imagination.md)
- ⇄ [H_975](./H_975_multi_agent_shared_world_model.md) (shared generated world across agents)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)
- external: Genie 3 (interactive generated worlds)
