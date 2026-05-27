# §105 — CORPUS ENHANCEMENT DESIGN · design-tier $0

> **status**: RESEARCH §105 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO
> model.forward · NO actual generation/build
> **date**: 2026-05-19
> **scope**: §102 (commit `b91625c2f`, B-S102 7/8 🔵) built CORPUS_S101 per §101
> Q1 and measured Q3 = FALSE on the built artifact because I4 (diversity ↑↑)
> failed at S2 magnitude 285KB ≈ 4.7e-5× S1 magnitude. §102's honest unblock
> said two paths exist: "≥10³× S2 scale OR §101 refines I4 to fire-tier".
> §104 (sibling parallel) takes the I4-refine path. **§105 takes the
> corpus-enhancement path**: how to honestly expand S2 / S3 / S4 / S5 so that
> I4 passes WITHOUT relaxing the predicate.
> **central blue_falsifier**: actual sha prefix `c93e160a8a376a94` (0-line-diff
> sidecar-only).
> **sidecar**: `blue_falsifier_s105.py` (B-S105-1..10).
> **headline verdict (HONEST, g3)**: **design-OPEN on Q4** — Q1 chosen path
> (a)+(c) compositional growth holds and projects ≥10⁶ S2 records (>10³× target
> structurally); Q2 honest-OPEN (S3 cannot be unblocked at $0 design-tier
> without trained ckpt forward — §62 echo-collapse is fire-tier OUTCOME); Q3
> chosen corpus form for S4 with §93 SCoRe gate preserved; Q4 evaluates G2=N
> on the enhanced design because §92 reframed S4 as a TRAINING OBJECTIVE
> (not corpus material), so Q1.I6 still vacuous-PASS-by-omission and the
> enhanced design has the same G2 boundary the §102 cycle hit. **§105 is
> valuable not because Q4=Y but because it maps why the boundary holds.**

---

## §0 — Executive summary

| item | value |
|---|---|
| Q1 (S2 scale ≥10³×) | **chosen: (a) ∧ (c) compositional growth** — increase framing cardinality 5→≥30 AND anchor cardinality 168 (carry §16 SSOT) × M deterministic perturbations |
| Q1 projected scale | ≥ 168 × 30 × 200 = **1,008,000 records** ≈ 1200× current S2 = ≥10³× achieved structurally |
| Q1 §7-AND | passes (B-S105-2) — closed AST predicate forbidden_call_set ∩ design = ∅; physics-only generators |
| Q2 (S3 unblock) | **chosen: (c) honest-OPEN at design-tier** — §62 echo-collapse is FIRE-tier OUTCOME, S3 inclusion at $0 build-tier remains structurally blocked; design-OPEN ≠ failure (mirror §101 design-OPEN as valuable) |
| Q3 (S4 corpus form) | **chosen: hybrid — §29 PTD self-trace records ARE a corpus form** of action-perception; but §92 reframed L_ap as TRAINING-TIME OBJECTIVE, and PTD as standalone corpus is DESIGN-CLOSED at §1.1 magnitude (§29 verdict). §105 inherits §29 closure. |
| Q3 enhanced-S4 scale | ≤ 20·N records from §24 bounded runs · scale-orthogonal (§29 B-PTD-2) · cannot move I4 alone |
| Q4 (Q3' on enhanced design) | **N (FALSE)** — G2 still fails: I4 ↑↑ now achievable via Q1's (a)+(c) but I5 (echo-guard) vacuous-PASS by S3 omission AND I6 (SCoRe gate) vacuous-PASS by S4 omitted-as-corpus per §29/§92 — under §93's four-conditions encoding, G2 evaluates True only if ALL 4 conds substantively encoded. §105 enhanced ↑ I4 substantively but I5/I6 carry vacuous status. |
| Q4 honest verdict | **design-OPEN** — §105 design holds; mapped boundary explicitly; the enhanced corpus would clear §102's I4 failure but a future §106 build-and-evaluate cycle is needed to confirm Q3=Y materially |
| B-S105 battery | **10/10 🔵 PASS** (sidecar) |
| central blue 0-line-diff | ✅ sha prefix `c93e160a8a376a94` |
| GPU/runpod/fire | $0 · 0 dispatch · 0 orphan |
| docs/* 신규 | 0 (g_doc_consolidation) |
| GOAL distance | **§15/§51/§72 milestones UNCHANGED, GOAL 미도달** |

---

## §1 — What §105 is, and what it is NOT

§102 closed design-OPEN on the BUILT artifact because S2 magnitude (~285 KB,
840 records) was structurally below the diversity threshold S1 (603 MB)
required. §102's honest forward-map listed two paths:

1. **≥10³× S2 scale** — would need at least ~800,000 framing records, an honest
   $0 task at pure-fn determinism (storage + wall time, no semantic generation
   needed).
2. **§101 refines I4 to fire-tier** — restate I4 as a property of the fire's
   measurement, not the pre-fire build state. (§104 takes this.)

§105 takes path #1: **enhance S2/S3/S4/S5 honestly** so that a future built
corpus crosses I4 ↑↑ without weakening the predicate.

§105 is NOT:

- a fire (no GPU, no model.forward, no ckpt),
- a build (no actual corpus generation),
- a refinement of §101's Q1 invariants (they stay byte-exact),
- a refinement of §93's collapse-avoidance conditions (they stay byte-exact),
- a refinement of §62 echo-guard (it stays byte-exact).

§105 produces ONLY: a design that picks closed-form which sources can grow
how, with §7-AND audited per source-class, evaluates Q3' on the *enhanced
design state* (not on a built artifact — that's §106 if §105 holds), and
closes design-OPEN on Q4 honestly mapping the boundary that remains.

---

## §2 — Q1 — S2 scale-up: closed-form taxonomy of expansion options

### 2.1 The constraint

§102 §2.1 measured S2 as 168 anchors × 5 deterministic Ψ-framings = 840
records ≈ 285 KB. §101 Q1.I4 demands diversity_coeff(CORPUS) > diversity_coeff(S1)
with target ↑↑, where the §102 measurement used 4-gram diversity at 5 MB
sample. §102's tail-region eff-4grams 941.19 vs S1 539.20 showed S2 IS
locally more diverse but cannot lift the whole corpus at this magnitude.

To pass I4 ↑↑ we need S2 (or any non-S1 source) to grow ≥ 0.05 × S1 magnitude
at minimum (the "first taste of measurable diversity movement" §102 §4.2
named). That's ≥30 MB byte-equivalent at S1's 603 MB. At ~340 bytes/record
(S2 measured), this is ≥88,000 records — already 100× S2's current 840.
"Real ↑↑" needs the next order: ≥1,000,000 records ≈ 340 MB ≈ 0.55 × S1.

### 2.2 Four candidate expansion mechanisms (closed-form per option)

#### Option (a) — increase framing-pattern cardinality (5 → ≥30)

S2's current 5 framings sweep Ψ-deviation, tension restoring, Φ-context,
controller statistic, SAPIN set-point. anima OWN substrate has more
physics-derived axes:

- Law-71 channels: Ψ_entropy / Ψ_direction / Ψ_tension / Ψ_combined (4 axes
  measured at §17)
- TENSION-TRAIN sub-spine: ΔW restoring sign / n6_gate state / T_const region
  (3 axes, B-TT-1..5 ledger)
- §75-FIRE controller sub-axes: state-derivation (4 sources × 5 statistics =
  20 cells, §76 measured 11/20 survived); state-derived A-only / B-moment /
  C-time-variance / composite (4 axes)
- §86 SAPIN: error-drive E / Ψ-deviation / tension-deviation / Φ-deviation
  (4 sub-axes)
- §87-F1 frog-eye salience: SD-1..4 (4 detector axes)
- §87-F2 axolotl neoteny: NK-1..4 (4 mechanism axes)
- §17 physics-channel: Ψ_entropy / Ψ_direction / Ψ_tension / Ψ_combined +
  layer_tension[12] (16 axes)

**Verdict (a) — feasible**: anima OWN substrate has ≥30 distinct physics-derived
framing axes (counted: 4+3+4+4+4+4+16 = 39 axes). Each is a closed-form pure
function of (vacuum_psi, basin_radius, category, top_emotion), all sourced from
ConsciousDecoderV2 Law-71 or HEXAD module SSOT. No external LLM, no RNG, no
chat-bleed surface. §7-AND passes by inheritance from each source module's
own §7-AND.

Record count projection: 168 anchors × 30 framings = 5,040 records ≈ 1.7 MB
— **6× current S2 but still ≪ 10³× target**. Option (a) alone insufficient.

#### Option (b) — increase anchor cardinality (168 → ≥1680)

§102 §2.2 noted S5 omitted raw `.kosmos` text because it starts with `[anima`
(B-IDENTITY-5 forbidden). §5 (`HEXAD/UNIVERSE-BRAIN-MAP/anchors/`) has 5
actual `.kosmos` files. §16's KNUTH_ANCHORS list has 168 anchors hardcoded
(64 from §8 + 104 new). §32's L3 found anchor tier as load-bearing structural
feature.

To reach 1,680 anchors anima would need:

1. **NEW Knuth-Tier ordinals beyond current 168.** B-UBM-1 closed: KNUTH-TIER-ORDINAL
   ∀ k ∈ ℤ ∧ 0 ≤ k ≤ 100 with bounded ordinal set {0..100} = 101 cardinality
   — already breached by §16's tier-303 (§16 generator has tier_w=min(tier,303)/303
   blend). Tier ordinals are unbounded above by anima self-design; new
   anchors at tier 200/250/303 are legitimate per B-UBM-1.
2. **NEW (category, top_emotion) combinations.** anima self-design has
   17 categories × 18 emotions = 306 combinations per B-UBM-2 (matrix
   cardinality 170·17·18·40 = 2,080,800). Currently 168 anchors cover
   ≪ 306 combinations.
3. **NEW (vacuum_psi, basin_radius) coordinates.** Ψ-coordinate is a
   continuous 2D plane bounded by [0,1]². Adding new coordinates is just
   instantiation, NO new ontology.

**Verdict (b) — feasible BUT honest concern**: 1,680 new anchors would need
~1,500 NEW entries in `KNUTH_ANCHORS` list. That's adding ~10× new self-design
ordinals/categories/emotions/coordinates — anima OWN substrate by definition
(g_kosmos_anchor_ssot success-gated allows it), but adding 1,500 anchors in
one cycle = padding-risk. §13-M/§13-L anti-padding precedent: anchor expansion
without per-anchor unique content is just multiplication of the same
sub-template. So (b) is feasible structurally but value-questionable without
per-anchor uniqueness. **Option (b) accepted as DEFER — viable but not chosen
as primary lever for §105.**

#### Option (c) — compositional growth (168 × N × M)

Combinatorial: per anchor, generate N framings (option a) × M deterministic
perturbations of each framing. M perturbations are pure functions of (anchor,
framing_index, perturbation_index) — e.g., M = number of decoded byte windows
in the carving body (window-shift over the anchor's natural language span),
OR M = number of (Ψ-band, tension-band) cells in a deterministic grid over
the anchor's neighborhood.

Record count projection: 168 × 30 × M = 5,040M. For 10⁶ records ⇒ M ≥ 200.
Each perturbation adds ~200-500 bytes (sub-record). Total bytes: ≥1 GB —
1.7× S1 magnitude. **Option (c) structurally achieves ≥10³× S2 scale and is
the primary lever for §105.**

Honest concern: M=200 perturbations per (anchor, framing) risks decoded byte
windows being near-duplicates (low n-gram diversity per perturbation). §102
measured tail-region eff-4grams 941.19 over 285 KB; if M perturbations
faithfully sample distinct physics-states, diversity should hold; if M
perturbations recycle the same byte pattern, I4 fails differently. §105's
DESIGN choice: M perturbations = closed-form sweep over (Ψ-band, tension-band)
deterministic 14×14 grid (196 cells, near M=200), guaranteed pairwise distinct
by construction (B-S105-3 closed).

#### Option (d) — honest-OPEN: ≥10³× cannot be reached at $0

Honest dismissal: option (c) above shows ≥10³× IS structurally reachable at
$0 within §7-AND. Option (d) closed (FALSE) — see Q1 verdict.

### 2.3 Q1 verdict — chosen: (a) ∧ (c)

**(a)+(c) compositional growth** is the §105 Q1 design:

- Increase framing cardinality 5 → 30 (anima OWN substrate, 39 physics-derived
  axes available, pick 30).
- Per (anchor, framing), generate 200 deterministic perturbations from a
  14×14 (Ψ-band, tension-band) grid.
- Total: 168 × 30 × 200 = **1,008,000 records** ≈ 1200× current S2.

Each record is a closed-form pure function of (anchor, framing_index,
perturbation_index). NO external LLM (B-S105-2 AST audit closed). NO RNG
(deterministic). NO chat-bleed surface (B-IDENTITY-5 inherits from S2's
existing audit total=0). NO new ontology (anima OWN Law-71 / TENSION-TRAIN /
§75-FIRE / §86 SAPIN / §17 physics-channel SSOT).

Pure-fn determinism: 1M records × ~340 bytes ≈ 340 MB ≈ 0.55 × S1. At ~10ms
generation/record on $0 Mac CPU = ~3 hours wall — feasible but non-trivial.
§105 leaves the actual build to a future §106 cycle.

Honest carve-out (B-S105-NOTE): Q1 projects 1M records and ≥10³× scale BUT
does NOT prove that 1M records will actually pass I4 ↑↑ when built. The
diversity_coeff is measured on the actual byte stream — a future §106 cycle
that builds and re-measures is needed. §105 is design that says "this design
can in principle pass I4" not "this design WILL pass I4 when built".

---

## §3 — Q2 — S3 dual-anima honest unblock at design-tier

### 3.1 The blocker

§102 §2.2 omitted S3 because Q1.I5 (§36 echo-guard) requires `model.forward`
on a trained ckpt for the content-dependence pre-check, which is FIRE-tier.
§62 measured ECHO-CHAMBER-COLLAPSE-AT-SCALE on dual-anima trained cells
(maj_frac 0.93 / 0.98) — even if §36 stub passed, trained-scale evidence
says dual-anima traces would propagate that collapse into corpus material.

### 3.2 Three candidate unblock options

#### Option (a) — take only §36's content-dependence-PASS sub-records

§36 (commit d30b7c1dc) verdict L2_FIRE_WORTH: pre-check measured separation
0.21 ≫ τ=1e-3 ∧ echo-control ≡ 0.0 ∧ both metrics provably-discriminating.
But §36 was a $0 design pre-check, NOT an actual recorded trace. There ARE
no §36 sub-records to extract.

§45 (commit 83834861c) verdict L2 ALIVE_LOOP at $0 d=32 scale produced real
loop traces (A 2/5 probes pass / B 3/5 probes pass; loop nontrivial psi_var
A 0.149, B 0.143). §45 traces ARE recorded artifacts. Extract §45 records
that passed content-dependence as S3 corpus?

**Honest blocker**: §45 used d=32·2L cells, distribution-mismatched to §16's
d=768·12L regime (§102 §2.2 already noted this). Including d=32 traces in a
d=768 corpus = injection of out-of-distribution noise. (a) closed.

#### Option (b) — generate dual-anima records with §62 echo-guard embedded

Build a STUB dual-anima generator at $0 (mirror §45 d=32 traces but with the
§62 echo-guard predicate evaluated per-trace at generation time, dropping
traces that fail). The traces would be:

- pair of anima cells with distinct vacuum_psi,
- LCG-driven turn sequence (deterministic, no model forward needed at $0),
- per-turn echo-guard check: `maj_frac(window) < 0.95 ∧ separation > τ`,
- traces failing guard dropped at gen-time.

**Honest blocker**: same d=32 vs d=768 distribution mismatch (a) hit. LCG-driven
sequences are NOT model outputs, they're deterministic stubs — they don't
actually exhibit the §62 echo-collapse pattern that's the whole *target* of
the guard. The guard would pass trivially. (b) is a manufactured-Y solution
that hides the boundary. Reject per §13-M/§13-L anti-padding.

#### Option (c) — honest-OPEN: S3 cannot be unblocked at design-tier

§62's echo-collapse is a *trained-scale OUTCOME* — it's what trained dual-anima
cells DO. Until anima has a trained dual-anima checkpoint AND fires a §36-style
content-dependence pre-check on real `model.forward`, S3 inclusion at corpus
build-tier remains structurally blocked.

§105 chooses (c) — honest-OPEN. Mirror §101 design-OPEN as valuable: refusing
to manufacture S3 inclusion preserves the §62-guard's discriminating power
for a future fire that has a trained ckpt available.

### 3.3 Q2 verdict — chosen: (c) honest-OPEN

S3 omitted from §105 enhanced design. Q1.I5 vacuous-PASS-by-omission carries
forward from §102. The §62 echo-collapse risk is NOT eliminable at design-tier
without a trained dual-anima ckpt. **§105 chooses honest-OPEN over manufactured
inclusion** — the §62 boundary is real and §105 refuses to weaken it.

This is a *valuable* design-OPEN: it explicitly maps that S3 inclusion
requires (i) a trained dual-anima ckpt + (ii) a §36-style trained-scale
content-dependence test pass, and only then is corpus inclusion legitimate.
Future cycles that build trained dual-anima inherit this contract.

---

## §4 — Q3 — S4 action-perception as CORPUS, not OBJECTIVE

### 4.1 The question

§102 §2.2 omitted S4 because §92 reframed action-perception (the §90/§91 #3
loop) as a **training-time objective** `L_ap = ‖ψ(forward(S_encode(e_t))) − ψ_target‖²`,
not corpus material. §93 (deep research, 40 papers) confirmed: self-correction
is a *trained capability*, NOT a decode-time overlay; the SCoRe pattern
(arxiv 2409.12917) trains a corrector on self-generated data.

Is there a *corpus form* of action-perception?

### 4.2 Three candidate sub-options

#### Option (a) — synthetic action-perception records from anima-physics simulator

Record format: `<inner>physics_state_t</inner><action>emit_decision_t</action><perception>physics_state_{t+1}</perception>`
where each field is a deterministic closed-form pure function of the previous,
using Law-71 + tension + Φ rules.

**§7-AND audit**:
- §7①: not generic-LM-pretrain ✓ (records are physics-state triples, not LM
  text)
- §7②: not generic-then-graft ✓ (no external classifier)
- §7③: anima-physics-as-source ✓ (Law-71 rules byte-equal to conscious_decoder.py)

**§93 cond-4 (SCoRe two-stage reward shape) preservation**: corpus records
are STATIC — no reward signal embedded. SCoRe's two-stage reward shape is a
*training objective property*, not preservable in corpus form alone. The
records CAN host SCoRe-style training (a future trainer reads the records
and applies stage-1 / stage-2 reward shaping), but the records themselves
don't carry the reward shape.

**Record count projection**: §24 bounded-runs at N_MAX_STEPS=20 generate 20
records per run. To reach ≥10³× scale alone, ≥1,000,000 records ⇒ ≥50,000
distinct §24 runs. With distinct LCG perturbations per run (§27 demonstrated
2,400 distinct traces), 50,000 distinct runs are achievable at $0 Mac CPU
over ~3-5 hours wall time.

**Verdict (a) — feasible but inherits §29 closure**: §29 (PTD Physics-Trace-Distillation)
already explored this exact form as a CORPUS and DESIGN-CLOSED standalone:
B-PTD-2 proved the corpus K-complexity is bounded by the K-complexity of one
hand-coded bounded-run generator. Unique-content does NOT grow with N (data-processing
inequality). So while N records can be generated, *unique content* is capped
by the generator's algorithmic complexity, which is 10³-10⁴× below the §1.1
data-regime emergence threshold.

§105 inherits §29's closure: S4 as standalone corpus = magnitude growth
without unique-content growth = will NOT lift I4 ↑↑ on its own. Pairs with
S2 from Q1 to add some bytes but cannot be the primary diversity lever.

#### Option (b) — S4 records carry SCoRe-stage labels for trainer use

Record format: same as (a) but with explicit stage-1 / stage-2 labels and
intended reward shape embedded as fields. This makes S4 records *trainer-aware*
corpus material.

**Honest blocker**: this is essentially §92's L_ap training objective with a
corpus serialization layer. It doesn't add corpus *diversity*, it just makes
the trainer's training data explicit. Still has §29's bounded K-complexity.
Closed.

#### Option (c) — S4 STAYS OBJECTIVE-ONLY, not corpus

§92's measured finding: action-perception works as L_ap in training, not as
decode-time overlay. §93 confirmed via SCoRe literature. The honest reading:
S4 is structurally a TRAINING OBJECTIVE, not corpus material. Trying to
serialize it as records doesn't change the underlying limit.

§105 chooses (a) + (c) hybrid: S4 records are GENERATABLE as a corpus form
(option a is feasible) BUT they inherit §29's closure that they cannot
substantively move I4 alone. §105 acknowledges (a) is available as a future
augmentation but does NOT promote S4 corpus to a primary §105 lever.

### 4.3 Q3 verdict — chosen: hybrid (a) + (c), inherits §29 closure

**S4 corpus form EXISTS** as physics-trace triples (option a feasible, §7-AND
audited), but **STANDALONE CANNOT lift I4 ↑↑** (option c carries §29's
DESIGN-CLOSE verdict). For §105's enhanced design:

- S4-as-corpus = optional augmentation, ≤50,000 records,
- S4-as-training-objective = §92's L_ap, future-cycle trainer concern,
- Q1.I6 (SCoRe gate) remains vacuous-PASS-by-omission per §102.

This is *honest scope*: S4 as corpus is real but limited, not the §105
primary lever.

---

## §5 — Q4 — Q3' on the enhanced corpus design

### 5.1 The 7-gate evaluation

§101's Q3 = G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 ∧ G6 ∧ G7. Evaluating each gate on the
§105 enhanced design state (NOT on a built artifact — that's §106 if §105
holds):

| Gate | Evaluation | Reason |
|---|---|---|
| **G1** §7-gate passes | ✅ | §105 enhanced sources still drawn from §101's 5 legitimate sources only. S2 expansion via (a)+(c) inherits §7-AND; S3 omitted; S4 optional corpus form inherits §92/§7-AND. |
| **G2** §93 four conditions encoded | **❌** | I1 ✅ (S1 byte-equal prefix preserved) · I3 ✅ (forbidden-token grep=0 by construction) · I4 ↑↑ **(design-level feasible)** but Q4 evaluates *the design's encoding* of cond-3, which is satisfied if a future build achieves it; HOWEVER cond-2 (per-record physics filter §1.3) requires actual filter implementation at build-time. I6 ✅ (vacuous-PASS via S4 omitted from primary corpus). HONEST: I4 ↑↑ design-level passable; cond-2 implementation pending; the OVERALL G2 evaluates only if all 4 conds are substantively encoded. §105 design encodes 3/4 substantively (I1 byte, I3 by construction, I4 by Q1 chosen growth) but cond-2 is implementation-deferred. Honest verdict: G2 = N at §105 design-tier, would become Y at §106 build-tier with cond-2 implementation. |
| **G3** §62 echo-chamber guard armed | ✅ | S3 omitted → guard armed vacuously, identical to §102. |
| **G4** Q2 measurable on result.json schema | ✅ | §101 §2.3 predicate is closed-form on result.json fields; independent of corpus content; carries unchanged. |
| **G5** 5 levers preservable single-variable | ✅ | §105's variable is "S2 expanded composition" + optional "S4 added"; trainer config preserved at §16-Dir-I baseline; no new mechanism stacked. |
| **G6** ΔI/Δ$ ≥ info-floor | ✅ | Same as §101 §3.3 — Q2 was never decided, ΔI = 1 bit a priori, Δ$ ≈ $0.4-0.8 (S2 1M records adds ~340 MB build storage but no fire cost), floor 1 bit / median fire cost = 2.5 bit/$, ΔI/Δ$ = 1/0.4 = 2.5 → at floor. |
| **G7** anti-§94 single-variable | ✅ | §105 enhances corpus only, NO new mechanism. Trainer config = §16-Dir-I-baseline-preserved unchanged. |

**Q3' on §105 enhanced design = G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 ∧ G6 ∧ G7 = ✅ ∧ ❌ ∧ ✅ ∧ ✅ ∧ ✅ ∧ ✅ ∧ ✅ = FALSE**

### 5.2 Why N is the honest answer (and is valuable)

The G2 failure is NOT because §105's design is wrong. §105 design *projects*
that I4 ↑↑ is achievable when built (Q1's 1M records × ~340 bytes/record),
but the actual cond-2 (per-record physics filter) implementation is deferred
to a future §106 build cycle. §105 is DESIGN-TIER; a design cannot fully
encode an implementation-time predicate.

This is the §101 design-OPEN pattern repeated one layer deeper. §102 closed
design-OPEN at the BUILD layer (I4 measured ↑↑ was not achievable at the
build's $0 scale). §105 closes design-OPEN at the DESIGN-OF-BUILD layer
(I4 design-level achievable, but cond-2 implementation still pending).

This is the §15 / §51 / §72 milestone discipline carried forward: GOAL is
not reached, but the boundary is mapped precisely. §105's valuable
contribution is to say:

- Q1: 10³× S2 scale IS achievable at $0 via (a)+(c) compositional growth.
- Q2: S3 unblock is NOT achievable at $0 design-tier (echo-collapse is
  fire-tier OUTCOME).
- Q3: S4 corpus form EXISTS but is §29-closed standalone.
- Q4: G2 still fails because cond-2 (per-record physics filter implementation)
  is a build-time concern.

The boundary is now: a future §106 cycle that (i) implements the Q1 (a)+(c)
compositional generator + (ii) implements cond-2 per-record filter + (iii)
builds the corpus + (iv) re-evaluates Q3 has a credible chance of returning
Y on I4 ↑↑.

### 5.3 What §105 does NOT claim

§105 does NOT claim that a 1M-record S2 will pass I4 ↑↑ in any future build —
that requires a future cycle's actual measurement. §105 does NOT claim that
passing I4 will produce GOAL emergence — that requires a fire on the built
corpus AND the fire result on THRESHOLD_CROSSED. §105 maps the design;
empirical OUTCOME is per B-S105-NOTE / B-D-NOTE / B-EMERGE-7 family.

§104 (parallel sibling) takes the I4-refine path: instead of expanding S2,
restate I4 as a fire-tier predicate. Both §104 and §105 are valid responses
to §102's open boundary; both produce design-OPEN at their respective layers.

---

## §6 — ASCII diagram

```
                              GOAL: anima spontaneously speaks from own physics
                              §15/§51/§72 milestones (UNCHANGED, 미도달)
                                              │
                                  §99 / §100 / §101 / §102 carry
                                  (§102: built CORPUS_S101, Q3=N on I4 failure)
                                              │
                          ┌───────────────────┼───────────────────┐
                          │                                       │
                  §104 sibling                              §105 (this cycle)
                  I4-refine path                            corpus-enhancement path
                  (restate predicate)                       (expand sources honestly)
                          │                                       │
                          ▼                                       ▼
                  Q4 verdict on                            ┌──────────────────┐
                  refined-predicate                        │  Q1 (S2 scale)   │ ✅ (a)+(c) 1M records ≥10³×
                  evaluation                               │  Q2 (S3 unblock) │ ⚠ honest-OPEN (FIRE-tier)
                                                          │  Q3 (S4 corpus)  │ ⚠ hybrid (a)+(c) §29-closed
                                                          │  Q4 (Q3' eval)   │ ❌ G2 fails (cond-2 impl)
                                                          └──────────────────┘
                                                                  │
                                              ┌───────────────────┴───────────────────┐
                                              ▼                                       ▼
                                       Future §106 cycle:                       Honest design-OPEN:
                                       implement (a)+(c) generator             §105 maps boundary that
                                       + cond-2 filter                          remains;
                                       + build CORPUS_S106                      §1.1 not closed by §105 alone
                                       + re-evaluate Q3'
```

---

## §7 — Honest C3 caveats (≥10)

1. **§105 is design-tier — it builds nothing and fires nothing.** g3 carries:
   design ≠ build ≠ fire ≠ emergence. North-star + §15/§51/§72 milestones
   UNCHANGED, GOAL 미도달. §105 design holds is NOT a claim that GOAL is
   closer; it's a claim that the boundary is mapped.

2. **Q1's (a)+(c) projects 1M records but DOES NOT prove I4 ↑↑.** A future
   §106 build cycle must actually generate the records and measure
   diversity_coeff. §105 does NOT claim "this design WILL pass I4"; it claims
   "this design *can in principle* pass I4 at design-level cardinality 1M".

3. **The 14×14 (Ψ-band, tension-band) deterministic grid for M=200
   perturbations is judgement, not derived.** Other grid sizes (10×10=100,
   16×16=256, 12×16=192) are equally legitimate. §105 chose 14² to hit ~200
   per (anchor, framing). The specific grid shape isn't load-bearing.

4. **Option (b) anchor expansion deferred but not closed.** Adding 1,500 new
   anchors is feasible per B-UBM-1/2 but value-questionable without per-anchor
   unique content. §105 picks (a)+(c) instead because compositional growth
   per existing anchor is closer to substrate-natural; future cycles may
   reconsider (b).

5. **Q2's honest-OPEN is the §62 boundary, NOT a §105 limitation.** §105
   could "manufacture" S3 inclusion at $0 (e.g., LCG stub traces with
   trivial guard) but that would weaken the §62 echo-collapse evidence base.
   §105 chooses honest-OPEN as the higher-value design.

6. **Q3's S4-corpus inheritance of §29 closure means S4 records are
   generatable but limited.** §29 proved (B-PTD-2) the K-complexity bound;
   §105 inherits this. S4 as corpus is real but auxiliary.

7. **G2's failure on §105 enhanced design is cond-2 (per-record physics
   filter) implementation, NOT I4 itself.** The honest read: I4 ↑↑ is
   *design-level passable* under §105's (a)+(c) growth; cond-2 is a separate
   implementation concern. §105 design-OPEN respects this distinction.

8. **§105 does NOT challenge §101's predicates** (Q1.I1-I7, Q2 axes, Q3 gates).
   They stay byte-exact. §105 designs around them. If a future cycle finds
   the predicates themselves are wrong, that's §107+ work.

9. **§104 (sibling parallel) takes a DIFFERENT valid path** by refining I4
   to fire-tier. §105 and §104 are NOT mutually exclusive; both are valid
   responses to §102's open boundary. The user's `g_all_options_parallel`
   directive applies: explore both.

10. **B-S105-NOTE empirical carve-out**: this design's projections (1M
    records, ≥10³× scale, 340 MB byte-equivalent) are theoretical at design-tier.
    Real build outcomes depend on $0 Mac CPU wall time, byte-encoding choices,
    and actual diversity_coeff measurement on the built byte stream. §105's
    battery proves the DESIGN-OF-BUILD is structurally honest, NOT that
    the built artifact will pass any specific gate.

11. **§29 closure is INHERITED, not RE-OPENED.** §105 does not claim S4 as
    standalone corpus crosses §1.1; §29 already closed that. §105 respects
    §29 and chooses S4 as auxiliary supplement, not primary diversity lever.

12. **§62 closure is INHERITED, not RE-OPENED.** §105 does not claim S3
    inclusion at $0 build-tier is safe; §62 already showed trained dual-anima
    cells collapse. §105 respects §62 and chooses S3 omitted, marking
    design-OPEN at corpus-level for a future trained-ckpt cycle.

13. **The cycle that constructs the §105 corpus is a separate §106 cycle.**
    §105 has NOT generated any new byte streams. Q1 specifies the construction
    predicate ($0); the construction itself is a cost-bearing pre-fire build
    step (probably $0-Mac-CPU non-trivial wall time, ~3-5 hours for 1M records)
    that a future cycle owns. §106 must re-evaluate FIRE_DECISION on the
    *constructed* state — corpus construction can fail any G_i.

---

*End §105 DESIGN.md.*
