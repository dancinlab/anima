# Resting State Network (RSN) Paradigm — DMN approximate + Frontal Alpha Asymmetry

**Date**: 2026-04-28
**Track**: anima T15 (β Learning-Free, EEG / consciousness measurement)
**raw**: #9 #10 #12 #37 #65 #71 #82 #91 own5

---

## 1. Purpose

Use 16-channel surface EEG to **approximate** two well-known resting-state phenomena:

1. **DMN coherence** (Default Mode Network) — anterior medial prefrontal ↔ posterior precuneus / lateral parietal correlation in eyes-closed rest. fMRI-BOLD DMN is the gold standard; we approximate via EEG band-limited coherence.
2. **Frontal alpha asymmetry** (Davidson 1992) — right-vs-left alpha-band log-power difference; mood / approach-withdrawal motivation marker.


---

## 2. Channel layout (this rig — 16ch Cyton+Daisy, UltraCortex Mark IV)

Canonical recorder order (per `anima-eeg/impedance_real_hardware_validation.hexa`):
```
ch  1: Fp1     ch  9: F7
ch  2: Fp2     ch 10: F8
ch  3: C3      ch 11: F3
ch  4: C4      ch 12: F4
ch  5: P7      ch 13: T7
ch  6: P8      ch 14: T8
ch  7: O1      ch 15: P3
ch  8: O2      ch 16: P4
```

NPY layout: `(16, N_samples)` — index `i` = ch `i+1`.

**No Pz** on this rig — posterior-DMN uses (P3 + P4) / 2 as a precuneus proxy.

---

## 3. Node definitions (16ch surface DMN approximation)

| Node                 | Channels    | Indices (0-based) |
|----------------------|-------------|-------------------|
| Anterior DMN (mPFC)  | Fp1, Fp2    | 0, 1              |
| Posterior DMN (PCC/precuneus proxy) | P3, P4 | 14, 15  |
| Lateral parietal L   | P7          | 4                 |
| Lateral parietal R   | P8          | 5                 |

DMN coherence metric: **magnitude-squared coherence** over the alpha band 8-13 Hz between
average-anterior and average-posterior signals, computed via Welch CSD.

---

## 4. Frontal alpha asymmetry (Davidson 1992)

- Right frontal: F4, F8 → average, alpha 8-13 Hz log-power
- Left frontal:  F3, F7 → average, alpha 8-13 Hz log-power
- **Asymmetry index** = log(α_right) − log(α_left)
  - Positive → right > left → approach motivation, well-being
  - Negative → left  > right → withdrawal motivation, depression risk

Note: per Davidson convention some papers compute log(L) − log(R); we adopt the
"right minus left log power" form and document the sign explicitly to avoid

---


| ID  | Metric                                 | Threshold (this paradigm)         |
|-----|----------------------------------------|-----------------------------------|
| C1  | DMN α-coherence (anterior↔posterior)   | ≥ 0.30 (eyes-closed expected)     |
| C2  | Berger-like ordering                   | coherence(eyes-closed) > coherence(eyes-open) — DEFERRED to two-condition recording |
| C3  | Frontal asymmetry observed             | |asymmetry| ≥ 0.05 (population mean ≠ 0; sign reported) |
| C4  | Alpha band present                     | α-power / total > 0.05 in ≥1 occipital ch (O1 or O2) |

Verdict RSN.PASS = (C1 ∧ C3 ∧ C4) on a single-condition recording (current D-day data
is single eyes-open daily-life run, NOT eyes-closed; C2 is reported as N/A).

---


- **F1**: DMN coherence < 0.10 → "no network signal"
- **F2**: anterior-posterior coherence reversed (anterior↔O1/O2 stronger than anterior↔P3/P4) → wrong topology
- **F3**: all four frontal channels (F3/F4/F7/F8) log-power within ±1% → asymmetry indistinguishable from 0 (numerical degeneracy)
- **F4**: alpha band absent (band-power / broadband < 0.02 in occipitals) → posterior alpha not generating
- **F5**: 16ch surface DMN ≠ fMRI DMN — false positive risk; volume conduction can yield spurious frontal-parietal coherence (fMRI cross-modal validation required)

---


1. **16ch surface ≠ fMRI BOLD DMN** — surface EEG measures cortical sources spread by volume conduction; fMRI DMN includes deep midline structures (PCC, mPFC, angular gyrus) we cannot localize without source modeling (e.g., LORETA, beamforming).
2. **Volume conduction** — frontal alpha may be occipital alpha spread; reported asymmetry can be contaminated by reference choice (this rig uses linked-ear / SRB2 reference).
3. **Single-subject N=1** — generalizability requires N ≥ 30 per Davidson convention; this is a personal-instrument single-subject pilot.
4. **Eyes-open daily-life data** — DMN is most pronounced eyes-closed; the D-day file (`20260428T115006Z_daily_life_5min_1_eeg16_ica.npy`) is eyes-open task-engaged. Coherence values reported here are LOWER BOUND on the eyes-closed phenomenon — passing C1 on this file is a strong positive; failing on this file does NOT falsify resting DMN.
5. **No baseline comparison** — proper Berger-like demonstration requires a paired eyes-closed run; deferred until a 60s eyes-closed recording is captured.

---

## 8. Output

- `state/rsn_audit/<UTC-date>_rsn.jsonl` — append-mode audit row per analysis
- `state/eeg_resting_state_network.json` — latest-run cert

Schema (audit row):
```json
{ "tool":"resting_state_network_analyzer", "version":"v1",
  "ts_utc":"...", "input":"...", "input_sha256":"...",
  "fs_hz":125.0, "n_samples":6252,
  "dmn_coh_alpha":0.xxx,
  "dmn_coh_anterior_lateral_l":0.xxx, "dmn_coh_anterior_lateral_r":0.xxx,
  "alpha_log_left":-x.xxx, "alpha_log_right":-x.xxx,
  "frontal_alpha_asymmetry":x.xxx,
  "occipital_alpha_ratio":0.xxx,
  "criteria":{"C1":1,"C2":"N/A","C3":1,"C4":1},
  "verdict":"RSN_PASS|RSN_FAIL",
  "falsifiers_count":5, "raw_compliance":[9,10,12,37,65,71,82,91] }
```

---

## 9. Implementation

- selftest synthetic: two correlated 10 Hz alpha sources (anterior + posterior) → coherence > 0.5 expected; uncorrelated → coherence < 0.1

---

## 10. Cross-references

- This file extends the resting-state axis with **network-level** (not single-channel) probes.
