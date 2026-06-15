---
id: H_ph6_betrothed_48_75
slug: betrothed-quasi-amicable-48-75
title: 첫 약혼수쌍(betrothed) (48,75) — s(a)=b+1 ∧ s(b)=a+1, σ=a+b+1 (4 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph6_betrothed_48_75/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph6_betrothed_48_75 — 첫 약혼수쌍(betrothed / quasi-amicable) (48, 75)

## Hypothesis

친화수쌍(s(a)=b, s(b)=a)의 "1 차이" 사촌인 **약혼수쌍(betrothed/quasi-amicable)**:
**s(a)=b+1 ∧ s(b)=a+1** (각 진약수합이 상대보다 정확히 1 큼). 동치로 σ(a)=σ(b)=a+b+1.
최소 약혼수쌍 (48, 75).

## Verify

`hexa verify` 4개 atom 모두 🔵 SUPPORTED-FORMAL.

```
aliquot(48)=76  → s(48)=76=75+1=b+1  🔵
aliquot(75)=49  → s(75)=49=48+1=a+1  🔵
sigma(48)=124   🔵   sigma(75)=124   🔵   → σ=124=48+75+1=a+b+1
```

합성 (🔵 atom 위 초등 산술): s(48)=76=75+1, s(75)=49=48+1, σ(48)=σ(75)=124=48+75+1.
전체 verbatim verdict → `.verdicts/ph6_betrothed_48_75/verdict.txt`

## Finding

첫 약혼수쌍 (48,75) 확정 (4/4 atom 🔵). 친화수쌍(σ=a+b)에서 합이 정확히 +1 이동한 변형
(σ=a+b+1) — aliquot 관계의 off-by-one class. 완전(σ=2n)·친화(σ=a+b)·sociable(s-cycle)·
betrothed(σ=a+b+1) 로 aliquot 관계군 확장. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 2/3 친화수쌍 (aliquot 교환 s(a)=b) 의 off-by-one 변형 (s(a)=b+1).
- atom: aliquot(48) aliquot(75) σ(48) σ(75) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph2_amicable_220_284.md · UNIVERSE/H_ph3_amicable_pairs_more.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-6 2026-05-29)
