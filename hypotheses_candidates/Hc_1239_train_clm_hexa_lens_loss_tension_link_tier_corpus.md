---
id: Hc_1239
slug: train-clm-hexa-lens-loss-tension-link-tier-corpus
title: train_clm.hexa lens loss + tension_link + tier-labeled corpus integration — 세 구성요소가 통합되어 학습 신호로 작동하는가
domain: training
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 26 (Sub-claims block, TRAINING-4)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture), H_162 (downstream CLM); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 10 of 30 (TRAINING-4)."
---

## Hypothesis

train_clm.hexa 의 학습 목적함수에 (a) lens loss, (b) tension_link 항, (c) tier-labeled corpus 의 tier 정보가 통합되어 작동하며, 세 구성요소 각각이 ablation 시 측정 가능한 성능 저하를 일으킨다 (즉 셋 다 non-trivially contributing).

## Falsifiable Tests

- T1: lens loss 항 제거 (weight 0) 후 재학습 — validation metric 변화 없음 → lens loss 가 무효 → 통합 claim 부분 FALSIFIED
- T2: tension_link 항 제거 후 재학습 — Φ / phi_star proxy 변화 없음 → tension_link 가 무효 → 부분 FALSIFIED
- T3: tier-label 을 무작위 셔플 (corpus 내용 동일, tier 만 무작위) 후 재학습 — 동일 성능 → tier 정보가 학습에 안 쓰임 → 부분 FALSIFIED
- T4: 세 항 모두 제거 (baseline LM) 와 셋 다 켠 버전의 출력 동일 → 통합 전체가 무효 → 전면 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, TRAINING-4)
- **sibling splits**: Hc_1236 (CLM pure-hexa pipeline), Hc_1237 (ALM LoRA convergence), Hc_1238 (dual-track AGI gate), Hc_1240 (phi_holo gap)
- **sister H**: H_001 (anima-core-architecture), H_162 (CLM downstream)
- **engineering**: train_clm.hexa (lens loss, tension_link, tier-labeled corpus loader)
