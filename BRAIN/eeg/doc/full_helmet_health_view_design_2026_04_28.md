# Full-Helmet Health View — Design Doc

**Date**: 2026-04-28
**Owner**: anima-eeg / electrode_adjustment_helper
**Status**: DESIGN (no code yet)
**Supersedes**: per-touch single-channel display in `electrode_adjustment_helper.hexa --live`

---

## 1. Problem

Current helper shows ONE active touch at a time. Operator donning a 16-channel helmet with 2 ear clips (SRB2 reference + BIAS driven-ground) cannot see total helmet health — they walk channel-by-channel, blind to neighbours degrading. Goal: single-screen status of all 18 elements simultaneously.

## 2. Element Inventory (18 total)

- 16 EEG: Fp1 Fp2 F7 F3 Fz F4 F8 T7 C3 Cz C4 T8 P7 P3 Pz P4 P8 O1 O2 — (subset to 16; final list in `config/montage_16ch.json`)
- 2 ear clips: **SRB2** (reference, A1) + **BIAS** (driven-ground, A2)

## 3. State Vocabulary (5 states)

| Symbol | Color | Name      | Meaning                                                    |
|--------|-------|-----------|------------------------------------------------------------|
| `✓`    | GREEN | OK        | connected + RMS in 5–50 µV + mains < 30% of band power     |
| `⚠`    | YELLOW| MARGINAL  | connected but RMS out-of-band OR mains 30–60% OR low corr  |
| `✗`    | RED   | BAD       | railed (|sample| > 90% ADC FS) OR floating (RMS < 0.5 µV)  |
| `·`    | GRAY  | UNKNOWN   | < 1.0 s of samples accumulated (warmup) or stale > 3 s     |
| `🔄`   | BLUE  | MEASURING | active impedance/calibration sweep on this electrode       |

## 4. Per-Element Classification

```
inputs (per electrode, rolling 1.0 s window @ 250 Hz = 250 samples):
  rms_uV         = sqrt(mean(x^2))            after 1–40 Hz bandpass
  mains_ratio    = bandpower(58–62) / bandpower(1–40)
  rail_frac      = fraction(|x_raw| > 0.9 * ADC_FS)
  corr_to_median = pearson(x, median_across_active_channels)
  age_ms         = now - last_sample_ts
```

Decision tree (evaluated each classification tick):
```
if age_ms > 3000 or sample_count < 250:    UNKNOWN (gray)
elif measuring_flag[ch]:                    MEASURING (blue)
elif rail_frac > 0.05:                      BAD (rail)
elif rms_uV < 0.5:                          BAD (floating)
elif rms_uV > 200:                          BAD (saturated)
elif mains_ratio > 0.60:                    BAD (mains-dominated)
elif rms_uV < 5 or rms_uV > 50:             MARGINAL (out-of-band)
elif mains_ratio > 0.30:                    MARGINAL (mains creeping)
elif abs(corr_to_median) < 0.10:            MARGINAL (uncorrelated → loose ref?)
else:                                        OK
```

### SRB2 (reference) inference
SRB2 has no own channel — health inferred from **median pairwise correlation** across all 16 EEG channels. Healthy SRB2 → all channels share common-mode → median |r| ≥ 0.4 in 1–40 Hz band. If median |r| < 0.15, SRB2 is BAD (likely lifted). Between → MARGINAL.

### BIAS (driven-ground) inference
BIAS health inferred from **mains rejection effectiveness**: median `mains_ratio` across 16 EEG. Healthy BIAS → median `mains_ratio` < 0.10. > 0.40 → BAD. Between → MARGINAL.

## 5. State Transitions

| From → To       | Trigger                                                                    | Hysteresis            |
|-----------------|----------------------------------------------------------------------------|-----------------------|
| UNKNOWN → OK    | classification passes OK criteria for ≥ 1 consecutive tick                 | none (warmup only)    |
| OK → MARGINAL   | any MARGINAL criterion holds for 2 consecutive ticks (≥ 2 s)               | 2-tick debounce       |
| MARGINAL → OK   | OK criteria hold for 3 consecutive ticks (≥ 3 s)                           | 3-tick debounce       |
| OK/MARGINAL → BAD | any BAD criterion holds for 1 tick (instant — operator must know)        | none (fail-fast)      |
| BAD → MARGINAL  | BAD criteria clear AND MARGINAL holds for 3 ticks                          | 3-tick debounce       |
| any → MEASURING | impedance sweep flag raised by helper                                      | latched until cleared |
| any → UNKNOWN   | `age_ms > 3000`                                                            | none                  |

Hysteresis prevents flicker on borderline electrodes (typical for forehead Fp1/Fp2 during eye blinks).

## 6. Screen Mockup (80×30)

```
+------------------------------------------------------------------------------+
| anima-eeg full-helmet health   tick=00:01:23  fps=60  link=OK   class=1.2s   |
+------------------------------------------------------------------------------+
|                                                                              |
|                          .---------------------.                             |
|                         /     Fp1 ✓   Fp2 ✓     \                            |
|                        /   F7 ⚠ F3 ✓ Fz ✓ F4 ✓ F8 ✗ \                        |
|     SRB2 (ref)        |                              |       BIAS (gnd)     |
|     [ ✓ OK ]          |  T7 ✓ C3 ✓ Cz 🔄 C4 ✓ T8 ✓   |       [ ✓ OK ]       |
|     med|r|=0.52       |                              |       mains=0.07     |
|                        \  P7 ✓ P3 ✓ Pz ✓ P4 ✓ P8 ⚠ /                         |
|                         \      O1 ✓     O2 ✓      /                          |
|                          '---------------------'                             |
|                                                                              |
|   Touched: Cz (2.1s)   ░░▓▓██  (animated, blink 2 Hz)                        |
|                                                                              |
+------------------------------------------------------------------------------+
| 13 ✓ OK    2 ⚠ MARGINAL    1 ✗ BAD    1 🔄 MEAS    0 · UNKNOWN               |
| Worst: F8 ✗ BAD  hint: "press F8 firmly, add gel; check cable for break"    |
+------------------------------------------------------------------------------+
```

Colors via ANSI 256: GREEN=`\e[92m`, YELLOW=`\e[93m`, RED=`\e[91m`, GRAY=`\e[90m`, BLUE=`\e[94m`. Touched-channel overlay reverse-video + 2 Hz blink.

## 7. Update Cadence

- **Render tick**: 60 fps (16.7 ms) — redraws layout + animation only.
- **RMS / mains / rail computation**: 10 Hz (every 100 ms) — slides 1.0 s window.
- **Classification**: 1 Hz (every 1.0 s) — applies decision tree + hysteresis. Independent of render.
- **SRB2/BIAS aggregate**: 0.5 Hz (every 2.0 s) — needs longer window for stable correlation.

Render reads last classification result (lock-free atomic snapshot). No skipped frames if classifier slow.

## 8. Touch-Detection Overlay

Existing `--live` touch detection retained as **overlay layer** above health view. Touched electrode:
- Symbol replaced with reverse-video block, blinking at 2 Hz.
- Footer line shows `Touched: <name> (<duration>s)`.
- Health classification continues underneath; on touch release, health symbol re-emerges.

Multi-touch (recent improvement) preserved: all touched electrodes blink concurrently.

## 9. Falsifier (raw #71)

**This design is invalidated if**: on a real 16-ch helmet with 2 ear clips, the 5-state classification disagrees with operator ground-truth assessment on > 30% of electrodes during a 60-s donning session, OR the 1 Hz classification cadence causes operator to wait > 5 s for state convergence after a known-good adjustment.

Concrete test:
1. Don helmet, deliberately leave 3 electrodes loose.
2. Run health view for 60 s.
3. Operator records true status of each electrode independently.
4. Compare: agreement must be ≥ 70% (≥ 13/18 correct).
5. Time-to-converge after fixing a loose electrode: median ≤ 5 s.

Failure → revisit thresholds (Section 4) or window length (Section 7).

## 10. Cost Estimate

| Item                                    | Effort       |
|-----------------------------------------|--------------|
| Classifier module (decision tree + hysteresis) | 1 day        |
| SRB2/BIAS aggregate inference           | 0.5 day      |
| ASCII layout renderer (60 fps)          | 1 day        |
| Touch overlay integration               | 0.5 day      |
| Falsifier test harness + 60 s session   | 0.5 day      |
| **Total**                               | **3.5 days** |

CPU: ~5% of one core @ 250 Hz × 16 channels (RMS + FFT @ 10 Hz). Memory: < 5 MB rolling buffers.

## 11. Out-of-Scope (Future)

- Per-electrode impedance Ω readout (needs hardware sweep mode).
- Saving health-history timeline for post-hoc review.
- Audio cues (TTS "F8 disconnected").
- Web dashboard mirror.

## 12. References

- Current helper: `anima-eeg/electrode_adjustment_helper.hexa`
- Live wrapper: `/tmp/anima_eeg_electrode_adjustment_helper.py --live`
- Montage: `anima-eeg/config/montage_16ch.json`
- BrainFlow sanity: `anima-eeg/eeg_brainflow_sanity.hexa`
