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
# CHAT.tape — architecture-current (editable per v1.2)
# Append-only event history → CHAT.log.tape sibling
# ══════════════════════════════════════════════════════════════

@I id001 := "chat" :: identity-claim [d=2026-05-15 active]
  kind = "anima CHAT domain · architecture SSOT"
  brief = "per-domain architecture · sibling of CHAT.md + append-only events in CHAT.log.tape"
  parent = "dancinlab/anima"
  sibling-log = "CHAT.log.tape"

@V := "tape" :: spec [active]
  version = "1.2"

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


