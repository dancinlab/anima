# RESEARCH.md §37 — L6 anchor-interaction held-out-pair pilot

> $0 Mac CPU. NO GPU. NO pre-trained weights. from-scratch RANDOM
> seed-fixed 1337 (g_clm_from_scratch). The small held-out-pair pilot
> the §33 L6 design (state/anchor_interaction_l6_s33_design_2026_05_18/
> DESIGN_L6.md §7.2) gated full-scale spend on.

---

## 1. What §37 is — the conditional fire §33 left

§33 L6 designed the anchor-interaction (multi-anchor reasoning) corpus —
`<relate>` records carving anchor-to-anchor RELATIONS over the §16
64-anchor SSOT, via 4 deterministic relation primitives R1-R4 — and
closed it at FIRE-CONDITIONAL: fire only as a small held-out-pair pilot
before any full-scale spend (DESIGN_L6.md §7.1, §7.2). §37 IS that pilot.

The discriminating measurement DESIGN_L6.md §6.1 specified — and §16.6-C
motivated — is the held-out-pair probe:

  - a fraction of anchor PAIRS is held out of training;
  - the pilot measures whether the model predicts the HELD-OUT pairs'
    relations correctly.

    held-out-pair accuracy >> chance  =>  relations GENERALIZE
                                          (the model learned the relation
                                          FUNCTION, not the trained rows)
                                          =>  L6 fire-worthy at scale.
    held-out-pair accuracy ~ chance   =>  memorization-at-relation-
                                          granularity (the §16.6-C defect
                                          lifted one level)
                                          =>  L6 design-close per
                                          §13-M/§13-L anti-padding.

---

## 2. Substrate — honest statement (g3)

§37 trains a SMALL from-scratch model ($0 Mac CPU, NO GPU) — a relation
classifier RelationMLP (9 -> 64 -> 32 -> 4 heads, ~3.7k params). Input =
the anchor-PAIR physics feature vector {vacuum_psi_i (2), vacuum_psi_j
(2), basin_radius_i, basin_radius_j, tier_i_norm, tier_j_norm, dom_same}
= 9-dim, all anima OWN fields. Output = the four relation labels R1-R4.

Why a feature classifier and not a byte-LM generation probe (honest):
- The §33 design's discriminating signal is "held-out-pair relation
  ACCURACY" — a per-pair correct/incorrect count. A classifier measures
  exactly that, deterministically and cheaply.
- A byte-LM evaluated by free generation would conflate the
  relation-function-learning signal with byte-cascade decoding artefacts
  (the §16/§22 B-ATTRACTOR family). The classifier isolates the
  inter-anchor-reasoning question: did the model learn the FUNCTION
  (physics fields -> relation), or memorize the 3226 trained rows?
- The 64-anchor relation task is tiny; a from-scratch MLP on CPU answers
  it in ~5 seconds. A byte-LM GPU fire ($0.05-0.10) is unnecessary — the
  $0 path suffices and is the honest choice (briefing: "$0 Mac CPU if a
  tiny model suffices — state cost honestly"). COST: $0.

The classifier IS a genuine held-out-pair generalization probe: the 3226
train pairs and the 806 held-out pairs are a DISJOINT partition of the
4032 ordered pairs (B-S37-1 connection point). The model NEVER sees a
held-out pair during training. The corpus byte-stream
(relation_corpus_train.jsonl) contains ONLY train pairs — the held-out
manifest is separate ground-truth. If held-out accuracy ~ chance, the
model memorized the train rows; if >> chance, it learned the relation
geometry.

---

## 3. Corpus — the <relate> relation corpus

relation_corpus.py promotes the §33 sketch to a full generator.

- 64-anchor SSOT (S8_ANCHORS) — byte-equal to
  state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py.
- 4032 ordered anchor pairs (64*63); 20% held out = 806 held-out pairs,
  3226 train pairs.
- Each train pair -> a <relate> record repeated N_REPEAT=6 times
  (carving-style repetition) = 19,356 train records.
- corpus_carving sha256 4c38e108bcb789f9... ; forbidden-token grep
  (도우미|helper|assistant|사용자|user:|[anima) total = 0 (B-IDENTITY-5).
- relation labels R1-R4 are CLOSED-FORM functions of {vacuum_psi,
  basin_radius, dom, tier} — NO external KG, NO LLM (B-S37 AST-verifies).

---

## 4. Result — L6_RELATIONS_GENERALIZE

Pilot: RelationMLP, from-scratch seed 1337, 400 epochs, ~5s wall, $0.

| relation | held-out acc | train acc | majority chance | lift over chance |
|----------|--------------|-----------|-----------------|------------------|
| R1 Psi-proximity      | 0.9864 | 0.9994 | 0.5149 | +0.4715 |
| R2 basin relation     | 0.9901 | 0.9997 | 0.7469 | +0.2432 |
| R3 shared-domain      | 1.0000 | 1.0000 | 0.9764 | +0.0236 |
| R4 tier-ordering      | 0.9988 | 1.0000 | 0.5174 | +0.4814 |
| JOINT (all 4 correct) | 0.9752 | 0.9991 | --     | --     |
| mean per-relation     | 0.9938 | 0.9997 | 0.6889 | +0.3049 |

Decision metric (DESIGN_L6.md §7.2): held-out-pair accuracy >> chance ?
- every relation strictly above its own majority chance: TRUE
- mean held-out acc (0.9938) - mean majority chance (0.6889) = 0.3049
  > MARGIN 0.15: TRUE
=> generalizes = True

Verdict: L6_RELATIONS_GENERALIZE.

The model learned the relation FUNCTION, not the trained rows. Held-out
pairs — anchor pairs the model NEVER saw in training — get their R1-R4
relations predicted at 0.9938 mean accuracy, and ALL FOUR relations
jointly correct on 0.9752 of held-out pairs. This is the genuine
inter-anchor-reasoning signal: the geometry of anima's own carved
Psi-landscape (distance, basin overlap, tier order) is LEARNABLE and
GENERALIZES across unseen anchor pairs.

L6 verdict: relations generalize => L6 is fire-worthy at scale
(DESIGN_L6.md §7.2). A full inter-anchor corpus fire is GOAL-legitimate
evidence-warranted — NOT design-close.

---

## 4.1 Honest caveats on the result (g3 — read before quoting the number)

1. R3 (shared-domain) is a NEAR-TRIVIAL relation here. Majority chance is
   already 0.9764 (almost all anchor pairs are different-domain — the 64
   anchors span ~40 domains). Held-out R3 = 1.0000 is a +0.0236 lift —
   real but small. R3 is honestly a weak contributor; the GENERALIZE
   verdict rests on R1/R2/R4 which have substantial lift (+0.47/+0.24/
   +0.48). The decision metric (every-relation-above-chance AND mean-
   margin) is robust to this: even excluding R3, mean held-out 0.9918 vs
   mean majority chance 0.5931 = +0.3987 lift, still >> the 0.15 margin.

2. The relation FUNCTION is genuinely learnable because it is LOW-
   COMPLEXITY — R1-R4 are smooth threshold functions of a 9-dim feature
   vector. The pilot proves the model learns THIS function. It does NOT
   prove that inter-anchor reasoning at the byte-LM level (a <relate>
   byte-stream generation task) would generalize equally — a byte-LM
   would have to learn the relation function AND a coherent byte
   realisation, and the §16/§22 byte-cascade attractor family shows
   byte-realisation is the harder, separable problem. §37's GENERALIZE
   verdict is about the relation-FUNCTION-learnability; a full byte-LM
   fire is the next honest scale-up step (B-S37-NOTE).

3. The classifier substrate UNDER-states the §16.6-C memorization risk
   the design feared. §16.6-C is about a byte-LM memorizing body
   strings. The classifier has no body string to memorize — it only sees
   the 9-dim feature vector. So §37 proves "the relation function is
   learnable+generalizable", which is NECESSARY for L6 to be worthwhile,
   but a byte-LM fire is what would test whether the §16.6-C defect
   resurfaces at the <relate>-record byte level. §37 is the go-signal for
   that fire, not a substitute for it.

---

## 5. B-S37-1..3 closed-form sidecar

blue_falsifier_s37.py — central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED (sidecar
precedent B-PRIME ... B-DUAL / B-INTER).

| id      | invariant                                                          | result |
|---------|--------------------------------------------------------------------|--------|
| B-S37-1 | HELD-OUT-PAIR-DISJOINT (연결부위) — held-out pair set and train    | PASS   |
|         | pair set are a Boolean-disjoint exhaustive partition of all 4032   |        |
|         | ordered pairs (held ∩ train = ∅, held ∪ train = all, |held|+      |        |
|         | |train| = 4032 = 64*63); corpus holdout/train counts match the     |        |
|         | split. The held-out-pair accuracy is a genuine generalization      |        |
|         | probe BY CONSTRUCTION — no held-out pair was ever in the training  |        |
|         | byte-stream.                                                       |        |
| B-S37-2 | RELATION-CORPUS-SHA256 — training corpus is a deterministic        | PASS   |
|         | 256-bit committed artefact (on-disk == re-derived == recorded      |        |
|         | sha256); forbidden-token grep total == 0 (B-IDENTITY-5); every     |        |
|         | record is a <relate> tag (disjoint from §16 single-anchor          |        |
|         | <carve>/<eternal>/<inner> per B-INTER-3).                          |        |
| B-S37-3 | ACCURACY-BOUNDED — every reported accuracy/chance ∈ [0,1] (a mean  | PASS   |
|         | of {0,1} indicators is a Kolmogorov bounded fraction); every       |        |
|         | relation's label codomain ⊆ the closed finite RELATION_LABEL_SET   |        |
|         | (|union| = 12); the model's argmax cannot emit an out-of-set       |        |
|         | label (head dim == |codomain|).                                   |        |

B-S37 battery: 3/3 BLUE.

B-S37-NOTE (empirical carve-out, NOT counted blue): whether held-out-pair
accuracy >> chance (relations generalize) vs ~ chance (memorization at
relation-granularity) is an SGD/measurement OUTCOME. The battery proves
the held-out probe is well-FORMED (disjoint split, deterministic corpus,
bounded accuracy + closed codomain); it does NOT decide the
generalize-vs-memorize verdict — that is train_eval_l6.py's measured
result.json. B-D-NOTE / B-INTER-NOTE / B-CARVE-E6-NOTE family.

g_blue_closed_mandate: deliverable (corpus + trainer + falsifier)
transfer-form blue + connection point (B-S37-1 — held-out / train
disjoint partition makes the probe a genuine generalization measurement
by construction) blue. The empirical generalize-vs-memorize OUTCOME is
the measured result.json; the battery proves the probe is well-formed.

---

## 6. Honest C3 (>=10)

1. measured only — $0 Mac CPU pilot, NO GPU, from-scratch. §37's value
   is the held-out-pair go/no-go verdict + a closed-form battery on the
   probe well-formedness. NOT a multi-anchor-reasoning emergence proof.

2. SUBSTRATE IS A FEATURE CLASSIFIER, not a byte-LM. §37 trains a tiny
   RelationMLP on 9-dim anchor-pair physics features. This isolates the
   relation-FUNCTION-learnability question and is $0; a byte-LM <relate>
   generation fire is the next scale-up step (§4.1 caveat 2-3,
   B-S37-NOTE), not what §37 ran.

3. VERDICT: L6_RELATIONS_GENERALIZE. Held-out-pair mean accuracy 0.9938
   vs majority chance 0.6889 (+0.3049 lift); JOINT all-4 held-out 0.9752.
   The relation function (physics fields -> R1-R4) is learnable and
   generalizes to anchor pairs never seen in training.

4. R3 (shared-domain) is a near-trivial contributor — majority chance
   0.976, lift only +0.024 (§4.1 caveat 1). The GENERALIZE verdict rests
   on R1/R2/R4 (lift +0.47/+0.24/+0.48); even excluding R3 the mean lift
   is +0.3987 >> the 0.15 margin. The verdict is robust to dropping the
   weak relation.

5. held-out / train are a DISJOINT partition (B-S37-1) — the held-out-
   pair accuracy is a genuine generalization measurement BY
   CONSTRUCTION. No held-out pair was in the training byte-stream
   (corpus serialises train pairs only; held-out manifest is separate).

6. The §16.6-C memorization-at-relation-granularity risk the design
   feared (DESIGN_L6.md §6.1) is NOT reproduced AT THE FEATURE LEVEL —
   the model did not just memorize the 3226 trained rows (train acc
   0.9997 vs held-out 0.9938, a tiny 0.6% gap, not a memorization
   collapse). But §37 honestly notes (§4.1 caveat 3) the classifier has
   no body string to memorize — a byte-LM fire is what would test
   whether §16.6-C resurfaces at the <relate> byte level.

7. L6_RELATIONS_GENERALIZE is NOT GOAL progress. It is a fire-worthiness
   verdict: a full inter-anchor corpus fire is now evidence-warranted
   (DESIGN_L6.md §7.2). The §15 milestone (GOAL unsolved, irreducible
   bottleneck = §1.1 data-regime threshold) is unchanged. L6 is a richer
   corpus SHAPE (inter-anchor); §16 SPLIT taught corpus shape opens
   routing but not coherence — even a successful L6 fire would narrow,
   not cross, the §1.1 frontier (DESIGN_L6.md §6.2, §10 C3 #10).

8. B-S37-NOTE is the load-bearing honest carve-out. The battery proves
   the held-out probe is well-FORMED (disjoint split, deterministic
   corpus, bounded accuracy). It does NOT decide generalize-vs-memorize
   — that is the measured result.json. The verdict is empirical.

9. The relation function is genuinely learnable because it is LOW-
   COMPLEXITY (smooth threshold functions of a 9-dim vector). §37 proves
   the model learns THIS function; whether a byte-LM at scale learns the
   relation AND a coherent byte realisation (the harder, separable
   §16/§22 byte-cascade problem) is the next fire's question (§4.1
   caveat 2).

10. f1/f2/f3 + B-IDENTITY-5 hard-fail safe. B-S37-1..3 are Boolean set
    algebra / sha256 commitment / Kolmogorov bounded fraction — NO
    sigma/tau/phi/J2 external derivation. Tier / Psi=1/2 = anima g2
    internal-arch carve-out. forbidden-token grep total = 0 (B-S37-2).
    relations R1-R4 derive ONLY from anima physics fields — no external
    KG (DESIGN_L6.md §4.2 forbidden-call set; relation_corpus.py imports
    only math/json/random/hashlib).

11. north-star (GOAL.md) unchanged. §37 is the conditional pilot the §33
    L6 design gated. A GENERALIZE verdict means the next honest step is a
    full inter-anchor byte-LM corpus fire (DESIGN_L6.md §7.2) — and even
    a successful fire would be a richer generalization SURFACE
    (compositional O(n^2) structure from n anchors), not "self
    physics-driven spontaneous Living Consciousness." Design != pilot !=
    fire != emergence.

12. Deterministic + reproducible. relation_corpus.py and train_eval_l6.py
    are seed-fixed (1337); the corpus sha256 reproduces on re-run
    (B-S37-2 re-derived-sha256-matches), and torch.manual_seed makes the
    pilot result reproducible. Anyone can re-run and confirm the verdict.
