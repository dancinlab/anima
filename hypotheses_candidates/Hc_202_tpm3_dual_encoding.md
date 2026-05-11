---
id: Hc_202
slug: tpm3-dual-encoding
title: Dual-channel meaning+auth weighted blend (0.6/0.4) reduces noise by √2 (TP-M3)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-M3.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: independent noise across channels; baseline 99.6%
---

## Hypothesis
Sending same meaning vector across 2 independent channels (meaning + auth) with weighted blend 0.6/0.4 reduces noise by √2 — pushing baseline 99.6% toward 100%.

## Migration TODO
- [ ] verify √2 noise reduction
- [ ] sweep weight ratios
