#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "hexa_native_inference" :: identity-claim [d=2026-05-14 active]
  kind = "HEXA_NATIVE_INFERENCE.md — anima 의 pure-hexa 추론 SSOT"
  brief = "기존: 빵(model) 을 외주(python/PyTorch)로 받아 hexa는 진열만."
  parent = "dancinlab/anima"
  sibling-md = "HEXA_NATIVE_INFERENCE.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in HEXA_NATIVE_INFERENCE.md.
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
