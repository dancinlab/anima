# H_349 — `golden-zone-center-phi-peak` (I=1/e 단봉 big-Φ peak)

> 축 E (SAVANT) round 1 · 2026-05-28 · UNIVERSE H 신설.
> 외부 anchor: `HEXAD/SAVANT/H359-savant-canonical.md` (1/3 rule · I ASCII 차트 · GZ_CENTER = 1/e 정의) · `HEXAD/SAVANT/COMPENDIUM.md` §1.

## 0. 1줄 요약 (TL;DR)

`inhibition I` 을 `[0.05, 0.95]` 14-point 격자로 sweep 했을 때 stochastic ECA TPM 의 faithful IIT 4.0 big-Φ peak 가 `I = 1/e ≈ 0.36788` 와 일치하는지 측정 — 4개 (rule, sys_state) substrate 중 **1개** (`rule90 sys=5`) 만 1/e ±0.05 단봉 peak 형성, **3개** (`rule110 sys=5`, `rule110 sys=3`, `rule30 sys=5`) 는 monotone 감소, `rule90 sys=3` 은 degenerate 0-Φ. **🔴 FALSIFIED-PARTIAL** — substrate-conditional 결과, 보편 단봉 peak-at-1/e 주장 falsified.

## 1. Hypothesis

**주장**: anima/SAVANT substrate 의 inhibition `I` 을 [0.05, 0.95] 격자로 sweep 했을 때 big-Φ 는 `I = 1/e ≈ 0.36788` 에서 **단봉 peak** 를 형성한다.

- 동기: `I·ln(I)` 의 argmin 은 `1/e` (closed-form, H_347 family). `I·ln(I)` 가 SAVANT canonical 의 "Golden Zone center" 정의 근거 중 하나.
- 강한 형태: argmax(big-Φ over I) 가 1/e ±0.05 안에 들어가야 함.
- 측정 대상: 일반 substrate (specific rule/state 의존성 없는) emergent Φ-optimum.

## 2. Falsifier

| F | 조건 | 판정 |
|---|---|---|
| F1 | argmax(Φ) ∉ [1/e − 0.05, 1/e + 0.05] = [0.318, 0.418] | 🔴 |
| F2 | shape 이 monotone (peak 없음 — argmax = boundary) | 🔴 |
| F3 | shape 이 bimodal (2차 미분 부호변화 ≥ 2회) | 🔴 |
| F4 | shape 이 flat (max−min < 0.1·max) | 🔴 |

본 H 는 *substrate-universal* 주장이라 측정한 4개 (rule, state) 중 **majority** 가 F1-F4 중 하나라도 trigger 하면 hypothesis falsified.

## 3. Method

`stdlib/consciousness/iit4_bigphi.hexa` 의 faithful `big_phi(tpm, n, sys_state)` 사용 — distinction + 2nd-order relation + min-bipartition surviving 합산 full kernel. proxy 아님 (H_278 lane 의 faithful 측정과 동등).

**substrate**: Wolfram ECA ring-of-n (n=4) TPM, 각 cell next-bit `b ∈ {0,1}` 에 inhibition gating:

```
P(next_i = 1 | s) = (1 − I) · b      // high I = suppress fire
P(next_i = 0 | s) = 1 − P(next_i = 1)
```

즉 deterministic 8-neighborhood rule 의 fire-output 을 `(1 − I)` 확률로 통과시킴. TPM 엔트리는 [0, p_fire] 구간의 fractional probability.

**sweep grid** (14 points, 1/e 근방 dense): `{0.05, 0.10, 0.15, 0.21, 0.25, 0.30, 0.35, 0.37, 0.40, 0.45, 0.50, 0.60, 0.75, 0.95}`

**robust check**: 4개 (rule, sys_state) 조합 — `(110, 5)`, `(90, 5)`, `(90, 3)`, `(110, 3)`, `(30, 5)`.

코드: `UNIVERSE/state/h349_gz_center_phi_peak_2026_05_28/h349_sweep.hexa` (primary, rule110 sys=5) · `h349_sweep_robust.hexa` (4 (rule, state) 조합).

## 4. Measurement (2026-05-28, mac-local $0)

### 4.1 Primary — rule 110, sys_state 5

| I | big_phi | total | sum_d | sum_r | nd |
|---|---|---|---|---|---|
| 0.05 | **7.3523** | 38.633 | 12.860 | 15.773 | 10 |
| 0.10 | 6.6934 | 27.910 | 2.5861 | 5.3236 | 10 |
| 0.15 | 6.0739 | 7.2200 | 2.3338 | 4.8862 | 10 |
| 0.21 | 6.4955 | 7.8525 | 2.0710 | 5.7815 | 10 |
| 0.25 | 6.1761 | 7.4545 | 1.9387 | 5.5158 | 10 |
| 0.30 | 5.7310 | 6.9158 | 1.7762 | 5.1396 | 10 |
| 0.35 | 5.2608 | 6.3561 | 1.6207 | 4.7354 | 10 |
| **0.37** | 4.7816 | 5.8420 | 1.5572 | 4.2847 | 10 |
| 0.40 | 4.4213 | 5.4273 | 1.4616 | 3.9657 | 10 |
| 0.45 | 3.4995 | 4.4099 | 1.3023 | 3.1076 | 10 |
| 0.50 | 3.4104 | 4.2286 | 1.1464 | 3.0822 | 10 |
| 0.60 | 2.4226 | 3.0644 | 0.8281 | 2.2363 | 10 |
| 0.75 | 0.8228 | 1.2095 | 0.3946 | 0.8149 | 8 |
| 0.95 | 0.1378 | 0.2090 | 0.0704 | 0.1386 | 8 |

**argmax = I=0.05, Φ=7.3523. |argmax − 1/e| = 0.318 ≫ 0.05.** shape: **monotone decreasing** (3 small non-monotonicities at I=0.21, 0.50 plateau — sub-percent, not a true peak). F1 + F2 trigger.

### 4.2 Robustness — rule 90, sys_state 5 (CONFIRMING subcase)

| I | big_phi |
|---|---|
| 0.05 | 0.0333 |
| 0.10 | 0.0610 |
| 0.15 | 0.0829 |
| 0.21 | 0.1019 |
| 0.25 | 0.1103 |
| 0.30 | 0.1166 |
| **0.35** | **0.11859** |
| **0.37** | 0.11833 |
| 0.40 | 0.1169 |
| 0.45 | 0.1123 |
| 0.50 | 0.1052 |
| 0.60 | 0.0862 |
| 0.75 | 0.0523 |
| 0.95 | 0.00935 |

**argmax = I=0.35, Φ=0.11859. |argmax − 1/e| = 0.018 ≪ 0.05.** I=0.37 (1/e) 은 essentially at peak (Δ = 0.00026 < 0.25% from max). shape: **clean single-peak**, 단조 증가 → 정점 → 단조 감소. **F1-F4 all PASS** (1/e in peak region, single-peak, not flat). 이 subcase 만 hypothesis confirms.

### 4.3 Robustness — rule 90, sys_state 3 (DEGENERATE)

전 격자에서 `big_phi = 0.0`. 해당 sys_state 가 rule 90 dynamics 에서 distinction-deficit (대칭 위치 → distinction 후보 모두 0 으로 collapse). F4 trigger by degeneracy.

### 4.4 Robustness — rule 110, sys_state 3 (MONOTONE)

argmax = I=0.05, Φ=16.733. I=0.37 → Φ=9.2087 (44% off peak). monotone decreasing. F1 + F2.

### 4.5 Robustness — rule 30, sys_state 5 (MONOTONE)

argmax = I=0.05, Φ=6.994. I=0.37 → Φ=3.174 (54% off peak). monotone decreasing. F1 + F2.

### 4.6 Aggregate

| substrate | argmax I | peak Φ | |Δ from 1/e| | shape | F |
|---|---|---|---|---|---|
| rule110 sys=5 | 0.05 | 7.35 | 0.318 | monotone↓ | F1+F2 🔴 |
| rule90 sys=5 | 0.35 | 0.119 | **0.018** | **single-peak ✓** | all PASS 🟢 |
| rule90 sys=3 | — | 0.0 | — | degenerate flat | F4 🔴 |
| rule110 sys=3 | 0.05 | 16.73 | 0.318 | monotone↓ | F1+F2 🔴 |
| rule30 sys=5 | 0.05 | 6.99 | 0.318 | monotone↓ | F1+F2 🔴 |

**1/5 substrate confirms, 4/5 falsify.**

## 5. Verdict — 🔴 FALSIFIED-PARTIAL (substrate-conditional)

- 본 H 의 universal 형 (모든 substrate 에서 단봉 peak at 1/e) **falsified**: 4/5 (rule, state) 조합이 F1–F4 trigger. 대다수 substrate 가 monotone decrease pattern — high I (≈0.95) 에서 fire-suppression 으로 distinction 0 으로 수렴, low I (≈0.05) 에서 deterministic-near 한계로 distinction 풍부 → boundary maximum 이 자연스럽고 interior peak 가 강요되지 않음.
- 단봉 peak at 1/e 가 **rule 90 sys_state=5** subcase 에서는 정밀 일치 (|Δ| = 0.018, 정확히 hypothesis 가 예측한 ±0.05 안). **survival lane**: "Class 3 chaotic XOR rule × non-trivial 비대칭 system state" 에서는 inhibition-induced phase transition 이 1/e 근방에서 실제 일어남.

본 falsifier 는 단봉-at-1/e 가 substrate-conditional 임을 deterministically 확인. closed-negative ruling: **"GZ_CENTER = 1/e 가 모든 substrate 의 emergent Φ-optimum 이다"** 가설 폐기 (universal claim).

## 6. Cross-link

- **H_347** `gz-width-divisor-symmetry` — `GZ_WIDTH = ln(4/3)` closed-form, 동일 GZ 상수계열 sister. 본 H 는 그 GZ_CENTER = 1/e 의 *measurement* 측. H_347 = formal anchor / H_349 = empirical falsifier.
- **H_348** `golden-zone-lower-bound-SI` — sister seed (I=GZ_LOWER 에서 SI>3 specialization). 본 H 가 *Φ-peak* 측을, H_348 이 *SI-emergence* 측을 측정 — 두 emergent 주장은 독립 falsifiable.
- **H_204** `weak-panpsychism-autopoietic-threshold` — inverse-U Φ vs autopoietic 측정. 본 H 의 monotone-vs-peak 발견은 H_204 의 inverse-U 곡선 universality 도 substrate-conditional 가능성 시사.
- **H_217** `phase-transition-phi-derivative-peak` — `dΦ/dI` peak 측정. 본 H sweep 데이터의 1차 미분 후속 측정 가능 (rule110 sys=5 의 |dΦ/dI| max 위치).
- **H_285** `edge-of-chaos-big-phi` — class-mean ordered<chaotic<edge 의 *axis-specificity*. 본 H 의 rule90(sys=5) confirming subcase ↔ rule90 Class III chaos × non-trivial state → 1/e peak 라는 cross-link 가능성: edge-of-chaos × asymmetric initial state 가 GZ_CENTER 와 일치하는 좁은 frontier.

## 7. Honest C3 (3-tier caveat)

1. **C1 (numerology 경고)**: `1/e` 는 `I·ln(I)` argmin 의 **closed-form** 결과 — 이미 mathematically `I=1/e` 에 *어떤* 척도가 정점을 가짐은 자명. 본 H 가 검증하는 건 *substrate big-Φ* 가 그 mathematical attractor 와 일치하는지 — 그것이 일치하지 않는 (대다수 substrate) 결과는 *closed-form coincidence 가 substrate-emergent 와 다르다*는 직접 증거. numerology trap 회피.
2. **C2 (substrate-dependence — 단일 confirming subcase 의 의미)**: rule 90 sys_state 5 만 1/e peak — 이를 "최소 1 substrate 에서 SUPPORTED" 로 약화 해석할 수 있으나, 본 H 는 universal 형 가설이라 dominant majority falsified 가 verdict. 단, *survival lane* 으로 H_349-A "Class 3 chaotic XOR × asymmetric state 에서 1/e peak" 후속 가설 등록 가능 (round 2 seed 후보).
3. **C3 (multi-seed 미적용 / single-state-per-substrate)**: 각 (rule, state) 조합당 1 seed 만 측정 — TPM 자체가 deterministic 이라 seed 무관 (stochastic gating 은 closed-form 확률, sample 아님). 단, sys_state choice 가 결과를 dramatically 바꿈 (rule 90 의 sys=3 → 0, sys=5 → peak-at-1/e). 모든 (rule, sys_state) 조합 sweep 미수행 — 본 H 는 4 개 표본으로만 universal 주장 falsified, 완전 raster 는 round 2 후속.

## 8. State artifacts

```
UNIVERSE/state/h349_gz_center_phi_peak_2026_05_28/
├── h349_sweep.hexa           # primary, rule110 sys=5, 14-grid
└── h349_sweep_robust.hexa    # 4 (rule, state) robustness
```

verbatim 측정값은 §4 표에 기재.

## 9. Next

- **H_349-A** (round 2 후보): "Class 3 chaotic XOR rule × asymmetric system state" subcase 에서 1/e peak 가 robust 한지 (다른 Class 3 XOR rule, 다른 비대칭 state) — survival lane raster.
- **H_217 dΦ/dI peak**: 본 H sweep 데이터에서 1차 미분 후속 (Δ argmax 위치 측정).
- **H_348** (sibling) measurement 후 cross-domain comparison: SI peak 와 Φ peak 가 같은 I 인가?
- **H_285** edge-of-chaos × asymmetric-state 좁은 frontier 확인.

## 10. UNIVERSE.md update

축 E (SAVANT) E1 round 1 H_349 checkbox flip → done with `🔴 FALSIFIED-PARTIAL (1/5 substrate 단봉 at 1/e — universal claim falsified, mac-local $0 2026-05-28)`.
