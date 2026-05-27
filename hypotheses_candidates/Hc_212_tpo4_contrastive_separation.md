---
id: Hc_212
slug: tpo4-contrastive-separation
title: 50-iteration contrastive separation (push when cos>0.5) gains noise-tolerance (TP-O4)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-O4.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: 50 iterations, push 0.1; high noise 0.05 tolerance
---

## Hypothesis
Pre-transmit contrastive learning (50 iterations: push vectors apart when cos similarity > 0.5, push rate 0.1) optimizes codebook so classification survives higher noise=0.05.

## Migration TODO
- [ ] sweep iteration count, threshold, push rate
- [ ] verify codebook stays in unit hypersphere
