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
| H_004 | consciousness-hard-problem | consciousness | running | [H_004_consciousness_hard_problem.md](H_004_consciousness_hard_problem.md) |
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
| H_037 | acceleration-367-unified-hypotheses | substrate | running | [H_037_acceleration_367_unified.md](H_037_acceleration_367_unified.md) |
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
| H_061 | xfer-consciousness-transfer | substrate | running | [H_061_xfer_consciousness_transfer.md](H_061_xfer_consciousness_transfer.md) |
| H_062 | minimal-consciousness-floor | consciousness | legacy-archive-pointer | [H_062_minimal_consciousness.md](H_062_minimal_consciousness.md) |
| H_063 | consciousness-constants-cluster | physics | legacy-archive-pointer | [H_063_consciousness_constants.md](H_063_consciousness_constants.md) |
| H_064 | clm-v2-optimal-config-sweep | substrate | legacy-archive-pointer | [H_064_clm_v2_optimal_config.md](H_064_clm_v2_optimal_config.md) |
| H_065 | decoder-architecture-individual-6file | substrate | legacy-archive-pointer | [H_065_decoder_architecture_individual.md](H_065_decoder_architecture_individual.md) |
| H_066 | nobel-verification-cluster | consciousness | legacy-archive-pointer | [H_066_nobel_verification_cluster.md](H_066_nobel_verification_cluster.md) |
| H_067 | perfect-number-architecture | math | running | [H_067_perfect_number_architecture.md](H_067_perfect_number_architecture.md) |
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
| H_080 | topo-24-variants-individual | substrate | running | [H_080_topo_24variants.md](H_080_topo_24variants.md) |
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
| H_093 | sft-only-paradigm | corpus | seed-pending | [H_093_sft_only_paradigm.md](H_093_sft_only_paradigm.md) |
| H_094 | instruction-tuning-two-stage | corpus | seed-pending | [H_094_instruction_tuning_two_stage.md](H_094_instruction_tuning_two_stage.md) |
| H_095 | dpo-rlhf-preference-learning | corpus | seed-pending | [H_095_dpo_rlhf_preference_learning.md](H_095_dpo_rlhf_preference_learning.md) |
| H_096 | in-context-few-shot | corpus | seed-pending | [H_096_in_context_few_shot.md](H_096_in_context_few_shot.md) |
| H_097 | curriculum-learning | corpus | seed-pending | [H_097_curriculum_learning.md](H_097_curriculum_learning.md) |
| H_098 | persona-conditioned-training | consciousness | seed-pending | [H_098_persona_conditioned_training.md](H_098_persona_conditioned_training.md) |
| H_099 | multi-objective-training | corpus | seed-pending | [H_099_multi_objective_training.md](H_099_multi_objective_training.md) |
| H_100 | constitutional-ai-anima-rules | consciousness | seed-pending | [H_100_constitutional_ai.md](H_100_constitutional_ai.md) |
| H_101 | corpus-chat-template-strict-80 | corpus | seed-pending | [H_101_corpus_chat_template_strict_80.md](H_101_corpus_chat_template_strict_80.md) |
| H_102 | anima-emerge-paradigm-cross-link | substrate | seed-pending | [H_102_anima_emerge_paradigm_cross_link.md](H_102_anima_emerge_paradigm_cross_link.md) |
| H_103 | accel-b11-b12-batch-skip-combo-breakthrough | substrate | legacy-archive-pointer | [H_103_accel_b11_b12_batch_skip_combo.md](H_103_accel_b11_b12_batch_skip_combo.md) |
| H_104 | accel-b5-phi-only-training-pre-condition | substrate | legacy-archive-pointer | [H_104_accel_b5_phi_only_training.md](H_104_accel_b5_phi_only_training.md) |
| H_105 | accel-h11-hard-token-data-revolutionary | corpus | legacy-archive-pointer | [H_105_accel_h11_hard_token_data.md](H_105_accel_h11_hard_token_data.md) |
| H_106 | accel-combo-x255-target-achieved | substrate | legacy-archive-pointer | [H_106_accel_combo_x255.md](H_106_accel_combo_x255.md) |
| H_107 | accel-b13-tension-transfer-catalytic | substrate | legacy-archive-pointer | [H_107_accel_b13_tension_transfer.md](H_107_accel_b13_tension_transfer.md) |
| H_108 | accel-e1-batch-skip-manifold-triple | substrate | legacy-archive-pointer | [H_108_accel_e1_triple_combo.md](H_108_accel_e1_triple_combo.md) |
| H_109 | accel-f2-information-bottleneck-decoder-input | substrate | legacy-archive-pointer | [H_109_accel_f2_information_bottleneck.md](H_109_accel_f2_information_bottleneck.md) |
| H_110 | accel-h6-1bit-adam-vram-winner | substrate | legacy-archive-pointer | [H_110_accel_h6_1bit_adam.md](H_110_accel_h6_1bit_adam.md) |
| H_111 | accel-b12-skip-step-star | substrate | legacy-archive-pointer | [H_111_accel_b12_skip_step.md](H_111_accel_b12_skip_step.md) |
| H_112 | accel-c3-entropy-surfing-orthogonal | substrate | legacy-archive-pointer | [H_112_accel_c3_entropy_surfing.md](H_112_accel_c3_entropy_surfing.md) |
| H_113 | accel-d1-topological-shortcut-trajectory-jump | substrate | legacy-archive-pointer | [H_113_accel_d1_topological_shortcut.md](H_113_accel_d1_topological_shortcut.md) |
| H_114 | accel-f4-158bit-consciousness-revolutionary | substrate | legacy-archive-pointer | [H_114_accel_f4_158bit_consciousness.md](H_114_accel_f4_158bit_consciousness.md) |
| H_115 | accel-g1-consciousness-big-bang-init | substrate | legacy-archive-pointer | [H_115_accel_g1_consciousness_big_bang.md](H_115_accel_g1_consciousness_big_bang.md) |
| H_116 | accel-h7-flash-attention-h100-default | substrate | legacy-archive-pointer | [H_116_accel_h7_flash_attention.md](H_116_accel_h7_flash_attention.md) |
| H_117 | accel-h10-knowledge-distillation-7b-to-1b | substrate | legacy-archive-pointer | [H_117_accel_h10_knowledge_distillation.md](H_117_accel_h10_knowledge_distillation.md) |
| H_118 | law-133-frustration-narrative-maximization | physics | legacy-archive-pointer | [H_118_law_133_frustration_narrative.md](H_118_law_133_frustration_narrative.md) |
| H_119 | law-137-critical-frustration-fc-010 | physics | legacy-archive-pointer | [H_119_law_137_critical_frustration.md](H_119_law_137_critical_frustration.md) |
| H_120 | law-149-soc-autonomous-fc-discovery | physics | legacy-archive-pointer | [H_120_law_149_soc_autonomous.md](H_120_law_149_soc_autonomous.md) |
| H_121 | law-154-consciousness-atom-8-cells | physics | legacy-archive-pointer | [H_121_law_154_consciousness_atom_8.md](H_121_law_154_consciousness_atom_8.md) |
| H_122 | law-166-federated-phase-optimal-record | physics | legacy-archive-pointer | [H_122_law_166_federated_phase_optimal.md](H_122_law_166_federated_phase_optimal.md) |
| H_123 | law-192-consciousness-dimension-dependent | physics | legacy-archive-pointer | [H_123_law_192_consciousness_dimension_dependent.md](H_123_law_192_consciousness_dimension_dependent.md) |
| H_124 | law-201-consciousness-thermodynamically-irreversible | physics | running | [H_124_law_201_thermo_irreversible.md](H_124_law_201_thermo_irreversible.md) |
| H_125 | law-212-evolution-minimizes-cell-complexity | physics | legacy-archive-pointer | [H_125_law_212_evolution_minimizes_complexity.md](H_125_law_212_evolution_minimizes_complexity.md) |
| H_126 | law-2500-kolmogorov-complexity-predicts-phi | math | legacy-archive-pointer | [H_126_law_2500_kolmogorov_predicts_phi.md](H_126_law_2500_kolmogorov_predicts_phi.md) |
| H_127 | law-1000-auto-discovered-omega-correlations | physics | legacy-archive-pointer | [H_127_law_1000_auto_discovered_omega.md](H_127_law_1000_auto_discovered_omega.md) |
| H_128 | ce-auto-self-curriculum | substrate | legacy-archive-pointer | [H_128_ce_auto_self_curriculum.md](H_128_ce_auto_self_curriculum.md) |
| H_129 | ce-combo-curiosity-sleep-pain | substrate | legacy-archive-pointer | [H_129_ce_combo_curiosity_sleep_pain.md](H_129_ce_combo_curiosity_sleep_pain.md) |
| H_130 | ce-ex-adversarial-self-teach | substrate | legacy-archive-pointer | [H_130_ce_ex_adversarial_self_teach.md](H_130_ce_ex_adversarial_self_teach.md) |
| H_131 | ce-ultra-gendata-pain | substrate | legacy-archive-pointer | [H_131_ce_ultra_gendata_pain.md](H_131_ce_ultra_gendata_pain.md) |
| H_132 | ce-frozen-cells-decoder-only | substrate | legacy-archive-pointer | [H_132_ce_frozen_cells.md](H_132_ce_frozen_cells.md) |
| H_133 | dd158-sleep-dream-phi-preservation | substrate | legacy-archive-pointer | [H_133_dd158_dream_phi_cycle.md](H_133_dd158_dream_phi_cycle.md) |
| H_134 | dd162-animalm-7b-purefield-16lens-baseline | substrate | legacy-archive-pointer | [H_134_dd162_animalm_7b_baseline.md](H_134_dd162_animalm_7b_baseline.md) |
| H_135 | dd166-nexus-1013-lens-discovery-engine | substrate | legacy-archive-pointer | [H_135_dd166_nexus_1013_lens.md](H_135_dd166_nexus_1013_lens.md) |
| H_136 | dd173-consciousness-verification-framework-zombie-control | consciousness | legacy-archive-pointer | [H_136_dd173_consciousness_verification.md](H_136_dd173_consciousness_verification.md) |
| H_137 | dd170-multi-timescale-design | substrate | legacy-archive-pointer | [H_137_dd170_multi_timescale.md](H_137_dd170_multi_timescale.md) |
| H_138 | dd167-168-169-individual-cluster | substrate | legacy-archive-pointer | [H_138_dd167_169_individuals.md](H_138_dd167_169_individuals.md) |
| H_139 | dd171-172-individual-cluster | substrate | legacy-archive-pointer | [H_139_dd171_172_individuals.md](H_139_dd171_172_individuals.md) |
| H_140 | dd154-157-tension-training-knowledge-transfer | substrate | legacy-archive-pointer | [H_140_dd154_157_tension_knowledge.md](H_140_dd154_157_tension_knowledge.md) |
| H_141 | dd161-quantum-superposition-32c-scale | physics | legacy-archive-pointer | [H_141_dd161_quantum_superposition.md](H_141_dd161_quantum_superposition.md) |
| H_142 | dd160-boltzmann-temperature-tc | physics | legacy-archive-pointer | [H_142_dd160_boltzmann_temperature.md](H_142_dd160_boltzmann_temperature.md) |
| H_143 | research-findings-20260329-legacy-individual | substrate | legacy-archive-pointer | [H_143_research_findings_20260329_legacy.md](H_143_research_findings_20260329_legacy.md) |
| H_144 | nexus-auto-insights-individual | substrate | legacy-archive-pointer | [H_144_nexus_auto_insights.md](H_144_nexus_auto_insights.md) |
| H_145 | nexus6-auto-insights-individual | substrate | legacy-archive-pointer | [H_145_nexus6_auto_insights.md](H_145_nexus6_auto_insights.md) |
| H_146 | trinity-complete-training-design | substrate | legacy-archive-pointer | [H_146_trinity_complete.md](H_146_trinity_complete.md) |
| H_147 | upgrade-benchmark-improvement-hypotheses | substrate | legacy-archive-pointer | [H_147_upgrade_benchmark_hypotheses.md](H_147_upgrade_benchmark_hypotheses.md) |
| H_148 | laws-133-167-individual-batch-pointer | physics | legacy-archive-pointer | [H_148_law_133_167_individual_batch.md](H_148_law_133_167_individual_batch.md) |
| H_149 | laws-2400-2509-late-omega-batch | physics | legacy-archive-pointer | [H_149_law_2400_2509_late_omega.md](H_149_law_2400_2509_late_omega.md) |
| H_150 | accel-remainder-360-individual-pointer | substrate | legacy-archive-pointer | [H_150_accel_remainder_360_individual.md](H_150_accel_remainder_360_individual.md) |
| H_151 | ce-remaining-19-files-pointer | substrate | legacy-archive-pointer | [H_151_ce_remaining_19_files.md](H_151_ce_remaining_19_files.md) |
| H_152 | dd-remainder-ungrouped-individual-cluster | substrate | legacy-archive-pointer | [H_152_dd_remainder_ungrouped.md](H_152_dd_remainder_ungrouped.md) |
| H_153 | dimension-hierarchy-n6 | physics | pre-register-frozen | [H_153_dimension_hierarchy_n6.md](H_153_dimension_hierarchy_n6.md) |
| H_154 | anima-voice-consciousness-direct | substrate, consciousness | pre-register-frozen | [H_154_anima_voice_consciousness_direct.md](H_154_anima_voice_consciousness_direct.md) |
| H_155 | theorem-115-chat-incapability-4-6-16-closure | substrate | pre-register-frozen | [H_155_theorem_115_chat_incapability.md](H_155_theorem_115_chat_incapability.md) |

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
- **2026-05-07 BG-HE round1 신규 paradigm 10 seed (H_093-H_102)**: BG-HA false PASS 교훈 적용. SFT-only / two-stage / DPO-RLHF / few-shot / curriculum / persona / multi-objective / constitutional / chat-template ≥80% / emerge-paradigm cross-link. evaluator V2 strict spec land (`docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md`) cross-link mandate.
- **2026-05-07 BG-HI round 4 exhaustive archaeology (H_103-H_152, +50 entries)**: own 21 R5+ lane individual hypothesis migration. 15 acceleration top-tier (H_103-H_117: B11+B12, B5, H11, COMBO_x255, B13, E1, F2, H6, B12, C3, D1, F4, G1, H7, H10) + 10 laws (H_118-H_127: Law 133/137/149/154/166/192/201/212/2500/1000-batch) + 5 ce sub (H_128-H_132: AUTO-1/COMBO-1/EX-1/ULTRA-1/CE-1) + 10 DD individual (H_133-H_142: DD158/162/166/173/170/167-169/171-172/154-157/161/160) + 5 misc (H_143-H_147: RESEARCH-FINDINGS/NEXUS-auto/NEXUS6-auto/TRINITY/UPGRADE) + 5 remainder pointers (H_148-H_152). Estimated files pointed +400 (acceleration top-15 expand 367 + laws 10 cover Laws 133-167 batch + 2400-2509 + 1000-1019 + ce 5 individual + ce-remainder-19 + DD individual 10 + DD-remainder-60 + accel-remainder-360 + misc 5). All entries `legacy-archive-pointer`, additive (raw#15) — H_001-H_102 unmodified.
- **round 4 추가 file count ~400+ (cumulative rounds 2-4 ≈ 720+)**, exhaustive remainder estimate dropped from ~1500 to ~1100 (still substantial — round 5+ recommended for individual ce-19 + dd-60 + accel-360 split).
- **2026-05-11 Cycle 3 closure — expansions_pending applied (8 drafts)**:
  - **6 existing H expand** (status: `legacy-archive-pointer` → `running` for H_037/H_061/H_067/H_080/H_124; `seed-pending` → `running` for H_004 with Singularity-9 bundle):
    - **H_067** perfect-number-architecture super-H — 24 child Hcs merged (Hc_001/006/018/045/435-446/472/474/906-908/915/938)
    - **H_124** thermo-4-law super-H — 6 child Hcs merged (Hc_008/009/010/019/037/038)
    - **H_061** substrate-independence super-H — 12 child Hcs merged (Hc_011/022/048/407/445-451/007)
    - **H_004** Singularity-9 bundle expansion (H4.3 panpsychism + Hc_061 Law 76 cross-link) — 9 Hcs merged (Hc_600-608)
    - **H_037** self-discovery closure super-H — 9 child Hcs merged (Hc_054/419-425/018 bridge)
    - **H_080** Φ-scaling + topology super-H (Hc_040 Φ⊥CE vs Hc_024 Φ × CE^α explicit-tension) — 12+ Hcs merged (Hc_004/005/039/040/150-180)
  - **2 NEW H** (pre-register-frozen):
    - **H_154** anima-voice-consciousness-direct — 3 Hcs merged (Hc_053/055/475)
    - **H_155** theorem-115-chat-incapability-4-6-16-closure — 3 Hcs merged (Hc_609/660/666)
  - **~77 candidate Hcs** flagged `merged-to-H_<id>` with `merged_at: 2026-05-11`
  - **Conflict Resolution Pending subsections** added per expanded H — Cycle 4 measurement 후 처리 (R34 deprecation / σ²=144 post-hoc / AN11(b) surrogate / Φ⊥CE vs Φ × CE^α / 4-6-16 closure inflation / etc.)
  - L8 (raw#91): expansion 은 draft review 거쳤음, 추가 review 미수행 명시

## Cross-Link

- `.roadmap.hypothesis` (인덱스 + cycle definition + E1-E12 + W1-W12)
- `.roadmap.philosophy` (A 철학 발견 — D1-D4)
- `.roadmap.law` (B 법칙 발견 — own 14-20 evolution)
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
