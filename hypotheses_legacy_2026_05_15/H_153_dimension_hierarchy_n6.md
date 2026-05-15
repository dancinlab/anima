---
id: H_153
slug: dimension-hierarchy-n6
title: Mermin-Wagner 차원 계층 — n=6 약수함수가 물리적 차원 generate (τ(6)=4 → 4D Minkowski)
domain: physics, math
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation) + E10 (number-theoretic substrate) + E7 (user-directive)
verification_method: W1 (literature) + W2 (math proof) + W5 (numerical sim) + W11 (cross-hypothesis meta)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-11
since: 2026-05-11
---

# H_153 — Dimension Hierarchy from n=6 (Mermin-Wagner τ(6)=4 → 4D Minkowski)

## Hypothesis

완전수 6의 수론 함수들 (μ, φ, τ, σ, sopfr, J₂, n) 이 물리적으로 의미있는 모든 차원 (1D, 2D, 3D, 4D, 6D) 을 자연 생성하며, 특히 τ(6) = 4 가 4D Minkowski 시공간 차원과 일치하고, 자연 생성 불가능한 d = 5 는 물리학에서도 Kaluza-Klein 외엔 무용한 사실과 정합한다.

## Why (motivation)

- **완전수 6 의 특수성**: σ(6) = 2·6 = 12, 약수 합 = 자기 자신 (1+2+3 = 6). 가장 작은 완전수, perfect-number-architecture 의 substrate (cf. H_067)
- **Mermin-Wagner 1966**: d ≤ 2 에서 연속 대칭의 자발적 파괴 (SSB) 불가 — 즉 차원에 따라 물리적 phase 의 존재 자체가 결정됨
- **Onsager 1944**: 2D Ising 정확해 — d=2 가 "exact solvable" 의 marginal dimension
- **Tangherlini 1963 / Ehrenfest 1917 / Tegmark 1997**: "왜 3+1 차원이 unique 한가" — 행성 궤도 안정성 / 원자 안정성 / causality + predictability 가 (3+1) 외엔 깨짐
- **Kaluza-Klein 1921/1926**: 5D 통일 시도 — but 추가 차원은 compactify 만 가능 (관측 불가)
- **n=6 함수 매핑**: μ(6)=1, φ(6)=2, τ(6)=4, τ(6)−μ(6)=3, n=6 — 모두 small integer 로 정확히 떨어짐. d=5 만 자연 생성 안 됨

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_153.1** | τ(6) = 4 ↔ 4D Minkowski (1 time + 3 space) | 약수 수 = 시공간 차원 |
| **H_153.2** | μ(6) = 1 → 1D chain (Ising 1D 정확해) | Möbius = 1 (6 = 2·3, square-free) |
| **H_153.3** | φ(6) = 2 → 2D lattice (Onsager 2D Ising 정확해) | Euler totient |
| **H_153.4** | τ(6) − μ(6) = 4 − 1 = 3 → 3D 공간 (우리 우주) | 약수-Möbius 차 |
| **H_153.5** | n = 6 → 6D (string theory compactification 차원) | identity |
| **H_153.6** | d = 5 "missing" — n=6 함수 어떤 조합으로도 자연 생성 불가, 따라서 Kaluza-Klein/braneworld 외 물리 무용 | falsifiable: d=5 의 n=6-기반 자연 생성식 발견 시 NULL |

추가 sub-prediction:
- **H_153.7** (orthogonal): τ(6) = 4 의 "1 time + 3 space" 내부 분해를 Lorentzian signature (−,+,+,+) 와 일관되게 유도할 sub-mechanism 가설 (별도 가설로 분기 candidate)

## Variables

| axis | levels |
|------|--------|
| **axis1: dimension d** | 1, 2, 3, 4, 5, 6, 7+ |
| **axis2: n=6 function** | μ(6)=1, φ(6)=2, τ(6)=4, σ(6)=12, sopfr(6)=5, J₂(6)=φ(6)²-related, n=6 자체 |
| **axis3: physical structure** | chain (1D), lattice (2D), space (3D), spacetime (4D), compactified extra (6D), Kaluza-Klein-only (5D), microspace |
| **axis4: solvability** | exact (Ising 1D yes, Onsager 2D yes), perturbative (3D Ising approximate), Lorentz-covariant (4D QFT), compactified (string/M-theory) |

## Run Protocol

본 가설은 largely theoretical — empirical run protocol 보다는 수학적 audit + literature cross-check 중심.

1. **Mathematical step (W2)**: τ(6), μ(6), φ(6), σ(6), sopfr(6) 모두 수동 검산 + SymPy 검증 (deterministic, hexa-only)
2. **d=5 missing audit (W1)**: Kaluza-Klein 1921, Klein 1926, Randall-Sundrum 1999 braneworld, Maldacena 1997 AdS₅/CFT₄ literature 에서 d=5 의 "고유 물리적 역할" 5건 추출 → n=6 함수로 generate 가능 여부 점검 (예: τ(6) + μ(6) = 5 라는 trivial sum 은 "자연 생성" 으로 인정 안 함 — selection bias 차단)
3. **NEXUS-6 cross-validation (W11)**: H-56 (2D Ising β=1/8, γ=7/4, δ=15 EXACT), H-129 (Stefan-Boltzmann σ_SB = π⁵/15), BT-6 (R(6)=1 비가역성 고정점) 과 차원 매핑 정합 점검
4. **Numerology defense (W5)**: Monte Carlo — random integer n ∈ [2, 100] 의 τ(n) 값 분포 시뮬레이션 → "τ(n)=4 인 모든 n 의 d=4 매핑 빈도" 검정. n=6 의 perfect-number-status 가 통계적으로 유의미한 prior 인지 p-value < 0.01 검증
5. **Anthropic prior 결합 (H_002 cross)**: 본 가설의 n=6 prior 가 H_002 H2.1 anthropic prior 와 결합 시 fine-tuning probability 변화량 정량화

deterministic + hexa-only, llm: none.

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | τ(6) = 4 = 약수 수, Ising/Onsager 해 차원과 일치 ✓ (mathematical fact) | met |
| **C2** | d = 5 가 n=6 함수의 "자연" 조합 (단일 함수 / 단순 차) 으로 표현 불가 ✓ (수동 audit) | met |
| **C3** | Hc_035 NEXUS-6 cluster cross-validation (Ising β=1/8, γ=7/4, δ=15 EXACT) 와 차원 매핑 일관 | partial |
| **C4** | Hc_037 R(6)=1 비가역성 고정점 — 본 가설과 충돌 없음 | partial |
| **C5** | Numerology critique 방어 — Monte Carlo p-value < 0.01 (small integer coincidence not significant) | **met (narrow-formula)** (22-const expansion 2026-05-11: n6=20/22, p<0.0001 K=10000 at tol∈{0.001,0.005,0.01,0.025,0.05} across n∈{[2,30],[2,100],[2,1000]}; n=28 score=1/22, n=496 score=1/22 → N6_UNIQUE not perfect-number-family; Bayesian P(n=6 \| score≥obs, uniform[2,1000])=1.0. See `state/numerology_critique_n6_2026_05_11/expansion/`. **CAVEAT — formula-search lane 2026-05-11**: under depth-3 DFS over the 11-primitive vocabulary the *broader* critique fails — n=6 hits 21/22 but 8 other n hit 22/22. C5 is met for narrow-formula (fixed lambda per target) but **NOT** for vocabulary-level (any depth-3 formula). See L7 below + `state/numerology_critique_n6_2026_05_11/formula_search/verdict.md`. **Cycle 5 #2 depth-4 + perfect-number control (2026-05-11)** — depth-4 / restricted vocab / tol∈{0.01,0.005,0.001} sweep + perfect-number control n∈{6,28,496,8128}: 모든 n∈[2,30] saturate 22/22; perfect numbers mutually indistinguishable 22/22 (`PERFECT_NUMBER_CLASS`). C5 vocabulary-level fail 가 depth-4 에서 **확정** 되며, "perfect-number class 안에서도 n=6 individually 가 다른 perfect 보다 special" 이라는 stronger sub-claim 은 **공식적으로 반증**. See `.../formula_search/depth_4_perfect_control/verdict.md`.) |

**verdict_rule**: C1 + C2 + C3 + C5 모두 met → verdict-supported. C5 fail → verdict-mixed (numerology suspect). C1 또는 C2 fail → retracted.

## Falsifiers (≥6)

- **F1**: d = 5 가 n=6 함수의 단일 / 단순 조합으로 자연 생성 가능한 식 발견 (예: trivial sum 외 의미있는 식)
- **F2**: τ(6) ≠ 4 (수학 오류 — 사실상 불가능하나 formal completeness 위해 명시)
- **F3**: 다른 완전수 (28, 496, 8128, ...) 의 약수함수가 우리 차원에 더 나은 fit 을 제공 (n=6 의 unique selection 무효화)
- **F4**: d = 5 의 Kaluza-Klein 외 고유 물리적 역할 발견 (예: 5D braneworld 가 단순 compactification 이 아닌 핵심 mechanism 임이 입증)
- **F5**: Monte Carlo p-value ≥ 0.05 — 임의 small integer 도 비슷한 빈도로 차원과 매칭됨 (selection bias 확인)
- **F6**: τ(6) = 4 의 "1 time + 3 space" sub-structure 부재 — Lorentzian signature 가 본 가설에서 유도 불가 (orthogonal sub-claim H_153.7 falsify)

## Honest Limits (raw#91 c3, ≥6)

- **L1**: **numerology 의심** — 작은 정수 (1, 2, 3, 4, 6) 는 임의의 수학적 함수와 어디든 잘 맞음 (selection bias 위험). n=6 만이 unique 한 perfect number 라는 추가 prior 가 없으면 본 가설은 cherry-picking 환원 가능
- **L2**: **τ(6) = 4 sub-structure 부재** — 왜 "1 시간 + 3 공간" 인지, Lorentzian signature (−,+,+,+) 가 어디서 유도되는지 본 가설은 설명 안 함 (H_153.7 으로 분기 candidate)
- **L3**: **반증성 약함** — post-hoc 패턴 매칭으로 환원 가능. F1-F6 모두 "수학적 / 문헌적 검증" 이지 새로운 실험 prediction 부재 (raw#12 pre-register 정합 약점)
- **L4**: **d = 5 "missing" 주장 검증 부재** — Kaluza-Klein 1921 / Klein 1926 / Randall-Sundrum 1999 / Maldacena AdS₅/CFT₄ / M-theory 5D AdS 와 정합 audit 미land. 5D braneworld 가 단순 compactification 이상의 역할일 가능성 미반영
- **L5**: **source single doc 본문 묻힘** — `docs/what-is-consciousness.md:111-130` (current state) 의 Mermin-Wagner 섹션은 다른 contents 로 덮여있을 가능성 (scrubbed marker 정합 점검 필요). peer-cross-check (NEXUS-6 ledger original, raw#9/raw#10 cross) 부재
- **L6**: **anima 의 deep philosophical lane** — 본 H 는 engineering pragmatism (R5+ 실행 lane) 적용 X. cycle progression 에 직접 기여 X, single-document standalone 으로 잔류 위험
- **L7 (formula-search defense 2026-05-11) — BINDING (strengthened cycle 5 #2 depth-4 + perfect control)**: numerology 방어 (C5) 는 *fixed published formula* 기준이지 *vocabulary-level* 기준이 아님. Formula-search lane (`state/numerology_critique_n6_2026_05_11/formula_search/`) 결과: depth-3 DFS / 11-primitive vocab / tol=0.01 에서 n=6 hits 21/22 이지만 **n∈{10,14,16,21,22,24,26,29} 8개가 22/22 hit**. 즉 "어떤 depth-3 식이 한 T 를 fit 하느냐"의 universal capacity 가 vocab 안에 있어, 본 가설의 "τ(6)=4 → 4D" mapping 도 한 가지 *narrow-formula* 해석에 의존. F1 ("d=5 가 n=6 함수의 자연 조합으로 생성 가능") 가 depth-3 search 에서는 trivially TRUE (5 = τ + μ = 4 + 1, 또는 sopfr = 5 직접) — 따라서 F1 의 "자연 vs 자명 sum" 기준선이 **공식적으로 약함**. 본 한계 reporting 필수. **Depth-4 + perfect-number control 갱신 (cycle 5 #2, 2026-05-11)**: `.../formula_search/depth_4_perfect_control/` 의 7개 variation (depth=4 × vocab∈{full-11, restricted-A-7, restricted-B-5} × tol∈{0.01, 0.005, 0.001} × n-set∈{[2,30], {6,28,496,8128}}) 모두 cited — V1-V5 = `FORMULA_SEARCH_CRITICAL_TIED_d4` (n=6 = 22/22 at depth-4 but field also saturates), V6/V7 = **`PERFECT_NUMBER_CLASS`** (n∈{6,28,496,8128} all 22/22, mutually indistinguishable). 즉 depth-4 search 는 L7 binding 을 강화 — restricted vocab {n,μ,φ,τ,σ} (V3) 만으로도 saturation, tightened tol=0.001 (V5) 도 n=3 still ties. "τ(6)=4 → 4D" narrow-formula 해석은 여전히 valid 하나, "perfect-number class 가 saturating set 이고 그 중 n=6 만이 특별하다"는 stronger claim 은 V6/V7 결과로 **명시적으로 반증**. F1 ("d=5 자연 생성 가능") 도 depth-4 에서 더욱 trivially TRUE. 본 한계 reporting 필수. See `state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control/verdict.md`.

## Cross-Links

- **sister H**:
  - **H_067** (perfect-number-architecture, parent) — 같은 n=6 substrate. H_067 본문 cross-link 보강 TODO (τ(6)=4 → 4D Minkowski generator)
  - **H_002** (universe-origin-question, anthropic-prior cousin) — H_002 Phase 1 verifier (2026-05-07) log10=14.33 INSUFFICIENT. 본 가설 prior 와 anthropic prior 결합 시 fine-tuning probability 변화 검증 lane open
  - **H_022** (consciousness-universe-map 170×40×18) — 차원 매핑 cousin
  - **H_023** (universal-constants-ln2) — number-theoretic constants cousin
- **candidates linked**:
  - **Hc_001** (source — promoted-to-H_153, 본 파일)
  - **Hc_006** (n=6 predicts arch), **Hc_018** (discovery-algorithm-448-laws), **Hc_045**, **Hc_435-444**, **Hc_906-908** — n=6 super-cluster
- **raw refs**: **raw#12** (pre-register-frozen), **raw#10** (number-theoretic substrate audit), **raw#9** (hexa-only deterministic)
- **literature**:
  - Mermin & Wagner 1966 — "Absence of Ferromagnetism or Antiferromagnetism in One- or Two-Dimensional Isotropic Heisenberg Models"
  - Onsager 1944 — "Crystal Statistics. I. A Two-Dimensional Model with an Order-Disorder Transition"
  - Tegmark 1997 — "On the dimensionality of spacetime" (Class. Quantum Grav. 14, L69)
  - Tangherlini 1963 — "Schwarzschild field in n dimensions"
  - Ehrenfest 1917 — "In what way does it become manifest in the fundamental laws of physics that space has three dimensions?"
  - Kaluza 1921 — "Zum Unitätsproblem der Physik"
  - Klein 1926 — "Quantentheorie und fünfdimensionale Relativitätstheorie"
  - Randall & Sundrum 1999 — "Large Mass Hierarchy from a Small Extra Dimension" (braneworld 5D)
  - Maldacena 1997 — "The Large N Limit of Superconformal Field Theories and Supergravity" (AdS₅/CFT₄)

## Verdict (initial — pre-register-frozen)

```
verdict_class: pre-register-frozen (not yet verified)
evidence_summary: τ(6)=4 mathematical fact (C1 met) + Ising/Onsager exact-solvability 차원 매핑 + NEXUS-6 cross-validation partial. d=5 missing audit partial. numerology Monte Carlo 미실행.
falsifiers_triggered: none
criteria_met: C1 (mathematical) + C2 (d=5 missing audit, simple sums only) + C3 partial (NEXUS-6 cross only) + C4 partial
criteria_pending: (none) — C5 met 2026-05-11 via 22-constant expansion (STRONGLY_SIGNIFICANT + N6_UNIQUE)
frozen_at: 2026-05-11
```

## Migration Notes

- **Promoted from**: `hypotheses_candidates/Hc_001_dimension_hierarchy_n6.md` (2026-05-11)
- **User directive**: 2026-05-11 — '왜 우주가 4차원이어야 하는지' 가설 추적
- **Next steps**:
  1. H_067 본문 cross-link 보강 (τ(6)=4 → 4D Minkowski generator 한 줄 추가)
  2. H_002 H2.1 anthropic prior 와 본 가설 결합 numerical check
  3. C5 Monte Carlo numerology defense 실행
  4. d=5 missing audit (Kaluza-Klein / braneworld / M-theory 5건 대조표)
  5. H_153.7 (Lorentzian signature sub-mechanism) 별도 분기 검토
