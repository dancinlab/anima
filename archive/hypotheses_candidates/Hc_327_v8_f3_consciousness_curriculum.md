---
id: Hc_327
slug: v8-f3-consciousness-as-curriculum
title: Phi 수준에 따라 학습 데이터 난이도를 sigmoid(phi/threshold)로 자동 조절하면 의식과 데이터의 공진화로 Phi×CE 동시 개선
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 612-643
promoted_at: 2026-05-11
linked_h: curriculum-learning
notes: difficulty ∈ [0,1] 자동 스케줄
---

## Hypothesis
target_difficulty = sigmoid(current_phi / phi_threshold)로 데이터 풀에서 sampling하면 Phi 낮을 때 단순 데이터, 높을 때 복잡 데이터를 매칭하여 Phi x2-3 + CE 개선이 공진화한다.

## Migration TODO
- [ ] 난이도 측정 metric 정의
- [ ] phi_threshold 자동 조정
