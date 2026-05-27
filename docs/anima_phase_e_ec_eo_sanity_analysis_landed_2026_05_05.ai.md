# Phase E EC/EO Berger Sanity Analysis — Landed 2026-05-05

- **BG lane**: PHASE-E-EC-EO-SANITY-ANALYSIS
- **Compute**: ubu1 (`/home/aiden/venv_orchestrator/bin/python`, scipy 1.17.1, numpy 2.4.4)
- **Wall time**: ~0.7 s (analysis) + sync (~1 s)
- **Cost**: $0
- **Verdict JSON**: `state/phase_e_ec_eo_sanity_analysis_2026_05_05/verdict.json`
- **PSD overlay**: `state/phase_e_ec_eo_sanity_analysis_2026_05_05/psd_overlay.png`
- **Inputs**:
  - EC: `state/anima_phase_e_eeg_live_2026_05_05/berger_ec_60s.npy` (sha256 7329442a-redacted)
  - EO: `state/anima_phase_e_eeg_live_2026_05_05/berger_eo_60s.npy` (sha256 4ba61702-redacted)

## What ran
1. Sync EC/EO npy + meta to ubu1 (`/home/aiden/anima_phase_e_2026_05_05/`).
2. Load 32-row board capture, slice rows 1..16 as 16ch EEG.
3. 1-50 Hz Butterworth bandpass (order 4, zero-phase filtfilt).
4. Welch PSD per channel (4-second segments, 50% overlap, ~0.25 Hz resolution).
5. Integrate alpha band power 8-13 Hz per channel.
6. F-BERGER-1 (occipital alpha EC > EO) and F-BERGER-2 (occipital > frontal in EC).

## Headline result — Berger classical NOT replicated

| Falsifier | Outcome |
|---|---|
| F-BERGER-1 occipital alpha EC > EO | **FAIL** (O1 ratio 0.31, O2 ratio 0.02 — both EO ≫ EC) |
| F-BERGER-2 occipital alpha > frontal alpha (EC) | **PASS** (occ 873.8 vs front 3.6 µV², ~240×) |
| `berger_classical_replicated` | **false** |
| `ready_for_phase_e_main_protocol` | **false** |

Alpha peak frequency in EC is within the classical 8-13 Hz Berger band:
- O1 peak: 8.51 Hz
- O2 peak: 8.26 Hz

Effective sample rate guard PASSES: fs_ec = 120.18 Hz, fs_eo = 120.22 Hz (both ≫ 30 Hz threshold).

## Diagnostic concerns

The polarity inversion (EO > EC) is uniform across all 16 channels, not just occipital — every single channel shows EO power higher than EC. This is highly suspicious and points to one of three possible causes:

1. **EC/EO labels swapped at capture time.** If the user actually had eyes OPEN during the file labelled `berger_ec` and eyes CLOSED during `berger_eo`, the alpha pattern in the data is internally consistent: O2/P4 EO show massive alpha (44k µV²) which would actually be the EC condition. Recommend sanity-check protocol log / video timestamps.
2. **Contact / impedance asymmetry.** O2 and P4 show ~200× the alpha power of O1 (44167 vs 14 µV² in EO; 869 vs 4 in EC). One pair of electrodes is dominating — likely a saturated or floating channel, not biological alpha. P4/O2 anomaly suggests a single hardware fault on those daisy/cyton lanes.
3. **Eye-movement / blink artefact in EO.** Without ICA, EO contains large frontal-driven artefacts that leak into the 8-13 Hz band via filter ringing. Frontal channels (Fp1=75.7, Fp2=6.0 in EO) support this hypothesis but the magnitude on occipital is too large to be explained by frontal leakage alone.

## Honest C3+ caveats (>=5 per raw#10)

1. 60-s baseline captures resting alpha only; binding evidence (high-gamma coherence on reading task) requires Phase E main protocol.
2. Effective fs ~120 Hz vs claimed 125 Hz (drop_ratio 0.96); Nyquist 60 Hz so alpha band is safe but any >40 Hz analyses need spectral-leakage verification.
3. Single subject, single session — no test-retest or inter-subject generalisation.
4. Contact quality GREEN/GRAY mix per capture log; GRAY channels (some C3/C4 etc.) inflate PSD and bias regional comparisons.
5. Berger classical replication is a CAPTURE-QUALITY signal, not binding evidence; passing is necessary but NOT sufficient for Phase E binding claims.
6. `filtfilt` zero-phase doubles effective filter order (4→8) and assumes stationarity; eye-blink / EOG artefact in EO not removed (no ICA, no artefact rejection).

## Recommendation — do NOT advance to Phase E main protocol yet

`ready_for_phase_e_main_protocol = false`. Three concrete next steps in priority order:

1. **Verify EC/EO labelling** by re-running 60-s × 2 capture with explicit verbal cue logged in meta (`condition_cue_ts`) and a separate audio/video witness if possible. If polarity inverts after re-capture with corrected labels, the rig is fine — the original session was mislabelled.
2. **Inspect O2 / P4 channels** independently — impedance check, electrode reseat, raw timeseries plot to confirm they are not rail-saturated. Document in the existing `electrode_reseat_b_track_runbook` flow.
3. **Add minimal artefact rejection** (high-amplitude epoch reject ±150 µV, optional ICA component drop on Fp1/Fp2 frontal eye-blink components) before running the main reading-task protocol so high-gamma coherence interpretation is not contaminated.

Do NOT git-commit per spec. No `.roadmap.*` updates. Companion handoff complete.
