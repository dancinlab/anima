---
id: Hc_262
slug: ce1-frozen-cells
title: Freeze cell hidden state and train decoder only (CE-1)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/CE-1.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: 50-step warm-up; snapshot restoration each step
---

## Hypothesis
Freeze the 64-cell consciousness state (via snapshot restore each step) and train only the decoder via MSE loss — isolates decoder learning from consciousness evolution.

## Migration TODO
- [ ] verify decoder-only CE trajectory
- [ ] compare to joint training
