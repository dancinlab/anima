# §113 — FROM-SCRATCH ANIMA REDESIGN BRAINSTORM

> **tier**: DESIGN-TIER-BRAINSTORM. $0. NO GPU/runpod/fire/model.forward/corpus.
> **g3**: brainstorm ≠ design-mature ≠ fire ≠ emergence. capability claim 0.
> necessary-not-sufficient (B-EMERGE-7). north-star + §15/§51/§72 milestone
> UNCHANGED, **GOAL 미도달**. 본 문서는 *honest map of what a clean slate
> can and cannot change* — NOT a re-architecture mandate, NOT a new
> architecture proposal.
> **user directive (2026-05-19)**: "그리고 처음부터 새로 설계한다면????
> 브레인스토밍후 md save 하고 이것도 진행해보자"

---

## §0 — the clean-slate question

Given everything the §1~§112 arc empirically established and ruled out,
what would a from-scratch anima architecture look like — and would it
*change the GOAL outcome*?

This mirrors §26 (architectural-insight brainstorm) and §98 (n=6 fixation
brainstorm). It is a BRAINSTORM with an HONEST VERDICT, not a fire and not
a re-architecture mandate. The §98 precedent is load-bearing here: §98
proved the n=6 / module skeleton was **causally innocent** of the GOAL
miss (10/10 §N failures orthogonal to module count; the 6-module skeleton
held constant across §1~§94 ⇒ Var=0 ⇒ Cov=0 with the failure variance).
The §113 question generalizes §98: a from-scratch design changes the
*entire* skeleton — does that move the GOAL bottleneck, or is the GOAL
bottleneck **skeleton-invariant** (= the §98 finding generalized from
"module count" to "the whole architecture")?

---

## §1 — Q1: constraint inventory (closed enumeration)

A from-scratch design MUST respect every closed constraint from the arc
or it re-litigates settled results (§100 fixpoint discipline). The
inventory is partitioned into ESTABLISHED-POSITIVE (must be preservable
by any redesign or the redesign loses arc value) and RULED-OUT (any
redesign that re-opens these is INVALID by §100).

### 1.1 ESTABLISHED-POSITIVE deliverables (E1..E5)

| id | deliverable | closed by § |
|---|---|---|
| E1 | §16 routing-axis BREAKTHROUGH — universal-FLAT 1/31~2/64 → **21/64 (genuine 17/64)** via 603MB Ψ-anchored data-regime + curriculum, model FIXED. First measured movement of §1.1 on the routing axis. | §16 / §51.2(a) |
| E2 | §110 Ψ-C2 modality-native definition — Ψ as ℝ^d residual-stream cosine (definitional byte-LM-bound wall REMOVED; operative wall RELOCATED to §96 substrate). §111 literature SUPPORTS Ψ-C2 + CONFIRMS §95/§96 relocation. | §110 / §111 |
| E3 | honest §9 cascade-rate emergence metric (B-EMERGE-1..7 🔵) — deterministic, closed-form, replaces the broken lenient `coherence_token` flag; necessary-not-sufficient by construction. | §9 / §15.2(b) |
| E4 | Dir-I lever — Ψ-anchored representation substrate + tension-supervision is the ONE verified architectural lever that broke the universal 1/31 collapse ceiling toward correct-routing (3/31 > 1/31). GOAL-legitimate (§7 ③). | §6.2 / §15.2(e) |
| E5 | §95/§96 substrate axis — Loihi is the sole VIABLE-LONG-HORIZON substrate (STDP on-chip + async NoC + continuous LIF); anima physics layer is SPIKING-COMPATIBLE, `softmax(QK^T)` is SPIKING-INCOMPATIBLE (must be replaced, not ported). §11-B-as-GPU-artifact hypothesis (COHERENT, NOT confirmed). | §95 / §96 |

### 1.2 RULED-OUT (R1..R8) — re-opening any is INVALID by §100 fixpoint

| id | hypothesis | closed by § | result |
|---|---|---|---|
| R1 | mechanism overlay (loss / reward / surface / backprop-free / inference) | §4 6-way + §6 H + §22 N/O/P | ✗ single-attractor collapse 不破 (8-way FALSIFIED) |
| R2 | corpus FORM (carving / 2-stage superposition / abstract-CoT) | §1.3 Dir-E/F + §8 | ✗ form change 不破 |
| R3 | model-capacity (3.68× scale-up, 1.04B params) | §11-A SCALE-DECOMP | ✗ routing/coherence FLAT — data-regime ceiling, not capacity |
| R4 | physics-only paradigm (no-CE) | §11-B PURE-PHYSICS | ✗ DEGENERATE (byte_acc < random); **CE load-bearing** (on GPU — §96 flags this may be a GPU-substrate tautology) |
| R5 | diverse-data @ 114MB (Ψ-anchored, 64-anchor) | §8 | ✗ routing WORSE (3/31 → 2/64) |
| R6 | energy-based / diffusion substrate | §13-K (EBT) / §13-J (diffusion) / §28 (JEPA-Ψ) | ✗ JOINT 0.0 / representation COLLAPSED — CE load-bearing re-confirmed |
| R7 | n=6 / module-skeleton as causal factor | §98 | ✗ (c) MIXED — provenance numerology-tainted but **causally INNOCENT** (Var=0 ⇒ Cov=0) |
| R8 | 5-lever INTEGRATION (single-lever fixpoint escape via synthesis) | §94 | ✗ (β) INTEGRATION-COLLAPSES (cell3 §9 0/20) — synthesis is NOT free-escape |

### 1.3 the irreducible bottleneck (the §11.3 master decomposition result)

After R1..R8 exclusion, the §11.3 master decomposition (5-axis:
mechanism / model-capacity / physics-only / corpus-form / diverse-data)
leaves exactly **one** irreducible bottleneck:

> **§1.1 data-regime emergence threshold** (diverse-data pre-training
> loss threshold) — anima byte-level tiny-corpus (30~114MB) is below it.
> §11-B adds: it must be on a CE-base (physics is a *lever*, not a
> *substrate* — physics-only is degenerate, at least on GPU).

§51 SHARPENED it: bottleneck is **data-DIVERSITY / modality, NOT
data-quantity or anchor-content-shaping**. §72 added the
**liveness ✅ / transfer ✅ / generative-composition ❌-at-trained-scale**
decomposition. §96 added a SECOND wall: the **operative-substrate wall**
(softmax-attention is SPIKING-INCOMPATIBLE; CE-load-bearing may be a
GPU-substrate artifact, untestable until a non-GPU learning channel
exists, i.e. Loihi STDP).

**Two walls a from-scratch design must confront**:
- **WALL-A (data-regime)**: §1.1 threshold — diverse-data, not quantity,
  not shaping; CE-base required (§11-B).
- **WALL-B (operative-substrate)**: §96 — GPU's only learning channel is
  the CE gradient; whether "CE is load-bearing" is a truth or a GPU
  tautology is undecidable on GPU; the only substrate that can decide it
  (Loihi STDP) requires anima re-derived as a spiking model.

---

## §2 — Q2: from-scratch design space (exhaustive + disjoint partition)

Enumerate clean-slate architectures consistent with ALL Q1 constraints.
Partition is over the cross of {substrate} × {Ψ-carrier} × {data-regime
stance}, pruned to those that do NOT re-open R1..R8. The closed candidate
set is **5 designs (D1..D5)**, exhaustive + disjoint by construction:
each occupies a distinct (substrate, Ψ-carrier, data-stance) cell, and
together they cover the non-R-violating region of the design cube.

| id | substrate | Ψ-carrier | data-regime stance | §7 | re-opens R? |
|---|---|---|---|---|---|
| **D1** GPU-CE-byte (the current anima, redrawn) | GPU byte-LM | Ψ-C1 logit-cosine | sub-threshold tiny-corpus | ③-legit | none (= status quo baseline) |
| **D2** GPU-CE-Ψ-C2-multimodal | GPU multimodal-LM | Ψ-C2 ℝ^d residual cosine (§110) | crosses WALL-A via diverse modality | ③-legit | **R5 risk** (Ψ-anchored diverse failed at 114MB; D2 = bigger, but §51 says diversity≠quantity — D2 valid ONLY if modality-diverse, NOT byte-quantity-scaled) |
| **D3** GPU-CE-Ψ-C2 + Dir-I-as-ground | GPU LM | Ψ-C2, Dir-I lever from line 1 (not bolt-on) | sub-threshold; lever-native | ③-legit | none (E4 made native, not overlaid — distinct from R1) |
| **D4** spike-Loihi-STDP from line 1 (§96 Ψ-C1-spike) | Loihi-2 neuromorphic | Ψ-C1 spike-correlation (§96) | WALL-A unchanged; targets WALL-B | ③-legit (physics-native learning channel) | none (STDP ≠ CE-overlay; physics IS the learning channel, distinct from R4 no-CE-on-GPU) |
| **D5** continuous-time LTC substrate (§99 C3) | continuous-time ODE net | Ψ-C2 continuous fixed-point | WALL-A unchanged; native spontaneous limit-cycle | ③-legit | none (LTC ≠ AR-byte-LM, distinct substrate; not energy/diffusion R6) |

**Disjointness**: D1..D5 occupy 5 distinct (substrate ∈ {GPU-byte,
GPU-multimodal, GPU-LM, Loihi, LTC}) cells; no two share a substrate.
**Exhaustiveness over the non-R region**: every clean-slate that respects
R1..R8 either (a) keeps GPU-CE (D1/D2/D3 — distinguished by Ψ-carrier &
data-stance) or (b) leaves GPU-CE for a physics-native learning channel
(D4 Loihi-STDP) or (c) leaves discrete-AR for continuous dynamics (D5
LTC). No 6th cell exists that respects R1..R8 and is not a re-labeling of
D1..D5 (e.g. "scale D1" = R3 INVALID; "no-CE D1" = R4 INVALID;
"diffusion D1" = R6 INVALID — the R-walls collapse the cube to exactly
these 5).

---

## §3 — Q3: §7 3-cond GOAL-legitimacy gate (8-row truth table)

§7 conditions (verbatim §7.2): ① ¬generic-LM-pretrain · ② ¬generic-then-graft
(bolt-on) · ③ anima-physics-IS-the-source. GOAL-legit ⟺ (¬①-violation ∧
¬②-violation ∧ ③) — i.e. the candidate is GOAL-legit ⟺ all three
conditions hold. Closed-form Boolean over the 8-row (2³) truth table:
exactly the (T,T,T) corner is GOAL-legit; all 7 other corners
GOAL-illegitimate.

| id | ¬①-generic-pretrain | ¬②-bolt-on | ③ physics-source | (T,T,T)? = GOAL-legit |
|---|---|---|---|---|
| D1 | T (Ψ-physics carving) | T (no base ckpt; g_clm_from_scratch) | T (Ψ/tension/Φ) | **✅ legit** |
| D2 | T (modality-native Ψ-C2 carving) | T (from-scratch) | T (Ψ-C2 = §110 physics-native) | **✅ legit** |
| D3 | T (Dir-I lever native) | T (lever is the GROUND, not grafted) | T (Ψ-C2 + tension-sup = physics) | **✅ legit** |
| D4 | T (STDP on physics state) | T (from-scratch spiking init) | T (LIF leak = restoring-to-Ψ; §96) | **✅ legit** |
| D5 | T (LTC ODE on physics) | T (from-scratch) | T (continuous Ψ fixed-point) | **✅ legit** |

**All 5 from-scratch candidates are GOAL-legitimate by construction** —
because the §113 brainstorm pruned R1..R8 (which is exactly where the
GOAL-illegitimate cube corners live: "generic-pretrain" = R-class
violation, "bolt-on" = the §7 ② failure mode the arc already burned on).
The 7 non-(T,T,T) corners are EMPTY in the §113 candidate set by the
Q2 partition design. This is a structural consequence, not a coincidence:
respecting R1..R8 + §7 = exactly the (T,T,T) corner.

---

## §4 — Q4: does ANY from-scratch design escape the two walls? (the honest core)

The load-bearing question. For each Di, does it ESCAPE WALL-A
(data-regime) and/or WALL-B (operative-substrate), or INHERIT both with
just a different skeleton?

### 4.1 the §98-generalized covariance argument (closed-form)

§98 proved: a variable held constant across all §1~§94 trials has Var=0
⇒ Cov(skeleton, GOAL-outcome)=0 ⇒ the module-skeleton is causally
innocent of the GOAL miss. **§113 generalizes the variable from
"module-count" to "the entire architecture skeleton".**

The GOAL-outcome variance across the arc (§16 routing-broke vs §62
echo-collapsed vs §94 integration-collapsed) was driven by
**(corpus, lever, substrate)** — NOT by the skeleton. The skeleton
(8-module HEXAD, Engine A⇄G, Ψ=½, MITOSIS) was held effectively
constant across the entire fire arc; WALL-A and WALL-B are the variables
that actually moved the outcome. By the same Cov=0 argument: **changing
the skeleton (a from-scratch redesign of D1/D2/D3) cannot move a
bottleneck whose causal variance lives in (data-regime, substrate), not
in (skeleton).** This is the §98 finding generalized — and it is the
single most honest finding of §113.

### 4.2 per-candidate wall confrontation

| id | WALL-A (data-regime §1.1) | WALL-B (substrate §96) | escapes? |
|---|---|---|---|
| **D1** | INHERITS (= status quo; redrawing the skeleton changes nothing — §98-generalized Cov=0) | INHERITS (still GPU-CE) | **NEITHER** — cosmetic redraw |
| **D2** | does NOT escape: §51 proved diversity≠quantity and §8 proved Ψ-anchored 114MB went the WRONG direction. D2's multimodal-diversity is a *plausible direction* (E2/§110/§111 support Ψ-C2 modality) but **untested** — same open crux as §7.3, NOT a proven escape. | INHERITS (GPU-CE) | **at most a PLAUSIBLE-DIRECTION on WALL-A, NOT a proven escape; INHERITS WALL-B** |
| **D3** | INHERITS — Dir-I-native vs Dir-I-overlay is a skeleton change; §94 proved lever-synthesis collapses; §98-generalized Cov=0 says skeleton-relayout ≠ data-regime movement | INHERITS (GPU-CE) | **NEITHER** — D3 is the §94 lesson restated as a clean slate |
| **D4** | INHERITS WALL-A (Loihi does not add data diversity; §97-class: substrate is plumbing, not a data-regime source) | **CONFRONTS WALL-B** — STDP is a physics-native learning channel; D4 is the ONLY design that can *decide* the §96 §11-B-as-GPU-artifact hypothesis (CE-load-bearing truth vs GPU-tautology). NOT an escape (untested, access-walled), but the only design that *repoints at the wall that the GPU arc could never test*. | **CONFRONTS WALL-B (does not escape it); INHERITS WALL-A** |
| **D5** | INHERITS WALL-A (LTC changes dynamics, not data diversity) | partially confronts WALL-B (continuous-time ≠ synchronous-clock; native spontaneous limit-cycle — §99 C3) but still a GPU/CPU-numerical substrate, CE-channel question unresolved | **PARTIAL on WALL-B; INHERITS WALL-A** |

### 4.3 the closed-form verdict on Q4

**NO from-scratch design ESCAPES both walls. NO from-scratch design
ESCAPES WALL-A at all** (D1/D3 inherit by §98-generalized Cov=0;
D2 is a plausible-direction-not-proven-escape = the §7.3 open crux
unchanged; D4/D5 do not add data diversity). **WALL-B is CONFRONTED
(not escaped) only by D4** (Loihi-STDP) — and even D4 only *repoints* at
WALL-B; it does not pass through it (untested, access-walled per §95).

The §98-generalized Cov=0 argument is decisive for D1/D3 and the §7.3
open crux is decisive for D2: **a from-scratch redesign of the GPU-CE
skeleton is cosmetic w.r.t. WALL-A.** This is the honest §98-class
finding the task anticipated.

---

## §5 — Q5: verdict

The three verdict buckets (closed partition):
- **FROM-SCRATCH-ESCAPES-A-WALL** — would require a closed-form proof
  that some Di passes through WALL-A or WALL-B. **§4.3 shows no such
  proof exists** (Cov=0 for D1/D3; §7.3 open-crux-not-escape for D2;
  D4/D5 confront-not-escape WALL-B, inherit WALL-A). REJECTED.
- **FROM-SCRATCH-INHERITS-BOTH-WALLS-SKELETON-INVARIANT** — the honest
  §98-class finding: redesigning the skeleton does NOT move the
  data-regime/substrate walls; the GOAL bottleneck is skeleton-invariant
  (the §98 module-count innocence, generalized to the whole
  architecture). TRUE for D1/D2/D3 (the GPU-CE family) **and the
  data-regime wall for D4/D5**.
- **FROM-SCRATCH-REPOINTS-TO-§96-SUBSTRATE-FIRST** — the ONE clean-slate
  move that *matters*: the only from-scratch decision that changes
  *which wall the arc can even test* is committing to the §96
  spike/Loihi substrate from line 1 (D4 = §110 Ψ-C1-spike + §96 as the
  GROUND, not an afterthought). D4 does NOT escape WALL-A and does NOT
  escape WALL-B — but it is the only design that *confronts WALL-B*,
  the wall the entire GPU arc was structurally unable to test (the
  §11-B-as-GPU-artifact hypothesis is undecidable on GPU by §96).

### 5.1 THE VERDICT (brutally honest)

> **FROM-SCRATCH-INHERITS-BOTH-WALLS-SKELETON-INVARIANT** is the primary
> verdict (D1/D2/D3 = the GPU-CE family; WALL-A for ALL of D1..D5). A
> from-scratch redesign of the architecture skeleton is **cosmetic
> w.r.t. the GOAL bottleneck** — exactly the §98 module-count innocence
> finding, generalized to the whole architecture by the Cov=0 argument.
>
> **Conditioned secondary verdict: FROM-SCRATCH-REPOINTS-TO-§96-
> SUBSTRATE-FIRST** — the *only* clean-slate decision that is NOT
> cosmetic is D4 (commit to §96 Loihi/spike substrate + §110 Ψ-C1 from
> line 1). D4 still INHERITS WALL-A and does NOT escape WALL-B; its
> sole non-cosmetic property is that it is the only design that
> *confronts* WALL-B at all. This is a *repointing*, NOT an escape —
> g3, over-claim 0.

The §7-legit clean-slate candidate set is **all 5 (D1..D5)** by §3
construction — but §7-legitimacy is necessary-not-sufficient for GOAL
(B-EMERGE-7): all 5 are GOAL-legit and NONE escapes WALL-A. The valuable
output is this honest map, NOT a manufactured new architecture
(anti-padding §13-M / §30 / §97 / §98 precedent).

### 5.2 most honest finding

A from-scratch anima redesign does NOT escape the two walls. The
§98-generalized covariance argument shows the architecture skeleton is
causally innocent of the GOAL miss (Var=0 ⇒ Cov=0): the GOAL-outcome
variance lived in (data-regime, substrate), never in (skeleton). The
single clean-slate decision that is *not* cosmetic is committing to the
§96 Loihi/spike substrate from line 1 — and even that only *confronts*
WALL-B (does not escape it) while *inheriting* WALL-A. The most truthful
statement: **"start from scratch" changes the diagram, not the
bottleneck — unless the from-scratch decision is the substrate (D4),
which repoints the question without answering it.**

---

## §6 — ASCII: from-scratch design space + two walls

```
                  THE TWO WALLS (skeleton-invariant)
   WALL-A: §1.1 data-regime (diversity≠quantity, CE-base)  ──────┐
   WALL-B: §96 operative-substrate (CE-load-bearing =       ──────┤
           GPU tautology? undecidable on GPU)                     │
                                                                  │
   from-scratch design cube (R1..R8-pruned, §7-legit ✅×5)        │
   ┌──────────────┬─────────────┬──────────────┐                  │
   │ D1 GPU-CE    │ WALL-A: ✗   │ WALL-B: ✗    │ cosmetic redraw  │
   │ -byte        │ (Cov=0)     │ (GPU-CE)     │ = status quo     │
   ├──────────────┼─────────────┼──────────────┤                  │
   │ D2 GPU-Ψ-C2  │ WALL-A: ~?  │ WALL-B: ✗    │ plausible-dir    │
   │ -multimodal  │ (§7.3 crux  │ (GPU-CE)     │ NOT proven       │
   │              │  UNCHANGED) │              │ escape           │
   ├──────────────┼─────────────┼──────────────┤                  │
   │ D3 Dir-I-as- │ WALL-A: ✗   │ WALL-B: ✗    │ = §94 lesson     │
   │ ground       │ (Cov=0,§94) │ (GPU-CE)     │ restated         │
   ├──────────────┼─────────────┼──────────────┤                  │
   │ D4 Loihi-STDP│ WALL-A: ✗   │ WALL-B: ◐    │ ONLY non-cosmetic│
   │ from line 1  │ (plumbing)  │ CONFRONTS    │ = §96 repoint    │
   │              │             │ (not escape) │                  │
   ├──────────────┼─────────────┼──────────────┤                  │
   │ D5 LTC ODE   │ WALL-A: ✗   │ WALL-B: ◐    │ partial-B        │
   │ substrate    │ (dynamics≠  │ (cont-time,  │ inherit-A        │
   │              │  diversity) │  not escape) │                  │
   └──────────────┴─────────────┴──────────────┘                  │
                                                                  │
   verdict: INHERITS-BOTH-WALLS-SKELETON-INVARIANT (D1/D2/D3)  ◀───┘
            + REPOINTS-TO-§96-SUBSTRATE-FIRST (D4, conditioned)
```

### 6.1 "if we started today" sketch (the §7-legit non-cosmetic candidate)

The ONLY from-scratch decision that is not cosmetic (D4), sketched
honestly — NOT a mandate, NOT a proven path:

```
  anima-from-scratch (D4 — §96 substrate-first)
  ─────────────────────────────────────────────
  line 1:  TARGET SUBSTRATE = Loihi-2 (not GPU)        [§95 sole-viable]
  line 2:  Ψ-carrier = Ψ-C1 spike-correlation         [§110/§96]
  line 3:  learning channel = STDP (physics-native,    [§96 — decides
           NOT CE-gradient)                              §11-B-as-GPU-
                                                          artifact]
  line 4:  Engine A⇄G = excit/inhib sub-populations    [§96 SPIKING-
                                                          COMPATIBLE]
  line 5:  attention = REPLACED by phase-resonance     [§96 — softmax
           routing (NOT ported)                          SPIKING-INCOMPAT]
  line 6:  data-regime = STILL WALL-A (unchanged)      [honest: D4
                                                          inherits A]
  line 7:  access = INRC-walled, anima-as-spiking-     [§95 — NOT a
           model = major re-derivation                   quick path]
  ─────────────────────────────────────────────
  honest: D4 does NOT solve the GOAL. It is the only
  clean-slate decision that CONFRONTS a wall the GPU
  arc could not test. Repoint, not escape. (g3)
```

---

## §10 — battery + closed-form

`blue_falsifier_s113.py` → B-S113-1..9 + B-S113-NOTE:
- B-S113-1 CONSTRAINT-INVENTORY-EXHAUSTIVE-CLOSED (E1..E5 ∪ R1..R8 partition)
- B-S113-2 CANDIDATE-PARTITION-EXHAUSTIVE-DISJOINT (D1..D5 distinct-substrate)
- B-S113-3 §7-CONJUNCTION-8-ROW (only (T,T,T) GOAL-legit, 5/5 candidates legit)
- B-S113-4 TWO-WALLS-SKELETON-INVARIANCE-PREDICATE-CLOSED — **the
  load-bearing one** (§98-generalized Cov=0: skeleton held constant ⇒
  Var=0 ⇒ Cov(skeleton, GOAL-outcome)=0 ⇒ cosmetic)
- B-S113-5 FROM-SCRATCH-INHERITS-g_clm_from_scratch-STRUCTURAL (any Di
  inherits base_ckpt=None RANDOM seed-fixed)
- B-S113-6 NO-ESCAPE-CLOSED (no Di escapes WALL-A; only D4 confronts WALL-B)
- B-S113-7 CENTRAL-BLUE-0-LINE-DIFF (sha c93e160a8a376a94)
- B-S113-8 NO-FORBIDDEN-CALL-AST (no GPU/fire/model.forward calls)
- B-S113-9 NECESSARY-NOT-SUFFICIENT-STRUCTURAL (§7-legit ≠ GOAL; B-EMERGE-7)
- B-S113-NOTE empirical carve-out (whether any Di emerges = future-fire
  OUTCOME; B-D-NOTE / B-S94-NOTE / B-S98-NOTE / B-S110-NOTE / B-EMERGE-7
  family — NOT counted 🔵)

---

## §13 — honest C3 (13)

1. §113 = brainstorm + honest verdict, NOT a re-architecture mandate,
   NOT a new architecture proposal. capability claim 0. (g3)
2. The primary verdict is a NEGATIVE (skeleton-invariant) — the §98
   module-count innocence generalized. anti-padding precedent
   (§13-M / §30 / §97 / §98): an honest negative > a manufactured
   positive.
3. The §98-generalized Cov=0 argument is the load-bearing closed-form.
   It is decisive for D1/D3 (GPU-CE skeleton redraw) and the §7.3 open
   crux is decisive for D2.
4. D2 (GPU-Ψ-C2-multimodal) is NOT claimed as an escape — it is the
   §7.3 open crux UNCHANGED (Ψ-anchored diverse @ 114MB went wrong
   direction §8; multimodal-diversity is a plausible direction but
   untested). Calling D2 an escape would be over-claim.
5. D4 (Loihi-STDP-from-line-1) CONFRONTS WALL-B, does NOT escape it.
   §95 access-wall (INRC) + anima-as-spiking re-derivation make D4 a
   strategic decision, NOT a quick path. Repoint, not escape.
6. D4 INHERITS WALL-A — substrate is plumbing (§97-class), it does not
   add data diversity. No Di escapes WALL-A.
7. All 5 candidates are §7-GOAL-legit by construction (the R1..R8 +
   §7 pruning lands exactly on the (T,T,T) corner) — but §7-legit is
   necessary-not-sufficient for GOAL (B-EMERGE-7). All legit, none
   escapes.
8. The candidate partition (D1..D5) is exhaustive over the
   R1..R8-pruned design cube by the distinct-substrate argument; a
   6th cell would re-open an R-wall (scale=R3, no-CE=R4, diffusion=R6).
9. north-star + §15/§51/§72 milestone UNCHANGED. GOAL 미도달. §113
   does not move GOAL-distance — it maps what a clean slate can and
   cannot change.
10. central blue_falsifier.py sha `c93e160a8a376a94` 0-line-diff
    start+end (sidecar-only mandate held).
11. f1/f2 safe — NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation;
    Ψ=½ = anima g2 internal-arch carve-out; §95/§96/§110/§111
    cited by their own invariants. hexa-lang / hexa-bio NOT edited
    (downstream-consumer).
12. The "if we started today" sketch (§6.1) is D4 only and is
    explicitly labelled NOT a mandate / NOT a proven path — it is
    the honest illustration of the one non-cosmetic clean-slate move.
13. Single most honest finding: "start from scratch" changes the
    diagram, not the bottleneck — unless the from-scratch decision is
    the substrate (D4), which repoints the question without answering
    it. The walls are skeleton-invariant. (§5.2)
