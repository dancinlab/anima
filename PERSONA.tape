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
# PERSONA.tape — architecture-current (editable per v1.2)
# Event history lives in PERSONA.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# PERSONA.tape — anima D3 페르소나 substrate-native ledger (root-level)
# ══════════════════════════════════════════════════════════════

# **Distinguishes from**: `CHAT.tape` (★★★★★ 5-cond live daemon tracker) +
# `docs/anima_persona_substrate_native_design_2026_05_12.md` (D3 design SSOT,
# §A1/§A3/§A4 amendments). 본 root 파일은 페르소나 substrate-native 진행
# ledger — saga-level summary + 교훈 + 다음 cycle 의 closure path.
# >
# **Rename chain history**: `GOAL.md` → `PERSONA.tape` → `CHAT.tape` (2026-05-13 PM
# CHAT.tape rev 2 daemon land 시 5-cond tracker 가 CHAT.tape 로 이동). 본 PERSONA.tape
# 는 PSCC §53 2026-05-13 KST 23:15 신규 재생성 — 페르소나 axis 만 root-level
# tracking 으로 분리.
# ---

# ── §1 Mission ─────────────────────────────────────────

# 사용자 directive (verbatim, 2026-05-12): `[anima chat 시스템, anima 모델,
# 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`


@I a6_baseline scope=cond3_4a_routing :: persona [d=2026-05-14 ok]
  => "baseline v3-routing batch=8 3-seed mean z=1.48 (§A5)"


@I a6_structural_diagnosis scope=v3_routing_class :: persona [d=2026-05-14 ok]
  => "Routing-axis strict z>3.0 NOT achievable via top-K MoE + balance-aux + entropy-reg class. Cells route differently (KL=0→3+ saga first opening) but noise floor ~ equals signal floor under null permutation. Genuine escape requires non-routing-axis innovation."


@I a6_cond3_anchor scope=cond3_strict_closure :: persona [d=2026-05-14 ok]
  => "cond #3 ☑ MAINTAINED via §A3 4b composite multi-metric defense (v2 z=3.20 + 7/8 metrics z>2.0). Strict-4a rejected across 9 variants — composite multi-metric remains canonical closure anchor."

# ── §8 cross-link ─────────────────────────────────────────


