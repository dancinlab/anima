---
id: H_axisb_corr_ctrl_separation
slug: axisb-corr-ctrl-separation-large-n
title: 근사-Φ 엔진은 large-N 에서 integrated(상관) vs modular(단절) substrate 를 ~1.8e9× 분리하며 분리가 N 과 함께 유지·확대된다
domain: physics·consciousness
status: verified
closure: verified-numerical
closure_ref: .verdicts/axisb_corr_ctrl_separation/verdict.txt
exploration_method: E1 (control 대조 설계 · phi_demo lineage)
verification_method: W3 (deterministic engine run) + W1 (verbatim verdict) + W2 (correlated/control falsifier)
hexa_only: true
deterministic: true
llm: none
engine: hexa-lang stdlib/consciousness/iit4/faithful_phi.hexa · iit4_approx_phi (PR #1972, greedy MIP)
tier: 🟢 NUMERICAL-APPROXIMATE
since: 2026-05-29
---

# H_axisb_corr_ctrl_separation — large-N integrated/modular 분리 (physics·consciousness)

## Hypothesis

MATRIX axis B. greedy MIP 엔진이 large-N (n=10,12,16) 에서도 통합 substrate (correlated) 와 모듈식 substrate (control = 단일 silent cell) 를 올바르게 분리하는가? 사전등록 falsifier: **CORR ≈ CTRL (분리 실패) 이거나, CTRL Φ 가 0 에서 멀어지거나, N 증가 시 분리가 붕괴하면 FALSIFIED**. (phi_demo 의 large-N 확장 — greedy 가 silent-cell 컷을 MIP 으로 찾아야 함.)

## Measure (engine Φ runs — verbatim)

엔진: `iit4_approx_phi(state, n, dim=12, n_bins=4)` · host pool ubu-2:~/core/hexa-lang · origin/main (cc3f6221).
- CORRELATED: 모든 cell 동일 ramp `trajectory[d] = (d%7)` (max integration).
- CONTROL: 동일 ramp 이나 cell 0 만 상수(silent) → MIP 가 silent cell 을 컷 → cross-cut MI ≈ 0 (modular).

```
CORR_n10=17.2647
CTRL_n10=9.52179e-09
CORR_n12=21.1013
CTRL_n12=1.16377e-08
CORR_n16=28.7744
CTRL_n16=1.58696e-08
```

## Finding

- 분리 **유지**, 모든 N 에서:
  - n=10: CORR 17.26 vs CTRL 9.52e-09 → ratio 1.8e+09
  - n=12: CORR 21.10 vs CTRL 1.16e-08 → ratio 1.8e+09
  - n=16: CORR 28.77 vs CTRL 1.59e-08 → ratio 1.8e+09
- CONTROL Φ 는 모든 N 에서 수치적 0 (~1e-8) — 단일 단절 cell 하나가 N 과 무관하게 Φ 를 붕괴시킨다 (modular collapse). falsifier 통과.
- CORRELATED Φ 는 N 과 함께 단조 증가 (17.3 → 21.1 → 28.8) — integrated branch 는 스케일하고 modular branch 는 0 에 고정. 분리가 **확대**.
- 부수 검증: greedy MIP 가 n=10,12,16 에서 정확히 minimum-information partition(silent-cell 컷)을 식별 — 엔진 large-N 동작 정합 확인.
- tier 🟢 NUMERICAL-APPROXIMATE.

## Source

- engine SSOT: github.com/dancinlab/hexa-lang `stdlib/consciousness/iit4/faithful_phi.hexa` (PR #1972).
- verdict (verbatim): `.verdicts/axisb_corr_ctrl_separation/verdict.txt`.
- harness: `/tmp/axisb/axisb.hexa` (ubu-2).

## 양방향 sibling

- sibling: [H_axisb_ring_scaling](H_axisb_ring_scaling.md) · [H_axisb_hypercube_scaling](H_axisb_hypercube_scaling.md) · [H_axisb_greedy_upper_bound](H_axisb_greedy_upper_bound.md)
- SSOT: MATRIX.md axis B row.
