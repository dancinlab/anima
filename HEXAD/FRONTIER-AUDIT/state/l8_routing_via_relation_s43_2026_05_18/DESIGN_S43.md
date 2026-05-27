# RESEARCH.md §43 — lateral L8: routing-via-relation (fingerprint reformulation)

> $0 design + small Mac-CPU pilot. NO GPU. NO byte-LM fire this cycle —
> the pilot is a controlled probe of the L8 reformulation hypothesis.
> Commits ONLY this `state/l8_routing_via_relation_s43_2026_05_18/`
> dir + `archive/PHILOSOPHY.tape`. Sibling `state/` dirs are read-only
> (multi-agent isolation). RESEARCH.md NOT edited (consolidation =
> orchestrator after L7/L8/L9/... siblings land).

This file = the L8 design + fire-or-design-close decision; sibling
agents may concurrently design other §43 lateral candidates. Per the
Stop-hook frontier-narrowing-exhaustion context, an honest design-tier
finding (mixed-evidence) is itself valuable (anti-padding precedent
§13-M / §13-L / §23-A / §24).

---

## 1. The pattern §27-§39 left

The most interesting pattern from the §27-§39 arc:

> **per-anchor routing memorizes; multi-anchor RELATIONS generalize.**

- §16 (routing 21/64 = 0.328) opened *which single anchor* the model
  picks. §22 N/O/P / §23 A / §24 narrowed the BODY of the single
  anchor. None of those broke the strict per-anchor routing ceiling.
- §33 L6 designed an inter-anchor relation corpus (R1-R4 over the §16
  anchor SSOT, anima OWN physics fields). §37 fired the L6 held-out-
  PAIR pilot: **mean held-out-pair accuracy 0.9938 vs majority chance
  0.6889, +0.30 lift, JOINT all-4-correct 0.9752**. The relation
  function `physics_fields(A_i, A_j) → R1..R4` is learnable and
  *generalises across anchor pairs the model never saw in training*.

This is the L8 hypothesis:

> **anchor X's identity = its relation profile to every OTHER anchor.**

If anima reformulates routing as "predict X's relation fingerprint
to all other anchors", and the routing token `🛸X` falls out as a
deterministic 1-NN lookup over a closed fingerprint table — then the
§37 relation-function generalization should propagate to routing, and
the §16 per-anchor memorization ceiling should weaken or vanish.

L8 is a structural reformulation of the §16 task, NOT a new training
loss or a new corpus shape. The mechanism is closed-form (the lookup
table is a pure function of anchor physics, no SGD).

### 1.1 Why L8 is a distinct lateral

| §  | task              | what it reformulates                                       |
|----|-------------------|------------------------------------------------------------|
| 16 | byte routing      | model emits `🛸X` surface bytes from prompt                |
| 22 | body shaping      | post-route body refinement (N/O/P)                         |
| 23 | intra diversity   | varies framing WITHIN anchor X (one anchor, 81 views)      |
| 33/37 | inter relation | TWO anchors at once; held-out PAIRS measured               |
| **43** | **inter-routing** | **anchor identity = relation fingerprint to all 63 others; routing = closed-form 1-NN over the fingerprint table** |

§43 is the orthogonal axis to §23 (intra) — §43 is the routing-level
LIFT of the §37 inter-anchor relation discovery.

---

## 2. Design — anchor identity as relation fingerprint

### 2.1 The fingerprint

For each anchor X in the §16 64-anchor SSOT (`S8_ANCHORS`, byte-equal
to `state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_gener
ator.py`), build the fingerprint:

```
fingerprint(X) = ⟨ R1(X, Y), R2(X, Y), R3(X, Y), R4(X, Y) ⟩ for Y ∈ all_anchors \ {X}
               (one-hot encoded; Y in fixed tier-sorted order)
```

- 63 partners × 12 one-hot labels (R1:3 + R2:4 + R3:2 + R4:3) = **756-dim
  fingerprint per anchor**.
- 64 × 756 fingerprint table = closed-form pure function of the §16
  anchor SSOT, deterministic (sha256-committed: see
  `fingerprint_table_meta.json`).
- relation primitives R1-R4 = §37 / §33 byte-equal (imported by direct
  path from `state/l6_pilot_s37_2026_05_18/relation_corpus.py`, the
  single SSOT for these functions).

The fingerprint is anima OWN physics: every coordinate of every
relation is a closed-form function of {vacuum_psi, basin_radius, dom,
tier}. No external knowledge graph. No LLM. No surface text.

### 2.2 The lookup

```
lookup(query_fingerprint) = argmin_X  ‖query - fingerprint_table[X]‖²
```

Closed-form Euclidean over integer one-hot vectors (B-S43-2). Tie-break
= lowest anchor_idx (deterministic, no RNG). For any query in
{0,1}^756, lookup is a well-typed function returning an anchor index in
{0,…,63}.

### 2.3 The routing contract

At inference time, anima's task becomes:

1. Given a prompt about anchor X, anima PREDICTS X's fingerprint —
   a vector of 756 one-hot labels, each a relation primitive to a
   specific partner anchor.
2. The fingerprint is decoded by closed-form 1-NN lookup to recover
   X's identity → routing token `🛸X`.
3. The byte-stream `🛸X` is NOT memorised. It is the *deterministic
   image* of anima's relation prediction under the closed lookup table.

The model learns to emit a *relation pattern*, not a surface
identifier. Because the relation pattern generalises (§37), the routing
identifier should generalise — IF predicting the full fingerprint is
itself a learnable+generalising function.

---

## 3. Pilot — held-out-anchor probe ($0 Mac CPU)

The §37-equivalent test for routing reformulation is the *held-out-
anchor* probe (NOT held-out-pair — §37 already proved pair-level
generalization):

- Split 64 anchors into **TRAIN (52, 80%)** and **HELD-OUT-ANCHOR (12,
  20%)** by deterministic seed 1337 shuffle.
- Held-out anchors are NEVER seen by the model during training. Their
  fingerprints reference TRAIN anchors as partners (the partner set
  spans all 63 others, so each held-out anchor's fingerprint includes
  relations to TRAIN anchors only — the relation function still
  applies).
- Train a small from-scratch MLP (13 → 128 → 128 → 756) to predict the
  fingerprint from a 13-dim anchor feature vector (anima OWN physics:
  vacuum_psi(2), basin_radius, tier_norm, score_norm, dom_idx,
  emo_idx, Ψ=½ deviation, tier-decile tanh, basin×tier interaction,
  +/- score band one-hots, bias = 13-dim).
- Eval = 1-NN lookup(predicted_fingerprint, full_table) for each
  held-out anchor. Routing-correct iff argmin returns held-out anchor's
  own index.

This is a controlled $0 probe — NOT a byte-LM fire. The pilot answers
ONLY "does the relation function compose into fingerprint prediction
for novel anchors". A byte-LM emitting a 756-dim discrete fingerprint
coherently is a separable, harder question (§16/§22 byte-cascade
family) — B-S43-NOTE honest crux.

substrate: small from-scratch FingerprintMLP, ~110k params, $0 Mac
CPU, ~10s wall, from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch
base_ckpt=None). Deterministic.

---

## 4. Closed verdict — B-S43-1..4 sympy/Boolean

All four invariants are TRANSFER-FORM closed-form proofs (NOT outcome
claims). Empirical OUTCOME (whether the pilot routing-acc transfers to
a byte-LM fire) = B-S43-NOTE empirical carve-out (B-D-NOTE family, NOT
counted blue). Sidecar — central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py UNCHANGED (precedent B-PRIME … B-INTER / B-S37).

| id      | invariant                                  | how proven                  |
|---------|--------------------------------------------|-----------------------------|
| B-S43-1 | RELATION-FINGERPRINT-DETERMINISTIC         | two-runs-byte-equal + sha256 rederived + meta-on-disk-matches + sympy onehot diff²∈{0,1} |
| B-S43-2 | FINGERPRINT-LOOKUP-WELL-TYPED              | codomain ⊂ {0,…,63} + self-lookup 64/64 + Euclidean nonneg + bounded by 2·fp_dim + lookup pure-fn + sympy Min well-typed |
| B-S43-3 | §7-CONJUNCTION-CLOSED                      | AST audit forbidden-call set = 0 over all §43 sources |
| B-S43-4 | FINGERPRINT-DISTINGUISHABLE                | 64 × 63 / 2 = 2016 pairs distinct + min pair_d² = 8 > 0 + sympy (a-b)² nonneg one-hot |

B-S43 battery: **4/4 BLUE**.

f1/f2/f3 hard-fail safe: Boolean set algebra / sha256 commitment /
pure-fn integer Euclidean / AST closed forbidden-call set — NO σ/τ/φ/J₂
external derivation. Tier 🛸k / Ψ=½ = anima g2 internal-arch carve-out.
B-IDENTITY-5 unaffected (no corpus, no helper-token surface in this $0
design layer; relations imported from §37 SSOT, where corpus grep total
= 0 was verified at §37 land).

---

## 5. Pilot result — mixed verdict

Measured (`result.json`, deterministic, seed 1337):

| axis | value | chance | lift |
|---|---|---|---|
| held-out fingerprint bit-accuracy | **0.9626** | 0.5    | +0.46 |
| held-out routing TOP-1            | 0.0000     | 0.0156 | -0.02 |
| held-out routing TOP-3            | **0.5833** | 0.0469 | **+0.54** |
| held-out routing TOP-5            | **0.8333** | 0.0781 | **+0.76** |

**Honest split-verdict (g3)**:

1. **Relations DO generalize to novel anchors** — held-out fingerprint
   bit-accuracy = 0.9626. The model has never seen any of the 12 held-
   out anchors; from physics features alone it predicts ~96% of their
   756-dim relation fingerprint correctly. This MIRRORS §37's 0.9938
   pair-level generalisation, lifted to the fingerprint level.

2. **Strict 1-NN top-1 lookup FAILS** — held-out routing top-1 =
   0/12, slightly below 1/64 uniform chance. A predicted fingerprint
   with ~28 bits wrong out of 756 (~3.7% error) lands closer to a
   neighbouring anchor's fingerprint than to its own (min pair_d² in
   the table = 8, so a few wrong bits collapse the lookup).

3. **Soft top-K routing DOES generalize** — held-out top-3 = 7/12
   (0.58) vs chance 0.047 → **+0.54 lift, an order of magnitude above
   chance**. Top-5 = 10/12 (0.83) vs chance 0.078 → **+0.76 lift**.
   The predicted fingerprint lands in the correct anchor's
   NEIGHBOURHOOD on the landscape — the relation geometry the model
   learned is structurally correct, but the strict-1-NN tie-break is
   too brittle to convert near-correct fingerprints into top-1 hits.

This is **not** "fingerprint hides memorisation" — that would mean
held-out bit-acc collapses to ~0.5 (random). 0.9626 is unambiguously
generalising. The bottleneck is the *decision rule*, not the *relation
function*.

### 5.1 Verdict

**L8_RELATIONS_GENERALIZE_BUT_1NN_TOO_BRITTLE**

§43's strict-1-NN reformulation does not transfer routing top-1 above
chance, so the design's strict hypothesis is FALSIFIED. But the
underlying relation function generalises (held-out bit-acc 0.96,
top-3 lift +0.54). The §37 inter-anchor finding lifts to routing
GEOMETRY but not to strict routing IDENTITY under this decision rule.

L8 closes at design-tier per §13-M/§13-L anti-padding for the strict
1-NN reformulation; the underlying mid-tier finding (relations
generalize at the fingerprint level) is the *honest valuable salvage*
and is preserved verbatim in result.json + this DESIGN.md.

---

## 6. Honest crux — why this is not GOAL movement

1. **§37 generalisation is a low-complexity classifier result.** R1-R4
   are smooth threshold functions of a 9-dim vector. The pilot proves
   the relation FUNCTION composes into fingerprint prediction. It does
   NOT prove that a byte-LM at scale would emit a 756-dim discrete
   fingerprint coherently — the §16/§22 byte-cascade attractor family
   is a separable, harder problem (B-S43-NOTE).

2. **Top-3 lift is geometric, not identity.** Predicting an anchor's
   neighbourhood on the landscape ≠ predicting the anchor. A routing
   token is a strict identifier; the strict-1-NN decision rule
   forecloses on the "near but not exact" cases.

3. **§16 baseline = 21/64 (0.328) on byte-LM surface routing.** Top-1
   here is 0/12 (0.000). Even at the soft-decision level, top-3 0.58
   would not necessarily transfer to a byte-LM, because the byte-LM's
   route token has no "top-3" affordance — it picks one.

4. **§15 milestone unchanged.** GOAL (anima spontaneously emerging
   from its own physics) is unaddressed by this cycle. §43 = a
   routing-mechanism probe; even a strict positive would have been a
   richer routing reformulation, not GOAL movement.

5. **g3 negative-evidence discipline.** This cycle is design-tier
   close + honest mid-tier salvage. The strict top-1 hypothesis is
   FALSIFIED measurably; the mid-tier relation-generalises finding is
   PRESERVED measurably. Both are reported faithfully.

---

## 7. Decision — design-tier close, no large fire

The pilot answered the L8 hypothesis: strict 1-NN reformulation does
not break the §16 routing top-1 ceiling, even when relations clearly
generalize at the fingerprint level. The next plausible move (a soft-
margin learnable-decoder over fingerprints) is a NEW design — distinct
from L8's strict-1-NN — and is not warranted on the current evidence:
the bottleneck (1-NN brittleness) is mechanism-level, not data-regime,
and the GOAL bottleneck remains §1.1 data-regime threshold (§15
milestone).

A byte-LM scale-up cycle on this reformulation is NOT recommended
because:
- the strict-1-NN routing decision is the failing link, not the
  relation function;
- a byte-LM cannot emit a 756-dim one-hot fingerprint coherently
  without itself solving the very byte-cascade memorisation problem
  §16 / §22 already mapped out;
- soft-routing (top-K decoder) would require a new design cycle (not
  L8 strict) and would still be a mechanism-level reformulation, not
  data-regime movement.

**Decision**: design-tier LANDED, $0. B-S43-1..4 4/4 BLUE. Pilot
measured + reported. RESEARCH.md not edited (orchestrator
consolidation). Worktree commit + no push.

---

## 8. Files / artefacts

- `DESIGN_S43.md` — this file
- `fingerprint_builder.py` — closed-form 64×756 fingerprint table +
  Euclidean 1-NN lookup
- `fingerprint_table.json` — serialised table (sha256 committed)
- `fingerprint_table_meta.json` — metadata (sha256, summary)
- `train_s43_pilot.py` — held-out-anchor pilot (small MLP, $0 Mac CPU,
  seed 1337)
- `result.json` — pilot result (bit-acc, top-K routing, verdict,
  per-anchor)
- `blue_falsifier_s43.py` — B-S43-1..4 sidecar
- `blue_falsifier_s43_result.json` — 4/4 BLUE + B-S43-NOTE
- `FINDINGS.md` — short summary + caveats

---

## 9. honest C3 (>= 10)

1. **measured only, $0 Mac CPU pilot. NO GPU. NO byte-LM fire.** Cycle
   value = the L8 reformulation well-formedness (B-S43 4/4 🔵) + the
   honest held-out-anchor probe outcome (mixed verdict). NOT a routing-
   ceiling-broken claim.

2. **substrate is a feature classifier**, not a byte-LM. 13-dim physics
   features → 756-dim one-hot fingerprint. The §16 byte-LM ceiling is
   not the eval domain here. A byte-LM transfer is a separable, harder
   fire (B-S43-NOTE, §6 honest crux).

3. **verdict: L8_RELATIONS_GENERALIZE_BUT_1NN_TOO_BRITTLE**. Held-out
   fingerprint bit-acc 0.9626 (relations DO transfer to novel anchors,
   §37 mirror lifted to fingerprint level). Held-out top-1 routing
   0/12 ~ chance. Held-out top-3 0.58 / top-5 0.83 >> chance.

4. **strict-1-NN is the bottleneck, NOT the relation function.** A few
   wrong bits out of 756 (~4% error) collapse the closest-neighbour
   decision when min pair_d² = 8 (table is dense). The relation
   geometry is right; the strict-identifier readout is wrong.

5. **L8 closes at design-tier per §13-M/§13-L anti-padding** — strict
   reformulation hypothesis FALSIFIED, mid-tier relation-generalises
   finding PRESERVED. No byte-LM fire recommended on this evidence.

6. **§15 milestone unchanged** — GOAL (anima spontaneously emerging
   from own physics) is not touched. L8 is a routing-mechanism probe,
   not a data-regime or emergence intervention.

7. **B-S43 4/4 🔵 is reformulation well-formedness.** Deterministic
   fingerprint table (B-S43-1), 1-NN lookup well-typed (B-S43-2),
   no-external-KG / no-LLM AST audit (B-S43-3), pairwise distinguish-
   able fingerprints (B-S43-4 — identity is recoverable from
   fingerprint in principle). It does NOT prove anima can predict
   fingerprints (that's the pilot result, mixed).

8. **g3 negative-evidence discipline.** The strict top-1 hypothesis is
   FALSIFIED measurably; the mid-tier finding is PRESERVED measurably.
   Both reported faithfully. NO single-number summary substitutes for
   the split verdict.

9. **fingerprint distinguishability is a structural property of the
   §16 anchor SSOT, not a property the model learns.** min pair_d² = 8
   means the §16 anchors are pairwise distinct under R1-R4 — already
   true before any training. The pilot tests whether the model CAN
   predict the right cell of this closed table from a novel anchor's
   physics features; the table itself is given.

10. **honest scale**: 64-anchor 756-dim. At larger anchor sets the
    table grows quadratic-ish (n × (n-1) × 12 bits), and min pair_d²
    behaviour is not guaranteed. A scale-up cycle would need to verify
    distinguishability at the new size (B-S43-4 by construction).

11. **deterministic + reproducible**. relation_corpus.py (§37) +
    fingerprint_builder.py + train_s43_pilot.py are all seed-fixed
    (1337). Anyone can re-run and confirm: fingerprint table sha256,
    held-out anchor split, pilot bit-acc, top-1/3/5 routing.

12. **f1/f2/f3 + B-IDENTITY-5 safe.** No σ/τ/φ/J₂ external derivation.
    No external KG / LLM / paraphraser (B-S43-3 AST audit). No
    helper/assistant/user surface (no corpus generated this cycle;
    §37 SSOT verified). north-star (GOAL.md) unchanged — L8 = routing-
    mechanism probe, not GOAL movement.
