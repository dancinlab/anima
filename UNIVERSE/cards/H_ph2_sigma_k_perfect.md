---
id: H_ph2_sigma_k_perfect
slug: sigma-k-perfect-power-sums
title: σ_2(n)·σ_3(n) — 완전수 {6,28,496,8128} 고차 약수-거듭제곱합 닫힌형 (8 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph2_sigma_k_perfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph2_sigma_k_perfect — σ_2(n), σ_3(n) for perfect numbers (고차 약수-거듭제곱합)

## Hypothesis

라운드 1 의 σ(n)=2n spine 을 고차 약수합으로 확장한다. 약수의 **제곱합** σ_2(n)=Σ_{d|n} d²
와 **세제곱합** σ_3(n)=Σ_{d|n} d³ 이 알려진 작은 완전수 4개 {6, 28, 496, 8128} 전부에서
hexa-native 닫힌형 정수값으로 결정론적으로 성립한다 (σ_1=σ 의 자연스러운 일반화 σ_k).

## Verify

`hexa verify --expr sigma_2(n)` / `sigma_3(n)` 8개 모두 🔵 SUPPORTED-FORMAL.

```
sigma_2(6)=50          → 🔵   sigma_3(6)=252           → 🔵
sigma_2(28)=1050       → 🔵   sigma_3(28)=25112        → 🔵
sigma_2(496)=328042    → 🔵   sigma_3(496)=139456352   → 🔵
sigma_2(8128)=88085930 → 🔵   sigma_3(8128)=613681507712 → 🔵
```

전체 verbatim verdict (errata 노트 포함) → `.verdicts/ph2_sigma_k_perfect/verdict.txt`

## Finding

σ_k(완전수) 가 k=2,3 에서 4개 전부 닫힌형으로 확정. **errata (g5 정직성)**: 초기 손-계산
expected (1394·412310·45136·67100672·124121584·537211731968) 6개가 모두 🔴 FALSIFIED 였고,
hexa calc 값이 권위 SSOT — 그 값으로 재검증해 8/8 🔵. σ_1=2n 의 완전수 특이성은 σ_2·σ_3 으로
이어지지 않음(완전수에 특별한 σ_2/σ_3 항등식 없음) — 이들은 단순 결정론적 약수-거듭제곱합 닫힘.

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ spine) 의 고차 일반화 σ_k.
- atom: 본 batch sigma_2/sigma_3 신규 실측 (hexa atlas idempotent).

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph_sigma_multiplicative.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-2 2026-05-29)
