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
# ANIMA-AGENT.log.tape — append-only event history sibling of ANIMA-AGENT.tape
# (v1.2 architecture-vs-history split, 2026-05-14).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — absorption events · repo lifecycle transitions
# (chronological, oldest first)

# ── §1 Status (2026-05-14) — absorption landing event ─────────────────────────────────────────

@D row_anima_repo_anima_anima_agent_0 :: anima-agent [ok]
  x = "**anima repo 흡수 (anima/anima-agent/)**"
  state = "✅ LANDED 2026-05-14 (rsync from ~/core/anima-agent/ minus .git)"

# ── §6 Provenance — repo cycle history ─────────────────────────────────────────

@D b_dancinlab_anima_agent_last_commi_0 :: anima-agent [ok]
  text = "흡수 출처: `dancinlab/anima-agent` (last commit 2026-05-14 `cfb9f46` \".tape v1.1"

@D b_1_anima_anima_agent_d290f1ae7_20_1 :: anima-agent [ok]
  text = "원래 출처 (사이클 1): `anima/anima-agent/` (`d290f1ae7`, 2026-05-04 extracted)"

@D b_2_anima_repo_delete_2 :: anima-agent [ok]
  text = "사이클 2 (본 흡수): 다시 anima 안으로 회수, 별도 repo delete 예정"

@D b_rsync_exclude_git_anima_git_hist_3 :: anima-agent [ok]
  text = "rsync `--exclude='.git'` 으로 통합. anima 의 git history 에 신규 commit 으로 추가."
