# anima EEG data inventory — 2026-04-28 (D-day)

**audit slug**: `anima_eeg_data_inventory_2026_04_28`
**raws**: 9 (pure-hexa /tmp helper for compute), 10 (real BrainFlow data, no synthetic),
65 (deterministic sha256 manifest), 91 (honest C3 disclosure of duration/dup limitations),
own#4 (single-source-of-truth state/audit/).
**scope**: all `*.npy` ≥100k under `/Users/ghost/core` excluding `.venv`/`site-packages`.

---

## 1. Discovery summary

- Total real-EEG `*.npy` (≥100k): **20 files**
  - 16 in `recordings/sessions/` (3 session families × 4 variants + 4 aliases)
  - 4 in `state/eeg_recordings/` (1 daily-life session × 4 variants)
- All recordings carry **today's timestamp** (2026-04-28). No older / archival sessions found.
- No `.fif` / `.edf` / `.bdf` / EEG-CSV under `/Users/ghost/core` outside scipy/MNE bundled samples.
- All sessions: `board_id=2` (Cyton OpenBCI), `serial_port=/dev/cu.usbserial-DP04WGIQ`,
  `sample_rate=125 Hz`, `tier=PHENOMENAL`, `raw10_honest=real_brainflow_segment`.

### Session families (5 distinct captures)

| family slug | session_ts (UTC) | task | rows × cols | dur (s) | verdict (recorder) |
|---|---|---|---|---|---|
| baseline_resting_60s_20260428 | ~11:29:07Z (filtered ts) | resting_baseline (60 s) | 16 × 7491 | 59.93 | filtered+ICA produced |
| baseline_resting_low_emi | 20260428T113016Z | baseline_resting_low_emi | 32 × 7493 | 62.31 | PASS |
| resting_eyes_open | 20260428T112816Z | resting_eyes_open (5 s) | 32 × 615 | 7.29 | PASS (TOO SHORT) |
| daily_life_5min_1 | 20260428T115006Z | daily_life_5min_1 | 32 × 6252 | 50.02 | (segment, not full 5 min) |
| baseline_resting_post_battery | 20260428T132612Z | baseline_resting_post_battery | 32 × 7490 | 62.29 | PASS |

> **raw#91 honest C3**: filename `daily_life_5min_1` is 50 s, not 300 s — only one segment retained.
> **raw#91 honest C3**: 4 × `session_*FAIL*.json` capture metadata (no .npy) — discarded segments.

---

## 2. Per-file inventory (20 files)

| file (basename) | shape | dtype | dur (s) | sidecar | sha256 (12) | role |
|---|---|---|---|---|---|---|
| baseline_resting_60s_20260428.npy | (16, 7491) | float64 | 59.93 | — | b64010436db5 | RAW 16ch |
| baseline_resting_60s_20260428_filtered.npy | (16, 7491) | float64 | 59.93 | _filtered.json | a1889072b2a1 | filtered |
| baseline_resting_60s_20260428_ica.npy | (16, 7491) | float64 | 59.93 | — | 62b1ad19ae45 | ICA |
| baseline_resting_low_emi_…seg000.npy | (32, 7493) | float32 | 62.31 | .meta.json | 6261ca437f50 | RAW 32ch (full) |
| baseline_resting_low_emi_…seg000_filtered.npy | (32, 7493) | float32 | 62.31 | — | dceff95f595f | filtered 32ch |
| baseline_resting_low_emi_…seg000_eeg16.npy | (16, 7493) | float32 | 62.31 | — | 05f15a75a685 | RAW 16ch slice |
| baseline_resting_low_emi_…seg000_eeg16_filtered.npy | (16, 7493) | float32 | 62.31 | — | bad1b217fa17 | filtered 16ch |
| baseline_resting_low_emi_…seg000_eeg16_ica.npy | (16, 7493) | float64 | 62.31 | — | 83f3672259e3 | ICA 16ch |
| baseline_resting_post_battery_…seg000.npy | (32, 7490) | float32 | 62.29 | .meta.json | 2df59faac3c1 | RAW 32ch |
| baseline_resting_post_battery_…seg000_eeg16.npy | (16, 7490) | float64 | 62.29 | — | c15f577610e4 | RAW 16ch slice |
| baseline_resting_post_battery_…seg000_eeg16_filtered.npy | (16, 7490) | float64 | 62.29 | — | b77fe75e3a74 | filtered 16ch |
| baseline_resting_post_battery_…seg000_eeg16_ica.npy | (16, 7490) | float64 | 62.29 | — | a90b46fde70e | ICA 16ch |
| post_battery_raw_16ch_2026_04_28.npy | (16, 7490) | float64 | 62.29 | — | c15f577610e4 | **dup of …eeg16.npy (alias)** |
| post_battery_filtered_16ch_2026_04_28.npy | (16, 7490) | float64 | 62.29 | — | 216fe5817391 | filtered 16ch (rename) |
| post_battery_ica_16ch_2026_04_28.npy | (16, 7490) | float64 | 62.29 | — | aa06abce5fc6 | ICA 16ch (rename) |
| resting_eyes_open_…seg000.npy | (32, 615) | float32 | 7.29 | .meta.json | aae860f4b02b | RAW 32ch (TOO SHORT) |
| 20260428T115006Z_daily_life_5min_1.npy | (32, 6252) | float64 | 50.02 | .json | 72789c068ff0 | RAW 32ch |
| 20260428T115006Z_daily_life_5min_1_eeg16.npy | (16, 6252) | float64 | 50.02 | (parent .json) | 9fcbfb63e967 | RAW 16ch |
| 20260428T115006Z_daily_life_5min_1_eeg16_filtered.npy | (16, 6252) | float64 | 50.02 | _filtered.json | 6e50a40497bc | filtered 16ch |
| 20260428T115006Z_daily_life_5min_1_eeg16_ica.npy | (16, 6252) | float64 | 50.02 | _ica.json | 3a636347f3d5 | ICA 16ch |

(Full sha256 list at `/tmp/eeg_full_sha.txt` and reproducible via `python3 -c 'import hashlib; …'`.)

### Classification

- **Today (2026-04-28 D-day, real)**: 20/20 = 100 %
- **Older (historical)**: 0/20 = 0 %
- **Synthetic / selftest**: 0 (no synth fixtures in inventory; selftest fixtures live in `/tmp` per raw#9)
- **Duplicate (sha-identical alias)**: 1 (`post_battery_raw_16ch_…` ≡ `…eeg16.npy`)

---

## 3. Analysis-readiness (raw#10 real-only, 16ch, ≥30 s)

A file is **analysis-ready** when shape `(16, N)` AND duration ≥ 30 s AND sample_rate is recorded.

| session family | analysis-ready variants (16ch) | duration | Berger gate eligibility |
|---|---|---|---|
| baseline_resting_60s_20260428 | RAW + filtered + ICA | 59.93 s | resting eyes-closed (assumed) ✅ candidate |
| baseline_resting_low_emi (113016Z) | RAW + filtered + ICA (16ch slice) | 62.31 s | resting eyes-closed ✅ candidate |
| baseline_resting_post_battery (132612Z) | RAW + filtered + ICA (16ch slice) | 62.29 s | resting eyes-closed ✅ candidate |
| daily_life_5min_1 (115006Z) | RAW + filtered + ICA | 50.02 s | eyes-open, motion-rich ✅ daily-life axis |
| resting_eyes_open (112816Z) | (32ch only, 7.29 s) | 7.29 s | ❌ TOO SHORT (5 s req → 60 s for sliding LZ76) |

**Analysis-ready count**: **12 files** (4 sessions × {raw, filtered, ica} 16-ch variants)
plus 3 raw 32-ch (full board) reusable for re-slicing = **15 usable**.

---

## 4. Quick-pass spectral metrics (welch PSD, fs=125 Hz, n_seg=512)

Computed live during this audit (not pre-registered; raw#91 honest disclosure).

| family (ICA where available, raw otherwise) | shape | dur (s) | mean α PSD (8–13 Hz) | β/α ratio (13–30 / 8–13) | spectral H (norm) | Berger gate prediction |
|---|---|---|---|---|---|---|
| baseline_resting_60s_20260428 | (16, 7491) | 59.93 | 7.32e+00 | 0.453 | 0.763 | resting → α should be HIGH; AAI vs ref = 0.28 → **FAIL** as resting-ref but signal looks low-α (eyes-open contamination?) |
| baseline_resting_low_emi (113016Z) | (16, 7493) | 59.94 | 3.45e+00 | 0.365 | 0.660 | low-EMI session has LOWEST α — anomaly worth inspecting (cleaner ICA may have removed eye-blink + α both?) |
| baseline_resting_post_battery (132612Z) | (16, 7490) | 59.92 | **2.63e+01** | 0.385 | 0.635 | **HIGHEST α** in dataset — drives ref_alpha; classic Berger PASS for resting-EC |
| daily_life_5min_115006Z | (16, 6252) | 50.02 | 2.02e+00 | 0.399 | 0.595 | AAI = 0.077 → **PASS** (large alpha attenuation expected for eyes-open daily-life) |
| resting_eyes_open_112816Z | (32, 615) | 4.92 | 5.84e+00 | 0.832 | 0.431 | **TOO_SHORT** — useful as F2-falsifier fixture only |

> ref_alpha (eyes-closed pooled max) = 26.3 — drives AAI denominator.
> raw#91 C3: `low_emi` session has anomalously low α — likely user was open-eyed or
>   filtering chain over-attenuated 8–13 Hz. Re-inspection recommended before LZ76.

---

## 5. LZ76 / γ–θ / spectral-entropy applicability prediction

For each analysis-ready 16-ch ICA file:

| family | LZ76 (Schartner b 0.5–0.9) | γ/θ ratio | spectral H | Berger Δα | verdict |
|---|---|---|---|---|---|
| post_battery (132612Z) ICA | likely b ≥ 0.65 (resting-EC) | low (resting) | 0.63 | n/a self | **PASS — best resting-EC candidate** |
| baseline_60s ICA | likely b ≈ 0.6–0.75 | mid | 0.76 | 0.28 vs ref | passes resting (high H) |
| low_emi ICA | b uncertain; α too low | mid | 0.66 | 0.13 vs ref | **inspect first** — possible eyes-open, label drift |
| daily_life ICA | b ≥ 0.70 expected (eyes-open) | elevated β | 0.60 | 0.08 vs ref | **PASS** for daily-life axis (raw#48 orthogonal) |
| resting_eyes_open | b indeterminate (5 s) | n/a | 0.43 | 0.22 | **TOO_SHORT** for sliding LZ76 |

---

## 6. Recommended batch analysis (today's verifiers)

### Tier-A (run now, high-confidence)
1. **`baseline_resting_post_battery_…_eeg16_ica.npy`** → run
   `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa` (raw#12 frozen resting-EC verifier).
   Predicted: Schartner b ∈ [0.65, 0.85], C1 PASS.
2. **`20260428T115006Z_daily_life_5min_1_eeg16_ica.npy`** → run
   `anima-eeg/tool/eeg_daily_life_verifier.hexa` (6-axis daily-life, raw#48).
   Predicted: ≥4/6 C-criteria PASS (β/α 0.40 mid-range; α attenuation 0.08 deep).
3. **`baseline_resting_60s_20260428_ica.npy`** → secondary resting-EC reference.

### Tier-B (inspection first)
4. **`baseline_resting_low_emi_…_eeg16_ica.npy`** — anomalously low α; verify
   eyes-state before treating as resting-EC.

### Tier-C (longitudinal pattern)
- Time-of-day series (3 resting captures within ~2 h spread:
  60 s / 113016Z / 132612Z) → small but valid α-power & b drift slice.
- post-battery vs pre-battery contrast (132612Z sits "post battery"
  per task slug; baseline_60s + low_emi pre-battery).
- Daily-life (115006Z) inserted between battery → 6-axis engagement
  signature comparison.

### Tier-D (do NOT analyze)
- `resting_eyes_open_…seg000.npy` — only 7.29 s; below all sliding-window
  minimums (raw#91 honest exclusion).

---

## 7. Cross-repo verification

- `/Users/ghost/core/n6-architecture/...`: no real EEG `.npy`; only scipy `levy_stable` test fixtures.
- `/Users/ghost/core/anima/.venv-eeg/...`: MNE bundled fsaverage `*.fif` (head models) and
  scipy validation CSVs — bundled, not user data.
- `/Users/ghost/core/void/...`: spleen-8x16.bdf is a font, not BioSemi EEG.

**Conclusion**: all real EEG data lives under `/Users/ghost/core/anima/`.

---

## 8. Honest C3 disclosures (raw#91)

1. `daily_life_5min_1` is 50 s (one segment), not 5 min (filename misleading).
2. `post_battery_raw_16ch_2026_04_28.npy` is sha-identical to
   `baseline_resting_post_battery_…_eeg16.npy` — counted once for analysis purposes.
3. Eyes-state labels are nominal (filename-derived); only `resting_eyes_open` is
   explicit. Berger AAI numbers are exploratory until labels are independently confirmed.
4. `low_emi` session α-power is anomalously low (~13 % of post-battery ref). Treat
   as INSPECT before downstream stats.
5. ref_alpha used in §4 is pooled max across resting captures (today only). With only
   today's data there is no longitudinal denominator — single-day inference only.
6. selftest / synthetic fixtures are NOT in this inventory by design (raw#9 keeps
   them in `/tmp/`). Production helpers regenerate them deterministically (raw#65).

---

## 9. Reproducibility manifest

- compute env: `/Users/ghost/core/anima/.venv-eeg` (python 3.12, numpy, scipy, mne).
- sha256 source-of-truth: `/tmp/eeg_full_sha.txt` (regenerable from
  `python3 -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' <file>`).
- inventory script: see Bash invocations in this audit's commit (transient, raw#9).
