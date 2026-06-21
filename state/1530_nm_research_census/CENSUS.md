# H_1530 — NEUROMODULATION-WALL escape: mechanism-FAMILY research census

> 📋 RESEARCH-CENSUS (no measurement — a lever map, not a verdict). Cited, ranked.
> Goal: census untried mechanism-FAMILIES that could break the **H_1284 NEUROMODULATION wall**.
> Lens discipline: `a_no_llm_frame_trap` (biology-first), `a_break_the_wall` (family taxonomy), c23 (no black-box sweep).

## 1. The measured root cause (what the wall actually IS)

H_1284 and its 10+ confirming lenses (`H_1284` global-gain · `H_1284_R3` regime-switch ·
`H_1422` 3 state-contingent lenses ACh/NE/DA · `H_1425` orthogonal ideation-temperature ·
`H_1509/b/c` Amoeba allosteric-buffer · `H_1523` multi-timescale · `H_1524` diversity ·
`H_1525` predictive · `H_1526` emit-gate) all measured the SAME structural ceiling:

> **The recall capability is bounded by key-GEOMETRY / capacity, NOT the operating-point
> schedule.** On a key-addressed store the abstain decision IS ALREADY a threshold on the live
> recall-margin, so any neuromodulator conditioning a knob (LR / SPLIT_THRESH / temperature /
> abstain-margin) on that SAME margin is **circular** — it re-partitions the margin axis but
> cannot beat the single best fixed partition. **A single tuned fixed point dominates every
> controller.** (verbatim H_1422 finding; H_1526 reproduced it on the last geometry-free knob.)

**Implication for the escape (the load-bearing constraint):** lift requires a mechanism that
acts on a signal/axis **ORTHOGONAL to the abstain margin** — i.e. one that changes WHAT
geometry/capacity is available, or WHAT gets stored — NOT one that re-schedules an operating
point on the existing geometry. **Every controller-family lens fails because it lives on the
margin axis. The escape MUST leave that axis.**

## 2. Family taxonomy (tried vs untried)

| family | acts on | tried? | status |
|--------|---------|--------|--------|
| **controller / operating-point** (gain · LR · timescale · diversity · predictive · emit-gate · allosteric buffer) | a knob ON the existing geometry | ✅ exhausted (10+ lenses) | 🧱 INERT — circular w/ abstain margin |
| **representation-geometry modulation** (ACh sharpening, normalization) | the encoding map / decorrelation | 🟡 sibling H_1527 testing | orthogonal-candidate |
| **adaptive capacity / neurogenesis** (add units, expand store) | number of cells (raw count) | ✅ sibling H_1528 LANDED | 🧱 WALL HELD — raw cell-COUNT is a monotone resource, no regime-dependent optimum for a SCHEDULE to exploit (best-fixed = grid ceiling everywhere) |
| **ideation-capability** | generative mouth breadth | 🟡 sibling H_1529 testing | orthogonal-candidate |
| **EXPANSION-RECODING / kernel lift** (Marr-Albus, Litwin-Kumar) | input→high-dim sparse map BEFORE store | ❌ UNTRIED | **top orthogonal lever** |
| **multi-store / complementary-learning-systems** (fast↔slow, encode/retrieve split) | WHERE/HOW a fact is held (2 stores) | ❌ UNTRIED | orthogonal lever |
| **metaplasticity / cascade consolidation** (Benna-Fusi) | per-synapse state → capacity over TIME | ❌ UNTRIED | orthogonal lever (capacity-over-time) |
| **active-sampling / curiosity acquisition** (Gottlieb-Oudeyer) | WHAT gets stored (which facts enter) | ❌ UNTRIED | orthogonal lever (input-selection) |
| **objective-modulation** | the loss/criterion the store optimizes | ❌ UNTRIED | orthogonal (out of scope this round) |

The controller family is the ONE the wall is built from. The four UNTRIED families below all act
on an axis the abstain-margin **cannot already see** — which is exactly the H_1422 "NOT RULED OUT"
escape condition.

---

## 3. Mechanism census (cited) — each: mechanism · why it might move a geometry/capacity bound · cheapest falsifiable test

### C1 — EXPANSION-RECODING (kernel lift before the store) ★ top pick
- **Mechanism.** The cerebellar granule layer recodes ~few mossy-fibre inputs into a vastly larger,
  sparse, high-dimensional granule-cell population (Marr 1969 / Albus 1971 codon theory). Theory
  (Litwin-Kumar et al. 2017; Cayco-Gajic et al. 2017; Babadi & Sompolinsky 2014) shows the
  granule→input ratio and the **per-granule fan-in (≈4–5 inputs)** are the values that MAXIMIZE the
  dimensionality of the representation and the downstream learning/pattern-separation capacity. The
  expansion acts as a fixed random nonlinear feature map = a **kernel machine** (Xie et al. 2023,
  eLife; "Cerebellum as a kernel machine", Front. Comput. Neurosci. 2022).
- **Why it can move a geometry-bound capability where controllers can't.** The wall is *key-geometry*
  bounded: two near-collinear keys are unresolvable no matter the threshold schedule. Expansion
  recoding **changes the geometry itself** — it lifts the byte-trigram FNV key into a higher-D sparse
  code BEFORE affinity is computed, *increasing the angle* between previously-collinear keys. This is
  the H_1527 representation-geometry family's strongest concrete instance and is **orthogonal to the
  abstain margin by construction** (it operates one stage upstream of the threshold). NOTE — distinct
  from the now-LANDED H_1528 raw-capacity wall: expansion raises the *dimensionality / angular
  separation* of the code, NOT the cell-COUNT (which H_1528 measured as a monotone resource with no
  regime-dependent optimum). C1 changes the GEOMETRY of a fixed store; H_1528 only changed how MANY
  cells — that is exactly why this lever is still open after H_1528.
- **Cheapest falsifiable test.** CAPABILITY = pair-separation recall on the H_1284 fixture restricted
  to *confusable* near-collinear key pairs (where the wall bites). KNOB = a frozen random sparse
  expansion E: key∈R^d → R^{kd} with per-row fan-in 4–5 + top-k sparsification, inserted before L2
  affinity. FROZEN bar (pre-register, MARGIN=0.05): recall_expand − recall_baseline ≥ +0.05 on
  ≥2/3 seeds on the confusable subset. ABLATION = collapse E to a non-expanding identity-rank map
  (kd→d projection, same param count) → must revert to baseline (proves the lift is the
  dimensionality expansion, not extra parameters). SHUFFLE = permute E's rows per-key → must collapse.
  $0 CPU, engine-native re-score path = the H_1284 harness key geometry.

### C2 — METAPLASTICITY / cascade consolidation (Benna-Fusi) — capacity over TIME
- **Mechanism.** Each synapse carries a cascade of internal states (Fusi-Drew-Abbott 2005;
  Benna & Fusi 2016). Repeated potentiation pushes a synapse DEEPER → it becomes progressively more
  resistant to change (metaplasticity), yielding **power-law (not exponential) forgetting** and
  near-optimal memory lifetime for bounded synapses. Position-in-cascade = a per-synapse timescale.
- **Why it can move a capacity bound.** The wall is a *static* capacity ceiling (fixed store, every
  fact overwrites at the same rate). Cascade states give the store a **graded per-cell consolidation
  axis orthogonal to the recall margin** — a well-grounded repeatedly-confirmed fact resists being
  clobbered by a later confusable fact, which a single global LR/threshold cannot express (controllers
  set ONE rate; this sets per-cell rates by history). Directly attacks the AB-AC interference the
  flat store suffers.
- **Cheapest falsifiable test.** CAPABILITY = retention of an early fact after K interfering later
  facts (interference/retention curve). KNOB = replace each cell's scalar weight with a 2–3 level
  Benna-Fusi cascade variable; consolidation depth = confirmation count. FROZEN bar: retention_cascade
  − retention_flat ≥ +0.05 at the interference horizon, ≥2/3 seeds. ABLATION = freeze cascade depth=0
  (reverts to flat single-timescale store) → must lose the lift. SHUFFLE = randomize which fact gets
  consolidated → collapse. $0 CPU.

### C3 — MULTI-STORE / complementary-learning-systems (fast↔slow; ACh encode/retrieve split)
- **Mechanism.** CLS (McClelland-McNaughton-O'Reilly 1995; Kumaran-Hassabis-McClelland 2016): a FAST
  high-fidelity low-capacity episodic store (hippocampus) + a SLOW generalizing store (neocortex),
  with interleaved replay preventing catastrophic interference. ACh (Hasselmo 1999/2006) **schedules
  encoding vs retrieval** — suppressing recurrent retrieval inputs during encoding so a new fact is
  laid down without interference from old retrievals (representational sharpening of prediction error,
  Audette/elife 2024).
- **Why it can move a capacity/interference bound.** anima has a SINGLE flat store — every fact binds
  at the same rate and competes in one geometry. A second store (or an encode-mode that gates out the
  retrieval path) lets confusable facts be **held in separate substrates / written at separate phases**
  — interference-avoidance that NO threshold-schedule on one store can produce. Note the discipline
  hazard: framed as "ACh modulates a gain" this re-enters the controller family and the wall absorbs
  it (cf. H_1422 ACh lens 🧱). The escape framing is **multi-STORE / phase-SEPARATED writes**, not a
  scalar gain — that is the orthogonal axis.
- **Cheapest falsifiable test.** CAPABILITY = AB-AC interference (learn A→B, then A→C, score A→B
  retention). KNOB = add a small fast episodic store written in an "encode phase" with the
  retrieval/recurrent path suppressed (Hasselmo encode-mode), slow store consolidates by replay.
  FROZEN bar: A→B retention_2store − retention_1store ≥ +0.05, ≥2/3 seeds. ABLATION = merge the two
  stores / disable phase-separation → reverts to single-store interference. SHUFFLE = randomize
  store-assignment → collapse. $0 CPU.

### C4 — ACTIVE-SAMPLING / curiosity acquisition (Gottlieb-Oudeyer) — changes WHAT is stored
- **Mechanism.** Active sampling / learning-progress curiosity (Gottlieb & Oudeyer 2018, Nat. Rev.
  Neurosci.; Gottlieb 2023): the agent **selects which inputs to acquire** to maximize information
  gain / reduce uncertainty; controlled, curiosity-gated acquisition yields faster and more robust
  memory than passive intake.
- **Why it can move a geometry bound.** All prior lenses took the input STREAM as fixed and tuned a
  knob. This family changes the **input distribution that the geometry must encode** — by preferentially
  storing high-information / margin-disambiguating facts (and skipping redundant near-duplicates that
  crowd the geometry), it improves the *effective* separability of the store without touching the
  threshold. Orthogonal to the abstain margin: it acts at acquisition time, before any recall.
- **Cheapest falsifiable test.** CAPABILITY = recall over a budget-limited store (can hold only N<all
  facts). KNOB = curiosity-gated admission: store a fact iff its key-novelty / expected info-gain
  exceeds an adaptive threshold (skip redundant collinear duplicates). FROZEN bar: recall_curiosity −
  recall_FIFO/random-admission ≥ +0.05 at fixed budget N, ≥2/3 seeds. ABLATION = random admission at
  the same budget → must lose the lift (proves selection, not capacity). SHUFFLE = permute info-gain
  scores → collapse. $0 CPU. (Lower break-prob than C1/C2 because it helps under a CAPACITY budget,
  less so when the store already holds everything — scope-limited.)

### (context) ACh representational-sharpening & attention-as-normalization
- Reynolds & Heeger (2009) normalization model of attention = gain-ON-representation. Cited for
  completeness: as a pure gain it is **controller-family → wall absorbs it** (H_1422 precedent). Only
  enters the escape set if recast as the C1 expansion (sharpening = increasing angular separation),
  which C1 already captures. Not ranked separately.

---

## 4. Ranking (a-priori break-probability × cheapness-to-test) → next-round implement specs

| rank | candidate | family | break-prob | cheap | why ranked here |
|------|-----------|--------|-----------|-------|-----------------|
| **1** | **C1 expansion-recoding** | geometry | HIGH | $0 CPU | attacks the EXACT measured bottleneck (key-geometry collinearity) one stage upstream of the margin; strongest theory (Litwin-Kumar dimensionality-max); clean expand-vs-rank ablation |
| **2** | **C2 cascade metaplasticity** | capacity-over-time | MED-HIGH | $0 CPU | gives per-cell consolidation the flat store lacks; directly targets AB-AC interference; clean depth=0 ablation |
| **3** | **C3 multi-store / encode-retrieve split** | multi-store | MED-HIGH | $0 CPU | only family that lets confusable facts live in SEPARATE substrates; strong CLS precedent; risk = must avoid the gain re-framing the wall absorbs |
| **4** | **C4 curiosity acquisition** | active-sampling | MED | $0 CPU | changes WHAT is stored; clean random-admission ablation; scope-limited to capacity-budget regime → lower a-priori |

### Next-round implement specs (concrete, ablation-bearing — to feed the implement lanes)

**SPEC-1 (C1) — EXPANSION-RECODING pre-store kernel lift.**
- capability: confusable-pair separation recall on the H_1284 fixture (near-collinear key subset).
- knob: frozen random sparse expansion E (R^d→R^{kd}, fan-in 4–5, top-k sparsify) before L2 affinity.
- frozen bar: recall_expand − recall_baseline ≥ +0.05, ≥2/3 seeds, on the confusable subset (MARGIN=0.05).
- ablation: rank-collapse E→identity-rank d-projection (same params) reverts; SHUFFLE rows → collapse.
- source: Marr 1969 / Albus 1971; Litwin-Kumar et al. 2017; Babadi & Sompolinsky 2014; Xie et al. 2023.

**SPEC-2 (C2) — CASCADE metaplasticity store.**
- capability: early-fact retention after K interfering facts (retention/interference curve).
- knob: per-cell 2–3 level Benna-Fusi cascade variable; consolidation depth = confirmation count.
- frozen bar: retention_cascade − retention_flat ≥ +0.05 at the interference horizon, ≥2/3 seeds.
- ablation: freeze cascade depth=0 → flat single-timescale store; SHUFFLE which fact consolidates → collapse.
- source: Fusi-Drew-Abbott 2005; Benna & Fusi 2016.

**SPEC-3 (C3) — MULTI-STORE encode/retrieve-separated CLS.**
- capability: AB-AC interference (A→B retention after learning A→C).
- knob: fast episodic store written in an encode-phase (retrieval path suppressed, Hasselmo), slow store via replay.
- frozen bar: A→B retention_2store − retention_1store ≥ +0.05, ≥2/3 seeds.
- ablation: merge stores / disable phase-separation reverts to 1-store; SHUFFLE store-assignment → collapse.
- source: McClelland-McNaughton-O'Reilly 1995; Kumaran-Hassabis-McClelland 2016; Hasselmo 1999/2006.

**SPEC-4 (C4) — CURIOSITY-gated acquisition.**
- capability: recall under a fixed store budget N<all facts.
- knob: admit a fact iff key-novelty / expected info-gain > adaptive threshold (skip redundant collinear dups).
- frozen bar: recall_curiosity − recall_random-admission ≥ +0.05 at budget N, ≥2/3 seeds.
- ablation: random admission @ same budget reverts; SHUFFLE info-gain scores → collapse.
- source: Gottlieb & Oudeyer 2018; Gottlieb 2023.

---

## 5. Honest scope / discipline

- 📋 RESEARCH-CENSUS only — NO measurement, NO verdict. This is a lever map (coordinates), not a result.
- All four candidates are UNTRIED FAMILIES distinct from the exhausted controller family and from the
  sibling structure lanes H_1527/1528/1529 (which this census's C1 directly reinforces and sharpens).
- Each spec is $0-CPU / mini-safe, engine-native re-scorable on the H_1284 harness key geometry,
  frozen-first, with a teeth-bearing ablation + shuffle (c9, `a_break_the_wall` type-(d) only after
  ablation survives).
- Discipline hazard flagged: C3's ACh component MUST be implemented as multi-STORE / phase-separated
  writes, NOT a scalar gain — the gain framing re-enters the controller family the wall already absorbs
  (H_1422 ACh lens 🧱).

## Sources
- Marr 1969 / Albus 1971 codon theory; Sanger et al. 2020 (J. Physiol.) "Expansion coding 50 years after Marr-Albus".
- Litwin-Kumar et al. 2017; Cayco-Gajic et al. 2017; Babadi & Sompolinsky 2014 (granule fan-in / dimensionality-max).
- Xie et al. 2023 (eLife) "Task-dependent optimal representations for cerebellar learning"; "Cerebellum as a kernel machine" Front. Comput. Neurosci. 2022.
- Fusi, Drew & Abbott 2005 "Cascade models of synaptically stored memories"; Benna & Fusi 2016 "Computational principles of synaptic memory consolidation" (Nat. Neurosci.); Fusi 2021 "Memory capacity of neural network models".
- McClelland, McNaughton & O'Reilly 1995 (CLS); Kumaran, Hassabis & McClelland 2016 "What Learning Systems do Intelligent Agents Need? CLS updated".
- Hasselmo 1999 (TiCS) "Neuromodulation: acetylcholine and memory consolidation"; Hasselmo 2006 "The role of acetylcholine in learning and memory".
- Aimone, Wiles & Gage 2009; Aimone, Deng & Gage 2010/2011 "Adult neurogenesis: integrating theories and separating functions" (pattern-separation, with the neurogenesis-paradox caveat).
- Gottlieb & Oudeyer 2018 (Nat. Rev. Neurosci.) "Towards a neuroscience of active sampling and curiosity"; Gottlieb 2023 "Emerging Principles of Attention and Information Demand".
- Reynolds & Heeger 2009 "The normalization model of attention" (context only — gain-on-representation).
