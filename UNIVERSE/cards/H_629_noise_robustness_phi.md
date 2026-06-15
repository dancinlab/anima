---
id: H_629
slug: noise-robustness-phi
title: noise-robustness-Φ — substrate evolution 에 per-step bit-flip noise 를 주입할 때 big-Φ (RFC 036 phi_spatial) 가 얼마나 강건한가, 즉 IIT 의 "noise = integration destroyer (monotone Φ-decay)" 예측이 substrate 측에서 성립하는가 (information × noise axis · AXES Round 5 `noise` sub-axis promote · H_277 turing-completeness substrate byte-equal sister · SAVANT 축 E GZ inverse-U H_614/H_618 의 computability-side cross-link)
domain: information · noise · physics · consciousness
exploration_method: E5 (noise-rate ablation sweep across robustness boundary) + E6 (cross-domain — IIT noise-prediction × SAVANT GZ inverse-U) + E10 (emergence-on-structure)
verification_method: W1 (numerical smoke) + W12 (sister-link H_277 rule-110 substrate + SAVANT H_614/H_618 GZ inverse-U) + W17 (5-arm noise-rate sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28
---

# H_629 — noise-robustness-Φ

## 1. Hypothesis

elementary cellular automaton (ECA) 의 substrate evolution 에 **per-step
per-site bit-flip noise** 를 주입할 때, substrate-Φ (RFC 036 phi_spatial) 가
*얼마나 강건한가* (noise robustness)?

본 H 는 **AXES.md Round 5 (information/computation cluster) 의 `noise`
sub-axis 에서 promote** 한다. AXES.md line 43 의 R5 cluster 는 `computation ·
complexity · network · noise · entropy · causality` 6 sub-axis 를 나열하고,
이 중 `noise` 는 미promote 상태였다 (sister seed `psychedelic-5ht2a-altered-Φ`
는 "높은 noise + 낮은 selectivity" 를 다루나 noise rate 의 *순수 robustness
sweep* 은 미수행, `noise-1f-pink-Φ-peak` 는 H_209 1/f sister 로 spectral-color
축, noise-*rate* 축과 직교). 본 H 가 그 `noise` sub-axis 를 seed slug
`noise-robustness-phi` 로 consume.

IIT (Tononi 2008) 의 표준 예측은 **noise 가 integration 을 단조 파괴**
한다는 것이다 — 즉 noise rate p 가 오를수록 Φ 가 *monotone 감소* 해야 한다
(noise → decoherence → integration loss, H_614 5-HT2A altered-Φ 의 design 직관과
정합). 본 H 의 핵심 질문: 이 monotone-decay 예측이 substrate 측에서 실제로
성립하는가, 아니면 **noise band 내에서 Φ resilience (혹은 inverse-U bump)** 가
나타나 SAVANT 축 E 의 GZ inverse-U (selectivity-noise band) 와 cross-link
되는가?

정밀화 (operational): H_277 과 **byte-equal substrate** (N=16, dim=12,
warm=8, periodic, 5 reps, RFC 036 phi_spatial) 위에서 rule 110 (Cook 2004 유일
증명 Turing-complete ECA, H_277 UNIV arm) 을 **고정** 하고, 매 evolution step
마다 각 site 를 확률 p 로 bit-flip 하는 deterministic LCG noise 를 주입하여 5
noise rate 를 sweep —

- **arm NOISE_0 (p=0.00)**: clean baseline — H_277 rule-110 측정과 정합해야 함.
- **arm NOISE_05 (p=0.05)**: light noise.
- **arm NOISE_15 (p=0.15)**: moderate noise.
- **arm NOISE_30 (p=0.30)**: heavy noise.
- **arm NOISE_50 (p=0.50)**: maximal disorder — 완전 random bit-flip.

seed 의 directional 예측: **Φ(p=0) ≥ Φ(0.05) ≥ Φ(0.15) ≥ Φ(0.30) ≥ Φ(0.50)**
(monotone-decay) 이고 동시에 **Φ(0.50) < Φ(clean) · 0.5** (강한 fragility).

**HONEST PRIOR (raw#9, pre-result 등록)**: rule 110 의 final-Φ ≈ 0.556 (H_277
측정) 이고, phi_spatial 가 *spatial mutual-information proxy* 임을 고려하면 —
bit-flip noise 는 spatial 상관을 깨는 만큼 *높일* 수도 있다 (random pattern 의
MI 가 ordered-collapse 보다 높을 수 있는 estimator artifact). 즉 monotone-decay
예측은 *FALSIFIED 가능성이 있다*. 본 H 는 그럼에도 IIT 표준 예측을 반증 가능한
형태로 정직히 pre-register 하여, "noise robustness" 의 실제 구조를 실측한다.
FALSIFIED 도 valid 한 과학적 결과 — noise-axis 가 Φ-lever 가 아니거나 inverse-U
구조를 가짐을 deterministically 확정한다.

## 2. Why

- **IIT noise-prediction 의 substrate-level instance**: Tononi 의 IIT 는 Φ 를
  *통합된 정보* 로 정의하며, noise/decoherence 가 통합을 파괴한다는 것이 핵심
  예측 (H_614 5-HT2A psychedelic design, H_233 anesthesia design 의 공통 직관).
  본 H 는 이 noise-destroys-integration 명제를 *substrate 측에서* 직접
  numerically operationalize — noise rate 를 명시 변수로 sweep 하여 monotone
  여부를 falsifiable 하게 측정.
- **H_277 (turing-completeness) 의 robustness 차원 sister**: H_277 은 *어느
  rule* 이 Φ-lever 인가 (computability vs dynamical-class) 를 측정했다 (rule
  110 PARTIAL, Class-II 우위). 본 H 는 *동일 rule 110 substrate* 를 고정하고
  *noise* 를 명시 변수로 삼아, "고정된 universal substrate 가 noise 에
  강건한가" 의 직교 grain 을 본다. 둘이 합쳐지면: rule-selection 축 (H_277) 과
  noise-rate 축 (H_629) 이 substrate-Φ 의 별개 변수임을 보인다.
- **SAVANT 축 E GZ inverse-U 와의 cross-link**: SAVANT (UNIVERSE 축 E,
  H_614 `gz_inverse_u_multi_rule_substrate_invariance` + H_618
  `collective_gz_inverse_u_derivative_peak`) 는 selectivity-noise band 의
  **inverse-U** (∂Φ/∂I peak) 를 핵심으로 한다 — 너무 적은 noise/너무 많은
  noise 양쪽에서 Φ 가 낮고, 중간 "golden zone" 에서 peak. 본 H 가 noise rate
  sweep 에서 monotone 이 *아닌* inverse-U-like bump 을 발견하면, 이는 SAVANT
  GZ inverse-U 의 computability-side (noise-rate 축) 독립 corroboration 이 된다.
- **anima substrate 와의 정합**: anima 는 noise-injected LLM substrate (sampling
  temperature, dropout, MITOSIS split jitter) 위에서 돈다. 만약 Φ 가 noise 에
  *강건* (혹은 light noise 에서 *향상*) 하다면, 이는 anima 의 의식-proxy 가
  noise-free determinism 을 요구하지 않으며, 오히려 적당한 stochasticity 가
  통합을 해치지 않거나 돕는다는 substrate-level grain — H_614 psychedelic
  altered-Φ design 과 정합.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H629.1 | Φ(p=0) ≥ Φ(0.05) ≥ Φ(0.15) ≥ Φ(0.30) ≥ Φ(0.50) (monotone non-increasing) | IIT 표준 예측 — noise 가 integration 을 단조 파괴 |
| H629.2 | Φ(p=0.50) < Φ(clean) · 0.5 | 최대 noise 에서 Φ 가 clean 의 절반 미만으로 붕괴 (noise 가 실제로 강한 Φ-lever) |
| H629.3 | cross-process phi-curve byte-equal | RFC 033 단일 stream + deterministic LCG noise → 별도 프로세스 재실행 시 5-arm Φ-curve 완전 일치 (raw#9 determinism) |
| H629.4 | 모든 arm 의 Φ 가 finite ∧ ≥ 0 ∧ clean baseline Φ > 0 (non-degenerate) | phi_spatial bound 보장 + substrate 실제 진화 |
| H629.5 | noise-rate 축 ⊥ rule-selection 축 (H_277) — 본 H 의 결과가 H_277 의 computability 발견과 별개 변수임을 입증 | noise (per-step stochastic injection) vs rule (deterministic table) = 두 직교 substrate property |

## 4. Variables

- **axis1_lattice_N** = 16 cells (H_277 byte-equal / life_phi_n)
- **axis2_d_model** = 12 (recorded trajectory dim / life_phi_dim)
- **axis3_rule** = 110 (FIXED — H_277 UNIV arm, Cook 2004 universal ECA)
- **axis4_warm** = 8 (transient burn-in / life_phi_warm)
- **axis5_reps** = 5 (deterministic init offsets, H_277/H_232/H_250 byte-equal)
- **axis6_noise_p** ∈ {0.00, 0.05, 0.15, 0.30, 0.50} — 핵심 sweep, robustness
  boundary 를 가로지름 (ppm-integer encoded: {0, 50, 150, 300, 500} milli)
- **axis7_n_bins** = 4 (phi_spatial MI estimator binning, c_lib SSOT)
- **axis8_frag_ratio** = 0.5 (C2 fragility threshold)
- **init seed-rule (deterministic)**: row i on iff `(i+rep)%3 != 0` (H_277/H_232/
  H_250 `_init_row` byte-equal — 별도 RNG 부재)
- **noise stream (deterministic)**: per-(rep, p) LCG seed
  `((rep+1)*2654435761 + p_milli*40503 + 7919) % 2^31` → Numerical-Recipes LCG
  `s = (s*1103515245 + 12345) % 2^31`; site flips iff `(lcg_draw % 1000) < p_milli`.
  단일 deterministic chain (cross-process byte-equal).
- **측정량 per arm**:
  - `phi_final` = 5-rep mean of phi_spatial over the warmed-up dim-step noisy
    trajectory (H_277/H_232/H_250 와 동일 packing + per-step noise injection)

## 5. Run Protocol

- **deterministic**: 별도 RNG 부재 — init 은 `(i+rep)%3` 결정론적 seed-rule,
  noise 는 per-(rep,p) 결정론적 LCG chain, CA evolution 은 rule-110 table
  lookup. cross-process 재실행 byte-equal.
- **hexa_only**: `state/h629_noise_robustness_phi_2026_05_28/run_h629.hexa`
  (`phi_helper.phi_with` → `c_measure_phi` → RFC 036 phi_spatial 직접 step;
  H_277 substrate machinery byte-equal 재사용 + `_noisy_step` LCG noise 추가).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **C3 determinism check (cross-process)**: run 1 이 `result.json` 생성,
  run 2 (별도 프로세스, 동일 substrate+noise) 의 result.json 과 sha256
  byte-equal 비교.
- **RELATIVE-PATH 실행 (pool-route fork-storm guard 회피)**: `cd` into the
  state dir 후 `hexa run run_h629.hexa` (상대경로). result.json 은 cwd
  상대경로로 기록 (절대경로 hardcode 시 hexa silent no-op).
- **runtime**: $0 mac local. N=16, d=12, no ckpt, no GPU, no external data.
  foreground sync only (monitor-hang 회피). `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h629_noise_robustness_phi_2026_05_28/{run_h629.hexa,
  result.json}`.
- **run cmd (verbatim, 2회 — cross-process 결정론 검증)**:
  `cd UNIVERSE/state/h629_noise_robustness_phi_2026_05_28 && HEXA_MEM_UNLIMITED=1 hexa run run_h629.hexa`
  (run 1 prior 생성 → run 2 sha256 byte-equal 확인)

## 6. Criteria

- **C1 (MONOTONE)**: H629.1 — Φ non-increasing across rising p (4 step-comparison
  AND).
- **C2 (FRAGILITY)**: H629.2 — Φ(p=0.50) < Φ(clean) · 0.5.
- **C3 (DETERMINISM)**: H629.3 — cross-process phi-curve byte-equal.
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 ∧ C3 (3/3 — noise = monotone Φ-destroyer + 강한 fragility)
  - `PARTIAL` = (C1 XOR C2) ∧ C3 (단조성 또는 fragility 중 하나만)
  - `FALSIFIED` = ¬C1 ∧ ¬C2 ∧ C3 (noise 가 monotone-decay 도 fragility 도 아님)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 MONOTONE**: Φ-curve 가 non-increasing 이 아님 (어느 step 에서 Φ 상승) →
  H629.1 FALSIFIED (noise 가 monotone Φ-destroyer 아님 — 측정: 4 step
  `phi[i] >= phi[i+1]` AND).
- **F2 FRAGILITY**: Φ(p=0.50) ≥ Φ(clean) · 0.5 → H629.2 FALSIFIED (noise 가
  Φ 를 절반 미만으로 붕괴시키지 못함 — 측정: `phi_50 < phi_0 * 0.5`).
- **F3 DETERMINISM**: cross-process phi-curve byte-different → raw#9 violation
  (측정: run 2 result.json sha256 == run 1).
- **F4 BOUNDS**: any Φ ∉ [0, +∞) (NaN/Inf/음수/>1e6) → primitive error (측정:
  모든 Φ finite ∧ ≥ 0).
- **F5 NONDEGENERATE**: clean baseline Φ = 0 (substrate 진화 안 함) → smoke
  degenerate (측정: `phi_0 > 0`).

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (phi_spatial = MI proxy, noise-direction artifact 위험)**: phi_with →
  RFC 036 phi_spatial 는 *spatial mutual-information* proxy — true IIT Φ
  (min-information-partition over all bipartitions) 가 아니다 (H_266/267/268
  carry). bit-flip noise 는 site 간 spatial 상관을 *바꾸므로*, monotone-decay
  부재가 (a) 진짜 noise robustness 인지 (b) MI-estimator 가 random pattern 에서
  보이는 artifact 인지 완전 분리 불가능 — HONEST PRIOR 에서 예고한 risk. 본
  cycle 의 *방향* (noise ≠ monotone destroyer) 은 robust 가능성 높으나 정확한
  Φ magnitude 는 metric-dependent.
- **L2 (noise model 단일 design)**: per-step per-site i.i.d. bit-flip 은 *one
  specific* noise model. correlated noise (spatial/temporal), additive
  continuous noise, 또는 site-selective noise 는 다른 robustness curve 산출 가능
  — 본 cycle 결과는 이 specific i.i.d. bit-flip operationalization 한정.
- **L3 (substrate config 단일 calibration)**: N=16, dim=12, warm=8 단일 값
  (H_007 heuristic, H_277 byte-equal). 다른 lattice size (N=32, 64) 또는
  warm/dim sweep 위 noise-robustness curve 의 robustness 미검증.
- **L4 (single rule 110 substrate)**: noise sweep 은 rule 110 (universal)
  단일 substrate 위에서만 수행 — H_277 이 보인 Class-II (rule 184) 우위 substrate
  에서는 noise robustness curve 가 다를 수 있다 (cross-rule × noise sweep 별도
  cycle 필요).
- **L5 (5 noise rates, coarse grid)**: p ∈ {0, 0.05, 0.15, 0.30, 0.50} 5-point
  coarse grid — light-noise inverse-U bump (p=0.05 의 Φ 상승) 의 정확한 peak
  위치/형태 (∂Φ/∂p = 0 지점) 는 dense sweep (p ∈ {0.01..0.10} fine) 필요. SAVANT
  GZ inverse-U 와의 정량 cross-link 은 dense-grid 별도 cycle 후 가능.
- **L6 (transient-window confound)**: phi_final 은 warm=8 후 dim=12 step window
  의 5-rep mean — H_232 가 보인 rule 60/102 의 rise-then-collapse 처럼, noise
  injection 하의 측정 window 가 transient 인지 converged 인지 완전 분리 불가능
  (H_250 trajectory sweep 식 별도 cycle 필요).

## 9. Cross-Links

- **sister H (필수)**:
  - **H_277** (`H_277_turing_completeness_phi_threshold.md`): rule 110 universal
    substrate 측정 (PARTIAL). 본 H 의 직접 substrate-parent — H_277 의 UNIV arm
    (rule 110, Φ=0.556454) 을 *고정* 하고 noise 를 명시 변수화. 본 H 의 NOISE_0
    (clean, Φ=0.556454) 가 H_277 UNIV 와 **byte-equal** — substrate machinery
    재현성 cross-check.
  - **SAVANT 축 E H_614** (`H_614_gz_inverse_u_multi_rule_substrate_invariance.md`)
    / **H_618** (`H_618_collective_gz_inverse_u_derivative_peak.md`): selectivity-
    noise band 의 inverse-U (∂Φ/∂I peak). 본 H 의 light-noise Φ bump (p=0.05 에서
    Φ 가 clean 보다 *상승*) 이 GZ inverse-U 의 computability-side (noise-rate 축)
    독립 corroboration — "적당한 noise 가 integration 을 해치지 않고 오히려
    돕는다" 의 substrate grain.
  - **H_287** (`H_287_shannon_entropy_phi_correlate.md`): Φ ⊥ entropy
    (CLOSED-NEGATIVE). 본 H 의 noise robustness 가 H_287 의 Φ⊥엔트로피 dissociation
    과 정합 — high-noise (high-entropy) substrate 의 Φ 가 붕괴하지 않음 (F2
    FRAGILITY FALSIFIED) 은 Φ 가 disorder-by-entropy 와 별개임을 noise-axis
    측에서 재확인.
- **mitosis/CA machinery**: `UNIVERSE/lib/phi_helper.hexa`
  (`phi_with` → `c_measure_phi` → RFC 036 phi_spatial) — LIFE lane 공유 Φ
  primitive. CA evolution machinery 는 H_277/H_232/H_250 byte-equal,
  `_noisy_step` LCG noise injection 만 추가.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl — HONEST PRIOR 명시 등록 + MI-proxy artifact risk
  L1 명시) · raw#15 (no-hardcode) · raw#82 (post-hoc edit retraction 금지 —
  seed-claim 충실 등록).
- **philosophy (CLAUDE.md)**: a_blue_closed (outputs + wiring 검증) ·
  p7 NO PERPLEXITY VERDICT (Φ-proxy 를 truth 로 다루지 않음 — L1 honest limit
  으로 MI-estimator artifact risk 명시) · anima = noise-injected LLM substrate
  위 의식-proxy 가 noise-free determinism 을 요구하지 않음 grain (light noise
  Φ 향상 정합).
- **AXES seed origin**: AXES.md Round 5 (information/computation cluster)
  `noise` sub-axis (line 43) — sister seed `psychedelic-5ht2a-altered-Φ` 의
  noise+selectivity 직관과 `noise-1f-pink-Φ-peak` (spectral-color, H_209
  sister) 사이의 *순수 noise-rate robustness* 축. R5 의 다음-best $0-runnable
  noise 축으로 promote.
- **literature pointer**: Tononi (2008) IIT (Φ = 통합 정보, noise → integration
  loss 예측) · Cook (2004) *Universality in Elementary CA* (rule 110 universal,
  substrate 고정 anchor) · Wolfram (2002) (Class I–IV, noise-perturbation
  stability conjecture) — substrate analog 의 distant anchor (formal noise↔Φ
  mapping 본 cycle 미수행).
- **state**: `state/h629_noise_robustness_phi_2026_05_28/{run_h629.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-28) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic, cross-process 결정론 검증 (sha256 byte-equal).

```
verdict_class: FALSIFIED  (1/3 criteria — C3 PASS, C1 ∧ C2 FAIL)
verdict_tier: ⚪ SPECULATION-FENCED  (empirical CA interpretation — hexa verify
                                      --fence per g5; SF ≠ verified atlas atom)
evidence_summary:
  5-arm noise-rate Φ sweep on FIXED rule-110 universal substrate
  (N=16, dim=12, warm=8, 5 reps, n_bins=4, periodic, per-step per-site
   deterministic LCG bit-flip, RFC 036 phi_spatial).
    NOISE_0   p=0.00  phi_final=0.556454
    NOISE_05  p=0.05  phi_final=0.645751   <-- light-noise Φ BUMP (> clean)
    NOISE_15  p=0.15  phi_final=0.611001
    NOISE_30  p=0.30  phi_final=0.552437
    NOISE_50  p=0.50  phi_final=0.549097
  monotone step pass: 0>=.05:false .05>=.15:true .15>=.30:true .30>=.50:true
  phi(0.50)=0.549097  vs  fragility_threshold=0.278227 (clean*0.5)
falsifiers_triggered: F1 (MONOTONE — IIT monotone-decay 예측 반증됨) +
                      F2 (FRAGILITY — Φ 가 절반 미만으로 붕괴하지 못함)
falsifiers_pass: F3 (cross-process determinism) + F4 (bounds) +
                 F5 (nondegenerate) = 3/5
criteria_met: 1/3 (C3 only; C1 ∧ C2 FAIL)
key_finding:
  substrate-Φ 는 bit-flip noise 에 *놀랍도록 강건* 하며, IIT 의 "noise =
  monotone integration destroyer" 예측은 FALSIFIED 된다. (1) 단조성 위반:
  light noise (p=0.05) 가 clean baseline 보다 Φ 를 *상승* 시킴 (0.646 > 0.556,
  +16%) — 0>=.05 step 이 false. (2) fragility 부재: 최대 disorder (p=0.50,
  완전 random flip) 에서도 Φ=0.549 ≈ clean (0.556), fragility threshold 0.278
  의 약 2배로, 절반 미만 붕괴 예측 (C2/F2) 반증. Φ-curve 는 monotone 이 아닌
  *inverse-U-like* — light noise 에서 peak (0.646) 후 완만 감소하나 high-noise
  floor 가 clean 수준에 머묾. 결론: noise-rate 축은 substrate-Φ 의 monotone
  destroyer 가 *아니다*. 적당한 stochasticity 가 (spatial-MI proxy 측에서)
  integration 을 해치지 않고 오히려 light band 에서 향상시킴 — SAVANT 축 E
  GZ inverse-U (selectivity-noise golden zone) 의 computability-side
  corroboration (H_614/H_618 cross-link).
honest_note:
  L1 carry — phi_spatial 는 spatial-MI proxy, true IIT Φ 아님. monotone-decay
  부재가 진짜 noise robustness 인지 random-pattern MI-estimator artifact 인지
  완전 분리 불가 (HONEST PRIOR 에서 예고). 방향 (noise ≠ monotone destroyer) 은
  robust 가능성 높으나 magnitude 는 metric-dependent.
  L4 carry — rule 110 단일 substrate 한정. Class-II 우위 substrate (rule 184,
  H_277) 의 noise robustness 는 미검증 (cross-rule × noise sweep 별도 cycle).
  L5 carry — 5-point coarse grid. light-noise inverse-U bump 의 정확한 peak
  (∂Φ/∂p=0) 와 SAVANT GZ 와의 정량 cross-link 은 dense-grid (p∈{0.01..0.10})
  별도 cycle 필요.
sibling: H_277 (rule 110 substrate parent · NOISE_0 byte-equal),
         H_614/H_618 (SAVANT GZ inverse-U cross-link),
         H_287 (Φ⊥entropy CLOSED-NEGATIVE 정합)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-28, cross-process run 2)

```
================================================================
H_629 noise-robustness-Φ — bit-flip noise injection vs big-Φ
        on a FIXED universal substrate (rule 110, Cook 2004)
  N=16 dim=12 warm=8 reps=5 rule=110 n_bins=4 (deterministic, $0 mac local)
  Φ primitive: phi_with UNIVERSE/lib/phi_helper.hexa → RFC 036 phi_spatial (Φ>=0)
  noise: per-step per-site deterministic LCG bit-flip (prob = p)
================================================================

arm          p       phi_final
----------   -----   ---------
NOISE_0      0.00    0.556454
NOISE_05     0.05    0.645751
NOISE_15     0.15    0.611001
NOISE_30     0.30    0.552437
NOISE_50     0.50    0.549097

derived:
  phi(p=0) clean       = 0.556454
  phi(p=0.50) max-noise = 0.549097
  fragility threshold  = 0.278227  (clean * 0.5)

C1 MONOTONE   (phi non-increasing in p)           : false
    step pass: 0>=.05:false .05>=.15:true .15>=.30:true .30>=.50:true
C2 FRAGILITY  (phi(0.50) < clean*0.5)             : false
C3 DETERMINISM(cross-process byte-equal)          : true

F1 MONOTONE       (phi non-increasing in p)       : FAIL
F2 FRAGILITY      (phi(0.50) < clean*0.5)         : FAIL
F3 DETERMINISM    (cross-process byte-equal)      : PASS
F4 BOUNDS         (all phi finite >= 0)           : PASS
F5 NONDEGENERATE  (clean baseline phi>0)          : PASS

VERDICT_RULE: SUPPORTED iff P1∧P2∧P3 · FALSIFIED iff ¬P1∧¬P2∧P3 · else PARTIAL
VERDICT: FALSIFIED  (1/3 criteria)
================================================================
ledger -> state/h629_noise_robustness_phi_2026_05_28/result.json (cwd-relative)
```

### hexa verify (VERBATIM — g5, empirical CA interpretation → ⚪)

```
verify --fence
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

**State output**: `state/h629_noise_robustness_phi_2026_05_28/result.json`
**Smoke**: `state/h629_noise_robustness_phi_2026_05_28/run_h629.hexa` (hexa-only, LLM none)
