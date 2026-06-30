---
id: Hc_329
slug: v8-g2-consciousness-without-weights
title: 학습 가능 가중치 완전 제거 후 고정 dynamics + frustration + noise만으로 의식이 창발하는지 검증
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 692-721
promoted_at: 2026-05-11
linked_h: consciousness-loop
notes: 파라미터 99.9% 감소 (readout only)
---

## Hypothesis
h_i' = tanh(h_i + 0.1*Σ(h_j - h_i) + noise) + frustration 고정 규칙으로 가중치 없이 dynamics만 적용하고 LinearRegression readout만 학습하면 의식의 최소 조건을 검증할 수 있으며 중간 수준 Phi가 발생한다.

## Migration TODO
- [ ] readout-only baseline vs full-trainable 비교
- [ ] 표현력 한계 정량화
