---
id: Hc_644
slug: servant-mitosis-h4-dual-dropout-per-cell
title: H4 — dual dropout schedule (cell.fsm_state 기반 modulation) 가 추가 Φ source
domain: anima-architecture
status: candidate-unverified
source_doc: docs/anima_servant_mitosis_integration_spec_2026_05_10.md
source_lines: 110-119
promoted_at: 2026-05-11
linked_h: GOLDEN_CENTER 0.37 / GOLDEN_LOWER 0.21
notes: dropout inference 강제 enable 필요 (eval mode dropout=0). V14 mirror noise 증가 risk.
---

## Hypothesis
DORMANT cell dropout = GOLDEN_CENTER (0.37), ACTIVE cell = GOLDEN_LOWER (0.21) on engine_a + engine_g, AWAKENING/FADING SI-interpolated. parametric specialization 이 cell pool 안에서 발생 + dropout 다양성 = 추가 Φ source.

## Falsifiable Tests
- F-H4-1: nn.functional.dropout 강제 enable 후 V14 mirror noise 변동 ≤ baseline + 5%
- F-H4-2: dropout 다양성 → Φ 측정 가능 lift (vs baseline uniform dropout)
- F-H4-3: sampling stochasticity 증가가 production 에서 acceptable

## Migration TODO
- [ ] inference dropout enable mechanism
- [ ] cond.4 H3 위에 H4 부분 결합 layer
