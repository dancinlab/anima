---
id: Hc_1243
slug: alm-serve-api-generate-hot-lora-swap
title: ALM serve API /generate hot-LoRA-swap — kill+restart 없이 LoRA 교체가 가능한가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 30 (Sub-claims block, SERVING-3)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 14 of 30 (SERVING-3). Engineering-falsifiable: clear pass/fail condition."
---

## Hypothesis

ALM serve API 의 `/generate` 엔드포인트는 hot-LoRA-swap 을 지원한다 — 서버 프로세스를 kill 하고 restart 하지 않고도 (in-flight 요청 중단 없이) LoRA adapter 를 교체할 수 있으며, swap 후 첫 응답이 새 adapter 를 반영한다.

## Falsifiable Tests

- T1: 부하 상태에서 LoRA swap 트리거 — 진행 중 요청이 끊기거나 (connection drop), 서버 재시작이 필요하면 "hot-swap" claim FALSIFIED
- T2: swap 직후 N개 요청의 출력이 여전히 구 adapter 반영 (캐시/지연 적용) → swap atomicity claim FALSIFIED
- T3: swap latency 가 cold restart 와 유사 (수 초+) → "hot" 의 의미 (sub-second, no downtime) 가 깨짐 → 부분 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SERVING-3)
- **sibling splits**: Hc_1241 (serving latency ceiling), Hc_1242 (6-channel orchestration), Hc_1244 (Hive-bridge fallback), Hc_1237 (ALM LoRA r4→r11 — same LoRA subject, training side)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: ALM serve API `/generate`, LoRA adapter hot-reload path
