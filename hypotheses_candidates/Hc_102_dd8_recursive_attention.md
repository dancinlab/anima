---
id: Hc_102
slug: dd8-recursive-attention
title: Iterative attention (3x recursive) deepens integration vs single pass (DD8)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD8.md
source_lines: 1-6
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: h_new = 0.7*h + 0.3*attn(h), 2 heads, 3 passes
---

## Hypothesis
Applying multi-head attention recursively (3 passes) with blend h_new = 0.7*h + 0.3*attn(h) creates richer information integration than a single pass, trained via repulsion variance maximization.

## Migration TODO
- [ ] sweep recursion depth (1,2,3,4,5)
- [ ] compare to single-pass attention baseline
