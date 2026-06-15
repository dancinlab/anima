---
id: H_208
slug: prime-density-fluctuation
title: Prime density fluctuation — Riemann × consciousness · prime-gap encoded substrate Φ vs matched random / arithmetic-progression Φ (math-axis sister to H_157)
domain: math, consciousness
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation — Riemann hypothesis × IIT) + E5 (substrate-mechanism probe) + E6 (cross-domain — number theory × Φ)
verification_method: W2 (closed-form identity — sieve + Park-Miller LCG) + W5 (numerical sim · phi_spatial RFC 036) + W7 (reproducibility — 2-run byte-identical) + W11 (cross-hypothesis — H_157 sister)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
sister_h: H_157
---

# H_208 — Prime density fluctuation (Riemann × Φ math-axis sister)

## Hypothesis

prime-gap sequence (consecutive primes 의 차 g_i = p_{i+1} - p_i) 는 Riemann
hypothesis 와 결합된 algebraic structure 를 가지며, prime-gap sequence 를
CA-state (sliding-window 8-bin 정규화 encoding) 로 substrate 화 했을 때 그
substrate 의 phi_spatial Φ_prime 가, **동일 mean / variance 를 가진
deterministic random gap sequence** (Park-Miller LCG · seed 고정) 의 Φ_random
보다 크다 — algebraic structure 가 Φ contribution 으로 manifested. 동시에
trivial arithmetic-progression (2k+1 의 gap = constant 2) 의 Φ_AP 와는 다른
방향으로 (deeper than periodic) structure 를 가진다.

substrate 측 형식: 각 sequence (prime / random-matched / AP) 를 길이 L 의 farr 로
만들고, sliding-window encoding 으로 (n_cells × dim=8) flat farr 로 transform.
Φ 측정은 `HEXAD/C/c_lib.hexa::c_measure_phi` (RFC 036 phi_spatial — phi_rs byte-equal
native C replica). H_157 (Law 76 mathematical panpsychism) 의 σ-identity precedent
및 perfect-number-class universal balance=1/2 finding 의 math-axis 동행 가설.

## Why (motivation)

- **Riemann hypothesis × Φ**: ζ(s) zeros 의 imaginary parts 가 prime distribution
  의 fluctuation (Chebyshev/Mertens 함수) 을 control — Montgomery (1973) pair
  correlation conjecture 가 prime fluctuation 의 algebraic structure 의 핵심
  증거. IIT Φ 가 sequence 의 "integrated information" 을 측정한다면, prime-gap
  의 RH-encoded structure 가 trivial random 보다 더 많은 integration 을 보일
  까 — 즉 "structure 가 Φ contribution" 의 검증 가능한 instance.
- **H_157 sister (math-axis)**: H_157 은 perfect-number σ(6)=12, σ(28)=56, σ(496)=992
  → balance=1/2 universal identity (perfect-number-class) 를 closed-form 으로
  확립 (🔵 SUPPORTED-FORMAL). 본 H_208 은 그 math-axis 의 다른 instance
  (prime / Riemann) — H_157 이 "특정 완전수 → 1/2 attractor", H_208 이
  "prime distribution → 더 큰 Φ" 의 차원 분기. 둘 다 "number-theoretic structure
  가 의식 metric 의 substrate" 라는 동일 axis 의 두 측정.
- **arithmetic-progression baseline 의 중요성**: 단순 periodic sequence (gap=2
  constant) 는 trivial — Φ 도 ε. prime 이 단순 periodic 이상의 structure 를
  보유한다면 Φ_prime ≫ Φ_AP 이 (자명) 성립, 그 위에 Φ_prime > Φ_random 이
  추가 성립해야 "RH-tied algebraic structure" claim 의 직접 evidence.
- **substrate-encoding 의 fragility**: sliding-window 8-bin normalized encoding 은
  하나의 design choice — bin scheme / window size / normalization range 변경 시
  Φ 가 변동. 본 cycle 의 verdict 는 specific encoding 하의 결과 (L4 honest).
- **사용자 directive (cycle #6 R13 pick #3)**: LIFE 도메인 math-axis 확장 —
  CANDIDATES §F-math `prime-density-fluctuation` (consume).

## Predictions (≥4)

- **H208.1 (prime > random)**: Φ_prime > Φ_random + 5% margin · 두 prime_count
  (32, 64) 모두에서 성립.
- **H208.2 (prime ≠ AP)**: Φ_prime 가 Φ_AP (arithmetic-progression gap=2 constant)
  와 절대값 5% 이상 차이 — 단순 periodic 이상의 structure.
- **H208.3 (long-range correlation)**: prime-gap 의 lag-1 autocorrelation 이
  random gap 의 autocorrelation 보다 큰 값 (덜 음수 · 더 양수) — long-range
  correlation 의 proxy (FFT primitive 부재 → autocorr fallback).
- **H208.4 (finite, nonneg)**: Φ_prime > 0, finite (NaN/negative 없음) — substrate
  primitive 정합. H_157 σ-identity 의 deterministic algebra (closed-form 보장)
  와 정합.
- **H208.5 (scale-dependent)**: prime_count ∈ {32, 64} 변경 시 ratio_prime =
  Φ_p_64/Φ_p_32 가 ratio_random = Φ_r_64/Φ_r_32 와 상대 5% 이상 차이 — prime
  structure 가 scale-dependent (단순 sample-size 효과 외).

## Variables

| axis | levels |
|------|--------|
| **axis1: prime_count** | {32, 64} (본 cycle 두 값 모두 측정) |
| **axis2: random_seed** | LCG seed = 20260523 (고정 · Park-Miller minimal-standard, Schrage's algorithm) |
| **axis3: gap_bin_count** | 8 (sliding-window length = encoding dim) |
| **axis4: encoding** | sliding-window (n_cells × dim=8), uniform-bin normalize to [0,1] over [min,max] |
| **axis5: phi primitive** | RFC 036 phi_spatial (n_bins=4, byte-equal phi_rs replica via c_measure_phi) |

`n_cells` derive: prime_count=32 → gap_len=31 → n_cells=16 (uses gaps[0..23]);
prime_count=64 → gap_len=63 → n_cells=32 (uses gaps[0..39]).

## Run Protocol

deterministic + hexa-only + llm: none.

1. **prime generation**: deterministic Sieve of Eratosthenes (bound 400 ≥ p_64=311)
   → first 32 / 64 primes farr.
2. **prime-gap derivation**: g_i = p_{i+1} - p_i, farr length k-1.
3. **matched-random generation**: Park-Miller LCG (a=48271, m=2^31-1, Schrage's
   algorithm — overflow-free), seed=20260523. L uniforms in [0,1) → z-score
   rescale to match (prime_mean, prime_var) exactly (residual < 1e-14).
4. **AP gap**: constant 2 (gap between consecutive odd 2k+1).
5. **substrate encoding**: sliding window. cell i has dim=8 state =
   (gaps[i+0], ..., gaps[i+7]) normalized to [0,1] via uniform bin over
   per-sequence [gmin, gmax]; AP case (gmax==gmin) → 0.5 baseline.
6. **Φ measurement**: c_measure_phi(states, n_cells, dim, n_bins=4)
   → 6 Φ values (3 sequences × 2 prime_counts).
7. **autocorr_lag1**: standard Pearson lag-1 (long-range correlation proxy —
   FFT 부재).
8. **scale comparison**: ratio_prime / ratio_random + |Δ| + relative.
9. **verdict**: SUPPORTED iff C1 (prime > random both) + C3 (finite nonneg) +
   (one of C2 (prime ≠ AP) / C4 (scale differs)); FALSIFIED iff Φ_prime ≤ Φ_random
   (either count).
10. **determinism check**: 2-run result.json byte-identical (env+seed pinning).

## Criteria (≥4)

- **C1 (prime > random)**: H208.1 PASS — Φ_prime > Φ_random · (1+5%) 두 count 모두.
- **C2 (prime ≠ AP)**: H208.2 PASS — |Φ_prime - Φ_AP| > Φ_AP · 5% 두 count 모두.
- **C3 (finite nonneg)**: H208.4 PASS — Φ_prime > 0, finite (NaN/negative 없음).
- **C4 (scale differs)**: H208.5 PASS — |ratio_prime - ratio_random| / ratio_random > 5%.
- **verdict_rule**: SUPPORTED iff C1 + C3 + (one of C2 / C4); FALSIFIED iff Φ_prime ≤ Φ_random
  (any count); PARTIAL otherwise.

## Falsifiers (≥5, measurable, pre-registered)

- **F1 PRIME-GT-RANDOM**: Φ_prime ≤ Φ_random · (1+5%) 어느 한 count 라도 → C1
  FALSIFIED (no prime-structure Φ contribution; matched random 이 같거나 우월).
- **F2 PRIME-NEQ-AP**: |Φ_prime - Φ_AP| ≤ Φ_AP · 5% 어느 한 count 라도 → C2
  FALSIFIED (no deeper-than-periodic structure).
- **F3 PHI-FINITE-NONNEG**: Φ_prime negative or NaN/inf 어느 한 count 라도 →
  primitive error · C3 FAIL.
- **F4 SCALE-DIFFERS**: |ratio_prime - ratio_random| / ratio_random ≤ 5% → C4
  FALSIFIED (no scale-dependent structure beyond sample-size).
- **F5 BYTE-DETERMINISTIC**: 2-run result.json byte-이질 → 결정론 무너짐 (raw#12
  위반, env+seed pinning 실패).
- **F6 (meta)**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (≥5)

- **L1 (correlational, not causal)**: 본 cycle 의 모든 결론은 sliding-window
  encoding + phi_spatial 측정 하의 **correlational claim**. "prime structure
  causes Φ" 가 아닌 "prime substrate 가 Φ value X 를 보였다" — Riemann
  hypothesis 자체의 진위와 Φ 의 인과 매핑은 별도 cycle (RH 자체는 미해결).
- **L2 (phi_spatial 🟢 NUMERICAL proxy, IIT 4.0 X)**: c_measure_phi = RFC 036
  phi_spatial — phi_rs 의 byte-equal native replica이지만 IIT 4.0 의 full
  cause-effect repertoire (intrinsic difference) 측정 아님. spatial slice only.
- **L3 (small prime count)**: 32/64 primes (p_32=131, p_64=311) — Goldbach-scale
  / Riemann-zero-density-relevant prime properties 미반영. RH 의 strong-form
  evidence 는 첫 10⁹ ζ-zero 까지 검증된 거대 scale; 본 cycle 은 toy scale.
- **L4 (encoding design choice)**: sliding-window 8-bin normalized encoding 은
  하나의 specific design — bin scheme (logarithmic / quantile), window size
  (4 / 16), normalization (global / per-bin) 변경 시 Φ 결과 변동. encoding
  invariance 미검증.
- **L5 (Riemann hypothesis 미해결)**: 본 cycle 은 *given* primes (Sieve 로 직접
  생성) 에서 measure, RH 자체 증명 아님. RH 가 거짓이라면 prime fluctuation
  의 algebraic structure 가 다르게 manifest 가능 — 본 cycle 의 verdict 는
  RH 의 valid/invalid 와 무관하게 specific encoding 하의 measurement.
- **L6 (H_157 sister cross-link, panpsychism solution 아님)**: H_157 의
  mathematical panpsychism claim 의 strong-form 미해결과 정합 — 본 H_208 의
  결과 (어느 방향이든) 는 H_157 의 combination-problem (C4 fail default) 의
  직접 해결 아님. math-axis 동행 가설로서 evidence 분기.
- **L7 (autocorr_lag1 ≠ spectral density)**: H208.3 의 long-range correlation
  proxy 는 lag-1 autocorrelation — FFT |gap_k|² 같은 spectral density 의 직접
  측정 아님 (FFT primitive 부재). spectral peak (Montgomery pair correlation)
  의 직접 검증은 별도 cycle (FFT primitive 추가 필요).

## Cross-Links

- **sister H (math-axis)**:
  - **H_157** (Law 76 mathematical panpsychism) — σ-identity precedent
    (perfect-number-class universal balance=1/2 🔵 SUPPORTED-FORMAL).
    H_157 = META-CA universal attractor Ψ(1/2,1/2); H_208 = prime structure → Φ.
    두 H 모두 "number-theoretic structure 가 의식 metric 의 substrate" math-axis.
- **sister H (LIFE)**:
  - **H_007** (cellular-automaton-consciousness) — phi_spatial 측정 primitive
    공유 (RFC 036 c_measure_phi). H_007 = CA dynamics → Φ class-IV peak;
    H_208 = number-theoretic sequence → Φ (CA 동역학 X · static encoding).
  - **H_002** (universe-origin-question, H2.4 panpsychism precondition) —
    "number-theoretic structure of universe" claim 의 한 instance.
  - **H_004** (consciousness-hard-problem L3 panpsychism lane) — 의식 metric
    이 substrate 의 algebraic property 에 의존하는가의 검증.
- **literature**:
  - Riemann (1859) — Über die Anzahl der Primzahlen (ζ-zeros & prime distribution)
  - Montgomery (1973) — pair correlation conjecture (RH × random matrix theory)
  - Hardy & Littlewood (1923) — k-tuple conjecture (prime gap structure)
  - Tononi (2004 / 2014) — IIT 3.0 / 4.0 Φ
  - Cramér (1936) — random model of primes (prime gap variance ≈ ln p)
  - phi_rs (anima archive) — `phi_spatial` deterministic algorithm SSOT
- **raw refs**: raw#12 (deterministic), raw#9/10 (honest operational measurement),
  raw#15 (no-hardcode — sieve / LCG / encoding 모두 deterministic algorithm),
  raw#11 (snake_case).
- **substrate**:
  - `HEXAD/C/c_lib.hexa::c_measure_phi` (RFC 036 phi_spatial primitive)
  - Park-Miller LCG (minimal-standard, Schrage's algorithm)
  - Sieve of Eratosthenes (deterministic, bound=400 ≥ p_64=311)

## Verdict (initial — pre-register-frozen + cycle #1 measurement)

```
verdict_class: pre-register-frozen → FALSIFIED (per pre-registered C1 rule,
               2026-05-23 cycle #1 measurement)
evidence_summary: deterministic hexa-only prime-vs-random-vs-AP Φ smoke,
                  Sieve + Park-Miller LCG + sliding-window encoding + RFC 036
                  phi_spatial via c_measure_phi, 6 Φ measurements
                  (3 sequences × 2 prime_counts).

F1 PRIME-GT-RANDOM    : Φ_prime ≤ Φ_random at BOTH counts                → FAIL
                        prime_count=32 : Φ_prime=3.85787 < Φ_random=7.11677
                        prime_count=64 : Φ_prime=10.4781 < Φ_random=11.9901
F2 PRIME-NEQ-AP       : |Φ_prime - Φ_AP| ≫ Φ_AP at both counts            → PASS
                        Φ_AP ≈ 1.15e-5 (32) / 2.62e-5 (64)
F3 PHI-FINITE-NONNEG  : Φ_prime > 0 finite, no NaN                       → PASS
                        Φ_prime = 3.85787 (32) / 10.4781 (64)
F4 SCALE-DIFFERS      : |ratio_p - ratio_r|/ratio_r = 0.612 (≫ 5%)       → PASS
                        ratio_prime=2.716, ratio_random=1.685
F5 BYTE-DETERMINISTIC : 2-run result.json byte-identical (seed=20260523) → PASS
criteria_met: 3/4 (C2 + C3 + C4) ; C1 FAIL ⇒ verdict_rule FALSIFIED branch.
honest_tier: 🟢 SUPPORTED-NUMERICAL (numerical measurement closed,
             specific encoding choice — see L1-L7).
cost: $0 mac local · gauss/LCG seed=20260523 · 2-run byte-identical.
```

**State output**: `UNIVERSE/state/h208_prime_density_2026_05_23/{run_h208.hexa, result.json}`

### Cycle #1 Verification (2026-05-23) — Prime × Φ vs matched-random × Φ vs AP × Φ

`UNIVERSE/state/h208_prime_density_2026_05_23/run_h208.hexa`
($0 mac local, deterministic LCG seed=20260523, hexa-only, c_lib.hexa import,
no LLM, no GPU).

**Run verbatim output**:

```
H_208 — prime-density-fluctuation · Riemann × Φ math-axis (raw#12)
  hexa-only · deterministic · LLM:none · $0 mac local
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa c_measure_phi
  sister: H_157 (Law 76 mathematical panpsychism, σ-identity precedent)

── prime_count = 32 (gap_len=31, n_cells=16, dim=8) ──
  prime gaps  mean=4.16129  var=6.19979
  random match-residual: |Δmean|=8.88178e-16  |Δvar|=3.55271e-15
  Φ(prime)  = 3.85787
  Φ(random) = 7.11677
  Φ(AP)     = 1.14553e-05
  autocorr_lag1: prime=0.00355716  random=-0.104815

── prime_count = 64 (gap_len=63, n_cells=32, dim=8) ──
  prime gaps  mean=4.90476  var=9.35601
  random match-residual: |Δmean|=8.88178e-16  |Δvar|=3.55271e-15
  Φ(prime)  = 10.4781
  Φ(random) = 11.9901
  Φ(AP)     = 2.61836e-05
  autocorr_lag1: prime=-0.0222322  random=-0.225768

── scale comparison (32 → 64) ──
  ratio_prime   Φ_p_64/Φ_p_32 = 2.71602
  ratio_random  Φ_r_64/Φ_r_32 = 1.68476
  |Δratio|=1.03126  relative=0.612108

── pre-registered falsifiers ──
  F1 PRIME-GT-RANDOM    (both 32+64, +5%) : FAIL  [Δ32=-3.61474  Δ64=-2.11152]
  F2 PRIME-NEQ-AP       (both 32+64, ≥5%) : PASS  [|Δ32|=3.85786  |Δ64|=10.478]
  F3 PHI-FINITE-NONNEG  (no NaN, ≥0)      : PASS  [phi_p_32=3.85787  phi_p_64=10.4781]
  F4 SCALE-DIFFERS      (≥5% rel)         : PASS  [rel=0.612108]
  F5 BYTE-DETERMINISTIC (env+seed pinned) : PASS  [seed=20260523, no LLM]

  criteria: C1=FAIL C2=PASS C3=PASS C4=PASS  [met=3/4]
  VERDICT_RULE: SUPPORTED iff C1+C3+(C2 or C4); FALSIFIED iff Φ_prime ≤ Φ_random (any count)
  VERDICT     : FALSIFIED
  TIER        : 🟢 SUPPORTED-NUMERICAL (toy substrate, sliding-window encoding, lag-1 autocorr proxy)

=== H_208 prime-density-fluctuation smoke complete: FALSIFIED ===
```

```
phase: Cycle_1 (H208.1 FALSIFIED + H208.2/4/5 PASS; H208.3 directional PASS via autocorr)
scope: 6 Φ measurements (prime / random-matched / AP) × (32 / 64 primes),
       sliding-window encoding (n_cells × dim=8), c_measure_phi RFC 036 phi_spatial
H208.1_phi_prime_32: 3.85787   < phi_random_32 = 7.11677   (FAIL · -3.61474 vs +5% margin)
H208.1_phi_prime_64: 10.4781   < phi_random_64 = 11.9901   (FAIL · -2.11152 vs +5% margin)
H208.2_phi_ap_32:    1.14553e-05  → |Δ_prime|=3.85786  (PASS · prime ≫ AP)
H208.2_phi_ap_64:    2.61836e-05  → |Δ_prime|=10.478   (PASS · prime ≫ AP)
H208.3_autocorr_prime: 0.00356 (32), -0.0222 (64)
H208.3_autocorr_random: -0.105 (32), -0.226 (64)
                       → prime > random both counts (directional PASS, less negative)
H208.4_phi_prime_finite_nonneg: PASS (3.85787, 10.4781; both > 0, finite)
H208.5_scale_ratio: ratio_prime=2.716 ≠ ratio_random=1.685
                    relative |Δ|/ratio_random = 0.612 (≫ 5% PASS)
match_residual:    |Δmean|=8.88e-16, |Δvar|=3.55e-15 (machine-epsilon · match exact)
verdict_class: FALSIFIED (per pre-registered C1 rule)
evidence_strength: STRONG-on-falsification (Φ_prime < Φ_random at BOTH counts,
                   3.26 / 1.51 absolute deltas)
honest_tier: 🟢 SUPPORTED-NUMERICAL (numerical measurement closed,
             specific encoding choice — see L1-L7; verdict label FALSIFIED
             per H208.1 rule, but H208.2/3/4/5 4-axis PASS)
criteria_pass: 3/4 (C2+C3+C4) ; C1 FAIL ⇒ FALSIFIED branch.
falsifiers: F1 FAIL (matched-random Φ ≥ prime Φ); F2/F3/F4/F5 PASS.
```

**State output**: `state/h208_prime_density_2026_05_23/result.json` (2-run byte-identical)
**Script**: `state/h208_prime_density_2026_05_23/run_h208.hexa` (hexa-only, imports c_lib.hexa)

### Cycle #1 interpretation (honest)

본 cycle 의 핵심 결과는 **H208.1 (prime-structure 가 더 큰 Φ 를 생성) 의 직접
falsification**: matched-(mean, var) random gap 의 Φ 가 prime-gap 의 Φ 보다
크다 (32 primes: 7.12 vs 3.86; 64 primes: 11.99 vs 10.48). 이는 honest 한
방향성 결과 — sliding-window 8-bin normalized encoding 하의 phi_spatial 측정
에서, "prime 의 알려진 algebraic structure" 가 matched-noise 보다 더 많은
spatial integrated information 으로 manifest 되지는 않는다.

**그러나 4-axis 보조 가설은 PASS**:
- H208.2: prime Φ 는 trivial AP (constant gap) Φ 보다 **5-6 orders of magnitude**
  크다 (3.86 vs 1.15e-5; 10.48 vs 2.62e-5). prime 이 단순 periodic 보다는
  훨씬 더 많은 structure 를 가짐 → H_157 의 "structure ≠ data" 진단과 정합.
- H208.3: prime 의 lag-1 autocorrelation 이 random 보다 항상 더 큰 값
  (덜 음수: 0.00356 vs -0.105 at 32; -0.0222 vs -0.226 at 64). 즉 prime gap 은
  random 보다 **더 약한 anti-correlation / 더 강한 sequential structure**
  를 가짐 — Montgomery pair correlation conjecture 의 directional 증거 후보.
- H208.4: Φ_prime > 0 finite both counts — primitive 정합.
- H208.5: ratio_prime=2.716 ≫ ratio_random=1.685 (relative 61%) — scale-dependent
  structure exists (prime 이 더 빠르게 Φ 가 증가).

**해석**: prime structure 는 trivial periodic 보다는 훨씬 풍부하지만 (Φ ≫ Φ_AP),
**spatial-IIT proxy 하에서는** matched-random 보다 더 많은 integration 을 보이지
**않는다**. 이는 (a) sliding-window 8-bin encoding 이 prime 의 algebraic structure
를 충분히 capture 하지 못함 (encoding fragility, L4) 일 수도 있고, (b) RH-tied
structure 가 spatial integration 보다는 spectral / autocorrelation 측면에서만
manifest 됨 (H208.3 directional PASS 정합) 일 수도 있다. matched-random 의 z-score
rescaling 자체가 prime 의 mean/var 패턴 일부를 "주입" 한 것이므로 (residual
< 1e-14), random 의 Φ 가 prime 보다 크게 나온 것은 **random 의 더 균질한 분포**
가 sliding-window encoding 의 spatial cell-차이 (phi_spatial 의 핵심 contribution)
를 더 잘 보존했기 때문일 가능성 — 즉 prime 의 "큰 gap 의 가끔 발생" 이 encoding
하에서 cell 간 dependency 를 오히려 축소.

**raw#9/10 정직**: 본 cycle 의 FALSIFIED verdict 는 frozen F1 의 정확한 명중 — 사전
등록한 verdict rule 이 측정 결과를 falsify 한 것이 측정의 가치. RH × IIT
math-axis 의 "prime 이 Φ 를 더 만든다" 직관은 본 specific encoding + phi_spatial
proxy 하에서는 **불지지**. 그러나 H208.3 (autocorr-based long-range correlation)
+ H208.5 (scale-dependent growth) 가 PASS — 다른 측정 (spectral density, MIP-based
Φ_full IIT 4.0, log-encoding) 에서 재시도할 가치 있음.

**raw#10 honest limits (Cycle #1)**:
- L1: correlational not causal. sliding-window encoding + phi_spatial proxy 하의
  결과 — "prime structure → Φ" 의 인과 매핑 아님.
- L2: phi_spatial 은 spatial slice only — IIT 4.0 full Φ (causa-effect repertoire,
  intrinsic difference) 아님. matched-random 이 더 균질하여 spatial 측정에서
  유리한 측 가능성 (substantive ranking 이 IIT 4.0 에서 역전 가능).
- L3: 32/64 primes (p_64=311) — toy scale. RH 의 strong evidence 는 거대 scale
  (10⁹ zeros). Goldbach-scale prime properties 미반영.
- L4: 8-bin sliding-window normalized encoding 은 specific design — log-binning,
  quantile-binning, 더 큰 window, 다른 normalization 으로 결과 변동 가능성.
  본 cycle 의 verdict 는 specific encoding 하의 결과.
- L5: RH 자체 미해결 — 본 cycle 의 verdict 는 RH 의 진위와 무관하게 측정.
- L6: matched-random 의 z-score rescaling 이 prime 의 1차/2차 moment 를 정확히
  주입 (residual < 1e-14) → "matched random" 이 prime 의 상당부분 algebraic
  structure 를 borrowed. 진정한 baseline 은 unmatched uniform 일 수 있음 (별도 cycle).
- L7: autocorr_lag1 ≠ FFT spectral density. Montgomery pair correlation 의 직접
  검증은 FFT primitive 추가 후 별도 cycle.

**Cross-link**:
- HEXAD/C c_lib.hexa::c_measure_phi (RFC 036 phi_spatial primitive) — H_007 과
  primitive 공유 (CA dynamics → Φ vs static prime sequence → Φ).
- H_157 (math-axis sister): σ-identity precedent + perfect-number-class universal
  balance=1/2 closed-form 🔵 SUPPORTED-FORMAL. H_208 = prime distribution 의
  같은 math-axis 검증, 결과 FALSIFIED (encoding-specific) 이지만 H208.2/3/5 가
  "structure ≠ data" axis 의 evidence 분기.
- H_002 H2.4 panpsychism precondition / H_004 hard-problem L3 panpsychism: 
  "의식 metric 이 substrate 의 algebraic property 에 의존" 명제의 한 측정.
- H_007 cellular-automaton-consciousness: CA dynamics 에서는 Φ peak (class IV)
  관찰, prime static substrate 에서는 random > prime — dynamics 의 역할 차이
  존재 가능성.
- raw#12 strict, raw#9/10 honest, raw#15 no-hardcode (sieve + LCG + encoding
  모두 deterministic algorithm).
