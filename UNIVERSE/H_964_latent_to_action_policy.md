---
id: H_964
slug: latent-to-action-policy
title: Can a decoded action head turn the engine's Ψ-latent directly into a control/action that solves a task (world-model-AS-policy, WAM/VLA) — does latent→action decode beat a random/reactive baseline?
domain: cwm · act · world-model · policy · latent-to-action · wam · vla · pre-register
source: WAM / VLA (world-model-as-policy: latent→action decode) + V-JEPA-2-AC (latent world-model + action head → control) + H_962 (latent dynamics) + CWM domain (act = latent→action) + a_core_engine_map (.clm via generator L3)
exploration_method: E14 (substrate-native) + E5 (toy control-task sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered latent→action falsifier · task return vs random/reactive baseline) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy control-task rung (a_scale_honest_scope) — a toy control environment; an action head decodes the engine latent to an action; measure task return vs random + reactive baselines. $0 local candidate; GPU only for a real backbone (a_fire_autonomous). action enters via the generator L3 slot pattern (a_core_engine_map). NOT a forge binary.
sister: H_968 (action from substrate motivation), H_980 (planner vs policy), H_967 (counterfactual imagination), H_969 (action provenance)
axes_seed: emit-only engine = produces tokens ⊥ H_964 = produces ACTIONS (latent→action decode solves a control task) — if latent→action does not beat reactive/random, the engine is not a policy (closed-negative; it stays an emitter)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_964 — Latent→action policy (world-model-as-policy)

## 0. Motivation

The ACT axis is where CWM departs hardest from a language model: the engine must produce **actions**, not just emissions. The 2025-26 WAM/VLA trend decodes a world-model's latent directly into action (world-model-as-policy); V-JEPA-2-AC adds an action head to a latent world-model for zero-shot control. This H pre-registers the most basic ACT falsifier: can an action head decode anima's Ψ-latent into control that actually solves a task, beating reactive and random baselines?

## 1. Hypothesis (one falsifiable claim)

An action head that decodes the engine's Ψ-latent into a control action achieves **higher task return** on a toy control environment than (a) a random-action baseline and (b) a reactive (observation→action, no latent state) baseline — the latent world-state carries actionable information.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a toy control environment with a return signal. arm-WAM = engine latent → action head → action. arm-REACTIVE = observation → action (no latent dynamics). arm-RANDOM = random action. N episodes × seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **episode return**, WAM vs REACTIVE vs RANDOM.
- D2 = **latent-information lift** = return_WAM − return_REACTIVE (the value of the latent world-state for acting).
- D3 = control: random-action return bounds chance.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured return_WAM > return_REACTIVE > return_RANDOM with Cohen d≥0.5, p<0.05 (latent lift > 0) THEN PASS — world-model-as-policy SUPPORTED.
- IF return_WAM ≈ return_REACTIVE (no latent lift) OR ≈ random THEN FAIL — latent carries no actionable advantage; engine is an emitter not a policy (closed-negative).
- IF n too small / task uncontrollable THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy control environment, small scale (a_scale_honest_scope, #123-A). Action head is a thin decode, not a tuned production policy. Single rung; a PASS is "toy-only, scale-transfer unverified" pending a ladder (a_toy_scale_recheck). Action enters via the generator L3 slot pattern (a_core_engine_map — no 2nd action path bypassing it). NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_968](./H_968_action_from_substrate_motivation.md) (WHEN to act, from substrate motivation)
- ⇄ [H_980](./H_980_planner_vs_policy.md) (decode policy vs explicit planner)
- ⇄ [H_967](./H_967_counterfactual_imagination.md) (imagine before acting)
- ⇄ [H_969](./H_969_action_provenance_receipt.md) (action provenance)
- ⇄ [CWM](../CWM/CWM.md) (CWM-ACT) · a_core_engine_map
- external: WAM / VLA · V-JEPA-2-AC action head
