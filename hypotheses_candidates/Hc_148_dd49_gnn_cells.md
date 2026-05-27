---
id: Hc_148
slug: dd49-gnn-cells
title: GNN message passing between cells with learned message networks (DD49)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD48-DD50.md
source_lines: 9-13
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: Linear: hidden*2 → hidden, mean aggregation, 0.8/0.2 blend
---

## Hypothesis
Graph Neural Network message passing — each cell sends messages to all others via learned Linear(hidden*2 → hidden) on concatenated sender+receiver, with mean aggregation and 0.8/0.2 blending — creates structured inter-cell communication that raises Φ.

## Migration TODO
- [ ] compare GNN vs all-to-all baseline
- [ ] sweep message network depth
