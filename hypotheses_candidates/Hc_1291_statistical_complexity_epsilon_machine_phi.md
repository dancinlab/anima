---
id: Hc_1291
slug: statistical-complexity-epsilon-machine-phi
title: faithful big-Φ 는 통계적 복잡도 Cμ(ε-machine 인과상태 수)를 LZ 보다 더 잘 추종하는가 — 복잡도의 3번째 얼굴, rule90 over-prediction 해소 후보
domain: information · consciousness · substrate · meta
status: candidate-unverified
seed: H_288 (LZ∥Φ r=0.831, but rule90 self-similar over-prediction L3) — Crutchfield ε-machine 통계적 복잡도 Cμ 는 자기유사 무작위성을 단순으로 봄 → rule90 잔차 해소 가능성
axes_seed: UNIVERSE/AXES.md R5 (information) — 복잡도 측도 triangulation
exploration_method: E5 (3번째 복잡도-측도 probe) + E0 (LZ over-prediction 잔차 진단)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (r(Cμ,Φ) ≥ r(LZ,Φ) AND rule90 Cμ 낮음) OR 🔴 CLOSED-NEGATIVE (Cμ 가 LZ 보다 못 추종 → 통계적 복잡도 ⊥ 통합)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

H_288 은 LZ-복잡도가 Φ 를 추종하나(r=0.831) rule90(Sierpinski 자기유사)에서 over-predict 함을 발견했다. Crutchfield 의 **statistical complexity Cμ** (ε-machine 의 인과상태 엔트로피, 미래 예측에 필요한 *최소 메모리*)는 LZ 와 결정적으로 다르다 — 순수 무작위(coin)는 LZ 최대지만 Cμ=0, 자기유사 fractal 도 Cμ 가 낮을 수 있다. 가설 H1: `r(Cμ, big_Φ) ≥ r(LZ_norm, big_Φ)` (Cμ 가 LZ 만큼 또는 더 잘 추종) **그리고** rule90 의 Cμ 가 통합 룰보다 낮다 (over-prediction 해소). 즉 Cμ 가 Φ 의 *진짜* 복잡도-얼굴.

## Why

복잡도에는 ≥3 얼굴이 있다 — 비압축성(LZ, H_288), 통계적 구조-메모리(Cμ, 본 H), 알고리즘적(Kolmogorov, LZ 의 부모). Φ 가 *어느 복잡도* 와 같은 축인지는 IIT 토대 질문이며 H_287/288 의 자연 연장. Cμ 가 rule90 잔차를 해소하면 H_288 L3 caveat 가 닫히고, 못 하면 Cμ ⊥ Φ 가 또 다른 X⊥Φ 서명. ε-machine 재구성은 표준(CSSR/subtree-merge), big_Φ = 재사용.

## Pre-Registered Falsifier

- **F1291.1 (Cμ-BEATS-OR-TIES-LZ)**: `r(Cμ, big_Φ)` < `r(LZ_norm, big_Φ) − 0.1` → H1 FALSIFIED (Cμ 가 LZ 보다 유의하게 못 추종).
- **F1291.2 (RULE90-RESOLUTION)**: rule90 의 Cμ 가 통합 룰(rule60/110/30) Cμ 의 중앙값 이상 → over-prediction 해소 실패 = 부분 falsify (Cμ 도 자기유사를 복잡으로 봄).
- **F1291.3 (COIN-ANCHOR)**: 순수 무작위 대조 시퀀스에서 Cμ ≈ 0 (LZ 는 최대) 아니면 ε-machine 구현 버그 → 무효.
- **F1291.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

Cμ(ε-machine 인과상태)와 big_Φ(MIP-EI)는 독립 정의 — Cμ 는 시계열 예측-메모리, big_Φ 는 기제 통합. F1291.3 coin-anchor 가 Cμ≠LZ 를 명시 보증해 측도 독립성 확보.

## Migration TODO
- [ ] ε-machine 재구성(CSSR-lite) → Cμ 하네스
- [ ] Cμ vs big_Φ + LZ vs big_Φ 동일 panel 비교 r, rule90 잔차 점검
