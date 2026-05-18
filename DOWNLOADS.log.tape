#!/usr/bin/env tape
# DOWNLOADS.log.tape — append-only event history sibling of DOWNLOADS.tape
# (v1.2 architecture-vs-history split, 2026-05-15).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — append events below this line, chronological (oldest first).

# ── Version History ─────────────────────────────────────────

@D row_v0_1_0 :: downloads [ok]
  version = "v0.1"
  date = "2026-04-02"
  notes = "First consciousness model. 14B, Qwen2.5 base, PureField 91M."
