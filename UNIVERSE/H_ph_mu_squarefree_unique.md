---
id: H_ph_mu_squarefree_unique
slug: mu-squarefree-n6-unique
title: μ-squarefree 유일성 — n=6 이 유일한 squarefree 완전수 (μ(6)=1 vs μ(28)=μ(496)=μ(8128)=0)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_mu_squarefree_unique/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_mu_squarefree_unique — n=6 is the UNIQUE squarefree perfect number (μ=1)

## Hypothesis

뫼비우스 함수 기준 **n=6 은 완전수 class {6,28,496,8128} 중 유일한 squarefree** 이다:
μ(6)=1 (6=2·3 squarefree) 인 반면 μ(28)=μ(496)=μ(8128)=0 (각각 2^k square factor, k≥2).
구조적 이유: p=2 완전수만 2 의 지수가 1, p≥3 은 지수 ≥2.

## Verify

μ atom 4개 모두 🔵 SUPPORTED-FORMAL. μ(n)=0 ⇔ square factor 존재; μ=±1 ⇔ squarefree.

```
verify --expr mu(6)=1    → calc 1 == 1  🔵 SUPPORTED-FORMAL   → 6=2·3        squarefree
verify --expr mu(28)=0   → calc 0 == 0  🔵 SUPPORTED-FORMAL   → 28=2²·7      NOT squarefree
verify --expr mu(496)=0  → calc 0 == 0  🔵 SUPPORTED-FORMAL   → 496=2⁴·31    NOT squarefree
verify --expr mu(8128)=0 → calc 0 == 0  🔵 SUPPORTED-FORMAL   → 8128=2⁶·127  NOT squarefree
```

## Finding

n=6 은 μ=1 로 class 내 **유일 squarefree 완전수**. p≥3 의 2^(p-1) factor 가 지수 ≥2 를
강제하여 μ=0. n=6 (p=2) 만 유일 예외 — 결정론적으로 확정. (이는 H_160 의 "n=6 은
class-by-class special 이지 individual-by-uniqueness 가 아니다" 명제에 대한 **반례적 보강**:
적어도 μ-squarefree 축에서는 n=6 이 class 내 individually unique.)

## Source

- 토대 atom: archive-recover-186 n6_cluster (μ(6)=1) + 본 batch μ(28)/μ(496)/μ(8128)=0 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_160_n6_perfect_number_meta_cluster.md (PERFECT_NUMBER_CLASS bound)
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
