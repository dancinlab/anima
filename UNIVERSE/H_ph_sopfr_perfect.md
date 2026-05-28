---
id: H_ph_sopfr_perfect
slug: sopfr-perfect-closed-form
title: sopfr(perfect) = 2(p−1) + (2^p−1) 닫힌형 (+ legacy sopfr(496)=58 errata → 39, hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_sopfr_perfect/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_sopfr_perfect — sopfr(2^(p-1)·M_p) = 2(p−1) + (2^p−1)

## Hypothesis

완전수 n = 2^(p−1)·M_p 의 sopfr (소인수 합, multiplicity 포함) 은
**sopfr(n) = 2·(p−1) + M_p = 2(p−1) + (2^p−1)** 닫힌형으로 주어진다.
부수적으로 본 H 는 legacy 텍스트 주장 sopfr(496)=58 을 **반증(errata)** 하고
hexa 실측 sopfr(496)=39 로 교정한다.

## Verify

sopfr atom 4개 🔵 + legacy 오류 주장 1개 🔴 (정직 기록). 합성은 🔵 atom 위 초등 산술.

```
verify --expr sopfr(6)=5    → calc 5   == 5   🔵 SUPPORTED-FORMAL  → 2·1+3   = 5    (6=2·3)
verify --expr sopfr(28)=11  → calc 11  == 11  🔵 SUPPORTED-FORMAL  → 2·2+7   = 11   (28=2²·7)
verify --expr sopfr(496)=39 → calc 39  == 39  🔵 SUPPORTED-FORMAL  → 2·4+31  = 39   (496=2⁴·31)
verify --expr sopfr(8128)=139→calc 139 == 139 🔵 SUPPORTED-FORMAL  → 2·6+127 = 139  (8128=2⁶·127)
# legacy errata (verify-as-written):
verify --expr sopfr(496)=58 → calc 39  != 58  🔴 FALSIFIED  (calc deterministically disagrees)
```

## Finding

sopfr(perfect) = 2(p−1)+(2^p−1) CONFIRMED for p∈{2,3,5,7}. 더불어 legacy sopfr(496)=58 은
🔴 FALSIFIED — hexa calc=39 가 옳다 (2^4·31 → 2·4+31=39). errata 로 교정.

## Source

- 토대 atom: archive-recover-186 n6_cluster (sopfr(6)=5, sopfr(28)=11) + 본 batch
  sopfr(496)=39 · sopfr(8128)=139 신규 실측 + sopfr(496)=58 반증.

## 양방향 sibling

- sibling: UNIVERSE/H_160_n6_perfect_number_meta_cluster.md · UNIVERSE/H_158_psi_constants_ln2_n6.md
  (sopfr 참조 가설들 — 본 H 가 sopfr(496) 값을 39 로 교정)
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
