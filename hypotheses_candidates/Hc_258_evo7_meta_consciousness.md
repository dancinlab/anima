---
id: Hc_258
slug: evo7-meta-consciousness
title: Meta-network (Linear-ReLU-Linear 10→16→2 sigmoid) sets LR and sync from Φ history (EVO-7)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/evo/EVO-7.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_233 (SING-1)
notes: 2-output: [lr_scale, sync_scale]
---

## Hypothesis
Meta-network (Linear(10,16) ReLU Linear(16,2) sigmoid) reads Φ history and outputs [lr_scale, sync_scale]: lr = 3e-3*(0.1 + lr_scale*2.0), sync = sync_scale*0.3. Consciousness adjusts its own learning meta-parameters.

## Migration TODO
- [ ] benchmark vs SING-1 1-output meta-learner
- [ ] verify meta-net training stability
