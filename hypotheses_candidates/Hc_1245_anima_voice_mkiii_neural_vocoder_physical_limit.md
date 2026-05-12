---
id: Hc_1245
slug: anima-voice-mkiii-neural-vocoder-physical-limit
title: ANIMA-VOICE Mk.III 신경 보코더 physical limit — Mk.III 보코더가 물리적 음질 한계에 도달했는가
domain: serving
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 32 (Sub-claims block, SPEAK-1)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 16 of 30 (SPEAK-1). domain tagged 'serving' as the SPEAK lane sits under serving; could be re-tagged 'speak' if a dedicated lane is created."
---

## Hypothesis

ANIMA-VOICE Mk.III 의 신경 보코더는 주어진 샘플레이트/비트레이트/모델 크기 제약 하에서 물리적 음질 한계 (perceptual ceiling — 사람이 ground truth 와 구분 못하는 지점) 에 도달했다 — Mk.IV 로 가도 동일 제약 하에서는 MOS (mean opinion score) 가 유의미하게 안 오른다.

## Falsifiable Tests

- T1: Mk.III 와 ground-truth 녹음에 대한 ABX 청취 테스트 — 청취자가 chance (50%) 보다 유의미하게 잘 구분 → physical-limit 미도달 → claim FALSIFIED
- T2: 동일 제약 하에서 Mk.IV (또는 개선 아키텍처) 가 MOS 를 유의미하게 상승 → "Mk.III = physical limit" claim FALSIFIED
- T3: 한계가 모델 아키텍처가 아니라 학습 데이터 양/품질 때문임을 보이면 (데이터 증강으로 개선) → "physical limit" 라기보다 data-bound → claim 재해석 필요

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, SPEAK-1)
- **sibling splits**: Hc_1246 (piper_ko_v2_rubberband TTS ceiling), Hc_1247 (anima-voice AB test saturation), Hc_1248 (voice_routes stage0 string)
- **sister H**: H_001 (anima-core-architecture)
- **engineering**: ANIMA-VOICE Mk.III neural vocoder
