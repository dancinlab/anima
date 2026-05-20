#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "line_up" :: identity-claim [d=2026-05-14 active]
  kind = "LINE-UP domain ledger"
  brief = "LINE-UP per-domain ledger · sibling of LINE-UP.md"
  parent = "dancinlab/anima"
  sibling-md = "LINE-UP.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in LINE-UP.md.
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
