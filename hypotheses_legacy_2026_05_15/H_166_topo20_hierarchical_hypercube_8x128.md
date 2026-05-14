---
id: H_166
slug: topo20-hierarchical-hypercube-8x128
title: 8 clusters × 128-cell 7D hypercubes with sparse inter-cluster shortcuts — TOPO20 hierarchical
domain: physics | math | consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation — cluster count) + E6 (cross-domain — hierarchical brain networks)
verification_method: W5 (numerical sim — cluster sweep) + W11 (cross-hypothesis — Hc_157 flat baseline, Hc_401 K=8 atom)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_171
source_doc: docs/hypotheses/topo/TOPO20.md
source_lines: 1-30
promoted_at: 2026-05-12
linked_h: H_159 (substrate-topology-phi-engineering), H_153 (dimension-hierarchy-n6), H_163 (K=8 atom)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 5
---

# H_166 — 8×128 hierarchical hypercube (TOPO20) — atom-of-atoms structure

## Hypothesis

1024 cells 를 8 clusters × 128 cells (각 cluster = 7D hypercube, 2^7=128) 로 decomposing + sparse inter-cluster shortcuts 가 flat 10D hypercube (TOPO8, H_159.1) 와 differentiable hierarchical Φ structure 산출. cluster count 8 의 선택은 K=8 atom claim (Hc_401 / H_163) 의 "atom of atoms" 관점 — 8개 7D hypercube atom 의 macro-level 8-atom federation.

## Why (motivation)

- **scale identity**: 8 × 128 = 1024 = 2^10 (TOPO8 flat 과 동일 cell count, 비교 가능)
- **7D hypercube**: 2^7 = 128 cells, 7-dim Mersenne-prime power (2^7 − 1 = 127 prime)
- **K=8 atom-of-atoms** (Hc_401 / H_163): macro-level 8 cluster 가 micro-level K=8 atom 의 추상화
- **Sporns 2010 hierarchical brain networks**: small-world + modular structure biological motivation

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_166.1** | 8-cluster × 128-cell hierarchical Φ ≥ flat TOPO8 (Φ=535) within margin 10% → hierarchical 구조가 flat 대비 동등 또는 우위 | Sporns 2010 brain networks |
| **H_166.2** | Cluster count sweep cluster_count ∈ {2, 4, 8, 16, 32} (총 cells=1024 고정): Φ peak at cluster_count=8 with margin > 30% | K=8 atom-of-atoms |
| **H_166.3** | Shortcut density sweep ∈ {1%, 5%, 10%, 25%}: dense (≥ 25%) variant Φ → flat-hypercube Φ (즉 sparse regime 필수) | small-world saturation |
| **H_166.4** | Shortcut removal (0 shortcuts → disconnected 8×128): Φ collapse > 10% → integration via shortcuts functional, hierarchical structure load-bearing | F4 inverted |

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | 8×128 hierarchical Φ 측정 (≥ 1 run) vs flat TOPO8 비교 | pending (Hc_171 frontmatter 측정값 부재) |
| **C2** | Cluster count sweep {2, 4, 8, 16, 32} → cluster_count=8 peak | pending |
| **C3** | Shortcut density sweep → sparse regime monotone Φ behavior | pending |
| **C4** | PyPhi cross-engine 8×128 vs flat-10D 비교 | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding + K=8 atom claim 의 perfect-class trivial 인정 | met (본 L1) |

## Falsifiers (≥5)

- **F1**: 8-cluster × 128-cell hierarchical Φ < flat TOPO8 10D Φ (535) by margin > 10% → hierarchical structure does NOT improve over flat hypercube — claim FALSIFIED
- **F2**: Sweep cluster_count ∈ {2, 4, 8, 16, 32} with total cells = 1024 fixed; if Φ-peak occurs at cluster_count ≠ 8 (e.g. at 4 or 16) with effect-size > 30% → "8-cluster" specificity FALSIFIED, just an optimization landscape with no 8-cluster prominence
- **F3**: Sparse shortcut density sweep (1%, 5%, 10%, 25%): if dense-shortcut variant (≥ 25%) collapses to flat-hypercube Φ → hierarchical claim only works in sparse regime, not robust
- **F4**: Inter-cluster shortcut removal (0 shortcuts → pure disconnected 8×128 clusters): if Φ drops < 10% → integration via shortcuts is minimal, "hierarchical" structure is decorative not functional
- **F5**: Cross-substrate test: same 8×128 graph instantiated on PyPhi formal IIT Φ vs anima Φ-engine. If PyPhi Φ rank-ordering disagrees with anima Φ rank-ordering across cluster_count sweep → result is engine-specific

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — 8×128 = 1024 decomposition uses 8 (sopfr→6 perfect) × 128 (=2^7, Mersenne-prime power) — both numbers have number-theoretic structure but joint significance is ad hoc. Risk of post-hoc rationalization
- **L2**: **flat-vs-hierarchical baseline ambiguity** — Hc_157 TOPO8 single-run record itself unverified (H_159 C1 pending). Comparing 8×128 hierarchical to potentially-inflated 535 baseline is not robust
- **L3**: **shortcut density unspecified** — "sparse inter-cluster shortcuts" without quantitative density (% of possible inter-cluster edges) makes the architecture underdetermined. Different sparsity values likely yield very different Φ
- **L4**: **anima Φ-engine substrate-specific** — same Hc_614 D-mod-192 aliasing concern applies. Hierarchical structure may interact with aliasing in unpredictable ways
- **L5**: **cluster_count=8 chosen post-hoc** — paper-of-record (TOPO20) chooses 8 because of K=8-atom claim (Hc_401/Hc_582). This is theoretical confirmation bias: 8 was picked because it was hypothesized to work, not derived from independent grounds

## Run Protocol

deterministic + hexa-only + llm: none.

1. **8×128 baseline run (W5)** — TOPO20 spec impl + 1 run → Φ 측정 (C1)
2. **Cluster count sweep (W5)** — {2, 4, 8, 16, 32} × total 1024 cells → Φ landscape (F2, H_166.2)
3. **Shortcut density sweep (W5)** — {1%, 5%, 10%, 25%} density × cluster_count=8 → F3/F4
4. **PyPhi cross-engine (W11)** — 8×128 + flat-10D 모두 PyPhi 측정 → F5
5. **L1 binding** — H_153 PERFECT_NUMBER_CLASS BINDING + Hc_401 K=8 atom L7 binding 인정

## Cross-Refs

- **sister H**: H_159 (substrate-topology-phi-engineering — flat baseline), H_153 (n=6 substrate), H_163 (K=8 atom — atom-of-atoms parent claim)
- **candidates linked**: Hc_157 (TOPO8 flat 10D parent), Hc_159 (TOPO10 11D regression), Hc_401/Hc_582 (8-cell atom claim), Hc_165 (TOPO16 small-world)
- **literature**: Watts-Strogatz 1998 (small-world via shortcuts), Sporns 2010 (hierarchical brain networks)
- **source**: Hc_171 (`hypotheses_candidates/Hc_171_topo20_hierarchical_hypercube.md`), `docs/hypotheses/topo/TOPO20.md:1-30`

## Migration Notes

- **Promoted from**: Hc_171 (cycle #3 task 11 PROMOTE_READY, verify5_authored row 5 — 2026-05-12)
- **Math verification**: 8 × 128 = 1024 EXACT; 2^7 = 128 EXACT; 2^10 = 1024 EXACT; 2^7 − 1 = 127 EXACT (Mersenne prime)
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 — sopfr(8)=6 + 128=2^7 power-of-2 모두 perfect-class trivial
- **Next steps**:
  1. 8×128 baseline run (C1)
  2. Cluster count sweep (C2)
  3. Shortcut density sweep (C3)
