# Phase 6 _integrations/ — Module Inventory + WRAP/PORT Decisions

  raw#9 hexa-only · raw#10 honest C3 · raw#42 host-delegation · raw#65 idempotent
  raw#71 falsifier-preregister · raw#77 audit-jsonl · raw#91 honest-triad
  raw#137 80% Pareto · raw 1 uchg-lock-cycle

  Date: 2026-04-29
  Phase: 6 (after Phase 3 _metrics, Phase 4 _paradigms batch 1, Phase 5 _hw)
  Author: agent: phase6-integrations
  Module count: 7 + 1 _integration_test runner

## Scope

Phase 6 lands the `_integrations/` namespace under `anima-eeg-core/tool/modules/`,
expressing cross-module integrations where multiple metric modules + a paradigm
combine into a higher-level verdict. The dispatcher gains an `integration` verb
namespace (separate from the legacy `integrate` verb that wraps clm-cli /
wearable / mobile bridges).

Race-condition avoidance: this cycle did NOT touch `_metrics/`, `_paradigms/`,
`_hw/`, or `_artifact/`. The dispatcher edit is append-only (new `integration`
verb branch); the help text and list table are extended.

## 7 Modules

| # | module                          | metric stack                | paradigm        | LoC | decision |
|---|---------------------------------|-----------------------------|-----------------|-----|----------|
| 1 | clm_eeg_p1.hexa                 | lz76                        | resting         | 263 | PORT     |
| 2 | clm_eeg_p3.hexa                 | gamma_theta                 | resting         | 269 | PORT     |
| 3 | berger_validate.hexa            | berger (alpha PSD triad)    | resting (eyes-c)| 235 | PORT     |
| 4 | artifact_pipeline.hexa          | 8 detector chain + meta     | resting         | 230 | PORT     |
| 5 | rsn_validate.hexa               | DMN coh + asym + occ alpha  | resting         | 246 | PORT     |
| 6 | cyborg_token_emit.hexa          | EEG segmenter → tokens      | daily-life      | 245 | PORT     |
| 7 | multi_subject_aggregate.hexa    | cohort LZ76                 | resting (N≥3)   | 286 | PORT     |
| - | _integration_test.hexa          | runner                      | -               | 158 | -        |

## WRAP-vs-PORT Decisions (Per Module)

Each decision follows raw#137 80% Pareto: WRAP for legacy backends with raw#12
frozen specs and large LoC (Phase 4 _paradigms pattern). PORT for green-field
synthesis or where legacy dependencies (scipy, numpy, BrainFlow USB, real EEG)
prevent direct selftest invocation under hexa-only constraint.

### 1. clm_eeg_p1.hexa  — DECISION: PORT

  - Legacy backend: anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa (353 LoC)
  - Frozen criteria: C1 lz76≥0.65, C2 |Δ|/human≤0.20
  - Selftest: PORT — LCG seed=42 fixture mirrors legacy synthetic_16ch_v1.json
    pattern-key generator (pattern_key 0..31 mod 32, distinct count → lz76
    proxy ×1000).
  - Live: NOT_YET_LANDED — requires real resting EEG + clm hidden-state
    cross-stream which no current dispatcher reach exposes.
  - Verdict at selftest: PASS  (lz76_proxy_x1000=1000, |Δ|/human=176‰ ≤ 200‰)

### 2. clm_eeg_p3.hexa  — DECISION: PORT

  - Legacy backend: anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa (718 LoC)
  - Frozen criteria: state/clm_eeg_p3_gamma_theta_pre_register.json
    (C1.loose [1500,4500], C1.strict [2500,3500], C2.cv ≤ 0.5, C3 occ>grand)
  - Selftest: PORT — synth fixture mirrors the JSON's frozen run block:
    grand_mean=2973, occipital=3722, cv=95 (pre-existing N=1 fixture).
  - Live: NOT_YET_LANDED — requires scipy.welch + .venv-eeg + real EEG.
  - Verdict at selftest: PASS  (all 4 criteria pass, 0 falsifiers)

### 3. berger_validate.hexa  — DECISION: PORT

  - Legacy backend: anima-clm-eeg/tool/clm_eeg_berger_sanity.hexa (646 LoC)
  - Frozen criteria: O1+O2 alpha-dominance triad (alpha>beta, alpha>delta,
    peak ∈ 8-13Hz), 6 sub-criteria total.
  - Selftest: PORT — synth fixture mirrors state/clm_eeg_berger_audit/
    2026-04-28_berger.jsonl synthetic_alpha line (alpha~28.5e6 µV², peak 10Hz).
  - Live: NOT_YET_LANDED — requires .venv-eeg + scipy.welch + real eyes-closed
    resting recording.
  - Verdict at selftest: PASS  (all 6 sub-criteria pass)

### 4. artifact_pipeline.hexa  — DECISION: PORT

  - Legacy backend: anima-eeg-core/tool/modules/_artifact/artifact_meta_classifier.hexa
    (under another agent's namespace — already LANDED, race-safe wrap-design only)
  - 8-detector chain: blink, motion, emg, ecg, emi, aging, refdrift, meta
  - Selftest: PORT — synthesizes 8 verdicts (CLEAN nominal); injection forces
    DOMINANT counts to test F_AP_02 quorum-policy.
  - Live: NOT_YET_LANDED — wraps the existing _artifact/ chain; selftest does
    NOT call into _artifact/ (race avoidance). Live mode delegates to
    `eeg_core artifact detect-all` route.
  - Verdict at selftest: PASS  (all 8 detectors CLEAN, 0 falsifiers)

### 5. rsn_validate.hexa  — DECISION: PORT

  - Legacy backend: anima-eeg/tool/resting_state_network_analyzer.hexa (288 LoC)
  - 4 criteria: DMN coh ≥ 0.5, |asym| ≤ 0.5, occ alpha ≥ 0.5, AO coh ≤ 0.3.
  - Selftest: PORT — synth fixture engineered from state/rsn_audit/
    2026-04-28_rsn.jsonl synthetic_correlated_dmn line (DMN=740, AO=170,
    occ=799). raw#10 honest C3: legacy frontal_alpha_asymmetry=1602 fails our
    stricter |asym|≤0.5 C2; selftest sets asym=100 to PASS — design choice
    is explicitly stricter than legacy's sign-only check (documented in module
    header).
  - Live: NOT_YET_LANDED — requires .venv-eeg + numpy/scipy + real recording.
  - Verdict at selftest: PASS  (all 4 criteria pass)

### 6. cyborg_token_emit.hexa  — DECISION: PORT

  - Legacy backend: anima-clm-eeg/tool/eeg_to_token_cyborg.hexa (730 LoC)
  - 5 criteria: round_trip_loss ≤ 250‰, alphabet=16, length=4*N_seg, N_seg≥50,
    only hex chars.
  - Selftest: PORT — LCG-seeded hex token stream, mirrors fixture line
    "synthetic_fnv_structured" (round_trip_loss_permille=38).
  - Live: NOT_YET_LANDED — requires real EEG segmenter + .venv-eeg numpy.
  - Verdict at selftest: PASS

### 7. multi_subject_aggregate.hexa  — DECISION: PORT (greenfield)

  - Legacy backend: NONE — raw#10 honest C3: no existing N≥3 cohort
    aggregator under anima-eeg/ or anima-clm-eeg/. eeg_to_token_cyborg has a
    multi-subject ledger notion but does NOT aggregate; this is a greenfield
    PORT.
  - 4 cohort criteria: N≥3, mean lz76 ≥ 0.65, cv ≤ 0.20, per-subject min ≥ 0.5
  - Selftest: PORT — 3 subjects synthesized via subject_seed = base_seed +
    k*101 (deterministic). Each subject gets 16-channel LZ76 proxy.
  - Live: NOT_YET_LANDED — CP2 G5 LIVE_HW_WITNESS_RATE deferred until N≥3
    real .npy files available (D+1 hardware arrival).
  - Verdict at selftest: PASS  (3 subjects, all 4 criteria pass)

## Falsifier Preregistration Summary (raw#71)

35 falsifiers preregistered across 7 modules (5 each):

```
F_P1_01..05   clm_eeg_p1               LZ_FLOOR / BASELINE_DRIFT / DIVERSITY / PARADIGM / CRITERIA
F_P3_01..05   clm_eeg_p3               OOB / HET / REGIONAL_REVERSED / THETA_DRIFT / GAMMA_LEAK
F_BG_01..05   berger_validate          ALPHA_O1 / ALPHA_O2 / DELTA_FLOOR / PEAK_O1 / PEAK_O2
F_AP_01..05   artifact_pipeline        CHAIN_INCOMPLETE / BAD_REC / META_FAILED / DEFICIT / SCHEMA_DRIFT
F_RSN_01..05  rsn_validate             DMN / ASYM / OCC / AO / SENTINEL
F_CT_01..05   cyborg_token_emit        LOSSY / ALPHABET / TRUNCATED / SEGMENT / INVALID_CHAR
F_MS_01..05   multi_subject_aggregate  COHORT_DEFICIT / FLOOR / HETEROG / OUTLIER / INGEST
```

Each module includes injection flags (`--inject_*` knobs in args_kv) so unit
tests can deterministically trigger each falsifier for coverage validation
in subsequent cycles.

## raw#10 Honest C3 — Unmet Legacy Dependencies

Per module, live mode is honestly NOT_YET_LANDED (raw#10 honest C3, no
pretense of working):

  1. clm_eeg_p1 — needs real resting EEG + clm hidden-state cross-stream
  2. clm_eeg_p3 — needs scipy.welch + .venv-eeg + real EEG
  3. berger_validate — needs scipy.welch + .venv-eeg + eyes-closed real EEG
  4. artifact_pipeline — needs real .npy ingest (delegates to _artifact/)
  5. rsn_validate — needs .venv-eeg numpy/scipy coherence
  6. cyborg_token_emit — needs real EEG segmenter + .venv-eeg numpy
  7. multi_subject_aggregate — needs N≥3 real subjects (D+1 hardware)

All 7 emit `verdict=PENDING_MIGRATION` rc=4 in --live mode with stderr trailer
indicating reason + fix.

## Selftest Evidence

```
$ /Users/ghost/core/hexa-lang/hexa.real run \
    anima-eeg-core/tool/modules/_integrations/_integration_test.hexa
...
Phase 6 _integrations integration summary
  total:   7
  pass:    7
  fail:    0
  details: clm_eeg_p1=PASS:PASS,clm_eeg_p3=PASS:PASS,berger_validate=PASS:PASS,
           artifact_pipeline=PASS:PASS,rsn_validate=PASS:PASS,
           cyborg_token_emit=PASS:PASS,multi_subject_aggregate=PASS:PASS
  audit:   state/anima_eeg_core_phase6_integrations_audit.jsonl
verdict: PHASE6_INTEGRATIONS_INTEGRATION_PASS ✓
```

7/7 modules selftest PASS via direct invocation AND via the integration test
runner. All 7 dispatcher routes verified via `eeg_core integration <noun>
--selftest` returning rc=0 BACKEND_PASS. Dispatcher selftest still passes
4/4 (no regression).

Audit jsonl appended at `state/anima_eeg_core_phase6_integrations_audit.jsonl`
(7 rows, raw#77 schema).

## Dispatcher Routes (7 + aliases)

```
integration clm-eeg-p1         → _integrations/clm_eeg_p1.hexa
integration clm-eeg-p3         → _integrations/clm_eeg_p3.hexa
integration berger             → _integrations/berger_validate.hexa
integration artifact-pipeline  → _integrations/artifact_pipeline.hexa
integration rsn                → _integrations/rsn_validate.hexa
integration cyborg-token       → _integrations/cyborg_token_emit.hexa
integration multi-subject      → _integrations/multi_subject_aggregate.hexa
```

Aliases: `p1`/`p3`/`clm_eeg_p1`/`clm_eeg_p3`/`berger-validate`/`rsn-validate`/
`cyborg_token_emit`/`multi_subject_aggregate`/`cohort`/`artifact_pipeline`.

## Next-Cycle Backlog

  - Live-mode landing for 7 modules pending hardware + .venv-eeg backend.
  - Add cross-module injection harness: a single CLI that triggers each
    falsifier in sequence and asserts trigger_count==1 (currently each
    module has the knobs but no orchestrator).
  - Surface `integration all --selftest` route (matches `metric all` design
    pattern but requires composite stdout aggregation).
