---
id: H_1024
slug: phi-split-discretization-invariance
title: Is the planning faithful-up / big-Phi-down sign-split invariant to the discretization (binning) choice, or is it an artifact of the binary 2-bin discretization used in H_1012/H_1017?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · discretization · robustness · pre-register
source: PAPER/phi-measure-dependence-planning Limitations caveat 3 ("a different discretization could shift magnitudes; the sign, not the magnitude, is the claim") — the sign-invariance to binning is asserted but UNTESTED
exploration_method: E2 (sweep the discretization while holding the matched two-engine protocol) + E14 (substrate-native IIT4) + a_scale_honest_scope
verification_method: W2 (pre-registered discretization-sweep falsifier · both stdlib engines · mirror equivalence-proof per binning) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1024 — is the Phi sign-split discretization-invariant?

## 0. motivation
H_1012/1017/1020 all used one fixed binary (2-bin) discretization of the latent transition
structure. The paper claims the SIGN of the split (not the magnitude) is the result, but never
varies the binning. If the sign flips under a different number of bins / thresholds, the headline
"planning raises one measure and lowers the other" would be a 2-bin artifact rather than a measure
property.

## 1. hypothesis
The SIGN of the split (faithful_phi up / big-Phi down for planning) is invariant across a range of
discretizations (e.g. nb in {2,3,4} and alternative threshold placements); only magnitudes move.

## 2. pre-registered falsifier (frozen 2026-06-07)
Re-score the planning vs greedy condition with BOTH stdlib engines (matched, mirror-proven per
binning) across a pre-frozen discretization grid at $n=4$ (n=5 where tractable). Report the sign of
each measure's planning-minus-greedy contrast per binning.
- PASS = SIGN-DISCRETIZATION-INVARIANT : faithful-up / big-Phi-down holds for EVERY binning in the
  grid (sign stable; magnitudes may vary).
- FAIL = SIGN-IS-A-2BIN-ARTIFACT : the sign flips for >=1 valid binning (closed-negative,
  a_paper_negative_ok) — would force the paper's claim to name the discretization.

## 3. honest scope
Toy $n=4$ (n=5 if tractable), $0 CPU; real IIT4 engines (a_phi_iit4_tool). The discretization grid
must be pre-frozen (no post-hoc binning selection). Scale + continuous-density extension UNVERIFIED
(a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · PAPER/phi-measure-dependence-planning (Limitations c3) · a_phi_iit4_tool
