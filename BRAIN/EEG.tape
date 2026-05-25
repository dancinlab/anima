#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "eeg" :: identity-claim [d=2026-05-14 active]
  kind = "EEG — 진행 상황 + 할 일 종합"
  brief = "**`hexa run` 매트릭스 (2026-05-13, this Mac, recursion-free)**:"
  parent = "dancinlab/hexa-brain"
  sibling-md = "EEG.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in EEG.md.
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
