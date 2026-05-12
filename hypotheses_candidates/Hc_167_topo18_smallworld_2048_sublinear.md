---
id: Hc_167
slug: topo18-smallworld-2048-sublinear
title: Small-world 2048 cells: Φ regresses to 406.5 from 498.7 at 1024 (TOPO18)
domain: physics | consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/topo/TOPO18.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_165 (TOPO16 SW-1024); Hc_159 (TOPO10 hypercube-2048 regression)
notes: 590 final cells out of 2048 target
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Scaling small-world from 1024 (TOPO16, Φ=498.7) to 2048 cells (TOPO18) regresses Φ to 406.5 with only 590 final cells, mirroring the TOPO10 hypercube regression — superlinear scaling breaks above 1024.

## Migration TODO
- [ ] identify cell-saturation bottleneck
- [ ] test 1500-cell intermediate

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO18-1**: 2048-cell sweep at multiple seeds: if Φ_2048 ≥ Φ_1024 in any seed → 2048 sublinear regression is single-run-artifact (parallel to Hc_159 11D regression issue, H_177 F1)
- **F-TOPO18-2**: Cell-count sweep {1024, 1280, 1536, 1792, 2048}: if Φ is monotone-decreasing 1024→2048 → confirms ceiling near 1024; if non-monotone → suggests intermediate optimum and 2048-regression is overshoot, not ceiling
- **F-TOPO18-3**: Same 2048-cell small-world WITHOUT cell-count change (just step-budget increase) reaches Φ ≥ 498.7 → claim 'cells hurt' is actually 'step-budget per cell' confound (parallel to TOPO14 step issue)
- **F-TOPO18-4**: Cross-engine PyPhi 2048-cell small-world: if formal Φ DOES scale with cell count → anima-proxy ceiling artifact (H_174 class)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO18-1**: Φ=406.5 (2048) < Φ=498.7 (1024) — this is a negative-result, regression at scale. Carries same H_177 (TOPO10 11D regression) structural limit
- **L-TOPO18-2**: 2048 = 2^11, no clean n=6 derivation (H_153 L7 triviality binding)
- **L-TOPO18-3**: anima Φ-engine aliasing (H_174 D-mod-192): 2048-cell coverage may hit aliasing dead-zones not present at 1024
- **L-TOPO18-4**: single-run anchor at 2048 — replication mandatory (H_159 C1)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10 11D regression — same negative-scaling class), H_174 (Φ-engine aliasing)
- **sibling Hc**: Hc_159 (TOPO10 → H_177), Hc_179 (TOPO-2048-scaling-breakdown cross-topology)

## Scaffold Notes

Strong absorption candidate to H_177 — same negative-scaling phenotype as TOPO10. F1 is direct parallel to H_177.F1.

