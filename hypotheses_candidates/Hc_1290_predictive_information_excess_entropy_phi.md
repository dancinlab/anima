---
id: Hc_1290
slug: predictive-information-excess-entropy-phi
title: faithful big-Φ 는 예측정보(excess entropy E = I[past;future])를 추종하는가 — 정보-측도 arc 의 4번째 얼굴 (Shannon⊥ · LZ∥ · TE∥ 이후)
domain: information · consciousness · substrate · meta
status: candidate-unverified
seed: H_287 (Shannon⊥Φ) · H_288 (LZ∥Φ) · H_290 (TE∥Φ) 정보-측도 arc — 4번째 측도 = Crutchfield/Bialek 예측정보(excess entropy), 과거-미래 상호정보
axes_seed: UNIVERSE/AXES.md R5 (information) — 정보-측도 arc 확장
exploration_method: E5 (4번째 정보-측도 probe) + E16 (cross-substrate 일관)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (r≥0.5 → arc 에 합류) OR 🔴 CLOSED-NEGATIVE (r<0.5 → 예측정보 ⊥ Φ, Shannon 계열로 분류)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

정보-측도 arc(H_287/288/290)는 Φ 가 *통계적 정보량*(Shannon, ⊥)이 아니라 *알고리즘/흐름 복잡도*(LZ∥, TE∥)와 정렬함을 보였다. 빠진 4번째 얼굴: **예측정보 / excess entropy** `E = I(past block ; future block)` — 시계열이 미래를 예측하기 위해 보존하는 정보량(Crutchfield-Feldman, Bialek-Nemenman-Tishby의 predictive information). 이는 Shannon-엔트로피(순간 비트수)와 LZ(비압축성) 어느 쪽과도 다른 *시간적 구조* 측도다. 가설 H1: ECA panel 에서 `r(excess_entropy, big_Φ) ≥ 0.5`.

## Why

excess entropy 는 "계가 자기 과거에서 미래에 대해 얼마나 기억/예측을 운반하는가"로, IIT 의 *시간적 통합* 직관과 가장 가까운 고전 측도다. Shannon(H_287)이 직교한 자리에서 excess-entropy 가 정렬하면 "Φ 의 정보-얼굴 = 시간구조 보존"이 강화되고, 직교하면 excess-entropy 가 Shannon 계열로 분류돼 arc 의 경계가 더 선명해진다. 새 metric 발명 아님: block-entropy 차분으로 excess entropy 표준 추정, big_Φ = H_288 재사용.

## Pre-Registered Falsifier

- **F1290.1 (r-VERDICT)**: 10-rule panel `r(excess_entropy, big_Φ)` < 0.5 → H1 FALSIFIED (예측정보 ⊥ Φ — Shannon 계열). ≥ 0.5 → SUPPORTED (LZ/TE arc 합류).
- **F1290.2 (DISTINCT-FROM-SHANNON)**: excess_entropy 가 단순 출력-엔트로피 H_out 과 r ≥ 0.95 (사실상 동일) 이면 → 측도 비독립 = 측정 설계 무효 (excess entropy 는 H_out 과 구별돼야).
- **F1290.3 (ANCHOR)**: 상수규칙 0/255 excess_entropy ≈ 0 AND big_Φ=0 아니면 무효.
- **F1290.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

excess entropy(과거-미래 MI)와 big_Φ(MIP-EI)는 독립 정의 — excess entropy 는 시간축 partition, big_Φ 는 공간/기제 partition. F1290.2 가 excess-entropy 의 Shannon-비독립성을 명시 게이트로 잡아 동어반복 방지.

## Migration TODO
- [ ] block-entropy → excess entropy 추정 하네스 (시계열 블록)
- [ ] excess_entropy vs big_Φ correlate + H_out 독립성 게이트, 10-rule panel
