---
id: H_642
slug: shape-invariance-vs-scalar-convention-meta
title: shape feature (peak 위치·monotone 방향·envelope 형태) 가 scalar value (absolute threshold·rate·magnitude) 보다 substrate-class 불변인가 — round 6 메타-발견 정량 격상
domain: consciousness · math · physics · meta · savant
status: FALSIFIED
verdict_class: FALSIFIED
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
| 90   | III-additive  | **0.05** | **0.276542** | **1** |
| 110  | IV-complex    | 0.18 | 21.3315 | 0 |
| 184  | II-particle   | 0.40 | 19.9171 | 0 |

> rule 90 (XOR-additive) 는 강한 outlier — IIT4 big-Φ 가 거의 0 (Φ(0.50)=0.0526) 이라 peak |dΦ/dI|=0.2765 가 다른 rule (10.8~21.7) 의 ~2% 수준. additive/linear ECA 의 cause-effect repertoire 가 maximally factorizable → 통합 부재. peak I=0.05 (grid 경계) 도 shape outlier.

**메타-통계 (5 rule, population CV)**

| feature | mean | population stddev | **CV** |
|---------|-----:|------------------:|-------:|
| shape (peak I)  | 0.242 | 0.137463 | **0.568028** |
| scalar (peak \|dΦ/dI\|) | 14.8216 | 8.28983 | **0.559306** |

- **ratio = CV_scalar / CV_shape = 0.984646**
- **M1 (CV_shape < CV_scalar) = FAIL** (0.568028 ≥ 0.559306 — shape 가 scalar 보다 *근소하게 더* class-variant)
- **M2 (ratio > 1) = FAIL** (ratio 0.9846 < 1)
- rule {30,54,110,184} peak_I = {0.18, 0.40, 0.18, 0.40} + peak_mag {21.74, 10.84, 21.33, 19.92} → H_614 재현 ✓ (engine 정합)

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

본 H 는 round 6 메타-발견 — *shape 가 scalar 보다 class-invariant* — 을 이 대표 쌍 위에서 **반증**했다 (CV_shape=0.568 ≥ CV_scalar=0.559, ratio 0.9846 < 1). 두 CV 는 거의 동일 (Δ=0.0087, 1.5% 차이) — shape 가 scalar *보다* 불변이라는 강주장은 깨지나, shape 가 scalar *만큼* class-variant 라는 약한 형태로 닫힌다. 핵심 원인: rule 90 (XOR-additive) 가 shape *와* scalar 양쪽 모두에서 outlier (peak I=0.05 경계 + peak_mag 0.28 ≈ 0) 라 두 변동을 동시에 끌어올렸다.

### C1 — shape/scalar feature 선택의 design 자의성 (반증의 fragility)

"shape feature" = dΦ/dI peak 위치, "scalar feature" = dΦ/dI peak 높이로 *조작적 정의*. round 6 메타-발견의 shape (peak 위치·monotone 방향·envelope 형태) 와 scalar (threshold·rate·magnitude) 는 더 넓은 범주이며 본 측정은 *한 쌍* (peak-위치 vs peak-높이) 만 정량화한다. ratio 0.9846 은 1 에 매우 가까워 (1.5% 차이) — 다른 shape proxy (sign-change 수, envelope skew) 나 scalar proxy (Φ(0.50) magnitude, AUC) 를 골랐다면 부등호가 뒤집힐 수 있는 borderline. 즉 본 반증은 "shape 가 scalar 보다 불변이라는 **강주장**이 이 대표 쌍에서 성립 안 함" 까지이고, 메타-발견의 *완전* 폐기가 아니라 *대표 쌍 위 강주장의* 폐기다. 실제로 H_628 (polarity ⊥ peak-위치) 는 shape-invariance 의 직접 증거로 남는다 — 본 H 는 그 invariance 가 *scalar 보다 우월* 하지는 않음을 보일 뿐.

### C2 — 5-rule sample + outlier 지배 (CV 의 통계적 fragility)

CV 는 5 점(rule) population 통계라 outlier 1개에 극도로 민감하다. rule 90 (XOR-additive, Φ≈0) 단독이 CV_shape (peak I=0.05 가 mean 0.242 를 끌어내림) *와* CV_scalar (peak_mag 0.28 이 mean 14.8 을 끌어내림) 양쪽을 동시에 지배 — rule 90 제거 시 4-rule CV 는 shape {0.18,0.40,0.18,0.40} 가 거의 binary (CV≈0.31), scalar {21.74,10.84,21.33,19.92} 가 CV≈0.26 로 부등호가 다시 shape>scalar 유지될 가능성도 있으나 (즉 반증 robust), additive-rule outlier 가 결론을 좌우한다는 사실 자체가 5-rule sample 의 한계. H_614 §7 C1 (4-rule, class I 부재) carry. 256-rule 또는 class-stratified sample 은 별도 round.

### C3 — peak-위치 grid-snap vs magnitude 연속성의 비대칭 (반증에 보수적)

shape feature (peak I) 는 13-point grid 에 *snap* 되는 이산량 (가능값 13개), scalar (peak magnitude) 는 *연속* 실수다. 이 비대칭은 CV_shape 를 인위적으로 *억제* 하는 방향 (grid 양자화가 위치 variance 를 압축) — 즉 grid 가 더 조밀했다면 CV_shape 가 *더 커져* 반증이 *강화* 될 수 있다. 따라서 본 FALSIFIED 는 측정 양식상 *보수적* (grid-snap 이 shape 를 유리하게 절제했음에도 여전히 CV_shape ≥ CV_scalar). n=4 small-n (H_614 C2) + 단일 inhibition mode `(1-I)·tpm` (H_628 L4) + rule 90 outlier 가 mean 을 비선형 왜곡 (CV 가 평균-정규화라 0-근접 mean 에 폭발적) 도 carry. 반증 결론의 정직한 scope = "이 대표 shape/scalar 쌍 + 5-rule + grid-snap 양식 위에서, shape 가 scalar 보다 class-불변이라는 강주장 deterministically 거부."

## 8. verdict

```
verdict_class: 🔴 FALSIFIED (M1 FAIL · M2 FAIL · n_rule=5) — substrate-class (rule
   {30,54,90,110,184}) 를 가로질러 shape feature (dΦ/dI peak *위치*) 의 변동계수
   CV_shape=0.568028 가 scalar feature (Φ magnitude peak *높이*) 의 변동계수
   CV_scalar=0.559306 보다 (근소하게) *크다* — ratio CV_scalar/CV_shape=0.984646
   < 1. 즉 shape 가 scalar 보다 class-invariant 라는 round 6 (mining H_632~639)
   메타-발견의 *강주장* 은 이 대표 shape/scalar 쌍 위에서 **반증**. 두 CV 가 거의
   동일 (Δ=0.0087, 1.5%) — shape 가 scalar *만큼* class-variant 라는 약한 형태로
   닫힘. rule 90 (XOR-additive, Φ≈0) 이 shape (peak I=0.05 경계) 와 scalar
   (peak_mag 0.28≈0) 양쪽 outlier 로 두 변동을 동시 지배.
config: 5-rule {30,54,90,110,184} n=4 ECA · 13-point GZ-dense I grid
   · tpm_mixed=(1-I)·tpm · faithful big-Φ 16-state mean · central-diff dΦ/dI
   · shape=argmax_I|dΦ/dI| · scalar=max_I|dΦ/dI| · population CV.
```

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_642: across Wolfram rules {30,54,90,110,184} (n=4 ECA, 13-point
   GZ-dense inhibition grid, faithful 16-state mean big-Φ, central-difference
   dΦ/dI), the coefficient of variation of the SHAPE feature (argmax_I |dΦ/dI|,
   peak position) is CV_shape=0.568028 vs the SCALAR feature (max_I |dΦ/dI|, peak
   height) CV_scalar=0.559306 (ratio CV_scalar/CV_shape=0.984646). Verdict:
   FALSIFIED — the structural peak-LOCATION is NOT more class-invariant than the
   scalar peak-MAGNITUDE (CV_shape >= CV_scalar by 1.5%), refuting round-6's STRONG
   meta-claim that SHAPE is more substrate-invariant than SCALAR convention on this
   representative pair; the two CVs are nearly equal so the weak form (shape as
   class-variant AS scalar) holds. The XOR-additive rule 90 (big-Φ ~= 0) is a joint
   outlier in both shape (peak I=0.05 boundary) and scalar (peak_mag 0.28), driving
   both CVs. Honest scope: one representative shape/scalar pair (peak-position vs
   peak-height) of a broader dichotomy, 5-rule sample (CV outlier-fragile, borderline
   ratio 0.98), shape is grid-snapped (13-point) vs scalar continuous — an asymmetry
   that CONSERVATIVELY suppresses CV_shape so the falsification is robust to it; toy
   n=4 single inhibition mode IIT4 big-Φ. Reproduces H_614 4-rule peak_I
   {0.18,0.40,0.18,0.40} + peak_mag {21.74,10.84,21.33,19.92}."
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

축 **G (ANIMA.mining 승격)** 에 round 6 메타-격상 row G8 추가 → done with `🔴 FALSIFIED (M1 FAIL · CV_shape=0.568028 ≥ CV_scalar=0.559306, ratio 0.984646 < 1, 5-rule {30,54,90,110,184} n=4, rule 90 XOR-additive joint-outlier, $0 mac-local 2026-05-28)`. round 6 메타-발견 (구조가 숫자보다 class-불변) 의 *강주장* 이 이 대표 shape/scalar 쌍 위에서 반증 — 두 CV 가 거의 동일 (1.5% 차이) → shape 가 scalar 만큼 class-variant 라는 약한 형태로 closed-negative.

## artifacts

- `UNIVERSE/state/h642_shape_invariance_meta_2026_05_28/run_h642.hexa` — 5-rule shape/scalar CV runner (H_614 패턴 확장, dependency = `iit4_eca` + stdlib `iit4_bigphi`)
- `UNIVERSE/state/h642_shape_invariance_meta_2026_05_28/result.json` — measurement SSOT (per-rule peak_I · peak_mag · CV_shape · CV_scalar · ratio · verdict)
- `UNIVERSE/H_642_shape_invariance_vs_scalar_convention_meta.md` — 본문 (SSOT)
