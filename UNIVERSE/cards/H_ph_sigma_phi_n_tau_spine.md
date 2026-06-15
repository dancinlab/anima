---
id: H_ph_sigma_phi_n_tau_spine
slug: sigma-phi-n-tau-spine-n6-unique
title: σ(n)·φ(n)=n·τ(n) spine — n=6 유일 (perfect-number class {6,28,496,8128} 전수 hexa 검증)
domain: math
status: verified
closure: verified-substrate
closure_ref: .verdicts/ph_sigma_phi_n_tau_spine/verdict.txt
hexa_only: true
deterministic: true
llm: none
since: 2026-05-29
---

# H_ph_sigma_phi_n_tau_spine — σ(n)·φ(n) = n·τ(n) ⇔ n=6 (perfect-number class)

## Hypothesis

약수함수 항등식 **σ(n)·φ(n) = n·τ(n)** 은 완전수 class {6, 28, 496, 8128} 중에서
**n=6 에서만 성립(HOLDS)** 하고 n=28/496/8128 에서는 모두 **반증(FAILS)** 된다.
즉 σφ=nτ spine 은 perfect-number class 안에서 **n=6-구조적 유일(structural unique)**
identity 이다. (이는 이미 H_067/H_160 에서 인용된 "σ(n)·φ(n)=n·τ(n) ⇔ n=6 uniqueness
lemma" 의 perfect-number-class 전수 hexa 실측 닫힘이다.)

## Verify

`hexa verify --expr` (pool ubu-2:~/core/hexa-lang), 12개 atom 전부 🔵 SUPPORTED-FORMAL.
합성(HOLDS/FAILS)은 🔵 atom 위의 초등 산술. 전문 verdict = closure_ref.

- n=6  : σ(6)=12 🔵 · φ(6)=2 🔵 · τ(6)=4 🔵 → 12·2=24 = 6·4=24 → **HOLDS**
- n=28 : σ(28)=56 🔵 · φ(28)=12 🔵 · τ(28)=6 🔵 → 56·12=672 ≠ 28·6=168 → **FAILS**
- n=496: σ(496)=992 🔵 · φ(496)=240 🔵 · τ(496)=10 🔵 → 992·240=238080 ≠ 496·10=4960 → **FAILS**
- n=8128: σ(8128)=16256 🔵 · φ(8128)=4032 🔵 · τ(8128)=14 🔵 → 16256·4032=65544192 ≠ 8128·14=113792 → **FAILS**

```
verify --expr sigma(6)=12   → calc 12 == 12  🔵 SUPPORTED-FORMAL
verify --expr phi(6)=2      → calc 2  == 2   🔵 SUPPORTED-FORMAL
verify --expr tau(6)=4      → calc 4  == 4   🔵 SUPPORTED-FORMAL
verify --expr sigma(28)=56  → calc 56 == 56  🔵 SUPPORTED-FORMAL
verify --expr phi(28)=12    → calc 12 == 12  🔵 SUPPORTED-FORMAL
verify --expr tau(28)=6     → calc 6  == 6   🔵 SUPPORTED-FORMAL
verify --expr sigma(496)=992→ calc 992== 992 🔵 SUPPORTED-FORMAL
verify --expr phi(496)=240  → calc 240==240  🔵 SUPPORTED-FORMAL
verify --expr tau(496)=10   → calc 10 == 10  🔵 SUPPORTED-FORMAL
verify --expr sigma(8128)=16256 → calc 16256==16256 🔵 SUPPORTED-FORMAL
verify --expr phi(8128)=4032    → calc 4032 ==4032  🔵 SUPPORTED-FORMAL
verify --expr tau(8128)=14      → calc 14   ==14    🔵 SUPPORTED-FORMAL
```

## Finding

σφ=nτ spine HOLDS at n=6 ONLY (class 전수 1/4). 이는 이미 falsified 된 physics-mapping
uniqueness 와는 **구별되는** 순수 number-theoretic 유일성 — perfect-number class vocabulary
안에서 n=6 만이 algebraic spine 을 만족함을 결정론적으로 확정.

## Source

- 토대 atom: archive-recover-186 n6_cluster (σ/φ/τ for 6,28,496) — 본 H 가 φ(496)/φ(8128)/
  σ(8128)/τ(8128) 추가 실측으로 class 전수 확장.
- 인용 lemma: H_067 (perfect-number-architecture, σ·φ=n·τ ⇔ n=6) · H_160 (n=6 meta-cluster).
- 동봉 verdict: .verdicts/proof-harvest/sigma-phi-n-tau-spine.txt (동일 내용 batch index).

## 양방향 sibling

- sibling: UNIVERSE/H_067_n6_super_expansion_draft.md · UNIVERSE/H_160_n6_perfect_number_meta_cluster.md
- SSOT: UNIVERSE/CANDIDATES.md (proof-harvest closed-form identity batch 2026-05-29)
