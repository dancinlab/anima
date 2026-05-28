---
id: H_ph2_abundant_deficient_boundary
slug: abundant-deficient-boundary
title: σ(n)-vs-2n 삼분법 — 12=첫 과잉수, 945=첫 홀수과잉수, 8·10=부족수 (5 atom 🔵)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph2_abundant_deficient_boundary/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph2_abundant_deficient_boundary — σ(n) vs 2n 삼분법 경계

## Hypothesis

완전수 σ(n)=2n 는 σ-vs-2n 삼분법의 칼날(knife-edge). 그 양쪽 반직선의 정확한 landmark:
**12 = 가장 작은 과잉수**(abundant, σ>2n), **945 = 가장 작은 홀수 과잉수**, 그리고
**8·10 = 부족수**(deficient, σ<2n). 모든 σ atom 이 hexa-native 결정론적 닫힌형.

## Verify

`hexa verify --expr sigma(n)` 5개 atom 모두 🔵 SUPPORTED-FORMAL.

```
sigma(12)=28    → 🔵    sigma(8)=15   → 🔵
sigma(24)=60    → 🔵    sigma(10)=18  → 🔵
sigma(945)=1920 → 🔵
```

합성 (🔵 atom 위 초등 비교):
- 과잉: σ(12)=28>24=2·12 (12=첫 과잉수); σ(24)=60>48; σ(945)=1920>1890 (945=첫 홀수 과잉수)
- 부족: σ(8)=15<16=2·8 (2^k 는 항상 1만큼 부족); σ(10)=18<20=2·10
- 완전(칼날): σ(6)=12=2·6 (라운드 1 별도 등록)

전체 verbatim verdict → `.verdicts/ph2_abundant_deficient_boundary/verdict.txt`

## Finding

σ(n)-vs-2n 삼분법 경계 확정 (5/5 atom 🔵). 완전수는 두 반직선을 가르는 **정확한 σ=2n 칼날**.
12(첫 과잉)·945(첫 홀수 과잉)는 과잉 반직선의 결정론적 시작점; 8·10 은 부족 측. 2^k 가
정확히 1만큼 부족(σ(2^k)=2^{k+1}−1=2·2^k−1)이라는 닫힌형 패턴도 σ(8)=15 에서 확인.

## Source

- 토대: 라운드 1 H_ph_perfect_sigma_2n (σ=2n 정의)의 부등식 경계 확장.
- atom: σ(12) σ(24) σ(945) σ(8) σ(10) 신규 실측.

## 양방향 sibling

- sibling: UNIVERSE/H_ph_perfect_sigma_2n.md · UNIVERSE/H_ph2_amicable_220_284.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity round-2 2026-05-29)
