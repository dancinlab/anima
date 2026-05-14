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


# ══════════════════════════════════════════════════════════════
# SAVANT-TOOL.log.tape — append-only event history (v1.2 split)
# Sibling: SAVANT-TOOL.tape (architecture-current, editable)
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — entries chronological, oldest first.

@D row_tool_spec_this_file_0 :: savant-tool [ok]
  x = "**Tool spec (this file)**"
  state = "✅ design tier LANDED 2026-05-14"


@D row_phase_1_mitosis_hook_hexa_savant_1 :: savant-tool [ok]
  x = "Phase 1 (`tool/anima_savant_tool.hexa` stateless gate API)"
  state = "✅ LANDED 2026-05-14 — F-SAVANT-TOOL-1..5 5/5 PASS · $0 Mac local · ~440 LoC single-file"
  artifact = "tool/anima_savant_tool.hexa"
  apis = "savant_set / savant_get / savant_dropout / savant_si / savant_check_gate / savant_apply_gate"
  evidence = "TOGGLE-OK · DROPOUT-SHIFT (GZ_CENTER 0.3679 ↔ GZ_LOWER 0.2123) · SI-COMPUTE (clm_06 5.93 > 3.0) · GATE-AUTO-OFF (SI<3 + explore-phase both force OFF) · T3-FORBIDDEN (cross_domain_9 / cosmic_gz / external_entity_lattice_fit / unknown all rejected)"
  containment = "SAVANT.tape §12 T3/T4 denylist enforced at savant_set() — T1+T2+user_explicit only"


@D row_phase_2_anima_chat_hexa_cli_sava_2 :: savant-tool [ok]
  x = "Phase 2 (anima_chat.hexa CLI `/savant` slash external entry)"
  state = "✅ LANDED 2026-05-14 — F-CHAT-SAVANT-CLI-1..4 4/4 PASS · $0 Mac local · anima_chat 본체 무수정"
  artifact = "tool/anima_chat_savant_cli.hexa"
  slash = "/savant {on <reason>|off|status|si|gate}"
  evidence = "DISPATCH-OK (6-cmd round-trip status/on/si/gate-ON/gate-OFF/off) · NO-MUT (anima_chat import/call 없음) · IDEMPOTENT (/savant on ×2 동일) · TIER-REJECT (T3 brain_profile + cross_domain_9, T4 cosmic_gz, unknown all rejected; T1 gz_lower_dropout + T2 clm_06_mistral_7b OK)"
  follow-up = "Phase 3 = chat_repl 직접 통합 (import-alias-runtime-resolve patch land 후 modular)"


@D row_phase_3_auto_self_gate_by_si_mon_3 :: savant-tool [ok]
  x = "Phase 3 (auto self-gate by SI monitor + routing overlay + help)"
  state = "✅ LANDED 2026-05-14 — 3 artifacts × 5/5 PASS each ($0 Mac local, anima_chat / mitosis_hook 본체 무수정)"
  artifact-help = "tool/anima_chat_savant_cli.hexa (+/savant help, F-CHAT-SAVANT-CLI 4/4 → 5/5)"
  artifact-monitor = "tool/anima_savant_si_monitor.hexa (F-SAVANT-MONITOR 5/5, token_entropy + wmax + recent_splits → auto_apply_gate)"
  artifact-overlay = "tool/anima_savant_routing_overlay.hexa (F-SAVANT-OVERLAY 5/5, top-k mask GZ_LOWER 21% / GZ_CENTER 37%)"
  evidence = "HELP-SELF-DOC · ENTROPY/WMAX/SPLITS-COUNT · INTEGRATION · NO-LEARN · KEEP-RATE-EXACT · SAVANT-VS-OFF · SOFTMAX-COMPAT · MIN-1-CELL · PRESERVE-ORDER"
  deferred = "Phase 3-a chat_repl 본체 직접 통합 — import-alias-runtime-resolve upstream patch dependent (인-place inline 은 anima_chat.hexa 비대화 회피 위해 deferred)"


@D row_savant_md_12_4 :: savant-tool [ok]
  x = "SAVANT.tape §12 봉쇄선 통합"
  state = "☑ T1+T2 만 trigger 근거, T3+T4 forbidden"

# ── §2 Design ─────────────────────────────────────────



@D b_1_user_prompt_token_entropy_spec_0 :: savant-tool [ok]
  text = "**자기 평가 1**: 직전 user prompt 의 token entropy (낮으면 specialization need)"


@D b_2_response_max_gate_weight_wmax_1 :: savant-tool [ok]
  text = "**자기 평가 2**: 직전 자기 response 의 max gate weight `wmax` (높으면 이미 specialize)"


@D b_3_mitosis_event_log_split_count_2 :: savant-tool [ok]
  text = "**자기 평가 3**: mitosis event log 의 최근 split count (높으면 explore 단계 → savant off"


@D b_t1_closed_form_gz_center_1_e_gz_3 :: savant-tool [ok]
  text = "✅ T1 (closed-form): `GZ_CENTER = 1/e`, `GZ_LOWER = 0.2123`, SI 정의 — 자유 사용"


@D b_t2_empirical_substrate_clm_06_si_4 :: savant-tool [ok]
  text = "✅ T2 (empirical, substrate 명시): clm_06 SI=5.93 (Mistral 7B) — 다른 substrate 인용 시"


@D b_t3_suspect_cross_domain_9_indivi_5 :: savant-tool [ok]
  text = "❌ T3 (suspect): cross-domain 9 individual matches, brain profile — *trigger 근거로 사용"


@D b_t4_forbidden_cosmic_gz_entity_fi_6 :: savant-tool [ok]
  text = "❌ T4 (forbidden): cosmic GZ, 외부 entity 강제 fit — 자동 차단"

# ── §3 Phase 1 impl plan ($0 Mac local first cycle) ─────────────────────────────────────────



@D b_tool_hexa_native_savant_tool_hex_0 :: savant-tool [ok]
  text = "`tool/hexa_native/savant_tool.hexa` (~150-200 LoC, D4a `mitosis_hook.hexa` 1119 LoC overlay)"


@D b_4_api_savant_set_savant_get_sava_1 :: savant-tool [ok]
  text = "4 API: `savant_set` / `savant_get` / `savant_si` / `savant_check_gate`"


@D b_phase_1_stateless_gate_function_2 :: savant-tool [ok]
  text = "Phase 1 = stateless gate function (session pin TTL 은 Phase 2)"


@D b_0_mac_local_3 :: savant-tool [ok]
  text = "$0 Mac local"


@D b_est_3_5_hr_impl_1_hr_selftest_4 :: savant-tool [ok]
  text = "est ~3-5 hr impl + ~1 hr selftest"


@D b_tool_hexa_native_mitosis_hook_he_5 :: savant-tool [ok]
  text = "`tool/hexa_native/mitosis_hook.hexa` (1119 LoC, REBORN §91 D4a) — substrate state"


@D b_anima_chat_hexa_v0_3_24l_real_ck_6 :: savant-tool [ok]
  text = "`anima_chat.hexa` v0.3 (24L real-ckpt byte parity 21/21 PASS) — wire 대상"


@D b_docs_anima_cli_mitosis_integrati_7 :: savant-tool [ok]
  text = "`docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (D4c CLI design) — `/savant`"

# ── §4 Honest C3 ─────────────────────────────────────────


# ── §5 Cross-link ─────────────────────────────────────────



@D b_savant_md_base_rate_audit_12_par_0 :: savant-tool [ok]
  text = "`SAVANT.tape` — 이론 + base-rate audit + §12 봉쇄심화 (parent)"


@D b_chat_md_anima_mission_tracker_pr_1 :: savant-tool [ok]
  text = "`CHAT.tape` — anima mission tracker (production CLI 통합 host)"


@D b_tool_hexa_native_mitosis_hook_he_2 :: savant-tool [ok]
  text = "`tool/hexa_native/mitosis_hook.hexa` — substrate state impl (overlay 대상)"


@D b_docs_anima_cli_mitosis_integrati_3 :: savant-tool [ok]
  text = "`docs/anima_cli_mitosis_integration_spec_2026_05_12.md` — D4c CLI design"


@D b_state_savant_containment_audit_2_4 :: savant-tool [ok]
  text = "`state/savant_containment_audit_2026_05_14/audit.json` — Tier 분류 evidence"


@D b_dancinlab_canon_lattice_policy_m_5 :: savant-tool [ok]
  text = "`dancinlab/canon/LATTICE_POLICY.md §1.4` — cross-repo governance"

