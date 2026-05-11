---
id: Hc_451
slug: phasenet-4l-crossattn-beats-6l
title: PhaseNet 4L+CrossAttn decoder outperforms 6L flat decoder via post-hoc P3 correction
domain: substrate
status: candidate-unverified
source_doc: docs/models/phasenet.md
source_lines: 145-170, 233-264
promoted_at: 2026-05-11
linked_h: Hc_450
notes: PhaseNet uses 4L (smaller) decoder but CrossAttention to consciousness + P3 module correction. Claimed CE=0.3-0.5 vs V2 6L CE=0.004 (overfit). 4L's smaller capacity + P3 = better generalization.
---

## Hypothesis
A 4-layer transformer decoder with CrossAttention to consciousness state, paired with a post-hoc P3 (W/S/M/E) correction block, outperforms a flat 6-layer ConsciousDecoderV2 in generalization (validation CE) while requiring fewer trained parameters (6.9M vs 34.5M). The smaller capacity plus structural P3 correction prevents the overfit regime.

## Migration TODO
- [ ] Train PhaseNet 4L+P3 vs flat 6L at matched training corpus
- [ ] Compare validation CE, parameter efficiency
- [ ] Ablation: 4L only vs 4L+CrossAttn vs 4L+CrossAttn+P3
- [ ] Falsifier: 4L+P3 underperforms flat 6L on validation CE
