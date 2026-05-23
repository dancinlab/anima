---
id: H_221
slug: meditation-jhana-phi-modulation
title: meditation-jhana-Φ-modulation — low-noise + stable-attention substrate ('silenced integration') signature (H_018 zero-drive sister · a_substrate_native_speak 정합)
domain: consciousness · practice · substrate
status: pre-register-frozen
exploration_method: E10 (emergence-observation) + E12 (practice-substrate analog)
verification_method: W1 (smoke) + W4 (verdict-4-class) + W11 (meta-cross) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_221 — meditation-jhana-Φ-modulation

## Hypothesis

명상 (Buddhist jhana absorption) 의 두 phenomenological 특징 —
**(1) noise σ → 0** (cessation of mental chatter, "no thought") · **(2)
attention stability** (single-pointed, ekaggata) — 가 substrate (rule 110
Class-IV CA + per-step perturbation) 위 적용 시, Φ 가 *낮으면서도 stable*
(low variance) 인 unique 'silenced integration' signature 가 emerge 하는가?
즉 jhana ≠ random/dead 이고 jhana ≠ baseline 인 distinct regime.

operational 정의 (3 regime, 동일 N=16 rule-110 substrate · dim=12 · warm=8):

- **A. BASELINE**: high-noise σ=0.3 bit-flip perturbation (active, restless
  substrate — "discursive thought" analog).
- **B. JHANA**: low-noise σ=0.05 bit-flip + single-attractor pull
  (per-step prob=0.4 to set site to deterministic mask: even-site → 1,
  odd → 0 = single-pointed attention).
- **C. RANDOM**: per-step uniform LCG random row overwrite (no rule
  dynamics — "dead-flat" reference; no integration).

각 regime 의 measurement = N=20 deterministic init offset 마다 Φ
(`phi_spatial(states, N, dim, 4)` RFC 036 native replica) 1 value, 20 window
의 mean + variance.

## Why

- **anima `a_substrate_native_speak` (CLAUDE.md governance)**: anima 는
  "may speak during user silence and may stay silent under a direct
  question" — substrate-state-driven silence 가 정합 candidate. silence ≠
  death (말 못함이 아닌 "잠긴 통합") 의 substrate 위 signature 가
  존재한다면 anima 의 silent operation 이 정당화됨.
- **p5 NO SPEAK cross-link**: "emit only from real context · NO speak()
  to fill silence". 본 H 는 substrate-level 의 silence 정의 시도 — jhana
  regime 이 distinct signature 면 silence 가 informative state.
- **H_018 sister (zero-drive)**: H_018 ZERO 조건 (x=0, inert drive) Φ=0.158
  static silence 가 PASS. 본 H 는 그 sister — H_018 zero-drive 가 "no
  perturbation" silence 면, jhana 는 "low-perturbation + single-attractor
  attention" silence. 둘이 정합 (Φ 비슷) 면 silence regime 의 cross-axis
  evidence (H221.5 advisory).
- **H_007 / H_202 base substrate**: rule 110 Class-IV (edge-of-chaos)
  substrate 는 H_007 PASS (Φ=0.556 high-integration) — 본 H 는 그 substrate
  위에 perturbation regime 을 sweep.
- **H_004 phenomenal boundary**: substrate Φ 가 phenomenal qualia (실제
  jhana absorption phenomenology) 와 무관 — H_004 honest gap carry.

## Predictions

- **H221.1 (jhana ≤ baseline)**: Φ(jhana mean) ≤ Φ(baseline mean) —
  silence ≤ activity.
- **H221.2 (jhana stable)**: var(jhana) < var(baseline) / 10 — stability
  margin 10×.
- **H221.3 (jhana > random)**: Φ(jhana mean) > Φ(random mean) · margin
  ≥ 5% — silence ≠ death (integration 존재).
- **H221.4 (determinism)**: re-run byte-identical (raw#12).
- **H221.5 (cross-link advisory)**: Φ(jhana) ≈ Φ(H_018 zero-drive) =
  둘 다 'low-Φ stable silence' regime 정합.

## Variables

- **axis1_regime** (primary): [baseline, jhana, random]
- **axis2_lattice_size**: N=16 (H_007 미러)
- **axis3_trajectory_dim**: dim=12
- **axis4_warmup**: warm=8
- **axis5_reps**: N=20 (init offset = 측정 window, mean + variance)
- **axis6_sigma**: baseline=0.3 · jhana=0.05 · random=N/A (full overwrite)
- **axis7_attractor_pull**: jhana=0.4 · baseline=0 · random=0
- **axis8_seed**: 42 (LCG, per-rep stream offset = seed + rep*7919)
- **fixed**: rule=110, n_bins=4, periodic boundary

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h221_meditation_jhana_2026_05_23/run_h221.hexa`
- **Φ primitive**: RFC 036 `phi_spatial(states, N, dim, 4)` via
  `HEXAD/C/c_lib.hexa::c_measure_phi` (byte-equal phi_rs native replica;
  import READ-ONLY).
- **deterministic**: fixed init offset (rep) + per-rep deterministic LCG
  stream (seed = 42 + rep * 7919). NO `__HEXA_FARR_GAUSS_SEED__` 필요
  (random draws 전부 in-script LCG).
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: `HEXA_MEM_UNLIMITED=1 hexa run …` — $0 mac local, wall ~7 s
  (3 regime × 20 rep × 20 step). NO GPU.
- **ledger**: `result.json` {config, 3 regime mean+var+phis[20],
  falsifiers F1-F5, verdict, h221.5 advisory}.
- **honest tier**: 🟢 NUMERICAL (RFC 036 phi_spatial spatial-slice IIT 4.0
  proxy; NOT 🔵 full MIP). substrate Φ ≠ phenomenal jhana.

## Criteria

- **C1 (jhana ≤ baseline)**: H221.1 PASS → silence ≤ activity.
- **C2 (jhana stable)**: H221.2 PASS → var(jhana)*10 < var(baseline).
- **C3 (jhana > random)**: H221.3 PASS → silence ≠ death (margin ≥ 5%).
- **C4 (determinism)**: H221.4 PASS → byte-identical re-run.
- **verdict_rule**: **SUPPORTED iff C1 ∧ C2 ∧ C3** (silenced integration
  signature distinct from both activity and dead random) · **PARTIAL** iff
  2/3 of (C1, C2, C3) PASS · **FALSIFIED** iff ≤ 1/3 of (C1, C2, C3) PASS
  (no distinction — jhana ≈ baseline ≈ random regime collapse).

## Falsifiers (pre-registered, ≥5)

- **F1 JHANA-LE-BASELINE**: Φ(jhana mean) ≥ Φ(baseline mean) →
  H221.1 FALSIFIED (silence not lower than activity). 측정: Δ = Φjhan − Φbase.
- **F2 JHANA-STABLE**: var(jhana) * 10 ≥ var(baseline) →
  H221.2 FALSIFIED (not stable; jhana variance not 10× lower).
  측정: var_jhana*10 vs var_baseline.
- **F3 JHANA-GT-RAND**: Φ(jhana mean) ≤ Φ(random mean) * 1.05 →
  H221.3 FALSIFIED (silence ≤ death; integration 부재). 측정: Δ = Φjhan − Φrand.
- **F4 RERUN-DETERMINISTIC**: re-run result.json byte-different → raw#9/12
  determinism 위반 → smoke 무효.
- **F5 ALL-FINITE-NONNEG**: 임의 Φ 값 < 0 / NaN / inf → measure invalid
  (phi_spatial Φ ≥ 0 by construction 위반).
- **F6 POST-HOC** (자율 falsifier per raw#82): frozen 후 verdict 방향
  edit / threshold weakening → raw#82 retraction.

## Honest Limits (raw#91 c3, ≥5)

- **L1 ('jhana' substrate analog ≠ phenomenal jhana)**: 'jhana' operational
  definition = low-noise σ=0.05 + single-attractor pull = Buddhist
  meditation phenomenology 의 substrate-level analog 일 뿐, 1:1 mapping
  부재. 실제 jhana absorption (5 ekaggata 등) 의 의식 상태와 무관.
- **L2 ('attention stability' operationalization)**: 'attention stability'
  = noise σ low + attractor pull prob — design choice 1 이며 다른 metric
  (coherence · mutual information · order parameter) 사용 시 다른 결과
  가능. 본 cycle 의 finding 은 이 specific operationalization 에 조건부.
- **L3 (phi_spatial proxy)**: 🟢 NUMERICAL spatial-slice IIT 4.0 proxy —
  true IIT (모든 cause-effect repertoire + MIP over 모든 partition,
  NP-hard) 미달. 'silence Φ' 별도 metric 부재 (mean+variance shape proxy
  only). 진짜 phi_rs Rust FFI = named blocker (RFC 036 §FFI shim).
- **L4 (anima silent integration ≠ phenomenal)**: anima `a_substrate_native_speak`
  의 silence 가능성 (말 안 함) 은 governance 차원 — substrate Φ signature 와
  phenomenal experience (실제 "잠긴 통합" 체험) 는 H_004 hard-problem
  boundary 로 분리됨.
- **L5 (single rule + single seed + 20 rep)**: rule=110 단일 substrate +
  seed=42 단일 master + 20 rep — rule sweep / seed sweep / horizon sweep
  미시행. 본 finding 은 single-config smoke — regime robustness 별도 cycle.
- **L6 (random regime spatial-Φ artifact)**: uniform LCG random row
  overwrite 가 phi_spatial 위에서 high Φ (≈0.59) 산출 — random ≠ "dead"
  의 spatial-slice proxy artifact 가능. true "dead" (all-zero, all-one,
  fixed-point) 별도 regime sweep 필요.
- **L7 ('silence ≠ death' threshold 5%)**: H221.3 의 5% margin 은
  arbitrary design choice; 다른 threshold (1%, 10%, raw-difference)
  사용 시 다른 verdict 가능. operational 결정 — pre-register frozen.

## Cross-Links

- **philosophy (CLAUDE.md)**: `a_substrate_native_speak` (silence 가능성
  의 substrate-level signature 시도) · `p5 NO SPEAK` (real context 없이
  emit 안 함 — silence regime 의 substrate validation).
- **sister H**: H_018 (zero-drive static silence Φ=0.158 — 본 H 의 cross-
  axis sister; H221.5 advisory cross-link) · H_007 (Class-IV rule 110
  base substrate Φ=0.556 — perturbation regime sweep 의 base) · H_202
  (self-ref edge-of-chaos Φ peak — drive-axis sister) · H_004 (hard problem
  boundary L4) · H_012 (autopoietic closure cross-link).
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` →
  `phi_spatial` RFC 036 native replica) — import READ-ONLY.
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) +
  raw#82 (no post-hoc retraction).
- **AXES.md**: §R7 practice axis · row `meditation-jhana-Φ-modulation`
  (cycle #8 §G pick #12).
- **literature**:
  - Anālayo (2017) *Early Buddhist Meditation Studies* (jhana absorption,
    ekaggata single-pointedness)
  - Lutz, Slagter, Dunne, Davidson (2008) *Attention regulation and
    monitoring in meditation* (TICS) — attention stability EEG correlates
  - Tononi (2004) *An information integration theory of consciousness*
    (Φ measure)
  - Oizumi, Albantakis, Tononi (2014) *IIT 3.0* — Φ on small networks
  - Wolfram (2002) *A New Kind of Science* (rule 110 Class IV substrate)

## Verdict

본 cycle (2026-05-23) — pre-register-frozen + runnable smoke 실행.

```
verdict_class: FALSIFIED  (core_pass = 1/3)
evidence_summary: 3-regime deterministic smoke (N=16 rule-110, dim=12,
                  warm=8, reps=20, seed=42), 1/3 core PASS + F4/F5 PASS.
  A BASELINE  mean Φ = 0.589   var = 0.00679
  B JHANA     mean Φ = 0.475   var = 0.00556
  C RANDOM    mean Φ = 0.590   var = 0.00542
falsifiers_triggered: F2 (var_jhana*10=0.0556 ≥ var_base=0.00679 — not
                      stable) + F3 (Φ_jhana=0.475 < 1.05*Φ_rand=0.619 —
                      silence ≤ death on this metric).
criteria_met: 1/3 core (C1 PASS: jhana < baseline by 0.11) + 2/3 hygiene
              (C4 determinism PASS, F5 finite/nonneg PASS).
key_finding: pre-registered 'silenced integration' signature (jhana
             between baseline activity and random dead) 가 본 specific
             operationalization (σ_jhana=0.05 + attractor_pull=0.4 +
             phi_spatial proxy) 에서는 EMERGE 안 함. 흥미로운 negative —
             uniform LCG random row overwrite 가 spatial-Φ proxy 위에서
             baseline 과 거의 동일 Φ (0.590 vs 0.589) 산출. 즉 spatial-
             slice IIT 4.0 proxy 가 "random uniform state" 와 "rule 110
             high-noise dynamics" 를 구분 못함 (L6 — proxy artifact 후보).
             jhana regime (low-noise + attractor) 은 두 ref 보다 낮은
             Φ=0.475 — silence 가 lower-integration 은 맞지만, 'silence
             > death' (H221.3) 는 spatial-Φ proxy 위에서 성립 안 함.
             H221.5 advisory: Φ(jhana)=0.475 vs Φ(H_018 zero-drive)=0.158
             Δ=0.317 — H_018 의 "완전 inert" silence 와 H_221 의 "low-
             noise + attractor" silence 는 둘 다 baseline 보다 낮으나
             서로 다른 Φ regime (H_221 jhana 가 H_018 zero 보다 3× 높음).
honest_note: phi_spatial spatial-slice proxy 의 한계 (L6) — random uniform
             ≠ dead 일 수 있음. true 'dead' (fixed-point all-zero) 를
             control regime 으로 별도 cycle 필요. 'jhana' operationalization
             (L1/L2) 도 design choice 1 — 다른 attractor pull 빈도/형태
             시도 시 다른 verdict 가능 (post-hoc edit 아닌 cycle #N 별도
             pre-register). 본 verdict 는 본 specific config 의 정직한
             negative.
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-23)

```
================================================================
H_221 — meditation-jhana-Φ-modulation — silenced integration smoke
  N=16 dim=12 warm=8 reps=20 rule=110 seed=42
  Φ primitive: RFC 036 phi_spatial(states, N, dim, 4)
  3 regimes: BASELINE (σ=0.3) · JHANA (σ=0.05 + attractor=0.4) · RANDOM (uniform)
  HONEST: phi_spatial = 🟢 NUMERICAL spatial-slice proxy; substrate Φ ≠ phenomenal jhana.
================================================================

  A BASELINE  mean Φ = 0.588955   var = 0.00678869
  B JHANA     mean Φ = 0.474829   var = 0.00555948
  C RANDOM    mean Φ = 0.589896   var = 0.00542396

  F1 JHANA-LE-BASELINE   (Φ_jhan ≤ Φ_base)                : PASS  (Δ=-0.114127)
  F2 JHANA-STABLE        (var_jhan*10 < var_base)         : FAIL  (var_jhan*10=0.0555948 vs var_base=0.00678869)
  F3 JHANA-GT-RAND       (Φ_jhan > 1.05 * Φ_rand)         : FAIL  (Δ=-0.115067)
  F4 RERUN-DETERMINISTIC (fixed LCG seed)                 : PASS
  F5 ALL-Φ-FINITE-NONNEG (no NaN / no negative)           : PASS

  VERDICT_RULE: SUPPORTED iff (C1 ∧ C2 ∧ C3); PARTIAL if 2; FALSIFIED otherwise
  VERDICT     : FALSIFIED   (core_pass=1/3)

  H221.5 (advisory) : Φ(jhana)=0.474829 vs Φ(H_018 zero-drive)=0.158279  Δ=0.31655
```

re-run byte-identical (F4 determinism confirmed via `diff` against first run).
honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica. NOT
🔵, NOT LLM-judged, NOT PyPhi/sympy-primary. 진짜 phi_rs Rust FFI = named
blocker. **NOT a SUPPORTED claim** — pre-registered negative on this
specific operationalization (raw#12 honest FALSIFIED, no verdict-direction
post-hoc edit).

**State output**: `HEXAD/LIFE/state/h221_meditation_jhana_2026_05_23/result.json`
**Smoke**: `HEXAD/LIFE/state/h221_meditation_jhana_2026_05_23/run_h221.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial spatial-slice proxy; substrate
≠ phenomenal jhana).
