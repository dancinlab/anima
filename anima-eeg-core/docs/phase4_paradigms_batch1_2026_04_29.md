# anima-eeg-core Phase 4 _paradigms/ Batch 1 — Land Note

**Date:** 2026-04-29  
**Author:** anima-eeg-core Phase 4 paradigms agent  
**Predecessor:** Phase 3 _metrics/ batch 1 (commit `44f9dc6df`)  
**Successor:** Phase 4 batch 2 (longitudinal / long_duration / sleep / pre_post)

raws: #9 hexa-only · #10 honest C3 · #12 frozen · #18 self-host · #42 mac-zero-compute · #65 idempotent · #71 falsifier ≥3 · #82 darwin · #91 honest triad · #95 triad-universal-mandate

---

## 1. Summary

Phase 4 _paradigms/ first-batch landing of **4 modules**:

| # | Module | Paradigm | Default protocol | Falsifiers |
|---|--------|----------|------------------|------------|
| 1 | `resting_baseline.hexa` | resting | 60 s eyes-open + 60 s eyes-closed @ 125 Hz × 16ch | 3 |
| 2 | `daily_life.hexa` | daily_life | 5 min × N segments, eyes-open active task | 3 |
| 3 | `visual_p300.hexa` | visual_p300 | 240 trials, 80/20, ISI 1500-2000 ms, parietal max | 5 |
| 4 | `auditory_p300.hexa` | auditory_p300 | 400 trials, 1000/1500 Hz, ISI 1500 ± 100 ms | 5 |

All four pass selftest; integration test PASS 4/4 (state/anima_eeg_core_phase4_paradigms_integration_audit.jsonl).

---

## 2. WRAP vs PORT decision (raw#10 honest C3)

| Module | Decision | Reason |
|--------|----------|--------|
| `resting_baseline` | WRAP-design + PORT-selftest | Legacy `anima-eeg/eeg_recorder.hexa` (584 LoC) has buggy argv normalizer (rejects `hexa.real run X.hexa <flags>`); raw#12 frozen forbids fixing. Selftest synthesises protocol log; live mode emits NOT_YET_LANDED with shell-direct fix pointer. |
| `daily_life` | WRAP-design + PORT-selftest | Two legacy backends (`daily_life_context_logger.hexa`, `eeg_daily_life_verifier.hexa`) work but require BrainFlow ingest. Selftest synthesises protocol-log kv-block; live → NOT_YET_LANDED. |
| `visual_p300` | PORT-selftest + WRAP-design-reference | Legacy `anima-eeg/protocols/p300_visual_oddball.hexa` (509 LoC) has hexa-strict auto-invoke conflict (top-level `main()` call + `fn main`) that prevents direct exec. Module ports trial-sequence builder + frozen ERP fixture. |
| `auditory_p300` | PORT-selftest + WRAP-design-reference | Legacy `anima-eeg/protocol/p300_auditory_oddball.hexa` (356 LoC) hits same argv-normalizer bug as eeg_recorder. Module ports schedule builder + 5-falsifier evaluation (LCG seed=20260428 reproduces nominal session). |

raw#18 self-host: legacy specs were the hypothesis source; Phase 5 will deprecate legacy in favour of these modules once live BrainFlow / Pyglet / afplay ingest lands.

---

## 3. kv-block contract (paradigm vs metric API axis)

Phase 3 _metrics/ used `_metric_<name>_kv(npy_path, sidecar_kv) -> string` (npy as primary input). Paradigm modules differ — recording protocols don't read .npy; they emit a protocol spec + falsifier verdict. Hence:

```
fn _paradigm_<name>_kv(args_kv: string) -> string
    // args_kv: comma-separated "key=value,key=value"
    // returned kv-block keys (canonical):
    //   schema=anima-eeg-core/_paradigms/<name>/1
    //   paradigm=<name>
    //   duration_s | n_trials | n_segments  (paradigm-specific scalar)
    //   sample_rate_hz=<int>
    //   channel_count=<int>
    //   protocol_steps=<csv-stim-spec>
    //   verdict=<PASS|FAIL|FALSIFIED>
    //   value_x1000=<int>            (uniform with _metrics for downstream readers)
    //   raw71_falsifier_count=<int>  (≥3, 5 for P300 family)
    //   raw71_triggered_count=<int>
    //   raw71_triggered_ids=<csv>    (e.g. F_VP300_01,F_VP300_03)
    //   raw91_evidence=<provenance-token>
    //   raw91_limit=<scope-token>
    //   raw95_enforce_layer=in_module
```

Difference vs _metrics/ contract is intentional and reconciled by the integration test which validates the **subset** of keys common across both axes (schema, verdict, value_x1000, raw71_falsifier_count, raw71_triggered_ids).

raw#65 idempotent: same `args_kv` (default seed) yields byte-identical kv-block.

---

## 4. raw#71 falsifiers (≥3 each, frozen 2026-04-28)

```
resting_baseline:
  F_RB_01: duration_s     != requested      → schedule mismatch
  F_RB_02: sample_rate_hz != 125            → wrong board
  F_RB_03: channel_count  != 16             → wrong montage

daily_life:
  F_DL_01: per-segment duration_s < 60      → window too short for LZ76
  F_DL_02: n_segments < 1                   → no recording requested
  F_DL_03: sample_rate_hz != 125            → wrong board

visual_p300:  (5 — preserves legacy F1-F5)
  F_VP300_01: n_oddball < 20                → trial count short
  F_VP300_02: peak outside 250-400 ms       → no peak in window
  F_VP300_03: oddball_peak < standard_peak  → reversed polarity
  F_VP300_04: chan not Pz/P3/P4             → regional reversal
  F_VP300_05: diff_peak_uv < 2.0            → subthreshold

auditory_p300:  (5 — preserves legacy F1-F5)
  F_AP300_01: |pct_actual - pct_target| > 2pp  → ratio off
  F_AP300_02: oddball in first 3 trials        → schedule violation
  F_AP300_03: isi_mean outside [1450,1550] ms  → jitter drift
  F_AP300_04: tone purity proxy (analytic)     → always PASS in synth
  F_AP300_05: consecutive oddball pairs > 0    → anti-clustering broken
```

---

## 5. Selftest results (2026-04-28T15:12:59Z)

```
Phase 4 _paradigms batch1 integration summary
  total:   4
  pass:    4
  fail:    0
  details: resting_baseline=PASS:PASS, daily_life=PASS:PASS,
           visual_p300=PASS:PASS, auditory_p300=PASS:PASS
verdict: PHASE4_PARADIGMS_BATCH1_INTEGRATION_PASS ✓
```

Audit ledger: `state/anima_eeg_core_phase4_paradigms_integration_audit.jsonl`  
Each module emits `verdict=PASS, value_x1000=<int>, backend_rc=0, raw71_triggered=""`.

End-to-end dispatcher route smoke test (representative):
- `hexa run anima-eeg-core/tool/eeg_core.hexa paradigm visual-p300 --selftest` → BACKEND_PASS rc=0
- `hexa run anima-eeg-core/tool/eeg_core.hexa list` → 4 new `paradigm <name>` rows show [landed]
- `hexa run anima-eeg-core/tool/eeg_core.hexa selftest` → DISPATCHER_SELFTEST_PASS

---

## 6. Dispatcher promotions

`anima-eeg-core/tool/eeg_core.hexa` updated:

| Verb noun | Pre | Post |
|-----------|-----|------|
| `record resting` | legacy:anima-eeg/eeg_recorder.hexa | landed:_paradigms/resting_baseline.hexa |
| `record daily-life` | legacy:daily_life_context_logger.hexa | landed:_paradigms/daily_life.hexa |
| `paradigm resting` | (absent) | landed:_paradigms/resting_baseline.hexa |
| `paradigm resting-baseline` | (absent) | landed |
| `paradigm daily-life` | (absent) | landed |
| `paradigm visual-p300` | (absent) | landed |
| `paradigm auditory-p300` | (absent) | landed |

`record sleep / long / longitudinal / pre-post` remain `legacy` — deferred to batch 2.

raw#1 chflags uchg re-applied to dispatcher post-edit.

---

## 7. Deferred — Phase 4 batch 2 (4 paradigms)

| Paradigm | Source | Notes |
|----------|--------|-------|
| `longitudinal` | anima-eeg/tool/longitudinal_session_recorder.hexa | scheduled multi-session recording |
| `long_duration` | anima-eeg/tool/long_duration_recorder.hexa | 60-120 min single session |
| `sleep_8hr` | anima-eeg/tool/sleep_tracker.hexa | overnight 28800 s |
| `pre_post_task` | anima-eeg/tool/pre_post_task_recorder.hexa | 2× 300 s pre/post task |

Pattern will mirror batch 1 (selftest synth + live → NOT_YET_LANDED, ≥3 falsifiers, kv-block contract).

---

## 8. Files

```
anima-eeg-core/tool/modules/_paradigms/
  resting_baseline.hexa            (~210 LoC)
  daily_life.hexa                  (~200 LoC)
  visual_p300.hexa                 (~280 LoC)
  auditory_p300.hexa               (~310 LoC)
  _integration_test.hexa           (~165 LoC)

anima-eeg-core/tool/eeg_core.hexa  (dispatcher routes + list table + help)
anima-eeg-core/docs/phase4_paradigms_batch1_2026_04_29.md  (this doc)
state/anima_eeg_core_phase4_paradigms_integration_audit.jsonl  (raw#77 audit)
```
