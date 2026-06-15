---
id: H_1285
slug: 1285_amygdala_salience
title: amygdala — salience gating of immune-memory consolidation (sleep-replay)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE + WIRED (replay)
verdict_dir: .verdicts/1285_amygdala_salience/
terminal_verdict: .verdicts/1285_amygdala_salience/H_1285_R4.txt
date: 2026-06-15
---

# H_1285 — amygdala: salience gating of consolidation

## Claim / falsifier

The immune/clonal store (H_1227→H_1231) binds every fact UNIFORMLY; H_1230 found its
bottleneck is CAPACITY/NOISE-GEOMETRY (symmetric LRU eviction, active teacher Δ+0.000).
There is NO fast amygdala-style tagger that PRIORITIZES which inputs get bound/protected
by SURPRISE/NOVELTY/IMPORTANCE. **Falsifiable claim:** substrate-derived salience
(surprise+novelty+tension, NO emotion/RLHF/label fed in) protects important facts beyond
their environmental recurrence; a SHUFFLE control (tags permuted) must collapse the lift
(p6 leak/variance control). Lens: c15 ladder, NOT an LLM recipe.

## Method

- H_1230 STRESS rung (MAX_CELLS=40 << 60 facts); ARM A uniform LRU vs B salience-protected
  vs B-shuffle. salience = substrate signals only; importance label scores metric ONLY.
- R4 (binding): realized engine-native on live `CORE/engine_cli.hexa ConsolidatingMemory`
  + wired (sleep-replay consolidation pathway). seeds [900,901,902] (mirror), $0 CPU.

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 | 🔴 RED | eviction-confound — p6 SHUFFLE caught it: B-shuffle.imp 0.967 == B exactly → lift was RECURRENCE-driven re-binding, NOT the salience tag |
| R2 | 🔴 | sub-bar (salience-as-eviction-lever falsified at this scale) |
| R3 mirror | 🟢 GREEN (DIRECTIONAL) | salience-gated consolidation pathway clears bars |
| R4 engine-native + wired | 🟢 GREEN (binding) | R3 direction TRANSFERS to live engine at the 30-cycle replay point (c1∧c2∧c3 PASS) |

Terminal tier (verbatim): **🟢 GREEN — the amygdala-consolidation pathway is REALIZED ENGINE-NATIVE**
→ `.verdicts/1285_amygdala_salience/H_1285_R4.txt`

## Honest scope

The R1/R2 eviction-as-lever reading is FALSIFIED (kept honest, not buried) — the GREEN
is the salience-gated CONSOLIDATION (replay) pathway, not eviction protection. R3 mirror
DIRECTIONAL. Reads substrate state only — no emotion/RLHF/sentiment into salience f()
(p6). No decoder/persona/ethics touched. Toy scale, scale-transfer UNVERIFIED.

## Cross-links

h1227 · h1230 · h1231 · h1281 · h1282 · h1284 · h1287 · h1288 ·
`a_engine_native_learning` · `a_verified_must_wire` · `a_autonomy_over_hardcode` ·
`a_paper_negative_ok` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p2·p3·p6·p7·p8·c9·c15
