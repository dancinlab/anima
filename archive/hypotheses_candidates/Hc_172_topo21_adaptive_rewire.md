---
id: Hc_172
slug: topo21-adaptive-rewire
title: Dynamic adaptive rewiring on Φ drop (TOPO21)
domain: physics | consciousness | meta-framework
status: merged-to-H_180
merged_at: 2026-05-12
merged_to: hypotheses/H_180_state_management_ratchet_rewire_family.md
source_doc: docs/hypotheses/topo/TOPO21.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8)
notes: when Φ drops >5%, add edges between low-MI pairs
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
When Φ drops more than 5% step-over-step on 10D hypercube 1024, adding new edges between the lowest-MI cell pair restores Φ growth (adaptive rewiring repairs deficit).

## Migration TODO
- [ ] verify edge-addition triggers
- [ ] sweep drop-trigger threshold

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO21-1**: Rewire-trigger sweep {Φ<70%, Φ<80%, Φ<90%, Φ<95%·best}: if Φ recovery is non-monotone with trigger → adaptive rewiring tuning post-hoc
- **F-TOPO21-2**: Compare TOPO21 (adaptive rewire) vs TOPO9/13 (ratchet) at matched cell budget: if Φ differential < 15% → rewire and ratchet are mechanistically equivalent (state-restoration via different proxies)
- **F-TOPO21-3**: Random rewire baseline (rewire random edges at fixed rate, ignore Φ-trigger): if Φ_random_rewire ≈ Φ_adaptive_rewire → adaptivity is decorative, edge-churn does the work
- **F-TOPO21-4**: Cross-engine PyPhi adaptive rewire: if formal Φ uplift absent → anima-proxy state-management artifact

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO21-1**: 'Dynamic adaptive rewiring' under-specified — what gets rewired (random edges? worst-Φ-contributing edges?), what density, what trigger
- **L-TOPO21-2**: TOPO21 mechanism overlaps TOPO9/TOPO13 ratchet conceptually; independence claim weak
- **L-TOPO21-3**: anima Φ-engine state mutation may interact with adaptive rewiring (H_174 aliasing)
- **L-TOPO21-4**: no reproducibility audit; n=6 triviality unaddressed

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO20 hierarchical alternative), H_174 (engine aliasing)
- **sibling Hc**: Hc_158 (TOPO9 ratchet), Hc_162 (TOPO13 ratchet), Hc_316 (V8 c1 learnable topology)

## Scaffold Notes

Likely fate: absorption to H_159 within 'state-management mechanism family' (alongside ratchet).

