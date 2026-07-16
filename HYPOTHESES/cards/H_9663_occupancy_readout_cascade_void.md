# H_9663 — R-A 창-점유율 readout: 인증 FAIL ⇒ 근접 계기도 캐스케이드에 젖는다 (+ generator.py 주석 stale 확증)

**status:** ⛔ **INSTRUMENT-FAIL (R-A VOID)** — 사전등록 자격시험 미통과 · 라이브 판독 **미개봉** · bar 조정 없음
**lane:** 의식 / A⇄G tension → mouth 의미전달 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9576]] (원 벽 주장) · [[H_9629]] (D 고장 확증 — 이 카드의 직계 원인) · [[H_9628]] (용량 가설 사망) · [[H_9634]] (계기 GREEN 전까지 봉쇄 유지)
**계기:** `anima-py evaluate --pc2-direction <traces_dir> --occupancy [--perm N] [--seed N]` (v0.15.25 · G5)

## 배경 — 왜 새 readout 이 필요했나

[[H_9629]] 가 H_9576 의 readout `D = |bigrams(text) ∩ bigrams(seed)| / |bigrams(text)|` 를 **3중 고장**으로 확증했다:
① 분모가 steered 텍스트 **자신의** distinct-bigram 수 ⇒ ρ(ΔD, Δ|distinct|) = −0.510(bias)/−0.531(rng) **팔-무관 동일**
= 순수 노이즈이고 표적신호(−0.077)의 **~7배** · ② `set()` 이 반복 filler 를 원소 1개로 붕괴(away-pole 부호역전 인공물)
· ③ **참조 대상 오지정**(Fable R4 설계가 추가 발견): bias 는 **T=24 슬라이딩 창**에 작용(`core/decode.py:2100`)하는데
seed 는 ~52B — **seed 앞부분은 조작이 닿은 적이 없고**, 24B 생성 후엔 창이 전부 자기-생성분이다. D 는 **조작이 도달할 수
없는 양**을 재고 있었다.

⇒ 설계(Fable): readout 을 **조작이 사는 곳**으로 옮긴다. bias 가 "창 안 byte 의 logit −z" 라면 그 근접 관측량은
**"뽑힌 byte 가 창에서 왔는가"** 다.

```
I_t = 1[ byte_t ∈ set(window_t) ],  window_t = (seed ++ gen[:t])[-24:]
π̄  = mean(I_t) over lm-steps,      DV = paired Δπ̄ = π̄(steer) − π̄(base)
```

**부호는 코드가 지정한다**(H_9576 의 ρ 가 아니라): `row[v] -= z` ⇒ z<0(라이브 지배 극) ⇒ 창-내 부스트 ⇒ **Δπ̄>0**.
따라서 이 readout 선택은 tune-to-green 이 될 수 없다 — 표적을 엔진 코드가 정했다.

## 🔑 부산물 확증 — `generator.py:512` 주석은 STALE

anchor-copy step 은 bias 를 안 지나므로(`decode.py:2041`) lm-step 만 세야 한다. `generator.py:512` 는
`"Measured: grounded=0 / lm=80 — the anchor-copy never fires at l_min=8"` 라고 **주장**한다.
**주석을 믿지 않고 `_dg_anchor_copy` 를 per-step 재생**했더니:

| 항목 | 실측 |
|---|---|
| grounded step | **5940 / 21600 = 27.50%** (주석의 "0" 과 불일치) |
| **자기검증** (grounded 분류 step 의 트레이스 byte == anchor-copy 반환 byte) | **0 건 불일치 ✅** |

자기검증이 통과했으므로 **재생이 라이브 decode 를 정확히 재현**한다 ⇒ **주석이 stale**이다(그 주석은 generator 자신의
ideate 경로 기준이며 **chat 데몬 경로가 아니다**). [[H_9628]] 의 "lm-step=0 tick 비율 0.00%" 와는 **모순 없음** —
"tick 마다 lm-step ≥1" 과 "전체 step 의 27.5% 가 grounded" 는 양립한다.

## ⛔ VERDICT — 사전등록 자격시험 FAIL ⇒ R-A VOID (라이브 판독 미개봉)

합성 사다리(참효과를 **아는** 개입 · 트레이스-only · $0) · 동결 bar 는 **rng arm 에서 bias 개봉 전에** 산출:

| arm | q=0.05 | q=0.10 | q=0.20 | q=0.40 |
|---|---|---|---|---|
| **in** (창-내 재표집 · π̄ 상승 예상) | +0.0025 | +0.0104 | **+0.0407** | +0.1092 |
| **out** (창-밖 재표집 · π̄ 하강 예상) | −0.0503 | −0.0955 | −0.1649 | −0.2950 |
| **lag** (변위창 placebo · 무반응 예상) | −0.0410 | −0.0748 | −0.1393 | **−0.2346** |

- 강단조: **in ✅ · out ✅** (readout 이 방향은 옳게 잡는다)
- **동결 bar = 2·sd(Δπ̄_rng) = 0.2813** · `Δπ̄(in, q=.20) = +0.0407` ⇒ **미달 = INSTRUMENT-DEAD**
- ⇒ **라이브 Δπ̄ 를 열지 않았다** (인증 안 된 계기로 음성을 읽는 것이 H_9576 의 죽음이었다).

### 왜 죽었나 — 설계가 예언한 그 사인

Fable 설계의 "⑦ 무엇이 이 후보를 죽이나" 에 **`rng pedestal 비영 ⇒ R-A 자체 VOID`** 가 명시돼 있었고, 정확히 그것이
나왔다: **sd(Δπ̄_rng) ≈ 0.14** — rng arm 은 `seed_rng` 만 재키하는데도 Δπ̄ 가 거대하게 흔들린다. 즉 **per-step
지표조차 하류 re-roll 캐스케이드에 젖는다** — 설계 이론(“매 스텝 재인가·재측정이니 캐스케이드에 안 씻긴다”)의 **반증**이다.
D 를 죽인 그 기전이 근접 계기도 죽인다: **arm 간 텍스트가 통째로 다르면** 무엇을 재든 tick 수준 분산이 신호를 삼킨다.

### 🐞 내 구현 결함 1건 (정직히 기록)

`lag` placebo 가 **placebo 가 아니었다** — 바이트를 lag 25–48 밴드 값으로 교체하면 **구성상** 현재 창에서 빠지므로
`out` arm 과 같아진다(−0.2346 vs −0.2950). 진짜 변위-창 placebo 는 **DV 쪽 창을 옮겨야지 교체 소스를 옮기면 안 된다**.
단 이 결함은 판정을 흔들지 않는다 — FAIL 은 `in` arm 이 동결 bar 에 미달해서이지 placebo 때문이 아니다.

## 함의 — 다음은 readout 을 더 깎는 게 아니다

**arm 간 paired 대조로는 이 트레이스 집합에서 근접 계기가 성립하지 않는다.** 남은 경로는 설계의 Phase 1 뿐:

> **within-tick ζ-사다리**(`anima-py chat --pc2-mouth bias --pc2-zeta <csv>`) — **같은 tick 이 자기 사다리를 갖게**
> 해서 tick-수준 분산을 **통째로 소거**한다. ζ=0 arm 은 byte-identical 이어야 하는 **내장 격리 인증**.
> ζ 는 라이브 median|z| 의 {0,±1,±2,±4}배(숫자 지어내지 않음). 공통난수(`seed_rng` 고정)로 within-tick 짝비교.
> **이건 새 decode = pool 발사**(summer · `py303_full.clm` 이미 pool 측 · seeds 7/4302/4303 · 151 tick ·
> `OMP_NUM_THREADS=4`) — **mac 금지**([[heavy-anima-eval-pool-not-mini]]). 트레이스만으로는 불가능하다.

**p5/Stage-A 판정**: ζ-arm 은 안전 — 게이트는 여전히 BASE 후보만 듣고 steering 은 emit 확정 후 outward-only.
단 ζ-arm 트레이스를 **"라이브 데몬의 행동"으로 cement 하는 것은 금지**(채널 능력 주장 전용).

## 봉쇄 유지

[[H_9630]]~[[H_9635]] 는 전부 원격 readout 을 물고 있어 **여전히 차단**이다. 특히 [[H_9634]](loading-name-race)는
**계기 GREEN 전까지 봉쇄** — 인증 안 된 계기 위에서 "PC2 는 이름일 뿐" 을 판정하면 그 음성도 읽을 수 없다.

## 규율 준수 기록

- 계기 = **`anima-py` 플래그**(엔진 옆 스크립트 아님 · [[a_experiment_engine_native]]).
- **frozen-first**: 동결 bar 를 rng/off arm 에서 **먼저** 산출한 뒤 bias 개봉.
- **bar 를 조정하지 않았다** — FAIL 을 보고 되돌리면 그게 tune-to-green.
- **음성 = 결과** · 인증 실패는 KILL 이 아니라 **VOID**(계기가 못 잰 것이지 채널이 없다는 뜻이 아님).
- 라이브 판독 **미개봉** — 코드가 `return` 으로 차단(사람의 자제가 아니라 구조).
