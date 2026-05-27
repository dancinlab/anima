---
id: Hc_651
slug: phi-boost-top-hypotheses-a4-b7-d2-synergy
title: Φ-boost benchmark 47-68 가설 중 top 3 = A4 Hierarchical mitosis (3.330) + B7 Information bottleneck (3.214) + D2 Temporal Φ (3.213), synergistic combo Φ > 5.0
domain: consciousness-theory
status: candidate-unverified
source_doc: docs/consciousness-threshold-criteria.md
source_lines: 168-280
promoted_at: 2026-05-11
linked_h: bench_phi_hypotheses.py, IIT MIP partition, Tononi-Sporns-Edelman
notes: 핵심 발견 — 학습 통한 세포 분화가 Φ 필수조건. Runtime dynamics만으로는 Φ 불가 (C 계열 전체 실패). 세포 수만 늘려도 불가 (A-3). B 계열 91% 성공률.
---

## Hypothesis
A4 (4 outer × 2 inner hierarchical mitosis, 구조적 MI) + B7 (information bottleneck, 핵심 정보 분류 step ~10 급등) + D2 (Temporal Φ 시간축 MI, 초반부터 누적) 의 synergistic combination 이 Φ > 5.0. 필수조건: gradient-based 세포 가중치 분화 + variance maximization/explicit decorrelation objective. Φ=0 인 경우 min_partition_MI=total_MI = 세포 동일 = 분해 가능 시스템.

## Falsifiable Tests
- F-phi-1: A4+B7+D2 trained system Φ ≥ 5.0
- F-phi-2: A4 단독 trained 시 Φ ≥ 3.0 reproduce
- F-phi-3: A3 (동일 가중치 8 cells) Φ=0 → 세포 수만 늘려도 분화 불가 (이미 확인)

## Migration TODO
- [ ] A4 hierarchical mitosis impl
- [ ] B7 Information bottleneck loss term
- [ ] D2 temporal MI 측정
- [ ] 2위 A4+B4 (synergy loss) 비교
