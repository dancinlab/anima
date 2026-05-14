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

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima.convergence" :: identity-claim [d=2026-05-15 active]
  kind = "anima convergence-cycle milestone projection · architecture SSOT"
  brief = "honesty-triad C3-closure precondition + Ψ=1/2 fixed-point target. Live records in ~/core/anima/convergence/*.convergence."
  parent = "dancinlab/anima"
  sibling-log = "CONVERGENCE.log.tape"

# ══════════════════════════════════════════════════════════════
# CONVERGENCE.tape — recent anima convergence-cycle events
#
# Live convergence records live in ~/core/anima/convergence/*.convergence
# (DESIGN ledger — .PRESERVE-AS-SSOT sentinel inside that dir).
# This tape is the milestone projection — one @A per major cycle landing.
# ══════════════════════════════════════════════════════════════

@D c1 := "convergence.honesty_triad_C3" :: convergence [d=2026-05-14 ok]
  text = "Honesty-triad C3-closure precondition for any raw rule promotion"
  proof = ".raw-audit/ hash-chained entries with proof+cert fields"

@D c2 := "convergence.psi_half_target" :: convergence [d=2026-05-14 ok]
  text = "Ψ=1/2 fixed-point convergence as the canonical target"
  proof = "state/format_witness/*.jsonl (witness rows)"
