# H_9285 CEMENT — 사전등록 (데이터 보기 전 동결)

**동결: 2026-07-12 · `run_cement.py` sha256 = `03a91579a126dde921bbe8e59305899913da4bac308aa9cf48f5d562ab6d4125`**
**`prev_exclude_all.json` sha256 = `6336d45add957485cd3ff10fc6371fb6e4e346da76e77df99d7a4f911d250bdc`** (run-1 ∪ run-2 = 250 tuple · 250 (A,B) · 309 cue word)

이 파일과 위 코드의 헤드라인·마진·V-gate·n·판정분기는 **arm이 한 번도 채점되기 전에** 고정됐다.
(예외적으로 **item pool 크기만** `PROBE_ONLY=1`(채점 없음 · 마이닝+θ만)으로 먼저 확인해 `TARGET_MAIN`을 정했다 —
pool 크기는 결과변수가 아니다. 확인값: fresh-cue 384 items @ `uni≥20·cnt≥4·pmi>0` tier · overlap 0/0/0 · θ=0.4640.)

## 0. 왜 3번째 발사인가 (앞 2회의 실패가 SSOT)

| run | 헤드라인 | 결과 |
|---|---|---|
| run-1 | `min(m_A_conj, m_B_conj)` = **순서통계량**(규칙①⑤ 위반) | INVALID → 검증자가 **사후에** live branch로 재계산해 KILL → lane CLOSED 선언 |
| run-2 | `m_B_conj` 사전등록 + disjoint 새 cue | **KILL 근거 소멸**: EXP−c0 −0.209(p=.033) → **+0.129 ns 부호반전** · V2(signed) SHOCK−c0 +0.100(p=.023) → **−0.086 ns FAIL** ⇒ INVALID · **CLOSED 철회** · seed 이질성 z=2.22 p=.026 = 통계적 불일치 |

**진단**: 이 축은 **부호-무작위 잡음 지배**다. 개입은 항목당 |Δ|=0.37~0.94로 detector에 크게 도달하는데
**signed mean ≈ 0으로 상쇄**된다. ⇒ signed V-gate는 구조적으로 통과 불가 · "ns"는 CLOSED를 licensing 못 함.

## 1. cement 3조건 (카드 등록 · 이번에 집행)

### (a) V-gate = **unsigned / 변위 기반** (헤드라인 detector 그 자체에 · 규칙⑤)
- **V0 (규칙⑧ 자원보존)**: 모든 arm의 mixture weight가 `|Σ_e P[t,e] − 1| ≤ 1e-13` — capacity 연산자가 무에서 자원을 창조하지 않음. 위반 → abort.
- **V0b SHAM-IDENT**: `k=E` arm(수학적 no-op) → `max_i |m_B_conj(SHAM) − m_B_conj(c0)| ≤ 1e-9`.
  ⇒ unsigned 통계량의 **수치 잡음 바닥이 0**임을 증명(잡음으로는 unsigned gate를 통과할 수 없음).
- **V1 liveness**: `mean_i m_B_conj(c0) > 0`, 단측 t > t_crit.
- **V2a 채널가시성(SHOCK · UNSIGNED)**: `mean_i |m_B_conj(SHOCK)_i − m_B_conj(c0)_i|`의 **95% 하한 > Δ_eq**.
- **V2b 채널가시성(EXP · UNSIGNED)**: **처치 arm 자체**에 같은 통계량, 95% 하한 > Δ_eq.
- ⇒ detector가 처치 채널에 **눈멀지 않았음을, 우리가 배제하려는 등가마진의 해상도에서** 증명한다:
  채널이 항목당 헤드라인을 Δ_eq **이상** 흔든다 ⇒ 그 위에서 signed mean이 ±Δ_eq 안이면 그것은
  "채널 없음"이 아니라 **"방향성 효과 없음"**이다. 하나라도 FAIL → **INVALID**.

### (b) n = **실측 sd 기준 사전산정** (규칙③)
- `sd_used = max(PRIOR_SD_ITEM = 1.2192, pilot sd의 상측 80% 한계)`.
  PRIOR = run-2 verdict set의 **실측** item-level sd(= block sd 0.545 × √5). run-2의 6-block pilot이 sd를 2.1배
  **과소추정**했으므로 이번엔 낙관적 pilot을 신뢰하지 않고 **보수적 max**를 쓴다.
- `N_REQ = ⌈(z₉₅+z₈₀)² · sd_used² / Δ_eq²⌉` (참값 0에서 TOST power ≈80%). sd=1.219 → **N_REQ = 230**.
- **n_main = 334** (fresh-cue pool 384 − pilot 50). `n_main < N_REQ` → **verdict = INVALID (underpowered)** — 코드에 내장, 채점 자체를 안 한다.
- pilot(50 items)은 **verdict set과 disjoint**하며 sd/MDE + c1_best 선택에만 쓴다(verdict set 미열람).

### (c) **TOST 등가성 검정** — "ns"가 아니라 실질적 0과의 등가를 증명해야 CLOSED
- **Δ_eq = 0.20 nats** (데이터 보기 전 고정). 근거(전부 사전):
  1. **분쟁 중인 효과의 크기 그 자체** — KILL을 licensing했던 −0.209와 run-2의 +0.129가 모두 0.20 이하.
     |effect| ≥ 0.20을 **양방향으로** 배제하는 TOST = 분쟁의 정확한 심판.
  2. **reach에서 의미 있는 최소 효과** — live detector 레벨(c0의 m_B_conj = +0.638(run-2) / +1.083(run-1))의 **~31%**.
     추가 spend를 정당화할 배분 레버라면 최소한 "이미 소비되는 cue의 마진"의 1/3은 움직여야 한다.
- 민감도(**보고만** · 판정에 미사용): Δ_eq ∈ {0.15, 0.25}.
- **등가 판정** = 각 대조의 signed paired delta의 **90% CI가 (−Δ_eq, +Δ_eq) 안에 완전히 포함**(TOST α=.05 양측 one-sided 2회).

## 2. 헤드라인 · 대조 · 부호반전 축(규칙⑥)

- **HEADLINE = `m_B_conj`** (단일 변수 · 순서통계량 아님 · run-2와 **동일 detector** ⇒ 두 disjoint seed가 비교가능).
  `lift(x|c) = logP(x|c) − logP(x|null)` (null = 두 cue byte-scramble) · `m_B_conj = lift(b|AB) − lift(f|AB)`.
- **1차 대조 = EXP − c0** (signed · paired · CRN · **분석단위 = item**, n=334; block(5 items) 수준도 부수 보고).
- 부호반전 축 3개 사전열거: **setpoint level**(EXP vs c0) · **constant-k level**(EXP vs c1_best · grid는 disjoint pilot에서 선택) · **schedule ordering**(EXP vs c2_shuf).
- 규칙① 준수: `Δ = exp − max(controls)` **미사용** · control별 paired-t 전부 + pooled-mean 보고. 규칙②: SEM/paired-t만.

| arm | 내용 |
|---|---|
| **EXP** | 절대-setpoint capacity schedule · `k_t = min{k : Σ_{i≤k} sorted_p[t,i] ≥ θ}` (θ = 코퍼스 probe 절대상수) |
| **c0** | 프로덕션 (DENSE soft mixture · top-k 없음 ⇒ k=E) |
| **c1** | best 상수 k (grid k∈{1,2,3}, **disjoint pilot**에서 선택) |
| **c2_shuf** | EXP와 동일 k 분포를 시간축 셔플(정렬만 파괴) |
| **SHOCK** | router 파괴(균등 mixing) — unsigned 채널가시성 probe |
| **SHAM_ident** | k=E no-op — unsigned 통계량의 0-바닥 증명 |

## 3. 데이터 — 이전 **2회 모두**와 disjoint

- (A,B) 재조합쌍 overlap **0** · 5-tuple overlap **0** · **cue 단어 overlap 0** (union 250 tuple / 309 cue 대비 · fresh-cue 모드).
- 새 seed: scramble **20260714**(prev 20260712/20260713) · arm-shuffle base **3000**(prev 1000/2000) ·
  θ probe seed **21** + **이전 두 run이 건드리지 않은 코퍼스 영역**(sns_en[0:700k]; prev = gen_en 두 구간).
- 사전 선언된 fallback ladder: fresh-cue가 고갈되면 pair-only(모든 (A,B)·5-tuple은 여전히 신규, cue 단어만 재사용).
  **PROBE 결과 fallback 불필요**(fresh-cue 384 확보).

## 4. 사전등록 판정분기 (규칙⑦ · 실행 가능한 코드)

```python
if   any V-gate fails:      verdict = "INVALID"             # V0·V0b·V1·V2a·V2b
elif n_main < N_REQ:        verdict = "INVALID"             # underpowered (abort · 채점 안 함)
elif PASS(all 3 controls):  verdict = "PASS_LEVER"          # EXP가 c0·c1·c2 각각 유의 우세 → lane = reach 레버
elif TOST equivalent on 3:  verdict = "EQUIVALENT_CLOSED"   # 90% CI ⊂ ±Δ_eq (3축 전부) → lane CLOSED (licensed)
else:                       verdict = "INCONCLUSIVE"        # 둘 다 아님 → cement 금지
```

## 5. engine-native / 금지

- ckpt = aiden `~/py303_full.clm` (d3784·E3·K3·L4·V256·T24) · trunk forward = 설치된 `anima_py` **프로덕션** `core/decode.py`.
- **PARITY GATE**: `max|Δ| = 0.0` vs `clm._fwd_logits` (byte-exact) 아니면 abort.
- 사후 detector/판정변수 교체 **금지**(규칙⑨). 순서통계량 헤드라인 금지. **tune-to-green / tune-to-red 둘 다 금지** —
  verdict는 위 코드가 반환하는 값 그대로.
