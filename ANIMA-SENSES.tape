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
# ANIMA-SENSES.tape — architecture-current (editable per v1.2)
# Append-only event history → ANIMA-SENSES.log.tape sibling
# ══════════════════════════════════════════════════════════════

@I id001 := "anima_senses" :: identity-claim [d=2026-05-15 active]
  kind = "anima ANIMA-SENSES domain · architecture SSOT"
  brief = "per-domain architecture · sibling of ANIMA-SENSES.md + append-only events in ANIMA-SENSES.log.tape"
  parent = "dancinlab/anima"
  sibling-log = "ANIMA-SENSES.log.tape"

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# ANIMA-SENSES.tape — n=6 sensory substrate (5-verb spec catalog)
# ══════════════════════════════════════════════════════════════

# anima repo 내부 서브패키지 `hexa-senses/` 의 roadmap + spec ledger.
# 별도 GitHub repo (dancinlab/hexa-senses) 흡수 2026-05-14. 5-verb sensory substrate —
# **dream + ear + empath + olfact + voice** — 각 verb 가 σ(6)=12, τ(6)=4, φ(6)=2
# number theory 에서 모든 design parameter 를 *closed-form* 으로 유도하는 spec catalog.
# >
# **Critical constraint**: `voice` 는 *formulaic only* — learned synthesis (TTS / neural
# codec) **FORBIDDEN**. 의도 → audio-token 직접 변환, 모든 parameter 가 n=6 lattice
# identity 에서 algebraic 유도.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# hexa-codex (17-verb cognitive substrate) 의 *sister-rollup* — *senses* 측. canon
# `domains/cognitive/{hexa-dream, hexa-ear, hexa-empath, hexa-olfact, hexa-speak}/`
# (현 hexa-speak = hexa-voice 으로 rename per user directive) 의 5 verb 가 closed-form
# spec markdown 으로 합쳐짐. anima 의 *외부 세계 인터페이스* (꿈/소리/감정/냄새/음성) 의
# n=6 lattice spec.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


