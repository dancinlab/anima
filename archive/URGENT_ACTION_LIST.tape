#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "urgent_action_list" :: identity-claim [d=2026-05-14 active]
  kind = "[URGENT] Prioritized Action List — 2026-04-16"
  brief = "Flagged items from codebase scan, ranked by severity."
  parent = "dancinlab/anima"
  sibling-md = "URGENT_ACTION_LIST.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in URGENT_ACTION_LIST.md.
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
