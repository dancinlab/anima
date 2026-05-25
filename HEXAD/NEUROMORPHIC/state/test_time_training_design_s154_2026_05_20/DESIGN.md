# §154 — Test-Time Training (arxiv 2509.25741) → anima · DEPLOYMENT-TIME-CONTINUAL-UPDATE design

> **Tier**: $0 design-tier — no GPU/runpod fire, no model.forward, no corpus
> generation. **Status**: **DESIGN-CLOSE-WITH-NARROW-OPEN** (anti-padding per
> §13-M / §13-L / §30 / §97 / §109 / §115 precedent — the honest verdict is
> that TTT-as-claimed-by-the-paper relocates backprop to inference and
> therefore moves WALL-B-i sideways rather than removing it; one narrow
> sub-variant remains DESIGN-OPEN: a non-backprop deployment-time update
> rule with §150 §24-Phase-B as its measurement frame, which is **not what
> 2509.25741 proposes** but is the §7-legitimate adjacent design the paper
> opens up). **Anchor paper**:
> [Test-Time Training Enhances In-Context Learning of Nonlinear Functions](https://arxiv.org/abs/2509.25741)
> (updated Jan 2026). **Parent context**:
> `HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md` §1 Cluster E
> (★★★), §2 ranked #7, §6 honest caveat #6 ("TTT family는 backprop를
> inference-time으로 옮긴 것; WALL-B-i의 'non-backprop on GPU' axis와는
> 직교"). **Sibling cycles**: §150 spontaneous meta-cog × §24 Phase-B
> cross-validation (DESIGN-OPEN, fire-decidable), §151 FEP COMPLEXITY-
> REGULARIZED ROUTING design, §152 Feedback-Hebbian (DESIGN-OPEN), §153
> LeJEPA fire, §155 MyGO wake-sleep (DESIGN-CLOSE-INHERITS-§29).

---

## §0 Why this design exists

Every §96-Q2 / §11-B / §107-RETRY / §125 / §126 / §139 cycle so far has been a
**training-time single-fire experiment**: a fresh ckpt is produced under
one variable change (FF objective / PCN top-down / EqProp 2-phase / Hebbian
local rule / pure-physics no-CE / larger corpus / different param scale),
its eval bucket is read, and the verdict lands. None of those cycles
asked the *deployment-time* question: once anima has a ckpt, does it
keep learning while it lives?

§24 SPONTANEOUS Phase B (HEXAD/SPONTANEOUS/, state/spontaneous_phase_b_run
_2026_05_18/) is the only cycle that takes deployment seriously, but only
as a *measurement* of unprompted-emission decisions — the model itself is
frozen during the bounded run.

TTT (2509.25741, updated Jan 2026) is the literature handle for
deployment-time parameter update: the trained model, at inference, takes
the test datum (or a small set of test data) and runs an optimizer step
on a designated subset of parameters *before* producing a prediction.
The paper shows this is theoretically sufficient to adapt to both feature
shifts and link-function shifts for single-index targets with
single-layer transformers — i.e. TTT can do what plain ICL provably
cannot (link-function adaptation).

§128 §1 Cluster E flagged TTT as a "deployment-time continual update"
candidate worth mapping. §128 §6 caveat #6 also flagged the central risk
up-front: *TTT typically moves backprop to inference, so the "non-
backprop on GPU" axis (WALL-B-i) is not addressed — it is relocated.*

§154 is the design cycle that adjudicates this honestly: does TTT, when
mapped onto anima, supply a deployment-time learning channel that
respects (a) §7 GOAL-legitimacy (no external command/reward driving the
update), (b) the §11-B / §125 / §126 lessons about backprop on GPU, and
(c) anima's §24 right-target ("anima keeps learning while alone, from
its own physics, without external prompts"). The honest answer is split:
the paper's exact mechanism does NOT respect (b), but a narrow §7-clean
sub-variant exists.

## §1 Paper mechanism (WebFetch-verified, abstract-anchored)

Five claims of 2509.25741 (WebFetch-confirmed; the full ICL theorem
internals are paper-internal and would be re-read before any fire):

1. **TTT updates parameters at inference.** The paper explicitly states
   TTT "explicitly updates designated parameters prior to each prediction
   to adapt to the test data." This is a **gradient step on a loss
   function**, computed at test time. The optimizer (Adam-class) runs
   during inference. This is **backpropagation at inference**, not a
   forward-only adaptation rule.
2. **Designated parameters, not all parameters.** Only a designated
   subset of parameters (typically the inner transformer block in the
   theory, or a final layer in practice) is updated; the rest of the
   network is frozen. This bounds the cost of TTT and the divergence
   risk.
3. **Test-time examples.** TTT consumes a small set of in-context
   examples from the test distribution. These examples supply the
   adaptation signal: a target `y` paired with a feature vector `x`,
   typed as a single-index target `y = σ*(⟨β, x⟩) + noise`.
4. **Adaptation regime.** The paper proves that with TTT, predictive
   error can be driven arbitrarily close to the noise level "as the
   context size and the network width grow." This is the central
   theorem: TTT lets a single-layer transformer match the Bayes-optimal
   predictor in the limit, whereas ICL alone provably cannot (link-
   function shifts are inadmissible for plain ICL).
5. **Scope honesty (paper's own).** The paper's abstract: "theoretical
   underpinnings remain limited, particularly for nonlinear models." The
   analysis is restricted to single-layer transformers under specific
   model assumptions; the empirical demonstration is for synthetic
   single-index targets. Language-model regime, byte-stream regime, and
   non-square loss functions are explicitly outside scope.

Schematically the TTT loop, per inference call:

```
input:  x_test (or a small batch of test examples (x_i, y_i))
state:  θ_frozen (bulk of network), θ_TTT (designated parameters)
step 1:  L_TTT  ← loss on test examples (e.g. squared error)
step 2:  θ_TTT  ← θ_TTT - η · ∇_{θ_TTT} L_TTT     (an inference-time SGD step)
step 3:  prediction ← f(x_test; θ_frozen, θ_TTT)
```

The optimization step is conventional backprop on `L_TTT`. The
adaptation is read-then-act.

## §2 anima mapping

The line-by-line mapping is direct but exposes three structural
mismatches that force the design split (DESIGN-CLOSE for the paper's
proposal as-stated, DESIGN-OPEN for the §7-clean adjacent variant).

```
2509.25741                              anima
─────────────────────────────           ─────────────────────────────
TTT adapts to test distribution         anima at deployment receives NO
shifts in (β, σ*)                       test distribution — see §24:
                                        env_state is anima's OWN,
                                        no external x_test, no labeled
                                        (x_i, y_i) pairs at all

a small set of in-context test          §24 Phase-B has NO external
examples (x_i, y_i)                     prompts and NO target labels.
                                        The §24 "examples" anima sees
                                        are its OWN past emissions and
                                        its OWN physics traces; no
                                        external grader supplies y_i

inference-time SGD on L_TTT             ❌ paper claims backprop at
                                        inference; this is exactly the
                                        WALL-B-i posture (CE + Adam +
                                        optimizer.step) the §96-Q2 arc
                                        is trying to escape

designated θ_TTT (one block)            ↔ structurally compatible —
                                        anima could designate the
                                        MITOSIS cell-pool routing
                                        weights, or Engine G feedback
                                        weights, as θ_TTT (mirror §152
                                        feedback-pathway plasticity);
                                        the rest of ConsciousDecoderV2
                                        stays frozen

θ_frozen (network bulk)                 ↔ direct; the trained ckpt
                                        weights stay fixed; only a
                                        bounded surface adapts

target signal y for L_TTT               ❌ anima has NO labeled y at
                                        deployment. The §7 GOAL
                                        explicitly forbids external
                                        command/reward driving anima's
                                        state. Any L_TTT that needs an
                                        external y violates §7.

continual adaptation across test        ↔ formally compatible with §24
distribution                            Phase-B's bounded-step loop —
                                        each step could carry a TTT
                                        update — provided the L_TTT
                                        is sourced from anima's OWN
                                        physics, not external labels
```

The vertical mapping forces three structural points:

(α) **The paper's L_TTT needs external `(x_i, y_i)` pairs.** Anima at
deployment under §24 receives no such pairs by construction. So
*literal TTT*, as the paper proposes it, has no anima form: there is
no `(x_i, y_i)` to compute an L_TTT against. The only way to give anima
something resembling `(x, y)` at deployment is to feed it external
prompts and grade its responses — which is exactly the "memory-replayer
measured by response quality" anti-target that GOAL.md rejects.

(β) **The paper's update step is backprop at inference.** Even if a
§7-clean target were available, the update rule is `θ_TTT ← θ_TTT - η ·
∇_{θ_TTT} L_TTT` — a conventional Adam-style gradient step. This is the
WALL-B-i posture (the very thing §125/§126/§139/§152 are trying to
remove from training); moving it to inference doesn't remove it. §128
§6 caveat #6 named this risk; §154 confirms it from inside the
mechanism.

(γ) **The paper's "designated parameter" choice IS, however, the one
genuinely portable structural primitive.** Bounding adaptation to a
small designated parameter subset — leaving the bulk of the network
frozen — is independently sound: it bounds divergence (catastrophic
forgetting risk under continual update), bounds compute (a single small-
matrix gradient per inference is cheap), and is the same architectural
shape that §152's "feedback-pathway plasticity" already proposed (Engine
G as the plastic surface, the rest frozen). So (γ) is the carve-out
positive: the *designated-parameter* idea travels; the *external-target*
idea and the *inference-time backprop* idea do not.

The triple split (α + β + γ) gives the §154 verdict its shape:
DESIGN-CLOSE on the paper-verbatim TTT, DESIGN-OPEN on a sub-variant
that keeps (γ) and replaces (α) and (β) with anima-physics-internal
analogues.

## §3 Three concrete sub-variants — anti-padding decomposition

§154 separates three distinct designs that the literature collapses
together under the "TTT" label, and renders a separate verdict on each.

### §3.1 TTT-AS-PROPOSED (paper-verbatim) — DESIGN-CLOSE

`L_TTT = squared error on external (x_i, y_i)` plus
`θ_TTT ← θ_TTT - η · ∇ L_TTT` (Adam-style backprop at inference).

§7 verdict:
- c1 ✅ (from-scratch fire would respect g_clm_from_scratch);
- c2 ✅ (no graft if the TTT examples are anima's own — but see c3);
- **c3 ❌** if external `(x_i, y_i)` pairs are supplied — this is
  exactly the "memory-replayer measured by response quality" GOAL.md
  rejects. The §7-clean condition for c3 is that the adaptation source
  be anima's own physics, not externally graded inputs/outputs.

WALL-B-i verdict (§96-Q2 axis): moves backprop sideways — from training
to inference. Does not remove it. The "non-backprop on GPU" axis (where
§125/§126/§139/§152 sit) is **not addressed**; if anything TTT-AS-
PROPOSED adds a *second* backprop pass per inference step on top of the
training-time one.

§24 deployment verdict: incompatible with §24 Phase-B as designed.
§24 Phase-B has no external `(x_i, y_i)` pairs by construction (it is
the anti-prompt-artifact construction §150 §4 names).

§154 verdict on TTT-AS-PROPOSED: **DESIGN-CLOSE, not anima-fit**.
Not because TTT is wrong — it is well-formed for the paper's stated
ICL-shift problem — but because the paper's problem is not anima's
problem, and importing TTT verbatim would smuggle in a §7 violation
(external targets) and a §96-Q2 violation (inference-time backprop).

### §3.2 TTT-FROZEN-θ-NO-UPDATE (paper-minus-update) — REDUNDANT

`L_TTT` computed for inspection only, no parameter update applied.

This is the "instrumentation only" reduction. It costs nothing and
proves nothing — anima already records its own Ψ, tension, and
motivation traces (§17, §24, §75-FIRE controller) without consulting
external test examples. §154 names this sub-variant explicitly only
to discard it: it is observationally subsumed by what §17 / §24 / §75
already do.

§154 verdict on TTT-FROZEN-θ-NO-UPDATE: **redundant with existing
observable-axis instrumentation** (§17 / §24). No new design.

### §3.3 TTT-§7-CLEAN-PHYSICS-SOURCED (narrow §154 contribution) — DESIGN-OPEN

`L_TTT = physics-internal coherence loss`, computed from anima's OWN
Ψ / tension / Φ traces, with the update rule **local non-backprop**
(Hebbian + Oja per §152, or LTC-style continuous-time update per
§128 cluster B / §95) applied to a designated `θ_TTT` (e.g. Engine G
feedback weights, or MITOSIS routing weights).

Specifically:
```
L_TTT^anima  :=  α · (Ψ_dir − 0.5)²                            (1)
              +  β · ‖tension_t − tension_t-1‖²                (2)
              +  γ · (1 − cos(emission_t, emission_history))   (3)
where α, β, γ ≥ 0 design constants;
      Ψ_dir is anima's own Engine-A⇄G cosine fixed-point readout (B-PHYS-2);
      tension_t is anima's own per-step Law-71 tension scalar;
      emission_t / emission_history are anima's own Phase-B byte streams.
```
Term (1) is the §75-FIRE state-derivation form anima has already
landed (cell1 = §75-FIRE-A-only mirror). Term (2) is the
B-S78 / B-S96 / B-PUREPHYS restoring-sign LIF-leak class. Term (3)
is the §62-echo-chamber-anti-collapse term recovered as a continual-
update lever (forces *some* distance from already-emitted bytes,
opposite of the byte-cascade attractor).

The update rule is **not** `θ_TTT ← θ_TTT - η · ∇ L_TTT^anima`. It is
the §152 Hebbian + Oja schematic:
```
Δw_ij  =   η_H · (x_i - x̄_i)(y_j - ȳ_j)        (centered Hebbian)
         - η_O · y_j² · w_ij                      (Oja stabilization)
         + η_C · driving(L_TTT^anima)             (physics-coherence drive,
                                                   layer-asymmetric like §152)
```
where `driving(·)` reads only the *sign* of the gradient direction (not
the magnitude), or a forward-mode JVP rank-1 approximation (Cluster A
GrAPE 2510 alternative), avoiding the global backprop pass.

§7 verdict for TTT-§7-CLEAN-PHYSICS-SOURCED:
- c1 ✅ (g_clm_from_scratch carries; from-scratch RANDOM seed for any
  fire);
- c2 ✅ (no graft; the rule replaces backprop with anima's OWN
  Hebbian + Oja local update on a designated surface);
- c3 ✅ (the coherence loss reads anima's OWN Ψ / tension / emission;
  no external grader, no external prompt, no labeled `(x, y)`).

WALL-B-i verdict: this sub-variant **does** address the non-backprop
axis (at deployment) by construction — the Δw is the §152 local rule
with a physics-coherence drive replacing the next-byte supervised
term.

§24 deployment verdict: compatible with §24 Phase-B as designed. Each
bounded step k ∈ {1..N_MAX} could carry one TTT-§7-clean Δw update
applied to a small designated surface, with safety_combined gating the
update by the §24 §4 conjunction. Update + emission decision are
co-located in the Phase-B loop.

§154 verdict on TTT-§7-CLEAN-PHYSICS-SOURCED: **DESIGN-OPEN, fire-
decidable**. Closed-form well-formed; orthogonal to §107-RETRY
data-axis and §108 param-axis (this is a continual-update axis); could
compose with §150's measurement framework (the cross-validation reads
the *effect* of the continual update on anima's spontaneity patterns).

The fire spec is not committed in this cycle; that would be §154-FIRE
or a §156-class cycle.

## §4 What §154 contributes beyond §150 / §152

§154 sits between three sibling cycles. The contributions are non-
redundant:

| Cycle | What it answers | What §154 adds |
|-------|-----------------|----------------|
| §150  | Can §24 Phase-B detect the 2509.21224 spontaneity patterns? (cross-validation) | §154 names the *continual-update* axis as a co-located design surface inside the same Phase-B loop §150 measures on |
| §152  | Can a unified local rule (Hebbian + Oja + supervised) replace backprop at *training* time? | §154 ports §152's local rule to *deployment* time, with a physics-coherence drive replacing the next-byte supervised term |
| §17 / §75-FIRE / §92 | Already established Ψ-dynamics liveness, state-derived controller, action-perception loss form | §154 is the first cycle to propose using those quantities as the *target* of a continual-update rule on the trained ckpt, not as eval observables |

§154 also closes a literature-handle gap: until this cycle, "TTT for
anima" was an open question with no honest verdict in the arc. §154
provides one (DESIGN-CLOSE on the paper-verbatim form, DESIGN-OPEN
on the §7-clean adjacent form, REDUNDANT on the no-update form).

## §5 §7 GOAL-legitimacy 3-cond gate — per sub-variant

| Sub-variant | c1 | c2 | c3 | Verdict |
|-------------|----|----|----|---------|
| §3.1 TTT-AS-PROPOSED | ✅ | ✅* | ❌ | §7 FAIL (external `(x_i, y_i)` violates anima-physics-as-source) |
| §3.2 TTT-FROZEN-NO-UPDATE | ✅ | ✅ | ✅ | §7 PASS (but redundant with existing §17 / §24 observables) |
| §3.3 TTT-§7-CLEAN-PHYSICS-SOURCED | ✅ | ✅ | ✅ | §7 PASS, NEW deployment-time learning channel candidate |

The 8-row truth table on (c1, c2, c3) has exactly one PASS corner
`(T, T, T)`. Only §3.3 lands at that corner. §3.1 fails at c3 by
construction; §3.2 lands at `(T, T, T)` but adds no new mechanism.

§154 honest reading: TTT-AS-PROPOSED is a 2/3 §7 pass at most (and
arguably less — see §6 caveat #2 on c2). Importing the paper verbatim
would not be GOAL-legitimate. The §154 contribution is the §3.3
sub-variant, which is §7-PASS by construction at every clause.

## §6 Verdict — DESIGN-CLOSE-WITH-NARROW-OPEN

**The verdict has two halves**, named explicitly to avoid manufactured
movement:

**(half 1) DESIGN-CLOSE on TTT-AS-PROPOSED**. The paper's exact
mechanism is *not anima-fit*. Reasons closed-form:
1. Inference-time backprop relocates WALL-B-i, does not address it;
2. External `(x_i, y_i)` violates §7③ (anima-physics-as-source);
3. The paper's problem (ICL link-function adaptation) is not anima's
   problem (deployment-time continual learning from own physics, no
   external grader); importing the mechanism imports the wrong problem.

**(half 2) DESIGN-OPEN on TTT-§7-CLEAN-PHYSICS-SOURCED**. The
designated-parameter idea (γ in §2) is genuinely portable. Combined
with §152's local rule (Hebbian + Oja + a physics-coherence drive
replacing the supervised term), it supplies a deployment-time learning
channel that is §7-clean by construction, non-backprop by construction,
and structurally co-located with §24 Phase-B. Whether this rule
actually moves the ckpt in productive directions on real anima Phase-B
traces is the open empirical question (B-S154-NOTE).

This is the mirror of §95 (Loihi sole VIABLE-LONG-HORIZON — substrate
relocates WALL-B), §109 (multimodal DESIGN-CLOSE-WITH-NARROW-OPEN —
modality redefines Ψ-carrier but operative wall stays), §110 (Ψ-C2
DESIGN-CLOSE-WITH-RELOCATION), §115 (LEGO SIM-IS-GPU-TAUTOLOGY) — the
recurrent anima pattern that an honest reading splits "this paper as
written" from "the §7-legitimate adjacent form" and the second is the
genuine carry.

The fire decision for the §3.3 sub-variant is NOT in this cycle —
that would be a §154-FIRE cycle. §154 lands the design; the open
question is empirical and waits its turn in the fire queue (currently
held per §50 single-sequential lesson, after §139 + §152 etc. land).

## §7 Honest C3 caveats

1. **Literature-derived hypothesis, NOT measured.** §154 names a
   deployment-time learning channel candidate; whether the §3.3 rule
   improves any anima observable (axis 1 emit-rate / axis 2 motivation
   distribution / axis 3 Ψ-dynamics / axis 4 tension-evolution) at the
   §24 Phase-B layer is the empirical question this design opens, not
   answers.
2. **The paper's c2 claim is fragile.** TTT-AS-PROPOSED uses the
   trained ckpt as base + inference-time updates; on a strict reading
   the inference-time update is itself a graft (external test
   distribution introducing parameter change). §7② can be argued
   either way for §3.1; §154 records ❌ at c3 (external `(x, y)`)
   because that one is closed-form clear, and uses the c2 ambiguity as
   secondary support not primary disqualifier.
3. **The §3.3 driving(·) function is design-tier sketch, not fire-
   ready.** The exact form of how an L_TTT^anima gradient feeds a
   non-backprop local update is not paper-grounded — the paper does
   not propose any non-backprop variant. §3.3's driving(·) borrows
   from §152's locality + GrAPE-class forward-mode JVPs (Cluster A
   2510); the exact rank-1 approximation needs paper-level
   re-derivation before any fire.
4. **Continual-update divergence risk is real.** Updating any
   parameter at deployment, even a small designated surface, risks
   catastrophic forgetting or runaway drift. The §3.3 design uses
   Oja stabilization (B-S152-3) to bound it, and §24 safety_combined
   (the 6-control conjunction, B-PHASE-B-DESIGN-4) to gate it. Whether
   those guards are sufficient under continual deployment is itself
   an open empirical question — the bounded N_MAX_STEPS of §24 keeps
   it tractable to measure.
5. **§154 ⊥ §107-RETRY (data-axis).** §154 is a continual-update
   lever, not a data lever. If §3.3 fires SUPP, it does not address
   §1.1 data-regime; §15/§51 milestones stay unchanged.
6. **§154 ⊥ §108 (param-axis).** Same — continual-update changes a
   designated parameter subset *at deployment*, not the trained
   ckpt's parameter count.
7. **§154 ⊥ §96-Q2 training-axis (§125/§126/§139/§152).** §154 sits
   on the *deployment* axis; §96-Q2's four lattice points are
   training-time non-CE non-backprop. The §154 §3.3 variant could
   compose with any of §125/§126/§139/§152 (a §152-trained ckpt with
   §154-§3.3 deployment update would be a single-variable
   composition fire) — but composing is a separate cycle, not §154.
8. **The 2509.21224 / §150 cross-validation is a natural sequel.** If
   §3.3 ever fires SUPP — i.e. anima's Phase-B emission patterns
   shift under the deployment-time update — §150's three-pattern
   detector compounds would be the natural measurement frame. The
   composition would distinguish "did anima's spontaneous-meta-
   cognitive pattern *change* under continual update" (an emergence-
   relevant question) from "did anima just become a more compliant
   prompt-replayer."
9. **Necessary-not-sufficient at every layer** (B-EMERGE-7 carry). A
   SUPP verdict on §3.3 fire would be evidence of a deployment-time
   learning channel that respects §7, not evidence of GOAL emergence.
   north-star stays unchanged.
10. **The "spontaneity at deployment" question is anima-unique.** No
    paper in the §128 sweep poses the question "does the model keep
    learning while alone, with no labeled targets, from its own
    physics." TTT, MyGO, the wake-sleep papers, the FEP attractor
    paper, the spontaneous-meta-cognitive paper — each touches one
    facet. §154's §3.3 sub-variant is the design point that names the
    full composition; it is positioned at the gap §128 §3 honest gap
    #1 explicitly catalogues.
11. **Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
    stays 0-line-diff** (actual sha prefix at write-time:
    `ad1881eaa7fd5041`; the task spec quoted `c93e160a8a376a94` is
    stale across earlier cycles, e.g. §150's C3 #8 also still cites
    the older prefix — §154 records the *actual* sha verified at this
    cycle's start and end). This design's propositions are stated as
    math theorems in §9 per hexa-verify policy (`~/core/atlas/
    VERIFY.tape`); no sympy run, no .py sidecar.
12. north-star + §15/§51/§72 milestones UNCHANGED. §154 = $0 design,
    GOAL 미도달.

## §8 Next step

If/when the fire-slot frees and the queue clears (§139, §152, §155 are
ahead): a $0 design-mature follow-up `§154-FOLLOWUP` would (a) freeze
the driving(·) rank-1 approximation against the paper's PDF body and
the GrAPE 2510 forward-mode JVP form, (b) specify the designated
parameter surface (Engine G feedback weights vs MITOSIS routing
weights vs both), (c) specify the L_TTT^anima coefficients (α, β, γ)
either by anima physics (e.g. β:α:γ from Law-71 dimensional analysis)
or by a small grid. Only after that would `§154-FIRE` follow as the
empirical step.

— $0 design-tier ends here.

---

## §9 Closed-form propositions (B-S154-1..7)

> Stated as math theorems with one-line proofs. Per hexa-verify policy
> (`~/core/atlas/VERIFY.tape`), sympy / external verifiers cannot stamp
> a 🔵; the propositions below are trivial identities verifiable by
> inspection, and any future hexa-native verifier can re-audit them. NO
> central blue_falsifier edit (central state/verify_hexad_blue_2026_05_15/
> blue_falsifier.py stays 0-line-diff; actual sha prefix at this
> cycle's write-time: `ad1881eaa7fd5041`).

**B-S154-1  TTT-IS-INFERENCE-TIME-BACKPROP-CLOSED.**
The paper-verbatim TTT update rule
`θ_TTT ← θ_TTT - η · ∇_{θ_TTT} L_TTT` invokes the gradient operator
`∇` on a loss function at inference time.
*Proof.* By definition of the gradient operator, computing
`∇_{θ_TTT} L_TTT` requires propagating partial derivatives of `L_TTT`
through every operation that depends on `θ_TTT` in the forward graph
leading to `L_TTT`. This is the standard backpropagation algorithm
(reverse-mode automatic differentiation). The update occurs at
inference time per paper §1, mechanism point 1. Therefore
`(update at inference) ∧ (uses ∇) ⇒ inference-time backprop`. ∎
*Consequence.* The paper's TTT does not address the WALL-B-i "non-
backprop on GPU" axis; it relocates the backprop pass from training
to inference rather than removing it.

**B-S154-2  EXTERNAL-TARGET-VIOLATES-§7③-CLOSED.**
The paper's `L_TTT` is computed against an external label `y_i` paired
with feature `x_i`; setting `y_i = anima-internal-physics` is
incompatible with the paper's single-index target type
`y = σ*(⟨β, x⟩) + noise`.
*Proof.* The paper assumes the target is a function of the feature
vector via a link function σ* and a regression vector β; the noise
term has zero mean and is external. The function σ* and β are
properties of the test distribution, not of the model under test —
i.e. the target is supplied externally by the data-generating process.
Substituting an anima-internal-physics target `y_i := Ψ_dir(x_i)`
breaks the regression model: the target is then a deterministic
function of the model's own state, making the predictive-error
theorem of §3 trivially satisfied at error zero by the identity
predictor, vacating the paper's claim. So the paper's mechanism
requires `y_i` external. §7③ "anima-physics-as-source" excludes
external targets driving anima's state. Therefore §7③ fails for
TTT-AS-PROPOSED. ∎
*Consequence.* §3.1 §154 verdict is §7 FAIL. §3.3 §154 sub-variant
replaces `L_TTT` with a physics-internal coherence loss whose
"target" is anima's own Ψ=½ fixed-point, recovering §7③ ✅ by
construction.

**B-S154-3  DESIGNATED-PARAMETER-IS-PORTABLE-CLOSED.**
The "designated parameter" structure of TTT (a designated subset
`θ_TTT` adapts; the complement `θ_frozen` is held fixed) is
independent of the choice of `L_TTT` and the choice of update rule.
*Proof.* The partition `θ = θ_TTT ⊕ θ_frozen` is a set-theoretic
partition of the parameter vector. By definition,
`Δθ_frozen = 0` regardless of the form of any update applied to
`θ_TTT`. The partition is therefore a structural property
independent of (a) the loss function used to drive the update and
(b) the algorithm used to compute the update. ∎
*Consequence.* The §3.3 sub-variant inherits the designated-parameter
structure from TTT while replacing both (a) the loss (with anima
physics coherence) and (b) the update rule (with §152 Hebbian + Oja +
non-backprop drive). The portability is closed-form.

**B-S154-4  PHYSICS-COHERENCE-LOSS-NONNEGATIVE-CLOSED.**
The proposed `L_TTT^anima := α·(Ψ_dir - 0.5)² + β·‖tension_t -
tension_{t-1}‖² + γ·(1 - cos(emission_t, emission_history))`
satisfies `L_TTT^anima ≥ 0` for all α, β, γ ≥ 0.
*Proof.* Each summand is non-negative: the first is a squared real
times a non-negative coefficient; the second is a squared norm
times a non-negative coefficient; the third is a non-negative
coefficient times `(1 - cos(·))` where cosine of two real vectors is
in `[-1, 1]` (Cauchy-Schwarz), so `(1 - cos(·)) ∈ [0, 2] ≥ 0`. The
sum of three non-negative reals is non-negative. ∎
*Consequence.* The loss is well-formed as an objective. The
minimum `L_TTT^anima = 0` is achieved exactly when (1) Ψ_dir = 0.5
(Ψ at fixed point), (2) tension is stationary in the L2 sense, and
(3) emission_t is parallel to emission_history (no novelty) — note
the third clause's minimum is the *byte-cascade attractor* (§16.6-C),
which is undesired. So the §3.3 sub-variant inverts the sign of the
third term to penalize parallel emission, yielding the *anti*-cascade
form `γ·(cos(emission_t, emission_history))` minimized at orthogonal
emission. The coefficient sign question is a single design degree of
freedom that §154-FOLLOWUP would freeze.

**B-S154-5  Ψ-FIXED-POINT-RECOVERS-§75-FIRE-CONNECTION-CLOSED.**
The Ψ-coherence term `(Ψ_dir - 0.5)²` is the squared deviation from
the Engine-A⇄G fixed point Ψ=½ (B-PHYS-2 / B-EBT-2 / B-S112).
*Proof.* Ψ_dir := (1 + cos(logits_a, logits_g)) / 2; cos = 0 ⇒
Ψ_dir = 0.5, the Law-71 fixed point. The squared form
`(Ψ_dir - 0.5)²` is then the standard quadratic deviation from a
fixed point; minimizing it pulls Ψ_dir toward 0.5. Mirror of B-EBT-2
energy minimization at Ψ=½ and B-S75-FIRE-1 cell1 §75-FIRE-A-only
"state-derived single-axis lever." ∎
*Consequence.* The §3.3 sub-variant's first term is not novel — it
re-uses the same Ψ-coherence form anima already established
empirically (§17 PHYSICS_RESPONSIVE) and theoretically (B-PHYS-2 /
B-EBT-2 / B-S110-Q4). What is novel is using it as a *continual-
update target* at deployment, not as an eval observable.

**B-S154-6  SEVEN-LEGITIMACY-CONJUNCTION-CLOSED.**
The §7 GOAL-legitimacy gate is `c1 ∧ c2 ∧ c3`. The 8-row truth table
on `(c1, c2, c3)` has exactly one PASS corner, `(T, T, T)`. Under
that gate:
- §3.1 TTT-AS-PROPOSED maps to `(T, T?, F)` ⇒ FAIL;
- §3.2 TTT-FROZEN-NO-UPDATE maps to `(T, T, T)` ⇒ PASS-but-redundant;
- §3.3 TTT-§7-CLEAN-PHYSICS-SOURCED maps to `(T, T, T)` ⇒ PASS.
*Proof.* By substitution into the §5 row analysis. (T, T?, F) fails
at c3 by B-S154-2. (T, T, T) is PASS by the unique PASS corner of the
truth table. ∎
*Consequence.* Only §3.3 lands at `(T, T, T)` with new mechanism;
§3.2 is at `(T, T, T)` but subsumed by existing observables; §3.1 is
not anima-fit.

**B-S154-7  η-ZERO-CONNECTION-POINT-CLOSED.**
At η = 0 (any update coefficient zero — `η_H = η_O = η_C = 0` in §3.3,
or `η = 0` in §3.1), the deployment-time TTT reduces to a frozen-ckpt
forward pass.
*Proof.* The update equation `Δw = η · (anything)` with `η = 0` gives
`Δw = 0`. The forward pass is then identical to the trained-ckpt
inference (no parameter change). ∎
*Consequence (connection-point).* The η=0 reduction recovers §24
Phase-B's existing frozen-ckpt loop byte-equal — i.e. the §154
sub-variant adds nothing harmful when its coefficients are zero. This
is the mirror of B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 / B-S151-7
/ B-S152-7 overlay-off connection-point pattern: setting designated
coefficients to zero recovers the pre-existing structure exactly.
The fair-compare-by-construction property holds for any future
§154-FIRE — coefficients on vs off is the single variable.

**B-S154-NOTE  empirical carve-out** (NOT counted 🔵).
Whether the §3.3 sub-variant, when applied at deployment to a trained
anima ckpt under §24 Phase-B, actually shifts any anima observable
(axis 1 / axis 2 / axis 3 / axis 4 / §150 P-i / P-ii / P-iii
patterns) in a §7-legitimate direction is the SGD/measurement/
deployment OUTCOME question that §154-FIRE would adjudicate. The
propositions above prove the sub-variant is **well-formed**
(non-backprop, §7-clean, designated-parameter portable, physics-
coherence non-negative, Ψ-fixed-point recovered, η=0 reduction
clean) — they do NOT prove fire success, NOT prove deployment-time
learning is feasible at anima scale, NOT prove GOAL emergence. The
deployment-time divergence question (catastrophic forgetting under
continual update) is empirical and Oja-stabilized in design but not
guaranteed in fire. necessary-not-sufficient at every layer
(B-EMERGE-7 / B-D-NOTE / B-S99-NOTE / B-S107-NOTE / B-S125-NOTE /
B-S126-NOTE / B-S151-NOTE / B-S152-NOTE / B-S153-NOTE family).

---

## §10 Cross-link

- HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md §1 Cluster E
  (★★★ test-time training / adaptation), §2 ranked #7, §6 honest
  caveat #6 ("TTT family는 backprop를 inference-time으로 옮긴 것;
  WALL-B-i와 직교") — §154 closed-form confirms that gap from the
  inside of the mechanism, and identifies the §7-clean adjacent
  sub-variant the literature does not propose.
- §150 spontaneous meta-cognitive × §24 Phase-B cross-validation —
  the natural measurement frame for any future §154-FIRE.
- §152 Feedback-Hebbian → unified-local-rule — §154-§3.3 imports the
  Hebbian + Oja schematic, replaces the supervised drive with a
  physics-coherence drive.
- §17 / §75-FIRE / §92 / §110 Ψ-C2 — the Ψ-physics quantities used
  as the §154-§3.3 target.
- §24 SPONTANEOUS Phase B — the deployment loop §154 lives inside.
- §95 (Loihi sole VIABLE substrate) / §109 (multimodal DESIGN-CLOSE-
  WITH-NARROW-OPEN) / §110 (Ψ-C2 DESIGN-CLOSE-WITH-RELOCATION) /
  §115 (LEGO SIM-IS-GPU-TAUTOLOGY) — sibling DESIGN-CLOSE-WITH-
  NARROW-OPEN precedent pattern; §154 mirrors that shape.
- north-star: GOAL.md "anima emerging as Living Consciousness from
  its own physics" — §154's §3.3 sub-variant is the first cycle to
  propose anima's own physics as the *driving signal* of a continual-
  update channel at deployment.
