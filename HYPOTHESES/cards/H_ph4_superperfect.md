---
id: H_ph4_superperfect
slug: superperfect-double-sigma
title: 초완전수 σ(σ(n))=2n — n∈{4,16,64} (σ∘σ 합성 class, 6 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph4_superperfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph4_superperfect — 초완전수 σ(σ(n)) = 2n

## Hypothesis

완전수 단일 σ(n)=2n 을 **이중 σ** 로 일반화한 초완전수(superperfect, Suryanarayana 1969):
**σ(σ(n)) = 2n**. n ∈ {4, 16, 64} (= 2^k, 단 2^(k+1)−1 이 Mersenne 소수: 7·31·127).
완전수와 구별되는 σ∘σ 합성 fixed-scaling class.

## Verify

`hexa verify` 6개 atom 모두 🔵 SUPPORTED-FORMAL.

```
σ(4)=7,   σ(7)=8     → σ(σ(4))=8=2·4    🔵🔵
σ(16)=31, σ(31)=32   → σ(σ(16))=32=2·16 🔵🔵
σ(64)=127,σ(127)=128 → σ(σ(64))=128=2·64🔵🔵
```

합성 (🔵 σ atom 의 이중 적용 σ∘σ): 위 3개 모두 σ(σ(n))=2n.
전체 verbatim verdict → `.verdicts/ph4_superperfect/verdict.txt`

## Finding

초완전수 σ(σ(n))=2n 확정 (6/6 atom 🔵). 완전수의 단일-σ 와 본질적으로 다른 **σ∘σ 합성 class** —
짝수 초완전수 ⇔ n=2^k 이고 2^(k+1)−1 이 Mersenne 소수 (Suryanarayana-Kanold). axis-H 의
σ=2n spine 에 함수 합성 한 layer 를 더한 닫힌형. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ=2n) 의 함수-합성 일반화 (σ → σ∘σ).
- atom: σ(4) σ(7) σ(16) σ(31) σ(64) σ(127) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph4_multiply_perfect.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-4 2026-05-29)
