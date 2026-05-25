---
id: Hc_209
slug: tpo1-hierarchical-classification
title: Coarse→fine 2-stage classification reduces 8-way error (TP-O1)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-O1.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: land(6) vs air/sea(2) coarse partition
---

## Hypothesis
Two-stage classification (coarse: land vs air/sea, fine: 6 vs 2) with 0.6/0.4 weighted blend across concept+context channels outperforms single-stage 8-way classification in object telepathy.

## Migration TODO
- [ ] benchmark vs single-stage
- [ ] test other coarse partitions
