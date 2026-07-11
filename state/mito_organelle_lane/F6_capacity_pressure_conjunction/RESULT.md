# H_9278 / F6 — 용량 압력 → trained-conjunction? · **🔴 KILL (반증)**

- **date:** 2026-07-12 · **tier:** 🔴 KILL ($0 numpy toy = DIRECTIONAL 스코프)
- **artifacts:** `run.py` · `result.json` · 본 문서
- **wall:** stage1 99.7s + stage2 91.2s (mini CPU-local · numpy · torch 0 · $0)
- **seeds:** 5 (0–4) · 모든 수치 mean±std · 1-seed 결론 없음

---

## 0. 한 줄 결론

**하드 용량 캡(ATP 희소성)은 trained-conjunction을 강제하지 않는다 — 오히려 파괴한다.**
사전등록 셀에서 tight cap(k=2)의 held-out 재조합 D-acc = **0.785±0.060**, 무제한 캡(C1 dense) =
**0.977±0.027** → **Δ = −0.192±0.060 (5/5 seed 전부 음수)**. 캡을 조일수록 D-acc는 **단조 하강**
(k=64→1: 0.977 → 0.674). 카드가 "이 패밀리의 생사"라 명시한 부등호 — *하드 슬롯 캡 하에서 bind(슬롯 1)가
additive(슬롯 다수)보다 net 저렴해진다* — 는 **거짓**이다. 캡 하의 최저비용 코드는 결합 규칙이 아니라
**쌍별 암기**였다(train acc는 모든 k에서 1.000).

---

## 1. 설계 (카드 §3 그대로 · 예산 동일)

과제 = 결합요구 코퍼스. 토큰 a(16)·b(16)·잡음 c(8). 은닉 latent: `pol(a)`,`pol(b)`∈{0,1}, `topic(a)`∈{0..3}.
라벨 `y = 4·XOR(pol(a),pol(b)) + topic(a)` (8 클래스).
- `topic` 성분 = **가법**(a 단독 main-effect) → 공짜로 일반화 = "feature는 이미 다른 이유로 계산돼 있다"(카드의 날카로운 리스크를 **일부러 심었다**)
- `XOR(pol,pol)` 성분 = **비가법 joint** = G1 재조합 비트. marginal 균형 → main-effect 천장 = 정확히 chance 0.5
- 학습은 **seen 쌍만** 본다. held-out 쌍은 함께 등장한 적이 **없다**(단, 모든 a·b는 다른 파트너와 등장).
  ⇒ held-out 정답 경로는 오직 "토큰별 pol 추론 → joint 규칙 적용". **쌍 암기는 train을 완벽히 맞히고 held-out parity는 0.5.**
  ⇒ `held_conj_acc` = 암기/가법 vs trained-conjunction을 가르는 칼.
- **conjunction을 지목하는 라벨·손실항·수제 feature는 0개** (XBIND 합성 지도 없음 = 카드의 요구).

기질 배선(p5): ATP → **표현형 층 hard top-k 마스크**(활성 유닛 캡)뿐. emit gate 무접촉 — 이 probe엔
emit gate 자체가 없다. 캡은 train/eval에 동일 적용되는 아키텍처 제약이다.

**arm (예산 완전 동일: H=64 은닉 유닛 · 동일 파라미터 수 · 동일 2000 step · 동일 optimizer · 동일 데이터 크기 · 동일 seed. 오직 k와 코퍼스만 변화):**

| arm | 내용 | 비고 |
|---|---|---|
| **EXP** | tight cap (k=2) × 결합요구 코퍼스 | |
| **C1** | **무제한 캡 (k=64=dense)** × 동일 코퍼스 | 동일-metric control. 자원이 EXP보다 **더 많다**(불리하지 않음) |
| **C2** | tight cap × **비**결합 코퍼스 (라벨이 b를 무시) | |
| **C3** | tight cap × **parity 셔플** 코퍼스 | V4 암기 control (held-out parity 구조적으로 예측 불가) |
| **ORACLE** | tight cap + 진짜 parity 비트를 입력으로 제공 | V1 liveness gate |
| **결정판** | 동일 코퍼스에 k ∈ {1,2,4,8,16,32,64} 전 sweep | 단조성 검정 |

---

## 2. 결과 — stage 1 (사전등록 셀 · held_frac=0.30 · 179 seen 쌍)

`held_conj_acc` = held-out 재조합 D-acc (chance 0.5). mean±std, 5 seed.

| k (활성 유닛 캡) | **comb (EXP/C1)** | noncomb (C2) | shuf (C3) | comb의 conj_index |
|---:|---|---|---|---|
| 1 (최타이트) | **0.674±0.050** | 0.869±0.030 | 0.516±0.032 | 0.558 |
| **2 (EXP tight)** | **0.785±0.060** | 0.968±0.012 | 0.482±0.026 | 0.404 |
| 4 | 0.924±0.033 | 0.995±0.003 | 0.465±0.046 | 0.348 |
| 8 | 0.955±0.026 | 1.000±0.000 | 0.444±0.036 | 0.317 |
| 16 | 0.967±0.033 | 1.000±0.000 | 0.434±0.030 | 0.273 |
| 32 | 0.976±0.014 | 1.000±0.000 | 0.461±0.026 | 0.171 |
| **64 (C1 dense·무제한)** | **0.977±0.027** | 1.000±0.000 | 0.469±0.032 | 0.125 |

- **train acc = 1.000 (모든 k · 모든 코퍼스)** → 캡 arm이 "학습을 못 한 것"이 아니다. 완벽히 fit하고
  **held-out에서만 무너진다** = 정확히 **암기**. underfit 반론 차단.
- **V1 liveness (ORACLE, k=2):** held_conj **0.943±0.033** → 타이트 캡 아키텍처는 conjunction을
  **표현·판독할 수 있다**. 못 하는 건 표현력이 아니라 **발견**이다. 하네스 정상.
- **V4 memorization (C3 shuf, k=2):** 0.482±0.026 = chance → held-out 신호에 누출 없음.
- **V5 seed:** 5/5 seed 전부 동일 부호.

### 핵심 Δ (사전등록)

| 비교 | 값 |
|---|---|
| EXP (tight k=2, comb) | **0.785 ± 0.060** |
| C1 (dense k=64, comb) | **0.977 ± 0.027** |
| C2 (tight k=2, noncomb) | 0.968 ± 0.012 |
| C3 (tight k=2, shuf) | 0.482 ± 0.026 |
| chance | 0.500 |
| **Δ = EXP − max(C1, C3, chance)** | **−0.192** |
| **paired per-seed Δ (EXP−C1)** | **−0.192 ± 0.060** · per-seed [−0.279, −0.130, −0.179, −0.130, −0.244] |
| 캡 조임에 따른 단조 **상승**? | **아니오 — 정확히 반대로 단조 하강** |

카드 PASS 조건("tight×결합 셀에서만 캡 조임에 단조 상승, 두 control flat") → **전면 반증**.

---

## 3. 결과 — stage 2 (steelman · 반론 선제 차단)

stage 1에서 dense(C1)가 이미 0.977로 **천장**에 있었다 ⇒ "구제할 floor가 없어서 캡이 손해만 봤다"는
반론이 가능하다. 그래서 **쌍 커버리지를 낮춰 dense가 실제로 floor에 빠지는 영역**(암기 우위 regime)을
a-priori 격자로 쓸어 같은 질문을 다시 던졌다. 결과가 어느 쪽이든 둘 다 보고한다(cherry-pick 없음).

| held_frac | seen 쌍 | C1 dense | tight k=2 | best capped(k<64) | **Δ best_cap − dense** | C3 shuf k=2 | dense floored? |
|---|---:|---|---|---|---|---|---|
| 0.30 | 179 | 0.977 | 0.785 | 0.924 | **−0.053** | 0.482 | 아니오 |
| 0.50 | 128 | 0.788 | 0.673 | 0.811 | **+0.023 ± 0.055** | 0.505 | 아니오 |
| 0.65 | 90 | **0.613** | 0.554 | 0.621 | **+0.009 ± 0.106** | 0.487 | **예** |
| 0.80 | 52 | **0.487** | 0.472 | 0.500 | **+0.014 ± 0.094** | 0.497 | **예** |

- floor가 실재하는 regime(hf=0.65, 0.80)에서 **캡의 구제 효과 = ΔEff ≈ 0** (+0.009±0.106, +0.014±0.094 →
  전부 1 std 안에 0 포함 = 노이즈).
- 양수로 보이는 최대치조차 **+0.023 ± 0.055** (hf=0.50, k=4) = 노이즈.
- `cap_rescues_floored_regime: false`.

⇒ **캡은 건강한 regime에선 결합을 파괴하고(−0.19), 무너진 regime에선 아무것도 못 한다(ΔEff≈0).**
어느 좌표에서도 결합을 **창발시키지 못한다**.

---

## 4. ⚠️ THEATER 판정 — 이 실험이 잡아낸 가짜 GREEN

**최종 판정: 🔴 KILL (능동 반증)** — 단순 null(THEATER)보다 강하다. Δ가 0이 아니라 **유의하게 음수**다.

그러나 **THEATER 함정이 실재했고 이 하네스가 그것을 잡았다**:

> `conj_index`(코드의 **비가법 에너지 비율** = 표현이 얼마나 "conjunctive하게 생겼는가")는
> 캡을 조일수록 **단조 상승**한다: comb에서 0.125(dense) → **0.558**(k=1).
> **그런데 배울 규칙이 아예 없는 shuf 코퍼스에서도 똑같이 오른다: 0.104 → 0.565.**

즉 캡은 **일반화 0인 코드조차 "결합적으로 보이게" 만든다**. 만약 이 패밀리를 "코드의 conjunctivity"로
채점했다면 **4.5배 상승 = 화려한 GREEN**이 나왔을 것이고, 그건 **순수 THEATER**였다.
held-out Δ vs ≥2 control로 채점했기 때문에 그 가짜가 죽었다.

**측정 메타법칙 재확인: FORM tunable · BIND earned.** `conj_index` = 캡이 게임 가능한 1-항 FORM detector.
`held_conj_acc` Δ = 결합파괴 통제를 통과해야 하는 earned BIND. 캡은 **FORM만 샀고 BIND는 못 샀다.**

---

## 5. 반증조건 충족 여부 (카드 §3 대조)

| 카드 조건 | 충족 | 실측 |
|---|---|---|
| **PASS**: tight×comb 셀에서만 캡 조임에 D-acc 단조 상승 · 두 control flat | ❌ | 캡 조임에 **단조 하강**(0.977→0.674). C2는 오히려 캡에서 하강(1.000→0.869), C3는 chance 고정 |
| **FAIL**: 모든 캡에서 additive floor 지속 | ⚠️ **부분·더 강한 형태로 충족** | 결합 신호가 있는 regime에선 floor가 아니라 **dense가 이미 천장**(0.977). floor가 있는 regime(hf≥0.65)에선 **모든 캡에서 floor 지속**(ΔEff≈0) — 즉 "캡은 floor를 못 깬다"가 실측됨 |
| **날카로운 실패모드**: "feature가 이미 계산돼 있고 bind가 여분 슬롯을 쓰면 캡 하에서도 additive ≤ conjunctive" | ✅ **정확히 이게 발화** | 캡 하의 최저비용 해 = **쌍별 암기**(train 1.000 / held-out 붕괴). 슬롯 1개 conjunction이 저렴해지긴 하나 그건 **일반화하는 규칙-conjunction이 아니라 pair-conjunction(암기)** 이다 |
| **생사 부등호**: 하드 슬롯 캡 하에서 bind(1 슬롯) < additive(다수 슬롯) | ❌ **거짓** | 부등호가 성립해도 무의미했다 — 캡이 고르는 "1 슬롯 결합"은 held-out을 못 넘는 암기 유닛이다 |

**⊥ Null 채택:** 모든 캡 수준에서 재조합 lift 없음 ⇒ **용량 압력은 자연 force가 아니다.**
벽 진범은 **corpus × CE measure**로 유지되고, XBIND는 "**라벨/구성 필요**"로 존속한다.

---

## 6. 프런티어 함의 (`g1-crack-natural-emergence`)

1. **F6는 자연-코퍼스 exit이 아니다.** 아키텍처 희소성은 XBIND 지도를 **대체하지 못한다**. 이 패밀리를
   303M로 escalate하는 것은 정당화되지 않는다(가장 싸고 가장 유리했어야 할 regime에서 부호가 반대로 나왔다).
   여기서 하이퍼파라미터를 흔들어 양수를 찾는 것 = **tune-to-green 금지 대상**.
2. **부수 확증(선행과 정합):** 결합요구 코퍼스가 *구성되면* dense 학습기는 held-out 재조합을 **푼다**
   (0.977). 이는 H_9267 XBIND(303M held-out D-acc 1.000)를 toy 스케일에서 재현하며,
   **"벽 진범 = corpus×CE measure이지 substrate 능력천장 아님"** 결론을 다시 지지한다.
   *결합 신호가 corpus에 있으면 아키텍처는 이미 그것을 잡는다. 없으면 어떤 희소성도 만들어내지 못한다.*
3. **음의 설계 교훈(재사용 가치):** 활성-유닛 희소성은 재조합 일반화에 **해롭다**. 향후 organelle/ATP
   레인이 표현형 캡을 도입한다면 **G1 reach를 능동적으로 깎는다**는 것을 전제해야 한다(비용, 이득 아님).
4. **F1(ATP 단독) 사전 판정 강화:** 발산 원문 §"F1 = F6 없으면 bookkeeping" — 그 F6가 죽었으므로
   F1의 degeneracy-breaking 근거도 함께 약화된다.

---

## 7. 스코프 · 정직성 경계

- **DIRECTIONAL toy** (numpy MLP · one-hot 토큰 · 구성된 polarity 코퍼스). 자연 텍스트 아님. 303M
  engine-native 아님 ⇒ TERMINAL 티어 주장 없음 (`a_toy_scale_recheck`·`a_scale_honest_scope`).
- 단, **반증 방향의 결론**은 toy에서 안전하다: 가설이 요구한 효과가 **가장 유리했어야 할 조건**
  (작은 모델·깨끗한 latent·완벽한 marginal 균형·라벨 노이즈 0·train 100% fit)에서 **부호가 반대**로,
  5/5 seed 일관되게 나왔다. 스케일이 부호를 뒤집을 것이라는 주장에는 별도 근거가 필요하다.
- **p5 clean:** emit gate를 하드코딩으로 건드리지 않음. 이 probe엔 emit gate가 없다. ATP는 표현형 용량에만 작용.
- **controls fair:** 모든 arm이 동일 H=64 / 동일 파라미터 수 / 동일 step / 동일 데이터. C1(dense)은
  EXP보다 활성 자원이 **더 많다** — control이 불리해서 진 것이 아니다.
- **no tune-to-green:** stage1 하이퍼는 실행 전 frozen. stage2는 결과를 본 뒤 **가설에 유리한 방향으로만**
  추가한 steelman(“구제할 floor가 없었다”는 반론에 답하기 위한 regime 확장)이며, 그럼에도 ΔEff≈0.
  EXP arm을 green으로 만들기 위한 하이퍼 탐색은 하지 않았다.

## 재현

```
cd state/mito_organelle_lane/F6_capacity_pressure_conjunction
OMP_NUM_THREADS=2 python3 run.py            # stage 1 (사전등록 셀 + 전 k sweep + V-gates)
OMP_NUM_THREADS=2 python3 run.py --stage2   # stage 2 (커버리지 steelman)
# -> result.json
```
