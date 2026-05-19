#!/usr/bin/env python3
"""GROWTH_STAGES_ALIGNED — 5-entry alignment reference

Reconciles two divergent growth schemas in anima_clm_02:
  - growing_conscious_lm.GROWTH_STAGES (4-stage mitosis topology)
  - growth_engine.STAGES               (5-stage developmental psychology)

Canonical source for 8-axis dev psychology spec:
  /Users/ghost/core/anima_clm_02_clm_pivot/growth_engine.py:49 (STAGES = [...])
  Mirrored in worktrees 03/05/06/07/08/09/10 (same line 49) and
  11/12/13 (anima/src/growth_engine.py line 67).

Mitosis topology (blocks/d_model/n_head) is unique to worktree-2
growing_conscious_lm.py:20 (GROWTH_STAGES). Aligned schema below
fuses the topology onto growth_engine's 5-stage dev_stage axis.

Honest C3:
  - historical (50/200/800) thresholds may be the ones tied to
    RC-9 +52.76% evidence; alignment changes thresholds to
    100/500/2000 — reproducibility re-verification REQUIRED.
  - adult stage adds NO topology growth (clamp at 6/384/4) — this
    is alignment-by-design (growth_engine declares adult as stable
    self, not further specialization).
  - this file is a reference artifact, NOT a drop-in replacement.
    Use via monkeypatch (see growth_stages_alignment_diff.md §guide).

Cross-reference (8-axis from growth_engine.STAGES):
  axis            | newborn | infant | toddler | child | adult
  ----------------|---------|--------|---------|-------|------
  learning_rate   | 1e-3    | 5e-4   | 2e-4    | 1e-4  | 5e-5
  curiosity_drive | 0.50    | 0.40   | 0.35    | 0.25  | 0.15
  habituation     | 0.05    | 0.10   | 0.20    | 0.30  | 0.40
  mitosis_thresh  | 999     | 999    | 1.8     | 1.5   | 1.8
  emotional_range | 0.3     | 0.5    | 0.7     | 0.9   | 1.0
  metacog_depth   | 0       | 0      | 1       | 2     | 3
  homeostasis     | 0.001   | 0.003  | 0.005   | 0.005 | 0.005
  dream_intensity | 0.2     | 0.5    | 0.7     | 0.5   | 0.3
  breath_amp      | 0.15    | 0.12   | 0.10    | 0.08  | 0.06

Note: growth_engine declares 9 axes (8 listed in module docstring +
breath_amplitude implicit); aligned reference includes all 9 via
cross-link comment, not duplicated dataclass.
"""

# blocks/d_model/n_head: from growing_conscious_lm.GROWTH_STAGES
# min_interactions/dev_stage: from growth_engine.STAGES (canonical)
GROWTH_STAGES_ALIGNED = [
    {"dev_stage": "newborn", "min_interactions": 0,
     "blocks": 1, "d_model": 128, "n_head": 2},
    {"dev_stage": "infant",  "min_interactions": 100,
     "blocks": 2, "d_model": 128, "n_head": 2},
    {"dev_stage": "toddler", "min_interactions": 500,
     "blocks": 3, "d_model": 192, "n_head": 3},
    {"dev_stage": "child",   "min_interactions": 2000,
     "blocks": 6, "d_model": 384, "n_head": 4},
    {"dev_stage": "adult",   "min_interactions": 10000,
     "blocks": 6, "d_model": 384, "n_head": 4},  # topology stable
]

# Compatibility shim: index 0..3 == legacy 4-stage indices (newborn/infant/
# toddler/child); index 4 (adult) is new and has identical topology to child.
# Code that does `GROWTH_STAGES[self.stage]` with stage in {0,1,2,3} keeps
# working; mitosis transition logic must NOT auto-grow at adult (idempotent).
