# Berger gate batch sweep — 2026-04-28 (D-day Tier-A #3)

**audit slug**: `berger_batch_sweep_2026_04_28`
**gate**: `anima-eeg-core/tool/modules/_gates/berger_alpha.hexa` (commit 50c519aab)
**raws**: 9 (transient .py helper) · 10 (real BrainFlow) · 12 (frozen criteria) · 65 · 71 (eyes-open falsifier) · 82 · 91 honest · own5 no-cap
**criteria (raw#12 frozen)**: C1 α>β · C2 α>0.30·δ · C3 peak∈[7,14]Hz on both O1+O2 → PASS

## 1. Per-file results (15 rows)

| # | family | eyes | variant | ch | verdict | O1 peak Hz | O2 peak Hz | O1 c1c2c3 | O2 c1c2c3 | mean α/β x1000 | mean α/δ x1000 | dom score | predicted | match |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | baseline_resting_60s | ec_resting | raw | 16 | FAIL | 1.7 | 1.7 | 0 | 0 | 538.0 | 72.5 | 305 | FAIL_lowα | ✓ |
| 2 | baseline_resting_60s | ec_resting | filtered | 16 | FAIL | 1.7 | 1.2 | 0 | 0 | 539.0 | 66.0 | 302 | FAIL_lowα | ✓ |
| 3 | baseline_resting_60s | ec_resting | ica | 16 | FAIL | 1.7 | 1.7 | 0 | 0 | 555.5 | 111.5 | 334 | FAIL_lowα | ✓ |
| 4 | baseline_resting_low_emi | ec_resting | raw16 | 16 | FAIL | 1.7 | 1.7 | 0 | 0 | 539.0 | 69.0 | 304 | FAIL_lowα | ✓ |
| 5 | baseline_resting_low_emi | ec_resting | filtered16 | 16 | FAIL | 1.7 | 1.7 | 0 | 0 | 540.0 | 66.0 | 303 | FAIL_lowα | ✓ |
| 6 | baseline_resting_low_emi | ec_resting | ica16 | 16 | FAIL | 1.5 | 1.7 | 0 | 0 | 499.5 | 57.5 | 278 | FAIL_lowα | ✓ |
| 7 | baseline_resting_low_emi | ec_resting | raw32 | 32 | FAIL | 1.7 | 1.7 | 0 | 0 | 539.0 | 69.0 | 304 | FAIL_lowα | ✓ |
| 8 | baseline_resting_post_battery | ec_resting | raw16 | 16 | FAIL | 1.2 | 1.2 | 100 | 100 | 1088.5 | 58.0 | 573 | PASS_high α | ✗ |
| 9 | baseline_resting_post_battery | ec_resting | filtered16 | 16 | FAIL | 1.2 | 1.2 | 100 | 100 | 1088.0 | 54.5 | 571 | PASS_high α | ✗ |
| 10 | baseline_resting_post_battery | ec_resting | ica16 | 16 | FAIL | 1.5 | 1.5 | 0 | 0 | 645.0 | 123.5 | 384 | PASS_high α | ✗ |
| 11 | baseline_resting_post_battery | ec_resting | raw32 | 32 | FAIL | 1.2 | 1.2 | 100 | 100 | 1088.5 | 58.0 | 573 | PASS_high α | ✗ |
| 12 | daily_life_5min_1 | eo_active | raw32 | 32 | FAIL | 1.2 | 1.5 | 0 | 0 | 524.5 | 78.0 | 301 | FAIL_eo | ✓ |
| 13 | daily_life_5min_1 | eo_active | raw16 | 16 | FAIL | 1.2 | 1.5 | 0 | 0 | 524.5 | 78.0 | 301 | FAIL_eo | ✓ |
| 14 | daily_life_5min_1 | eo_active | filtered16 | 16 | FAIL | 1.2 | 1.5 | 0 | 0 | 525.5 | 77.5 | 302 | FAIL_eo | ✓ |
| 15 | daily_life_5min_1 | eo_active | ica16 | 16 | FAIL | 1.5 | 1.2 | 0 | 0 | 563.0 | 33.0 | 298 | FAIL_eo | ✓ |

## 2. Predicted-vs-actual confusion matrix

| | actual PASS | actual PARTIAL | actual FAIL |
|---|---|---|---|
| **predicted PASS** | 0 | 0 | 4 |
| **predicted FAIL** | 0 | 0 | 11 |

## 3. Falsifier (raw#71)

- Eyes-open daily_life PASSing Berger (false positive count): **0**
- Expected: 0 (eyes-open should NOT pass occipital alpha gate)

## 4. Best / worst α dominance

- **Best α/β**: baseline_resting_post_battery/raw16 (mean α/β x1000 = 1088.5)
- **Worst α/β**: baseline_resting_low_emi/ica16 (mean α/β x1000 = 499.5)

## 5. Honest C3 disclosures (raw#91)

1. Inventory predicted 2 PASS (post_battery ICA + daily_life ICA on AAI basis) but Berger gate is occipital-O1/O2-α dominance, not AAI. Predictions stated `α=26.3` for post_battery → highest α power, but α/β and α/δ ratios are what gate measures.
2. Channel ordering: O1=idx 6, O2=idx 7 per gate convention; if BrainFlow board layout (board_id=2 Cyton) maps differently, occipital identity is nominal.
3. fs=125 Hz, nperseg=512 → ~0.244 Hz bin resolution; peaks <7 Hz inflate δ band and force C2 fail even with real α.
4. raw#10 honest: all 15 files are real BrainFlow segments; no synthetic data used.
