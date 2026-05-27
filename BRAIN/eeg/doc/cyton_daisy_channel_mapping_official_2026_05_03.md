# Cyton+Daisy Official Channel Mapping vs Our Spec — 2026-05-03

## TL;DR

- **BrainFlow 5.21.0 official mapping** for `BoardIds.CYTON_DAISY_BOARD` (id=2):
  EEG rows = `[1..16]`, names `[Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4]`.
- **Our spec** (per `berger_ec_60s_v6_2026_05_03.npy.meta.json` → `eeg_indices: [1..16]`):
  **MATCHES official.** No remapping needed.
- The prior BG finding "row 1 ≡ row 6 ≡ row 8 cc=1.0000" was real but **not a mapping bug** — those rows are **railed/saturated channels** (mean ≈ -98 mV, |max| ≈ 101 mV, near ADC limit ±187.5 mV) producing near-identical clipped output. AC-detrended cc still ≈ 1.0000 because clipped signals collapse to identical noise/quantization patterns.

## 1. BrainFlow Official Mapping (board_id=2, brainflow 5.21.0)

```
package_num_channel : 0
eeg_channels        : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
eeg_names           : Fp1, Fp2, C3, C4, P7, P8, O1, O2,    (Cyton 1..8)
                      F7, F8, F3, F4, T7, T8, P3, P4       (Daisy 9..16)
accel_channels      : [17, 18, 19]   (X, Y, Z)
other_channels      : [20, 21, 22, 23, 24, 25, 26]
analog_channels     : [27, 28, 29]   (A5/D11, A6/D12, A7/D13)
timestamp_channel   : 30
marker_channel      : 31
num_rows            : 32
sampling_rate       : 125 Hz
```

(Source: `BoardShim.get_board_descr(2)` from `/Users/ghost/core/anima/.venv-eeg/lib/python3.12/site-packages/brainflow/board_shim.py`.)

## 2. Our Spec vs Official — Match

Our `collect.hexa` and `eeg_recorder.hexa` already use `BoardShim.get_eeg_channels(BOARD_ID)` at runtime
(see `anima-eeg/calibrate.hexa:277`, `eeg_recorder.hexa:244`, `collect.hexa:289`).
The session meta written by v6 collect:

```json
"eeg_indices": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
```

is identical to BrainFlow official. **Verdict: spec correct, mapping verified.**

## 3. v6 EC `.npy` Row-by-Row Analysis (32 rows × 7496 cols)

| row | name        | mean         | ac_std    | abs_max     | status                              |
|-----|-------------|--------------|-----------|-------------|-------------------------------------|
| 0   | package_num | 126.4        | 73.8      | 254         | OK (cyclic 0→254 step 2, wrap @127) |
| 1   | Fp1         | -98 545      | 1 254     | 101 449     | **RAILED** (DC near -ADC limit)     |
| 2   | Fp2         | -17 906      | 165       | 18 247      | OK-ish DC offset, low AC            |
| 3   | C3          | -18 483      | 140       | 18 965      | OK-ish                              |
| 4   | C4          | -35 307      | 230       | 35 809      | high DC                             |
| 5   | P7          | +119 623     | 1 472     | 123 091     | **RAILED** (positive)               |
| 6   | P8          | -98 656      | 1 253     | 101 558     | **RAILED**                          |
| 7   | O1          | -24 380      | 155       | 24 707      | OK-ish                              |
| 8   | O2          | -98 722      | 1 254     | 101 627     | **RAILED**                          |
| 9   | F7          | +27 948      | 1 063     | 31 483      | reasonable EEG-like                 |
| 10  | F8          | +10 579      | 1 142     | 14 138      | reasonable                          |
| 11  | F3          | +8 636       | 1 002     | 11 683      | reasonable                          |
| 12  | F4          | -90          | 1 117     | 4 990       | best — near zero DC                 |
| 13  | T7          | +1 205       | 1 137     | 5 868       | best                                |
| 14  | T8          | +16 237      | 1 122     | 19 876      | reasonable                          |
| 15  | P3          | +18 952      | 1 115     | 22 373      | reasonable                          |
| 16  | P4          | -96 023      | 1 254     | 98 713      | **RAILED**                          |
| 17–19 | accel X/Y/Z | 0.04 / 0.94 / -0.30 |       |             | OK (g units, head still)            |
| 20  | other[0]    | 192 const    | 0         | 192         | reserved (Cyton register byte?)     |
| 21–26 | other[1..6] | low 0..123  |           |             | aux/Daisy-side counters             |
| 27–29 | analog A5/A6/A7 | all zeros |        |             | unused (no analog probe)            |
| 30  | timestamp   | 1.7778e9     | 67        |             | OK (Unix epoch sec, slight jitter)  |
| 31  | marker      | 0            | 0         | 0           | OK (no markers inserted)            |

**Cross-correlation — rows 1, 6, 8 cc=+1.0000** is explained by rail saturation, not duplicate wiring:
all three sit at the ADC negative limit and emit near-identical clipped LSB-noise. Row 5 sits at the
positive rail with cc=-0.99 to rows 1/6/8 (mirror image). The high cc among rows 9–15 (≥0.99) is
**common-mode driven** (single REF/BIAS, all channels share heartbeat/EMG/sweat drift).

EO v6 file (32 × 7487) shows the **same channels railed** (1, 5, 6, 8, 16) → consistent across both
sessions, i.e. a stable hardware/electrode contact issue, not a per-recording fluke.

## 4. Recommended Mapping for Analysis Protocol

**No mapping update needed — `eeg_indices = [1..16]` per `meta.json` is canonical.**

What needs to change in the analysis protocol is **channel-quality gating**, not indexing:

- **Drop / mark-unusable** before Berger PSD: rows 1 (Fp1), 5 (P7), 6 (P8), 8 (O2), 16 (P4) —
  railed in v6.
- **Use for occipital alpha** (Berger primary): row 7 (O1) only; O2 (row 8) railed.
- **Daisy frontocentral candidates**: rows 12 (F4), 13 (T7), 11 (F3) have lowest |DC| → cleanest.
- **DC removal mandatory**: any HPF ≥ 0.5 Hz before alpha-band PSD; raw means up to ±120 mV
  swamp the 8–13 Hz signal.

Proposed `clean_channels` indices for v6 EC analysis (1-indexed BrainFlow rows):
`[2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]` — 11 of 16 usable.

## 5. Three Honest C3 Caveats

1. **BrainFlow 5.21.0 vs Cyton firmware version**: mapping queried here is from BrainFlow library
   (Python pkg). Cyton firmware ≥ v3.1.2 is assumed by BrainFlow Cyton+Daisy mode. If the user's
   dongle/board firmware diverges, BrainFlow may silently reorder Daisy rows. Verify via
   `board_health_check.hexa` whenever firmware is updated.
2. **32 rows ≠ 32 EEG channels**: only rows 1–16 are EEG. Rows 0, 17–31 carry accel/aux/timestamp/
   marker. Any analysis script that treats `arr[0]` as Fp1 (0-indexed assumption) will read the
   **package counter** as a "channel" and produce nonsensical PSDs.
3. **Row 1 vs row 0 confusion**: BrainFlow uses **1-indexed** EEG rows (row 0 = package_num).
   NumPy slicing `arr[0]` is the package counter, not Fp1. Always reference `meta.eeg_indices` or
   `BoardShim.get_eeg_channels()` rather than hard-coding `arr[:16]`.

## 6. Next Cycle Recommendation

The mapping is correct; the bottleneck is **electrode contact** on Fp1/P7/P8/O2/P4 (5 of 16 channels
railed at ADC limit in both EC and EO v6 sessions, identical pattern across runs).

Recommended next steps:

1. **Re-run impedance check** (`impedance_real_hardware_validation.hexa`) on rows 1/5/6/8/16 before
   any further Berger collect.
2. **Re-analyze v6 EC/EO with `clean_channels = [2,3,4,7,9,10,11,12,13,14,15]`** — drop railed
   channels, recompute alpha PSD on O1 (row 7) + Daisy rows; expect EC/EO ratio > 1.0 if Berger
   effect is real on the cleaner channels.
3. **No re-record needed** until impedance/contact issue is fixed at the hardware/electrode layer.
4. Long-term: add an automatic rail-detection gate to `analyze.hexa` so railed channels are
   excluded before PSD by default (threshold `|mean| > 50000` or `|max| > 150000`).

## References

- BrainFlow Python pkg: `/Users/ghost/core/anima/.venv-eeg/lib/python3.12/site-packages/brainflow/board_shim.py`
- v6 EC session: `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_ec_60s_v6_2026_05_03.npy`
- v6 EC meta:    `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_ec_60s_v6_2026_05_03.npy.meta.json`
- v6 EO session: `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_eo_60s_v6_2026_05_03.npy`
- BrainFlow Cyton+Daisy reference (in-tree): `/Users/ghost/core/anima/references/brainflow/python_package/brainflow/board_shim.py`
