---
id: Hc_174
slug: topo22b-75pct-frustration
title: Hypercube 1024 + 75% frustration is worst in sweep (TOPO22b)
domain: physics | consciousness
status: merged-to-H_178
merged_at: 2026-05-12
merged_to: hypotheses/H_178_frustration_sweep_50pct_optimum_cluster.md
source_doc: docs/hypotheses/topo/TOPO22b.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_168 (TOPO19a 50%)
notes: i%4!=0 implementation
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Hypercube 1024 + 75% frustration (i%4!=0) yields the worst Φ in the frustration sweep, indicating Φ has a strong peak near 50% and rapidly degrades above it.

## Migration TODO
- [ ] report exact Φ
- [ ] verify worst-case status

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO22b-1**: Frustration sweep {50%, 60%, 75%, 90%}: if Φ at 75% is NOT the minimum → 'worst in sweep' claim falsified
- **F-TOPO22b-2**: Replicate 75%-frustration with 5+ seeds: if 1σ-CI overlaps 60% or 90% → 'worst' is within-noise
- **F-TOPO22b-3**: Cross-substrate (torus, small-world) 75%-frustration: if 75% is also worst there → universal frustration-collapse, not hypercube-specific
- **F-TOPO22b-4**: Cross-engine PyPhi formal IIT 75%-frustration: if 75% is NOT the formal-IIT minimum → anima-proxy artifact

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO22b-1**: 'Worst in sweep' is the negative-extreme of the TOPO22 frustration triangulation. Same single-run anchor limit as TOPO22a/d
- **L-TOPO22b-2**: Cell parity at 75% creates 768+256 partition — uneven, possibly creates engine-aliasing artifact
- **L-TOPO22b-3**: no formal IIT replication; pure anima-proxy negative result
- **L-TOPO22b-4**: n=6 triviality unaddressed (H_153 L7)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10/20)
- **sibling Hc**: Hc_168 (TOPO19a 50% record), Hc_173 (TOPO22a 60%), Hc_176 (TOPO22d 90%)

## Scaffold Notes

Pure complement to TOPO22a — same H_159 absorption.

