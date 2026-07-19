---
id: H_9719
title: ATT-SHARP-INIT — emergent address via committed-but-arbitrary code (canonical slot is an oracle artifact)
tier: PROPOSED (lab-full EA divergence · DESIGN-ONLY · pool cost-gated · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-emergent-address (w_addr=0 — no CE(att,target_slot) anywhere)
created: 2026-07-17
series: EA-1
related: "[[H_9672]] · [[H_9692]] · [[H_9718]] · [[H_9720]]"
---

# H_9719 (EA-1) — the deadlock needs distinctness+consistency, not correctness: sharp low-temp init lets ANY injective entity→slot code self-organize

## Claim (one line · falsifiable)
With `w_addr=0`, initializing the address softmax SHARP (low temperature τ₀≪1, annealed → 1)
breaks the bootstrap deadlock because a random-but-CONSISTENT entity→slot assignment (W_q is
deterministic ⟹ same entity → same argmax every step) lets val differentiate per-slot from
step 0, after which the address gradient self-reinforces — the canonical target_slot that
oracle/addr-loss names is an ARTIFACT of supervision; emergence only requires the code be
injective and stable, which eval P1 (answer bytes) is already blind to.

## Mechanism (engine-native)
`anima-py train --store-att-temp τ0[:τ1@N]` — temperature on the CLMS address softmax
(core/clms.py forward, trainer-scheduled; default absent = byte-identical). No target named,
no new loss term, no new params.

## $0 pre-screen (KILL-before-spend)
Collision census on the D0-3 pen-dump artifact (outcome-branch reuse, NOT re-proposing D0-3):
frozen pen features × random-init W_q (k seeds) × K → argmax slot per entity. Measures
(a) injectivity (collision rate at 303M entity count vs slot count) and (b) per-entity argmax
stability across prompt variants. KILL-before-spend if collisions ≥ ~40% of entities across
all W_q seeds (sharp init would install a degenerate many-to-one code) or if argmax is
prompt-unstable (no consistency ⟹ no code to commit to).

## Pre-registered PASS/KILL (303M pool · 2-seed {7,11} · T3 config with w_addr=0)
- Controls: ① arm-C reproduction (τ default, w_addr=0) = null — must stay at chance
  (P1≈0.586 band, ln2 stall); if it escapes, premise broken → INVALID. ② addr-loss arm
  (H_9672 config) = positive control — known open. ③ scratch d768 = emergence positive ($0 cite).
- PASS: P1-balanced ≥ 0.75 ∧ flip ≥ 0.90 (both seeds) ∧ att sharp (mean max-mass ≥ 0.8) ∧
  per-entity consistency ≥ 0.9 — note addr-gap vs CANONICAL slot is NOT a gate here
  (permuted codes are admissible by construction); report canonical addr_mass separately,
  labeled diagnostic-only.
- KILL: P1-balanced TOST-equivalent to arm-C (ε pre-set from arm-C band) at matched power,
  both seeds, across τ₀ ∈ {0.1, 0.3} (2-point dose, no wider scan — scan = tune-to-green).

## Distinct-from-kills
- NOT addr supervision in disguise: no slot is ever named; the symmetry is broken by
  commitment, the CODE is chosen by the model's own init randomness + gradient.
- Closest kill: H_9692 (RV-2) explicitly DEMOTED temperature-annealing as "sharp-but-wrong
  contaminates val". That demotion holds in the SUPERVISED lane where a canonical target
  exists and addr-loss will later fight the wrong commitment. In the w_addr=0 frame there is
  no canonical target to be wrong AGAINST — sharp-but-permuted is a PASS condition, not
  contamination. This reframe is itself falsifiable: if K[entity] geometry hard-pins the
  correct slot (keys frozen to entity reps), a permuted commitment fights K and the H_9692
  objection transfers — the $0 consistency census reads exactly this.
- NOT lr/steps (schedule ≠ budget; equal-budget arm recorded), NOT store-size, NOT RF.

## Cost
$0 census → pool-GPU 2-seed (T3-scale co-train, 2 τ points + null arm).

## Verdict-integrity self-check
Over-claim risks: (1) a PASS is still "self-organized READ code over a hand-bolted store" —
CLMS itself is installed; p1–p8 purity claim capped at the read policy, never "emergent
memory". (2) A permuted-code PASS must NOT be reported as canonical addressing learned;
publish the permutation. (3) Value-read seed-fragility (H_9672 correction) applies here too —
a 1-seed P1 win is the SAME trap that produced the 0.9688 headline; 2-seed gate is
non-negotiable. (4) If PASS only at τ₀=0.1 and not 0.3, that is dose-fragility — report as
DIRECTIONAL-fragile, do not cherry the working point.
