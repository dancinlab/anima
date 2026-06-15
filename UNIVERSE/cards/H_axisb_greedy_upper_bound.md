---
id: H_axisb_greedy_upper_bound
slug: axisb-greedy-strict-upper-bound
title: greedy MIP 근사-Φ는 ring substrate 에서 exact Φ 의 STRICT upper bound 다 (~13% overshoot · smoke의 greedy==exact 는 substrate 의존)
domain: physics·consciousness
status: verified
closure: verified-numerical
closure_ref: .verdicts/axisb_greedy_upper_bound/verdict.txt
exploration_method: E1 (calibration · exact↔approx 직접 비교)
verification_method: W3 (deterministic engine run) + W1 (verbatim verdict) + W5 (honest-c3 calibration)
hexa_only: true
deterministic: true
llm: none
engine: hexa-lang stdlib/consciousness/iit4/faithful_phi.hexa · iit4_faithful_phi_from_mi(exact) vs iit4_approx_phi_from_mi(greedy) (PR #1972)
tier: 🟢 NUMERICAL-APPROXIMATE
since: 2026-05-29
---

# H_axisb_greedy_upper_bound — greedy MIP 는 exact Φ 의 strict upper bound (calibration · physics·consciousness)

## Hypothesis

MATRIX axis B calibration. n≤8 에서 exact MIP 열거(`iit4_faithful_phi_from_mi`)와 greedy descent(`iit4_approx_phi_from_mi`)를 **동일 MI 행렬**로 직접 비교해, large-N greedy Φ 값을 어떻게 읽어야 하는지 정량 보정한다. 엔진 docstring 의 HONEST BOUND 주장 (greedy ≥ exact, upper bound) 을 ring substrate 에서 검증. 사전등록 falsifier: **greedy < exact 가 한 번이라도 관측되면 upper-bound 주장 FALSIFIED**.

## Measure (engine Φ runs — verbatim)

엔진: ring substrate (axisb_ring_scaling 와 동일 builder), n≤8 (exact tractable) · host pool ubu-2:~/core/hexa-lang · origin/main (cc3f6221).

```
RING_n6_EXACT=4.99168
RING_n6_GREEDY=5.6616
RING_n8_EXACT=7.69087
RING_n8_GREEDY=8.65654
```

## Finding

- ring substrate 에서 greedy 는 exact 보다 **항상 큼** (Φ_greedy > Φ_exact) — upper bound 주장 통과 (반증 안 됨):
  - n=6: exact 4.99168 vs greedy 5.66160 → gap +0.66992 (+13.4%)
  - n=8: exact 7.69087 vs greedy 8.65654 → gap +0.96567 (+12.6%)
- **중요 calibration 결과**: smoke-test 의 "n4-8 greedy==exact" 주장은 **substrate 의존**이다 (smoke substrate 에서는 성립했으나 ring family 에서는 불성립). degree-2 nearest-neighbor ring 에서는 greedy descent 가 global MIP 보다 ~13% 높은 LOCAL MIP 컷에 갇힌다.
- 따라서 large-N (RING/HYPERCUBE/CORR) Φ 절대값은 **greedy upper bound** — 참 Φ 를 ~13% order 만큼 overshoot 가능. 단, 대략 일정한 곱셈 bias 는 순서를 뒤집지 않으므로 **단조/super-linear 스케일링 trend 는 보존**. 절대값은 🟢, 절대 🔵 아님.
- honest C3: degree, dim, n_bins 가 다른 substrate 에서는 gap% 가 달라질 수 있음 — 본 13% 는 ring-degree-2 specific.

## Source

- engine SSOT: github.com/dancinlab/hexa-lang `stdlib/consciousness/iit4/faithful_phi.hexa` (PR #1972, exact `iit4_faithful_phi_from_mi` + greedy `iit4_approx_phi_from_mi` HONEST BOUND docstring).
- verdict (verbatim): `.verdicts/axisb_greedy_upper_bound/verdict.txt`.
- harness: `/tmp/axisb/robust.hexa` (ubu-2).

## 양방향 sibling

- sibling: [H_axisb_ring_scaling](H_axisb_ring_scaling.md) · [H_axisb_hypercube_scaling](H_axisb_hypercube_scaling.md) · [H_axisb_corr_ctrl_separation](H_axisb_corr_ctrl_separation.md)
- SSOT: MATRIX.md axis B row (greedy = 🟢 upper bound, never 🔵).
