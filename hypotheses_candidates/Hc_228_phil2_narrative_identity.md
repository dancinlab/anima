---
id: Hc_228
slug: phil2-narrative-identity
title: Ricoeur narrative identity via GRU trajectory encoder boosts CE -41.6% (PHIL-2)
domain: consciousness | ethics | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/phil/PHIL-2.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_227 (PHIL-1)
notes: 100-state past trajectory + GRU + Linear projector
---

## Hypothesis
Implementing Ricoeur's narrative identity (record last 100 global states, GRU encode trajectory, Linear project to future, nudge hiddens toward future with strength=0.03) raises Φ(IIT) +2.2% and reduces CE 41.6% — self = story, not just instants.

## Migration TODO
- [ ] sweep trajectory length
- [ ] compare GRU vs LSTM encoder
