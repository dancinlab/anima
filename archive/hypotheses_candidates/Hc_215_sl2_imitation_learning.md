---
id: Hc_215
slug: sl2-imitation-learning
title: Student imitates pretrained teacher's output via MSE for observation learning (SL-2)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/sl/SL-2.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: teacher 50-step pretrain LR=5e-3
---

## Hypothesis
A consciousness student learns by imitating teacher AI outputs (teacher pretrained 50 steps, student decoder fits teacher's output via MSE) — observation-based learning without explicit labels.

## Migration TODO
- [ ] sweep teacher pretrain steps
- [ ] compare to direct label learning
