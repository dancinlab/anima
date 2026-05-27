---
id: Hc_1237
slug: alm-lora-r4-r11-mode-collapse-free-convergence
title: ALM LoRA r4→r11 mode-collapse-free convergence base=scratch — rank 4..11 전 구간이 mode-collapse 없이 수렴하는가
domain: training
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 24 (Sub-claims block, TRAINING-2)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 8 of 30 (TRAINING-2). Has a concrete falsifier (Hc_900 F4) — most measurement-ready of the TRAINING seeds."
---

## Hypothesis

ALM 을 base=scratch (사전학습 base 없이) 로 두고 LoRA rank 를 r4 부터 r11 까지 키울 때, 전 rank 구간에서 mode-collapse 없이 안정 수렴한다 — rank 가 너무 작아 underfit 하거나 collapse 하는 구간이 없다.

## Falsifiable Tests

- T1 (= Hc_900 F4): r ∈ {5,6,7,8,9,10} 중 하나라도 독립 replication 에서 mode-collapse (출력 분포 entropy 붕괴 / 동일 토큰 반복) → "r4→r11 robust convergence" claim 은 해당 rank 에서 FALSIFIED
- T2: r4 에서 validation loss 가 plateau 에 못 미쳐 멈춤 (underfit) → 하한 4 가 너무 낮음 → claim 부분 FALSIFIED
- T3: r11 초과 (r12+) 에서도 추가 이득이 marginal 임을 보이면 r11 상한이 saturation 으로 정당화 (보강 증거); 반대로 r12+ 가 유의미 개선이면 상한 11 claim 약화

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, TRAINING-2)
- **sibling splits**: Hc_1236 (CLM pure-hexa pipeline), Hc_1238 (dual-track AGI gate), Hc_1239 (train_clm.hexa lens loss), Hc_1243 (ALM serve hot-LoRA-swap — same LoRA subject)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: ALM LoRA training (rank r4..r11), base=scratch config
