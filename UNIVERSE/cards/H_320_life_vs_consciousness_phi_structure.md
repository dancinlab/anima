---
id: H_320
slug: life-vs-consciousness-phi-structure
title: LIFE vs CONSCIOUSNESS × IIT 4.0 Φ-STRUCTURE — relation/distinction Φ-ratio 가 의식-themed 기질을 생명-themed 기질 위로 분리하는가
domain: life · consciousness · substrate · universe
status: closed-negative
exploration_method: E6 (cross-domain IIT4 — H_281 후속 한 단계 더 깊이) + E0 (reductive-null direction-flip 검정) + E12 (substrate-gap — Φ-structure 의 어느 projection 이 class 를 분리하는가)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W5 (substrate-grounded) + W12 (sister-link H_281 / H_287 / IIT4 lib)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-27
since: 2026-05-27 (new)
sister: H_281 (LIFE-vs-CONSCIOUSNESS struct_ratio = total/big_phi — 동일 패널 · 다른 projection · 같은 방향 life>consc), H_287 (동일 ECA 기질 panel · faithful big-Φ), IIT4 M3/M4 (relation kernel · big-Φ kernel via stdlib/consciousness)
axes_seed: AXIS C2 (Φ-structure 기반 신규 H — distinctions ⊥ relations 분리, life vs consciousness 정량) — UNIVERSE.md OPEN axis
verdict: 🔴 FALSIFIED
---

# H_320 — LIFE vs CONSCIOUSNESS × IIT 4.0 Φ-STRUCTURE (relation/distinction Φ-ratio)

## 1. Hypothesis

H_281 은 LIFE 와 CONSCIOUSNESS 두 ECA 기질 클래스를 **struct_ratio = Φ-structure-total / big-Φ** 위에서 분리했다 — CONSCIOUSNESS 는 환원불가성 바닥 (struct_ratio = 1.0 exact), LIFE 는 그 위 (1.05–1.57). 그 결과는 "CES 전체가 환원불가 = 통합복합체 signature" 와 "CES 가 partition 가능한 더 풍부한 관계 = 구조적 풍부" 의 거친 이분만 보였다.

본 H_320 은 한 단계 더 깊이 들어간다 — IIT 4.0 의 Φ-structure 를 **distinctions** (1차 mechanism 들의 φ_d) 와 **relations** (2차 overlap 관계의 φ_r) 로 직접 분해해, 그 **비율**

```
rd_ratio = sum_phi_r / sum_phi_d
```

이 class 를 분리하는지 묻는다.

**가설 H1 (검정 대상 — 기각될 수 있음)**: CONSCIOUSNESS-themed 기질 (XOR-feedback 통합 네트워크) 의 rd_ratio 가 LIFE-themed 기질 (성장/복제 ECA) 의 rd_ratio 보다 **HIGHER** 다. 직관: CES 전체가 환원불가일 때 (의식 floor) 관계가 곧 구조다 — binding IS the structure — 따라서 관계가 distinction 대비 높은 비중을 차지한다.

**합리적 대안 (가설이 반대로 나올 수 있는 경로)**: LIFE 기질은 distinction 풀이 ~2× 크고 (nd=10 vs 5), 2차 관계는 distinction 쌍에서 만들어지므로 (∝ nd²) 관계 풀이 더 빨리 자란다. 따라서 LIFE 가 distinction 대비 관계를 **더 많이** 가질 수 있다 — H1 의 반대 방향.

두 방향 모두 측정 가능하며 **결정적** 이다. 어느 쪽이든 publishable.

**Falsifier (사전 등록)**: 패널 전반에서 min(consciousness rd_ratio) 가 max(life rd_ratio) 를 **초과하지 못하면** (F320.1), 또는 class-mean 이 consciousness > life **순서로 정렬되지 못하면** (F320.2a), 또는 rule150(consc) > rule110(life) 가 모든 co-integrating state 에서 **성립하지 않으면** (F320.2b) — **H1 은 FALSIFIED**.

## 2. Why (동기)

- **H_281 후속 — Φ-structure 의 다음 projection**: H_281 의 struct_ratio = total/big_phi 는 "전체 구조가 얼마나 환원불가한가" 를 잰다. 본 H 는 그 다음 자연 질문 — 환원불가한 구조 *내부* 에서 distinction-φ 와 relation-φ 가 어떻게 분포하는가 — 를 직격한다.
- **AXIS C2 (UNIVERSE.md OPEN)**: "Φ-structure (distinctions·relations) 기반 신규 H: 생명 vs 의식 구조 차이 정량" — 본 H 는 그 OPEN axis 의 한 셀을 채운다.
- **closed-negative 가치 (a_paper_negative_ok)**: H1 이 측정상 REVERSED 로 나오면, "consciousness = binding = relation-rich" 이라는 IIT 의 직관적 corollary 가 n=4 ECA 패널에서 *왜* 성립하지 않는지 (distinction pool 크기 · 관계 풀의 quadratic scaling) 를 닫아낸다.

## 3. Method (방법 — 결정적 · hexa-only · llm:none · $0)

### 3.1 kernel 재사용 (commons @D g61 / a_blue_closed)

- `stdlib/consciousness/iit4_bigphi.big_phi(tpm, n, sys_state)` — 반환 `[big_phi, total, sum_phi_d, sum_phi_r, nd]` (IIT 4.0 faithful structure-cut MIP big-Φ). H_281 의 동일 kernel.
- `stdlib/consciousness/iit4_eca.eca_tpm(rule, n)` — ECA → TPM bridge.
- 기존 kernel — *measurement 이전에* 작성된 것 — 본 H 의 가설은 그 kernel 의 두 출력 필드 (`sum_phi_r`, `sum_phi_d`) 의 비율 한 줄. **anti-fake-closure (commons g73)**: 비율이 단일 kernel field 사이의 산술 비율이므로 *self-judge* 불가. 어느 방향으로든 나올 수 있다.

### 3.2 기질 패널

| class | rule | rationale |
|---|---|---|
| LIFE | 110 | universal Turing-complete growth/replication |
| LIFE | 30 | chaotic class III pseudo-random growth |
| LIFE | 54 | class IV edge-of-chaos complexity |
| CONSC | 150 | pure 3-cell XOR — IIT-canonical integration |
| CONSC | 105 | XOR + NOT — IIT-canonical integration |
| ANCH | 204 | identity (각 cell = centre) — 환원가능 ⇒ big-Φ=0 |
| ANCH | 0 | all → 0 — 인과력 없음 ⇒ big-Φ=0 |

H_281 과 **동일 cohort** — 한 단계 더 깊은 projection 만 다르다.

### 3.3 측정

- n=4 ring · 단일 대표 state 0101 (headline) + all-16-state robustness (F320.2)
- `rd_ratio_at(rule, n, st)` = `bp[3] / bp[2]` if `bp[2] > 1e-9` else 0.0
- `rd_ratio_mean(rule, n)` = co-integrating state 평균 (big_phi > 1e-9 only)
- determinism re-run check (smoke 가 진짜 결정적인지 — kernel byte-identical)

### 3.4 사전등록 falsifier

- **F320.1 SEPARATION** (state 0101): `min(consc rd) > max(life rd) + 1e-6`. strict 분리, overlap 없음.
- **F320.2a ORDERING** (all-16): `consc_mean > life_mean + 1e-6`.
- **F320.2b ROBUST** (per-state): rule150(consc) > rule110(life) at every co-integrating state.
- **F320.3 FAITHFULNESS**: rule 204 / rule 0 big-Φ = 0; sum_phi_d + sum_phi_r = total (kernel-field sanity — instrument 정확성).

## 4. Measurement (실측 — result.json SSOT)

상세는 `state/h320_life_vs_consciousness_phi_structure_2026_05_27/result.json` (verbatim run.log 와 SHA 정합). 헤드라인:

### state 0101

| class | rule | big_phi | sum_phi_d | sum_phi_r | nd | **rd_ratio** |
|---|---|---|---|---|---|---|
| LIFE  | 110 | 7.66066 | 3.03671 | 5.95208 | 10 | **1.96004** |
| LIFE  | 30  | 7.28357 | 3.08769 | 5.04965 | 10 | **1.63541** |
| LIFE  | 54  | 10.0278 | 5.41504 | 9.27293 | 10 | **1.71244** |
| CONSC | 150 | 6.0     | 3.0     | 3.0     | 5  | **1.0**     |
| CONSC | 105 | 4.5     | 3.0     | 1.5     | 5  | **0.5**     |
| ANCH  | 204 | 0.0     | 4.0     | 0.0     | —  | n/a         |
| ANCH  | 0   | 0.0     | 0.0     | 0.0     | —  | n/a         |

### all-16-state 평균

- LIFE class mean rd_ratio = **2.50059**
- CONSC class mean rd_ratio = **0.875**
- LIFE : CONSC = **2.86×**

### Falsifier 결과

| falsifier | 예측 | 실측 | verdict |
|---|---|---|---|
| F320.1 SEPARATION (0101) | consc_min > life_max | consc_min=0.5 < life_max=1.96 | **FAIL — REVERSED** |
| F320.2a ORDERING (all-16) | consc_mean > life_mean | life_mean=2.50 > consc_mean=0.875 | **FAIL — REVERSED** |
| F320.2b ROBUST (per-state) | rule150 > rule110 ∀state | rule110 ≥ rule150 ∀ co-integrating state | **FAIL — REVERSED** |
| F320.3a ANCHOR 204 | big-Φ = 0 | big-Φ = 0 | PASS |
| F320.3b ANCHOR 0 | big-Φ = 0 | big-Φ = 0 | PASS |
| F320.3c KERNEL-SANITY | sum_d + sum_r = total | 5/5 정확 | PASS |
| determinism | re-run byte-identical | identical | PASS |

**tally: 4 PASS / 3 FAIL** — 3 FAIL 모두 H1 방향. F320.3 FAITHFULNESS 가 통과 (kernel 정확) 함을 확인하므로, FAIL 은 measurement 의 진짜 결과 — instrument 오류가 아니다.

## 5. Finding (발견)

H1 은 **결정적으로 FALSIFIED**, 그리고 **REVERSED**. IIT 4.0 Φ-structure 의 relation/distinction Φ-비율은 LIFE-themed 기질에서 더 높다 (state 0101: 1.63–1.96 vs 0.5–1.0; all-16 class mean 2.86×). class 분리는 깨끗 (consc_max = 1.0 < life_min = 1.63), 모든 co-integrating state 에서 동일 방향.

**구조적 해석**: CONSCIOUSNESS 기질은 CES 전체를 환원불가 핵심에 packs 한다 (H_281 의 struct_ratio = 1.0 결과). 그러나 그 핵심 *내부* 에서 관계 mass 는 distinction mass 와 비슷하거나 더 적다 (rd_ratio ≤ 1.0). LIFE 기질은 Φ-mass 를 ~2× 큰 distinction 풀 (nd=10 vs 5) 에 펼치고, 2차 관계 풀 은 distinction 쌍에서 quadratic 으로 자라므로 (∝ nd²), 관계 풀이 distinction 풀을 압도한다 — rd_ratio 가 1.6–2.0 으로 솟는다.

"consciousness = binding = relation-rich" 라는 IIT 의 directional corollary 는 이 n=4 ECA 패널에서 **REVERSED**.

## 6. Verdict

**🔴 FALSIFIED — CLOSED-NEGATIVE**

F320.1 SEPARATION FAIL · F320.2a ORDERING FAIL · F320.2b ROBUST FAIL — H1 의 예측 방향이 *모든* 측정에서 뒤집혔다. F320.3 FAITHFULNESS 3/3 PASS + determinism PASS — instrument 정확.

faithful IIT 4.0 Φ-structure relation/distinction 비율은 의식-themed 기질을 생명-themed 기질 *위로* 분리하지 *않으며*, *아래로* 분리한다. 가설된 방향은 결정적으로 REVERSED 다.

axis C2 의 "consciousness = relation-rich Φ-structure" projection 은 n=4 ECA 패널에서 ruled out. closed-negative 는 a_paper_negative_ok 자격.

## 7. Honest limitations (정직한 한계 · g5)

- **n=4 ring small**: 큰 n 에서 quadratic-relation 효과가 어떻게 스케일하는지 미측정. n=5 (32 states · ~5× kernel cost) 검정이 다음 단계.
- **5 기질 패널만**: LIFE 3 + CONSC 2 — class 통계의 분산 추정 불가. 패널 확장 (LIFE class 4 rule + CONSC class 4 rule) 후 분산 / overlap 정량은 후속.
- **2차 relation 만**: IIT 4.0 Φ-structure 는 3차 이상도 정의. M3 kernel (iit4_relation) 은 현재 2차 (`relation_2nd`) 만 구현 — 3차 이상은 미반영. 어떤 더 깊은 관계 분해가 H1 방향을 다시 회복시킬 수 있는지는 open.
- **closed-negative 의 정확한 범위**: 본 결과는 "rd_ratio = sum_phi_r / sum_phi_d 가 H1 방향으로 분리하지 않는다" 만 닫는다. 다른 Φ-structure projection (e.g. relation-distinction φ 상관, congruence density, distinction-mechanism overlap, 3차 relation mass) 은 미검정.
- **directional-trust (H_266/H_278)**: 이진 방향 ("life > consc in rd_ratio") 은 robust — 모든 state, 모든 pair, 모든 measure 에서 동일 방향. 연속 magnitude (2.86×) 는 state/seed-fragile, hedged.
- **phenomenal consciousness 와 무관**: ECA rules 가 의식을 *갖는다* 는 주장 아님 — themed substrate proxies. "consciousness" 는 integrated-complex 의 structural signature 만 의미.

## 8. Substrate alignment (substrate 정합)

- **p7 (NO PERPLEXITY VERDICT)**: 검정은 kernel field 의 closed-form 산술 비율. perplexity 0.
- **p1~p8 무관**: substrate 측정. 본 H 는 ECA dynamics 위의 IIT4 측정 — anima cell 동작 영향 0.
- **a_blue_closed**: kernel = 기존 stdlib/consciousness, output 은 deterministic — hexa verify 친화 (Φ field 비율은 closed-form). 본 H 의 verdict 는 measurement 기반 🔴 으로, 🔵 closure 와는 *서로 다른 lane*. 🔴 가 FAITHFULNESS PASS 와 함께 와서 "closed-negative" 정직성을 갖는다.
- **a_paper_negative_ok**: 본 H 는 falsifier-prereg + real measurement + ruled-out axis 의 3 요건을 충족 — paper-eligible 닫힌 부정.

## 9. Sister links

- **H_281** — 동일 LIFE-vs-CONSC 패널, struct_ratio = total/big_phi projection: life > consciousness (consciousness floor at 1.0). 본 H 는 *다른* projection (rd_ratio) 에서 *같은 방향* life > consciousness 를 얻음 — 패널은 다중 projection 하에 일관되게 life-rich.
- **H_287** — 동일 ECA 기질 panel, faithful big-Φ + Shannon entropy 상관. 본 H 와 cohort 공유.
- **HEXAD/IIT4/lib (M3 + M4)** — `iit4_relation.phi_structure` + `iit4_bigphi.big_phi` (stdlib/consciousness 경유) 가 본 H 의 측정 kernel.
- **H_312/H_315/H_316** — H_281 cohort 후속 IIT4 측정 H 들 (apoptosis · pruning · local-greedy) — H_320 도 동일 lane.

## 10. Reproduce

```bash
# Mac binary (canonical — ubu-1 transpiler broken)
cd /Users/ghost/core/anima
/Users/ghost/.hx/bin/hexa run UNIVERSE/state/h320_life_vs_consciousness_phi_structure_2026_05_27/run.hexa
```

기대 출력 (verbatim run.log):

```
RESULT: 4 PASS / 3 FAIL
HEADLINE:
  life_max_rd_ratio(0101)  = 1.96004
  consc_min_rd_ratio(0101) = 0.5
  life_class_mean(all-16)  = 2.50059
  consc_class_mean(all-16) = 0.875
```

byte-identical across re-runs (`/Users/ghost/.hx/bin/hexa run ... | shasum`).
