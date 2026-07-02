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
status: measured
verdict: 🟢 SPLIT-PERSISTS-N6 / ROBUST-THROUGH-N6-EXACT (honest partial — sign-split holds at every reached exact n=4,5,6; n=6 EXACT completed 3.16h/96-core; route(b) MC estimator validated max|Δ|=0.0000 vs EXACT at n≤5; n=7 sampled-MC proxy infeasible-cap → n≥7 UNVERIFIED a_scale_honest_scope)
measured_at: 2026-06-08
pod: vast 39863592 (96-core, 192 cpu)
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

## 5. measurement (2026-06-08, vast pod 39863592, 96-core / 192-cpu, EXACT)
Independent 96-core re-measure. STEP 0 re-proved BOTH CPU mirrors == stdlib hexa engines at
$n=4,5,6$ before any scoring (`{4: True, 5: True, 6: True}`, all $|\Delta|<4\times10^{-6}$). STEP 1
validated the route(b) sampled-MC big-Phi estimator against EXACT over 24 TPMs. STEP 2 ran the
matched PLAN(depth-8)−GREEDY contrast with BOTH engines at exact $n=4,5,6$ (150 evals/n over 96
workers). STEP 3 (n=7 sampled-MC proxy) was dispatched but did NOT complete in feasible wall-time
(>4h on 96 cores at harvest) → honest infeasible cap.

### per-n EXACT contrast table (PLAN depth-8 − GREEDY, matched binary discretization)
| n | big-Phi contrast | d | p | dir | faithful_phi contrast | d | p | dir | SIGN-DISAGREEMENT | wall |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | −4.0083  | −1.834 | 2.50e-08 | LOWERS | +2.3332 | +5.178 | 6.72e-27 | RAISES | **True** | 15.0s |
| 5 | −13.3732 | −2.284 | 2.35e-10 | LOWERS | +3.0624 | +4.652 | 4.40e-23 | RAISES | **True** | 408.6s |
| 6 | −42.1569 | −3.595 | 2.25e-17 | LOWERS | +3.5332 | +3.452 | 2.64e-16 | RAISES | **True** | 11384.9s (3.16h) |

### route(b) estimator validation (MC big-Phi vs EXACT)
- n=4: max|Δ|=0.0000, mean|Δ|=0.0000, max_rel=0.0000 (24 TPMs)
- n=5: max|Δ|=0.0000, mean|Δ|=0.0000, max_rel=0.0000 (24 TPMs)
→ the sampled-MC big-Phi estimator is exact-equivalent at $n\le5$ (validated, but n≥7 still infeasible at S=256 in feasible wall-time).

### n=7 cap
n=7 SAMPLED-MC proxy (`--n7-samples 256`) dispatched 150 MC evals over 96 workers, ran >4h without
completing → honest computational cap. n≥7 UNVERIFIED (a_scale_honest_scope).

## 6. finding
🟢 **SPLIT-PERSISTS-N6** — the planning sign-split (faithful_phi RAISES, big-Phi LOWERS) holds at
EVERY reached exact system size, now extended one rung past the previous H_1012 cap to $n=6$ EXACT.
The disagreement does NOT close at scale — on the contrary it STRENGTHENS monotonically in big-Phi
effect size ($d=-1.834 \to -2.284 \to -3.595$ across $n=4,5,6$), directly contradicting the
SPLIT-CLOSES-AT-SCALE falsifier. This independently reconfirms H_1012 on a fresh 96-core pod with a
re-proven engine mirror at each $n$. Honest scope: the verdict is ROBUST-THROUGH-N6-EXACT; the
route(b) MC estimator is exact-equivalent at $n\le5$ but the $n=7$ run remained an infeasible cap, so
$n\ge7$ is UNVERIFIED (a_scale_honest_scope). The previously expected $n=6$ "honest CPU cap" was
cleared by the 96-core dispatch (3.16h wall).

## 4. sibling / xlinks
to [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1020](./H_1020_redundancy_predictor_robustness.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · PAPER/phi-measure-dependence-planning · a_phi_iit4_tool
