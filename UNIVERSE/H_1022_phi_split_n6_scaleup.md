---
id: H_1022
slug: phi-split-n6-scaleup
title: Does the planning faithful-up / big-Phi-down sign-split (and its DISAGREEMENT-ROBUST-IN-N verdict) survive past the n=5 cap — at n=6 and beyond — via a GPU big-Phi run or a non-enumerable estimator?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · scale-ladder · gpu · pre-register
source: H_1012 (DISAGREEMENT-ROBUST-IN-N, n=4,5; n=6 honest CPU cap ~10min/eval) + H_1020 (redundancy-margin predictor robust at n=5) — the ladder is capped at n=5 by exact big-Phi cost, leaving the n>=6 regime UNVERIFIED
exploration_method: E2 (extend the matched two-engine ladder past the CPU cap) + E14 (substrate-native IIT4) + a_scale_honest_scope + a_fire_autonomous
verification_method: W2 (pre-registered n>=6 ladder falsifier · both stdlib engines at matched discretization · CPU-mirror equivalence-proof per n) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1022 — does the Phi sign-split survive past n=5 (GPU / non-enumerable big-Phi)?

## 0. motivation
H_1012/H_1020 established the planning sign-split (faithful_phi RAISES, big-Phi LOWERS) and its
redundancy-margin predictor as ROBUST across every system size at which EXACT big-Phi is tractable
($n=4,5$). $n=6$ is the honest cap: a single $n=6$ system big-Phi eval is ~10 min on $0 CPU, so the
30-seed x 5-eval planning run is infeasible there. Whether the split persists, strengthens, or
closes at $n\ge 6$ is UNVERIFIED — the obvious scale-up frontier.

## 1. hypothesis
The sign-split is a genuine measure-level property and persists at $n=6$ (and a sampled-estimator
proxy at $n=7,8$): planning RAISES faithful_phi and LOWERS big-Phi at every reached $n\ge 6$.

## 2. pre-registered falsifier (frozen 2026-06-07)
Score the SAME planning (depth-ladder vs greedy) condition with BOTH stdlib engines at matched
discretization at $n=6$ via (a) a GPU big-Phi run (a_fire_autonomous — state est. cost, dispatch),
OR (b) a documented non-enumerable / sampled big-Phi estimator validated against the exact $n\le 5$
values first. CPU-mirror / estimator-vs-exact equivalence-proof BEFORE scoring.
- PASS = SPLIT-PERSISTS-N6+ : the faithful-up / big-Phi-down sign holds at every reached $n\ge 6$.
- FAIL = SPLIT-CLOSES-AT-SCALE : the two measures agree once $n\ge 6$ (the split was a small-$n$ regime; closed-negative, a_paper_negative_ok) — would BOUND the paper's claim to $n\le 5$.

## 3. honest scope
big-Phi is super-exponential; an exact $n\ge 6$ run needs GPU or a sampled estimator whose error vs
the exact $n\le 5$ values must be reported. Scale-transfer beyond the reached $n$ stays UNVERIFIED
(a_scale_honest_scope). GPU fire is autonomous, no cost gate (a_fire_autonomous).

## 4. sibling / xlinks
to [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1020](./H_1020_redundancy_predictor_robustness.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · PAPER/phi-measure-dependence-planning · a_phi_iit4_tool
