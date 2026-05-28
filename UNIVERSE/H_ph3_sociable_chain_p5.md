---
id: H_ph3_sociable_chain_p5
slug: sociable-chain-period-5-12496
title: 주기-5 sociable aliquot 사이클 12496→14288→15472→14536→14264→12496 (5 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph3_sociable_chain_p5/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph3_sociable_chain_p5 — 주기-5 sociable aliquot 사이클

## Hypothesis

aliquot-궤도 계층의 다음 class: **주기-5 sociable 사이클** (Poulet 1918, 최소 5-cycle).
12496 → 14288 → 15472 → 14536 → 14264 → 12496 이 aliquot 사상 하에서 정확히 5-주기로
닫힌다 (s⁵(n)=n, 중간 어느 항도 n과 같지 않음). 완전수(1-cycle)·친화수(2-cycle) 의 일반화.

## Verify

`hexa verify` 5개 atom 모두 🔵 SUPPORTED-FORMAL.

```
aliquot(12496)=14288 🔵
aliquot(14288)=15472 🔵
aliquot(15472)=14536 🔵
aliquot(14536)=14264 🔵
aliquot(14264)=12496 🔵   ← 사이클 닫힘
```

합성 (🔵 atom 위 사이클 닫힘): s(12496)→14288→15472→14536→14264→12496 이므로
s⁵(12496)=12496 이고 중간항 모두 ≠12496 → 진짜 주기-5 sociable 사이클.
전체 verbatim verdict → `.verdicts/ph3_sociable_chain_p5/verdict.txt`

## Finding

주기-5 sociable 사이클 확정 (5/5 atom 🔵, 사이클 결정론적 닫힘). aliquot-궤도 계층이
**1-cycle(완전, R1) · 2-cycle(친화, R2/R3) · 5-cycle(sociable, R3)** 로 완성. 동일한 aliquot
사상 위에서 궤도 주기만 바뀌는 통일 구조 — 완전·친화·sociable 은 하나의 aliquot 동역학의
서로 다른 주기 fixed-orbit. composite 🔵 는 atom verdict 위에서만 (g5/#1027).

## Source

- 토대: 라운드 1 완전수(aliquot 1-cycle) + 라운드 2/3 친화수(2-cycle) → sociable(≥3-cycle) 확장.
- atom: 5-cycle aliquot 사상 5개 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph3_amicable_pairs_more.md · UNIVERSE/H_ph2_amicable_220_284.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-3 2026-05-29)
