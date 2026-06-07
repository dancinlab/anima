---
id: H_1029
slug: phi-objective-hazard
title: Do agents that MAXIMIZE faithful_phi vs MAXIMIZE big-Phi as their objective pursue measurably DIVERGENT policies on the same task — making the paper's "consciousness-targeting objective is measure-dependent" claim a falsifiable behavioral result rather than a discussion remark?
domain: universe · cwm · cross-cutting · consciousness · iit4 · big-phi · faithful-phi · objective · agent · pre-register
source: PAPER/phi-measure-dependence-planning Discussion ("an agent trained to maximize Phi will pursue opposite policies depending on which Phi is wired into the objective") — asserted as a design hazard but NOT measured; H_1012/1017 (the split exists + is redundancy-driven) make the prediction concrete
exploration_method: E14 (substrate-native IIT4 as reward) + E5 (policy search) — search/select a policy to maximize faithful_phi, and a separate policy to maximize big-Phi, on the SAME control substrate; compare the resulting behaviors + each measure under both
verification_method: W2 (pre-registered behavioral-divergence falsifier · both stdlib engines as objectives · policy comparison) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1029 — is "maximize Phi" a measure-dependent OBJECTIVE hazard? (falsifiable)

## 0. motivation
The paper argues, in Discussion only, that wiring "Phi" into an agent objective is hazardous because
faithful_phi and big-Phi disagree: maximizing the scalar rewards deliberation (redundant shared
info), while maximizing big-Phi penalizes the same deliberation when it modularizes the system. H_1012
(split) + H_1017 (redundancy mechanism) make this a concrete, testable behavioral prediction rather
than a remark. This is the cross-cutting capstone joining the Phi-measure arc and the CWM control arc:
the measure you optimize literally changes what the agent DOES.

## 1. hypothesis
A policy selected to MAXIMIZE faithful_phi and a policy selected to MAXIMIZE big-Phi, on the same
substrate, produce measurably DIVERGENT behavior (e.g. the faithful-maximizer deliberates / plans
more — redundancy-raising — while the big-Phi-maximizer avoids the modularizing deliberation), with
each measure higher under its own maximizer.

## 2. pre-registered falsifier (frozen 2026-06-07)
On the planning-control substrate, run two policy searches with identical setup differing ONLY in the
objective: (A) reward = faithful_phi, (B) reward = big-Phi (both from the stdlib engines, mirror-
proven). Compare the selected policies' behavior (e.g. realized planning depth / action distribution)
and cross-evaluate each measure under both policies. Multi-seed.
- PASS = OBJECTIVE-HAZARD-REAL : the two maximizers select divergent behavior (frozen divergence
  metric exceeds threshold) AND each measure is higher under its own maximizer — the hazard is real.
- FAIL = OBJECTIVES-CONVERGE : both objectives select near-identical policies (closed-negative,
  a_paper_negative_ok) — the split, though present in measurement, would NOT translate to a behavioral
  objective hazard.

## 3. honest scope
Toy substrate, $0 CPU (GPU only if the policy search is heavy — a_fire_autonomous). Real IIT4
engines as the objective, no proxy (a_phi_iit4_tool). p6/p7 honored — no fine-tuned ethics, no
perplexity verdict; this measures behavioral divergence under two honest objectives. Scale-transfer
UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to PAPER/phi-measure-dependence-planning (Discussion) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · [H_1029-sibling H_1021](./H_1021_imagine_rollout_vs_mpc.md) · a_phi_iit4_tool · p6 · p7
