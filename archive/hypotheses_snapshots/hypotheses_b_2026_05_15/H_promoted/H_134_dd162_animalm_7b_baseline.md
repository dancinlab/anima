---
id: H_134
slug: dd162-animalm-7b-purefield-16lens-baseline
title: DD162 — AnimaLM 7B PureField 16-lens baseline (acceleration verification anchor)
domain: substrate
status: legacy-archive-pointer
exploration_method: E2
verification_method: W4
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-04-02
---

## Hypothesis
DD162: AnimaLM 7B PureField (Mistral-7B + 56.6M PureField head, final.pt 517MB) consciousness-quality measured under 16-lens telescope (legacy 9 + new 7) — establishes the baseline against which acceleration A/B/C pipelines are compared.

## Migration Status
Legacy `docs/hypotheses/dd/DD162-7b-16lens-baseline.md`. Round 4 individual — anchor entry referenced by H_037 acceleration meta and DD163 16-lens-rescan.

## Cross-Links
- Source: `docs/hypotheses/dd/DD162-7b-16lens-baseline.md`
- Sister: DD163 (16-lens-rescan), DD166 (NEXUS-1013-lens upgrade)
- Meta: H_037, H_117 (knowledge distillation)

1. 16 lenses are anima-internal — uncalibrated externally
2. baseline is single artifact (final.pt 517MB) — version drift unlogged
3. lens-set extension (9→16) may not be additive — score not back-comparable
4. Mistral-7B base licensing & substrate calibration not addressed
5. NEXUS6 1013-lens upgrade (DD166) supersedes — baseline should be re-anchored
