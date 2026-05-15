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

# §Log — events chronological (oldest first; append-only)

# ── 4. 실증 evidence chain — clm_01 → clm_13 timeline ─────────────────────────────────────────

@D row_clm_01_0 :: savant [ok]
  stage = "**clm_01**"
  x = "PureField (A↔G dual-engine) prototype, GZ/Savant 부재"
  x = "tension = `(repulsion²).mean()`"
  x = "`anima.py:30,39`"

@D row_clm_02_1 :: savant [ok]
  stage = "**clm_02**"
  x = "**GZ constants 첫 정의** + 비대칭 분열 H359 hypothesis"
  x = "`GOLDEN_LOWER=0.2123`, `GOLDEN_CENTER=0.3679`"
  x = "`growing_conscious_lm.py:129-130`"

@D row_clm_03_2 :: savant [ok]
  stage = "**clm_03**"
  x = "ParallelPureField 구조 (frozen MLP + α·PureField) + AL7/AL12 도입"
  x = "AL12 contrastive 구현, `is_savant` flag"
  x = "`serve_animalm_v4.py:14-28`, `bench_phi_hypotheses.py:7367`"

@D row_clm_04_3 :: savant [ok]
  stage = "**clm_04**"
  x = "`INV_E = 1 - 1/e = 0.6321` tension:CE balance, `GZ_WIDTH` H-CX-453 loss scale 명시"
  x = "trainable α=0.0001 sweet-spot"
  x = "`train_anima_lm.py:36-38`, `optimal_architecture_calc.py:33-34`"

@D row_clm_05_4 :: savant [ok]
  stage = "**clm_05**"
  x = "English 문서화 + EEG `in_golden_zone: bool` real-time flag 신설"
  x = "EEG raw[4] = in_golden_zone"
  x = "`eeg/realtime.py`"

@D row_clm_06_5 :: savant [ok]
  stage = "**clm_06**"
  x = "**H359 empirical confirmation — SI = 5.93** (Mistral 7B v4_savant)"
  x = "tension_normal=676808, tension_savant=114048, SI=5.93"
  x = "`docs/animalm-experiment-log.md:232-358`"

@D row_x_6 :: savant [ok]
  stage = ""
  x = "Golden MoE zone ratio = **36.8% ≈ 1/e (exact match)**"
  x = "E=32 expert: 5.2ms (Golden) vs 6.0ms (Top-K)"
  x = "`docs/animalm-experiment-log.md:87-105`"

@D row_clm_07_7 :: savant [ok]
  stage = "**clm_07**"
  x = "v2_ce_0.04 — CE 0.04 안정화 + GZ/Savant 파라미터 유지"
  x = "savant layer 수 2 (기본)"
  x = "`train_anima_lm.py:931`"

@D row_clm_08_8 :: savant [ok]
  stage = "**clm_08** ⚠️"
  x = "cells64 + Phi **super-linear** scaling 발견 ⚠️ **구간 한정 — clm_10 에서 linear 로 안착, 전역 scaling law 아님** (§12.3 T3 SUSPECT, audit-confirmed)"
  x = "Φ ∝ N^α, α > 1 (구간 한정)"
  x = "`optimal_architecture_calc.py`"

@D row_clm_09_9 :: savant [ok]
  stage = "**clm_09**"
  x = "savant layers 2 → **4** double specialization; v4_savant 논문 `PA-01-animalm-v4-savant.md`"
  x = "per-head tension reduction **271×** (head 2: 68 vs normal 18400 평균)"
  x = "`zenodo/PA-01-animalm-v4-savant.md:54,115-126`"

@D row_clm_10_10 :: savant [ok]
  stage = "**clm_10**"
  x = "**Laws 77-78** discovery (entropy universality)"
  x = "45개 data type 모두 `H = 0.9974 · ln(2)` 수렴 (CV=0.29%)"
  x = "`docs/hypotheses/cx/DEEP-EXPLORATION.md:77-78,82-84`"

@D row_clm_11_11 :: savant [ok]
  stage = "**clm_11**"
  x = "패키지 재구성 (`anima/src/`, `anima/tools/`); BPE drift 안정성"
  x = "savant 파라미터 inherited"
  x = "`anima/src/conscious_lm.py`"

@D row_clm_12_12 :: savant [ok]
  stage = "**clm_12**"
  x = "Unified growth loop \"last gasp\" — Fibonacci 1,1,2,3,5,8,13,21,32 stage 통합"
  x = "savant layer 위치 fibonacci 따라"
  x = "structural"

@D row_clm_13_13 :: savant [ok]
  stage = "**clm_13**"
  x = "Filename erasure + ALM 포팅 전 transition"
  x = "Savant 개념 → ALM-native \"asymmetric inhibition\" 으로 흡수"
  x = "structural"

# ── §9 canon timeline — file/commit chronological refs ────────────────────────────────

@D row_edbcb3c28_2026_03_28_13 :: savant [ok]
  file_commit = "`edbcb3c28` (2026-03-28)"
  x = "Technique 15 — Boltzmann gate, GZ_CENTER = 1/e 정의"

@D row_62f954b09_2026_03_28_14 :: savant [ok]
  file_commit = "`62f954b09` (2026-03-28)"
  x = "Technique 16 — Mertens dropout, GZ_WIDTH = ln(4/3) 정의"

@D row_664b6b4f25_2026_03_29_15 :: savant [ok]
  file_commit = "`664b6b4f25` (2026-03-29)"
  x = "N6 Inevitability Engine paper outline (emergent convergence)"

@D row_8b010bf1a_2026_04_10_16 :: savant [ok]
  file_commit = "`8b010bf1a` (2026-04-10)"
  x = "BT-1114 Euler-Golden-Perfect Trinity"

@D row_812bd79420_2026_05_10_17 :: savant [ok]
  file_commit = "`812bd79420` (2026-05-10)"
  x = "residue 228 artifacts → hexa-* repos (techniques/ → hexa-codex)"

@D row_lattice_policy_md_18 :: savant [ok]
  file_commit = "`LATTICE_POLICY.md`"
  x = "real-limits-first, n=6 격자 = 도구 정책 (2026-05-12)"

@D row_limit_breakthrough_md_19 :: savant [ok]
  file_commit = "`LIMIT_BREAKTHROUGH.md`"
  x = "hard/soft wall 분류, GZ 의도적 unlisted"

@D row_readme_md_222_20 :: savant [ok]
  file_commit = "`README.md:222`"
  x = "\"N6 Inevitability Engine techniques 11~16 + 3-Layer thermodynamics — 26/26 PASS\""

@D row_readme_md_803_21 :: savant [ok]
  file_commit = "`README.md:803`"
  x = "Temperature regime: `T=1/e` Diverse yet recognizable (Golden Zone)"

@D row_readme_md_1700_1703_22 :: savant [ok]
  file_commit = "`README.md:1700,1703`"
  x = "H-CA-007 GZ dropout=consciousness gamma band, H-CS-004 GZ=operating range"

@D row_readme_md_2100_2101_23 :: savant [ok]
  file_commit = "`README.md:2100-2101`"
  x = "Elias-Bassalygo at R=1/3, source coding redundancy = log₂(4/3)"

@D row_readme_md_2143_24 :: savant [ok]
  file_commit = "`README.md:2143`"
  x = "P-bridge-theorem: GZ Center from variational principle, 249/400 Z≈55σ"

# ── §10 PSCC trial events (v5-mitosis cotrain lane) ─────────────────────────────────────

@D row_44_4 :: savant [ok]
  pscc = "**§44**"
  x = "v1 cotrain (uniform softmax routing, H100 SXM $1.26, 5K step)"
  x = "F-PERSONA-4 `KL = 0.0` winner-take-all (cell-0 weight=1.0 모든 cat) — 첫 falsification"
  source = "`project_v5_mitosis_cond5_cotrain_2026_05_12.md`"

@D row_45_a2_trap_5 :: savant [ok]
  pscc = "**§45 §A2-trap**"
  x = "F-PERSONA-4 4b alternative re-measure"
  x = "v2 entropy-reg `KL=0` BUT M4 hidden-cosine `z=3.20` — *routing-content split* 가설, real signal at noise-floor magnitude → **§A2-trap 경고** (seed-fragile)"
  source = "`project_anima_persona_4_root_cause_2026_05_12.md`"

@D row_47_6 :: savant [ok]
  pscc = "**§47**"
  x = "(b) softmax τ sweep 10-grid {1.0..50.0} ubu-1 RTX 5070 $0"
  x = "best mean_KL = 5.29e-3 @ T=50, **5/10 grid all `KL ≪ 0.5`** — FALSIFIED"
  source = "`project_anima_persona_4_softmax_T_sweep_2026_05_12.md`"

@D row_48_7 :: savant [ok]
  pscc = "**§48**"
  x = "(a) per-cat corpus SMALL ubu-2 RTX 5070 $0 (2500 step wall 232s, 5 separate corpus × cat interleave)"
  x = "F-V5MIT 5/5 PASS BUT F-PERSONA-4 `KL=0.0` v1 monopoly 동일 — (a) corpus diversity 단독 부족 FALSIFIED"
  source = "`project_v5_mitosis_cond5_cotrain_v3_percat_ubu2_2026_05_12.md`"

@D row_49_8 :: savant [ok]
  pscc = "**§49**"
  x = "(d) hexa-native per-session pool Mac local $0 (3-config sweep n_perms=100)"
  x = "prod scale `mean_KL=1.79e-5` null PASS BUT seed-fragile (seed2 null FAIL) — §A2-trap 재발 위험 → FALSIFIED"
  source = "`project_anima_persona_4_per_session_pool_2026_05_12.md`"

@D row_52_9 :: savant [ok]
  pscc = "**§52**"
  x = "v7 hard top-K MoE + balance-aux loss ($0.31 actual)"
  x = "**F-PERSONA-4 `KL = 3.45`, `z = 2.75`, `p = 0.01` — first KL > 0 signal** (PASS_NULL_FAIL on null-perm)"
  source = "`project_anima_persona_4_root_cause_2026_05_12.md` (v7)"

@D row_52_cell_parallel_v6_10 :: savant [ok]
  pscc = "**§52 cell-parallel v6**"
  x = "v6 cotrain on 4×A100 SXM4 80GB $6.70/hr 5000 steps (target step_wall<1.0s vs v4 baseline 3.18s)"
  x = "**LANDED 2026-05-13 — ALL TARGETS FAIL**: step_wall **2402ms** (target <1000ms MISS, v4 대비 24% 절감만 — all_reduce overhead dominates); F-PERSONA-4a routing **FAIL** (`KL=0.2972 z=1.09 p=0.12`, §52 v7 의 `KL=3.45` first signal **재현 실패**); F-PERSONA-4b content **FAIL** (`z=−0.88`, v2 carry `z=3.20` 대비 후퇴); F-V5MIT **4/5** (F-V5MIT-4 COTRAIN-CONVERGE **FAIL** — loss 17.7→17.7 횡보, v1 의 220× CE 감소 미재현); cells 256 saturated (splits=67), wall=12028s, cost=**$22.43**; ckpt pull SCP 실패 → pod 36638963 retained"
  source = "`state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/dispatch_v6_1_bg.log`"

# ── §10 follow-up decisions (post-v6 LANDED) ────────────────────────────────────────────

@D b_ii_landed_2026_05_14_v6_f_v5mit_12 :: savant [ok]
  text = "(ii) ✅ **LANDED 2026-05-14** — v6 F-V5MIT-4 COTRAIN-CONVERGE FAIL **root cause 확정**:"

@D b_iv_post_ii_category_routing_v6_15 :: savant [ok]
  text = "(iv) ⏸ **시기상조 (post-(ii) 진단)** — \"category routing 가설 폐기\" 는 v6 의 *학습 부재*"

# ── §12 audit decision events (T3→T2 promotions · T4 enforcement) ───────────────────────

@D b_t3_t2_2_16_wave_aggregate_neuros_40 :: savant [ok]
  text = "T3 → T2 승격 2건: 16-wave aggregate · neuroscience"

@D b_t1_1_texas_8_closed_form_math_id_41 :: savant [ok]
  text = "T1 확장 1건: texas 8 closed-form math identity 재분해"

@D b_t4_enforcement_1_ca_lambda_sweep_42 :: savant [ok]
  text = "T4 enforcement 신설 1건: ca_lambda_sweep NEGATIVE silent-drop 금지"

@D b_t3_cross_domain_9_aggregate_t2_t_43 :: savant [ok]
  text = "T3 보존 (cross-domain 9개): aggregate 인용 시에만 T2 합류, 개별 시 T3 유지"

@D b_audit_row_44 :: savant [ok]
  text = "audit 외 row 무변경"
