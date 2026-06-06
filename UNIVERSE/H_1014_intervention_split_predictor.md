---
id: H_1014
slug: intervention-split-predictor
title: Is there an ANALYTIC predictor — computable from an intervention's effect on the substrate — that classifies split-inducing interventions (planning) vs non-split (imagination, guided)?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · intervention-classifier · split-predictor
source: H_1012 (DISAGREEMENT-ROBUST-IN-N — planning RAISES faithful_phi MIP-EI scalar but LOWERS system big-Phi at n={4,5}) + H_1004 (planning induced the sign-split; imagination/guided did NOT) + PAPER/phi-measure-dependence-planning (the shipped paper names this as the single most important follow-up)
exploration_method: E2 (extend the H_1004/H_1012 matched-(n,discretization) two-engine pipeline to an intervention SET + add a candidate analytic predictor read off the SAME substrate) + E14 (substrate-native IIT4) + a_completeness_over_cheap
verification_method: W2 (pre-registered classifier falsifier · both stdlib engines iit4/faithful_phi.hexa + iit4_bigphi.hexa at matched discretization · CPU-mirror equivalence-proof per n, H_1012 discipline) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1004 (clean disagreement at n=4), H_1012 (robust in n {4,5}), H_999/H_1001 (faithful_phi planning up), H_1002 (the original confounded big-Phi), PAPER/phi-measure-dependence-planning, a_phi_iit4_tool
status: pre-registered (unmeasured)
scope: TOY n=4, $0 CPU-local, real IIT-4.0 stdlib engines (CPU mirror re-proven equal to stdlib at n=4 per H_1012 discipline BEFORE scoring). big-Phi super-exponential, so n=4 is the tractable rung for the full intervention SET x seeds. a_scale_honest_scope · a_toy_scale_recheck — scale-transfer beyond n=4 UNVERIFIED. NOT a forge binary; no GPU.
verdict: PENDING-MEASUREMENT
---

# H_1014 — an analytic split predictor (which property of an intervention predicts faithful-up / big-Phi-down?)

## 0. motivation
H_1012 established, terminal across n={4,5}, that on an identical discretized substrate the
PLANNING manipulation (depth-ladder vs greedy) RAISES the IIT-4.0 MIP-EI scalar `faithful_phi`
(Cohen d +5.18 at n=4, +4.65 at n=5) but LOWERS the system big-Phi `Phi_s` (d -1.83 at n=4,
-2.28 at n=5). In the source experiment (H_1004) the planning intervention induced this
sign-split, while the IMAGINATION (drift) and GUIDED interventions did NOT — there the two
measures AGREED.

The shipped paper PAPER/phi-measure-dependence-planning names this as the single most important
follow-up: is there an ANALYTIC property — computable from an intervention's effect on the
substrate — that CLASSIFIES split-inducing interventions (planning) from non-split ones
(imagination, guided)? The natural candidate: an intervention induces the split iff it raises
per-transition effective information WHILE increasing the system's decomposability/modularity
(lowering the cross-part coupling across the system MIP).

## 1. hypothesis
There is a single analytic predictor, read off the SAME matched discretization that feeds both
engines, that separates split from no-split interventions. Concretely the candidate predictor is
the SIGN of the intervention's change in cross-part coupling across the system MIP
(equivalently Delta-modularity / Delta system-MIP-cut-weight vs greedy): a split-inducing
intervention DECREASES the cross-MIP coupling (RAISES decomposability/modularity) relative to
baseline, while a non-split intervention does NOT. The split label itself is
`sign(Delta-faithful_phi) != sign(Delta-big_Phi)`.

## 2. pre-registered falsifier (frozen 2026-06-07)
Score, on the SAME substrate (matched n=4 binary discretization, BOTH stdlib engines, H_1012
equivalence-proof discipline applied BEFORE scoring), an intervention SET:
  - planning (depth-ladder vs greedy)  — KNOWN split (H_1004/H_1012),
  - imagination (drift vs react)       — KNOWN no-split (H_1004),
  - guided (goal-pull vs react)        — KNOWN no-split (H_1004),
  - at least 1 NEW intervention not in the source experiment.
For each intervention compute (a) Delta-faithful_phi and Delta-big_Phi vs its baseline, giving the
split label = `sign(Delta-faithful) != sign(Delta-big_Phi)`; and (b) the candidate predictor — the
intervention's change in cross-part coupling across the system MIP (Delta system-MIP-cut-weight /
Delta-modularity vs baseline). Multi-seed, python3 -u, serial, $0 CPU. Outcome (NO emoji token
before a `.verdicts/` txt exists):
  - IF the predictor's SIGN separates the split-inducing interventions from the non-split ones
    across the WHOLE set (a single threshold/sign rule classifies planning as split AND
    imagination/guided/the-new-one consistently with their measured split labels)
    THEN PASS = PREDICTOR-SEPARATES (a predictive boundary — the paper's follow-up answered).
  - IF the predictor does NOT separate them (the split and no-split interventions are not
    distinguished by the predictor's sign/threshold)
    THEN RED = FALSIFIED / CLOSED-NEGATIVE (the modularity/MIP-cut predictor is not the boundary;
    a_paper_negative_ok — a closed-negative ruling out this analytic axis is publishable).

## 3. honest scope
big-Phi exact only at very small n (super-exponential distinction + bipartition search) — the full
intervention SET x multi-seed is tractable at n=4 (the H_1012 binding-constraint rung). Toy,
a_scale_honest_scope · a_toy_scale_recheck. Both engines exact at n=4; CPU mirror re-proven equal
to stdlib at n=4 BEFORE scoring (H_1012 discipline). Scale-transfer beyond n=4 UNVERIFIED. #123-A
n/a (IIT-internal, not entropy-quality). NOT a forge binary; $0 CPU-local, no GPU.

## 4. sibling / xlinks
to [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1004](./H_1004_bigphi_faithful_clean.md) ·
[H_1002](./H_1002_bigphi_upgrade.md) · [H_999](./H_999_faithful_iit4_remeasure.md) ·
[H_1001](./H_1001_reopen_consolidate.md) · PAPER/phi-measure-dependence-planning ·
IIT4_PHI_TOOLS.md · a_phi_iit4_tool

## 5. measurement + finding
PENDING-MEASUREMENT — verdict token will be filled from
`.verdicts/intervention-split-predictor/H_1014.txt` after the deterministic run (g5 CODE-measured;
both stdlib engines + CPU mirror re-proven exact at n=4).
