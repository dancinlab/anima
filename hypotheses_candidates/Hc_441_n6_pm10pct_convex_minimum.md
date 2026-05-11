---
id: Hc_441
slug: n6-pm10pct-convex-minimum
title: f(n) has a CONVEX minimum at n=6 — f(6.6) and f(5.4) both worse than f(6)
domain: math
status: merged-to-H_067
merged_to: hypotheses/H_067.md
merged_at: 2026-05-11
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 298-301, 492-498
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: ±10% sensitivity convexity check. Convex extremum = real optimum candidate; flat = overfit. §7.4.
---

## Hypothesis
For SoC objective functions f built from the n=6 family, perturbing n by ±10% (n=6.6 or n=5.4) yields strictly worse f. The n=6 optimum is a convex extremum, not a flat plateau. Flat-response would indicate overfit / numerology-by-coincidence.

## Migration TODO
- [ ] Build empirical f and run ±10% sensitivity sweep
- [ ] Test sharper bounds: ±5%, ±1%
- [ ] Falsifier: f(6.6) ≤ f(6) or f(5.4) ≤ f(6) on any non-trivial objective
- [ ] Identify flat-response cases (these are the false-positives to remove)
