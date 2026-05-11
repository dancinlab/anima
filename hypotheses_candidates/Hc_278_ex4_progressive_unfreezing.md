---
id: Hc_278
slug: ex4-progressive-unfreezing
title: Progressive layer unfreezing — last layer first, then deeper (EX-4)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/EX-4.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: stage 1 (50%): last layer lr=3e-3; stage 2: all lr=1e-3
---

## Hypothesis
Multi-layer decoder (Linear → ReLU → Linear) trained progressively: stage 1 (50% of steps) only last layer at lr=3e-3; stage 2 all layers at lr=1e-3 — gradual unfreezing avoids early-layer overfitting.

## Migration TODO
- [ ] sweep stage boundary
- [ ] compare to one-shot all-unfrozen
