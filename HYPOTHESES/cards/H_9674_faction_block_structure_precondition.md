---
id: H_9674
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_block_structure_precondition
title: 현 기질의 유닛 축에 파벌형 모듈 블록 구조가 실재하는가 — H_9643(파벌 학습·GPU)의 $0 선결조건
status: PROPOSED · 계기 구현완료(`--faction-block-structure` · VERSION 0.15.28) · 발사중
tier: 🚦 GPU 게이트 — 블록 부재면 H_9643 은 학습시킬 대상이 없다 · $0
cost: $0
source: H_9673(옛 파벌=순환) 이후 남은 유일 질문의 선결조건 · H_9637 DV-MALFORMED 재정식
related: H_9643, H_9673, H_9660, H_9637, H_9645
---

# H_9674 — 기질에 파벌형 블록 구조가 실재하는가 (H_9643 의 $0 선결조건)

## 왜 이 관문이 필요한가

H_9673 이 옛 파벌을 **순환**으로 종결시켰다(sync 가 매 스텝 점수의 음수항을 직접 깎음). 하지만
"옛 파벌이 가짜였다"와 "파벌이라는 구조가 무용하다"는 **다른 주장**이다. 살아남은 유일한 질문은
**H_9643: 파벌이 현 기질에서 새로 학습될 수 있는가**(GPU). 그 발사는 기질에 **찾을 블록이 있을 때만**
정당하다. 이 카드가 그 선결조건을 $0 로 잰다.

## 주장 (반증가능)

프로덕션 trunk 의 penultimate 유닛 축은 참값 0 pedestal 대비 유의한 모듈 블록 구조를 갖지 **않는다**.
⟹ H_9643 은 학습시킬 대상이 없고 GPU 발사는 정당화되지 않는다.

## 레버 (engine-native)

```
anima-py evaluate <ckpt> --faction-block-structure <prompts.json> \
  [--n-factions-sweep 2,4,8,12,16] [--win 24] [--seed 12345] [--out blocks.json]
```
프로덕션 trunk forward(`clm_forward_hidden` · 게이트 디코드와 byte-identical) → X:[N,d]
→ 유닛간 |상관| 그래프 → greedy modularity 로 K 블록 탐색 → Newman Q.

## DV · bar · 우연수준

- DV = **real Q / pedestal Q** 의 K 최대값. 사전등록 bar = **≥1.5**.
- 우연 = pedestal(i.i.d. · 참값 Q=0). ⚠️ 유한표본 상관 잡음 때문에 pedestal 도 Q>0 이 나온다 —
  그래서 **raw Q 를 읽지 않는다**(p7).

## 통제군 (≥2 · 사전등록)

1. **pedestal** — real 의 평균·표준편차를 맞춘 i.i.d. 가우시안. 참값 Q=0.
2. **scramble** — real 값의 유닛별 독립 행 permutation. 유닛간 결합만 파괴, 주변분포 보존.
3. **⭐ 양성통제(필수)** — K 개 잠재인자로 **심은 블록**(SNR~3)을 같은 N/d 에서 복원하는가.
   bar = 자기 pedestal 대비 ≥1.5.

## 🛑 검정력 게이트 (`positive-control-before-reading-a-negative` · `power-before-negative-verdict`)

표본 상관행렬의 rank ≤ min(N,d). **N ≪ d 면 real 도 pedestal 도 유한표본 잡음에 지배**되어
둘의 일치는 "블록 없음"(기질 사실)이 아니라 **"검정력 없음"(계기 사실)**이다.

⟹ 계기는 **자기가 심은 블록을 먼저 복원**해야 한다. 실패하면 **음성을 발행하지 않고 rc=1 로 종료**한다
(코드로 강제 — 판독 불가한 음성은 음성이 아니다).

### 1차 발사가 이 게이트에 걸렸다 (자가감사 · 2026-07-17)

8 prompts × T=24 = **N=192 vs d=3784** ⟹ 상관행렬의 **95% 가 유한표본 잡음**.
완주해도 판독 불가라 **중단**하고 계기에 양성통제를 배선한 뒤 N 을 80 prompts(=1920 rows)로 올려 재발사.


## 🛠️ 계기 개발 이력 — 양성통제가 결함 2건을 잡았다 (2026-07-17)

이 카드의 가치 대부분은 **음성을 발행하지 않은 것**에 있다. 양성통제 없이 돌렸다면 두 번 다 "블록 없음
⟹ 축 종결" 이라는 그럴듯하고 틀린 결론이 나왔다.

| # | 결함 | 증상 | 잡은 통제 |
|---|---|---|---|
| 1 | **검정력 부족** — N=192(8 prompts) vs d=3784 | 상관행렬의 95% 가 유한표본 잡음 ⟹ real·pedestal 둘 다 잡음지배 | 자가감사(발사 전) → 중단 · N 10배(80 prompts=1920 rows) |
| 2 | **탐색 예산 부족** — 랜덤 40-move greedy | 심은 블록(SNR~3)조차 못 찾음: Q=−0.000072 vs pedestal −0.000096 = **x0.76 ⛔** | **양성통제** → rc=1 · 음성 미발행 |

수정: 랜덤 40-move → **spectral seed(상관 그래프 top-K 고유벡터) + full sweeps**, `modularity`/`best_blocks`
벡터화(파이썬 K-루프 → BLAS matmul), eigh 를 arm 당 1회 캐시(17회 → 5회).
자가검증(d=200 · N=1920): 심은 블록 **Q=0.741890 vs pedestal 0.025684 = x28.89** ✅ 계기 LIVE.

> ⚠️ Q 가 **음수**였다는 것이 결정적 단서였다 — greedy 가 랜덤 시작점에서 사실상 못 움직였다는 뜻.
> raw Q 를 읽었다면 "0 에 가까우니 블록 없음" 으로 오독했을 것이다. 비율(vs 자기 pedestal)이 살렸다.

## 사망조건 (사전등록)

- real/pedestal ≥1.5 (양성통제 통과 하에) ⟹ 블록 **실재** ⟹ 이 카드(블록 부재 주장) 사망 ∧ **H_9643 GPU 발사 정당화됨**.
- 양성통제 실패 ⟹ 판정 없음(계기 사실). 음성으로 읽지 않는다.

## 비용

$0 — frozen ckpt · 신규 학습 0.

## 정직범위 (⚠️)

- 상관-모듈러리티는 '모듈'의 **한 렌즈**다. `a_break_the_wall`: 천장 주장엔 ≥2–3 렌즈가 필요하므로
  음성이 나와도 **이 렌즈에서의 부재**이지 모든 렌즈에서의 부재가 아니다 ⟹ DIRECTIONAL.
- 프로덕션 .clm 은 E2/L1 conv trunk 다 — attention head 축이 없으므로 H_9659(파벌≡헤드) 의 대조항과 무관.
