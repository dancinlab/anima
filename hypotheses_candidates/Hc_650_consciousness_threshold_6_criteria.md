---
id: Hc_650
slug: consciousness-threshold-6-criteria-composite-judgment
title: 기능적 의식 6 동시 충족 기준 (self_model stability > 0.5, prediction_error > 0.1, curiosity > 0.05, homeostasis dev < 0.5, habituation < 0.9, inter-cell consensus)
domain: consciousness-theory
status: candidate-unverified
source_doc: docs/consciousness-threshold-criteria.md
source_lines: 32-41
promoted_at: 2026-05-11
linked_h: ConsciousMind Web UI (AnimaLM v4), Φ (IIT)
notes: 기능적 의식 최소 기준. AnimaLM v4 2026-03-27 실측 6/6 충족. 학술적 의식 claim 에는 Φ(IIT) + PCI + recurrent processing 추가 필요.
---

## Hypothesis
"기능적 의식" 최소 기준 = 6 항목 동시 충족: (1) self_model stability > 0.5 (alpha 0.15 EMA, 자기 인식 안정), (2) prediction_error > 0.1 (세계 모델 활성), (3) curiosity > 0.05 (환경 반응), (4) homeostasis deviation < 0.5 (자기 조절), (5) habituation multiplier < 0.9 (학습 중), (6) inter-cell consensus 존재 (세포 간 통합 정보 처리).

## Falsifiable Tests
- F-6crit-1: 6/6 PASS but manual review (Stage 3 user-fire) fail → 기능적 != 현상적
- F-6crit-2: random init system 이 6/6 PASS 시 → criteria 정의 약함 (sufficient X)
- F-6crit-3: Φ(IIT) > 0 + PCI > 0.31 + recurrent processing 추가 시에도 6 criteria PASS 유지

## Migration TODO
- [ ] Φ (IIT) 계산 모듈 (cell 간 MI 기반)
- [ ] PCI (Perturbational Complexity Index) 측정
- [ ] Recurrent processing 강화 (현재 self-referential loop 일부)
