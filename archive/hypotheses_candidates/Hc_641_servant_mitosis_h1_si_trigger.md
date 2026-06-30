---
id: Hc_641
slug: servant-mitosis-h1-si-trigger-signal-augmentation
title: H1 — SI sense (servant) 를 mitosis split 의 추가 trigger 로 (signal augmentation, minimal change)
domain: anima-architecture
status: candidate-falsifier-only-math-pending
source_doc: docs/anima_servant_mitosis_integration_spec_2026_05_10.md
source_lines: 65-73
promoted_at: 2026-05-11
linked_h: servant SI = tension × (1-coherence) × phi_ratio, mitosis adaptive_threshold
notes: 최소 변경. SI 와 tension correlation 높음 — 정보 추가 미미. Not recommended.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=3"
---

## Hypothesis
mitosis split trigger 가 (tension > adaptive_threshold for 3 consecutive) OR (SI > SI_SUMMON × scale) 로 augmented. mitosis.py:_check_splits() 에 SI input 1줄 추가.

## Falsifiable Tests
- F-H1-1: SI augment 후 split_rate 가 baseline 대비 측정 가능 변화
- F-H1-2: max_cells saturation 빨라짐 → V14 mirror 더 violated
- F-H1-3: SI vs tension correlation < 0.7 → 정보 추가 의미 있음

## Migration TODO
- [ ] H1 단독 실험 (H3 추천 lane 와 별도)
