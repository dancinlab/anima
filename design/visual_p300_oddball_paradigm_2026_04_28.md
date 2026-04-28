# Visual P300 Oddball Paradigm — Design (2026-04-28)

**Project**: anima T3 — Visual P300 ERP paradigm
**Status**: DESIGN + REFERENCE IMPLEMENTATION (synthetic selftest only; live BrainFlow deferred)
**Compliance**: raw#9 hexa-only · raw#10 honest-C3 · raw#12 frozen pre-registered · raw#37 transient · raw#65 idempotent · raw#71 falsifier-3+ (5 here) · raw#82 darwin-native · raw#91 honesty-class · own 5
**anima main-track**: β Learning-Free (memory: project_main_track_beta) — additive paradigm, orthogonal axis to LZ76 baseline (Schartner 2017).

## 0. Executive Summary

The Visual P300 Oddball is the gold-standard cognitive ERP paradigm in clinical
consciousness assessment (e.g. coma vigil, Schartner 2017 cross-validation
references P300 in awake-vs-anesthesia separation). Two stimulus classes
(80% standard / 20% oddball) presented in random sequence with stimulus-locked
EEG epochs averaged per class; the oddball-minus-standard difference wave at
parietal Pz, peaking 250-400 ms post-onset, is the canonical P300 marker.

This module lands the protocol runner + analysis spec **synthetically**. Real
BrainFlow stimulus-trigger sync is deferred to a follow-up cycle (raw#10 honest:
no Pyglet/screen present in this landing, terminal-based stimulus only).

## 1. Protocol

### 1.1 Stimulus design

| Class | Probability | Visual (terminal) | Visual (Pyglet — deferred) |
|---|---|---|---|
| Standard | 80% | `[ ]` blue square (ANSI 24-bit) | blue square sprite |
| Oddball | 20% | `<>` red triangle | red triangle sprite |

- **Total stimuli per session**: 200-400 (configurable; default 240 for 5-min)
- **ISI (inter-stimulus interval)**: random uniform 1.5-2.0 s
- **Stimulus duration on-screen**: 200 ms
- **Sequence**: randomized with constraint *no two oddballs adjacent* (avoids
  refractory contamination of P300; standard ERP-paradigm rule).
- **RNG**: LCG seeded with `--seed` (default 42) → deterministic sequence
  reproducible run-to-run for selftest.

### 1.2 Trigger sync

- Stimulus onset timestamp (`t_onset_ms`) recorded via monotonic clock at
  the moment the visual is rendered to terminal (or Pyglet `flip()` in the
  deferred GUI path).
- **Time precision**: targeted ≤1 ms via `python3 -c "import time; print(int(time.monotonic_ns() // 1000000))"`
  shellout (raw#82 darwin-native: macOS `clock_gettime(CLOCK_MONOTONIC)` is
  ns-resolution; ms truncation gives 1 ms guarantee).
- BrainFlow streaming is started before the first stimulus and stopped after
  the last stimulus + 500 ms post-window. Trigger timestamps are aligned to
  EEG samples by board sample rate (250 Hz Cyton+Daisy → 4 ms sample period;
  trigger placement uses nearest-sample lookup).
- **Honesty (raw#10/91)**: terminal stimulus path is C3-typical (no GPU
  vsync); cross-platform jitter typically 5-15 ms. Pyglet path (deferred)
  with `vsync=True` would give ≤1 ms. Selftest uses synthetic offsets, not
  real timing.

### 1.3 Epoching & analysis

- Per-stimulus epoch: 0-500 ms post-onset (125 samples @ 250 Hz).
- Baseline correction: -100 to 0 ms pre-stimulus (mean-subtract).
- Average epochs per class → standard-ERP and oddball-ERP traces.
- Difference wave: oddball-ERP minus standard-ERP.
- Peak detection: search difference wave for max amplitude in 250-400 ms
  window at Pz (or P3/P4 surrogate average if Pz unavailable on the 16ch
  Cyton+Daisy montage).

## 2. Frozen criteria (raw#12 pre-registered, anchored on file)

| ID | Criterion | Numerical bound |
|---|---|---|
| C1 | Oddball trial count averaged | N >= 20 |
| C2 | Oddball amplitude > Standard amplitude in 250-400 ms window | `peak_oddball_uV > peak_standard_uV` |
| C3 | Parietal max amplitude (Pz / P3 / P4 surrogate) | parietal channel = argmax across montage |
| C4 | P300 latency in window | 250 ms ≤ t_peak ≤ 400 ms |
| C5 (honesty) | Difference-wave peak amplitude is non-trivial | `peak_diff_uV >= 2.0` (subthreshold guard) |

## 3. Falsifiers (raw#71, ≥5)

| ID | Falsifier | Trigger |
|---|---|---|
| F1 | Trial count statistically insufficient | oddball N < 20 |
| F2 | P300 absent | no peak in 250-400 ms window above 2 µV in difference wave |
| F3 | Reversed polarity | oddball amplitude < standard amplitude (subject not attending) |
| F4 | Regional reversal | parietal NOT max — frontal or temporal channel dominates |
| F5 | Subthreshold amplitude | `peak_diff_uV < 2.0` (electrode/contact issue, raw#10 honest C5 falsifier) |

## 4. Implementation

### 4.1 Files

- `anima-eeg/protocols/p300_visual_oddball.hexa` — protocol runner, ~250 LoC,
  `--selftest` only (live ingest deferred).
- `state/p300_visual_audit/<ts>_session.jsonl` — per-session audit ledger
  (one line per session run).
- `/tmp/p300_visual_helper.py` — Python helper for live BrainFlow stream +
  Pyglet stimulus (DEFERRED, not landed in this cycle).

### 4.2 selftest synthetic

- 240 stimuli, 80/20 split → ~48 oddball / ~192 standard.
- Synthetic ERPs:
  - Standard: 1 µV noise at 0 ms, no peak.
  - Oddball: 1 µV noise + 8 µV bell-curve peak centered at 320 ms, FWHM
    100 ms, on Pz channel only.
- Difference wave at Pz: ~7 µV peak around 320 ms.
- Tests assert all 5 frozen criteria met on synthetic (positive) and that
  perturbations trigger the 5 falsifiers (negative tests).

### 4.3 Determinism

- LCG seeded → identical stimulus sequence per `--seed`.
- Synthetic ERP shapes are pure-math (no RNG in epoch synthesis).
- raw#65 idempotent: re-running `--selftest` produces byte-identical
  audit JSONL row (timestamp slot uses fixed `selftest_synth` string in
  selftest mode).

## 5. User-action path (5-10 min real session — DEFERRED)

The following commands are documented for later landing once the Pyglet/
BrainFlow live path is implemented. They are **not** wired in this cycle:

```
# Real 5-min session (deferred — Pyglet stimulus + BrainFlow streaming)
$HEXA_LANG/hexa.real run anima-eeg/protocols/p300_visual_oddball.hexa --live --duration-min 5 --seed 42
```

Available now:

```
# Synthetic selftest (no hardware, no display, deterministic)
$HEXA_LANG/hexa.real run anima-eeg/protocols/p300_visual_oddball.hexa --selftest
```

## 6. References

- Schartner, M. M. et al. (2017). *Global and local complexity of intracranial
  EEG decreases during NREM sleep.* — LZ76 b in 0.5-0.9 awake range.
- Sutton, S. et al. (1965). *Evoked-potential correlates of stimulus
  uncertainty.* — original P300 oddball discovery.
- Polich, J. (2007). *Updating P300: An integrative theory of P3a and P3b.*
  *Clinical Neurophysiology* 118:2128-2148. — 250-400 ms latency window
  reference.
- BrainFlow Cyton+Daisy SDK — sample-rate-aligned trigger insertion.
