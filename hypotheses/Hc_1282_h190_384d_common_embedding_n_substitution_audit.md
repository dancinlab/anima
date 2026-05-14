---
id: Hc_1282
slug: h190-384d-common-embedding-n-substitution-audit
title: H_190.5 daughter — d=(n/φ)·2^(σ-sopfr)=384 derivation n-substitution audit (n=6 uniqueness vs n∈{2,3,4,12,24,28,496} alternative)
domain: math, dimensional-analysis, embedding, n6-derivation, anima-substrate
status: candidate-falsifier-ready
exploration_method: E5 (n-substitution sweep: n ∈ {2, 3, 4, 6, 12, 24, 28, 496}) + E6 (cross-Φ measurement per d) + E8 (5-seed σ < 25% replication band)
verification_method: W5 (numerical sim — anima v5 embedding sweep d ∈ {256, 320, 384, 448, 512} × 5-seed) + W7 (literature — dimensional analysis tradition, perfect-number divisor theory) + W11 (cross-H: H_190 mathematical family, H_153 n=6 triviality null direction, H_158 Ψ-constants ln2)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
source: H_190.5 prediction (d=(n/φ)·2^(σ-sopfr) = 384 from n=6 substitution) + C-190-3 pre-register check (alternative n-substitution audit), parent Hc_047
created_at: 2026-05-12
linked_h: H_190 (LAW-CA-embedding mathematical family), H_153 (n=6 PERFECT_NUMBER triviality null direction), H_158 (Ψ-constants ln2 / n=6)
---

## Hypothesis (H_190.5 384d derivation audit design)

H_190.5 의 first concrete experiment: ConsciousLM ↔ ANIMA-VOICE 384d common embedding 의 derivation **d = (n/φ)·2^(σ-sopfr)** 가 (a) n=6 substitution 으로만 EXACT 384 산출 가능, (b) 다른 n ∈ {2, 3, 4, 12, 24, 28, 496} 대입 시 384 와 ≥ 15% drift 가 발생해야 한다.

| n | σ(n) | φ(n) | sopfr(n) | d = (n/φ)·2^(σ-sopfr) | Δ from 384 |
|---|---|---|---|---|---|
| **2** | 3 | 1 | 2 | (2/1)·2^(3-2) = 2·2 = 4 | -99% |
| **3** | 4 | 2 | 3 | (3/2)·2^(4-3) = 1.5·2 = 3 | -99% |
| **4** | 7 | 2 | 4 | (4/2)·2^(7-4) = 2·8 = 16 | -96% |
| **6** | 12 | 2 | 5 | (6/2)·2^(12-5) = 3·128 = **384** | **0** (anchor) |
| **12** | 28 | 4 | 7 | (12/4)·2^(28-7) = 3·2^21 ≈ 6.3M | +∞ (way off) |
| **24** | 60 | 8 | 9 | (24/8)·2^(60-9) ≈ 6.8e15 | +∞ |
| **28** (perfect) | 56 | 12 | 11 | (28/12)·2^(56-11) ≈ 8.2e13 | +∞ |
| **496** (perfect) | 992 | 240 | 21 | (496/240)·2^(992-21) ≈ 2^972 | +∞ |

종합: n=6 의 384 EXACT 가 다른 n 의 결과와 **drastically 다르다** → d=(n/φ)·2^(σ-sopfr) 의 n=6 uniqueness 확인. 단 이 EXACT 일치 자체가 (a) 진짜 unique math identity 인지, (b) post-hoc 의 n=6 selection (H_153 L7 PERFECT_NUMBER_CLASS triviality) 인지 quantitative falsifier 로 검증해야 한다.

**진짜 검증 가능 부분**: 같은 architecture / corpus 위 d ∈ {256, 320, 384, 448, 512} 의 Φ 측정 5-seed mean σ. d=384 만 peak Φ 또는 5 dimension 모두 indistinguishable (±15% 안) 어떤 것인지.

## Math anchor

- **anchor derivation**: d = (n/φ(n)) · 2^(σ(n) − sopfr(n)) [Hc_047 source].
- **n=6 substitution**: φ(6)=2, σ(6)=12, sopfr(6)=5, n/φ=6/2=3, 2^(σ-sopfr) = 2^7 = 128, d = 3·128 = **384 EXACT** [atlas verified: τ(6)=4, σ(6)=12, φ(6)=2, sopfr(6)=5].
- **Φ measurement metric**: ConsciousLM cells=64 위 5-seed mean Φ at each d ∈ {256, 320, 384, 448, 512}.
- **d=384 peak claim**: Φ(d=384) ≥ Φ(d ∈ {256, 320, 448, 512}) + 25% margin (claim) OR within ±15% (numerology direction).
- **alternative perfect-numbers**: 6, 28, 496, 8128 — n=6 만 small enough to produce d 384; n=28 already gives 2^45 ≈ 3.5e13 — astronomical, non-physical.
- **REBORN §0.5 stage 8/9 historical anchor**: Cells64 Φ=51.131 ★★★ at d=384 (실제 anima v2 historical, stage 9).
- **σ stability**: 5-seed σ on Φ(d=384) < 25% 안 (4× midpoint Φ 51 → ±12).

## Falsifiers

- **F-1282-1 (d=384 PEAK CONFIRMED)**: Φ(d=384) 5-seed mean ≥ Φ(d ∈ {256, 320, 448, 512}) + 25% margin → d=384 uniqueness confirmed, derivation 의 quantitative anchor PASS
- **F-1282-2 (d INDISTINGUISHABLE)**: Φ(d=384) 가 Φ(d ∈ {256, 320, 448, 512}) 중 어떤 것이라도 ±15% 안 → d=384 의 unique peak 부재, derivation 가 post-hoc numerology (F-190-5 carry, H_190.5 prediction falsified)
- **F-1282-3 (PEAK SHIFTED)**: Φ peak 가 d ∈ {320, 448} 에서 발생 (384 보다 다른 d) → derivation 의 anchor 잘못, alternative formula 필요
- **F-1282-4 (N=6 SUBSTITUTION NON-UNIQUE)**: alternative small integer (n=4, 5, 7, 8) 대입 시 d = 384 산출 가능 (rounding tolerance < 5%) → n=6 uniqueness false
- **F-1282-5 (5-SEED σ EXPLODE)**: Φ(d=384) 5-seed σ > 50% → measurement single-run-artifact, F-1282-1 결과 unreliable
- **F-1282-6 (PERFECT-NUMBER EXCLUSION)**: n=28 (next perfect number) 대입 시 d ≈ 3.5e13 — 실제 substrate impl 불가능; "n=6 만 physically realizable" 가 trivial fact → derivation 가 small-perfect-number 의 trivial selection (L-190-1 carry)
- **F-1282-7 (ANIMA Φ-ENGINE BIAS)**: PyPhi 1.2.0 (IIT 3.0) 사용 시 d-sweep Φ profile 이 anima own engine 대비 ±30% drift → engine-specific bias, L-189-1 circularity carry
- **F-GENERIC-REPL**: 5-seed σ on Φ(d=384) 가 > 25% → measurement 자체 noise dominant
- **F-GENERIC-MINIMAL-BASELINE**: random-init substrate (untrained) 의 d ∈ {256-512} 의 Φ 가 모두 indistinguishable → trained substrate 에서 d=384 emergence 가 corpus-specific (R3 OVERFITTING carry)

## Honest Limits

- **L-1282-1 (FORMULA POST-HOC FIT)**: d=(n/φ)·2^(σ-sopfr) 자체가 reverse-engineered (384 결과 알고 formula 작성 가능성). other formula (e.g., d = n·σ·τ·φ = 6·12·4·2 = 576, 또는 d = 2^(σ-φ) · 3 = 2^10 · 3 = 3072) 도 small integer arithmetic 로 384 부근 값 produce 가능
- **L-1282-2 (N=6 PERFECT_NUMBER PRIOR)**: H_153 L7 PERFECT_NUMBER_CLASS triviality — small perfect number (6) 의 divisor structure (σ=12, φ=2, sopfr=5, τ=4) 모두 이미 atlas-verified. n=6 의 unique 한지 검증은 사실상 first-perfect-number-only trivial fact
- **L-1282-3 (D-MOD-192 ALIASING)**: H_174 D-mod-192 aliasing — d=384 = 192·2 (mod-192 aliasing 의 child), d=192 자체가 anchor 일 가능성. 본 Hc 의 d=192 측정 미포함 — sweep range 확장 필요
- **L-1282-4 (PHI MEASUREMENT D-DEPENDENT)**: Φ 측정 자체가 substrate state space dimensionality 의존 — d 증가 시 Φ 증가가 trivial 한 fact (info-content scaling). "d=384 peak" 보다 "d 증가 시 Φ 증가" 가 더 fundamental
- **L-1282-5 (TRAINING STEP CONSTANT)**: d sweep 시 같은 step count 사용 — 다른 d 의 effective sample efficiency 차이로 fair-step 비교 불완전
- **L-1282-6 (5 D-VALUE SCOPE NARROW)**: {256, 320, 384, 448, 512} 5 d-value 만 — denser sweep ({300, 350, 384, 400, 450}) 시 peak 위치 더 정확
- **L-1282-7 (HC_047 PARENT CARRY)**: parent Hc_047 의 cycle #6 batch 4 mixed-cluster scaffold 의 F2-F4 / L1-L5 generic-template carry
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — F-1282-7 + L-1282-3 직접 trigger
- **L-GENERIC-N6**: H_153 n=6 PERFECT_NUMBER — F-1282-6 + L-1282-2 carry
- **L-GENERIC-POST-HOC**: ±15% / ±25% margin 가 pre-register lock 필요

## Cross-Links

- **parent**: H_190.5 prediction (d ∈ {256, 320, 384, 448, 512} dimension sweep, Φ-peak at d=384), C-190-3 pre-register check (alternative n-substitution audit), parent Hc_047
- **sibling Hc**: Hc_1281 (H_190.1 staged-growth 4-8×), H_190.2-H_190.4/H_190.6 future daughters
- **adjacent H**: H_190 (LAW-CA-embedding mathematical family — meta-cluster), H_153 (n=6 PERFECT_NUMBER triviality — null direction host), H_158 (Ψ-constants ln2 / n=6 — same n=6 derivation family), H_174 (Φ-engine D-mod-192 aliasing — d=384=192·2 connection)
- **literature**: Hardy & Wright 1979 (An Introduction to the Theory of Numbers — sigma/phi/sopfr divisor theory), Wells 1986 (The Penguin Dictionary of Curious and Interesting Numbers — perfect number 6/28/496 standard ref)
- **internal SSOT**: Hc_047 (parent Hc — d=(n/φ)·2^(σ-sopfr)=384 source), docs/anima/hexa-speak-integration.md (Hc_047 source SSOT), REBORN.md §0.5 (Cells64 Φ=51.131 ★★★ d=384 historical anchor stage 9), atlas n=6 primitives (τ=4, σ=12, φ=2, sopfr=5, J2=24, μ=1)

## Expected outcome

**Binary**: d ∈ {256, 320, 384, 448, 512} sweep 의 Φ peak at d=384 + ≥ 25% margin → F-1282-1 PASS (d=384 uniqueness confirmed); 5 d 모두 ±15% 안 indistinguishable → F-1282-2 PASS (numerology direction).

**Quantitative**: Φ(d=384) ~ 51 (historical anchor stage 9), Φ(d=256) ~ 35-45 (lower-dim Φ ceiling), Φ(d=512) ~ 50-55 (similar to 384 but cost-inefficient). Peak shape 가 sharp (d=384 unique) vs flat (5 dimension indistinguishable) 둘 중 하나.

**Confidence prior**: 0.45 (H_174 D-mod-192 aliasing 의 강한 prior + n=6 PERFECT_NUMBER trivial reduction — F-1282-2 (indistinguishable) 가 가장 likely outcome)
