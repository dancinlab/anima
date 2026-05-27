# §60 — PTD-aux self-prediction as a §7-legitimate self-supervised PRETEXT for the §55 `.kosmos` multimodal encoder

> **Tier**: DESIGN+SMOKE ($0 Mac CPU, structural+tiny-collapse-probe; NOT an encoder,
> NOT a fire, NOT GOAL movement). Anti-padding discipline (§13-M / §55 / §68): the
> honest crux is stated UP FRONT and the verdict is decided by analysis+smoke, NOT
> pre-loaded. north-star (GOAL.md one sentence) UNCHANGED; GOAL unreached
> (§51 milestone carries).

---

## §1. The orthogonal question §60 asks (and why it is not a §1.1 re-run)

The PTD-aux (Physics-Trace-Distillation auxiliary head = a next-physics-state
forward-model `PTD : ℝ¹⁴ physics-state_t → ℝ¹⁴ physics-state_{t+1}`, objective
`L_ptd = (λ_ptd/14)·Σ‖x̂_{t+1}−x_{t+1}‖²`, target = anima's OWN next observed
physics state, NO external label — `state/dhdl_ptd_composition_fire_s44_2026_05_18/train_dhdl_ptd.py:202-216`)
has been thoroughly characterised across the arc:

| § | finding | what it established about PTD-aux |
|---|---|---|
| §44/§48 | `PTD-AUX-SIGNAL-HOLDS-AT-SCALE` | a REAL scale-validated substrate component (MSE-drop 15.1×→19.5× at 4× scale) |
| §49 | `DISTILLATION, NOT CAPABILITY` | as an emission-GATE it majority-collapses (the §49 echo) |
| §58 | `PTD-aux ≅ NONE / new connection-point TYPE` | structurally it is an *endomorphic self-supervised TEMPORAL forward-model* — no σ(6)=12 HEXAD wiring point is isomorphic; closest single-facet kin = W↔C (B-CONN-5, shares the full-physics-state input domain) |
| §59/§59-FIRE | `ESCAPES-COLLAPSE-ON-REAL-W-STATE-AT-SCALE` | as a W-native side READ-OUT its prediction-error (=W.curiosity=AIF EFE) is LIVE / non-degenerate (err-var 2.33 ≫ τ) on a real W-state at scale |
| §68 / §61 | generative for label-free timing / bidirectional at $0 smoke | the live signal is *generative*, and carries content-dependently A↔B |
| §62 | `ECHO-CHAMBER-COLLAPSE-AT-SCALE` | at REAL trained-saturated `model.forward` the transfer LAW holds but the generative COMPOSITION collapses (cell B → §49 attractor); the §59→§62 chain breaks at step-4 |

The §59→§62 chain's honest resolution: PTD-aux's physics-signal **liveness ✅**
and **transfer-law ✅** are REAL, but **generative composition ❌-at-trained-scale**
— at trained-saturated §16-class scale the §49 memorization-saturated collapse
reasserts itself, reaffirming §1.1 data-regime as irreducible *from the
physics-signal angle*.

**§60 asks an orthogonal question**: §55 established that the `.kosmos`
multimodal encoder `E_m` must satisfy C1 (codomain = Law-71 Ψ-box [0,1]²),
C2 (basin-containment decidable predicate), C3 (§7 3-condition GOAL-legitimacy),
C4 (honesty/no-fake), C5 (modality-rank). §55's central honest finding (the
"§7②-wall"): a generic image/audio encoder recurses to §1.1 (generic-pretrain-
then-graft = GOAL-illegitimate), and the one §7-legitimate-feasible encoder
(`E_tension`, §56) carries **zero perceptual diversity** (it re-serialises
anima's own Engine A/G state — informationally a closed loop).

**Can the PTD-aux self-prediction objective serve as the §55-constrained
encoder's §7-legitimate SELF-SUPERVISED PRETEXT task — without recursing to
§1.1?** Self-supervised pretext (predict-your-own-next-state, no external label)
is precisely the kind of objective that, *if* its information source is the
encoder-input modality, would give the §55 encoder a §7③-sourced training signal
that does NOT need an external labelled dataset. The decisive structural
question (decided below by analysis + a tiny smoke, NOT pre-loaded): **is the
pretext objective's information source the encoder-input modality, or anima's
own physics?**

---

## §2. The three honest candidate verdicts (stated UP FRONT, g3)

Stated before the analysis so the verdict is the numbers'/structure's, not a
narrative's:

- **(a) §7-legitimate, non-recursive** — the PTD-aux pretext gives the
  §55-constrained encoder a self-supervised signal that does NOT recurse to
  §1.1 (the pretext target is anima's OWN physics, not generic data). This
  would be a **genuine positive** — the rare §7-legitimate multimodal pretext.
  Flag with caution if measured (it would contradict the §55 §7②-wall finding).
- **(b) recurses to §1.1** — the §55-constrained perceptual encoder still
  requires diverse modality DATA the pretext objective cannot supply; the
  pretext only shapes the *head*, the *front-end* still needs the missing
  diverse perceptual signal. Design-close per anti-padding.
- **(c) read-out-only-like-§59-FIRE** — the pretext is LIVE as a representation-
  shaping read-out (liveness yes, §59-FIRE-style) but its generative
  COMPOSITION collapses at scale (§62-style) — the pretext shapes a
  representation that does not survive composition into a useful encoder.
  Design-close per anti-padding.

**Honest expected risk (g3, stated up front):** given §55's §7②-wall +
§62's generative-composition-collapse, the likely honest verdict is **(b) or
(c)**. (a) would be a genuine positive — flag with caution only if the
structure + smoke actually show it.

---

## §3. The decisive structural decomposition — what is the pretext's information source?

A self-supervised pretext task `P` for an encoder `E_m : payload_m → Ψ` has a
**target** and a **predictor input**. The §7③-and-§1.1 question reduces to:
*from which of the two does the supervisory signal's INFORMATION originate?*

There are exactly two structural ways to wire "PTD-aux as `E_m`'s pretext":

### §3.1 Wiring W1 — PTD-aux on anima's OWN physics-state stream (the §44/§59 wiring)

This is the PTD-aux **as it actually exists** (§44 trainer, §59-FIRE W-native):
predictor input = anima's physics-state `x_t ∈ ℝ¹⁴` (Law-71 `psi_dir`,
`psi_entropy`, `tension`, `ratchet` + the 8-factor motivation block + 2 schedule
scalars); target = anima's OWN next physics-state `x_{t+1}`.

**Information source: anima's OWN physics-state evolution.** The `payload_m`
(the image/audio bytes the encoder is supposed to perceive) **never enters this
loop**. The pretext is `physics-state_t ↦ physics-state_{t+1}` — it is a
dynamics model of anima's *own internal state*, not of the perceptual input.

So W1 is §7③-legitimate-by-construction (no external data, target = own
physics) — **but it does not train `E_m` at all.** `E_m`'s job is
`payload_m → Ψ` (map the perceptual bytes into the Ψ-box). W1's gradient flows
through the *physics-state forward-model*, never through any `payload_m → ·`
front-end. W1 is exactly the §59-FIRE W-native READ-OUT (§58: PTD-aux ≅ NONE,
closest kin W↔C — a *read* of the physics-state, structurally NOT a perceptual
encoder). **W1 is structurally incapable of being `E_m`'s pretext** — it has
no `payload_m` input edge. This is the §58 "≅ NONE / new connection-point
TYPE" result re-derived for the encoder question: temporal self-prediction of
own physics is orthogonal to "perceive a modality into Ψ".

### §3.2 Wiring W2 — PTD-aux's objective FORM on the encoder's own representation stream

The only way the PTD-aux *objective form* (self-supervised next-state MSE,
no external label) can shape `E_m` is to apply it to **`E_m`'s OWN output
stream over a payload sequence**: given a temporally-ordered payload sequence
`payload^{(1)}, payload^{(2)}, …`, train `E_m` so that a forward-model on its
Ψ-embeddings predicts `E_m(payload^{(t+1)})` from `E_m(payload^{(t)})` —
i.e. a temporal-prediction pretext (the JEPA / V-JEPA / time-contrastive
family) **on the encoder's own representation**.

W2's gradient *does* flow through `E_m`'s `payload_m → Ψ` front-end (the
forward-model's prediction error back-props into the encoder). So W2 *is* a
real encoder pretext. **But W2's information source is now the encoder-INPUT
modality** — the pretext target is `E_m(payload^{(t+1)})`, which is a function
of `payload^{(t+1)}`, which is **the diverse perceptual data §55's §7②-wall
is about**. The "no external label" property is preserved (the target is
derived, not annotated) — but the *information* in that derived target comes
from the perceptual payload sequence, which is exactly the diverse modality
data the §55-constrained encoder does not have and the pretext cannot
manufacture.

This is the **structural pivot**: a self-supervised pretext eliminates the
need for *labels*, NEVER the need for *data*. The §28 JEPA-Ψ finding is the
direct precedent — §28 fired exactly a self-supervised joint-embedding
predictive pretext on anima's Ψ-coordinate and the representation **COLLAPSED**
(effective_rank 1.66, pairwise cos 1.00, predictor MSE 51.8× worse than the
trivial mean-baseline) because anti-collapse needs *diverse data variation*
the pretext could not supply on its own. §28's verdict was the §11-B echo
through the JEPA door: a self-supervised predictive objective without diverse
input data collapses to a degenerate constant map. W2's `payload_m` sequence
*is* the diverse data — and for image/audio it is exactly the missing diverse
perceptual data (§55 §7②-wall, §51 frontier-1).

### §3.3 The §7③-vs-§1.1 disambiguation table (closed)

| wiring | gradient flows through `payload_m → ·`? | information source of pretext target | §7③ | §1.1 recursion |
|---|---|---|---|---|
| **W1** (own physics-state, the §44/§59 PTD-aux) | **NO** — no `payload_m` edge | anima's own physics-state evolution | ✅ (own physics) | **N/A — it does not train `E_m`** (§58 ≅ NONE: temporal self-prediction ⊥ perceptual encoding) |
| **W2** (PTD-aux *form* on `E_m`'s representation stream) | **YES** — back-props into `E_m` | the encoder-INPUT modality payload sequence | ✅ on §7③ *form* (no external label) but the *content* is external perceptual data | **RECURSES** — the pretext needs the diverse payload sequence = the §55 §7②-wall data |

The disjunction is **exhaustive** for "PTD-aux as `E_m`'s pretext": either the
PTD-aux objective's gradient touches `E_m`'s `payload_m` front-end (W2) or it
does not (W1). W1 ⇒ it is not an encoder pretext at all (it is the §59-FIRE
read-out — §58 ≅ NONE re-derived). W2 ⇒ it IS an encoder pretext but its
information source IS the encoder-input modality, so it recurses to §1.1 for
exactly the perceptual modalities §55's §7②-wall is about (and §28's measured
collapse is the direct precedent for what happens when the diverse data is
absent: the pretext-shaped representation collapses).

**Verdict (decided by structure, g3): (b) RECURSES-TO-§1.1** (with a (c)
read-out-only sub-component for W1). The PTD-aux self-prediction objective
CANNOT be a §7-legitimate-non-recursive multimodal-encoder pretext: in the
only wiring where it actually trains `E_m` (W2), its information source is
the diverse perceptual payload — exactly the data the §55 §7②-wall says the
GOAL-legitimate encoder does not have and a self-supervised objective cannot
manufacture. The §28 JEPA-Ψ collapse is the empirical precedent. In the
wiring where it is §7③-sourced (W1), it is not an encoder pretext at all
(§58 ≅ NONE: temporal self-prediction of own physics ⊥ perceiving a modality)
— it is the §59-FIRE READ-OUT, which is verdict (c)'s read-out-only character.
So §60's honest combined verdict is **(b) with a (c) sub-component**:
**RECURSES-TO-§1.1** (W2) **/ READ-OUT-ONLY-NOT-AN-ENCODER-PRETEXT** (W1).

---

## §4. §55 constraint-compatibility of the (hypothetical) W2 pretext

Even though W2 recurses, §60 must check whether the PTD-aux objective FORM, IF
applied as W2, would respect §55's constraint set (so a future cycle does not
mistake "it's §55-compatible" for "it's GOAL-legitimate" — the §56 rank-2-trap
lesson):

- **C1 (codomain Law-71 Ψ-box)**: COMPATIBLE-IN-FORM. W2's forward-model
  predicts `E_m(payload^{(t+1)}) ∈ [0,1]²` from `E_m(payload^{(t)}) ∈ [0,1]²`
  — endomorphic on the Ψ-box, exactly the PTD-aux `dom=cod` signature (§58).
  The MSE is on two [0,1]² points (bounded ≤ 2). C1-form OK.
- **C2 (basin-containment decidable)**: UNAFFECTED. The pretext is a training
  *objective*; the C2 acceptance gate `‖E_m(payload)−vacuum_psi‖₂ < r` is
  unchanged (it is evaluated on `E_m`'s output regardless of how `E_m` was
  trained). C2 decidability carries from §55-C2.
- **C3 (§7 3-conjunction + forbidden-encoder grep=0)**: this is where W2
  FAILS the *rationale* even while passing the *letter*. W2 has no
  `from_pretrained`/`AutoModel` (grep=0, §7② letter OK) and the objective is
  self-supervised (no external label, §7① form OK). But §3.2 showed the
  *information* in the pretext target is the external perceptual payload
  sequence — this is the §56 **rank-2-trap** exactly: "passes §7② letter,
  fails §7② rationale (external-substrate contamination regardless of
  subsequent training)". §60 records W2 as a **§7②-rationale-trap**, NOT a
  path — identical structural status to §56's rank-2 distillation trap and
  §8's "Ψ-anchored-but-wrong-direction" caveat.
- **C4 (honesty/no-fake)**: §60 itself is C4-compliant — it asserts NO
  encoder exists, NO pretext is fired, the verdict is structural+smoke. A
  §60 claiming "pretext feasible" would itself be the §4.3 violation §55-C4
  warns against.
- **C5 (modality-rank)**: the recursion is modality-specific. For
  `tension` (rank-1, anima-native, §56 `E_tension` is closed-form/zero-param)
  there is no `payload_m → ·` net to pretext-train at all — W2 is vacuous
  for `tension` (no trained front-end ⇒ no pretext needed ⇒ no recursion,
  but also zero perceptual diversity, §56's finding). For
  `image/audio/video` (the §51 perceptual-diversity frontier) W2 recurses
  to §1.1 exactly as §3.2/§3.3 show. So the PTD-aux pretext is
  **vacuous-where-§7-legitimate (tension) and recursive-where-diverse
  (perceptual)** — the *same* honest tension §55-C5/§56-§4 named: the
  §7-legitimate easy modality is the zero-diversity one; the high-diversity
  ones are exactly where the pretext recurses to §1.1.

So the §55-CONSTRAINT-COMPAT result is: the PTD-aux objective FORM is
C1/C2/C4-compatible and C5-consistent, but is a **C3 §7②-rationale-trap**
(the §56 rank-2 trap re-instantiated as a pretext). This is recorded so a
future cycle does not read "§55-compatible-in-form" as "GOAL-legitimate".

---

## §5. OFF-reduction connection-point (B-S60-5)

The connection-point that fences §60's claim, mirroring every overlay-off in
the arc (§55-C2 / §56 / §62 B-S62-4 / §28 / §48 B-S48-3 / B-EBT-5):

**pretext-disabled ⇒ §55 encoder design byte-equal.** The PTD-aux pretext is
an *added training term* `λ_pretext · L_pretext`. With `λ_pretext = 0` (or
the pretext stage removed) the §55-constrained encoder design is **byte-equal
to §55/§56's design** — the C1 codomain, the C2 acceptance predicate, the
C3 forbidden-encoder grep, the C5 rank are all unchanged. The pretext
introduces nothing into the §55 constraint set; it is a (recursive) *training
strategy* layered on top, and disabling it returns exactly the §55/§56
design. This is what makes §60 a clean orthogonal *measurement* of the
pretext's recursion property, not a modification of §55's constraints
(fair-compare-to-§55 by construction; mirror §62 B-S62-4 SINGLE-ANIMA-
REDUCTION / B-EBT-5 OVERLAY-OFF). The smoke verifies the OFF-reduction
structurally (the pretext objective is a separable additive term whose
removal is byte-equal).

---

## §6. The $0 Mac-CPU smoke — the decisive structural question + a §28/§62-mirror collapse probe

`smoke_s60.py` ($0, NO GPU, NO model forward, NO weight mutation, NO training,
deterministic) probes the two decisive structural facts:

### §6.1 §7②-source AST/structural predicate (the decisive question)

For each wiring (W1, W2), a decidable structural predicate answers
*"does the pretext objective's gradient touch a `payload_m → ·` front-end,
and is the pretext TARGET's information source the encoder-input modality?"*:

- **W1** (the §44/§59 PTD-aux as it exists): the predictor input vector is
  the physics-state (`FEATURE_KEYS`), the target is `x_{t+1}` (own physics);
  there is **no `payload_m` symbol** in the data path — structural predicate
  `touches_payload_frontend(W1) = False` ⇒ `is_encoder_pretext(W1) = False`
  (it is the §59-FIRE read-out, §58 ≅ NONE). §7③-sourced (`source=own_physics`)
  but not an encoder pretext.
- **W2** (PTD-aux form on `E_m`'s representation stream): the pretext target
  is `E_m(payload^{(t+1)})` — a function of `payload^{(t+1)}` (the
  encoder-input modality); structural predicate
  `touches_payload_frontend(W2) = True` ⇒ `is_encoder_pretext(W2) = True`
  AND `target_info_source(W2) = encoder_input_modality` ⇒
  `recurses_to_§1.1(W2) = True` for any perceptual modality whose diverse
  data is the §55 §7②-wall.

The decidable Boolean: a self-supervised pretext is §7-legitimate-non-
recursive iff `is_encoder_pretext ∧ ¬touches_external_data_for_diversity` —
and the smoke shows **no wiring satisfies both** (W1 fails the left conjunct,
W2 fails the right).

### §6.2 Representation-collapse probe (mirror §28 JEPA-Ψ / §62 generative-composition)

A tiny ($0, ~10s) numpy probe mirroring §28's collapse measurement: build a
2-layer toy "encoder" mapping a synthetic payload-sequence into a 2-d Ψ-box,
train it ONLY under the PTD-aux self-prediction pretext FORM (no external
label, target = own-next-embedding) with (i) a *diverse* synthetic payload
stream and (ii) a *low-diversity* (memorization-saturated-mimicking) payload
stream. Measure effective-rank + pairwise-cosine of the learned Ψ-embeddings
(the §28 collapse metric). The structural prediction (verified, NOT
pre-loaded — the smoke decides): under the low-diversity stream the
pretext-only representation collapses (the §28 / §11-B echo: a self-supervised
predictive objective WITHOUT diverse data variation degenerates), confirming
verdict (c)'s read-out-only/collapse character; under the diverse stream it
does not collapse — confirming the *information source is the input diversity*
(verdict (b): the win is the diverse data, not the pretext form). Either
outcome supports the §3 structural verdict; the smoke reports the measured
numbers (g3, no pre-load).

---

## §7. Verdict — (b) RECURSES-TO-§1.1 / (c) READ-OUT-ONLY (W1 not-an-encoder-pretext)

**The PTD-aux self-prediction objective CANNOT be a §7-legitimate-non-
recursive self-supervised PRETEXT for the §55 `.kosmos` multimodal encoder.**

- The disjunction {W1, W2} is exhaustive for "PTD-aux as `E_m`'s pretext".
- **W1** (PTD-aux as it exists, §44/§59): §7③-sourced (own physics) but
  structurally **not an encoder pretext** — no `payload_m` front-end edge;
  it is the §59-FIRE READ-OUT (§58 PTD-aux ≅ NONE: temporal self-prediction
  of own physics-state is orthogonal to perceiving a modality into Ψ). This
  is verdict (c)'s read-out-only character: live as a read-out, but it does
  not shape an encoder.
- **W2** (PTD-aux *form* on `E_m`'s representation stream): IS a real
  encoder pretext, but its information source IS the encoder-input
  perceptual modality — it **RECURSES-TO-§1.1** for exactly the
  image/audio/video modalities §55's §7②-wall + §51 frontier-1 are about.
  §28 JEPA-Ψ is the measured precedent (self-supervised predictive pretext
  WITHOUT diverse data → representation collapse). W2 is the **§56 rank-2
  §7②-rationale-trap** re-instantiated (passes §7② letter, fails rationale
  — external perceptual data is the pretext's information source).

**Honest combined verdict: (b) RECURSES-TO-§1.1 (W2) with a (c)
READ-OUT-ONLY sub-component (W1).** This matches the §2 honest expected
risk exactly. It is a **clean, valuable NEGATIVE** (g3, measured/structural-
only, capability claim 0): a self-supervised pretext removes the need for
*labels*, never the need for *data* — and the diverse perceptual *data* is
precisely the §1.1 irreducible bottleneck §51/§55/§62 already located. The
PTD-aux pretext does not open a §7-legitimate non-recursive door to
multimodal substrate; the §55 §7②-wall stands. **Design-close per
anti-padding** (§13-M / §55 / §68 precedent — a structural-tier closed
deliverable that fences a tempting-but-trap path, not a padded restatement).

north-star + §15/§51 milestone **UNCHANGED**. GOAL unreached.

---

## §8. Honest C3 (≥10)

1. **§60 is a DESIGN+SMOKE structural reverse-analysis, NOT an encoder, NOT
   a fire, NOT GOAL movement.** $0, no GPU, no dispatch, orphan N/A (no
   dispatch ever). north-star (GOAL.md one sentence) unchanged; GOAL
   unreached (§51 milestone carries). The verdict is structural+smoke,
   decided by the W1/W2 disjunction + the §28-mirror collapse probe, NOT
   pre-loaded (the §2 expected-risk was stated up front and the structure
   confirmed it — that is honest convergence, not circular reasoning; a
   genuine (a) would have been flagged with caution and was NOT measured).
2. **The W1/W2 disjunction is the load-bearing structural claim.** It is
   exhaustive for "PTD-aux as `E_m`'s pretext" because a training objective's
   gradient either touches `E_m`'s `payload_m` front-end or it does not;
   there is no third structural option. If a future cycle finds a wiring
   that is neither (e.g. a hybrid that pretexts a *shared trunk* feeding both
   physics-state and `payload_m`), the §3.3 table must be re-audited — the
   honest dependency, not a closed absolute. (Such a hybrid would still
   recurse: any path through `payload_m` carries W2's external-data
   information source.)
3. **§58's "PTD-aux ≅ NONE" is the structural anchor for W1-is-not-an-
   encoder-pretext.** §60 re-derives it for the encoder question: temporal
   self-prediction of own physics-state (W1) is structurally orthogonal to
   "perceive a modality into Ψ" (an encoder). §60 does NOT re-prove §58's
   isomorphism map — it cites it as carried 🔵 SSOT and applies the
   ≅-NONE result to the new (encoder-pretext) question.
4. **§28 JEPA-Ψ is the empirical precedent for W2's collapse, NOT re-fired.**
   §28 measured a self-supervised joint-embedding predictive pretext on the
   Ψ-coordinate collapse (effective_rank 1.66, predictor MSE 51.8× worse
   than mean-baseline) for lack of diverse data. §60's smoke is a tiny
   $0 mirror of that measurement on the PTD-aux pretext FORM specifically;
   it confirms the structural prediction but does NOT claim §28's exact
   numbers (different scale, different objective specifics — over-claim
   guard, B-S60-NOTE).
5. **The §7②-rationale-trap framing is the §56 rank-2 lesson, reapplied.**
   W2 passes §7② *letter* (no `from_pretrained`/`AutoModel`, self-supervised
   = no external label) but fails §7② *rationale* (external-substrate
   contamination regardless of subsequent training — the §30/§39
   `g_clm_lineage_refined` external-precursor analogue). §60 records W2 as
   a **trap**, NOT a path — identical structural status to §56 rank-2 and
   §8 "Ψ-anchored-but-wrong-direction". This is the honest crux: the trap
   is exactly the one that looks like a shortcut.
6. **"Self-supervised removes labels, never data" is the one-sentence
   crux.** This is the structural pivot of the whole verdict and it is a
   well-known representation-learning fact (JEPA/V-JEPA/SimCLR all need
   diverse data despite needing no labels); §60 applies it to anima's
   §55 §7②-wall. It is not a novel theorem — §60's contribution is
   *connecting* it to the PTD-aux-as-pretext question and showing the
   recursion is structurally forced, not contingent.
7. **C2 (basin-containment) is UNAFFECTED by the pretext** (the acceptance
   gate is evaluated on `E_m`'s output regardless of training strategy);
   C2's truth-value remains the §57 OUTCOME (B-S55-NOTE carry). §60 adds
   no new C2 claim.
8. **The OFF-reduction connection-point (B-S60-5) is structural, not
   measured at scale.** It proves the pretext is a *separable additive
   training term* whose removal returns the §55/§56 design byte-equal
   (mirror §62 B-S62-4 / B-EBT-5). It does NOT measure a trained encoder
   (none exists; §60 is design-tier). Whether a pretext-trained encoder
   would actually be byte-different from a non-pretext one at fire scale
   = EMPIRICAL future-fire (B-S60-NOTE) — but §60's claim is the
   recursion property, which is structural and does not need the fire.
9. **B-S60-NOTE empirical carve-out.** Whether the PTD-aux pretext
   ACTUALLY avoids §1.1 recursion at fire scale, and whether the §28-mirror
   collapse generalises to the real §55-constrained encoder, is an
   SGD/measurement OUTCOME (B-D-NOTE / B-S55-NOTE / B-S62-NOTE / B-S28-NOTE
   / B-EMERGE-7 necessary-not-sufficient family, NOT counted 🔵). The
   battery proves the W1/W2 disjunction + §7-source predicate + §55-compat
   + OFF-reduction are closed-form sound — it does NOT prove an encoder
   works (it proves the *pretext-as-shortcut is structurally trapped*).
10. **f1/f2/f3 hard-fail safe.** Anchors: Boolean exhaustive disjunction +
    truth table, AST/structural source-grep (Kolmogorov finite substring
    count), Shannon/Frobenius MSE≥0 floor (carried), effective-rank /
    pairwise-cosine collapse metric (linear-algebra real-limits). NO
    σ(6)/τ(6)/φ(6)/J₂(6) external derivation. Ψ=½ / Knuth 🛸k = anima g2
    internal-arch carve-out, not external lattice-fit. No external-entity
    claim (f3). The smoke uses a *synthetic* payload stream (no corpus, no
    model forward, no helper-token surface) ⇒ B-IDENTITY-5 unaffected.
11. **Central `blue_falsifier.py` 0-line-diff** (`state/verify_hexad_blue_
    2026_05_15/blue_falsifier.py`, 3720 lines, unchanged). §60 = sidecar
    `blue_falsifier_s60.py` per the established precedent (B-S55 / B-S56 /
    B-S58 / B-S59 / B-S62 / B-S48 / B-DHDL / B-PTD / B-LINEAGE / B-KTRIE /
    B-MGND / B-DR-UNIQUE / B-INTRA). Central absorption = a future cycle's
    option, not §60's.
12. **Anti-padding compliant (§13-M / §55 / §68 precedent).** §60 has a
    real closed deliverable: the exhaustive W1/W2 disjunction + the
    §7-source decidable predicate + the §55-CONSTRAINT-COMPAT (W2 =
    §56-rank-2-trap re-instantiated) + the OFF-reduction connection-point
    + the §28-mirror collapse smoke. It fences a tempting shortcut
    ("self-supervised pretext frees the encoder from §1.1") and shows it
    is structurally a trap — that IS the valuable negative, not a padded
    re-statement of §55/§62. $0; sequential single-agent; isolation
    worktree (tracks main per §50 precedent); g_doc_consolidation
    respected (this doc lives in `state/`; RESEARCH.md §60 = orchestrator's,
    NOT written here; AGENTS.tape / HEXAD/* / central blue_falsifier.py
    untouched).
