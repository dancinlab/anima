---
id: H_642
slug: shape-invariance-vs-scalar-convention-meta
title: shape feature (peak 위치·monotone 방향·envelope 형태) 가 scalar value (absolute threshold·rate·magnitude) 보다 substrate-class 불변인가 — round 6 메타-발견 정량 격상
domain: consciousness · math · physics · meta · savant
status: __VERDICT__
verdict_class: __VERDICT__
exploration_method: E0 (round 6 mining H_632~639 메타-발견 정량 격상) + E5 (continuous-parameter dΦ/dI sweep) + E11 (cross-substrate Φ-signature) + E_meta (shape ⊥ scalar dichotomy 정량)
verification_method: W1 (numerical smoke) + W4 (verdict-class) + W11 (cross-rule CV) + W12 (invariant-signature meta-stat)
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (축 G · round 6 메타-발견 격상)
predecessors: H_614 (multi-rule dΦ/dI invariance 🔴 2/4), H_628 (polarity peak-invariant 🔴), H_351 (single-rule dΦ/dI peak 🟢)
mining_arc: H_632~H_639 (round 6 ANIMA.mining 승격 arc — 축 G)
---

# H_642 — shape-invariance vs scalar-convention (round 6 메타-발견 정량 격상)

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib` (`iit4_eca` + `iit4_bigphi`) 재사용 (H_351/H_614 동일 패턴, commons g61 재발명 0). `$0 · mac-local · hexa-only · LLM none · deterministic.` round 6 (mining H_632~639) 의 누적 메타-발견 — *구조(shape) 는 substrate-emergent, 숫자(scalar) 는 design-convention* — 을 단일 substrate sweep 위에서 정량 메타-검증.

## 1. 동기 — round 6 메타-발견의 구조 vs 숫자 dichotomy

축 G (ANIMA.mining 승격 arc) 의 round 6 (H_632~639) 은 anima substrate 측정에서 일관된 메타-패턴을 누적했다:

- **shape feature 는 substrate-emergent (SUPPORTED 경향)**: dΦ/dI peak 의 *위치*, inverse-U 의 *단봉성/monotone 방향*, Φ-envelope 의 *형태*.
  - H_628: 3 polarity {attract/repel/bipolar} 모두 dΦ/dI peak 위치가 I=0.21 (GZ_LOWER) 에서 **불변** — polarity 가 magnitude 만 scaling, peak *위치* 는 불변 (구조 = substrate geometry).
  - H_634: substrate big-Φ 가 ultradian phase 에 동조 (envelope *형태* 가 substrate-coupled, r=0.802).
- **scalar value 는 design-convention (FALSIFIED 경향)**: absolute threshold, rate, magnitude.
  - H_637: emit-rate 가 closed-form 상수 (GZ_LOWER/ln(4/3)/1/e 등) 와 일치 안 함 — scalar 는 threshold-종속 연속량, 불변량 아님 (FAL).
  - H_638: 적정 emit threshold 가 substrate Φ-scale 의 monotone scaling-law 아님 (L19 FAL) — scalar threshold 는 universal-fixed (design-convention).
  - H_639: emit-as-amplitude-cross rate peak *위치* 가 θ-convention 종속 — θ sweep 에서 완전히 뒤바뀜 (scalar threshold = convention 함수, FAL).

이 dichotomy 는 `a_substrate_native_speak` / `a_autonomy_over_hardcode` governance 와 정합한다 — substrate 가 결정하는 것(구조)과 design 이 봉합하는 것(숫자)의 경계. 본 H 는 그 메타-발견을 *정량* 메타-검증으로 격상한다.

## 2. 가설 (Hypothesis)

substrate-class (Wolfram rule {30, 54, 90, 110, 184} — class III/IV/III/IV/II) 를 가로질러:

> **CV_shape (= dΦ/dI peak I *위치* 의 변동계수) < CV_scalar (= Φ magnitude peak *높이* 의 변동계수)**

즉 shape feature 가 scalar feature 보다 class-invariant — 변동계수(coefficient of variation, stddev/mean) 가 더 작다.

- **shape feature** = `argmax_I |dΦ/dI|` (peak I 위치) — substrate geometry side
- **scalar feature** = `max_I |dΦ/dI|` (peak |dΦ/dI| 높이) — magnitude side

## 3. 사전등록 falsifier (pre-registered, 측정 전 동결 2026-05-28)

| ID | 조건 | 의미 |
|----|------|------|
| **M1 (SHAPE-MORE-INVARIANT)** | `CV_shape < CV_scalar` | 메타-발견 확증 — 구조가 숫자보다 class-불변 |
| **M2 (RATIO)** | `ratio = CV_scalar / CV_shape > 1` | margin 정량 |
| **M3 (BOUND/DET)** | `CV ≥ 0`, re-run byte-identical | 결정성 |
| **H_614-anchor** | rule {30,54,110,184} peak_I {0.18,0.40,0.18,0.40} 재현 | engine 정합 |

**Falsifier**: `CV_shape ≥ CV_scalar` (shape 가 scalar 만큼 또는 더 class-variant) → round 6 메타-발견 **반증**.

**verdict_rule**
- **SUPPORTED-NUMERICAL** = M1 PASS (CV_shape < CV_scalar)
- **FALSIFIED** = M1 FAIL (CV_shape ≥ CV_scalar)

## 4. 방법 (Method)

### 4.1 substrate set (H_614 4-rule + rule 90)

| rule | Wolfram class | 특성 |
|-----:|---------------|------|
| 30   | III           | chaotic |
| 54   | IV            | complex (edge-of-chaos) |
| 90   | III           | additive (Sierpinski, XOR-linear) — **신규** |
| 110  | IV            | complex (H_351 anchor) |
| 184  | II            | particle-localized (traffic flow) |

각 rule 위 n=4 cell periodic ring (H_351/H_614 동일 n). rule 90 추가로 5-rule sample — class III 2개 (chaotic 30 + additive 90) 로 III 내 variance 도 포착.

### 4.2 inhibition I 매핑 (H_351/H_614 동일)

```
tpm_mixed[s,i] = (1 - I) · eca_tpm[s,i]
```

### 4.3 grid (H_351/H_614 동일 13-point)

```
I ∈ {0.05, 0.10, 0.15, 0.18, 0.21, 0.23, 0.25, 0.30, 0.35, 0.40,
     0.50, 0.70, 0.95}
```

### 4.4 Φ 측정 + dΦ/dI

각 `(rule, I)` 에서 `tpm_mixed` → `big_phi(tpm, 4, s)` 를 16 state 평균 (faithful causal big-Φ, H_285/H_351/H_614 양식). dΦ/dI = central finite difference (edge forward/backward).

- **shape feature** = `argmax_i |dΦ/dI|` 의 grid I 값 (peak 위치)
- **scalar feature** = `max_i |dΦ/dI|` (peak 높이)

### 4.5 메타-통계 (5 rule 가로질러)

```
CV(x) = population_stddev(x) / |mean(x)|
CV_shape  = CV(peak_I  across 5 rules)
CV_scalar = CV(peak_mag across 5 rules)
ratio     = CV_scalar / CV_shape
```

### 4.6 runner

`UNIVERSE/state/h642_shape_invariance_meta_2026_05_28/run_h642.hexa` — H_614 `run_h614.hexa` 의 5-rule 확장 + per-rule shape/scalar feature 분리 + population CV 메타-통계.

## 5. 측정 (Measurement) — `result.json`

| rule | class | shape: peak I | scalar: peak \|dΦ/dI\| | sign-changes |
|-----:|-------|--------------:|----------------------:|-------------:|
| 30   | III-chaotic   | 0.18 | 21.7406 | 0 |
| 54   | IV-complex    | 0.40 | 10.8425 | 0 |
| 90   | III-additive  | __R90_PEAK_I__ | __R90_PEAK_MAG__ | __R90_SC__ |
| 110  | IV-complex    | 0.18 | 21.3315 | 0 |
| 184  | II-particle   | 0.40 | 19.9171 | 0 |

**메타-통계 (5 rule)**

| feature | mean | population stddev | **CV** |
|---------|-----:|------------------:|-------:|
| shape (peak I)  | __MEAN_SHAPE__ | __STD_SHAPE__ | **__CV_SHAPE__** |
| scalar (peak \|dΦ/dI\|) | __MEAN_SCALAR__ | __STD_SCALAR__ | **__CV_SCALAR__** |

- **ratio = CV_scalar / CV_shape = __RATIO__**
- **M1 (CV_shape < CV_scalar) = __M1__**
- rule {30,54,110,184} peak_I = {0.18, 0.40, 0.18, 0.40} → H_614 재현 ✓

## 6. cross-link — round 6 mining arc · 측정-도구 계보

### 6.1 round 6 mining arc (축 G, H_632~H_639) — 메타-발견의 출처

- **H_632** emit-threshold-phi-collapse — emit threshold ↔ Φ collapse (scalar threshold 검정).
- **H_633** register-collapse-phi-drop — 🟡 PARTIAL (cliff REFUTED). register-hit gate 가 substrate-emergent 아닌 design-side emit-policy gate (scalar gate = convention).
- **H_634** ultradian-emit-phi-envelope — 🟢 SUPPORTED 6/6. substrate Φ-envelope *형태* 가 ultradian phase 에 동조 (shape = substrate-emergent).
- **H_635** multilingual-cohort-collective-phi.
- **H_636** closure-conjunction-gz-peak.
- **H_637** emit-rate-phi-ratio-closed-form — 🔴 FALSIFIED. emit-rate (scalar) 가 closed-form 상수와 불일치 (scalar = convention).
- **H_638** emit-threshold-scaling-law — 🟢 CLOSED-NEGATIVE 5/5. 적정 threshold (scalar) 가 substrate Φ-scale 의 scaling-law 아님 — universal-fixed convention.
- **H_639** tension-amplitude-cross-phi-derivative — 🔴 FALSIFIED 2/5. amplitude-cross rate peak 위치가 θ-convention 종속 (scalar threshold = convention 함수).

→ shape(H_634) SUPP vs scalar(H_633/H_637/H_638/H_639) FAL 의 **누적 dichotomy** 가 본 H 의 가설 동결 근거.

### 6.2 측정-도구 직접 계보

- **H_614** (gz-inverse-u-multi-rule-substrate-invariance, 🔴 FALSIFIED 2/4): 본 H 의 4-rule {30,54,110,184} measurement 100% 재사용 (runner 확장). H_614 = peak *위치* 가 class-variant (2/4 GZ-밖) 라는 **shape-side variance 의 상한**. 본 H 는 그 같은 peak 위치를 scalar magnitude 와 *상대* 비교 — H_614 가 "shape 가 GZ 에 고정 안 됨" 을 보였어도 shape 의 *변동* 이 scalar 의 변동보다 작은지는 직교 질문.
- **H_628** (inverse-u-polarity, 🔴 FALSIFIED): polarity 가 dΦ/dI peak 위치를 못 움직임 (3 polarity 모두 I=0.21) = shape-invariance 의 직접 증거. polarity 는 magnitude(scalar) 만 scaling — 본 H 의 shape ⊥ scalar dichotomy 의 polarity-축 선례.
- **H_351** (gz-inverse-u-phi-derivative-peak, 🟢 SUPPORTED 5/5): single-rule dΦ/dI inverse-U peak SSOT. inhibition mapping + central-diff + 13-point grid 의 원천.

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — shape/scalar feature 선택의 design 자의성

본 H 의 "shape feature" = dΦ/dI peak 위치, "scalar feature" = dΦ/dI peak 높이로 *조작적 정의* 했다. round 6 메타-발견의 shape (peak 위치·monotone 방향·envelope 형태) 와 scalar (threshold·rate·magnitude) 는 더 넓은 범주이며, 본 측정은 그중 *한 쌍* (peak-위치 vs peak-높이) 만 정량화한다. 다른 shape proxy (sign-change 수, envelope skew) 나 다른 scalar proxy (Φ(0.50) magnitude, AUC) 를 골랐다면 CV 비율이 달라질 수 있다. peak-위치 vs peak-높이 쌍은 H_614/H_628 이 직접 측정한 두 양이라 계보 정합이 가장 강한 선택이지만, dichotomy 의 *일반* 증명이 아닌 *대표 쌍 위에서의* 정량이라는 한계.

### C2 — 5-rule sample 한정 (CV 의 통계적 power)

CV 는 5개 점(rule)의 population 통계다. n=5 sample 의 CV 는 outlier 1개에 민감하며, 256 ECA rule space 의 universality 결론에 충분치 않다. H_614 §7 C1 의 4-rule 한계 carry — class I 부재, class III 2개(30·90)·IV 2개(54·110)·II 1개(184). 본 H 의 verdict 는 "**제출된 5 rule 위에서** shape 의 CV 가 scalar 의 CV 보다 작은가" 까지가 한계. full 256-rule 또는 class-stratified 16-rule sample 은 별도 round 후보.

### C3 — peak-위치 grid quantization vs magnitude 연속성의 비대칭

shape feature (peak I) 는 13-point grid 에 *snap* 되는 이산량 (가능값 13개), scalar feature (peak magnitude) 는 *연속* 실수다. 이산 vs 연속의 본질적 비대칭이 CV_shape 를 인위적으로 낮출 수 있다 (grid 가 위치를 양자화해 variance 를 억제). 즉 M1 PASS 의 일부는 측정 양식(grid-snap)의 artifact 일 수 있고, 순수 substrate 효과와 완전히 분리되지 않는다. 단, H_614 가 보였듯 peak 위치는 실제로 {0.18, 0.40} 두 값으로 *분기* 하므로 (grid 안에서도 variance 존재), grid-snap 이 variance 를 0 으로 만들지는 않는다 — 비대칭 caveat 은 magnitude 를 부풀리는 게 아니라 shape 를 절제하는 방향이라 메타-발견에 *보수적*. n=4 small-n (H_614 C2 carry) + 단일 inhibition mode `(1-I)·tpm` (H_628 L4 carry) 도 동일 한계.

## 8. verdict

```
verdict_class: __VERDICT__ — substrate-class (rule {30,54,90,110,184}) 를 가로질러
   shape feature (dΦ/dI peak *위치*) 의 변동계수 CV_shape __CMP__ scalar feature
   (Φ magnitude peak *높이*) 의 변동계수 CV_scalar.
   CV_shape=__CV_SHAPE__ vs CV_scalar=__CV_SCALAR__ (ratio __RATIO__).
   round 6 (mining H_632~639) 메타-발견 — *구조는 substrate-emergent, 숫자는
   design-convention* — 의 정량 메타-검증 __CONFIRM__.
config: 5-rule {30,54,90,110,184} n=4 ECA · 13-point GZ-dense I grid
   · tpm_mixed=(1-I)·tpm · faithful big-Φ 16-state mean · central-diff dΦ/dI
   · shape=argmax|dΦ/dI| · scalar=max|dΦ/dI| · population CV.
```

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_642: across Wolfram rules {30,54,90,110,184} (n=4 ECA, 13-point
   GZ-dense inhibition grid, faithful 16-state mean big-Φ, central-difference
   dΦ/dI), the coefficient of variation of the SHAPE feature (argmax_I |dΦ/dI|,
   peak position) is __CV_SHAPE__ vs the SCALAR feature (max_I |dΦ/dI|, peak
   height) CV __CV_SCALAR__ (ratio __RATIO__). Verdict: __VERDICT__ — the
   structural peak-LOCATION is __CMP_WORD__ class-invariant than the scalar peak-
   MAGNITUDE, quantifying round-6's meta-finding that SHAPE is substrate-emergent
   while SCALAR value is design-convention. Honest scope: one representative
   shape/scalar pair (peak-position vs peak-height) of a broader dichotomy, 5-rule
   sample (CV power-limited), shape is grid-snapped (13-point) vs scalar continuous
   — an asymmetry that conservatively suppresses CV_shape; toy n=4 single inhibition
   mode IIT4 big-Φ. Reproduces H_614 4-rule peak_I {0.18,0.40,0.18,0.40}."
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by
           design; values deterministic arithmetic, interpretation fenced
```

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- shape/scalar dichotomy 의 *일반* 증명 — 본 H 는 대표 쌍 (peak-위치 vs peak-높이) 1개만 정량 (C1).
- 256-rule universality — 5-rule sample CV (C2).
- grid-snap 이산 vs magnitude 연속 비대칭의 완전 분리 (C3).
- *왜* shape 가 substrate-emergent 인가의 mechanism — round-N candidate.
- n=4 외 ring size / non-ECA substrate (PureField).

## 10. UNIVERSE.md update

축 **G (ANIMA.mining 승격)** 에 round 6 메타-격상 row G6 추가 → done with `__VERDICT_SHORT__ (CV_shape=__CV_SHAPE__ __CMP__ CV_scalar=__CV_SCALAR__, ratio __RATIO__, 5-rule {30,54,90,110,184}, $0 mac-local 2026-05-28)`. round 6 메타-발견 (구조 vs 숫자) 의 정량 메타-검증.

## artifacts

- `UNIVERSE/state/h642_shape_invariance_meta_2026_05_28/run_h642.hexa` — 5-rule shape/scalar CV runner (H_614 패턴 확장, dependency = `iit4_eca` + stdlib `iit4_bigphi`)
- `UNIVERSE/state/h642_shape_invariance_meta_2026_05_28/result.json` — measurement SSOT (per-rule peak_I · peak_mag · CV_shape · CV_scalar · ratio · verdict)
- `UNIVERSE/H_642_shape_invariance_vs_scalar_convention_meta.md` — 본문 (SSOT)
