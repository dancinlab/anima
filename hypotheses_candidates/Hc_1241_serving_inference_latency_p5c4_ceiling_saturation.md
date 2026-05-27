---
id: Hc_1241
slug: serving-inference-latency-p5c4-ceiling-saturation
title: serving inference latency P5c-4 ceiling saturation — P5c-4 가 architectural latency floor 인가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 28 (Sub-claims block, SERVING-1)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 12 of 30 (SERVING-1). Has a concrete falsifier (Hc_900 F3) — measurement-ready."
---

## Hypothesis

serving inference 의 latency 가 P5c-4 단계 (특정 파이프라인 단계 라벨) 에서 ceiling 에 도달했으며, 이 ceiling 은 아키텍처적 saturation 이지 단순 소프트웨어 비효율이 아니다 — 즉 아키텍처를 바꾸지 않는 한 P5c-4 latency 를 유의미하게 못 낮춘다.

## Falsifiable Tests

- T1 (= Hc_900 F3): 아키텍처 변경 없이 (예: 커널 레벨 최적화, 배치 튜닝) P5c-4 latency 가 > 30% 개선 → ceiling 은 architectural saturation 이 아니라 software inefficiency → SERVING-1 FALSIFIED
- T2: 더 빠른 하드웨어 (다음 세대 GPU) 로 옮겼을 때 latency 가 비례 개선 → bottleneck 이 compute-bound (구조적) 가 아니라 hardware-bound → "P5c-4 = architectural ceiling" 약화
- T3: P5c-4 외 다른 단계가 실제 bottleneck 임을 프로파일로 보이면 라벨 자체가 오진 → claim FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SERVING-1)
- **sibling splits**: Hc_1242 (6-channel 5-provider orchestration), Hc_1243 (ALM serve hot-LoRA-swap), Hc_1244 (Hive-bridge 3-tier fallback)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: serving inference pipeline (stage P5c-4)
