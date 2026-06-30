---
id: Hc_675
slug: hxc-text-heavy-mixed-5pp-combined-lever-clear-80pct
title: text-heavy +5pp + mixed +5pp 결합 = aggregate +2.7pp, 78.65% v8 strengthen gate (현 -2.41pp) clear + 80% Pareto 약 ~1pp 접근
domain: hxc-deploy
status: candidate-unverified
source_doc: docs/hxc_text_heavy_ceiling_advance_candidates_2026_04_28.md
source_lines: 16-65
promoted_at: 2026-05-11
linked_h: Hc_657 (wire ceiling), 53c711eb 78.05%, d631a902 A18 v3-o2 text-heavy 49.09%, Shannon H_4 0.813 b/B
notes: DESIGN-ONLY scout (no impl/commit). bottleneck class arithmetic: text-heavy 23.99% byte share + mixed ~30% share = combined +2.7pp aggregate. A26 sparse PPM-D RETIRED (91MB > raw 42 200MB jetsam).
---

## Hypothesis
text-heavy class (현 49.09% saving on 5MB sample, 23.99% byte share, gap 30.91pp to 80% class) 와 mixed class (현 58.49%, ~30% byte share, gap 21.51pp) 동시 +5pp lift 시 aggregate 76.24% + 2.7pp = 78.94% — 78.65% v8 strengthening gate clear + 80% Pareto frontier 1pp 안 접근. NEW entropy-coder paradigm (현 catalog A1-A26 absent) 으로만 가능. json-heavy 94.38% 포화 / small-file 0% passthrough = 추가 lever 부재.

## Falsifiable Tests
- F-class-lift-1: text-heavy +5pp 실측 (현 49.09% → ≥54%)
- F-class-lift-2: mixed +5pp 실측 (현 58.49% → ≥63.5%)
- F-class-lift-3: combined +2.7pp aggregate 정합 (수치 product 검증)
- F-paradigm: 신규 entropy-coder paradigm (CM, DMC, BWT+LZ 등) 가 A1-A26 보다 우월

## Migration TODO
- [ ] CM (context mixing, paq-style w/o cmix-ban A28 위반 회피)
- [ ] DMC (Dynamic Markov Coding)
- [ ] BWT + LZ hybrid (Burrows-Wheeler)
- [ ] 1-2 candidate next-cycle dispatch + falsifier preregister
- [ ] raw 42 jetsam ≤200MB constraint check
