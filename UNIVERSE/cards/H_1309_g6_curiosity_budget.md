---
id: H_1309
slug: 1309_g6_curiosity_budget
title: G6 IDEATION ★ depth-floor dig r2 — curiosity-gated multi-sample budget (gate vs raw budget)
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: 🟠 HONEST-THIN (curiosity GATE load-bearing but bar UNMOVED, c9)
verdict_dir: .verdicts/1309_g6_curiosity_budget/
terminal_verdict: .verdicts/1309_g6_curiosity_budget/result.txt
date: 2026-06-16
---

# H_1309 — G6 IDEATION ★ depth-floor r2: curiosity-gated multi-sample budget

> id 1306 was taken by a concurrent ko-mitosis lane on origin/main → renumbered to H_1309.

## Why (refines H_1305 🟠 THIN)

G6 IDEATION ★ is anima's STARRED gate. H_1305 found the depth-floor THIN: flat ideation
scores FALS=0 (no falsifiable hypothesis); composition (recombination shell) nudged FALS
0.00→0.667 but sub-threshold (M2 FALS≥1 FALSE, M1 DIST≥5 FALSE), controls decisive.

r2 tests ONE NEW ANGLE (a_no_llm_frame_trap — NOT "scale the model"): a **curiosity-gated
multi-sample BUDGET**. Spend MORE DRAWS under a substrate curiosity signal and ask: does it
cross ≥5-distinct AND ≥1-falsifiable, and is it the CURIOSITY GATE or just raw budget?

## Method (FREEZE.txt, frozen-first, c9/p7)

For each of the 5 live G6 `IDEATION_SEEDS`, draw B candidate continuations (budget ladder
B ∈ {1,4,16,64}; each draw a distinct deterministic `seed_rng` = a genuine new sample, same
`gauge_lib._decode` top-k=40 temp=0.7 live G6 path). All arms SELECT from the SAME candidate
pool (only the selection rule differs):

- **B_curiosity** — keep the candidate MAXIMISING curiosity = novelty(corpus-absent content-
  grams) + under-exposure(1 − max jaccard vs running kept set). Reads ONLY substrate state,
  NO injected answer/quality label (p6).
- **SHUFFLE** — random-keep one of the B candidates (SAME budget spent, NO gate). DECISIVE
  control: if random-keep crosses too, the count gain is a SAMPLING ARTIFACT, not curiosity.
- **B_ablate** — curiosity OFF, keep the FIRST candidate (budget collapses to 1).

Score the 5 SELECTED ideas on DIST (distinct coherent, jaccard≤0.5) and FALS (≥1 falsifiable
via the **FROZEN H_1305 `_is_falsifiable` detector reused VERBATIM** — comparator+measurable+
negatable, NEVER an LLM-judge, p7). 3 outer seeds [7,4302,4303]. $0 CPU torch-mouth.

### FROZEN bars (reuse H_1305 thresholds — NOT moved)

- M1 COUNT `DIST(curiosity) ≥ 5` · M2 DEPTH `FALS(curiosity) ≥ 1`
- M4 EARNED-GATE `FALS(curiosity) ≥ FALS(SHUFFLE)+1` (gate beats raw-budget random-keep)
- M5 EARNED-BUDGET `FALS(curiosity) ≥ FALS(B_ablate)+1` (budget beats budget=1)
- MOVED iff (M1 ∧ M2 ∧ M4 ∧ M5) at SOME budget.

## Result (verbatim → .verdicts/1309_g6_curiosity_budget/result.txt)

Detector calibration 10/10 (reused verbatim). Budget ladder COMPLETED to B=__CEILING__
(honest CPU ceiling = B=16; 3 rungs [1,4,16] completed; B=64 ≈ 2 h beyond the envelope and
FALS plateaued 4→16 → stopped, a_cpu_local_no_waiter + a_scale_honest_scope ≥3 rungs). Means
over 3 seeds [7,4302,4303]:

| budget | arm | DIST | FALS | NOVEL |
|---|---|---|---|---|
| 1 | curiosity | 3.0 | 0.0 | 5.0 |
| 1 | SHUFFLE | 3.0 | 0.0 | 5.0 |
| 1 | ablate | 3.0 | 0.0 | 5.0 |
| 4 | curiosity | 4.33 | 0.667 | 18.0 |
| 4 | SHUFFLE | 3.0 | 0.0 | 3.33 |
| 4 | ablate | 3.0 | 0.0 | 5.0 |
| 16 | curiosity | **4.33** | **0.667** | **45.67** |
| 16 | SHUFFLE | 2.33 | 0.0 | 12.0 |
| 16 | ablate | 3.0 | 0.0 | 5.0 |

PER-SEED at B=16 (DIST,FALS): curiosity = (4,1)·(4,0)·(5,1) → **FALS≥1 in 2/3 seeds, DIST≥5
in 1/3**; SHUFFLE = (3,0)·(2,0)·(2,0) → 0/3; ablate = (3,0)·(3,0)·(3,0) → 0/3.

FROZEN MEAN BARS: M1 DIST(cur)≥5 → 4.33 FALSE · M2 FALS(cur)≥1 → 0.667 FALSE · M4
FALS≥SHUF+1 → 0.667 vs 1 FALSE · M5 FALS≥ABL+1 → 0.667 vs 1 FALSE · moved=FALSE · no shuffle
artifact at any budget · curiosity_per_seed_cross=TRUE (shuffle/ablate per_seed_cross=FALSE).

VERDICT: 🟠 HONEST-THIN — the curiosity GATE is LOAD-BEARING (lifts FALS 0→0.667 + NOVEL
5→46 at every budget≥4 while SHUFFLE same-budget random-keep stays FALS=0, NO sampling
artifact) and crosses the depth floor PER-SEED (2/3 seeds FALS≥1, 1/3 DIST≥5 at B=16), BUT
the FROZEN 3-seed MEAN bar M2 (FALS≥1) is UNMOVED. G6 depth stays THIN (bar UNMOVED, c9).

## Reading (honest, c9)

1. **Budget 1 = no selection room**: all three arms identical (DIST 3.0, FALS 0.0). The
   single-draw flat path reproduces the H_1305 depth-floor (FALS 0).
2. **The curiosity GATE is load-bearing, not raw budget** (the central r2 finding): at B=4
   curiosity lifts FALS 0.0→0.667 and NOVEL 5→18, while SHUFFLE (random-keep, SAME budget)
   stays FALS 0.0, NOVEL 3.3 — same draws spent, the gate selects the testable structure the
   random keep does not. SHUFFLE never shows a sampling artifact (it does not cross the floor).
3. **But the floor is NOT cleared on the MEAN** (bar UNMOVED): curiosity FALS plateaus at
   0.667 — going 4→16 draws (4×) raised NOVEL (18→46) but did NOT raise mean FALS (0.667→
   0.667) or mean DIST (4.33→4.33). More curiosity-selected draws surface more novel strings
   but NOT more reliably TESTABLE structure. The depth floor is CAPACITY-limited, not budget-
   limited: a curiosity-selected 303M mouth produces a falsifiable hypothesis SOMETIMES (2/3
   seeds) but not RELIABLY. Capability-vs-scale thesis from the DRAW side — a_no_llm_frame_trap:
   the fix is a STRUCTURE lane (a hypothesis-form scaffold), not more draws and not a bigger net.

## Scope (UNVERIFIED)

DIRECTIONAL torch-mouth mirror — engine-native byte-exact reconfirm = follow-on only if
clean-GREEN (a_engine_native_learning · a_verified_must_wire). Toy 303M / 5 ideation seeds /
3 outer seeds; CPU budget ceiling capped the top rung (B=64 not run). G6 brain wiring
untouched. a_toy_scale_recheck / a_scale_honest_scope apply.

xref: H_1305 (composition r1, same detector reused) · gauge_lib G6 path · MODEL.md G6 ·
a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope ·
a_toy_scale_recheck · p6 · p7 · p8 · c9 · c15.
