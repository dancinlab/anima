---
id: Hc_277
slug: ex3-multi-decoder-vote
title: 8 independent decoders, winner-take-all on minimum error per step (EX-3)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/EX-3.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: 8 Linear decoders + 8 optimizers
---

## Hypothesis
8 independent decoders (Linear + Adam each) run in parallel; each step, only the winner (lowest MSE) decoder's CE loss is backpropagated — ensemble selection at decoder level.

## Migration TODO
- [ ] sweep decoder count (4/8/16)
- [ ] compare to averaged decoder
