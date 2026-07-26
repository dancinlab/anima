# H_9986 · 사전등록 — 자연 **대화** 코퍼스는 **상대 때문에** 재조합-연산자를 공급하는가?

**상태: PROPOSED · 판정표 동결 · 측정 0 · 계기 = 인증된 `anima-py evaluate --earned` · $0**
**계열: H_9984 ① 결합 사다리의 공급 다리 사전관문 · 선행 = H_9968(독백 사다리 CLOSED) · H_9985(MEASURED)**

## 왜 이걸 먼저 재는가

H_9984 가 지목한 **미개봉 공급 칸**은 "코퍼스에 상대방이 없었다"이다. 지금까지 잰 건(H_9968 의 41× 사다리
포함) 전부 **리뷰=독백**이라, 학습 텍스트가 다음-바이트 예측을 **상대의 직전 발화에 의존**하게 만든 적이 없다.
① 결합 사다리는 세 다리 중 하나로 이 공급을 깔고 서는데, 그 다리가 실재하는지 **학습 없이 $0 로** 먼저
재는 게 표준이다(비싼 레버 앞의 사전관문 · 공급 ~0 이면 에스컬레이션 사살에 충분).

## 계기가 부과한 제약 — 맨 대화 코퍼스로는 질문 자체가 안 선다

`--earned` 는 `(text, B, T)` 를 요구하고 **T 는 토큰 밖 사람 주석**이어야 한다. 코드의 근거:
*"If A, B and T are all read off the same token stream, then 'trigram beats bigram-product' is true
BY CONSTRUCTION — a tautology, not an experiment. So this instrument requires a LABELLED corpus;
pure web/wiki cannot even pose the question."* ⟹ 라벨 없는 대화 덤프는 이 계기로 못 잰다.
그래서 **사람이 발화마다 주석을 단 자연 대화**를 쓴다.

## 코퍼스 — DailyDialog (자연 · 사람 주석 · EN)

`li2017dailydialog/daily_dialog` · 13,118 대화 · 87,170 발화 · 발화마다 **감정(7종)·화행(4종) 사람 주석**.
합성 드릴이 아니라 자연 대화이므로 p9 regime = **`natural`**. EN-FIRST 지시에도 부합.

- **행** = 발화 t (= 응답). t≥2 로 제한 — t−1(상대)과 t−2(자기)가 **둘 다** 존재해야 두 팔이 같은 행을 채점한다.
- **A** = 응답 본문의 내용어 어간 (계기가 뽑음)
- **T** = 응답에 감정이 달렸는가(`emotion != 0`) — **주석자 판단**이지 토큰에서 결정되지 않는다.
  (화행은 `?` 로 사실상 결정돼 tautology 위험이 있어 T 로 쓰지 않는다.)
- **B** = 이진 맥락 비트. **여기가 대화 고유의 축이다.**

## 조작 — B의 **출처만** 바꾼 짝지은 두 팔

| 팔 | B 출처 | 뜻 |
|---|---|---|
| `partnerB` | **t−1 = 상대의 직전 발화**가 감정을 띠었는가 | 처치 — "상대 때문에" |
| `selfB` | **t−2 = 자기 자신의 직전 발화**가 감정을 띠었는가 | 🧱 **짝지은 통제 — 독백-B** |

같은 코퍼스·같은 행·같은 본문·같은 T, **오직 B의 출처만** 다르다(실제로 갈리는 행 12,291 / 76,743 = 16.0%).
⟹ 차이가 나오면 그건 "시간 맥락 일반"이 아니라 **상대**가 산 것이다
([[control-must-match-mediating-covariate]] — 명목만 맞춘 통제가 아니라 매개 공변량을 맞춘 통제).

행 76,743 · T=1 비율 0.180(양 팔 동일) · B=1 비율 partner 0.153 / self 0.137.
⚠️ B 주변확률이 완전히 같지는 않다(0.016 차). 계기의 귀무는 **T 층 안에서만 B를 치환**하므로 P(B,T)는
보존되지만, 이 불균형은 결과 해석 시 명시한다.

## DV 와 자

- **DV = EARNED (nats)** — held-out (A, B=1) 셀에서 `[CE_add − CE_op]관측 − [CE_add − CE_op]치환`.
  학습 모델 미접촉이라 **공급 상한**이다.
- **자(ruler)** = 계기가 연산자를 **심어 둔** 코퍼스에서 읽는 값 **+5.29653 nats**. 절대값이 아니라 이 자 대비로 읽는다.
- **선행 기준선** = H_9968 독백 사다리 5 rung 전부 **DATA-ADDITIVE**(최대 +0.00438, 41× 에 단조 비증가).
- seeds 기본 3 — 단일 draw 로 순위 주장 금지(구간 겹치면 "더 크다" 불가).

## 판정표 (사전 동결 · 발사 전)

**V. 계기 게이트 — 계기 자신이 강제한다. 통과 못 하면 아래를 읽지 않는다**
- `G-ALIVE`(합성 XOR ≥ +0.30) ∧ `G-PEDESTAL`(합성 가법 |EARNED| ≤ 0.02) ∧ `G-POWER`(MDE_3σ ≤ 0.02).
- `G-POWER` 실패 = **INVALID/DATA-SPARSE**, 결코 KILL 아님 — 작은 n 은 음성 결과가 아니다.

| 결과 | 조건 | 읽기 |
|---|---|---|
| 🟢 **DIALOGUE-SUPPLY** | `EARNED(partnerB) ≥ +0.05` ∧ `EARNED(partnerB) − EARNED(selfB) ≥ 3·MDE` | **상대가** 비가법 연산자를 공급한다. H_9984 의 미개봉 공급 칸이 실재 ⟹ ① 결합 사다리가 설 코퍼스가 생긴다 |
| ⚪ **NOT-DIALOGUE-SPECIFIC** | 두 팔 다 ≥ +0.05 인데 차이 < 3·MDE | 공급은 있으나 **상대가 아니라 시간 맥락**이 산 것 ⟹ "코퍼스에 상대방이 없었다" 프레임은 값을 못 산다(이력 있는 독백도 같은 걸 준다) |
| 🔴 **DATA-ADDITIVE (KILL)** | 두 팔 다 `|EARNED| < max(0.02, 3·MDE)` | 대화도 닫힌 독백 사다리보다 더 공급하지 않는다 ⟹ **미개봉 공급 칸이 닫힌다**; ① 결합 사다리는 (3) 공급 다리를 잃는다 |
| 🟠 **REVERSED** | `EARNED(selfB) − EARNED(partnerB) ≥ 3·MDE` | 자기 이력이 상대보다 더 공급 — 우연 아래쪽까지 표가 덮는다([[prereg-table-must-cover-below-chance]]), 그 자체가 결과 |

## 범위 — 이 카드가 살 수 없는 것

- **필요조건이지 충분조건이 아니다.** 공급 > 0 은 "어떤 모델이 뽑을 수 있는 것이 있다"까지이고, 뽑는다는
  주장이 아니다. 반대로 공급 ≈ 0 은 학습 에스컬레이션을 **사살하기엔 충분**하다($0 스크리너의 요점).
- **대화 능력 주장 아님.** COMPOSE 는 여전히 G1(결합기)의 몫이다(H_9985 가 실측으로 확인).
- **공급은 상한**이고 값싼 경로 필터 전까지는 그렇다([[supply-density-is-an-upper-bound-until-the-shortcut-filter]]).

## 실행

```
anima-py evaluate --earned dd_partnerB.tsv --out partnerB.json
anima-py evaluate --earned dd_selfB.tsv    --out selfB.json
```
$0 · 순수 numpy · 학습 모델 미접촉. regime = `natural`.
