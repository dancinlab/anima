---
id: Hc_439
slug: b4-scaling-log-log-regression
title: B^4 scaling exponent for SoC primary spec — log-log regression slope = 4.00 ± 0.05
domain: physics
status: merged-to-H_067
merged_to: hypotheses/H_067.md
merged_at: 2026-05-11
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 293-296, 481-490
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Scaling exponent regression on data [10,20,30,40,48] vs b^4 confirms slope 4.00±0.05. Confinement (B^4) / area sigma^2 / volume sigma^3 scaling laws. §7.3.
---

## Hypothesis
The SoC primary-spec scaling obeys a B^4 power law: log-log regression on canonical n=6-family data points [10, 20, 30, 40, 48] yields slope 4.00 ± 0.05. Confinement scaling B^4, area scaling σ^2, volume scaling σ^3 form a self-consistent triple. A slope outside [3.95, 4.05] rejects the scaling-law family.

## Migration TODO
- [ ] Reproduce regression on independent data points
- [ ] Test scale invariance: same slope at different magnitude ranges
- [ ] Falsifier: slope outside 4.0 ± 0.1 on real SoC measurements
