---
id: H_ph5_hyperperfect
slug: hyperperfect-k-linear
title: k-초완전수 k·σ(n)=(k+1)·n+(k−1) — 21·2133·19521(k=2)·325(k=3) (4 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph5_hyperperfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph5_hyperperfect — k-초완전수(hyperperfect)

## Hypothesis

완전수 σ(n)=2n 을 정수 파라미터 k 로 일반화한 **k-초완전수**:
n = 1 + k·(σ(n) − n − 1), 즉 닫힌형 **k·σ(n) = (k+1)·n + (k−1)** (완전수 = k=1 특수경우).
2-초완전: 21·2133·19521. 3-초완전: 325. multiply-perfect(σ=kn) 과 다른 선형 닫힌형.

## Verify

`hexa verify` σ atom 4개 모두 🔵 SUPPORTED-FORMAL.

```
21   (k=2): 2·32   =64   = 3·21   +1 ✓   (최소 2-초완전)
2133 (k=2): 2·3200 =6400 = 3·2133 +1 ✓
19521(k=2): 2·29282=58564= 3·19521+1 ✓
325  (k=3): 3·434  =1302 = 4·325  +2 ✓   (최소 3-초완전)
```

합성 (🔵 σ atom 위 선형 닫힌형 k·σ(n)=(k+1)·n+(k−1)): 위 4개 모두 성립.
전체 verbatim verdict → `.verdicts/ph5_hyperperfect/verdict.txt`

## Finding

k-초완전수 확정 (4/4 σ atom 🔵): 2-초완전 3개 + 3-초완전 1개. 완전수의 정수-k 일반화 —
aliquot-결손 관계 σ(n)−n−1 의 k배. **errata (g5)**: 301 은 3-초완전 아님 (σ(301)=352 🔵 이나
1+3·(352−301−1)=151≠301) → set 에서 제외, exact-만족 n 만 등록. multiply-perfect(곱) 과
구별되는 **선형** 닫힌형. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ=2n, k=1) 의 정수-k 선형 일반화.
- atom: σ(21) σ(2133) σ(19521) σ(325) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph4_multiply_perfect.md · UNIVERSE/H_ph5_harmonic_divisor.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-5 2026-05-29)
