# RESULT — H_9273 / F1 · ATP 대사경제 **REFIRE** (원 판정 ⛔INVALID 재발사)

**판정: 🎭 THEATER (licensed negative)** — 원 INVALID 와 달리, 이번 음성은 **설계가 아니라 데이터에서** 나왔다.

> 한 줄: **예산은 진짜로 묶이고(binding 52.8%) 수요→용량 배분 채널은 실재(+2.42pp vs 동일지출 수요맹목, t=+11.4, 20/20)하지만, F1 고유 내용인 「보존 ATP 장 + 저장(reservoir)」의 기여는 정확히 0 (vs c5 Δ=−0.0007±0.0014, ns, 9/20 동전) 이고 bursty 수요에선 −2.88pp 로 오히려 해롭다. 게다가 경제 전체가 「ATP 를 9% 더 쓰기」(c1)에 −1.90pp 로 진다 ⇒ ATP 회계장부 = bookkeeping THEATER.**

- 실행: `$0` numpy · mini CPU-local · OMP=2 · wall ≈ 168s · seed 20 (paired-CRN) · torch 0
- 산출: `run.py` · `result.json` · 본 파일 (원본 `../run.py` `../RESULT.md` `../REFUTE.md` 무수정)

---

## 0. 원 INVALID 결함 → 이번에 무엇을 고쳤나 (REFUTE.md §재실행 조건 i~vi 전부)

| # | 원 결함 (REFUTE.md) | 이번 수정 | 실측 증거 |
|---|---|---|---|
| **R1** 검출력 0 — 처치 대역 동적범위 1.12pp < 유의문턱 1.71pp ⇒ 가설이 참이어도 sig=True 수학적 불가 | **(iv)** pilot seed(100–105 · main과 disjoint)에서 **실행 전** MDE 계산. 못 넘으면 그 자리에서 abort 하도록 코드에 박음 | **band(k∈1..4) = 18.12pp · MDE(n=20) = 0.351pp ⇒ MDE/band = 0.019** (검출력 여유 **52배**). 원 프로브 대비 축이 16배 넓고 문턱이 5배 낮다 |
| **R2** 항진적 처치 — `policy_atp`가 batch/loss/model 을 인자로도 클로저로도 안 받는 자율 폐루프(주기-3 클럭). 수요를 `afford`로 정의해 **수요>생산이 구조적 불가** | **(i)** demand 를 supply 에서 외생화: `demand_i = #{e : S_e > 0.5·max S}` (S = 라우터 원점수) = **입력 × 모델상태**의 함수. `k = min(demand, afford)` ⇒ 수요>공급이 구조적으로 **가능** | binding_rate = **0.528** (수요>공급이 실제 발생 · 원 설계에선 정의상 0). demand corr(m) = **+0.938**, std = 1.08 (운영대역 분산>0). demand 셔플 시 EXP 의 k 가 **43.6%** 바뀜 / c1·c2 는 **0%** = 정보채널 존재 증명 |
| **R3** 용량 레인 inert — route_acc 전 arm 우연 이하(1/16), k = 평균화(smoothing) 노브 = FORM | **(ii)(iii)** 기질 교체: expert = **(topic × polarity) 결합**, 라벨 = 활성 결합들의 vote 합, vote 는 극성무관 ⇒ **선형 지름길 = 최빈클래스 baseline**. 게이트는 재정규화 없는 **합** ⇒ k<m 이면 표가 실제로 빠진다 | **route_recall = 0.998 vs chance 0.156 = 6.39×**. **선형 지름길 0.5173 vs 최빈클래스 0.5174 ⇒ Δ = −0.01pp (ns)** = 선형사상이 최빈클래스 위에 **정확히 0** 추가 (MoE 는 0.820) ⇒ 기질이 진짜 비가산. acc(k=1)=0.648 → acc(k=4)=0.829 |
| **R4** c1 ≡ c2 per-seed byte-identical (통제 2개가 아니라 1개) | **(v)** primary 2 통제를 **구조적으로 다르게**: `c1` = STATIC 정수캡(분산 0 · 수요맹목 · ATP 를 **더** 씀 = 보수적) / `c2` = PERMUTED-k(EXP 의 k multiset·총지출 **정확히** 일치 · 수요-표본 결합만 파괴). + `c4`(수요 스크램블) `c5`(저장만 제거) `c3`(no-bank raw) | 지출 실측: EXP **3.669** / c1 **4.000**(더 씀) / c2 **3.669**(정확 일치) / c5 **3.668**. c1 과 c2 는 acc 가 0.759 vs 0.716 로 **서로 4.3pp 다르다** (byte-identical 불가) |
| **R5** p5 constructive test 가 dead-code 항진명제(`_zero`/`_rand` 계산만 하고 미주입) | **(vi)** `emit_decide(logits, thr, atp_ctx)` — atp 를 **실제 인자로 주입**하고 real/zeros/random 3 문맥 결정 해시 비교 + 본문 심볼검사 | 20/20 seed **illegal_channel_closed = True** (3 문맥 해시 byte-identical + 본문에 `atp` 심볼 부재). 동시에 **합법경로는 살아있음**: emit_rate 가 static k=1 → 0.423, EXP → 0.462, k=8 → 0.500 으로 **용량에 따라 변한다** (ATP→용량→표현→tension→emit) |
| **+R6 (내가 추가로 발견)** 원 카드의 control 은 c1(무한 ATP)·c2(never-binds) **둘 다 EXP 보다 자원이 많다**. acc 가 k 에 단조증가인 이상 "제약 arm 이 무제약 arm 을 이겨라"는 PASS 조건은 **구조적 달성불가** | 질문을 과학적으로 의미있게 교정: **"동일 비용에서, ATP 경제가 수요맹목 지출보다 잘 배분하는가?"** 원 카드의 문자 그대로의 대비도 `ref_unbudgeted_demand`·`ref_static_kmax` 로 **함께 보고**(숨기지 않음) | ref_unbudgeted 0.833 · ref_static_kmax 0.820 · EXP 0.740 — 예상대로 자원 우위 arm 이 이긴다. 원 PASS 조건은 실제로 달성불가였음이 확인됨 |

### 정직 고지 (tune-to-green 방어)
- 기질 상수(NOISE·TAU·STEPS·LR)는 **arm-무관 속성**(route_recall · static-k acc 곡선 · demand 센서 품질)만 보고 고정했다.
- 다만 기질 구축 중 **seed 0 에서 EXP-vs-control 대비를 한 번 보았다**(EXP < static-ceil, EXP > perm). 그 관찰 **이후 어떤 상수도 바꾸지 않았고**, 추가한 것은 통제(`c4`·`c5`·bursty 조건)뿐이다 = **통제 강화 방향**(음성을 강화). REFUTE.md 자신의 판례("c3/V-gate 사후추가는 통제 강화라 합법")를 따른다.
- **V2 게이트 null 수정 이력**: 첫 실행에서 V2 가 FAIL(선형 지름길 0.3023 > 1/C+0.05)로 떴다. 원인은 **내 게이트 자신의 detector-fairness 결함** — (a) 클래스 사전확률이 비균일한데 null 을 `1/C = 0.25` 로 잡았고 (b) 선형 회귀에 **절편을 안 넣었다**. 올바른 null(최빈클래스 baseline = 0.5174) + 절편 포함으로 재측정하니 선형 지름길 = **0.5173 = 최빈클래스와 정확히 동일(Δ=−0.01pp, ns)**. 즉 게이트 의도(기질 비가산성)는 **완벽한 여유로 충족**이었고 오탐이었다. **문턱을 옮긴 게 아니라 잘못 지정된 null 을 고쳤다** — 그리고 이 수정의 방향은 verdict 를 INVALID(회피) 에서 **THEATER(음성 확정)** 으로 **더 단정적인 음성**으로 만든다 = tune-to-green 의 정반대.

---

## 1. 사전 검출력 (R1 fix · 실행 전 산출)

```
static-k acc 곡선 (pilot seeds 100–105):
  k=1 0.6479 · k=2 0.7676 · k=3 0.8127 · k=4 0.8291 · k=5 0.8254 · k=6 0.8233 · k=7 0.8232 · k=8 0.8230
처치가 사는 대역(k∈1..4) 동적범위 = 18.12 pp
MDE (n=20 · paired-CRN · α=.05 · t*=2.093) = 0.351 pp
⇒ MDE / band = 0.019   (사전등록 통과선 < 0.20)          POWER_OK = True
```
원 프로브: band **1.12pp** < 문턱 **1.71pp** (비율 1.53 ⇒ 검출력 0). 이번: 비율 **0.019** = **80배 개선**.
최빈클래스 baseline = 0.517 이므로 acc 0.648(k=1) → 0.829(k=4) 는 전부 baseline 위의 실질 신호다.

## 2. V-GATES (전부 **헤드라인 detector 자체**에 건다 — 규약 5)

| gate | 내용 | 값 | PASS |
|---|---|---|---|
| **V1** 용량레인 liveness | 헤드라인 detector 상 static k=8 − k=1 | Δ = **+0.179** SEM 0.0089 **t=+20.16** 20/20 | ✅ |
| **V2** expert 특화 + 기질 비가산성 | route_recall vs 1/E · 선형지름길 vs 최빈클래스 | **0.998 / 0.156 = 6.39×** · 선형 0.5173 − 최빈 0.5174 = **−0.0001 (ns)** | ✅ |
| **V3** 정보채널 (규약 4) | (a) 처치 결정변수가 control 이 못 보는 입력의 함수 (b) 운영대역 분산>0 | demand std **1.079** · corr(demand,m) **+0.938** · k_std(EXP) **0.608** · demand 셔플 시 k 변경 **EXP 43.6% / c1 0% / c2 0%** | ✅ |
| **V4** 예산 공정성 | primary control 이 EXP 보다 ATP 를 적게 쓰지 않는다 | EXP **3.669** · c1 **4.000**(+9%) · c2 **3.669**(정확 일치) · c5 **3.668** | ✅ |
| **V5** 예산이 실제로 묶인다 | 수요 > 공급 발생률 | **binding = 0.528** (mean_demand 2.53 > sustainable_k 1.6) | ✅ |
| **p5** | ATP→emit 직결 부재 + 합법경로 생존 | 20/20 해시 byte-identical · 본문 `atp` 심볼 부재 · emit_rate k1 0.423 / EXP 0.462 / k8 0.500 | ✅ |

## 3. 헤드라인 — control별 paired-t **전부** (규약 1: `max(controls)` 금지)

헤드라인 detector = **배치정책 하 held-out test acc**, ATP 지출 매칭. n=20 paired-CRN.

### 조건 A — `iid` 수요 (사전등록 기본)
`binding=0.528 · mean_k(EXP)=1.669 · corr(afford, demand) = −0.005`

| arm | mean_k | ATP/샘플 | acc (micro) | acc (macro) |
|---|---|---|---|---|
| **EXP** ATP 경제 | 1.669 | **3.669** | **0.7403 ± 0.0109** | 0.7405 |
| `c1` static cap (수요맹목 상수) | 2.000 | 4.000 ⬆ | 0.7593 ± 0.0115 | 0.7596 |
| `c2` permuted-k (동일 multiset·동일 지출) | 1.669 | 3.669 = | 0.7161 ± 0.0112 | 0.7164 |
| `c4` demand-shuffled | 1.669 | 3.669 = | 0.7158 ± 0.0110 | 0.7161 |
| `c5` **no-bank** (afford 주변분포 동일, 저장만 제거) | 1.668 | 3.668 = | 0.7410 ± 0.0110 | 0.7414 |
| `c3` no-bank raw (자원 열위) | 1.000 | 3.000 ⬇ | 0.6411 ± 0.0126 | 0.6415 |
| `ref` unbudgeted demand (자원 우위) | 2.527 | 4.527 ⬆ | 0.8331 ± 0.0095 | 0.8339 |
| `ref` static k=8 (자원 우위) | 8.000 | 10.000 ⬆ | 0.8201 ± 0.0083 | 0.8211 |

| Δ (EXP − control) | micro Δ | SEM | t | p | wins | sig | macro Δ (규약2) |
|---|---|---|---|---|---|---|---|
| **PRIMARY** vs `c1_static_ceil` | **−0.0190** | 0.0023 | **−8.36** | 8.6e-08 | 0/20 | ✅ | −0.0190 |
| **PRIMARY** vs `c2_perm_k` | **+0.0242** | 0.0021 | **+11.37** | 6.4e-10 | 20/20 | ✅ | +0.0241 |
| mech vs `c4_demand_shuffled` | +0.0245 | 0.0028 | +8.73 | 4.5e-08 | 20/20 | ✅ | +0.0244 |
| **mech vs `c5_nobank_affperm`** | **−0.0007** | 0.0014 | **−0.53** | 6.0e-01 | **9/20** | ❌ **ns** | −0.0009 |
| mech vs `c3_nobank_raw` | +0.0992 | 0.0075 | +13.22 | 5.0e-11 | 20/20 | ✅ | +0.0990 |
| ref vs `ref_unbudgeted_demand` | −0.0929 | 0.0039 | −23.97 | <1e-12 | 0/20 | ✅ | −0.0933 |
| ref vs `ref_static_kmax` | −0.0799 | 0.0039 | −20.41 | <1e-12 | 0/20 | ✅ | −0.0805 |

**POOLED(primary c1,c2) = +0.0026 (micro) / +0.0025 (macro)** · 두 규약에서 **부호 보존** ✅ (규약 6)

### 조건 B — `bursty` 수요 (자기상관 · 주변분포 동일 · 블록 25)
`binding=0.512 · mean_k(EXP)=1.642 · corr(afford, demand) = −0.560`

| Δ (EXP − control) | micro Δ | SEM | t | p | wins | sig |
|---|---|---|---|---|---|---|
| PRIMARY vs `c1_static_ceil` | −0.0280 | 0.0031 | −9.01 | 2.8e-08 | 0/20 | ✅ |
| PRIMARY vs `c2_perm_k` | +0.0191 | 0.0021 | +8.99 | 2.8e-08 | 20/20 | ✅ |
| mech vs `c4_demand_shuffled` | +0.0161 | 0.0028 | +5.82 | 1.3e-05 | 18/20 | ✅ |
| **mech vs `c5_nobank_affperm`** | **−0.0288** | 0.0022 | **−13.24** | 4.9e-11 | **0/20** | ✅ **(해롭다)** |

**POOLED(primary) = −0.0044** · 부호 보존 ✅

---

## 4. 판정 분해 — 무엇이 살고 무엇이 죽었나

### 4.1 🎭 **F1 고유 내용 = 「보존 ATP 장 + 저장(reservoir)」 → THEATER (기여 정확히 0)**

결정적 통제는 `c5_nobank_affperm` 이다: **지출도 같고(3.668 vs 3.669), afford 의 주변분포도 EXP 와 정확히 같고(permutation), 수요 신호도 그대로 쓰되, 저장(시간상태) 동역학만 파괴**했다. 그 Δ = **−0.0007 ± 0.0014 (t=−0.53, p=0.60, 9/20 = 동전)**.

⇒ **ATP 를 보존하고 저수지에 쌓았다가 나중에 쓰는 것**이 산출하는 값 = **0**.
왜인가 — 코드가 아니라 구조가 답한다: iid 수요에서 `corr(afford, demand) = −0.005`. **저수지 잔고는 다음 샘플의 난이도와 무상관**이므로, 저장은 cap 의 *주변분포*만 바꾸는 **FORM 노브**일 뿐 예측적 배분을 하지 못한다. 저장의 marginal 만 복제하면(=c5) 성능이 **완전히 재현**된다.

그리고 bursty 수요에선 **−0.0288 (t=−13.24, 0/20) 로 적극적으로 해롭다**: `corr(afford, demand) = −0.560` — 어려운 샘플이 연달아 오면 저수지가 **바로 그때** 고갈된다(탐욕적 지출이 지속수요와 역상관). 저장은 도움이 되기는커녕 **수요가 뭉칠수록 나쁜 배분기**다.

> 측정 메타법칙 그대로: FORM(예산이 52.8% 묶인다 · ATP 장·생산·소비·저수지 전부 작동)은 화려하게 움직이는데 BIND(held-out Δ)는 **정확히 0**. 원 카드의 Null("예산 회계는 bookkeeping THEATER") 이 **이번엔 licensed 되게** 참이다.

### 4.2 ✅ **수요→용량 배분 채널 = EARNED (그러나 F1 의 것이 아니다)**

vs `c2`(동일 k multiset·동일 총지출·수요-표본 결합만 파괴) **+0.0242 (t=+11.37, 20/20)**, vs `c4`(수요 스크램블) **+0.0245 (t=+8.73, 20/20)**. 두 통제가 일치 ⇒ **+2.4pp 전량이 demand↔표본 정렬에서 나온다.**

이건 lane 이 이미 세운 유일한 생존 기제(**F10 수요주도 biogenesis** Δthr=+0.0080 5.7σ · **F4-SEC 절대 setpoint** t=+5.50)의 **세 번째 독립 재현**이다 — 이번엔 다른 기질(topic×polarity 결합), 다른 헤드라인(held-out acc), 다른 통제(multiset-permutation), n=20.

**그러나 이 채널은 ATP 회계를 전혀 필요로 하지 않는다.** `ref_unbudgeted_demand` (ATP 예산 **없이** k=demand 만) = **0.8331**, 지출 4.53 — **static k=8(0.8201, 지출 10.0)을 절반도 안 되는 비용으로 이긴다.** 즉 값은 **"수요만큼만 켜라"** 에 있지, **"장부를 적고 저수지를 굴려라"** 에 있지 않다.

### 4.3 ❌ **경제 전체가 「그냥 9% 더 쓰기」에 진다**

vs `c1`(수요맹목 상수캡 k=2, ATP 를 **9% 더** 씀) = **−0.0190 (t=−8.36, 0/20)**. 배분 이득(+2.4pp)이 예산 증분(+1.9pp 이상)보다 작다 ⇒ **ATP 경제는 레버가 아니라 예산 증분의 열등한 대체재**다. `POOLED(primary) = +0.0026 ≈ 0`.

> 이것이 `Δ = exp − max(controls)` 를 금지하는 이유의 교과서적 실례다. 만약 `max` 를 썼다면 c1 하나가 전부를 삼켜 **KILL** 이 나왔을 것이고, `min` 을 썼다면 c2 만 보고 **PASS** 가 나왔을 것이다. 둘 다 거짓이다. **control 마다 서로 다른 질문에 답하며, 각각 유의하다.**

### 4.4 두 판정층의 화해 (`result.json` 읽는 법)

`result.json.verdict` 는 **사전등록 규칙**이 뱉은 문자열이고, 그 규칙은 **primary control(c1,c2)만** 본다:

> `SPLIT/DIRECTIONAL — 동일지출 수요맹목 통제(c2)는 이기나 지출이 더 많은 static 상수(c1)에는 짐`

이는 **틀리지 않았지만 F1 을 채점하지 않는다** — c1/c2 대비는 "수요 정렬 배분"을 재는 것이지 "ATP 장" 을 재는 게 아니다. **H_9273 이 주장하는 것(보존 스칼라장·생산·소비·저수지)** 을 직접 채점하는 통제는 `c5` 하나뿐이며(동일지출·동일 afford 주변분포·저장만 제거), 그 답은 **Δ = −0.0007 (ns, 9/20)** 이다. 따라서:

| 층 | 대비 | 판정 |
|---|---|---|
| 사전등록 primary 규칙 | EXP vs {c1, c2} | SPLIT/DIRECTIONAL |
| **H_9273 고유 기제** (`verdict_decomposition.atp_field_itself_storage`) | **EXP vs c5** | **🎭 THEATER** |
| 부수 기제 (F10/F4 소관) | EXP vs {c2, c4} | ✅ EARNED |

**⇒ 카드 H_9273 의 최종 판정 = THEATER.** (SPLIT 은 "배분 채널"에 대한 것이지 "에너지 경제"에 대한 것이 아니다.)

### 4.5 학습단계 경제 (부차 · 공통 k=8 평가)

`mean_k=1.67 · binding=0.697` — vs static Δ=**−0.0186** (t=−8.56) · vs perm-k Δ=**−0.0004** (t=−1.04, **ns**).
⇒ 학습 중 ATP 경제도 **수요맹목 순열 대비 이득 0**(ns)이고, 상수 대비로는 손해(용량이 낮아서). 학습 레인에서도 THEATER.

---

## 5. 결론 · 원 카드 대비

| 원 카드 | 이번 재발사 |
|---|---|
| PASS 조건: "예산이 유의 비율로 binding **AND** 용량 조임 → downstream Δ > 두 control" | binding ✅ **0.528** (원 설계에선 정의상 불가능했던 것). 그러나 두 control 은 **자원 우위**라 구조적 달성불가 ⇒ **동일비용 대비**로 교정 |
| FAIL 조건: "어느 캡에서도 ΔEff≈0 ⇒ bookkeeping theater" | **ATP 장 자체 ΔEff = −0.0007 (ns, 9/20)** ⇒ **THEATER 확정 — 이번엔 검출력 52배 여유·정보채널 실증·통제 5개 하에서** |

**⇒ H_9273 = 🎭 THEATER (licensed).** 원 판정 ⛔INVALID 는 "채점 불가"였고 이번엔 **채점됐다**. F1 레인은 이제 THEATER 로 닫아도 되며, 그 근거는 "Δ 를 못 쟀다" 가 아니라 **"동일지출·동일 afford 주변분포에서 저장 동역학의 기여가 0 임을 20/20 seed 로 쟀다"** 이다.

**살아남은 것**은 F1 의 것이 아니다 — 수요→용량 배분(F10/F4 기제)의 **3번째 독립 재현**이며, 그것은 **ATP 회계 없이 더 싸게** 얻어진다.

### SYNTHESIS.md §4.3 (NO-SPEND 권고)에 미치는 영향
- 강화한다. F1 의 "에너지 경제" 프레임은 **순수 오버헤드**로 확정 — 303M 에 ATP 회계를 얹을 이유가 사라졌다.
- 다만 §4.3 (b) 제안(**abs-setpoint 배분기를 ConvMoE capacity schedule 에 eval-only 로 결착**)은 **여전히 유효하고 오히려 더 선명해졌다**: 배선할 것은 **저수지가 아니라 "수요만큼만 켜라"(k=demand) 규칙 하나**다. ATP 장·생산·소비·health 동역학은 전부 버려도 된다(0 손실).

### 남은 것 / 이 프로브가 답하지 못한 것 (scope)
1. **라우팅은 학습되지 않았다** — 수용장(receptive field)을 (topic×polarity)로 **고정(frozen-first)** 했다. CE 로 라우터를 처음부터 학습시키면 이 토이에선 **대칭 붕괴**로 특화가 안 생긴다(전 arm route_recall ≈ chance — 원 프로브 R3 와 같은 실패). 라우팅 학습가능성은 본 가설(에너지 경제)의 대상이 아니라서 기질 속성으로 고정했으나, **"실기질에서 demand 센서가 이만큼 좋을 것인가"는 미측정**이다 (여기선 corr(demand,m)=+0.94 = 준-오라클).
2. **저장이 값을 낼 수 있는 유일한 조건**은 `corr(afford, demand) > 0` — 즉 **수요를 예측하는** 저수지다(현 설계는 탐욕적이라 iid 에서 무상관, bursty 에서 역상관). 예측적 배분기(수요 예보 + 선제적 비축)는 미탐. 단 이는 이미 F10 의 경계조건("수요 지속성 > 할당 지연")과 같은 축이며, **F1 고유의 새 레버가 아니다**.
3. **engine-native 0** — numpy toy. `a_engine_native_learning` 상 DIRECTIONAL 천장. 다만 본 판정은 **음성(THEATER)** 이므로 cement 대상이 아니다.
