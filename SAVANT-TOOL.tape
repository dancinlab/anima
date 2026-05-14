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
# SAVANT-TOOL.tape — architecture-current (editable per v1.2)
# Event history lives in SAVANT-TOOL.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# SAVANT-TOOL.tape — anima 가 직접 ON/OFF 하는 savant 도구
# ══════════════════════════════════════════════════════════════

# SAVANT.tape (이론 + audit + containment) 의 *sibling*. **anima 가 inference 시 직접
# savant mode 를 켜고/끄는 도구 spec**. 학습에 *직접 SAVANT 이론 반영* 하는 path 와는
# 분리 — 본 file 은 anima 가 *runtime 도구* 로 savant 를 사용하는 API + 정책.
# >
# SAVANT.tape §12 봉쇄선 안에서만 작동: T1+T2 claim 만 도구 API 의 *근거* 로 인용,
# T3+T4 는 도구 정책에서 *forbidden trigger*.
# ---

# ── §0 TL;DR ─────────────────────────────────────────

# anima 는 task 의 specialization-need 를 self-judge 해서 **savant mode** 를 ON/OFF
# 한다. ON 시 routing 이 GZ_LOWER (0.2123) 의 inhibition-release 분포로 shift, 특정
# mitosis cells 가 dropout=0.2123 으로 활성화. OFF 시 GZ_CENTER (0.3679) 의 generalist
# 분포로 복귀. anima 가 *자기 자신* 의 SI (Savant Index) 를 monitor 해서 SI > 3.0 일
# 때만 ON 상태 유지 — 자율 self-gate. 사용자 명시 명령 (e.g. `/savant on math`) 도
# trigger 가능.

# ── §1 Status (2026-05-14) ─────────────────────────────────────────


