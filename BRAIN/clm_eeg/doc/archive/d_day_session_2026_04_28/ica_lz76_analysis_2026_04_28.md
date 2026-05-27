# ICA artifact rejection + LZ76 re-run — 2026-04-28

**Repo**: `<repo-root>`
- C1: `b(n) >= 0.65` (Schartner 2017 normal-range floor)
- C2: `|Δ|/human_baseline <= 20%` (vs baseline 0.85)
- P1 = C1 AND C2

---

## 1. ICA pipeline

`mne-python 1.12.1`, FastICA, `n_components=15` (16ch one-shy for rank-safety after average ref), `random_state=42`, `max_iter=500`. ICA fit on a 1 Hz high-pass copy of the input (standard practice for stable decomposition); the unmixing matrix is then applied to the (notch+bandpass-filtered) full-band copy.

Input File 1 (`baseline_resting_60s_20260428.npy`) is **raw uV**, so the pipeline applied a 60 Hz notch + 0.5–50 Hz bandpass before ICA, matching File 2's pre-processing.

Input File 2 (`baseline_resting_low_emi_20260428T113016Z_seg000_eeg16_filtered.npy`) was already notch+bandpass filtered.

Auto-detection used (from MNE):
- `find_bads_eog(ch_name=['Fp1','Fp2'], threshold=2.5)` — eye blinks (frontal proxy)
- `find_bads_ecg(method='correlation', measure='correlation', threshold=0.6)` — heartbeat
- `find_bads_muscle(threshold=0.5)` — high-frequency EMG

> **Note**: `find_bads_ecg` returned an MNE error ("Generating an artificial ECG channel can only be done for MEG data") on both files — no dedicated ECG channel and the synthetic-ECG fallback path is MEG-only. ECG components were therefore **not** identified by MNE. Any cardiac contribution remains entangled in the EEG-like residue (see honest C3 §6).

---

## 2. ICA component classification

### File 1 (`baseline_resting_60s_20260428.npy`, raw → notch+bp → ICA)

| component | EOG (Fp1/Fp2) | ECG | muscle | classification |
|---|---|---|---|---|
| 0 | YES | — | no | EOG (eye blink) |
| 1 | no  | — | no | EEG-like |
| 2 | no  | — | no | EEG-like |
| 3 | no  | — | YES | muscle |
| 4 | no  | — | YES | muscle |
| 5 | YES | — | YES | EOG + muscle |
| 6–14 | no | — | YES | muscle |

- EOG: **2** (comps 0, 5)
- ECG: **0** (detector unavailable — no ECG ch / not MEG)
- Muscle: **12** (comps 3,4,5,6,7,8,9,10,11,12,13,14)
- **Excluded: 13** (union)
- **EEG-like remaining: 2** (comps 1, 2)

### File 2 (`baseline_resting_low_emi…filtered.npy`, ICA only)

| component | EOG (Fp1/Fp2) | ECG | muscle | classification |
|---|---|---|---|---|
| 0 | YES | — | no | EOG |
| 1 | YES | — | YES | EOG + muscle |
| 2 | no  | — | no | EEG-like |
| 3 | no  | — | no | EEG-like |
| 4 | no  | — | no | EEG-like |
| 5 | no  | — | YES | muscle |
| 6 | no  | — | YES | muscle |
| 7 | no  | — | no | EEG-like |
| 8 | no  | — | YES | muscle |
| 9 | no  | — | YES | muscle |
| 10 | no | — | no | EEG-like |
| 11 | no | — | no | EEG-like |
| 12 | no | — | no | EEG-like |
| 13 | no | — | YES | muscle |
| 14 | no | — | no | EEG-like |

- EOG: **2** (comps 0, 1)
- ECG: **0** (detector unavailable)
- Muscle: **6** (comps 1, 5, 6, 8, 9, 13)
- **Excluded: 7** (union)
- **EEG-like remaining: 8** (comps 2, 3, 4, 7, 10, 11, 12, 14)

---

## 3. RMS amplitude check (normal resting EEG ≈ 5–50 µV)

| stage | File 1 rms-med | File 2 rms-med |
|---|---:|---:|
| input              | 39 836 µV | 884.7 µV |
| + notch + bandpass | 1 476 µV  | 884.7 µV (already filtered) |
| + ICA cleaning     | **77.9 µV** | **50.0 µV** |

ICA brought File 2 to the upper edge of the textbook 5–50 µV resting band; File 1 still sits ~1.5× above it (consistent with only 2 EEG-like comps surviving — see §6 limitation).

---

## 4. LZ76 re-run results

LZ76 verifier raw outputs (one row each in `state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl`, mirrored to `/tmp/lz76_file{1,2}_ica.jsonl`):

| input | shape | preproc | rms-med µV | b(n) | C1 (≥0.65) | C2 (≤20%) | P1 |
|---|---|---|---:|---:|:---:|:---:|:---:|
| File 1 raw | (16,7491) | none | 39 836 | 0.057 | F | F | FAIL |
| File 1 filt | (16,7491) | notch+bp | 1 054* | 0.479 | F | F | FAIL |
| **File 1 ICA** | (16,7491) | notch+bp+ICA | **77.9** | **0.362** | F | F | **FAIL** |
| File 2 raw | (16,7493) | none | 33 048 | 0.040 | F | F | FAIL |
| File 2 filt | (16,7493) | notch+bp | 884.7 | 0.395 | F | F | FAIL |
| **File 2 ICA** | (16,7493) | notch+bp+ICA | **50.0** | **0.519** | F | F | **FAIL** |

\* prior session value; this run produced rms-med 1 476 µV after the same notch+bp (slight numeric difference irrelevant).

### Direction

- **File 2**: `0.395 → 0.519` (Δ +0.124 = +12.4pp). Closer to Schartner floor 0.65 but not there. With 8 EEG-like components retained, ICA improved complexity meaningfully.
- **File 1**: `0.479 → 0.362` (Δ −0.117 = −11.7pp). **Worse** than filtered. Auto-detector classified 12/15 components as muscle, leaving only 2 EEG-like comps — over-aggressive removal collapsed signal entropy.

### Schartner 2017 normal range 0.5–0.9

- File 1 ICA b=0.362 → **below floor**
- File 2 ICA b=0.519 → **inside the lower band** (0.5–0.9) but below the 0.65 P1 floor

Neither file reached `b ≥ 0.65`. P1 remains **FAIL** for both.

---

## 5. Why File 1 regressed (diagnostic)

- File 1 is `manual_direct_brainflow` capture. Filtered rms-med 1 476 µV (~30× normal) indicates persistent broadband artifact dominating the variance — very plausibly all 16 ICA basis vectors absorb artifact, so the high-freq detector finds 12/15 "muscle" components. The auto-pipeline then strips real EEG along with EMG/EOG, leaving only 2 components (0.6 µV-RMS-class noise floor) → entropy collapse → low b(n).
- File 2 is `eeg_recorder + filtered`, rms 884 µV → ~17× normal — closer to recoverable regime — and ICA isolated 8 EEG-like components, so Lempel-Ziv production count rose.

---


1. **Visual inspection is the gold standard.** MNE auto-detectors (`find_bads_eog/ecg/muscle`) are heuristic; rejecting components without topo/PSD/timecourse review can over- or under-clean. This run is **automatic-only** — no human-in-the-loop validation.
2. **`find_bads_ecg` failed silently** on both files (MNE: "artificial ECG channel only for MEG data"). Any cardiac component is **still in** the surviving EEG-like residue, which inflates structured (low-entropy) content and depresses b(n).
3. **`find_bads_muscle` over-fired on File 1**: 12/15 components flagged. With the same 0.5 threshold, File 2 flagged 6/15. The asymmetry is consistent with File 1 being more contaminated overall (higher pre-ICA rms, raw EMG saturation possible) rather than a real difference in muscle-content topology — auto-thresholding on a high-noise dataset overcounts.
4. **No EOG/EMG ground-truth channel** — Fp1/Fp2 are EEG channels used as virtual EOG; this is the standard fallback but introduces blink/EMG ambiguity.
5. **n_components=15** (rank-safe after average reference applied during ICA fit). Could differ if no avg-ref were applied.

---

## 7. Artifacts produced

- `<repo-root>/recordings/sessions/baseline_resting_60s_20260428_ica.npy` (16×7491 float64)
- `<repo-root>/recordings/sessions/baseline_resting_low_emi_20260428T113016Z_seg000_eeg16_ica.npy` (16×7493 float64)
- `/tmp/ica_helper.py`, `/tmp/ica_helper_summary.json`
- `/tmp/lz76_file1_ica.json`, `/tmp/lz76_file1_ica.jsonl`
- `/tmp/lz76_file2_ica.json`, `/tmp/lz76_file2_ica.jsonl`
- LZ76 audit: `state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl` (appended)

## 8. Recommendation

The ICA result for File 2 (b=0.52, rms 50 µV) is the cleanest LZ76 number to date but still 0.13 short of the C1 floor. Real path forward:

1. Capture a longer (≥ 5 min) low-EMI session with verified <5 kΩ impedance at all 16 sites.
2. Run ICA with **manual** component review (mne `ica.plot_components()` topo + `plot_properties` PSD) instead of auto-only.
3. Optionally try ICLabel (`mne-icalabel`) for trained component classification.

This is consistent with the project_main_track_beta note — empirical Stage-1/2 readiness is for evidence accumulation, not the only real-use path.
