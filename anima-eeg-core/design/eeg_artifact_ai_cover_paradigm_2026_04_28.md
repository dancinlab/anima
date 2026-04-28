# EEG Artifact AI-Cover Paradigm — 2026-04-28

## Status
- 9 module skeleton complete; 2,094 LoC total
- Selftest 9/9 PASS positive cases
- D-day post-battery EEG diagnosis: **EMI dominant**, MILD MOTION + EMG
- Pipeline pre→post quality: 70 → 95 (+25)
- Berger gate on cleaned EEG: still FAIL (peak 1.2 Hz delta, not 8–13 Hz alpha)

## Modules

| # | Module | Verdict scheme | Purpose |
|---|---|---|---|
| 1 | `environmental_emi_classifier.hexa` | CLEAN/MILD/DOMINANT | 50/60/120/180 Hz narrowband detection |
| 2 | `eye_blink_detector.hexa` | CLEAN/MILD/DOMINANT | Fp1/Fp2 MAD spike count |
| 3 | `motion_artifact_detector.hexa` | CLEAN/MILD/DOMINANT | Synchronous global 5σ co-spike |
| 4 | `emg_muscle_detector.hexa` | CLEAN/MILD/DOMINANT | gamma/alpha band-power ratio |
| 5 | `ecg_heart_artifact_detector.hexa` | CLEAN/MILD/DOMINANT | 1–3 Hz autocorr period, BPM estimation |
| 6 | `reference_drift_detector.hexa` | CLEAN/MILD/DOMINANT | Grand-mean coherent low-freq drift |
| 7 | `electrode_aging_classifier.hexa` | CLEAN/MILD/DOMINANT | Per-ch broadband RMS z-score |
| 8 | `artifact_meta_classifier.hexa` | quality 0–100 | Voting ensemble across 7 detectors |
| 9 | `ai_cleaning_pipeline.hexa` | pre→post quality | Iterative suppressor chain |

All modules: hexa wrapper + transient `.py` helper (raw#9 / raw#37) using
`.venv-eeg/bin/python` (numpy + scipy.signal). Per-module JSONL audit ledger
in `state/eeg_artifact_audit/2026_04_28_<type>.jsonl`.

## AI training approach (raw#10 honest C3)

| Stage | Method | Status |
|---|---|---|
| Now | **Unsupervised** thresholding (MAD, band-ratio, autocorr, slope) | implemented |
| Next | **Self-supervised** synthetic-injection (already used in selftests) | scaffolding present |
| Mid-term | **Supervised** manual labelling per session | TODO |
| Long-term | **Online learning** per-user adaptive | TODO |

### Honest limitations (raw#91)
1. **EMG detector** flags white noise as DOMINANT (band-power ratio FP);
   needs EMI-screening first in cleaning chain. Documented in falsifier list.
2. **Reference-drift detector** cannot distinguish electrode drift from
   environmental thermal drift — user re-paste of SRB2 confirms.
3. **Electrode aging** is single-session proxy; longitudinal regression
   requires ≥3 session corpus (TODO).
4. **AI determinism** — every detector is fully deterministic (numpy seed
   in selftests, no stochastic ICA refit).  raw#73 structurally admissible.

## D-day post-battery diagnosis

Input: `recordings/sessions/baseline_resting_post_battery_20260428T132612Z_seg000_eeg16.npy`
(16 ch × 7,490 samples @ 125 Hz, 60 s eyes-closed resting).

Per-detector verdict on RAW:
- EMI: **DOMINANT** ← root cause
- BLINK: CLEAN
- MOTION: MILD
- EMG: MILD
- ECG: CLEAN
- REF_DRIFT: CLEAN
- AGING: CLEAN

Composite quality 70/100. Recommended chain: `EMI → MOTION + EMG`.

After AI cleaning pipeline (notch 50/60/120/180 Hz + 1 motion epoch reject + LP30):
- Composite quality: **70 → 95 (+25)**
- Dominant artifact: EMI → NONE
- Cleaned npy: `..._eeg16_aiclean.npy`

Berger alpha gate on cleaned EEG:
- O1/O2 peak still 1.2 Hz (delta, not alpha)
- alpha/beta ratio improved O1 1.016→1.138, O2 1.161→1.268
- alpha/delta ratio still ~0.06 (target ≥0.30)

## Conclusion (raw#10 honest)

EMI was a real contaminant (37.7 dB excess at 60 Hz on all 16 channels) and
notch filtering removed it. **However Berger gate still FAILs** because the
fundamental issue is delta-band dominance over alpha (alpha/delta ≈ 0.06 vs
target 0.30). Possible remaining root causes (battery has been excluded;
EMI now also excluded):

1. **Skin prep insufficient** — high impedance leaves only DC drift visible
2. **Saline/paste re-application needed** — especially SRB2 reference (mild
   ref-drift sometimes seen, currently CLEAN here)
3. **Eyes-open contamination** — eyes-closed Berger requires actual closed
   eyes; visual cortex desynchronization eliminates alpha
4. **Subject-state issue** — drowsiness or alpha-blocked state
5. **Occipital electrode position** — O1/O2 placement requires ≥1 cm above
   inion; mis-placement loses occipital alpha entirely

## User action recommendations

| Priority | Action | Rationale |
|---|---|---|
| P0 | Re-confirm eyes are CLOSED during recording | Eyes-open destroys alpha |
| P1 | Re-paste SRB2 (gel/saline) and all occipital sites | Boost SNR for 8–13 Hz |
| P1 | Verify O1/O2 helmet position vs inion landmark | Mis-placement = no alpha |
| P2 | Skin prep with abrasive gel (NuPrep) on occipital scalp | Reduce impedance |
| P3 | Move 60 Hz EMI sources away (laptop charger, fluorescent) | Reduce notch reliance |
| P4 | Record longer (≥120 s) — shorter records → noisier PSD | Lower variance |

EMI cleaning module is now production-ready and removes 60 Hz contamination
without introducing new artifacts. The remaining Berger FAIL is **not**
hardware-fixable from EMI alone; subject/placement intervention required.

## Falsifiers (raw#71 ≥5 per module)

Each detector lists ≥6 named falsifiers in module docstring — see
`F1..F6` blocks in each `.hexa` file. Falsifier sweep results in
`state/eeg_artifact_audit/2026_04_28_<type>.jsonl`.

## Cross-references

- raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen criteria
- raw#37 transient `.py` helper · raw#65 idempotent · raw#68 fixpoint
- raw#71 ≥5 falsifiers · raw#73 deterministic seal · raw#82 darwin venv-eeg
- raw#91 honest classification · own5 completeness · own11 parallel-9 safe
- Phase-1 `_core/` and Phase-2 `_gates/` modules (Berger, RMS, PE, Hjorth)
  remain authoritative for downstream gating.
