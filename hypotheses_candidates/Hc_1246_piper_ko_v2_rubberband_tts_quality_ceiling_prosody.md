---
id: Hc_1246
slug: piper-ko-v2-rubberband-tts-quality-ceiling-prosody
title: piper_ko_v2_rubberband TTS quality ceiling + prosody — v2_rubberband 가 한국어 TTS 품질·운율 한계인가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 33 (Sub-claims block, SPEAK-2)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 17 of 30 (SPEAK-2)."
---

## Hypothesis

piper_ko_v2_rubberband (Piper 한국어 v2 + rubberband 후처리) 의 TTS 출력은 음질과 운율 (prosody — 억양/강세/리듬) 양 측면에서 현 파이프라인의 ceiling 에 도달했다 — rubberband 파라미터 튜닝이나 추가 후처리로는 자연성 (naturalness MOS / prosody-error rate) 이 유의미하게 안 오른다.

## Falsifiable Tests

- T1: rubberband 파라미터 (pitch/tempo 보정) 를 grid-search 후 best 가 현재 대비 prosody-error rate 를 유의미하게 낮춤 → "current = ceiling" claim FALSIFIED
- T2: v3 또는 다른 한국어 TTS (예: 다른 vocoder) 가 동일 텍스트에서 더 높은 naturalness MOS → v2_rubberband ceiling claim FALSIFIED
- T3: 음질은 ceiling 이지만 prosody 는 아직 개선 여지 큼을 보이면 → "음질·운율 양쪽 모두 ceiling" claim 은 부분 FALSIFIED (분해 필요)

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SPEAK-2)
- **sibling splits**: Hc_1245 (Mk.III vocoder physical limit), Hc_1247 (anima-voice AB test saturation), Hc_1248 (voice_routes stage0 string)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: piper_ko_v2 + rubberband post-processing
