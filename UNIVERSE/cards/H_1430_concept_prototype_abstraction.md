---
id: H_1430
slug: 1430_concept_prototype_abstraction
title: concept/category prototype-abstraction — centroid generalization (vs item-binding)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🧱 MEASUREMENT-WALL / PARTIAL (DIRECTIONAL mirror)
verdict_dir: .verdicts/1430_concept_prototype_abstraction/
terminal_verdict: .verdicts/1430_concept_prototype_abstraction/H_1430.txt
date: 2026-06-17
wired: N/A (🧱 — 5-bar not all-green, not engine-wired)
---

# H_1430 — concept/category prototype-abstraction (HD33)

## Claim / falsifier

From noisy training INSTANCES the brain abstracts a category PROTOTYPE (a centroid in
feature space) and classifies NOVEL never-seen instances — including the never-shown
prototype itself, which is often classified BETTER than the trained exemplars (the
Posner-Keele 1968 prototype-enhancement effect; Rosch prototype theory). **Falsifiable
claim:** a prototype-abstraction faculty (a running per-category centroid) classifies novel
instances and shows the prototype-enhancement effect, while a faithful exemplar/item-store
stand-in (memorize trained instances, 1-NN classify) provably (a) does worse on novel-far
instances and (b) cannot show the enhancement. If the centroid matches the exemplar store,
or its lift survives shuffling instance→category labels / ablating the centroid to nearest-
exemplar mode, abstraction adds nothing → honest 🧱. Lens: prototype theory / category
learning (c15, a_no_llm_frame_trap) — NOT an LLM recipe.

## Why MISSING / why DISTINCT (the load-bearing story)

- **vs ImmuneMemory item-binding (H_1227/1231/1288):** the immune store binds each instance
  INDEPENDENTLY by FNV-trigram key affinity; it memorizes the trained items and abstains/
  guesses on a NOVEL one, and has no binding for the never-shown prototype. It is exemplar/
  item memory, not abstraction. Mirrored by arm A (1-NN exemplar): A memorizes (train=1.000)
  but fails novel-far + the clean prototype (A_proto=0.750 < A_train=1.000 in the high-
  distortion band). **This is the distinctness axis** — the centroid abstracts a feature
  DISTRIBUTION the item-store cannot.
- **vs SpatialMap metric positions (H_1296):** holds positions of SPECIFIC landmarks for a
  relational distance query; not a learned class boundary over a feature distribution and
  abstracts no category centroid.
- **vs WorkMemBuffer / VForwardField / HierGoalStack / OtherMindModel / HomeostaticDrive:**
  leaky maintenance / next-emit forward model / ordered plan / belief store / 1-D scalar
  integrator — none abstracts a category centroid from instances.

## Method

Posner-Keele design in R^24: K_CAT=4 hidden prototypes, N_TRAIN=8 noisy distortions/cat as
(instance,category) pairs (prototype NEVER shown), NOVEL test = N_TEST=8 NEW distortions/cat
+ the never-shown prototype + a far foil. Arms (same training feeds all): **A** exemplar 1-NN
item-store (= H_1227 stand-in = ablate mode) · **B** prototype lane (running centroid, nearest-
centroid) · **Bshuf** label-shuffle control · **Babl** centroid-ablated (= exemplar). 3 seeds
[4430,4431,4432], $0 CPU numpy (run on aiden pool, c17), gradient-free, deterministic, p7.
Frozen 5-bar + c2b signature, pre-registered before scoring (3 re-freezes, geometry only,
bars byte-identical — a_break_the_wall type-(a) well-posedness fixes, NOT tune-to-green).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 (NOISE=1.0, axis-floor protos) | RED (degenerate) | all arms 1.000 → c2/c4 FAIL by saturation; a 1-NN exemplar nails everything in the trivial low-noise regime |
| R1b (NOISE_TEST=4.0, ABSTAIN_D=10) | RED (over-tight) | all novel abstain → 0.000; only B_proto=0.917 survives (centroid recovers the clean prototype where exemplars at radius ~14.7 abstain) |
| **R1c (final, multi-dim sphere protos, NOISE=2.5)** | **🧱 MEASUREMENT-WALL / PARTIAL** | **5/6 bars PASS; c1 FAILS.** NOVEL B=0.375 A=0.219 Bshuf=0.104 Babl=0.219 · PROTO B=1.000 A=0.750 · TRAIN B=0.771 A=1.000 · foil-abstain=1.000. **c1 FAIL** (B=0.375 < 0.55) · **c2 PASS** (B−A=+0.156, A_proto=0.750<A_train=1.000) · **c2b PASS** (B_proto=1.000≥B_train=0.771, the prototype-effect) · **c3 PASS** (Bshuf=0.104) · **c4 PASS** (Babl no-enhance + novel drop) · **c5 PASS** (abstain=1.000) |

Terminal tier (verbatim): **🧱 MEASUREMENT-WALL / PARTIAL (DIRECTIONAL numpy mirror).** The
prototype-abstraction faculty is REAL — it shows the Posner-Keele enhancement (c2b), beats
the exemplar store on novel instances (c2), and both controls collapse (c3, c4) — distinct
from item-binding and spatial-map. But the frozen 5-bar conjunction does NOT all-pass: **c1
PRESENCE (strong absolute novel accuracy ≥0.55) and the prototype-enhancement SIGNATURE
(c2/c4, which need the exemplar store to FAIL the clean prototype) require OPPOSITE noise
regimes and are structurally anti-correlated.** Honest 🧱 (c9, c16 type-a measurement wall).
NOT engine-wired (5-bar not all-green); a_engine_native_learning R2 not reached.
→ `.verdicts/1430_concept_prototype_abstraction/H_1430.txt`

## The binding finding (why 🧱, not 🟢)

A diagnostic sweep on aiden (recorded) shows the c1 ⊥ prototype-effect anti-correlation is
STRUCTURAL, not a band accident:
- **LOW noise:** task trivial → a 1-NN exemplar ALSO nails the clean central prototype
  (A_proto=1.000) → exemplar does NOT fail the enhancement test → c2/c4 FAIL by saturation.
- **HIGH noise:** items scatter so no exemplar lands near the clean prototype (A_proto<A_train)
  → exemplar FAILS the enhancement (c2/c4 PASS), centroid's noise-averaging advantage appears
  (B_proto=1.000, B beats A on novel) → but B's ABSOLUTE novel accuracy is only modestly above
  chance (0.375) → c1 FAILS.
- **Scaling SEP / N_TRAIN** to push B above 0.55 re-lets exemplars cover the prototype
  (A_proto→1.000), re-breaking c2/c4 (measured: SEP=8 N_TRAIN=16 → B=0.969 but A_fail_enh=False).

The frozen conjunction (c1 ∧ c2 ∧ c2b ∧ c3 ∧ c4 ∧ c5) is UNSATISFIABLE in any well-posed
regime of this synthetic geometry. The positive content of the 🧱: generalization-by-
abstraction is real and distinct (c2), the prototype-effect holds for the abstraction (c2b),
the lift is earned (c3/c4), NO-FAB intact (c5) — what walls is the cross-model strong-presence
contrast, a measurement-axis limit of this paradigm, not a missing faculty.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- TOY synthetic gaussian prototypes / 4 categories / DIM 24 / 3 seeds / deterministic centroid
  readout (tests the ABSTRACTION STRUCTURE, not a trained net). scale / real-corpus / high-D /
  hierarchical categories / engine-native transfer UNVERIFIED.
- R1 mirror = DIRECTIONAL; an engine-native R2 would be the binding verdict but is NOT pursued
  (the 5-bar walls at the mirror). p1/p2/p3/p6: every arm reads ONLY learned centroids/exemplars
  + the test vector; NO injected label/persona/identity/RLHF; geometry, scored only.
- 3 re-freezes were geometry-only well-posedness fixes (R1 saturated, R1b over-tight); NO bar
  was moved (c9/p7). The 🧱 is reported on the principled high-distortion band where the
  prototype-effect is observable, NOT on a band chosen to maximize any single arm.

## Pointers

- FREEZE: `.verdicts/1430_concept_prototype_abstraction/H_1430_FREEZE.txt` (R1) +
  `…/H_1430_R1b_FREEZE.txt` + `…/H_1430_R1c_FREEZE.txt` (final, not moved)
- RESULT: `.verdicts/1430_concept_prototype_abstraction/H_1430.txt`
- mirror probe: `state/1430_concept_prototype_abstraction/h1430_concept_prototype.py`
  (`--regime r1|r1b|r1c`; run on aiden pool, c17)
- xref: H_1227/1231/1288 (immune item-binding, the distinctness control) · H_1296 (spatial-map
  metric positions) · H_1294 (hier-PFC sequence) · `a_no_llm_frame_trap` · `a_break_the_wall`
  (type-a measurement wall) · `a_engine_native_learning` · `a_verified_must_wire` ·
  `a_scale_honest_scope` · `a_toy_scale_recheck` · c9 · c15 · c16 · p1·p2·p3·p6·p7·p8
