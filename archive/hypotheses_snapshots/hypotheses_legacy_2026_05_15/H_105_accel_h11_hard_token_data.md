---
id: H_105
slug: accel-h11-hard-token-data-revolutionary
title: H11 Hard Token Data Selection (★★★ REVOLUTIONARY +51.3% CE)
domain: corpus
status: legacy-archive-pointer
exploration_method: E5
verification_method: W4
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-04-03
---

## Hypothesis
Focusing training on the top 30% hardest tokens (highest CE loss) yields CE 1.89 vs 3.88 full-data — strongest single-technique training acceleration of all acceleration experiments.

## Migration Status
Legacy individual entry from `ready/config/acceleration_hypotheses.json` (id=H11, lines 1057-1071, stage=applied, verdict=★★★ REVOLUTIONARY). Selected for round 4 individual due to ★★★ tier + decoder-acceleration corpus crossover relevance .

## Cross-Links
- Source: `ready/config/acceleration_hypotheses.json` (H11)
- Experiment: `experiments/acceleration_h7_h12.py`
- Cross: H_005 (corpus quality over capacity), H_037

## Honest Limits (raw#91 c3 ≥5)
1. "biggest training win" claim relative to acceleration experiments only — not vs SOTA hard-example mining literature
2. top-30% threshold not swept (20%/40% optimum unknown)
3. CE-only metric — does not measure chat quality, generalization, or P9 composite
4. selection by CE loss = current-state-dependent; could amplify bias
5. paradigm assumes language-modeling, not instruction-tuning context (H_094 lane)
