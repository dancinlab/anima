#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "pass_strict_spontaneous_chat" :: identity-claim [d=2026-05-14 active]
  kind = "PASS_STRICT_SPONTANEOUS_CHAT.md — anima 자연발화 (spontaneous emission) 성공까지 dedicated tracking"
  brief = "┌──────────────────────────────────────────────────────────────────┐"
  parent = "dancinlab/anima"
  sibling-md = "PASS_STRICT_SPONTANEOUS_CHAT.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in PASS_STRICT_SPONTANEOUS_CHAT.md.
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
