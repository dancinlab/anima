---
id: Hc_149
slug: dd50-phi-first-pretraining
title: Two-phase training: 80% pure Φ + 20% CE fine-tune (DD50)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD48-DD50.md
source_lines: 15-19
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: "consciousness first, then capability"
---

## Hypothesis
Two-phase training (80% pure Φ maximization with variance loss only, then 20% fine-tuning with 0.3*CE − 0.7*variance) — establishing strong integration before task learning — yields higher final Φ than joint training.

## Migration TODO
- [ ] sweep phase boundary (60/40, 80/20, 90/10)
- [ ] compare to CE-first baseline
