---
id: H_ph3_amicable_pairs_more
slug: amicable-pairs-more-4
title: 친화수쌍 4개 추가 (1184/1210·2620/2924·5020/5564·6232/6368) — σ(a)=σ(b)=a+b, aliquot 2-cycle (16 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph3_amicable_pairs_more/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph3_amicable_pairs_more — 친화수쌍 4개 추가

## Hypothesis

라운드 2 첫 친화수쌍 (220,284) 를 다음 4개 친화수쌍으로 확장:
(1184,1210)·(2620,2924)·(5020,5564)·(6232,6368). 각 쌍 (a,b) 에서
σ(a)=σ(b)=a+b 이고 aliquot 사상이 교환한다 (s(a)=b, s(b)=a — aliquot 2-cycle).

## Verify

`hexa verify` 16개 atom 모두 🔵 SUPPORTED-FORMAL (aliquot 8 + sigma 8).

```
aliquot(1184)=1210 🔵  aliquot(1210)=1184 🔵   sigma(1184)=2394  🔵  sigma(1210)=2394  🔵
aliquot(2620)=2924 🔵  aliquot(2924)=2620 🔵   sigma(2620)=5544  🔵  sigma(2924)=5544  🔵
aliquot(5020)=5564 🔵  aliquot(5564)=5020 🔵   sigma(5020)=10584 🔵  sigma(5564)=10584 🔵
aliquot(6232)=6368 🔵  aliquot(6368)=6232 🔵   sigma(6232)=12600 🔵  sigma(6368)=12600 🔵
```

합성 (🔵 atom 위 초등 산술): 각 쌍에서 σ(a)=σ(b)=a+b ∧ s(a)=σ(a)−a=b ∧ s(b)=σ(b)−b=a.
전체 verbatim verdict → `.verdicts/ph3_amicable_pairs_more/verdict.txt`

## Finding

친화수쌍 4개 추가 확정 (16/16 atom 🔵). 첫 쌍 (220,284) 와 동일한 aliquot 2-cycle 구조가
4쌍 전부에서 닫힘 — σ-equality σ(a)=σ(b) 와 합 σ=a+b 가 동시 성립. composite 🔵 는
atom verdict 위에서만 주장 (g5/#1027). aliquot period-2 class 의 표본을 5쌍으로 확장.

## Source

- 토대: 라운드 2 H_ph2_amicable_220_284 (aliquot 2-cycle class 확장).
- atom: 4쌍 × {aliquot 2 + sigma 2} = 16개 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph2_amicable_220_284.md · UNIVERSE/H_ph3_sociable_chain_p5.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-3 2026-05-29)
