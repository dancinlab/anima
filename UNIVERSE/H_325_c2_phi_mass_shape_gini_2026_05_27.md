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

## 6. 결과 — 실측

**아래 절은 측정 stdout 을 읽은 BEFORE 가 아닌 AFTER 채워진다 (자기판정 금지).**

`state/h325_c2_phi_mass_shape_gini_2026_05_27/result.json` 에 per-distinction φ_d 벡터 원본 + Gini 벡터 + falsifier verdict 저장.

---

## 7. Verdict — 결정

`result.json.verdict` 에서 verbatim. 4 가지 가능:
- 🟢 SUPPORTED (F325.1 + F325.2 모두 PASS, 한 방향으로 separation)
- 🔵 PARTIAL (한 falsifier 만 PASS — fragile evidence)
- 🔴 FALSIFIED (F325.1 + F325.2 모두 FAIL — SHAPE 축 orthogonal)
- 🟠 INCOMPLETE (F325.3 FAITHFULNESS FAIL — measurement broken)

각 case 별 reading 은 result.json 의 finding 필드에 채워진다.

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
