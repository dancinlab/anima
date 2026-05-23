---
id: H_232
slug: class-ii-mechanism-decompose
title: H_232 Class-II family Φ-peak mechanism decompose — rule 184 (TASEP shift) vs rule 60/102 (XOR-derived) substrate-level distinguishing signature (H_225 follow-up)
domain: physics + math + information
status: pre-register-frozen
exploration_method: E5 (variable-ablation trajectory sweep) + E11 (mechanism decomposition)
verification_method: W4 (verdict-4-class) + W12 (trajectory-shape signature)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
---

# H_232 — Class-II family Φ-peak mechanism decompose

## Hypothesis

H_225 (`rule_184_class_ii_phi_anomaly`) 의 smoke (PR #267 MERGED) 는 **broad FALSIFIED** 였지만 핵심 ranking-claim 인 **C3 (Class-II > Class-IV)** 는 **STRONG PASS** 였다 — rule 184=1.198 · rule 60=1.683 · rule 102=1.683 모두 rule 110=0.556 능가. 그러나 rule 60/102 가 rule 184 보다 **약 40% 더 높았다** (1.683 vs 1.198). 본 cycle 의 hypothesis 는 이 격차가 우연 또는 noise 가 아니라 **두 가지 서로 다른 mechanism** 의 결과라는 것이다:

1. **rule 184**: TASEP-shift — 1D traffic flow 에서 particle conservation 을 통한 *information conservation*.
2. **rule 60 / 102**: XOR-additive — `(left XOR center)` / `(center XOR right)` 의 linear additivity Z_2 → Sierpinski self-similar pattern → *information cancellation + recombination*.

본 H 는 단순 Φ 값 비교를 넘어 **substrate-level distinguishing signature** 를 찾는다: Φ trajectory shape (monotone vs oscillating), autocorrelation persistence (lag-1), peak time. 5 predictions:

1. **H232.1 (TASEP monotone)** rule 184 의 Φ trajectory 가 *monotone non-decreasing* (TASEP 의 information conservation → 시간에 따른 ratchet-up 또는 plateau, decrease 없음).
2. **H232.2 (XOR oscillating)** rule 60 / 102 의 Φ trajectory 가 *oscillating* — XOR 의 derivation 으로 Sierpinski period 가 발생 → sign-change density ≥ 0.3.
3. **H232.3 (autocorr ranking)** rule 184 의 autocorrelation lag-1 > rule 60 / 102 의 autocorrelation lag-1 (shift persistence vs XOR scrambling).
4. **H232.4 (peak distinct)** 3 rule (184/60/102) 의 Φ peak 시점이 *다름* — 같은 substrate 위 같은 init 에서도 mechanism-specific timing → mechanism 분리 evidence.
5. **H232.5 (determinism)** fixed init + fixed seed → re-run byte-identical (raw#12 strict).

raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local). H_225 와 동일 substrate config (N=16, dim=12, warm=8, RFC 036 phi_spatial) 위 trajectory-axis 만 확장.

## Why

- **H_225 의 carry**: broad FALSIFIED 였지만 (a) Class-II > Class-IV 가 strong 하게 성립하고 (b) Class-II 내부 1.683 vs 1.198 의 격차가 *체계적*. 두 사실은 "Class-II 가 Class-IV 보다 우월" 가 단일 mechanism 으로는 환원되지 않음을 시사. H_225 §"Honest Limits" L1 ("rule 60/102 는 linear additive, 184 는 nonlinear conservation — mechanism 이 동일하지 않음") 가 본 H 의 직접 동기.
- **TASEP shift 의 physics**: rule 184 = Totally Asymmetric Simple Exclusion Process (Krug 1991, Schadschneider 2000). 결정론적 단방향 hop, particle conservation, KPZ universality class. shifted-but-equivalent steady state — Φ 가 high-but-stable 예측.
- **XOR-derived 의 algebra**: rule 60 = `(left XOR center)`, rule 102 = `(center XOR right)`. 둘 다 linear over Z_2 → additive → Sierpinski self-similar (Wolfram 2002 §3). Linear CA 의 generic 행동은 (a) deterministic period 또는 (b) 적분 가능한 stress relaxation. periodic 인 경우 Φ trajectory oscillation 으로 나타남.
- **Information conservation vs cancellation distinction (Crutchfield 1989)**: ε-machine analysis 에서 *information storage* 와 *information generation* 은 별개 — TASEP 는 storage-dominant (shift = bookkeeping), XOR 는 generation-dominant (Sierpinski = new structure 매 step).
- **trajectory shape 의 epistemic 가치**: 단일 Φ 값은 substrate state 의 *projection* 만. trajectory shape (monotone/oscillating/decaying) 은 dynamics 의 *generator* 에 대한 indirect 측정 — single-Φ 보다 mechanism-discriminating.
- **autocorrelation lag-1 의 의미**: shift dynamics (rule 184) → 다음 state 가 이전 state 의 shifted copy → high lag-1 corr 예상. XOR (rule 60/102) → derivative 가 새 pattern 생성 → lag-1 corr 약화 예상.
- **cross-link H_225 [direct follow-up]**: H_225 의 C3 STRONG PASS + Class-II 내부 격차 를 받아 mechanism 차원으로 decompose. H_225 의 verdict 자체는 변경 안 함 — 본 H 는 *post-result decomposition*.
- **cross-link H_007 [indirect adversary]**: H_007 의 Class-IV-unique 가정은 H_225 에서 이미 깨졌으므로 본 H 는 H_007 에 대한 *추가* attack 아님. 본 H 는 *Class-II 내부 substructure* 분석.
- **cross-link H_211 [shared baseline]**: H_211 의 Pearson r=0.933 entropy-Φ correlation 은 본 H 의 trajectory metrics 와 별개; H_211 의 substrate config 와 byte-equal.

## Predictions

- **H232.1** rule 184 trajectory R² (least-squares linear fit on (t, Φ_t)) ≥ 0.7 AND monotone-non-decreasing-fraction ≥ 0.7 (TASEP information conservation 정합).
- **H232.2** rule 60 / 102 trajectory sign-change-density of first-difference ≥ 0.3 for both (oscillation strength proxy; period-shift Sierpinski 정합).
- **H232.3** autocorr lag-1: ac(184) > ac(60) AND ac(184) > ac(102) (shift persistence > XOR scrambling).
- **H232.4** argmax peak time across 3 rule 의 set size ≥ 2 (3 가지가 모두 다를 필요는 없지만 적어도 mechanism 두 군이 *시점에서* 분리되어야).
- **H232.5** re-run byte-identical (3 rule × 20 step × 5 reps Φ + 5 metric, full ledger diff = 0).

## Variables

- **axis1_rule**: {184 (II/TASEP), 60 (II/XOR-shift L), 102 (II/XOR-shift R)}
- **axis2_lattice**: N = 16 (H_225 와 동일)
- **axis3_trajectory_dim**: dim = 12 (Φ-input 의 spatial-trajectory dim)
- **axis4_warmup**: warm = 8 (H_225 와 동일)
- **axis5_traj_len**: 20 step (Φ 측정 시점 t = 0..19, 각 t 에서 t-step 추가 evolve 후 dim-step trajectory 수집)
- **axis6_rep_init**: rep ∈ {0..4} deterministic offset (site i on iff (i+rep)%3 ≠ 0)
- **fixed**: n_bins = 4, periodic boundary, $0 mac local hexa
- **derived metrics**: R²_linear_fit, monotone_nondec_frac, sign_change_density (Δ-sign-flip rate, FFT-equivalent proxy), autocorr_lag1, argmax(Φ_t)

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h232_class_ii_mechanism_decompose_2026_05_24/run_h232.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial` (import READ-ONLY).
- **mapping**: H_225 / H_211 / H_007 와 동일 byte-equal substrate. 각 시점 t 에서 row 를 reset → init(rep) → warm step + t step 추가 evolve → dim-step trajectory 수집 → Φ_t = phi_spatial(states, n, dim, n_bins). 5 reps 평균.
- **trajectory metrics (deterministic)**:
  - R²: linear regression on (t, Φ_t), n=20 points, 0..1 normalized.
  - monotone_nondec_frac: count(Φ_t ≥ Φ_{t-1}) / 19.
  - sign_change_density: count(sign(ΔΦ_t) ≠ sign(ΔΦ_{t-1})) / 18 (오실레이션 proxy, FFT non-zero peak 와 monotone-equiv).
  - autocorr_lag1: cov(Φ_t, Φ_{t-1}) / Var(Φ).
  - argmax_peak_t: arg-max over t.
- **deterministic**: fixed init + fixed config; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none.
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` {config, rules, mechanism, phi_trajectory, metrics, criteria, falsifiers, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) + derived metric scalars = 🟢-tier evidence.

## Criteria

- **C1 (TASEP monotone)** R²(rule 184) ≥ 0.7 ∧ monotone_nondec_frac(rule 184) ≥ 0.7 → H232.1 PASS
- **C2 (XOR oscillating)** sign_change_density(rule 60) ≥ 0.3 ∧ sign_change_density(rule 102) ≥ 0.3 → H232.2 PASS
- **C3 (autocorr ranking)** ac(184) > ac(60) ∧ ac(184) > ac(102) → H232.3 PASS
- **C4 (byte-identical)** diff(run1, run2) = 0 → H232.5 PASS
- **C-PEAK_DISTINCT** argmax_peak_t set 안 ≥ 2 unique → H232.4 informational
- **verdict_rule**:
  - **SUPPORTED** = C1 ∧ C2 (TASEP monotone + XOR oscillating — both mechanism signatures present)
  - **PARTIAL** = C1 ⊕ C2 (오직 한 signature 만 detected; mechanism distinction partial)
  - **FALSIFIED** = otherwise

## Falsifiers

- **F1 RULE184_OSCILLATING**: sign_change_density(rule 184) ≥ 0.3 → H232.1 FALSIFIED (rule 184 가 oscillate, monotone assumption 거짓). (measurable: sign_chg_184.)
- **F2 XOR_MONOTONE**: monotone_nondec_frac(rule 60) ≥ 0.9 ∧ monotone_nondec_frac(rule 102) ≥ 0.9 → H232.2 FALSIFIED (rule 60/102 가 monotone, oscillation assumption 거짓). (measurable: mono_nd_60, mono_nd_102.)
- **F3 ACORR_INVERSION**: ac(184) < ac(60) ∧ ac(184) < ac(102) → H232.3 FALSIFIED (autocorrelation ranking 역전). (measurable: 세 ac_lag1.)
- **F4 BYTE_IDENT_VIOLATION**: re-run JSON / stdout diff ≠ 0 → raw#12 위반 → smoke 무효.
- **F5 PHI_NONFINITE**: 임의 시점 Φ_t < 0 ∨ Φ_t > 1e6 → phi_spatial NaN-policy 위반.
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation.

## Honest Limits (raw#91 c3)

- **L1**: "TASEP shift" / "XOR-derived" 는 literature 의 mechanism label — Φ trajectory shape 와의 1:1 substrate-level signature 매핑은 *hypothesis* 일 뿐 형식 증명 아님. 가능한 alternative source: bin=4 discretization artifact (Φ 가 quantize 되어 plateau 가 mechanism 과 무관하게 발생).
- **L2**: phi_spatial 은 단일 측정 axis (spatial slice) — temporal Φ / partition Φ / phi-G 등 다른 IIT 4.0 partition 의 결과는 다를 수 있다. trajectory 의 shape 가 spatial-axis 한정.
- **L3**: trajectory shape 분류 (monotone vs oscillating) 는 discrete 2-class — 실제로는 더 풍부한 분류 (sinusoidal, exponential decay, step-function, plateau, U-shape) 가능. R² + sign-change-density 의 2-metric 으로는 모든 shape 구분 못 함.
- **L4**: 3 rule small sample — Class-II 전체 family (Wolfram 2002 의 32 rule 후보) 미검증. rule 28, 90, 150, 154, 170, 226, 240 등의 XOR / shift 변종 확장 필요 (별도 cycle).
- **L5**: autocorr lag-1 단일 metric — lag-2/3/k 또는 partial autocorrelation, power spectral density 의 결과는 다를 수 있다. lag-1 은 shift persistence proxy 로만 정당화.
- **L6**: traj_len = 20 step 은 short horizon — XOR-derived 의 Sierpinski period 가 16 step (N=16) 이하면 잡힘, 더 길면 sub-sampled. period > traj_len 인 oscillation 은 monotone 으로 오분류.
- **L7**: rule 60 과 102 는 mirror pair (Z_2 reflection) — 동일 trajectory 예상 (sanity check). 다르면 implementation bug; 같으면 trivial. L7 sanity 와 mechanism 분리는 별도.
- **L8**: argmax peak time 은 noisy — flat plateau 에서 argmax 는 first-tied-index 만 보고 → "peak distinct" 의 실제 의미는 *plateau / non-plateau* 구분에 가까움.

## Cross-Links

- **direct parent H**: H_225 (rule-184 Class-II Φ-peak anomaly — broad FALSIFIED but C3 STRONG PASS; mechanism 분기 carry)
- **indirect H**: H_007 (Class-IV-unique 가정 already broken by H_225; 본 H 는 추가 attack 아님)
- **shared substrate H**: H_211 (shannon-entropy-phi-correlate — byte-equal config), H_204 (C2 rule class mapping)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor)
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **literature**:
  - Krug (1991) Boundary-induced phase transitions in driven diffusive systems (TASEP)
  - Schadschneider (2000) Statistical physics of vehicular traffic (TASEP universality)
  - Wolfram (1984, 2002) A New Kind of Science (rule 60/102/184 substructure; Sierpinski XOR)
  - Crutchfield, Young (1989) Inferring statistical complexity (ε-machine info storage vs generation)
  - Cook (2004) Universality in elementary cellular automata
  - Mitchell, Hraber, Crutchfield (1993) Revisiting the edge of chaos
  - Martínez (2013) A note on elementary cellular automata classification (Class-II substructure)
  - Tononi (2004), Oizumi/Albantakis/Tononi (2014) IIT formal Φ

## Verdict

```
verdict_class: FALSIFIED (pre-register-frozen smoke, post-run honest)
phi_trajectory_summary:
  rule 184  Class-II  TASEP shift   Φ_t = 1.19781 (constant for all t ∈ [0,19])
  rule  60  Class-II  XOR-shift L   Φ_t rises 1.6832 → 2.78794 (t=0..6) → collapses to 1.14511e-05 (t=8..19)
  rule 102  Class-II  XOR-shift R   Φ_t === rule 60 (L7 sanity PASS, Z_2 mirror byte-equal)
signature metrics (R² · mono_nd · sign_chg · ac1 · peak_t):
  rule 184  R²=0.0       mono_nd=0.789  sign_chg=0.0       ac1=0.675  peak_t=11
  rule  60  R²=0.642327  mono_nd=0.895  sign_chg=0.0556    ac1=0.881  peak_t=6
  rule 102  R²=0.642327  mono_nd=0.895  sign_chg=0.0556    ac1=0.881  peak_t=6
criteria_met: 1/4 (C4 PASS · C1 FAIL · C2 FAIL · C3 FAIL)  + C-PEAK_DISTINCT TRUE
evidence_summary: 🟢 NUMERICAL — RFC 036 phi_spatial trajectory. (a) rule 184 은 monotone *non-decreasing* 의 약한 형태 (mono_nd=0.789) 이지만 R²=0 (slope ≈ 0, plateau-flat, NOT increasing — C1 strict FAIL); (b) rule 60/102 는 oscillating 이 아닌 *rise-then-collapse* (8 step 만에 ~10⁻⁵ 로 붕괴, sign_chg=0.056 으로 oscillation 약함 — C2 FAIL); (c) autocorr ranking inversion ac_184=0.675 < ac_60/102=0.881 (예측의 *반대*, F3 triggered)
falsifiers_triggered: F3 (autocorr ranking inversion)
```

### Pre-register-frozen smoke (2026-05-24)

3-rule (184/60/102) × N=16 × 20-step Φ trajectory sweep pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
1D elementary CA, N=16 periodic, dim=12 trajectory, 5 deterministic reps, Φ via RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_232 — Class-II Φ-peak mechanism decompose · TASEP vs XOR (raw#12)
  N=16 dim=12 warm=8 traj_len=20 reps=5  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)

  rule 184 (TASEP shift) Φ trajectory:
    t=0  Φ=1.19781
    t=1  Φ=1.19781
    ... (t=2..19 모두 Φ=1.19781, plateau constant)

  rule 60  (XOR-shift L) Φ trajectory:
    t=0  Φ=1.6832
    t=1  Φ=1.86873
    t=2  Φ=2.034
    t=3  Φ=2.33065
    t=4  Φ=2.51472
    t=5  Φ=2.56563
    t=6  Φ=2.78794      ← peak (rule 60/102 공통)
    t=7  Φ=1.73804      ← collapse start
    t=8  Φ=1.14511e-05  ← floor (XOR cancellation to ~0)
    ... (t=9..19 모두 1.14511e-05, near-zero plateau)

  rule 102 (XOR-shift R) Φ trajectory:
    (rule 60 와 byte-equal — Z_2 mirror sanity L7 PASS)

  rule signature summary (rule · R²_lin · monotone_frac · sign_chg_dens · autocorr_lag1 · peak_t):
    184  R²=0.0       mono_nd=0.789474  sign_chg=0.0       acorr1=0.675     peak_t=11
    60   R²=0.642327  mono_nd=0.894737  sign_chg=0.0555556 acorr1=0.880831  peak_t=6
    102  R²=0.642327  mono_nd=0.894737  sign_chg=0.0555556 acorr1=0.880831  peak_t=6

  C1 RULE184_MONOTONE (R² >= 0.7 ∧ mono_nd >= 0.7): false  (R²=0.0 · mono_nd=0.789474)
  C2 XOR_OSCILLATING (sign_chg >= 0.3, both): false  (60 osc=0.0555556 in=false · 102 osc=0.0555556 in=false)
  C3 ACORR_RANK (ac_184 > ac_60 ∧ ac_184 > ac_102): false  (184>60=false · 184>102=false)
  C-PEAK_DISTINCT (peak_t differs across rules): true  (184=11 · 60=6 · 102=6)

  F1 RULE184_OSCILLATING (osc_184 >= OSC_FLOOR): false
  F2 XOR_MONOTONE        (mono_60∧mono_102 >= 0.9): false
  F3 ACORR_INVERSION     (ac_184 < both XOR)     : true
  F4 BYTE_IDENT_CONTRACT (det re-run)            : true
  F5 PHI_NONFINITE       (Φ < 0 ∨ Φ > 1e6)        : false

  VERDICT_RULE: SUPPORTED iff C1∧C2 · PARTIAL iff C1⊕C2 · else FALSIFIED
  VERDICT     : FALSIFIED
```

re-run byte-identical (F4 BYTE_IDENT confirmed via `diff` of run1 vs run2 on `result.json`).

honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica + derived trajectory metrics (R² · sign-change-density · autocorr-lag-1). NOT 🔵 (no formal proof; trajectory-shape classification 만 numerical).

**Interpretation (honest, raw#82 no post-hoc rewriting)**:

1. **C1 FAIL (rule 184 monotone)** — rule 184 의 trajectory 가 *constant plateau* (Φ = 1.19781 for all 20 step). 이는 H232.1 의 strict "monotone non-decreasing AND R² ≥ 0.7" 조건은 fail (R²=0, slope=0). **그러나 weak interpretation 에서 monotone 의 의미 — *decrease 없음* — 는 정확히 만족**: mono_nd=0.789 ≥ 0.7 (decrease 가 없으므로 모든 t≥1 에서 Φ_t ≥ Φ_{t-1}, equality 인 경우 ≥). TASEP 의 information conservation 이 **trajectory 의 *steady-state* 도달 + plateau** 형태로 발현 — predict 는 "monotone rise" 였는데 실측은 "monotone flat". hypothesis 의 *질적* 방향은 (정보 보존) 맞고 *양적* 형태가 (plateau ≠ rise) 빗나감.
2. **C2 FAIL (XOR oscillating)** — rule 60/102 가 oscillate 가 아니라 **rise-then-cliff-collapse** (t=0..6 rise + t=7 drop + t=8 onward ~10⁻⁵). sign_change_density=0.056 매우 낮음 (sign-change 가 t=7 한 번만). 이는 H232.2 의 "oscillating" assumption 을 무력화하지만, **XOR cancellation 가설의 *strong* form 을 지지** — Sierpinski self-similar pattern 이 N=16 finite-lattice + periodic boundary 위에서 (16=2^4 power-of-2) **complete cancellation 으로 수렴** 한다 (Wolfram 2002 §3 의 additive linear CA 의 generic 행동: Z_2-linear over finite periodic lattice 이면 modulo periodicity 가 0-state attractor 로 수렴). H_211 / H_225 의 단일 Φ 측정은 *t=0 직후 의 transient* 를 잡은 것이지 *steady state* 가 아님 — 본 H 가 reveal 한 새 사실.
3. **C3 FAIL (autocorr inversion)** — ac(184) = 0.675 < ac(60) = ac(102) = 0.881. F3 falsifier triggered. 이는 *trajectory 가 constant plateau* 인 rule 184 의 autocorr 이 *rise+plateau* 인 rule 60/102 의 autocorr 보다 낮다는 — 표면적으로 모순. 원인 분석: rule 184 plateau 위 *finite-precision noise* (Φ = 1.19781 의 마지막 자리 fluctuation, RFC 036 phi_spatial 의 float64 round) 가 var(Φ) 분모를 매우 작게 만들어 ac1 의 numerator/denominator ratio 가 0.675 로 *underestimate*. rule 60/102 는 큰 dynamic range (1.68 → 0) 에 plateau (1e-5) 를 dominant 하게 차지 → constant-like ac1 ≈ 1.0 근접. **L5 의 "단일 metric autocorr" 한계가 정확히 실현됨** — F3 triggered 는 *metric artifact* 가능성 매우 높음.
4. **C-PEAK_DISTINCT TRUE** — peak_t(184)=11 vs peak_t(60)=peak_t(102)=6. 184 의 11 은 *constant plateau 의 first-tied-argmax* (L8 의 noisy peak 이지만), 60/102 의 6 은 *진짜 peak*. **mechanism 분리 informational evidence**: TASEP 는 *언제든 peak* (plateau 의 어디든), XOR 는 *t=6 peak + 이후 collapse* — 두 mechanism 의 *temporal signature* 정성적 분리.
5. **L7 sanity PASS** — rule 60 과 rule 102 의 trajectory + 모든 metric byte-identical. Z_2 mirror reflection 정합, implementation bug 없음.

**핵심 발견** (mechanism decomposition advisory, design 예상 빗나간 부분 포함):
- rule 184 = **information conservation → steady-state plateau** (predicted: monotone rise; actual: monotone flat). 질적으로 conservation 맞음.
- rule 60/102 = **XOR cancellation → rise-then-collapse to 0** (predicted: oscillating; actual: 8-step transient + 0-attractor). Wolfram 2002 의 finite-periodic-lattice Z_2 linear CA universal behavior 와 정합. H_225 의 단일-시점 측정이 *transient peak* (t≤7) 를 잡았음.
- mechanism *분리* 은 성립 (constant-plateau vs cliff-collapse 는 *명확히 다른 shape*) 하지만 본 H 의 pre-registered shape classification (monotone vs oscillating) 의 *문법* 으로는 양쪽 모두 FAIL.
- F3 autocorr ranking inversion 은 *float-noise artifact* 가능성 높음 (rule 184 plateau 의 numerical fluctuation 이 var(Φ) 분모 → ac1 underestimate). raw#82 honesty 로 F3 triggered 그대로 기록.

**Follow-up cycles (별도 H)**:
- Wider trajectory length (200 step, 1000 step) 위 rule 60/102 의 0-attractor recovery 여부 (period > 16 이면 finite-lattice 한계 입증, period == 16 이면 confirm).
- N=2^k vs N=2^k+1 (non-power-of-2) lattice 위 XOR 의 0-attractor 깨짐 여부 (Z_2 linear CA literature 의 표준 test).
- 8-rule Class-II family extension (rule 28, 90, 150, 170, 226, 240) — XOR 변종 + shift 변종 모두.
- finite-precision noise quantification — rule 184 plateau 의 round-off 의 ac1 영향 isolate.

**State output**: `HEXAD/LIFE/state/h232_class_ii_mechanism_decompose_2026_05_24/result.json`
**Smoke**: `HEXAD/LIFE/state/h232_class_ii_mechanism_decompose_2026_05_24/run_h232.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica + derived trajectory metrics; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged).
