# Long-Duration EEG Recording Protocol (T13)

**Date**: 2026-04-28
**Author**: anima T13 track
**Frozen**: raw#9 / 10 / 12 / 37 / 65 / 71 / 82 / 91 / own 5

---

## 1. Motivation

Existing 60s short-window EEG recordings are insufficient for:

- **Gamma statistics stability** — gamma band power (25–45 Hz) requires ≥10 min
  for stable per-subject central tendency (CV ≤ 15%).
- **State transition observation** — drowsy onset, attention release, mental
  fatigue all manifest on minute-to-tens-of-minutes time scales.
- **LZ76 b(n) drift characterization** — within-session b drift cannot be
  separated from between-session drift on 60s windows.

T13 introduces a **1 hour+ continuous recording protocol** with mid-flight
integrity checks, ICA + LZ76 sliding window, and PELT change-point analysis.

---

## 2. Pre-flight checklist

| # | Step | Acceptance |
|---|------|------------|
| 1 | Saline application — soak each electrode pad for ≥60s, refill cup-electrodes to ~3/4 full | All 16 electrodes wet, no dry pads |
| 2 | Helmet strap tightening — chin strap + cap drawstring | Helmet does not slip when subject nods |
| 3 | Impedance baseline — `impedance_check --check --green-kohm 750` | 16/16 GREEN at t=0 |
| 4 | BrainFlow streaming sanity — `eeg_setup --board-health` | board_health PASS |
| 5 | Subject seated, eyes-open neutral resting state for 30s pre-roll | RMS within 5–50 µV per channel |

---

## 3. Recording structure

```
duration_minutes  = 60   (also supports 90 / 120)
segment_seconds   = 60
inter_segment_gap = 0    (continuous)
total_segments    = duration_minutes  (== 60 for 1h)
```

- **Output array**: `state/long_duration_recordings/<date>_<duration>min.npy`
  (shape `[total_segments, 16, 250*60]` = `[60, 16, 15000]` for cyton_daisy 250 Hz)
- **Per-segment ledger**: `state/long_duration_audit/<date>_segments.jsonl`
  one JSONL row per segment with metrics + integrity flags.

---

## 4. Mid-flight integrity checks

### 4.1 Per 10 min — impedance recheck

- Pause streaming, run `z`-command sweep (16ch, ~20s).
- Compute drift `Δz_kohm[ch] = z_now[ch] − z_baseline[ch]`.
- **F1 saline-dry falsifier**: any channel with `Δz > 200 kΩ` → flag segment
  as `saline_dry=true`, abort recording at boundary.

### 4.2 Per 5 min — ICA + LZ76 sliding window

- Sliding window: 60s width, 30s stride → 2 windows/min, ~120 windows/hour.
- ICA application: 16-component decomposition, eye-blink + EMG components
  removed (EOG corr > 0.7, gamma broadband > 1.5σ).
- LZ76 b(n) computed on cleaned signal per window.
- **State transition detection** via PELT change-point detection on
  `b[w]` time series:
  - β = 3·log(N) penalty (BIC-style)
  - min segment length = 4 windows (2 min)
  - reported events: `{onset_iso, b_pre, b_post, Δb}`.

---

## 5. Post-flight

| # | Step | Output |
|---|------|--------|
| 1 | Final impedance sweep | `impedance_max_kohm_final` per ch |
| 2 | Per-segment metrics aggregation | mean/std of LZ76, gamma/theta, engagement, drowsy |
| 3 | State transition timeline | PELT change-points overlaid on b(n) plot (ASCII) |
| 4 | Drift quantification | rms variance per channel vs baseline first 5 min |
| 5 | Ledger seal | `chflags uchg` on JSONL + npy (raw#37 SSOT) |

---

## 6. Frozen criteria (raw#12)

- **F-saline**: impedance change > 100% over 60 min on any channel ⇒ saline-dry.
- **F-drift**: per-channel rms variance > 3× baseline ⇒ helmet slipped.
- **F-usable**: ≥ 70% segments (≥ 42 / 60) survive artifact rejection. Below
  threshold ⇒ session marked `unusable=true`, retracted from longitudinal pool.

---

## 7. raw#71 falsifiers (5+)

| ID | Falsifier | Detection | Action |
|----|-----------|-----------|--------|
| F1 | impedance Δz > 200 kΩ over 60 min | per-10min sweep | abort, flag `saline_dry` |
| F2 | SRB2 disconnect mid-recording | RMS collapse on all ch simultaneously | abort, flag `srb2_loss` |
| F3 | motion artifact > 50% of segments | per-segment rms-z > 4 detector | session unusable |
| F4 | BrainFlow streaming gap > 10 s | timestamp delta scan | abort, flag `stream_gap` |
| F5 | subject removed helmet (indirect — no touch sensor) | sustained rms < 2 µV across ≥ 8 ch for ≥ 20 s | abort, flag `helmet_off` |
| F6 | SD-card fill (BrainFlow log buffer) | exit code from streamer | abort, flag `disk_full` |

All falsifiers are evaluated post-segment and recorded in the per-segment
ledger row alongside the metrics.

---

## 8. Implementation skeleton

- `anima-eeg/tool/long_duration_recorder.hexa` (~150 LoC, this commit)
  - protocol runner: 60 min auto-record + mid-flight impedance hooks
  - selftest path: synthetic 60-segment × 16ch deterministic FNV simulation
  - JSONL ledger append (raw#37 SSOT, raw#65 idempotent)

- Real-data path (deferred to T13.1):
  - BrainFlow live stream → npy buffer
  - ICA via `.venv-eeg/bin/python` helper (transient `/tmp` script — raw#37)
  - PELT change-point via `ruptures` package or pure-hexa min-cost dynprog

---

## 9. User action plan

```
# 1) Pre-flight
.venv-eeg/bin/python -m anima_eeg_setup --board-health
hexa run anima-eeg/impedance_check.hexa -- --check --green-kohm 750

# 2) Start 60-min recording
hexa run anima-eeg/tool/long_duration_recorder.hexa -- \
    --duration-min 60 --segment-sec 60 --append

# 3) Post-flight
hexa run anima-eeg/impedance_check.hexa -- --check
# inspect: state/long_duration_audit/<date>_segments.jsonl
```
