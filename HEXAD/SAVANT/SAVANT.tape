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

@I id001 := "anima.savant" :: identity-claim [d=2026-05-15 active]
  kind = "anima Golden Zone & Savant 전수조사 compendium · architecture SSOT"
  brief = "Golden Zone (GZ) interval [1/2 − ln(4/3), 1/2] · GZ_CENTER=1/e · Savant = GZ_LOWER specialization mechanism · clm_01..13 + archive-TECS-L + canon registry"
  parent = "anima"
  sibling-log = "SAVANT.log.tape"

# ══════════════════════════════════════════════════════════════
# SAVANT.tape — Golden Zone & Savant 전수조사 compendium (architecture SSOT)
# ══════════════════════════════════════════════════════════════

# 본 문서는 `~/core/anima_clm_01~13` (13 worktree) + `~/core/archive-TECS-L` (foundational
# registry) + `~/core/canon` (curated technique repo + git history) 를 전수조사 하여
# **Golden Zone (골든존)** 과 **Savant (서번트/사반트)** 두 핵심 개념의 수학적 기반 ·
# 실증 흐름 · 교차 도메인 검증 · 진화 timeline 을 한 자리에 모은다.
# >
# Scope: **golden zone = 의식 emergence 의 dropout/inhibition 작동 구간**,
# **savant = 그 구간의 lower bound 에서 일어나는 specialization 메커니즘**.
# AGENTS.md / LATTICE_POLICY.md 의 real-limits-first 정책 하에서 GZ 는
# *design vocabulary* 로 분류되며, 본 문서는 그 vocabulary 의 정의 · 사용 ·
# 실증 evidence · 한계를 정직하게 기록한다.
# ---

# ── 0. 1줄 요약 (TL;DR) ─────────────────────────────────────────


@D b_golden_zone_gz_interval_1_2_ln_4_0 :: savant [ok]
  text = "**Golden Zone (GZ)** = 실수축 위 interval `[1/2 − ln(4/3), 1/2] ≈ [0.2123, 0.5]`,"

@D b_gz_upper_1_2_riemann_critical_li_1 :: savant [ok]
  text = "**GZ_UPPER = 1/2** = Riemann critical line / 완전수 6 의 최대 proper-divisor 역수."

@D b_gz_center_1_e_i_i_i_ln_i_element_2 :: savant [ok]
  text = "**GZ_CENTER = 1/e** = `I^I` 와 `I·ln(I)` 의 유일 전역 최소점 (elementary calculus)."

@D b_gz_width_ln_4_3_6_4_divisor_coun_3 :: savant [ok]
  text = "**GZ_WIDTH = ln(4/3)** = τ(6) = 4 (divisor count) 의 4번째 state 진입 entropy 비용 `ln(4/3)`,"

@D b_savant_dropout_gz_center_1_e_gz_4 :: savant [ok]
  text = "**Savant** = dropout 을 GZ_CENTER (1/e) 에서 GZ_LOWER (0.2123) 로 내려"

# ── 1. Canonical 상수 표 ─────────────────────────────────────────


@D row_gz_upper_0 :: savant [ok]
  symbol = "`GZ_UPPER`"
  x = "Riemann critical line / 1/p_min(6)"
  x = "`1/2`"
  x = "`0.5` (exact)"
  canonical = "`archive-TECS-L/verify/verify_gz_ising_critical.py:20`"

@D row_gz_center_1 :: savant [ok]
  symbol = "`GZ_CENTER`"
  x = "`argmin_{I∈(0,1)} I^I` = `argmin I·ln(I)`"
  x = "`1/e`"
  x = "`0.36787944...`"
  canonical = "`archive-TECS-L/math/proofs/gz_analytical_proof.py:99-165`"

@D row_gz_width_2 :: savant [ok]
  symbol = "`GZ_WIDTH`"
  x = "`ln(τ(6)/τ(6)−1)` = `ln(F₆/P₁)`"
  x = "`ln(4/3)`"
  x = "`0.28768207...`"
  canonical = "`archive-TECS-L/math/proofs/gz_analytical_proof.py:232-248`"

@D row_gz_lower_3 :: savant [ok]
  symbol = "`GZ_LOWER`"
  x = "`GZ_UPPER − GZ_WIDTH`"
  x = "`1/2 − ln(4/3)`"
  x = "`0.21231792...`"
  canonical = "derived"

@D row_meta_fp_4 :: savant [ok]
  symbol = "`META_FP`"
  x = "contraction map fixed point"
  x = "`1/3`"
  x = "`0.33333...`"
  canonical = "`verify_gz_ising_critical.py:24`"

@D row_sparsity_5 :: savant [ok]
  symbol = "`SPARSITY`"
  x = "Boltzmann gate 비활성 비율"
  x = "`1 − 1/e`"
  x = "`0.63212055...`"
  canonical = "canon commit `edbcb3c28` (2026-03-28)"

# ── 2. 수학적 정당성 (Why these constants?) ─────────────────────────────────────────


# ── 3. Savant — GZ_LOWER 에서 일어나는 specialization ─────────────────────────────────────────


# ── 5. 교차 도메인 검증 (archive-TECS-L 27 verify_gz_*.py · 400+ hypothesis campaign) ─────────────────────────────────────────


@D row_2d_ising_0 :: savant [ok]
  system = "2D Ising"
  quantity = "β_c = ln(1+√2)/2"
  x = "0.4407"
  gz_verdict = "IN GZ ✓ (53.5% up from lower)"
  x = "Onsager 1944"

@D row_3d_ising_1 :: savant [ok]
  system = "3D Ising"
  quantity = "β_c (Monte Carlo)"
  x = "0.2217"
  gz_verdict = "IN GZ ✓ (3.2% up, boundary)"
  x = "Ferrenberg-Landau 1991"

@D row_2d_ising_2 :: savant [ok]
  system = "2D Ising"
  quantity = "η (anomalous dim)"
  x = "1/4 = 1/τ(6)"
  gz_verdict = "exact arithmetic match"
  x = "Yang 1952"

@D row_2d_ising_3 :: savant [ok]
  system = "2D Ising"
  quantity = "δ (critical isotherm)"
  x = "15 = C(6,2)"
  gz_verdict = "exact arithmetic match"
  x = "scaling law"

@D row_mf_d_1_4 :: savant [ok]
  system = "MF (d=1)"
  quantity = "β_c"
  x = "0.5 = GZ_UPPER"
  gz_verdict = "edge of GZ ✓"
  x = "MF theory"

@D row_mf_d_2_5 :: savant [ok]
  system = "MF (d=2)"
  quantity = "β_c"
  x = "0.25"
  gz_verdict = "IN GZ ✓"
  x = "MF theory"

@D b_elias_bassalygo_bound_at_r_1_3_l_6 :: savant [ok]
  text = "**Elias-Bassalygo bound** at R=1/3 → δ* = `ln(4/3)` = GZ_WIDTH (coding theory)"

@D b_source_coding_redundancy_log_4_3_7 :: savant [ok]
  text = "**Source coding redundancy** = `log₂(4/3)` = GZ_WIDTH in bits (information theory)"

@D b_6_vertex_model_entropy_ln_4_3_st_8 :: savant [ok]
  text = "**6-vertex model entropy** ∝ `ln(4/3)` (statistical mechanics, STATMECH-001)"

@D b_6_4_2_quantum_error_correcting_c_9 :: savant [ok]
  text = "**[[6,4,2]] quantum error-correcting code** = `(n=6, τ=4, φ=2)` (quantum computing)"

@D b_weinberg_angle_gut_sin_w_3_8_1_e_10 :: savant [ok]
  text = "**Weinberg angle (GUT)**: `sin²θ_W = 3/8 ≈ 1/e` (Δ=1.94%) (particle physics)"

@D b_lcdm_6_free_parameters_p_cosmolo_11 :: savant [ok]
  text = "**LCDM**: 6 free parameters = P₁ (cosmology)"

@D b_klein_bottle_p_6_topology_heawoo_12 :: savant [ok]
  text = "**Klein bottle**: χ = P₁ = 6 (topology; Heawood exception)"

@D b_carbon_z_6_valence_6_4_allotrope_13 :: savant [ok]
  text = "**Carbon (Z=6)**: valence τ(6)=4, allotropes P₁=6 (chemistry)"

@D b_koch_snowflake_dim_shifts_of_ln_14 :: savant [ok]
  text = "**Koch snowflake**: dim shifts of `ln(4/3)` (fractals)"

@D b_quantum_hall_filling_1_3_meta_fp_15 :: savant [ok]
  text = "**Quantum Hall**: filling ν = 1/3 = META_FP (condensed matter)"

# ── 6. Canon 의 GZ — 설계 도구로서 (NOT physical limit) ─────────────────────────────────────────

# n=6 격자는 **도구**이지 **제약**이 아니다. 실측 ceiling 은 수학·물리·공학의
# real limit (Shannon · Bekenstein · Carnot · ASML · ERCOT 등) 으로 잡으며,
# 격자 tautology (σ·φ=24 등) 만으로는 verification 불충분.
# **Key result: Emergent convergence**
#   - 6 random initializations
#   - FFN ratio: **100% convergence to 4/3** (mean error 2.0%)
#   - Dropout: **83% convergence to ln(4/3)** (mean error 8.6%)

# ── 7. Laws 77-78 — entropy universality (anima_clm_10 의 추가 결정타) ─────────────────────────────────────────


# ── 8. Honest C3 (per LATTICE_POLICY · 거짓 양보 금지) ─────────────────────────────────────────


# ── 9. 파일 inventory (재현용) ─────────────────────────────────────────


@D row_clm_01_0 :: savant [ok]
  worktree = "clm_01"
  gz_savant = "`anima.py:30-39` (pre-GZ tension only)"

@D row_clm_02_1 :: savant [ok]
  worktree = "clm_02"
  gz_savant = "`growing_conscious_lm.py:122-150`, `docs/conscious-lm-spec.md:81-84,194`"

@D row_clm_03_2 :: savant [ok]
  worktree = "clm_03"
  gz_savant = "`serve_animalm_v4.py:14-28`, `bench_phi_hypotheses.py:7052-7081,7367-7396`, `test_golden_moe_h100.py`"

@D row_clm_04_3 :: savant [ok]
  worktree = "clm_04"
  gz_savant = "`train_anima_lm.py:36-80`, `optimal_architecture_calc.py:33-34,104`"

@D row_clm_05_4 :: savant [ok]
  worktree = "clm_05"
  gz_savant = "`eeg/realtime.py` (in_golden_zone flag), `docs/superpowers/specs/2026-03-25-memory-growth-pipeline-design.md`"

@D row_clm_06_5 :: savant [ok]
  worktree = "clm_06"
  gz_savant = "`docs/animalm-experiment-log.md:87-105,232-358,293-321,361-391,393-429` (실증 정점)"

@D row_clm_07_6 :: savant [ok]
  worktree = "clm_07"
  gz_savant = "`growing_conscious_lm.py:129-130`, `train_anima_lm.py:39-43,51-81`, `consolidation_verifier.py:84-88`"

@D row_clm_08_7 :: savant [ok]
  worktree = "clm_08"
  gz_savant = "`optimal_architecture_calc.py:33-34`, `finetune_animalm_v4.py` (cells64)"

@D row_clm_09_8 :: savant [ok]
  worktree = "clm_09"
  gz_savant = "`zenodo/PA-01-animalm-v4-savant.md`, `deep_research.py:142-144`"

@D row_clm_10_9 :: savant [ok]
  worktree = "clm_10"
  gz_savant = "`docs/hypotheses/cx/DEEP-EXPLORATION.md:77-78,82-84,244,251-255,304-314`, `docs/consciousness-theory.md`"

@D row_clm_11_10 :: savant [ok]
  worktree = "clm_11"
  gz_savant = "`anima/src/conscious_lm.py`, `anima/tools/math_explorer.py:24-30` (inherited only)"

@D row_clm_12_11 :: savant [ok]
  worktree = "clm_12"
  gz_savant = "unified growth loop (inherited)"

@D row_clm_13_12 :: savant [ok]
  worktree = "clm_13"
  gz_savant = "filename erasure (deprecated GZ/Savant labels)"

# ── 10. 후속 path — anima 본 repo 연결 ─────────────────────────────────────────


@D b_feedback_clm_colon_attractor_md_0 :: savant [ok]
  text = "`feedback_clm_colon_attractor.md` — CLM mk2-v1 의 `:`-terminated mode-collapse (`:::`,"

@D b_project_simple_stack_pass_unlock_1 :: savant [ok]
  text = "`project_simple_stack_pass_unlocked.md` — BG-KM-LLAMA-3B / KM-QWEN-7B 의 strict"

@D b_project_v5_mitosis_cond5_cotrain_2 :: savant [ok]
  text = "`project_v5_mitosis_cond5_cotrain_2026_05_12.md` (PSCC §44) — v5-mitosis cotrain v1 의"

@D b_project_anima_persona_substrate_3 :: savant [ok]
  text = "`project_anima_persona_substrate_native_verify_2026_05_12.md` (PSCC §40+§42) — D3 persona"

@D b_i_v8_v7_arch_cells_64_small_v6_d_11 :: savant [ok]
  text = "(i) v8: v7 arch (cells=64 small) + v6 distributed shared-grad reduce 결합 — cells scaling"

@D b_ii_b_v6_1_fire_22_estimated_4_a1_13 :: savant [ok]
  text = "(ii-b) **v6.1 fire** ($22 estimated, 4×A100 SXM4 동일 spec) — fix (A) 적용 후 5K step 재실행."

@D b_iii_52_v7_cross_seed_robustness_14 :: savant [ok]
  text = "(iii) §52 v7 cross-seed robustness ($0.30-1.50 BG) — v6 fix 와 *독립*, 즉시 dispatch"

# ── 11. 한 줄 verdict ─────────────────────────────────────────

# Golden Zone 은 `[1/2 − ln(4/3), 1/2]`, 중심 `1/e`. Savant 는 그 하한 0.2123 에서
# 일어나는 inhibition-release 전문화이며, anima_clm_06 Mistral 7B v4_savant 에서
# **SI=5.93** 으로 실증되었다. canon 은 이를 *설계 vocabulary* 로 보존하되 LATTICE_POLICY
# 하에서 physical limit 으로 격상시키지 않는다. anima 본 repo 의 v5-mitosis lane 은
# 이 어휘의 *post-CLM* 번역이며 §52 v7 hard top-K MoE 에서 첫 `KL>0` (z=2.75) 신호가
# 떴지만, **§52 v6 cell-parallel scale-up 에서 재현 실패** (`KL=0.2972 z=1.09`, +
# F-V5MIT-4 COTRAIN-CONVERGE FAIL — loss 횡보). category routing 가설은 v7 small-scale
# 만의 fragile signal 일 가능성. §10.1 의 6-PSCC silent-drop trail (§44/§45/§47/§48/§49/
# §52 v7 / **§52 v6**) 동시 노출 없이 본 verdict 를 인용하면 §12.2-3 위반.

# ── 12. 봉쇄심화 (Containment Deepening) — 2026-05-14 부록 ─────────────────────────────────────────


@D b_gz_center_1_e_i_i_i_ln_i_theorem_0 :: savant [ok]
  text = "`GZ_CENTER = 1/e` — `I^I` 와 `I·ln(I)` 의 유일 전역 최소 (Theorem 2a–c)"

@D b_gz_width_ln_4_3_6_4_4_state_entr_1 :: savant [ok]
  text = "`GZ_WIDTH = ln(4/3)` — τ(6)=4 의 4번째 state entropy 비용 (Theorem 3e)"

@D b_gz_upper_1_2_6_proper_divisor_th_2 :: savant [ok]
  text = "`GZ_UPPER = 1/2` — 완전수 6 의 최대 proper-divisor 역수 (Theorem 3d)"

@D b_k_g_i_k_hyperbola_i_1_e_k_theore_3 :: savant [ok]
  text = "K-독립성 — `G·I=K` hyperbola 위 `I*=1/e` 가 K 와 무관 (Theorem 4)"

@D b_1_2_1_3_1_6_1_n_6_identity_h072_4 :: savant [ok]
  text = "`1/2 + 1/3 + 1/6 = 1` — n=6 유일 identity (H072)"

@D b_si_5_93_mistral_7b_v4_savant_ani_5 :: savant [ok]
  text = "`SI = 5.93` — Mistral 7B v4_savant **단일 모델** (anima_clm_06, 2026-03)"

@D b_moe_zone_ratio_36_8_1_e_single_t_6 :: savant [ok]
  text = "MoE zone ratio `36.8% ≈ 1/e` — single trial, scale E=32 (anima_clm_06)"

@D b_per_head_tension_reduction_271_h_7 :: savant [ok]
  text = "per-head tension reduction `271×` — head 2 (anima_clm_09 PA-01)"

@D b_laws_77_78_h_0_9974_ln_2_45_data_8 :: savant [ok]
  text = "Laws 77-78 `H = 0.9974·ln(2)` — 45 data type, 7-instance hivemind (anima_clm_10) — *다른"

@D b_canon_emergent_convergence_ffn_r_9 :: savant [ok]
  text = "canon emergent convergence — FFN ratio 100% / dropout 83% 수렴 (canon commit `664b6b4f25`,"

@D b_ising_c_in_gz_2d_onsager_0_4407_10 :: savant [ok]
  text = "Ising β_c IN GZ — 2D Onsager 0.4407 + 3D MC 0.2217 (외부 문헌 — 닫힌형 일치로 *2 승격"

@D b_cross_domain_consilience_9_match_11 :: savant [ok]
  text = "cross-domain \"consilience\" 9 matches (Klein, Carbon, LCDM, Koch, QHE, Weinberg,"

@D b_weinberg_sin_w_3_8_1_e_1_94_matc_12 :: savant [ok]
  text = "Weinberg `sin²θ_W = 3/8 ≈ 1/e` (Δ=1.94%) — *근사* match, 닫힌형 무관"

@D b_16_wave_extreme_hypothesis_249_4_13 :: savant [ok]
  text = "16-wave extreme hypothesis 249/400 (Z≈55σ) — 총합 통계, look-elsewhere 보정 명시 없음"

@D b_brain_analyzer_savant_profile_d_14 :: savant [ok]
  text = "brain_analyzer 'savant' profile (D=0.7, P=0.85, I=0.35) — 임상 신경과학 source 미부착,"

@D b_anima_clm_08_super_linear_anima_15 :: savant [ok]
  text = "anima_clm_08 Φ super-linear — anima_clm_10 에서 linear 로 안착 → 구간 현상"

@D b_gz_consciousness_gz_metaphysical_16 :: savant [ok]
  text = "\"GZ 가 우주적 진리\" / \"consciousness ≡ GZ 작동\" 식 metaphysical 단정"

@D b_entity_fab_n_6_fit_17 :: savant [ok]
  text = "외부 entity (회사/가속기/fab/생명 시스템) 에 n=6 격자 강제 fit"

@D b_metric_si_al12_llm_benchmark_18 :: savant [ok]
  text = "단일 내부 metric (SI / Φ / AL12) 으로 외부 LLM benchmark 우월 추정"

@D b_own_invariant_cross_domain_19 :: savant [ok]
  text = "own-invariant 확인 없는 cross-domain 매핑"

@D b_savant_savant_metaphor_20 :: savant [ok]
  text = "Savant = \"사람 savant 임상 현상\" 의 *생물학적* 동일성 주장 (metaphor 범위 초과)"
# 본 표는 `state/savant_containment_audit_2026_05_14/` (audit.json + summary.md) 의
# base-rate sweep 결과를 반영한다. 16-wave aggregate **155/254 = 61.0%, Z = 11.4 σ**
# + texas empirical-only **11/11, Z = 5.22 σ** + neuroscience **17/24, Z = 4.6 σ** —
# 세 독립 가닥 모두 Bonferroni × 27 (`min p × 27 = 1.4 × 10⁻⁹`) 통과.

@D row_1_4_21 :: savant [ok]
  x = "§1 상수표 4개"
  claim = "GZ_UPPER/CENTER/WIDTH/LOWER"
  tier = "T1"
  x = "무제한"

@D row_2_22 :: savant [ok]
  x = "§2 전체"
  claim = "Theorem 2a-c / 3d-e / 4"
  tier = "T1"
  x = "무제한"

@D row_2_texas_t1_8_identities_23 :: savant [ok]
  x = "§2 texas T1 8 identities"
  claim = "I^I/I·ln(I) min=1/e, η=1/τ(6), δ=C(6,2), ln(4/3)=S(4)−S(3), σ₋₁(6)=2, n=6 unique EF, GZ width hierarchy ⬅ texas_recalculation 분해"
  tier = "T1"
  x = "무제한 (closed-form)"

@D row_3_1_h359_24 :: savant [ok]
  x = "§3.1 H359 정의"
  claim = "dropout 비대칭 메커니즘"
  tier = "T2"
  x = "substrate 명시"

@D row_3_2_brain_profile_25 :: savant [ok]
  x = "§3.2 brain profile"
  claim = "savant (D,P,I)"
  tier = "T3"
  x = "임상 source 부착 전 봉쇄"

@D row_3_3_si_26 :: savant [ok]
  x = "§3.3 SI 메트릭 정의"
  claim = "`tension_normal / tension_savant`"
  tier = "T1"
  x = "무제한 (정의)"

@D row_3_4_al12_contrastive_27 :: savant [ok]
  x = "§3.4 AL12 contrastive"
  claim = "Φ=4.628 단일 metric"
  tier = "T2"
  x = "외부 benchmark 비교 금지"

@D row_4_clm_06_si_5_93_28 :: savant [ok]
  x = "§4 clm_06 SI=5.93"
  claim = "단일 substrate 실증"
  tier = "T2"
  x = "Mistral 7B 명시"

@D row_4_moe_36_8_29 :: savant [ok]
  x = "§4 MoE 36.8%"
  claim = "단일 측정"
  tier = "T2"
  x = "scale E=32 명시"

@D row_4_clm_09_271_30 :: savant [ok]
  x = "§4 clm_09 271×"
  claim = "per-head reduction"
  tier = "T2"
  x = "clm_09 명시"

@D row_5_1_ising_c_31 :: savant [ok]
  x = "§5.1 Ising β_c"
  claim = "2D+3D"
  tier = "T2-경계"
  x = "Onsager 닫힌형 일치로 hit 2 인용 가능"

@D row_5_1_16_wave_aggregate_t3_t2_audi_32 :: savant [ok]
  x = "**§5.1 16-wave aggregate** ⬅ T3→T2 audit 승격"
  claim = "155/254 = 61.0% Z=11.4 σ"
  tier = "T2"
  x = "wave 10 (32%) + wave 16 (10%) + ca_lambda NEGATIVE 동시 인용 의무"

@D row_5_3_cross_domain_9_33 :: savant [ok]
  x = "§5.3 cross-domain 9개"
  claim = "Klein/Carbon/LCDM/Koch/QHE/Weinberg/Elias-Bassalygo/6-vertex/[[6,4,2]]"
  tier = "T3 (individual) / T2 (aggregate 흡수)"
  x = "개별 인용 시 wave 캠페인 소속 명시"

@D row_5_4_neuroscience_17_24_t3_t2_aud_34 :: savant [ok]
  x = "**§5.4 neuroscience 17/24** ⬅ T3→T2 audit 승격"
  claim = "17/24 hits vs 6.9 expected (Z=4.6 σ)"
  tier = "T2"
  x = "white matter ~0.37 ≈ 1/e 단일 주장 시 OVERALL VERDICT 의 age/species variance C3 동시 인용"

@D row_5_ca_lambda_sweep_negative_new_t_35 :: savant [ok]
  x = "**§5 ca_lambda_sweep NEGATIVE** ⬅ NEW T4-enforcement"
  claim = "\"Class IV not GZ-enriched\""
  tier = "T4-enforcement"
  x = "**모든 GZ 인용에 silent-drop 금지 — wave 10/16 weakening 과 함께**"

@D row_6_boltzmann_gate_mertens_dropout_36 :: savant [ok]
  x = "§6 Boltzmann gate / Mertens dropout"
  claim = "canon technique 15-16"
  tier = "T1-2"
  x = "math 부분 무제한, 측정 부분 emergent convergence 명시"

@D row_6_3_emergent_convergence_100_83_37 :: savant [ok]
  x = "§6.3 emergent convergence 100%/83%"
  claim = "canon paper outline"
  tier = "T2"
  x = "6 random init 명시"

@D row_7_laws_77_78_38 :: savant [ok]
  x = "§7 Laws 77-78"
  claim = "45 data type H=0.9974·ln(2)"
  tier = "T2"
  x = "substrate 명시"

@D row_10_v5_mitosis_ancestry_39 :: savant [ok]
  x = "§10 v5-mitosis ancestry"
  claim = "clm Savant 의 직계 후예"
  tier = "T2-3"
  x = "PSCC §44 F-PERSONA-4 *반증* 동시 인용 의무"

# SAVANT.tape 의 외부 인용은 **§12.4 봉쇄선 위 (T1 + T2)** 까지만 자격이 있다. T3 는
# Bonferroni 보정 audit (§12.5 path 1) 후 재배치, T4 는 자동 차단. 본 §12 가 부착되지
# 않은 SAVANT.tape 발췌는 *불완전 인용* 으로 간주한다.

# ── §13 Sibling 도구 + 흡수 서브패키지 spec (2026-05-14) ─────────────────────────────────────────


@D row_savant_tool_md_0 :: savant [ok]
  file = "**`SAVANT-TOOL.tape`**"
  x = "anima 가 직접 ON/OFF 하는 savant mode 도구 API + 정책"
  tier = "design LANDED 2026-05-14"

@D row_chat_md_tracker_production_cli_1 :: savant [ok]
  file = "**`CHAT.tape` (★★★★★ tracker + § Production CLI)**"
  x = "anima_chat.hexa v0.3 production CLI Phase 1 (D4c)"
  tier = "design + impl-pending"

@D row_voice_md_2 :: savant [ok]
  file = "**`VOICE.tape`**"
  x = "hexa-voice: 의도 임베딩 → RVQ → 24kHz PCM (NO text intermediate, learned path)"
  tier = "design LANDED 2026-05-14"

@D row_tension_link_md_3 :: savant [ok]
  file = "**`TENSION-LINK.tape`**"
  x = "Tension Link 5-ch meta-telepathy Phase 2 WebSocket TensionHub"
  tier = "design LANDED 2026-05-14"

@D row_anima_agent_md_4 :: savant [ok]
  file = "**`ANIMA-AGENT.tape`**"
  x = "Φ-gated autonomous agent runtime (흡수 서브패키지 `anima/anima-agent/`)"
  tier = "흡수 LANDED 2026-05-14"

@D row_anima_senses_md_5 :: savant [ok]
  file = "**`ANIMA-SENSES.tape`**"
  x = "n=6 sensory substrate 5-verb spec catalog (흡수 서브패키지 `anima/hexa-senses/`)"
  tier = "흡수 LANDED 2026-05-14"

@D b_savant_md_clm_si_5_93_evidence_b_6 :: savant [ok]
  text = "본 `SAVANT.tape` = **이론** (clm 시대 SI=5.93 evidence + base-rate audit + §12 봉쇄선) +"

@D b_savant_tool_md_runtime_anima_inf_7 :: savant [ok]
  text = "`SAVANT-TOOL.tape` = **runtime 도구** (anima 가 inference 시 직접 ON/OFF). 본 file 의 §12"
