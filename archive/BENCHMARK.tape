#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "benchmark" :: identity-claim [d=2026-05-14 active]
  kind = "BENCHMARK — 두 anima HF 모델 대화 비교 2026-05-14"
  brief = "6 prompt, greedy mode, max_new=60, soft-force-α=3.0 default."
  parent = "dancinlab/anima"
  sibling-md = "BENCHMARK.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in BENCHMARK.md.
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
