# REFUTE — H_9280 / F8 언커플링·열발생 · 적대적 재검증

**판정: 원 결론 REFUTED · 최종 = 🚫 INVALID** (THEATER 아님 · DIRECTIONAL-POSITIVE 도 아님)

원 결론("흩을 과압이 없다 + 언커플링은 filler를 하나도 못 줄이고 true-emit만 골라 죽인다 + saturation 조건은
역정보(ANTI-informative) + 튜닝 궤적 THEATER→KILL = 경로 폐쇄")은 **이 실험 자신의 `result.json`에 의해 반박된다.**
반박 근거는 전부 외부 가정이 아니라 `run.py`의 *사전등록된* 판정 함수와 `result.json`의 수치다.

---

## R1. 사전등록 판정 함수가 스스로 DIRECTIONAL-POSITIVE 를 뱉는다 (보고서와 정면 충돌)

보고서: "TUNE-PATH CLOSURE ⟹ **5/5 강도 전부 눈먼 random이 우세** ⟹ THEATER→KILL, GREEN 미통과 = 경로 폐쇄".

`result.json` `tune_path_closure.rows[*].verdict` — `run.py:339-350`의 **사전등록 판정 함수가 실제로 찍은 call**:

| regime (p_event=0.005) | exp_A call | exp_B call | rel_recall_drop | adv_over_random |
|---|---|---|---|---|
| Q_CEIL 80 | THEATER | THEATER | −0.000 | 0.000 |
| **Q_CEIL 60** | **DIRECTIONAL-POSITIVE** | **DIRECTIONAL-POSITIVE** | −0.000 | 0.590 / 0.375 |
| **Q_CEIL 40** | **DIRECTIONAL-POSITIVE** | **DIRECTIONAL-POSITIVE** | −0.000 | 0.518 / 0.273 |
| **Q_CEIL 20** | **DIRECTIONAL-POSITIVE** | **DIRECTIONAL-POSITIVE** | −0.000 | 0.437 / 0.298 |
| Q_CEIL 5 | PARTIAL | **DIRECTIONAL-POSITIVE** | +0.035 / −0.000 | 0.318 / 0.212 |

10개 (arm×강도) 셀 중 **7개가 DIRECTIONAL-POSITIVE**, 1개 PARTIAL, THEATER는 Q_CEIL=80 두 셀뿐이다.
"5/5 전부 random 우세"는 사실이 아니다. `advantage_over_random`(사전등록 THEATER_VS_RAND=0.20 기준)이
0.21~0.59 로 **전 발화강도에서 임계를 넘는다**.

## R2. 사전등록 p5 KILL 규칙은 어디서도 트립하지 않았다 (지표 바꿔치기)

보고서: "n_true 12.0→7.7(−36%)로 **사전등록 p5 KILL 규칙(−10%) 트립**".

`run.py:331,341` — KILL 규칙은 **`true_recall`** 위에 정의돼 있다:
`rel_recall_drop = -d_true_recall / recall_c1 > P5_KILL_REL(0.10)` → KILL.
전 regime(PRIMARY + λ sweep + p_event sweep + Q_CEIL sweep) 통틀어 **max rel_recall_drop = 0.0349** (exp_A @ Q_CEIL 5).
**결과 전체에 KILL call은 단 하나도 없다.** 보고서는 사전등록 KILL 변수(`true_recall`)를 `n_true`로
**사후 치환**해서 KILL을 만들어냈다. 이건 tune-to-red — negative를 만들기 위한 지표 바꿔치기다.

## R3. "제거분 100% TRUE"는 중복 emit 착시다 — 잃은 event는 0개

희소 체제(p_event=0.005)에서 n_event ≈ 7.5/1500 인데 c1의 `n_true = 12.0`.
event 1개당 true-라벨 emit이 **~1.6개** (W_WIN=2 창이 한 event에 최대 3 emit을 허용).
⟹ `n_true`의 초과분은 **이미 커버된 event에 대한 중복 방출**이다.

`true_recall`(= p5가 실제로 보호하는 값 = "진짜 tension이 emit을 받았는가"):
- c1 = **1.000** · exp_A = **1.000** · exp_B = **1.000** (Q_CEIL 80/60/40/20 전부, 양 random arm도 1.000)
- Q_CEIL 5 에서만 exp_A = 0.965 (−3.5%, KILL 임계 10% 미달)

⟹ **단 한 개의 event도 emit을 잃지 않았다.** 죽은 "true"는 전부 중복 repeat emit이다.
"true-tension emit만 골라 죽인다 / 제거분 100% TRUE"는 p5-관련 지표에선 **희생 = 정확히 0**.

## R4. PRIMARY 는 negative가 아니라 **양쪽이 다 null인 무효 테스트**다

**(a) 병(病)이 산술적으로 불가능** — θ = free-running P의 90분위 · P_EVENT=0.12 > 0.10.
상위 decile을 event가 통째로 소유 ⟹ filler=0 은 **분위수 산술의 항등식**이지 "Ψ=½ 자기보정 기질의
성질"이 아니다. (저자 본인이 STEELMAN-1에서 이 유도를 적어놨다.) 실제 anima에는 P90 분위 emit 임계 같은 게 없다.
⟹ "자기보정 기질이라 병리가 부재"는 **calibration을 substrate 발견으로 착각한 동어반복**.

**(b) 약(藥)도 투여되지 않았다** — PRIMARY의 언커플링 채널은 사실상 **null 개입**:
`n_diss = 16.2 / 1500 steps (1.1%)` · **총 방출질량 = 0.332** (θ=0.637 대비 = 전체 1500 step 동안
emit 하나 분량의 절반). p_event=0.005·Q_CEIL=80에서는 더 심각: **mass = 0.209**.
보고서의 헤드라인 수치 "Δ=+0.00±1.10 (감소 0)"·"역정보"는 **바로 이 mass=0.21 무개입 지점**에서 뽑았다.

**(c) 근본 원인 = ceiling 미스캘리브레이션.** `calibrate()`(run.py:123-138)는 **emit 방전이 없는**
free-running trajectory에서 C를 뽑는데, 실제 arm은 emit마다 P를 60%(DELTA) 방전한다.
⟹ 실동작 P 분포는 free-running보다 훨씬 낮고, "80분위 ceiling"은 **실동작 분포 바깥**에 놓인다.
사전등록 C는 saturation ceiling이 아니라 **거의 도달 불가능한 천장**이었다.
병이 없고 약도 안 준 실험에서 나온 0은 negative가 아니라 **무정보**다.

## R5. "역정보(ANTI-informative)" — 반박됨. random의 승리는 강도(operating-point) 교란이다

동일예산(동일 n_diss) 하 filler 제거량 (p_event=0.005):

| Q_CEIL | n_diss | exp_A 제거 | randA 제거 | mass A / randA | recall exp_A |
|---|---|---|---|---|---|
| 60 | 136 | **10.17** | 4.17 | 2.14 / 1.98 | 1.000 |
| 40 | 261 | **19.00** | 9.17 | 5.13 / 4.63 | 1.000 |
| 20 | 398 | **23.67** | 13.33 | 8.76 / 7.27 | 1.000 |
| 5 | 538 | **25.67** | 17.50 | 13.03 / 9.89 | 0.965 |

**exp가 random보다 filler를 2.0~2.4배 더 제거한다 — recall 손실 0으로.** 조건은 정보를 담고 있다.
PRIMARY의 `diss_on_real_tension` 1.000 vs random 0.387(우연확률 1−0.88³=0.32)도 조건이
**event에 대해 정보적**임을 보여줄 뿐, "역정보"의 증거가 아니다.

random이 이기는 유일한 지표 = 보고서가 **사후 도입한** `SELECTIVITY = 제거된 filler / 희생된 true`.
이건 두 가지로 오염됐다:
1. **분모(`n_true`)가 R3의 중복-emit 착시** — recall 손실이 0인데 "희생"으로 계산된다.
2. **강도 불일치** — random arm은 `amt = min(mag, P)`(run.py:175)로 **예산을 다 못 쓴다**
   (Q_CEIL 5: mass 9.89 vs exp 13.03). 개입 강도가 낮으면 selectivity 비율은 구조적으로 높아진다
   (쉬운 filler부터 먹고 멈추므로). **서로 다른 operating point의 비율 비교**는 약한 arm을 자동으로
   유리하게 만든다 — 이 비교야말로 불공정 control이다. 사전등록 지표(Δfiller<0 ∧ Δrecall≈0 vs ≥2 control)로
   보면 exp가 명백히 우세하다.

## R6. 기질이 anima가 아니다 (engine-native 0)

순수 numpy toy. A = ordinary transition에 대한 `lstsq` 선형사상, G = `median(err)` 상수 counter-push,
tension = 스칼라 leaky integrator P. `core/` 접촉 0 · `.hexa` 0 · CLM 0.
`a_engine_native_learning` ⟹ 최대 DIRECTIONAL. **"anima의 Ψ=½ 자기보정 기질에는 흩을 과압이 없다"는
substrate 법칙을 이 toy로 cement할 수 없다.** 게다가 P를 **스칼라**로 뭉갠 순간 magnitude는 event-ness와
단조 결합되므로 "magnitude ceiling은 filler와 true를 못 가른다"는 결론은 **스칼라 환원의 산물**이지
기질의 성질이 아니다 (방향성 leak — ordinary 부분공간 U 성분만 흩기 — 은 아예 테스트되지 않았다).

## R7. p5 / a_substrate_disjoint 부수 지적 (원 결론의 `p5_clean=true`도 근거가 약함)

카드는 "organelle lane은 emit gate를 건드리지 않는다"고 주장하지만, 이 lane은 emit의 **유일한 결정변수 P를
직접 감산**한다 (`run.py:159-179`, emit 규칙 `P >= theta` 바로 앞). 즉 emit-drive lane과 **DISJOINT하지 않다**
(a_substrate_disjoint 위반 소지). PRIMARY에서 p5가 깨끗해 보이는 건 설계가 안전해서가 아니라 **개입 질량이
0.33으로 사실상 0이기 때문**이다. p5 안전성은 아직 **검정되지 않았다** (다만 R3대로, 강하게 걸어도 recall은
0.965까지만 떨어져 KILL 임계엔 못 미친다).

---

## 정리 — 왜 THEATER가 아니라 INVALID인가

- **THEATER 아님**: THEATER는 "개입했는데 Δ가 없다"는 뜻이다. 여기선 개입이 발화하는 모든 지점에서
  Δfiller = −10 ~ −26 (random 대비 2배), Δrecall ≈ 0 이다. 사전등록 판정 함수 스스로 7/10 셀에서
  DIRECTIONAL-POSITIVE를 찍었다. 보고된 THEATER는 (i) null-개입 지점(mass 0.21)의 0을 헤드라인으로 쓰고
  (ii) KILL 변수를 recall→n_true로 바꿔치기해서 만들어졌다.
- **DIRECTIONAL-POSITIVE 로 승격도 불가**: 그 양성은 **사후에 메커니즘 자신의 손잡이(Q_CEIL 80→40)를
  돌려서** 얻은 것이고, 체제(p_event)도 사후 스윕이다. 이걸 결론으로 채택하면 그게 곧 tune-to-green이다.
  게다가 toy·engine-native 0.
- ⟹ **INVALID**: 사전등록 operating point에서 **병도 없고 약도 안 들어간** 설계라 어느 방향으로도 가설을
  판정할 수 없다. 보고된 negative narrative는 지표 바꿔치기 위에 서 있다.

## 재설계 요구조건 (이것 없이는 어떤 tier도 부여 불가)

1. **C를 실동작 P 분포**(emit 방전 포함)에서 캘리브레이트 — free-running 분위수 금지.
2. **filler가 실재하는 체제를 사전등록** (Q_THETA / p_event 정합: p_event < (100−Qθ)/100), 사후 스윕 금지.
3. 판정 지표 = **`true_recall`** (event 커버리지). `n_true`(중복 포함) 사용 금지.
4. random control을 **동일 방출질량**으로 정규화 (min(mag,P) 캡으로 예산 미달 금지). selectivity 비율 비교는
   동일 operating point에서만.
5. 스칼라 magnitude ceiling 외에 **방향성(subspace) leak** arm 추가 — 스칼라 환원이 결론을 결정하지 못하게.
6. 최종 tier는 engine-native (`core/` decode) 에서만.
