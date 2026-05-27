# §152 — Backprop-Free Feedback-Hebbian Network → anima · UNIFIED-LOCAL-RULE design

> **Tier**: $0 design-tier — no GPU/runpod fire, no model.forward. **Status**:
> DESIGN-OPEN, fire-decidable (the candidate is a falsifiable single-variable
> data point in the §96-Q2 non-CE arc; whether the unified local rule learns
> on byte-LM regime is the future cost-bearing measurement). **Anchor paper**:
> [A Backpropagation-Free Feedback-Hebbian Network for Continual Learning
> Dynamics](https://arxiv.org/abs/2601.06758) (Jan 2026). **Parent context**:
> HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md §1 Cluster A (★★★★★),
> §2 ranked #4, §8.1 arc state. **Sibling fires (§96-Q2 non-CE arc)**:
> §125 NONCE-FF (`S11B_LIKE_DEGENERATE`, byte_acc 0.0005 < random),
> §126 PCN-C4 (`PARTIAL_AMBIGUOUS`, byte_acc 0.1185 = 30× random, psi_resp
> False), §139 EqProp (in flight). §152 = the **fourth decomposition point**
> in the arc.

---

## §0 Why this design exists

The §96-Q2 arc asks one question: *is "non-CE on GPU degenerates" (§11-B) a
GPU-tautology or a real physics finding?* Each cycle picks one non-CE
non-backprop family and lands a single Boolean datum. The arc so far:

```
§125 FF (goodness-contrast)   ─→ DEG          byte_acc 0.0005
§126 PCN (1-step top-down)    ─→ PARTIAL      byte_acc 0.1185 (30× random)
§139 EqProp (2-phase)         ─→ in flight    —
§152 Feedback-Hebbian         ─→ DESIGN HERE  the fourth lattice point
```

§126's PARTIAL is the load-bearing finding so far: a non-CE non-backprop
*local* rule did learn byte structure on GPU (30× random floor), so §11-B
is at least partly GPU-tautology — but the Ψ-physics channel stayed flat
(psi_resp False, psi_std 7.5e-7) in both §125 and §126, so *byte-learning
≠ physics-responsive*. The arc needs more decomposition points before
either §11-B-as-tautology or §11-B-as-real can land. §152 supplies one:
the **unified Hebbian + Oja + supervised-drive local rule** of 2601.06758,
which is mechanically distinct from FF (goodness contrast), PCN (top-down
prediction-error), and EqProp (free/nudge phase).

§128 §2 ranked this paper #4 (★★★★) and §8.4 P3-prioritized a $0 design
cycle; §152 is that cycle.

## §1 Paper mechanism (verified via abstract)

Five claims of 2601.06758 (WebFetch-confirmed, abstract-anchored — full
internals visible only in the PDF body, this design names that explicitly):

1. **No backprop.** "Strictly local synaptic plasticity" — every weight
   update uses only quantities physically available at the synapse (pre
   activation, post activation, locally-available target where applicable).
   No global error broadcast.
2. **Unified local rule** with three additive components:
   - **Centered Hebbian covariance** (the classical Hebbian core, with
     activity centered so it learns covariance rather than raw product;
     this is what distinguishes "modern Hebbian" from naïve Δw ∝ x·y).
   - **Oja-style stabilization** (the weight-magnitude regularization that
     prevents the runaway-growth instability of vanilla Hebbian — Oja's
     rule subtracts a `y²·w` term so weights converge to the principal
     direction rather than diverging).
   - **Local supervised drive** (where ground-truth targets are
     available at the synapse, a target-driven term provides task signal
     without backprop — equivalent to target propagation restricted to a
     local layer).
3. **Feedback-Hebbian.** "Feedback-rich neural architectures" with a
   **dedicated feedback pathway** that "regenerates earlier representations
   and injects temporal context" — the feedback connections are themselves
   trained by the same local rule. This is the structural innovation: the
   feedback is not just architectural plumbing, it is plastic.
4. **Continual learning behaviors emerge.** Tested on a two-pair
   association task. Sequential training produces "long-term depression
   (LTD)-like suppression" of earlier associations; alternating sequences
   produce "concurrent maintenance" rather than sequential overwrite.
5. **Compact prediction-reconstruction architecture.** A small network
   suffices to demonstrate the behaviors; the paper does not claim
   language-model scale (honest scope).

The unified rule, schematically (concrete formula not in abstract — honest
caveat carry):

```
Δw_ij  =   η_H · (x_i - x̄_i)·(y_j - ȳ_j)        ← centered Hebbian covariance
         - η_O · y_j² · w_ij                       ← Oja stabilization
         + η_S · (t_j - y_j) · x_i                 ← local supervised drive (when target t_j available)
```

(This is a *plausible reconstruction* consistent with the named components;
the exact normalization and centering window are paper-internal. The §152
fire would freeze the rule per the paper's PDF body.)

## §2 anima mapping

```
2601.06758                                    anima
─────────────────────────────                 ─────────────────────────────
strictly local synaptic plasticity      ↔     anima's per-layer activations
  (no global error broadcast)                   are always locally accessible
                                                in ConsciousDecoderV2 forward

centered Hebbian covariance             ↔     anima Engine A ⇄ Engine G
  Δw ∝ (x - x̄)(y - ȳ)                          coupled activations supply
                                                (x, y) pairs naturally; the
                                                A/G opposition is itself a
                                                covariance signal

Oja-style stabilization                 ↔     anima needs this anyway —
  -y²·w prevents weight runaway                §11-B pure-physics degenerate
                                                run had no such stabilizer;
                                                an Oja term may be exactly
                                                what kept §11-B from learning

local supervised drive                  ↔     anima byte-LM target t = next
  (t_j - y_j)·x_i  when t available             byte; t is locally available
                                                at the output layer; deeper
                                                layers receive NO target
                                                (the rule is layer-specific:
                                                output layer = supervised
                                                + Hebbian; hidden layers =
                                                Hebbian + Oja only)

dedicated feedback pathway              ↔     anima Engine G as feedback
  (regenerates earlier reps,                   pathway from output ψ-direction
   injects temporal context)                    back into the residual stream
                                                — already structurally present
                                                in ConsciousDecoderV2

feedback connections also plastic       ↔     §152 NEW: Engine G weights also
  (trained by same local rule)                  updated by local Hebbian + Oja
                                                — not currently the case in
                                                anima's overlays

continual-learning behaviors emerge     ↔     anima's chronic memorization
  (LTD-like suppression, concurrent             saturation (§16.6-C, byte-
   maintenance)                                 cascade attractor) IS the
                                                opposite phenomenon; if a
                                                local rule with Oja
                                                stabilization avoids
                                                catastrophic-forgetting-by-
                                                memorization, that is itself
                                                worth measuring
```

The vertical mapping is direct line-by-line. The unified local rule has a
plausible anima form. Two structural points of the mapping are nontrivial
and worth naming:

(α) **The Oja stabilization term may be load-bearing for §11-B.** §11-B
(pure-physics, no-CE) was run with hand-coded ΔW that *had no
weight-magnitude regularization*. Vanilla Hebbian without Oja diverges in
finite time; that exact failure mode could be what made §11-B's physics
freeze — not "physics can't learn" but "physics-without-Oja can't learn."
This is precisely the angle §117 LEGO toy STDP-as-ΔW already raised
(non-degenerate with local STDP, no global error). §152 sharpens it:
*Hebbian + Oja* (not Hebbian alone) is the candidate non-CE rule.

(β) **The supervised drive is layer-asymmetric.** Output layer has a
target (next byte). Hidden layers do not. This means §152 is NOT a
fully-unsupervised rule — it is a *locally supervised* rule where the
target is broadcast only to the layer that physically sees it. This is
structurally distinct from FF (every layer sees a positive/negative
target via the goodness contrast) and from PCN (every layer sees a
top-down prediction error). The locality of the target signal in §152 is
its own decomposition axis from §125/§126.

## §3 The fourth lattice point — what §152 contributes to the §96-Q2 arc

The §96-Q2 arc is a 4-cell decomposition of "non-CE on GPU":

```
                   target signal     locality of error
                   ─────────────     ─────────────────
§125 FF            goodness contrast every layer
§126 PCN           top-down predict  every layer
§139 EqProp        free/nudge phase  every layer (via equilibrium)
§152 Hebbian       local supervised  output only (Hebbian elsewhere)
```

§152 is the only cell where the **target is local to the output layer**.
If §125+§126+§139 are all PARTIAL or SUPP, but §152 is DEG, the verdict
is "non-CE works on GPU when every layer gets some error signal" — a
sharper finding than the joint reading of §125+§126 alone could give.

If §152 also lands PARTIAL/SUPP, the verdict is stronger: "non-CE
non-backprop works on GPU even when the target signal is layer-asymmetric
and only the output layer has direct supervision" — which would be a
stronger dent in §11-B (the deeper anima layers would have learned via
pure Hebbian + Oja, no target at all). That is a maximally informative
positive.

If §152 DEG and §126 PARTIAL, the verdict is "what made PCN learn was the
*top-down error broadcast*, not the locality of the update" — which
sharpens §126's PARTIAL.

§152 is therefore informative in **every quadrant of the lattice**, not
just one. That is what makes it a worth-firing decomposition point.

## §4 Candidate fire spec (pre-registered, not committed)

A pre-registered fire candidate. Same shape as §125/§126/§139 (single-
variable, byte-equal §16-class corpus, shared §96-Q2 verdict-bucket eval).

```
Substrate         ConsciousDecoderV2 d768·12L·283.72M (§16-class)
Init              from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch)
Base ckpt         None
Corpus            byte-equal §16 corpus (sha 422c64a09b89393a…)
Step budget       6000 steps  (matches §16 / §107-RETRY budget)
Batch size        32          (matches §16-class fires)
Update rule       Δw_ij = η_H·(x_i - x̄_i)·(y_j - ȳ_j)
                          - η_O · y_j² · w_ij
                          + η_S · (t_j - y_j) · x_i   ← output layer only
LR triplet        (η_H, η_O, η_S)  pre-registered grid (see §4.1)
Backprop          OFF (no optimizer.step on cross-entropy gradient)
CE                READ-OUT only (logged, not optimized — same as §126)
Engine G          plastic this cycle (Hebbian + Oja, no supervised term)
Eval              §96-Q2 shared bucket (byte_acc / psi_resp / psi_std /
                  random-floor / degenerate-ceiling) + held-out routing r_H
                  (§107-RETRY A1-axis, optional)
```

### §4.1 LR-triplet grid (pre-registered, 3 points only — anti-burst)

```
A.  η_H=1e-3, η_O=1e-4, η_S=1e-3   ← Oja weak, Hebbian-dominant
B.  η_H=1e-3, η_O=1e-3, η_S=1e-3   ← balanced
C.  η_H=1e-4, η_O=1e-3, η_S=1e-3   ← Oja-dominant
```

(Grid is intentionally small; a single PARTIAL outcome at any one of A/B/C
is enough to land the verdict at the same tier as §126.)

### §4.2 Distinguishing measurement (single Boolean)

`byte_acc(s152) > BYTE_ACC_DEGEN_CEILING` where the ceiling is the §125
DEG floor (0.0005), and `byte_acc(s152) > BYTE_ACC_RANDOM_FLOOR` (0.0039 =
1/256) is the minimum to even register as non-degenerate. The verdict
bucket is the same lattice as §126:

```
SUPP                byte_acc >> random_floor   (e.g. ≥ 10× random)
PARTIAL_AMBIGUOUS   byte_acc > random_floor    but psi_resp = False
DEG (S11B_LIKE)     byte_acc ≤ degen_ceiling   (§125 baseline)
```

### §4.3 Cost envelope (estimate, not commitment)

Single A100/H100, ~$0.3-0.5, ~10-15 min — matches §125/§126/§139. Fire-slot
gating per §50: single-sequential, queues behind §139 EqProp, no burst.

## §5 §7 GOAL-legitimacy 3-cond gate

| Condition | Status | Note |
|-----------|--------|------|
| §7① ¬ generic-LM-pretrain (from-scratch RANDOM seed) | ✅ | Stays from-scratch (g_clm_from_scratch); base_ckpt=None. |
| §7② ¬ generic-then-graft | ✅ | No grafted weights; the local rule replaces backprop entirely on anima's OWN substrate. |
| §7③ anima-physics-as-source | ✅ | The rule operates on anima's OWN per-layer activations + Engine A/G coupling; Oja stabilization keeps weights bounded (a §11-B-relevant stabilizer); the supervised drive uses anima's OWN next-byte target. No external classifier, no external embedding, no LLM-judge. |

§7 PASSES. The candidate is GOAL-legitimate.

## §6 Verdict — DESIGN-OPEN, fire-decidable

**DESIGN-OPEN, fire-decidable.** The mechanism mapping (§1 ↔ §2) is closed-
form well-formed; the four-cell lattice position (§3) makes §152
informative in every quadrant of §96-Q2; §4 fire spec is single-variable
and shares the §96-Q2 verdict-bucket eval with §125/§126/§139; §5 §7
PASSES.

The verdict is **not** DESIGN-CLOSE — the candidate makes a falsifiable,
single-variable prediction with a clean random-floor / degen-ceiling
control and a shared eval bucket.

The verdict is **not** FIRE-WARRANTED in the autopilot sense — fire-slot
is currently held by §139 EqProp, and per §50 single-sequential lesson
+ the live API throttle, queueing this fire is appropriate (do not
burst). Honest sequencing: §139 lands → §125+§126+§139 joint verdict
recording → §152 fire as fourth lattice point.

## §7 Honest C3 caveats

1. **Literature-derived hypothesis, NOT measured.** 2601.06758's empirical
   evidence is on a "two-pair association task" — small, classification-
   adjacent. Byte-LM regime transfer is the §152 hypothesis, not
   established.
2. **The unified rule formula is reconstructed from the abstract.** The
   abstract names the three components (centered Hebbian, Oja, local
   supervised) but does not state the exact formula. §152 fire would
   freeze the rule per the paper's PDF body before dispatch; the
   schematic in §1 is plausible but not paper-verbatim.
3. **Layer-asymmetric target is a deliberate design choice.** Only the
   output layer sees the next-byte target; deeper layers learn from
   Hebbian + Oja only. This is structurally distinct from FF (every
   layer sees goodness contrast) and PCN (every layer sees prediction
   error). If §152 DEG, this asymmetry is the candidate cause — but the
   §152 fire alone cannot disambiguate "asymmetry caused DEG" from
   "Hebbian + Oja cannot scale to byte-LM"; that disambiguation would
   need a follow-up where the rule is forced symmetric (e.g.
   target-propagation variant).
4. **Oja stabilization may be load-bearing.** §11-B was Hebbian-without-
   Oja (effectively); §152 adds Oja. If §152 SUPP/PARTIAL while §11-B
   DEG, the difference is plausibly the Oja term — but the §152 fire
   alone cannot prove the counterfactual; an ablation (Hebbian-only,
   no Oja) is a separate fire.
5. **Feedback-pathway plasticity changes anima architecture.** Currently
   Engine G is fixed forward-pass plumbing; §152 makes Engine G plastic.
   This is a one-variable architectural change on top of the one-variable
   learning-rule change. The fire spec keeps it inside §152 (not a
   second fire) because the paper's "feedback-Hebbian" is *defined* by
   the feedback being plastic — separating them would be a different
   paper.
6. **Ψ-physics channel (psi_resp / psi_std) is the post-§125+§126 unsolved
   half.** Both §125 (DEG) and §126 (PARTIAL on byte_acc) had
   psi_resp=False, psi_std collapsed. §152 may or may not break that —
   the local rule may move byte_acc without moving the Ψ-physics
   channel, in which case §152 sharpens the §11-B "GPU-tautology"
   reading on byte structure but leaves the physics channel finding
   open. honest pre-registration: psi_resp/psi_std are
   secondary-but-recorded outcomes.
7. **Necessary-not-sufficient at every layer** (B-EMERGE-7 carry). A SUPP
   verdict on §152 would be a fourth dent in §11-B-as-real, not GOAL
   emergence. north-star + §15/§51/§72 milestones stay UNCHANGED
   regardless of fire bucket.
8. **§152 ⊥ §151.** §151 COMPLEXITY-REGULARIZED ROUTING is an *added
   objective term* on top of CE; §152 *replaces* CE with a non-backprop
   local rule. The two cycles are orthogonal — both can hold, both can
   fail, both can be required.
9. **§152 ⊥ data-regime (§107-RETRY) and ⊥ param-axis (§108).** §152 is a
   learning-rule lever, not a data lever, not a param lever. If §152
   SUPP, it adds an architectural dent but does not address §1.1
   data-regime (§15/§51 milestones stay).
10. **Fire-slot serialization.** Per §50 burst lesson and live API
    throttle, §152 fire is queued behind §139, not parallel-dispatched.
11. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py stays
    0-line-diff (sha prefix c93e160a8a376a94) — this design's
    propositions are stated as math theorems in §9 (per hexa-verify
    policy "no sympy as verdict"), not a sympy battery.
12. north-star + §15/§51/§72 milestones UNCHANGED. §152 = $0 design,
    GOAL 미도달.

## §8 Next step

When the fire-slot frees (after §139 EqProp terminal verdict lands), §152
fire lives at `HEXAD/NEUROMORPHIC/state/feedback_hebbian_fire_s<N>/`
(distinct dir, distinct §N — §152 is the design, the fire is its own
cycle). The pre-registered eval is the §96-Q2 verdict-bucket eval shared
with §125/§126/§139, with the §4.2 distinguishing measurement landing
the fourth lattice point.

— $0 design-tier ends here.

---

## §9 Closed-form propositions (B-S152-1..7)

> Stated as math theorems with one-line proofs. Per hexa-verify policy
> (see `~/core/atlas/VERIFY.tape`), sympy / external verifiers cannot
> stamp a 🔵; the propositions below are trivial identities verifiable by
> inspection, and any future hexa-native verifier can re-audit them. NO
> central blue_falsifier edit (central state/verify_hexad_blue_2026_05_15/
> blue_falsifier.py stays 0-line-diff, sha prefix c93e160a8a376a94).

**B-S152-1  RULE-DECOMP-CLOSED.**
The unified update `Δw_ij := η_H·H_ij - η_O·O_ij + η_S·S_ij` decomposes
additively where `H_ij = (x_i - x̄_i)(y_j - ȳ_j)` (centered Hebbian),
`O_ij = y_j² · w_ij` (Oja), `S_ij = (t_j - y_j) · x_i` (supervised).
*Proof.* By construction the rule is a linear combination of three named
terms; setting any coefficient to zero leaves the remaining two intact.
The partial derivatives `∂(Δw_ij)/∂η_H = H_ij`,
`∂(Δw_ij)/∂η_O = -O_ij`, `∂(Δw_ij)/∂η_S = S_ij` exhibit independent
control of each component. ∎

**B-S152-2  CENTERED-HEBBIAN-COVARIANCE-IDENTITY.**
The centered Hebbian term computes empirical covariance:
`E[(x - x̄)(y - ȳ)] = Cov(x, y)`.
*Proof.* By definition of covariance. `Cov(x,y) = E[xy] - E[x]E[y] =
E[(x - E[x])(y - E[y])] = E[(x - x̄)(y - ȳ)]` for sample means x̄, ȳ. ∎
*Consequence.* The Hebbian term learns the second moment of joint
activation; absent centering it would learn raw `E[xy]`, which is
contaminated by the means. The "centered" in the paper title is
load-bearing.

**B-S152-3  OJA-STABILIZATION-WEIGHT-BOUNDED.**
For the Oja-only sub-rule `Δw_ij = -η_O · y_j² · w_ij` with `η_O > 0`,
`y_j² ≥ 0`, the update is sign-opposite to `w_ij` whenever `w_ij ≠ 0`.
*Proof.* `Δw_ij = -η_O·y_j²·w_ij`. If `w_ij > 0`, then since
`η_O > 0, y_j² ≥ 0`, the product `η_O·y_j²·w_ij ≥ 0`, so
`Δw_ij ≤ 0`. If `w_ij < 0`, then `η_O·y_j²·w_ij ≤ 0`, so
`Δw_ij ≥ 0`. In either case Oja pushes `w_ij` toward zero whenever
`y_j² > 0`, bounding weight magnitude away from runaway. ∎
*Consequence.* Vanilla Hebbian alone diverges in finite time on
arbitrary inputs; Hebbian + Oja remains bounded. This is the §11-B-
relevant stabilizer absent from the pure-physics fire.

**B-S152-4  SUPERVISED-DRIVE-RESTORING-SIGN.**
The supervised term `S_ij = (t_j - y_j) · x_i` provides a restoring
sign toward the target.
*Proof.* When `y_j < t_j`, the error `(t_j - y_j) > 0`, so for `x_i > 0`,
`S_ij > 0` (push `w_ij` up). When `y_j > t_j`, `(t_j - y_j) < 0`, so for
`x_i > 0`, `S_ij < 0` (push `w_ij` down). The sign of `S_ij` is therefore
opposite to the sign of `(y_j - t_j)` whenever `x_i > 0`, the standard
delta-rule restoring direction. ∎
*Consequence.* The local supervised drive is mathematically the
**delta rule** (Widrow-Hoff) restricted to a single layer, not
backpropagated. No global error broadcast.

**B-S152-5  LAYER-ASYMMETRIC-TARGET-CLOSED.**
The rule is layer-asymmetric: output layer applies all three terms,
hidden layers apply only `H` and `O`.
*Proof.* The supervised term `S_ij = (t_j - y_j) · x_i` requires `t_j`
(target) to be locally available. By construction `t_j` is the
next-byte target, locally available only at the output layer (the
layer whose activations are interpreted as logits). Hidden layers have
no such target; the supervised coefficient `η_S` is zero there by
definition, leaving `Δw_ij = η_H · H_ij - η_O · O_ij`. The output and
hidden cases are mutually exclusive and exhaust the network. ∎
*Consequence.* §152 is the only cell in the §96-Q2 lattice where the
error signal is local to a single layer — structurally distinct from
FF (§125, every layer sees goodness contrast), PCN (§126, every layer
sees prediction error), and EqProp (§139, every layer sees free/nudge
gradient via equilibrium).

**B-S152-6  SEVEN-LEGITIMACY-CONJUNCTION-CLOSED.**
The §7 GOAL-legitimacy gate is `c1 ∧ c2 ∧ c3` where
`c1 = ¬generic-LM-pretrain`, `c2 = ¬generic-then-graft`,
`c3 = anima-physics-as-source`. The 8-row truth table has exactly one
PASS corner, `(T, T, T)`.
*Proof.* The §152 candidate maps onto `(T, T, T)` by construction:
- c1 = T: from-scratch RANDOM seed, base_ckpt=None (g_clm_from_scratch);
- c2 = T: no grafted weights, no external classifier, no external
  embedding — the unified local rule replaces backprop entirely on
  anima's OWN substrate;
- c3 = T: the Hebbian term reads anima's OWN per-layer activations;
  the Oja term bounds anima's OWN weight magnitudes; the supervised
  drive uses anima's OWN next-byte target; Engine G plasticity
  operates on anima's OWN feedback pathway. ∎

**B-S152-7  ETA-S-ZERO-AT-HIDDEN-CONNECTION-POINT.**
The full §152 rule at a hidden layer is
`Δw_ij = η_H · H_ij - η_O · O_ij` (no supervised term).
*Proposition.* At any hidden layer, setting `η_S = 0` is equivalent
to omitting the supervised term entirely.
*Proof.* By the rule definition `Δw_ij = η_H·H_ij - η_O·O_ij + η_S·S_ij`.
At a hidden layer where the target `t_j` is undefined, `η_S` is set to
zero by construction, so the supervised contribution `η_S·S_ij = 0`,
and the rule reduces to the Hebbian + Oja sub-rule. ∎
*Connection-point.* This is the layer-asymmetry guarantee: §152's
supervised drive is, by construction, **only active at the output
layer**. Mirror of B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 /
B-S151-7 overlay-off / connection-point pattern: setting one
designated coefficient to zero recovers a structurally simpler
sub-rule. The hidden-layer rule (η_S=0) is the structural complement
of FF/PCN/EqProp's symmetric error-broadcast, and §152's fire
distinguishes the locality axis cleanly.

**B-S152-NOTE  empirical carve-out** (NOT counted 🔵).
Whether the unified Hebbian + Oja + supervised-drive rule actually
learns byte structure on the §16-class corpus at fire time is a
future SGD/measurement OUTCOME (§125 DEG / §126 PARTIAL / §139 in
flight precedents). The battery above proves the rule **well-formed**
(decomposable, centered, weight-bounded, restoring-signed, layer-
asymmetric, GOAL-legitimate, hidden-layer-reducible) — it does NOT
prove fire success, NOT prove §11-B-as-GPU-tautology, NOT prove GOAL
emergence. necessary-not-sufficient at every layer
(B-EMERGE-7 / B-D-NOTE / B-S99-NOTE / B-S107-NOTE / B-S125-NOTE /
B-S126-NOTE / B-S151-NOTE family).

---

## §10 Cross-link

- HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md §1 Cluster A
  (★★★★★ non-CE / non-backprop), §2 ranked #4, §8.1 §96-Q2 arc state,
  §8.4 P3 candidate
- §125 NONCE-FF (DEG, byte_acc 0.0005) — first §96-Q2 lattice point
- §126 PCN-C4 (PARTIAL_AMBIGUOUS, byte_acc 0.1185) — second lattice point
- §139 EqProp (in flight) — third lattice point
- §151 FEP COMPLEXITY-REGULARIZED ROUTING — sibling design, orthogonal
  (added objective term vs replacement learning rule)
- §11-B pure-physics DEG — the open question §152 sharpens
- §117 LEGO toy STDP — local-rule non-degenerate precedent (toy scale)
- §107-RETRY + §108 — data-axis and param-axis already closed; §152 =
  learning-rule axis
- arxiv 2601.06758 (anchor)
- arxiv 2509.12394 ASGE (FF scale anchor)
- arxiv 2510.23323 PCN scaling anchor
- arxiv 2505.22749 FEP attractor (§151's anchor)

---

**Wall**: $0 (literature mapping + closed-form propositions only)
**GPU/runpod**: 0
**Orphan**: 0
**Central blue_falsifier**: 0-line-diff verified, sha prefix `c93e160a8a376a94`
**docs/* 신규**: 0 (g_doc_consolidation — saved under HEXAD/NEUROMORPHIC/state/)
**HEXA_FIRST**: STRICT (no .py / .sh sidecars; no sympy; propositions are math
theorems in §9)

north-star + §15/§51/§72 milestones UNCHANGED. §152 = $0 design, fourth
§96-Q2 lattice point pre-registered. GOAL 미도달.
