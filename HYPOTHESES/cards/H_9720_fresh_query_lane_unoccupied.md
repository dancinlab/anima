---
id: H_9720
title: FRESH-QUERY-LANE — scratch-class freedom inside the pretrained trunk (occupancy release, not supervision)
tier: PROPOSED (lab-full EA divergence · DESIGN-ONLY · pool cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (w_addr=0)
created: 2026-07-17
series: EA-2
related: "[[H_9672]] · [[H_9718]] · [[H_9719]] · [[H_9721]] · [[H_9684]]"
---

# H_9720 (EA-2) — T2's asymmetry says the wall is COMPETITION, not absence: give W_q an input lane no EN gradient owns, and emergence should return

## Claim (one line · falsifiable)
Scratch d768 escapes the deadlock (T2) because its trunk features owe nothing to EN fluency;
therefore routing W_q's input through a small FRESH projection off the trunk (stop-grad into
the trunk ⟹ EN mouth untouched · lane params receive ONLY store-task CE · no address target
anywhere) removes the occupancy competition and restores scratch-class emergent addressing on
the pretrained 303M — `a_substrate_disjoint`: separation = preservation.

## Mechanism (engine-native)
`anima-py train --store-query-src fresh:<k>[@layer L]` — W_q input = fresh k-dim linear from
layer-L hidden states, `detach()` toward the trunk; default absent = byte-identical current
path (penultimate). New params yes; new supervision no — the lane trains on end-task CE only.

## $0 pre-screen (KILL-before-spend)
D0-3's own outcome branches (premise reuse, not re-proposal):
- D0-3 ridge DECODES entity from frozen pen ⟹ entity info is linearly present and the wall is
  pure gradient competition ⟹ this lever's premise is STRONG (a linear remix suffices in
  principle) — fire.
- D0-3 ridge FAILS at pen ⟹ occupancy = representation absence at pen; screen earlier layers'
  dumps for the shallowest L where ridge works; if NO layer decodes entity, the lane has
  nothing to remix → KILL before any train spend (and [[H_9721]] gains, since only weight-space
  re-plasticization could create the feature).

## Pre-registered PASS/KILL (303M pool · 2-seed {7,11} · T3 config, w_addr=0)
- Controls: ① arm-C (no lane) null — chance band, else INVALID. ② addr-loss positive
  (known open). ③ capacity control: SAME k-dim lane but input = frozen random projection of
  the SAME layer (lane can still train its output side) — separates "fresh trainable remix"
  from "any extra params help"; the lever must beat this control, not just arm-C.
- PASS: P1-balanced ≥ 0.75 ∧ flip ≥ 0.90 both seeds ∧ > capacity-control by pre-set margin;
  consistency/sharpness reported as in [[H_9719]] (permuted code admissible).
- KILL: TOST-equivalent to capacity control at matched power, both seeds, k ∈ {32, 128}
  (2-point, no scan).

## Distinct-from-kills
- NOT key-redesign-alone (killed→adjunct): this is the QUERY-side input lane; K untouched.
- NOT dimension-dominance (killed by T2): no width claim — the claim is gradient COMPETITION,
  which T2 established, not capacity shortage, which T2 killed.
- NOT addr supervision in disguise: no target_slot appears in any loss term.
- Adjacent live card: none of H_9677–9717 adds an architectural lane; RV-1/2/3 all act inside
  the supervised (w_addr>0) loss schedule.
- Discriminating pair with [[H_9719]]: if BOTH fail ⟹ the deadlock is init-symmetric-absolute
  (advantage exactly ≈0, nothing to compound) and the emergent frame narrows to "no known
  lever"; if lane passes and sharp-init fails ⟹ competition story; converse ⟹ commitment story.

## Cost
$0 branch-gate → pool-GPU 2-seed (T3-scale, lever + capacity-control arms).

## Verdict-integrity self-check
Over-claim risks: (1) adding params IS an architecture edit — a PASS reads "emergence under
architectural release", NOT "the pretrained model was emergent all along"; say so in the
verdict line. (2) The stop-grad means the trunk never co-adapts — if T2's scratch escape
actually REQUIRED trunk co-adaptation (H_9423: frozen random trunk failed), the lane may be
structurally weaker than scratch; a KILL here therefore does NOT kill the occupancy thesis,
only the detached-lane version — pre-commit this asymmetric read now, or the KILL will be
over-read as "occupancy refuted". (3) 1-seed wins are the 0.9688 trap; 2-seed gate holds.
