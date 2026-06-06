---
id: H_995
slug: wm-as-imagined-critic
title: Can the world-model serve as its OWN critic — learn a value function on its latent, then at decision time imagine each candidate action's rollout, score the imagined terminal value, and pick the best action with NO access to environment reward (Dreamer-style planning in the head)?
domain: cwm · act · imagine · critic · value · dreamer
source: CWM 2nd slate — extends H_967🟢 (imagined ranking GIVEN returns) + H_964🟢 (latent→action) + H_980🟢 (policy-implicit) toward learned imagined value (Dreamer actor-critic) + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (latent reward-landscape decision task)
verification_method: W2 (pre-registered imagined-value-beats-baselines + rank-corr falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE latent reward-landscape rung (a_scale_honest_scope); $0 CPU. NOT a forge binary.
sister: H_967 (counterfactual imagined ranking), H_964 (latent→action), H_980 (planner-vs-policy), H_991 (imagination drift)
axes_seed: "imagined value is enough to act (Dreamer)" ⊥ MEASURED "imagined-rollout error corrupts the value estimate — imagined value < reactive greedy" — bounds where imagination-based control pays off
verdict: 🔴 FAIL (closed-negative) — imagined-value policy beats RANDOM (d=1.34) but LOSES to a reactive 1-step greedy (d=−0.80); imagined-vs-true action rank-corr only 0.57. Imagined-rollout error degrades value-ranking at this toy rung. Ladder OPEN.
---

# H_995 — WM-as-critic: pick actions from imagined value (Dreamer-style)

## 0. Motivation

H_967🟢 showed action-conditioned imagined rollouts RANK actions correctly when given the true returns. H_980🟢 found MPC ≈ direct policy (policy-implicit). The Dreamer leap is stronger: the WM learns a VALUE function on its latent, then at decision time imagines each candidate's rollout, reads the imagined terminal value, and picks the best — planning entirely in the head, no environment reward at decision time. This H tests whether the WM can be its own critic.

## 1. Hypothesis (one falsifiable claim)

A policy that imagines each candidate action's rollout and selects by imagined terminal value (no env reward at decision time) achieves true return above both a random-action and a reactive 1-step-greedy baseline, with imagined action-value ranking matching the true ranking.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** latent task with a hidden Gaussian reward-landscape; offline trajectories train a value head latent→return and the WM transition. At test, for each candidate action imagine the H-step rollout, read imagined value, pick argmax. Baselines: random action; reactive 1-step greedy. 24 seeds.

**Measurement (g5 CODE-measured):**
- D1 = imagined-value return vs random (Welch).
- D2 = imagined-value return vs reactive greedy (Welch).
- D3 = Spearman(imagined action-value, true action-value).

**Outcome rules (future conditional):**
- IF imagined beats random AND greedy (p<0.05) AND rank-corr > 0.7 THEN PASS — WM is its own critic.
- IF imagined does not beat baselines OR ranks differ THEN FAIL (closed-negative; a_paper_negative_ok).

## 3. Honest scope

Toy reward-landscape rung (a_scale_honest_scope, #123-A). The value head is a ridge readout; rollout uses the delay-embedding LDS. Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h995_wm_as_critic.py` · verdict: `.verdicts/995_wm_as_imagined_critic/h995_wm_as_critic.txt`

| policy | true return achieved |
|---|---|
| IMAGINED-VALUE (WM critic) | 0.5781 ± 0.2518 |
| RANDOM action | 0.3046 ± 0.1294 |
| REACTIVE 1-step greedy | **0.7994 ± 0.2890** |

D1 imagined > random: d=**1.34**, p=5.0e-05 ✓. D2 imagined vs greedy: d=**−0.80**, p=8.1e-03 (imagined LOSES). D3 imagined-vs-true rank-corr = **0.573** (< 0.7).

**VERDICT 🔴 FAIL (closed-negative)** — the WM cannot reliably serve as its own critic at this toy rung: imagined-value selection beats random but is *worse* than a reactive 1-step greedy, and its action-value ranking only weakly tracks truth (0.57). The cause is imagined-rollout error (cf H_991 drift): rolling the latent forward to score value accumulates error that corrupts the ranking, so myopic-but-accurate greedy wins. This bounds the Dreamer-style claim and is consistent with H_980's policy-implicit finding (direct latent→action ≈ planning here). A_paper_negative_ok; ladder OPEN.
