---
id: H_1023
slug: phi-split-substrate-generality
title: Does the redundancy-driven faithful-up / big-Phi-down split generalize beyond the planning-control substrate to a DIFFERENT generative substrate (a trained CLMConvMoE latent, or an unrelated task TPM)?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · substrate-generality · pre-register
source: H_1017 (redundancy explains the split) + H_1020 (mechanism predictor robust n=5) — both measured ONLY on the planning depth-ladder control substrate; cross-substrate generality is untested
exploration_method: E2 (re-run the two-engine + PID protocol on a NEW substrate) + E14 (substrate-native IIT4) + a_scale_honest_scope
verification_method: W2 (pre-registered cross-substrate falsifier · both stdlib engines + WB I_min PID · mirror equivalence-proof) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
---

# H_1023 — is the redundancy-split substrate-general?

## 0. motivation
The split + redundancy mechanism (H_1012/1017/1020) were all measured on ONE substrate: the latent
transition structure of the planning-control toy. If the split is a genuine property of the two Phi
measures (not of that one task), an intervention that floods a DIFFERENT substrate with redundant
shared information should also produce faithful-up / big-Phi-down — and the redundancy-margin should
again predict it. Tests whether the finding is about the measures or about the task.

## 1. hypothesis
On a different generative substrate (e.g. the discretized latent of a trained CLMConvMoE, or an
unrelated structured TPM), a redundancy-injecting intervention reproduces the sign-split and the
redundancy-margin again separates split from no-split — the split is substrate-general.

## 2. pre-registered falsifier (frozen 2026-06-07)
Build >=1 NEW substrate (not the planning-control env). Apply a redundancy-raising vs a
synergy-raising intervention; score faithful_phi + big-Phi (matched discretization, mirror-proven)
and the WB I_min redundancy-margin, at $n=4$ (and $n=5$ if tractable).
- PASS = SPLIT-SUBSTRATE-GENERAL : the redundancy-raising intervention reproduces faithful-up /
  big-Phi-down on the new substrate AND the redundancy-margin separates it from the synergy control.
- FAIL = SPLIT-TASK-LOCAL : the split does NOT reproduce off the planning substrate (closed-negative,
  a_paper_negative_ok) — would BOUND the paper to the control task.

## 3. honest scope
Toy $n=4$ (n=5 if tractable), $0 CPU; real IIT4 engines, no proxy (a_phi_iit4_tool). The PID is the
explanatory variable, not a Phi proxy. Substrate choice + intervention construction must be stated
and pre-frozen. Scale-transfer UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1017](./H_1017_split_redundancy_mechanism.md) · [H_1020](./H_1020_redundancy_predictor_robustness.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) · PAPER/phi-measure-dependence-planning · a_phi_iit4_tool
