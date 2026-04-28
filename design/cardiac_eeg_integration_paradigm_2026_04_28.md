# Cardiac (ECG/PPG) ↔ EEG Cross-Modal Integration — C20

Date: 2026-04-28
Genus (raw#106): cardiac-eeg-cross-modal-correlation-paradigm
Frameworks (own-5 ≥ 2): Pan-Tompkins 1985 (R-peak), Task Force 1996 (HRV RMSSD),
                         Thayer 2009 (cardiac-vagal/EEG coupling),
                         McCraty 2014 (heart-brain coherence), Critchley 2003 (interoception)

## Purpose

Pair OpenBCI Cyton's auxiliary analog GPIO (D11, D12, A6, A7) with the existing
EEG pipeline so that cardiac rhythm (ECG R-peaks → HR/HRV) and EEG state
(LZ76, engagement, drowsy_idx, alpha-attenuation) can be correlated within
a single deterministic synth pipeline. This unlocks the heart-brain coherence
hypothesis (HRV ↔ DMN coherence; RR-interval ↔ alpha attenuation) on the
β Learning-Free main track without any cloud/API call (raw#13).

## NO API (raw#13)

NO Claude / LLM / remote inference. All processing is local: BrainFlow auxiliary
channels → numpy/scipy Pan-Tompkins → Pearson correlation. Synth selftest is
deterministic by (mode, seed) (raw#65 idempotent).

## Hardware path

- OpenBCI Cyton + Daisy → 8/16 EEG channels (existing)
- Cyton auxiliary GPIO: D11, D12 (digital), A6, A7 (analog) — 250 Hz aux rate
- ECG path (Lead-II preferred): RA + LL + RL ground → A6 (single ended)
- PPG path (alternative, simpler): finger-clip transmissive PPG → A7
- BrainFlow exposes via `BoardShim.get_other_channels()` (Cython aux mapping)

### ECG vs PPG choice (frozen, raw#12)

PRIMARY = PPG (finger-clip).
Reason: (a) no chest electrode placement = lower friction; (b) movement
artifact tolerable for resting baseline; (c) avoids 60 Hz mains coupling
that plagues bare-chest ECG without driven-shield. ECG is supported as a
fallback when finer R-peak timing is needed (HRV RMSSD < 25 ms regimes).

## Signal processing (frozen criteria, raw#12)

1. 250 Hz analog ingest via BrainFlow `get_other_channels()`
2. Bandpass 0.5–40 Hz (ECG) or 0.5–10 Hz (PPG)
3. R-peak detection: Pan-Tompkins 1985
   - derivative → squaring → moving-window integration (150 ms)
   - adaptive threshold = 0.3125 × signal-level + 0.6875 × noise-level
   - 200 ms refractory; T-wave rejection via slope ratio
4. RR-intervals → instantaneous HR (BPM)
5. HRV RMSSD over 5-min sliding window: sqrt(mean(diff(RR)^2))
6. HR physiological clamp 40–180 BPM (out-of-range → flag invalid window)

## EEG-ECG paired correlation (raw#82 cross-modal)

For each 5-min sliding window we emit JSONL row containing:
- hr_bpm, hrv_rmssd_ms, rr_count
- eeg_alpha_atten_x1000, eeg_engagement_x1000, eeg_drowsy_x1000, eeg_lz76_x1000
- pearson_hrv_alpha_x1000, pearson_hr_engagement_x1000

Acceptance threshold (frozen): |r| ≥ 0.30 over N ≥ 1 week of paired windows
to call the heart-brain coupling REAL (raw#10 honest C3 pattern).

## Falsifiers (raw#71 ≥ 5)

- F1: synth ECG at fixed 60 BPM → detected_hr_bpm in [58, 62]
- F2: physiological clamp — HR < 40 (40 too low) or > 180 → marked invalid
- F3: 60 Hz mains injection (synth EMI) → detector still finds R-peaks
      with > 0.95 recall (Pan-Tompkins is mains-tolerant via bandpass)
- F4: idempotent — same (mode, seed) ⇒ identical row (raw#65)
- F5: low-r relationship sane — synth 'desync' mode produces |r| < 0.10
      between HRV and alpha (i.e. when uncoupled, we DETECT uncoupled)

## Files

- design/cardiac_eeg_integration_paradigm_2026_04_28.md (this doc)
- anima-eeg/tool/cardiac_eeg_integrator.hexa (~150 LoC)
- /tmp/cardiac_helper.py (transient, raw#37; numpy + Pan-Tompkins)
- state/cardiac_eeg_audit/<UTC-date>_cardiac.jsonl (raw#77 audit)
- state/anima_eeg_cardiac_selftest_synth.json (selftest fixture)

## raw / own-5 bookkeeping

raw#9 · raw#10 · raw#12 · raw#37 · raw#65 · raw#71 · raw#77 · raw#82 · raw#91 · own 5

## raw#10 honest C3 (hardware gap)

The user does not currently own an ECG chest-strap or finger-clip PPG sensor.
This tool LANDS the software path (selftest + falsifiers PASS on synth) so
that cardiac integration is shovel-ready; the moment the user solders A6/A7
to an off-the-shelf PPG (e.g. Pulse Sensor SEN-11574, ~$25) the `--tick`
path becomes a 250 Hz live feed without further code changes.

## User action plan

1. Order finger-clip PPG (Pulse Sensor SEN-11574 or equivalent), ~$25
2. Solder 3-pin header (V+, GND, signal) to Cyton's A7 + GND + 3.3 V rail
3. Run `hexa.real run anima-eeg/tool/cardiac_eeg_integrator.hexa --tick`
   while EEG `eeg_recorder.hexa` records in parallel
4. After 1 week of paired data, run `--correlate` to compute |r| HRV↔alpha
