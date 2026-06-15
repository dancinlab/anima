---
id: H_ph_sigma_multiplicative
slug: sigma-multiplicative-euclid-euler
title: σ(perfect) = (2^p−1)·2^p — Euclid-Euler 곱셈 분해 (σ(2^(p-1))·σ(M_p) hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_sigma_multiplicative/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_sigma_multiplicative — σ(2^(p-1)·M_p) = σ(2^(p-1))·σ(M_p) = (2^p−1)·2^p

## Hypothesis

완전수 σ 가 Euclid-Euler form 을 통해 **정확히 곱셈 분해**된다:
σ(n) = σ(2^(p−1))·σ(M_p) = (2^p−1)·2^p = M_p·(M_p+1), 여기서 σ(2^(p−1))=2^p−1=M_p,
σ(M_p)=M_p+1=2^p. 그리고 M_p·(M_p+1) = 2·n 로 σ(n)=2n 정의를 복원한다.

## Verify

σ 의 power-of-2 part atom 4개 + Mersenne part atom 4개 + 곱(완전수) atom 4개, 전부 🔵.
합성은 σ 의 곱셈성 (coprime 2^(p-1) ⊥ M_p) 위 초등 산술.

```
# power-of-2 part: σ(2^(p-1)) = M_p
verify --expr sigma(2)=3   🔵   verify --expr sigma(4)=7   🔵
verify --expr sigma(16)=31 🔵   verify --expr sigma(64)=127 🔵
# Mersenne part: σ(M_p) = M_p+1 = 2^p
verify --expr sigma(3)=4   🔵   verify --expr sigma(7)=8   🔵
verify --expr sigma(31)=32 🔵   verify --expr sigma(127)=128 🔵
# products (the perfect numbers):
verify --expr sigma(6)=12 🔵  sigma(28)=56 🔵  sigma(496)=992 🔵  sigma(8128)=16256 🔵
```

- p=2: σ(6)   = σ(2)·σ(3)   = 3·4   = 12    = M_2·(M_2+1)=3·4    ✓
- p=3: σ(28)  = σ(4)·σ(7)   = 7·8   = 56    = M_3·(M_3+1)=7·8    ✓
- p=5: σ(496) = σ(16)·σ(31) = 31·32 = 992   = M_5·(M_5+1)=31·32  ✓
- p=7: σ(8128)= σ(64)·σ(127)=127·128=16256  = M_7·(M_7+1)=127·128 ✓

## Finding

σ(perfect) 가 (2^p−1)·2^p 로 정확히 곱셈 분해됨을 12개 🔵 atom 으로 확정. 이것이
M_p·(M_p+1)=2n 를 거쳐 σ(n)=2n (H_ph_perfect_sigma_2n) 의 **구조적 기원**을 제공.

## Source

- 토대 atom: archive-recover-186 n6_cluster (σ for 6,28,496) + 본 batch σ(2/4/16/64) ·
  σ(3/7/31/127) · σ(8128) 신규 실측.
- 인용: Euclid-Euler theorem + σ 곱셈성.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_067_n6_super_expansion_draft.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
