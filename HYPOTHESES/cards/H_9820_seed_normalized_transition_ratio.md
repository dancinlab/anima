# H_9820 — 시드-정규화 전이비로 場 가속을 다시 묻는다 (5-seed · 사전등록)

**status:** 🔒 PRE-REGISTERED (판정표 동결 · 실행 전 커밋) · **DIRECTIONAL-SCREEN 상한** (토이·torch)
**wired:** yes — 신규 코드 0줄. `anima-py train --steps N --tension-field … --tension-concord …`
· 채점 = `--serialize-parity` torch 2AFC 팔
**source:** [[H_9819]] OUT-OF-TABLE — 판정을 못 낸 원인이 **결과가 아니라 지표**였다.

## 왜 다시 묻는가 (H_9819 가 자수한 결함)

[[H_9819]] 의 DV 는 "duel 전이점이 baseline 보다 **몇 칸** 빠른가" 였다. 그런데 baseline
전이점 자체가 seed-가변(seed7 10800 · seed11 14400)이라 **분모가 흔들렸고**, 같은 duel
전이점(두 seed 모두 7200)이 seed7 에선 1칸·seed11 에선 2칸으로 읽혔다. 즉 갈린 것은 場의
효과가 아니라 **기준선의 위치**였다. 2칸 요건은 그 변동성을 과소평가한 내 설계 결함이다.

**교정 = 분모를 seed 안으로 넣는다.** 각 seed 에서

> **전이비** `r_arm = 전이점(arm) / 전이점(baseline)`

를 계산한다. r < 1 이면 그 seed 안에서 더 빠르다는 뜻이고, baseline 이 어디 있든 **그 seed
자신의 기준으로 정규화**되므로 seed 간 비교가 성립한다.

## 개입 — 5 seed × 3 팔 × 조기중단 사다리

**고정 조건**([[H_9819]] 과 동일): K=2 길이-매칭 xor 패널 · `--answer-ce-weight 0` ·
`--trunk-norm global` · d=64 · L=6 · seq 96 · batch 8 · `--n-blocks 4000` · corpus seed 7.

- **사다리(동일 rung)**: steps ∈ {3600, 7200, 10800, 14400, 21600, 28800}
- **팔**: `baseline` · `duel × morph` · `rank1 × morph`(특이성 통제)
- **seed**: {7, 11, 4302, 4303, 13} — 5개(저장소 multiseed 관례 {7,4302,4303} + 11,13)

**전이점 정의(동일)**: d_acc ≥ 0.75 를 처음 만족하는 step. 끝까지 미달이면 `>28800`.

**조기중단(사전 등록 · 사후 절약 아님)**: 한 팔이 전이점을 만족하면 그 팔의 **나머지 rung 은
돌리지 않는다**. 근거는 정의 자체다 — 전이점은 *최초* 도달 step 이므로 그 뒤 rung 은 전이점을
**앞당길 수 없다**. 이 규칙이 5-seed 를 로컬 $0 예산 안에 넣는다.

## 🔒 판정표 (데이터 보기 전 동결 · DV = 전이비 r · 낮을수록 빠름)

**바의 유래(결과가 아니라 rung 간격에서 도출)**: 인접 rung 의 배율은 최소 1.33×
(10800→14400). 따라서 "**최소 한 rung 이상 빠름**" 은 `r ≤ 0.75` 로 표현된다. 이 숫자는
관측치가 아니라 **사다리 구조**에서 나온다.

**선결 무효 조건 2개** (둘 중 하나라도 깨지면 팔을 읽지 않는다):
1. `baseline` 이 **5/5 seed** 에서 사다리 안에 전이점을 가질 것 (아니면 ⛔ LADDER-TOO-SHORT).
2. **재현 검사**: seed 7·11 의 전이점이 [[H_9819]] 와 **일치**할 것
   (base 10800·14400 / duel 7200·7200 / rank1 14400·10800). 불일치면 ⛔ NON-DETERMINISTIC —
   계기가 재현되지 않는다는 뜻이므로 [[H_9819]] 를 포함해 이 계보 전체가 재검토 대상이 된다.

| 조건 (선결 통과 전제) | 판정 |
|---|---|
| `duel` r ≤ 0.75 가 **≥4/5 seed** ∧ 같은 seed 에서 `rank1` r > `duel` r 가 **≥4/5** | 🟢 **場-특이 가속** — 場이 전이를 앞당기고, rank-1 요약으론 안 된다. [[H_9816]] 🔴 뒤집힘 · 303M 이식 정당화 |
| `duel` r ≤ 0.75 가 ≥4/5 ∧ `rank1` 도 ≤0.75 가 ≥4/5 | 🟡 **비특이 가속** — 상승 실재하나 場-특이 아님(기존 스칼라 이음매로 충분) |
| `duel` r ≤ 0.75 가 **≤2/5 seed** | 🔴 **NEGATIVE** — 場은 전이를 앞당기지 않는다. [[H_9816]] 🔴 가 올바른 예산에서 재확인됨 |
| `duel` r ≤ 0.75 가 3/5 | 🟡 **부분** — 별도 사전등록 없이 연장 금지 |

**⚠️ 정직 고지 (이 H 의 정보량이 어디 있는지)**: seed 7·11 은 [[H_9819]] 에서 **이미
측정됐고 그 전이비는 0.667 · 0.500 으로 둘 다 바(≤0.75)를 통과한다.** 따라서 이 H 의 시험대는
**새 seed 3개(4302·4303·13)** 이며, ≥4/5 요건은 **새 seed 중 최대 1개만 실패해도 통과**를
뜻한다. 바를 rung 간격에서 도출한 것도 이 때문이다 — 관측치에 맞춘 바였다면 이 H 는
`tune-to-green` 의 위장일 뿐이다. 새 seed 3개 중 2개 이상이 바를 못 넘으면 🔴 로 떨어진다.

**추가 스윕 금지**: 이 표 밖 하이퍼 불변. 결과가 무엇이든 **토이 스크린이며 verdict 가 아니다**.

## 재생성 커맨드 (seed 포함 · 재감사용)

```
anima-py corpus bindpanel --lang en --out bp.txt --bind-k 2 --n-blocks 4000 --seed 7 --bind-task xor
   # md5(bp.txt) = 786b798f58708c588bfd1294708c7c2e  (3-호스트 동일 확인됨)
anima-py train --arch clm --corpus bp.txt --d 64 --L 6 --seq-len 96 --batch-size 8 \
  --answer-ce-weight 0 --trunk-norm global --steps <N> --seed <S> \
  [--tension-field {duel,rank1} --tension-concord morph] \
  --serialize-parity bp.txt.seen_panel.json --out <cell>.clm
```

## Cross-links

[[H_9819]] 지표 결함의 출처(이 H 의 동기) · [[H_9817]] 상전이 실측 · [[H_9816]] 재심 대상
