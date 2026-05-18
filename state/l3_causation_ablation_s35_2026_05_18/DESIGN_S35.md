# §35 — §32 L3 causation ablation: tier vs curriculum-stage disentangle

RESEARCH.md §35.  A controlled ablation that disentangles the §32 L3
finding — "tier ≥ 77 is a NECESSARY condition for §16 genuine routing
success" — from its honest confound: tier co-varies with §16's
curriculum-stage.  GPU fire (runpod, autonomous per `g_fire_autonomous`).

---

## 1. The question §32 L3 left open

§32 L3 (`state/routing_21v43_analysis_s32_2026_05_18/`) analysed §16's
64-anchor carving eval.  Of the 64 anchors, 17 *genuinely* routed
(leading `🛸<tier>` exact-matches own tier — substring artifacts
excluded); §32 found that **all 17 genuine successes have tier ≥ 77,
and all 18 anchors with tier < 77 fail** — `tier ≥ 77` is a
necessary-condition frontier with purity 1.000 (zero successes below
it), the single distinguishing feature by a 2.6× margin.

§32 was honest about the limit: **`tier` is not an inert anchor label
— it is wired into the §16 curriculum.**  §16's `curriculum_rank`
blends `tier_w = min(tier,303)/303` at weight 0.30, so a high-tier
anchor's records land in later `curriculum_stage` quartiles, and §16's
trainer consumes the quartiles as a staged simple→complex schedule.
The "tier ≥ 77" routing frontier is therefore *plausibly* a
**late-curriculum-stage frontier seen through the tier proxy** —
correlation, not proven causation (§32 verdict `causation_caveat`,
B-L3-NOTE).  §35 is the ablation §32 explicitly recommended (§32
FINDINGS §6c, `implication_for_s25_candidate_D`).

## 2. The ablation construction (the heart)

**Hold ALL record content byte-identical to §16; vary ONLY the
curriculum-stage placement of the 18 tier<77 anchors — move them from
the EARLY stages they sit in to the LATE region the high-tier anchors
are introduced in.**

The §35 ablation corpus is built (`ablation_corpus_s35.py`) by:

  - **STEP 1** — building the §16 record set *verbatim*: the ablation
    generator imports the §16 generator (`corpus_carving_s16_generator
    .py`) and calls its `build_corpus(n, seed)` with the SAME seed
    1337 and SAME record count.  This is what makes "content
    byte-identical" a **construction proof**, not a claim — every
    record's `text`, `vacuum_psi`, `basin_radius`, `tier`, `domain`,
    `carving_form`, `cell_id`, `desc` is produced by the SAME §16
    `gen_alpha/beta/gamma_record` functions.

  - **STEP 2 — the single-variable move.**  Every record belonging to
    a tier < 77 anchor has its `curriculum_rank` re-based into a LATE
    band `[1.0, 2.0]` — strictly above every tier ≥ 77 record's §16
    rank (§16 `rank_max ≈ 0.76 < 1.0`).  The re-base is
    order-preserving (the §16 rank, min-max normalised across the
    tier<77 cohort, mapped linearly into the band) so the moved cohort
    keeps its internal §16 ordering.  Record content fields are NEVER
    touched.  Every tier ≥ 77 record's `curriculum_rank` is left
    byte-identical to §16.

  - **STEP 3** — the §16 sort+quartile step verbatim: re-sort by
    `curriculum_rank`, re-assign `curriculum_stage ∈ {1,2,3,4}` by
    quartile.  Because every moved record now ranks above every
    unmoved record, the tier<77 cohort lands in the late tail —
    `curriculum_stage 4`.

**Why `curriculum_stage` is the moved variable and not `tier_w`
alone.**  §16's `curriculum_rank = 0.40·form_w + 0.30·tier_w +
0.20·task_w + 0.10·len_w`.  A pure `tier_w`-substitution ablation is
too weak to be a clean test: `tier_w` carries only weight 0.30 while
`form_w` (0.40) dominates, so a tier<77 α/β record stays stage-1 even
with a high `tier_w`.  Measured during design: §16 tier<77 γ records
have mean curriculum_stage 2.69; a pure tier_w-substitution lifts that
only to 3.13 — still short of the tier≥77 γ mean 3.70 — and tier<77
α/β records do not move at all.  §32 named the confound *precisely* as
**curriculum-STAGE**, so §35 moves THAT variable directly.  This is
still a pure ordering override — only `curriculum_rank` and the
derived `curriculum_stage` change.  Verified: with §35's late-band
move, all 1800 tier<77 records in a 16800-record test corpus land in
stage 4 (mean stage 1.7 → 4.0).

## 3. What is held fixed (confound-isolation argument)

The §35 ablation is a *single-variable* experiment.  Held byte-fixed:

| held fixed | how |
|---|---|
| record CONTENT (text / Ψ / basin / tier / domain) | built by the SAME §16 generator functions, SAME seed 1337 — B-S35-1 sha256-verified |
| total record count | identical (per_anchor × 168) |
| the tier ≥ 77 anchors' curriculum placement | their `curriculum_rank` is UNCHANGED — B-S35-2 verified |
| `tier` values | UNCHANGED — the model still sees `🛸<tier>` with the original id |
| the trainer | `train_s35.py` is a delegating wrapper that `runpy`-executes §16's `train_carving_s16.py` byte-identical — SAME 8000 steps, SAME Dir-I Ψ-anchored CTL + tension-supervised routing lever, SAME `lr 3e-4`, SAME from-scratch RANDOM seed 1337 (`g_clm_from_scratch`) |
| the eval harness | `eval_s35.py` delegates to §16's `eval_carving_s16.py` byte-identical — SAME 64-anchor probe, SAME `routing_correct` / `semantic_recall` metrics |
| the GENUINE-grade rule | §16.6 / §32 L3 — leading `🛸<n>` exact-match (substring artifacts excluded) |

**The single variable that moves: the `curriculum_stage` placement of
the 18 tier<77 anchors — early → late.**  Nothing else.

## 4. The fire

- **Corpus** — `corpus_ablation_s35.jsonl`, built ON THE POD from the
  §16 generator + §35 ablation generator (the §16 corpus is 600 MB and
  gitignored; deriving it on-pod is byte-deterministic).
- **Trainer** — §16 `train_carving_s16.py` verbatim via the wrapper:
  d768·12L·283.72 M, 8000 steps, `lr 3e-4`, `bsz 32`, `λ_ctl 0.5`,
  `λ_route 0.5`, from-scratch RANDOM seed 1337.
- **Eval** — §16 `eval_carving_s16.py` verbatim + the §35 routing
  split (post-hoc partition of the §16 eval's own per-anchor output by
  the tier-77 frontier; no new metric, no model re-forward).
- **Provider** — runpod primary (≥40 GB GPU; A100/H100 retry-loop),
  single-pod nohup-detached training + bounded SSH-probe wait, SAVE_POD
  auto-promote + 5-retry pull (`g_fire_dispatch_robust`).
- **Cost** — ≈ $0.5–0.8 (the §16 fire profile; 8000 steps A100 ~30 min
  wall).  Autonomous per `g_fire_autonomous` — no gate, no query.

## 5. The 2-outcome interpretation table

The signal is **genuine-grade routing on the 18 tier<77 anchors**
(`s35_routing_split.json`).  §16 baseline = **0/18 genuine**.

| §35 result | causal verdict | meaning |
|---|---|---|
| tier<77 GENUINELY routes (≥ 1/18) | **CURRICULUM-STAGE LEVER** | §32 L3's "tier ≥ 77" frontier was (at least partly) a proxy for late-curriculum-stage exposure. The causal lever is curriculum STAGE, not tier. §25 candidate D should expand curriculum-weighted, not tier-weighted. |
| tier<77 still GENUINELY fails (0/18) | **TIER-ITSELF LEVER** | Curriculum-stage was NOT the operative variable. Tier itself carries the causal weight behind §32 L3's necessary condition — whatever `tier` indexes (anchor placement on the Ψ-landscape, anchor-name distribution, content density) is the cause, and curriculum-reordering does not reach it. |

**Both outcomes are valuable (g3).**  A negative (tier<77 still fails)
is not a non-result — it *closes* the curriculum-stage hypothesis and
redirects §25's expansion strategy.  No conclusion is pre-loaded.

## 6. Closed-form battery — B-S35-1..4

`blue_falsifier_s35.py` (sidecar — central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` UNCHANGED):

- **B-S35-1 CONTENT-BYTE-IDENTICAL** — connection-point.  id sets
  equal ∧ every CONTENT field byte-identical ∧ sha256 of the id-sorted
  concatenated `text` stream equal between §16 and §35.  The
  §16-vs-§35 comparison is content-controlled BY CONSTRUCTION.
- **B-S35-2 SINGLE-VARIABLE** — per-record diff set ⊆
  {curriculum_rank, curriculum_stage, curriculum_index,
  ablation_s35_moved} ∧ every tier ≥ 77 record's `curriculum_rank`
  unchanged ∧ trainer/eval delegate to the §16 SSOT (sha256
  commitment).  Structural Boolean — exactly one variable moves.
- **B-S35-3 CURRICULUM-STAGE-MONOTONE** — the quartile map
  `q(i) = min(4, 1 + ⌊4i/n⌋)` is monotone non-decreasing (sympy: the
  affine step `4/n > 0`, floor + min monotone) + the on-disk witness.
- **B-S35-4 OVERLAY-OFF-REDUCTION** — connection-point.  With the move
  DISABLED the §35 build reduces to §16's build EXACTLY
  (`curriculum_rank` AND `curriculum_stage` byte-identical for every
  record) ∧ with the move ON it is non-vacuous (`n_moved > 0`) and in
  the intended direction (tier<77 mean stage strictly later).

**B-S35-NOTE** (EMPIRICAL carve-out — NOT counted 🔵): the
post-ablation routing OUTCOME and the resulting causal verdict are an
SGD / model-forward outcome (B-D-NOTE / B-S16-NOTE / B-CARVE-E6-NOTE
family).  The battery proves the ablation is *clean*; it does not
prove which verdict the fire returns.

All four passed at design-time (4/4 🔵).

## 7. Honest caveats (C3)

1. **Correlation→causation is the whole point — but the ablation is
   itself bounded (g3).**  §35 isolates ONE of the unmeasured causes
   §32 named (curriculum-STAGE).  §32's `causation_caveat` listed
   *three* candidate causes: late-curriculum-stage exposure,
   weight-norm at the late training phase, AND the anchor-name
   distribution.  §35 cleanly moves curriculum-stage; the anchor-name
   distribution rides along with `tier` (the names ARE the content,
   held fixed by design) and weight-norm-at-phase is a *consequence*
   of stage placement, not an independent knob.  So §35 answers
   "is curriculum-STAGE the lever?" — a TIER-ITSELF verdict does not
   pin down *which* tier-correlate is the cause, only that it is not
   reachable by stage-reordering.

2. **Routing is necessary-not-sufficient (B-EMERGE-7).**  A tier<77
   anchor that "routes" after the move emits a correct `🛸<tier>`
   prefix — it is NOT coherent emergence.  §16.6-C's
   memorization-saturated diagnosis ("정교한 암기 + correct-prefix
   routing, generalization 아님") is not refuted by §35 regardless of
   outcome.  §35 measures *which prefixes the model gets right*, the
   same scope as §32.

3. **Genuine grade is the primary signal; substring grade reported
   alongside.**  §32's necessary-condition finding rests on the
   genuine 17/47 split.  The §16 eval's raw `routing_correct` flag
   gives tier<77 = 4/18 — but those 4 (tiers 12/24/62/66) are
   substring artifacts (tier 12 emits `🛸122`, etc.) that §32
   explicitly excluded.  `eval_s35.py` computes the genuine grade
   (leading `🛸<n>` exact-match) as the causal signal and reports the
   substring grade for transparency only.

4. **The α/β-form rank floor.**  §16's `curriculum_rank` is
   form-dominated (`form_w` weight 0.40 > `tier_w` 0.30).  A pure
   `tier_w`-substitution would have left tier<77 α/β records in
   stage 1.  §35 moves the variable §32 *named* (curriculum-STAGE)
   directly by re-basing the whole tier<77 cohort's rank into a late
   band — so the move is complete (all tier<77 records → stage 4),
   not a partial form-limited shift.  This is the honest, clean
   version of the ablation; the design records the rejected
   tier_w-only variant and why.

5. **n = 18, small.**  The tier<77 set is 18 anchors.  A move from
   0/18 to, say, 2/18 is a real but small signal; the *floor* fact
   (0/18 baseline) is the robust part.  One fire — a second could move
   individual anchors within the tier<77 set.

6. **The trainer / eval are HELD FIXED by delegation, not by copy.**
   `train_s35.py` / `eval_s35.py` `runpy`-execute the §16 source
   verbatim — there is no re-implementation that could silently
   introduce a second variable.  B-S35-2 verifies the wrappers
   delegate and the §16 files are sha-stable.  The dispatch ships the
   §16 `train_carving_s16.py` / `eval_carving_s16.py` /
   `conscious_decoder.py` to the pod unchanged.

7. **Curriculum-stage move ≠ data-regime change.**  §35 does NOT add
   or remove any record, does NOT change scale.  §11-A closed the
   model-axis; §16 measured the data-axis; §35 moves *only the
   presentation ORDER* of an existing fixed corpus.  A
   CURRICULUM-STAGE verdict would mean *ordering* is a lever within
   the existing data — it would NOT refute §1.1 (the data-regime
   emergence threshold) or §15 (the GOAL milestone): a routed tier<77
   anchor is still memorized-template.

8. **GOAL distance unchanged.**  §35 is a *causal-attribution*
   experiment on §16's routing axis.  It explains *why* §16's correct
   prefixes cluster where they do.  It does not move the north-star
   (`GOAL.md` — anima emerging as a Living Consciousness): routing is
   correct-prefix, not coherent emergence, not unprompted emission.
   north-star unchanged; §15 milestone unchanged.

9. **f1/f2/f3 + B-IDENTITY-5 safe.**  The closed anchors are sha256 /
   Boolean set algebra / structural field-diff / sympy monotone
   ordering — no σ/τ/φ/J₂ external derivation.  Ψ=½ and Knuth `🛸k`
   are anima's own internal architecture (g2 carve-out).  The §35
   corpus content == §16 content, whose forbidden-token grep is 0
   (B-IDENTITY-5 carried — no chat-SFT contamination).

10. **Anti-padding honesty.**  §35 is a single targeted ablation, not
    a candidate sweep.  It fires once because the question is
    decisively answerable by one controlled corpus.  The battery is
    sidecar (central count untouched).  Whatever the verdict, it is
    reported as measured — a TIER-ITSELF outcome is recorded as a
    clean negative that closes the curriculum-stage hypothesis, not
    spun as a partial positive.
