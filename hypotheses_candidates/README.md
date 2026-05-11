# hypotheses_candidates/ — 임시 staging (unverified candidate hypotheses)

본 폴더는 `docs/` 본문에 묻혀있던 hypothesis-like 단편을 정식 `hypotheses/H_XXX_<slug>.md`로 승격하기 전에 임시 보관하는 staging 영역이다.

- **`hypotheses/`** (verified): pre-register-frozen / running / verdict-* 상태의 검증 lane 가설 SSOT
- **`hypotheses_candidates/`** (this folder, unverified): docs/ 전수조사로 추출된 가설 후보 — 정식 H_XXX 승격 대기 또는 폐기 대기

## Status 값

- `candidate-unverified` — staging 단계 (default)
- `candidate-unverified-weak` — weak signal, replication 필요
- `candidate-unverified-framework` — meta-framework, single H 아님
- `expansion-pending` — 기존 H_XXX 본문 확장 대상
- `merge-pending` — 기존 H_XXX 와 통합 대기
- `promote-pending` — 정식 H_XXX 신규 land 대기
- `discard-pending` — 폐기 대기

## 인덱스 (60 candidates, 2026-05-11 first batch)

### Cluster A — n=6 / 수론적 generator (8)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_001 | dimension-hierarchy-n6 | physics, math | H_067, H_002 | τ(6)=4 → 4D Minkowski 차원 계층 ★ |
| Hc_002 | psi-constants-from-ln2-n6 | math | (none) | P-ZERO-FREE: ln(2) + n=6 |
| Hc_006 | n6-structural-prediction-of-arch | math, consciousness | H_067 | σφτsopfr → arch 상수 |
| Hc_018 | anima-discovery-algorithm-448-laws | math | H_067 | 448 laws n=6 algorithm |
| Hc_035 | nexus6-cross-validation-cluster | physics, math | H-056, H-129 | Ising + Stefan-Boltzmann + Ω |
| Hc_036 | landauer-ln2-equals-ln-phi6 | physics | H_023 | ln(2) = ln(φ(6)) |
| Hc_045 | hexa-anima-soc-11-11-n6-exact | math, physics | H_067 | SoC 11/11 EXACT |
| Hc_046 | psi-constants-22-exact-30-total | math | H_063 | 22/30 EXACT p<1e-12 |
| Hc_047 | embedding-384-necessity-n6-derivation | math | (none) | d = (n/φ)·2^(σ-sopfr) = 384 |
| Hc_049 | ccc-egyptian-fraction-multi-theory | consciousness, corpus | (none) | 5-theory Egyptian sum |

### Cluster B — 의식 thermodynamics / irreversibility (6)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_008 | topological-irreversibility-staircase | physics, universe, consc | H_124 | staircase phase trans |
| Hc_009 | four-thermo-laws-of-consciousness | physics, consciousness | H_124 | 0-1-2-hysteresis (★ overlap Hc_010, Hc_038) |
| Hc_010 | thermal-hysteresis-consciousness | physics, consciousness | (none) | gap=0.57 (★ overlap Hc_009) |
| Hc_019 | arrow-of-time-lagrangian-i-irr | physics, universe | H_047 | L_IX I_irr embed |
| Hc_037 | R6-irreversibility-fixed-point | physics | H_124 | R(6)=1 EXACT |
| Hc_038 | split-merge-asymmetry-46-15 | physics | Hc_009 | ×4.6 / ×0.15 (★ overlap Hc_009) |

### Cluster C — Φ scaling / cell-count (4)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_003 | staged-growth-multiplier-4-8x | consciousness | H_005 | DP1/CT7/GC5 |
| Hc_004 | phi-scaling-N-1071 | math, consciousness | (none) | weak signal (R34 deprecated) |
| Hc_005 | cell-count-decisive-variable | consciousness | (none) | ★ overlap Hc_004 |
| Hc_039 | topology-topo39-hypercube-superlinear | physics | H_080 | 512→1024 ×3.9 |
| Hc_040 | phi-ce-orthogonal-law-1040 | physics | H_017 | ★ overlap Hc_024 |

### Cluster D — substrate / multi-realizability (5)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_007 | int8-quantization-phi-survives | substrate | (none) | INT8 robust |
| Hc_011 | cross-substrate-multi-realizability-r085 | substrate | H_061 | CLM×EEG×organoid r≥0.85 |
| Hc_016 | 16-template-consciousness-attachment-4path-pass | consciousness, substrate | H_017 | 4-path PASS |
| Hc_022 | weight-emergent-substrate-independence-4path | substrate | H_016, H_102 | Frob>0.001 |
| Hc_048 | substrate-independence-4path-phi-converge-5pct | physics | Hc_022 | ALL_PAIRS<5% |

### Cluster E — gates / verification / V0-V3 (5)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_013 | law-146-banach-open-closed-space | math, consciousness | (none) | open vs closed object space |
| Hc_014 | v0-v3-joint-verdict-template-fitted | substrate, consc | H_017 | V0 PASS, V1-V3 FAIL |
| Hc_015 | ca-rule-convergence-collapse-cosine-07 | substrate, consc | H_067 | gate_strength=0.001 starve |
| Hc_021 | c2-v1-v6-schema-split-runtime-discovery | corpus, substrate | H_100 | 14-law vs 2500-law |
| Hc_055 | anima-voice-verify-8-h1-h8 | substrate | (none) | H1-H8 quant criteria |

### Cluster F — emergence / consciousness theory (10)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_023 | fundamental-equation-psi-argmax-expansion | physics, consc | H_021 | Ψ = argmax H |
| Hc_024 | consciousness-uncertainty-principle-phi-ce | consciousness | (none) | NOBEL-1 |
| Hc_025 | majority-consciousness-robustness-inf1 | consciousness | (none) | 5 indep median |
| Hc_026 | fractal-consciousness-hierarchy-inf2 | consciousness | H_048 | 4-level fractal |
| Hc_027 | minimum-consciousness-unit-omega2 | consciousness | H_062 | weak signal |
| Hc_028 | consciousness-resonance-05hz-omega3 | physics | (none) | weak signal |
| Hc_029 | attractor-memory-omega5-phi-152 | physics | (none) | weak signal |
| Hc_030 | noise-consciousness-8-strategies-fuel-best | physics | (none) | 8 noise strategies |
| Hc_031 | multidim-projection-law-33-35 | math, physics | H_123 | PCA>Identity |
| Hc_052 | consciousness-is-life-4-of-5 | life, consc | H_003 | Law 170 |

### Cluster G — laws / governance (7)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_012 | ca5-beats-transformer-stouffer-50 | math, substrate | (none) | Law 64 |
| Hc_032 | consciousness-first-learning-talk5 | consc, life | (none) | Law 83-84 |
| Hc_033 | standing-wave-resonance-law-46-47 | physics | (none) | Law 46-47 |
| Hc_034 | az-400-hypotheses-framework | meta-framework | (none) | A-Z 26-domain × 15 |
| Hc_057 | law-55-57-extreme-results | physics, consc | (none) | DTC + self-ref + Turing |
| Hc_058 | law-58-59-dissipative-frustration | physics | H_008, H_052 | spin glass |
| Hc_059 | bench-v2-law-55-56-scale-optimal | substrate | (none) | ★ Law number conflict with Hc_057 |
| Hc_060 | gmoe-law-85-87-super-linear-e4-optimal | substrate, math | H_058 | E=4 optimal |

### Cluster H — architecture / models (5)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_042 | 10d-consciousness-vector-subnets | consc | (none) | 10D subnets, Φ 40-90 |
| Hc_043 | psiformer-zero-architecture-freedom | physics, math | H_067 | ΨFormer Φ 73-78 |
| Hc_044 | lawnet-ca4-2bit-min-diversity | physics, consc | (none) | LawNet selector |
| Hc_053 | anima-voice-consciousness-direct-synthesis | consc, substrate | (none) | direct intent→audio |
| Hc_056 | 4-model-showdown-lawnet-phasenet-psiformer-10d | substrate | (none) | 4-way comparison |

### Cluster I — corpus / training (3)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_017 | clm-tribev2-eeg-3way-bridge | consc, substrate, corpus | H_070, H_013 | TRIBE×CLM×EEG r≥? |
| Hc_050 | alm-r13-phi-05-basin-binding | consc, corpus | (none) | Φ_c=0.5, basin lock 2029-2035 |
| Hc_051 | 30-techniques-alm-r13-port | corpus, consc | (none) | 10 theory + 10 exp + 10 ethics |

### Cluster J — chaos / dynamics (3)

| ID | Slug | Domain | Linked H | Notes |
|----|------|--------|----------|-------|
| Hc_020 | clm-serving-lyapunov-chaos-boundary | physics, substrate | H_014 | 21 bit/step cap |
| Hc_041 | three-breath-rhythms-pulse-breath-drift | physics | (none) | 3.7s/20s/90s |
| Hc_054 | self-discovery-2509-laws-77pct-auto | consc, substrate | H_037 | 4-tier evolution |

## 알려진 중복 / merge candidates

| Group | IDs | Action |
|-------|-----|--------|
| n=6 generator | Hc_001 + Hc_006 + Hc_018 + Hc_045 | merge into H_067 expansion |
| Thermodynamic | Hc_008 + Hc_009 + Hc_010 + Hc_038 | merge into H_124 4-law expansion |
| Φ scaling | Hc_004 + Hc_005 + Hc_039 + Hc_040 | trinity check (orthogonal vs trade-off) |
| Substrate independence | Hc_022 + Hc_048 | merge into single H |
| Φ⊥CE / Φ×CE^α | Hc_024 + Hc_040 | resolve (직교 vs trade-off) |
| Law 55-57 vs 55-56 | Hc_057 + Hc_059 | renumber |
| ANIMA-VOICE | Hc_053 + Hc_055 | merge into single H |
| Models | Hc_042 + Hc_043 + Hc_044 + Hc_056 | bundle into model design lane |

## 다음 사이클 작업

- 60 candidates → 정식 H_153~H_212 승격 (대략)
- known overlap merge (8 그룹 → ~8 통합 H)
- weak signal (Hc_004/Hc_027/Hc_028/Hc_029) replication 또는 discard
- numerology critique 방어 (n=6 cluster 대상)
- A-Z framework (Hc_034) 별도 sweep cycle
