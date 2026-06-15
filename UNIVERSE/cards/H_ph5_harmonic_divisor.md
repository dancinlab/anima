---
id: H_ph5_harmonic_divisor
slug: ore-harmonic-divisor
title: Ore 조화약수 H(n)=n·τ(n)/σ(n)∈ℤ — {6,28,140,270,496} (τ·σ 비율 identity, 8 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph5_harmonic_divisor/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph5_harmonic_divisor — Ore 조화약수(harmonic divisor) 수

## Hypothesis

약수의 조화평균 **H(n) = n·τ(n)/σ(n)** 이 정수인 수(Ore 1948 조화약수수).
n ∈ {6, 28, 140, 270, 496}. Ore 정리: 모든 완전수는 조화약수수 (6·28·496 완전 + 140·270 비완전).
axis-H 1~4 라운드가 σ / aliquot / σ_k 단독을 썼던 것과 달리 **τ 와 σ 를 하나의 비율 identity** 로 묶음.

## Verify

`hexa verify` τ·σ atom 8개 모두 🔵 SUPPORTED-FORMAL (σ(28)=56·σ(496)=992 는 라운드 1 재사용).

```
H(6)  =6·4/12   =2 ∈ℤ ✓   H(28) =28·6/56  =3 ∈ℤ ✓   H(140)=140·12/336=5 ∈ℤ ✓
H(270)=270·16/720=6 ∈ℤ ✓  H(496)=496·10/992=5 ∈ℤ ✓
```

합성 (🔵 τ,σ atom 위 결정론적 나눗셈 정수성): 위 5개 모두 n·τ(n)/σ(n) ∈ ℤ.
전체 verbatim verdict → `.verdicts/ph5_harmonic_divisor/verdict.txt`

## Finding

Ore 조화약수수 확정 (8/8 τ·σ atom 🔵, 비율 정수성 결정론적). axis-H 에서 처음으로
**τ × σ 두 함수를 한 항등식** 으로 결합 — H(n)=nτ(n)/σ(n) 의 정수성. 완전수(6·28·496)는
전부 조화 (Ore 정리), 140·270 은 비완전 조화수. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 H_ph_sigma_phi_n_tau_spine (τ·σ 결합 spine) 의 조화평균 확장.
- atom: τ(6) τ(28) τ(140) τ(270) τ(496) σ(140) σ(270) (+σ(6) 재검) 신규/재사용 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_sigma_phi_n_tau_spine.md · UNIVERSE/H_ph5_hyperperfect.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-5 2026-05-29)
