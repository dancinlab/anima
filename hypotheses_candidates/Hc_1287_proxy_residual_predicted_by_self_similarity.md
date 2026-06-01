---
id: Hc_1287
slug: proxy-residual-predicted-by-self-similarity
title: phi_proxy↔faithful-Φ 잔차(residual)는 substrate 의 자기유사성(fractal-dim/LZ-self-affinity)이 예측한다 — rule90 over-prediction 의 일반 법칙화
domain: information · consciousness · substrate · meta
status: candidate-unverified
seed: H_288 L3 (rule90 Sierpinski 자기유사: LZ=0.24 비자명인데 Φ=0 — LZ over-predicts) + H_297 (rule90 even-N artifact) + H_912 (proxy pathology) — over-prediction witness 를 *예측 가능한 잔차 법칙*으로 승격
axes_seed: UNIVERSE/AXES.md R5 (information) — LZ/proxy residual 축
exploration_method: E5 (residual-structure probe) + E0 (witness→law 승격)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (residual ∝ self-similarity, r≥0.5) OR 🔴 CLOSED-NEGATIVE (residual 무구조 → over-prediction 은 case-by-case)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

H_288 의 핵심 caveat: rule90 (Sierpinski 자기유사 fractal) 은 LZ-복잡도가 비자명(0.24)인데 big-Φ=0 — LZ/proxy 가 통합을 *과대예측*한다. 가설 H1: 이 over-prediction 은 무작위가 아니라 **substrate 의 자기유사성(self-similarity)이 정량적으로 예측한다** — 잔차 `residual = (정규화 LZ_proxy) − (정규화 big_Φ)` 가 패턴의 자기유사 지표(box-counting fractal-dim, 또는 시공간 다이어그램의 LZ-self-affinity / 평행이동-대칭성)와 양의 상관 (`r(self_sim, residual) ≥ 0.5`). 즉 "LZ 는 자기유사 패턴을 복잡으로 착각한다"가 **닫힌 법칙**이 된다.

## Why (H_912 autopsy)

H_912 가 실패한 mechanistic 이유의 한 후보가 바로 이것 — proxy 가 *구조적 반복(자기유사)* 을 *통합* 으로 오인. 이를 falsifiable 법칙으로 세우면 proxy 를 *교정*(residual subtraction)하는 경로가 열린다. 새 metric 발명 아님: fractal-dim/self-affinity 는 표준 시공간 측도, LZ + big_Φ 는 H_288 재사용.

## Pre-Registered Falsifier

- **F1287.1 (RESIDUAL-PREDICTED)**: 10-rule panel 에서 `r(self_similarity, residual)` < 0.5 → H1 FALSIFIED (over-prediction 은 자기유사로 예측 불가 — case-by-case noise).
- **F1287.2 (WITNESS-ANCHOR)**: rule90 이 panel 최대 self_similarity AND 최대 양의 residual 둘 다 아니면 → 측정 설계 무효 (rule90 은 알려진 worst-case witness).
- **F1287.3 (SIGN)**: 통합 룰(rule150/105, Φ>0)의 residual ≈ 0 또는 음수가 아니면 (over-prediction 은 자기유사 룰에 국한 예측) → 부분 falsify.

## Circularity Guard

self_similarity 는 *기하학적* 측도(시공간 반복 구조), big_Φ 는 *인과* 측도 — 독립 정의. residual 을 self_similarity 로 예측하는 것은 동어반복 아니라 cross-metric 예측.

## Migration TODO
- [ ] box-counting fractal-dim + LZ-self-affinity 하네스 (시공간 다이어그램)
- [ ] residual = LZ_norm − Φ_norm vs self_sim correlate (10-rule panel)
