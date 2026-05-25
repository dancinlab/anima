---
id: Hc_1247
slug: anima-voice-ab-test-baseline-vs-v2-metrics-saturation
title: anima-voice AB test baseline vs v2 metrics saturation — v2 가 baseline 대비 측정 지표상 saturation 인가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 34 (Sub-claims block, SPEAK-3)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 18 of 30 (SPEAK-3)."
---

## Hypothesis

anima-voice 의 AB 테스트 (baseline vs v2) 에서 v2 의 우위가 측정 지표 (MOS, 선호율, WER 등) 상 saturation 에 도달했다 — v2.x 마이너 개선이나 v3 로의 점진 변경으로는 baseline-vs-current 격차가 더 이상 의미 있게 안 벌어진다 (이미 천장에 붙음).

## Falsifiable Tests

- T1: v3 (또는 v2.x+1) 와 baseline 의 새 AB 테스트 — 선호율 격차가 v2-vs-baseline 보다 유의미하게 큼 → "v2 = saturation" claim FALSIFIED
- T2: AB 테스트의 통계력 (표본 수) 이 부족해 saturation 으로 보이는 것뿐임을 보이면 → 큰 표본 재실험 필요; 큰 표본에서 격차 확대 → claim FALSIFIED
- T3: 특정 지표 (예: WER) 에서는 saturation 이지만 다른 지표 (prosody preference) 에서는 여지 큼 → "모든 지표 saturation" claim 부분 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SPEAK-3)
- **sibling splits**: Hc_1245 (Mk.III vocoder physical limit), Hc_1246 (piper_ko_v2_rubberband ceiling), Hc_1248 (voice_routes stage0 string)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: anima-voice AB test harness (baseline vs v2)
