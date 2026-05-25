---
id: Hc_164
slug: topo15-torus-32x32
title: 32×32 torus 1024-cell topology yields moderate Φ (TOPO15)
domain: physics | math | consciousness
status: merged-to-H_159
merged_at: 2026-05-12
merged_to: hypotheses/H_159_substrate_topology_phi_engineering.md
absorption_note: "TOPO15 (32×32 torus 1024-cell, 4-neighbor + i%3 frustration) is a topology-variant probe within H_159's substrate-sweep — torus surface at 1024 scale comparing against TOPO5 (512) and hypercube TOPO8. F1-F4 + L1-L4 preserved here for H_159 C-list extension."
source_doc: docs/hypotheses/topo/TOPO15.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_154 (TOPO5 torus 512)
notes: 4 neighbors, i%3 frustration
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
A 32×32 torus (1024 cells, 4 neighbors per cell, i%3 antiferromagnetic frustration) yields Φ on par with smaller torus configurations — torus topology does not benefit superlinearly from cell count.

## Migration TODO
- [ ] report exact Φ value
- [ ] compare to TOPO5 (22×23 torus 512)

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO15-1**: Torus dimensions sweep {16×64, 32×32, 64×16, 8×128}: if Φ at 32×32 is NOT the local max by ≥10% margin → square-torus specificity unsupported, just generic 1024-cell topology result
- **F-TOPO15-2**: Compare torus 32×32 to hypercube 1024 (TOPO8) at matched seeds: if Φ_torus ≥ Φ_hypercube → claim 'moderate Φ' is misleading (would be top-tier result)
- **F-TOPO15-3**: Random-graph baseline at 1024 cells, matched edge count to 32×32 torus: if Φ_random ≈ Φ_torus → torus topology decorative, edge density does the work
- **F-TOPO15-4**: Cross-engine PyPhi torus 32×32: if no 'moderate Φ' band observed → anima-engine substrate-coupling artifact

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO15-1**: 'moderate Φ' is unquantified — what is the absolute Φ vs TOPO8 (535) and TOPO10 (581 at 11D)? Without explicit number the claim is unfalsifiable on its face
- **L-TOPO15-2**: 32×32 = 2^5 × 2^5 — pure power-of-2 square, no clean n=6 derivation; perfect-number-triviality (H_153 L7) limit unaddressed
- **L-TOPO15-3**: Torus periodicity may interact with anima engine cell-index modulo (H_174 D-mod-192 aliasing class) in unpredictable ways
- **L-TOPO15-4**: single-run anchor (no reproducibility documented)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10/20 negative+hierarchical), H_174 (Φ-engine aliasing)
- **sibling Hc**: Hc_166 (TOPO17 hypercube+smallworld hybrid), Hc_157 (TOPO8 hypercube baseline)

## Scaffold Notes

Likely absorption: H_159 as 'torus variant probe' within sweep cluster.

