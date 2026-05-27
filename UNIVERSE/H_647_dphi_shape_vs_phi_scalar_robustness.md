---
id: H_647
slug: dphi-shape-vs-phi-scalar-robustness
title: dΦ/dI shape vs Φ scalar — seed-robustness 축 (shape feature 가 scalar 보다 seed 변동에 robust 한가)
domain: consciousness · math · physics · meta
status: FALSIFIED
verdict_class: CLOSED-NEGATIVE
exploration_method: E0 (round-6 메타-발견 seed-robustness 각도) + E11 (cross-substrate Φ-signature) + E5 (continuous-parameter sweep) + E0 (H_642 cross-rule sister)
verification_method: W1 (numerical) + W4 (verdict-5-class) + W11 (cross-axis sister) + W12 (invariant signature)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28 (UNIVERSE 축 G · round-6 메타-발견 seed-robustness 축)
sister: H_642 (cross-RULE peak robustness sister · still running), H_351 (single-substrate dΦ/dI peak GZ_LOWER), H_618 (collective dΦ_c/dI peak GZ_LOWER), H_639 (amplitude-cross × Φ-derivative convention-FAL)
---

# H_647 — dΦ/dI shape vs Φ scalar — seed-robustness 축

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib`(`iit4_eca` + `iit4_bigphi` → `stdlib/consciousness/iit4_bigphi.hexa`) 재사용 (commons g61, 재발명 0). 통합 척도 = **faithful causal big-Φ** (H_285/H_351 양식, 2^n state-mean). `$0 · mac-local · hexa-only · LLM none · deterministic(LCG)`.

## 1. 가설 (Hypothesis) — round-6 메타-발견 seed-robustness 각도

round 6 메타-발견 = **"shape > scalar substrate-class robustness"** — shape feature
(dΦ/dI peak 위치) 가 scalar feature (Φ 값) 보다 substrate-class 변동에 강건하다는
패턴. H_642 (still running) 가 그 패턴을 **cross-RULE** peak 차원에서 검정 중이다.

본 H_647 은 *다른 축* — **cross-SEED perturbation robustness**:

| feature | 정의 | robustness 측도 |
|---|---|---|
| **SHAPE** | `argmax_I |dΦ/dI|` (peak 위치) | 절대 std `peak_std` (단위 I, [0,1] 정규화 좌표) |
| **SCALAR** | `Φ(I=0)` (baseline big-Φ magnitude) | 상대 std `phi0_cv = std/mean` (CV) |

**H1** (본 가설): 같은 rule × 다른 random seed (N≥10) 에서
**dΦ/dI peak 위치의 (절대) std `<` Φ magnitude 의 상대 std (CV)** —
즉 shape 는 seed 변동에 robust, scalar 는 seed-sensitive.

**Falsifier (H0)**: `peak_std ≥ phi0_cv` — peak 위치 std 가 Φ magnitude CV 이상
(shape 도 seed-sensitive 하거나, scalar 가 오히려 더 robust).

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1** SHAPE-ROBUST | `peak_std < phi0_cv` | 핵심 — shape>scalar (가설 H1) |
| **F2** SHAPE-TIGHT | `peak_std ≤ 0.05` | peak 위치 절대 안정 |
| **F3** SCALAR-VARIES | `phi0_cv > 0` | scalar 가 실제로 seed 에 변동 (대조 유효) |
| **F4** N-SUFFICIENT | `N ≥ 10` | 표본 충분 |
| **F5** BYTE-EQUAL | in-process recompute byte-identical (`|Δ| ≤ 1e-12`) | RFC 033 결정론 |

**verdict_rule**
- **SUPPORTED** = F1 ∧ F2 ∧ F3 ∧ F4 ∧ F5 (shape>scalar 확증)
- **PARTIAL** = F1 ∧ (!F2) ∧ F3 ∧ F4 ∧ F5 (shape>scalar 但 절대-안정 미달)
- **FALSIFIED** = !F1 (`peak_std ≥ phi0_cv` — shape 가 scalar 보다 robust 하지 않음)

## 3. 방법 (Method)

### 3.1 substrate (H_351 carry — 재발명 0)

ECA **rule 110** (Wolfram class IV, edge-of-chaos, H_285/H_351 anchor) on a periodic
ring of **n = 4 cells**. faithful causal big-Φ 측정은 H_351 과 동일 엔진 (`iit4_eca` +
`iit4_bigphi`), 각 TPM 에서 **2^n = 16 state-mean** (single-state fragility 회피, H_285 양식).

### 3.2 seed perturbation 정의 (substrate random realization)

"random seed" = **per-state multiplicative inhibition JITTER** 의 random realization.
각 seed `s` 마다 deterministic LCG(s) (Numerical Recipes 상수, RNG single-stream 회피
[[reference-life-cycle-hexa-run-gotchas]]) 로 per-state jitter factor 를 뽑는다:

```
u[k]      ~ LCG(s)  ∈ [0,1)
factor[k] = 1 + A·(2·u[k] − 1)   ∈ [1−A, 1+A],   A = 0.30
tpm_seed[k] = clamp( eca_tpm[k] · factor[k], 0, 1 )
```

이는 substrate 의 microscopic random realization (구현/측정 노이즈) 을 모사한다.
seed 는 deterministic CA 의 *질적* 동역학을 유지하되 전이확률을 ±30% 흔든다.

### 3.3 per-seed I-sweep (H_351 mapping)

각 seed 의 `tpm_seed` 에 H_351 과 동일한 inhibition mixing:

```
tpm_mixed[k] = (1 − I) · tpm_seed[k]
```

I-grid (H_351 양식, dense near GZ region):

```
I ∈ {0.05, 0.10, 0.15, 0.18, 0.21, 0.23, 0.25, 0.30, 0.35, 0.40,
     0.50, 0.70, 0.95}                                   — 13 points
```

`dΦ/dI` central finite difference (forward at idx=0, backward at idx=m−1),
`peak_I = argmax_I |dΦ/dI|` (SHAPE). `phi0 = Φ(I=0) = mean_big_phi(tpm_seed)` (SCALAR).

### 3.4 robustness 측도

N=12 seed (≥10) 에 대해:
`peak_std = std(peak_I[·])` (절대) · `phi0_cv = std(phi0[·]) / mean(phi0[·])` (상대).
peak_I 가 [0,1] 정규화 좌표이므로 절대-std 와 CV 의 동차 비교 가능. 보조: `peak_cv`.

### 3.5 runner

`UNIVERSE/state/h647_shape_vs_scalar_robustness_2026_05_28/run_h647.hexa`
(단일 hexa, dependency-free, foreground sync, $0). H_642 (cross-rule) 와 다른 축
(cross-seed) — 같은 rule 110 fixed, seed 만 변동.

## 4. 측정 (Measurement) — `result.json`

| seed | peak_I (SHAPE) | Φ0 (SCALAR) |
|---:|---:|---:|
| 0  | 0.10 | 14.0189 |
| 1  | 0.21 | 14.7039 |
| 2  | 0.05 | 13.6870 |
| 3  | 0.40 | 13.9578 |
| 4  | 0.25 | 12.2792 |
| 5  | 0.05 | 14.3762 |
| 6  | 0.23 | 13.4621 |
| 7  | 0.05 | 13.6547 |
| 8  | 0.35 | 14.0269 |
| 9  | 0.05 | 13.5082 |
| 10 | 0.21 | 13.3048 |
| 11 | 0.23 | 13.8189 |

| 측도 | 값 |
|---|---:|
| N seeds | 12 |
| peak_I mean | 0.181667 |
| **peak_I std (SHAPE, abs)** | **0.116536** |
| peak_I cv | 0.641481 |
| Φ0 mean | 13.7332 |
| Φ0 std | 0.578163 |
| **Φ0 cv (SCALAR, rel)** | **0.0420996** |
| byte_eq | true |

## 5. 결과 (Result)

- **peak_std = 0.116536** ≫ **phi0_cv = 0.0420996** (약 **2.77배**).
- SHAPE (peak 위치) 가 seed 변동에 **강하게 sensitive** — peak_I 가 0.05 ↔ 0.40
  사이를 넘나든다 (mean 0.18 근방, 但 CV=0.64 의 큰 산포).
- SCALAR (Φ magnitude) 는 seed 변동에 **놀랍도록 robust** — mean 13.73, std 0.58
  (CV 4.2% 뿐), 12 seed 모두 [12.28, 14.70] 좁은 band 안.
- byte-equal recompute 통과 (결정론 확증).

## 6. falsifier 결과 + Cross-link

| ID | 결과 | 값 |
|----|------|-----|
| F1 SHAPE-ROBUST (`peak_std < phi0_cv`) | **FAIL** | 0.116536 ≥ 0.0420996 |
| F2 SHAPE-TIGHT (`peak_std ≤ 0.05`) | **FAIL** | 0.116536 > 0.05 |
| F3 SCALAR-VARIES (`phi0_cv > 0`) | PASS | 0.0421 > 0 |
| F4 N-SUFFICIENT (`N ≥ 10`) | PASS | 12 ≥ 10 |
| F5 BYTE-EQUAL | PASS | `|Δ| ≤ 1e-12` |

`!F1` 발동 → **VERDICT = FALSIFIED (CLOSED-NEGATIVE)**.
shape>scalar 확증 **부정** — 오히려 **scalar(Φ magnitude)가 더 robust**, shape(peak 위치)가
seed-sensitive. 가설의 **방향이 뒤집혔다** (reversed).

### Cross-link

- **H_642 (cross-RULE peak robustness, still running)** — 본 H_647 의 sister. H_642 는
  *cross-rule* 차원, 본 건은 *cross-seed* 차원. 두 축은 독립이며, 본 cross-seed
  결과는 round-6 메타-발견("shape>scalar")이 **seed-perturbation 축에서는 성립하지 않음**
  을 보인다 — H_642 가 cross-rule 에서 SUPPORTED 로 나오더라도 그 robustness 는 축-한정.
- **H_351 (single dΦ/dI peak GZ_LOWER, 🟢 5/5)** — clean rule 110 의 단일 peak (I=0.18,
  GZ_LOWER ±0.05) 는 jitter 없는 점-측정. 본 건은 그 peak 가 **±30% 전이확률 jitter
  아래에서 위치 불안정** 함을 보여 H_351 의 peak-위치 SUPPORTED 가 noise-free 조건부임을 정량.
- **H_618 (collective dΦ_c/dI peak, |Δ|=0.00232)** — collective 차원 peak-위치 robust 했으나,
  그 robustness 는 *coupling-weight* 축이지 seed-jitter 축이 아님 — 본 건과 직교.
- **H_639 (amplitude-cross × Φ-derivative, 🔴 convention-FAL)** — emit feature 의 substrate-Φ
  wiring 이 convention-종속이라 FAL. 본 건은 그 negative-signature 의 *seed-jitter* 판본 —
  축 G "emit/shape feature 가 Φ-구조에 약하게/비-robust 결합" 누적 negative-signature 강화.

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — seed N 과 peak 위치 해상도 (핵심 honest)

peak_I 는 **13-point I-grid 상의 discrete argmax** — 연속 peak 위치가 아니다.
grid 간격이 0.02~0.25 로 불균일하므로 peak_std 0.1165 에는 **grid-discretization 분산**이
섞여 있다. 단 이 discretization 은 phi0(연속 실수) 에는 없는 SHAPE 측 고유 한계이며,
오히려 본 결론(shape 가 scalar 보다 산포 큼)을 *과장* 이 아니라 *구조적으로 설명* 한다
— peak 위치는 argmax 가 grid-cell 사이를 점프하는 이산량이라 본질적으로 fragile.
N=12 (≥10 falsifier 충족) 는 std 추정에 충분하나, peak_std 의 신뢰구간은 N↑ + grid 해상도↑
(예: I-grid 50-point uniform) 로 좁힐 여지 — 본 결론(2.77배 gap)은 그 정밀화에 robust 할 것으로 예상.

### C2 — jitter amplitude A=0.30 의 sensitivity

A (per-state ±30% 전이확률 jitter) 는 단일 설정. A→0 이면 peak_std→0 (clean H_351 단일 peak 수렴),
A↑ 이면 peak_std↑ 가 자명. 따라서 "shape 가 scalar 보다 산포 크다" 는 *방향* 결론은
A>0 전역에서 성립하나 (Φ magnitude 가 16-state 평균으로 jitter 를 흡수 평균화 vs argmax 는
단일 극값이라 jitter 증폭), peak_std 의 절대값은 A-종속. F1 의 inequality (peak_std≥phi0_cv)
가 A 의 어느 범위에서 뒤집히는지는 미검정 — A-sweep 후속 lane (H_647b 후보).

### C3 — substrate scope (single-rule single-n)

rule 110, n=4 단일 substrate. cross-rule(H_642) · cross-n 으로의 일반화는 본 건 scope 밖.
본 cross-seed 결과는 round-6 메타-발견의 **seed-축 반례** 1건 — "shape>scalar" 가 *모든*
robustness 축에서 성립하는 universal 패턴이 아니라 **축-종속**임을 보인다 (negative finding 의 정보값).

## 8. verdict

**FALSIFIED (CLOSED-NEGATIVE, 3/5)** — F3·F4·F5 PASS, F1·F2 FAIL.

ruled-out: **dΦ/dI peak 위치(shape)가 Φ magnitude(scalar)보다 random-seed perturbation 에
강건하다** 는 가설 (round-6 메타-발견의 seed-축 확장). 측정 결과 **방향 역전** —
scalar CV 4.2% 가 shape abs-std 11.7% 보다 2.77배 작다 (scalar 가 더 robust).

## 9. honest scope

- **deterministic** · in-process byte-equal (F5 PASS) · LCG single-stream · $0 mac-local · LLM none.
- single rule 110 · n=4 · jitter A=0.30 · I-grid 13-point · N=12 seed. C1~C3 의 한계 보유.
- negative result — round-6 메타-발견("shape>scalar")이 **cross-seed 축에서는 반증**됨을
  확정 (cross-rule H_642 와 독립). robustness 의 축-종속성 (cross-rule ≠ cross-seed) 을 식별.

## 10. UNIVERSE.md update

축 G — round-6 메타-발견 seed-robustness 축 = G6 row 추가 (🔴 CLOSED-NEGATIVE).

## artifacts

- `UNIVERSE/state/h647_shape_vs_scalar_robustness_2026_05_28/run_h647.hexa` — runner (단일 hexa)
- `UNIVERSE/state/h647_shape_vs_scalar_robustness_2026_05_28/result.json` — 측정 SSOT
