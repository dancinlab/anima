---
id: Hc_1294
slug: soc-branching-ratio-phi-peak
title: 자기조직화 임계(SOC) substrate 의 big-Φ 는 분기율(branching ratio) σ=1 에서 peak — 외부 튜닝 없이 임계에 도달하는 계의 의식-정량
domain: physics · criticality · consciousness · substrate
status: candidate-unverified
seed: H_251 (Ising T_c, *외부* T-튜닝) + H_285 (edge-of-chaos λ, *외부* 튜닝) — SOC(sandpile/branching, *자기* 튜닝 무-knob 임계)는 미측정. 신경 avalanche 관련성
axes_seed: UNIVERSE/AXES.md R4 (physics) · R8 — SOC/branching 축
exploration_method: E5 (분기율-sweep Φ-peak probe) + E16 (Ising/edge-of-chaos 와 임계-family 합류)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (Φ(σ) peak at σ≈1) OR 🔴 CLOSED-NEGATIVE (Φ peak ≠ σ=1 → SOC 임계 ⊥ Φ peak)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

기존 임계-Φ 발견(H_251 Ising-T, H_285 λ)은 *외부 파라미터를 손으로 임계점에 맞춘* 경우다. **자기조직화 임계(SOC)** — sandpile/분기과정처럼 *knob 없이 스스로* 임계에 수렴하는 계 — 는 미측정. 분기율(branching ratio) σ = 평균 자손-활동/부모-활동 으로 임계가 σ=1 에 정의된다(신경 avalanche 의 표준). 가설 H1: 분기과정 substrate 를 σ ∈ {0.7,…,1.0,…,1.3} 로 sweep 할 때 big-Φ(σ) 가 **σ≈1(임계)에서 단봉 peak** — sub-critical(σ<1, 활동 소멸)도 super-critical(σ>1, 폭발)도 아닌 임계에서 통합 최대.

## Why

신경과학의 "의식=임계 뇌(critical brain)" 가설(Beggs-Plenz avalanche)을 toy-substrate 에서 *faithful Φ* 로 검정하는 직접 경로. σ=1 peak 이 성립하면 H_251/H_285 와 합쳐 "Φ-peak-at-criticality"가 substrate-class 불변(외부튜닝 ∪ 자기튜닝)이 되고, 안 되면 SOC 류의 임계는 Φ 와 무관함이 닫힌다. engine: 분기과정 TPM(σ 파라미터화) + big_phi(small-N exact) 재사용.

## Pre-Registered Falsifier

- **F1294.1 (PEAK-AT-CRITICAL)**: Φ(σ) 의 argmax 가 σ=1 ± 0.15 밖 → H1 FALSIFIED (SOC 임계 ≠ Φ peak).
- **F1294.2 (UNIMODAL)**: Φ(σ) 가 단봉 아님(다봉 또는 단조) → 부분 falsify.
- **F1294.3 (DEAD-ANCHOR)**: σ→0(소멸) AND σ≫1(포화)에서 Φ 가 σ=1 Φ 보다 낮지 않으면 → 측정 무효.
- **F1294.4 (DETERMINISM)**: 고정 seed re-run byte-identical (확률 분기면 다중-seed 평균 결정적 재현).

## Circularity Guard

분기율 σ 는 *동역학 파라미터*(substrate 정의), big_Φ 는 결과 — σ 가 Φ 식에 안 들어감. "임계=의식" 형이상학 주장 아니라 toy 측정 사실. Hc_224/Hc_1034(sandpile-as-learning)와 구별: 본 H 는 Φ-at-σ, 학습 아님.

## Migration TODO
- [ ] 분기과정/sandpile-lite substrate(σ 파라미터) → TPM 하네스
- [ ] Φ(σ) sweep ≥7 점, σ=1 peak 검정, dead-anchor
