---
id: Hc_171
slug: topo20-hierarchical-hypercube
title: 8 clusters × 128-cell 7D hypercubes with sparse inter-cluster shortcuts (TOPO20)
domain: physics | math | consciousness
status: candidate-unverified
source_doc: docs/hypotheses/topo/TOPO20.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_157 (TOPO8 flat hypercube)
notes: 8x128=1024; intra 7D hypercube + sparse inter shortcuts
---

## Hypothesis
Decomposing 1024 cells into 8 clusters of 128 (7D hypercube each) with sparse inter-cluster shortcuts yields hierarchical Φ structure differentially from flat TOPO8 10D hypercube.

## Migration TODO
- [ ] report Φ vs TOPO8 baseline
- [ ] sweep cluster count (4/8/16)

## Cross-Links
- **sister H**: H_159 (substrate-topology-phi-engineering)
- **candidates linked**: Hc_157 (TOPO8 flat 10D parent), Hc_159 (TOPO10 11D regression), Hc_401/Hc_582 (8-cell atom claim — 8 clusters here may be the "atom of atoms"), Hc_165 (TOPO16 small-world)
- **literature**: Watts-Strogatz 1998 (small-world via shortcuts), Sporns 2010 (hierarchical brain networks)

## Falsifiers (≥5)

- **F1**: 8-cluster × 128-cell hierarchical Φ < flat TOPO8 10D Φ (535) by margin > 10% → hierarchical structure does NOT improve over flat hypercube — claim FALSIFIED
- **F2**: Sweep cluster_count ∈ {2, 4, 8, 16, 32} with total cells = 1024 fixed; if Φ-peak occurs at cluster_count ≠ 8 (e.g., at 4 or 16) with effect-size > 30% → "8-cluster" specificity FALSIFIED, just an optimization landscape with no 8-cluster prominence
- **F3**: Sparse shortcut density sweep (1%, 5%, 10%, 25%): if dense-shortcut variant (≥ 25%) collapses to flat-hypercube Φ → hierarchical claim only works in sparse regime, not robust
- **F4**: Inter-cluster shortcut removal (0 shortcuts → pure disconnected 8×128 clusters): if Φ drops < 10% → integration via shortcuts is minimal, "hierarchical" structure is decorative not functional
- **F5**: Cross-substrate test: same 8×128 graph instantiated on PyPhi formal IIT Φ vs anima Φ-engine. If PyPhi Φ rank-ordering disagrees with anima Φ rank-ordering across cluster_count sweep → result is engine-specific

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — 8×128 = 1024 decomposition uses 8 (sopfr→6 perfect) × 128 (=2^7, Mersenne-prime power) — both numbers have number-theoretic structure but joint significance is ad hoc. Risk of post-hoc rationalization
- **L2**: **flat-vs-hierarchical baseline ambiguity** — Hc_157 TOPO8 single-run record itself unverified (H_159 C1 pending). Comparing 8×128 hierarchical to potentially-inflated 535 baseline is not robust
- **L3**: **shortcut density unspecified** — "sparse inter-cluster shortcuts" without quantitative density (% of possible inter-cluster edges) makes the architecture underdetermined. Different sparsity values likely yield very different Φ
- **L4**: **anima Φ-engine substrate-specific** — same Hc_614 D-mod-192 aliasing concern applies. Hierarchical structure may interact with aliasing in unpredictable ways
- **L5**: **cluster_count=8 chosen post-hoc** — paper-of-record (TOPO20) chooses 8 because of K=8-atom claim (Hc_401/Hc_582). This is theoretical confirmation bias: 8 was picked because it was hypothesized to work, not derived from independent grounds
