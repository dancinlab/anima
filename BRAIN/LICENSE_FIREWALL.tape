#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "license_firewall" :: identity-claim [d=2026-05-14 active]
  kind = "License Firewall"
  brief = "hexa-brain is **MIT-licensed**. The `GOOGLE_CONSCIOUSNESS_CHIP.md` survey"
  parent = "dancinlab/hexa-brain"
  sibling-md = "LICENSE_FIREWALL.md"

# ─── §Log (append @A / @D events here, chronological) ────────────────
# 
# Pre-existing log entries live in LICENSE_FIREWALL.md.
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
