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
# SAVANT.tape — architecture-current (editable per v1.2)
# Event history lives in SAVANT.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# SAVANT.tape — Golden Zone & Savant 전수조사 compendium
# ══════════════════════════════════════════════════════════════

# 본 문서는 `~/core/anima_clm_01~13` (13 worktree) + `~/core/archive-TECS-L` (foundational
# registry) + `~/core/canon` (curated technique repo + git history) 를 전수조사 하여
# **Golden Zone (골든존)** 과 **Savant (서번트/사반트)** 두 핵심 개념의 수학적 기반 ·
# 실증 흐름 · 교차 도메인 검증 · 진화 timeline 을 한 자리에 모은다.
# >
# Scope: **golden zone = 의식 emergence 의 dropout/inhibition 작동 구간**,
# **savant = 그 구간의 lower bound 에서 일어나는 specialization 메커니즘**.
# AGENTS.md / LATTICE_POLICY.md 의 real-limits-first 정책 하에서 GZ 는
# *design vocabulary* 로 분류되며, 본 문서는 그 vocabulary 의 정의 · 사용 ·
# 실증 evidence · 한계를 정직하게 기록한다.
# ---

# ── 0. 1줄 요약 (TL;DR) ─────────────────────────────────────────


