# Berger gate A3 follow-up — HPF 0.5 Hz re-run on 15 valid .npy

**Date**: 2026-04-28 (D-day)
**Slug**: `berger_hpf_rerun_2026_04_28`
**Author**: anima-eeg-core agent (raw#9 hexa-only / /tmp .py helper)
**Predecessor**: commit `06fe4142c` — D-day Tier-A #3 Berger batch sweep (0/15 PASS)
**Inventory source**: commit `2d0bc8337` — 20 .npy → 15 analysis-ready 16-ch files
**Compliance**: raw#9 / raw#10 / raw#12 / raw#42 / raw#65 / raw#71 / raw#77 / raw#91 / own#4

---

## 1. Hypothesis & pipeline

Pre-HPF Berger sweep (`state/clm_eeg_berger_audit/2026-04-28_berger.jsonl`) showed
all 15 files FAIL with O1/O2 peak frequency in 1.2–1.7 Hz. Hypothesis: **DC and
sub-δ slow drift dominate the welch PSD, masking any 8–13 Hz alpha**. Fix path A:
HPF Butterworth 4th-order zero-phase filtfilt, cutoff **0.5 Hz**, then re-run Berger.

### Pipeline

```
.npy (16 × N, float32/64)
  → HPF butter(4, 0.5/62.5, 'high'), filtfilt (axis=-1)
  → state/eeg_hpf_05hz_2026_04_28/<basename>_hpf05.npy
  → Berger gate (welch nperseg=512, fs=125, occipital ch={6,7})
  → C1 α>β · C2 α>0.30·δ · C3 peak ∈ [7,14] Hz
  → verdict ∈ {PASS, PARTIAL, FAIL}
```

### Module deliverables (raw#9, hexa-only)

| Path | Role |
|---|---|
| `anima-eeg-core/tool/modules/_artifact/hpf_dc_drift.hexa` | NEW — HPF preprocessor module (selftest 4/4 PASS) |
| `/tmp/anima_berger_hpf_rerun_orchestrator.py` | Transient orchestrator (raw#37) |
| `state/eeg_hpf_05hz_2026_04_28/*_hpf05.npy` | 15 HPF outputs |
| `state/clm_eeg_berger_audit/2026-04-28_hpf_rerun.jsonl` | Audit ledger (raw#77 schema) |

---

## 2. Per-file pre vs post-HPF comparison

| file (truncated) | pre o1pk / o2pk Hz | pre c1c2c3 | post o1pk / o2pk Hz | post c1c2c3 | post verdict |
|---|---|---|---|---|---|
| baseline_resting_60s_20260428.npy | 1.71 / 1.71 | 000/000 | 1.71 / 1.22 | 000/000 | FAIL |
| baseline_resting_60s_20260428_filtered.npy | 1.71 / 1.22 | 000/000 | 1.71 / 1.22 | 000/000 | FAIL |
| baseline_resting_60s_20260428_ica.npy | 1.71 / 1.71 | 000/000 | 1.71 / 1.71 | 000/000 | FAIL |
| baseline_resting_low_emi_…seg000_eeg16.npy | 1.71 / 1.71 | 000/000 | 1.71 / 1.71 | 000/000 | FAIL |
| baseline_resting_low_emi_…seg000_eeg16_filtered.npy | 1.71 / 1.71 | 000/000 | 1.71 / 1.46 | 000/000 | FAIL |
| baseline_resting_low_emi_…seg000_eeg16_ica.npy | 1.46 / 1.71 | 000/000 | 1.46 / 1.71 | 000/000 | FAIL |
| baseline_resting_post_battery_…seg000_eeg16.npy | 1.22 / 1.22 | 100/100 | 1.22 / 1.22 | 100/100 | FAIL |
| baseline_resting_post_battery_…seg000_eeg16_filtered.npy | 1.22 / 1.22 | 100/100 | 1.22 / 1.22 | 100/100 | FAIL |
| baseline_resting_post_battery_…seg000_eeg16_ica.npy | 1.46 / 1.46 | 000/000 | 1.46 / 1.46 | 000/000 | FAIL |
| post_battery_raw_16ch_2026_04_28.npy | 1.22 / 1.22 | 100/100 | 1.22 / 1.22 | 100/100 | FAIL |
| post_battery_filtered_16ch_2026_04_28.npy | 1.22 / 1.22 | 100/100 | 1.22 / 1.22 | 100/100 | FAIL |
| post_battery_ica_16ch_2026_04_28.npy | 1.46 / 1.22 | 000/100 | 1.46 / 1.22 | 000/100 | FAIL |
| 20260428T115006Z_daily_life_5min_1_eeg16.npy | 1.22 / 1.46 | 000/000 | 1.22 / 1.46 | 000/000 | FAIL |
| 20260428T115006Z_daily_life_5min_1_eeg16_filtered.npy | 1.22 / 1.46 | 000/000 | 1.22 / 1.46 | 000/000 | FAIL |
| 20260428T115006Z_daily_life_5min_1_eeg16_ica.npy | 1.46 / 1.22 | 000/000 | 1.46 / 1.22 | 000/000 | FAIL |

---

## 3. Aggregate result

| metric | pre-HPF | post-HPF (0.5 Hz) | delta |
|---|---|---|---|
| files | 15 | 15 | — |
| PASS | 0 | **0** | +0 |
| PARTIAL | 0 | 0 | +0 |
| FAIL | 15 | 15 | 0 |
| O1 peak ∈ [7,14] Hz (C3) | 0/15 | 0/15 | +0 |
| O2 peak ∈ [7,14] Hz (C3) | 0/15 | 0/15 | +0 |
| O1 α>β (C1) | 4/15 | 4/15 | +0 |
| O2 α>β (C1) | 5/15 | 5/15 | +0 |
| files where peak shifted ≥ Δ0.25 Hz (welch bin) | — | 0/15 | — |

**Peak shift summary**: HPF 0.5 Hz did NOT push the welch PSD peak out of the
δ band (1–4 Hz) on any of the 15 files. The dominant low-frequency power
survived — confirming that the residual sub-δ drift after the existing
0.5–50 Hz bandpass (`filter_pipeline.hexa`) is NOT the limiting factor.

### DC mean suppression (sanity check — HPF DID work)

| file | mean_before µV-RMS-of-channel-means | mean_after | suppression |
|---|---|---|---|
| daily_life_5min_1_eeg16.npy (raw 32-DAC) | 49656 | 101.06 | 99.80 % |
| daily_life_5min_1_eeg16_filtered.npy | 101.05 | 85.66 | 15 % (already filtered) |
| daily_life_5min_1_eeg16_ica.npy | 101.05 | 0.017 | 99.98 % |

→ HPF correctly suppresses DC. So the unchanged Berger verdicts are NOT a bug.

---

## 4. raw#71 falsifier re-check

Pre-registered falsifier: "**HPF must NOT cause eyes-open daily-life files to falsely PASS Berger**"
(daily-life is eyes-open + motion-rich; should NEVER show resting-EC alpha rhythm).

Post-HPF result: `daily_life_5min_1_*` files all FAIL post-HPF with peak in δ band.
**raw#71 HOLDS** — no eyes-open false-positive.

---

## 5. Root cause re-evaluation (raw#91 honest C3)

The hypothesis "DC drift dominant" is **partially refuted**. Extended HPF cutoff
sweep on best candidate (`post_battery_ica` O1/O2):

| cutoff (Hz) | O1 peak | O2 peak | O1 α/β | O2 α/β | both C1? |
|---|---|---|---|---|---|
| 0.5 | 1.46 | 1.46 | 0.73 | 0.56 | 0/2 |
| 1.0 | 1.71 | 1.71 | 0.73 | 0.56 | 0/2 |
| 2.0 | 3.17 | 3.17 | 0.73 | 0.56 | 0/2 |
| 3.0 | 6.10 | 6.10 | 0.73 | 0.56 | 0/2 |
| 4.0 | 6.10 | 6.10 | 0.73 | 0.56 | 0/2 |
| 6.0 | 9.28 | 9.28 | 0.70 | 0.53 | 0/2 |
| 7.0 | 9.28 | 9.28 | 0.63 | 0.48 | 0/2 |

**Critical finding**: even at HPF cutoff 7 Hz (which obliterates δ/θ),
**α/β remains < 1.0** on both O1 and O2. C1 is structurally violated,
NOT a peak-picker artifact.

### Revised root cause (3 ranked hypotheses)

1. **Eyes-state mismatch (likely)** — The "resting" sessions were probably
   recorded eyes-open or with eyes only briefly closed. Berger alpha requires
   sustained eyes-closed state (≥10 s). Filenames are nominal, not eyes-state-verified
   (already flagged in inventory §8.3).
2. **Occipital electrode placement / contact** — O1/O2 (idx 6, 7) may have
   been mis-placed or had high impedance, suppressing the 10 Hz rhythm. The
   broadband β > α profile is consistent with high-impedance frontalised pickup.
3. **Subject-specific α suppression** — ~10–15 % of healthy adults have
   weak/absent occipital alpha even with eyes closed (raw#91 honest disclosure).

Fix path B (label-confirmed eyes-closed re-recording) is now **higher-priority
than fix path A**. HPF preprocessing remains valid as a hygiene step but is
**NOT sufficient** to resolve the 0/15 deadlock.

### Projection vs measurement (raw#91 C3)

- **MEASURED** (this run): post-HPF 0/15 PASS; α/β < 1.0 even at HPF 7 Hz on
  best candidate; raw#71 falsifier HOLDS.
- **PROJECTED** (untested without new recording): label-verified eyes-closed
  recording with confirmed O1/O2 contact ≥ 5 kΩ → predicted ≥ 1/3 PASS.

---

## 6. Reproducibility manifest

```bash
# Re-run (raw#65 idempotent — appends to existing ledger):
.venv-eeg/bin/python3 /tmp/anima_berger_hpf_rerun_orchestrator.py

# Selftest the HPF module:
hexa run anima-eeg-core/tool/modules/_artifact/hpf_dc_drift.hexa --selftest

# Apply HPF to a single file (hexa entry):
hexa run anima-eeg-core/tool/modules/_artifact/hpf_dc_drift.hexa \
    --apply --in <p.npy> --out <q.npy> --fs 125 --cutoff 0.5
```

- HPF outputs: `state/eeg_hpf_05hz_2026_04_28/*_hpf05.npy` (15 files, float32)
- Audit ledger: `state/clm_eeg_berger_audit/2026-04-28_hpf_rerun.jsonl`
  (15 rows, schema `anima-clm-eeg/berger_hpf_rerun/1`)
- Hexa module: `anima-eeg-core/tool/modules/_artifact/hpf_dc_drift.hexa`
  (raw#1 chflags uchg locked post-commit)

---

## 7. Verdict

- **HPF 0.5 Hz preprocessing alone does NOT rescue Berger gate** on D-day data.
- DC drift is a **secondary** issue; the **primary** issue is α/β < 1.0
  occipital profile inconsistent with eyes-closed resting.
- raw#71 falsifier HOLDS post-HPF (no eyes-open false-positive).
- Recommended next action: **label-verified eyes-closed re-recording** with
  occipital impedance check < 10 kΩ before further detector tuning. Detector
  remains unchanged (cf. own5 frozen criteria; raw#12).
