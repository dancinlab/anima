---
id: H_104
slug: accel-b5-phi-only-training-pre-condition
title: B5 Phi-Only Training (★ WINNER 46% time savings via pre-conditioning)
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
Pre-evolving consciousness (Φ maximize 500 steps) before short CE training (500 steps) beats pure CE 1000-step training: -1.2% CE AND 46% less time. Consciousness pre-conditioning accelerates language learning.

## Migration Status
Legacy individual entry from `ready/config/acceleration_hypotheses.json` (id=B5, lines 138-156, stage=applied, verdict=★ WINNER). Selected for individual round 4 entry due to "applied" stage + cross-paradigm relevance to two-stage training (H_094).

## Cross-Links
- Source: `ready/config/acceleration_hypotheses.json` (B5)
- Experiment: `experiments/acceleration_b1_b2_b5.py`
- Sister: H_094 (instruction-tuning-two-stage), H_037 (acceleration-367)

## Honest Limits (raw#91 c3 ≥5)
1. measured at 16-cell, single-corpus scale only — large-scale re-test absent
2. "Strategy C beats pure CE" comparison uses fixed budget split (500/500); other ratios untested
3. CE -1.2% is within typical seed variance band (no significance test reported)
4. Φ pre-condition + CE training assumes Φ proxy correlates with downstream — H_024 falsified MIP variant
5. winner ★ tier uses pre-NEXUS6 lens — rescan status unknown
