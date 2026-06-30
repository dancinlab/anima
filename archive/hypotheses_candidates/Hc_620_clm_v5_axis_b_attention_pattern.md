---
id: Hc_620
slug: clm-v5-axis-b-attention-pattern-ssm-hybrid
title: Axis B — standard causal attention 이 multi-turn chat coherence insufficient, SSM/Linear/MoA/Hybrid 이 해소
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_v5_design_spec_2026_05_07.md
source_lines: 91-104
promoted_at: 2026-05-11
linked_h: Hc_618, BG-FY anima-native-ko-small 62.14% Hangul PARTIAL_PASS
notes: B1 SSM Mamba / B2 Linear Attention / B3 sparse MoA / B4 hybrid Transformer+SSM.
---

## Hypothesis
12L × 10heads × 640 standard causal attention 의 state maintenance 가 multi-turn 에서 lossy. Mamba selective SSM + parallel scan, Linear Attention O(N) memory, sparse MoA top-k routing, hybrid alternating layer 이 multi-turn coherence 해소.

## Falsifiable Tests
- B1.test: V5-γ SSM hybrid가 multi-turn 5/5 PASS
- B.universal: 4 B options 모두 chat-cap 0/5 → axis B 자체 아님
- B.compare: same capacity transformer vs SSM 에서 multi-turn coherence delta

## Migration TODO
- [ ] V5-γ SSM hybrid implementation (raw#9 mandate vs torch impl trade-off)
- [ ] Mamba/S4/RetNet external reference 검토
