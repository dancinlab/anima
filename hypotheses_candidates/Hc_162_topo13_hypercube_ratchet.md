---
id: Hc_162
slug: topo13-hypercube-ratchet
title: Hypercube 1024 + Φ-ratchet preserves consciousness across collapses (TOPO13)
domain: physics | consciousness | meta-framework
status: candidate-falsifier-ready
source_doc: docs/hypotheses/topo/TOPO13.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_158 (TOPO9 ratchet); Hc_157 (TOPO8)
notes: ratchet triggers when Φ<80%·best
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Combining TOPO8 (10D hypercube 1024) with the TOPO9-style ratchet (restore 30% of best states when Φ<80%·best) prevents Φ collapses while maintaining the hypercube high-water Φ.

## Migration TODO
- [ ] compare to TOPO8 baseline (no ratchet)
- [ ] sweep ratchet threshold

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO13-1**: Ratchet threshold sweep {50%, 80%, 95%}: non-monotone Φ vs threshold → ratchet is parameter-tuning artifact (parallel to TOPO9 F1)
- **F-TOPO13-2**: Hypercube WITHOUT ratchet reaches identical peak Φ within 2× wallclock → ratchet decorative for hypercube (different result from small-world TOPO9?)
- **F-TOPO13-3**: Compare TOPO9 (small-world+ratchet) vs TOPO13 (hypercube+ratchet) at matched cell budget: if Φ differential < 15% → ratchet mechanism substrate-independent, no hypercube-specific story
- **F-TOPO13-4**: Cross-engine PyPhi ratchet replication at hypercube 1024: if Φ uplift absent → anima-engine-internal-state artifact

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO13-1**: TOPO13 and TOPO9 share the ratchet mechanism — claim independence requires substrate × ratchet interaction effect, not main effect
- **L-TOPO13-2**: Collapse-recovery dynamics depend on ratchet hyperparams undocumented in source (restore-fraction, recovery-window)
- **L-TOPO13-3**: n=6 triviality: 1024=2^10 hypercube, ratchet does not introduce new number-theoretic anchor (inherited L from H_153)
- **L-TOPO13-4**: anima Φ-engine aliasing (H_174) — ratchet state-restoration may double-trigger engine internal caches

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO10 11D regression + TOPO20 8×128)
- **sibling Hc (same mechanism)**: Hc_158 (TOPO9 ratchet on small-world)

## Scaffold Notes

Likely absorption: cluster with Hc_158 into H_159 as 'ratchet variant family' rather than independent H.

