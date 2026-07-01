# H_6162 HE-AS-OBJECTIVE — STAGE-1 FAIR cheap-gate RESULT (2026-07-02)

**TIER: 🧱 DIRECTIONAL-FLOOR (NOT-SUPPORTED).** torch mirror = DIRECTIONAL (a_engine_native_learning);
engine-native GPU **NOT authorized** (frozen bar failed). Objective-axis exhausted reconfirmed (DPI meta-law).

## v2 (FREEZE_v2.md — oracle-control sanity, 5 seeds). oracle_ok=True (task compositionally solvable → floor = real recombination gap, not noise/undertrain).

| seed | OFF(λ=0) held-out | best-λ ON held-out | Δ |
|---|---|---|---|
| 7    | 0.032 | 0.118 | +0.086 |
| 4302 | 0.131 | 0.243 | +0.112 |
| 4303 | 0.088 | 0.000 | -0.088 (regress) |
| 4304 | 0.121 | 0.121 | 0.000 |
| 4305 | 0.000 | 0.116 | +0.116 |

chance = 0.111. **n(Δ>=+0.15) = 0/5**, **no_regress = False** (seed 4303 collapses). ON held-out stays
at/near chance except seed 4302 (0.243). FROZEN bar (>=+0.15 on >=2/3 AND no regress) FAILED -> FLOOR.

## Reading
The target-agnostic homomorphism-error aux loss (L_HE = MSE(pair-rep, learned target-blind composition
of part-reps), both trainable) gives noisy sub-threshold lifts and one full collapse — no reliable
held-out compositional gain. Consistent with H_1602 (InfoNCE recomb-obj 9/9 floor) + H_1840 (gamma fair-gate
FALSIFIED): the trunk-training-OBJECTIVE axis does not open G1 recombination. The pair-rep can be made
homomorphically reconstructable from parts without that structure transferring to unseen pairings.

## Provenance
FREEZE v1 mis-specified sanity (baseline-beats-wall -> INCONCLUSIVE; convergence fair-cheap-gate-design-1)
-> FREEZE_v2 oracle-control fix, bar unchanged. aiden pool CPU, torch 2.10, OMP=4, $0. Artifacts:
run_v1.log/result_v1.json (INCONCLUSIVE), run_v2.log/result_v2.json (FLOOR), both toy scripts.
