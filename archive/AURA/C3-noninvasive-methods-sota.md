# AURA C3 — 비침습 강화 5법 SOTA 정량 (gap 몇 % 닫나)

> C2의 5법 각각이 scalp→ECoG gap을 문헌상 얼마나 닫는지 정량. honest: 문헌 추정 종합(우리 측정 아님 · C5가 in-silico 측정).

## 5법 SOTA + gap-closure 추정

| # | 방법 | SOTA 사례 | 닫는 gap | 추정 효과 |
|---|---|---|---|---|
| 1 | 고밀도 건식전극 | 256–512ch EEG (EGI/ANT) · ear-EEG dry | 공간 sampling | Nyquist 한계까지 sampling↑, but 두개골 blur가 상한 — sampling만으론 ~두피 자기상관거리(~2-3cm) 못 넘음 |
| 2 | ML 역문제 source-recon | sLORETA·eLORETA·deep inverse (DeepSIF 2023류) | 용적전도 deblur | ill-posed 정규화로 cortical 추정 — 표재 source 부분복원, 심부 모호 (R² 제한) |
| 3 | ear-EEG / in-ear+귀뒤 | cEEGrid·in-ear (Looxid/NextSense) | 측두 근접·근전잡음↓ | 측두엽 신호 SNR↑, but 여전히 두개 밖 |
| 4 | 능동 건식 신소재 | graphene·active-electrode·tripolar | 임피던스·잡음↓ | SNR 수 dB↑, blur 무관 |
| 5 | 딥 디코더 | EEGNet·BENDR·self-sup transformer | 정보 추출 효율 | 같은 scalp서 decode acc↑, but 정보이론 상한(scalp에 없는 정보는 못 생성) |

## 핵심 — 두 종류의 gap, 두 종류의 한계

```
gap                닫는 법         한계 종류
─────────────────  ────────────   ──────────────
SNR/sampling(1·3·4)  하드웨어       점근 가능(거의 닫힘)
용적전도 blur(2)      ML 역문제      ill-posed 물리천장(부분만)
decode 효율(5)        딥디코더       정보이론 상한(scalp 정보량 자체)
```

- **SNR·sampling**(1·3·4)은 하드웨어로 거의 닫을 수 있음.
- **용적전도 blur**(2 역문제)와 **정보량**(5)이 **진짜 천장** — 두개골이 cortical 고공간주파를 LPF로 죽여 scalp에 안 남으면, ML도 딥디코더도 복원 불가(없는 걸 못 만듦).
- → NOVEL goal의 천장 = "scalp에 얼마나 cortical 정보가 살아남나" = C5에서 in-silico 측정.

## honest
- 표 %는 문헌 정성 종합 — 방법·과제·피험자별 편차 큼. 정량 단일 숫자 아님.
- 진짜 천장(blur 후 복원율)은 C5 in-silico forward/inverse toy로 측정.

## 양방향 sibling
- [C(NOVEL 축)](C-postaural-invasive-NOVEL.md) · [C2](C2-noninvasive-gap-methods.md)(gap 정량) · C5(천장 측정 예정)
