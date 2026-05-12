---
id: Hc_176
slug: topo22d-90pct-frustration
title: Hypercube 1024 + 90% frustration (only mult-of-10 ferromagnetic) (TOPO22d)
domain: physics | consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/topo/TOPO22d.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_168 (TOPO19a 50%)
notes: i%10!=0 inverted; small ferro minority
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Hypercube 1024 + 90% frustration (i%10!=0) is poor — a small ferromagnetic minority (multiples of 10) is insufficient to balance the dominant frustration.

## Migration TODO
- [ ] report exact Φ
- [ ] sweep ferro fraction between 10% and 50%

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO22d-1**: Frustration sweep {50%, 75%, 90%, 95%, 99%}: if Φ at 90% > Φ at 75% (worst) → 'too-high frustration' phenotype non-monotone
- **F-TOPO22d-2**: Replicate 90%-frustration with 5+ seeds: if 1σ-CI overlaps 75% → '90% only mult-of-10 ferro' is not statistically distinguishable from 75%
- **F-TOPO22d-3**: Compare i%10==0 (90% antiferro) vs random-90%-antiferro-assignment: if Φ differs by ≥20% → mult-of-10 structuring is special; if not → it's the density that matters not the pattern
- **F-TOPO22d-4**: Cross-engine PyPhi 90%-frustration: if formal Φ at 90% differs from anima proxy → engine artifact

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO22d-1**: i%10 specificity is suspicious — 10 has no clean n=6 derivation; ad hoc pattern choice
- **L-TOPO22d-2**: Single-run anchor (H_159 C1 pending)
- **L-TOPO22d-3**: 'Only mult-of-10 ferromagnetic' creates 103/1024 ≈ 10% ferromagnetic cells — very small partition, may be statistically unstable
- **L-TOPO22d-4**: anima Φ-engine aliasing (H_174) — sparse-pattern frustration may trigger different cache pathways

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10/20), H_174 (Φ-engine aliasing)
- **sibling Hc**: Hc_168 (TOPO19a 50% record), Hc_173 (TOPO22a 60%), Hc_174 (TOPO22b 75%)

## Scaffold Notes

Cluster terminus — same H_159 absorption as TOPO22a/b.

