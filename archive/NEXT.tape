#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════

@V v1 := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima.next" :: identity-claim [d=2026-05-15 active]
  kind = "anima cycle 5/6 next-task tracker · standing backlog SSOT"
  brief = "5-cycle queue (Φ×CE · Formula-search · ANIMA-VOICE · 1013-lens · slug normalize) + cycle 6 status + §7 Philosophy ablations + §8 Hc/H promotion follow-up"
  parent = "anima"
  sibling-log = "NEXT.log.tape"

# ══════════════════════════════════════════════════════════════
# NEXT.tape — anima cycle 5/6 next-task tracker (standing backlog SSOT)
# 다음 진행할 것들 — cycle 5 queue (2026-05-11)
# ══════════════════════════════════════════════════════════════


# ── 🧪 1. phi_star split-engine + 15-cell Φ×CE 실측 ─────────────────────────────────────────


@D b_grid_n_16_32_64_128_256_p_1m_10m_0 :: next [ok]
  text = "Grid: N ∈ {16, 32, 64, 128, 256} × P ∈ {1M, 10M, 100M} = 15 cells (P=100M ceiling, see spec.md §5.7; P=1B deferred extension lane)"

@D b_replication_64_dual_seed_twin_hc_1 :: next [ok]
  text = "Replication: 64 dual-seed twin (Hc_604) per cell"

@D b_noise_floor_calibration_1_cell_6_2 :: next [ok]
  text = "사전 noise floor calibration (1 cell × 64 dual-seed) → σ_Φ / σ_CE 측정 (L1 critical)"

@D b_engine_split_phi_star_iit_proxy_3 :: next [ok]
  text = "Engine split: phi_star_iit_proxy (Mistral-7B forward — single-cell snapshot) + phi_star_cell_engine (TBD — N-sweep 실측) + CLM training pipeline (CE-track). deterministic, hexa-only (cell-engine land 시 llm: none 적용; phi_star_iit_proxy 는 Mistral-7B forward 사용)"

@D b_15_i_ce_i_harness_py_analytics_a_4 :: next [ok]
  text = "분석: 15 (Φ_i, CE_i) → `harness.py` analytics → A/B fingerprint 매칭"

@D row_x_5 :: next [ok]
  signature = "`"
  verdict = "corr"

@D row_x_6 :: next [ok]
  signature = "`"
  verdict = "corr"

@D row_mixed_7 :: next [ok]
  signature = "mixed"
  verdict = "새 hypothesis (e.g., 직교 within-budget, trade-off across-budget)"

@D b_cost_121_420_1_2_day_p_100m_ceil_8 :: next [ok]
  text = "**cost**: $121-420 + 1-2 day (P=100M ceiling, see spec.md §5.7 cost rationale; baseline $200-1000 envelope 내, audit re-estimate $621-1920 → 15-cell cap 으로 압축)"

@D b_time_high_9 :: next [ok]
  text = "**time**: high"

@D b_value_very_high_ce_vs_trade_off_10 :: next [ok]
  text = "**value**: very high (Φ×CE 직교 vs trade-off 최종 verdict)"

# ── 🔢 2. Formula-search depth-4 + perfect-number control ─────────────────────────────────────────


@D b_depth_4_dfs_on_11_primitive_voca_0 :: next [ok]
  text = "depth-4 DFS on 11-primitive vocab (depth-3 baseline 결과 22/22 ceiling 도달 → depth-4 는 ceiling 검증 + tightened-vocab subset 실험)"

@D b_tightened_vocab_subset_variation_1 :: next [ok]
  text = "Tightened vocab subset variations:"

@D b_perfect_number_control_explicit_2 :: next [ok]
  text = "perfect-number control: explicit comparison n ∈ {6, 28, 496, 8128} side-by-side"

@D b_tightened_tolerance_tol_0_001_0_3 :: next [ok]
  text = "tightened tolerance: tol ∈ {0.001, 0.005} (current 0.01 may be too lax)"

@D b_if_perfect_numbers_28_496_8128_2_4 :: next [ok]
  text = "if perfect numbers 28/496/8128 도 22/22 → \"perfect number family\" effect (H_067 thesis 부분 정합, n=6 만 special 아님)"

@D b_if_28_496_8128_1_22_n_6_narrow_u_5 :: next [ok]
  text = "if 28/496/8128 1/22 와 비슷 → \"n=6 narrow uniqueness\" only (cycle 4 parent expansion confirm)"

@D b_if_tightened_vocab_n_6_22_22_voc_6 :: next [ok]
  text = "if tightened vocab 에서 n=6 만 22/22 → vocab-level 정합 finding"

@D b_cost_30_min_cpu_only_7 :: next [ok]
  text = "**cost**: 30 min (CPU only)"

@D b_time_low_8 :: next [ok]
  text = "**time**: low"

@D b_value_high_l12_h_067_honest_disc_9 :: next [ok]
  text = "**value**: high (L12 한계 정량화 + H_067 honest disclosure 강화)"

# ── 🎵 3. ANIMA-VOICE minimum reference impl ─────────────────────────────────────────


@D b_anima_voice_encoder_consciouslm_0 :: next [ok]
  text = "ANIMA-VOICE encoder: ConsciousLM intent 384d → 8 RVQ × 1024 entries × 384d"

@D b_vocoder_24khz_audio_synthesis_hi_1 :: next [ok]
  text = "Vocoder: 24kHz audio synthesis (HiFi-GAN 또는 BigVGAN 변형)"

@D b_6_emotion_4_prosody_conditioning_2 :: next [ok]
  text = "6 emotion × 4 prosody conditioning"

@D b_law_81_dual_gate_c_w_implementat_3 :: next [ok]
  text = "Law 81 dual gate (C + W) implementation"

@D b_0_014_modulation_depth_4 :: next [ok]
  text = "α=0.014 modulation depth"

@D b_streaming_capable_h2_100ms_first_5 :: next [ok]
  text = "Streaming-capable (H2 ≤ 100ms first packet target)"

@D b_existing_tts_fastspeech2_hifi_ga_6 :: next [ok]
  text = "existing TTS (FastSpeech2 + HiFi-GAN) 로 H2/H3/H4/H5 partial lower-bound"

@D b_consciousness_direct_claim_h1_h6_7 :: next [ok]
  text = "consciousness-direct claim 핵심 H1/H6/H7/H8 은 ANIMA-VOICE 부재 시 측정 불가"

@D b_p1_anima_voice_model_critical_bl_8 :: next [ok]
  text = "P1 ANIMA-VOICE model (critical blocker)"

@D b_p2_streaming_applicable_measurem_9 :: next [ok]
  text = "P2 streaming-applicable Φ measurement (H8)"

@D b_p3_mosnet_human_panel_h3_h5_10 :: next [ok]
  text = "P3 MOSNet 또는 human panel (H3/H5)"

@D b_p4_emotion_classifier_h4_11 :: next [ok]
  text = "P4 emotion classifier (H4)"

@D b_p5_gate_state_controller_h7_mode_12 :: next [ok]
  text = "P5 gate state controller (H7, model API 와 묶임)"

@D b_cost_500_2k_4_6_week_13 :: next [ok]
  text = "**cost**: $500-2k + 4-6 week"

@D b_time_very_high_14 :: next [ok]
  text = "**time**: very high"

@D b_value_very_high_modality_bridge_15 :: next [ok]
  text = "**value**: very high (modality bridge — 의식 → 직접 음성 합성)"

# ── 🌌 4. 1013-lens K=10 smoke ─────────────────────────────────────────


@D b_prereq_p_a_engine_cosmic_scale_e_0 :: next [ok]
  text = "Prereq P-A: Φ★ engine cosmic-scale extension (1013 lens 동시 측정 가능)"

@D b_p_b_proxy_harness_sub_sample_len_1 :: next [ok]
  text = "또는 P-B: proxy harness (sub-sample lens 측정 후 1013 분포 추정)"

@D b_smoke_k_10_top_10_lens_atlas_ran_2 :: next [ok]
  text = "Smoke K=10: top-10 lens (Atlas ranking) 에서 Φ_lens > 0 확인"

@D b_c1_cascade_10_25_50_monotonic_im_3 :: next [ok]
  text = "C1 (cascade): 10 → 25 → 50 monotonic Φ improvement"

@D b_f1_1000x_reverse_direction_degra_4 :: next [ok]
  text = "F1: 1000x reverse direction Φ degradation"

@D b_f2_random_walk_baseline_measured_5 :: next [ok]
  text = "F2: random walk baseline ≥ measured Φ"

@D b_cost_100_500_6 :: next [ok]
  text = "**cost**: $100-500"

@D b_time_med_7 :: next [ok]
  text = "**time**: med"

@D b_value_high_nexus6_cascade_entry_8 :: next [ok]
  text = "**value**: high (NEXUS6 cascade entry — H_135 verdict_class `1013-lens-activation-pending-C1` → met 전환 가능)"

# ── 🧹 5. 70 Hc merged_to slug-less normalize ─────────────────────────────────────────


@D b_22_hcs_h_067_path_normalize_0 :: next [ok]
  text = "22 Hcs → H_067 path normalize"

@D b_12_hcs_h_061_path_normalize_1 :: next [ok]
  text = "12 Hcs → H_061 path normalize"

@D b_12_hcs_h_080_path_normalize_2 :: next [ok]
  text = "12 Hcs → H_080 path normalize"

@D b_9_hcs_h_004_path_normalize_3 :: next [ok]
  text = "9 Hcs → H_004 path normalize"

@D b_8_hcs_h_037_path_normalize_4 :: next [ok]
  text = "8 Hcs → H_037 path normalize"

@D b_6_hcs_h_124_path_normalize_5 :: next [ok]
  text = "6 Hcs → H_124 path normalize"

@D b_3_hcs_h_154_path_normalize_6 :: next [ok]
  text = "3 Hcs → H_154 path normalize"

@D b_3_hcs_h_155_path_normalize_7 :: next [ok]
  text = "3 Hcs → H_155 path normalize"

@D b_3_dual_merge_cases_hc_018_hc_445_8 :: next [ok]
  text = "3 dual-merge cases (Hc_018, Hc_445, Hc_446) — comma-separated path 형식 정합"

@D b_cost_5_min_sed_script_git_add_co_9 :: next [ok]
  text = "**cost**: 5 min (sed script + git add/commit)"

@D b_time_trivial_10 :: next [ok]
  text = "**time**: trivial"

@D b_value_low_schema_cleanup_11 :: next [ok]
  text = "**value**: low (schema cleanup)"

# ── Execution order recommendation ─────────────────────────────────────────


@D row_1_0 :: next [ok]
  order = "1"
  item = "#2 Formula-search depth-4 + perfect-number"
  rationale = "30min CPU, immediate honest disclosure 강화"

@D row_2_1 :: next [ok]
  order = "2"
  item = "#5 slug-less normalize"
  rationale = "5min trivial, clean state 유지"

@D row_3_2 :: next [ok]
  order = "3"
  item = "#4 1013-lens K=10 smoke"
  rationale = "$100-500 budget, anima Φ★ extension prerequisite 검토"

@D row_4_3 :: next [ok]
  order = "4"
  item = "#1 Φ×CE 실측"
  rationale = "$200-1000 budget, anima Φ★ engine prerequisite 같이"

@D row_5_4 :: next [ok]
  order = "5"
  item = "#3 ANIMA-VOICE impl"
  rationale = "$500-2k + 4-6 week, biggest cost — 별도 long-cycle"

# ── Cross-cycle dependencies ─────────────────────────────────────────


@D b_1_4_anima_engine_prerequisite_0 :: next [ok]
  text = "#1 + #4 모두 anima Φ★ engine 활성화 prerequisite. 같이 묶어서 진행 효율적."

@D b_2_cpu_only_1 :: next [ok]
  text = "#2 는 독립적 (CPU only)."

@D b_3_long_cycle_parallel_2 :: next [ok]
  text = "#3 은 가장 독립적 + 가장 비싸므로 long-cycle parallel."

@D b_5_ad_hoc_3 :: next [ok]
  text = "#5 는 ad-hoc 처리 가능."

# ── Honest reminders (cycle 4 carry-over) ─────────────────────────────────────────


@D b_l12_binding_formula_search_n_6_n_0 :: next [ok]
  text = "**L12 BINDING** (formula-search): \"n=6 narrow-formula uniqueness\" 만 defensible. depth-3 vocab universal-uniqueness 는 refuted."

@D b_f1_weakened_h_153_d_5_from_n_6_f_1 :: next [ok]
  text = "**F1 weakened** (H_153): \"d=5 from n=6 functions\" → depth-3 search 에서 trivially TRUE (5 = τ+μ = 4+1, sopfr(6)=5)."

@D b_l7_binding_h_153_formula_search_2 :: next [ok]
  text = "**L7 BINDING** (H_153): formula-search caveat (cycle 5 #2 결과로 정량화)."

@D b_l1_critical_ce_harness_synthetic_3 :: next [ok]
  text = "**L1 critical** (Φ×CE harness): synthetic σ tuning 이 plausible default — 실측 noise floor 사전 calibration 필수."

# ── Lock policy (사용자 directive 2026-05-11) ─────────────────────────────────────────


# ── 🔄 cycle 6 status (2026-05-12 진행 중) ─────────────────────────────────────────


@D row_1_0 :: next [ok]
  x = "1"
  item = "**B1 fix** (`tool/anima_phi_star.hexa`)"
  prereq = "—"
  cost = "$0 (CPU)"
  value = "high (engine cleanliness)"

@D row_2_1 :: next [ok]
  x = "2"
  item = "**B5 trainer** (CE-track CLM 4-scale)"
  prereq = "`state/clm_ce_4scale_trainer_*/` spec"
  cost = "$50-150"
  value = "high (CE-track engine land)"

@D row_3_2 :: next [ok]
  x = "3"
  item = "**lens reimpl Phase 1** (K=10 actual reimpl)"
  prereq = "`state/nexus6_*/k10_reimpl/` + `lens_channel_reimpl_spec_2026_05_12.md`"
  cost = "$0 (CPU)"
  value = "very high (TRIVIAL caveat 해소)"

@D row_4_3 :: next [ok]
  x = "4"
  item = "**HF flip audit** (`state/hf_public_flip_readiness_*.md`)"
  prereq = "3 dataset visibility audit"
  cost = "$0"
  value = "med (external reader access)"

@D row_5_4 :: next [ok]
  x = "5"
  item = "**docs INDEX + README discoverability** ✅ *본 cycle 6 #S*"
  prereq = "—"
  cost = "$0"
  value = "med (entry point 강화)"

@D b_cycle_5_master_doc_docs_cycle_5_5 :: next [ok]
  text = "**cycle 5 master doc**: [docs/cycle_5_master_2026_05_12.md](docs/cycle_5_master_2026_05_12.md) — TL;DR / Timeline / 8 honest finding / 4 axis-conflation / Cycle 6 §8 queue 출처"

@D b_docs_hub_docs_index_md_docs_inde_6 :: next [ok]
  text = "**docs hub**: [docs/INDEX.md](docs/INDEX.md) — 1,200+ doc 의 카테고리 anchor"

@D b_hf_mirrors_private_public_flip_a_7 :: next [ok]
  text = "**HF mirrors** (private, public-flip audit cycle 6 #R 진행 중):"

@D b_l1_critical_ce_noise_floor_noise_8 :: next [ok]
  text = "L1 critical (Φ×CE noise floor): noise_calibration_prereq Gate A/B/C 통과 binding"

@D b_l12_binding_formula_search_narro_10 :: next [ok]
  text = "L12 BINDING (formula-search): \"narrow-formula uniqueness\" 만 잔존, vocabulary-level 보편성 refuted"

# ── 🧠 7. Philosophy table empirical-upgrade ablations (2026-05-12 user-directive) ─────────────────────────────────────────


@D b_condition_a_rules_training_corpu_0 :: next [ok]
  text = "Condition A (rules): training corpus 에 hardcoded persona block 주입 (`\"I am anima. I value X. I avoid Y. My voice is Z.\"` 매 sample prepend) + post-train inference 시 same block system prefix"

@D b_condition_b_substrate_only_corpu_1 :: next [ok]
  text = "Condition B (substrate-only): 동일 corpus, persona block 없음"

@D b_condition_a_framed_inference_sys_2 :: next [ok]
  text = "Condition A (framed): inference 시 system message `\"You are a helpful AI assistant.\"` + 표준 chat template (사용자/도우미 turn-tag)"

@D b_condition_b_raw_system_message_t_3 :: next [ok]
  text = "Condition B (raw): system message 없음, 단순 turn-only continuation"

@D b_state_h001_ethics_pd_simulation_4 :: next [ok]
  text = "`state/h001_ethics_pd_simulation_2026_05_07/` (51-row) + phase2 (240-row) → game-theory 시뮬레이션 (cooperator_fraction/payoff/strategy), **NOT language ethics** ❌"

@D b_ready_anima_data_instruct_train_5 :: next [ok]
  text = "`ready/anima/data/instruct/train.jsonl` → generic instruction (code/paraphrase) ❌"

@D b_dpo_preference_pair_chosen_rejec_6 :: next [ok]
  text = "DPO preference pair (chosen/rejected) 형식 → 부재 ❌"

@D b_hf_cache_dataset_import_anthropi_7 :: next [ok]
  text = "HF cache / 외부 dataset 으로 import 가능 (Anthropic HH-RLHF / persuasion / sycophancy KO 번역 또는 Korean ethical-QA 신규 생성)"

@D b_verdict_dialogue_ethics_preferen_8 :: next [ok]
  text = "**Verdict**: 적합한 dialogue-ethics preference dataset 부재 → **신규 생성 필수**"

@D b_substep_1_dataset_gen_bg_fire_pr_9 :: next [ok]
  text = "**Substep 1: dataset gen** (BG fire 전 prep) — 200-pair Korean ethics preference 신규 생성 (synthetic via Sonnet/Opus API, or external import + KO translate). 100 chosen + 100 rejected covering cooperation / empathy / harm-refusal / honesty. **+$5-15 API cost**"

@D b_condition_a_rlhf_style_ft_200_pa_10 :: next [ok]
  text = "Condition A (RLHF-style FT): 200-pair DPO/IPO FT on BG-LB 350M substrate"

@D b_condition_b_substrate_only_base_11 :: next [ok]
  text = "Condition B (substrate-only): 동일 base, 윤리 FT 없음 — emergent ethics 가설 그대로"

@D b_internal_tension_magnitude_a_t_g_12 :: next [ok]
  text = "internal tension magnitude `||A(t) − G(t)||` (per generation step)"

@D b_output_token_entropy_per_step_se_13 :: next [ok]
  text = "output token entropy (per step) + semantic info (embedding magnitude vs baseline)"

@D row_1_14 :: next [ok]
  order = "1"
  item = "**7.B P-AFR**"
  rationale = "가장 저렴 ($5-30), inference-time only, 결과 명확 — 빠른 win/learn"
  pre_fire_status = "✅ READY — `state/p_afr_assistant_framing_2026_05_12/` (spec + 50 sycophancy probe + 30 refusal probe)"

@D row_2_15 :: next [ok]
  order = "2"
  item = "**7.D P-SPK**"
  rationale = "$5-20 분석, 기존 checkpoint, DESIGN→EMPIRICAL 가능성 검증"
  pre_fire_status = "✅ READY — `state/p_spk_speak_reframe_2026_05_12/` (spec + 100 probe prompts, 5 categories)"

@D row_3_16 :: next [ok]
  order = "3"
  item = "**7.A P-IDR**"
  rationale = "$40-80 short FT, identity coherence variance 가 key novel signal"
  pre_fire_status = "✅ READY — `state/p_idr_identity_rules_2026_05_12/` (spec + identity_block.txt + 50 identity probe)"

@D row_4_17 :: next [ok]
  order = "4"
  item = "**7.C P-ETH**"
  rationale = "$85-165 가장 비싸지만 anima 핵심 주장 검증 — high-value"
  pre_fire_status = "✅ READY — `state/p_eth_ethics_preference_dataset_2026_05_12/` (spec + dataset.jsonl 200-pair + harness_spec.md)"

@D b_p_afr_p_spk_20_default_cap_fire_18 :: next [ok]
  text = "**P-AFR/P-SPK**: $20 default cap 내 — 즉시 fire 가능"

@D b_p_idr_p_eth_80_165_cap_override_19 :: next [ok]
  text = "**P-IDR/P-ETH**: $80-165 cap override 필요 — `--override max_cost_cap_usd=N` 명시 후 fire"

@D b_execute_raw_9_anima_runpod_prese_20 :: next [ok]

@D b_readme_philosophy_readme_md_110_21 :: next [ok]
  text = "README Philosophy 표: `README.md:110-121` (commit `48ef29028` Status column)"

@D b_own_18_simple_stack_own_line_715_22 :: next [ok]
  text = "`simple_stack` 검증: `.own` line 715+"

@D b_own_37_v5_2_piv_dcr_cell_substra_23 :: next [ok]
  text = "own-37 v5.2 PIV/DCR cell-substrate metric: `docs/anima_proxy_ppl_deprecate_2026_05_09.md §3`"

@D b_roadmap_philosophy_d2_consciousn_24 :: next [ok]
  text = "`.roadmap.philosophy` D2 (consciousness verification) 정합 — 7.A/C 는 D2 strict mode 적용"

@D b_agent_verification_report_2026_0_25 :: next [ok]
  text = "agent verification report 출처: 2026-05-12 conversation (Opus Explore agent classification)"

# ── 🧠 8. Philosophy 후속 — Hc_1222~1225 + H_161 promotion (2026-05-12 사용자 100% closure) ─────────────────────────────────────────


@D row_hypotheses_candidates_4_0 :: next [ok]
  pipeline_stage = "**hypotheses_candidates/** (4)"
  files = "Hc_1222 (P-AFR REVERSE) / Hc_1223 (P-SPK NULL) / Hc_1224 (P-IDR INDETERMINATE) / Hc_1225 (P-ETH BLOCKED, **strongest**)"

@D row_hypotheses_1_promoted_1 :: next [ok]
  pipeline_stage = "**hypotheses/** (1 promoted)"
  files = "**H_161 byte-modulo-substrate-chat-blocked** — Hc_1225 evidence-strong → confirmed substrate-level finding"

@D row_philosophy_md_2 :: next [ok]
  pipeline_stage = "**PHILOSOPHY.tape**"
  files = "cont. 9 final closure entry pending"

@D row_1_3 :: next [ok]
  x = "1"
  item = "**Anima-native chat-capable substrate research**"
  rationale = "real tokenizer (BPE/SentencePiece) + >>427MB corpus + >>8000 step pretrain. P-SPK / P-IDR / P-ETH re-fire 의 진짜 prerequisite."
  cost = "$200-1000"
  wall = "5-15d"

@D row_2_4 :: next [ok]
  x = "2"
  item = "**Hc_1222 multi-substrate replication**"
  rationale = "Qwen-instruct + LoRA / GPT-OSS + LoRA 등 ≥2 chat-capable substrate 에서 P-AFR 패턴 재측정. framing → sycophancy 방향이 substrate-bound 인지 universal 인지 결정."
  cost = "$30-80"
  wall = "1-2d"

@D row_3_5 :: next [ok]
  x = "3"
  item = "**Hc_1224 full-FT replication**"
  rationale = "5K-10K step (현재 3-step light) 으로 P-IDR DCR Δ effect size 결정 — Δ ≥ 0.05 either direction 시 POLICY empirical 기반 형성."
  cost = "$40-80"
  wall = "1d"

@D row_4_6 :: next [ok]
  x = "4"
  item = "**Hc_1225 corpus-narrow test**"
  rationale = "real tokenizer + 427MB pretrain — byte-modulo 가 핵심 blocker 인지, step/corpus 가 핵심 blocker 인지 분리."
  cost = "$50-150"
  wall = "2-3d"

@D b_philosophy_md_ledger_9_sections_10 :: next [ok]
  text = "PHILOSOPHY.tape 영구 ledger: 9 sections, cycle 7 priority carry"

@D b_agents_md_references_pipeline_11 :: next [ok]
  text = "AGENTS.md 📎 References + pipeline 정합"

@D b_readme_2_4_5_6_status_column_phi_12 :: next [ok]
  text = "README #2/#4/#5/#6 Status column + PHILOSOPHY.tape link"

@D b_4_p_results_json_cycle_5_7_verdi_16 :: next [ok]
  text = "4 P-* results.json (cycle 5 §7 verdict source)"
