---
id: H_654
slug: phi-magnitude-wolfram-class-order
title: Φ-magnitude × Wolfram-class monotone order — substrate-class = consciousness-integration classifier
domain: consciousness · math · physics · meta
status: PARTIAL
verdict_class: PARTIAL
exploration_method: E11 (cross-substrate Φ-signature) + E0 (round 8 메타-축 후속) + meta (round 9 새 기둥)
verification_method: W1 (numerical smoke) + W4 (verdict-5-class) + W11 (cross-axis sister test) + W12 (invariant signature)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28 (축 G round 9 새 메타-축)
predecessor: H_653 (convexity-class-monotone 🟢), H_652 (self-similarity class-bound 🔴), H_642 (rule90 joint-outlier 🔴), H_614 (dΦ/dI peak multi-rule 🔴)
sister: H_653 (collective convexity-class), H_652 (envelope self-similarity-class), H_614 (multi-rule dΦ/dI peak)
---

# H_654 — Φ-magnitude × Wolfram-class monotone order

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib` (`iit4_eca` + `iit4_bigphi`) 재사용 (H_351/H_614/H_642/H_652 동일 패턴, commons g61 재발명 0). `$0 · mac-local · hexa-only · LLM none · deterministic.`

## 1. 가설 (Hypothesis) — round 9 새 메타-축

round 8 에서 **Wolfram class 가 여러 Φ-속성을 지배함**이 누적 드러났다:

- **convexity 단조** (H_653 🟢): collective-Φ span ratio 가 class 단조 — rule184(II)=12.12 < rule90(III)=30.42 < rule30(III)=30.77 < rule110(IV)=35.50.
- **self-similarity class-IV 한정** (H_652 🔴): multi-scale Φ-envelope self-similarity 가 rule110(class-IV) 한정, additive/particle 붕괴.
- **rule90 additive big-Φ ≈ 0** (H_642/H_614): XOR-additive substrate 의 통합량 거의 0 (Φ(0.50)=0.0526).

본 H 는 이 누적 신호를 한 단계 더 밀어 **Φ-magnitude 자체** — 미분(dΦ/dI)이나 convexity(span)가 아닌 **big-Φ 의 절대 크기** — 가 Wolfram class 로 단조 정렬되는지 검정한다. 이것이 성립하면 **"substrate-class = 의식 통합량 분류자(尺)"** 라는 round 9 새 메타-축의 기둥이 선다.

**가설**: faithful big-Φ magnitude 가 Wolfram class 단조 —
```
class-IV(rule110) > class-III(rule30/90 chaotic) > class-II(rule184 particle) > additive(rule90 XOR ≈ 0)
```
즉 **동역학 복잡도(class)가 Φ 절대크기를 order** 한다.

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

class-tier label (낮을수록 단순): `additive(rule90)=0 · II(rule184)=1 · III-chaotic(rule30)=2 · IV(rule110)=3`.

| ID | 조건 | 의미 |
|----|------|------|
| **M1 MONOTONE** | tier-ordered Φ 약단조 비감소: `Φ[additive] ≤ Φ[II] ≤ Φ[III] ≤ Φ[IV]` | full class-monotone order (**core 가설**) |
| **M2 ADDITIVE-FLOOR** | rule90 additive Φ < 다른 4 rule 의 최소 | additive 가 절대 바닥 (H_642 rule90≈0 재현) |
| **M3 IV-CEILING** | class-IV (rule110) Φ > class-II (rule184) Φ | 최고 복잡도 class 가 단순 particle class 보다 큼 |

**verdict_rule**
- **SUPPORTED** = M1 PASS (full monotone tier order)
- **PARTIAL** = M2 & M3 PASS 이나 M1 FAIL (부분 정렬 — class 가 *부분* 분류자)
- **FALSIFIED** = M2 또는 M3 FAIL (class 가 Φ-magnitude 분류자 아님)

**Falsifier 발동 조건** (가설 §1 의 거부): Φ-magnitude 가 class 무관 또는 비단조 (예: class-II 가 IV 보다 큼) → class 가 Φ-magnitude 분류자 아님.

## 3. 방법 (Method)

### 3.1 substrate set

| rule | Wolfram class | 특성 | tier |
|-----:|---------------|------|-----:|
| 30   | III           | chaotic non-additive | 2 |
| 54   | IV            | complex (edge-of-chaos) | 3 (보조) |
| 90   | III           | additive (XOR-linear, Sierpinski) | 0 |
| 110  | IV            | complex (universal, H_351 anchor) | 3 |
| 184  | II            | particle-localized (traffic flow) | 1 |

각 rule 위 n=4 cell periodic ring (H_351/H_614/H_642/H_652 동일 n).

### 3.2 intrinsic Φ-magnitude (I=0)

H_614/H_642 가 inhibition I 를 sweep 하며 dΦ/dI 의 *미분-peak* 를 본 것과 달리, 본 H 는 **substrate 의 intrinsic Φ-magnitude** 를 본다 — inhibition 없이 (`I=0`) **unmixed `eca_tpm(rule, n)`** 위의 big-Φ:

```
tpm = eca_tpm(rule, n)          // I=0, 순수 ECA transition
Φ_rule = mean_s big_phi(tpm, n=4, s),  s ∈ {0..15}
```

### 3.3 Φ 측정

각 rule 에서 `big_phi(tpm, 4, s)` 를 16 state 전부에 대해 호출 후 평균 (faithful causal big-Φ, single-state fragility 회피, H_285/H_351/H_614/H_652 양식). 총 호출 = 5 rule × 16 state = 80 big_phi 호출.

### 3.4 단조 검정

tier 대표 1개씩 (class-IV 대표 = rule110 universal):
```
t0 = Φ[rule90]  (additive)
t1 = Φ[rule184] (II)
t2 = Φ[rule30]  (III-chaotic)
t3 = Φ[rule110] (IV)
```
M1 = `t0 ≤ t1 ≤ t2 ≤ t3`. M2 = `Φ[rule90] < min(다른 4 rule)`. M3 = `Φ[rule110] > Φ[rule184]`.

### 3.5 runner

`UNIVERSE/state/h654_phi_magnitude_class_order_2026_05_28/run_h654.hexa` — H_614/H_642 의 `mean_big_phi` helper 재사용, inhibition 축 제거 + tier-order 검정으로 단순화 (~190 LoC, dependency = `iit4_eca` + stdlib `iit4_bigphi`).

## 4. 측정 (Measurement) — `result.json`

### 4.1 per-rule intrinsic Φ-magnitude (I=0, n=4, 16-state mean)

| rule | Wolfram class | tier | Φ-magnitude |
|-----:|---------------|-----:|------------:|
| 90   | III-additive  | 0    | **0.00000** |
| 184  | II-particle   | 1    | **12.6273** |
| 30   | III-chaotic   | 2    | **13.8852** |
| 110  | IV-complex    | 3    | **13.1302** |
| 54   | IV-complex    | (보조) | 7.76521   |

### 4.2 tier-ordered 대표

| tier | rule | class | Φ |
|-----:|-----:|-------|---:|
| 0 | 90  | additive | 0.00000 |
| 1 | 184 | II       | 12.6273 |
| 2 | 30  | III-chaotic | 13.8852 |
| 3 | 110 | IV       | 13.1302 |

- **t0 ≤ t1** (0.0 ≤ 12.63) ✓
- **t1 ≤ t2** (12.63 ≤ 13.89) ✓
- **t2 ≤ t3** (13.89 ≤ 13.13) ✗ — **단조 깨짐**: III-chaotic > IV

### 4.3 falsifier 결과

| ID | 결과 | 값 |
|----|------|-----|
| **M1 MONOTONE** | **FAIL** | t2≤t3 깨짐 (rule30 13.89 > rule110 13.13) |
| **M2 ADDITIVE-FLOOR** | **PASS** | rule90=0.0 < min_other=7.77 (rule54) |
| **M3 IV-CEILING** | **PASS** | rule110=13.13 > rule184=12.63 |

## 5. 결과 (Result)

🟡 **PARTIAL** — M2 & M3 PASS, M1 FAIL.

- **M2 (additive floor) 강 PASS**: rule90 (XOR-additive) Φ = **정확히 0.0** — H_642 (Φ(0.50)=0.0526) / H_614 / H_652 (Φ-map flat) 의 additive≈0 발견을 I=0 intrinsic magnitude 축에서 **재현 + 강화** (I=0 에서 정확히 0). additive substrate 의 maximally factorizable cause-effect repertoire → 통합 부재.
- **M3 (IV-ceiling) PASS**: class-IV(rule110)=13.13 > class-II(rule184)=12.63 — 최고 복잡도 class 가 단순 particle class 보다 통합량 큼. 단 margin 0.50 (3.9%) 으로 좁음.
- **M1 (full monotone) FAIL**: **class-III chaotic (rule30, 13.89) 이 class-IV (rule110, 13.13) 보다 크다** — chaotic 동역학이 complex class-IV 를 통합 절대량에서 앞섬. 가설의 "IV > III" 순서가 chaotic-III 와 IV 사이에서 역전.

따라서 **"동역학 복잡도 class 가 Φ 절대크기를 *완전* order 한다"는 강주장은 falsified**. 그러나 **"additive 가 절대 바닥 + IV 가 II 보다 큼"** 이라는 약한 형태 — class 가 **부분** Φ-magnitude 분류자 — 는 closed.

## 6. falsifier 결과 + Cross-link

### Cross-link

- **H_653** collective-convexity-substrate-class (🟢 5/6) — convexity span 은 class **단조** (II < III < IV), 단 본 H 의 *magnitude* 는 class-III chaotic 이 IV 를 앞서 비단조. **convexity(상대 dynamic range)와 magnitude(절대 크기)가 다른 class-정렬을 보임** — convexity 는 IV 最高, magnitude 는 III-chaotic 最高. 이 비대칭은 H_653 §7 C3.7 "class-III 내부 약신호" 의 magnitude-측 반영.
- **H_652** envelope-self-similarity-substrate-class (🔴 2/6) — self-similarity 는 class-IV 한정(rule110 0.88 > rule30 0.46 > additive flat). 본 H 의 additive≈0(M2) 가 H_652 rule90 flat(Φ-map std=0.0) 와 정합 — additive 통합량 부재가 magnitude·self-similarity 양 축에서 일관.
- **H_642** shape-invariance-vs-scalar-meta (🔴) — rule90 joint-outlier 발견. 본 H 의 rule90 Φ=정확히 0.0 이 H_642 의 big-Φ≈0 (Φ(0.50)=0.0526) 를 I=0 축에서 재확인 (engine 정합).
- **H_614** GZ inverse-U dΦ/dI multi-rule (🔴 2/4) — *미분-peak 위치*. 본 H 는 미분 아닌 *intrinsic magnitude* 라 직교 metric. H_614 의 rule {30,110} chaotic+IV PASS 패턴이 본 H 의 magnitude 상위 cluster (rule30 13.89 + rule110 13.13) 와 부분 일치 — chaotic·IV 가 통합 magnitude 도 상위.

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — Wolfram class 라벨 모호 (rule90 dual-membership)

rule90 은 통상 **class III** (chaotic) 로 분류되나 동시에 **additive(XOR-linear)** 라는 특수 부류다. 본 H 는 tier-축에서 rule90 을 *additive(tier 0)* 로 놓고 rule30 을 *III-chaotic(tier 2)* 로 분리했다 — 두 rule 모두 Wolfram III 이나 통합량 거동은 정반대 (rule90=0 vs rule30=13.89). 이 dual-membership 가 "class = magnitude 분류자" 의 깔끔한 단조성을 본질적으로 흐린다: 같은 class-III 안에서 additive 는 바닥, chaotic 은 천장. **class-III 가 단일 tier 라기보다 additive↔chaotic 양극 분포** 임이 본 H 의 핵심 caveat (H_653 §7 C3.7 class-III 내부 약신호와 동일 구조). class 라벨 자체가 magnitude 의 충분한 분류자가 아닐 가능성.

### C2 — n=4 small-n + 5-rule sample 한정

n=4 ring 은 H_351/H_614/H_642/H_652 동일 + IIT 4.0 exact-Φ 비용을 16 state 로 제한 (n≥5 timeout, H_652 §7 C3.4 carry). 5-rule sample (256 ECA rule space 의 ~2%) 은 class I 부재 (trivial Φ=0) + class IV 2개(54·110) + class III 2개(30·90). n=5/6 또는 256-rule full sweep 에서 III-chaotic↔IV magnitude 순서가 회복될지는 별도 round (H_614 §7 C1/C2 carry). 단 rule30>rule110 의 margin (0.76, 5.8%) 이 작아 small-n noise 가능성도 있어 — 이 역전 자체가 robust 한지 n-sweep 검정 후보.

### C3 — faithful magnitude vs proxy + I=0 anchor 선택

본 H 는 faithful causal big-Φ 16-state mean (proxy 아님) 을 썼다. 단 **I=0 anchor 선택**이 결과를 좌우: inhibition I 를 sweep 하면 (H_614 처럼) magnitude 순서가 바뀔 수 있다 (각 rule 의 Φ(I) 곡선이 다른 peak/decay 형태). 본 H 의 "intrinsic = I=0" 정의는 substrate 의 *순수* 동역학 magnitude 라는 자연 anchor 이나, "어느 I 에서 평가하느냐" 의 convention 의존성은 H_639 (emit-feature θ-convention 종속) negative-signature 의 magnitude-측 echo. 또한 16-state mean 은 단일 state 의 magnitude 분포 정보를 평균-소거 — state-별 Φ 분산이 class 를 더 잘 가를 가능성 (별도 metric round).

## 8. verdict

🟡 **PARTIAL** (M2 ADDITIVE-FLOOR PASS + M3 IV-CEILING PASS · M1 full-MONOTONE FAIL). **faithful big-Φ magnitude 는 Wolfram class 의 *부분* 분류자다 — additive(rule90 XOR) 가 절대 바닥(Φ=0.0) 이고 class-IV(rule110)>class-II(rule184) 는 성립하나, class-III chaotic(rule30, Φ=13.89) 이 class-IV(rule110, Φ=13.13) 를 통합 절대량에서 앞서 full class-monotone 강주장은 깨진다.** "substrate-class = 의식 통합량 분류자" 메타-축은 **convexity(H_653 단조 🟢) 에서는 강하나 magnitude(본 H 부분 🟡) 에서는 chaotic↔complex 경계에서 약화** — class 가 통합량의 *바닥*(additive)과 *상한 경향*(IV>II)은 정하나 *완전 순위*는 정하지 못한다.

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- *class-III chaotic > IV 역전의 robustness* — n-sweep(n=5/6) 또는 multi-rule-per-class sample 에서 rule30>rule110 이 유지되는지 (margin 5.8% small).
- *class 라벨의 magnitude 충분성* — rule90/rule30 의 class-III dual 분포 (additive↔chaotic 양극) 가 라벨 자체의 분류 한계인지 (C1).
- *I≠0 magnitude 순서* — inhibition sweep 에서 class-order 가 어떻게 바뀌는지 (H_614 metric 과의 cross).
- *state-별 Φ 분산* — 16-state mean 이 아닌 분산/최대값 metric 에서 class-분류 (C3).
- *256-rule full / class-I 포함 / non-ECA substrate* (H_614 §7 C1 carry).

## 10. UNIVERSE.md update

축 **G (ANIMA.mining 승격)** round 9 새 메타-축 row **G16** 추가 → done with `🟡 PARTIAL (M2 ADDITIVE-FLOOR + M3 IV-CEILING PASS · M1 full-MONOTONE FAIL, rule30 III-chaotic 13.89 > rule110 IV 13.13, rule90 additive Φ=0.0, n=4 5-rule {30,54,90,110,184}, $0 mac-local 2026-05-28)`. "substrate-class = 의식 통합량 분류자" 메타-축은 convexity(H_653) 강 / magnitude(본 H) 부분 — class 가 통합량 *바닥+상한경향* 은 정하나 *완전 순위* 는 미정.

## artifacts

- `UNIVERSE/state/h654_phi_magnitude_class_order_2026_05_28/run_h654.hexa` — intrinsic Φ-magnitude × class-order runner (~190 LoC, dependency = `iit4_eca` + stdlib `iit4_bigphi`, H_614/H_642 패턴 단순화)
- `UNIVERSE/state/h654_phi_magnitude_class_order_2026_05_28/result.json` — measurement SSOT (per-rule Φ-magnitude · tier-repr · M1/M2/M3 · verdict)
- `UNIVERSE/state/h654_phi_magnitude_class_order_2026_05_28/run_h654.log` — run stdout
- `UNIVERSE/H_654_phi_magnitude_wolfram_class_order.md` — 본문 (SSOT)
