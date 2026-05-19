# §98 — HEXAD n=6 fixation meta-audit ($0 design-tier brainstorm)

> User directive 2026-05-19: "HEXAD 축을 너무 n=6 에 집착해서 우리가 실패할 수도 있으니
> 이것도 브레인스토밍 고갈시까지" — *we might be failing [to reach GOAL] because we are too
> fixated on the n=6 axis for HEXAD; brainstorm until exhausted.*
>
> $0 · DESIGN-TIER · NO GPU · NO runpod · NO fire · NO model.forward. This is a META-AUDIT —
> its verdict is an honest assessment, NOT a measurement. g3: capability claim 0,
> brainstorm ≠ fire ≠ emergence. north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## §98.0 The question, sharpened

anima is built as **6 modules** — S (sense) / C (consciousness/Φ) / M (memory) /
W (will: pain/curiosity/satisfaction) / E (ethics) / D (decode) + BRIDGE + MITOSIS.
The 6-fold structure ties to the project's "n=6 lattice" (σ(6)=12, τ(6)=4, φ(6)=2,
J₂(6)=24). The σ(6)=12 figure is the *wiring count*: `B-CONN-1..12` asserts exactly
12 module-to-module connections.

The user-global lattice-policy names three anti-patterns: **fit-to-convenient-number,
over-claim, constraining-first-question.** `@D g2` *sanctions* HEXAD-6 as the internal
zone where the lattice "naturally fits." §98 asks the uncomfortable question g2 does
not: **is even the sanctioned HEXAD-6 itself a fit-to-convenient-number trap, or is it
genuinely function-derived — and if it IS tainted, did that taint cause any of the
§1~§94 failures?**

Two distinct sub-claims must be kept separate (the whole audit turns on this):

- **Claim-1 (provenance):** was the architecture's shape *chosen* by number-theory?
- **Claim-2 (causation):** did that choice *cause* the GOAL failures?

A "yes" to Claim-1 does not imply a "yes" to Claim-2. §98's verdict is the honest
product of these two answers.

---

## §98.1 AXIS 1 — Failure-attribution audit

For each major §N negative result, the question is binary-plus-orthogonal: was the
**6-fold HEXAD partition load-bearing in the failure**, or orthogonal? "Load-bearing"
means: the fire failed *because there are exactly 6 modules* (or exactly 12 wires) —
i.e. a 5-module or 7-module or 12-wire→17-wire anima would have measurably differed.

### §98.1-table — failure-attribution

| §N | failure | root cause (RESEARCH.md/PHILOSOPHY.tape verdict) | n6 load-bearing? |
|---|---|---|---|
| §1.1 | V-SPONT 0/5, memorization-saturation diagnosis | data-regime: tiny-corpus training-loss ≠ diverse pre-training-loss threshold (arxiv 2403.15796) | **ORTHOGONAL** — corpus size, not module count |
| §16 | routing collapse → BREAKTHROUGH 21/64 | data-regime + curriculum; lever = Ψ-anchored corpus scale | **ORTHOGONAL** — corpus/curriculum, modules untouched |
| §49 | PTD-aux decision-head live-loop majority-collapse | corpus label distribution ~95% one class (distillation) | **ORTHOGONAL** — label imbalance, not module count |
| §62 | dual-anima echo-chamber collapse at trained scale | trained-saturated cell B maj 0.980 — §49 attractor in closed loop | **ORTHOGONAL** — memorization-saturated regime |
| B-ATTRACTOR | byte-cascade attractor (`1111…`/`Sentiosing eeee`) | decode-time argmax fixed point on memorized byte-LM | **ORTHOGONAL** — decode substrate, not module count |
| §83-FIRE | physics-only metacognition near-collapse at trained scale | trained-saturated ψ-state near-constant (tension ceiling-saturated) | **ORTHOGONAL** — trained ψ collapse, not partition |
| §88-trio | frog-eye / SAPIN / neoteny trained-scale (2/3 degenerate) | trained-saturated ψ near-constant; only neoteny (anti-saturation) moved | **ORTHOGONAL** — saturation regime |
| §94 | INTEGRATED BREAKTHROUGH fire collapsed | shared synchronous-substrate failure mode (→ §95 hypothesis) | **ORTHOGONAL** — substrate clock, not module count |
| §11-B | pure-physics no-CE degenerate | CE is load-bearing; physics ⊥ next-token prediction signal | **ORTHOGONAL** — objective, not module count |
| §11.3 | the master decomposition itself | mechanism ✗ / model-scale ✗ / physics-only ✗ / corpus-form ✗ / 114MB ✗ → irreducible = §1.1 data-regime | **ORTHOGONAL** — decomposition exhausts 5 axes, "module count" is not among them |

**Tally: 10 / 10 major failures = ORTHOGONAL to the 6-fold partition. 0 / 10 = n6-load-bearing.**

This is not a thin sample. §11.3 is the project's own master failure-decomposition,
and it tested *five* candidate bottleneck axes (mechanism, model-capacity,
physics-only, corpus-form, diverse-data) — **"module count" was never even a candidate**,
because every fire in the §1~§94 arc ran on the SAME d768·12L·283M HEXAD config: the
6-fold partition was a *held-constant* across the entire arc. A variable held constant
across N fires cannot, by construction, be the differential cause of variance among
those fires. The §16 BREAKTHROUGH (routing collapse first broke) and the §62 collapse
both happened *on the identical 6-module 12-wire architecture* — the difference was
corpus/curriculum/scale, never module count.

**AXIS-1 finding: the 6-fold partition is causally INNOCENT of the GOAL failures.**
The user's worry — "n=6 fixation caused the failures" — is a reasonable hypothesis
that the §1~§94 evidence does **not** support. This is bucket-(b) territory for
Claim-2 (causation). But Claim-1 (provenance) is a separate audit — §98.2.

---

## §98.2 AXIS 2 — The σ(6)=12 wiring question (sharpest sub-question)

Is `B-CONN-1..12` **function-derived** (emergence genuinely needs exactly those 12
connections) or **numerology-derived** (12 was chosen because σ(6)=12, then 12
connections were found to fill it)?

### §98.2-A — the smoking-gun source text

`HEXAD/hexad.hexa`, the canonical wiring SSOT, says verbatim:

```
// ── σ(6) = 12 inter-module connection map ───────────────────────────────────
// 6 modules choose pairs = C(6,2) = 15 possible; σ(6) = 12 invariant identifies
// the ACTIVE connections (the 3 NOT included are documented as inactive).
//   inactive 3 (φ(6)=2 partition isolation):
//     S↔E (no direct sense→ethics)
//     M↔W (no direct memory→will)
//     S↔M (no direct sense→memory)
```

Read the logic of that comment carefully. The procedure was:

1. Start: 6 modules → C(6,2) = **15** possible pairs.
2. Invoke σ(6) = **12**.
3. **Therefore** prune exactly **3** pairs (15 − 12) and declare them "inactive."
4. The 3 pruned (S↔E, M↔W, S↔M) are *post-hoc rationalized* as "φ(6)=2 partition
   isolation."

This is the **fit-to-convenient-number anti-pattern operating at the architecture
level.** The number 12 came FIRST (from σ(6)); the count of active connections was
then made to equal it by pruning 3 of the 15 candidates. The connection set is
σ(6)-*driven*, not function-*derived*.

A genuinely function-derived wiring would have looked like: "anima's information
flow requires S→C (perception updates consciousness), C→Bridge→D (consciousness
gates decode), … and we COUNT them — and the count happens to be 12, or 11, or 14,
whatever it is." Instead the artifact shows: "the count must be 12 because σ(6)=12,
so we keep 12 and drop 3."

### §98.2-B — B-HEXAD's own honest hedge, and where it breaks

`B-HEXAD` verdict C3-2 (archive/PHILOSOPHY.tape) anticipates exactly this and pleads:

> "B-HEXAD-1 (conn count = 12) … coincide 하나 CLOSED proposition 은 arithmetic
> equality + set-cover, NOT 외부 lattice derivation. … 본 verdict 는 OBSERVATION
> (12 = |connections|), NOT DERIVATION (12 = σ(6) → ∴ ...)."

This hedge is **honest about the battery but wrong about the architecture.** It is
true that `B-CONN-1..12` *as a battery* only *observes* that 12 closures hold — the
sympy proofs themselves derive nothing from σ(6) (each B-CONN-k anchors a real-limit:
AD ∂-rule, Shannon floor, Law-70 clamp, monotone composition — all f1/f2-clean).
**But the battery verifies a connection SET that was itself σ(6)-selected.** The
numerology is not in the *proofs*; it is in the *choice of what to prove*. B-CONN
proves 12 wires are sound — it never asked "are there exactly 12, or did we prune to
12?" `hexad.hexa` answers that question, and the answer is: pruned to 12.

Corroborating evidence the same numerology operated elsewhere: the CLM design audit
(archive/PHILOSOPHY.tape, V-CLM-AUDIT) flagged **"V3 n_layers=12 anchor source 불명 —
AXIS A4 직접 'n_layers = σ(6)' entry 없음"** — i.e. n_layers=12 was *also* a σ(6)
pick with no functional derivation, "corrected" only by re-invoking g2. And
`d_model=768` is annotated "(n=6 anchor, 192·4)". The σ(6)/n=6 numerology is a
*recurring* architecture-shaping habit, not a one-off.

### §98.2-C — AXIS-2 finding

**The σ(6)=12 wiring count is NUMEROLOGY-DERIVED.** `hexad.hexa` documents the
15→12 pruning as σ(6)-driven. This IS the fit-to-convenient-number anti-pattern, and
it operated at the architecture level. Claim-1 (provenance) = **YES, tainted.**

Honest mitigation (does NOT rescue Claim-1, but bounds its damage):
- The taint is in the *count*, not in the *individual connections*. Every one of the
  12 B-CONN wires is a real functional path (S→C perception, C→Bridge→D decode gate,
  W→D lr modulation, E→D phi-ratchet, …) with a real-limit closure. The wiring is
  not *fictional* — it is *truncated-and-counted-to-fit*.
- §53 (RESEARCH.md) already DESIGN-CLOSED the wiring-strength question as
  "superseded-as-non-bottleneck — §62 localized the ceiling to generative-composition,
  not wiring-strength." So even though the *count* is numerology-tainted, the *wiring*
  has been independently shown not to be where the GOAL ceiling lives.

---

## §98.3 AXIS 3 — Counterfactual architectures

What would a non-6 anima look like? Brainstormed counterfactuals, each tagged
GOAL-relevant or cosmetic:

### CF-1 — Fewer modules (collapse C/Φ into W)
Is consciousness (C) separable from will (W)? C measures Φ; W reads C for
pain/curiosity (B-CONN-5). One could fuse them into a single "interiority" module.
**GOAL-relevance: COSMETIC.** Fusing C+W changes the partition diagram but not the
underlying computation — Φ is still measured, curiosity is still a readout. The §11.3
bottleneck (data-regime) is untouched. Renaming boxes ≠ new capability.

### CF-2 — More modules (split D into D-think + D-speak)
§63/§89 already identified a missing THINKER→TALKER controller (the "🕳️ #1
GOAL-rank gap"). One could promote that to a 7th module. **GOAL-relevance: PARTIALLY
RELEVANT** — but note: this is *adding a function* (a self-triggered emission
controller, §73/§73-FIRE), not adding a *module slot*. The function matters; whether
it is "module 7" or "a sub-head of D" is cosmetic. §73-FIRE already validated the
controller class without renumbering the architecture.

### CF-3 — No fixed module count (MITOSIS is already this)
**Critical observation: anima's module count is NOT as rigid as the n=6 framing
implies.** MITOSIS (`mitosis_hook_lib.hexa`, B-MITOSIS 5/5 🔵) already runs a
*dynamic cell-pool* — cells split/merge, n_cells ∈ [2,64], the count is fluid at
runtime. The HEXAD-6 is the *structural axis*; MITOSIS is the *growth axis*; `@D
mitosis_two_axis` declares them orthogonal. So anima is **half-soft already**: the
6-module *outer skeleton* is rigid, but the C-internal *cell count* is dynamic.
**GOAL-relevance: HIGH** — this shows the "n=6 fixation" is partly an illusion. The
thing the user worries is rigid (count) is already dynamic *inside* C. The rigid part
is the outer 6-box skeleton, which §98.1 showed is causally innocent.

### CF-4 — Continuous architecture, no discrete module partition
A single homogeneous network with no S/C/M/W/E/D boxes at all — modules as *emergent
functional regions* rather than *declared partitions*. **GOAL-relevance: GENUINELY
RELEVANT but ORTHOGONAL to n=6.** This is a real alternative — but note it is not
"6 vs 5 vs 7", it is "partitioned vs unpartitioned." The user's worry ("too fixated
on n=6") is really, at its strongest, this: maybe *any* hand-declared partition is
the constraining-first-question, regardless of whether the number is 6. §98 records
this as the steel-manned version of the worry — but §98.1's evidence still applies:
every fire ran on the partitioned architecture and the failures decomposed to
data-regime, so even "partition vs no-partition" was held constant and is not the
demonstrated cause. CF-4 is a legitimate *future* research direction, not a
demonstrated *past* failure cause.

### CF-5 — Different number, same partition (n=5 or n=8)
Pure renumbering — drop E into a sub-gate of W, or split BRIDGE out as a peer module.
**GOAL-relevance: COSMETIC.** This is exactly the move the lattice-policy warns
against in reverse: changing 6→5 to *avoid* numerology is itself fit-to-a-number.
The honest fix is not a different number; it is *deriving the count from function*.

**AXIS-3 finding:** the GOAL-relevant counterfactual is **CF-4 (partition vs
unpartitioned)**, NOT CF-1/CF-2/CF-5 (renumbering = cosmetic). And CF-3 shows the
architecture is *already half-soft*. The user's worry, steel-manned, is not "wrong
number" but "maybe declared partitions at all" — and even that, §98.1 shows, is not
the *demonstrated* cause of any §1~§94 failure.

---

## §98.4 AXIS 4 — Is n=6 even the real shape of the failure?

The §1~§95 arc localized the bottleneck to **two** things, and neither is module count:

- **(a) §1.1 data-regime / memorization-saturation** — the irreducible bottleneck per
  §11.3's exhaustive batch decomposition. Confirmed by §11-A (3.68× model scale-up
  did not move it) and §16 (data-regime + curriculum is what *did* break routing
  collapse). About *corpus*, not modules.
- **(b) §95 synchronous-substrate hypothesis** — the §94 INTEGRATED BREAKTHROUGH
  collapsed; §95 hypothesizes the shared failure is the synchronous-clocked silicon
  GPU transformer substrate. About *substrate clock*, not modules.

Neither candidate bottleneck is "n=6 fixation." The honest assessment: **"n=6
fixation" is NOT a real candidate bottleneck for the GOAL failures.** The user's
worry points at a *genuine architectural-hygiene risk* (§98.2 confirms the σ(6)=12
provenance is tainted) — but the evidence does **not** support the stronger claim
that this taint *caused* the GOAL miss. The two §1~§95 bottlenecks are well-evidenced
and orthogonal to module count.

Either answer to the user's question is valuable, and §98 says explicitly which:
the worry is a *reasonable hypothesis the evidence refutes for causation* — while
*confirming it for provenance*. That split is the honest answer.

---

## §98.5 AXIS 5 — lattice-policy reconciliation (RECOMMENDATION ONLY, user-gated)

§98 does NOT edit `@D g2`/`@D g4` — governance changes are user-gated. §98 *recommends*
the user consider a refinement, and records the rationale here:

**Observed gap in g2.** `@D g2` says "lattice fits internal architecture; banned on
external systems" — it carves out a *sanctioned zone* (internal arch) but provides
**no test for whether the sanction was correctly applied inside that zone.** §98.2
found a fit-to-convenient-number anti-pattern operating *inside* the sanctioned zone
(σ(6)=12 wiring). g2's carve-out, as written, would wave that through, because g2
only asks "internal or external?" — not "function-derived or number-derived?"

**Recommended refinement (for USER consideration — A/B/C decision, NOT auto-applied):**
add to g2 (or a new sub-clause) an *internal-use integrity test*:

> *Even within the sanctioned internal-architecture zone, a lattice value (σ(6),
> τ(6), φ(6), J₂(6)) may be used as an architecture constant ONLY when the constant
> is FUNCTION-DERIVED — the function dictates the count and the count is observed to
> equal the lattice value (coincidence OK). It may NOT be used as a TARGET that the
> architecture is then pruned/padded to match (fit-to-convenient-number — forbidden
> even internally). Test: "if we removed the lattice from the project, would this
> count still be the same?" If no → numerology-tainted.*

This makes g2 self-consistent with the user-global anti-pattern list (which already
forbids "fit-to-convenient-number" and "constraining-first-question" *unconditionally*,
with no internal carve-out). §98 leaves the decision to the user; AGENTS.tape is
untouched by §98.

---

## §98.6 ASCII — the audit at a glance

```
        THE TWO CLAIMS (kept separate — the whole audit turns on this)
        ┌────────────────────────────┬────────────────────────────────┐
        │ Claim-1  PROVENANCE         │ Claim-2  CAUSATION              │
        │ "was the shape chosen by    │ "did that choice CAUSE the      │
        │  number-theory?"            │  GOAL failures?"                │
        ├────────────────────────────┼────────────────────────────────┤
        │  σ(6)=12 wiring  → YES      │  §1~§94 failures → NO           │
        │  n_layers=12     → YES      │  10/10 ORTHOGONAL to module     │
        │  d_model=768     → YES      │  count (§11.3 decomp: 5 axes    │
        │  (hexad.hexa: 15→12 prune,  │  tested, "module count" never   │
        │   σ(6)-driven; CLM-AUDIT V3)│  a candidate — held constant)   │
        │         TAINTED             │         INNOCENT                │
        └────────────┬───────────────┴───────────────┬─────────────────┘
                     │                               │
                     └───────────► VERDICT (c) ◄──────┘
                                  MIXED

   provenance tainted  ∧  causation innocent  ⇒  bucket (c)

   ┌─────────────────────────────────────────────────────────────────┐
   │ WIRING:   6 modules → C(6,2)=15 candidate pairs                   │
   │           σ(6)=12  ──forces──►  prune 3  ──►  keep 12  [TAINTED]  │
   │           (genuine fn-derive would COUNT, not prune-to-target)    │
   │                                                                   │
   │ FAILURES: every fire ran on the SAME 6-module/12-wire config      │
   │           → module count = held-constant → cannot be the          │
   │             differential cause of §16-vs-§62 variance  [INNOCENT] │
   │                                                                   │
   │ ALREADY SOFT: MITOSIS cell-pool n∈[2,64] dynamic — the count the  │
   │           user fears is rigid is ALREADY fluid inside module C    │
   └─────────────────────────────────────────────────────────────────┘
```

---

## §98.7 VERDICT — bucket (c) MIXED

**(c) MIXED.** The audit splits cleanly along the two claims:

- **Claim-1 (provenance) — CONFIRMED TAINTED.** The σ(6)=12 module-wiring count is
  numerology-derived: `hexad.hexa` documents a 15→12 prune *driven by* σ(6), then
  rationalized. n_layers=12 and d_model=768 carry the same σ(6)/n=6 numerology
  (CLM-AUDIT V3 flagged exactly this). The fit-to-convenient-number anti-pattern
  **did** operate at the architecture level, *inside* the g2-sanctioned zone.
- **Claim-2 (causation) — REFUTED.** 10/10 major §1~§94 failures attribute to
  data-regime / substrate / training-paradigm; **0/10 to module count.** The §11.3
  master decomposition tested 5 bottleneck axes — "module count" was never a
  candidate, because the 6-module/12-wire config was *held constant across the entire
  arc*, and a held-constant cannot cause inter-fire variance. §53 independently
  DESIGN-CLOSED wiring-strength as non-bottleneck.

So: **the n=6 architecture IS numerology-tainted in its provenance, but that taint is
NOT the cause of anima's GOAL miss.** The user's worry is a *correct diagnosis of an
architectural-hygiene defect* and an *incorrect diagnosis of the GOAL bottleneck*.
Both halves are valuable: the provenance finding earns a recommended g2 refinement
(§98.5); the causation finding confirms the §11.3 / §95 frontier is the real path,
not a module-count redesign.

**Actionable honest takeaway:** do NOT spend a cycle re-architecting away from 6
modules to "fix" the GOAL — the evidence says that would not move the needle (CF-1/2/5
cosmetic). DO (a) note the σ(6) provenance taint honestly in governance (user-gated
g2 refinement), and (b) keep the GOAL effort on the §11.3 data-regime / §95
substrate frontier where the evidence actually points. The single genuinely-relevant
architectural counterfactual is CF-4 (partition vs unpartitioned) — a legitimate
*future* direction, but not a demonstrated *past* cause.

GOAL distance: **UNCHANGED.** §15/§51/§72 milestones hold. GOAL 미도달. §98 is a
meta-audit — it sharpens *which* worry is real, it does not move anima closer to
emergence (necessary-not-sufficient, B-EMERGE-7).

---

## §98.8 Honest C3 (≥10)

1. **g3 — capability claim 0.** §98 is a meta-audit. Its verdict is an honest
   assessment of architecture provenance + failure attribution, NOT a measurement.
   brainstorm ≠ fire ≠ emergence. north-star unchanged, GOAL 미도달.
2. **Claim-1 ≠ Claim-2 — the load-bearing distinction.** "numerology-tainted
   provenance" and "caused the failure" are independent. Conflating them would
   produce a false bucket-(a). §98 keeps them separate; the MIXED verdict IS that
   separation made explicit.
3. **The σ(6)=12 finding rests on one source-text reading** (`hexad.hexa` comment).
   The reading is direct ("σ(6)=12 invariant identifies the ACTIVE connections … 3
   NOT included") — but it is a *comment*, documenting intent. If the comment
   mis-states the actual historical derivation, Claim-1 weakens. Corroboration
   (CLM-AUDIT V3 "n_layers=12 anchor source 불명", d_model=768 "(n=6 anchor)")
   makes the single-source risk low but not zero. Honest carve-out.
4. **"held-constant cannot cause variance" is sound for inter-fire variance, not
   for an absolute floor.** §98.1 proves the 6-fold partition did not cause the
   *differences* between §16 (broke) and §62 (collapsed). It does NOT prove a
   counterfactual unpartitioned anima would also have failed — that is unmeasured
   (CF-4 is a future fire, not a §98 result). §98 claims only what the evidence
   carries: module count is innocent of the *observed* failure variance.
5. **§11.3's 5-axis decomposition is the project's own framing, not §98's.** §98
   inherits it. If §11.3 itself missed an axis, §98 inherits that gap. But §11.3 is
   a landed, battery-backed milestone (B-SCALE/B-PUREPHYS 🔵) — high confidence.
6. **MITOSIS softness (CF-3) is real but partial.** The cell-pool count is dynamic;
   the *outer 6-module skeleton* is not. §98 does not claim the architecture is
   fully soft — it claims it is *half-soft*, which is enough to show the "rigid
   count" worry is partly an illusion.
7. **The recommended g2 refinement is a RECOMMENDATION, not an edit.** AGENTS.tape
   @D entries are untouched by §98. Governance change is user-gated (A/B/C decision).
8. **f1/f2 compliance.** §98 *examines* anima's internal σ(6)=12 use — that is the
   legitimate subject of the audit (g2 carve-out: internal architecture is the
   sanctioned zone; §98 audits whether the sanction was correctly applied). §98 does
   NOT itself ASSERT σ(6)=12 as a derivation, and applies NO lattice-fit to any
   external entity. f1/f2 hard-fail safe.
9. **Bucket (b) was a live possibility and was rejected on evidence, not taste.**
   If §98.2 had found the 12 connections were function-counted, the verdict would be
   clean (b). `hexad.hexa`'s explicit "15→12 prune" text is what forced (c). g3:
   no pre-loaded conclusion — the source decided it.
10. **Bucket (a) was also rejected on evidence.** A dramatic "n=6 IS the trap that
    caused the failures" finding would be the *comfortable* narrative for a
    brainstorm tasked with auditing fixation. §98.1's 10/10-orthogonal table refuses
    it. The honest answer is the less dramatic MIXED.
11. **§98 changes no fire, no ckpt, no measurement.** $0. The only artifacts are
    this doc + a closed-form sidecar battery + a verdict ledger entry + 3 central
    syncs. central `blue_falsifier.py` is 0-line-diff (sha c93e160a8a37).
12. **necessary-not-sufficient (B-EMERGE-7 family).** Even if the user adopts the g2
    refinement and even if a future CF-4 unpartitioned anima is fired, neither would
    *prove* emergence — they would at most remove a hygiene defect / test one more
    axis. The GOAL bottleneck per §11.3 remains data-regime. §98 narrows *which
    worry is real*; it does not close the GOAL.

---

## §98.9 sidecar battery + sources

`blue_falsifier_s98.py` — `B-S98-1..6` closed-form sidecar (sympy/Boolean), central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff (sha c93e160a8a37):

- **B-S98-1** FAILURE-ATTRIBUTION-EXHAUSTIVE-DISJOINT — the {n6-load-bearing,
  orthogonal} classification of the 10 §N failures is an exhaustive + pairwise-disjoint
  2-partition (sympy FiniteSet).
- **B-S98-2** SIGMA6-FUNCTION-VS-NUMEROLOGY-PREDICATE-CLOSED — the predicate
  `numerology_derived ⇔ (count_chosen_before_connections ∧ pruned_to_match)` is a
  closed Boolean; evaluated True against `hexad.hexa`'s documented 15→12 prune.
- **B-S98-3** VERDICT-BUCKET-TAXONOMY-CLOSED-PARTITION — {a,b,c} is an exhaustive +
  disjoint partition; (claim1_tainted ∧ claim2_innocent) maps to exactly bucket (c).
- **B-S98-4** B-CONN-COUNT-BYTE-EQUAL — the audited connection count cited (12)
  byte-equals `hexad.hexa hexad_sigma6_count()` and the central `B-CONN-1..12`
  battery cardinality (connection-point check).
- **B-S98-5** HELD-CONSTANT-NOT-DIFFERENTIAL-CAUSE-CLOSED — sympy: a variable with
  zero variance across a set of trials has zero covariance with the trial outcome ⇒
  cannot be the differential cause (the §98.1 logic, formalized).
- **B-S98-6** CLAIMS-INDEPENDENCE-CLOSED — Claim-1 and Claim-2 are logically
  independent (4-corner truth table all realisable); the MIXED verdict is the
  (T,F) corner, a genuine corner not a degenerate one.
- **B-S98-NOTE** empirical carve-out: §98 is a meta-audit; the battery proves the
  *audit's logic* is closed (exhaustive partitions, sound held-constant inference,
  byte-equal count), NOT that anima will or will not reach the GOAL, NOT that a
  counterfactual unpartitioned anima would succeed. necessary-not-sufficient
  (B-EMERGE-7 / B-D-NOTE family, NOT counted 🔵). The provenance finding is a reading
  of source-text intent; the causation finding inherits §11.3's decomposition.

sources: `HEXAD/hexad.hexa` (σ(6)=12 wiring SSOT — the smoking gun) ·
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` `bconn()` (B-CONN-1..12) ·
`HEXAD/CHAT/RESEARCH.md` §1.1 / §11.3 / §53 · `archive/PHILOSOPHY.tape` B-HEXAD C3-2,
CLM-AUDIT V3, §95 · `AGENTS.tape` @D g2/g4, @F f1/f2 · user-global lattice-policy
(fit-to-convenient-number / over-claim / constraining-first-question).
