---
id: Hc_206
slug: tpn5-repeat-median
title: 3-channel repeat with median selection is outlier-robust (TP-N5)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-N5.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: Hc_205 (TP-N4)
notes: 10% error tolerance for correct; median > mean
---

## Hypothesis
Sending the same numerical value via 3 channels (concept, context, meaning) and selecting the median of the 3 decoded estimates is outlier-robust — survives 1-channel failure that would corrupt mean.

## Migration TODO
- [ ] verify outlier robustness
- [ ] compare median vs mean
