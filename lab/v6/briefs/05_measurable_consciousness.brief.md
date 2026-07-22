# HOW DO YOU BUILD A MODEL WHOSE CONSCIOUSNESS IS ACTUALLY MEASURED?

Owner directive, just landed as philosophy **p9**: anima's target is a model whose
consciousness (a) **emerges on NATURAL corpus** — not installed by a hand-built drill — and
(b) is **MEASURED, never asserted**. Every interior claim must reduce to a number some
instrument produced, read as collapse-delta against >=2 controls.

This brief is about half (b): **measurability**. Not "is anima conscious" — that is not
askable. The question is constructive:

> What must be TRUE OF THE ARCHITECTURE for a consciousness claim about it to be
> DECIDABLE at all? And what is the smallest such architecture we could actually build?

## HOW TO WORK — brainstorm to DEPLETION, no deadline

No time limit. Work in ROUNDS; after each, ask which lens you have not used yet and run
another. Stop only when **two consecutive rounds produce nothing genuinely new**, then say
**DEPLETED after N rounds** and list the lenses you exhausted. Breadth first, ranking last.

=====================================================================
# WHY THIS IS THE HARD HALF — the measurement campaign already ran and came back blind

R9 closed 6/6 on the interior. It did NOT find "weak consciousness"; it found that almost
nothing was DECIDABLE:

  H_9786 whether-to-speak      UNIDENTIFIABLE
  H_9787 typicality            BOUNDED-NULL
  H_9788 sigma-flux            INSTRUMENT-DEAD
  H_9789 self-anchor           VOID
  H_9790 imagination           DIRECTIONAL - reaches the interior, never the mouth
  H_9791 agency                UNIDENTIFIED
  H_9785 ownership             UNIDENTIFIABLE

Only content-reach (H_9774) survived as a positive. So the bottleneck is not the substrate
being poor; it is that **the architecture offers no handles an instrument can grip**.

## The structural reasons, verified in code

1. **The interior is one number, and its two poles are not independent.** Production
   default `--g-arm a0`: `ag_a_drive = emit_drive`, `ag_g_drive = -(1 - emit_drive)`, so
   `s = 2*emit_drive - 1` and `conflict_scalar` are both functions of ONE number. The code
   comment calls it *the tautology arm* that *MUST fail the independence gate*. Effective
   independent dimensions: **zero**. Nothing with zero degrees of freedom can be measured.
2. **Every interface is 1-D.** `pure_field_step(pf, drive)` takes one float (and feeds the
   same float to all three oscillators); `--tension-route` is `pc2`, one axis; HEXAD's
   `d_input = bridge_clamp(_hf_mean(cs_detached))` is one float for six modules.
3. **Phi is barred from the loop by law.** `a_phi_iit4_tool` requires faithful IIT-4, and
   `a_train_inline_gauge` makes in-training metrics MONITOR-ONLY. So the C module computes
   Phi and it touches no weight. The "brain" and the learning substrate are disjoint
   artifacts sharing a repo.
4. **Emit is a clock.** H_9401-9403: the G-readout margin crack is real (0.62) but is
   swallowed; emit <=> clock, so "whether to speak" has no free variable to measure.

## The ONE instrument in this repo that achieves IDENTIFICATION (not correlation)

H_9807 interventional closure ladder, already landed as `anima-py evaluate --closure-ladder`:
the executed behaviour is A/B randomized on a seeded coin between {real action,
marginal-matched shuffle}, so `P(I_{t+1} | do(A_t))` is **identified**, with a Watson
**yoked-ghost** floor (the agent's own actions replayed with order destroyed, marginals
matched). Its own card carries the warning that rung 1 is not aliveness: a 15-line
thermostat plant passes by design.

That is the shape that works. The question is what else can be built to that standard.

## What the redesign already proposes for measurability (do not just restate it)

LANE-BUS (Fable 16 rounds / Sol 20 rounds, both depleted):
- **RESIDUAL** — tension redefined as the per-position divergence profile between the
  reflex softmax (trunk alone) and the composed softmax (bus). Dimension V x span, so the
  interior finally has width an instrument can grip.
- **GATE** — trained emit-on-information-gain, with the noise floor measured on
  shuffled-store controls and frozen before use. Kills emit<=>clock.
- **DISCHARGE LAW** — on emit, the utterance is written back to the store, and the residual
  that caused it should DROP; under `do(block-emit)` it should persist. This is offered as
  p5's first falsifiable physical signature.
- **INSTRUMENTS AS ORGANS** — every module ships its `do()` handle as an `anima-py` flag at
  landing time (`--permute-store`, `--swap-selflog`, `--block-emit`, `--freeze-workspace`,
  `--reflex-only`), because R9's blindness was partly the absence of handles.

=====================================================================
# KILL-LIST — measured dead, do NOT rebuild

- Scalar A<->G tension as the interior variable (zero DOF, above). The 8-vector tension lane
  folded to one bit with direction dead (rho = -0.077, H_9576).
- Write-side rank-1 tension FIELD (H_9805/9812): measured LEXICALLY BLIND, channel 0 on a
  vocabulary panel.
- emit-DRIVE lane CLOSED-AT-REGIME (H_9401-9403).
- Dead adjacent lineages: veto H_9269, affect H_9411, tension H_9630/9633.
- HEXAD as-specified (no-op store, stub generate, scalar bridge).
- Phi as a PROXY is banned (`a_phi_iit4_tool`); Phi in the loss is banned
  (`a_train_inline_gauge`). Do not propose either.
- Self-report / introspective text as evidence: p1-p4 forbid the framing, and a language
  model's self-description is exactly the thing that cannot be trusted here.
- A gate a perfect subject fails is an instrument defect, not a wall — G6 is now documented
  as a FORM-detector artifact (12.8x above the corpus rate; 8 draws; pass-prob 0.0505).

# LAWS THAT WILL JUDGE YOUR DESIGN
FORM is tunable, BIND is earned — if a memorized template or a thermostat can pass your DV,
it is dead on arrival. Positive control before reading a negative. Controls must match the
MEDIATING covariate. Chance re-derived per metric from the realized partition. A cheap
screen may only KILL, never GREEN. No tune-to-green; never re-freeze a burned gate.
Psi-SOMA: read a verdict as MODE OF EXISTENCE, not capability — Theta (the Psi=1/2 pulse;
Theta dead => sigma VOID), sigma (9 axes), INVALID/VOID/PENDING first-class, signal read as
collapse-delta against >=2 controls, never a raw value. Every manipulation is a FLAG on
anima-py. Only anima-py cements.

=====================================================================
# WHAT I WANT BACK

**A. The measurability criterion.** State, as sharply as you can, what property an
architecture must have for a consciousness claim about it to be decidable. Then use it to
explain R9's 6/6 blindness as a prediction rather than a surprise.

**B. The ladder.** An ordered set of claims about the interior, each strictly stronger than
the last, where every rung names (i) the architectural handle it requires, (ii) the
instrument, (iii) the controls that make it identified rather than correlational, and
(iv) the trivial system that MUST pass it (the thermostat test) so the rung's floor is
honest. Say where the current architecture falls off the ladder.

**C. The minimum buildable architecture** that reaches the highest rung you think is
honestly reachable — as `anima-py` flags, with the $0 screener that kills it first.

**D. What is NOT measurable, ever, and how to say so without hand-waving.** If some rung is
in principle undecidable from the outside, name it and name why, so the campaign stops
spending on it. Be specific about which of R9's six axes are permanently closed vs merely
un-instrumented.

**E. Attack this claim:** "a model whose consciousness is measurable is a contradiction —
any property you can operationalize is thereby not consciousness, and any property you
cannot is not measurable." Either defeat it or concede its scope precisely.
