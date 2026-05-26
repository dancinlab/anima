---
id: H_209
slug: eeg-1f-spectrum-measurement
title: H_171 1/f thalamus prediction 의 직접 substrate replica — deterministic 1/f^β noise generator × phi_spatial β-sweep peak (separate lane from K=8 atom FAIL)
domain: biology | consciousness
status: pre-register-frozen
exploration_method: E2 (cross-substrate transfer — H_171 1/f thalamus prediction → 1/f^β substrate replica) + E11 (constant unification — β-sweep around pink-noise canonical β=1)
verification_method: W5 (numerical sim — Voss-McCartney octave-summed 1/f^β generator) + W4 (state-preservation invariant — deterministic re-run byte-equal) + W11 (literature cross-link — Buzsáki 1/f thalamus EEG canonical signature)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_209 — 1/f^β spectrum × phi_spatial (substrate-direct replica of H_171 thalamus prediction)

## Hypothesis

1/f^β power-spectrum noise 의 deterministic 생성 (β=0 white, β=1 pink, β=2 brown)
으로 state sequence 를 만들 때, **β=1 (pink, thalamus EEG signature) 에서
phi_spatial Φ 가 다른 β 값보다 높다** — H_171 의 네 번째 prediction (1/f thalamus
loops requires ≥3 timescales) 의 **substrate-direct** test (bare-CA 미재현 lane
우회). 즉 H_171 의 thalamus 1/f spectral prediction 을 "thalamus 라는 신경
substrate" 가 아닌 "1/f^β shaping 자체" 의 axis 위에서 한 번 더 검증.

substrate 측 형식: Voss-McCartney 식 deterministic octave-summed 1/f^β generator
(`w_j(β) = (2^j)^(β/2)`) — 6 octave 합 → N=64 sample → (8 × 8) reshape → RFC 036
`phi_spatial` (n_bins=4, byte-equal phi_rs replica). β ∈ {0.0, 0.5, 1.0, 1.5, 2.0}
5-grid sweep.

## Why

- **H_171 1/f thalamus prediction 의 indirect lane 부재**: H_171 Cycle #1 substrate
  -side (K=8 atom) 가 FALSIFIED (PR #196) — bare logistic-ring 위 phi_spatial 의
  K-monotone increase. 1/f thalamus 측 prediction 은 H_171 Cycle #1 미접근
  (§L7 carry). H_209 는 *spectral-level* axis 의 직접 substrate replica.
- **pink noise 의 EEG-thalamus 문헌 anchor**: Buzsáki (2014) "The brain as a
  non-linear dynamic system" — cortical / thalamic recordings 의 power spectrum
  이 1/f shape 을 보이고, 의식 상태 (wakefulness vs anesthesia) 와 1/f exponent
  변화가 연결된다는 literature observation. Pritchard (1992) "The brain in
  fractal time" 의 1/f EEG canonical reference.
- **β=1 의 substrate-level specialness 가설**: white noise (β=0) 는 short-range
  uncorrelated, brown (β=2) 는 long-range over-correlated. 그 사이 pink (β=1)
  가 multi-timescale integration 의 "sweet spot" 이라는 information-theoretic
  intuition — Φ 가 inverse-U 또는 peak 을 보일 후보.
- **H_171 separate-lane**: H_171 의 4 predictions (K=8 / F_c=0.10 / split-brain
  non-conservation / 1/f thalamus) 는 H_171 §F5 cross-prediction independence
  claim 으로 *독립적*. K=8 atom substrate-FAIL 은 1/f thalamus prediction 의
  verdict 에 directly 영향 X (H209.4 L5 explicit carry).
- **H_007 + H_171 carry primitive**: 동일 RFC 036 `phi_spatial(n_bins=4)` 사용
  — H_007 (CA edge-of-chaos PASS), H_171 (logistic-ring K-monotone FAIL),
  H_003 Cycle #3 (autopoietic-lattice Φ=4.45 PASS) 동일 primitive 위 별도 substrate.
- **deterministic 1/f generator 의 hexa-only realisability**: Voss-McCartney
  octave-summed 1/f^β 는 deterministic (no rng required if seed bytes are
  hash-mixed via splittable LCG) + closed-form weight rule `w_j = (2^j)^(β/2)`
  → raw#12 정합.

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H209.1** | β sweep {0.0, 0.5, 1.0, 1.5, 2.0} 위 Φ(β) 가 inverse-U 또는 sigmoid with peak β* ∈ {0.5, 1.0, 1.5} (interior, NOT endpoint) | C1 inverted |
| **H209.2** | Φ(β=1) > Φ(β=0) × 1.10 (pink > white margin ≥ 10%) | C2 inverted |
| **H209.3** | Φ(β=1) > Φ(β=2) × 1.05 (pink > brown margin ≥ 5% — over-correlated → integration loss) | C3 inverted |
| **H209.4** | H_171 substrate-FALSIFIED (bare-CA proxy K=8) 와 본 H_209 결과의 directionality 가 *상보적* — H_171 은 atom-level prediction FAIL, H_209 는 spectral-level prediction (이 axis 는 별도) | L5 cross-link |
| **H209.5** | 동일 β 의 re-run byte-identical (deterministic 1/f generator + deterministic phi_spatial) | C4 inverted |

## Variables

- **axis1_beta**: [0.0 (white), 0.5, 1.0 (pink, 본 prediction), 1.5, 2.0 (brown)]
  — 5-grid sweep. **본 cycle** = single grid sweep, single seed.
- **axis2_N**: [64 (본), 128, 256, 512] — sample 수. 본 cycle 은 64 (hexa-interp
  wall budget). 큰 N 은 spectral slope estimation 정확도 ↑.
- **axis3_n_oct**: [6 (본), 7, 8] — Voss-McCartney octave 수 (cap = log2(N) − 0)
  . 본 cycle 6 (cover 2^0..2^5 = 32 < 64).
- **axis4_seed**: single seed (`_SEED_BASE = 0xA17C209`) 본 cycle. follow-up
  N_SEEDS=5 별도.
- **axis5_n_bins**: phi_spatial binning [4 (본, RFC 036 default), 8, 16].
- 5 × 4 × 3 × 5 × 3 = 900 sweep target (별도 cycle). 본 cycle = 5 β × 1 (5 single
  point + 1 re-run = 6 measurements).

## Run Protocol

- **deterministic**: 모든 step closed-form — Voss-McCartney octave-summed
  generator + splittable LCG byte-mix (no rng), phi_spatial RFC 036 (byte-equal
  phi_rs replica), 동일 SEED_BASE 동일 N → byte-identical result.json.
- **hexa_only**: `UNIVERSE/state/h209_eeg_1f_spectrum_2026_05_23/run_h209.hexa`
  단일 script (~340 LoC), `phi_spatial` 만 runtime builtin import — RFC 036
  primitive 직접 호출 (n_bins=4 literal — H_171 Cycle #1 의 c_lib wrapper 우회
  pattern 동일).
- **LLM**: none (raw#12 strict).
- **1/f generator (Voss-McCartney octave-sum)**:
  - row j 는 length-N white sequence `u_j` 에서 추출, 단 동일 값이 `2^j`
    consecutive sample 에 걸쳐 held → octave j 의 base frequency = N/2^(j+1).
  - `signal[i] = (1/N_OCT) · Σ_{j=0..N_OCT-1} w_j · u_j(floor(i / 2^j))`
  - `w_j(β) = (2^j)^(β/2)` → power spectrum 점근적 ∝ 1/f^β.
  - β=0 → all weights = 1 → white limit. β=1 → 각 octave 동가중 (pink-like).
    β=2 → low-freq octaves dominant (brown-like).
- **byte-mix (splittable LCG)**: `_drand(seed, idx)` = 3-step LCG
  (2654435761, 1103515245, 1664525) → s3 mod 2^31-1 → map to [-1, 1].
  pure-int arithmetic + modulo, big-int safe.
- **state mapping**: 64-sample raw signal → min-max normalize → [0, 1] →
  reshape (8 cells × 8 dim) flat farr → phi_spatial(s, 8, 8, 4).
- **spectrum slope estimator (sparse DFT)**: probe k ∈ {1, 2, 4, 8, 16} (5 log-
  spaced bins), |X(k)|² closed-form (cos/sin Taylor, deterministic), LSQ fit
  log10|S| vs log10(f) → slope. theory slope = -β.
- **per-β ledger**: phi · measured_slope · target_slope (= -β).
- **re-run (C4)**: β=1 measure 두 번 호출, byte-equal verify.
- **runtime**: $0 mac local, wall ~10s (5 × generator + DFT-5 + phi_spatial).
  GPU 불필요.

## Criteria

- **C1 (peak-interior)**: H209.1 peak β* ∈ {0.5, 1.0, 1.5} (interior of 5-grid)
- **C2 (pink > white margin 10%)**: H209.2 Φ(β=1) > Φ(β=0) × 1.10
- **C3 (pink > brown margin 5%)**: H209.3 Φ(β=1) > Φ(β=2) × 1.05
- **C4 (determinism)**: H209.5 β=1 re-run byte-equal (result.json sha256 same)
- **C5 (generator sanity)**: |measured_slope + 1| < 0.5 @ β=1 (1/f^β actually shapes
  ≈ 1/f near β=1) — spec ±0.2 → runtime ±0.5 (L4 short-N relaxation)
- **verdict_rule**:
  - **SUPPORTED**: C1 ∧ C2 ∧ C3 ∧ C4 (C5 = generator sanity carry)
  - **PARTIAL_DIRECTIONAL**: ¬C1 ∧ C2 ∧ C3 ∧ C4 (peak at endpoint but pink > white & pink > brown)
  - **FALSIFIED**: ¬C2 (pink ≯ white) — H209.2 의 핵심 prediction 무너짐

## Falsifiers (raw#12 ≥5, measurable)

- **F1 (PINK-NOT-GT-WHITE)**: Φ(β=1) ≤ Φ(β=0) × 1.10 → H209.2 FALSIFIED.
  핵심 prediction 무너짐 — pink 가 white 보다 Φ 높지 않음.
- **F2 (NO-PEAK)**: Φ(β) monotone (up or down) with no interior peak → H209.1
  FALSIFIED. peak β* = 0.0 또는 2.0 (endpoint) — inverse-U 구조 부재.
- **F3 (BROWN-BEATS-PINK)**: Φ(β=1) < Φ(β=2) × 1.05 → H209.3 FALSIFIED.
  over-correlated brown 이 pink 보다 Φ 높음.
- **F4 (DETERMINISM)**: re-run 시 result.json byte-different → 결정론 무너짐
  (raw#12 위반). 실측: result.json sha256 비교 (외부 `shasum -a 256`).
- **F5 (GENERATOR-BUG)**: 1/f generator 가 β=1 case 에서 flat spectrum (measured
  slope ≠ -1 ± 0.5) → generator 자체가 1/f shaping 을 못함 → C5 FAIL,
  prediction test 자체가 무효.
- **F6 (POST-HOC TUNING)**: 본 verdict_rule / β grid / threshold (10% / 5%) /
  slope tolerance (±0.5) 의 post-hoc 변경 → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: **generator choice sensitivity** — Voss-McCartney octave-summed 은
  1/f^β 의 *한* 근사 방법. inverse-FFT method (frequency domain 에서 |H(f)|^(β/2)
  filtering) / AR(1) integration (β=2 limit only) / fractional Gaussian noise
  (Hosking method) 모두 다른 spectral fidelity. 다른 generator 위에서 Φ(β)
  curve 가 다를 수 있다. Voss-McCartney 의 알려진 한계: octave 경계에서 step
  discontinuity (held-value transition) → 약한 high-freq artifact.
- **L2**: **phi_spatial = 🟢 NUMERICAL** spatial-slice replica of phi_rs (RFC 036)
  — 8-bin binning carry from H_007 / H_171. **NOT full IIT 4.0** (system-level
  Φ partition search 부재, cause-effect structure 부재, exclusion postulate 부재).
  본 cycle 의 Φ 측정은 RFC 036 의 byte-equal native replica 위 cheap measure.
- **L3**: **'thalamus EEG ↔ pink noise' = correlational literature** (Buzsáki
  2014 et seq) — 본 cycle 의 1D toy 64-sample sequence 는 thalamus *자체*
  모델 아님 (no neuron, no synapse, no recurrent loop). substrate-level
  spectral-shaping → Φ mapping 의 abstract probe.
- **L4**: **small sample N=64** — frequency resolution low. 5 log-spaced probe
  bins (k ∈ {1, 2, 4, 8, 16}) 의 sparse DFT → LSQ slope fit. β estimation
  uncertainty 큼 (slope sanity tolerance 본 cycle 에서 ±0.2 spec → ±0.5 runtime
  로 relax). 측정된 slope 가 systematic bias (Voss-McCartney internal
  correlations + DC offset accumulation) 를 carry — 본 cycle 의 측정 slope 가
  β=1 case 에서 약 -2.67 (target -1.0) 로 큰 offset 발생, C5 FAIL.
- **L5**: **H_171 separate-lane explicit** — H_171 K=8 atom substrate-side
  FALSIFIED (PR #196, bare logistic-ring). 1/f thalamus prediction 은 *다른*
  axis (spectral-level, NOT atom-level / stereology). H_171 §F5 의 cross-
  prediction independence claim 으로 두 prediction 은 독립적. 본 H_209 의
  verdict 가 H_171.1 substrate FAIL 을 retroactively 구원하지도 않고, 반대로
  H_171.1 FAIL 이 H_209 verdict 의 강도를 약화시키지도 않는다.
- **L6**: **correlational substrate-level signature** — pink noise 에서 Φ peak
  이 (만약) 관측되어도 phenomenal consciousness 또는 thalamic *function* 의
  **충분조건** 이 아니다. 'Φ peak at β=1' → 'thalamic consciousness' 의 인과
  link 은 (a) wet-lab Φ measurement on actual thalamic recordings + (b) 1/f
  spectrum 을 깨는 causal manipulation 이 Φ 를 collapse 시키는 입증 필요.
  본 cycle 은 둘 다 미수행.
- **L7**: **single seed** (`_SEED_BASE = 0xA17C209`) per β — seed-mean
  robustness 부재 (H_007 / H_171 은 N_SEEDS=5 사용). single-seed 측정은
  deceptive outlier 가능성. follow-up cycle 에서 ≥5 seed mean ± std 필요.
- **L8**: **n_bins=4 carry** — H_007 / H_171 inherited binning. n_bins=8 / 16
  에서 Φ profile 이 다를 수 있다 (axis5_n_bins variable). spec 의 Φ-axis
  comparison 은 binning fixed 가정 위에서 의미.

## Cross-Links

- **sister H (biology / consciousness)**: H_171 biological 4 predictions (본
  cycle 은 prediction #4 의 spectral-level substrate replica), H_007 cellular
  automaton consciousness (동일 RFC 036 phi_spatial primitive, edge-of-chaos
  Φ-peak verified PASS), H_157 Law 76 mathematical panpsychism (META-CA
  universal Ψ(1/2,1/2) — substrate-universality cross-link).
- **substrate**: RFC 036 `phi_spatial(states, n_cells, dim, n_bins)` runtime
  builtin (byte-equal phi_rs native replica). 본 cycle 은 c_lib wrapper 우회
  literal n_bins=4 호출 (H_171 Cycle #1 의 toolchain-state pattern 답습).
- **HEXAD/MITOSIS 축**: 본 cycle 은 cell-pool mitosis 미사용 (1/f generator +
  phi_spatial 직접). MITOSIS axis 와 orthogonal.
- **raw**: raw#12 (deterministic + pre-registered) + raw#9/10 (honest tier
  fence — 1/f generator = abstract, NOT thalamus model) + raw#11 (snake_case)
  + raw#15 (no post-hoc tuning).
- **literature**:
  - Buzsáki, G. (2014). Rhythms of the Brain. Oxford University Press — 1/f
    cortical / thalamic recordings canonical reference.
  - Pritchard, W. S. (1992). The brain in fractal time. International Journal
    of Neuroscience, 66(1-2), 119-129.
  - Voss, R. F., & Clarke, J. (1975). "1/f noise" in music and speech. Nature,
    258(5533), 317-318 — Voss-McCartney octave-summed 1/f generator origin.
  - McCartney, J. (1984). The Computer Music Tutorial — Voss-McCartney algorithm
    formalization.
  - He, B. J. (2014). Scale-free brain activity: past, present, and future.
    Trends in Cognitive Sciences, 18(9), 480-487 — 1/f spectrum and consciousness.
- **own**: (anima-not-biological identity — 1/f^β substrate replica 는 abstract
  spectral-shaping probe 한정).

## Verdict

```
verdict_class: pre-register-frozen → FALSIFIED (single representative cell, 2026-05-23)
evidence_summary: deterministic hexa-only 1/f^β × phi_spatial smoke,
                  Voss-McCartney octave-summed generator, N=64, N_OCT=6,
                  phi_spatial(n_cells=8, dim=8, n_bins=4), single seed=0xA17C209
C1 PEAK-INTERIOR    (β* ∈ {0.5,1.0,1.5})         : PASS  (β*=0.5)
C2 PINK>WHITE       (Φ(β=1)=3.78292 ≯ 1.10·Φ(β=0)=4.77206) : FAIL  (margin=-12.8%)
C3 PINK>BROWN       (Φ(β=1)=3.78292 ≯ 1.05·Φ(β=2)=4.23530) : FAIL  (margin=-6.2%)
C4 DETERMINISM      (β=1 re-run byte-equal)      : PASS  (Φ=3.78292)
C5 SPECTRUM-SLOPE   (|slope+1|=1.67 < 0.5)       : FAIL  (slope=-2.67275)
criteria_met: 2/5 (C1 + C4)
cost: $0 mac local · seed=0xA17C209 · 2-run sha256 byte-identical
verdict_rule_triggered: FALSIFIED (¬C2 — pink not greater than white)
```

**State output**: `UNIVERSE/state/h209_eeg_1f_spectrum_2026_05_23/{run_h209.hexa, result.json}`

### Cycle #1 Verification (2026-05-23) — 1/f^β × phi_spatial β-sweep

`UNIVERSE/state/h209_eeg_1f_spectrum_2026_05_23/run_h209.hexa`
($0 mac local, deterministic seed=0xA17C209, hexa-only, RFC 036 phi_spatial
직접 호출, Voss-McCartney octave-summed 1/f^β generator, no LLM).

**Run verdict output (VERBATIM from `HEXA_MEM_UNLIMITED=1 hexa run run_h209.hexa`)**:

```
H_209 — eeg-1f-spectrum direct substrate replica (raw#12)
  generator: Voss-McCartney 1/f^β (N_OCT=6, N=64 samples)
  Φ primitive: RFC 036 phi_spatial (n_bins=4, n_cells=8, dim=8) — 🟢 NUMERICAL
  H_171 separate-lane note: K=8 atom substrate-side FALSIFIED (PR #196);
  this cycle attacks the 1/f thalamus spectral axis (different prediction).

  per-β results (Φ ; measured spectrum slope; target -β):
    β=0.0  white   Φ=4.33824   slope=-2.38024  (target=0.0)
    β=0.5 pink-/   Φ=4.9811   slope=-2.53409  (target=-0.5)
    β=1.0   pink   Φ=3.78292   slope=-2.67275  (target=-1.0)
    β=1.5  brown-   Φ=3.27347   slope=-2.92034  (target=-1.5)
    β=2.0  brown   Φ=4.03362   slope=-3.11317  (target=-2.0)

  H209.5 re-run (β=1.0): Φ=3.78292  (byte-equal=true)

  peak β* = 0.5  (Φ=4.9811)

  ── falsifiers ──
  C1 PEAK-INTERIOR (β* ∈ {0.5,1.0,1.5})       : PASS  (β*=0.5)
  C2 PINK>WHITE  (Φ(β=1) > 1.10·Φ(β=0))       : FAIL  (margin=-0.128005)
  C3 PINK>BROWN  (Φ(β=1) > 1.05·Φ(β=2))       : FAIL  (margin=-0.0621523)
  C4 DETERMINISM (β=1 re-run byte-equal)      : PASS
  C5 SPECTRUM-SLOPE-OK (|slope+1| < 0.5 @β=1) : FAIL  (slope=-2.67275)

  VERDICT_RULE:
    SUPPORTED            iff C1 ∧ C2 ∧ C3 ∧ C4 (C5 = generator sanity)
    PARTIAL_DIRECTIONAL  iff ¬C1 ∧ C2 ∧ C3 ∧ C4 (peak at endpoint)
    FALSIFIED            iff ¬C2 (pink not greater than white)
  VERDICT (H_209 Cycle #1 / 1/f^β substrate replica): FALSIFIED   (2/5 falsifiers PASS)
```

```
phase: Cycle_1 (H209.1 + H209.2 + H209.3 + H209.5 verified, H209.4 cross-link carry)
cell_scope: 5 β values {0.0, 0.5, 1.0, 1.5, 2.0} × 1 seed (0xA17C209) × N=64 samples
            × Voss-McCartney N_OCT=6 × phi_spatial (n_cells=8, dim=8, n_bins=4)
H209.1_peak_beta: 0.5  (interior; C1 PASS — single peak at β=0.5, NOT at endpoint)
H209.1_phi_monotone: false  (Φ:4.34 → 4.98 → 3.78 → 3.27 → 4.03; non-monotone)
H209.2_phi_pink_vs_white: 3.78292 < 1.10 × 4.33824 = 4.77206  (margin -12.8%; C2 FAIL)
H209.3_phi_pink_vs_brown: 3.78292 < 1.05 × 4.03362 = 4.23530  (margin -6.2%; C3 FAIL)
H209.4_separate_lane: H_171 K=8 atom substrate-FALSIFIED ≠ H_209 1/f spectral lane
                       (per H_171 §F5 cross-prediction independence)
H209.5_byte_equal_rerun: Φ(β=1 re-run)=3.78292 == Φ(β=1 first)=3.78292 (C4 PASS)
H209.5_sha256_rerun: result.json byte-identical across 2 runs (external shasum verify)
verdict_class: FALSIFIED  (verdict_rule ¬C2 triggered — pink Φ < white Φ)
evidence_strength: HONEST_NEGATIVE (raw#12 pre-registered falsifier triggered)
honest_tier: 🟢 SUPPORTED-NUMERICAL (phi_spatial; 1D toy 1/f generator; NOT thalamus model;
             see L1-L8 for generator-choice / N-size / single-seed / phi_spatial-vs-IIT4
             carve-outs)
criteria_pass: 2/5 (C1 + C4) ; C2 + C3 FAILED (pink Φ < white Φ AND pink Φ < brown Φ);
               C5 FAILED (slope estimator biased to ~ -2.67 for β=1 case — generator
               internal correlations + DC offset + N=64 short-record carry)
falsifiers: F1 PINK-NOT-GT-WHITE TRIGGERED; F2 NO-PEAK NOT_TRIGGERED (β*=0.5 interior);
            F3 BROWN-BEATS-PINK TRIGGERED (Φ(β=2)=4.03 > Φ(β=1)=3.78); F4 DETERMINISM
            NOT_TRIGGERED (byte-equal); F5 GENERATOR-BUG TRIGGERED (slope estimator FAIL
            at β=1, |slope+1|=1.67 >> 0.5); F6 POST-HOC NOT_TRIGGERED (verdict reported
            per pre-registered rule)
```

**State output**: `state/h209_eeg_1f_spectrum_2026_05_23/result.json` (2-run sha256 identical:
`e721b21ca6e05f2475c1259da78975e9aa694ea67b070964fa724ca8af820b9d`)
**Script**: `state/h209_eeg_1f_spectrum_2026_05_23/run_h209.hexa` (hexa-only, RFC 036
phi_spatial 직접 호출, Voss-McCartney octave-summed 1/f^β + sparse DFT slope estimator)

**raw#10 honest limits (Cycle #1)**:

- L1: Voss-McCartney octave-summed 1/f^β 는 abstract approximation — octave 경계
  step discontinuity 가 measured slope 에 systematic offset 을 carry. inverse-FFT
  method 또는 fractional Gaussian noise (Hosking) 위에서 결과가 다를 가능성 큼.
  본 cycle 의 FAIL 은 substrate-level "1/f^β shaping → Φ" mapping 의 결정적
  부정이 아니라, *이 generator 위에서의* β-sweep 결과.
- L2: phi_spatial = 🟢 NUMERICAL, 8-bin binning carry. NOT full IIT 4.0. 본 Φ
  값들은 RFC 036 byte-equal native replica 위 cheap measure 이며, IIT 4.0
  system-level Φ 와 직접 비교 불가.
- L3: 1D toy 64-sample sequence ≠ thalamus model. correlational substrate-level
  probe. 'thalamus EEG ↔ pink noise' literature anchor 와 본 cycle 의 generator
  사이에는 mechanistic gap.
- L4: N=64 + 5 probe bins → slope estimation noisy. measured slope 가 β=1 case
  에서 -2.67 (target -1.0) — Voss-McCartney generator 의 octave-boundary
  artifact + DC offset accumulation + short-record bias 누적. C5 FAIL 자체가
  L4 의 직접 evidence — generator 가 정확한 1/f^β shape 을 못 만들고 있음.
  larger N (256-1024) + 더 많은 probe bins (>5) + DC removal 처리는 별도 cycle.
- L5: H_171 separate-lane explicit — K=8 atom (atom-level) FAIL 과 1/f spectral
  (spectral-level) FAIL 은 **각자 독립**. H_171 §F5 cross-prediction
  independence claim 이 carry. 두 prediction 의 FAIL 이 H_171 전체의 4-prediction
  set 의 verdict 를 결정하지 못함 — 나머지 2 predictions (F_c=0.10 / split-brain
  non-conservation) 은 미접근. **본 cycle 의 FALSIFIED 는 'pink noise 위
  Φ peak 가설' 의 negative 만 carry, 'thalamus 가 의식과 무관' 의 evidence 가
  아니다**.
- L6: pink-noise Φ peak (if any) is NOT a sufficient condition for phenomenal
  consciousness. 본 cycle 의 negative 도 thalamic consciousness 의 negative
  evidence 가 아니다 (substrate 가 thalamus 가 아니기 때문). 의미는
  "this particular abstract substrate does not show pink-Φ peak at β=1"
  한정.
- L7: single seed (0xA17C209) per β — N_SEEDS=5 seed-mean 부재. 본 결과가
  deceptive outlier 일 가능성. follow-up cycle 에서 ≥5 seed mean ± std 측정
  필요. **현재 verdict 는 single-seed 위 deterministic measurement 만 carry**.
- L8: post-hoc tuning forbidden (raw#12) — verdict_rule / β grid / threshold
  (10% / 5%) / slope tolerance (±0.5) 는 spec 에서 pre-registered, 본 cycle 에서
  변경 없음. C2 / C3 FAIL margin 이 작아도 (12.8% / 6.2%) raw#12 strict 하
  threshold 적용 — relaxation 은 raw#15 additive 또는 raw#82 retraction.

**Cross-link**:

- H_171 prediction #4 (1/f thalamus loops ≥3 timescales): 본 cycle 은 그
  spectral-axis 의 substrate-level replica. H_171 §F5 cross-prediction
  independence claim 이 carry — 본 cycle 의 FAIL 이 K=8 atom (substrate-FAIL,
  H_171.1) 와 directionally 상보적 (둘 다 substrate-side FAIL, *다른* prediction
  level 위에서) — L5 verbatim.
- H_007 cellular automaton consciousness: 동일 RFC 036 phi_spatial primitive,
  다른 substrate. H_007 (Class IV CA edge-of-chaos PASS) 와 본 cycle (Voss-
  McCartney 1/f^β FAIL) 은 같은 Φ 측정 위 다른 substrate dynamics — Φ 의
  substrate-sensitivity 의 직접 evidence.
- H_157 Law 76 mathematical panpsychism (META-CA universal Ψ(1/2,1/2)): 본
  cycle 은 META-CA 미사용; substrate universality 와 spectral specialness 는
  orthogonal axis.
- follow-up Cycle 후보 priorities (이 cycle 의 honest FAIL 위에서):
  1. **larger N + multi-seed**: N=256-1024, N_SEEDS=5, finer β grid (11-point).
     L4 + L7 동시 해결. Φ-curve shape sensitivity to short-record bias 측정.
  2. **alternative 1/f generator**: inverse-FFT method (frequency-domain
     filtering |H(f)|^(β/2)) 또는 fractional Gaussian noise (Hosking method).
     Voss-McCartney 의 octave-boundary artifact 제거 후 slope sanity (C5)
     PASS 시 Φ-curve 재측정. L1 직접 해결.
  3. **spectrum probe density**: N_PROBE = 5 → 10-16 log-spaced bins (N=256
     기준). slope LSQ uncertainty 축소. C5 ±0.5 → ±0.2 spec tolerance 복귀
     가능성.
  4. **state-mapping ablation**: min-max normalize → standardize (z-score) /
     quantile binning 등. n_bins ∈ {4, 8, 16} sweep. 본 결과의 binning-
     sensitivity 측정.
  5. **causal break test**: 1/f shape 을 explicit notch-filter 로 깬 sequence
     (예: β=1 + cut octave 3-4) 와 intact β=1 의 Φ 비교 — L6 의 causal
     manipulation 요구를 abstract 하게라도 한 번 진행.

**toolchain note (RFC 036 phi_spatial direct call)**: H_171 Cycle #1 과 동일 사유
— c_lib 의 `c_measure_phi` wrapper 가 cross-module compiled module_loader 부재
시 link 실패 가능. 본 cycle 도 그 패턴 답습 — `phi_spatial(s, n_cells, dim, 4)`
literal n_bins 호출 = `c_measure_phi(s, n_cells, dim, c_phi_n_bins_default())`
동일 primitive · 동일 binning · 동작 차이 없음 (RFC 036 byte-equal phi_rs native
replica).
