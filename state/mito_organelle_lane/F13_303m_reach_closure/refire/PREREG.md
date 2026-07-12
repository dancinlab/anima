# H_9285 REFIRE — 사전등록 (데이터 보기 전 동결)

**동결 시각: 2026-07-12 · run_refire.py sha256 = `7b1d3760d46125f4f38ccd5291d272c1909c40b0be2889d9a43bfecd34ca9c7d`**
이 파일은 **측정 실행 전에** 작성됐다. 아래 헤드라인·V-gate·판정분기는 결과를 보기 전에 코드로 못박혔다.

## 왜 재발사인가

원 F13 run의 헤드라인 = `m_conj = min(m_A_conj, m_B_conj)` = **순서통계량**(규칙①⑤ 위반).
→ run이 INVALID를 냈고, 검증자가 **사후에** live branch `m_B_conj`로 재계산해 KILL을 얻었다.
그 KILL은 **directional일 뿐 licensed 아니다** — 사후 detector 교체는 F8을 INVALID로 찍은 바로 그 죄다.

이번 재발사는 헤드라인을 **데이터 보기 전에** `m_B_conj`로 못박고, **새 disjoint seed**로 재측정한다.

## 1. 사전등록 헤드라인 detector (순서통계량 아님)

**HEADLINE = `m_B_conj`** — held-out 2-cue 문맥에서 근접(proximal) cue의 결합 소비 마진:

```
lift(x|c) = logP(x|c) − logP(x|null)          # null = 두 cue 모두 byte-scramble
m_B_conj  = lift(b|AB) − lift(f|AB)           # b = B의 content, f = foil
```

- 단일 변수. `min()`/`max()` 등 **순서통계량 아님**.
- 검출력 사전확인(원 run 데이터 기준): c0 = **+1.083**, t = **+4.69**, MDE 0.190 ≪ 1.083.
- 이 detector가 헤드라인이자 **V-gate가 걸리는 바로 그 축**(규칙⑤).

## 2. 새 데이터 — 이전 verdict seed와 disjoint

| 축 | 이전 run | 재발사 |
|---|---|---|
| items | 120 (특정 (A,B) 쌍 120개) | **fresh-cue 130개** — (A,B) 재조합쌍 overlap **0**, 5-tuple overlap **0**, cue 단어가 이전 142 cue와 **완전 disjoint** |
| scramble seed | 20260712 | **20260713** |
| arm-shuffle seed | 1000+idx | **2000+idx** |
| θ probe | seed 7 · gen_en[0:400k] | **seed 13 · gen_en[400k:1.2M]** (disjoint 영역) |

**PROBE_ONLY 사전확인(측정 전 실행)**: mine_mode=`fresh-cue` · 134 items 확보 · overlap_tuple=0 · overlap_ab=0 · disjoint_ok=True · θ=0.4643.

## 3. arm

| arm | 내용 |
|---|---|
| **EXP** | 절대-setpoint capacity schedule — `k_t = min{k : Σ_{i≤k} sorted_p[t,i] ≥ θ}`, θ = 코퍼스 probe에서 고정된 절대상수 |
| **c0** | 프로덕션 고정 (= DENSE soft mixture, top-k 없음 ⇒ k=E) |
| **c1** | best 상수 k — grid k∈{1,2,3} 전수, **disjoint pilot에서 선택**(verdict set 미열람) |
| **c2** | shuffled-schedule — EXP와 동일 k 분포를 시간축 셔플(정렬만 파괴) |
| **SHOCK** | router 파괴(균등 mixing) — V-gate 채널가시성 probe |

## 4. V-gate — **헤드라인 detector 그 자체(m_B_conj)에** 건다 (규칙⑤)

- **V1 liveness**: c0에서 mean(m_B_conj) > 0, paired-t vs 0, **t > +2.093** (α=.05, n=20).
- **V2 channel-visibility**: SHOCK(router 파괴) vs c0 **on m_B_conj**, **|t| > 2.093**
  — 처치 채널(MoE mixing)이 **이 detector에 보이는가**.
- 둘 중 하나라도 FAIL → **verdict = INVALID** (cement 금지).

## 5. MDE (규칙③) — 분석과 disjoint한 pilot

- MDE는 **verdict set(100 items / 20 blocks)과 disjoint한 pilot item set(30 items / 6 blocks)**에서만 추정.
  (원 run은 pilot이 analysis blocks의 **부분집합**이었다 — 이번에 분리.)
- 축 = 헤드라인 m_B_conj = 처치가 인과적으로 도달하는 축.
- power 조건: `MDE < |pilot c0 level|`. 불충족 → INVALID.

## 6. 정보채널 증명 (규칙④)

- 결정변수 `k_t = f(위치 t의 router cumulative mass)` = **입력 토큰의 함수** — 상수 arm(c1)은 볼 수 없음.
- 운영 대역에서 `Var(k_t) > 0` 실측 보고 (항진적 처치 arm 방지).

## 7. 부호반전 축 전수 (규칙⑥ · 설계에 내장)

부호를 뒤집을 수 있는 축 3개를 사전 열거하고, **PASS 조건에 세 축 모두의 부호보존을 포함**한다:
1. **setpoint level** — EXP vs c0
2. **constant-k level** — EXP vs c1_best (grid 전수)
3. **schedule ordering** — EXP vs c2_shuf (동일 k 분포, 정렬만 파괴)

## 8. 사전등록 판정분기 (규칙⑦ · 실행 가능한 코드)

```python
T_CRIT = 2.093                                  # t_.975,19
beats  = lambda r: r["t"] > T_CRIT              # EXP가 control 위로 유의
PASS   = beats(EXP_vs_c0) and beats(EXP_vs_c1_best) and beats(EXP_vs_c2_shuf)
all_deg_or_ns = all(r["t"] <= T_CRIT for r in (EXP_vs_c0, EXP_vs_c1_best, EXP_vs_c2_shuf))

if   not V1_pass:  verdict = "INVALID"      # 헤드라인 죽음
elif not V2_pass:  verdict = "INVALID"      # 헤드라인이 처치채널에 눈멂
elif not mde_ok:   verdict = "INVALID"      # 검출력 부족
elif PASS:         verdict = "PASS_LEVER"   # organelle lane = reach 레버 (놀라운 결과)
elif all_deg_or_ns:verdict = "FAIL_CLOSED"  # 모든 capacity 처치가 열화/ns → lane CLOSED cement (KILL)
else:              verdict = "MIXED"
```

- **PASS_LEVER** = EXP가 c0·c1·c2 **각각** 유의 우세 ⇒ organelle lane이 reach 레버 (⇒ 303M spend 재검토).
- **FAIL_CLOSED** = 모든 capacity 처치가 헤드라인을 열화시키거나 ns ⇒ **organelle lane CLOSED cement**
  (카드 사전등록 FAIL 시나리오 · H_9283 예측).

## 9. 금지

- 사후 detector/변수 교체 **금지** (이것이 원 INVALID·F8 INVALID의 진범).
- 순서통계량 헤드라인 **금지**. `Δ = exp − max(controls)` **금지** — control별 paired-t 전부 보고.
- `mean vs 1·std` 휴리스틱 금지 — SEM/paired-t만.
- 금지지표 `conj_index`·`purity`·`acc/ATP` 비율 미사용.
- **tune-to-green / tune-to-red 둘 다 금지**. verdict는 위 코드가 반환하는 값 그대로.

## 10. engine-native

- ckpt = aiden `~/py303_full.clm` (d3784 · E3 · K3 · L4 · V256 · T24).
- trunk forward = 설치된 `anima_py` **프로덕션** `core/decode.py` 경로 재사용.
- **PARITY GATE**: dense 재구성이 `clm._fwd_logits`와 **max|Δ| = 0.0** (byte-exact) 여야 진행. 아니면 abort.
- 구조적 사실: 프로덕션 router = **DENSE soft mixture** (top-k 자체가 없음) ⇒ c0 = dense = k=E,
  모든 capacity gating은 정보를 **버리는** 연산이다.
