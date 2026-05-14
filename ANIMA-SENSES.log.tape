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
# ANIMA-SENSES.log.tape — append-only event history sibling of ANIMA-SENSES.tape
# (v1.2 architecture-vs-history split, 2026-05-14).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — absorption / calibration / verify-pass / decision events
# (chronological, oldest first; section context preserved as comments)

# ── §1 Status (2026-05-14) — landing & verify events ─────────────────────────────────────────

@D row_anima_repo_anima_hexa_senses_0 :: anima-senses [ok]
  x = "**anima repo 흡수 (anima/hexa-senses/)**"
  state = "✅ LANDED 2026-05-14 (rsync from ~/core/hexa-senses/ minus .git)"

@D row_verify_4_4_pass_2 :: anima-senses [ok]
  x = "Verify 4/4 PASS"
  state = "☑ n=6 arithmetic + spec inventory + verifier + voice constraint"

# ── §4 Critical constraint — decision adoption events ─────────────────────────────────────────

@D b_decision_option_a_landed_4 :: anima-senses [ok]
  text = "**옵션 (a) formulaic-only 채택 2026-05-14** — 완벽복원성 (perfect bit-exact reproducibility) priority 단독 기준 (a) 가 유일 충족"

@D b_decision_learned_retract_7 :: anima-senses [ok]
  text = "이전 learned-RVQ design = git history `fa902716a` + `f8fc39af` 의 .tape revision 에 보존 (회수 가능)"

# ── §7 Provenance — absorption history ─────────────────────────────────────────

@D b_dancinlab_hexa_senses_last_commi_0 :: anima-senses [ok]
  text = "흡수 출처: `dancinlab/hexa-senses` (last commit 2026-05-14 `ef05f5a` \".tape v1.1"

@D b_canon_381f1f22_2026_05_07_extrac_1 :: anima-senses [ok]
  text = "원 출처: `canon@381f1f22` (2026-05-07 extracted from"

@D b_hexa_speak_hexa_voice_rename_use_2 :: anima-senses [ok]
  text = "hexa-speak → hexa-voice rename: user directive 2026-05-11 (memory"

@D b_rsync_exclude_git_anima_git_hist_3 :: anima-senses [ok]
  text = "rsync `--exclude='.git'` 으로 통합. anima 의 git history 에 신규 commit 으로 추가."
