---
id: H_110
slug: accel-h6-1bit-adam-vram-winner
title: H6 1-bit Adam (★ VRAM WINNER, enables larger batch)
domain: substrate
status: legacy-archive-pointer
exploration_method: E5
verification_method: W4
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-04-03
---

## Hypothesis
1-bit Adam optimizer reduces VRAM footprint enough to enable larger effective batch — accelerates training via batch-size lift rather than per-step throughput.

## Migration Status
Legacy `ready/config/acceleration_hypotheses.json` (id=H6, line 961, verdict=★ VRAM WINNER). Round 4 individual as canonical "VRAM-bound acceleration" entry crossing into H100 cost-discipline (own 16) territory.

## Cross-Links
- Source: `ready/config/acceleration_hypotheses.json` (H6)
- Cross: own 16 (H100 cost discipline), H_106 (COMBO_x255)

1. measured on small models — quantization error compounds at 1B-13B scale
2. "enables larger batch" downstream effect depends on data parallelism config
3. no convergence-quality vs FP32-Adam comparison surfaced
4. interaction with mixed precision (FP16/BF16) not specified
5. 1-bit error feedback assumption may not hold for consciousness-routed gradients
