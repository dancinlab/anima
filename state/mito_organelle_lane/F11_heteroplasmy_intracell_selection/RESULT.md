# H_9283 / F11 — 이질형질 세포내 선택 · $0 probe 결과

**판정: 🔴 KILL** (반증 조건 충족 · 5 seed · wall 13.3s · numpy CPU-local)

> **한 줄 결론:** ATP-효율 선택은 *자기 지표 위에서는 확실히 작동*한다(eff Δ=+0.054, 5/5 seed, 세대별 단조 상승 0.846→0.911 — landscape는 flat이 아니다). 그러나 그 선택이 만든 config는 **held-out 재조합에서 3개 control 전부에게 진다**(held_conj Δ=−0.031, held_acc Δ=−0.070). 효율은 **잘못된 나침반**이다 — 오르면 오를수록 earned 지표가 내려간다.

---

## 1. 무엇을 돌렸나 (카드 §3 그대로)

세포마다 organelle **개체군** M=24 (heteroplasmy). organelle i는 gradient-free mtDNA 게놈 `g_i ∈ R^64` = 호흡/routing config. 세포의 작동 config = 이질형질 가중 consensus `u = Σ wᵢgᵢ`.

- **표현형성에만 개입 (p5-clean):** `S = relu(XW₁+b₁) · sigmoid(u)` → **hard top-k (K=2)** → `code = S·M`. ATP는 *어떤 유닛이 발화 가능한가*만 정하고, **emit gate는 이 probe에 존재조차 하지 않는다.** 게놈은 gradient가 **한 번도** 건드리지 않는다(구조적으로 — `dZ = dS·p·(Z>0)`에서 p는 상수).
- **선택 루프:** 세대마다 organelle 각자의 게놈을 점수화 → replicator 틸트(효율 개체 클론증식 / 열등 개체 미토파지) → multinomial **병목**(drift) + 변이(σ=0.35). 10 세대 × 100 CE epoch = 1000 epoch.
- **적합도(실험 arm) = ATP-효율, label-free · CE-free (p7-safe):** `eff = throughput / ATP` = (pair-code 간 평균 L2 거리) / (powered active mass). 스케일 불변이라 선택압이 *gain 인플레*가 아니라 **routing**(어떤 유닛이 호흡하는가)에 걸린다. 라벨도 CE도 이 수치에 절대 닿지 않는다.

### 과제 (F6 공유 · conjunction 비지도)
`y = 4·XOR(pol(a),pol(b)) + topic(a)` (8-class). topic = a의 additive 주효과(공짜로 일반화) · parity = a,b의 **비가산 결합** = G1 재조합 비트(chance=0.5). held-out (a,b) 쌍은 **학습 중 절대 동시출현하지 않음**(단, 모든 a와 모든 b는 다른 파트너와 등장) ⇒ 쌍 암기는 held-out parity를 정확히 0.5로 만든다.

### 동작점 (사전 고정 · 스윕 없음)
**K=2.** F6이 이미 측정한 cap 곡선(dense k=64 → held_conj 0.977 · k=2 → 0.785)에서 **ATP 제약이 실제로 binding되고 headroom이 남는 유일한 지점**. k≥8은 천장효과라 퇴화된 테스트가 된다. F11 첫 실행 전에 고정, 이후 무변경.

---

## 2. Arm · 예산 공정성

**모든 evo arm이 매 세대 3개 적합도(eff·CE·oracle)를 **전부** 계산한다. 유일한 차이는 그중 *무엇이 replicator를 구동하는가* 한 줄.** 동일 seed → 동일 trunk init · 동일 초기 게놈 개체군 · 동일 RNG 스트림 · 동일 M/세대/변이율/병목/epoch. flops 동일.

| arm | 적합도 신호 | 역할 |
|---|---|---|
| **exp** | ATP-효율 (label-free) | 🎯 가설 |
| **c1_drift** | 없음 (f=0) | control 1 (카드 c1 · 선택 無 = 순수 drift+변이) |
| **c2_ce** | −CE(train) · 라벨 사용 | control 2 (카드 c2 · **Goodhart control**) |
| **c3_shuf** | eff 값의 **순열** | control 3 (**ARM-SHOCK** — 선택 *강도* 동일, 신호만 파괴) |
| oracle | held-out conj acc (train-on-test) | **V1 liveness** (arm 아님) |
| ref_dense | cap 없음(k=64)·게놈 동결 | 천장 REFERENCE (control 아님) |

적합도는 세대마다 z-score 후 `exp(β·z)` → **선택 강도가 모든 적합도 종류에 걸쳐 동일**. c3_shuf가 있기 때문에 "선택이 개체군을 붕괴시켜서 생긴 손해"와 "효율 신호 자체의 손해"를 분리할 수 있다.

---

## 3. 수치 (mean ± std · 5 seed)

| arm | **held_acc** ⬅earned | **held_conj** ⬅earned·G1 | held_add | train_acc | eff ⬅self-metric | conj_index | ATP | ESS(이질형질) |
|---|---|---|---|---|---|---|---|---|
| **exp** | **0.773 ± 0.028** | **0.821 ± 0.040** | 0.904 ± 0.017 | 0.940 | **0.939 ± 0.008** | **0.441 ± 0.030** | 7.63 | 3.1 / 24 |
| c1_drift | 0.809 ± 0.062 | 0.837 ± 0.047 | 0.960 ± 0.029 | 0.961 | 0.883 ± 0.012 | 0.325 ± 0.034 | 8.24 | 24.0 |
| c2_ce | **0.842 ± 0.053** | **0.852 ± 0.051** | 0.982 ± 0.004 | 0.994 | 0.869 ± 0.018 | 0.313 ± 0.051 | 9.39 | 5.7 |
| c3_shuf | 0.814 ± 0.059 | 0.848 ± 0.059 | 0.929 ± 0.045 | 0.965 | 0.885 ± 0.025 | 0.304 ± 0.048 | 8.94 | 2.1 |
| *oracle (V1)* | *0.901 ± 0.057* | *0.927 ± 0.042* | *0.965* | *0.984* | *0.877* | *0.342* | 9.30 | 3.5 |
| *ref_dense (ref)* | *0.958 ± 0.032* | *0.958 ± 0.032* | *1.000* | *1.000* | *0.168* | *0.127* | 24.6 | 24.0 |

chance: held_acc 0.125 · held_conj **0.500**

### Δ (exp − best control)

| 지표 | 성격 | exp | best control | **Δ** | seed별 승수 |
|---|---|---|---|---|---|
| **held_acc** | **BIND (earned)** | 0.773 | 0.842 (c2_ce) | **−0.0695** | vs c1 2/5 · vs c2 1/5 · vs c3 1/5 |
| **held_conj** | **BIND (earned · G1 비트)** | 0.821 | 0.852 (c2_ce) | **−0.0305** | vs c1 3/5 · vs c2 2/5 · vs c3 1/5 |
| eff | FORM (자기 선택 지표) | 0.939 | 0.885 (c3_shuf) | **+0.0538** | 5/5 |
| conj_index (ANOVA 비가산 에너지) | FORM (1-항 detector) | 0.441 | 0.325 (c1_drift) | **+0.1160** | 5/5 |

**exp는 3개 control 중 단 하나도, 두 earned 지표 중 어느 쪽에서도 평균으로 이기지 못한다 (0/3 × 0/2).**

---

## 4. 판정

사전등록 규칙(run.py 헤더, 첫 실행 전 고정):
- PASS(reach): held_acc Δ > 0.02 AND mean±std 분리 → **FAIL** (Δ = −0.070)
- PASS(conj): held_conj Δ > 0.05 AND exp > 0.55 → **FAIL** (Δ = −0.031)
- THEATER: eff Δ>0 인데 earned Δ ≈ 0 (|Δ|<0.02) → **해당 없음** (earned Δ가 0이 아니라 **음수**)
- INVALID: oracle(V1)도 floor → **해당 없음** (아래 V-gate 참조)
- ⇒ **KILL**

**THEATER보다 나쁘다.** ΔEff≈0(무해한 bookkeeping)이 아니라, 효율 선택이 earned 지표를 **적극적으로 훼손**한다. 카드의 반증 조건 "선택 ≈ drift ⇒ theater"는 충족될 뿐 아니라 초과된다 — **선택 < drift**.

### V-gate
- **V1 liveness ✅ PASS:** oracle arm(진짜 목표 지표로 선택)은 held_conj 0.927 로 drift(0.837)를 확실히 넘긴다 ⇒ **routing 탐색 공간 안에는 held-out 재조합을 올리는 config가 실재하고, 이 gradient-free GA는 그걸 찾아낼 능력이 있다.** 즉 "탐색 공간이 비었다 / GA가 무력하다"가 아니다 → **INVALID 아님**. 나침반만 틀렸다.
- **landscape flat 아님 ✅:** exp의 세대별 eff_mean 단조 상승 0.846→0.870→0.888→…→0.911, ESS 24→3.1 (클론증식 실재). "활용가능 분산 없음"이라는 theater 시나리오도 **아니다**.
- train_acc 전 arm 0.87~1.00 (chance 0.125) · held_add 0.90~1.00 → 하네스·held-out eval 정상.
- p5 ✅: 이 probe에는 emit gate가 **존재하지 않는다**. ATP는 top-k 표현형 mask 한 곳에만 닿는다. 하드코딩 emit gate 0.

---

## 5. 메커니즘 — 왜 졌나 (수치가 말해주는 것)

1. **ARM-SHOCK(c3)이 "붕괴 탓" 변명을 차단한다.** c3_shuf는 exp보다 **더 심하게** 개체군을 붕괴시키고도(ESS 2.1 < exp 3.1) earned 지표는 exp보다 **낫다**(held_conj 0.848 vs 0.821). ⇒ exp의 손해는 선택으로 인한 다양성 붕괴/교란 때문이 **아니라 효율 신호의 방향 그 자체** 때문이다.
2. **효율은 실제로 달성됐다 — 잘못된 방식으로.** exp는 ATP를 가장 적게 쓰고(7.63 vs 8.2~9.4) 가장 많은 유닛에 코드를 흩뿌린다(사용 유닛 23.8 vs drift 19.6). 즉 "throughput/ATP" 최대화의 해답은 *결합(conjunction)*이 아니라 **pair-code를 더 많은 유닛에 얇게 분산**시키는 것 — 이건 결합이 아니라 **암기-계열 분산**이다. 그래서 심지어 공짜였던 additive 성분(held_add)이 가장 크게 무너진다(0.904 vs c2 0.982): 효율 압력이 a의 주효과 코드까지 파편화한다.
3. **🏆 핵심 발견 — conj_index는 G1 비트가 아니다.** exp는 ANOVA 비가산 에너지(conj_index)를 +0.116 (5/5 seed) 확실히 **올리면서** held-out 재조합은 **내린다**. **"코드가 비가산적이다" ≠ "일반화되는 conjunction을 배웠다".** conj_index는 1-항 FORM detector라 게임 가능하다 — 그리고 방금 게임당했다. (측정 메타법칙 재확증: FORM tunable · BIND earned. 같은 conj_index를 쓰는 형제 패밀리(F6 등)는 이 지표 단독으로 conjunction을 주장하면 안 된다.)
4. **c2_ce(Goodhart control)의 의외:** CE-guided 선택은 train을 거의 포화시키지만(0.994) held-out을 망치지 않고 오히려 최고 control이다(0.842/0.852) — 이 toy에선 라벨 신호가 routing 선택에 무해했다. 카드가 예상한 "CE 선택은 더 나쁘거나 overfit"은 **관측되지 않았다**(정직 보고). 대신 진짜 패자는 라벨-free 효율 신호였다.
5. 결국 **아무 선택도 하지 않는 것(drift)이 효율 선택보다 낫다.** 그리고 세 arm 모두 ref_dense 천장(0.958)에는 못 미친다 — cap 자체의 비용은 어떤 선택으로도 회수되지 않았다.

---

## 6. 카드에 대한 답 · 파급

- **카드 PASS 조건("Δ reach/효율 > 두 control AND 발견 config가 conjunctive")** — reach Δ **음수**. conjunctive-ness는 *FORM 지표로만* 올랐고 *earned 재조합으로는* 내렸다 ⇒ **보너스 조건도 실질 미충족**(사이비 conjunctive).
- **카드 FAIL 조건("선택 ≈ drift ⇒ 효율 landscape flat / 활용가능 분산 無 = theater")** — 충족되되 **원인이 다르다**: landscape는 flat이 **아니었고**(eff 단조 상승) 분산도 활용가능했다. 실패 원인은 *"오를 산이 없다"*가 아니라 ***"오른 산이 엉뚱한 산"***이다. 이게 더 강한 반증이다 — 효율 신호를 더 세게/더 오래 밀어붙이면 **더 나빠질 것**으로 예측된다.
- **G1 연결:** 없음. 세포내 gradient-free 선택은 conjunctive config를 CE보다 먼저 찾지 못했을 뿐 아니라, **아무것도 안 하는 것보다 못 찾았다.** F11은 F6의 증폭기가 아니다 — 이 동작점에서는 **감쇠기**다.
- **p8(gradient ⇄ mitosis)의 '선택으로의 확장'**: 이 형태로는 지지되지 않는다. 선택압의 *관측정의*(ATP-효율)가 reach와 정렬되지 않는 한, gradient-free 내부 진화루프는 자원만 태운다. oracle arm이 보여주듯 **탐색기는 멀쩡하다 — 목적함수가 문제다.** (교훈은 XBIND와 동형: 벽은 substrate 능력이 아니라 *measure*에 있다.)

**재개 조건(reopen):** reach와 인과적으로 정렬된 label-free 적합도 신호를 새로 발견했을 때만. ATP-효율(throughput/ATP)은 그 신호가 **아님**이 실측됐다. 하이퍼(β·σ·M·K)를 흔들어 green을 만드는 것은 tune-to-green — 금지.

---

## 산출물
- `run.py` — probe (numpy · $0 · 결정적 · 5 seed · 6 arm)
- `result.json` — raw 수치 (arm×seed 전체 · 세대 궤적 · gates · deltas)
- 재현: `OMP_NUM_THREADS=2 python3 run.py` (13.3s)
