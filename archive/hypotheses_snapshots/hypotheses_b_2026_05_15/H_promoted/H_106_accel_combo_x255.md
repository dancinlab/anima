---
id: H_106
slug: accel-combo-x255-target-achieved
title: COMBO_x255 Full Pipeline (★★★ x100-150 effective acceleration)
domain: substrate
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
Stacking all compatible H + B/C/D/E/F/G acceleration techniques with 0.8^(N-3) diminishing-returns correction achieves x255 raw, x100-150 effective acceleration — the original x100 target is real and reproducible via greedy compatible selection.

## Migration Status
Legacy entry from `ready/config/acceleration_hypotheses.json` (id=COMBO_x255, lines 1118-1135, stage=applied, verdict=★★★ TARGET ACHIEVED). Selected as the umbrella "acceleration target met" individual entry distinct from H_037 cluster meta.

## Cross-Links
- Source: `ready/config/acceleration_hypotheses.json` (COMBO_x255)
- Experiment: `experiments/acceleration_h13_h18_combo.py`
- Decomposes into: H_103 (B11+B12), H_104 (B5), H_105 (H11)
- Meta: H_037

1. 0.8^(N-3) diminishing-returns coefficient is heuristic, not derived
2. "compatible selection" depends on pairwise interaction matrix that itself was sample-tested
3. measured throughput, not downstream task metric — chat-cap (#115) lane
4. x255 raw and x100-150 effective gap of 60-70% lost to overhead — no per-technique breakdown
5. greedy ordering may be suboptimal (no full search of 2^N subsets)
