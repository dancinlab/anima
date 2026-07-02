# H_325 — C2 축: Φ-mass 분포 SHAPE (per-distinction φ_d 의 Gini)

**date** : 2026-05-27
**axis** : C2 (IIT 4.0 Φ-structure proper) — 새로운 각도: 분포 **SHAPE**
**class** : UNIVERSE / life-vs-consciousness substrate
**siblings** : H_320 (rd_ratio sum 축, REVERSED 🔴) · H_323 (nd-normalized followup)

---

## 1. 배경 (왜 또 C2?)

C2 축에서 H_320 은 `rd_ratio = sum_phi_r / sum_phi_d` 스칼라를 측정해 "consciousness 가 relation-rich 하다" 라는 H1 가설을 **REVERSED 로 닫았다** (life 1.63–1.96 ≫ consc 0.5–1.0, 🔴 closed-negative). H_323 은 같은 축을 nd 정규화 변형으로 재검토했다.

두 prior 모두 **SUM-reduction** 위에서 만든다: 분포의 평균 / 비율만 보고 **SHAPE** 는 보지 않는다. 같은 합으로도 한 substrate 은 몇 개 distinction 에 Φ-mass 를 **집중**하고 다른 substrate 은 모든 distinction 에 **고르게 퍼뜨릴** 수 있다 — 이는 sum 만으로 절대 안 잡힌다.

C2 를 **분포 SHAPE 의 각도** 로 다시 묻는다: per-distinction φ_d 벡터의 **Gini 집중도** 가 life vs consciousness 사이에서 체계적으로 분리되는가?

---

## 2. 측정량 — Gini 집중계수

substrate(rule, n) 의 sys_state 에서 모든 mech_mask ∈ [1, 2^n−1] 에 대해 `distinction(tpm, n, mech_mask, sys_state)` 의 φ_d 를 모아 벡터 v 를 만든다 (φ_d > 0 항목만; 실제 distinction 만 카운트). Gini :

```
G  =  Σ_i Σ_j |v_i − v_j|  /  (2 · N · Σ v)
```

- N ≤ 1 또는 Σv = 0 시 G = 0 (convention; concentration contest 불가)
- G = 0 : 모든 distinction 이 동일 Φ-mass → 완전 균등 분포
- G → 1 : 한 distinction 이 Φ-mass 독점 → 완전 집중

Gini 공식은 **class-blind** : 입력은 오직 φ_d 벡터, 출력은 정의에 의한 스칼라. life/consciousness 라벨을 계산 어디서도 사용하지 않는다 → tautology 회피 (g73).

---

## 3. H1 — Φ-mass CONCENTRATION 이 class 를 가른다

**hypothesis** : n=4 ECA 패널에서 life class {30, 54, 110} 과 consciousness class {150, 105} 의 per-distinction φ_d Gini 가 체계적으로 분리된다.

방향은 양방향 admissible :
- **(a) consciousness > life** — XOR-feedback 통합 substrate 이 몇 개 대칭 distinction 에 Φ-mass 를 집중 ("binding" 우세)
- **(b) life > consciousness** — life substrate 이 분포를 fragment 하고 consciousness 가 대칭으로 spread

H_320 이 SUM 축에서 reverse 방향을 찾았으므로, SHAPE 축에서 어느 방향이든 separation 이 나오면 새 발견. 둘 다 안 나오면 SHAPE 축도 orthogonal — closed-negative 누적.

---

## 4. Pre-registered falsifiers (frozen 2026-05-27 측정 BEFORE)

- **F325.1 SEPARATION** : state 0101 에서 min(class_A Gini) > max(class_B Gini) 가 **(A,B) ∈ {(life,consc), (consc,life)}** 중 적어도 하나에서 strict (overlap 없음). 양방향 admissible — 어느 방향으로 separate 하든 SUPPORTED.
- **F325.2 ORDERING** : 전체 16 state 에 대한 class-mean Gini 가 strict separated 이고, **class-flip 없음** — 어떤 life substrate Gini 도 두 consc Gini 사이에 들어가지 않고 그 반대도 성립.
- **F325.3 FAITHFULNESS** : anchors (rule 204 identity · rule 0 constant) 가 ≤1 distinction 이고 Gini = 0 (대조군 sanity). AND 측정된 5 substrate 모두 Gini ∈ [0, 1] (정의역 sanity).

**Iron rule (g73)** : Gini 공식은 class-independent. `iit4_distinction.distinction()` 는 이 가설 이전 작성. 모든 falsifier 는 독립 계산된 값의 산술 비교. 🔴 CLOSED-NEGATIVE 결과는 valid finding — C2 축에 SHAPE 무관성 추가하여 H_320 family 의 closed-negative 자산을 확장한다.

---

## 5. 방법 — H_320 kernel 재사용 + 확장

| 단계 | 출처 | 행위 |
|---|---|---|
| substrate 패널 | H_320 동일 | life {110, 30, 54} + consc {150, 105} + anchor {204, 0} |
| φ_d 벡터 | `stdlib/consciousness/iit4_distinction.distinction()` | mech_mask 1..2^n−1, φ_d > 0 항목 collect |
| Gini | 본 run.hexa | 정의식 직접 계산 (closed-form) |
| headline state | 0101 (=5) | H_320 동일 |
| robustness | 16 state class-mean | F325.2 |

deterministic · hexa-only · $0 mac-local · LLM none · NO GPU. wall ≈ second.

⚠ **실행 환경 주의** : mac 부하 회피를 위해 ubu-2 에서 pool 경유 실행 (ubu-1 transpiler broken). 결정론 보장 → byte-identical across host.

---

## 6. 결과 — 실측 (2026-05-27, ubu-2 via pool)

### 6.1 per-distinction φ_d 벡터 @ state 0101

| substrate | N_d | φ_d vector | **Gini** |
|---|---|---|---|
| LIFE rule 110 | 10 | [0.166, 0.208, 0.415, 0.166, 0.491, 0.292, 0.208, 0.491, 0.415, 0.184] | **0.232658** |
| LIFE rule 30  | 10 | [0.439, 0.439, 0.439, 0.271, 0.208, 0.051, 0.439, 0.250, 0.138, 0.415] | **0.241641** |
| LIFE rule 54  | 10 | [0.439, 0.439, 0.415, 0.439, 0.415, 0.439, 0.415, 1.000, 0.415, 1.000] | **0.176340** |
| CONSC rule 150 | 5 | [0.5, 0.5, 0.5, 0.5, 1.0] | **0.133333** |
| CONSC rule 105 | 5 | [0.5, 0.5, 0.5, 0.5, 1.0] | **0.133333** |
| ANCHOR rule 204 | 4 | [1, 1, 1, 1] | 0.0 |
| ANCHOR rule 0   | 0 | [] | 0.0 |

핵심 관측 : **consc rule 150 / 105 가 동일 φ_d vector** [0.5×4, 1.0] 산출 — XOR-symmetry 정확 검증 (3-input XOR feedback isomorphism). life 는 diverse spread.

### 6.2 all-16-state class-mean Gini (F325.2 robustness)

| substrate | all-state mean Gini |
|---|---|
| LIFE rule 110 | 0.250135 |
| LIFE rule  30 | 0.186631 |
| LIFE rule  54 | 0.138498 |
| CONSC rule 150 | 0.133333 |
| CONSC rule 105 | 0.133333 |
| **life class mean** | **0.191754** |
| **consc class mean** | **0.133333** |
| ratio (life / consc) | **1.44×** |

**class-flip 없음** : 모든 consc rule 의 all-state-mean < 모든 life rule 의 all-state-mean (strict).

### 6.3 Falsifier 결과 (5 PASS / 1 FAIL)

- **F325.1 SEPARATION PASS** — life_min 0.17634 > consc_max 0.133333 (margin 0.04301, **LIFE > CONSC direction**)
- **F325.2 ORDERING PASS** — class-mean strict + no-flip 둘 다 성립 (LIFE > CONSC)
- **F325.3a FAITHFULNESS FAIL** (letter) — rule 204 N_d=4 (≤1 pre-reg 위반); intent 는 충족 (Gini=0 — 모든 φ_d=1.0, concentration contest 없음). honest 공시 (g73).
- **F325.3b FAITHFULNESS PASS** — rule 0 N_d=0, Gini=0
- **F325.3c BOUNDS PASS** — 모든 Gini ∈ [0, 1]
- **determinism PASS** — re-run byte-identical

---

## 7. Verdict — **🟢 SUPPORTED (with FAITHFULNESS letter caveat)**

**H1 SUPPORTED in LIFE > CONSC direction.** Φ-mass 분포 SHAPE 축은 small-n IIT4 scale 에서 life-class 와 consciousness-class 를 **separates** — strictly, no class-flip, 1.44× class-mean ratio.

### 해석
- life substrate (110/30/54) 는 Φ-mass 를 다양한 distinction 들에 **불균등 spread** (Gini 0.176–0.242) — fragmentation
- consc substrate (150/105) 는 Φ-mass 를 high-symmetry 소수 distinction 에 **균등 distribute** (Gini 0.133, identical) — symmetric uniformity
- 방향 : **H_320 의 reversed 방향과 일관** — 두 측정 모두 life > consc on Φ-structure richness

### H_320 / H_323 family 와의 통합

| H | 측정 축 | direction | tier |
|---|---|---|---|
| H_281 | struct_ratio = total/big-Φ | life > consc (above floor) | CLOSED |
| H_320 | rd_ratio = Σφ_r/Σφ_d (SUM) | life > consc (REVERSED H1) | 🔴 closed-negative |
| H_323 | nd-normalized rd_ratio | (H_320 family) | followup |
| **H_325** | **Gini of φ_d vec (SHAPE)** | **life > consc (LIFE direction)** | **🟢 SUPPORTED** |

C2 축은 **structure 가 있다** — but the structure runs OPPOSITE to the original IIT-intuition. small-n ECA scale 에서 life-themed substrate 이 **양 축** (SUM, SHAPE) 모두에서 더 풍부한 Φ-structure 를 carry 한다.

### F325.3a 의 honest 처리
사전등록 F325.3a 는 rule 204 가 ≤1 distinction 일 것이라 가정했으나, 실측 N_d=4 (각 cell 이 trivial single-cell self-distinction, all φ_d=1.0). Gini=0 (concentration contest 부재) 이라는 **의도** 는 충족되지만 **letter** 가 어긋남 — 보수적으로 FAIL 처리, g73 자기판정 금지 원칙. core 결론에 영향 없음 (F325.3a 는 anchor sanity, primary hypothesis 와 무관).

---

## 8. Honest scope

- n = 4 ring substrate, 5 ECA + 2 anchor — 작은 패널 (확률적 잡음 없음, 그러나 substrate diversity 제한)
- headline = single representative state 0101; F325.2 가 16-state class-mean robustness 추가
- Gini 는 SHAPE 의 **1 차원 metric** : entropy / variance / max-share 같은 alt SHAPE metric 은 따로 측정 필요 (orthogonal followup)
- ECA rule space 256 중 5 만 측정 — extension 은 더 큰 life/consc cohort 가 필요
- IIT 4.0 stdlib 의 distinction 정의에 binding — 다른 IIT version (3.0 등) 에서 다를 수 있음 (verify-fence)

---

## 9. 선행 / 후속 관계

**선행 (이미 닫힘)**
- H_281 : struct_ratio = total/big-Φ — consc 가 irreducibility floor (=1.0), life > 1.0. CLOSED.
- H_320 : rd_ratio = Σφ_r/Σφ_d — life > consc REVERSED. 🔴 CLOSED-NEGATIVE.
- H_323 : nd-normalized rd_ratio — H_320 follow-up.

**H_325 의 차별점** : H_320 family 가 SUM-축 만 다뤘다. H_325 는 SHAPE 축 — 같은 분포라도 다른 형태가 보일 가능성. SHAPE 도 orthogonal 이면 C2 closed-negative 가 더 굵게 묶임.

**후속 (둘 다 결과에 무관)**
- H_???-entropy : Gini 외 Shannon entropy of φ_d 분포
- H_???-max-share : max(φ_d) / Σφ_d 한 distinction 의 dominance
- H_???-rule-256 : 256 rule 전수 패널로 확장하여 statistical power 확보

---

## 10. 산출물

- `UNIVERSE/H_325_c2_phi_mass_shape_gini_2026_05_27.md` — 이 문서
- `UNIVERSE/state/h325_c2_phi_mass_shape_gini_2026_05_27/run.hexa` — REAL computation
- `UNIVERSE/state/h325_c2_phi_mass_shape_gini_2026_05_27/run.log` — stdout
- `UNIVERSE/state/h325_c2_phi_mass_shape_gini_2026_05_27/result.json` — per-distinction φ_d 벡터 + Gini per substrate + falsifier verdict
