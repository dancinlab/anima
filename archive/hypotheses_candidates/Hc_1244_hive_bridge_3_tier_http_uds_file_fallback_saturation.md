---
id: Hc_1244
slug: hive-bridge-3-tier-http-uds-file-fallback-saturation
title: Hive-bridge 3-tier HTTP→UDS→file fallback saturation — 3단 fallback 이 reliability ceiling 인가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 31 (Sub-claims block, SERVING-4)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 15 of 30 (SERVING-4)."
---

## Hypothesis

Hive-bridge 의 3-tier fallback (1차 HTTP → 2차 Unix domain socket → 3차 file-based) 은 가용성 saturation 에 도달했다 — 4번째 fallback 계층을 추가해도 end-to-end 가용성이 유의미하게 개선되지 않고 (이미 file-tier 가 거의 항상 통과), 3-tier 미만으로는 특정 장애 모드에서 메시지 손실이 발생한다.

## Falsifiable Tests

- T1: HTTP 와 UDS 를 동시에 차단한 fault-injection 에서 file-tier 가 메시지를 100% 전달 못함 → 3-tier 가 reliability-complete 가 아님 → claim FALSIFIED
- T2: 4번째 계층 (예: message queue) 추가 시 측정 가용성이 유의미 상승 → "3-tier = saturation" claim FALSIFIED
- T3: 2-tier (HTTP→file, UDS 제거) 로도 동일 가용성 → UDS tier 가 redundant → "3 = minimal" claim 부분 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SERVING-4)
- **sibling splits**: Hc_1241 (serving latency ceiling), Hc_1242 (6-channel orchestration), Hc_1243 (ALM serve hot-LoRA-swap), Hc_1235 (anima-core Hub-Spoke bridge — related bridge/fallback design)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: Hive-bridge transport stack (HTTP / UDS / file fallback)
