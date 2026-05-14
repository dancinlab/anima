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
#
# SAVANT-TOOL.log.tape — append-only event history sibling of SAVANT-TOOL.tape
# (v1.2 architecture-vs-history split, 2026-05-15).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — append events below this line, chronological (oldest first).

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
