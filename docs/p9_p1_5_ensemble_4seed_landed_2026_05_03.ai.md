# P9 P1.5 4-Seed Ensemble — Holdout-500 cv Verdict (2026-05-03)

## TL;DR

P1.5 ensemble (s42/s43/s44/s45) on holdout-500 BLEU/ROUGE/chrF: **mechanical
cv<0.30 says PHASE_1_5_REAL_LIFT, but reality says BOTH_NOISE_FLOOR**.

P1.5 4-seed mean BLEU-1 = **0.00556** = **1.45% of Llama anchor (0.382)**, and
**BELOW ablation_A baseline (0.00651)**. Low cv just measures the consistency
of garbage at the noise floor.

## 4-Seed cv Stats

| metric  | mean    | std     | cv     |
|---------|---------|---------|--------|
| BLEU-1  | 0.00556 | 0.00020 | 0.0361 |
| ROUGE-L | 0.00553 | 0.00019 | 0.0345 |
| chrF    | 0.02065 | 0.00351 | 0.1697 |

Per seed BLEU-1: s42=0.00564, s43=0.00526, s44=0.00570, s45=0.00564.

## B Ensemble Comparison (s42/s43/s44/s45)

| metric  | mean    | std     | cv     |
|---------|---------|---------|--------|
| BLEU-1  | 0.00811 | 0.00262 | 0.3235 |
| ROUGE-L | 0.00796 | 0.00257 | 0.3227 |
| chrF    | 0.02631 | 0.00524 | 0.1993 |

s42=0.0120 outlier; s43/44/45 = 0.0068/0.0062/0.0075. **Without s42, B mean =
0.00683 ≈ A (0.00651)** → confirms s42 was seed luck.

## Ranked Ensemble Means (BLEU-1)

1. ablation_B_ensemble: 0.00811 (2.12% Llama) — skewed by s42
2. ablation_A_single:   0.00651 (1.70%)
3. **phase1_5_ensemble: 0.00558 (1.45%) — BELOW A**
4. llama_anchor:        0.38216 (100%)

## Implications

- **A-prime switch (qualitative gates) re-confirmed.**
- BLEU/ROUGE benchmark cannot resolve real lift at 350M+50k scale.
- "B = seed luck" claim **CONFIRMED**.
- "P1.5 = real lift" claim **REFUTED** (4-seed mean below A baseline).
- Future P1+ work: drop BLEU/ROUGE as primary; rely on qualitative gates.

## Substrate / Cost

- Compute: ubu1 RTX 5070 (one s45 retry, ~4min, $0).
- All other 3 seeds (s42/s43/s44) had v2 per_prompt already.
- Compute_ensemble.py runs locally on Mac (~50ms).

## Artifacts

- `state/p9_p1_5_ensemble_2026_05_03/verdict_4seed.json`
- `state/p9_p1_5_ensemble_2026_05_03/per_seed_results.json`
- `state/p9_p1_5_ensemble_2026_05_03/comparison_vs_b_ensemble.json`
- `state/p9_p1_5_ensemble_2026_05_03/phase1_5_seed{43,44,45}_per_prompt.json`
- `state/markers/p9_p1_5_ensemble_4seed_landed.marker`
