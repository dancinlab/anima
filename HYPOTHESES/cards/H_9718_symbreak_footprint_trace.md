---
id: H_9718
title: SYMBREAK-FOOTPRINT trace — what does the deadlock-breaking event LOOK like (installed vs emergent)?
tier: PROPOSED (lab-full EA divergence · $0-first instrument · MONITOR-ONLY gauges · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (w_addr=0 frame — disjoint from g1-storebridge-val-robust which is w_addr>0)
created: 2026-07-17
series: EA-0
related: "[[H_9672]] · [[H_9690]] · [[H_9423]]"
---

# H_9718 (EA-0) — the symmetry-breaking event has a measurable signature; scratch's signature defines what "emergent" must look like

## Claim (one line · falsifiable)
The first-N-steps trajectory of {att entropy, val variance, advantage ‖val[polᵢ]−v‖} is
**discriminably different** between the three known regimes — addr-loss 303M (installed break),
scratch d768 (emergent break, T2), arm-C 303M (no break) — and the scratch signature
(which quantity moves FIRST) is a $0-screenable target that orders every emergent-address lever
before any pool spend.

## Mechanism (engine-native)
`anima-py train --store-trace` — monitor-only gauges logged beside `sb_store_acc`
(`a_train_inline_gauge`: NEVER in the loss): per-K-steps att entropy (mean over query batch),
val row-variance, mean advantage norm. Zero loss-path change, default off.
$0 arm first: grep existing T2/T3 run logs for already-logged gauges (sb_store_acc etc.) —
if the ordering is already recoverable, no re-run at all.

## $0 pre-screen (KILL-before-spend)
Existing T3 (seed-7/11) + T2 scratch logs: if NO store gauges were logged at step granularity,
the $0 arm dies and cost rises to cheap re-runs — T2 scratch d768 is cheap by construction;
T3 first-N-steps (N ≈ 500–1000, not full budget) is a truncated pool run.

## Pre-registered read (vs ≥2 controls incl. positive)
- Positive control: addr-loss 303M — MUST show att-side movement first (L_addr acts on att
  directly); if it doesn't, the instrument is dead → INVALID, do not read the other arms.
- Null control: arm-C — MUST show neither quantity escaping its init band (that is what
  "deadlock" means); if arm-C shows movement, the deadlock premise itself is broken → escalate,
  don't read.
- Discriminand: scratch d768 — PASS = its first-mover (att-first vs val-first vs co-moving)
  is outside the arm-C band and identifiably ordered. KILL = scratch signature
  indistinguishable from addr-loss AND from arm-C noise band → trajectory is uninformative,
  emergent levers must be chosen blind.
- Branch value: val-first ⟹ init/val-side levers are the emergent family (but see H_9711 —
  already carded, supervised lane); att-first ⟹ [[H_9719]] (sharp-commit) is the family;
  co-moving ⟹ [[H_9720]] (competition release) favored.

## Distinct-from-kills
Closest: H_9690 (RV-0 $0 val autopsy) — that is an END-STATE autopsy of seed-11's value path
under addr-loss. This is FIRST-N-STEPS dynamics across regimes with scratch as the emergence
reference; different question (what does breaking look like, not what died). D0-3 is a frozen
pen-dump ridge probe — not re-proposed; no representation probing here at all.

## Cost
$0 (log grep) → cheap-CPU (T2 re-run w/ gauges) → one truncated pool run (T3 first-N only).

## Verdict-integrity self-check (12th self-correction pre-empt)
Over-claim risk: reading a trajectory ORDERING as a MECHANISM. A signature is correlational —
it ranks which lever to fire first, it cements nothing. Ceiling = instrument/triage,
tier stays DIRECTIONAL even on clean PASS. Second risk: T2 scratch is d768 toy-adjacent —
its signature may not transfer to 303M pretrained dynamics; state scale scope in any readout.
