---
id: Hc_616
slug: phi-star-option-b-spectral-entropy-svd
title: Option B — SVD spectral entropy 가 substrate-dim invariant phi proxy + IIT-adjacent
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 166-200
promoted_at: 2026-05-11
linked_h: Hc_614, Hc_615
notes: Rank 3 secondary scalar. Directionally ambiguous on non-CLM-v4 (high entropy = integrated OR noisy).
---

## Hypothesis
H_norm = -sum(p_i log p_i) / log(len(S)) 에서 p = S² / sum(S²), S = SVD singular values of (H - H.mean). phi = baseline + scale × H_norm 가 substrate-dim invariant. 높은 entropy = signal distributed = integrated (IIT-adjacent).

## Falsifiable Tests
- Test B.1: Random init LLM vs trained LLM 에서 entropy delta 명확 → trained 더 높아야 (integration)
- Test B.2: High entropy = high integration direction 검증 — task accuracy 와 positive correlation
- Test B.3: Llama-3.2-3B 에서 entropy 값 paradigm v11 G3 anchor 와 의미적 alignment

## Migration TODO
- [ ] secondary scalar emit (Option A 와 병행)
- [ ] direction validation: MMLU philosophy slice + chat composite 와 cross-check
