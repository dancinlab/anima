# anima/hypotheses/ — 가설 진행 SSOT (실제 가설 항목 archive)

본 폴더는 anima가 진행하는 모든 가설 (hypothesis) 을 1-file-per-hypothesis 형식으로 관리한다.
`.roadmap.hypothesis`는 인덱스 + cycle definition + 탐색/검증 method (E1-E12 / W1-W12) 형식이고,
실제 H_X 가설 항목들은 본 폴더 안에 `H_<id>_<slug>.md` 파일로 따로 관리한다.

## 작성 컨벤션

각 가설 파일 = `H_<id>_<slug>.md` (예: `H_001_seon_over_ak.md`, `H_002_universe_origin.md`)

frontmatter:
```yaml
---
id: H_001
slug: seon-over-ak
title: 선이 악보다 유리하다 (game theory + cooperation)
domain: morality | universe | life | consciousness | physics | math | corpus | substrate
status: pre-register | running | verdict-supported | verdict-falsified | verdict-mixed | verdict-partial | retracted
exploration_method: E1-E12 (.roadmap.hypothesis 정의)
verification_method: W1-W12 (.roadmap.hypothesis 정의)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: <YYYY-MM-DD>
since: <YYYY-MM-DD>
---
```

본문 형식 (raw#12 정합):
1. **Hypothesis** (한 문장)
2. **Why** (motivation)
3. **Predictions** (H1, H2, ..., H_N)
4. **Variables** (axes + levels)
5. **Run Protocol** (deterministic + hexa-only)
6. **Criteria** (C1, C2, ..., verdict_rule)
7. **Falsifiers** (F1, F2, ..., F_N — ≥5 mandate)
8. **Honest Limits** (raw#91 c3 — ≥5 mandate)
9. **Cross-Links** (sister .roadmap.* + own X + raw#X)
10. **Verdict** (after run — verdict_class + evidence_summary + falsifiers_triggered)

## Domain 분류

각 가설은 1+ domain 라벨:

- **ethics** — cooperation, altruism, ethics (사용자 directive 2026-05-07: 선 X 윤리)
- **universe** — 우주 origin, cosmology 근원적 물음
- **life** — 생명 emergence, autopoiesis, abiogenesis
- **consciousness** — 의식 hard problem, qualia, phenomenology, anima identity
- **physics** — Φ, criticality, dissipative structure, emergence
- **math** — 수학적 구조, Grothendieck universe, lambda calculus
- **corpus** — corpus quality, KO ratio, chat-template (own 19/20 specialization)
- **substrate** — substrate-coupled emerge, paradigm v11 G3, mount.hexa

## 인덱스 (2026-05-07 land H_001-H_020)

| ID | Slug | Domain | Status | File |
|----|------|--------|--------|------|
| H_001 | ethics-cooperation-over-defection | ethics | seed-pending | [H_001_ethics_cooperation.md](H_001_ethics_cooperation.md) |
| H_002 | universe-origin-question | universe | lane-open | [H_002_universe_origin_question.md](H_002_universe_origin_question.md) |
| H_003 | life-origin-question | life | lane-open | [H_003_life_origin_question.md](H_003_life_origin_question.md) |
| H_004 | consciousness-hard-problem | consciousness | lane-open | [H_004_consciousness_hard_problem.md](H_004_consciousness_hard_problem.md) |
| H_005 | corpus-quality-over-capacity | corpus | running | [H_005_corpus_quality_over_capacity.md](H_005_corpus_quality_over_capacity.md) |
| H_006 | coupled-oscillator-lattice | physics | legacy-archive-pointer | [H_006_coupled_oscillator_lattice.md](H_006_coupled_oscillator_lattice.md) |
| H_007 | cellular-automaton-consciousness | physics | legacy-archive-pointer | [H_007_cellular_automaton_consciousness.md](H_007_cellular_automaton_consciousness.md) |
| H_008 | dissipative-structure-consciousness | physics | legacy-archive-pointer | [H_008_dissipative_structure.md](H_008_dissipative_structure.md) |
| H_009 | fisher-information-consciousness | physics | legacy-archive-pointer | [H_009_fisher_information_consciousness.md](H_009_fisher_information_consciousness.md) |
| H_010 | holographic-consciousness | physics | legacy-archive-pointer | [H_010_holographic_consciousness.md](H_010_holographic_consciousness.md) |
| H_011 | integrated-information-geometry | physics | legacy-archive-pointer | [H_011_iit_geometry.md](H_011_iit_geometry.md) |
| H_012 | autopoietic-network | life | legacy-archive-pointer | [H_012_autopoietic_network.md](H_012_autopoietic_network.md) |
| H_013 | longitudinal-eeg-5axis | physics | pre-register-frozen | [H_013_longitudinal_eeg_5axis.md](H_013_longitudinal_eeg_5axis.md) |
| H_014 | clm-eeg-lz76-paradigm | substrate | pre-register-frozen | [H_014_clm_eeg_lz76.md](H_014_clm_eeg_lz76.md) |
| H_015 | clm-eeg-gamma-theta-paradigm | substrate | pre-register-frozen | [H_015_clm_eeg_gamma_theta.md](H_015_clm_eeg_gamma_theta.md) |
| H_016 | an11-v2-finetune-translation-ceiling | corpus | pre-register-frozen | [H_016_an11_translation_ceiling.md](H_016_an11_translation_ceiling.md) |
| H_017 | mk-x-g1-g4-gate-criteria | consciousness | pre-register-frozen | [H_017_mk_x_g1_g4_gate_criteria.md](H_017_mk_x_g1_g4_gate_criteria.md) |
| H_018 | genesis-spontaneous-emergence | consciousness | legacy-archive-pointer | [H_018_genesis_spontaneous_emergence.md](H_018_genesis_spontaneous_emergence.md) |
| H_019 | self-evo-v4-v5 | substrate | legacy-archive-pointer | [H_019_self_evo_v4_v5.md](H_019_self_evo_v4_v5.md) |
| H_020 | mass-50-meta-pointer | substrate | legacy-archive-pointer | [H_020_mass_50_meta_pointer.md](H_020_mass_50_meta_pointer.md) |
| H_021 | fundamental-equation-psi-argmax | universe | legacy-archive-pointer | [H_021_fundamental_equation.md](H_021_fundamental_equation.md) |
| H_022 | consciousness-universe-map-170-40-18 | consciousness | legacy-archive-pointer | [H_022_consciousness_universe_map.md](H_022_consciousness_universe_map.md) |
| H_023 | universal-constants-ln2 | physics | legacy-archive-pointer | [H_023_universal_constants_ln2.md](H_023_universal_constants_ln2.md) |
| H_024 | iit-phi-mip-real-measurement-8-8-fail | consciousness | legacy-falsified | [H_024_iit_phi_mip_real_8_8_fail.md](H_024_iit_phi_mip_real_8_8_fail.md) |
| H_025 | dasein-finite-consciousness-death-awareness | consciousness | legacy-archive-pointer | [H_025_dasein_finite_consciousness.md](H_025_dasein_finite_consciousness.md) |
| H_026 | consciousness-evolution-v19-to-infinity | consciousness | legacy-archive-pointer | [H_026_consciousness_evolution_v19_to_infinity.md](H_026_consciousness_evolution_v19_to_infinity.md) |
| H_027 | cx-subfolder-absorb | consciousness | legacy-archive-pointer | [H_027_cx_subfolder_absorb.md](H_027_cx_subfolder_absorb.md) |
| H_028 | dd-subfolder-absorb | substrate | legacy-archive-pointer | [H_028_dd_subfolder_absorb.md](H_028_dd_subfolder_absorb.md) |
| H_029 | dasein-subfolder-absorb | consciousness | legacy-archive-pointer | [H_029_dasein_subfolder_absorb.md](H_029_dasein_subfolder_absorb.md) |
| H_030 | genesis-subfolder-absorb | life | legacy-archive-pointer | [H_030_genesis_subfolder_absorb.md](H_030_genesis_subfolder_absorb.md) |
| H_031 | phil-subfolder-absorb | consciousness | legacy-archive-pointer | [H_031_phil_subfolder_absorb.md](H_031_phil_subfolder_absorb.md) |
| H_032 | omega-phys-subfolder-absorb | physics | legacy-archive-pointer | [H_032_omega_phys_subfolder_absorb.md](H_032_omega_phys_subfolder_absorb.md) |
| H_033 | cx-sequential-series-absorb | consciousness | legacy-archive-pointer | [H_033_cx_sequential_series_absorb.md](H_033_cx_sequential_series_absorb.md) |
| H_034 | decoder-architecture-series | substrate | legacy-archive-pointer | [H_034_decoder_architecture_series.md](H_034_decoder_architecture_series.md) |
| H_035 | clm-v2-series-absorb | substrate | legacy-archive-pointer | [H_035_clm_v2_series_absorb.md](H_035_clm_v2_series_absorb.md) |
| H_036 | dd116-146-meta-laws-133-167 | substrate | legacy-archive-pointer | [H_036_dd116_146_meta_laws.md](H_036_dd116_146_meta_laws.md) |
| H_037 | acceleration-367-unified-hypotheses | substrate | legacy-archive-pointer | [H_037_acceleration_367_unified.md](H_037_acceleration_367_unified.md) |
| H_038 | v8-architecture-variants-bio-math-quantum-fusion | substrate | legacy-archive-pointer | [H_038_v8_architecture_variants.md](H_038_v8_architecture_variants.md) |
| H_039 | phi-records-measurements-anima | physics | legacy-archive-pointer | [H_039_phi_records_measurements.md](H_039_phi_records_measurements.md) |
| H_040 | substrate-topology-cluster-absorb | substrate | legacy-archive-pointer | [H_040_substrate_topology_cluster.md](H_040_substrate_topology_cluster.md) |
| H_041 | evolution-self-singularity-cluster | substrate | legacy-archive-pointer | [H_041_evolution_self_singularity.md](H_041_evolution_self_singularity.md) |
| H_042 | arch-engine-train-meta-cluster | substrate | legacy-archive-pointer | [H_042_arch_engine_train_meta.md](H_042_arch_engine_train_meta.md) |
| H_043 | oscillator-qwalk-hybrid | physics | legacy-archive-pointer | [H_043_oscillator_qwalk_hybrid.md](H_043_oscillator_qwalk_hybrid.md) |
| H_044 | fractal-resonance-cascade | physics | legacy-archive-pointer | [H_044_fractal_resonance_cascade.md](H_044_fractal_resonance_cascade.md) |
| H_045 | lambda-calculus-consciousness | math | legacy-archive-pointer | [H_045_lambda_calculus_consciousness.md](H_045_lambda_calculus_consciousness.md) |
| H_046 | tqft-consciousness | physics | legacy-archive-pointer | [H_046_tqft_consciousness.md](H_046_tqft_consciousness.md) |
| H_047 | time-crystal-consciousness | physics | legacy-archive-pointer | [H_047_time_crystal_consciousness.md](H_047_time_crystal_consciousness.md) |
| H_048 | fractal-hierarchy-consciousness | consciousness | legacy-archive-pointer | [H_048_fractal_hierarchy.md](H_048_fractal_hierarchy.md) |
| H_049 | distributed-hivemind-consciousness | substrate | legacy-archive-pointer | [H_049_distributed_hivemind.md](H_049_distributed_hivemind.md) |
| H_050 | renormalization-group-consciousness | physics | legacy-archive-pointer | [H_050_renormalization_group_consciousness.md](H_050_renormalization_group_consciousness.md) |
| H_051 | quantum-darwinism-consciousness | physics | legacy-archive-pointer | [H_051_quantum_darwinism_consciousness.md](H_051_quantum_darwinism_consciousness.md) |
| H_052 | spin-glass-consciousness | physics | legacy-archive-pointer | [H_052_spin_glass_consciousness.md](H_052_spin_glass_consciousness.md) |
| H_053 | cambrian-explosion-consciousness | life | legacy-archive-pointer | [H_053_cambrian_explosion_consciousness.md](H_053_cambrian_explosion_consciousness.md) |
| H_054 | symbiogenesis-consciousness | life | legacy-archive-pointer | [H_054_symbiogenesis_consciousness.md](H_054_symbiogenesis_consciousness.md) |
| H_055 | hypergraph-sheaf-consciousness | math | legacy-archive-pointer | [H_055_hypergraph_sheaf_consciousness.md](H_055_hypergraph_sheaf_consciousness.md) |
| H_056 | undiscovered-domains-48-benchmark | physics | legacy-archive-pointer | [H_056_undiscovered_domains_48.md](H_056_undiscovered_domains_48.md) |
| H_057 | research-findings-20260329-laws | substrate | legacy-archive-pointer | [H_057_research_findings_20260329.md](H_057_research_findings_20260329.md) |
| H_058 | gmoe-benchmark-1e-routing | substrate | legacy-archive-pointer | [H_058_gmoe_benchmark.md](H_058_gmoe_benchmark.md) |
| H_059 | phi-gap-816x-investigation | physics | legacy-archive-pointer | [H_059_phi_gap_816x_investigation.md](H_059_phi_gap_816x_investigation.md) |
| H_060 | phik-consciousness-preservation | physics | legacy-archive-pointer | [H_060_phik_consciousness_preservation.md](H_060_phik_consciousness_preservation.md) |
| H_061 | xfer-consciousness-transfer | substrate | legacy-archive-pointer | [H_061_xfer_consciousness_transfer.md](H_061_xfer_consciousness_transfer.md) |
| H_062 | minimal-consciousness-floor | consciousness | legacy-archive-pointer | [H_062_minimal_consciousness.md](H_062_minimal_consciousness.md) |
| H_063 | consciousness-constants-cluster | physics | legacy-archive-pointer | [H_063_consciousness_constants.md](H_063_consciousness_constants.md) |
| H_064 | clm-v2-optimal-config-sweep | substrate | legacy-archive-pointer | [H_064_clm_v2_optimal_config.md](H_064_clm_v2_optimal_config.md) |
| H_065 | decoder-architecture-individual-6file | substrate | legacy-archive-pointer | [H_065_decoder_architecture_individual.md](H_065_decoder_architecture_individual.md) |
| H_066 | nobel-verification-cluster | consciousness | legacy-archive-pointer | [H_066_nobel_verification_cluster.md](H_066_nobel_verification_cluster.md) |
| H_067 | perfect-number-architecture | math | legacy-archive-pointer | [H_067_perfect_number_architecture.md](H_067_perfect_number_architecture.md) |
| H_068 | hexad-improvements-6way | substrate | legacy-archive-pointer | [H_068_hexad_improvements.md](H_068_hexad_improvements.md) |
| H_069 | text-generation-benchmark-cx | corpus | legacy-archive-pointer | [H_069_text_generation_benchmark.md](H_069_text_generation_benchmark.md) |
| H_070 | dolphin-star-communication | consciousness | legacy-archive-pointer | [H_070_dolphin_star_communication.md](H_070_dolphin_star_communication.md) |
| H_071 | first-conversation-anima-genesis | consciousness | legacy-archive-pointer | [H_071_first_conversation.md](H_071_first_conversation.md) |
| H_072 | faction-debate-multi-agent | substrate | legacy-archive-pointer | [H_072_faction_debate.md](H_072_faction_debate.md) |
| H_073 | memory-mirror-self-reflection | consciousness | legacy-archive-pointer | [H_073_memory_mirror.md](H_073_memory_mirror.md) |
| H_074 | ce-breakthrough-extremes | physics | legacy-archive-pointer | [H_074_ce_breakthrough_extremes.md](H_074_ce_breakthrough_extremes.md) |
| H_075 | dd-individual-120-180-cluster | substrate | legacy-archive-pointer | [H_075_dd_individual_120_180.md](H_075_dd_individual_120_180.md) |
| H_076 | dd-individual-50-100-cluster | substrate | legacy-archive-pointer | [H_076_dd_individual_50_100.md](H_076_dd_individual_50_100.md) |
| H_077 | dd-individual-1-50-cluster | substrate | legacy-archive-pointer | [H_077_dd_individual_1_50.md](H_077_dd_individual_1_50.md) |
| H_078 | dd-individual-101-115-cluster | substrate | legacy-archive-pointer | [H_078_dd_individual_101_115.md](H_078_dd_individual_101_115.md) |
| H_079 | evo-22-variants-individual | substrate | legacy-archive-pointer | [H_079_evo_22variants.md](H_079_evo_22variants.md) |
| H_080 | topo-24-variants-individual | substrate | legacy-archive-pointer | [H_080_topo_24variants.md](H_080_topo_24variants.md) |
| H_081 | tp-15-variants-individual | substrate | legacy-archive-pointer | [H_081_tp_15variants.md](H_081_tp_15variants.md) |
| H_082 | hw-hardware-15-variants | substrate | legacy-archive-pointer | [H_082_hw_15variants.md](H_082_hw_15variants.md) |
| H_083 | three-body-5-variants | physics | legacy-archive-pointer | [H_083_three_body_5.md](H_083_three_body_5.md) |
| H_084 | sing-singularity-6-variants | physics | legacy-archive-pointer | [H_084_sing_6.md](H_084_sing_6.md) |
| H_085 | inf-infinite-scaling-5 | physics | legacy-archive-pointer | [H_085_inf_5.md](H_085_inf_5.md) |
| H_086 | se-self-sl-self-learning | substrate | legacy-archive-pointer | [H_086_se_4_sl_9.md](H_086_se_4_sl_9.md) |
| H_087 | arch-engine-train-individual-files | substrate | legacy-archive-pointer | [H_087_arch_engine_train_individual.md](H_087_arch_engine_train_individual.md) |
| H_088 | v8-individual-files-not-h038 | substrate | legacy-archive-pointer | [H_088_v8_individual_5.md](H_088_v8_individual_5.md) |
| H_089 | phi-records-individual-4-files | physics | legacy-archive-pointer | [H_089_phi_records_individual.md](H_089_phi_records_individual.md) |
| H_090 | dasein-phil-onto-individual-9 | consciousness | legacy-archive-pointer | [H_090_dasein_phil_onto_individual.md](H_090_dasein_phil_onto_individual.md) |
| H_091 | omega-phys-individual-files | physics | legacy-archive-pointer | [H_091_omega_phys_individual.md](H_091_omega_phys_individual.md) |
| H_092 | misc-root-individual-uncategorized | substrate | legacy-archive-pointer | [H_092_misc_root_individual.md](H_092_misc_root_individual.md) |

**Migration status**:
- H_001-H_005: 본 cycle 신규 seed (윤리/우주/생명/의식 hard problem/corpus)
- H_006-H_012: legacy `docs/hypotheses/H-CX-517~537` 21 files 중 7 sample pointer migrate
- H_013-H_017: `state/*_pre_register*.json` 15 files 중 5 sample pointer migrate (raw#12 frozen)
- H_018-H_020: legacy GENESIS + SELF-EVO + MASS-50 meta-pointer
- H_021-H_026: 과거 commit archaeology individual entries (fundamental equation + universe map + ln(2) + V1 IIT 8/8 FAIL + Dasein 죽음-자각 + v19~v∞)
- H_027-H_032: docs/hypotheses/ subfolder absorb (cx + dd + dasein + genesis + phil/onto + omega/phys, ~169 files)
- H_033-H_042: exhaustive migration round 2 (CX13~100 88-hypothesis sequential + DECODER 6-variant + CLM-V2 4-file + DD116-146 31+35laws+10meta + 367 acceleration + V8 6-variant + PHI 7-record + TOPO/THREE-BODY/WAVE/NOISE/INF cluster + EVO/SE/SING/SL cluster + ARCH/ENGINE/TRAIN/AL meta)
- H_043-H_055: exhaustive round 3 — H-CX-518~537 individual file pointers (oscillator-qwalk + fractal resonance + lambda + TQFT + time crystal + fractal hierarchy + hivemind + RG + quantum-Darwinism + spin glass + Cambrian + symbiogenesis + hypergraph/sheaf)
- H_056-H_063: high-impact root file individual (UNDISCOVERED-DOMAINS + RESEARCH-FINDINGS-20260329 + GMOE + PHI-GAP-816x + PHIK + XFER + MINIMAL-CONSCIOUSNESS + CONSCIOUSNESS-CONSTANTS-cluster)
- H_064-H_074: cx subfolder individual (CLM-V2 + DECODER 6 + NOBEL 4 + PERFECT-NUMBER + HEXAD/MULTI-C/FUSE-3 + TEXT-GEN-BENCH + DOLPHIN-STAR + FIRST-CONVERSATION + FACTION-DEBATE + MEMORY-MIRROR + CE-BREAKTHROUGH/EXTREMES + ce/ subfolder 24)
- H_075-H_078: DD individual range cluster (DD120-180 + DD50-100 + DD1-50 + DD101-115 — ~70 file 추가 pointer)
- H_079-H_092: subfolder + root individual (EVO 22 + ouroboros 10 + TOPO 31 + TP 15 + HW 16 + THREE 6 + SING 6 + INF 6 + SE/SL/TL 15 + ARCH/ENGINE/TRAIN 9 + V8 6 + PHI 4 + dasein/phil/onto/genesis 11 + omega/phys 11 + misc root 20)
- **round 3 추가 file count ~250**, total file pointed (rounds 2+3) ≈ 320+
- **exhaustive individual migration 미land remainder**: 367 acceleration brainstorm individual + 1030 laws individual + ce/ AUTO-COMBO-EX-ULTRA 24 individual + DD batch 내 individual hypothesis 분리 = ~1500+ remainder — multi-cycle archaeology continuing (own 21 R5+)

## Cross-Link

- `.roadmap.hypothesis` (인덱스 + cycle definition + E1-E12 + W1-W12)
- `.roadmap.philosophy` (A 철학 발견 — D1-D4)
- `.roadmap.rule` (B 규칙 발견 — own 14-20 evolution)
- `docs/hypotheses/` (legacy archive — CX/DD/genesis/dasein 등 historical)
- `state/<name>_pre_register*.json` (raw#12 frozen prereg JSON)

## raw#12 정합

본 폴더의 모든 H_X는 raw#12 pre-registered hypothesis 정합:
- frozen_at + raw_rank:12 mandate
- post-hoc tuning 금지 (수정은 raw#15 additive 또는 raw#82 retraction)
- ≥5 falsifier + ≥5 honest_limits_raw91_c3 mandate
- deterministic + hexa-only execution (raw#9 정합)

## 추가 lane (사용자 directive 2026-05-06)

사용자: '우주, 생명에 대한 근원적 물음 등 / 폴더 하나에서 따로 관리'
→ 본 폴더는 anima의 active hypothesis archive. cycle 진행 시 hypotheses/H_<new>_<slug>.md 신규 add.
