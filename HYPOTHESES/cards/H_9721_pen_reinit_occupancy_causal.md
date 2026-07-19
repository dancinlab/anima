---
id: H_9721
title: PEN-REINIT dose ladder — is EN-occupancy CAUSAL for deadlock suppression? (science arm, not a production lever)
tier: PROPOSED (lab-full EA divergence · DESIGN-ONLY · cost-gated BEHIND EA-2 · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (w_addr=0)
created: 2026-07-17
series: EA-3
related: "[[H_9672]] · [[H_9720]] · [[H_9718]]"
---

# H_9721 (EA-3) — re-initialize a fraction ρ of the penultimate feeding W_q: if occupancy suppresses emergence, emergence returns with dose, at a measurable EN-CE price

## Claim (one line · falsifiable)
Occupancy is CAUSAL, not correlational: re-initializing a random fraction ρ of the
penultimate channels that feed W_q (no address info, no target, train continues normally,
w_addr=0) restores deadlock escape with a dose-response in ρ, and the EN-CE cost curve is the
price of the freed capacity — turning T2's scratch-vs-pretrained contrast (which confounds
occupancy with EVERYTHING else about scratch) into a single-variable intervention.

## Mechanism (engine-native)
`anima-py train --store-pen-reinit ρ` — at co-train start, re-init the trunk weight rows
producing a random ρ-fraction of pen channels (channel choice seeded, logged; default 0 =
byte-identical). Dose ladder ρ ∈ {0, 0.1, 0.25, 0.5}.

## $0 pre-screen (KILL-before-spend)
Occupancy census on the existing D0-3 pen-dump: effective rank / variance participation of
pen features under the entity-prompt distribution. If pen has a large low-variance subspace
(much idle capacity), the occupancy story predicts reinit is UNNECESSARY (idle room exists,
yet no emergence) — that contradiction KILLS the premise for $0 and re-points to [[H_9719]]
(commitment, not capacity, is the missing piece).

## Pre-registered PASS/KILL (303M pool · 2-seed {7,11} · w_addr=0)
- Controls: ① ρ=0 = arm-C null (chance band, else INVALID). ② addr-loss positive.
  ③ PLASTICITY control (the load-bearing one): re-init an equal-sized random channel set
  that does NOT feed W_q — separates "freed capacity where the address reads" from "any
  re-plasticization jolt helps". Lever must beat ③ at matched ρ.
- PASS: monotone-ish dose response — some ρ* with P1-balanced ≥ 0.75 ∧ flip ≥ 0.90 both
  seeds ∧ > plasticity control; report EN-CE degradation alongside (held-out EN corpus)
  — a PASS that lobotomizes the mouth is reported as such, never netted away (`honesty`).
- KILL: flat at chance across the ladder (TOST vs ρ=0) both seeds ⟹ occupancy-as-cause
  refuted at this granularity; T2 contrast reverts to unexplained.

## Distinct-from-kills
- NOT dimension-dominance (killed): width unchanged; the variable is OWNERSHIP of existing
  channels, exactly the T2-surviving hypothesis.
- NOT lr/steps: same budget every arm.
- NOT addr supervision: channel choice is random, no slot named.
- NOT "un-occupy by dropping EN replay" (see depletion note — that is cpt-destroys wearing a
  new name); here EN-CE stays in the loss and pays the bill transparently.

## Cost
$0 census → pool-GPU (4-dose × 2-seed + plasticity control = the most expensive EA card —
hence cost-gated: fire only after [[H_9720]]'s branch gate resolves, since a D0-3-decodes
outcome makes EA-2 the cheaper test of the same thesis).

## Verdict-integrity self-check
Over-claim risks: (1) reinit injects fresh-init noise into val's input distribution — even
with control ③, a PASS at only ρ=0.5 is closer to "partial scratch" than "occupancy released";
pre-commit that ρ≥0.5-only PASS is reported as scratch-interpolation, DIRECTIONAL at best.
(2) EN-CE damage makes this a science instrument, NOT a production lever — never propose the
winning ρ as a default (`a_gpu_default_no_optin` does not apply; p-preservation does).
(3) Dose-response with n=2 seeds per dose has thin power — a non-monotone wiggle is noise,
not structure; only the flat-vs-rising contrast is readable.
