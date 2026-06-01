---
id: Hc_1293
slug: phi-inverse-u-over-energy-gradient
title: big-Φ 는 에너지-구배(drive)에 대해 역-U 를 그린다 — 평형도 최대구동도 아닌 중간 far-from-equilibrium 대역에서 Φ peak (edge-of-chaos 의 열역학 버전)
domain: thermodynamics · physics · consciousness · substrate
status: candidate-unverified
seed: H_204/H_285 (Φ inverse-U over λ/closure-strength) + H_251 (Ising T_c Φ peak) + H_008 (far-from-equilibrium) — *구동축(energy-gradient)* 위 inverse-U 는 미측정 (기존 inverse-U 는 λ/T/closure 축)
axes_seed: UNIVERSE/AXES.md R8 · 열역학 축 — 구동축 inverse-U
exploration_method: E5 (구배-sweep Φ-peak probe) + E0 (edge-of-chaos 의 열역학 재해석)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (Φ vs gradient 단봉 inverse-U, 중간 peak) OR 🔴 CLOSED-NEGATIVE (단조 또는 무봉 → 구동축 inverse-U 부재)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

기존 inverse-U 발견(H_204 closure-strength, H_285 λ-gain, H_251 Ising-T)은 모두 *내부 결합/온도* 축이다. 빠진 축: **외부 에너지-구배/구동(drive)** — 계를 평형에서 얼마나 멀리 미느냐. 가설 H1: substrate 를 외부 bias-field/구동 강도 g 로 sweep 할 때 big-Φ(g) 가 **단봉 역-U** 를 그린다 — g=0(평형, 활동 死)도 g=max(포화, 결정론적 死)도 아닌 *중간 far-from-equilibrium 대역*에서 Φ 가 최대. 이는 edge-of-chaos(H_285)의 *열역학적* 표현 — "의식은 평형과 포화 사이의 산일적 가장자리에 산다".

## Why

Prigogine 소산구조·England 소산적응은 "구조는 중간 구동에서 발생"을 함의하나 Φ-정량 검정이 없다. 구동축 inverse-U 가 성립하면 H_204/285(내부축)의 inverse-U 와 *구동축에서도* 합류해 inverse-U 가 substrate-축 불변임이 강화되고, 안 되면 inverse-U 가 내부결합 축에 국한됨이 닫힌다. engine: ECA + 확률적 bias-flip(구동 g 로 forward-TPM 변형) + big_phi 재사용.

## Pre-Registered Falsifier

- **F1293.1 (SHAPE-VERDICT)**: Φ(g) 가 단조(증가 또는 감소) OR 무봉(flat, max−min < 0.2×mean) → H1 FALSIFIED (구동축 inverse-U 부재).
- **F1293.2 (PEAK-INTERIOR)**: Φ-peak 가 g 범위의 끝점(g=0 또는 g=max)에 위치 → inverse-U 아님 = 부분 falsify (peak 는 내부에 있어야).
- **F1293.3 (DEAD-ANCHOR)**: g=0(평형 정지) 와 g=max(포화 고정점) 둘 다에서 Φ 가 중간-g Φ 보다 낮지 않으면 → 측정 무효.
- **F1293.4 (DETERMINISM)**: 고정 seed re-run byte-identical (확률 구동이면 다중-seed 평균의 결정적 재현).

## Circularity Guard

energy_gradient g 는 *외생 구동 파라미터*(substrate 에 주입), big_Φ 는 결과 측정 — g 가 Φ 정의에 들어가지 않으므로 독립. inverse-U 형태는 데이터가 결정(사전 강제 아님). H_629(noise inverse-U-like bump) 와의 구별: 본 H 는 deterministic drive-bias, noise-rate 아님 — 결과에 명시.

## Migration TODO
- [ ] bias-field 구동 g 로 forward-TPM 변형 하네스 (g-sweep ≥7 점)
- [ ] Φ(g) 곡선 + peak 위치 + 단봉성 검정, dead-anchor 포함
