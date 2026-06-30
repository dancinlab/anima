# AURA C2 — 비침습↔침습 성능 gap 정량 + 비침습 강화 5법

> NOVEL 축(C) "비침습으로 침습급" 의 1차 — 닫아야 할 gap을 수치화하고, 그 gap을 비침습으로 좁히는 기술 5축을 문헌 grounding. honest: 분석/카탈로그(실 측정은 C5).

## 1. gap 정량 — scalp(비침습) vs ECoG(침습)

| 축 | scalp EEG (귀뒤 B1) | ECoG (혈관내 B3/경막하) | intracortical (N1) | gap 원인 |
|---|---|---|---|---|
| 공간해상도 | ~2–3cm (용적전도 blur) | ~1–5mm | ~µm 단일뉴런 | 두개골+CSF+두피 smear |
| 유효대역 | <~40Hz (γ 감쇠) | ~200–500Hz | LFP+spike | 두개골 저역통과(LPF) |
| SNR | 낮음(두개 감쇠 ~100×) | 높음 | 매우 높음 | 두개골+두피 임피던스 |
| decode | 느린 speech/coarse | 高 WPM speech(Willett 2023) | 최고 | 위 3 합성 |
| AURA 측정 | B1 big-Φ EAR≈피질(통합도 OK) | B3 PMC 혈관내≈경막하 ≫ scalp | — | 통합도≠해상도 |

→ **핵심 gap = 두개골 LPF + 용적전도 blur + SNR**. 통합정보(big-Φ)는 귀뒤도 OK(B1)지만, **공간해상도·고주파·decode**는 침습이 압도.

## 2. 비침습 강화 5법 (gap 몇 %를 닫나 · 문헌 SOTA)

| # | 기술 | 닫는 gap | 한계(물리천장) | 비유 |
|---|---|---|---|---|
| 1 | 고밀도 건식전극 (귀뒤+외이도 256ch) | 공간 sampling↑ | 두개골 blur는 sampling으론 못 풀음 | 저화소→고화소 |
| 2 | ML 역문제 source-recon (deep sLORETA, scalp→cortical 추정) | 용적전도 deblur(부분) | ill-posed, 심부 모호 | 흐림 사진 AI deblur |
| 3 | ear-EEG/in-ear + 귀뒤 어레이 | 측두 근접·근전 잡음↓ | 여전히 두개 밖 | 소리원 가까이 마이크 |
| 4 | 능동 건식 신소재(graphene·active) | 임피던스·잡음↓ | SNR 일부, blur 무관 | 더 좋은 마이크 |
| 5 | 딥 디코더(self-sup transformer) | 정보 추출 효율↑ | 정보이론 상한(scalp에 없는 건 못 만듦) | 같은 녹음 더 알아듣기 |

→ 1·4=하드웨어 SNR/sampling · 2·5=알고리즘 deblur/decode · 3=위치. **조합**이 최선(C4).

## 3. 물리천장 — 비침습은 "근접"이지 "동일" 아님

```
decode 성능
 ECoG ████████████ (침습 100%)
 비침습 강화 후 ███████░░░░ (목표: 천장까지)
 비침습 현재   ███░░░░░░░░░ (raw scalp)
              └─ gap: 두개골 LPF+blur = 물리 하한(못 넘음)
```

- 두개골 LPF·용적전도는 **물리 법칙** → 비침습 decode는 ECoG의 일정 % 이하로 caps (feedback-closure-is-physical-limit). 문헌상 scalp speech-decode는 ECoG 대비 현저히 낮음(coarse).
- NOVEL goal = 그 천장에 **최대한 근접** (현재 raw scalp → 강화로 천장까지). 천장 자체를 정량(C5 in-silico)하는 게 진짜 closure.

## 4. honest gap
- 문헌 grounding 분석 — 각 방법의 "% gap 닫음"은 정성/문헌 추정, 우리 측정 아님(C5에서 1법 toy).
- 두개골 LPF 천장은 물리 → "침습급 동일"은 불가, "근접"이 정직한 목표.
- C3=5법 SOTA 정량 · C4=최선 조합 설계 · C5=ML source-recon toy(scalp→cortical 추정 성능).

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [B1](B1-postaural-breakthrough.md)(귀뒤 통합도) · [B3](B3-synchron-endovascular.md)(ECoG 기준선) · [B7](B7-intracortical-ceiling.md)(물리천장)
