---
id: H_ph_tau_perfect_2p
slug: tau-perfect-2p-euclid-euler
title: τ(perfect)=2p — Euclid-Euler 완전수의 약수개수는 소수 p 의 2배 (hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_tau_perfect_2p/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_tau_perfect_2p — τ(2^(p-1)·M_p) = 2p (Euclid-Euler form)

## Hypothesis

짝수 완전수 n = 2^(p−1)·(2^p−1) (M_p = 2^p−1 가 메르센 소수) 는 약수개수
**τ(n) = 2p** 를 가진다. 즉 소수 지수 p 는 τ(n)/2 로 복원된다. p ∈ {2,3,5,7} 가
완전수 {6,28,496,8128} 에 대응.

## Verify

τ atom 4개 + M_p 소수성 witness τ(M_p)=2 4개 모두 🔵 SUPPORTED-FORMAL.
합성은 τ 의 곱셈성 (coprime 2^(p-1) ⊥ M_p) 위 초등 산술.

```
verify --expr tau(6)=4    → calc 4  == 4   🔵   → 2·2=4   (p=2, M_2=3 prime: τ(3)=2 🔵)
verify --expr tau(28)=6   → calc 6  == 6   🔵   → 2·3=6   (p=3, M_3=7 prime: τ(7)=2 🔵)
verify --expr tau(496)=10 → calc 10 == 10  🔵   → 2·5=10  (p=5, M_5=31 prime: τ(31)=2 🔵)
verify --expr tau(8128)=14→ calc 14 == 14  🔵   → 2·7=14  (p=7, M_7=127 prime: τ(127)=2 🔵)
verify --expr tau(3)=2    → calc 2 == 2 🔵    verify --expr tau(7)=2   → calc 2 == 2 🔵
verify --expr tau(31)=2   → calc 2 == 2 🔵    verify --expr tau(127)=2 → calc 2 == 2 🔵
```

τ(n) = τ(2^(p-1))·τ(M_p) = p·2 = 2p (M_p 소수이므로 τ(M_p)=2).

## Finding

τ(perfect)=2p CONFIRMED for p∈{2,3,5,7}. 약수개수가 정확히 소수 인덱스 p 의 2배 —
완전수의 Euclid-Euler 구조가 τ 한 값으로 인코딩됨을 결정론적으로 확정.

## Source

- 토대 atom: archive-recover-186 n6_cluster (τ for 6,28,496) + 본 batch τ(8128)=14 + τ(M_p)=2 신규 실측.
- 인용: Euclid-Euler theorem (even perfect ⇔ 2^(p-1)·(2^p−1), M_p prime).

## 양방향 sibling

- sibling: UNIVERSE/H_153_dimension_hierarchy_n6.md (τ(6)=4→4D) · UNIVERSE/H_160_n6_perfect_number_meta_cluster.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
