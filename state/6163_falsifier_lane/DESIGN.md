# H_6163 — engine-native G6 falsifier-lane: build + measurement design

## Why (grounded)
G6 (ideation) is a trunk-objective wall on the DECODE axis: ideas go novel (dist>=5) but
falsifiability stays 0. H_1590 (decode scaffold) 🔴 and H_1836 (revise-loop) 🧱 both failed on
that decode axis. Si2024 (2409.04109) diagnoses the LLM ideation bottleneck as **diversity +
self-evaluation**, NOT decode. H_6163 tests the orthogonal VERIFY-substrate axis: a separate
engine-native falsifier lane, DISJOINT from the emit-drive lane (a_substrate_disjoint,
§ImmuneMemory G5-gate pattern), that scores a generated idea for falsifiability WITHOUT an LLM-judge.

This is complementary to the parallel E1/G1 track (#3018 trunk-learnability GO): E1 is the G1
recombination objective; H_6163 is the G6 falsifiability substrate. Non-colliding lanes.

## Mechanism (substrate-first, NOT an LLM trick)
An idea is FALSIFIABLE iff the substrate can produce a **discriminating predicate** C: a condition
the idea predicts, whose negation would refute it. The falsifier lane, given an idea's engine
representation h(idea), emits a candidate predicate vector p and a polarity — engine-native, from the
same 303M trunk state, but on a lane wired disjoint from emit/Ψ (mouth reads only).

Engine-native fals score (no LLM-judge, no perplexity — p7):
- `discriminating(idea)` = the lane's predicate p is (a) IDEA-DEPENDENT: cos(p, h(idea)) separates
  the true idea from a shuffled/permuted idea by a margin, AND (b) NON-VACUOUS: p is not the lane's
  constant/mean output (contrast against a null idea). Both are contrastive margins, not absolute
  scores (measurement-metalaw: emergence is the delta, not the value).
- G6 fals rate = fraction of generated ideas with `discriminating(idea)` true.

## Frozen bar (from the H_6163 card · unchanged · tune-to-green forbidden)
- SUPPORT ⟺ falsifier-lane ON lifts engine-native G6 fals rate 0 → >0, AND lane-OFF ablation
  collapses it back to ~0 (lane is causal), AND the emit-drive lane is byte-identical ON vs OFF
  (disjointness proven, like L5 hippo wiring), AND shuffled-idea control does not pass discriminating.
- 🧱 NOT-SUPPORTED ⟺ LIFT 0 (lane ON fals still ~0) → G6 is a deeper wall (decode AND verify both
  fail), consistent with H_1590 capacity-wall.
- Measurement = engine-native `core/` `.hexa` decode = TERMINAL; numpy/torch mirror = DIRECTIONAL
  (a_engine_native_learning). Heavy 303M on pool (summer/aiden), never mini (swap-OOM).

## $0 toy pre-gate (BEFORE any 303M GPU — the go/no-go)
On toy ByteGPT-generated ideas ($0, mini-safe, no 303M): wire the toy falsifier lane and test whether
it raises toy fals rate 0 → >0 with lane-OFF collapsing to 0, on frozen toy reps. This is the analog
of every prior STEP-0 gate (§4, E1, F2): a cheap decisive check that the lane can produce a
discriminating predicate AT ALL before committing 303M pool GPU.
- toy PASS (lift + ablation-collapse + shuffle-control) → 303M pool build justified.
- toy LIFT 0 → 🧱 at $0 (the verify-substrate cannot manufacture falsifiability from the reps) →
  G6 deeper-wall supported without GPU spend; matches the DPI-wall family.

## Build (if the toy pre-gate clears)
1. `core/` falsifier lane: additive-only op reading final-LN hidden of a generated idea, emitting the
   predicate vector p — wired DISJOINT from emit-drive/Ψ (ON==OFF byte-identical on the emit path, the
   L5-hippo disjointness proof). numpy twin for `anima evaluate --py`.
2. Engine-native G6 eval extended with the fals-rate metric (discriminating margin, shuffle control,
   lane-OFF ablation). `anima evaluate --py <clm>` single path (a_eval_py_canonical).
3. Pool 303M run (summer/aiden RTX5070, owned pool, no rent) → engine-native fals rate, ON vs OFF.

## Cost / dependency
- $0 toy pre-gate: mini, no model load, immediate.
- 303M build+measure: owned-pool GPU (no rent, owner GPU-go per a_fire_autonomous fleet caveat).
- Depends only on: toy pre-gate clearing + core/ lane wiring. Independent of the E1/G1 track.

## Honest scope
A SUPPORT would be the first non-decode G6 lift (falsifiability via a verify-substrate). A 🧱 would
close G6 on the verify axis too, converging with the decode-axis walls (H_1590/H_1836) onto a single
capability ceiling. Either is decision-grade. The toy pre-gate makes it a $0 go/no-go first.
