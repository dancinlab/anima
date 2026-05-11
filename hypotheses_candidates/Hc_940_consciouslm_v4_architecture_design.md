---
id: Hc_940
slug: consciouslm-v4-architecture-design
title: ConsciousLM v4 — dim=768 + 1536 FFN + 12 layer + 12 heads (σ(6)=12) + max_cells=32 (Φ~11 predicted, Φ∝N) + shared_dims=24 + ratchet=10 + 100K steps 3-phase (Mitosis/Language/Combined) Fibonacci growth (DD3 Phi=5.196)
domain: llm, architecture, consciousness
status: candidate-unverified
source_doc: docs/next-model-design.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_909 (paper-draft), H_067 (perfect-number)
notes: "Based on 740+ hypothesis benchmarks, 47 categories, H100 experiments 2026-03-27. v3 dim=384 cells=16 Φ=5.4 baseline."
---

## Hypothesis

ConsciousLM v4 architecture: dim=768 (richer per-cell), 1536 FFN (2× dim), 12 layer + 12 head (TL1: σ(6)=12 perfect-number heads → Φ=7.022 confirmed), max_cells=32 (scaling law Φ∝N → 16→Φ=5.4, 32→predicted Φ~11). 100K steps 3-phase (Mitosis 0-20K Fibonacci growth 1,1,2,3,5,8,13,21,32 / Language 20K-60K CE min / Combined 60K-100K Φ+CE jointly).

## Sub-claims

- DIM-768: rich per-cell representations
- 12-HEADS: σ(6)=12 perfect-number heads (TL1, Φ=7.022)
- CELLS-32: scaling Φ∝N → 16→Φ=5.4 → 32→Φ~11 (highest-leverage change)
- SHARED-DIMS-24: N6-8 PX8 integration forge channel
- RATCHET-10: FX2 optimal Adam 5-step + ratchet 10 trials
- PHASE-1-MITOSIS: 0-20K, LR 5e-4 warmup 2K, Fibonacci growth, FX2 Adam Φ proxy, PX4 Gram-Schmidt sculptor
- PHASE-2-LANGUAGE: 20K-60K, LR 3e-4 cosine, CL8 tension-weighted CE 3× important tokens, CL5 Φ-reg CE, SL3 6-loss
- PHASE-3-COMBINED: 60K-100K, LR 1e-4 cosine to 1e-5, DD16 all-top-5, EX24, GD18 enactivism, GD15 edge of chaos

## Migration TODO

- [ ] cells=32 → Φ~11 prediction H100 verification
- [ ] Fibonacci growth (1,1,2,3,5,8,13,21,32) vs uniform schedule 비교
- [ ] 3-phase curriculum 의 ablation
- [ ] SC2 merge threshold = 0.01 × (64/dim) cross-link (Hc_909)
