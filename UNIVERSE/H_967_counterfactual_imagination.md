---
id: H_967
slug: counterfactual-imagination
title: Can the engine roll out "what if I act X" counterfactual branches whose imagined latents differ in a way that correctly RANKS action value (off-policy imagined evaluation) — counterfactual imagination?
domain: cwm · imagine · world-model · counterfactual · action-conditioned-rollout · planning · dreamer · pre-register
source: H_962 (latent forward dynamics) + CWM domain (counterfactual imagination "what if I act X") + Dreamer imagined value estimation + V-JEPA-2-AC action-conditioned rollout + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (toy action-conditioned branch sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered imagined-value-ranking falsifier · imagined vs true return correlation) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy action-conditioned rollout rung (a_scale_honest_scope) — a toy world with a small action set; engine rolls out each candidate action's latent branch and ranks them; compare imagined ranking to true environment return. $0 local candidate. NOT a forge binary; action = abstract decision, .clm emit path OPEN (a_core_engine_map).
sister: H_962 (latent dynamics — branches roll along it), H_980 (planner vs policy), H_964 (latent→action policy), H_973 (planning-as-consciousness)
axes_seed: forward dynamics = predicts the ON-policy future ⊥ H_967 = predicts OFF-policy counterfactual futures per candidate action AND ranks them by value — if imagined ranking does not track true return, the model cannot imagine consequences of its own actions (closed-negative)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_967 — Counterfactual imagination (can it imagine "what if I act X"?)

## 0. Motivation

The bridge from world-model to agency is **action-conditioned imagination**: before acting, roll out "what would happen if I do X vs Y" and pick the better. Dreamer estimates value from imagined rollouts; V-JEPA-2-AC conditions the predictor on candidate actions for MPC. This H tests whether anima's engine can imagine the consequences of its *own* candidate actions and rank them — the prerequisite for deliberate, auditable action (vs reflexive).

## 1. Hypothesis (one falsifiable claim)

For a set of candidate actions from a given state, the engine's action-conditioned imagined rollouts produce branch latents whose imagined-value ordering **correlates with the true environment return** of those actions — the model can rank what it has never executed.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a toy world with a small discrete action set and a known return function. From sampled states, the engine rolls out each action's latent branch h steps and scores an imagined value; the environment provides the true return. N states × seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **rank correlation** (Spearman/Kendall) between imagined-value order and true-return order across actions per state.
- D2 = **top-1 regret**: true return of the imagined-best action vs the actual best.
- D3 = control: random ranking bounds chance.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured rank correlation CI_lo > 0 (beats random) AND top-1 regret < random-selection regret (Cohen d≥0.5, p<0.05) THEN PASS — counterfactual imagination SUPPORTED.
- IF rank correlation ⊆ chance OR regret ≈ random THEN FAIL — cannot imagine action consequences (closed-negative).
- IF n too small / actions indistinguishable THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy world, small discrete action set, small scale (a_scale_honest_scope, #123-A). "Imagined value" is an operational scoring of branch latents, not a learned critic at production scale. Single rung; horizon short. NOT a forge binary; action is an abstract decision, the .clm/.kosmos emit path is OPEN (a_core_engine_map).

## 4. Sibling / xlinks

- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (branches roll along the latent dynamics)
- ⇄ [H_980](./H_980_planner_vs_policy.md) (explicit MPC planner vs implicit policy)
- ⇄ [H_964](./H_964_latent_to_action_policy.md) (latent→action policy)
- ⇄ [H_973](./H_973_planning_as_consciousness.md) (planning-as-consciousness)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE / CWM-ACT)
- external: Dreamer imagined value · V-JEPA-2-AC action-conditioned MPC
