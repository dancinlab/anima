---
id: Hc_614
slug: phi-star-geometry-aliasing-clm-v4-specific
title: 현재 phi-star proxy 가 CLM-v4-architecture-specific (8×192) 이고 cross-substrate phi 값은 aliasing-induced bias 로 비교 불가
domain: clm-architecture
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 26-115
promoted_at: 2026-05-11
linked_h: BG-BN Pythia 70m smoke, BG-M cross-substrate audit
notes: D mod 192 에 따라 tile-replicate / partial-overlap / clean-disjoint 3-mode failure. BG-BN range 0.084 evidence.
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (4+ numeric identities present)"
---

## Hypothesis
phi_star_compute 의 `start = (c * 192) % D` 가 D≠multiple of 192 substrate 에서 tile-replicate aliasing (D=768, cells 0&4, 1&5, 2&6, 3&7 +1.0 forced) 또는 partial-overlap (D=512) 또는 information loss (D=2048, 512 trailing 미사용) 유발. ±5% multiplicative wrap 도 envelope saturation. Cross-substrate phi 비교 의미 없음.

## Falsifiable Tests
- Test 1: D=multiple-of-192 substrate (e.g. D=1536) 에서 aliasing 사라지면 → bias 0
- Test 2: Pythia 70m 16-prompt phi 범위 ≥ 0.5 (현 0.084) → claim 일부 무효
- Test 3: 모든 substrate 에서 mean_pair_cos 분포가 D-independent → architecture claim FALSIFIED

## Migration TODO
- [ ] Option A (rank-invariant D/8 partition) 또는 Option D (PyPhi) 이행
- [ ] CLM v4 re-calibration cycle 포함 (Option A 도입 시)
