---
id: Hc_1240
slug: phi-holo-gap-816x-benchmark-vs-training-closure
title: phi_holo gap 816× benchmark vs training closure — 816배 격차가 학습으로 좁혀지는가
domain: training
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 27 (Sub-claims block, TRAINING-5)
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry — Φ), H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 11 of 30 (TRAINING-5). Has a concrete numeric anchor (816×) so it is measurement-shaped."
---

## Hypothesis

phi_holo (holographic Φ proxy) 가 benchmark 평가 시점과 training 종료 시점 사이에 816× 격차를 보이며, 이 격차는 training 으로 (현 파이프라인 또는 개선 파이프라인) 폐쇄 가능하다 — 즉 격차가 측정 artifact 가 아니라 학습-수렴-부족이다.

## Falsifiable Tests

- T1: 추가 학습 (longer schedule / 더 큰 corpus) 후 phi_holo 격차 측정 — 격차가 816× 에서 줄지 않음 → "training 으로 폐쇄 가능" claim FALSIFIED (격차가 architectural / measurement artifact)
- T2: benchmark phi_holo 와 training phi_holo 의 측정 방식 (slice 기하, normalization) 이 다름을 보이면 816× 는 apples-to-oranges → 격차 자체가 spurious → claim FALSIFIED
- T3: 격차 비율이 substrate 마다 (CLM v4 vs Pythia vs Mamba) 크게 다름 → "816×" 는 보편 상수가 아니라 substrate-specific → claim 일반화 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, TRAINING-5)
- **sibling splits**: Hc_1236 (CLM pure-hexa pipeline), Hc_1239 (train_clm.hexa lens loss), Hc_1241 (serving latency ceiling)
- **sister H**: H_011 (iit-geometry — Φ measurement), H_174 (phi_star geometry aliasing — measurement-validity bound)
- **candidates linked**: Hc_614 (phi_star geometry aliasing — cross-substrate Φ comparability caveat)
