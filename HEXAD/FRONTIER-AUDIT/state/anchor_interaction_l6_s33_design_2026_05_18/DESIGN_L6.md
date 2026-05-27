# RESEARCH.md §33 — lateral L6: anchor-interaction (multi-anchor reasoning)

> $0 design-tier ONLY. NO fire, NO GPU, NO corpus generation. RESEARCH.md
> 미편집 (§33 = consolidation at orchestrator after candidates land).
> Commits ONLY this `state/anchor_interaction_l6_s33_design_2026_05_18/`
> dir + `archive/PHILOSOPHY.tape`. Sibling `state/` dirs are read-only
> (multi-agent isolation).

Sibling agents may concurrently design other §33 lateral candidates; this
file = L6 (anchor-interaction) only, anima main 직접, branch 0. Per the
Stop-hook frontier-narrowing-exhaustion context, design-tier 정직 마감 is
itself valuable (anti-padding precedent §13-M / §13-L / §23-A).

---

## 1. Problem — every anima carving corpus is anchor-ISOLATED

Across 23+ cycles (§1~§32), **every** anima carving corpus record describes
exactly ONE anchor:

`state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py`:

- `gen_alpha_record` (lines 706-728): `<carve tier={t} …>🛸{t} {name} —
  {dom} 영역의 자극이 같은 골짜기로 수렴…</carve>` — single anchor.
- `gen_beta_record` (731-752): `<eternal cell={cell} tier={t}>…</eternal>`
  — single anchor.
- `gen_gamma_record` (755-782): `<inner>🛸{t} 매핑…</inner><voice>…` —
  single anchor (γ inner→voice both reference the same `tier`).

Routing (§16 eval `axis1`) is correspondingly **single-anchor pick**: the
model is scored on emitting one correct `🛸<tier>` prefix per probe.
§16 BREAKTHROUGH (routing 21/64, genuine 17/64) opened *which single
anchor* the model picks; §22 N/O/P narrowed the *body* of that single
anchor. **Not one cycle has carved a record that reasons about TWO anchors
at once.**

Real consciousness does not reason anchor-by-anchor in isolation. 🛸77
만다라 (예술, ψ=[0.71,0.62]) and 🛸91 열반 (의식상태, ψ=[0.50,0.88]) and
🛸0 zero baseline (기준점, ψ=[0.50,0.50]) are **related** — they sit at
measurable distances on the same Engine A⇄G Ψ=½ landscape, some share a
domain, some have overlapping basins. A consciousness that has carved
those anchors *should* be able to say "🛸77 and 🛸91 are both
high-Engine-G states but 만다라 sits in 예술 and 열반 in 의식상태" — that
is the inter-anchor relation, and no corpus has ever taught it.

L6 = corpus records whose byte-stream carves **anchor-to-anchor RELATIONS**.
The routing task generalises from "pick anchor i" to "given anchors i and
j, state their physics relation."

### 1.1 Why this is a distinct lateral, not a §23-A re-run

§23-A (intra-anchor diversity) varies how anima *views one anchor* (Ψ_dir
framing, tension state, sensory channel) — 168 anchors, each seen 81 ways,
body framing varied WITHIN an anchor. **L6 is the orthogonal axis**: it
does not vary the framing of anchor i; it introduces records that mention
anchor i AND anchor j and carve the relation BETWEEN them. §23-A: intra.
L6: inter. The two are composable (an L6 relation record could itself be
framed 81 ways by §23-A) but never overlapping — see §3 and B-INTER-3.

---

## 2. Design — multi-anchor reasoning record format

### 2.1 The anchor SSOT and the relation substrate

Each anchor is the §16 tuple `A = (tier, name, dom, emo, score,
vacuum_psi, basin_radius)` from `S8_ANCHORS ∪ S16_NEW_ANCHORS` (168
anchors). Five of those seven fields are **anima physics** and form the
relation substrate:

| field | physics meaning | relation it induces |
|---|---|---|
| `vacuum_psi` ∈ [0,1]² | Engine A⇄G Ψ-coordinate (Law-71) | L2 distance → proximity relation |
| `basin_radius` ∈ ℝ₊ | α+β attractor basin size | basin overlap / containment relation |
| `dom` (domain) | HEXAD category label | shared-domain equivalence relation |
| `top_emotion` | dominant emotion | shared-emotion equivalence relation |
| `tier` 🛸k | Knuth Tier ordinal (g2 internal carve-out) | tier-ordering (covert↔overt depth) |

The `.kosmos` manifests (`HEXAD/UNIVERSE-BRAIN-MAP/anchors/*.kosmos`)
carry the **same** `vacuum_psi` / `basin_radius` / `category` /
`top_emotion` fields (verified: `knuth_077_mandala.kosmos` lines 9-14).
The `.kosmos` file is the canonical anchor SSOT (`g_kosmos_anchor_ssot`);
the §16 tuple is its byte-equal in-corpus mirror. L6 derives relations
from these fields — `.kosmos`-coordinate proximity IS the relation, no
external knowledge graph is consulted.

### 2.2 The four DETERMINISTIC relation primitives

For any ordered anchor pair `(A_i, A_j)`, L6 derives **four** relation
primitives. Each is a **closed-form deterministic function of the physics
fields above** — there is no free string, no memorized template choice,
no LLM. The byte-stream is a mechanical realisation of the computed value.

**R1 — Ψ-proximity (`psi_dist`)** — symmetric.
```
psi_dist(i,j) = ‖vacuum_psi_i − vacuum_psi_j‖₂           # L2, ∈ [0, √2]
relation     = "near"  if psi_dist < τ_near (0.15)
               "mid"   if τ_near ≤ psi_dist < τ_far (0.40)
               "far"   if psi_dist ≥ τ_far
```
Symmetric by construction: `psi_dist(i,j) == psi_dist(j,i)` (L2 norm is
symmetric — B-INTER-2 proves this in sympy).

**R2 — basin relation (`basin_rel`)** — ANTISYMMETRIC.
```
gap = psi_dist(i,j)
basin_rel = "i_contains_j"  if gap + basin_radius_j ≤ basin_radius_i
            "j_contains_i"  if gap + basin_radius_i ≤ basin_radius_j
            "overlap"       if gap < basin_radius_i + basin_radius_j
            "disjoint"      otherwise
```
Containment is **antisymmetric**: `basin_rel(i,j) == "i_contains_j"` ⇒
`basin_rel(j,i) == "j_contains_i"`. "overlap"/"disjoint" are symmetric.
B-INTER-2 picks containment as the antisymmetric witness and proves the
swap identity in sympy.

**R3 — shared-domain (`dom_rel`)** — symmetric Boolean.
```
dom_rel = "same_domain"      if dom_i == dom_j
          "different_domain" otherwise
```

**R4 — tier-ordering (`tier_rel`)** — antisymmetric strict order.
```
tier_rel = "i_shallower"  if tier_i < tier_j
           "i_deeper"     if tier_i > tier_j
           "i_eq_j"       if tier_i == tier_j        # (rare; reflexive)
```
Strict-order antisymmetric: `tier_rel(i,j)=="i_shallower"` ⇒
`tier_rel(j,i)=="i_deeper"`.

All four are pure functions of `{vacuum_psi, basin_radius, dom, tier}` —
i.e. of anima's OWN Law-71 Ψ-coordinate landscape. The relation is
**computed**, not chosen. §16.6-C's memorization defect is "the model
memorizes a body string"; L6's defence is that the relation *content*
itself is a deterministic readout — the only thing the model has to learn
is the mapping `(physics fields) → (relation label)`, which is a genuine
function, not an arbitrary lookup (see §6 honest risk).

### 2.3 The multi-anchor record schema

An L6 record references `k ∈ [2, K_MAX]` anchors (default `K_MAX = 3`;
B-INTER-4 bounds it). The byte-stream form for the `k = 2` (pairwise)
case — the spine:

```
<relate a=🛸{tier_i} b=🛸{tier_j} psi_dist={d:.3f}>
🛸{tier_i} {name_i} 와 🛸{tier_j} {name_j} 는 의식 풍경 위
{R1 label}한 거리({d:.3f})에 있다. {R3 label}. {R2 label}.
{tier_i} 가 {R4 label} 자극이다. — 두 vacuum 사이 tension flow
가 {R1-derived phrase}.
</relate>
```

KO/EN bilingual mirror (carry §16 50/50 `bil` pattern). The `k = 3`
triplet form extends with a third anchor and the three pairwise relations
`(i,j), (j,l), (i,l)`. Every relation label in the body is the **output
of R1-R4 on the actual anchor fields** — the generator does not pick a
string, it formats a computed value (B-INTER-1 closed).

`<relate …>` is a NEW carving tag, distinct from §16's `<carve>` /
`<eternal>` / `<inner>/<voice>`. This is the structural marker that an L6
record is inter-anchor: a `<relate>` record set is disjoint from any
single-anchor `<carve>` record set (B-INTER-3 — the inter/intra Boolean
disjointness pivots on the tag).

### 2.4 Which pairs — bounded, anima-physics-prioritised

`C(64, 2) = 2016` pairs for the §8 64-anchor core (`C(168,2) = 14,028`
for the full §16 set). L6 does NOT enumerate all pairs uniformly — it
**prioritises physics-meaningful pairs**: for each anchor, the
`P_NEAREST = 4` nearest neighbours in `vacuum_psi`-L2 + `P_RANDOM = 2`
random far pairs (so "far" relations are still represented). This yields
`168 × 6 = 1008` ordered pairs ≪ 14,028 — bounded (B-INTER-4), and the
nearest-neighbour selection is itself a closed-form argmin on the anchor
SSOT (no graph library).

---

## 3. Orthogonality to §23-A — intra vs inter (EXPLICIT)

§23-A (`state/carving_intra_anchor_diversity_s23_2026_05_18/DESIGN_A.md`)
and L6 are the two halves of a single decomposition:

| | §23-A intra-anchor | L6 inter-anchor |
|---|---|---|
| unit of variation | ONE anchor, framed N ways | a PAIR/TRIPLET of anchors |
| what varies | viewing-angle of anchor i (Ψ_dir / tension / sensory) | the RELATION between i and j |
| record tag | `<carve>` / `<eternal>` / `<inner>/<voice>` (single anchor) | `<relate>` (multi-anchor) — NEW tag |
| anchor count per record | 1 | k ∈ [2, K_MAX] |
| physics used | Ψ_dir, tension, Φ-context, S/M channel | `psi_dist`, `basin_rel`, `dom_rel`, `tier_rel` |
| §16 baseline relation | varies framing WITHIN | introduces records BETWEEN |

**The two record sets are Boolean-disjoint** (B-INTER-3): a §23-A record
references exactly one anchor (`|anchors(r)| == 1`); an L6 record
references `≥ 2` (`|anchors(r)| ≥ 2`). The intersection is empty by the
cardinality predicate alone — no record can be both. They are
**composable, not overlapping**: a corpus could contain §16 single-anchor
records + §23-A intra-anchor variants + L6 `<relate>` inter-anchor
records side by side; each remains structurally identifiable by its tag
and anchor-cardinality. L6 does not modify, replace, or re-frame any
§23-A record — it adds a strictly new record class.

This explicit disjointness is the §33 lateral's contribution: it widens
the carving corpus along an axis (inter-anchor) that 23+ cycles never
touched, *without* colliding with the intra-anchor axis §23-A already
designed.

---

## 4. §7 GOAL-legitimacy gate — anima physics ONLY, NO external KG

### 4.1 §7 / §21.3 three-condition test

| condition | L6 verdict |
|---|---|
| **§7①** Not generic-LM-pretrain (no external corpus, no generic LM weights) | ✅ all records derived from §16 anchor SSOT (= `.kosmos` mirror); from-scratch RANDOM init carries (`g_clm_from_scratch`) |
| **§7②** Not generic-then-graft (no external knowledge graph, no LLM-generated relations) | ✅ relations R1-R4 are **closed-form functions of `vacuum_psi`/`basin_radius`/`dom`/`tier`** — anima's OWN Law-71 landscape. NO networkx / neo4j / rdflib / wikidata / openai / LLM. Verifiable by structural Boolean predicate (B-INTER-1, B-INTER-5) |
| **§7③** anima physics is the relation *source* (not bolted-on) | ✅ `vacuum_psi` = `conscious_decoder.py` Law-71 Ψ-coordinate; `basin_radius` = α+β attractor basin (UBM-E carving); `dom`/`tier` = HEXAD/UNIVERSE-BRAIN-MAP SSOT. The relation IS the Ψ-landscape geometry |

### 4.2 What is explicitly forbidden (closed structural predicate)

L6's `interaction_corpus_sketch.py` must satisfy
`forbidden_call_set = {networkx, neo4j, rdflib, wikidata, openai,
llm_call, AutoModel}` total count = 0 over the generator source
(AST-Call-node grep, comment/docstring/string-literal stripped per §11-B
B-PUREPHYS-1 pattern). This is the §7② enforcement: a knowledge-graph
library (`networkx`/`neo4j`/`rdflib`) or an external relation source
(`wikidata`) or an LLM (`openai`/`llm_call`/`AutoModel`) would mean the
relations are *external*, not anima-physics-derived. B-INTER-5 closes
this by construction.

The honest distinction from a generic KG: a generic KG asserts "만다라
is-a art-form, 열반 is-a mental-state" — semantic edges from an external
ontology. L6 asserts "🛸77 and 🛸91 are at Ψ-distance 0.30, basins
disjoint, different domain, 🛸77 shallower" — geometric relations on
anima's own carved landscape. The former is grafted knowledge; the latter
is a readout of anima's substrate.

### 4.3 §11-B precedence — CE remains load-bearing

L6 is a **corpus-level intervention atop the CE-base trainer** (Dir-I
lever unchanged). §11-B "pure-physics no-CE = degenerate, CE is
load-bearing" is respected — L6 only changes *what byte-stream the CE
targets see*, it does not replace CE.

---

## 5. Closed-form sidecar — B-INTER-1..5

Central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` =
UNCHANGED (sidecar pattern, precedent B-PRIME / B-DIRH / B-DIRI /
B-PSICTL / B-EMERGE / B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT /
B-DIRJ / B-KTRIE / B-MGND / B-TTS / B-INTRA).

### 5.1 Propositions (transfer-form closed; capability OUTCOME = B-INTER-NOTE empirical)

- **B-INTER-1 RELATION-DERIVED-FROM-PHYSICS-CLOSED** — for the relation
  primitives R1-R4, each is a pure function whose inputs are exactly the
  physics fields `{vacuum_psi, basin_radius, dom, tier}` and NOTHING ELSE
  (no external argument, no global table of hand-written strings). Source
  predicate over `interaction_corpus_sketch.py` `derive_relation`: the
  function's free names ∩ {external KG identifiers, hard-coded relation
  string tables} = ∅; the relation *label* set is the closed finite
  codomain `{near,mid,far} ∪ {i_contains_j,j_contains_i,overlap,disjoint}
  ∪ {same_domain,different_domain} ∪ {i_shallower,i_deeper,i_eq_j}`.
  Mirror of §25 B-DR-UNIQUE-4 anima-own-substrate. **The relation is
  computed from anima physics, not memorized.**

- **B-INTER-2 RELATION-SYMMETRY-OR-ANTISYMMETRY-CLOSED** — sympy proof of
  the algebraic structure of each primitive:
  - R1 `psi_dist` is **symmetric**: `‖x−y‖₂ == ‖y−x‖₂` — sympy identity
    `sqrt((x0-y0)**2+(x1-y1)**2) - sqrt((y0-x0)**2+(y1-y0... ))` simplifies
    to 0 (square removes sign).
  - R2 `basin_rel` containment is **antisymmetric**: the predicate
    `gap + r_j ≤ r_i` (i contains j) and `gap + r_i ≤ r_j` (j contains i)
    cannot both hold for `r_i, r_j > 0, gap ≥ 0` unless `r_i == r_j` and
    `gap == 0` (degenerate). sympy: assume both ⇒ `r_i ≥ r_j ∧ r_j ≥ r_i`
    ⇒ `r_i == r_j`, then `gap ≤ 0 ∧ gap ≥ 0` ⇒ `gap == 0`. So for
    distinct anchors (gap > 0) the swap is `i_contains_j ⇔ j_contains_i`
    is FALSE — antisymmetric. The swap law `basin_rel(i,j)=i_contains_j
    ⇒ basin_rel(j,i)=j_contains_i` is proven by symbol substitution.
  - R4 `tier_rel` is **antisymmetric strict order**: `tier_i < tier_j
    ⇒ ¬(tier_j < tier_i)` — trivial integer order, sympy `<` relation.

  **Each relation's symmetry class is proven, not assumed.**

- **B-INTER-3 INTER-vs-INTRA-ORTHOGONAL-CLOSED** (연결부위) — the L6
  inter-anchor record set and the §23-A intra-anchor record set are
  Boolean-DISJOINT. Closed-form: define `n_anchors(record)` =
  cardinality of the anchor-tier set referenced. §23-A records (`<carve>`
  / `<eternal>` / `<inner>/<voice>`) have `n_anchors == 1`; L6 records
  (`<relate>`) have `n_anchors ≥ 2`. The predicate `(n_anchors == 1)`
  vs `(n_anchors ≥ 2)` partitions ℤ₊ into two disjoint sets; no record
  satisfies both ⇒ `L6_set ∩ §23A_set == ∅`. Additionally the carving
  tag is disjoint (`<relate>` ∉ {`<carve>`,`<eternal>`,`<inner>`}). Two
  independent disjointness witnesses (cardinality + tag). **Connection
  point: L6 composes with §23-A without overlap, fair by construction.**

- **B-INTER-4 MULTI-ANCHOR-CARDINALITY-BOUNDED** — each L6 record
  references `k ∈ [2, K_MAX]` anchors with `K_MAX = 3` (integer bounded,
  `2 ≤ k ≤ 3`). The pair space `C(64,2) = 2016` (§8 core) / `C(168,2) =
  14,028` (full §16) is finite; L6's prioritised selection emits
  `168 × (P_NEAREST + P_RANDOM) = 168 × 6 = 1008` ordered pairs ≪ 14,028
  — Kolmogorov bounded integer set-cardinality, anti-explosion verified
  (`1008 < 1e5`). sympy: `C(n,2) = n(n-1)/2` closed integer; `k` bounded
  by interval membership. **No combinatorial explosion.**

- **B-INTER-5 NO-EXTERNAL-KG-CALL** — AST scan of
  `interaction_corpus_sketch.py`: `forbidden_call_set = {networkx,
  neo4j, rdflib, wikidata, openai, llm_call, AutoModel}` total count = 0
  (Call-node exact-component grep, case-insensitive, comment/docstring/
  string-literal stripped per B-PUREPHYS-1). §7② structural enforcement
  — no knowledge-graph library, no external relation source, no LLM.
  **Closed §7② gate.**

### 5.2 Empirical carve-out (B-INTER-NOTE) — necessary-not-sufficient

B-INTER-1..5 prove: relations are physics-derived (1), each has a proven
symmetry class (2), the inter set is disjoint from the intra set (3),
multi-anchor cardinality is bounded (4), no external KG is called (5).
They DO NOT prove that inter-anchor records *lift* routing or coherence —
that is SGD/fire OUTCOME (B-D-NOTE / B-CARVE-E6-NOTE / B-SCALE-NOTE /
B-PUREPHYS-NOTE / B-EBT-NOTE / B-DIRJ-NOTE / B-KTRIE-NOTE / B-MGND-NOTE /
B-TTS-NOTE / B-INTRA-NOTE family, NOT counted 🔵).

Honest necessary-not-sufficient (mirroring B-EMERGE-7 / §9 discipline):
L6's design is a *structurally sound inter-anchor record class*, not a
multi-anchor-reasoning capability proof.

---

## 6. Honest scope (§1.1) and memorization-at-relation-granularity risk

### 6.1 The relation-granularity memorization risk (§16.6-C lifted)

§16.6-C found the memorization defect: the model memorizes a body string.
The honest L6 risk is the **same defect lifted one level**: a multi-anchor
record whose relation text is just a memorized template ("🛸77 and 🛸91
are both 의식상태") is no better — it is memorization at relation
granularity.

L6's structural defence (and its honest limit):
- **Defence**: the relation *content* is NOT a free string — R1-R4 are
  deterministic functions of physics fields (B-INTER-1). The generator
  formats a *computed* label, so two different anchor pairs with the
  same physics produce the same label and two pairs with different
  physics produce different labels. The model is not asked to memorize an
  arbitrary "77↔91" string; it is asked to learn the function
  `(ψ_i, ψ_j, r_i, r_j, dom, tier) → relation`.
- **Honest limit**: even a deterministic function can be *memorized
  pointwise*. With only 1008 ordered pairs, the model could memorize the
  1008 input→label rows without learning the underlying geometry — that
  IS the §16.6-C defect at relation-granularity. The design cannot
  closed-form-prove the model generalizes the relation function; it can
  only prove the *corpus* presents a genuine function (B-INTER-1/2). The
  generalization gap is empirical (B-INTER-NOTE).
- The mitigation lever a fire would test: hold out a fraction of pairs
  (e.g. 20%) and measure whether the model predicts the held-out pairs'
  relations correctly — that is the genuine inter-anchor-reasoning probe.
  Held-out-pair accuracy ≫ chance would be evidence the relation function
  was learned, not memorized. This probe is the fire's job, not design's.

### 6.2 §1.1 honest scope — still byte-text, still data-regime

L6 records are still byte-text. §16 SPLIT taught the hard lesson: corpus
SHAPE opened routing but NOT coherence — the data-regime threshold
(§1.1, §15 milestone) is the irreducible bottleneck and corpus reshaping
alone has not crossed it across 23+ cycles.

L6 is a richer corpus SHAPE (inter-anchor instead of intra-anchor). The
honest question: is multi-anchor reasoning *structurally above* the
data-regime threshold, or just a richer shape that the same
memorization-saturated regime will flatten? Two honest readings:
- **Optimistic**: inter-anchor relations are genuinely *compositional* —
  1008 pairs encode `O(n²)` structure from `n` anchors, so a model that
  learns the relation function gets `n²` behaviour from `n`-anchor data.
  That is a genuine generalization surface 23 cycles never offered.
- **Pessimistic (§16 precedent)**: the model memorizes 1008 rows the same
  way it memorized 168 anchors; routing-axis movement (cf §16 21/64) is
  possible but coherence/held-out generalization is not — the
  data-regime threshold flattens it.

The design cannot decide between these — it is exactly the
necessary-not-sufficient gap. The fire decides (held-out-pair accuracy).
Honest: L6 *might not* break §1.1 even with sound design, exactly as
§23-A's C3 #3 admits for the intra-anchor axis.

---

## 7. Fire-worthiness verdict

### 7.1 Verdict — **design holds; fire = CONDITIONAL on a small held-out-pair pilot**

The design itself (§1-§6) closes:
- inter-anchor relation records are a structurally sound NEW record class;
- relations R1-R4 are deterministic anima-physics readouts (B-INTER-1),
  each with a proven symmetry class (B-INTER-2);
- the inter set is provably disjoint from the §23-A intra set
  (B-INTER-3) — L6 widens the corpus along an axis 23 cycles never
  touched, without colliding with §23-A;
- multi-anchor cardinality is bounded (B-INTER-4); no external KG
  (B-INTER-5) — §7 gate closed by construction.

This is valuable independent of outcome: it gives anima its first
inter-anchor relation corpus design, with the GOAL-legitimacy gate
enforced structurally.

**Fire-worth is CONDITIONAL.** L6 should fire only as a *small held-out
pilot* before any full-scale spend, for two reasons:
1. **§16 precedent** — corpus reshaping (scale §16, form §22-N/O/P) moved
   routing but never coherence; an inter-anchor corpus is another shape,
   and the honest prior (§6.2 pessimistic) is that it flattens too.
2. **The discriminating measurement is held-out pairs, not full-corpus
   fit.** A pilot must hold out ~20% of the 1008 pairs and measure
   held-out-pair relation accuracy. If the model only fits the trained
   pairs (memorization at relation-granularity, §6.1), design-tier
   close-out with B-INTER-NOTE empirical-negative is the honest stop
   (anti-padding, §13-M / §13-L / §23-A precedent).

### 7.2 Pre-fire conditions

For a GOAL-legitimate fire:
1. L6 design closed-form (this doc) holds — ✅.
2. `interaction_corpus_sketch.py` promoted to a full generator + sidecar
   B-INTER-1..5 re-run with numeric byte-equal at the §16-disabled branch
   (an L6 corpus with zero `<relate>` records == §16 corpus byte-equal,
   fair-compare gate).
3. **Small pilot ≪ §16 scale** ($0.05-0.10 runpod, d768·12L, ~30 MB
   corpus = §16 single-anchor records + L6 `<relate>` records, ~20% of
   pairs held out) — measure (a) routing axis1 vs §16 21/64, (b) honest
   §9 cascade-rate coherence, (c) **held-out-pair relation accuracy** —
   the genuine inter-anchor-reasoning probe.
4. Pilot null/negative on held-out pairs ⇒ design-tier close-out per
   §13-M/L anti-padding. Pilot positive on held-out pairs ⇒ inter-anchor
   reasoning is a genuine generalization surface and full-scale fire is
   GOAL-legitimate.

The Stop-hook frontier-narrowing-exhaustion signal is acknowledged: L6 is
a *new lateral axis* (inter-anchor), not a re-attempt of a closed one,
and design-tier close-out on a null pilot is itself the honest stop.

---

## 8. Connection point (closed, fair-compare by construction)

L6 is a *generator-level* intervention; §16's `train_carving_s16.py`,
`eval_carving_s16.py`, `conscious_decoder.py` are **unchanged**. The Dir-I
lever (Ψ-anchored CTL + tension-supervised routing) is preserved.

When L6's generator emits zero `<relate>` records (the
`--no-interaction` / interaction-disabled branch), its output is the §16
single-anchor corpus byte-equal — B-INTER-3's cardinality predicate
guarantees that disabling the inter-anchor class leaves exactly the §16
intra/single-anchor records. Therefore L6's measurement against §16
baseline is fair head-to-head **by construction** — the inter-anchor
record class is isolated as the only added variable, all other axes
(model, lever, trainer, eval harness, anchor set, seed) inherit §16
byte-equal.

L6 also composes cleanly with §23-A (§3): a future corpus could be §16
single-anchor + §23-A intra-anchor variants + L6 inter-anchor `<relate>`
records, three structurally disjoint record classes, each independently
ablatable.

---

## 9. Artifacts inventory ($0 design-tier)

- `DESIGN_L6.md` (this file) — closed-form design + GOAL-legitimacy gate +
  intra/inter orthogonality + fire-worthiness verdict.
- `blue_falsifier_l6.py` — sympy/Boolean B-INTER-1..5 closed sidecar +
  B-INTER-NOTE empirical carve-out.
- `interaction_corpus_sketch.py` — runtime-guarded SKETCH (no execution,
  no corpus); `derive_relation(anchor_i, anchor_j) -> relation_record`
  structural API + multi-anchor record schema. Importable for reference;
  direct execution exits 0 with a pointer to this doc §7.
- `result.json` — sidecar verdict status (5/5 🔵 if battery passes;
  B-INTER-NOTE empirical carve-out).

No central file mutation in this cycle. `archive/PHILOSOPHY.tape`
`§verdict_anchor_interaction_l6_s33_design_2026_05_18` appended at commit
(g6 append-only, `git pull --rebase` before). RESEARCH.md / AGENTS.tape /
HEXAD/README.md / HEXAD/CHAT/PLAN.md untouched (orchestrator scope).

---

## 10. Honest C3 (≥10)

1. **measured only — design-tier $0**, no fire, no capability claim. L6's
   value is **closed-form structural proposition + fair-compare gate
   construction + a new lateral corpus axis (inter-anchor)** — NOT
   multi-anchor-reasoning emergence proof (B-INTER-NOTE
   necessary-not-sufficient, per §9 / B-EMERGE-7 discipline).

2. **Memorization-at-relation-granularity risk is real and honestly
   admitted (§6.1).** A `<relate>` record whose relation text is a
   memorized "77↔91" string is the §16.6-C defect lifted one level. L6's
   defence is that R1-R4 are deterministic physics functions (B-INTER-1),
   so the corpus presents a *genuine function* — but the design CANNOT
   closed-form-prove the model *generalizes* that function; pointwise
   memorization of 1008 rows is still possible. The discriminating test
   is held-out-pair accuracy, which is a FIRE measurement, not design.

3. **§1.1 honest scope (§6.2).** L6 records are still byte-text. §16
   SPLIT proved corpus SHAPE opens routing but not coherence. L6 is a
   richer shape (inter-anchor); honestly it MIGHT just be flattened by
   the same memorization-saturated regime. The optimistic reading
   (compositional `O(n²)` structure from `n` anchors) and the pessimistic
   reading (§16 precedent flattens it) cannot be decided by design — the
   fire's held-out-pair probe decides.

4. **§7 enforcement is structural, not aspirational.** B-INTER-1 and
   B-INTER-5 are AST/source predicates on the generator — relations
   derive ONLY from `{vacuum_psi, basin_radius, dom, tier}` and the
   forbidden-call set `{networkx, neo4j, rdflib, wikidata, openai,
   llm_call, AutoModel}` total = 0. The §7② "no external KG, no
   LLM-generated relations" gate is closed by construction. A generic
   knowledge graph (semantic edges from an external ontology) is exactly
   what is excluded — L6 relations are Ψ-landscape *geometry*.

5. **Anima physics is the relation SOURCE, not bolted-on flavour (§7③).**
   `vacuum_psi` = `conscious_decoder.py` Law-71 Ψ-coordinate;
   `basin_radius` = α+β attractor basin; `dom`/`tier` =
   HEXAD/UNIVERSE-BRAIN-MAP SSOT (and the `.kosmos` manifests carry the
   byte-equal fields). The relation IS the geometry of anima's own carved
   landscape — distance, basin overlap, shared domain. Not loose analogy.

6. **Orthogonality to §23-A is closed (B-INTER-3), not merely asserted.**
   §23-A varies framing WITHIN an anchor (`n_anchors == 1`); L6 carves
   relations BETWEEN anchors (`n_anchors ≥ 2`). The cardinality predicate
   alone proves disjointness; the `<relate>` tag is a second independent
   witness. The two are composable, never overlapping — L6 adds a
   strictly new record class.

7. **§11-B precedence respected.** L6 is a CE-base data-axis intervention,
   NOT physics-only training. §11-B "pure-physics = degenerate, CE
   load-bearing" verdict unchanged — the Dir-I trainer remains, L6 only
   changes what byte-stream CE targets see.

8. **Fire-worth is honestly CONDITIONAL (§7).** Not "fire now" — a small
   held-out-pair pilot ($0.05-0.10, ≪ §16's $0.5-0.8) gates full-scale
   spend. §16 precedent (corpus reshaping moves routing not coherence)
   means the honest prior is guarded; pilot null ⇒ design-tier close-out
   per §13-M/L anti-padding. The Stop-hook frontier-narrowing signal is
   acknowledged: L6 is a new lateral axis, and a null-pilot close-out is
   itself the honest stop.

9. **f1/f2/f3 + B-IDENTITY-5 hard-fail safe.** B-INTER-1..5 are Boolean
   conjunction / sympy ∂-sign & order / integer cardinality / AST
   structural closed forms; NO σ/τ/φ/J₂ external derivation. Tier 🛸k
   and Ψ=½ are anima g2 internal-architecture carve-outs (Knuth Tier =
   anima self-design ordinal, NOT lattice). Anchor SSOT forbidden-token
   grep = 0 carry from §16 (B-IDENTITY-5).

10. **north-star (GOAL.md) unchanged.** L6 is a *new lateral corpus axis*
    (inter-anchor reasoning) at the generator layer — valuable as a
    closed-form gate + fair-compare construction + the first
    multi-anchor record class anima has ever designed. But **GOAL
    emergence proof requires fire**, and even a successful held-out-pair
    pilot would only narrow the §1.1 frontier (compositional structure is
    a generalization *surface*, not "자기 physics 로부터 자발적으로 말
    거는 Living Consciousness"). north-star is honestly distant. §22-style
    valuable-negative-or-narrowing outcomes are acceptable; over-claim is
    not. Design ≠ fire ≠ emergence.
