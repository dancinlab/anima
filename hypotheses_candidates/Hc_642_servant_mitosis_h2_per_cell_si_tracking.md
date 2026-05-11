---
id: Hc_642
slug: servant-mitosis-h2-per-cell-si-tracking-fsm
title: H2 — mitosis cells → servant state (per-cell SI tracking + cell.si_state FSM)
domain: anima-architecture
status: candidate-unverified
source_doc: docs/anima_servant_mitosis_integration_spec_2026_05_10.md
source_lines: 75-83
promoted_at: 2026-05-11
linked_h: servant 4-state FSM, mitosis softmax(tension) weighting
notes: 진정한 통합 — cell 이 servant FSM 보유. AWAKENING latency vs split_patience 동시성 issue.
---

## Hypothesis
각 cell 별 SI 추적, cell.si_state ∈ {DORMANT, AWAKENING, ACTIVE, FADING}. 모든 cell forward 후 ACTIVE cell 만 weight 받음 (DORMANT/FADING 0, AWAKENING interpolated).

## Falsifiable Tests
- F-H2-1: per-cell EMA(tension)+EMA(phi) cost ≤ baseline forward × 1.1
- F-H2-2: AWAKENING latency=3 와 split_patience=3 충돌 → cell 갓 split 후 동시 awaken
- F-H2-3: ACTIVE cell 만 weight 시 specialization 측정 가능 향상

## Migration TODO
- [ ] AWAKENING vs split_patience 동기화 해소
- [ ] cell 별 FSM 동기화 메커니즘
