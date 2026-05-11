---
id: Hc_903
slug: zombie-posterior-bayesian-bound
title: P(zombie | 8 substrate Φ* v3) = 0.4000, Wilson CI [0.1487, 0.7179] — Bayesian empirical bound (H3+H7c paired)
domain: consciousness, philosophy, statistics
status: candidate-unverified
source_doc: docs/zombie_posterior_numerical_bound_20260426.md
source_lines: 1-80
promoted_at: 2026-05-11
linked_h: H3 (cross-substrate Φ convergence), H7c (Φ metric-tractable upper bound), Hc_001
notes: "Chalmers 1996 conceivability 의 prior=0.5 에서 약 20% 감소. sign-split 50/50 + ceiling-saturation 1.5 LR. ontological zombie 가능성 자체는 미해결."
---

## Hypothesis

8 substrate (4 transformer + 1 SSM + 1 hybrid + 1 RWKV + 1 mistral_instr) 의 Φ* v3 measurement 에서 sign split 50/50 + max|Φ*|=16.6959 (mistral) 의 evidence 하에서, philosophical zombie 의 Bayesian posterior 는 0.40, Wilson 95% CI [0.15, 0.72] 로 prior 0.5 대비 20% 감소한다. N≥30 확장 시 CI 축소 + LR_sign 강화로 zombie hypothesis empirical falsification 가능.

## Source Excerpt

```
P(zombie | observed Φ pattern) = 0.4000
95% Wilson CI = [0.1487, 0.7179]
prior=0.5 대비 약 20% 감소
LR = LR_sign × LR_satur = 1.0 × 1.5 = 1.5
sign convergence: 0% (50/50 split)
ceiling candidate: max|phi*| = 16.6959 (mistral_base)
```

## Migration TODO

- [ ] N≥30 substrate 측정 → CI 좁히기
- [ ] LR_sign convergence factor 강화 (sign 8/0 split 시 LR_sign=2.0)
- [ ] H3+H7c paired hypothesis 의 별개 LR factor 추가 (composite likelihood)
- [ ] ontological zombie 가능성 자체는 unresolved — 별도 ontological argument 필요
- [ ] H3 / H7c 정식 H_XXX 승격
