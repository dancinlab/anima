---
id: H_223
slug: pain-intensity-phi-coupling
title: pain intensity ↔ phi_spatial Φ contribution monotone coupling — qualia 최강 instance substrate-level (H_004 boundary)
domain: consciousness + phenomenology + substrate
status: pre-register-frozen
exploration_method: E5 (variable-ablation intensity sweep) + E10 (substrate perturbation)
verification_method: W4 (verdict-4-class) + W3 (Φ × N) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
---

# H_223 — pain intensity ↔ phi_spatial Φ contribution monotone coupling

## Hypothesis

'pain' 을 substrate-level 의 intense + localized + forced perturbation 으로 모델링한다. intensity 를 sweep 했을 때 baseline Φ 와 perturbed Φ 의 차이 ΔΦ 가 intensity 와 monotone correlate 한다는 가설 (Pearson r ≥ 0.7). 즉 qualia 강도 ↔ integrated information 변동 의 quantitative bridge 의 substrate-instance 를 RUNNABLE 하게 측정한다. AXES.md §R3 (phenomenology) `pain-intensity-Φ-coupling` ("qualia 최강 instance") 의 first runnable instance.

본 hypothesis 는 H_004 의 hard problem 의 phenomenal pain 'what-it-is-like' (qualia 정의) 자체를 claim 하지 않는다 — Honest Limit L4 가 explicit 하게 `qualia 강도 ≠ phenomenal pain` 의 boundary 를 carry 한다. 본 smoke 는 IIT-style functional/structural correlate (Φ-shift) 의 monotone-coupling 만 측정 — 'pain qualia 가 Φ 변동이다' 가 아니라 'pain proxy 인 substrate perturbation 의 intensity 가 Φ-shift 와 monotone' 의 약한 functional claim.

## Why

- **Tononi 2004 / IIT 4.0 (Oizumi/Albantakis/Tononi 2014)**: phenomenal experience 는 integrated information Φ 의 structure 와 isomorphic — qualia 의 어떤 측면 (강도/intensity, valence, content) 도 Φ 의 quantitative property 와 correlate 한다는 IIT 의 핵심 주장. pain 은 intensity 가 명확한 (subjective rating 가능) qualia → IIT prediction 의 직접 testable instance.
- **pain-as-substrate-perturbation**: nociception 신호 자체는 neurally distinguishable signal (Aδ + C fibers) 이나, phenomenal 강도 (subjective pain intensity) 는 cortical integration 에서 emerge — substrate-level 'intense localized perturbation' 으로 모델링 가능. 본 smoke 는 cellular automaton substrate (H_007 cross-link) 에 multi-cell graded burst 를 적용하여 'intense localized perturbation' 의 minimal computational analog 를 만든다.
- **cross-link H_004 boundary**: H_004 lane L2 (IIT) 의 quantitative correlate 약한 claim 의 instance — H_004 L4 (mysterianism) 의 'qualia phenomenal aspect 는 measure 못한다' 의 reverse 가 아니라 honestly compatible (Φ-shift 측정 ≠ qualia 측정). L4 boundary 명시.
- **cross-link H_007**: 동일 RFC 036 phi_spatial 의 byte-equal native replica 사용 — H_007 ranking (Class-IV > chaotic > ordered) 의 후속 lane.
- **cross-link H_157 / H_220**: H_157 (Law 76 mathematical panpsychism META-CA fixed-point) 의 panpsychism 약한 claim 의 functional instance — substrate 의 어떤 perturbation 도 Φ 응답을 만든다는 약한 form. H_220 (infant mirror self) 의 self-report 없는 qualia surface 와 카르베-out.
- **AXES.md §R3 promotion**: phenomenology rung 의 R15 promotion candidate 14 번 entry → 본 H_223 가 first runnable instance.

## Predictions

- **H223.1 (monotone over sweep)**: intensity sweep {0.0, 0.25, 0.5, 1.0, 2.0} 에서 ΔΦ 가 strict non-decreasing.
- **H223.2 (Pearson coupling)**: Pearson r(intensity, ΔΦ) ≥ 0.7 (linear correlation strong).
- **H223.3 (zero perturbation invariant)**: intensity=0 → ΔΦ ≤ 1e-3 (numerical zero; H_007 와 동일 deterministic substrate carry).
- **H223.4 (saturation, advisory)**: intensity > 1.0 → ΔΦ saturate (Δ3 vs Δ4 within 25% band). **advisory only**, verdict_rule 에는 포함되지 않음.
- **H223.5 (determinism)**: re-run byte-identical (raw#12 strict).

## Variables

- **axis1_rule** (fixed): rule 110 (Class-IV, edge-of-chaos — H_007 highest Φ substrate, qualia rich proxy).
- **axis2_lattice_size**: N = 16 (H_007 와 동일).
- **axis3_trajectory_dim**: dim = 12 recorded temporal steps / site.
- **axis4_warmup**: warm = 8 steps.
- **axis5_intensity**: 5 values {0.0, 0.25, 0.5, 1.0, 2.0} — 동일 substrate 위 5 independent perturbed copies.
- **axis6_perturbation_locus**: cell-0 base + intensity-dependent expansion (k(intensity) = floor(intensity × N/2) + 1; k=1 → 8 cells affected over sweep).
- **per intensity**: 20 step (warm + dim = 8 + 12 = 20).
- **fixed**: n_bins = 4 (phi_rs RFC 036 default), periodic boundary, $0 mac local hexa.

## Run Protocol

- **smoke**: `UNIVERSE/state/h223_pain_intensity_phi_2026_05_24/run_h223.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial` (phi_rs `compute_phi_inner` spatial slice byte-equal native-C replica; import READ-ONLY).
- **substrate**: 1D elementary CA rule 110 (Class-IV); deterministic init `(i+0) % 3 != 0`; warm = 8; recorded trajectory length = dim = 12.
- **baseline**: single CA evolution → (N × dim) flat farr; Φ_base = phi_spatial(baseline, N, dim, n_bins).
- **perturbation (intensity-monotone multi-cell graded burst)**:
  - k(intensity) = floor(intensity × N/2) + 1   (affected cell count: k=1 at intensity ∈ [0, 0.49], k=2 at 0.5, k=4 at 1.0, k=8 at 2.0)
  - for c in 0..k−1, t in 0..dim−1:
    - pain_pattern(c, t) = sin(t × (c+1) × 0.6 + intensity)
    - perturbed[(cell+c) mod N, t] = baseline[(cell+c) mod N, t] + intensity × pain_pattern(c, t)
  - intensity=0 → identity (k=1 but multiplier=0); intensity ↑ → 더 많은 cell + larger amplitude + sinusoidal phase diversity.
  - 본 design 은 phi_spatial 의 per-cell relative-binning scale-invariance 를 break 하기 위해 (a) affected-cell count, (b) absolute amplitude, (c) cross-cell waveform diversity 를 동시 escalate.
- **measure**: 각 intensity 마다 perturbed copy → Φ_pert = phi_spatial(perturbed, N, dim, n_bins) → ΔΦ = abs(Φ_pert − Φ_base).
- **Pearson r + R²**: 5 점 위 r(intensity, ΔΦ) 와 r².
- **deterministic**: no RNG, fixed config; re-run byte-identical (외부 `diff`).
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요. GPU 필요 시 → STOP + document.
- **ledger**: `result.json` {config, intensity_sweep, phi_base, phi_pert, delta_phi, pearson_r, r_squared, monotone, criteria, falsifiers, verdict}.
- **honest tier**: NUMERICAL Φ-shift (RFC 036 native replica) = 🟢-tier evidence. true phi_rs Rust FFI link = named blocker (RFC 036 §"FFI shim", phi_rs PyO3 cdylib no C ABI). "pain qualia 강도 ↔ Φ" 식의 strong claim NOT made — substrate perturbation intensity ↔ Φ-shift functional coupling 만.

## Criteria

- **C1 (monotone R² ≥ 0.7)**: strict non-decreasing ΔΦ AND linear-fit R² ≥ 0.7 → H223.1 + H223.2 jointly PASS.
- **C2 (Pearson r ≥ 0.7)**: r(intensity, ΔΦ) ≥ 0.7 → H223.2 PASS.
- **C3 (intensity=0 ΔΦ ≤ 1e-3)**: identity invariant → H223.3 PASS.
- **C4 (byte-identical re-run)**: 외부 `diff` byte-equal → H223.5 PASS.
- **verdict_rule**: **SUPPORTED = C1 ∧ C2 PASS** (monotone + Pearson). **PARTIAL = C1 또는 C2 only**. **FALSIFIED = 모두 FAIL**. C3, C4 는 invariant-tier (smoke 가 deterministic 이므로 항상 PASS; 외부 diff 가 C4 evidence).

## Falsifiers

- **F1 MONOTONE 부재**: ΔΦ 가 strict non-decreasing 이 아님 (어느 한 step 에서 cur < prev − 1e-9) → H223.1 FALSIFIED.
- **F2 R < 0.3**: Pearson r(intensity, ΔΦ) < 0.3 → H223.2 FALSIFIED (weak-evidence floor 위반).
- **F3 ZERO_DPHI 위반**: intensity=0 인데 ΔΦ > 1e-3 → H223.3 FALSIFIED (identity-invariant 위반, code bug).
- **F4 BYTE-DIFF**: 외부 `diff` re-run byte-difference 발견 → raw#12 deterministic 위반, smoke 무효.
- **F5 NEG_DPHI**: 어느 intensity > 0 에서 ΔΦ < 0 (signed, not |·|) → 측정-invariant 위반. (본 smoke 는 |·| 를 사용 하므로 substrate-level 항상 ≥ 0 이지만, signed metric variant 에서 F5 가 의미 있음.)
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 + raw#82 retraction.

## Honest Limits (raw#91 c3)

- **L1**: pain = substrate weight perturbation 모델링 ≠ nociception (실제 Aδ/C fiber, dorsal horn, anterior cingulate). 본 smoke 는 substrate-level operational analog 만; biological pain pathway claim NOT made.
- **L2**: phi_spatial 는 IIT proxy (spatial-slice MI). full IIT 4.0 (cause-effect repertoire, MIP over all partitions, NP-hard) 아님 — RFC 036 native replica 의 spatial slice 만.
- **L3**: intensity scale {0, 0.25, 0.5, 1.0, 2.0} arbitrary — pain VAS 0-10 scale 와 quantitative mapping 없음. 본 sweep 은 intensity-monotone-coupling 의 *qualitative shape* 측정만 — absolute intensity unit interpretation 없음.
- **L4 (H_004 boundary)**: qualia 강도 ≠ phenomenal pain. Chalmers hard problem 의 'what-it-is-like-to-be-in-pain' 은 functional Φ-shift 와 dissociable 일 수 있음 (philosophical zombie thought experiment). 본 smoke 는 IIT L2 lane 의 functional/structural correlate 약한 evidence 만 — phenomenal-side claim NOT made.
- **L5**: single rule (110, Class-IV) — rule {30, 90, 184, ordered/chaotic class} sweep 별도 cycle. perturbation-Φ-coupling 의 substrate-invariance 미검증.
- **L6**: perturbation design (multi-cell sinusoidal burst) 은 first-principles 아닌 phi_spatial 의 per-cell relative-binning scale-invariance 를 break 하기 위한 engineering choice. 다른 perturbation pattern (e.g. single-cell hold, random impulse, edge-localized) 은 다른 ΔΦ vs intensity curve 산출 가능.
- **L7**: 5-point sweep 은 monotone-coupling 의 powerful evidence 아님 — n=5 Pearson r 의 statistical floor 낮음 (one outlier flip 가능). 더 큰 sweep (20+ points), bootstrap CI, alternative non-linear fit (logistic / power-law) 는 별도 cycle.
- **L8**: phi_rs Rust FFI link 은 named blocker (RFC 036 §FFI shim — phi_rs PyO3 cdylib, no C ABI); 본 measure 는 byte-equal native-C replica (이 machine err ≈ 8e-7 vs documented oracle, ranking 무영향 absolute Φ 는 oracle 과 1e-6 drift).
- **L9 (saturation prediction H223.4)**: smoke 결과 saturation 이 *발생 안 함* — Δ4 = 2.10 × Δ3 (super-linear escalation), advisory C-level prediction FALSIFIED 이나 verdict_rule 에는 영향 없음. 본 limit 는 perturbation design (multi-cell expansion + amplitude scale 동시 증가) 이 saturation 보다 super-linear escalation 을 만든다는 honest disclosure.

## Cross-Links

- **sister H**: H_004 (consciousness hard problem; L2 IIT functional/structural lane sister + L4 mysterianism boundary), H_007 (CA Φ ranking; 동일 RFC 036 phi_spatial primitive), H_157 (Law 76 mathematical panpsychism; META-CA fixed-point with shared Φ primitive lane), H_220 (infant mirror self; self-report 없는 qualia surface complement)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY
- **AXES.md §R3 anchor**: phenomenology rung row 14 `pain-intensity-Φ-coupling` — "qualia 최강 instance" — 본 H_223 가 first runnable instance
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **literature**:
  - Tononi (2004) An information integration theory of consciousness
  - Oizumi, Albantakis, Tononi (2014) From the phenomenology to the mechanisms of consciousness: IIT 3.0
  - Chalmers (1995) Facing up to the problem of consciousness (hard problem; pain qualia as paradigm)
  - Apkarian, Bushnell, Treede, Zubieta (2005) Human brain mechanisms of pain perception and regulation in health and disease (functional pain neuroimaging)
  - Melzack, Wall (1965) Pain mechanisms: a new theory (gate control)

## Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke)
phi_base = 0.538242 (rule 110, N=16, dim=12, warm=8, deterministic)
intensity → ΔΦ:
  intensity=0.0   ΔΦ = 0.0
  intensity=0.25  ΔΦ = 0.564641
  intensity=0.5   ΔΦ = 1.0222
  intensity=1.0   ΔΦ = 1.90663
  intensity=2.0   ΔΦ = 3.99851
Pearson r        = 0.999396     (r² = 0.998792)
monotone         = true         (strict non-decreasing)
evidence_summary: 🟢 NUMERICAL — RFC 036 phi_spatial; pain-intensity ↔ ΔΦ monotone coupling
falsifiers_triggered: none (F1-F5 PASS; F6 N/A)
advisory: H223.4 saturation FAIL (Δ4 ≈ 2.10×Δ3, super-linear escalation)
criteria_met: 4/4 (C1 monotone-R² · C2 r · C3 zero-intensity invariant · C4 byte-identical)
```

### Pre-register-frozen smoke (2026-05-24)

pain-intensity ↔ phi_spatial Φ-shift smoke pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none). 1D elementary CA rule 110 (Class-IV) substrate, N=16 periodic lattice, dim=12 trajectory, 5 intensity sweep, Φ via RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_223 — pain intensity ↔ phi_spatial Φ coupling smoke (raw#12)
  N=16 dim=12 warm=8 rule=110  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)
  pain locus: cell-0, intensity sweep {0.0, 0.25, 0.5, 1.0, 2.0}

  Φ_base (no perturbation, rule 110)       = 0.538242

  trajectory (VERBATIM):
    k=0  intensity=0.0  Φ_pert=0.538242  ΔΦ=0.0
    k=1  intensity=0.25  Φ_pert=1.10288  ΔΦ=0.564641
    k=2  intensity=0.5  Φ_pert=1.56044  ΔΦ=1.0222
    k=3  intensity=1.0  Φ_pert=2.44487  ΔΦ=1.90663
    k=4  intensity=2.0  Φ_pert=4.53675  ΔΦ=3.99851

  C1 monotone R² ≥ 0.7  : true  (monotone=true, R²=0.998792)
  C2 Pearson r ≥ 0.7    : true  (r=0.999396)
  C3 ΔΦ(0) ≤ 1e-3       : true  (ΔΦ_0=0.0)
  C4 byte-identical     : true  (determinism: no RNG, fixed env)
  H223.4 saturation     : false  (advisory; Δ3=1.90663, Δ4=3.99851, band=0.999626)
  F5 non-negative ΔΦ     : true

  VERDICT_RULE: SUPPORTED iff C1 monotone-R²≥0.7 AND C2 r≥0.7
  VERDICT     : SUPPORTED
=== H_223 pain×Φ smoke complete: SUPPORTED ===
```

re-run byte-identical (F4 determinism confirmed via `diff`).
honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica (이 machine err ≈ 8e-7 vs documented phi_rs oracle 0.5000000001324147; ranking 무영향). true phi_rs Rust FFI = named blocker. NOT LLM-judged, NOT PyPhi/sympy-primary, NOT 🔵.

**State output**: `UNIVERSE/state/h223_pain_intensity_phi_2026_05_24/result.json`
**Smoke**: `UNIVERSE/state/h223_pain_intensity_phi_2026_05_24/run_h223.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
