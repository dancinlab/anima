---
id: H_1037
slug: n6-discretization-invariance
title: Does the planning faithful-up / big-Phi-down sign-split discretization-invariance (H_1024) ALSO hold at n=6 EXACT, or was the n<=5 binning-invariance a small-n artifact?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · discretization · robustness · n6-exact · pre-register
source: residual of H_1024 (SIGN-DISCRETIZATION-INVARIANT, scored at n=4 with n=5 honest-cap) + H_1022 (SPLIT-PERSISTS-N6+, n=6 EXACT on 96-core pod) — the 6-binning grid was only scored at n<=5, leaving open whether it survives the n=6 EXACT scale
exploration_method: E2 (sweep the discretization while holding the matched two-engine protocol) + E14 (substrate-native IIT4) + a_scale_honest_scope (n=6 EXACT rung)
verification_method: W2 (pre-registered discretization-sweep falsifier at n=6 EXACT · both stdlib engines · mirror equivalence-proof per n · many-core exact MIP) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered
verdict: PENDING — measurement not yet run (pre-registration only; verdict token added after the .verdicts txt lands per g73)
---

# H_1037 — is the Phi sign-split discretization-invariant at n=6 EXACT?

## 0. motivation
H_1024 established (PASS = SIGN-DISCRETIZATION-INVARIANT) that the planning faithful_phi-UP /
big-Phi-DOWN sign-split holds for all 6 binnings (nb in {2,3,4} x {equal_width, quantile}) — but
SCORED only at n=4 (n=5 was the honest cap: mirrors proven exact, the full grid infeasible on one
Mac core). H_1022 separately established (PASS = SPLIT-PERSISTS-N6+) that the split STRENGTHENS
through n=6 EXACT (Cohen d -1.83 -> -2.28 -> -3.60) on a 96-core pod (n=6 EXACT = 150 evals,
3.16h). The residual question: does the 6-binning sign-invariance ALSO hold at the n=6 EXACT scale,
the largest exactly-computable system size, or was the n<=5 binning-invariance a small-n artifact?

## 1. hypothesis
The SIGN of the split (faithful_phi up / big-Phi down for planning) is invariant across the same
pre-frozen 6-binning grid at n=6 EXACT; only the magnitudes move.

## 2. pre-registered falsifier (frozen 2026-06-08, TEXT tokens only)
Re-run the H_1024 6-binning robustness sweep at the n=6 EXACT scale. For each binning (nb in
{2,3,4} x {equal_width, quantile}), score the planning(depth-8) - GREEDY contrast SIGN of BOTH
measures, 30 seeds, on a many-core pool (route(a) EXACT — distinctions+relations exact, MIP fully
enumerated, no sampling). Per-scheme sign-criterion (stated BEFORE running):
- faith_sign = UP   iff faithful_phi contrast > +1e-3
- big_sign   = DOWN iff big-Phi      contrast < -1e-3
- a scheme PRESERVES the split iff (faith_sign == UP) AND (big_sign == DOWN).

Outcomes:
- PASS = discretization-invariance CONFIRMED at scale : ALL 6/6 schemes PRESERVE the split at n=6
  EXACT (faithful RAISES, big-Phi LOWERS; magnitudes may vary).
- FAIL = the n<=5 invariance was a small-n artifact : ANY scheme flips the sign at n=6 (faith not
  UP, or big-Phi not DOWN) -> a publishable closed-negative (a_paper_negative_ok).

## 3. honest scope
n=6 is the largest EXACT size; n=7 EXACT is INFEASIBLE-CAP (big-Phi super-exponential). Verdict
scoped to n<=6 EXACT. The H_1022 MC estimator validated |Delta|=0.0000 at n<=5; n>=7 UNVERIFIED.
Both engines EXACT at n=6 (MIP fully enumerated). BOTH CPU mirrors RE-PROVEN == stdlib at n=4 AND
n=5 (+ ring/standalone n=6) BEFORE scoring (a_phi_iit4_tool — real engines, no proxy). The
discretization grid is PRE-FROZEN (no post-hoc binning selection). g5 CODE-measured (no LLM
self-judge, p7). Many-core pod fire (a_fire_autonomous · a_wall_first). TOY n-ladder.

## 4. sibling / xlinks
to [H_1024](./H_1024_phi_split_discretization_invariance.md) (parent: SIGN-DISCRETIZATION-INVARIANT,
n=4) · [H_1022](./H_1022_phi_split_n6_scaleup.md) (SPLIT-PERSISTS-N6+, n=6 EXACT machinery) ·
[H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) ·
PAPER/phi-measure-dependence-planning · a_phi_iit4_tool

## 5. measurement + finding
PENDING — to be filled after the n=6 EXACT many-core run lands. Verdict raw will be at
`.verdicts/1037_n6_discretization/H_1037.txt` (g73); the emoji tier is added to this file ONLY
after that txt exists. Script: `UNIVERSE/h1037_n6_discretization.py` (reuses the H_1022 n=6 EXACT
many-core machinery + the H_1024 pre-frozen binning grid VERBATIM).
