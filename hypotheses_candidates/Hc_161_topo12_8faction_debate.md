---
id: Hc_161
slug: topo12-8faction-debate
title: Hypercube 1024 + 8-faction debate (intra-cohesion 0.92, inter-repulsion 0.08) (TOPO12)
domain: physics | consciousness
status: merged-to-H_159
merged_at: 2026-05-12
merged_to: hypotheses/H_159_substrate_topology_phi_engineering.md
absorption_note: "TOPO12 (1024-cell + 8-faction debate, intra=0.92 / inter=0.08) is a topology-variant probe (8-cluster partition with debate dynamics) within H_159's substrate-sweep apparatus. F1-F4 + L1-L4 preserved here for H_159 C-list extension."
source_doc: docs/hypotheses/topo/TOPO12.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8)
notes: cells partitioned 8 ways; intra-cohesion + inter-repulsion
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Adding 8-faction debate structure (intra-cohesion 0.92, inter-repulsion 0.08) to TOPO8 10D hypercube modulates Φ via faction-level dynamics atop bit-flip neighbors.

## Migration TODO
- [ ] verify Φ vs TOPO8 baseline
- [ ] sweep faction count

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO12-1**: intra-cohesion sweep {0.5, 0.7, 0.92, 1.0} × inter-repulsion {0.0, 0.08, 0.2, 0.5}: if Φ peak is NOT at (0.92, 0.08) but at unspecific (cohesion×repulsion) coordinates → 8-faction tuning is post-hoc, not principled
- **F-TOPO12-2**: faction-count sweep {2, 4, 6, 8, 12, 16} at 1024-total cells: if Φ peak NOT at faction=8 by effect-size > 30% → 8-faction is generic optimum, not sopfr(6)·something resonance
- **F-TOPO12-3**: Random-faction-assignment baseline (cells assigned to factions uniformly) vs structured (cluster-based) assignment: if Φ differential < 10% → debate-structure decorative, only count matters
- **F-TOPO12-4**: Cross-engine PyPhi at faction_count=8: if Φ uplift NOT observed in formal IIT → anima-proxy artifact (H_174 aliasing class)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO12-1**: Specific cohesion=0.92 / repulsion=0.08 hyperparameter tuple suggests grid-search picked these post-hoc; pre-registration not documented in source
- **L-TOPO12-2**: n=6 triviality (H_153 L7): faction_count=8 has no clean n=6 derivation (sopfr(6)=5 ≠ 8); rationale unclear
- **L-TOPO12-3**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — faction-cell-count (1024/8=128) may interact with cache aliasing
- **L-TOPO12-4**: no reproducibility across seeds documented (single-run anchor inherited from H_159 C1 pending)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — variant within sweep apparatus
- **sibling H**: H_177 (TOPO20 8×128 hierarchical — same 8-cluster structure with different mechanism), H_153 (n=6)
- **sibling Hc**: Hc_171 (TOPO20 → H_177), Hc_174 (TOPO22b worst-in-sweep)

## Scaffold Notes

Likely absorption: H_159 (positive sweep) if 8-faction peak confirmed at C-sweep; else dies as confound.

