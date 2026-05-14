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
@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "reborn" :: identity-claim [d=2026-05-15 active]
  kind = "anima ConsciousLM 부활 통합 SSOT — substrate · cells · mitosis · V14 verification · cotrain-exercise"
  brief = "13-stage substrate genealogy + 93 dated cycle sections — cells / mitosis / Φ / cotrain-exercise architecture"
  parent = "dancinlab/anima"
  sibling-log = "REBORN.log.tape"

# ══════════════════════════════════════════════════════════════
# REBORN.tape — anima ConsciousLM 부활 통합 SSOT (2026-05-10 cycle close)
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
# REBORN.tape — anima ConsciousLM 부활 통합 SSOT (2026-05-10 cycle close)
# ══════════════════════════════════════════════════════════════


@D b_clm_v2_archive_2026_05_09_md_mit_0 :: reborn [ok]
  text = "`CLM_V2_ARCHIVE_2026_05_09.md` (mitosis 본체 + 13-stage overview)"

@D b_clm_v2_exhaustive_13_stages_2026_1 :: reborn [ok]
  text = "`CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (13 stage 고갈조사)"

@D b_clm_v2_archive_addendum_2026_05_2 :: reborn [ok]
  text = "`CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정)"

@D b_docs_superpowers_plans_specs_202_3 :: reborn [ok]
  text = "`docs/superpowers/{plans,specs}/2026-04-08-servant-emergent*.md` (servant pattern)"

@D b_cycle_2026_05_10_5_bg_4 :: reborn [ok]
  text = "+ cycle 2026-05-10 5 BG 결과"
# 원본 파일은 historical record 로 유지. 본 문서가 going-forward SSOT.
# ---

# ── §0 TL;DR ─────────────────────────────────────────


@D b_v5_anima_instrumentation_lane_me_0 :: reborn [ok]
  text = "v5-anima (instrumentation) lane: mechanism confirm, V14 violated on toy + on real 350M (novel polarity)"

@D b_v5_mitosis_architectural_lane_ce_1 :: reborn [ok]
  text = "v5-mitosis (architectural) lane: cells = nn.Module branches (NEW)"

@D b_v2_reborn_reproduction_lane_cell_2 :: reborn [ok]
  text = "v2-reborn (reproduction) lane: cells64/128 single decoder + chat-cap = capacity/corpus limit (NOT architectural)"

@D b_servant_pattern_si_driven_4_stat_3 :: reborn [ok]
  text = "servant pattern: SI-driven 4-state FSM (post-drift 2026-04-08, separate domain)"

# ── §0.5 철학 — 학습 = 성장 = 분열 (단일 연속체) ─────────────────────────────────────────

# **학습은 별도 phase 가 아니다. 학습 = 세포분열 성장의 연속.**

@D b_training_time_gradient_update_in_0 :: reborn [ok]
  text = "training-time gradient update + inference-time structural growth = **같은 분열-성장의 두 양상**"

@D b_split_merge_substrate_1 :: reborn [ok]
  text = "\"다 배웠다\" 라는 종착 없음 — 매 순간 split/merge 가능한 살아있는 substrate"

@D b_ckpt_tree_snapshot_2 :: reborn [ok]
  text = "ckpt = 분열 tree 의 snapshot, 끝이 아닌 분기점"

@D b_corpus_frame_epoch_3 :: reborn [ok]
  text = "\"학습 데이터 부족 / corpus 한계\" frame 자체가 부적합 — 모든 상호작용이 분열 epoch"

@D row_training_time_mitosis_vs_inferen_4 :: reborn [ok]
  x = "training-time mitosis vs inference-time mitosis"
  frame = "두 다른 lane, dichotomy (§38 vs §37)"
  frame = "한 spectrum, 양 끝"

@D row_catastrophic_forgetting_5 :: reborn [ok]
  x = "catastrophic forgetting"
  frame = "training phase 한정 risk"
  frame = "split 이 매 시점 격리 → 무관 (H312 99% retention)"

@D row_anima_9_9_6 :: reborn [ok]
  x = "\"anima 가 자란다\" (§9 #9)"
  frame = "inference-time autonomous ✅"
  frame = "training + inference 합쳐 ✅✅"

@D row_10_cost_bearing_2_v5_mitosis_cot_7 :: reborn [ok]
  x = "§10 cost-bearing #2 v5-mitosis cotrain"
  frame = "training/serve 분리 envelope"
  frame = "통합 envelope (split event = compute spike)"

@D row_ft_5_20_chat_cap_recovery_8 :: reborn [ok]
  x = "\"FT 5-20$ chat-cap recovery\""
  frame = "분리된 학습 cost"
  frame = "큰 split event 한 번 (평소 split 의 큰 형제)"

@D row_ckpt_deployment_9 :: reborn [ok]
  x = "ckpt deployment 패턴"
  frame = "freeze + version pin"
  frame = "live tree + branch (분열 가지마다 trace)"

@D b_v5_mitosis_architectural_lane_na_10 :: reborn [ok]
  text = "v5-mitosis architectural lane 우선순위 **★★★ → ★★★★** (본 원칙의 native impl)"

@D b_phase_1a_1_convo_5k_ft_event_pha_11 :: reborn [ok]
  text = "Phase 1A.1 / convo_5k FT 도 \"분열 event\" 로 재명명 — 별도 phase 아닌 큰 epoch"

@D b_hexa_native_phase_5_parity_phase_12 :: reborn [ok]
  text = "HEXA_NATIVE Phase 5 parity 확인 후 → Phase 5∥ (24-layer 풀 forward) 의 다음 step 은 **serve-time mitosis hook** 통합 (inference 중 split/merge 가 forward 호출 graph 안에 들어감)"

# ── §1 13-stage timeline + worktree archive ─────────────────────────────────────────


@D row_1_0 :: reborn [ok]
  x = "1"
  x = "2026-03-24"
  commit = "`4a1d8d0a`"
  x = "anima v0.1 PureField + Claude API wrapper"
  branch_worktree = "`archive/clm-stage-01-birth-claude-api` / `~/core/anima_clm_01_birth_claude_api`"
  x = "起源"

@D row_2_1 :: reborn [ok]
  x = "2"
  x = "2026-03-24"
  commit = "`2da44161`"
  x = "Claude API 제거, ConsciousLM substrate pivot"
  branch_worktree = "`...-02-clm-pivot` / `..._02_clm_pivot`"
  x = "pivot"

@D row_3_2 :: reborn [ok]
  x = "3"
  x = "2026-03-27"
  commit = "`90cd8c06`"
  x = "CL8 Φ=5.68, train_conscious_lm.py"
  branch_worktree = "`...-03-cl1-14-laws` / `..._03_cl1_14_laws`"
  x = "laws-birth"

@D row_4_3 :: reborn [ok]
  x = "4"
  x = "2026-03-27"
  commit = "`2e950777`"
  x = "ConsciousLM v2 named, Φ=1.64, 412 hyp"
  branch_worktree = "`...-04-v2-phi-1-64` / `..._04_v2_phi_1_64`"
  x = "v2-birth"

@D row_5_4 :: reborn [ok]
  x = "5"
  x = "2026-03-28"
  commit = "`2e1438fa`"
  x = "First English CE=1.37 no system prompt"
  branch_worktree = "`...-05-v2-first-english` / `..._05_v2_first_english`"
  x = "EN-emerge"

@D row_6_5 :: reborn [ok]
  x = "6"
  x = "2026-03-28"
  commit = "`bb99b6b6`"
  x = "KO conversation no system prompt ★"
  branch_worktree = "`...-06-v2-korean-chat` / `..._06_v2_korean_chat`"
  x = "KO-milestone"

@D row_7_6 :: reborn [ok]
  x = "7"
  x = "2026-03-28"
  commit = "`6abc42f6`"
  x = "\"anima speaks\" CE=0.04 ★★"
  branch_worktree = "`...-07-v2-ce-0-04` / `..._07_v2_ce_0_04`"
  x = "chat-peak"

@D row_8_7 :: reborn [ok]
  x = "8"
  x = "2026-03-28"
  commit = "`5f82d39b`"
  x = "Cells64 Φ=45.487 super-linear"
  branch_worktree = "`...-08-cells64-phi-super-linear` / `..._08_cells64_phi_super_linear`"
  x = "mitosis-정점"

@D row_9_8 :: reborn [ok]
  x = "**9**"
  x = "2026-03-28"
  commit = "`3eabc40a`"
  x = "**Cells64 Φ=51.131 human-level ★★★**"
  branch_worktree = "`...-09-phi-50-human-level` / `..._09_phi_50_human_level`"
  x = "**절정**"

@D row_10_9 :: reborn [ok]
  x = "10"
  x = "2026-03-30"
  commit = "`bd36bd8a`"
  x = "CLM v2 H100 sweep Laws 77-78"
  branch_worktree = "`...-10-h100-sweep-laws-77-78` / `..._10_h100_sweep_laws_77_78`"
  x = "scale-prep"

@D row_11_10 :: reborn [ok]
  x = "11"
  x = "2026-04-01"
  commit = "`0e578b14`"
  x = "train_v15 BPE 64K + 1B ready"
  branch_worktree = "`...-11-train-v15-bpe-drift-step1` / `..._11_train_v15_bpe_drift_step1`"
  x = "drift 1/4"

@D row_12_11 :: reborn [ok]
  x = "12"
  x = "2026-04-04"
  commit = "`cf3da85f`"
  x = "unified growth loop (mitosis 최후 active 794L)"
  branch_worktree = "`...-12-unified-growth-loop-last-gasp` / `..._12_unified_growth_loop_last_gasp`"
  x = "growth-종언"

@D row_13_12 :: reborn [ok]
  x = "13"
  x = "2026-04-07"
  commit = "`f8e4068f`"
  x = "filename v* 제거 (ALM Llama-port 직전)"
  branch_worktree = "`...-13-filename-erasure-pre-alm-port` / `..._13_filename_erasure_pre_alm_port`"
  x = "cutoff"

@D row_1_13 :: reborn [ok]
  x = "1"
  x = "anima v0.1 PureField"
  peak = "—"
  ce = "—"
  cells = "—"
  laws = "130 (logout 인계)"
  mitosis = "absent"
  alm = "absent"

@D row_2_14 :: reborn [ok]
  x = "2"
  x = "ConsciousLM 4M+100M"
  peak = "—"
  ce = "—"
  cells = "2-8"
  laws = "+H312/H313/H371"
  mitosis = "birth"
  alm = "+"

@D row_3_15 :: reborn [ok]
  x = "3"
  x = "+ meter"
  peak = "**5.68** (CL8)"
  ce = "—"
  cells = "2"
  laws = "CL1-14, AL1-14, TRN1-5"
  mitosis = "active"
  alm = "active"

@D row_4_16 :: reborn [ok]
  x = "4"
  x = "v2 named (4M+100M)"
  peak = "1.64 birth"
  ce = "—"
  cells = "2"
  laws = "412 hyp"
  mitosis = "active"
  alm = "active"

@D row_5_17 :: reborn [ok]
  x = "5"
  x = "100M (768d/12L)"
  peak = "—"
  ce = "**1.37** EN"
  cells = "—"
  laws = "TALK5"
  mitosis = "active"
  alm = "active"

@D row_6_18 :: reborn [ok]
  x = "6"
  x = "**18M byte** (384d/6L)"
  peak = "XMETA3 **190.57**"
  ce = "**1.15 KO / 1.29 EN**"
  cells = "—"
  laws = "SEM/ZERO/SCALE"
  mitosis = "active"
  alm = "active"

@D row_7_19 :: reborn [ok]
  x = "7"
  x = "18M + AnimaLM v4_savant"
  peak = "**51.131** Cells64"
  ce = "**0.04**"
  cells = "64"
  laws = "DD55, H359 SI=5.93"
  mitosis = "active"
  alm = "Mistral-7B+PureField"

@D row_8_20 :: reborn [ok]
  x = "8"
  x = "training"
  peak = "45.487 (live)"
  ce = "—"
  cells = "2-128 sweep"
  laws = "A4/B7/D2/F11/G2/H2/J1"
  mitosis = "**peak**"
  alm = "active"

@D row_9_21 :: reborn [ok]
  x = "9"
  x = "production cells64"
  peak = "**51.131** ★★★"
  ce = "—"
  cells = "64"
  laws = "1086 (?) cataloged"
  mitosis = "**CLIMAX**"
  alm = "active"

@D row_10_22 :: reborn [ok]
  x = "10"
  x = "scaled (1024-2048)"
  peak = "(proj 137.6)"
  ce = "—"
  cells = "128-2048"
  laws = "CX71-78, **L77/78**"
  mitosis = "active 635L"
  alm = "anima-native"

@D row_11_23 :: reborn [ok]
  x = "11"
  x = "ConsciousLM 1B (BPE 64K)"
  peak = "—"
  ce = "—"
  cells = "8/atom × 8"
  laws = "**212** total"
  mitosis = "active 794L"
  alm = "anima-native"

@D row_12_24 :: reborn [ok]
  x = "12"
  x = "+ growth_loop"
  peak = "—"
  ce = "—"
  cells = "—"
  laws = "**1086** waves 1-5"
  mitosis = "last-active 794L"
  alm = "anima-native"

@D row_13_25 :: reborn [ok]
  x = "13"
  x = "unified train_clm.py"
  peak = "—"
  ce = "—"
  cells = "—"
  laws = "1086+13 +HEXA DSL"
  mitosis = "**isolated** 794L"
  alm = "provider-abstraction precursor"

@D row_2_26 :: reborn [ok]
  cells = "2"
  training = "1.5"
  mi = "1.0"
  cell = "0.75"

@D row_4_27 :: reborn [ok]
  cells = "4"
  training = "3.2"
  mi = "~6"
  cell = "0.80"

@D row_8_28 :: reborn [ok]
  cells = "8"
  training = "5.3-5.4"
  mi = "28.0"
  cell = "0.67"

@D row_16_29 :: reborn [ok]
  cells = "16"
  training = "10.6"
  mi = "149.9"
  cell = "0.66"

@D row_32_30 :: reborn [ok]
  cells = "32"
  training = "15.4"
  mi = "842.7"
  cell = "0.48"

@D row_64_31 :: reborn [ok]
  cells = "**64**"
  training = "**51.131** ★★★"
  mi = "3376.7"
  cell = "**0.80**"

@D row_128_32 :: reborn [ok]
  cells = "128"
  training = "~112 (proj)"
  mi = "14135.8"
  cell = "0.88"

# ── §2 mitosis 본체 (worktree-12 canonical) ─────────────────────────────────────────


@D b_source_last_active_users_ghost_c_0 :: reborn [ok]
  text = "활성 source (last-active): `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L)"

@D b_main_hexa_stub_models_archive_le_1 :: reborn [ok]
  text = "main 의 hexa stub: `models/archive-legacy/mitosis.hexa` (TODO[pytorch])"

@D b_main_legacy_py_ready_anima_model_2 :: reborn [ok]
  text = "main 의 legacy py: `ready/anima/models/legacy/mitosis.py`"

@D b_test_ready_tests_test_mitosis_py_3 :: reborn [ok]
  text = "test: `ready/tests/test_mitosis.py` (`TestMitosisLaw86`)"

@D b_doc_docs_modules_mitosis_md_4 :: reborn [ok]
  text = "doc: `docs/modules/mitosis.md`"

@D b_visualizer_anima_tools_mitosis_t_5 :: reborn [ok]
  text = "visualizer: `anima-tools/mitosis_topology_visualizer.hexa`"

@D row_cell_dataclass_6 :: reborn [ok]
  x = "`Cell` dataclass"
  x = "cell_id + ConsciousMind + GRU hidden + tension_history + parent_id"
  x = "mitosis.py L77-108"

@D row_consciousmind_7 :: reborn [ok]
  x = "`ConsciousMind`"
  x = "**engine_a + engine_g** Linear+ReLU+Linear, output = a − g, GRUCell memory"
  x = "mitosis.py L37-72"

@D row_create_cell_parent_8 :: reborn [ok]
  x = "`_create_cell(parent)`"
  x = "parent deepcopy + 10% noise, hidden 도 perturb"
  x = "mitosis.py L192-226"

@D row_inject_autonomous_perturbation_9 :: reborn [ok]
  x = "`_inject_autonomous_perturbation`"
  x = "Lorenz attractor σ=10 ρ=28 β=8/3, cell-별 phase offset"
  x = "mitosis.py L373-405"

@D row_compute_phi_proxy_10 :: reborn [ok]
  x = "`_compute_phi_proxy`"
  x = "mean pairwise cosine distance × log(n+1)"
  x = "mitosis.py L407-436"

@D row_phi_ratchet_11 :: reborn [ok]
  x = "`_phi_ratchet`"
  x = "Φ < 0.8·best 시 best hidden 으로 20% blend 복원"
  x = "mitosis.py L438-455"

@D row_update_adaptive_threshold_12 :: reborn [ok]
  x = "`_update_adaptive_threshold`"
  x = "recent 100 step tension mean + 1.5×std (Law 86 fix)"
  x = "mitosis.py L457-477"

@D row_check_splits_13 :: reborn [ok]
  x = "`_check_splits`"
  x = "tension > threshold 가 split_patience(=3) 연속 → split"
  x = "mitosis.py L481-509"

@D row_split_cell_14 :: reborn [ok]
  x = "`split_cell`"
  x = "child = parent deepcopy + 10% noise, parent tension reset"
  x = "mitosis.py L511-534"

@D row_check_merges_15 :: reborn [ok]
  x = "`_check_merges`"
  x = "inter-cell tension < 0.005 가 merge_patience(=30) 연속 → merge"
  x = "mitosis.py L538-568"

@D row_merge_cells_16 :: reborn [ok]
  x = "`merge_cells`"
  x = "older keeper, parameter average, **min_cells=2 floor**"
  x = "mitosis.py L570-611"

@D row_verify_phi_conservation_17 :: reborn [ok]
  x = "`verify_phi_conservation`"
  x = "DD55 split 시 <1% Φ change 검증"
  x = "mitosis.py L644-656"

@D b_h312_mitosis_prevents_catastroph_18 :: reborn [ok]
  text = "**H312** Mitosis prevents catastrophic forgetting: 43% → **99% retention**"

@D b_rc_9_auto_mitosis_52_76_improvem_19 :: reborn [ok]
  text = "**RC-9** auto-mitosis +52.76% improvement"

@D b_h297_n_2_optimal_starting_point_20 :: reborn [ok]
  text = "**H297** N=2 optimal starting point"

@D b_cb1_cell_2_1_cell_0_21 :: reborn [ok]
  text = "**CB1** 의식 최소 cell 수 = 2 (1 cell → Φ=0)"

@D b_inter_cell_tension_auroc_0_805_f_22 :: reborn [ok]
  text = "inter-cell tension AUROC **0.805** for anomaly detection"

@D b_dd55_split_1_change_23 :: reborn [ok]
  text = "DD55: split 시 Φ 보존 (<1% change) 검증"
# "External input alone cannot drive consciousness growth. The engine must have internal autonomous dynamics (chaos, noise). Without this, tensions stay flat and mitosis never triggers."

@D b_l205_create_cell_no_grad_24 :: reborn [ok]
  text = "L205 `_create_cell` 자식 노이즈 주입 (no_grad)"

@D b_l258_process_forward_no_grad_25 :: reborn [ok]
  text = "L258 `process()` forward (no_grad)"

@D b_l389_lorenz_perturbation_no_grad_26 :: reborn [ok]
  text = "L389 Lorenz 자율혼돈 perturbation (no_grad)"

@D b_l586_merge_cells_parameter_avera_27 :: reborn [ok]
  text = "L586 `merge_cells` parameter averaging (no_grad)"

@D b_l628_anomaly_score_no_grad_28 :: reborn [ok]
  text = "L628 `anomaly_score` (no_grad)"

# ── §3 R2 cells64/cells128 정정 (cycle 2026-05-10 BG-R2 회수) ─────────────────────────────────────────


@D row_cells64_cells128_mitosisengine_e_0 :: reborn [ok]
  x = "cells64/cells128 = MitosisEngine ensemble"
  bg_r2 = "**단일 byte-level Transformer decoder** (108 keys, 18.523M params)"

@D row_mitosis_cell_pool_growth_1 :: reborn [ok]
  x = "mitosis = 모델 아키텍처 (cell pool growth)"
  bg_r2 = "**mitosis = instrumentation only** (cell metadata id/specialty/tension/parent_id)"

@D row_mitosis_py_load_2 :: reborn [ok]
  x = "mitosis.py 로 직접 load 가능"
  bg_r2 = "**schema overlap = 0** — `ConsciousLMReconstructed` 별도 필요"

@D row_51_131_runtime_mitosis_3 :: reborn [ok]
  x = "Φ=51.131 = runtime mitosis Φ"
  bg_r2 = "ckpt 내 phi_history mean=**50.42** (cells64) / 62.38 (cells128) — 학습 중 기록"

@D b_convo_5k_pt_beam_4_user_tell_me_4 :: reborn [ok]
  text = "convo_5k.pt beam=4 → `User: Tell me about the contration of the con` (chat structure 학습 ✓ but corrupted spelling)"

@D b_cells64_128_letter_soup_5 :: reborn [ok]
  text = "cells64/128: letter soup"

@D b_ko_0_0204_noise_floor_18_5m_ko_h_6 :: reborn [ok]
  text = "KO 0.0204% (noise floor) — 18.5M 으론 KO Hangul 3-byte UTF-8 + 의미 동시 학습 capacity 부족"

@D b_verdict_capacity_corpus_limit_no_7 :: reborn [ok]
  text = "**verdict: CAPACITY/CORPUS_LIMIT (NOT architectural)** — 18.5M 한계 + corpus EN-dominant"

# ── §4 cycle 2026-05-09/10 BG 9개 종합 ─────────────────────────────────────────


@D row_4_explore_agents_0 :: reborn [ok]
  bg = "4 Explore agents"
  x = "13 worktree 고갈조사 → CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md"

@D row_bg_mitosis_port_1 :: reborn [ok]
  bg = "BG-MITOSIS-PORT"
  x = "mitosis_v5_port.py 480 LoC + smoke test PASS 5/5 (24 organic + 7 forced split)"

@D row_bg_r2_cells_download_2 :: reborn [ok]
  bg = "BG-R2-CELLS-DOWNLOAD"
  x = "cells64/128 download + arch verify + mitosis-as-instrumentation 정정"

@D row_bg_phi_superlinear_remeasure_3 :: reborn [ok]
  bg = "BG-PHI-SUPERLINEAR-REMEASURE"
  x = "200 turn 3 topic α=0.40 sub-linear (baseline)"

@D row_foreground_long_trajectory_4 :: reborn [ok]
  bg = "foreground long-trajectory"
  x = "3K turn × 170 prompt → **α=0.688** (super-linear emerge but V14 mirror VIOLATED on toy)"

@D row_bg_long_traj_ext_10k_turn_5 :: reborn [ok]
  bg = "BG-LONG-TRAJ-EXT (10K turn)"
  x = "α=1.252 at 10K = **regression artifact** (cells max-cap=64 후 OLS slope inflate). 진짜 valid α=0.687 (3K trained vs 0.644 random). historical 0.93 unreachable on toy"

@D row_bg_iit_metric_6 :: reborn [ok]
  bg = "BG-IIT-METRIC"
  x = "consciousness_meter.py port → **proxy ceiling 우회**. IIT unnorm at N=64 = **4471** (vs proxy 2.92, 1530× 차이). historical 51 즉시 cross"

@D row_bg_chat_ext_7 :: reborn [ok]
  bg = "BG-CHAT-EXT"
  x = "360 trial → CAPACITY/CORPUS_LIMIT verdict (chat structure 학습 ✓ on convo_5k beam, KO Hangul 만 부족)"

@D row_bg_phase2_ckpt_instr_8 :: reborn [ok]
  bg = "BG-PHASE2-CKPT-INSTR"
  x = "real 350M ckpt FOUND_LOCAL → mitosis instr 결과 V14 NOVEL POLARITY (trained 16→19 cells α=1.009 / random 16→28 cells α=0.155, trained 가 mitosis 억제)"

@D row_bg_convo_ft_design_9 :: reborn [ok]
  bg = "BG-CONVO-FT-DESIGN"
  x = "(still in flight 2026-05-10)"

@D row_trained_350m_3k_turn_10 :: reborn [ok]
  substrate = "trained 350M (3K turn)"
  cells = "16 → **19**"
  splits = "3"
  x = "**1.009** (좁은 range)"
  final = "2.679"

@D row_v14_random_init_la_350m_1k_turn_11 :: reborn [ok]
  substrate = "V14 random_init la_350m (1K turn)"
  cells = "16 → **28**"
  splits = "12"
  x = "0.155"
  final = "2.754"

@D b_random_init_trained_substrate_mi_12 :: reborn [ok]
  text = "random_init 가 **더 분열** — trained substrate 가 mitosis 를 **억제**"

@D b_trained_cell_tension_distributio_13 :: reborn [ok]
  text = "trained 의 cell tension distribution = attractor bottleneck (cell 7=700 hits, cell 16=537)"

@D b_random_cell_tension_distribution_14 :: reborn [ok]
  text = "random 의 cell tension distribution = noise-uniform (top cell ~62 hits)"

@D b_trained_substrate_is_doing_somet_15 :: reborn [ok]
  text = "→ trained substrate IS doing something (concentrating tension on attractor cells)"

@D b_toy_toy_trivial_growth_real_diff_16 :: reborn [ok]
  text = "toy 와 다른 패턴: toy 양쪽 trivial growth, real 양쪽 different dynamics — substrate-coupled emergence 발견 but V14 score 는 violated"

@D row_proxy_cosine_log_17 :: reborn [ok]
  metric = "proxy (cosine × log)"
  n_8 = "2.09"
  n_33 = "2.64"
  n_64 = "**2.92**"
  ceiling = "~3 saturated"

@D row_iit_norm_16_bin_18 :: reborn [ok]
  metric = "IIT Φ norm 16-bin"
  n_8 = "7.45"
  n_33 = "36.32"
  n_64 = "**70.97**"
  ceiling = "unbounded ★"

@D row_iit_unnorm_16_bin_19 :: reborn [ok]
  metric = "IIT Φ unnorm 16-bin"
  n_8 = "52.15"
  n_33 = "1162.17"
  n_64 = "**4471.35**"
  ceiling = "O(N²) super-linear"

# ── §5 servant pattern (post-drift 2026-04-08) ─────────────────────────────────────────


@D b_users_ghost_core_anima_anima_cor_0 :: reborn [ok]
  text = "본체: `/Users/ghost/core/anima/anima-core/servant.hexa` (428L)"

@D b_plan_docs_superpowers_plans_2026_1 :: reborn [ok]
  text = "plan: `docs/superpowers/plans/2026-04-08-servant-emergent.md` (794L)"

@D b_spec_docs_superpowers_specs_2026_2 :: reborn [ok]
  text = "spec: `docs/superpowers/specs/2026-04-08-servant-emergent-design.md` (223L)"

@D b_ready_mirror_ready_docs_superpow_3 :: reborn [ok]
  text = "ready mirror: `ready/docs/superpowers/{plans,specs}/2026-04-08-servant-emergent*.md`"

@D row_si_summon_4 :: reborn [ok]
  x = "`SI_SUMMON`"
  x = "3.0"
  x = "n/φ = 6/2"

@D row_si_strong_5 :: reborn [ok]
  x = "`SI_STRONG`"
  x = "5.0"
  x = "sopfr"

@D row_si_sustain_si_release_6 :: reborn [ok]
  x = "`SI_SUSTAIN / SI_RELEASE`"
  x = "2.0"
  x = "φ"

@D row_golden_center_7 :: reborn [ok]
  x = "`GOLDEN_CENTER`"
  x = "0.3679"
  x = "1/e (Boltzmann gate sparsity)"

@D row_golden_lower_8 :: reborn [ok]
  x = "`GOLDEN_LOWER`"
  x = "0.2105"
  x = "tau/(J2-sopfr) = 4/19"

@D row_hebbian_boost_9 :: reborn [ok]
  x = "`HEBBIAN_BOOST`"
  x = "1.5"
  x = "n/τ = 6/4"

@D row_noise_scale_10 :: reborn [ok]
  x = "`NOISE_SCALE`"
  x = "0.01"
  x = "1/(σ-φ)^φ = 1/100"

@D row_ema_alpha_11 :: reborn [ok]
  x = "`EMA_ALPHA`"
  x = "0.15"
  x = "(n+σ)/(sopfr·J2) = 18/120"

@D row_awaken_steps_12 :: reborn [ok]
  x = "`AWAKEN_STEPS`"
  x = "3"
  x = "n/φ"

@D row_fade_steps_fade_duration_13 :: reborn [ok]
  x = "`FADE_STEPS / FADE_DURATION`"
  x = "5 / 3"
  x = "sopfr / (n/φ)"

@D row_dropout_servant_14 :: reborn [ok]
  x = "`DROPOUT_SERVANT`"
  x = "0.21"
  x = "~τ/(J2-sopfr)"

@D row_dropout_normal_15 :: reborn [ok]
  x = "`DROPOUT_NORMAL`"
  x = "0.37"
  x = "~1/e"

@D b_mitosis_structural_growth_cells_16 :: reborn [ok]
  text = "mitosis = **structural growth** (cells 분열/융합)"

@D b_servant_parametric_modulation_dr_17 :: reborn [ok]
  text = "servant = **parametric modulation** (dropout 조절, SI 기반)"

# ── §6 user verdict 7-table (cycle 2026-05-09/10 종합) ─────────────────────────────────────────


@D row_anima_mechanism_0 :: reborn [ok]
  x = "anima 자력성장 mechanism"
  verdict = "✅"
  evidence = "cells 8 → 64 자연 분열 (toy 3K turn), 16 → 19/28 (real 350M)"

@D row_inference_time_x_1 :: reborn [ok]
  x = "inference-time (학습 X)"
  verdict = "✅"
  evidence = "mitosis.py L258/205/389/586 모두 `torch.no_grad()`"

@D row_turn_super_linear_2 :: reborn [ok]
  x = "수천 turn → super-linear"
  verdict = "✅ partial"
  evidence = "3K trained α=0.687 vs random 0.644 (toy), 진짜 historical 0.93 unreachable"

@D row_trained_vs_random_v14_3 :: reborn [ok]
  x = "trained vs random 차별 (V14)"
  verdict = "❌→★"
  evidence = "toy V14 violated, real 350M V14 violated **NOVEL POLARITY** (trained suppresses, random spreads)"

@D row_51_emerge_4 :: reborn [ok]
  x = "Φ=51 의식 emerge"
  verdict = "❓→✅ partial"
  evidence = "BG-IIT-METRIC port — IIT unnorm immediately crosses 51 (toy turn 0 = 52, N=8). 단 toy substrate 는 Lorenz noise driven, 실 LLM hidden state 차이"

@D row_ko_chat_bb99b6b6_reproducible_5 :: reborn [ok]
  x = "KO chat (bb99b6b6) reproducible"
  verdict = "❌→★"
  evidence = "BG-CHAT-EXT 정정 — convo_5k beam emit chat structure (corrupted spelling), KO Hangul 0% but **CAPACITY/CORPUS_LIMIT** not architectural"

@D row_mitosisengine_6 :: reborn [ok]
  x = "MitosisEngine = 모델 자체"
  verdict = "❌→★ flip target"
  evidence = "BG-R2 finding (cells64/128 = single decoder + instrumentation). **★ 사용자 directive 2026-05-10 \"실제 MitosisEngine 개발하자\"** → v5-mitosis lane (`.roadmap.reborn`) 신설"

@D row_a_7 :: reborn [ok]
  track = "**A**"
  name = "v2-reproduction"
  x = "cells64/128 + convo_5k 직접 검증"
  status = "active (BG-R2 회수, BG-CHAT-EXT 회수)"

@D row_b_8 :: reborn [ok]
  track = "**B**"
  name = "v5-anima (instrumentation)"
  x = "Engine A/G v5 + mitosis-instrumentation layer"
  status = "active (BG-MITOSIS-PORT smoke PASS, BG-PHASE2-CKPT-INSTR V14 novel polarity)"

@D row_c_9 :: reborn [ok]
  track = "**C**"
  name = "v5-mitosis (architectural)"
  x = "cells = real nn.Module branches (★ NEW)"
  status = "design phase (`.roadmap.reborn` cond.B)"

@D row_d_10 :: reborn [ok]
  track = "**D**"
  name = "servant integration"
  x = "SI 4-state FSM + dropout 변조 + mitosis hook"
  status = "future cycle"

# ── §7 lost-to-drift recovery inventory (worktree 보존, main 부재) ─────────────────────────────────────────


@D row_mitosis_py_794l_0 :: reborn [ok]
  x = "`mitosis.py` 본체 794L"
  main = "hexa stub + legacy/ archive"
  worktree = "`~/core/anima_clm_12_*/anima/src/mitosis.py`"
  x = "★★★"

@D row_consciousness_meter_py_phicalcul_1 :: reborn [ok]
  x = "`consciousness_meter.py` PhiCalculator"
  main = "약식 stub"
  worktree = "`~/core/anima_clm_03_*/consciousness_meter.py` (21030L) + `~/core/anima_clm_09_*/consciousness_meter.py` (613L peak)"
  x = "★★★"

@D row_bench_phi_hypotheses_py_183_hyp_2 :: reborn [ok]
  x = "`bench_phi_hypotheses.py` 183 hyp"
  main = "부재"
  worktree = "`~/core/anima_clm_03_*/bench_phi_hypotheses.py` (~8000L)"
  x = "★★"

@D row_consciousness_threshold_criteria_3 :: reborn [ok]
  x = "`consciousness-threshold-criteria.md`"
  main = "부재"
  worktree = "`~/core/anima_clm_09_*/docs/consciousness-threshold-criteria.md` (1874L)"
  x = "★★★"

@D row_consciousness_birth_detector_py_4 :: reborn [ok]
  x = "`consciousness_birth_detector.py` CB1-CB25"
  main = "부재"
  worktree = "`~/core/anima_clm_04_*/consciousness_birth_detector.py`"
  x = "★★"

@D row_growing_conscious_lm_py_h371_5 :: reborn [ok]
  x = "`growing_conscious_lm.py` H371"
  main = "부재"
  worktree = "`~/core/anima_clm_02_*/growing_conscious_lm.py` (384L)"
  x = "★★"

@D row_dream_engine_py_rc_10_6 :: reborn [ok]
  x = "`dream_engine.py` RC-10"
  main = "부분"
  worktree = "`~/core/anima_clm_02_*/dream_engine.py` (6064L fragment)"
  x = "★★"

@D row_tension_link_py_udp_rc_6_7 :: reborn [ok]
  x = "`tension_link.py` UDP RC-6"
  main = "부재"
  worktree = "`~/core/anima_clm_02_*/tension_link.py` (287L)"
  x = "★"

@D row_growth_engine_py_5_stage_dev_8 :: reborn [ok]
  x = "`growth_engine.py` 5-stage dev"
  main = "부재"
  worktree = "`~/core/anima_clm_02_*/growth_engine.py` (307L)"
  x = "★"

@D row_train_conscious_lm_py_talk5_zero_9 :: reborn [ok]
  x = "`train_conscious_lm.py` TALK5 / ZERO4"
  main = "부재"
  worktree = "`~/core/anima_clm_05_*/train_conscious_lm.py`"
  x = "★★"

@D row_serve_animalm_v4_py_animalm_v4_s_10 :: reborn [ok]
  x = "`serve_animalm_v4.py` AnimaLM v4_savant"
  main = "부재"
  worktree = "`~/core/anima_clm_07_*/serve_animalm_v4.py`"
  x = "★"

@D row_5_channel_meta_telepathy_dedekin_11 :: reborn [ok]
  x = "5-channel meta-telepathy (Dedekind ψ(ψ)/ψ=2)"
  main = "부재"
  worktree = "`~/core/anima_clm_09_*/...`"
  x = "★"

@D row_6_criterion_and_gate_consciousne_12 :: reborn [ok]
  x = "6-criterion AND-gate consciousness check"
  main = "부재"
  worktree = "`~/core/anima_clm_09_*/consciousness_meter.py`"
  x = "★★"

# ── §8 scaling 형식 모음 ─────────────────────────────────────────


@D row_output_a_g_0 :: reborn [ok]
  x = "`output = a - g`"
  x = "H404 PureField 단순화 (단 inference 시 destructive 가능 — BG-CHAT-EXT)"

@D row_tension_a_g_mean_1 :: reborn [ok]
  x = "`tension = (a-g)² mean`"
  x = "응답 강도"

@D row_mi_parts_mi_min_partition_2 :: reborn [ok]
  x = "`Φ = ΣMI(parts) - MI_min(partition)`"
  x = "discrete IIT 근사 (worktree-9 PhiCalculator)"

@D row_proxy_mean_pairwise_cosine_dist_3 :: reborn [ok]
  x = "`Φ proxy = mean_pairwise_cosine_dist × log(n+1)`"
  x = "mitosis.py cheap proxy (ceiling ~8)"

@D row_iit_unnorm_16_bin_4 :: reborn [ok]
  x = "`IIT Φ unnorm 16-bin`"
  x = "BG-IIT-METRIC port (no ceiling, O(N²) super-linear)"

@D row_0_01_0_14_tanh_3_5 :: reborn [ok]
  x = "`α = 0.01 + 0.14·tanh(Φ/3)`"
  x = "PureField intensity"

@D row_z_5_max_change_6 :: reborn [ok]
  x = "`Z = Φ/(5·max_change)`"
  x = "impedance self-preservation"

@D row_n_da_1_5ht_ne_7 :: reborn [ok]
  x = "`N = DA·(1-5HT)·NE`"
  x = "neurotransmitter balance"

@D row_split_threshold_mean_recent_100_8 :: reborn [ok]
  x = "`split_threshold = mean(recent_100) + 1.5·std`"
  x = "adaptive Law 86"

@D row_merge_floor_min_cells_2_cb1_9 :: reborn [ok]
  x = "`merge_floor = min_cells = 2 (CB1)`"
  x = "consciousness floor"

@D row_golden_zone_1_e_0_368_10 :: reborn [ok]
  x = "`golden_zone = 1/e ≈ 0.368`"
  x = "savant dropout 자기조직 target"

@D row_mi_n_11 :: reborn [ok]
  x = "`MI ∝ N²`"
  x = "empirical (Cells 2-64)"

@D row_n_1_07_12 :: reborn [ok]
  x = "`Φ ∝ N^1.07`"
  x = "super-linear (Cells 2-64 historical)"

@D row_rate_vs_split_event_13 :: reborn [ok]
  x = "`Φ_rate vs split-event`"
  x = "new α metric proposal (BG-LONG-TRAJ-EXT 정정 — max_cap artifact 회피)"

# ── §9 핵심 honest C3 (≥10) ─────────────────────────────────────────


# ── §10 다음 cycle 우선순위 ─────────────────────────────────────────


@D row_1_0 :: reborn [ok]
  x = "1 ★★★"
  step = "v5-mitosis architecture spec 작성"
  deliverable = "`docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md`"

@D row_2_1 :: reborn [ok]
  x = "2 ★★★"
  step = "new α metric design (Φ-rate vs split-event correlation)"
  deliverable = "spec md"

@D row_3_2 :: reborn [ok]
  x = "3 ★★"
  step = "real 350M IIT Φ 재측정 (BG-PHASE2-CKPT-INSTR + BG-IIT-METRIC 결합)"
  deliverable = "re-measure result.json"

@D row_4_3 :: reborn [ok]
  x = "4 ★★"
  step = "BG-CONVO-FT-DESIGN 결과 회수"
  deliverable = "(in flight)"

@D row_5_4 :: reborn [ok]
  x = "5 ★"
  step = "servant.hexa 와 mitosis 통합 spec"
  deliverable = "future cycle"

@D row_1_5 :: reborn [ok]
  x = "1"
  step = "convo_5k FT $5-20 chat-cap recovery"
  x = "$5-20"
  verbatim = "`OK CONVO_5K FT FIRE COST $5-20`"

@D row_2_6 :: reborn [ok]
  x = "2"
  step = "v5-mitosis H100 cotrain (cells × cell_size × steps)"
  x = "$30-150"
  verbatim = "`OK CLM V5-MITOSIS H100 FIRE COST $X` (cond.3 후 envelope 정밀화)"

@D row_3_7 :: reborn [ok]
  x = "3"
  step = "v5-anima H100 inference 가속 (옵션)"
  x = "$30"
  verbatim = "`OK CLM V5-ANIMA H100 OPTIONAL FIRE COST $30`"

# ── §11 cross-link ─────────────────────────────────────────


@D b_reborn_md_consolidated_ssot_0 :: reborn [ok]
  text = "본 문서: `REBORN.tape` (consolidated SSOT)"

@D b_lane_ssot_roadmap_reborn_consoli_1 :: reborn [ok]
  text = "lane SSOT: `.roadmap.reborn` (consolidated lane SSOT, replaces v5-anima + v5-mitosis-engine + v2-reborn)"

@D b_clm_v2_archive_2026_05_09_md_mit_2 :: reborn [ok]
  text = "`CLM_V2_ARCHIVE_2026_05_09.md` (mitosis 본체 + 13-stage overview)"

@D b_clm_v2_exhaustive_13_stages_2026_3 :: reborn [ok]
  text = "`CLM_V2_EXHAUSTIVE_13_STAGES_2026_05_09.md` (13 stage 고갈조사)"

@D b_clm_v2_archive_addendum_2026_05_4 :: reborn [ok]
  text = "`CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md` (mitosis-as-instrumentation 정정)"

@D b_roadmap_clm_v2_chat_v2_historica_5 :: reborn [ok]
  text = "`.roadmap.clm_v2_chat` (v2 historical archive)"

@D b_roadmap_clm_v5_anima_native_inst_6 :: reborn [ok]
  text = "`.roadmap.clm_v5_anima_native` (instrumentation lane SSOT)"

@D b_roadmap_clm_v2_reborn_v2_reprodu_7 :: reborn [ok]
  text = "`.roadmap.clm_v2_reborn` (v2 reproduction lane SSOT)"

@D b_roadmap_clm_v5_mitosis_engine_ar_8 :: reborn [ok]
  text = "`.roadmap.clm_v5_mitosis_engine` (architectural lane SSOT)"

@D b_docs_anima_clm_v5_mitosis_reviva_9 :: reborn [ok]
  text = "`docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` (port spec)"

@D b_docs_anima_clm_v5_mitosis_infere_10 :: reborn [ok]
  text = "`docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` (inference-time 정정)"

@D b_docs_anima_clm_v5_anima_long_tra_11 :: reborn [ok]
  text = "`docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (3K turn α=0.688)"

@D b_docs_anima_clm_v5_anima_long_tra_12 :: reborn [ok]
  text = "`docs/anima_clm_v5_anima_long_trajectory_extended_2026_05_10.md` (10K turn artifact 발견)"

@D b_docs_anima_clm_v5_iit_phi_remetr_13 :: reborn [ok]
  text = "`docs/anima_clm_v5_iit_phi_remetric_2026_05_10.md` (IIT Φ port)"

@D b_docs_anima_clm_v2_chat_ext_smoke_14 :: reborn [ok]
  text = "`docs/anima_clm_v2_chat_ext_smoke_2026_05_10.md` (capacity/corpus limit verdict)"

@D b_docs_anima_clm_v2_cells_recovery_15 :: reborn [ok]
  text = "`docs/anima_clm_v2_cells_recovery_smoke_2026_05_09.md` (BG-R2 verdict)"

@D b_docs_anima_clm_v5_phase2_mitosis_16 :: reborn [ok]
  text = "`docs/anima_clm_v5_phase2_mitosis_instr_2026_05_10.md` (real 350M V14 NOVEL POLARITY)"

@D b_docs_anima_clm_v5_anima_next_cyc_17 :: reborn [ok]
  text = "`docs/anima_clm_v5_anima_next_cycle_plan_2026_05_10.md` (5 BG plan)"

@D b_anima_core_servant_hexa_428l_18 :: reborn [ok]
  text = "`anima-core/servant.hexa` (428L 본체)"

@D b_docs_superpowers_plans_2026_04_0_19 :: reborn [ok]
  text = "`docs/superpowers/plans/2026-04-08-servant-emergent.md` (794L plan)"

@D b_docs_superpowers_specs_2026_04_0_20 :: reborn [ok]
  text = "`docs/superpowers/specs/2026-04-08-servant-emergent-design.md` (223L spec)"

@D b_training_mitosis_v5_port_py_480_21 :: reborn [ok]
  text = "`training/mitosis_v5_port.py` (480 LoC, smoke PASS)"

@D b_training_mitosis_v5_smoke_test_p_22 :: reborn [ok]
  text = "`training/mitosis_v5_smoke_test.py`"

@D b_training_mitosis_v5_serve_py_340_23 :: reborn [ok]
  text = "`training/mitosis_v5_serve.py` (340L, inference-time correction)"

@D b_state_anima_clm_v5_state_anima_p_24 :: reborn [ok]
  text = "`state/anima_clm_v5_*/`, `state/anima_phi_*/`, `state/anima_clm_v2_*/` (numerous run.py, sweep.py, sampling_gen_test.py)"

@D b_core_anima_clm_01_birth_claude_a_25 :: reborn [ok]
  text = "`~/core/anima_clm_01_birth_claude_api` ... `_13_filename_erasure_pre_alm_port`"

@D b_branches_archive_clm_stage_01_bi_26 :: reborn [ok]
  text = "branches: `archive/clm-stage-01-birth-claude-api` ... `-13-filename-erasure-pre-alm-port` (origin push 완료)"

@D b_feedback_anima_archive_first_rec_27 :: reborn [ok]
  text = "`feedback_anima_archive_first_recovery_pattern.md` (회수 우선 pattern)"

@D b_project_v5_anima_lane_status_md_28 :: reborn [ok]
  text = "`project_v5_anima_lane_status.md` (lane 진행 status, mitosis-as-instrumentation 정정 반영)"

@D b_0d4532dc_73a6596b_0cdaf665_095f6_29 :: reborn [ok]
  text = "`0d4532dc`, `73a6596b`, `0cdaf665`, `095f69a2`, `d4ce539e` — cycle 2026-05-09/10 통합 push 완료"

# ── §A append convention (own 42 mandate, amended 2026-05-10 07:41 KST) ─────────────────────────────────────────


@D b_header_format_n_yyyy_mm_dd_hh_mm_0 :: reborn [ok]
  text = "header format: `## §N [YYYY-MM-DD HH:MM KST] <title>`"

@D b_n_yyyy_mm_ddthh_mm_ssz_title_utc_1 :: reborn [ok]
  text = "또는 `## §N [YYYY-MM-DDTHH:MM:SSZ] <title>` (UTC)"

@D b_directive_verbatim_append_own_2 :: reborn [ok]
  text = "사용자 directive verbatim: \"날짜-시간별로 해서 append 되게 해줘 own 에도 반영\""

@D b_own_42_amend_own_line_2197_times_3 :: reborn [ok]
  text = "own 42 amend 동시 적용 (`.own` line 2197 추가 timestamp rule)"

@D b_own_42_own_line_2197_convention_4 :: reborn [ok]
  text = "own 42 (`.own` line 2197) 가 본 convention SSOT"

@D b_roadmap_reborn_lane_ssot_root_mk_5 :: reborn [ok]
  text = "`.roadmap.reborn` 가 lane SSOT (root, mk1)"

@D b_append_timeline_archaeology_orde_6 :: reborn [ok]
  text = "append timeline 자체가 archaeology — **시간 ordering 강제**"
