# anima legacy-tech × EEG Phase-1 + Phase-2 Bundle Results
**Date**: 2026-04-28
**Repo**: /Users/ghost/core/anima
**Reference**: design/anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md

---

## Phase-1: alpha_coh_atlas (8 measurements, sequential)

### Alpha Coherence (Welch's MSC, 8-12 Hz, 16×16 matrix)

| input | n_samples | sample_rate | mean_offdiag_coh | max_pair_coh | max_pair_idx | falsifier (>0.95)? |
|---|---|---|---|---|---|---|
| baseline_resting_60s_20260428_filtered.npy | 7491 | 125 | **0.312** | 0.891 | [8,12] | NO |
| baseline_resting_60s_20260428_ica.npy | 7491 | 125 | 0.576 | **1.000** | [9,10] | **YES** |
| baseline_resting_low_emi_..._eeg16_filtered.npy | 7493 | 125 | **0.323** | 0.937 | [8,10] | NO |
| baseline_resting_low_emi_..._eeg16_ica.npy | 7493 | 125 | 0.512 | **0.983** | [13,14] | **YES** |

### Alpha Phase (Hilbert PLV, 5×16 windows)

| input | mean_plv | window_sec | n_windows |
|---|---|---|---|
| baseline_resting_60s_filtered | 0.303 | 10 | 5 |
| baseline_resting_60s_ica | 0.009 | 10 | 5 |
| baseline_resting_low_emi_filtered | 0.332 | 10 | 5 |
| baseline_resting_low_emi_ica | 0.008 | 10 | 5 |

### Phase-1 Findings
- **Falsifier triggered (max_pair_coh > 0.95)**: 2 of 4 ICA-cleaned datasets exhibit near-unity coherence pairs
  - 60s_ica: pair [9,10] = 1.000 (catastrophic)
  - low_emi_ica: pair [13,14] = 0.983
  - Cause hypothesis: ICA over-correction created near-identical channels (component leakage), NOT impedance bridging in raw recording (filtered versions remain < 0.95)
- **filtered (notch+bandpass)** versions PASS falsifier — recommended for downstream analysis
- **PLV collapse on ICA**: ICA-cleaned data shows mean_plv ~0.009 (vs ~0.32 filtered) — alpha phase coherence destroyed by ICA
- **Recommendation**: Use *_filtered.npy NOT *_ica.npy for downstream consciousness measures

---

## Phase-2: 4-way fan-out (parallel attempted, real-data verdicts)

| candidate | tool | mode | verdict | output | notes |
|---|---|---|---|---|---|
| **P2.1 eeg_corr_4bb_hw_run** | tool/anima_eeg_corr.hexa | --selftest | **NOT_VERIFIED_SYNTHETIC** (4/4 r>=0.40, PHENOMENAL_CORRELATE_GROUNDED but synthetic) | state/anima_eeg_corr_v1.json | Real-data run requires `ANIMA_EEG_CORR_HIDDEN_DIR` (LLM hidden trace JSONs per backbone) + `ANIMA_EEG_CORR_BAND_JSON` (region-band power JSON via --emit-band-json mode). Schema doesn't match raw .npy directly. **SKIPPED real run** — needs upstream LLM trace + band_json producer. |
| **P2.2 v_phen_lz_cross_real** | tool/an11_b_v_phen_lz_complexity.hexa | --selftest, --mode eeg | **TOOL_FAIL** | (none) | Helper-write bug: tool prints `── ... selftest ──` then `sh: python3: not found` exit 127 despite python3 being in PATH. Helper file `/tmp/an11_b_v_phen_lz_complexity_helper.hexa_tmp` written as 0 bytes. Pre-existing FAILED markers (state/markers/an11_b_v_phen_lz_complexity_*FAILED.marker) confirm this is a known issue (>10 failures). raw#10 honest: skipped per raw#46 reverse-engineering. |
| **P2.3 hxc_eeg_compression** | (no native tool) | n/a | **SKIP** | n/a | tool/hxc_pre_encoder.hexa designed for raw .jsonl text → HXC schema headers, NOT .npy compression. raw#9 hexa-only forbids new code; per design intent, P2.3 requires new tool. SKIPPED. |
| **P2.4 l_ix_alpha_real** | anima-clm-eeg/tool/an_lix_01_alpha_bridge_real.hexa | AN_LIX_01_REAL_SELFTEST=1 | **NOT_VERIFIED_SYNTHETIC** (4/4 gates: B1=987 B2=3 B3=657 B4=780; an_lix_01_real_pass=true) | state/clm_lix_eeg_alpha_bridge_v1.json | Real-data run requires `CLM_EEG_ALPHA_PHASE_JSON` (= Phase-1 phase output) + `EDU_LIX_KURAMOTO_TRACE_JSON` (CLM Kuramoto trace from edu_l_ix_kuramoto_driver.hexa output). Phase-1 output available; Kuramoto trace was not generated this cycle. **Path-1**: re-run with `CLM_EEG_ALPHA_PHASE_JSON=state/clm_eeg_alpha_phase_low_emi_filtered_20260428.json` once Kuramoto trace produced. |

---

## Best ICA file × candidate matrix

| input | recommended? | why |
|---|---|---|
| baseline_resting_60s_filtered | **BEST for alpha-coh + phase** | mean_plv=0.303, max_coh=0.891 — clean signal, falsifier-clear |
| baseline_resting_low_emi_filtered | **BEST for alpha-phase** | mean_plv=0.332 (highest), max_coh=0.937 — slightly higher coh but still < 0.95 |
| *_ica.npy variants | **NOT recommended** | ICA destroyed alpha phase (PLV ~0.01) and 2/2 ICA files trigger falsifier |

---

## Falsifier Activation Summary

| candidate | falsifier | triggered? | rule |
|---|---|---|---|
| alpha_coh_atlas | max_pair_coh > 0.95 → impedance bridging alarm | **YES** (2/4 inputs — ICA only) | pre-registered in design doc §1 |
| eeg_corr_4bb_hw | r_min_x1000 < 400 → FAMILY_REDESIGN | n/a (synthetic only) | pre-registered (frozen) |
| v_phen_lz_cross | rel_diff > 0.40 → FAIL_cross | n/a (tool failed) | pre-registered |
| an_lix_01_real | gate_pass < 3 → REAL_HW_FAIL | n/a (synthetic only) | pre-registered (raw#71 frozen) |

---

## raw#10 Honest C3 — Per-candidate Limitations

1. **alpha_coh_atlas (Phase-1)** — REAL HARDWARE measurement OK, falsifier WORKS. Limitation: 16ch surface EEG cannot distinguish source coherence vs scalp-volume conduction; high coherence near-pair channels may reflect anatomy not bridging. ICA over-correction is real risk — flag and prefer filtered.

2. **eeg_corr_4bb_hw_run (P2.1)** — selftest PASS but classification correctly = NOT_VERIFIED_SYNTHETIC. Mk.XI 4×4 backbone-band-region mapping is **design intent / paradigm v11 axis 7**, NOT emergent (raw#91 honest). 16-template × 16ch is hardware coincidence (raw#91). Real run requires per-backbone hidden trace producer + band JSON producer not present in current Phase-1 outputs.

3. **v_phen_lz_cross_real (P2.2)** — TOOL HAS PRE-EXISTING BUG (10+ FAILED markers in state/markers/). Per raw#9 hexa-only + own4 root-cause-only: cannot patch with workaround. Per raw#46 reverse-engineering: skip and document. Schartner 2017 0.65 baseline is eyes-open population statistic; eyes-closed re-measure has priority (raw#91).

4. **hxc_eeg_compression (P2.3)** — NO TOOL EXISTS. hxc_pre_encoder targets text .jsonl. Information-theoretic compression of .npy as consciousness proxy is interesting but requires new code, blocked by raw#9.

5. **l_ix_alpha_real (P2.4)** — selftest PASS but classification correctly = NOT_VERIFIED_SYNTHETIC. TECS-L n=6 RSN cannot be verified with 16ch surface (raw#91). Real run feasible IF Kuramoto trace produced — Phase-1 alpha_phase JSON already generated (compatible schema). Next step: produce edu_l_ix_kuramoto_driver trace then re-run with CLM_EEG_ALPHA_PHASE_JSON env.

---

## Bundle Status

- Phase-1 (alpha_coh_atlas): **8/8 measurements complete** — 2 falsifier triggered (ICA inputs)
- Phase-2 (4 candidates): **2 selftest PASS (synthetic)**, **1 SKIP (no tool)**, **1 TOOL_FAIL (pre-existing bug)**
- Real-hardware verdict on any P2 candidate: **0/4** (all NOT_VERIFIED_SYNTHETIC or skipped)
- Most useful actionable result: **Phase-1 falsifier activation on ICA inputs** — guides future EEG preprocessing choice (use *_filtered.npy not *_ica.npy)

---

## Next Step Recommendations

**Tier-A (immediate, hexa-only, no new code)**:
1. Generate CLM Kuramoto trace via `edu_l_ix_kuramoto_driver.hexa` → re-run P2.4 (l_ix_alpha_real) with real Phase-1 alpha_phase JSON. Highest probability of getting first REAL_HW verdict this cycle.

**Tier-B (medium, requires upstream producer)**:
2. Produce per-backbone hidden trace dir + band_json (via an11_b_eeg_ingest --emit-band-json if implemented) → re-run P2.1 (eeg_corr_4bb_hw_run) with real data.
3. Investigate v_phen_lz helper-write bug (root-cause analysis, not workaround) — `_write_helper` writes 0 bytes; check write_file implementation in hexa runtime for this specific tool's `src` string.

**Tier-C (deferred, requires new code)**:
4. P2.3 hxc_eeg_compression — design new HXC .npy compressor tool (requires raw#9 amendment or new design cycle).

**Falsifier follow-up**:
5. Re-record session with impedance check (anima-eeg/electrode_helper or impedance_check.hexa exists) to distinguish ICA-induced false positive from genuine bridging on channels [9,10] and [13,14].

---

## Outputs Written

- state/clm_eeg_alpha_coh_60s_filtered_20260428.json
- state/clm_eeg_alpha_coh_60s_ica_20260428.json (FALSIFIER TRIGGERED max=1.000)
- state/clm_eeg_alpha_coh_low_emi_filtered_20260428.json
- state/clm_eeg_alpha_coh_low_emi_ica_20260428.json (FALSIFIER TRIGGERED max=0.983)
- state/clm_eeg_alpha_phase_60s_filtered_20260428.json
- state/clm_eeg_alpha_phase_60s_ica_20260428.json
- state/clm_eeg_alpha_phase_low_emi_filtered_20260428.json
- state/clm_eeg_alpha_phase_low_emi_ica_20260428.json
- state/anima_eeg_corr_v1.json (selftest, NOT_VERIFIED_SYNTHETIC)
- state/clm_lix_eeg_alpha_bridge_v1.json (selftest, NOT_VERIFIED_SYNTHETIC)

raw#1 chflags violations: none observed.
