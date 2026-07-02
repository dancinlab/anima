---
id: H_1429
slug: 1429_transitive_inference
title: transitive inference — serial-order premise-integration (A>B, B>C ⊢ A>C) vs item/given-order/metric
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
wired: engine-native (live TransOrder lane in CORE/engine_cli.hexa + smoke cases 159-165; full engine_cli_smoke end-to-end gated by a pre-existing host-wide hexa toolchain bug — ING follow-on)
verdict_dir: .verdicts/1429_transitive_inference/
terminal_verdict: .verdicts/1429_transitive_inference/H_1429.txt
date: 2026-06-17
---

# H_1429 — Transitive inference / serial-order premise-integration (HD34)

## Claim / falsifier

Every prior lane either MEMORIZES the facts it is given (ImmuneMemory), is HANDED its
order (HierGoalStack), or stores a GIVEN metric (SpatialMap) — none INTEGRATES disjoint
adjacent ordinal premises into a unified order and infers an UNOBSERVED relation.
**Falsifiable claim:** a transitive-inference faculty, shown ONLY the adjacent premises
A>B, B>C, C>D, D>E, integrates them into a latent 1-D rank and answers the NEVER-PRESENTED
non-adjacent pairs (A>C, A>D, B>D, B>E, C>E) well above chance; a faithful item/episodic
store (memorize the presented pairs, answer only an exact bound pair) provably ABSTAINS
on every unobserved pair → at/below chance. If the integration lane matches the item
store (or its lift survives flipping the premise directions / ablating the rank to per-pair
lookup), integration adds NOTHING → honest 🧱 (subsumed). Lens: Bryant & Trabasso 1971;
hippocampal relational integration (Dusek & Eichenbaum 1997); the symbolic-distance effect
(c15, a_no_llm_frame_trap) — NOT an LLM recipe.

## Why MISSING / why DISTINCT (the load-bearing story — c2 vs EVERY nearest lane)

- **vs ImmuneMemory item-binding (H_1227/1231/1288) — the load-bearing distinctness:** the
  immune store binds each presented pair INDEPENDENTLY by FNV-trigram key affinity; on an
  UNOBSERVED pair no key matches → it ABSTAINS. Mirror: item-store unobserved-acc **0.000**
  (abstains on all 15 non-adjacent pairs); the integration lane **1.000**. SAME premises,
  the lane adds the integrated rank.
- **vs HierGoalStack given-order (H_1294):** an ordered plan's order is HANDED IN (the
  subgoal list is the input); it executes a pointer over a given sequence and answers
  "which subgoal next", never "is X above Y" for an unobserved pair. TransOrder INFERS the
  order from disjoint local premises — case 159 ranks the GLOBAL endpoints A/E from
  LOCAL-only premises, which no handed-in pointer plan performs.
- **vs SpatialMap metric (H_1296):** a directly-STORED metric (given coordinates) is not a
  rank INFERRED from ordinal comparisons; no coordinates exist here, only "X>Y" premises.

## Method

7 opaque tokens / episode with a HIDDEN linear order; ONLY the 6 adjacent ordered premises
are presented. Queries split: 6 OBSERVED-adjacent (sanity, both arms recall) · 15 UNOBSERVED
non-adjacent (the falsifier) · a FAR-FOIL with an unknown token (NO-FAB). ABSTAIN counts as
INCORRECT on the accuracy bar (a conservative floor; the item store scores 0.000). Arms:
A ITEM-STORE (faithful immune stand-in, the live-engine analogue) · B TRANSITIVE-INFERENCE
(integrate premises → latent rank → compare) · Bshuf (flip each premise direction p=0.5,
re-integrate) · Babl (integration disabled → per-pair lookup). 3 seeds [4429,4430,4431],
30 episodes/seed, $0 CPU, gradient-free, p7, deterministic. Frozen bars c1–c5 in the FREEZE.

## Verdict by round

| round | tier | key numbers (UNOBSERVED-pair falsifier) |
|-------|------|------------------------------------------|
| R1 mirror | 🟢 GREEN (DIRECTIONAL) | B=1.000 · A=0.000 · Bshuf=0.433 · Babl=0.000 · B−A=+1.000; OBS A=B=1.000 (both recall premises); far-abstain 1.000; symbolic-distance curve d2..d6 all 1.000 (NON-GATING). c1 PRESENCE B−chance≥0.30 (each+mean, +0.500) · c2 DISTINCT B−A≥0.30 & A≤0.60 · c3 SHUFFLE Bshuf−chance≤0.10 (−0.067) · c4 ABLATE Babl≤A+0.10 · c5 NO-FAB abstain≥0.90 — all PASS. Deterministic run1==run2 (md5-identical, PYTHONHASHSEED-independent). |
| R2 engine-native | 🟢 GREEN (binding) | live `TransOrder` lane (`CORE/engine_cli.hexa` § TRANSITIVE-INFERENCE): the 5 frozen bars reproduced as deterministic hexa assertions on the live lane functions — 159 observed recall · 160 infers A>C,A>D,A>E,B>D,B>E,C>E (order-independent) · 161 item-store answers observed / ABSTAINS unobserved · 162 shuffle breaks the far order · 163 ablate → item-store floor · 164 NO-FAB on unknown token · 165 infers global endpoints from local-only premises. **7/7 PASS, RC=0, deterministic (md5-identical run1==run2)** on summer. |

Terminal tier (verbatim): **🟢 GREEN (ENGINE-NATIVE)** — a premise-integration faculty
infers the unobserved non-adjacent order that item-binding/given-order/metric provably
cannot; both controls collapse; lane wired Ψ-disjoint. → `.verdicts/1429_transitive_inference/H_1429.txt`
+ `.verdicts/1429_transitive_inference/H_1429_R2_engine_native.txt`
(frozen bar `…/H_1429_FREEZE.txt`, not moved).

## Wire status (a_verified_must_wire 4-rung ladder)

1. **DIRECTIONAL mirror GREEN** ✅ — 5/5 bars, 3 seeds, deterministic.
2. **ENGINE-NATIVE re-verify** ✅ — the live `TransOrder` lane functions reproduce the
   frozen bars as hexa assertions (RC=0, deterministic, summer).
3. **live CORE wire-in** ✅ code landed — `CORE/engine_cli.hexa` § TRANSITIVE-INFERENCE
   (struct `TransOrder` + `trans_order_new`/`_new_ablated`/`_premise`/`_integrate`/
   `_higher`/`_item_higher`/`_shuffle`/`_count`) + `engine_cli_smoke.hexa` cases 159-165.
   ⚠ FULL `engine_cli_smoke` END-TO-END RC=0 is BLOCKED by a PRE-EXISTING host-wide hexa
   toolchain bug: the released `hexa 0.1.0-dispatch` binary on BOTH pool hosts (summer AND
   aiden) crashes at case_10 (`wm_buffer_new`, WorkMemBuffer) with "cannot multiply
   non-numeric operand (tag 24 * tag 24)" — an x86_64-linux HexaVal int-tag bug. The
   PRISTINE origin/main smoke fails IDENTICALLY at case_10 → the blocker is the toolchain,
   NOT this lane (type-(c) INFRASTRUCTURE wall, a_break_the_wall; NO bar moved). The
   standalone lane harness (`state/.../h1429_transorder_standalone.hexa`, 7/7 RC=0) PROVES
   the wired lane functions are engine-native correct — the smoke cases are byte-identical
   calls to the same functions. Filed to `hexa-lang/inbox/patches/`. ING follow-on.
4. **ARCHITECTURE.json lockstep** ✅ — CORE node "🪜 Transitive inference — TransOrder" added
   + the engine_cli.hexa §-note lane list updated.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- **B=1.000 is SATURATED = an EXISTENCE-PROOF** (the lane CAN integrate), not an effect-size.
  The DISCRIMINATORS carry the dissociation: item-store 0.000 (abstains on every unobserved
  pair), shuffle 0.433≈chance, ablate 0.000 — all at/below the chance band, so saturation
  does not undermine the dissociation (the lift IS the integrated rank).
- TOY: 7 items / 30 episodes / 3 seeds / 1 paradigm / opaque tokens; scale + paraphrase +
  real-corpus orderings + longer chains + partial/noisy premises UNVERIFIED.
- p1/p2/p3/p6: reads ONLY the presented ordinal premises; NO label/persona/identity/RLHF.
  The hidden order is a TASK structure, scored only.

## Pointers

- FREEZE: `.verdicts/1429_transitive_inference/H_1429_FREEZE.txt`
- RESULT (R1): `.verdicts/1429_transitive_inference/H_1429.txt`
- RESULT (R2 engine-native): `.verdicts/1429_transitive_inference/H_1429_R2_engine_native.txt`
- mirror probe: `state/1429_transitive_inference/h1429_transitive_inference.py`
- engine lane: `CORE/engine_cli.hexa` § TRANSITIVE-INFERENCE · smoke `CORE/engine_cli_smoke.hexa` cases 159-165 · standalone lane harness `state/1429_transitive_inference/h1429_transorder_standalone.hexa`
- xref: H_1227 (immune item-binding, nearest distinctness) · H_1294 (HierGoalStack given-order) ·
  H_1296 (SpatialMap metric) · sibling brain-lanes H_1427/1428/1430 · `a_no_llm_frame_trap` ·
  `a_engine_native_learning` · `a_verified_must_wire` · `a_autonomy_over_hardcode` · c9 · c15 · p1·p2·p3·p6·p7
