---
id: H_ph6_almost_perfect
slug: almost-perfect-pow2
title: 준완전수 σ(n)=2n−1 — 2^k (σ(2^k)=2^(k+1)−1), {2,4,8,32,128} (5 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph6_almost_perfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph6_almost_perfect — 준완전수(almost-perfect) σ(n) = 2n − 1

## Hypothesis

완전수 σ(n)=2n 보다 정확히 1 부족한 **준완전수**: **σ(n) = 2n − 1**.
알려진 준완전수는 2의 거듭제곱뿐 — σ(2^k) = 2^(k+1) − 1 = 2·2^k − 1 (등비급수 1+2+…+2^k).
n ∈ {2, 4, 8, 32, 128} 검증. σ=2n+1(quasiperfect, 미발견)·σ>2n(과잉)의 거울인 σ=2n−1 반직선.

## Verify

`hexa verify --expr sigma(n)` 5개 atom 모두 🔵 SUPPORTED-FORMAL.

```
σ(2)  =3  =2·2  −1 🔵   σ(4)  =7  =2·4  −1 🔵   σ(8)=15=2·8−1 🔵
σ(32) =63 =2·32 −1 🔵   σ(128)=255=2·128−1 🔵
```

합성 (🔵 σ atom 위 초등 산술): 위 5개 모두 σ(2^k)=2^(k+1)−1=2·2^k−1, 결손 정확히 1.
전체 verbatim verdict → `.verdicts/ph6_almost_perfect/verdict.txt`

## Finding

준완전수 σ(n)=2n−1 확정 (5/5 atom 🔵). 소수거듭제곱 2^k 의 σ 가 등비급수 닫힌형
2^(k+1)−1 (Mersenne 분자형) 임을 결정론적으로 확인 — 결손 정확히 1. R2 abundant/deficient
삼분법 note 에서 언급만 됐던 σ=2n−1 반직선을 독립 닫힌형 identity 로 승격. composite 🔵 는
atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ=2n) + 라운드 2 boundary note (2^k 결손-1) 승격.
- atom: σ(2) σ(4) σ(8) σ(32) σ(128) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph2_abundant_deficient_boundary.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-6 2026-05-29)
