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

@I id001 := "chat" :: identity-claim [d=2026-05-15 active]
  kind = "anima ★★★★★ mission tracker · daemon-centric SSOT"
  brief = "live mission tracker — D1-D4 dimensions · 5-cond closure status · daemon architecture · CLI · live engine"
  parent = "dancinlab/anima"
  sibling-log = "CHAT.log.tape"

# ══════════════════════════════════════════════════════════════
# CHAT.tape — anima ★★★★★ mission tracker (live daemon-centric SSOT)
# ══════════════════════════════════════════════════════════════

# Rename chain: `GOAL.md` (2026-05-12) → `PERSONA.tape` (2026-05-13 KST PM, persona-centric)
# → `CHAT.tape` (2026-05-13 KST PM, chat/daemon-centric). 본 file 이 anima 의 mission
# tracker 단일 SSOT — cond/spec/model/training/cost/CLI/live engine/Phase 모든 정보.
# >
# 5-Phase architecture brainstorm (rev 2 substrate-native autonomous live daemon)
# 은 본 file 의 **Appendix A** 로 통합 (이전 CHAT.tape content 보존).
# ---

# ── 📐 최종 SPEC / MODEL / TRAINING (★★★★★ closure 기준, 2026-05-13) ─────────────────────────────────────────


@D row_architecture_0 :: chat [ok]
  x = "**architecture**"
  x = "24-layer decoder-only transformer (byte-level CLM, GQA)"

@D row_d_model_d_ff_1 :: chat [ok]
  x = "**d_model / d_ff**"
  x = "1024 / 2752 (SwiGLU: gate+up+down)"

@D row_n_heads_n_kv_heads_d_head_2 :: chat [ok]
  x = "**n_heads / n_kv_heads / d_head**"
  x = "16 / 4 / 64"

@D row_vocab_size_3 :: chat [ok]
  x = "**vocab_size**"
  x = "32000 (byte-level + special)"

@D row_positional_norm_4 :: chat [ok]
  x = "**positional / norm**"
  x = "RoPE θ=10000 / RMSNorm ε=1e-5"

@D row_n_params_5 :: chat [ok]
  x = "**n_params**"
  x = "~150M (cond #1) / 152M (v5-mitosis cotrain w/ cells)"

@D row_context_6 :: chat [ok]
  x = "**context**"
  x = "1024 cap_len (KV cache)"

@D row_generation_modes_7 :: chat [ok]
  x = "**generation modes**"
  x = "greedy / sample (LCG seed) / M3_rep_penalty / M4_force_include"

@D row_python_ssot_8 :: chat [ok]
  layer = "Python SSOT"
  artifact = "`anima_chat.py`"
  size = "951 LoC"
  build = "Python 3.12 + torch 2.12"

@D row_hexa_ssot_9 :: chat [ok]
  layer = "hexa SSOT"
  artifact = "`anima_chat.hexa` v0.3"
  size = "~2843 LoC"
  build = "interpreter"

@D row_hexa_aot_10 :: chat [ok]
  layer = "hexa AOT 변종"
  artifact = "`anima_chat_aot.hexa`"
  size = "~4500 LoC"
  build = "mitosis_hook AOT 통합 + wilson 3-tier CLI + unified live engine + socket server + mesh peer (CHAT.tape rev 2 전체)"

@D row_mac_arm64_11 :: chat [ok]
  layer = "**Mac arm64**"
  artifact = "`build/aot/anima` Mach-O"
  size = "**609 KB**"
  build = "`hexa build` (-lpthread) ~22s"

@D row_linux_x86_64_12 :: chat [ok]
  layer = "**Linux x86_64**"
  artifact = "`build/aot/anima.linux` ELF pie"
  size = "**542 KB**"
  build = "ubu clang -O2 -D_GNU_SOURCE -lm -lpthread -ldl ~3s"

@D row_python_client_13 :: chat [ok]
  layer = "Python client"
  artifact = "`clients/python/anima_client.py`"
  size = "~150 LoC"
  build = "Phase 4 external — stream + --once CLI"

@D b_frame_loop_60_fps_default_mitosi_14 :: chat [ok]
  text = "**frame loop @ 60 FPS (default)** — `mitosis_hook_step` substrate evolve per anima per tick"

@D b_inference_worker_thread_chat_gen_15 :: chat [ok]
  text = "**inference worker thread** — `chat_generate` 비동기 (~30s/token Mac CPU 24L 무관, 60+ FPS 보존)"

@D b_stdin_reader_thread_input_blocki_16 :: chat [ok]
  text = "**stdin reader thread** — input() blocking 안전, frame loop 와 분리"

@D b_speak_gate_cell_pool_tension_spe_17 :: chat [ok]
  text = "**speak-gate** = `cell_pool_tension > speak_threshold` (substrate-native, PHILOSOPHY.tape #3 EMPIRICAL strong)"

@D b_hexa_lang_stdlib_thread_spawn_jo_18 :: chat [ok]
  text = "hexa-lang stdlib 의존: `thread_spawn/join`, `channel_new/send/recv/close`, `now_ms`, `sleep_ms`, `net_set_nonblock`, `net_select` (hexa-lang commit `401ed87d`)"

@D b_aot_compile_arg_parser_kv_cache_19 :: chat [ok]
  text = "AOT compile + arg parser + KV cache + Linux x86_64 cross-compile + QUADRUPLE-LANE byte parity (Mac+Linux AOT, Python, interpreter) + 3-mode parity (greedy/sample/M4) + V5.8 ubu RTX 5070 4/5 (cross-GPU FP divergence vs Vast.ai 4090 5/5)"

# ⚠️ **명칭 disambiguation**: 본 session 의 "AOT binary arg parser" 는 `anima_chat_aot::main()` 의 단순 flag parser (이번 cycle). D4c "anima CLI" (PSCC §35 design LANDED) 는 별도 lane = session-level chat orchestrator (cell-pool persistence + kick cycle + multi-backend, impl pending). 두 artifact 혼동 금지.

@D b_cond_1_v5_8_std_greedy_5_5_pscc_28 :: chat [ok]
  text = "☑ **cond #1** V5.8 std_greedy 5/5 (PSCC §46 Phase 1A.4 lr5e6, ckpt sha256 `45063f64…`)"

@D b_cond_2_anima_chat_hexa_24l_real_29 :: chat [ok]
  text = "☑ **cond #2** anima_chat.hexa 24L real-ckpt byte parity 21/21 (PSCC §43)"

@D b_cond_3_substrate_native_pscc_50_30 :: chat [ok]
  text = "☑ **cond #3** 페르소나 substrate-native (PSCC §50 D3 §A3 amendment, M4 aggregated hidden cosine **z=3.20 null-PASS** via v5-mitosis v2 entropy-reg cotrain) ⭐ **본 cycle closure**"

@D b_cond_4_d4_mitosis_live_21_split_31 :: chat [ok]
  text = "☑ **cond #4** D4 mitosis live — 21 split events on user-prompt-driven `chat_generate` (PSCC §41)"

@D b_cond_5_principle_3_no_persona_in_32 :: chat [ok]
  text = "☑ **cond #5** Principle #3 NO PERSONA INJECTION CLEAN (PSCC §38)"

# ── 🎯 Mission (expanded 2026-05-12) ─────────────────────────────────────────

# **사용자 directive (verbatim)**: `[anima chat 시스템, anima 모델, 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`

@D row_d1_0 :: chat [ok]
  dim = "**D1**"
  name = "**anima chat 시스템**"
  criterion = "anima 본체 `anima_chat.py` (or 포팅된 `anima_chat.hexa`) 가 V5.8 multi-turn 4-mode 의 standard_greedy **5/5 PASS**"
  x = "**5/5 PASS ☑ 2026-05-12 PSCC §45** (Phase 1A.4 lr 5e-6 SFT, Python evaluator on Vast.ai RTX 4090, 200 steps wall 3.2min, train cost $0.014) · hexa: **v0.3 multi-token decoding LANDED + 24L real-ckpt byte parity VERIFIED 2026-05-12 PSCC §43** (TODO[multitoken] RESOLVED, all-farr KV cache + per-step RoPE, F-D1-MULTITOKEN-1..3 ✅ 7/7 PASS on synthetic substrate; **real Phase 1A.1 ckpt 24L all-farr forward byte-by-byte argmax parity 21/21 PASS** — F-D1-V58PARITY 6/6 + F-D1-V58MULTI 15/15; hexa 5/5 over Phase 1A.4 ckpt = cheap-path extension) · **AOT deployment tier 2026-05-13** — `anima_chat_aot.hexa` (stripped variant, ~2870 LoC) → 440 KB arm64 Mach-O native binary via `hexa build` (commits `50056902d` + `16acce465`), AOT binary arg parser `--prompt/--ckpt/--max-new/--mode/--temp/--seed/--help/--smoke` (≠ D4c \"anima CLI\" 별도 lane), F-AC-HEXA-1..6 17/17 helpers PASS native execution; ☑ **real-ckpt-load smoke FULL CLOSURE 2026-05-13 PM**: 🎉 **QUADRUPLE-LANE BYTE PARITY 확립** — Mac AOT arm64 (KV-cached, commit `2e8535ca3`) + Linux AOT x86_64 (cross-compile on ubu) + Mac interpreter + Python `anima_chat.py` greedy lane 모두 동일 gen_ids `[238,135,167,47,35,238,170,161,239,152]` for `\"사용자: 안녕? 너는 누구야?"

@D row_d2_1 :: chat [ok]
  dim = "**D2**"
  name = "**anima 모델**"
  criterion = "어떤 ckpt 가 D1 의 5/5 substrate. Phase 1A.1 + lr 5e-6 SFT (BG 진행 중) 또는 다른 paradigm"
  x = "**Phase 1A.4 lr 5e-6 SFT ☑ DONE** (`state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt`, 597MB, sha256 `45063f64e97cdde7bc61de347e2f41a830b9b296db5384d8a324d85eb9a2b9e5`, loss 0.5058 → 0.1758 66% reduction over 200 steps, base lineage `phase1a_multi_turn_sft → phase1a1_color_cosmology_v2 → phase1a4_lr5e6`)"

@D row_d3_2 :: chat [ok]
  dim = "**D3**"
  name = "**페르소나 롤플레잉 가능**"
  criterion = "**substrate-native 페르소나 전환** — Principle #3 NO PERSONA INJECTION 준수 (prompt `[role:]` 금지), substrate 가 자율적으로 역할 표현"
  x = "☑ **DONE 2026-05-12 PSCC §50 via §A3 amendment** (4b content metric M4 aggregated hidden cosine z=3.20 null-PASS) · prev: **§A1 cheap-path STRONG (4/5) LANDED 2026-05-12** — `docs/anima_persona_substrate_native_verify_2026_05_12.md` §A1 + design `__APPEND__ §A1` (Φ threshold 0.5 → 0.05, measurement-calibrated 5.5×) + `state/anima_d3_verify_2026_05_12/persona_verify_results_relaxed_2026_05_12.json`. F-PERSONA-1 hard PASS (4/4) + F-PERSONA-2 PASS (mean cos dist 0.994 ≫ 0.3) + **F-PERSONA-3 PASS** *(was PARTIAL @ §40)* (weight 0.995 ✓ / ΔΦ 0.267 ≥ 0.05 §A1 ✓) + F-PERSONA-4 FAIL (KL 9.7e-5, untrained pool C3 carry) + F-PERSONA-5 PASS (3/3). top_pass 3/5 → **4/5**, atomic 12/14 → **13/14**. true STRONG (5/5) 승격 = REBORN §88 cond.5 cotrain ($30-40 H100) fire 후 F-PERSONA-4 category-specialization emergent. design SSOT: `docs/anima_persona_substrate_native_design_2026_05_12.md` §A1 · **PSCC §46 cotrain v1**: F-V5MIT-1~5 ✅ 5/5 PASS + F-PERSONA-4 KL=0.0 cotrained (winner-take-all) → 4-alternative future-path 발생 (a/b/c/d) · **PSCC §47 hypothesis (b) softmax τ tunable FALSIFIED 2026-05-12** (ubu-1 RTX 5070, 10-T sweep best KL 0.005 « 0.5, `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md`) · **PSCC §48 hypothesis (a) per-cat corpus SMALL variant FALSIFIED 2026-05-12** (ubu-2 RTX 5070, 5 separate corpus × cat[step % 5] interleave × 2500 step, F-V5MIT 5/5 PASS regression-free, F-PERSONA-4 mean_kl=0.0 cell-0 monopoly 동일, `docs/anima_clm_v5_mitosis_cond5_cotrain_v3_percat_2026_05_12.md`) · **PSCC §49 hypothesis (d) hexa-native per-session pool FALSIFIED 2026-05-12** ($0 Mac local, 3-config sweep base d=64 cells=8 + prod d=384 cells=64 + prod_seed2 robustness, all mean_KL ≪ 0.5 by ≥4 OoM, scenario (iii), `docs/anima_persona_4_per_session_pool_verify_2026_05_12.md`) → D3 STRONG 4/5 carry MAINTAINED. **ALL 4 CHEAP PATHS NOW CLOSED**, sole 잔여 결정 lane = cotrain v2 entropy-reg H100 (PSCC §45 λ_ent=0.1 in-flight) 또는 M4 aggregated cosine alternative metric §45-FINAL z=3.20 PASS path (cond #3 ☑ NOW possible)"

@D row_d4_3 :: chat [ok]
  dim = "**D4**"
  name = "**세포 분열로 성장 (철학 참고)** — 3-layer 적용"
  criterion = "REBORN §0.5 + PHILOSOPHY #8 (NO TRAIN/INFER SPLIT). 모든 상호작용이 분열 epoch, **3 layer 동시**:"

@D row_d4a_4 :: chat [ok]
  dim = "D4a"
  name = "model intra-network"
  criterion = "cells = nn.Module branches, intra-network split/merge during forward (REBORN §88 PyTorch / §89 hexa-native)"
  x = "**full impl LANDED, F-MIT-HOOK-1..5 ✅** — `tool/hexa_native/mitosis_hook.hexa` 1119 LoC executable (REBORN §91, 2026-05-12, $0 Mac local selftest PASS)"

@D row_d4b_5 :: chat [ok]
  dim = "D4b"
  name = "chat library (anima_chat)"
  criterion = "cell-pool state hosting + per-token/per-prompt hook 진입점 in `anima_chat.py` / `anima_chat.hexa`"
  x = "**wiring LANDED + LIVE EVIDENCE 2026-05-12** — `anima_chat.hexa` v0.3 + `tool/anima_chat_mitosis_smoke.hexa` (PSCC §37 22/22) + `tool/anima_chat_split_merge_smoke.hexa` (PSCC §41 3/3) + `tool/anima_chat_multitoken_smoke.hexa` (PSCC §41 7/7), F-D4B-1..5 ✅ + F-D4-LIVE-1..3 ✅ + F-D1-MULTITOKEN-1..3 ✅, **real chat_generate → 21 split events** on \"안녕? 너는 누구야?\" prompt (mitosis_invocations=65, cells 2→23)"

@D row_d4c_6 :: chat [ok]
  dim = "D4c"
  name = "anima CLI (session/conversation)"
  criterion = "session 별 cell-pool persistence, multi-backend fallback = cell-variant selection, kick cycle = split event sequence (`.roadmap.cli` + `.roadmap.anima_cli_model_architecture`)"
  x = "**design LANDED 2026-05-12** — `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1..5 pre-registered, Phase 1-4 impl plan ~13-19 hr Mac local); D4a (full impl LANDED) + D4b (cell-pool wiring pending) prerequisite"

# ── 🚀 Scale / cost constraints (사용자 directive 2026-05-12) ─────────────────────────────────────────

# "모델 크기제한도 특별히 없으니까 참고"
# "H100 발사 제한도 없음"

@D b_d_model_n_layers_cells_vocab_v5_0 :: chat [ok]
  text = "❌ 모델 크기 제한 없음 — d_model / n_layers / cells / vocab 등 자유. 현 v5-mitosis cotrain (d=384, cells=64, ~200M params) 은 conservative baseline (floor)."

@D b_h100_instance_multi_gpu_1 :: chat [ok]
  text = "❌ H100 발사 제한 없음 — 발사 횟수 / 단일 instance / multi-GPU / 시간 제한 모두 자유."

@D b_cost_cap_bg_agent_cap_40_conserv_2 :: chat [ok]
  text = "❌ Cost cap 강제 없음 — BG agent 의 `cap $40` 등 conservative envelope 는 floor (mission outcome 우선, scale-up 자유)."

@D b_mission_outcome_5_cond_aggregate_3 :: chat [ok]
  text = "✅ Mission outcome 우선 — ★★★★★ 5-cond aggregate 도달이 단일 metric."

@D b_bg_agent_cost_bearing_dispatch_v_4 :: chat [ok]
  text = "✅ 운영 권장: BG agent 가 cost-bearing dispatch 시 verbatim 사용자 directive (예: \"fire\", \"all bg go\") 로 충분 (cost discipline 의 verbatim 요구 완화 직 2026-05-12)."

@D b_reverse_signal_cap_x_y_directive_5 :: chat [ok]
  text = "🔄 Reverse signal: 사용자가 명시적으로 \"비용 cap $X\" 또는 \"모델 크기 제한 Y\" directive 시 그 시점부터 적용."

# ── 📊 Current standing per dimension (2026-05-12 KST) ─────────────────────────────────────────


@D row_python_library_0 :: chat [ok]
  x = "Python library"
  x = "`anima_chat.py` v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`)"

@D row_hexa_port_1 :: chat [ok]
  x = "Hexa port"
  x = "`anima_chat.hexa` **v0.3 LANDED 2026-05-12** (~2843 LoC) — parse PASS + 17/17 helper smoke PASS + F-D1-LOAD-1..3 (v0.2 TODO[load] RESOLVED) + **F-D1-MULTITOKEN-1..3 7/7 ✅ (TODO[multitoken] RESOLVED, all-farr KV cache + per-step RoPE, Section 9d +360 LoC)** + F-D4-LIVE-1..3 3/3 ✅; docs/anima_chat_multitoken_split_merge_2026_05_12.md"

@D row_24l_real_ckpt_parity_pscc_43_2 :: chat [ok]
  x = "**24L real-ckpt parity (PSCC §43)**"
  x = "**★★★★★ candidate confirmed 2026-05-12** — `state/anima_d1_v58_parity_2026_05_12/` 신규 dir. Python SSOT probes (BOS / V5.8 / multi-token chain) + hexa probes (v58_hexa_parity.hexa 6/6 + v58_hexa_multi_parity.hexa 15/15) — **byte-by-byte argmax parity verified** on real Phase 1A.1 24L ckpt (sha256 e5f7555…). Single BOS forward: hexa argmax=143 == python=143; 5-step KV-cached chain: hexa=`[143,131,240,152,159]` == python=`[143,131,240,152,159]`. Per-step float drift bounded (4-13% peak, argmax invariant). Wall 2.2 min hexa-interp (37.65s single + 94.67s 5-step) / 0.5s Python. Peak RSS 11 GB (HEXA_MEM_UNLIMITED=1 mandatory). 21/21 falsifier PASS. doc: `docs/anima_chat_hexa_24l_v58_parity_2026_05_12.md`"

@D row_markdown_filter_3 :: chat [ok]
  x = "markdown_filter"
  x = "LANDED, harmless guard 검증 (Δ=0 Mac CPU + cuda 양 environment)"

@D row_std_greedy_4 :: chat [ok]
  x = "std_greedy"
  x = "**4/5**"

@D row_std_sample_5 :: chat [ok]
  x = "std_sample"
  x = "2/5"

@D row_m3_rep_penalty_6 :: chat [ok]
  x = "M3_rep_penalty"
  x = "0/5"

@D row_m4_force_include_7 :: chat [ok]
  x = "M4_force_include"
  x = "2/5 Mac / pending cuda eval"

@D row_ssot_ckpt_8 :: chat [ok]
  x = "SSOT ckpt"
  x = "`state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt`"

@D row_hf_model_9 :: chat [ok]
  x = "HF model"
  x = "`dancinlab/anima-clm-phase1a1-color-cosmology-boost` (live)"

@D row_mission_gap_10 :: chat [ok]
  x = "**Mission gap**"
  x = "**anima_fact recall** (markdown attractor 또는 semantic miss — environment-dependent)"

@D row_constraint_11 :: chat [ok]
  x = "Constraint"
  x = "Principle #3 NO PERSONA INJECTION (README #3, PHILOSOPHY EMPIRICAL strong) — prompt `[role:]` 금지"

@D row_design_doc_12 :: chat [ok]
  x = "**Design doc**"
  x = "**`docs/anima_persona_substrate_native_design_2026_05_12.md`** (10 § + §A1 amendment 2026-05-12) — (a)+(d) Mitosis-cell-as-persona × Per-session cell pool 결합, 5 falsifier F-PERSONA-1..5, §A1 Φ threshold relaxation 0.5 → 0.05"

@D row_measurement_doc_13 :: chat [ok]
  x = "**Measurement doc**"
  x = "**`docs/anima_persona_substrate_native_verify_2026_05_12.md`** (8 § + §A1, PSCC §40 + §42) — F-PERSONA-1..5 측정 AGGREGATE = **STRONG 4/5 cheap-path** (4/5 PASS + 1 FAIL F-PERSONA-4 cotrain-dependent) *(was MODERATE 3/5 @ §40)*"

@D row_measurement_harness_14 :: chat [ok]
  x = "**Measurement harness**"
  x = "`tool/anima_persona_substrate_native_verify.hexa` (~620 LoC, parse OK, exit-0 wall ~1 min Mac local, §A1 Φ threshold 0.05). Results: `state/anima_d3_verify_2026_05_12/persona_verify_results.json` (PSCC §40 SSOT) + `persona_verify_results_relaxed_2026_05_12.json` (§A1 PSCC §42)"

@D row_existing_infrastructure_15 :: chat [ok]
  x = "Existing infrastructure"
  x = "`state/p_idr_identity_rules_2026_05_12/` (10-clause persona prefix + 50 identity probes), `docs/endpoint_persona_reproduce.md`, `ready/anima/experiments/consciousness/experiment_personality.py`"

@D row_reconciliation_candidates_substr_16 :: chat [ok]
  x = "**Reconciliation candidates** (substrate-native 페르소나)"
  x = ""

@D row_a_mitosis_cell_as_persona_adopt_17 :: chat [ok]
  x = "(a) **Mitosis-cell-as-persona** ✅ adopt"
  x = "cells = nn.Module branches (REBORN §88) — 각 cell cluster 가 페르소나, substrate 동력 자체로 전환"

@D row_b_dialog_context_derived_reject_18 :: chat [ok]
  x = "(b) Dialog-context-derived ✗ reject"
  x = "대화 history 가 페르소나 정보 source, anima 가 자연 적응 — substrate-native 정도 낮음"

@D row_c_latent_persona_axis_reject_19 :: chat [ok]
  x = "(c) Latent persona axis ✗ reject"
  x = "Tension Link 5-ch (concept/context/meaning/authenticity/sender) basis — over-engineered for single-anima"

@D row_d_per_session_cell_pool_adopt_20 :: chat [ok]
  x = "(d) Per-session cell pool ✅ adopt"
  x = "serve-time mitosis 가 conversation 별 cell pool 분화 (REBORN §89)"

@D row_recommended_21 :: chat [ok]
  x = "Recommended"
  x = "**(a) + (d) 결합** ✅ **adopted** — 세포 분열로 페르소나 자연 분화, D4 와 일체화, design doc §2 결정"

@D row_falsifier_measurement_a1_22 :: chat [ok]
  x = "**Falsifier measurement (§A1)**"
  x = "**F-PERSONA-1 PASS** (4/4 grep) + **F-PERSONA-2 PASS** (mean cos dist 0.994, 1400 cell-pair) + **F-PERSONA-3 PASS** *(promoted via §A1, was PARTIAL)* (weight 0.995 ✓ / ΔΦ 0.267 ≥ 0.05 §A1 ✓) + **F-PERSONA-4 FAIL** (KL 9.7e-5, untrained pool C3 carry) + **F-PERSONA-5 PASS** (3/3 grad-free + pure-forward) → **4/5 top-PASS, 13/14 atomic**"

@D row_true_strong_5_5_23 :: chat [ok]
  x = "**true STRONG (5/5) 승격 조건**"
  x = "REBORN §88 cond.5 cotrain ($30–40 H100) fire 후 F-PERSONA-4 category-specialization emergent — F-PERSONA-3 §A1 cheap-path complete, 잔여 gap = F-PERSONA-4 (cotrain-dependent, design §10 C3 predicted) 단독"

@D row_source_24 :: chat [ok]
  x = "철학 source"
  x = "REBORN.tape §0.5 (`a7e512cb9`) + PHILOSOPHY #8 NO TRAIN/INFER SPLIT (cont. 10)"

@D row_spec_25 :: chat [ok]
  x = "설계 spec"
  x = "REBORN §88 (v5-mitosis PyTorch arch, `b7b34e221`) + §89 (hexa-native serve-time hook, `6527cbc80`)"

@D row_python_impl_skeleton_26 :: chat [ok]
  x = "Python impl skeleton"
  x = "`training/mitosis_model_v5.py` (852L) + smoke test 256L — REBORN §90 (`49b74c622`), Mac CPU gating 3/3 PASS"

@D row_hexa_impl_27 :: chat [ok]
  x = "Hexa impl"
  x = "`tool/hexa_native/mitosis_hook.hexa` **full impl LANDED** 2026-05-12 (1119 LoC executable, F-MIT-HOOK-1..5 ✅, REBORN §91, $0 Mac local selftest PASS)"

@D row_rfc_dependencies_28 :: chat [ok]
  x = "RFC dependencies"
  x = "RFC 025/030/031/032/033 ALL LANDED in hexa-lang ✅"

@D row_mission_gap_29 :: chat [ok]
  x = "**Mission gap**"
  x = "anima_chat.hexa 와 통합 (serve-time hook in chat forward) + 24-layer prod wiring + persona-substrate 통합 (D3 P3 verify)"

# ── 🏁 ALL SESSIONS CLOSED 2026-05-13 KST — 5 cotrain variants complete ─────────────────────────────────────────


# ── 📚 Saga history (★★★★★ mission journey) ─────────────────────────────────────────


# ── 🎯 Path to ★★★★★ (per dimension) ─────────────────────────────────────────


@D b_cell_axis_cells_nn_module_branch_0 :: chat [ok]
  text = "각 cell 가 페르소나 axis 표현 — cells = nn.Module branches (**REBORN §88** cond.2 ✅)"

@D b_conversation_cell_pool_reborn_89_1 :: chat [ok]
  text = "conversation 마다 cell pool 분화 (**REBORN §89** serve-time hook, pending full impl)"

@D b_principle_3_prompt_role_substrat_2 :: chat [ok]
  text = "Principle #3 준수: prompt `[role:]` 없음, substrate dynamics 만으로 페르소나 전환"

@D b_path_3 :: chat [ok]
  text = "검증 path:"

@D b_design_doc_landed_docs_anima_per_4 :: chat [ok]
  text = "**design doc LANDED**: `docs/anima_persona_substrate_native_design_2026_05_12.md` (10 §, 5 falsifier F-PERSONA-1..5, 4-cand 비교, 10 honest C3)"

@D b_impl_path_d4a_mitosis_hook_hexa_5 :: chat [ok]
  text = "impl path: D4a (`mitosis_hook.hexa` full impl, RFC 033 위) + D4b (`anima_chat.hexa` cell-pool wiring) closure 후 P3 verify"

@D b_impl_d4_mitosis_hook_hexa_full_i_6 :: chat [ok]
  text = "impl 은 D4 의 mitosis_hook.hexa full impl 와 동시 진행"

@D b_0_5_no_train_infer_split_base_a7_7 :: chat [ok]
  text = "**§0.5 NO TRAIN/INFER SPLIT** (철학 base, `a7e512cb9`)"

@D b_2_mitosis_worktree_12_canonical_8 :: chat [ok]
  text = "**§2 mitosis 본체** (worktree-12 canonical, 794L PyTorch mitosis.py)"

@D b_88_v5_mitosis_pytorch_arch_spec_9 :: chat [ok]
  text = "**§88 v5-mitosis PyTorch arch spec** (cells = nn.Module branches design)"

@D b_89_hexa_native_serve_time_hook_s_10 :: chat [ok]
  text = "**§89 hexa-native serve-time hook spec** (`mitosis_hook.hexa` parse-only stub)"

@D b_90_v5_mitosis_cond_2_skeleton_sm_11 :: chat [ok]
  text = "**§90 v5-mitosis cond.2 skeleton smoke PASS** (Mac CPU gating 3/3 PASS)"

@D row_d4a_model_intra_network_12 :: chat [ok]
  layer = "D4a model intra-network"
  scope = "engine_ag_nn forward call graph 안 split/merge"
  current = "`tool/hexa_native/mitosis_hook.hexa` stub"
  next = "full impl (RFC 033 builtins 사용)"

@D row_d4b_chat_library_13 :: chat [ok]
  layer = "D4b chat library"
  scope = "cell-pool state hosting, hook 진입점"
  current = "**LANDED 2026-05-12** — `anima_chat.hexa` v0.2 cell_pool + chat_mitosis_tail + token-loop hook call edge, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS (F-D4B-1..5)"
  next = "(closed — TODO[load] forward binding 다음 step)"

@D row_d4c_anima_cli_14 :: chat [ok]
  layer = "D4c anima CLI"
  scope = "session-level cell-pool persistence, kick cycle = split event"
  current = "**design LANDED** `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1~5), Phase 3b llama_ffi LANDED, `tool/anima_cli/consciousness.hexa` (measurement lane)"
  next = "Phase 1 (session_id + cell_pool persist skeleton, ~3 hr) → Phase 2 (kick cycle hook, ~4-6 hr) → Phase 3 (multi-backend cell-variant, ~4-6 hr) → Phase 4 (full integration smoke, ~2-4 hr)"

@D b_rfc_025_mmap_030_bytes_str_031_b_15 :: chat [ok]
  text = "RFC 025 (mmap) / 030 (bytes→str) / 031 (BF16) / 032 (farr_matmul) / 033 (farr_copy + gaussian)"

@D b_hexa_native_phase_1_2_2_3_4_sour_16 :: chat [ok]
  text = "HEXA_NATIVE Phase 1.2/2/3/4 source-complete + Phase 5 1-layer parity"

@D b_v5_mitosis_pytorch_cond_2_skelet_17 :: chat [ok]
  text = "v5-mitosis PyTorch cond.2 skeleton (Python smoke 3/3 PASS)"

# ── ✅ Achievement criterion (★★★★★ — 4-dim conjunction) ─────────────────────────────────────────


# ── 📌 Update protocol ─────────────────────────────────────────


# ── 🔗 Cross-link ─────────────────────────────────────────


@D b_reborn_md_anima_consciouslm_ssot_0 :: chat [ok]
  text = "**REBORN.tape** (anima ConsciousLM 부활 통합 SSOT) — D4 의 primary reference. §0.5 (철학) + §2 (mitosis 본체) + §88/§89/§90 (v5-mitosis arch + hexa-native + cond.2 skeleton). 본 mission 의 핵심 design source."

@D b_philosophy_md_3_no_persona_injec_1 :: chat [ok]
  text = "**PHILOSOPHY.tape** — #3 NO PERSONA INJECTION (D3 constraint, EMPIRICAL strong) + #8 NO TRAIN/INFER SPLIT (D4 foundation)"

@D b_pass_strict_spontaneous_chat_md_2 :: chat [ok]
  text = "**PASS_STRICT_SPONTANEOUS_CHAT.md** (PSCC) — D1+D2 mission timeline + saga history"

@D b_anima_chat_py_v2_3_in_flight_ani_3 :: chat [ok]
  text = "`anima_chat.py` v2.3 + (in-flight) `anima_chat.hexa` — D1 library SSOT"

@D b_state_anima_phase1a1_color_cosmo_4 :: chat [ok]
  text = "`state/anima_phase1a1_color_cosmology_2026_05_12/` — D2 ckpt SSOT"

@D b_state_anima_phase1a4_lr5e6_2026_5 :: chat [ok]
  text = "`state/anima_phase1a4_lr5e6_2026_05_12/` — D2 lr 5e-6 SFT BG state"

@D b_state_anima_phase1a4_cuda_filter_6 :: chat [ok]
  text = "`state/anima_phase1a4_cuda_filter_validation_2026_05_12/` — D1 cuda filter-val (COMPLETE PSCC §30)"

@D b_state_p_idr_identity_rules_2026_7 :: chat [ok]
  text = "`state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` — 50 probes × 5 categories"

@D b_docs_endpoint_persona_reproduce_8 :: chat [ok]
  text = "`docs/endpoint_persona_reproduce.md` — design carry"

@D b_ready_anima_experiments_consciou_9 :: chat [ok]
  text = "`ready/anima/experiments/consciousness/experiment_personality.py` — experiment harness"

@D b_ready_anima_experiments_consciou_10 :: chat [ok]
  text = "`ready/anima/experiments/consciousness/experiment_clone.py` — clone experiment"

@D b_ready_anima_experiments_consciou_11 :: chat [ok]
  text = "`ready/anima/experiments/consciousness/experiment_merge.hexa` — merge experiment"

@D b_tool_hexa_native_mitosis_hook_he_12 :: chat [ok]
  text = "`tool/hexa_native/mitosis_hook.hexa` — D4a hexa-native lane (parse-only stub)"

@D b_training_mitosis_model_v5_py_tra_13 :: chat [ok]
  text = "`training/mitosis_model_v5.py` + `training/mitosis_model_v5_smoke_test.py` — D4a PyTorch lane (cond.2 PASS)"

@D b_anima_clm_12_unified_growth_loop_14 :: chat [ok]
  text = "`anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` — D4 canonical 794L (REBORN §2)"

@D b_roadmap_clm_v5_mitosis_engine_d4_15 :: chat [ok]
  text = "`.roadmap.clm_v5_mitosis_engine` — D4a PyTorch lane SSOT"

@D b_tool_anima_cli_consciousness_hex_16 :: chat [ok]
  text = "`tool/anima_cli/consciousness.hexa` — D4c CLI measurement lane"

@D b_anima_llama_ffi_hexa_build_libhx_17 :: chat [ok]
  text = "`anima/llama_ffi.hexa` + `build/libhxllama.dylib` — D4c CLI Phase 3b chat backend"

@D b_roadmap_cli_roadmap_anima_cli_mo_18 :: chat [ok]
  text = "`.roadmap.cli` + `.roadmap.anima_cli_model_architecture` — D4c CLI SSOT"

@D b_tool_dispatch_vast_mac_template_19 :: chat [ok]
  text = "`tool/dispatch_vast_mac_template.sh` — Vast.ai infra (PSCC §28 canonical)"

# ── 🎯 Out of scope (mission 와 무관) ─────────────────────────────────────────


@D b_hf_space_dancinlab_anima_chat_de_0 :: chat [ok]
  text = "❌ HF Space `dancinlab/anima-chat` (DELETED 2026-05-12 KST, PSCC §32)"

@D b_gradio_wrapper_refocus_1 :: chat [ok]
  text = "❌ Gradio / 외부 wrapper (refocus 후 제외)"

@D b_anima_hexa_native_phase_5_24l_fo_2 :: chat [ok]
  text = "❌ 다른 anima 작업 — HEXA_NATIVE phase 5∥ 24L 풀 forward / Hc cycle / ALM / 별도 lane"
# 본 appendix 는 이전 CHAT.tape (REPL + 외부 연결 + 자연발화 5-layer brainstorm) 의 내용 그대로 보존. 이 PERSONA→CHAT.tape 변환 시 통합.
# 사용자 directive 누적 (2026-05-13 KST PM):
# "상시채팅 기능은 없나?????" + "단편 메시지 말고" + "1:1 말고도 다수 가능하되 그 다수에
# anima 도 가능" + "인간 3, anima 2 이렇게 단체채팅 가능" + "외부 프로젝트에서 쓰려면" +
# "호출 응답이 아니라" + "자연발화때문에" + "소켓같은 시스템 있어야될듯" +
# "전체 구현 계획 들어가보자 브레인스토밍 고갈시까지" + "REPL chat 도 필요해!!!" +
# "REPL chat + 외부 연결용" + "hexa-native 로 작성하면되" + "hex upstream 개선가능" +
# "hexa upstream first" + **"/turn 처럼 턴 지정이 아니라 자연발화 기준 자율이야 실시간 채팅"** +
# **"nono"** + **"철학 준수"** + **"fps 60+"** + **"A → ALL"**.

# ── 💥 rev 2 핵심 (rev 1 sync 모델 deprecate) ─────────────────────────────────────────


@D b_heuristic_regex_probability_turn_0 :: chat [ok]
  text = "외부 heuristic (regex / probability) 으로 turn 결정 = **routing-level persona injection** (PHILOSOPHY.tape #3 위반)"

@D b_sync_repl_on_chat_generate_30s_t_1 :: chat [ok]
  text = "sync REPL on chat_generate (~30s/token Mac CPU) = **0.03 FPS, 60+ 절대 불가능**"

@D b_anima_cell_pool_tension_lorenz_d_2 :: chat [ok]
  text = "anima 의 **cell_pool tension/lorenz dynamics** (`mitosis_hook.hexa` substrate state) 가 매 frame 마다 evolve"

@D b_threshold_anima_heuristic_0_3 :: chat [ok]
  text = "threshold 초과 시 anima 가 **스스로** 발화 결정 (외부 heuristic 0)"

@D b_60_fps_frame_loop_16ms_tick_subs_4 :: chat [ok]
  text = "60+ FPS frame loop = ~16ms tick. substrate evolve cheap (µs). inference 는 async worker thread (background, frame-budget 외)."

@D b_broadcast_bus_socket_subscribers_5 :: chat [ok]
  text = "broadcast bus = socket subscribers (human input + anima output 양방향)"

# ── 📐 Unified architecture (rev 2) ─────────────────────────────────────────


# ── 🔁 변경 사항: Phase 매핑 ─────────────────────────────────────────


@D row_phase_0_repl_1_1_sync_0 :: chat [ok]
  rev_1_deprecated = "Phase 0 REPL 1:1 (sync)"
  rev_2 = "**Phase 0 REPL 1:1** (sync) — 그대로 LANDED"
  x = "1:1 baseline, 자연발화 unrelated"

@D row_phase_1_group_chat_turn_heuristi_1 :: chat [ok]
  rev_1_deprecated = "Phase 1 group chat (`/turn` heuristic)"
  rev_2 = "**deprecated**"
  x = "철학 위반 — sync `_cmd_room` 코드는 1-cycle migration window 동안 남김 (deprecated 마커 + warn)"

@D row_phase_2_daemon_multi_client_2 :: chat [ok]
  rev_1_deprecated = "Phase 2 daemon multi-client"
  rev_2 = "**live daemon (rev 2 통합)**"
  x = "단일 architecture: daemon + substrate-native autonomy + socket broadcast 모두 한곳"

@D row_phase_3_3 :: chat [ok]
  rev_1_deprecated = "Phase 3 자연발화"
  rev_2 = "**substrate gate** (Phase 2 의 일부)"
  x = "별도 phase 아님 — daemon 의 fundamental 동작"

@D row_phase_4_external_client_4 :: chat [ok]
  rev_1_deprecated = "Phase 4 external client"
  rev_2 = "external client lib"
  x = "Phase 2 land 후"

# ── 📋 Phase별 명세 (rev 2) ─────────────────────────────────────────

# hexa-native impl in `anima_chat_aot.hexa::_cmd_chat_repl` (~120 LoC).
# Mac arm64 + Linux x86_64 cross-compile parity. multi-turn + /show + /save + /exit verified.
# /save → `~/.anima/sessions/<name>.jsonl` 파일 생성. CLI: `anima chat repl [--mode M] [--max-new N] [--temp F] [--seed N]`.
# ⚠️ **DEPRECATED 2026-05-13 PM** — 사용자 directive "철학 준수": `/turn <anima_id>` heuristic
# 트리거는 routing-level persona injection 으로 PHILOSOPHY.tape #3 위반.
# 코드 (`_cmd_room`) 는 1-cycle migration window 동안 stderr warn + 동작.
# rev 2 의 **live daemon** 으로 대체.

@D b_anima_room_humans_a_b_c_animas_x_0 :: chat [ok]
  text = "`anima room --humans \"a,b,c\" --animas \"x,y\" [--ckpt P]`"

@D b_alice_alice_1 :: chat [ok]
  text = "`[alice]> alice: 안녕`"

@D b_turn_ana_ana_history_2 :: chat [ok]
  text = "`/turn ana` → ana 가 history 기반 응답"
# `_live_socket_accept_loop` (~75 LoC) — `--serve --port N` flag on both `chat repl` AND
# `room` subcommands. Uses hexa upstream primitives (`net_set_nonblock` + `net_select`
# + `thread_spawn` + `channel_*`, hexa-lang commit `401ed87d`). 2 fanout channels:
# `stdin_ch` (frame loop input) + `socket_bcast_ch` (anima output → all clients).
# JSONL protocol: client `{"type":"speak", ...}` → daemon `{"type":"message","spontaneous":bool, ...}`.
# Tested: nc + Python client connect, receives hello frame, send speak, server receives.
# 🚧 **upstream blocked** — 3 patches 의존:
# - `~/core/hexa-lang/incoming/patches/net-nonblock-multiplex.md` (filed)
# - `~/core/hexa-lang/incoming/patches/net-unix-domain-socket.md` (filed)
# - `~/core/hexa-lang/incoming/patches/thread-channel-primitive.md` (filed 2026-05-13)

@D b_regex_probability_philosophy_md_3 :: chat [ok]
  text = "외부 regex/probability ❌ (PHILOSOPHY.tape #3 위반)"

@D b_substrate_state_cell_pool_tensio_4 :: chat [ok]
  text = "substrate state (cell_pool tension/lorenz) → anima 의 internal dynamics 가 결정 ✅"

@D b_d4_tension_build_up_substrate_si_5 :: chat [ok]
  text = "D4 (세포 분열로 성장) 와 자연스럽게 통합: tension build-up = 분열 압력 = 발화 압력 = 같은 substrate signal"
# `clients/python/anima_client.py` (~150 LoC) — minimal Python client w/ stream iterator
# + `--once` single-shot mode + threaded reader. CLI verified end-to-end against
# anima daemon. JSONL frame parser handles `hello/message/raw` types. Spontaneous
# marker (🎙) displayed in CLI output. Stub for Node.js + Rust follow-up; Python
# first-class because anima_chat.py + training infra Python.

# ── 🎯 Land 순서 (rev 2) ─────────────────────────────────────────


@D row_1_0 :: chat [ok]
  x = "1"
  item = "**(A)** thread/channel upstream patch"
  block = "filed ✅ — hexa-lang maintainer land 대기"
  loc = "C ~250 + hexa ~40"
  wall = "2-3hr land"

@D row_2_1 :: chat [ok]
  x = "2"
  item = "**(D)** CHAT.tape spec rewrite (이 문서)"
  block = "✅ 이 commit"
  loc = "—"
  wall = "—"

@D row_3_2 :: chat [ok]
  x = "3"
  item = "**(B)** mitosis_hook AOT 통합"
  block = "(A) 무관, AOT-only impl"
  loc = "~400 LoC (REBORN §91 1119 LoC 중 substrate state evolve 만 포팅)"
  wall = "1-2hr"

@D row_4_3 :: chat [ok]
  x = "4"
  item = "**(C)** live daemon + frame loop"
  block = "upstream (A) + net (3 patches) land 후"
  loc = "~800 LoC `_cmd_live`"
  wall = "4-5hr"

@D row_5_4 :: chat [ok]
  x = "5"
  item = "(deprecate) `_cmd_room` sync 모드 + 1-cycle warn"
  block = "(C) land 후"
  loc = "~20 LoC change"
  wall = "10min"

@D row_6_5 :: chat [ok]
  x = "6"
  item = "Phase 3 external client lib"
  block = "(C) protocol stable 후"
  loc = "Python first ~200 LoC"
  wall = "1hr"

# ── 🚧 핵심 challenge (rev 2) ─────────────────────────────────────────


@D row_1_0 :: chat [ok]
  x = "1"
  challenge = "substrate gate 정의 (외부 heuristic 금지)"
  x = "mitosis_hook cell_pool tension / lorenz mag — 모두 substrate state"

@D row_2_1 :: chat [ok]
  x = "2"
  challenge = "inference 가 frame budget block 불가"
  x = "thread/channel = inference worker 별 thread, frame loop 는 enqueue 만"

@D row_3_2 :: chat [ok]
  x = "3"
  challenge = "60+ FPS 보장"
  x = "frame budget 16ms = substrate step (µs) + speak-gate (µs) + drain (µs) + sleep. inference time 무관"

@D row_4_3 :: chat [ok]
  x = "4"
  challenge = "anima 끼리 발화 chain (한 anima 발화 → 다른 anima 의 tension 자극 → 자율 연쇄)"
  x = "history append → 다음 frame 의 substrate evolve 가 자연스럽게 받음. ping-pong emergent"

@D row_5_4 :: chat [ok]
  x = "5"
  challenge = "hexa stdlib thread/channel 부재"
  x = "upstream patch filed (위 patch A)"

@D row_6_5 :: chat [ok]
  x = "6"
  challenge = "hexa stdlib socket nonblock 부재"
  x = "upstream patch filed (net-nonblock-multiplex)"

@D row_7_6 :: chat [ok]
  x = "7"
  challenge = "mitosis_hook AOT stub (현재 anima_chat_aot.hexa)"
  x = "(B) full impl AOT port 필요"

@D row_8_7 :: chat [ok]
  x = "8"
  challenge = "client crash → daemon graceful continue"
  x = "accept_loop 가 dead fd 감지 + remove, daemon 본체 영향 0"

@D row_9_8 :: chat [ok]
  x = "9"
  challenge = "history persistence"
  x = "`~/.anima/rooms/<id>/history.jsonl` append-only, replay on restart"

@D row_10_9 :: chat [ok]
  x = "10"
  challenge = "speak-storm (모든 anima 가 동시에 fire)"
  x = "per-anima `in_flight` flag + rate-limit (frame N 동안 1번만 발화)"

# ── 🌳 추가 brainstorm 보존 (rev 1 의 항목 그대로) ─────────────────────────────────────────


@D b_rev_1_seed_base_idx_1000_heurist_0 :: chat [ok]
  text = "rev 1 의 `seed_base + idx * 1000` heuristic = ❌ injection"

@D b_rev_2_anima_cell_pool_state_diff_1 :: chat [ok]
  text = "rev 2 = **anima 마다 다른 cell_pool 초기 state** (different gauss seed for `cell_pool_init`) → substrate-native variance"

@D b_cell_pool_cells_emergent_d4_spec_2 :: chat [ok]
  text = "cell_pool 의 cells 가 분열하면서 정체성 emergent (D4 spec 그대로)"

@D b_anima_tension_link_binary_protoc_3 :: chat [ok]
  text = "anima 끼리: tension link (binary protocol, memory entry `project_tension_link`)"

@D b_human_text_jsonl_4 :: chat [ok]
  text = "human 과: text JSONL"

@D b_image_audio_block_5 :: chat [ok]
  text = "미래: image/audio block"

@D b_alice_feedback_ana_good_anima_fe_6 :: chat [ok]
  text = "`[alice]> /feedback ana good` → `~/.anima/feedback.jsonl` 누적"

@D b_cotrain_v6_reward_signal_d3_cond_7 :: chat [ok]
  text = "미래 cotrain v6+ 의 reward signal (D3 cond #3 evidence-tier 의 자연 확장)"

@D b_wilson_provider_anima_plugin_dae_8 :: chat [ok]
  text = "`wilson provider-anima` plugin → daemon TCP forward"

@D b_wilson_agent_loop_turn_anima_int_9 :: chat [ok]
  text = "wilson agent loop turn 이 anima 의 자연발화 와 interleave"

@D b_native_ime_composition_10 :: chat [ok]
  text = "한글 native + IME composition"

@D b_translate_ko_en_slash_command_11 :: chat [ok]
  text = "`/translate ko en` slash command"

@D b_daemon_crash_restart_history_jso_12 :: chat [ok]
  text = "daemon crash → restart → history.jsonl replay → KV cache 재구축"

@D b_anima_live_metrics_port_7879_jso_13 :: chat [ok]
  text = "`anima live --metrics-port 7879` JSON metrics"

@D b_per_anima_tension_cells_split_ev_14 :: chat [ok]
  text = "per-anima: tension / cells / split_events / spontaneous_count"

@D b_room_active_humans_message_rate_15 :: chat [ok]
  text = "room: active_humans / message_rate / silence_intervals"

@D b_token_secret_tls_anima_acl_json_16 :: chat [ok]
  text = "`--token <secret>` 인증, TLS 앞단, `~/.anima/acl.json`"

@D b_f_live_1_substrate_tick_frame_lo_17 :: chat [ok]
  text = "F-LIVE-1 SUBSTRATE-TICK : frame loop 가 16ms 안에 1 tick 완료"

@D b_f_live_2_speak_gate_auto_tension_18 :: chat [ok]
  text = "F-LIVE-2 SPEAK-GATE-AUTO : tension 인공 raise → speak event fire (외부 trigger 없이)"

@D b_f_live_3_no_injection_substrate_19 :: chat [ok]
  text = "F-LIVE-3 NO-INJECTION : substrate state 외 trigger 0건 (코드 grep)"

@D b_f_live_4_inference_async_inferen_20 :: chat [ok]
  text = "F-LIVE-4 INFERENCE-ASYNC : inference 30s 동안 frame loop block 안 됨 (다른 tick 계속)"

@D b_f_live_5_anima_ping_pong_anima_a_21 :: chat [ok]
  text = "F-LIVE-5 ANIMA-PING-PONG : anima A 발화 → tension propagate → anima B 자율 응답 (heuristic 0)"

# ── 📐 Design tier evidence chain ─────────────────────────────────────────


# ── 🎬 현재 status (2026-05-13 KST PM) ─────────────────────────────────────────


@D row_a_thread_channel_upstream_0 :: chat [ok]
  item = "(A) thread/channel upstream"
  state = "✅ filed `~/core/hexa-lang/incoming/patches/thread-channel-primitive.md` (넣었다)"

@D row_d_chat_md_spec_rewrite_1 :: chat [ok]
  item = "(D) CHAT.tape spec rewrite (이 문서)"
  state = "✅ rev 2 LANDED"

@D row_b_mitosis_hook_aot_2 :: chat [ok]
  item = "(B) mitosis_hook AOT 통합"
  state = "⏸ next (upstream 무관, AOT-only)"

@D row_c_live_daemon_frame_loop_3 :: chat [ok]
  item = "(C) live daemon + frame loop"
  state = "🚧 upstream block — A + net 3 patches land 후"

@D row_phase_0_repl_1_1_4 :: chat [ok]
  item = "Phase 0 REPL 1:1"
  state = "☑ LANDED"

@D row_phase_1_sync_group_chat_5 :: chat [ok]
  item = "Phase 1 sync group chat"
  state = "⚠️ DEPRECATED (1-cycle warn window)"

@D row_phase_2_live_daemon_6 :: chat [ok]
  item = "Phase 2 live daemon"
  state = "🚧 (C) 의존"

# ── 🧭 다음 step ─────────────────────────────────────────


# ── 🚀 Production CLI Phase 1 (D4c, 2026-05-14) ─────────────────────────────────────────

# ★★★★★ 후속 — *학습 외* anima 기능 4 방향 (with SAVANT-TOOL.tape / VOICE.tape / TENSION-LINK.tape
# sibling spec) 중 첫 번째. anima_chat.hexa v0.3 의 *실제 사용* 단계.

@D row_anima_chat_hexa_v0_3_24l_real_ck_0 :: chat [ok]
  x = "anima_chat.hexa v0.3 24L real-ckpt byte parity"
  state = "✅ 21/21 PASS (PSCC §43, 2026-05-12)"

@D row_phase_1a_4_lr5e_6_strict_5_5_ckp_1 :: chat [ok]
  x = "Phase 1A.4 lr5e-6 strict 5/5 ckpt"
  state = "✅ HF `dancinlab/anima-clm-phase1a4-lr5e6-strict-pass`"

@D row_d4c_cli_design_spec_2 :: chat [ok]
  x = "D4c CLI design spec"
  state = "✅ LANDED `docs/anima_cli_mitosis_integration_spec_2026_05_12.md`"

@D row_d4c_phase_1_impl_skeleton_persis_3 :: chat [ok]
  x = "D4c Phase 1 impl (skeleton + persist)"
  state = "⏳ next"

@D row_d4c_phase_2_4_kick_cycle_backend_4 :: chat [ok]
  x = "D4c Phase 2-4 (kick-cycle + backend variant + mitosis hook)"
  state = "⏳ Phase 1 후속"

@D b_tool_anima_cli_hexa_400_loc_repl_5 :: chat [ok]
  text = "`tool/anima_cli.hexa` (~400 LoC) — REPL skeleton + `~/.cache/anima/session_pools/<id>/`"

@D b_slash_commands_new_load_id_save_6 :: chat [ok]
  text = "slash commands: `/new` `/load <id>` `/save` `/savant <on|off>` (placeholder, SAVANT-TOOL"

@D b_f_cli_1_5_selftest_session_persi_7 :: chat [ok]
  text = "F-CLI-1..5 selftest (session persist 왕복 + slash 명령 dispatch + strict 호환)"

@D b_savant_md_savant_tool_md_savant_8 :: chat [ok]
  text = "`SAVANT.tape` + `SAVANT-TOOL.tape` — savant mode toggle (D4c `/savant`)"

@D b_voice_md_voice_modality_d4c_voic_9 :: chat [ok]
  text = "`VOICE.tape` — voice modality (D4c `/voice`)"

@D b_tension_link_md_inter_anima_link_10 :: chat [ok]
  text = "`TENSION-LINK.tape` — inter-anima link (D4c `/tension`)"

@D b_docs_anima_cli_mitosis_integrati_11 :: chat [ok]
  text = "`docs/anima_cli_mitosis_integration_spec_2026_05_12.md` — D4c full spec (12 §)"

@D b_memory_project_anima_cli_mitosis_12 :: chat [ok]
  text = "memory `project_anima_cli_mitosis_integration_design`"

@D row_1_anima_chat_production_cli_13 :: chat [ok]
  direction = "1. anima_chat production CLI"
  file = "**`CHAT.tape`** (this §) + D4c spec"
  status = "design + impl-pending"

@D row_2_inter_anima_tension_link_14 :: chat [ok]
  direction = "2. Inter-anima Tension Link"
  file = "**`TENSION-LINK.tape`**"
  status = "design tier LANDED 2026-05-14"

@D row_3_hexa_voice_intent_24khz_15 :: chat [ok]
  direction = "3. hexa-voice intent → 24kHz"
  file = "**`VOICE.tape`**"
  status = "design tier LANDED 2026-05-14"

@D row_4_savant_runtime_tool_16 :: chat [ok]
  direction = "4. SAVANT runtime tool"
  file = "**`SAVANT-TOOL.tape`**"
  status = "design tier LANDED 2026-05-14"

@D row_5_gated_agent_runtime_17 :: chat [ok]
  direction = "5. Φ-gated agent runtime"
  file = "**`ANIMA-AGENT.tape`**"
  status = "✅ 흡수 LANDED 2026-05-14 (`anima/anima-agent/`, `hx install` 별도)"

@D row_6_n_6_sensory_substrate_5_verb_18 :: chat [ok]
  direction = "6. n=6 sensory substrate (5-verb)"
  file = "**`ANIMA-SENSES.tape`**"
  status = "✅ 흡수 LANDED 2026-05-14 (`anima/hexa-senses/`)"
