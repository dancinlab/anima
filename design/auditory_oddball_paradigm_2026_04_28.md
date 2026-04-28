# Auditory Oddball P300 Paradigm — anima T4

**Date**: 2026-04-28
**Track**: anima β Learning-Free (main-track), EEG measurement axis T4 (auditory P300)
**Companion**: T3 visual oddball (separate axis; not yet landed)
**Status**: Design + selftest landed; real-hardware tier deferred until Cyton+Daisy session

## 1. Purpose

Detect the P300 ERP component (positive deflection ~300ms post-stimulus over
centro-parietal scalp) elicited by an auditory oddball paradigm. Provides
a **second consciousness axis** orthogonal to T3 (visual oddball): subjects
may keep eyes closed, eliminating motion artifacts and visual-cortex
contamination, and recruiting auditory cortex (T7/T8 lateral temporal lobes).

raw#10 honest: P300 is a well-established ERP, but our detection pipeline
in this iteration emits **markers only** (audit jsonl) — actual ERP
extraction (epoch averaging, baseline correction, peak detection) is the
downstream `analyze.hexa` consumer's job. This file is an **experiment
runner**, not an analyzer.

## 2. Protocol

| Param            | Value                                           |
|------------------|-------------------------------------------------|
| Standard tone    | 1000 Hz sinusoid, 50 ms duration, 80% of trials |
| Oddball tone     | 1500 Hz sinusoid, 50 ms duration, 20% of trials |
| ISI              | 1.5 s (jitter ±100 ms uniform; raw#10 honest)   |
| Trials           | ~300-600 (default n=400 over ~10 min)           |
| Subject task     | Silent count of oddballs (no motor response)    |
| Eyes             | Closed permitted (relaxed baseline, no visual)  |
| Output           | jsonl audit ledger (per-trial markers)          |

## 3. Differences from T3 (visual oddball)

| Axis              | T3 visual                          | T4 auditory (this file)               |
|-------------------|------------------------------------|---------------------------------------|
| Stimulus modality | Screen flash / shape               | Speaker tone (1000 Hz / 1500 Hz)      |
| Eyes              | MUST be open (fixate)              | Closed permitted (recommended)        |
| Motion artifact   | Eye-saccade / blink contamination  | Minimal — relaxed seated subject      |
| Cortex            | Visual O1/O2 + central P300        | Auditory T7/T8 (N1) + central P300    |
| C3 frozen pick    | O1+O2 dominant + Pz P300           | T7+T8 max (N1) + Cz/Pz P300           |
| Baseline tier     | DEGRADED (motion sensitive)        | APPROXIMATE_HW (lower noise floor)    |

## 4. Implementation

- **Runner**: `anima-eeg/protocol/p300_auditory_oddball.hexa` (~180 LoC)
- **Audio**: `afplay` darwin-native (synthesized WAV files in `/tmp`)
  - Helper Python writes 1000 Hz / 1500 Hz 50ms WAVs once via stdlib `wave` module
  - `afplay` invocation per trial; ~5-10ms latency (not strict timing — DEGRADED)
- **Timing**: `time.monotonic()` for ISI, target ±5ms jitter (afplay launch latency)
  - raw#10 honest: this is **not** sub-ms PsychoPy precision; tier is
    APPROXIMATE_HW. For P300 analysis the ~5ms onset uncertainty is below
    the EEG sample period (250 Hz → 4 ms) so net effect is negligible.
- **Audit**: `state/audit/p300_auditory_oddball_<ts>.jsonl`
  - One line per trial: `{ts, trial_idx, tone_hz, is_oddball, t_offset_s,
    isi_actual_ms}`
  - Session header: `{schema, mode, n_trials, oddball_pct, duration_planned_s}`
- **BrainFlow streaming**: NOT directly invoked here; this file is paradigm-only.
  Pair with `collect.hexa` for parallel BrainFlow capture (same pattern as
  experiment.hexa `--run-with-eeg`).

## 5. Five Falsifiers (raw#71 preregistered)

- **F1** Standard:Oddball ratio = 80:20 ± 2pp over n=400 trials (selftest count)
- **F2** Oddball never appears in first 3 trials (raw#10 — to avoid first-trial
  novelty confound)
- **F3** ISI distribution mean ∈ [1.45, 1.55]s and SD ∈ [0.05, 0.07]s
  (uniform ±100ms jitter target)
- **F4** Audio file 1000 Hz fundamental peak FFT amplitude > 1500 Hz peak by
  ≥ 20 dB (purity check on synthesized WAV)
- **F5** No two consecutive oddballs (raw#10 — anti-clustering for cleaner ERP
  averaging; oddball-to-oddball gap ≥ 1 standard tone)

## 6. C3 frozen criteria modification (auditory variant)

- **Region pick**: T7 + T8 (left + right lateral temporal — auditory cortex)
  for N1 (~100ms) + central Cz/Pz for P300 (~300ms)
- **Frozen** at design-time, not data-driven (raw#71)
- **Criterion**: P300 peak ∈ [250, 400] ms post-oddball, amplitude > 2× standard
  P300 amplitude (effect size > 0; not p-value)
- **Failure mode**: if T7+T8 lead-off impedance > 750 kΩ at session start
  (impedance_check.hexa GREEN gate), abort — auditory cortex coverage required.

## 7. raw rules referenced

- raw#9 hexa-only · raw#10 honest scope · raw#12 silent-error-ban
- raw#37 transient-helper-in-/tmp · raw#65 idempotent (selftest synthetic)
- raw#71 preregistered-falsifiers · raw#82 darwin-native (afplay)
- raw#91 honesty-triad · own #5 user audit (commit deferral if selftest fails)

## 8. User action plan (post-landing)

1. **Impedance pre-check** (≥ 5 GREEN at T7/T8/Cz/Pz/Fz):
   `hexa run anima-eeg/impedance_check.hexa --check`
2. **Run paradigm** (10 min, eyes closed, silent count oddballs):
   `hexa run anima-eeg/protocol/p300_auditory_oddball.hexa --run --n-trials 400`
3. **Pair with BrainFlow capture** (separate terminal):
   `hexa run anima-eeg/collect.hexa --output recordings/sessions/p300_aud_<ts>.npy --duration 700`
4. **Downstream analysis**: `analyze.hexa` ERP module (Phase 5 deferred).
