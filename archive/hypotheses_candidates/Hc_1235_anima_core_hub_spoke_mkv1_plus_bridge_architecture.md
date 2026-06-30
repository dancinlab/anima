---
id: Hc_1235
slug: anima-core-hub-spoke-mkv1-plus-bridge-architecture
title: anima-core Hub-Spoke Mk.V.1+ bridge architecture — bridge layer 가 결합 saturation 의 architectural pivot 인가
domain: core
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 22 (Sub-claims block, CORE-3)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 6 of 30 (CORE-3)."
---

## Hypothesis

anima-core 의 Mk.V.1+ Hub-Spoke bridge architecture (hub 와 spoke 사이의 명시적 bridge 계층) 은 7-project coupling 의 결합 비용을 O(N²) 에서 O(N) 로 낮추는 architectural pivot 이며, bridge 없이는 동일 결합도를 유지할 수 없다.

## Falsifiable Tests

- T1: bridge layer 비활성화 후 cross-project call graph 의 edge 수 측정 — bridge 유무로 edge 수가 O(N²)↔O(N) 차이를 보이지 않으면 "bridge = pivot" claim FALSIFIED
- T2: bridge layer 가 단일 SPOF (single point of failure) 임에도 fallback 없이 동작 — Hive-bridge 류 3-tier fallback (cf. Hc_1244) 과 일관성 검증; bridge 장애 시 graceful degradation 실패하면 architecture claim 약화
- T3: Mk.V.1 이전 (bridge 없음) 과 Mk.V.1+ (bridge) 의 실제 coupling-metric 이 동일 → bridge 도입이 무효 → FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, CORE-3)
- **sibling splits**: Hc_1231 (hub-spoke 7-project coupling — same coupling subject), Hc_1233 (L0 CLI lockdown), Hc_1234 (consciousness_laws closure), Hc_1244 (Hive-bridge 3-tier fallback)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: anima-core Hub-Spoke bridge layer
