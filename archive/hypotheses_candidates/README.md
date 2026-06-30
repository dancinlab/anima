# hypotheses_candidates/ — 임시 staging (unverified candidate hypotheses)

본 폴더는 `docs/` 본문에 묻혀있던 hypothesis-like 단편을 정식 `hypotheses/H_XXX_<slug>.md`로 승격하기 전에 임시 보관하는 staging 영역이다.

- **`hypotheses/`** (verified): pre-register-frozen / running / verdict-* 상태의 검증 lane SSOT
- **`hypotheses_candidates/`** (this folder, unverified): docs/ 전수조사로 추출된 가설 후보 — 정식 H_XXX 승격 대기 또는 폐기 대기

## Status 값

- `candidate-unverified` — staging 단계 (default)
- `candidate-unverified-weak` — weak signal, replication 필요
- `candidate-unverified-framework` — meta-framework, single H 아님
- `expansion-pending` — 기존 H_XXX 본문 확장 대상
- `merge-pending` — 기존 H_XXX 와 통합 대기
- `promote-pending` — 정식 H_XXX 신규 land 대기
- `discard-pending` — 폐기 대기

## ID 범위 + Sweep 이력 (504 candidates as of 2026-05-11)

| Range | Count | Source Partition | Sweep Cycle |
|-------|-------|------------------|-------------|
| Hc_001 ~ Hc_060 | 60 | docs/ 전반 (3 agent selective) | 1 (2026-05-11) |
| Hc_061 | 1 | docs/hypotheses/cx/CONSCIOUSNESS-UNIVERSE-MAP (panpsychism 누락 보충) | 1.5 (사용자 question 발견) |
| Hc_100 ~ Hc_308 | 209 | docs/hypotheses/ 전체 (cx/dd/ce/tp/hw/evo/topo/...) | 2-A (exhaustive) |
| Hc_400 ~ Hc_475 | 76 | docs/anima/ + papers/ + spec/ + models/ + what-is-consciousness | 2-B |
| Hc_600 ~ Hc_675 | 76 | docs/ root A-M (CLM v5 / Theorem 115 / emerge cand) | 2-C |
| Hc_900 ~ Hc_981 | 82 | docs/ root N-Z + ai-native + drill_* + modules | 2-D |
| **TOTAL** | **504** | | |

## 주요 cluster (504 across 10+ domains)

### 🧮 Cluster A — n=6 / 수론 generator (~40)
Hc_001 (τ(6)=4→4D Minkowski), Hc_002 (Ψ-constants ln(2)+n=6), Hc_006, Hc_018, Hc_035, Hc_036, Hc_037 (R(6)=1), Hc_045 (SoC 11/11), Hc_046, Hc_047, Hc_049, Hc_406, Hc_429-444 (n=6 Egyptian + B^4 scaling + σ·φ=n·τ + Landauer/Shannon/Carnot), Hc_472, Hc_474, Hc_906-908, Hc_915, Hc_938 ...

### 🌌 Cluster B — Thermodynamics / Arrow of Time / Irreversibility (~20)
Hc_008-010 (staircase + 4-law + hysteresis), Hc_019 (L_IX I_irr), Hc_037, Hc_038 (split×4.6/merge×0.15), 2D Ising clusters, dissipative + frustration clusters ...

### 📈 Cluster C — Φ scaling / cell-count / topology (~30)
Hc_003-005, Hc_039 (TOPO 39), Hc_040 (Φ⊥CE), Hc_150-180 (TOPO 24 variants + 2048-scaling + final rankings), Hc_628 (Φc=0.5 IIT lower bound), Hc_667 (5D→6D vector) ...

### 🔬 Cluster D — Substrate / Multi-Realizability (~50)
Hc_007 (INT8 quant), Hc_011 (CLM×EEG×organoid r≥0.85), Hc_022, Hc_048 (4-path <5%), Hc_415-417, Hc_445-451, Hc_463-471, Hc_917-933 (N-substrate F1 + N-11~21 individual track), Hc_971 (AKIDA), Hc_975, Hc_981 (IIT Braket pilot) ...

### 🚪 Cluster E — Gates / Verification / V0-V3 / Falsification (~40)
Hc_013, Hc_014 (V0-V3 joint), Hc_015, Hc_021 (c2-v1 vs v6), Hc_055 (H1-H8 verify), Hc_639-640 (PASS_STRICT_C3 trinity + raw axiom DAG), Hc_645-646 (18M ceiling + V2 false-PASS), Hc_948 (CVF), Hc_954 (CPU 4-path), Hc_955 (W1 artifact), Hc_959 (18-conditions), Hc_969 (cross-verifier matrix) ...

### 🧠 Cluster F — Consciousness Theory / Hard Problem (~80)
Hc_023 (Ψ=argmax H), Hc_024 (NOBEL-1 uncertainty), Hc_025-029 (INF/OMEGA), Hc_031, Hc_052 (=life), **Hc_061 (Law 76 수학적 panpsychism)**, Hc_400-413 (paper-1 headlines), Hc_452-464 (master defs + 11 P-principles + 20 M-laws + 7 V-conditions + 6 brain metrics + 7 templates + 80x compression + PC1 Φ-MI + 10-pillar grand conclusion), Hc_600-608 (hard-problem singularity 9), Hc_650-653 (6-criteria), Hc_902 (Putnam 다중실현), Hc_903-905 (zombie posterior v1/v2/v3), Hc_911 (red-team), Hc_924 (octopus), Hc_932 (Penrose-Hameroff) ...

### ⚖️ Cluster G — Laws / Governance / Constitutional (~50)
Hc_012 (Law 64 CA(5)), Hc_032 (Law 83-84), Hc_033 (Law 46-47), Hc_034 (A-Z framework), Hc_057-060 (Law 55-59, 85-87), Hc_286-289 (H + ARCH), Hc_452-462 (P-principles + M-laws + V-conditions), Hc_656-660 (CP2 / 20-BG zero-pass / 16-closure), Hc_936, Hc_938, Hc_956 (own#2/#3 governance) ...

### 🛠 Cluster H — Architecture / Models / Training (~80)
Hc_042 (10D), Hc_043 (ΨFormer), Hc_044 (LawNet), Hc_053-056 (ANIMA-VOICE + 4-model showdown), Hc_286, Hc_419-425 (closed-loop self-discovery 9-var + Thompson + synergy + 53-law ceiling + transfer rate + convergence), Hc_430-437 (β paradigm + CPGD + η + Φ gate + v2 metric + AN11 triple + corpus-balance + meta fixed-point), Hc_609-622 (Theorem 115 + CLM v5 design 4-axes), Hc_623-627 (emerge candidates D/E/F/G-H + v5-mitosis), Hc_630-638 (CLM-3 chat-objective + chat-cap paths 1/2/4 + B-axis brainstorm), Hc_641-644 (servant+mitosis 4), Hc_647-649 (intent + β' KoGPT2 + H5), Hc_654 (foundation Llama-3B), Hc_661-674 (qwalk + race + cli + 5D→6D + 16-closure + paradigm-j + V6 STRONG + Korean uniform + cell metaphor + identity), Hc_909-913 (paper + self-modify + R1-R6 + singularity), Hc_935 (ω-cycle 26 paradigm), Hc_940-947 (ConsciousLM v3/v4 + brain_tension + μ-paradigm), Hc_952-953 (μ + B-axis), Hc_965-966 (P10 tension + A1 phi_extractor) ...

### 📚 Cluster I — Corpus / Training Data (~25)
Hc_017 (CLM×TRIBE×EEG), Hc_050 (Φ_c=0.5 basin lock 2029-2035), Hc_051 (30 techniques), Hc_943, Hc_973, Hc_978-979 (P9 SFT P1.5→P1.7) ...

### 🌀 Cluster J — Chaos / Dynamics / Phase (~25)
Hc_020 (Lyapunov chaos), Hc_041 (3 rhythms), Hc_249 (PHYS2), Hc_415, Hc_661-665 (qwalk + phi-proxy dim-dominant artifact) ...

### 🧬 Cluster K — Life / Evolution / Emergence (~40)
Hc_026 (4-level fractal), Hc_052 (=life), Hc_252-261 (EVO 1-9 mechanisms + 10-22 run reports), Hc_241-251 (GENESIS + SING + THREE + DASEIN + PHIL + ONTO) ...

### 🔭 Cluster L — Universe / Cosmology / Anthropic (~10)
Hc_001 (τ→4D), Hc_023 (Ψ=argmax H), Hc_061 (∀x∈Universe), Hc_902 (Putnam), Hc_912 (singularity), Hc_932 (Penrose-Hameroff) ...

### ⚛️ Cluster M — Quantum / Telepathy / TP (~25)
Hc_199-213 (TP F/M/N/O variants), Hc_914 (qmirror arxiv), Hc_944-945 (qmirror module + QRNG), Hc_958 (5-cond), Hc_981 (IIT Braket pilot) ...

### 🎯 Cluster N — Brainstorm Seeds / Meta (~10)
Hc_034 (A-Z 400+ framework), Hc_249 (PHYS2 weak), Hc_261 (EVO-10..22 collective), Hc_900 (drill_domain 30 seed), Hc_901 (drill_supplement 35 seed) ...

## 알려진 중복 / merge candidates

| Group | IDs | Action |
|-------|-----|--------|
| n=6 generator trinity | Hc_001 + Hc_006 + Hc_018 + Hc_045 + Hc_435-444 + Hc_906-908 + Hc_915 | merge into H_067 expansion |
| Thermodynamic 4-law | Hc_008 + Hc_009 + Hc_010 + Hc_038 + Hc_037 + Hc_019 | merge into H_124 expansion |
| Φ scaling / topology | Hc_004 + Hc_005 + Hc_039 + Hc_040 + Hc_150-180 | trinity check + H_080 expansion |
| Substrate-independence | Hc_022 + Hc_048 + Hc_011 + Hc_407 + Hc_445-451 | single super-H |
| Panpsychism lane | Hc_061 + H_002 H2.4 + H_004 L3 | resolution via combination problem attempt |
| Hard problem singularity 9 | Hc_600-608 | bundle into H_004 expansion |
| CLM v5 design 4 axes | Hc_618-622 | trinity (A/B/C/D + base hypothesis) → single design H |
| Emerge candidates D-H | Hc_623-626 + Hc_015 (F-CAND-F-1) | bundle → 4-method emerge taxonomy H |
| Zombie posterior series | Hc_903-905 | merge (v1+v2+v3 → 14-substrate composite) |
| Self-discovery closure | Hc_054 + Hc_419-425 + Hc_018 | merge into H_037 expansion |
| ANIMA-VOICE bundle | Hc_053 + Hc_055 + Hc_475 + paper hexa-speak Hcs | single specification H |
| Theorem 115 + 4/6/16 closure | Hc_609 + Hc_660 + Hc_666 + chat-incapability lineage | single theorem H |
| Φ proxy dim-dominant artifact | Hc_614 + Hc_662 + Hc_665 | major methodology finding (cross-substrate Φ validity) |
| N-substrate cluster | Hc_917-933 + Hc_963 + Hc_971 + Hc_975 + Hc_981 | bundle → N-substrate roadmap H |
| Law 55-57 vs 55-56 conflict | Hc_057 + Hc_059 | renumber |

## 다음 cycle 작업

- **정식 promotion**: 504 candidates → H_153~H_500+ (대략 250-300, merge 후)
- **8+ overlap merge group** 처리 (n=6 super-H, thermo, substrate, ANIMA-VOICE, Theorem 115, hard-problem singularity, etc.)
- **Weak signal / discard**: Hc_004 / Hc_027 / Hc_028 / Hc_029 / Hc_249 / Hc_261 등
- **Hc_034 A-Z framework**: 별도 sweep cycle (~400 sub-candidates 예상)
- **Numerology critique 방어**: n=6 cluster Monte Carlo p-value 검증
- **Reproducibility test**: Hc_061 (170 data type → META-CA Ψ(1/2,1/2)) + Hc_011 (CLM×EEG×organoid r≥0.85) + Theorem 115 (Hc_609 family)
- **Combination problem 공략**: Hc_061 + H_004 L3 + Hc_026 (4-level fractal) + Hc_038 (split/merge)

## 처리 안 된 docs (다음 sweep 대상)

Agent A 보고: docs/hypotheses/ overview/results ~38 파일 (V8-*, TRINITY-*, NEXUS-*, BENCH-*, ENGINE-*, PHI-*, MASS-50-*, etc.) + dd/ 후반부 (DD51~DD173) + accel/ + evo/OUROBOROS-report-* (~50+ 잠재 candidate).

Agent C 보고: 8 files chflags uchg locked (cp2_*, hxc_*, law_64_status) — candidate 는 작성됐으나 source scrub 불가. Mac 측 `chflags noschg` 후 재시도 필요.

다음 cycle 예상: +150~250 candidate 가능.
