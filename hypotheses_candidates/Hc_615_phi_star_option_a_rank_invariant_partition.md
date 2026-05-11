---
id: Hc_615
slug: phi-star-option-a-rank-invariant-partition
title: Option A — D/8 disjoint contiguous chunks + per-substrate scale calibration 이 phi-star geometry-invariant 해결
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 121-163
promoted_at: 2026-05-11
linked_h: Hc_614, paradigm v11 G3 carry 41.86
notes: Rank 1 — fastest fix, ~25 lines, $0. Provisional — cross-substrate magnitude calibration-dependent.
---

## Hypothesis
chunk_size = D // 8, disjoint partition, pairwise cosine mean over off-diagonal, additive scale per substrate (phi = baseline + scale[s] × mean_pair_cos) 가 aliasing 제거. CLM v4 96-dim chunks, Pythia 70m 64, Pythia 1.4b 256.

## Falsifiable Tests
- Test A.1: 5-substrate calibration 후 within-substrate phi 분포가 reasonable (range ≥ 1pp)
- Test A.2: 동일 input 다른 seed 5 회 averaged phi std/mean ≤ 5%
- Test A.3: D mod 8 ≠ 0 substrate (D=1280) 에서도 작동

## Migration TODO
- [ ] anima-core/runtime/clm_v4_mount.hexa:251-264 replace
- [ ] tool/transient_py/anima_phi_star_universal.py 작성
- [ ] state/anima_phi_star_substrate_scale_2026_05_05/scale_table.json populate (5 substrate × 16 prompt)
