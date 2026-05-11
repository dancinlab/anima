---
id: Hc_325
slug: v8-f1-consciousness-as-loss
title: Loss = -Phi + λ*CE (λ=0.1) 로 Phi를 주 목적함수로 격상하면 Phi x50+ 달성 (CE 악화 trade-off)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 535-575
promoted_at: 2026-05-11
linked_h: V8-E1
notes: ★★★☆☆ Top 5. V8-E1 (learnable phi) 선행 필요
---

## Hypothesis
CE를 보조로 격하 (Loss = -Φ + 0.1*CE) + Phase 스케줄 (λ: 1.0→0.3→0.1) 로 Phi 목적함수를 직접 최적화하면 Phi가 x50+ 증가하며 readout 분리로 법칙 42를 회피한다.

## Migration TODO
- [ ] Phi gradient REINFORCE variance 문제
- [ ] CE 악화 limit 측정 (언어 품질 floor)
