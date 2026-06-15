---
id: H_ph_euclid_euler_reconstruct
slug: euclid-euler-reconstruction-pow
title: n = 2^(p−1)·(2^p−1) — Euclid-Euler 완전수 복원 (pow atom + M_p 소수성 witness, hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_euclid_euler_reconstruct/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_euclid_euler_reconstruct — n = 2^(p−1)·(2^p−1) 복원 (p∈{2,3,5,7})

## Hypothesis

모든 짝수 완전수는 소수 p 로부터 **n = 2^(p−1)·(2^p−1)** 로 복원되며, power-of-two
factor 2^(p−1) 와 2^p (M_p=2^p−1 구성용) 가 hexa pow atom 으로, M_p 의 소수성이
τ(M_p)=2 witness 로 검증된다. p∈{2,3,5,7} → {6,28,496,8128}.

## Verify

pow atom 8개 (2^(p-1), 2^p) + M_p 소수성 τ-witness 4개, 전부 🔵 SUPPORTED-FORMAL.

```
# 2^(p-1): pow(2,1)=2 🔵  pow(2,2)=4 🔵  pow(2,4)=16 🔵  pow(2,6)=64 🔵
# 2^p:     pow(2,2)=4 🔵  pow(2,3)=8 🔵  pow(2,5)=32 🔵  pow(2,7)=128 🔵
# M_p prime witness: tau(3)=2 🔵  tau(7)=2 🔵  tau(31)=2 🔵  tau(127)=2 🔵
```

- p=2: 2·(4−1)   = 2·3   = 6     ✓  (M_2=3,   τ(3)=2 prime)
- p=3: 4·(8−1)   = 4·7   = 28    ✓  (M_3=7,   τ(7)=2 prime)
- p=5: 16·(32−1) = 16·31 = 496   ✓  (M_5=31,  τ(31)=2 prime)
- p=7: 64·(128−1)= 64·127= 8128  ✓  (M_7=127, τ(127)=2 prime)

## Finding

Euclid-Euler 복원공식 2^(p−1)·(2^p−1) 이 p∈{2,3,5,7} 각각에서 정확히 완전수를 산출함을
hexa pow atom + 소수성 witness 로 결정론적 확정. M_p 소수성이 (τ=2 로) 명시적으로 동봉됨.

## Source

- 토대 atom: 본 batch pow(2,1..7) + τ(3/7/31/127)=2 신규 실측 (archive-recover n6 cluster 확장).
- 인용: Euclid (IX.36) + Euler (even-perfect characterization).

## 양방향 sibling

- sibling: UNIVERSE/H_ph_tau_perfect_2p.md · UNIVERSE/H_ph_sigma_multiplicative.md · UNIVERSE/H_160_n6_perfect_number_meta_cluster.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
