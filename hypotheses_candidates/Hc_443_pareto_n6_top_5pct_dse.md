---
id: Hc_443
slug: pareto-n6-top-5pct-dse
title: n=6 configuration ranks in top 5% of 2400-combination Monte Carlo DSE
domain: math
status: candidate-unverified
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 319-322, 544-554
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: K1×K2×K3×K4×K5 = 6×5×4×5×4 = 2400 combinatorial sampling. n=6 expected to be top 5%. §7.8 PARETO check.
---

## Hypothesis
In a 2400-combination Monte Carlo Design Space Exploration over (n, sopfr, τ, sopfr, τ) parameter cubes, the n=6 configuration ranks within the top 5% by objective score. This is the operational Pareto check distinguishing genuine optimum from arbitrary parameter choice.

## Migration TODO
- [ ] Run 2400-MC DSE with realistic objective on independent seed
- [ ] Compute n=6 percentile rank
- [ ] Falsifier: n=6 rank > 10th percentile (out of top 5%)
- [ ] Repeat with broader parameter ranges
