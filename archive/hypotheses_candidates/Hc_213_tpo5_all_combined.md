---
id: Hc_213
slug: tpo5-all-combined
title: TP-O1+O2+O3+O4 combined achieves ~100% under high noise=0.05 (TP-O5)
domain: math | corpus | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-O5.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: Hc_209 (TP-O1), Hc_210 (TP-O2), Hc_211 (TP-O3), Hc_212 (TP-O4)
notes: 30 contrastive iters, shapes + ensemble
---

## Hypothesis
Combining hierarchical classification + 3-channel ensemble + shape boost + contrastive separation (30 iters, threshold 0.3, push 0.05) achieves near-100% object telepathy under high noise=0.05.

## Migration TODO
- [ ] benchmark each individual technique
- [ ] sweep noise even higher (0.1, 0.2)
