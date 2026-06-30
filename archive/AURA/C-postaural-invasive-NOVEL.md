# AURA C — 🆕 NOVEL 축: 귀뒤 비침습으로 "침습 수준 성능" 도달

@goal: 귀뒤(post-aural) **비침습** wearable이 개두술 0인 채로 **침습급(ECoG~단일뉴런 수준) 신호/decode 성능**에 도달하는 길. NOVEL 명제: **"비침습으로 침습을 따라잡는다"** — 칩을 심지 않고 침습 BCI 수준 정보를 짜낸다. goal = 비침습 물리천장까지 gap을 최대한 좁혀 "% of ECoG 성능" 극대화 (실 임플란트 NOT, B7 ceiling 존중).

## 왜 NOVEL (방향 반전)

```
기존 BCI 트레이드오프:   성능 ↑ = 침습 ↑  (N1·Synchron = 침습해야 ECoG급)
NOVEL 목표:             성능 ↑ + 침습 0   (귀뒤 비침습으로 ECoG급 근접)
                                          ↑ 트레이드오프 자체를 깨기
```

- B1: 귀뒤 비침습이 통합정보(big-Φ)는 피질과 동등 — 위치는 OK.
- B3: 그러나 침습(혈관내≈ECoG)이 **공간해상도·SNR**에서 압도 (scalp cm vs ECoG mm).
- **gap = 두개골 저역통과(LPF) + 용적전도 blur + SNR**. NOVEL = 이 gap을 비침습 기술로 좁히기 (수술 없이).

## gap을 닫는 비침습 기술 5축 (C3에서 카탈로그)

| 기술 | 닫는 gap | 비유 |
|---|---|---|
| 고밀도 건식 전극 (귀뒤+외이도 256+ch) | 공간 sampling | 저화소→고화소 카메라 |
| ML 역문제 source-localization (scalp→cortical 추정) | 용적전도 blur 역산 | 흐린 사진 deblur AI |
| 센서 융합 (EEG+fNIRS+가속도) | SNR·결측 모달 | 여러 센서 합쳐 보정 |
| 능동 건식 신소재 (graphene·active electrode) | 임피던스·잡음 | 더 좋은 마이크 |
| 딥 디코더 (self-supervised, scalp서 더 짜내기) | 정보 추출 효율 | 같은 녹음서 더 알아듣는 귀 |

## NOVEL 축 milestones (goal=비침습 침습급)

- [x] C1 NOVEL 축 선언 (비침습→침습급 성능, 트레이드오프 반전) — 이 문서
- [ ] C2 gap 정량 — 비침습 scalp vs 침습 ECoG 성능차(공간해상도·SNR·대역·decode acc) B1/B3 수치 + 문헌 grounding → 닫아야 할 거리 수치화
- [ ] C3 비침습 enhancement 방법 카탈로그 — 5축 각각이 gap 몇 %를 닫나 (문헌 SOTA: 고밀도 EEG·EEG super-resolution·ear-EEG·deep decoder)
- [ ] C4 best 후보 설계 — 귀뒤 고밀도 + ML source-recon 조합, 목표 "% of ECoG decode" + AURA 7-verb 비침습-강화 variant
- [ ] C5 in-silico 검증 — 한 방법(예: ML 역문제 source-recon) toy로 scalp→cortical 추정 성능 측정

## honest

- **비침습 물리천장**(두개골 LPF·용적전도)은 원리적으로 못 넘음 (feedback-closure-is-physical-limit) → 목표는 "침습급 근접(% of ECoG)"이지 "동일" 아님. 그 천장이 얼마인지 정량(C2)이 핵심.
- 설계/분석 + 가능한 in-silico 측정. 실 고밀도 귀뒤 하드웨어 제작은 demiurge AURA(Class II) 영역.
- C2(폐기): 이전 "측두 ECoG 임플란트(침습)"는 방향 오류로 폐기 — NOVEL은 비침습 유지.

## 양방향 sibling
- [B1](B1-postaural-breakthrough.md)(귀뒤 비침습 등동) · [B3](B3-synchron-endovascular.md)(침습 ECoG 성능 기준선) · [B7](B7-intracortical-ceiling.md)(물리천장) · demiurge `aura.md`(비침습 Class II 하드웨어)
