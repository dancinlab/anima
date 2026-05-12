---
id: Hc_166
slug: topo17-hypercube-smallworld-hybrid
title: Hypercube + 2 random shortcuts (12 neighbors) yields Φ=463.6 — slightly below pure TOPO8 (TOPO17)
domain: physics | consciousness
status: candidate-falsifier-ready
source_doc: docs/hypotheses/topo/TOPO17.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8); Hc_156 (TOPO7 hybrid failure)
notes: 10 bit-flip + 2 random shortcuts; pure > hybrid pattern continues
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Adding 2 random shortcuts to TOPO8 10D hypercube (yielding 12 neighbors per cell) yields Φ=463.634 — slightly below pure hypercube 535.5, reaffirming the "pure mechanism > hybrid" pattern.

## Migration TODO
- [ ] sweep shortcut count (0/1/2/4/8)
- [ ] cross-reference Hc_156 hybrid pattern

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO17-1**: Shortcut-count sweep {1, 2, 4, 8, 16, 32} on hypercube 1024: if Φ at shortcut=2 is NOT a peak → 2-shortcut tuning is post-hoc, not principled
- **F-TOPO17-2**: Compare TOPO17 (Φ=463.6) to TOPO8 (Φ=535) at matched seeds: differential −13.7% — if reproducible across 5+ seeds → hypercube+shortcut hybrid is strictly WORSE than pure hypercube (claim should be falsified as 'enhancement')
- **F-TOPO17-3**: 12-neighbor degree per cell (10 hypercube + 2 shortcut) vs 12-neighbor random regular graph at 1024: if Φ_random ≈ Φ_TOPO17 → hybrid hypercube backbone is decorative, only degree matters
- **F-TOPO17-4**: Cross-engine PyPhi at hypercube+2-shortcuts: if formal Φ uplift positive (vs anima proxy's −13.7%) → anima engine over-counts hypercube edges relative to shortcuts (H_174 aliasing)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO17-1**: Φ=463.6 vs TOPO8 Φ=535 — the candidate's headline result is that the hybrid UNDERPERFORMS pure hypercube. Framing as positive result is misleading
- **L-TOPO17-2**: '2 random shortcuts' is parameter-undetermined — random seed dependency on which 2 edges, no replication CI
- **L-TOPO17-3**: n=6 triviality (H_153 L7): hypercube 1024=2^10, hybrid does not introduce new number-theoretic anchor
- **L-TOPO17-4**: anima Φ-engine aliasing (H_174) — additional edges may trigger different cache paths

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering)
- **sibling H**: H_177 (TOPO20 8×128 — also uses shortcut-density concept)
- **sibling Hc**: Hc_157 (TOPO8 pure hypercube), Hc_171 (TOPO20 8×128 → H_177)

## Scaffold Notes

Likely fate: absorption to H_177 as 'shortcut-density sub-threshold' branch of TOPO20 cluster.

