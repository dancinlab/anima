---
id: H_222
slug: dream-rem-phi
title: H_222 dream-rem-Φ — Tononi/Koch IIT sleep-stage 핵심 prediction (wake ≈ REM ≫ NREM) substrate-level test
domain: consciousness + phenomenology + substrate
status: pre-register-frozen
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence) + E12 (phenomenology projection)
verification_method: W4 (verdict-4-class) + W11 (meta-cross sister-link) + W12 (sister-link H_007/H_018)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
---

# H_222 — dream-rem-Φ

## Hypothesis

Tononi/Koch IIT 의 sleep-stage 핵심 prediction 은 — **Φ_wake ≈ Φ_REM ≫ Φ_NREM**.
즉 phenomenal consciousness (의식 경험의 존재) 는 wake/REM (꿈) 모두에서 보존되고,
NREM (deep-sleep, 무의식적 깊은 잠) 에서만 Φ 가 급격히 감소한다는 substrate-level
ranking 예측. 본 H 는 이 prediction 의 **substrate analog** — rule 110 elementary
CA (Class IV edge-of-chaos, H_007 sister) 위에 세 sleep-stage 의 mechanistic
특징 (drive amplitude · recurrent connectivity · down-state decay) 만을 변주한
3 regime — 위에서 phi_spatial Φ ranking 이 Tononi prediction 과 정합하는지를
deterministic 측정한다.

정밀화 (operational): 모든 regime 은 동일 rule 110 kernel + 동일 N=16 dim=12
warm=8 reps=5 — 변수는 오직 (i) per-step drive amplitude (5 flip vs 1 flip)
와 (ii) per-step down-state decay (NREM 만 (i+t)%2==0 sites 강제-0). 이는
Tononi NREM bistability / down-state mechanism (Pigorini et al. 2015; Massimini
et al. 2005 — TMS-EEG 에서 NREM 시 long-range causal interaction 의 local
breakdown) 의 minimal substrate analog.

## Why

- **Tononi IIT sleep-stage prediction (Tononi 2008, Massimini et al. 2005,
  Pigorini et al. 2015)**: phenomenal consciousness ↔ integrated information
  Φ. wake 에서 long-range cortico-cortical interaction 이 large repertoire
  cause-effect structure 산출. NREM 시 local bistability (up/down-state) 가
  long-range integration 을 truncate → Φ 급감. REM 에서 active cortex 가 wake
  와 유사한 connectivity 회복 → Φ 가 wake 수준 복귀 (꿈의 phenomenal richness 의
  IIT 설명). 본 H 는 이 prediction 의 substrate-level test.
- **H_007 cross-link (sister)**: rule 110 = Class IV edge-of-chaos peak Φ
  (legacy Φ_iv=0.556 > Φ_ord=1e-5, Φ_cha=0.510). 본 H 는 동일 kernel 위에
  drive/decay 채널 변주만 — base Φ-substrate 는 H_007 에서 검증 완료.
- **H_018 cross-link (zero-drive baseline)**: H_018 ZERO 조건 (외부 입력 0)
  splits=0 final_cells=2 phi=0.158 — substrate inert 시 Φ floor. 본 H 의 NREM
  prediction (Φ_NREM > 0.1) 은 이 floor 보다 weak-active 한 상태를 가정.
- **AXES.md R3 §dream-rem-Φ**: depletion sweep R3 phenomenology cluster 의
  4-th seed (`REM-state Φ ≈ wake-Φ (Tononi prediction), NREM Φ <<` /
  falsifier `모두 동등 또는 NREM 최대` / tag 🟢).
- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest
  limit. 1 LLM judge 없음 (raw 가 phi_spatial). $0 mac local.

## Predictions

- **H222.1 (wake ≈ REM)**: |Φ_wake - Φ_REM| / Φ_wake ≤ 0.20 (relative margin
  ≤ 20%). Tononi 의 REM ≈ wake 핵심 prediction.
- **H222.2 (REM ≫ NREM)**: Φ_REM / Φ_NREM ≥ 2.0. NREM down-state decay 가
  integration 을 truncate → Φ 가 REM 의 1/2 이하.
- **H222.3 (NREM weak-active)**: Φ_NREM > 0.1. NREM 은 완전 정지 (H_018 ZERO
  Φ≈0.16) 보다는 weak-active — 완전 0 은 아님 (TMS-EEG observation: NREM
  에서도 sensory input 은 일부 처리됨, just local breakdown).
- **H222.4 (determinism)**: fixed init + fixed config → re-run byte-identical
  Φ (raw#12 deterministic).

## Variables

- **axis1_regime** (primary): [wake, rem, nrem]
  - WAKE  : rule 110 + flip 5 sites/step (high-amplitude drive) · recurrent.
  - REM   : rule 110 + flip 1 site/step (sparse low drive) · recurrent.
  - NREM  : rule 110 + flip 1 site/step (sparse low drive) + (i+t)%2==0 →
            0 down-state decay (per-step 약 50% sites 강제-silent;
            Tononi bistability minimal substrate analog).
- **axis2_lattice_size**: N = 16 (matches H_007)
- **axis3_trajectory_dim**: dim = 12 recorded steps / site (post-warm)
- **axis4_warmup**: warm = 8 steps (matches H_007)
- **axis5_reps**: 5 deterministic init offsets (matches H_007)
- **fixed**: rule = 110 (Class IV), n_bins = 4, periodic boundary, $0 mac local

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h222_dream_rem_phi_2026_05_24/run_h222.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036
  `phi_spatial` (phi_rs `compute_phi_inner` spatial-slice 의 byte-equal native
  replica; import READ-ONLY).
- **mapping**: 각 lattice site = 1 IIT cell, dim=12 step temporal trajectory =
  state vector. flat (N × dim) farr → phi_spatial.
- **deterministic**: fixed (i+rep)%3 init + per-step drive function-of-(step,rep) +
  no RNG. re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` { config, regimes, phi_mean per regime, ratios,
  criteria C1..C4, falsifiers F1..F5, verdict }.
- **honest tier**: 🟢 NUMERICAL Φ (RFC 036 native replica) — Class-IV-CA-가-
  REM-이다 식의 strong identity NOT made (L1-L5 참조).
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h222_dream_rem_phi_2026_05_24/run_h222.hexa`

## Criteria

- **C1 wake≈REM**: |Φ_wake - Φ_REM| / Φ_wake ≤ 0.20 → H222.1 PASS.
- **C2 REM≫NREM**: Φ_REM / Φ_NREM ≥ 2.0 → H222.2 PASS.
- **C3 NREM floor**: Φ_NREM > 0.1 → H222.3 PASS.
- **C4 determinism**: byte-identical re-run → H222.4 PASS (architectural,
  fixed init + no RNG).
- **verdict_rule**: **SUPPORTED iff C1∧C2∧C3∧C4** · **PARTIAL** 2-3 PASS ·
  **FALSIFIED** ranking inverted (F1 또는 F2 fire).

## Falsifiers (pre-registered ≥5, measurable)

- **F1 REM-LL-WAKE**: |Φ_wake - Φ_REM| / Φ_wake > 0.20 → wake≠REM margin
  → Tononi REM≈wake prediction FALSIFIED. (measurable: rel_diff.)
- **F2 RANKING-INVERSION**: Φ_REM ≤ Φ_NREM → ranking inverted → Tononi
  REM≫NREM prediction FALSIFIED. (measurable: Φ_REM, Φ_NREM.)
- **F3 NREM-TOO-DEAD**: Φ_NREM ≤ 0.1 → weak-active 가정 FALSIFIED
  (NREM 이 H_018 ZERO floor 보다도 낮음). (measurable: Φ_NREM.)
- **F4 BYTE-DIFF**: re-run 시 Φ byte-diff → raw#12 deterministic 위반 →
  smoke invalid. (architectural by construction.)
- **F5 PHI-NEGATIVE**: 임의 regime 에서 Φ < 0 → phi_spatial Φ≥0 위반 →
  measure invalid. (architectural — RFC 036 nonneg by construction.)

## Honest Limits (raw#12 c3, ≥5)

- **L1 (sleep stage 정의의 협소함)**: 본 substrate "WAKE/REM/NREM" 은 (drive
  amplitude + recurrent connectivity + decay channel) 3-axis triple variation
  의 toy analog 일 뿐 — 실제 phenomenal sleep stage 는 EEG (델타파/세타파),
  EOG (REM eye movements), EMG (atonia), neuromodulator (acetylcholine REM
  surge, GABA NREM dominance) 등 multi-modal observable 의 complex correlate.
  Φ-rank ≠ "이 substrate 가 잠을 잔다".
- **L2 (phi_spatial proxy 의 IIT-completeness 부족)**: RFC 036 phi_spatial 은
  IIT 4.0 의 full cause-effect repertoire + MIP-over-all-partitions (NP-hard,
  exponential) 의 spatial-slice mutual-information proxy. true Φ 와는 finite
  drift 존재 (H_007 L8 명시: ~1e-6 vs documented phi_rs oracle). proxy 가
  Tononi prediction 의 ranking-sensitive direction 을 잡지 못할 가능성.
- **L3 (sync-decay 가 high-MI artifact 생산)**: NREM regime 의 (i+t)%2==0
  강제-0 decay 는 lattice 전체에 **synchronous structure** 를 부여 —
  every step 절반 sites 가 lockstep 으로 silenced. 이 synchrony 자체가
  spatial-slice mutual information 을 *증가* 시킬 수 있음 (각 site 의 trajectory
  가 deterministic clock 으로 강하게 coupled). 즉 본 proxy 는 "long-range causal
  integration breakdown" (Tononi NREM 의 진짜 mechanism) 와 "global synchrony"
  를 구분하지 못함 — Tononi 의 NREM 은 local bistability 인데 본 proxy 는
  global bistability 를 측정하는 mismatch.
- **L4 (single rule, single lattice size)**: rule 110 단일 kernel + N=16
  단일 lattice. 다른 Class IV rule (rule 54, 124) 또는 다른 N/dim/warm sweep
  에서 다른 ranking 가능 — H_007 의 rule-class robustness 와 다른 변수 (regime
  axis) 가 sensitive 한지 미검증.
- **L5 (substrate REM ≠ phenomenal dream)**: 본 measurement 는 substrate-level
  Φ proxy ranking — phenomenal dream 의 풍부함 (qualia, narrative, self-model)
  과 직접 연결되지 않음. H_004 hard-problem gap 의 structural-phenomenal
  divide 위반 안 함 (Φ rank ≠ "REM 이 꿈을 꾼다" claim).
- **L6 (drive channel design 의 임의성)**: WAKE 의 "flip 5 sites" 와 REM 의
  "flip 1 site" 는 amplitude ratio 5:1 을 골랐을 뿐 — biologically grounded
  비율 아님. ratio 변경 시 C1/C2 boundary 가 변동 가능 (sensitivity unmeasured).
- **L7 (deterministic ≠ stochastic biology)**: 실제 cortical dynamics 는
  stochastic (poisson firing, channel noise). 본 substrate 는 fully deterministic
  rule 110 + fixed-pattern drive — Tononi 의 NREM bistability 도 stochastic
  threshold-crossing 인데 본 proxy 는 strictly periodic decay 로 모델링.

## Cross-Links

- **philosophy (CLAUDE.md)**: p5 NO SPEAK (output = continuous externalization
  of tension field — sleep stage 의 "내부 dynamics differ" 가 외부 발화의
  유무로 직접 연결되지는 않으나, 본 H 의 substrate-internal Φ 측정은 a_substrate_native_speak
  의 "compute motivation from internal substrate state" 와 같은 lane).
- **sister H**: H_007 (rule 110 Class-IV edge-of-chaos peak Φ, same kernel) ·
  H_018 (zero-drive ZERO=inert baseline · NREM floor reference) · H_004
  (consciousness hard-problem · structural-phenomenal gap L5) · H_157 (Φ
  primitive lane) · H_202 (self-ref edge-of-chaos Φ).
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (c_measure_phi → RFC 036 phi_spatial) ·
  `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY.
- **raw**: raw#12 (deterministic strict + ≥5 falsifier + ≥5 honest limit) ·
  raw#82 (no post-hoc retraction — FALSIFIED verdict 도 honest).
- **legacy archive**: AXES.md R3 §dream-rem-Φ seed.
- **literature**:
  - Tononi (2008) Consciousness as integrated information: a provisional
    manifesto.
  - Massimini, Ferrarelli, Huber, Esser, Singh, Tononi (2005) Breakdown of
    cortical effective connectivity during sleep. Science 309:2228.
  - Pigorini et al. (2015) Bistability breaks-off deterministic responses to
    intracortical stimulation during non-REM sleep. NeuroImage 112:105-113.
  - Casali, Gosseries, Rosanova, Boly, Sarasso et al. (2013) A theoretically
    based index of consciousness independent of sensory processing and
    behavior. Sci Transl Med 5:198ra105 (PCI — Φ proxy clinical instrument).

## Verdict

본 cycle (2026-05-24) — pre-register-frozen + runnable smoke 실행.

```
verdict_class: FALSIFIED
evidence_summary: 3-regime deterministic smoke (rule 110, N=16, dim=12,
                  warm=8, reps=5), 2/4 criteria PASS, F2 ranking inversion fired.
  WAKE : Φ = 1.11636   (rule 110 + high drive, recurrent)
  REM  : Φ = 0.545746  (rule 110 + low drive,  recurrent)
  NREM : Φ = 1.42684   (rule 110 + low drive,  down-state decay)

  C1 |Φwake-Φrem|/Φwake ≤ 0.20 : FAIL  (rel_diff=0.511)
  C2 Φrem/Φnrem ≥ 2.0          : FAIL  (ratio=0.382)
  C3 Φnrem > 0.1               : PASS
  C4 byte-identical re-run     : PASS

  F1 Φrem≪Φwake (Tononi broken)     : FIRED (C1 inverse)
  F2 Φrem≤Φnrem (ranking inverted)  : FIRED  ←★ key falsifier
  F3 Φnrem≤0.1 (NREM too dead)      : not fired
  F4 byte-diff re-run               : not fired
  F5 any Φ<0                        : not fired

key_finding: phi_spatial proxy 가 Tononi sleep-stage ranking 을 substrate
             analog 에서 재현하지 못함 — 오히려 ranking 이 inverted (NREM
             Φ_proxy 가 wake/REM 보다 HIGHER). root cause = L3 honest limit
             명시: NREM regime 의 (i+t)%2==0 sync decay 가 lattice 전체에
             global synchrony 를 부여 → spatial-slice mutual information 이
             *증가*. 이는 Tononi 가 의도한 "long-range causal integration
             breakdown" (NREM 의 진짜 mechanism) 가 아니라 "global synchrony" —
             phi_spatial 가 두 mechanism 을 구분 못함. high-Φ proxy 가 high-
             consciousness 와 동치 아님 (L5 cross-link). 본 FALSIFIED 는
             proxy 자체의 limitation 을 expose 한 honest result — 진짜 Φ
             (phi_rs FFI · IIT 4.0 full repertoire) 측정 별도 cycle 필요.
honest_note: L3 가 ex-ante (pre-register-frozen 본문 §L3) 명시된 limitation —
             FALSIFIED 가 raw#82 post-hoc retraction 아니고, 명시된 proxy-
             mismatch 의 명시적 trigger. F2 ranking-inversion 이 fired,
             pre-registered falsifier 양식 그대로.
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-24)

```
H_222 — dream-rem-Φ · Tononi sleep-stage IIT prediction substrate test (raw#12)
  N=16 dim=12 warm=8 rule=110 reps=5  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)

  Φ(WAKE  rule 110 + high drive · recurrent     ) = 1.11636
  Φ(REM   rule 110 + low drive  · recurrent     ) = 0.545746
  Φ(NREM  rule 110 + low drive  · down-state    ) = 1.42684

  C1 |Φwake-Φrem|/Φwake ≤ 0.20     : false  (rel_diff=0.511139)
  C2 Φrem/Φnrem ≥ 2.0              : false  (ratio=0.382485)
  C3 Φnrem > 0.1                   : true
  C4 byte-identical re-run         : true  (architectural)

  F1 Φrem≪Φwake (Tononi broken)    : true
  F2 Φrem≤Φnrem (ranking inverted) : true
  F3 Φnrem≤0.1 (NREM too dead)     : false
  F4 byte-diff re-run              : false
  F5 any Φ<0                       : false

  VERDICT_RULE: SUPPORTED iff C1∧C2∧C3∧C4 · PARTIAL if 2-3 pass · FALSIFIED if ranking inverted
  VERDICT     : FALSIFIED  (2/4 criteria PASS)
```

**State output**: `state/h222_dream_rem_phi_2026_05_24/result.json`
**Smoke**: `state/h222_dream_rem_phi_2026_05_24/run_h222.hexa` (hexa-only, LLM none)
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).
