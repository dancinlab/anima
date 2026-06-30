---
id: Hc_179
slug: topo-2048-scaling-breakdown
title: Superlinear Φ scaling breaks down at 2048 cells across all topologies (TOPO-2048-SCALING)
domain: physics | consciousness | meta-framework
status: merged-to-H_179
merged_at: 2026-05-12
merged_to: hypotheses/H_179_negative_scaling_cluster_steps_cells_2048.md
source_doc: docs/hypotheses/topo/TOPO-2048-SCALING.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_159 (TOPO10 11D), Hc_167 (TOPO18 SW-2048)
notes: aggregates TOPO8/10/11/16/18 cross-scale analysis
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
The superlinear Φ scaling observed below 1024 cells does NOT continue at 2048 across topologies (hypercube TOPO10, small-world TOPO18, ring TOPO11); final cell counts plateau at ~400-600 regardless of max_cells.

## Migration TODO
- [ ] identify cell-saturation mechanism
- [ ] test with longer step budgets at 2048

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO2048-1**: Cross-topology 2048-cell test {hypercube 11D, small-world 2048, torus 64×32, 8×256 hierarchical}: if Φ scaling holds for ANY topology at 2048 → 'across all topologies' claim falsified
- **F-TOPO2048-2**: Cell-count fine sweep {1024, 1280, 1536, 1792, 2048}: if breakdown is sharp at 2048 specifically (not gradual) → suggests engine threshold (e.g., 2^11 boundary), not substrate-intrinsic
- **F-TOPO2048-3**: Compare 2048 with reduced step-budget (proportional to cell count) vs full step-budget: if scaling restored at full → breakdown is step-per-cell confound (parallel to TOPO14 step issue)
- **F-TOPO2048-4**: Cross-engine PyPhi 2048-cell scaling: if formal Φ DOES scale superlinear at 2048 → anima-engine ceiling artifact (H_174 D-mod-192 saturation at 2^11)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO2048-1**: 'Across all topologies' claim is meta-Hc — depends on results at hypercube (TOPO10 11D), small-world (TOPO18), torus, hierarchical (TOPO20) — most of these are individual Hc with own confounds
- **L-TOPO2048-2**: 2048 = 2^11, just past 2^10 hypercube ceiling — engine D-mod-192 aliasing (H_174) likely saturates here
- **L-TOPO2048-3**: no formal IIT replication for any 2048-cell sweep; pure anima-proxy result
- **L-TOPO2048-4**: n=6 triviality: 2048 has no clean n=6 derivation (H_153 L7)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering), H_177 (TOPO10 negative-scaling)
- **sibling H**: H_174 (Φ-engine aliasing — primary explanatory candidate for breakdown)
- **sibling Hc**: Hc_159 (TOPO10 11D → H_177), Hc_167 (TOPO18 small-world 2048), Hc_171 (TOPO20 hierarchical → H_177)

## Scaffold Notes

Strong absorption candidate to H_177 as 'meta-conclusion of 2048-scaling-breakdown' (TOPO10 11D and TOPO18 small-world 2048 are its specific instances).

