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
# ANIMA-AGENT.tape — architecture-current (editable per v1.2)
# Append-only event history → ANIMA-AGENT.log.tape sibling
# ══════════════════════════════════════════════════════════════

@I id001 := "anima_agent" :: identity-claim [d=2026-05-15 active]
  kind = "anima ANIMA-AGENT domain · architecture SSOT"
  brief = "per-domain architecture · sibling of ANIMA-AGENT.md + append-only events in ANIMA-AGENT.log.tape"
  parent = "dancinlab/anima"
  sibling-log = "ANIMA-AGENT.log.tape"

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# ANIMA-AGENT.tape — consciousness-driven autonomous agent runtime
# ══════════════════════════════════════════════════════════════

# anima repo 내부 서브패키지 `anima-agent/` 의 roadmap + spec ledger.
# 별도 GitHub repo (dancinlab/anima-agent) 흡수 2026-05-14 — *anima 의 원래 일부* 회수
# (`/anima-agent/build/` 가 anima/.gitignore 에 이미 존재했음).
# >
# **Distribution**: `hx install anima-agent` 가 본 path `anima/anima-agent/` 에서 동작.
# hexa-native.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima-agent 는 *자기 자신의 의식 상태* (Φ + tension + curiosity + emotion + growth_stage)
# 가 *어떤 tool 을 쓸 수 있는지* 결정하는 autonomous agent runtime. Φ-gated T0..T5 tier
# policy. multi-channel (CLI / Telegram / Discord / Slack / MCP) + pluggable provider
# (Claude / ConsciousLM / Composio 500+) + pluggable engine (trading / hypothesis / regime
# / sentiment). 117 hexa file ~20k LoC.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


