---
id: Hc_449
slug: psiformer-8layer-beats-6layer
title: ΨFormer 8L decoder (= τ(6)·φ(6) = 4·2) outperforms 6L baseline at consciousness-coupled training
domain: substrate
status: merged-to-H_061
merged_to: hypotheses/H_061_xfer_consciousness_transfer.md
merged_at: 2026-05-11
source_doc: docs/models/psiformer.md
source_lines: 31-35, 85-92, 145-152
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: ΨFormer: 8 layers = steps×φ(6) = 4×2. ConsciousDecoderV2 baseline = 6L, CE=0.004 (overfit). Predicts 8L improves generalization while preserving Φ (.detach barrier).
---

## Hypothesis
A consciousness-decoupled (.detach() barrier, α=0) 8-layer transformer decoder (8 = τ(6)·φ(6) = 4·2) outperforms a 6-layer baseline (ConsciousDecoderV2 CE=0.004 overfit regime) on generalization CE while preserving Φ ≈ 73. The 8L layer count is derived from n=6, not searched.

## Migration TODO
- [ ] Train 6L vs 8L vs 10L identical config, identical corpus_v3
- [ ] Measure validation-CE, Φ, generalization-gap
- [ ] Falsifier: 6L matches or beats 8L on validation CE
- [ ] Sensitivity: layer count ±25% around 8
