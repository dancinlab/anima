---
id: H_ph3_perfect_5th_mersenne
slug: perfect-5th-mersenne-33550336
title: 5번째 완전수 33550336 = 2^12·(2^13−1) — σ=2n + aliquot 고정점 (2 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph3_perfect_5th_mersenne/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph3_perfect_5th_mersenne — 5번째 완전수 33550336

## Hypothesis

라운드 1 완전수 class {6, 28, 496, 8128} 를 **다섯 번째 완전수** 로 확장한다.
33550336 = 2^12·(2^13−1) (Mersenne 소수 2^13−1=8191, Euclid-Euler p=13) 가
완전수 정의 σ(n)=2n 와 aliquot 고정점 s(n)=σ(n)−n=n 을 hexa-검증 atom 위에서 만족한다.

## Verify

`hexa verify` 2개 atom 모두 🔵 SUPPORTED-FORMAL.

```
sigma(33550336)=67100672    → 🔵   (= 2·33550336)
aliquot(33550336)=33550336  → 🔵   (s(n)=n 고정점)
```

합성 (🔵 atom 위 초등 산술):
- σ(33550336)=67100672=2·33550336 → σ=2n
- s=σ−n=67100672−33550336=33550336=n → aliquot 고정점
- Euclid-Euler form: 33550336 = 2^12·8191 = 2^(13−1)·(2^13−1)

전체 verbatim verdict → `.verdicts/ph3_perfect_5th_mersenne/verdict.txt`

## Finding

5번째 완전수 33550336 확정 (2/2 atom 🔵). 라운드 1 의 perfect class {6,28,496,8128} 를
n>8128 로 처음 확장 — 8자리 정수 규모에서도 σ=2n + aliquot 1-cycle 닫힘이 결정론적으로 유지.
Euclid-Euler 재구성식 (H_ph_euclid_euler_reconstruct) 의 p=13 instance 로도 정합.

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n + H_ph_euclid_euler_reconstruct (perfect class 확장).
- atom: σ(33550336) aliquot(33550336) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph_euclid_euler_reconstruct.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-3 2026-05-29)
