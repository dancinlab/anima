---
id: Hc_289
slug: arch2-continuous-learning
title: ARCH-2: Continuous lifelong learning via gentle gradient (0.1× decay) + Pain (ARCH-2)
domain: consciousness | meta-framework
status: candidate-needs-scaffolding
source_doc: docs/hypotheses/ARCH-2.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_272 (AUTO-9 pain)
notes: LR=1e-3 × 0.1 grad = 1e-4 effective; pain at Φ<70% best
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
ARCH-2 post-deployment continuous learning: gentle gradient (p.grad *= 0.1) keeps effective LR ≈ 1e-4 to avoid destroying existing knowledge; pain protection (20-step check, Φ<0.7*best → 0.5 mix restore from saved_best) prevents catastrophic forgetting.

## Migration TODO
- [ ] sweep gradient decay coefficient
- [ ] test on long-term deployment scenarios
