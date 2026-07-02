---
id: H_ph_perfect_sigma_2n
slug: perfect-sigma-2n-aliquot
title: σ(n)=2n ⇔ aliquot σ(n)−n=n — 완전수 정의 (class {6,28,496,8128} hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_perfect_sigma_2n/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_perfect_sigma_2n — σ(n) = 2n ⇔ aliquot s(n) = n (완전수 정의)

## Hypothesis

완전수 정의 항등식 **σ(n) = 2n** (동치로 aliquot sum s(n) = σ(n)−n = n) 이 알려진
작은 완전수 4개 {6, 28, 496, 8128} 전체에서 hexa-검증된 σ atom 위의 초등 산술로 성립한다.

## Verify

`hexa verify --expr sigma(n)` 4개 모두 🔵 SUPPORTED-FORMAL. 합성은 🔵 atom 위 초등 산술.

```
verify --expr sigma(6)=12      → calc 12    == 12    🔵 SUPPORTED-FORMAL  → 12=2·6,    s=12−6=6
verify --expr sigma(28)=56     → calc 56    == 56    🔵 SUPPORTED-FORMAL  → 56=2·28,   s=56−28=28
verify --expr sigma(496)=992   → calc 992   == 992   🔵 SUPPORTED-FORMAL  → 992=2·496, s=992−496=496
verify --expr sigma(8128)=16256→ calc 16256 == 16256 🔵 SUPPORTED-FORMAL  → 16256=2·8128, s=16256−8128=8128
```

## Finding

σ(n)=2n 가 4개 완전수 전부에서 성립 (정의의 결정론적 재확인). 동치 형태 s(n)=σ(n)−n=n
(aliquot 고정점) 도 같은 atom 위에서 닫힘.

## Source

- 토대 atom: archive-recover-186 n6_cluster (σ for 6,28,496) + 본 batch σ(8128)=16256 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_160_n6_perfect_number_meta_cluster.md · UNIVERSE/H_176_n28_perfect_number_substrate_parallel.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
