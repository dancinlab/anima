---
id: Hc_1288
slug: phi-proxy-is-variance-artifact-partial-correlation
title: cheap phi_proxy 가 emergence 와 직교한 이유는 그것이 통합이 아니라 raw state-variance 를 측정하기 때문 — variance 통제 partial-correlation 으로 진단
domain: information · consciousness · substrate · meta
status: candidate-unverified
seed: H_912 (phi_proxy ⊥ emergence, r=-0.277 "proxy pathology") — *왜* 직교했는지의 mechanistic 진단 (variance-confound 가설)
axes_seed: UNIVERSE/AXES.md R5 (information) · R8 (meta) — H_912 root-cause lane
exploration_method: E5 (confound-isolation probe) + E0 (partial-correlation 진단)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (variance 통제 후 phi_proxy↔emergence 잔존상관 → 0) OR 🔴 CLOSED-NEGATIVE (variance 통제해도 잔존상관 유지 → variance-artifact 가설 기각)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

H_912 는 cheap variance-기반 phi_proxy 가 emergence(LZ) 와 직교함(r=-0.277)을 측정했으나 *원인*을 닫지 않았다. 가설 H1: phi_proxy 는 통합(integration)이 아니라 substrate 의 **raw state-variance** 를 측정하며, 이 variance 가 emergence 와 무관하기 때문에 직교가 발생한다. 검정: substrate panel 에서 (a) `r(phi_proxy, emergence)`, (b) `r(state_variance, emergence)`, (c) variance 를 통제한 **편상관** `r(phi_proxy, emergence | state_variance)` 를 측정. H1 예측: phi_proxy 의 emergence-신호가 거의 전부 variance 로 설명됨 → 편상관 |r| < 0.1 (phi_proxy 의 고유 통합-신호 ≈ 0).

## Why (H_912 autopsy)

이것이 H_912 의 root-cause 진단이다. "proxy 가 직교한다"(현상) → "proxy 는 variance 를 잰다"(mechanism). 편상관이 H1 을 지지하면 phi_proxy 의 폐기가 *원리적으로* 정당화되고, faithful big-Φ 만이 통합-신호를 보유한다는 H_288 의 대비가 강화된다. faithful big-Φ 도 같은 partial-correlation 에 넣어 대조군으로 — big-Φ 의 emergence-신호는 variance 통제 후에도 살아남아야(예측).

## Pre-Registered Falsifier

- **F1288.1 (VARIANCE-CONFOUND)**: 편상관 `r(phi_proxy, emergence | variance)` 의 |값| ≥ 0.3 → H1 FALSIFIED (phi_proxy 는 variance 너머의 고유 신호를 보유 — 직교는 variance-artifact 가 아님).
- **F1288.2 (FAITHFUL-CONTROL)**: 대조군 `r(big_Φ, emergence | variance)` 이 |값| < 0.3 으로 같이 붕괴하면 → 진단 설계 무효(variance 통제가 모든 신호를 죽임 = over-control). big-Φ 신호는 잔존해야 진단 유효.
- **F1288.3 (DETERMINISM)**: re-run byte-identical 아니면 무효.

## Circularity Guard

state_variance 와 phi_proxy 의 정의가 부분적으로 겹칠 수 있음 — 이것이 정확히 H1 의 *검정 대상*이다(겹침이 클수록 H1 지지). emergence(LZ) 는 둘과 독립 정의이므로 편상관의 외생변수로 유효. variance≈proxy 동일성이 *증명*되면 그 자체가 닫힌 진단(동어반복 폭로).

## Migration TODO
- [ ] state_variance + phi_proxy + LZ-emergence + big_Φ 4-tuple 하네스
- [ ] Pearson 편상관 (variance 통제) inline, 10-rule panel
