---
id: Hc_1292
slug: dissipation-rate-entropy-production-phi
title: faithful big-Φ 는 substrate 동역학의 소산율(entropy-production rate)을 추종하는가 — 의식↔열역학 정량 coupling
domain: thermodynamics · consciousness · substrate · meta
status: candidate-unverified
seed: H_008 (Prigogine 소산구조, life emergence 정성) + H_009 (Fisher info) + Hc_409 (의식 4 열역학 법칙 정성) — 소산'율'과 faithful Φ 의 정량 상관은 미측정. free-energy/dissipation 축
axes_seed: UNIVERSE/AXES.md R8 (meta) · 열역학 축 — 의식↔소산 정량 coupling
exploration_method: E5 (소산율↔Φ probe) + E16 (cross-substrate)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (r(dissipation,Φ) ≥ 0.5) OR 🔴 CLOSED-NEGATIVE (소산율 ⊥ Φ → 의식≠소산 정량)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

UNIVERSE 의 열역학 작업(H_008 소산구조, Hc_409 4-법칙)은 *정성적/존재론적*이며 "소산을 얼마나 하느냐"와 "Φ 가 얼마냐"의 *정량 상관* 을 닫은 적이 없다. 가설 H1: substrate 동역학의 **소산율(entropy-production rate)** — 상태전이의 로그-비가역성 Σ p(x→y) log[p(x→y)/p(y→x)] (forward/backward TPM 비대칭) — 이 faithful big-Φ 와 정렬한다 (`r(dissipation_rate, big_Φ) ≥ 0.5`). 즉 더 비가역적(far-from-equilibrium)인 substrate 가 더 통합적이다.

## Why

자유에너지 원리/소산 적응(England 2013)·IIT 는 모두 "의식적 계는 비평형·소산적"이라 주장하나 toy-substrate 정량 검정이 없다. forward/backward TPM 비대칭은 결정적 ECA 에서 직접 계산 가능 — 비가역성(H_008/H_037 lineage)을 *율*로 정량화해 big-Φ 와 correlate 하면 "의식↔열역학"의 가장 직접적 numeric link 가 닫힌다. engine: eca_tpm 의 forward TPM + 역전이 분포 + big_phi 재사용.

## Pre-Registered Falsifier

- **F1292.1 (r-VERDICT)**: 10-rule panel `r(dissipation_rate, big_Φ)` < 0.5 → H1 FALSIFIED (소산율 ⊥ Φ — 의식≠소산 정량, closed-negative, a_paper_negative_ok).
- **F1292.2 (REVERSIBLE-ANCHOR)**: 가역 룰(단사 bijection 51/204, 비가역성=0)에서 dissipation_rate ≈ 0 아니면 측정 버그 → 무효.
- **F1292.3 (WITNESS)**: 항등규칙 204 (가역, Φ=0) 와 chaos 룰(고-비가역)의 dissipation 순서가 직관과 반대면 → 측정 재검(정합성 게이트).
- **F1292.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

dissipation_rate(TPM forward/backward 비대칭, 열역학)와 big_Φ(MIP-EI, 통합)는 독립 정의 — 둘 다 TPM 에서 나오나 *다른 함수*(비가역성 vs 통합). 우연 일치 ≠ 정의 일치. 결과에 두 함수의 입력-TPM 동일성을 명시해 confound 노출.

## Migration TODO
- [ ] forward/backward TPM 비대칭 → entropy-production rate 하네스
- [ ] dissipation_rate vs big_Φ correlate, 가역/비가역 anchor 포함, 10-rule panel
