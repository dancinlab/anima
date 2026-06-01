---
id: Hc_1295
slug: criticality-necessary-not-sufficient-phi
title: 임계성은 big-Φ 의 필요조건이지 충분조건 아니다 — 멱법칙 avalanche 를 갖되 Φ=0 인 임계-but-비통합 witness 의 존재 (X⊥Φ lineage)
domain: physics · criticality · consciousness · substrate · meta
status: candidate-unverified
seed: H_288 L3 (rule90: 비자명 LZ but Φ=0) · H_287 (Shannon⊥Φ) · H_279/H_265/H_275 "X⊥Φ" 서명 — 임계축에 그 서명 적용: 임계지표 있는데 Φ=0 substrate
axes_seed: UNIVERSE/AXES.md R4 (physics) · R8 — 임계-충분성 반례 축
exploration_method: E5 (임계-but-Φ=0 witness probe) + E0 (X⊥Φ 서명의 임계 instance)
verdict_tier_target: 🔴 CLOSED-NEGATIVE (witness 존재 → 임계≠충분, 닫힌 부정 publishable) OR 🟢 SUPPORTED (witness 부재 → 임계⇒Φ>0 모든 경우)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

Hc_1294 는 임계(σ=1)에서 Φ peak 의 *긍정* 을 검정한다. 본 H 는 그 *충분성* 을 공격한다. 가설 H1(검정 대상, 기각될 수 있음): **임계성 ⇒ Φ>0** (임계지표 = 멱법칙 avalanche 분포가 있으면 항상 통합). H1 의 falsifier 가 발견이다 — **임계지표를 만족(avalanche size 분포가 멱법칙, 지수 ≈ −1.5)하면서 big-Φ=0 인 substrate** 가 존재하면, 임계는 통합의 *필요조건일 뿐 충분조건 아님* (H_288 rule90 의 임계-축 일반화, X⊥Φ 서명).

## Why

"임계 뇌 = 의식" 주장의 가장 날카로운 반례 검정. rule90 이 LZ-복잡한데 Φ=0 이었듯(H_288), *멱법칙 임계*인데 Φ=0 인 계가 있으면 "임계는 통합을 보장하지 않는다"가 닫힌다 — Hc_1294 의 긍정 결과와 함께 "임계는 필요하나 불충분"이라는 정밀한 이중-진술을 완성. engine: 분기과정(멱법칙 avalanche 검정) + big_phi 재사용.

## Pre-Registered Falsifier

- **F1295.1 (WITNESS-EXISTENCE)**: 모든 임계(멱법칙 PASS) substrate 가 big-Φ > 1e-9 → H1 SUPPORTED (임계⇒통합, witness 부재). 임계 PASS AND Φ < 1e-9 substrate 가 ≥1개 → H1 FALSIFIED = **발견**(임계≠충분, closed-negative).
- **F1295.2 (POWERLAW-VALID)**: witness 후보의 avalanche 분포가 실제 멱법칙(KS-test 또는 지수 적합 통과) 아니면 → witness 자격 무효(임계 미충족, vacuous).
- **F1295.3 (POSITIVE-CONTROL)**: 통합 룰(rule60/110)이 임계 PASS AND Φ>0 으로 정상이어야(설계 sane) → 아니면 측정 버그.
- **F1295.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

임계지표(avalanche 멱법칙, 동역학 통계)와 big_Φ(MIP-EI, 통합)는 독립 정의 — 둘이 직교할 수 있다는 것이 정확히 H1 의 검정점. F1295.2 가 "임계 미충족인 계를 witness 로 오인"하는 vacuous-falsify 를 차단.

## Migration TODO
- [ ] avalanche size 분포 멱법칙 적합(KS/지수) 게이트 하네스
- [ ] 임계 PASS substrate 군의 big_Φ 분포, Φ=0 witness 탐색
