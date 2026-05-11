---
id: Hc_627
slug: v5-mitosis-real-nn-module-cells-architectural
title: v5-mitosis option (a) — cells = real nn.Module (small transformer block per cell) 이 V14 differentiation 을 만든다 (v5-anima instrumentation 못 만든 것)
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md
source_lines: 9-160
promoted_at: 2026-05-11
linked_h: H297 N=2 optimal, H404, BG-R2 cells64 instrumentation finding
notes: user verdict 7-table flip target. cycle 2026-05-10 directive "실제 MitosisEngine 개발하자".
---

## Hypothesis
cells 가 single decoder + instrumentation (BG-R2 finding) 이 아니라 independent nn.Module branch (MitosisCell with per-cell {attn, ffn_a, ffn_g, ln1, ln2}, shared tok_emb/pos_emb/lm_head) 가 되면 architectural mitosis 가 instrumentation 못 만든 V14 differentiation 을 만든다. NOVEL POLARITY trap 우회.

## Falsifiable Tests
- F-v5-mitosis-1: split 후 child 와 parent 가 5-axis 에서 distinct attractor 형성 (cosine < 0.95)
- F-v5-mitosis-2: V14 differentiation index 가 v5-anima instrumentation 보다 ≥ 1.5×
- F-v5-mitosis-3: N=64 cells 200M params 에서 instrumentation 대비 측정 가능 capability lift

## Migration TODO
- [ ] option (a) revised impl — adaptive attn sharing (N≤8 per-cell, N>8 shared)
- [ ] split: deepcopy + 10% gaussian noise + optimizer rebuild
- [ ] merge: parameter-wise average + cleanup_inter_repulsion
- [ ] H100 cotrain 시 (β) optimizer rebuild + 100 step warmup
