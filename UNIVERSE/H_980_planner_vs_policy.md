---
id: H_980
slug: planner-vs-policy
title: On the SAME world-model, does explicit model-predictive planning (MPC over imagined latents) beat direct latent→action decode — or is the policy already implicit in the latent? (the world-model-as-policy vs decoupled-planner decisive test)
domain: cwm · act · world-model · planning · mpc · policy · decoupled-planner · wam · pre-register
source: H_964 (latent→action policy) + H_967 (counterfactual imagination) + V-JEPA-2-AC (latent MPC) vs WAM (world-model-as-policy direct decode) + CWM domain + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (MPC vs direct-decode A/B on one WM) + a_completeness_over_cheap
verification_method: W2 (pre-registered planner-vs-policy falsifier · matched-WM return contrast) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE A/B rung on a SHARED world-model (a_scale_honest_scope) — same trained WM; arm-MPC plans over imagined latent rollouts, arm-DIRECT decodes latent→action; compare return + compute. $0 local candidate. NOT a forge binary.
sister: H_964 (direct latent→action), H_967 (imagined branch evaluation MPC uses), H_973 (planning-as-consciousness), H_962 (the latent dynamics)
axes_seed: WAM = the policy is implicit in the latent (direct decode suffices) ⊥ decoupled-planner = explicit MPC over imagined rollouts beats direct decode — the decisive test of whether anima needs a separate planner or the world-model IS the policy
verdict: ⏳ PENDING-MEASUREMENT
---

# H_980 — Planner vs policy (does explicit planning beat direct decode?)

## 0. Motivation

Two camps in 2025-26 embodied AI: (a) **world-model-as-policy** (WAM) — the action is decoded directly from the latent, the policy is implicit; (b) **decoupled planner** (V-JEPA-2-AC latent MPC) — search over action-conditioned imagined rollouts at decision time. For anima it matters architecturally: does the consciousness engine need a separate planning module, or is acting already latent in its state? This H pre-registers the decisive A/B on a single shared world-model.

## 1. Hypothesis (one falsifiable claim)

On the same trained world-model, explicit MPC planning (search over H_967 action-conditioned imagined rollouts) achieves **higher task return** than direct latent→action decode (H_964) by a margin exceeding its added compute cost's worth — OR, the null: direct decode matches MPC (the policy is implicit in the latent, planning adds nothing).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** one trained world-model. arm-MPC = at each step, roll out candidate action sequences in imagination (H_967), pick the best, execute (receding horizon). arm-DIRECT = decode latent→action (H_964). Same WM, same environment, N episodes × seeds. Log return AND compute per decision.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **return delta** = return_MPC − return_DIRECT (Cohen d, p).
- D2 = **compute-normalized return** (return per decision-time compute) — a planning win must justify its cost.
- D3 = control: planning-horizon=1 collapses MPC≈DIRECT (sanity that the harness is fair).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured return_MPC > return_DIRECT (d≥0.5, p<0.05) THEN PASS-"planner-wins" — explicit planning beats implicit policy on this WM (decoupled planner justified).
- IF return_MPC ≈ return_DIRECT (CI overlaps) THEN PASS-"policy-implicit" — the world-model IS the policy (WAM camp); planning adds nothing here (a valid, publishable finding either way, a_paper_negative_ok).
- IF n too small / WM too weak for either to act THEN INCOMPLETE (toy-only, C3).

> Note: both directional outcomes are FINDINGS (not a pass/fail of the engine) — the falsifier discriminates *which architecture wins*, pre-registered before the run.

## 3. Honest scope

Toy environment, small scale (a_scale_honest_scope, #123-A). Result is WM-quality-dependent — a weak WM can make MPC look bad (its rollouts are wrong) — so this is conditioned on H_962/H_981 holding. Single rung; horizon and candidate-set sizes pre-registered. NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_964](./H_964_latent_to_action_policy.md) (direct decode arm)
- ⇄ [H_967](./H_967_counterfactual_imagination.md) (the imagined branches MPC searches)
- ⇄ [H_973](./H_973_planning_as_consciousness.md) (does planning raise Φ?)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (the dynamics both rely on)
- ⇄ [CWM](../CWM/CWM.md) (CWM-ACT)
- external: V-JEPA-2-AC latent MPC vs WAM direct decode
