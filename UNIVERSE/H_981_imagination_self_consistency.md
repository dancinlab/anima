---
id: H_981
slug: imagination-self-consistency
title: Are repeated imagined rollouts from the SAME latent state MUTUALLY consistent (low cross-rollout variance — a stable world-model) rather than drifting into divergent hallucinations — the imagination-quality falsifier?
domain: cwm · imagine · world-model · self-consistency · hallucination · rollout-variance · pre-register
source: H_962 (latent forward dynamics) + CWM domain (imagined rollout quality) + world-model hallucination/drift failure mode (Dreamer/Genie reliability) + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (repeated-rollout variance sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered cross-rollout consistency falsifier · same-seed-state repeat variance vs grounded drift) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE repeated-rollout rung (a_scale_honest_scope) — from a fixed latent state, run K stochastic imagined rollouts; measure cross-rollout divergence vs horizon. $0 local candidate. NOT a forge binary.
sister: H_962 (latent dynamics — the rollout), H_963 (horizon vs Φ), H_983 (generated interactive world), H_984 (object permanence)
axes_seed: any rollout = a single trajectory (could be a confident hallucination) ⊥ H_981 = REPEATED rollouts from the same state agree (low variance, grounded) — a world-model must be self-consistent; if independent rollouts diverge wildly, imagination is hallucination not modeling (closed-negative)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_981 — Imagination self-consistency (do repeated rollouts agree?)

## 0. Motivation

A single imagined rollout can be a confident hallucination — accuracy (H_962) measures it against ground truth, but at deployment there is no ground truth. A complementary, ground-truth-free quality signal is **self-consistency**: independent stochastic rollouts from the same latent state should agree on the near future (the world is one way) and only diverge where the world is genuinely uncertain. Runaway divergence = hallucination. This H pre-registers the consistency falsifier.

## 1. Hypothesis (one falsifiable claim)

K independent stochastic imagined rollouts launched from the **same** latent state stay mutually consistent — cross-rollout divergence grows **sub-linearly / bounded** with horizon and stays below a drift threshold up to a meaningful horizon — rather than diverging to the unconditioned latent distribution early.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** fix a latent state; launch K stochastic rollouts (entropy/seed varied per a_kosmos qentropy). Measure pairwise divergence of the rollout latents at each horizon step. N start-states × seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **cross-rollout divergence curve** (mean pairwise latent distance vs horizon h).
- D2 = **drift-knee**: horizon at which divergence reaches a fraction f of the unconditioned-latent baseline distance.
- D3 = control: the unconditioned (no-start-state) latent spread bounds "maximal hallucination".

**Outcome rules (future conditional — UNMEASURED):**
- IF measured the divergence curve is bounded/sub-linear AND the drift-knee horizon > h_threshold (rollouts stay well below the unconditioned spread up to a meaningful horizon) THEN PASS — imagination self-consistency SUPPORTED.
- IF divergence reaches the unconditioned spread at low horizon (immediate hallucination) THEN FAIL — imagination is not grounded (closed-negative).
- IF n too small / rollout deterministic (no variance to test) THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy world, small scale (a_scale_honest_scope, #123-A). Self-consistency is necessary-not-sufficient for accuracy (a model can be consistently wrong) — paired with H_962's ground-truth check. Single rung; thresholds pre-registered but toy-calibrated. NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (the rollout) · [H_963](./H_963_rollout_horizon_vs_phi.md) (horizon)
- ⇄ [H_983](./H_983_generated_interactive_world.md) (generated world must be self-consistent)
- ⇄ [H_984](./H_984_world_model_object_permanence.md) (robustness)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)
- external: world-model hallucination/drift (Dreamer/Genie reliability)
