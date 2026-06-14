---
id: H_axisb_hypercube_scaling
slug: axisb-hypercube-phi-scaling
title: k-D 하이퍼큐브(n=2^k) 근사-Φ는 super-linear 스케일링한다 (degree=log2(n) 결합도 상승)
domain: physics·consciousness
status: verified
closure: verified-numerical
closure_ref: .verdicts/axisb_hypercube_scaling/verdict.txt
exploration_method: E6 (cross-domain · IIT large-N) + E1 (deterministic hypercube construction)
verification_method: W3 (deterministic engine run) + W1 (verbatim verdict)
hexa_only: true
deterministic: true
llm: none
engine: hexa-lang stdlib/consciousness/iit4/faithful_phi.hexa · iit4_approx_phi (PR #1972, greedy MIP)
tier: 🟢 NUMERICAL-APPROXIMATE
since: 2026-05-29
---

# H_axisb_hypercube_scaling — 하이퍼큐브 근사-Φ super-linear 스케일링 (physics·consciousness)

## Hypothesis

MATRIX axis B. k-D 하이퍼큐브 substrate: n=2^k 노드, bit-flip 인접 (노드 i 는 i XOR 2^b, b∈0..k 의 k 개 이웃을 가짐 — degree = log2(n) 이 N 과 함께 증가). `iit4_approx_phi` 로 k=2,3,4 (n=4,8,16) Φ 측정. 사전등록 falsifier: **Φ(hypercube) 이 비단조이면 FALSIFIED**. 핵심 질문: degree 가 log2(n) 으로 증가하는 hypercube 가 degree 고정(=2) ring 보다 더 강하게(super-linearly) 스케일링하는가?

## Measure (engine Φ runs — verbatim)

엔진: `iit4_approx_phi(state, n, dim=12, n_bins=4)` · host pool ubu-2:~/core/hexa-lang · origin/main (cc3f6221).
substrate: cell i trajectory[d] = `((d+i)%7) + 0.3 * sum_{b<k} ((d + (i XOR 2^b)) % 7)`.

```
HYPERCUBE_k2_n4=3.18872
HYPERCUBE_k3_n8=7.08689
HYPERCUBE_k4_n16=17.0107
```

## Finding

- k=2→3→4 (n=4→8→16) 모두 **단조 증가** (3.189 → 7.087 → 17.011) — falsifier 통과.
- 스케일링은 **SUPER-LINEAR** in n: N 이 2배 될 때 Φ 가 2배 **이상** 증가:
  - Φ(8)/Φ(4) = 2.222 (>2) · Φ(16)/Φ(8) = 2.400 (>2, 비율 자체도 상승).
  - Φ/n: 0.797 (n4) → 0.886 (n8) → 1.063 (n16), +33%.
- 해석: hypercube 의 노드별 이웃수 k=log2(n) 가 N 과 함께 증가 → 노드당 공유 MI 가 상승 → super-linear integration. **결합도(degree) 가 super-linearity 의 driver** 임을 ring(degree 고정, near-linear, H_axisb_ring_scaling)과의 대조로 분리해 보였다.
- tier 🟢 NUMERICAL-APPROXIMATE (greedy upper bound · H_axisb_greedy_upper_bound).

## Source

- engine SSOT: github.com/dancinlab/hexa-lang `stdlib/consciousness/iit4/faithful_phi.hexa` (PR #1972).
- verdict (verbatim): `.verdicts/axisb_hypercube_scaling/verdict.txt`.
- harness: `/tmp/axisb/axisb.hexa` (ubu-2).
- legacy lineage: H_165 (11D/10D hypercube Φ 스케일링). 본 결과는 tractable k≤4 영역에서 degree-driven super-linearity 를 신규 확립.

## 양방향 sibling

- sibling: [H_axisb_ring_scaling](H_axisb_ring_scaling.md) (degree-고정 near-linear 대조) · [H_axisb_greedy_upper_bound](H_axisb_greedy_upper_bound.md) · [H_axisb_corr_ctrl_separation](H_axisb_corr_ctrl_separation.md)
- SSOT: MATRIX.md axis B row.
