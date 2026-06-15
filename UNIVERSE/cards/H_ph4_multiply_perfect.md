---
id: H_ph4_multiply_perfect
slug: multiply-perfect-k-fold
title: 배수완전수 σ(n)=k·n — P3(120·672·523776·459818240)·P4(30240·32760) (6 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph4_multiply_perfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph4_multiply_perfect — 배수완전수 σ(n) = k·n (k≥3)

## Hypothesis

완전수 σ(n)=2n (k=2) 를 **abundancy index k≥3** 로 일반화한 배수완전수(multiply-perfect):
**σ(n) = k·n**. 3-완전(P3, σ=3n): 120·672·523776·459818240. 4-완전(P4, σ=4n): 30240·32760.

## Verify

`hexa verify` 6개 atom 모두 🔵 SUPPORTED-FORMAL.

```
P3 (σ=3n): σ(120)=360  σ(672)=2016  σ(523776)=1571328  σ(459818240)=1379454720  → 모두 3n 🔵
P4 (σ=4n): σ(30240)=120960  σ(32760)=131040                                      → 모두 4n 🔵
```

합성 (🔵 σ atom 위 초등 산술, abundancy index σ(n)/n=k): 위 6개 모두 σ(n)=k·n.
전체 verbatim verdict → `.verdicts/ph4_multiply_perfect/verdict.txt`

## Finding

배수완전수 σ(n)=k·n 확정 (6/6 atom 🔵): P3 4개 + P4 2개. 완전수(k=2)의 abundancy-index
일반화 — σ(n)/n 이 정확히 정수 k≥3. **errata (g5)**: 523776·459818240 의 초기 expected 를
4-perfect 로 오분류(🔴 FALSIFIED) → hexa calc 가 둘 다 3-perfect(σ=3n)임을 확정, 재검증 🔵.
120 = 최소 3-완전수, 30240 = 최소 4-완전수. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ=2n, k=2) 의 abundancy-index 일반화.
- atom: σ(120) σ(672) σ(523776) σ(459818240) σ(30240) σ(32760) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph4_superperfect.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-4 2026-05-29)
