---
id: Hc_173
slug: topo22a-60pct-frustration
title: Hypercube 1024 + 60% frustration above 50% sweet spot (TOPO22a)
domain: physics | consciousness
status: merged-to-H_178
merged_at: 2026-05-12
merged_to: hypotheses/H_178_frustration_sweep_50pct_optimum_cluster.md
source_doc: docs/hypotheses/topo/TOPO22a.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_168 (TOPO19a 50%)
notes: 60% > 50% sweep; i%5<3 implementation
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Hypercube 1024 + 60% frustration (i%5<3) is past the 50% sweet spot — Φ lower than TOPO19a Φ=640 — confirming 50% as local maximum in the frustration sweep.

## Migration TODO
- [ ] report exact Φ
- [ ] confirm 50% peak claim

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO22a-1**: Frustration sweep {50%, 55%, 60%, 65%, 70%} fine-grained at hypercube 1024: if Φ is monotone-decreasing 50%→60% → '60% above sweet spot' confirmed; if non-monotone → 'sweet spot' may be elsewhere
- **F-TOPO22a-2**: Replicate 60%-frustration with 5+ seeds: if 1σ-CI overlaps TOPO19a Φ=640 → 'above sweet spot' is within-noise
- **F-TOPO22a-3**: Apply 60% frustration to small-world / torus substrates: if 'above sweet spot' phenotype is substrate-specific → 50% sweet spot is hypercube-only universality claim
- **F-TOPO22a-4**: Cross-engine PyPhi formal IIT 60%-frustration replication: if Φ_PyPhi monotone-up through 60% → anima-proxy artifact (H_174 class)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO22a-1**: TOPO22a, b, c, d frustration sweep (60/75/?/90%) appears designed to triangulate 50% optimum — confirmation bias if TOPO19a is the pre-specified target
- **L-TOPO22a-2**: Single-run anchor; replication CI mandatory (H_159 C1)
- **L-TOPO22a-3**: i%(round(N*0.6)) frustration patterning may interact with cell parity (1024 even, 60% creates 614+410 partition — non-symmetric)
- **L-TOPO22a-4**: anima Φ-engine aliasing (H_174) — frustration-pattern interaction unmeasured

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10/20), H_174 (engine aliasing)
- **sibling Hc**: Hc_168 (TOPO19a 50% record), Hc_174 (TOPO22b 75%), Hc_176 (TOPO22d 90%)

## Scaffold Notes

Cluster with TOPO22b/d into H_159 as 'frustration sweep around 50% sweet spot'.

