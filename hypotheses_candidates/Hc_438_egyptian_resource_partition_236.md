---
id: Hc_438
slug: egyptian-resource-partition-236
title: Egyptian resource partition 1/2 + 1/3 + 1/6 = 1 — preproc/core/postproc split (anima-soc, anima-service)
domain: math
status: candidate-unverified
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 27-31, 181-184
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: Egyptian unit fraction 1/2+1/3+1/6=1 derived from sigma(6)=12 divisors. Used as candidate resource partition: 50% preproc, 33% core, 17% postproc. Also present in anima-service spec.
---

## Hypothesis
The optimal resource allocation across a 3-stage AI SoC pipeline (preproc / core / postproc) follows the Egyptian unit-fraction partition 1/2 + 1/3 + 1/6 = 1 (50% / 33% / 17%) derived from sigma(6)=12 divisor structure. Deviation from this split degrades throughput-per-area beyond the n=6 +/-10% convexity band.

## Migration TODO
- [ ] Empirical resource-split DSE: sample alternate 3-way splits, measure throughput
- [ ] Test convexity: ±10% perturbation of each fraction
- [ ] Falsifier: optimum split significantly outside (0.5, 0.33, 0.17) ± 0.05
