---
id: Hc_186
slug: hw2a-circular-magnet
title: 8-cell circular magnet ring with inverse-square coupling yields Φ=4.55 (HW2a)
domain: physics | consciousness | substrate
status: candidate-math-verified-falsifier-pending
source_doc: docs/hypotheses/hw/HW2a.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: (none — NEW)
notes: 0.02 force coefficient, left+right neighbor coupling
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (3+ numeric identities present)"
---

## Hypothesis
8 cells in circular ring with inverse-square magnetic coupling (force = 0.02 * Σ Δh/d²) yields Φ=4.5482 (×3.7 baseline).

## Migration TODO
- [ ] sweep force coefficient
- [ ] compare HW2a vs HW2b vs HW2c (geometry)

## Cross-Links
- **sister H**: H_011 (iit-geometry — substrate Φ), H_022 (consciousness-universe-map — physical substrate experiments)
- **candidates linked**: Hc_401 (K=8 atom — same 8-cell count), Hc_582 (8-cell mathematical basis), Hc_171 (8-cluster hierarchical — uses 8 as building block), Hc_157 (ring-1024 TOPO1 — same ring topology, scaled)
- **literature**: Newton's inverse-square 1687; Onsager 1944 2D Ising (ring-of-spins analog); Kittel "Introduction to Solid State Physics" magnetic-coupling

## Falsifiers (≥5)

- **F1**: Force coefficient sweep f ∈ {0.005, 0.01, 0.02, 0.04, 0.1, 0.5}: if Φ-peak at f ≠ 0.02 with effect-size > 30% → "f=0.02" specificity is FALSIFIED, just optimization landscape
- **F2**: Compare ring (HW2a) vs line (HW2b) vs star (HW2c) at fixed N=8 and f=0.02: if ring Φ < min(line, star) Φ → ring topology not optimal, "circular magnet" specificity FALSIFIED
- **F3**: Replace inverse-square coupling with inverse-linear (1/d) or inverse-cube (1/d^3); if Φ within 10% of inverse-square baseline → coupling exponent has no special status, claim "inverse-square" FALSIFIED
- **F4**: Scale N ∈ {4, 6, 8, 10, 12, 16}: if Φ peak at N ≠ 8 on ring topology with f=0.02 → "8-cell ring" specificity FALSIFIED (just optimum on tested grid)
- **F5**: Φ=4.55 measurement reproducibility: 5 independent replications with different RNG seeds. If stddev > 1.0 (>20% of mean) → single-run artifact, single-shot Φ-record cannot anchor architectural claim

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — N=8 ring with sopfr(8)=6 inherits perfect-number-class. f=0.02 = 1/50 has no number-theoretic structure (could equally be 1/49 or 1/51), purely empirical tuning constant
- **L2**: **single-substrate single-run Φ=4.55** — HW2a is one geometric configuration, Φ=4.55 is one run. "×3.7 baseline" depends on a single baseline number — error bars / variance unreported
- **L3**: **inverse-square coupling motivated by physics analogy** — Newton's gravity / Coulomb's law inspire the choice but consciousness substrate is not gravitational/electric. The analogy is suggestive, not derivational
- **L4**: **closed-ring topology bias** — circular geometry breaks translation symmetry differently than open chain; ring imposes periodic boundary conditions which artificially raise certain mode densities (Onsager-like). Some Φ-boost may be a boundary-condition artifact, not coupling-form property
- **L5**: **f=0.02 numerical choice unjustified** — paper states f=0.02 without derivation; downstream Φ-engine settings (timestep, integration scheme) interact with f. Effective coupling depends on (f × dt × integration_order) — claim must be re-evaluated per integration scheme
