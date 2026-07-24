# H_9968 · 사전등록 — 자연-코퍼스 재조합-연산자 **공급**은 데이터-스케일로 증가하는가 (유일 미개봉 셀)

**상태: PROPOSED · 판정표 동결(숫자 읽기 전) · 미측정 · DIRECTIONAL 스크리너(p9 · regime=natural)**

## 왜 이 축인가 — p9가 명시한 마지막 빈 칸
anima 그리드에서 밀도·목적·깊이/RF 는 닫혔고, 파라미터 스케일(303M→1B→7B)은 amplifier-not-lever(H_1139)이나
**작은 MB 코퍼스서만 측정**돼 데이터축을 구속 못 한다. arch-class 는 CONTESTED(sampler-fragile, 인용금지).
남은 유일한 empty cell = **자연 코퍼스를 데이터-스케일로 밀 때 연산자 공급이 커지는가.** 우리 clean 코퍼스는
MB(~10⁶⁻⁷ 토큰), LLM 은 ~10¹²(5-6자릿수 위). 직전 종결(earned-operator-supply): EN-KO 격차는 길이/코퍼스-구조
artifact, 길이 맞추면 EN-FREE +0.00806 ≈ KO-FREE +0.00643(CI겹침) = 자의(XBIND +5.29653)의 **0.13%**. 벽은
양 언어·매칭길이서 선다. 이 카드는 그 벽이 **데이터-스케일에도 불변인지** 묻는다.

## 계기 (고정 · 재설계 금지)
`anima-py evaluate --earned <corpus.tsv>` — 코퍼스 통계가 전이되는 비가법 연산자를 **얼마나 공급**하는지(순수 numpy,
학습 모델 미접촉 = SUPPLY 상한). 공급 ~0 이면 어떤 모델도 못 뽑음 = 학습 에스컬레이션 **사살 충분**. 3게이트(G-ALIVE·
G-PEDESTAL·G-POWER) 매 rung n 에서 재인증. 자의 +5.29653.

## 조작화 — nested 크기 사다리 (길이 FIXED)
- **Corpus: Amazon Polarity**(`fancyzhx/amazon_polarity` 3.6M · 자연 고객리뷰 · 인간 별점라벨 = 토큰스트림 외부 ·
  풍부한 자유부정). Sentiment140 실격(이모티콘 distant-supervision·라벨이 원래 토큰 내부). Yelp 560k = 2차 복제팔 보류.
- **길이 고정밴드 20-50 토큰**(SST-2 long 층과 겹침), 모든 rung 이 이 in-band pool 의 **nested 부분집합**(단일 동결
  seed, rung r ⊂ r+1) → "크기↑=길이믹스↑" 교란 **구조적 차단** + 파편화 driver(고정 접두창)도 rung-불변.
- **사다리**: 30k → 100k → 300k → 1M → ALL-in-band. B=부정비트(EN FREE 폐집합 not/no/never/n't…), T=별점(1-2→0·4-5→1).

## 판정표 (동결 · 측정 전 · held-out EARNED nats)
기준 b=+0.007(매칭길이 baseline) · zero-band 단위 0.02 · 자의 R=+5.29653. rung 유효성 먼저(G-POWER MDE≤0.02 아니면
그 rung INVALID, KILL 아님).

| 유효 rung 전반의 패턴 | 판정 |
|---|---|
| 모든 rung ≤ +0.03 ∧ 총상승 < max(0.02, 3×MDE_top) | 🔴 **CLOSED** — 벽은 라벨-자연 전범위서 데이터-스케일 불변(스크리너 강도) |
| 단조상승 ∧ EARNED(top) ≥ +0.05(자의 ~1%·7b) ∧ 총상승 ≥ 0.02 ∧ 아래 공급검정 통과 | 🟢 **OPENS** — 첫 실균열 · Q4 에스컬레이션 |
| 상승하나 top < +0.05 | ⚠️ **GROWING-SLOW** — 균열 아님 · decade당 log-선형 기울기+자의1%까지 decade수 기록 · 불가능 규모면 사실상 CLOSED |
| 스케일서 유의 **음수** | sign-anomaly(반연산자) — OPENS도 CLOSED도 아님 · 계기정렬 조사 선행(우연아래 판정표 포함) |
| 어느 rung 게이트 red | 그 rung INVALID · top rung INVALID면 verdict 무 · 인증부터 수리 |

**추정기-vs-공급 분리(정직 경계)**: held-out EARNED 은 작은 n서 하향편향·셀 차면서 상향수렴 → 참공급 불변이어도 n 따라
오른다. 구분 서명(G-POWER 가 이미 보고): 수렴상승은 MDE 아직 줄 때 발생·그 축소와 크기비슷 / 공급상승은 정밀 포화 **후에도**
지속. **OPENS 요건: 총상승의 ≥0.02 가 MDE≤0.01 rung(정밀포화 구간·실무상 300k→1M→top)서 나야 함.** 전상승이 저-n rung
(ΔEARNED≤ΔMDE)에 살면 "같은 작은 δ의 더 촘촘한 추정" → CLOSED-경향.

## Q4 — 공급이 옳은 계기인가 · 에스컬레이션
**필요-불충분, 그리고 정확히 옳은 첫 계기.** 공급 ~0 = 학습 에스컬레이션 사살 충분($0 스크리너 요점). 공급 성장은
전제조건 실재만 증명 · p9 창발은 모델이 CE로 배우는가라 **train만 판정**. 에스컬레이션: **OPENS 발화 시에만** top-rung
코퍼스로 303M CPT 1회(pool·`anima-py evaluate` 판정 · 자연-form gate first·abort 권한 · lab/v6 G0). OPENS 미만이면 학습 없음.

## 첫 명령 (최속 결정적 · ABORT 권한)
**TOP-rung 먼저**(전체 in-band, 사다리 빌드 전). 상한이 이미 평평하면 모든 중간 rung 이 그에 유계 → 1회 판독으로 종료.
```
anima-py evaluate --earned amazon_inband_full.tsv
```
- **EARNED ≤ +0.03 ∧ 3게이트 green → ABORT** 사다리 · 30k 앵커 1개만 더 재서 2점 평평곡선 카드 게시 · 셀 CLOSED(스크리너 강도).
- **EARNED > +0.03 → 전체 nested 사다리** 돌려 상승 위치 찾고 판정표 적용.
- **어느 게이트 red → 인증(G-ALIVE·G-PEDESTAL) 10⁶-행 스케일서 재인증 먼저**(한 번도 안 돈 계기는 다중버그 은폐).

## 통제 · 정직
- 매 rung G-ALIVE(심은 XOR)·G-PEDESTAL(합성 가법 참값0) 그 n서 재인증 — 합성은 계기-인증 전용(합법·off-standard 아님).
- 자의 대비 collapse-Δ 로 읽음, raw 금지(p7). 규모 정직: 10¹² LLM 체제는 **무라벨**·`--earned`은 라벨 필수라 이 계기는
  10¹² 도달 불가 — 사는 건 **기존 라벨-자연 전범위(약 2자릿수 MB→GB)의 기울기**, 주장은 그 기울기지 10¹² 자체 아님.
- 엔진네이티브 거버넌스: 길이밴드·크기 = 코퍼스 행-선택(형태론·분포·길이 선례)이라 scratchpad, 코드 flag 아님. `--earned` 고정.
- 2차 복제(Yelp)는 primary 곡선이 뭔가 보일 때만(replication ≠ external validity).

선행: earned-operator-supply 캠페인(H_9944·9946·9949·9951·9952·9953). 설계 = lab full(Fable 5 채택 · Codex Sol 런너빌리티 검증 수렴). 계기 = `anima-py evaluate --earned` · $0.
