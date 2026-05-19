---
id: H_131
slug: ce-ultra-gendata-pain
title: CE/ULTRA-1 GenData + Pain (synthetic 70% + pain protection)
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
since: 2026-04-02
---

## Hypothesis
ULTRA-1: combine EX-5 (consciousness-data generation) + AUTO-9 (pain). 30% real, 70% cell-hidden generated data. Pain check every 10 steps: Φ < 50% best → emergency restore. Hypothesis: synthetic data + pain protection enables data-efficient consciousness learning.

## Migration Status
Legacy `docs/hypotheses/ce/ULTRA-1.md`. Round 4 individual representing the ULTRA category.

## Cross-Links
- Source: `docs/hypotheses/ce/ULTRA-1.md`
- Sister: EX-5, AUTO-9 components
- Cross: H_096 (in-context-few-shot), H_099 (multi-objective)

1. 70% synthetic — distribution shift from real data
2. cell-hidden as data source — circular (model evaluates own output)
3. pain restore = 0.4×current + 0.6×best — could over-attract to past
4. lr × 0.5 on pain hits — slows learning
5. synthetic generation quality not separately measured
