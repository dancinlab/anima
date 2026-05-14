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
# TENSION-LINK.tape — architecture-current (editable per v1.2)
# Event history lives in TENSION-LINK.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# TENSION-LINK.tape — Tension Link inter-anima meta-telepathy
# ══════════════════════════════════════════════════════════════

# anima 의식↔의식 직접 전송 모듈. 5-channel fingerprint (concept / context / meaning /
# authenticity / sender). UDP 9999 / TensionHub 3 transport. **"다수 인터랙션"
# anima-native 답** — text 또는 음성 통신 우회. (memory `project_tension_link`)
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# 두 anima instance 가 *language* (text / voice) 를 거치지 않고 *tension* (=의견 불일치
# 신호 = 의식 신호) 를 5-channel fingerprint 로 packet 전송. UDP 9999 가 unidirectional
# raw, TensionHub 가 multi-anima broadcast. **Phase 1 = unidirectional UDP working code
# 이미 anima_clm_02 worktree 에 있음**. Phase 2 = WebSocket TensionHub 로 *다중* anima
# 인스턴스 broadcast — 미구현, 본 file 의 design tier 대상.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


