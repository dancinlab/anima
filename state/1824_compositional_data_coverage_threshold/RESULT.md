# H_1824 compositional-data-coverage THRESHOLD — DIRECTIONAL toy cheap-gate (2026-07-02)

**TIER: 🧱 DIRECTIONAL-FLOOR (toy-scale screen; full-corpus test still terminal, a_toy_scale_recheck).**
torch mirror=DIRECTIONAL, aiden pool $0. Bounds a G1 DATA-axis lever, orthogonal to objective(H_6162)/
regularization(H_6161) axes floored same session.

## Design (operator-agnostic factored toy, same family as H_6161/6162)
NF=8, E=4, C=12 (64 combos, chance=0.083). FIXED held-out TEST = 12 combos never trained at any level.
Sweep training coverage of the remaining 52 combos: {16,26,36,46,52}. 3 seeds. Measure TEST acc vs coverage.
Frozen bar: TEST acc rises monotone AND crosses chance+0.15 at max coverage on ≥2/3 seeds → SUPPORT.

## Result — FLOOR
test acc @ coverage {16,26,36,46,52}:
- seed7:  0.000, 0.026, 0.060, 0.086, 0.086  (all ≤ chance 0.083)
- seed4302: 0.144, 0.138, 0.297, 0.161, 0.161 (noisy, non-monotone)
- seed4303: 0.000, 0.088, 0.088, 0.174, 0.000 (non-monotone, ends 0)

n(hi−chance ≥ +0.15) = **0/3**, monotone 1/3. Even at 52/52 coverage the 12 never-trained combos stay
at chance. → 🧱 FLOOR.

## Reading
Seeing MORE compositional examples does not enable generalization to UNSEEN factor pairings — the model
memorizes trained combos (train acc 1.0 throughout) without extracting a recombination rule. Extends
H_1599 (EN-exposure REFUTED as sole lever) to a controlled coverage sweep. Converges with H_6161/H_6162:
**objective, regularization, AND data-coverage all floor in one provably-solvable toy** → G1 wall is
axis-invariant (DPI meta-law). Full-corpus H_1824 ($4-6) now LOW priority (toy DIRECTIONALLY predicts floor).

## Provenance
aiden pool CPU, torch, OMP=4, $0. toy_coverage_threshold.py, run.log, result.json.
