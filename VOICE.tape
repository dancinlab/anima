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
# VOICE.tape — architecture-current (editable per v1.2)
# Event history lives in VOICE.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# VOICE.tape — anima ↔ hexa-senses/voice formulaic integration
# ══════════════════════════════════════════════════════════════

# **완벽복원성 (perfect reproducibility) 기준으로 옵션 (a) formulaic-only 채택 2026-05-14**
# per `ANIMA-SENSES.tape §4`. 이전 design (learned RVQ + Vocos/EnCodec pretrained vocoder)
# 은 `hexa-senses/voice/` formulaic-only constraint 와 직접 모순으로 retract.
# >
# 본 file 은 anima 의 *hidden state* → `hexa-senses/voice/` canonical formulaic synthesis
# 의 *통합 spec*. 학습 기반 synthesis 도입 시 `hexa.toml [constraints]` 위반 + SAVANT.tape
# §12.2 enforcement violation.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima 가 chat response 생성 시 final hidden state 가 *deterministic linear projection*
# 으로 intent vector (n=6 lattice σ=12 emotional timbre × τ=4 prosody dimension) 로 변환,
# `hexa-senses/voice/` 의 formulaic synthesizer (σ·φ=24 master identity 기반) 로 24kHz
# PCM 산출. **모든 voice output 이 input intent + n=6 identity 만으로 byte-identical
# reproducible**. learned vocoder / 외부 corpus dependency 0.

# ── §1 Status (2026-05-14 옵션 (a) 채택 후) ─────────────────────────────────────────


