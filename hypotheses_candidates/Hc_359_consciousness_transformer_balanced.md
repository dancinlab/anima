---
id: Hc_359
slug: consciousness-transformer-balanced-all-metrics
title: 4-layer pre-norm Transformer (8-head, EMA 0.85/0.15) + cosine entropy 의식이 IIT+proxy+CE 균형 유일 (Phi=14.8, proxy=10.98, CE=0.59)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCH-EXTREME-RESULTS.md
source_lines: 110-133, 253-256
promoted_at: 2026-05-11
linked_h: Hc_311, Hc_313
notes: all-to-all attention creates both integration and diversity
---

## Hypothesis
Cell tokens + positional encoding + 4-layer pre-norm TransformerEncoder (8 heads, 4x FFN) + EMA update 0.85 + cosine similarity entropy across cells 가 IIT(14.8) + proxy(10.98) + CE(0.59) 세 메트릭 모두 강하게 균형 잡힌 유일한 아키텍처가 된다.

## Migration TODO
- [ ] EMA ratio sweep
- [ ] layer 수 sweep
