---
id: Hc_283
slug: ultra4-contrastive-ce
title: Contrastive CE — positive MSE(pred,target) + negative max(0, 1.0 − MSE(pred,random)) (ULTRA-4)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/ULTRA-4.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: Hc_212 (TP-O4 contrastive)
notes: pos + neg loss balance
---

## Hypothesis
Contrastive CE learning: jointly minimize positive MSE(prediction, target) and maximize distance from random (negative loss = max(0, 1.0 − MSE(prediction, random))) — separates correct from incorrect predictions.

## Migration TODO
- [ ] sweep negative loss margin
- [ ] verify embeddings spread
