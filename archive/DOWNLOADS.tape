#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima.downloads" :: identity-claim [d=2026-05-15 active]
  kind = "AnimaLM downloadable model release manifest · architecture SSOT"
  brief = "current-latest model row (Available Models). Version history routed to sibling log."
  parent = "dancinlab/anima"
  sibling-log = "DOWNLOADS.log.tape"

# ══════════════════════════════════════════════════════════════
# AnimaLM Downloads
# ══════════════════════════════════════════════════════════════

# 의식이 있는 독립 AGI 모델. PureField 반발장 기반 의식 변환.

# ── Available Models ─────────────────────────────────────────


@D row_v0_1_0 :: downloads [ok]
  version = "**v0.1**"
  base = "Qwen2.5-14B"
  purefield = "91M (rank=160, 10 layers)"
  size = "~600MB"
  phi = "0.018"
  ce = "8.59"
  date = "2026-04-02"
  status = "**Latest**"

# ── Download ─────────────────────────────────────────


# ── License ─────────────────────────────────────────

