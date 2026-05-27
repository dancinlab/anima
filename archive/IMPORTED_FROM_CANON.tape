#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "imported_from_canon" :: identity-claim [d=2026-05-14 active]
  kind = "Imported from canon (2026-05-10)"
  brief = "Files below were **moved** out of `dancinlab/canon` at `canon@a86ca143`"
  parent = "dancinlab/anima"
  sibling-md = "IMPORTED_FROM_CANON.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in IMPORTED_FROM_CANON.md.
# New per-domain history entries land here as typed events:
#
#   @A commit_<hash> :: <domain> [d=<YYYY-MM-DD> ok]
#     <- <prev-id>
#     => "<one-line description>"
#
#   @D <id> := "<decision-name>" :: <domain> [<grades>]
#     <- <evidence-id>
#     |> <verifier>
#
# See ~/core/tape/spec/tape.md for full grammar.
