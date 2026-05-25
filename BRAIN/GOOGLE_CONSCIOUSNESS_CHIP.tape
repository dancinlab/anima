#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "google_consciousness_chip" :: identity-claim [d=2026-05-14 active]
  kind = "구글 투자 '의식 이동 / 디지털 칩' 회사 리서치 — 심층판"
  brief = "\"의식 이동\" 전체 파이프라인"
  parent = "dancinlab/hexa-brain"
  sibling-md = "GOOGLE_CONSCIOUSNESS_CHIP.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in GOOGLE_CONSCIOUSNESS_CHIP.md.
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
