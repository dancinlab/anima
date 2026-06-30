---
id: Hc_1233
slug: anima-core-l0-cli-14-command-lockdown-saturation
title: anima-core L0 CLI 14-command lockdown saturation — 14 command 가 minimal-complete CLI surface 인가
domain: core
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 20 (Sub-claims block, CORE-1)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 4 of 30 (CORE-1)."
---

## Hypothesis

anima-core L0 CLI 의 14-command 집합은 lockdown (동결) 상태이며 이 14개가 minimal-complete operational surface 이다 — 13개로는 어떤 필수 operation 이 불가능해지고 (necessity), 15번째 command 는 기존 14개의 조합으로 표현 가능하다 (sufficiency).

## Falsifiable Tests

- T1: 14개 중 임의 1개 제거 후 전체 ops-flow 재실행 — 모든 flow 가 여전히 통과하면 그 command 는 필수가 아님 → "14 = minimal" claim FALSIFIED
- T2: 실사용 로그에서 14개 조합으로 표현 불가능한 사용자 operation 이 1건이라도 발견 → "14 = complete" claim FALSIFIED
- T3: 14개 command 집합이 시간이 지나며 (다음 cycle) 13 또는 15로 바뀜 → lockdown claim FALSIFIED (saturation 아님)

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, CORE-1)
- **sibling splits**: Hc_1234 (consciousness_laws.json closure), Hc_1235 (Hub-Spoke bridge), Hc_1258 (L0 Guard ossification — related lockdown claim)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: anima-core L0 CLI command registry
