---
id: H_ph2_amicable_220_284
slug: amicable-pair-220-284
title: 친화수쌍 (220,284) — σ(220)=σ(284)=504=220+284, aliquot 2-cycle (4 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph2_amicable_220_284/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph2_amicable_220_284 — 첫 친화수쌍 (220, 284)

## Hypothesis

완전수(aliquot 1-cycle 고정점 s(n)=n)의 바로 다음 aliquot-궤도 class 인 **친화수쌍**.
첫 친화수쌍 (220, 284) 에서 σ(220)=σ(284)=504=220+284 이고, aliquot 사상이 둘을 교환한다:
s(220)=σ(220)−220=284, s(284)=σ(284)−284=220. 즉 s²(n)=n ∧ s(n)≠n (주기-2 궤도).

## Verify

`hexa verify` 4개 atom 모두 🔵 SUPPORTED-FORMAL.

```
sigma(220)=504    → 🔵      aliquot(220)=284  → 🔵
sigma(284)=504    → 🔵      aliquot(284)=220  → 🔵
```

합성 (🔵 atom 위 초등 산술):
- σ(220)=504=220+284, σ(284)=504=220+284 → σ-equality σ(220)=σ(284)
- s(220)=504−220=284 (=aliquot(220) 🔵), s(284)=504−284=220 (=aliquot(284) 🔵)
- s∘s(220)=s(284)=220 → aliquot 2-cycle

전체 verbatim verdict → `.verdicts/ph2_amicable_220_284/verdict.txt`

## Finding

(220,284) 친화수쌍 확정 (4/4 atom 🔵 + 합성 초등 산술). 완전수의 aliquot 1-cycle 과 대비되는
**period-2 궤도** — 동일 aliquot 사상 위 한 단계 위 class. σ-equality σ(220)=σ(284) 와
교환-aliquot s(a)=b ∧ s(b)=a 가 동시 성립하는 결정론적 닫힌형. composite 🔵 는 atom verdict 위에서만
주장 (g5/#1027 준수 — composite-direct 🔵 금지).

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (aliquot 고정점 s(n)=n) 의 궤도-class 확장 (1-cycle → 2-cycle).
- atom: σ(220) σ(284) aliquot(220) aliquot(284) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph_sopfr_perfect.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-2 2026-05-29)
