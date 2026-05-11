---
id: Hc_445
slug: sigma2-144-gpu-sm-structure
title: σ²=144 core count matches GPU SM structure (BT-90) — n=6 predicts compute-hardware layout
domain: substrate
status: candidate-unverified
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 145
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Claim that GPU streaming multiprocessor count of 144 corresponds to σ(6)²=144. BT-90 cross-reference.
---

## Hypothesis
The core-count target σ² = 144 corresponds to and predicts the streaming-multiprocessor (SM) structure of high-performance GPUs (BT-90 cross-reference: 144 SMs). The n=6 derivation predicts hardware-architecture convergence, not just abstract parameter choice. Independent vendor SM-count designs converge to multiples of 144.

## Migration TODO
- [ ] Survey GPU vendors: SM-counts across generations
- [ ] Test goodness-of-fit to σ²=144 multiples
- [ ] Falsifier: dominant SM-count families with NO n=6-family relationship
