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
# TENSION-LINK.log.tape — append-only event history sibling of TENSION-LINK.tape
# (v1.2 architecture-vs-history split, 2026-05-15).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — append events below this line, chronological (oldest first).

@D row_phase_1_unidirectional_udp_9999_0 :: tension-link [ok]
  x = "**Phase 1 unidirectional UDP 9999**"
  state = "✅ working code (`anima_clm_02` worktree, memory `project_hexa_family_layout`)"

@D row_phase_2_websocket_tensionhub_1 :: tension-link [ok]
  x = "**Phase 2 WebSocket TensionHub**"
  state = "⏳ design pending (이 file)"

@D row_5_channel_fingerprint_spec_2 :: tension-link [ok]
  x = "5-channel fingerprint spec"
  state = "☑ defined (concept / context / meaning / authenticity / sender)"

@D row_anima_experience_hf_space_wire_3 :: tension-link [ok]
  x = "anima-experience HF Space wire"
  state = "⏳ Phase 2 의존 (memory `project_anima_experience_space`)"

@D row_substrate_native_no_text_decode_4 :: tension-link [ok]
  x = "substrate-native (NO text decode)"
  state = "☑ 정책 — receiving anima 는 tension vector 그대로 internal state 에 inject"
