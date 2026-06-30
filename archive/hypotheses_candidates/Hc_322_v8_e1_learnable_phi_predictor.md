---
id: Hc_322
slug: v8-e1-learnable-phi-predictor
title: 4-16 세포 시스템에서 정확한 IIT Phi 계산 + MLP 학습으로 1024c Phi를 밀리초 예측하면 측정 정확도 x10+ 향상
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 447-479
promoted_at: 2026-05-11
linked_h: ML-for-physics
notes: ★★★★☆ Top 5. 측정 혁신이 모든 다른 가설의 기반
---

## Hypothesis
n ∈ {4,6,8,10,12,14,16} 작은 시스템에서 정확한 IIT Phi (O(2^n))를 계산하여 (features→phi_exact) 학습 데이터 생성 후 PhiNet MLP를 훈련하면 1024c 시스템의 진짜 Phi를 밀리초 단위로 외삽 예측할 수 있다.

## Migration TODO
- [ ] scaling law 검증 (n=16 → n=1024 외삽 신뢰도)
- [ ] feature engineering: MI, entropy, sync, eigenvalue 등
