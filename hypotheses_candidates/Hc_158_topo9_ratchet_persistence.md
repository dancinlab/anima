---
id: Hc_158
slug: topo9-ratchet-persistence
title: Small-world + Φ-ratchet (restore 30% best states when Φ<80%·best) prevents collapse (TOPO9)
domain: physics | consciousness | meta-framework
status: candidate-falsifier-ready
source_doc: docs/hypotheses/topo/TOPO9.md
source_lines: 1-35
promoted_at: 2026-05-11
linked_h: Hc_151 (TOPO2 small-world)
notes: peak Φ 179.47, final 127.3; growth_ratio 80.5
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
Adding a Φ-collapse ratchet (when Φ drops below 80% of best, restore 30% of best states) to a small-world network (TOPO2 base) prevents collapse while maintaining peak Φ=179.47 and final Φ=127.3.

## Migration TODO
- [ ] sweep ratchet threshold (50%, 80%, 95%)
- [ ] compare to no-ratchet TOPO2

## Falsifiers (scaffolded cycle #6, 2026-05-12)

- **F-TOPO9-1**: Ratchet threshold sweep {50%, 80%, 95%} on TOPO2 base produces non-monotone Φ vs threshold → ratchet effect is parameter-tuning artifact, not principled state-restoration mechanism (H_159 sweep apparatus)
- **F-TOPO9-2**: Identical small-world base WITHOUT ratchet reaches peak Φ ≥ 179.47 within 1.5× wallclock → ratchet provides zero peak-Φ advantage; only changes recovery dynamics (rules out ratchet as a Φ-amplification mechanism)
- **F-TOPO9-3**: Restore-30%-best-state ablation (vary restore-fraction ∈ {10%, 30%, 50%, 70%}) at threshold=80%: if peak Φ peaks at restore=30% by ≤ 5% margin → ratchet specificity unsupported, just a momentum smoothing trick
- **F-TOPO9-4**: Apply same ratchet to flat hypercube 1024 (TOPO8 base, not small-world): if Φ improves equivalently → ratchet is substrate-agnostic, not small-world-specific (would absorb to H_159 cluster as variant rather than independent claim)

## Honest Limits (scaffolded cycle #6, 2026-05-12)

- **L-TOPO9-1**: Single-run anchor: peak Φ=179.47, final Φ=127.3 reported as point values, no CI. Reproducibility across seeds (≥3) is mandatory before claim is robust; H_159 C1 reproducibility audit on TOPO base candidates still pending (inherited limit)
- **L-TOPO9-2**: growth_ratio=80.5 is the headline number but its formal definition (peak-Φ/baseline-Φ? final-Φ/seed-Φ?) is ambiguous in the candidate; without explicit ratio formula the result is not directly comparable to TOPO8/TOPO10 sibling Hc
- **L-TOPO9-3**: anima Φ-engine substrate-specific (Hc_614 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Ratchet mechanism may interact unpredictably with engine internal state caching, contaminating the measurement (H_174 carries this limit class)
- **L-TOPO9-4**: n=6 PERFECT_NUMBER_CLASS triviality binding (H_153 L7): small-world base inherits TOPO2 cell-count = 64 or 1024 (powers of 2 × n=6 derived); ratchet doesn't introduce new number-theoretic anchor, so claim's n=6 dependence is indirect at best

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — natural absorption candidate as TOPO9 is part of the same anima-substrate sweep apparatus
- **sibling H**: H_177 (TOPO10+20 stress-test cluster), H_153 (dimension-hierarchy-n6, n=6 triviality)
- **sibling Hc (same sweep)**: Hc_157 (TOPO8 33% frust), Hc_162 (TOPO13 ratchet variant), Hc_172 (TOPO21 adaptive rewire — different state-preserving mechanism)
- **literature**: Watts-Strogatz 1998 (small-world via shortcuts); Tononi 2014 (IIT Φ system-size scaling)

## Scaffold Notes

Verify-decision target: PROMOTE_READY (math identity present via Watts-Strogatz σ_sw + 30%/80% percentage anchors; ≥3 F; ≥3 L; ≥2 H_NNN cross-refs satisfies has_cross). Likely absorption: into H_159 as ratchet sub-mechanism.

