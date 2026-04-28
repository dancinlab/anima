# LZ76 EEG verifier — raw vs scipy-filtered comparison (2026-04-28)

raw#10 honest C3 disclosure: filter modifies the *input data*; the LZ76
algorithm and the C1/C2 thresholds remain frozen (raw#12 pre-registered).
Only the binarization input changed. All measurements below are first-shot,
no post-hoc tuning.

## Inputs

| Item                  | Value                                                                    |
| --------------------- | ------------------------------------------------------------------------ |
| Raw .npy              | recordings/sessions/baseline_resting_60s_20260428.npy                    |
| Raw sha256            | b64010436db580361bf3641dd87ae2d106ac45304bcd9dd35892e51edf866a09         |
| Filtered .npy         | recordings/sessions/baseline_resting_60s_20260428_filtered.npy           |
| Filtered sha256       | a1889072b2a11560be12851e24713da407559b6f76184bfea0ec33c3419143d2         |
| Filtered sidecar      | recordings/sessions/baseline_resting_60s_20260428_filtered.json          |
| Shape                 | (16, 7491) float64 (16 ch × 60 s @ 125 Hz)                               |

## Filter spec (canonical EEG preprocessing)

1. Notch 60 Hz (mains EMI):  `scipy.signal.iirnotch(60.0, Q=30, fs=125)`
2. Bandpass 0.5–50 Hz (Butterworth order=4): `scipy.signal.butter(4, [0.5, 50.0], btype='band', fs=125)`
3. Application: per channel, sequential — notch -> bandpass — both via `scipy.signal.filtfilt` (zero-phase).

Implementation: `/tmp/eeg_filter_helper.py` (raw#37 transient).

## Pre vs post-filter signal stats

| Metric                                    | Raw (pre)              | Filtered (post)        | Ratio       |
| ----------------------------------------- | ---------------------- | ---------------------- | ----------- |
| RMS per ch — min (µV)                     | 469.787                | 14.650                 | 0.0312      |
| RMS per ch — mean (µV)                    | 39647.094              | 1054.389               | 0.0266      |
| RMS per ch — max (µV)                     | 84653.258              | 2246.931               | 0.0265      |
| 60 Hz mains power (Σ all ch, 59–61 Hz)    | 1.578e+08              | 2.267e+07              | 0.144       |
| Alpha 8–13 Hz power (Σ all ch)            | 3.784e+08              | 1.381e+09              | 3.65        |

Observations:
- DC drift + mains EMI removed (RMS drops ~37×), but post-filter RMS (14–2246 µV) is still **above** the typical normal-EEG resting band (5–50 µV). The amplifier appears to be running at ~20×–45× the nominal scale. This is hardware/signal-chain magnitude, not a filter issue — the filter cannot rescale, only band-limit.
- 60 Hz mains drops to 14.4 % of original (notch effective).
- Alpha-band power *increases* 3.6× relative to total — a real EEG-like spectral shape now dominates.

## LZ76 result comparison (frozen criteria — raw#12)

| Quantity                       | Raw (input direct)   | Filtered (input filtered) | Δ                |
| ------------------------------ | -------------------- | ------------------------- | ---------------- |
| n_channels                     | 16                   | 16                        | —                |
| n_samples / ch                 | 7491                 | 7491                      | —                |
| binarized_length               | 119856               | 119856                    | —                |
| c(n) productions               | 409                  | 3415                      | +3006 (8.35×)    |
| log2(n)_x1000                  | 16828                | 16828                     | —                |
| **b(n)_x1000** (= LZ76_norm)   | 57                   | **479**                   | +422 (8.40×)     |
| b(n) (normalized 0..1)         | 0.057                | **0.479**                 | +0.422           |
| abs_delta_x1000 (vs human 850) | 793                  | 371                       | -422             |
| pct_delta_permille             | 932 ‰                | 436 ‰                     | -496 ‰           |
| C1 (b ≥ 0.65)                  | FAIL                 | **FAIL**                  | (still below)    |
| C2 (\|Δ\|/h ≤ 20 %)            | FAIL                 | **FAIL**                  | (43.6 % > 20 %)  |
| P1 verdict                     | P1_FAIL              | **P1_FAIL**               | (still FAIL)     |
| classification                 | REAL_HW_FAIL         | REAL_HW_FAIL              | unchanged        |

## Interpretation (raw#10 honest)

- The filter pushed `b(n)` from 0.057 → 0.479 — an **8.4×** increase in normalized LZ76 complexity. Direction is correct: removing 60 Hz mains + DC drift reduces the dominant low-entropy structure that previously made the binarized sequence highly predictable.
- However, 0.479 is still **below** the C1 floor (0.65) and **outside** the Schartner 2017 normal-resting-EEG range (0.85 ± 0.05 → 0.80–0.90).
- Honest assessment: filter is necessary but not sufficient. The remaining gap suggests one or more of:
  1. **Residual non-EEG artifacts** outside 0.5–50 Hz scope (e.g. movement, electrode-pop, heartbeat) — not addressed by simple bandpass.
  2. **Amplifier saturation / clipping** in the raw record — once a channel saturates, even after filtering the binarization will inherit the residual structure.
  3. **Electrode contact issues** — high-impedance channels add structured noise that survives bandpass.
  4. **Possible non-resting state** (the input is labelled "resting 60 s" but the µV magnitudes suggest movement/artifact contamination).
- Post-filter RMS 14–2246 µV is still 0.3×–45× the normal physiological range; this is consistent with hypothesis (2) or (3).

## Verdict

raw#12 frozen criteria preserved. Filter applied as data-preprocessing, not algorithm tuning. Verdict P1_FAIL retained but with substantially closer approach (Δ b = +0.422). Next steps for the operator (not executed here):
- Verify electrode impedance per channel.
- Apply ICA artifact rejection (eye-blink, muscle, ECG).
- Rule out amplifier scale mismatch (the µV magnitudes are unusually high after filtering).

## Audit trail (state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl)

Last two rows:

```json
{"ts":"2026-04-28T11:24:15Z","tool":"clm_eeg_lz76_real","mode":"real","input":"recordings/sessions/baseline_resting_60s_20260428.npy","sha256":"b64010436db580361bf3641dd87ae2d106ac45304bcd9dd35892e51edf866a09","n_channels":16,"n_samples":7491,"binarized_length":119856,"c_n":409,"b_n_x1000":57,"verdict":"P1_FAIL","classification":"REAL_HW_FAIL"}
{"ts":"2026-04-28T11:30:08Z","tool":"clm_eeg_lz76_real","mode":"real","input":"recordings/sessions/baseline_resting_60s_20260428_filtered.npy","sha256":"a1889072b2a11560be12851e24713da407559b6f76184bfea0ec33c3419143d2","n_channels":16,"n_samples":7491,"binarized_length":119856,"c_n":3415,"b_n_x1000":479,"verdict":"P1_FAIL","classification":"REAL_HW_FAIL"}
```

## References

- Schartner et al. 2017 — LZ76 EEG complexity normal range (resting human cohort, 0.85 ± 0.05).
- Kaspar & Schuster 1987 (Phys Rev A 36:842) — LZ76 production-count algorithm + normalization c(n)·log2(n)/n.
- scipy.signal.iirnotch / scipy.signal.butter / scipy.signal.filtfilt — canonical zero-phase Butterworth + IIR notch.
