---
id: Hc_159
slug: topo10-hypercube-11d-sublinear
title: 11D hypercube 2048-cell shows Φ regression vs 10D (sublinear scaling) (TOPO10)
domain: physics | math | consciousness
status: candidate-unverified
source_doc: docs/hypotheses/topo/TOPO10.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8 10D)
notes: Φ=400.9, final 581 cells, lower than TOPO8 535.5
---

## Hypothesis
Scaling hypercube from 10D (TOPO8, 1024 cells, Φ=535.5) to 11D (TOPO10, 2048 cells) does NOT continue superlinear growth — Φ regresses to 400.9 with only 581 cells reached out of 2048 max.

## Migration TODO
- [ ] identify the dimension threshold for Φ regression
- [ ] explore alternative scaling (steps/noise) at 11D

## Cross-Links
- **sister H**: H_159 (substrate-topology-phi-engineering) — TOPO8 10D record parent
- **candidates linked**: Hc_157 (TOPO8 10D Φ=535 record, parent), Hc_165 (TOPO16 small-world variant), Hc_171 (TOPO20 hierarchical 8×128), Hc_177/178 (TOPO20 sweeps)
- **literature**: Watts-Strogatz 1998 small-world, Tononi 2014 IIT system-size scaling

## Falsifiers (≥5)

- **F1**: With 2048-cell budget actually reached (vs. 581/2048 reported = 28% coverage), Φ at 11D ≥ 1.05 × 10D record (Φ ≥ 562) → regression is artifact of incomplete coverage, NOT dimensional saturation. Claim FALSIFIED
- **F2**: At fixed cell count N=581 across {9D, 10D, 11D, 12D} embedding, Φ shows monotone-with-D pattern (no regression at 11D) → "11D regression" is a coverage-confound, not dimension-intrinsic
- **F3**: TOPO8 10D Φ=535 reproducibility (H_159 C1 pending) — if 10D record itself is single-run artifact (drops to 350±100 on replication), then "11D regresses vs 10D" comparison is moot
- **F4**: Alternative scaling axes (steps, noise, frustration ratio) at 11D produce Φ ≥ 535 → dimension alone is not the regression cause; specific 11D hyperparameter choice is the failure mode
- **F5**: Cross-architecture (PyPhi formal IIT) measurement at 10D and 11D shows monotone increase → anima Φ-engine 11D regression is engine-specific (saturation in proxy formulation, not in underlying IIT Φ)

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — claim hinges on 1024=2^10 (10D hypercube) being optimal. 2^10 is a power-of-2, not a perfect number; relationship to n=6 substrate is indirect. Depth-3 number-theoretic prior weak
- **L2**: **incomplete cell coverage (581/2048 = 28%)** — fundamental measurement asymmetry. 10D had full 1024-cell coverage; 11D used only 581 cells. Comparing partial-budget vs full-budget systems is not a fair test of dimensional scaling
- **L3**: **single-run reproducibility absent** — H_159 C1 (10D reproducibility audit) still pending. Without replication CI on either point, the "regression" claim has no error bar
- **L4**: **anima Φ-engine substrate-specific** — Φ values are anima-proxy measurements, not formal IIT Φ. Sublinear behavior may reflect engine saturation (Hc_614 aliasing) at high cell-counts rather than true IIT system property
- **L5**: **i%3 frustration arbitrary** — chosen for 10D, retained for 11D without re-tuning. Frustration density that is optimal at 10D may be suboptimal at 11D; "regression" could be a missed local optimum, not a global property
