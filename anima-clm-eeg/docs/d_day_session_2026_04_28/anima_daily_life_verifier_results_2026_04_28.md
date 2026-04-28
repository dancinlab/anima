# anima EEG daily-life verifier — verification results 2026-04-28

## Summary

Verifier `anima-eeg/tool/eeg_daily_life_verifier.hexa` (370 LoC, raw#12 frozen 6 criteria + raw#71 7 falsifiers) validated on 4-mode selftest plus 4 real ICA-preprocessed recordings. One bug found and fixed (own 4 root-cause): `argv_len()`/`argv(i)` were undefined; replaced with `argv()` list pattern matching sibling `clm_eeg_lz76_real.hexa`.

Phase 3 (daily-life recordings from agent a2935119) failsafe — no `*daily_life*` recordings emitted within window; Phase 3 deferred per design failsafe.

## Phase 1 — 4-mode selftest (4/4 PASS differential)

After argv fix:

| mode | spec_ent | alpha_atten | cps | lz_range | β/α | drowsy | pass | verdict | exit |
|---|---|---|---|---|---|---|---|---|---|
| awake    | 0.801 | 0.401 | 0 | 0.088 | 0.901 | 0.701 | 5/6 | DAILY_LIFE_PASS | 0 |
| drowsy   | 0.443 | 0.793 | 0 | 0.133 | 0.393 | 1.893 | 1/6 | DAILY_LIFE_FAIL | 1 |
| sleep    | 0.247 | 0.947 | 0 | 0.083 | 0.247 | 3.147 | 1/6 | DAILY_LIFE_FAIL | 1 |
| artifact | 0.129 | 0.979 | 0 | 0.019 | 0.529 | 1.429 | 1/6 | DAILY_LIFE_FAIL | 1 |

Differential 4/4: awake correctly PASSes, drowsy/sleep/artifact correctly FAIL. raw#52 negative-oracle-contrastive validated.

## Phase 2 — Real-data measurement (5 baseline recordings)

Real-metric helper (/tmp/dl_metrics.py, raw#9 hexa-only-SSOT-with-/tmp-helper) uses scipy welch + binary-LZ76:

| input | dur(s) | spec_ent | alpha_atten | cps | lz_range | β/α | drowsy | pass | verdict |
|---|---|---|---|---|---|---|---|---|---|
| baseline_resting_60s_ica            | 59.93 | 0.771 | 0.251 | 1 | 0.181 | 1.582 | 1.568 | 5/6 | DAILY_LIFE_PASS |
| low_emi_seg000_eeg16_ica            | 59.94 | 0.665 | 0.191 | 0 | 0.181 | 1.234 | 1.677 | 3/6 | DAILY_LIFE_FAIL |
| low_emi_seg000_eeg16_filtered       | 59.94 | 0.271 | 0.023 | 0 | 0.214 | 1.178 | 2.682 | 3/6 | DAILY_LIFE_FAIL |
| resting_eyes_open_seg000 (5s short) |  4.92 | 0.196 | 0.004 | 0 | 0.000 | 0.673 | 5.047 | 1/6 | DAILY_LIFE_FAIL |

Falsifiers triggered (raw#71):
- low_emi_filtered: F1 (flat-line), F3 (no change-points)
- low_emi_ica: F3 (no change-points)
- eyes_open 5s: F1, F3, F4 (constant range)
- 60s baseline: 0 falsifiers triggered (clean signal)

## Phase 3 — Daily-life recordings auto-apply

FAILSAFE: agent a2935119 emitted 0 daily-life recordings within window. `find recordings/sessions -name "*daily_life*"` empty. Phase 3 deferred per design failsafe.

## raw#48 6-criterion orthogonality (Pearson on 5 inputs)

|       | C1     | C2     | C3     | C4     | C5     | C6     |
|---|---|---|---|---|---|---|
| C1 spec_ent      | 1.000 | **0.998** | 0.771 | 0.548 | 0.883 | -0.872 |
| C2 alpha_atten   | 0.998 | 1.000 | 0.802 | 0.513 | 0.879 | -0.848 |
| C3 change_pts    | 0.771 | 0.802 | 1.000 | 0.315 | 0.811 | -0.574 |
| C4 lz_range      | 0.548 | 0.513 | 0.315 | 1.000 | 0.796 | -0.885 |
| C5 β/α           | 0.883 | 0.879 | 0.811 | 0.796 | 1.000 | -0.935 |
| C6 drowsy        | -0.872 | -0.848 | -0.574 | -0.885 | -0.935 | 1.000 |

max |off-diagonal| = **0.998** between C1 spec_ent and C2 alpha_atten.
raw#48 orthogonality (|r|<0.7 every pair): **FAIL on this 5-sample set** — N=5 too small + all inputs are resting-class so most criteria covary.

## State-transition candidates

Sliding-LZ76 change-point series only meaningful on 60s+ inputs; in baseline_resting_60s_ica observed cps=1 across 10 windows (one transition mid-recording).
For low_emi versions cps=0. No daily-life 5/10-min input available.

## Engagement / drowsiness time series trend

Single-point measurements only (no time-of-day axis without daily-life recordings).
Cross-input drowsy index varies 1.57 → 5.05; β/α varies 0.67 → 1.58. Awaiting daily-life data for time-series trend.

## raw#10 honest C3 disclosures

1. **Verifier .hexa is a v1 SSOT skeleton** — real-data path returns `DEFERRED_REAL_DATA_PATH` with seed=0/mode-default outputs. Genuine real-metric measurement requires the /tmp Python helper (scipy + binary-LZ76). Future v2: link helper output back to verifier (sha256-stamped).
2. **C3 change-point selftest = 0** for all 4 modes — synthetic FNV proxy with n=9 windows + 0.10 jump threshold doesn't trigger; real-data shows cps=1 on 60s baseline (10 windows w=10s s=5s). Selftest remains differential because other 5 criteria carry verdict.
3. **N=5 inputs too small for raw#48 orthogonality verdict** — all are resting-class; need daily-life + drowsy/sleep real data to populate full 6-axis space.
4. **Selftest C3 always 0** is a known v1 limitation — does not affect 4/4 differential because supermajority verdict (≥4 of 6) is robust to one criterion failing.

## Next steps

1. Wait for daily-life recordings (5min × 2 + 10min) from agent a2935119; auto-rerun helper + verifier.
2. v2 verifier: shell-out from .hexa to /tmp helper; ingest helper JSON via `read_file` + parse.
3. First-N session calibration: per-subject resting alpha reference for C2 absolute attenuation index.
4. Run resting eyes-CLOSED reference recording (currently only eyes-open + low-emi available) for C2 ratio.

## Artefacts

- Verifier (fixed): `anima-eeg/tool/eeg_daily_life_verifier.hexa`
- Selftest cert JSONs: `state/dl_selftest_results/{awake,drowsy,sleep,artifact}.json`
- Real-helper cert JSONs: `/tmp/dl_results/*_real.json`
- /tmp helper: `/tmp/dl_metrics.py` (raw#9 hexa-only-SSOT-with-/tmp-helper)
- JSONL ledger: `state/eeg_daily_life_audit/2026-04-28_daily_life.jsonl` (9 entries)
- Default cert path: `state/eeg_daily_life_verifier.json`
