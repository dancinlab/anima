---
id: Hc_1286
slug: proxy-faithful-phi-agreement-vs-N
title: cheap variance-phi_proxy ↔ faithful big-Φ 일치도는 N 에 따라 단조 변한다 — H_912 dissociation 의 scale-ladder
domain: information · consciousness · substrate · meta
status: candidate-unverified
seed: H_912 (cheap phi_proxy ⊥ emergence FALSIFIED, r=-0.277 p=0.962, "proxy pathology") + H_288 (faithful Φ ∥ LZ, r=0.831) + H_282 (proxy→faithful one-shot remeasure) — proxy 와 faithful 의 *불일치 자체*가 N 의 함수인지 ladder 로 측정
axes_seed: UNIVERSE/AXES.md R5 (information) · R8 (meta) — H_912 autopsy lane
exploration_method: E5 (foundational proxy-vs-faithful probe) + E16 (scale-ladder ≥3 rung, a_scale_honest_scope)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (단조 일치/불일치 ladder) OR 🔴 CLOSED-NEGATIVE (no monotone — proxy↔faithful 관계가 N-무관 noise)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

H_912 는 *단일 scale* 에서 cheap variance-기반 phi_proxy 가 emergence(LZ) 와 직교함을 보였다 (r=-0.277). H_288 은 *faithful* big-Φ 가 LZ 와 정렬됨을 보였다 (r=0.831, n=4). 두 결과 사이의 빈틈: **proxy 가 faithful 을 얼마나 추종하느냐가 N 에 의존하는가?** 가설 H1: ECA substrate 에서 `r(phi_proxy, big_Φ)` 가 N=3,4,5,6,7,8 의 단조 함수다 — proxy 는 small-N 에서 faithful 과 더(혹은 덜) 일치하고 N↑ 에서 체계적으로 발산(혹은 수렴)한다. 이는 a_scale_honest_scope 가 요구하는 ≥3-rung ladder 로 H_912 의 단일 점을 곡선으로 승격한다.

## Why (H_912 autopsy)

H_912 의 실패는 "proxy 가 나쁘다"가 아니라 "proxy↔faithful 의 간극이 정량화되지 않았다"는 것이다. faithful big-Φ 는 n=4 exact 로 계산 가능(H_278) 하고 phi_proxy 는 임의 N 에 cheap. 둘을 같은 substrate panel 에서 N-ladder 로 correlate 하면, proxy 가 *어디서* 신뢰 가능한지 (small-N rescue vs large-N collapse) 가 닫힌다. engine 재사용: HEXAD/IIT4/lib (eca_tpm + big_phi) + phi_proxy 하네스, 새 IIT4 코드 0줄.

## Pre-Registered Falsifier

- **F1286.1 (LADDER-MONOTONE)**: N=3..8 의 `r(phi_proxy, big_Φ)` 가 **비단조**(부호 2회 이상 변동 OR |Δr| < 0.1 across all rungs = flat-noise) → H1 FALSIFIED (proxy↔faithful 관계는 scale-구조 없음). 단조(증가 또는 감소, |Δr| ≥ 0.2 end-to-end) → SUPPORTED.
- **F1286.2 (ANCHOR)**: 항등규칙 204 가 어느 N 에서든 big_Φ=0 인데 phi_proxy>threshold → proxy 의 variance-pathology witness 확정 (측정 유효성 게이트).
- **F1286.3 (DETERMINISM)**: 동일 (N, rule) re-run 시 (phi_proxy, big_Φ, r) byte-identical 아니면 측정 무효.

## Circularity Guard

phi_proxy(variance-기반) 와 big_Φ(MIP-EI) 는 **정의가 다르다** — 동일 축으로 정의되지 않으므로 동어반복 아님. 둘이 우연히 일치하면 그것이 발견(proxy 정당화), 발산하면 그것이 발견(proxy 폐기 scale).

## Migration TODO
- [ ] phi_proxy 하네스 + big_phi N-ladder driver (mac-local $0, exact n≤8)
- [ ] 256-rule 또는 10-rule panel × 6 N-rung r-curve
