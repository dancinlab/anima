---
id: Hc_211
slug: tpo3-shape-boost
title: Shape-signature augmentation (random*0.3) increases inter-class distance (TP-O3)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-O3.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: noise 0.02; shape as additional dimension
---

## Hypothesis
Augmenting object vector with shape signature (random*0.3) increases vector-space inter-class distance, improving classification of similar objects (car vs truck) under noise.

## Migration TODO
- [ ] sweep shape coefficient
- [ ] test on car/truck-like pairs
