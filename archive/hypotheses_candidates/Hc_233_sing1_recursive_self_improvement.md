---
id: Hc_233
slug: sing1-recursive-self-improvement
title: Meta-learner uses CE history to determine LR multiplier via REINFORCE (SING-1)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/sing/SING-1.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_104 (DD6 phi-feedback LR)
notes: Linear(5,1); LR mult 0.1-3.1; REINFORCE on improvement
---

## Hypothesis
A meta-learner Linear(5,1) reads last 5 CE values and outputs LR multiplier (range [0.1, 3.1] via sigmoid); meta_loss = −improvement × meta_pred (REINFORCE on CE decrease) — system learns to improve its own learning rate.

## Migration TODO
- [ ] verify meta-learner converges
- [ ] sweep history length
