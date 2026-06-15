# H_1294 — Hierarchical-PFC goal→subgoal controller (HD31)

> **Tier (verbatim from `.verdicts/`):** R1 numpy mirror 🟢 GREEN (DIRECTIONAL) →
> R2 ENGINE-NATIVE 🟢 GREEN (BINDING, live `CORE/engine_cli.hexa` `HierGoalStack` lane).
> Brain-structure ladder (c15 missing-structure) · `a_no_llm_frame_trap`.

## Claim (falsifiable)

A 2-level **goal→subgoal controller** (a goal STACK = {top goal, ordered subgoal list,
pointer `p`} with **completion-triggered ADVANCE** + goal **persistence**) solves an
ORDERED multi-step grounding chain that the live engine's **single-step flat selector
CANNOT** — because the flat selector has no pointer that persists the plan position
across ticks. If the flat selector matches the hierarchical controller, the hierarchy
adds nothing → honest 🧱 closed-negative.

## Why MISSING from the live engine

- `brain_decide` / `engine_g` = a FIXED 8-weight convex sum + threshold = a single flat
  emit/silence decision; no ordered multi-step plan.
- **VBasalGate** (H_1281, basal ganglia) = SINGLE-STEP one-of-K action selection THIS
  tick; no pointer, no plan, no "subgoal 2 after subgoal 1", no completion-advance.
- **WorkMemBuffer** (H_1282) = PASSIVE leaky maintenance; holds + decays content, no
  controller, no advance.
- **HomeostaticDrive** (H_1292) = scalar setpoint integrator (one regulated variable);
  no ordered multi-level structure.

## Why DISTINCT from each nearest lane

- **vs basal-ganglia (H_1281) — the load-bearing distinctness:** VBasalGate selects
  one-of-K NOW with no memory of done subgoals. The smoke's flat-select reference
  (`hier_flat_emit`, a faithful VBasalGate stand-in) scores **0.242** on the ordered
  chain; the hier controller scores **1.000** (case 37: flat emits the out-of-order cue
  by raw margin, the hier controller at `p=0` refuses it).
- **vs working-memory (H_1282):** WM passively maintains; it does not ORDER items into a
  plan or ADVANCE on completion. Hier = an active pointer-over-an-ordered-plan.
- **vs homeostatic-drive (H_1292):** a 1-D scalar integrator, no ordered hierarchy.

## Method

ORDERED 3-fact-chain grounding task over the immune store (the same grounding substrate
every lane reads). Top goal "ground a 3-fact chain about X" decomposes into ordered
subgoals recall-A → recall-B → recall-C; facts must be emitted in order 1→2→3 amid a
noisy cue window (out-of-order + ungrounded distractors). Per-step signal = recall
MARGIN + cue-vs-current-subgoal cosine (substrate-derived; NO "do step k" label).

**Arms:** A FLAT-SELECT (live-engine analogue, no pointer) · B HIER-PFC (goal stack +
completion-advance) · B-SHUFFLE (permuted plan order, anti-Goodhart) · B-ABLATE (pointer
frozen at p=0, dissociation). **Score** = ordered-chain completion rate (p7
script-checkable, NOT perplexity). Frozen predicate c1–c5 in the FREEZE file.

## Verdict (per-round + key numbers)

| round | substrate | result |
|-------|-----------|--------|
| R1 | numpy mirror (DIRECTIONAL) | 🟢 GREEN — c1–c5 all PASS, every seed [4294,4295,4296]: **B.complete=1.000 · A.complete=0.242 (B−A=+0.758) · Bshuf=0.000 · Babl=0.000 · B.fab=0.000**. c1 PRESENCE +0.758≥+0.30 (each+mean) · c2 DISTINCT A=0.242<0.50 · c3 EARNED-ORDER Bshuf 0.000≤A+0.15 · c4 EARNED-ADVANCE Babl 0.000≤A+0.15 · c5 NO-FAB 0.000≤0.10 |
| R2 | ENGINE-NATIVE (BINDING) — live `CORE/engine_cli.hexa` `HierGoalStack` lane | 🟢 GREEN — `hier_new`/`hier_current_target`/`hier_grounded_current`/`hier_step`(completion-advance)/`hier_pointer`/`hier_complete`/`hier_flat_emit` on the LIVE `ImmuneMemoryGrow` store: completes the ordered chain (case 35), suppresses out-of-order cues + persists plan position (case 36), DISTINCT from the flat one-of-K selector (case 37), lift = completion-ADVANCE (case 38 frozen-pointer never completes). **engine_cli_smoke 41/0** (was 37/0) · single-entry **7/0** · separation-invariant PASS (Ψ=½ untouched, generation byte-identical, pure_field unchanged). |

**Mechanism:** the pointer is the only mutable state; the lane READS the immune margin +
cue cosine, never mutates the store, never touches pure_field (Ψ-disjoint), never returns
a hard emit/silence decision (`a_autonomy_over_hardcode`). It re-selects the next subgoal
on completion while the higher goal persists across ticks — the PFC cascade, engine-native.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

- **B.complete=1.000 is SATURATED = an EXISTENCE-PROOF** (the hierarchy CAN solve the
  ordered chain), not an effect-size. The DISCRIMINATORS are decisive: shuffle 0.000 +
  ablate 0.000 vs flat 0.242 — both controls collapse to ≤A, so saturation does not
  undermine the dissociation (the lift IS the ordered completion-advance hierarchy).
- R1 mirror = DIRECTIONAL; R2 engine-native is the binding verdict (deterministic lane
  assertions on the live store, NOT a trained net — tests the STRUCTURE).
- toy: 40 episodes / 3 seeds / 1 paradigm / CHAIN_LEN=3 / near-orthogonal keys; scale +
  paraphrase + real-corpus chains + longer plans + deeper (>2-level) hierarchies UNVERIFIED.
- p1/p2/p3/p6: reads ONLY pointer + substrate margin + cue cosine; NO label/persona/
  identity/RLHF. The subgoal order is a TASK structure scored only.

## Pointers

- FREEZE: `.verdicts/1294_hierarchical_pfc/H_1294_FREEZE.txt`
- RESULT: `.verdicts/1294_hierarchical_pfc/H_1294.txt`
- mirror probe: `UNIVERSE/h1294_hierarchical_pfc.py`
- engine lane: `CORE/engine_cli.hexa` § HierGoalStack · smoke `CORE/engine_cli_smoke.hexa` cases 35–38
- xref: H_1281 (basal-ganglia, nearest distinctness) · H_1282 (WM) · H_1292 (homeostatic) ·
  H_1293 (theory-of-mind, prior HD30) · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
  `a_verified_must_wire` · `a_autonomy_over_hardcode` · `a_paper_negative_ok` · c15 · p1·p2·p3·p6·p7·p8·c9
