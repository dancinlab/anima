# BG-CAP-VS-TRAINING-RATIO-AUDIT — spec

**Cycle**: 2026-05-10 | **Lane**: anima mitosis V14 polarity mechanism quantification | **Mode**: $0 local additive analysis (raw#15)

## Mission

Quantify the candidate multi-factorial mechanism that combines:
- §45 cap-conditional polarity (cap-vs-training-saturation ratio)
- §50 engine_a refined cotrain dynamics
- §51 trained-correlation slower-dispersion at high cap

Specifically: is `ratio = inference_cap / training_observed_max_cells` the **single best predictor** of V14 polarity, or is multi-factor required?

## Inputs (existing data, NO re-fire)

9 data points pulled from already-completed BG state directories (raw#15 additive):

- §38 BG-V14-STRICT-RESOLUTION (substrate A, 10-seed)
- §47 BG-V14-MULTI-SUBSTRATE-AUDIT (B, C, D, E at max=128, 5-seed each)
- §51 BG-V14-MAX256-CAP-FREE-MULTI (A, C, E at max=256, 2-5-seed)
- §37 reborn record (substrate C cells64 trained at max=64, inference at max=64 → V14_VIOLATED 0/5)

Source files:
- `/Users/ghost/core/anima/state/anima_v14_strict_resolution_2026_05_10/result_10seed.json`
- `/Users/ghost/core/anima/state/anima_v14_multi_substrate_audit_2026_05_10/per_substrate_v14_results.json`
- `/Users/ghost/core/anima/state/anima_v14_max256_cap_free_multi_2026_05_10/per_substrate_max256_results.json`

## Encoding

| variable | values | notes |
|---|---|---|
| verdict_score | PASS=+1, AMBIGUOUS=0, VIOLATED=-1 | ordinal target |
| ratio | inference_cap / training_observed_max_cells | ∞ rows substituted with training_observed_max=1 (worst case) |
| chat_cotrain | binary | A=1 (Phase 2 cotrain has chat-head loss); B/C/D/E=0 |
| mitosis_aware | binary | C=1, D=1; A/B/E=0 |
| inference_cap | continuous | 64, 128, 256 |
| params_M | continuous | A/B=298.8, C/D/E=18.5 |
| is_engine_ag | binary | A/B=1; C/D/E=0 |

## Methods

1. Univariate: Spearman + Kendall on ratio vs verdict_score; also on inference_cap alone
2. Threshold scan on ratio (t ∈ {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0, 50.0, 100.0})
3. Multinomial logistic regression on standardized features (3 classes)
4. Decision tree max_depth ∈ {1, 2, 3} with feature importance + rule export
5. Within-substrate cap-polarity flip analysis
6. Subset analysis: finite-ratio only (drop ∞ rows)

## Falsifiers

- F-RATIO-1: |Spearman(ratio, verdict)| < 0.5 → ratio insufficient as single predictor
- F-RATIO-2: ∞-ratio rows split across PASS and VIOLATED → ratio doesn't drive verdict
- F-RATIO-3: n=9 underpowered → no statistical decision possible

## Output artifacts

- `data_table.json` — 9-row precision table with all encoded features
- `regression_result.json` — full numeric output (correlations, LR coefs, DT rules, threshold scan)
- `verdict.md` — final mechanism verdict + honest C3
- `run_regression.py` — analysis script (committed to state, raw#9 NOT applicable since no model training)

## Constraints honored

- raw#15: existing data only, no model re-fire
- : $0 local CPU only
- : REBORN.md NOT directly appended; dispatcher injects §59 slot
- : doc save to state/anima_cap_vs_training_ratio_audit_2026_05_10/
