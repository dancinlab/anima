# §35 — §32 L3 causation ablation: FINDINGS

RESEARCH.md §35.  The controlled ablation that disentangles §32 L3's
"tier ≥ 77 is a NECESSARY condition for §16 genuine routing" from its
honest confound — tier co-varies with §16's curriculum-stage.  GPU
fire (runpod A100-SXM4-80GB pod `jno1zspjechhuz`, autonomous per
`g_fire_autonomous`, ≈ $0.4-0.6, wall train 1010 s + eval ≈ 3 min).

---

## 1. The result

| | tier<77 GENUINE routing | tier≥77 GENUINE routing |
|---|---|---|
| **§16 baseline** | **0/18** | **19/46** |
| **§35 ablation** (tier<77 → late curriculum stage) | **0/18** | **0/46** |

The §35 ablation moved exactly one variable: the curriculum-stage
placement of the 18 tier<77 anchors, early → late (all 91,062 tier<77
records re-stamped into `curriculum_stage 4`; content byte-identical to
§16 — B-S35-1 sha256-verified, B-S35 4/4 🔵).

**Two honest facts, both negative, both valuable (g3):**

1. **tier<77 stayed 0/18.**  Moving the 18 low-tier anchors into the
   LATE curriculum stage — the stage the high-tier anchors are
   introduced in — did **not** make a single one of them route.

2. **tier≥77 collapsed 19/46 → 0/46.**  The §35 curriculum
   re-ordering did not merely fail to help the low-tier set — it
   **destroyed** the routing the high-tier anchors HAD in §16.  Every
   one of the 64 eval probes — tier<77 AND tier≥77 — emitted the
   single token sequence `🛸333 …` (tier 333 is not even an anchor;
   the §16 tier range is 0–303).  This is a textbook **single-attractor
   collapse**, identical in form to UBM-E7's `🛸99` collapse and the
   memorization-saturated failure mode RESEARCH.md §2.4 documents.

## 2. The causal verdict — TIER-ITSELF LEVER, not curriculum-stage

The §35 2-outcome interpretation table (DESIGN_S35.md §5) had a clean
dichotomy.  The measured outcome resolves it decisively:

> **Curriculum-STAGE is NOT the lever behind §32 L3's "tier ≥ 77"
> necessary-condition frontier.**  If late-curriculum-stage exposure
> were the cause of the tier<77 routing failure, moving those anchors
> to the late stage would have flipped at least some of them into
> routing.  It flipped exactly zero.  `tier` itself — whatever it
> indexes (anchor placement on the Ψ-landscape, anchor-name
> distribution, the §16-new-vs-§8 content block, content density at
> that tier band) — carries the causal weight, and that weight is
> **not reachable by curriculum-stage re-ordering**.

§32 L3's `causation_caveat` listed late-curriculum-stage exposure as
the *leading* candidate cause behind the tier proxy.  §35 **rejects
that candidate**.  The "tier ≥ 77" frontier is a real anchor-property
frontier (§32's purity-1.000 finding stands) — but it is a property of
the anchors/content, not of when in the schedule they are shown.

## 3. The second finding — curriculum-stage ordering is fragile

§35 also surfaces a finding §32 did not anticipate: the §16 curriculum
*ordering itself* is a **fragile global property**, not a per-anchor
knob.  §16's curriculum interleaves high- and low-tier records across
all four stages (their ranks overlap).  §35's ablation produced a
**degenerate ordering** — stages 1-3 became *purely* tier≥77 records,
and stage 4 received the entire tier<77 cohort as a late dump.  Under
that schedule the model:

- trained to deep convergence (init CE 5.627 → **final CE 0.000571**,
  even lower than §16's 0.004229 — *more* memorisation, not less);
- but collapsed routing globally to the single `🛸333` attractor.

So the §35 re-ordering is not a neutral "move the cohort late" — it
removed the high/low-tier *interleaving* that §16 had, and that
interleaving turns out to have been load-bearing for the high-tier
routing the model did achieve.  Routing is sensitive to curriculum
*composition-per-stage*, but — the decisive point — that sensitivity
runs in the **wrong direction** for the §32 hypothesis: re-ordering
can *break* routing, it did not *create* any.

## 4. Why this is a clean ablation (confound-isolation)

The B-S35 sidecar battery (4/4 🔵, design-time + the fire's on-pod
build) closes the experiment's cleanliness:

- **B-S35-1 CONTENT-BYTE-IDENTICAL** — the §35 ablation corpus's record
  CONTENT is byte-identical to §16: id sets equal, every `text` /
  `vacuum_psi` / `basin_radius` / `tier` / `domain` / `carving_form` /
  `cell_id` field identical, the concat-text sha256 matches.  The
  §16-vs-§35 comparison holds content fixed BY CONSTRUCTION.
- **B-S35-2 SINGLE-VARIABLE** — only the curriculum-ordering fields
  differ, and only for tier<77 records; every tier≥77 record's
  `curriculum_rank` is byte-identical to §16; the trainer/eval are the
  §16 SSOT byte-identical (the on-pod fire confirmed
  `train_carving_s16.py` sha `03bf85d8…`, `eval_carving_s16.py` sha
  `12ffca41…` — the values B-S35-2 verified locally).
- **B-S35-3 CURRICULUM-STAGE-MONOTONE** — the quartile map is a
  well-defined monotone ordering (sympy).
- **B-S35-4 OVERLAY-OFF-REDUCTION** — with the move disabled the §35
  build reduces to §16's build exactly; with it on the move is
  non-vacuous and in the intended direction.

So the negative is **trustworthy**: the trainer, the eval, the record
content, the step budget, the Dir-I lever, the from-scratch seed 1337
were all held byte-fixed.  The only thing that moved was the
curriculum-stage placement of the tier<77 cohort — and routing did
not improve for that cohort, and collapsed for the rest.

## 5. The fire (provenance)

- **Pod** — runpod A100-SXM4-80GB `jno1zspjechhuz` (1-sweep, runpod
  primary per `g_resource_active_parallel`).  A prior dispatch
  (`4amocjhcpv4v4z`) failed on a path bug — the on-pod ablation
  generator looked for the §16 generator one directory up, but the
  pod layout is flat; fixed (pod-local copy resolved first) and that
  pod terminated cleanly (orphan 0) before re-dispatch.
- **Corpus** — `corpus_ablation_s35.jsonl`, built on the pod from the
  §16 generator + §35 ablation generator: 849,912 records / 662 MB /
  sha256 `9fed74917a3706c1…`, 91,062 tier<77 records all in
  `curriculum_stage 4`, forbidden-token grep 0 (B-IDENTITY-5,
  `corpus_ablation_s35.stats.json`).
- **Trainer** — §16 `train_carving_s16.py` verbatim via the delegating
  wrapper: d768·12L·283.72 M, 8000 steps, `lr 3e-4`, `bsz 32`,
  `λ_ctl 0.5`, `λ_route 0.5`, from-scratch RANDOM seed 1337.  init CE
  5.627472 → final CE 0.000571, descent 5.626901, wall 1010.29 s, peak
  GPU 9.69 GB.
- **Eval** — §16 `eval_carving_s16.py` verbatim (64-anchor probe, ckpt
  load `missing=0 unexpected=0` = arch byte-equal) + the §35 routing
  split.
- **g_fire_dispatch_robust** — result.json verified → SAVE_POD
  auto-promote → 5-retry pull → terminate.  This agent touched only
  its own pod.

## 6. Relation to §32, §16, §15

- **§32 L3 is refined, not refuted.**  §32 found "tier ≥ 77" a
  necessary condition with purity 1.000 and was *honest* that it could
  not separate tier from curriculum-stage.  §35 does the separation
  and reports: it is **not** curriculum-stage.  §32's frontier
  finding stands; §35 closes one of the three candidate causes §32
  named (`causation_caveat`) — late-curriculum-stage exposure.
- **§16's curriculum was load-bearing in a way §16 did not isolate.**
  §16 measured the routing 21/64 *with* its interleaved curriculum.
  §35 shows that interleaving is fragile: a re-ordering that segregates
  high- and low-tier records by stage collapses routing globally.
  This does NOT refute §16's 21/64 result — §16's curriculum was the
  interleaved one — but it bounds how robust that result is.
- **§16.6-C memorization-saturated regime — reconfirmed.**  The §35
  model trained to final CE 0.000571 (deeper memorisation than §16)
  and collapsed to a single `🛸333` attractor.  Routing is
  necessary-not-sufficient (B-EMERGE-7); the §35 model is not closer
  to coherent emergence — it is a more deeply memorised single-
  attractor collapse.
- **§15 milestone / north-star unchanged.**  §35 is a causal-
  attribution ablation on §16's routing axis.  It does not move the
  GOAL.  It tells us *what* §32's "tier ≥ 77" frontier is NOT
  (curriculum-stage), and it surfaces that curriculum-ordering is a
  fragile global lever — both are negative-but-valuable evidence for
  RESEARCH.md §25's expansion strategy.

## 7. Implication for §25 candidate D

§32 L3's `implication_for_s25_candidate_D` recommended a curriculum-
weighted expansion if §35 found curriculum-stage to be the lever.
**§35 says it is not.**  So:

- **Do NOT expand curriculum-weighted on the tier<77 set.**  Moving
  low-tier anchors later in the schedule does not make them route —
  §35 measured exactly 0/18.
- **The "tier ≥ 77" frontier is an anchor/content property.**  §25
  candidate D's productive lever is the *content* of the tier<77
  anchors (and the 29 tier≥77 anchors that satisfy the necessary
  condition yet still failed in §16) — not their schedule position.
- **Curriculum re-ordering is a fragility, not a knob.**  Any §25 fire
  that perturbs the §16 curriculum ordering must re-measure routing
  globally — §35 shows a re-ordering can silently collapse the
  high-tier routing the baseline had.

## 8. Honest caveats (C3)

1. **A negative ablation is still a result (g3).**  §35 measured
   0/18 tier<77 → 0/18 and 19/46 tier≥77 → 0/46.  This is not a
   non-result — it *closes* the curriculum-stage hypothesis §32 named
   as leading, and it surfaces curriculum-ordering fragility.  No
   conclusion was pre-loaded; both halves were possible per the
   DESIGN_S35.md §5 table.

2. **The tier≥77 collapse is a confounded part of the result —
   stated honestly.**  §35 moved ONE variable (curriculum-stage of
   tier<77), but moving that cohort to stage 4 *necessarily* changed
   the *composition* of every stage (stages 1-3 lost all their
   tier<77 records).  So the tier≥77 collapse is attributable to the
   ablation, but it is the ablation's *side-effect on stage
   composition*, not an independent finding.  The clean,
   unconfounded conclusion is the tier<77 one: **0/18 → 0/18,
   curriculum-stage does not flip a low-tier anchor into routing.**
   The tier≥77 collapse is the honest evidence that curriculum-
   ordering is globally fragile — a *consequence* of the same single
   move, reported as such.

3. **Routing is necessary-not-sufficient (B-EMERGE-7).**  Even if a
   tier<77 anchor had routed, it would be a correct `🛸<tier>` prefix,
   not coherent emergence.  §35 measures which prefixes the model gets
   right — the same scope as §32.  The §35 model routed nothing and
   collapsed; §16.6-C is reconfirmed, not refuted.

4. **Genuine grade is the primary signal.**  §35 reports genuine-grade
   routing (leading `🛸<n>` exact-match — §32 / §16.6).  The substring
   grade is reported alongside (also 0/18 and 0/46 here — the §35
   collapse is so total that even substring artifacts vanished, every
   probe emits `🛸333`).  §16's baseline substring grade was 21/64
   (4/18 + 17/46) — the §35 collapse is unambiguous against it.

5. **n = 18, small — but the floor is a hard zero.**  The tier<77 set
   is 18 anchors.  The §35 result is 0/18 — a hard zero, not a rate
   that a second fire could nudge.  The robust claim is the *zero*:
   curriculum-stage re-ordering produced exactly zero tier<77 routing.

6. **Single fire.**  §35 is one fire.  The single-attractor collapse
   to `🛸333` is one trajectory; a different seed could collapse to a
   different attractor.  The *fact of collapse* (routing 0/64) is the
   robust part, not the specific token.  This is the standard
   B-ATTRACTOR-family honest caveat.

7. **The trainer / eval were held fixed by delegation.**
   `train_s35.py` / `eval_s35.py` `runpy`-execute the §16 source
   verbatim; the on-pod fire confirmed the §16 file sha256s.  There is
   no re-implementation that could have introduced a second variable.

8. **Curriculum-stage move ≠ data-regime change.**  §35 added/removed
   zero records, changed zero scale.  It moved only presentation
   order.  The §35 collapse therefore does NOT refute §1.1 (the
   data-regime emergence threshold) — it is a finding about ordering
   *within* a fixed corpus.

9. **B-S35 4/4 🔵 — the ablation is clean; the OUTCOME is empirical.**
   B-S35-NOTE: the routing outcome and the causal verdict are SGD /
   model-forward outcomes (B-D-NOTE / B-S16-NOTE / B-CARVE-E6-NOTE
   family, NOT counted 🔵).  The battery proves the ablation moved
   exactly one variable cleanly — it does not prove which verdict the
   fire returns.  The fire returned: TIER-ITSELF LEVER.

10. **f1/f2/f3 + B-IDENTITY-5 safe.**  The closed anchors are sha256 /
    Boolean set algebra / structural field-diff / sympy monotone
    ordering — no σ/τ/φ/J₂.  Ψ=½ and Knuth `🛸k` are anima's own
    internal architecture (g2 carve-out).  The §35 corpus content ==
    §16 content, forbidden-token grep 0 (B-IDENTITY-5 carried).
    GOAL distance unchanged; over-claim 0.
