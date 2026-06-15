---
id: H_axisb_ring_scaling
slug: axisb-ring-phi-scaling
title: 링(ring) family 근사-Φ는 N=6..16 에서 단조 증가하며 near-linear 스케일링한다
domain: physics·consciousness
status: verified
closure: verified-numerical
closure_ref: .verdicts/axisb_ring_scaling/verdict.txt
exploration_method: E6 (cross-domain · IIT large-N) + E1 (deterministic substrate construction)
verification_method: W3 (deterministic engine run) + W1 (verbatim verdict) + W9 (DIM robustness replication)
hexa_only: true
deterministic: true
llm: none
engine: hexa-lang stdlib/consciousness/iit4/faithful_phi.hexa · iit4_approx_phi (PR #1972, greedy MIP)
tier: 🟢 NUMERICAL-APPROXIMATE
since: 2026-05-29
---

# H_axisb_ring_scaling — 링 family 근사-Φ near-linear 단조 스케일링 (physics·consciousness)

## Hypothesis

MATRIX axis B (large-N faithful Φ). n>8 영역에서 exact MIP 열거가 불가하므로 hexa-lang `iit4_approx_phi` (greedy MIP, PR #1972) 로 결정론적 ring substrate 의 Φ(N) 을 측정한다. ring = n 개 cell 의 cycle, nearest-neighbor (degree-2) 결합. 사전등록 falsifier: **Φ_approx(ring, n) 이 n=6..16 에서 비단조(어딘가 감소)하면 FALSIFIED**. 부수 질문: 스케일링이 sub-linear 인가 super-linear 인가 linear 인가?

## Measure (engine Φ runs — verbatim)

엔진: `iit4_approx_phi(state, n, dim=12, n_bins=4)` · host pool ubu-2:~/core/hexa-lang · origin/main faithful_phi (cc3f6221).
substrate: cell i trajectory[d] = `((d+i)%7) + 0.5*(((d+(i+1)%n)%7) + ((d+(i-1+n)%n)%7))`.

```
RING_n6=4.99168
RING_n7=6.27584
RING_n8=7.69087
RING_n9=10.757
RING_n10=11.4576
RING_n11=11.684
RING_n12=12.859
RING_n13=13.6515
RING_n14=16.3131
RING_n15=17.7722
RING_n16=19.5549
```

DIM robustness (ring n=12): DIM8=13.962 · DIM12=12.859 · DIM16=13.6379 (±8%, 구조적).

## Finding

- 11 개 샘플 (n=6..16) 모두 **단조 증가** — falsifier 통과 (반증 안 됨). 비단조 지점 0.
- 스케일링은 **near-LINEAR**: slope (19.55−4.99)/(16−6) = 1.456 Φ/cell. Φ/n 은 0.832 (n6) → 1.222 (n16) 로 ~1.47× 완만 상승 (약하게 super-linear 한 잔차를 갖는 dominant-linear). degree 가 N 과 무관하게 고정(=2)인 ring 의 특성과 정합 — H_axisb_hypercube_scaling 의 degree-증가 super-linearity 와 대조.
- tier 🟢 NUMERICAL-APPROXIMATE. greedy 는 upper bound (H_axisb_greedy_upper_bound 참조) — 절대값은 ~13% overshoot 가능하나 단조/스케일링 순서는 보존.

## Source

- engine SSOT: github.com/dancinlab/hexa-lang `stdlib/consciousness/iit4/faithful_phi.hexa` (PR #1972, `iit4_approx_phi`/`iit4_approx_phi_from_mi`).
- verdict (verbatim): `.verdicts/axisb_ring_scaling/verdict.txt`.
- harness: `/tmp/axisb/axisb.hexa` + `/tmp/axisb/robust.hexa` (ubu-2).
- legacy 비교: H_165 "11D hypercube 2048-cell Φ regression vs 10D sublinear" (large-N Φ 스케일링 lineage). 본 결과는 tractable n≤16 영역에서 ring near-linear trend 를 신규 확립.

## 양방향 sibling

- sibling: [H_axisb_hypercube_scaling](H_axisb_hypercube_scaling.md) (degree-증가 super-linear 대조) · [H_axisb_greedy_upper_bound](H_axisb_greedy_upper_bound.md) (calibration) · [H_axisb_corr_ctrl_separation](H_axisb_corr_ctrl_separation.md)
- SSOT: MATRIX.md axis B row (large-N faithful Φ scaling findings).
