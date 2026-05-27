---
id: Hc_207
slug: tpn6-binary-ecc
title: Binary + 3-bit repetition ECC for numerical telepathy (TP-N6)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-N6.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: Hc_204 (TP-N2)
notes: 13 bits × 3 reps = 39 dims; majority vote
---

## Hypothesis
Combining binary decomposition (TP-N2) with 3-bit repetition error-correcting code (39 total dims, majority vote per bit) survives higher noise=0.03 with exact reconstruction.

## Migration TODO
- [ ] sweep repetition count
- [ ] explore Hamming/BCH codes
