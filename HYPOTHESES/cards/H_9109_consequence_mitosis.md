---
id: H_9105
slug: 9105_consequence_mitosis
title: "Consequence-driven mitosis — does REAL-task (exogenous) fitness selection cross the from-scratch pure-split wall where random fitness cannot?"
group: MITOSIS-ENGINE (frontier C2 · session insight = exogenous-consequence channel bolted onto the dead pure-split wall)
campaign: frontier_rebrainstorm C2 (state/frontier_rebrainstorm/BRAINSTORM.md)
terminal_tier: "🔴 SELECTION INERT-TO-HARMFUL — C2 thesis FALSIFIED (engine-native, 2 regimes, no-selection baseline decisive)"
verdict_dir: state/verdicts/9105_consequence_mitosis/
terminal_verdict: state/verdicts/9105_consequence_mitosis/H_9105.txt
wired: none (RED/wall — no GREEN mechanism to wire; a_verified_must_wire fires only on GREEN)
date: 2026-07-03
host: aiden pool, hexa v0.548.0 (byte-identical to local mini — deterministic LCG)
---

# H_9105 — consequence-driven mitosis: exogenous fitness vs random fitness

## Claim / falsifier (frontier C2)

from-scratch PURE-split mitosis is 🔴 TERMINAL (`a_mitosis_train`: gradient/SELECTION absence =
bottleneck). This session's decisive insight: learning/emit walls fall to the DPI meta-law UNLESS
the driving signal carries **exogenous** information the substrate cannot derive internally. C2
bolts the session's **living external selection** onto the dead wall: lineage selection by **REAL
task success (consequence)**; control = **random fitness**. Thesis: if real-task fitness makes
lineage capability **DIVERGE** from random, the pure-split wall's bottleneck was *selection-absence*
(🟢); if INERT, selection can't save it (🔴). This is the FIRST **engine-native** measurement of
consequence-driven mitosis selection — H_1568 tested the same idea DIRECTIONAL numpy-mirror-only,
found INERT, and its card explicitly deferred the engine-native run.

## Method (engine-native · live core/engine_cli.hexa · NO numpy/torch/mirror — grep gate CLEAN)

Load-bearing LIVE core ops: **`immune_embed_key`** (DIM=64 byte-trigram FNV-1a receptive key =
the substrate's own representation) + **`engine_mitosis_tick`** (the p8 growth gate; EVERY cell
birth — novel spawn AND clonal reproduction — passes through it, gated `cfg.mitosis`). Population
bookkeeping (nearest-scan, apoptosis removal, stats) = harness (VAdaptField has no cell-removal op).

**Task** (gives exogenous selection a genuine, non-rigged channel — the novelty vs H_1568, whose
next-byte task had no signal/noise structure to exploit → tied random): a capacity-limited clonal
**classifier** over labeled concept clusters, half SIGNAL (stable ground-truth answer gid%2) half
NOISE (answer flips randomly each occurrence). MAX_CELLS=12 << #clusters forces the population to
CHOOSE which clusters to cover. Cell = (immune_embed_key of birth query, inherited label bit);
prediction = nearest cell's label; correct iff == query's TRUE answer (exogenous). Arms (identical
query stream/seed, MATCHED churn KILL_K=REPRO_K=2, only SELECTION differs): **EXO** (kill bottom-k
by real correct-rate, reproduce top-k), **RAND** (k random), **SHUF** (fitness vs a fixed permuted
cluster→answer map — the DPI/tautology control), **EXO_NOAPOP** (reproduce-only), plus the decisive
**NOSEL** (spawn-only, no selection at all = the actual pure-split floor). 5 seeds; held-out = 100
fresh signal-cluster queries. Two regimes: A balanced 12/12, B noise-heavy 12/36 (maximally favors
apoptosis-enrichment — signal cells are immortal, noise cells churn). Code:
`state/9105_consequence_mitosis/consequence_mitosis.hexa`. Pre-reg: `state/9105_consequence_mitosis/PREREG.md`.

## Verdict (read VERBATIM from state/verdicts/9105_consequence_mitosis/H_9105.txt)

held-out signal accuracy (mean/5 seeds):

| regime | EXO | RAND | SHUF | EXO_NOAPOP | **NOSEL** | B1 EXO−RAND | B2 EXO−SHUF | **EXO−NOSEL (decisive)** |
|--------|----:|-----:|-----:|-----------:|----------:|------------:|------------:|-------------------------:|
| A (12/12) | 0.434 | 0.138 | 0.240 | 0.522 | **0.522** | +0.296 PASS | +0.194 PASS | **−0.088 HARMFUL** |
| B (12/36) | 0.086 | 0.078 | 0.000 | 0.288 | **0.288** | +0.008 FAIL | +0.086 FAIL | **−0.202 HARMFUL** |

B4 data-validity VALID (within-cluster L2 0.078 < FIRE_RADIUS 0.30 < cross-cluster L2 1.412).
cond_acc|fire = 1.0 (regime A) → overall accuracy == distinct-signal-cluster COVERAGE (cross-cluster
keys orthogonal, so a query only ever fires its own cluster's cell). coverage/12: A EXO=4.4 vs NOSEL=6.0;
B EXO=1.2 vs NOSEL=3.0.

**TERMINAL TIER: 🔴 SELECTION INERT-TO-HARMFUL — the C2 thesis (selection was the missing ingredient)
is FALSIFIED.** The pre-registered B1/B2 (EXO vs random/shuffle) PASS in regime A — which would have
cemented a **false 🟢** — but the **no-selection baseline (NOSEL = just let cells spawn) BEATS
consequence-selection in BOTH regimes** (EXO−NOSEL = −0.088 / −0.202). EXO "diverges" from RAND/SHUF
ONLY because random/shuffled churn is **destructive**, not because consequence carries useful info.

## What this means (the c9 / a_break_the_wall finding — load-bearing)

- **EXO_NOAPOP == NOSEL byte-exact in both regimes** → consequence-driven REPRODUCTION has **zero net
  effect**: clonal split can only DUPLICATE an already-covered cluster (H_1310 "split can't target the
  UNCOVERED region"). The one channel selection could use to add capability is inert by construction.
- **Apoptosis is net-DESTRUCTIVE**: killing cells + refilling from a 50/50 (or 25/75) novel stream
  churns away coverage faster than it enriches; even the noise-heavy regime that MAXIMALLY favors
  apoptosis-enrichment (immortal signal cells) makes EXO *worse* than NOSEL, not better.
- The apparent EXO≫RAND divergence is exactly the **DPI trap** this session flagged: a control that is
  actively harmful (random churn) manufactures a false divergence. The stricter, load-bearing control
  (no-selection) — added AFTER B3 exposed NOAPOP==NOSEL, and which makes GREEN HARDER not easier
  (c9-compliant, NOT a bar move) — overturns the naive reading.
- **Reconfirms `a_mitosis_train` from-scratch pure-split wall ENGINE-NATIVE.** The bottleneck was NOT
  selection-absence: exogenous, exploitable, real-task consequence still cannot make pure-split mitosis
  a positive learner because split-reproduction is structurally non-constructive. H_1568 found this
  DIRECTIONAL (numpy); H_9105 confirms it on the live engine AND adds the no-selection baseline that
  H_1568 lacked.

## Frozen bars (PREREG.md — NOT moved; c9)
- B1 DIVERGE : mean(EXO−RAND) ≥ 0.15 (reported verbatim: A PASS +0.296, B FAIL +0.008).
- B2 SHUFFLE : mean(EXO−SHUF) ≥ 0.15 (reported verbatim: A PASS +0.194, B FAIL +0.086).
- B3 APOPT   : mean(EXO−EXO_NOAPOP) ≥ 0.10 (FAIL both: −0.088 / −0.202 — apoptosis HURTS).
- DECISIVE (no-selection): EXO−NOSEL ≥ 0.10 = selection is a positive channel — FAIL both (−0.088 / −0.202).
- Verdict rule as executed: 🟢 needs EXO to clear the no-selection baseline in ≥1 regime — it does not.

## Honest scope
Engine-native TERMINAL (live core/ decode, sha256-verified, aiden pool output byte-identical to local
mini). TOY concept-classification scope (not a 303M production claim). Does NOT touch the compositional-
depth wall (H_1310) — it removes the "maybe selection was the missing lever" escape from
`a_mitosis_train`. Remaining pure-split escape (per the wall): a CONSTRUCTIVE reproduction operator that
places offspring in the uncovered/error region (gradient-like) — i.e. no longer pure split. The living
external-selection lever is closed.
