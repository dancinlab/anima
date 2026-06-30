---
id: Hc_205
slug: tpn4-multichannel-distributed
title: 3-channel decomposition (log + order + linear) with weighted blend (0.5/0.2/0.3) (TP-N4)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-N4.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: Hc_203 (TP-N1)
notes: noise=0.01; concept(log) + context(order) + meaning(linear)
---

## Hypothesis
Decomposing single numerical value into 3 channel representations (log magnitude, order-of-magnitude, linear normalization) and weighted combining (0.5*log + 0.2*order + 0.3*linear) achieves high correlation across the full range.

## Migration TODO
- [ ] sweep blend weights
- [ ] compare to TP-N1 single-channel
