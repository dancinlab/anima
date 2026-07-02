---
id: H_1534
slug: 1534_nm_curiosity
title: NEUROMODULATION wall — C4 curiosity-gated acquisition under a store BUDGET (active-sampling lens) 🧱 WALL HOLDS (thin directional lift, DIRECTIONAL)
group: brain-structure-ladder · H_1284 neuromodulation wall-break (census C4)
terminal_tier: 🧱 WALL HOLDS (DIRECTIONAL/numpy) — curiosity gate load-bearing + per-seed consistent but pre-registered GREEN not cleanly cleared (c9, frozen-first)
verdict_dir: state/verdicts/1534_nm_curiosity/
terminal_verdict: state/verdicts/1534_nm_curiosity/H_1534_R1.txt
wired: DIRECTIONAL-mirror (numpy; engine-native R2 = follow-on ING only if clean-GREEN — NOT triggered, WALL)
date: 2026-06-21
---

# H_1534 — neuromodulation wall: C4 curiosity-gated acquisition (active-sampling)

## Why (census C4 — orthogonal lever the 12 prior lenses lacked)

H_1284 NEUROMODULATION is 🧱 (no-free-lunch): a state-driven controller of the
engine's LR / SPLIT_THRESH / abstain never beats a single tuned FIXED operating
point. Four prior census families (controller / capacity / geometry / interference
/ retrieval — 12 lenses) all shared ONE hidden precondition: the store ADMITTED
EVERY FACT (random/full admission). When the store holds everything, selecting WHAT
to store cannot help — structurally why those probes were INERT.

**C4 (active-sampling, Gottlieb & Oudeyer 2018 Nat Rev Neurosci)** adds the missing
precondition: a FIXED store BUDGET N < total facts. A curiosity / info-gain ADMISSION
gate that ADMITS by key-novelty and SKIPS redundant near-collinear duplicates should
spend the scarce budget on DISTINCT facts → higher recall than random admission at the
same budget. HONEST scope (c9): if curiosity only ties random-admission, the wall
EXTENDS to the active-sampling family.

## Method (frozen-first — H_1534_FREEZE.txt pre-registered BEFORE running, p7)

Numpy DIRECTIONAL mirror of `core/engine_cli.hexa` VAdaptField (host has no torch;
`a_engine_native_learning`). Reuses the H_1284 probe's key geometry VERBATIM
(`key_vec` / `fnv1a` / `make_facts`, byte-trigram FNV-1a → DIM-16 unit key,
split-on-novelty TH0=0.30, refine LR0=0.20, abstain 0.45). 30 subjects, store
BUDGET N=18 < 30. Arrival stream = each fact ONCE distinct + 3 near-collinear
DUPLICATES (jitter σ=0.10 → L2≈0.38 > TH0, so a dup SPAWNS its own cell under a
naive admitter, wasting a slot; yet stays near its distinct parent so subject
recall still finds the cluster). Stream shuffled so dups interleave. 3 seeds
[11,22,33], MARGIN 0.05, $0 CPU, deterministic.

**Arms** (same stream + budget): RANDOM (uniform-random admit subset — best
fixed-budget baseline) · CURIOSITY (admit iff novelty > running EMA of seen
novelty; near-dups fall below → SKIPPED; reads ONLY key geometry, NO injected
answer/quality label, p6) · ABL (curiosity OFF → reverts to RANDOM) · SHUFFLE
(gate ON but per-fact novelty scores phase-scrambled → decoupled).

### FROZEN bars (verbatim, NOT moved)

- B1 LIFT `recall(CUR) − recall(RANDOM) ≥ +0.05` on ≥2/3 seeds
- B2 EARNED-ABL `recall(CUR) ≥ recall(ABL)+0.05` AND `|ABL−RANDOM| ≤ 0.03`
- B3 EARNED-SHUF `recall(CUR) ≥ recall(SHUF)+0.05` AND `|SHUF−RANDOM| ≤ 0.03`
- B4 NO-FAB `fab(CUR) − fab(RANDOM) ≤ +0.05`
- 🟢 WALL-BROKEN iff B1∧B2∧B3∧B4; else 🧱 WALL HOLDS.

## Result (verbatim → state/verdicts/1534_nm_curiosity/H_1534_R1.txt)

Means over 3 seeds (recall accuracy / fab):

| arm | acc | fab |
|---|---|---|
| RANDOM | 0.4333 | 0.0296 |
| CURIOSITY | **0.5000** | 0.0296 |
| ABL (curiosity OFF) | 0.4333 | 0.0296 |
| SHUFFLE (scores scrambled) | 0.4000 | 0.0222 |

Per-seed acc [11,22,33]: RANDOM [0.40, 0.50, 0.40] · CURIOSITY [0.467, 0.50, 0.533]
· ABL [0.40, 0.50, 0.40] · SHUFFLE [0.367, 0.433, 0.40]. Lift cur−random = **+0.0667**
mean (per-seed +0.067 / 0.0 / +0.133; CUR ≥ RANDOM on **3/3** seeds). cur−abl +0.0667,
cur−shuffle +0.10.

FROZEN bars: **B1 LIFT ✓** (+0.0667, 2/3 seeds ≥ MARGIN) · **B2 EARNED-ABL ✓**
(cur ≥ abl+0.05 AND abl reverts EXACTLY to random) · **B3 EARNED-SHUF ✗** — primary
clause `cur ≥ shuf+0.05` PASSES (0.50 ≥ 0.40+0.05) but the collapse-band clause
`|SHUF−RANDOM| ≤ 0.03` FAILS by 0.003 (shuffle 0.40 vs random 0.4333 = 0.033 gap) ·
**B4 NO-FAB ✓** (fab equal 0.0296).

**VERDICT: 🧱 WALL HOLDS** (DIRECTIONAL/numpy) — pre-registered GREEN (B1∧B2∧B3∧B4)
NOT met because B3's frozen collapse-band clause missed by 0.003.

## Reading (honest, c9 — frozen-first, NO tune-to-green)

1. **The curiosity ADMISSION gate IS load-bearing under a budget** (the real C4
   finding): curiosity 0.50 > random 0.4333 (+0.0667), CUR ≥ RANDOM on **every**
   seed, and ABL (curiosity OFF) reverts EXACTLY to the random baseline (0.4333) —
   so the lift is the GATE, not the budget. This is the FIRST census candidate to
   produce a coupled, per-seed-consistent directional lift over best-fixed admission:
   the budget precondition (N < total) the 12 prior full-store lenses lacked is the
   regime where active sampling can act.
2. **But the pre-registered GREEN is NOT cleanly cleared** (bar UNMOVED): B3's frozen
   second clause required SHUFFLE to land within 0.03 of random (a "collapse to
   baseline" check); shuffle instead decoupled to 0.40 — *below* random by 0.033,
   overshooting the band by 0.003. SHUFFLE landing below random is in fact *stronger*
   evidence the signal is real (decoupling the novelty score from its fact hurts),
   but the literal frozen bar is not met. Per `a_break_the_wall` / c9, the bar is
   NOT moved post-hoc to manufacture GREEN → terminal **🧱 WALL HOLDS**.
3. **Wall classification (a_break_the_wall taxonomy):** the directional lift is THIN
   (mean +0.0667 on a 30-fact toy) and the GREEN miss is a control-band technicality,
   not a null result. This is a 🟠/🧱 boundary recorded as 🧱 (honest, frozen-first).
   The active-sampling family is NOT inert here (unlike the 12 full-store lenses) —
   it is the most promising un-walled direction, but a single thin DIRECTIONAL toy
   round does not clear the pre-registered GREEN. Follow-on (un-triggered until a
   cleanly-GREEN round): tighten the curiosity signal (per-cluster info-gain vs the
   global EMA), sweep budget N and dup_factor, re-freeze B3 as the single primary
   clause `cur ≥ shuf+MARGIN` BEFORE running, then engine-native R2 reconfirm.

## Scope (UNVERIFIED)

DIRECTIONAL numpy mirror — engine-native byte-exact reconfirm = follow-on ONLY if a
later round is clean-GREEN (`a_engine_native_learning` · `a_verified_must_wire`; NOT
triggered — WALL). TOY 30 subjects / budget-regime only / 3 seeds; scale / real-corpus
/ longer streams / engine-transfer UNVERIFIED (`a_scale_honest_scope` ·
`a_toy_scale_recheck`). RED/🧱 ⇒ NO wiring.

## Cross-links

H_1284 (neuromodulation wall, parent) · H_1422 (state-contingent NM) · H_1309
(curiosity-gated budget, G6 ideation — same curiosity lever, different gate) · H_1227 ·
H_1231 (immune key geometry reused) · H_1529 (nm-ideation wall, prior round) ·
`a_break_the_wall` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p6 · p7 · p8 · c9 · c15.
