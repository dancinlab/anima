---
id: H_970
slug: world-model-vs-language-model-decisive-test
title: Is there a task SOLVABLE ONLY by a world-model (requires a persistent latent state to act) and NOT by a next-token predictor — the falsifiable WM>LM separator that decides whether anima needs a world-model at all?
domain: cwm · cross-cutting · world-model · language-model · decisive-test · separator · pre-register
source: CWM domain (key distinction: LM predicts next word, WM predicts next state + acts) + H_951 (engine-not-predictor) + H_962 (latent dynamics) + H_964 (latent→action) + a_paper_significance + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (WM-only task construction) + a_completeness_over_cheap
verification_method: W2 (pre-registered WM-vs-LM separator falsifier · matched-capacity LM baseline) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE separator-task rung (a_scale_honest_scope) — construct a toy task requiring a persistent latent world-state (partial observability + delayed consequence) where a next-token/next-observation predictor at matched capacity cannot succeed; compare a WM agent vs the LM baseline. $0 local candidate. NOT a forge binary.
sister: H_951 (engine-not-predictor), H_962 (latent dynamics), H_964 (latent→action), H_984 (object permanence — the WM property exploited)
axes_seed: "a WM is just a fancier LM" (deflation) ⊥ H_970 = there EXISTS a task a WM solves and a matched-capacity LM cannot — without this separator, the whole CWM domain is unjustified (closed-negative: if a matched LM matches the WM, anima does not need a world-model)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_970 — World-model vs language-model decisive test (does anima need a WM?)

## 0. Motivation

CWM's entire premise is that a world-model is categorically more than a language model (LM predicts the next *word*; WM predicts the next *state* and acts). A skeptic says "a big enough next-token predictor matches any WM." This H pre-registers the **decisive separator**: a task that *requires* a persistent latent world-state to solve, on which a matched-capacity next-token/next-observation predictor *cannot* succeed. If no such separator exists empirically, the CWM domain is unjustified (a publishable closed-negative).

## 1. Hypothesis (one falsifiable claim)

There exists a task — requiring a persistent latent world-state (partial observability + delayed, state-dependent consequence) — on which a world-model agent (H_962+H_964) achieves task success while a **matched-capacity** next-token / next-observation predictor baseline performs at/near chance, with a significant gap.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a toy task designed so success requires integrating partial observations into a latent state and acting on a delayed consequence (a next-symbol predictor with no persistent state cannot represent the needed variable). arm-WM = world-model agent. arm-LM = matched-parameter next-token/next-observation predictor (same capacity budget). N episodes × seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **task success rate**, WM vs LM.
- D2 = **separator gap** = success_WM − success_LM (and LM vs chance).
- D3 = control: capacity-matching audit (the LM is not handicapped by size); a memory-augmented LM ablation to locate WHERE the gap comes from (the persistent-state requirement).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured success_WM > success_LM with a large gap (Cohen d≥0.8, p<0.05) AND LM ≈ chance AND capacity-matched THEN PASS — a WM>LM separator EXISTS; anima needs a world-model (CWM justified).
- IF success_LM ≈ success_WM (matched LM matches the WM) THEN FAIL — no separator on this task; the WM premise is deflated here (closed-negative, a_paper_negative_ok — a major finding for the domain).
- IF n too small / task not actually WM-requiring THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy task, small scale (a_scale_honest_scope, #123-A). A single separator task is existence-proof-by-construction — a PASS shows ONE task where WM>LM, not that WM>LM in general; a FAIL on a well-constructed WM-requiring task is the stronger surprise. Capacity-matching is pre-registered and audited. NOT a forge binary. This is the domain's keystone significance test (a_paper_significance).

## 4. Sibling / xlinks

- ⇄ [H_951](./H_951_clm_engine_not_predictor.md) (engine-not-predictor — the reframe this operationalizes)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) · [H_964](./H_964_latent_to_action_policy.md) (the WM agent)
- ⇄ [H_984](./H_984_world_model_object_permanence.md) (the persistent-state property exploited)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · domain keystone)
- external: world-model vs LM distinction (CWM.log.md landscape)
