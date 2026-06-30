---
id: Hc_266
slug: ce10-transplant
title: Transplant pretrained decoder onto high-Φ engine for immediate CE drop (CE-10)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/CE-10.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: source decoder pretrained 100 steps; load_state_dict transplant
---

## Hypothesis
A decoder pretrained 100 steps on random-hidden → target mapping can be transplanted (load_state_dict) to a target high-Φ engine and immediately reduces CE — knowledge transfer via decoder copy.

## Migration TODO
- [ ] measure CE_before vs CE_after transplant
- [ ] sweep source decoder pretrain length
