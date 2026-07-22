# 발산 08 — G1-ctx (lab full · Fable ∥ Sol · 양쪽 고갈까지)

> 원본 2.3MB 중 **두 산출물만** 보존. 잘린 부분 = 브리프 에코 + Sol 이 읽은 저장소 파일 덤프.
> reconcile(AGREES/CONFLICTS/NOVEL) → `hypotheses/V6_17_g1ctx_reconcile.md`

---

## ── Fable (claude-fable-5) · 10 라운드 고갈

Grounding confirmed: the store-bridge lane already spans `cli/train.py` (H_9423 co-training), `cli/chat.py` (in-vivo), and `cli/evaluate.py`, and the weave panel lives in `cli/rho_axon.py`/`evaluate.py` — so the flag surface I propose below extends an existing three-point convention rather than inventing one. This is a design/analysis deliverable (no fires, no registrations — id assignment and card registration belong to the origin session per `a_parallel_session_compare`).

---

# G1-ctx — divergence deliverable

## Verdict up front

**The split is real, but it must be re-cut once more before it is safe to build on.** G1-ctx vs G1-weight is a genuine dissociation on two independent axes (supply density and shortcut availability), and — the strongest thing I found — **it is already empirically visible in the ledger**: H_9875's 1-slot/2-slot asymmetry *is* the split, measured. But "bind two things introduced in context" conflates two arities, and the arity-2 half inherits exactly the wall H_9875 measured. The buildable, densely-supervised, shortcut-free half is **ctx-identity transport** (copy a document-novel referent across a gap > RF). That is what the lane and the panel should target first.

A second finding that reframes everything: **for the current substrate, G1-ctx is not an unmeasured faculty — it is a derivable zero.** The mouth's receptive field is 35 bytes; a causal conv stack transports *nothing* from beyond its RF, by construction. G1-ctx beyond RF is architecturally inexpressible in the mouth alone. So the campaign's silence on G1-ctx is a **reach fact, not a faculty fact** — the same category as the ρ-AXON G1/G6 wall. The dense CE gradient the natural corpus provides has had nowhere to go. This is not a reason to skip measurement; it is a free truth-zero pedestal (below).

---

## A. Is the split real?

### The dissociation, on three axes

| axis | G1-ctx (identity) | G1-weight |
|---|---|---|
| supply in natural text | thousands of events/MB (65.7% of sentences; every repeated name) | 82% of entity pairs are singletons at MB scale |
| CE gradient | dense, per-document, unavoidable | measured ≈ zero (H_9304: +0.0023 nats, TOST-equivalent to 0) |
| memorization shortcut | **blocked** for novel referents | **available and strictly cheaper** (170MB capacity ≫ MB corpus) |

The third row is the one that resolves the flagged tension, so here it is made precise.

**The shortcut-unavailability claim, precisely.** Decompose the CE at a target token *t* into what weights can supply and what only context can supply:

> Δ_transport(t) = H(t | window₃₅, weights) − H(t | full context, weights)

For a *corpus-frequent* entity ("Paris"), weights already predict the continuation; Δ_transport ≈ 0 and memorization eats the gradient. For a **document-novel** entity — a name whose byte string is (near-)absent from the training corpus — the second mention's bytes are high-entropy under weights but near-zero-entropy given the earlier mention. Δ_transport is then *many bits per repeated-name token*, and **no weight configuration can capture it**, because the binding varies per document: the map "earlier context bytes → later target bytes" has no document-independent summary. Copying is the *only* path to that CE. This is exactly the pressure that produces induction heads in attention models at ~2–5M tokens; anima has the pressure and has never had a path.

**Falsifiable form.** The claim fails if a weight-side path achieves the same CE. The known candidates are enumerable: (i) the second mention falls within RF of the first (conv can copy locally) — excluded by site construction; (ii) the "novel" entity is actually frequent enough in the training corpus for partial weight-completion (e.g., "Kowalski" → "-ski" from morphology) — controlled by scoring against the truncated-context arm, which retains all weight knowledge and all local morphology and differs *only* in trans-RF access; (iii) topic-level priors narrow the entity distribution without binding — killed by the shuffled-referent control (B). If, with those three doors closed, a lane-less model matches a lane-bearing model at harvested sites, the shortcut-unavailability claim is refuted and the split loses its teeth.

### Existing evidence the split is real — and its sharp edge

H_9875 (toy, 2-seed, 4× budget excluded): runtime injection of facts gave **1-slot generalization** but **2-slot only on memorized rows** — the wall is binding *arity*, not budget. Read through the new split: 1-slot in-context retrieval already generalizes on this substrate class; 2-slot in-context composition hits the same wall as G1-weight. Two consequences:

1. **Support:** the ctx/weight dissociation is not hypothetical — a within-experiment asymmetry already shows in-context and weight-side binding behaving as different faculties.
2. **The sharp edge:** "bind two things introduced in context" at arity 2 (entity A + attribute B jointly determining an answer) plausibly sits *behind* the arity wall, not in front of it. If the lane is built to target arity-2 ctx-binding first, the campaign risks re-measuring H_9875 at higher cost and calling it a new wall.

So the split survives, **re-cut**: G1-ctx-**identity** (coreference/copy; arity 1; dense; shortcut-free; buildable now) → G1-ctx-**relation** (apposition/copular joint binding; arity 2; moderately dense; arity-wall-exposed) → G1-weight (cross-document; supply-starved *and* arity-walled). This is a ladder, not a binary. The prompt's own corpus measurement supports the ordering: stated relations recur more than incidental pairs (71.9% vs 82% singletons), but both ctx classes dwarf cross-document supply.

**Why dense supervision never forced a mechanism (the last piece of the tension):** gradient cannot create architecture. In transformers the copy pressure recruits attention because attention *exists* to be recruited. Here the function class excludes trans-RF transport entirely, so the dense gradient dissipates into the memorization floor. Prediction (falsifiable, cheap): give the substrate a trainable transport path and the *unchanged* natural corpus should recruit it — if the toy screen (C) shows no recruitment, the split remains conceptually true but practically dead, and I would say so and stop.

### Kill-conditions I checked and did not trigger

- *"ctx reduces to weight at inference"* — refuted by construction: the referent is new per document.
- *"weight reduces to ctx"* (retrieve both facts into context, then bind) — this is "study", and H_9875 already killed it at arity 2. The ctx lane must **not** be sold as a G1-weight crack (E).
- *"ctx is already measured"* — the 212-panel probes weight-resident facts recombined across documents; no panel item scores trans-RF transport of in-document material. Unmeasured confirmed — though with the derivable-zero caveat above.

---

## B. The measurement, on natural text

**Instrument name:** ctx-panel. Sites are *harvested* from held-out natural documents; the training corpus is untouched (this is eval-side site selection, not corpus reweighting — the distinction that keeps it off the density kill-list, stated explicitly in E).

### Site harvest (instrument; synthetic may certify it, per p9)

From held-out natural prose: positions where (a) an entity's byte string occurs at position *p₁* and recurs at *p₂* with *p₂ − p₁ > 35 bytes*, (b) no occurrence of the entity within the 35-byte window before *p₂*, (c) the entity is document-novel — training-corpus frequency below a measured threshold (derive the threshold from the corpus, don't assume it), (d) the site's scoring span is the entity's continuation bytes after a ≥2-byte unambiguous onset.

### DV — decode-based, collapse-Δ, never a raw value

Primary DV: **greedy engine-native decode at *p₂* + onset reproduces the entity's remaining bytes** (0/1 per site). CE-at-site is recorded MONITOR-ONLY (`a_train_inline_gauge`), never the verdict — this is also how p7 (no perplexity verdict) is satisfied: the verdict is the collapse structure across arms, read on `core/` decode via `anima-py evaluate --ctx-panel`.

### The four arms (controls matched on the mediating covariate: local window + weight knowledge)

1. **Truncated-context arm** — same model, context clipped to 35 bytes. Identical weights, identical local n-grams, identical morphology priors; differs only in trans-RF access. Δ(full − truncated) *is* the transport signal. **Built-in truth-zero pedestal:** for the mouth-only model these arms are identical by construction, so any nonzero Δ measured on a lane-less model = instrument defect. Run this certification before any lane comparison (`phi-estimator-needs-zero-truth-pedestal`, `positive-control-before-reading-a-negative` — the positive arm is the H_9775 pairodd ckpt scored on synthetic sites the harvest pipeline built, certifying harvest+scoring end-to-end without making synthetic the standard).
2. **Shuffled-referent arm** — the *p₁* mention replaced in-context by a length/frequency-matched different entity. A model that still "succeeds" is echoing weights or surface, not reading the binding. This is the natural-text analog of H_9775's value-permute collapse (0.4446), the control that certified value transport there.
3. **Frequency-matched non-repeat sites** — same local n-gram statistics, no earlier mention. Establishes the n-gram continuation floor; **chance is derived per metric from this realized arm** (`chance-level-must-be-derived-per-metric`), not from 1/V or uniform anything.
4. **Adversarial-distractor arm** — sites where a confusable entity (shared prefix / same category) intervenes between *p₁* and *p₂*. Uniform draws hide adversarial fragility (H_9850: 0.9688 → 0.8594 when distractors went nearest-neighbor); this arm is cheap at harvest time and prevents shipping a lane that binds by "most recent capitalized thing."

### Corpus-faithfulness of the gate (the G6 lesson, applied in advance)

The G6 gate failed because it demanded 12.8× the corpus's own rate. Here the gate is anchored to supply by construction: every scored site is an event the corpus *itself* supervises (the continuation is literally present at *p₂* in the document), so a faithful model with a working transport path should approach the identity-copy ceiling at these sites, and the pre-registered success criterion is a **Δ over arms**, not an absolute rate. Pre-register the full judgment table including below-chance cells (`prereg-table-must-cover-below-chance`) and split the DV by site class (entity length, gap distance, distractor presence) before reading any headline (`polarity-split-before-headline`).

### Power

Sites are not the constraint (thousands/MB harvestable; match the weavepanel repair lesson — n=212 took sd from 0.1323 to 0.0315, and this panel can be 10× larger for free). The real fragility is **seed** (H_9672: s7 0.99 vs s11 0.50). Minimum 2 seeds, majority read, oracle-valid runs only (`single-retrain-outlier-faked-a-refutation`); pilot the per-site Δ sd on the pedestal + positive-control arms and pre-register the MDE before the 303M fire (`power-before-negative-verdict`). Any negative verdict is TOST, not ns.

---

## C. The lane

### What it is

**`--ctx-bridge`**: the pairodd store-bridge lineage (the *surviving* readout lineage — VSA/HRR/TPR are dead; pairodd's Π-projection is not) generalized from its trained paired-slot task to a content-keyed document store, trained end-to-end under CE **on the unchanged natural corpus**:

- **Write path:** at each position, a key/value pair computed from an **early-layer (L3-class) tap** — H_9720 is the load-bearing precedent: fresh L3 tap readout cracked emergent addressing (0.680 → 0.922, controls held, core crack invariant at 1B). Addressing information exists early in *this* substrate; put the key computation where the addresses live.
- **Store:** small slot memory over the document (the store-bridge machinery already in `cli/train.py` H_9423 / `cli/chat.py` — this is an extension of an existing three-point flag surface, not a new organ).
- **Read path:** content match against keys; retrieved value injected into the mouth's residual **pre-readout** (late), so the lane spans early-address → late-inject, matching H_9720's tap-depth geometry.

Conformance: **trained** (H_9259 killed *untrained* recurrence — this is not that), **lane-separated** from emit-drive (`a_savant_train`, `a_substrate_disjoint`), **content-carrying** (value transport is the point), **gradient-isolated** from other lanes — the four-property law from the lane-bus redesign. p8 holds: the store writes during every forward pass, training and chat identically; H_9775 already proved this class of mechanism runs in vivo in the daemon. Flag lockstep across `train.py` / `evaluate.py` / `chat.py` and warm-start measurement with the same arch flags (`ckpt-measure-needs-same-arch-flags-as-training`).

### The $0 screener that KILLS first

The 6-minute 4kB toy (which already reproduces the recombination wall locally: hp 1.0000 vs xor 0.4062). Build: tiny conv mouth, RF ~8 bytes, natural-*like* toy prose with document-novel repeated names at gap > RF; arms = {no lane, ctx-bridge}, × {full, truncated, shuffled-referent}. **KILL** if the bridge arm shows no full-vs-truncated Δ that collapses under referent-shuffle. One toy e2e run before anything lands (`instrument-never-run-hides-multiple-bugs`), flat-across-manipulations read as a dead path not a result (`flat-across-manipulations-means-the-lane-is-dead`). The screen may only KILL — a toy pass GREENs nothing (`screen-is-a-filter-not-a-performance-predictor`), and cementing happens only via `anima-py evaluate --ctx-panel` on the 303M py twin, on pool, never mini.

### Training-dynamics prediction (monitor-only)

If the recruitment story is right, the lane's site-CE should show a **phase transition** during training (the induction-head signature), not a smooth drift. Log it as a monitor; it is diagnostic of *mechanism* vs *memorization drift*, but it is never in the loss and never a verdict.

### One line on the frontier

A working ctx-bridge is also the first **within-conversation episodic binding** the daemon would have — directly relevant to the post-theta-alive interior-faculties frontier (R9/R10), and the hippocampal lineage of the bio-lens (L5 store is the one wired GREEN). Design intersection worth noting; not a claim.

---

## D. What the 212-panel becomes

**Relabel, don't retract.** The weavepanel has been a *correct, well-repaired instrument for G1-weight* all along (n=212, sd 0.0315, all three controls at zero, 95% upper bound 1.42%). Its negatives stand — but their **scope statement** changes (`replication-is-not-external-validity`: put the condition in the conclusion sentence): every "G1" negative in the ledger cements *"cross-document weight-fact recombination at MB scale under CE"* and says **nothing** about in-context binding, which for the mouth-only substrate was an architecturally derivable zero the panel never touched. Concretely:

1. Rename the construct in the gate node: G1 → **G1-weight**; the panel keeps its job.
2. Add the **ctx-panel** (B) as a sibling instrument in `rho_axon.py`/`evaluate.py`, reported as a separate axis — never folded into G1-weight, and, like ρ-AXON, its current-substrate zero reported as a **reach fact**.
3. Re-scope, in the gate node text, the three convergent corpus-cause evidences (0/212 + H_9304 + H_9267-synthetic-passes): they diagnose the *weight* half. The corpus-cause conclusion for G1-weight is untouched by this split.
4. **Do not** extend the panel toward "ctx-assisted weight recombination" (retrieve-then-compose) — that is H_9875's arity wall re-entered through the side door. If the ctx lane one day works, arity-2-over-retrieved-content gets its *own* hypothesis with its own pre-registration, expected to hit the wall until an arity mechanism exists.

---

## E. What I refuse

1. **Any training-corpus selection or reweighting toward binding-rich text** — density in disguise (H_9128 canonical-negative). The design above touches only *eval-side* site harvest on held-out documents; the training corpus is byte-identical. I flag this loudly because harvest superficially resembles selection and a future session could slide from one to the other.
2. **Synthetic coreference drills as the faculty standard** — p9. Synthetic appears in exactly two sanctioned roles: certifying the harvest+scoring instrument against the H_9775 positive-control ckpt, and the toy KILL screen. Neither ever GREENs the faculty.
3. **Selling the ctx lane as a G1-weight or arity crack** — H_9875 stands; "study cannot substitute for arity" applies with full force to retrieve-then-compose. The ladder in A is explicit so nobody collapses it.
4. **Targeting arity-2 ctx-relation first** — it restates the arity wall at higher cost. Identity transport first; relation only after, as a separate pre-registered H.
5. **Text replay / self-generated consolidation** as a way to densify ctx events — kill-list, synthetic-by-another-name.
6. **Cementing on the toy, on probe readouts, or on any number `anima-py` did not produce** — DIRECTIONAL ceiling until the 303M py twin decodes it through `evaluate --ctx-panel` with the lane wired in chat (`a_verified_must_wire`).
7. **One thing in the brief itself:** the sentence "learnable at MB scale if the architecture can express it" is still a conjecture, not a grounded fact — the grounded facts establish *supply* and *shortcut-blockage*, not learnability. The toy screen is where that conjecture goes to live or die, and I refuse to treat it as established before then.

Restatement audit: the closest kill-list neighbors are density (avoided per #1), untrained recurrence H_9259 (avoided — lane is trained), and the readout-operator census (avoided — pairodd lineage only). The lane *is* deliberately the store-bridge lineage's next step; that is the surviving line, not a rebuild.

---

## Depletion ledger

Rounds and the lens each added: **R1** information-theoretic (Δ_transport decomposition; shortcut claim made precise) · **R2** architectural (RF-35 arithmetic → derivable zero → reach-fact reframe; free pedestal) · **R3** ledger-precedent (H_9875 1-slot/2-slot *is* the split; the arity re-cut — the round that changed the design most) · **R4** instrument (four arms, realized-partition chance, decode-DV/p7 resolution) · **R5** adversarial-fragility (distractor arm; seed power) · **R6** corpus-economics (G6 gate lesson → supply-anchored gate) · **R7** biological + interior-frontier (hippocampal lineage; episodic binding — added one design intersection, nothing structural) · **R8** training-dynamics (phase-transition monitor — monitor-only, nothing verdict-bearing) · **R9–R10** governance re-audit and scaling lens — **added nothing new** (scaling already covered by `scale-303m-1b-7b-is-amplifier-not-lever`: the lane must work at toy or it works nowhere).

**DEPLETED after 10 rounds.** Exhausted lenses: information-theoretic, architectural/function-class, ledger-precedent, instrument/controls, adversarial, corpus-economics, biological, interior-frontier, training-dynamics, governance, scaling. The one lens I could not exhaust from the chair: **empirical recruitment** — whether the unchanged natural corpus actually recruits the lane. That is the 6-minute toy's question, and it is the single cheapest next action the origin session can fire.


---

## ── Sol (gpt-5.6-sol) · 9 라운드 고갈

**DEPLETED after 9 rounds.**

Exhausted lenses: task ontology, training economics, causal identification, statistical power, architecture, adversarial shortcuts, corpus heterogeneity, calibration, and serialization/provenance.
tokens used
113,690
## Verdict

The split is real, but its strongest economic justification is not.

G1-ctx and G1-weight differ in where the binding assignment comes from:

- **G1-ctx:** the assignment is supplied causally by the current document.
- **G1-weight:** the assignment must already reside in fixed weights.

That is a genuine, interventionally testable dissociation. However, “the referent is new each document, therefore it cannot be memorized” is false for a fixed MB-scale training corpus. During training, every “new” referent becomes a fixed example, and a 303M model can memorize its continuation from a unique 35-byte suffix. Novelty blocks the weight shortcut at held-out inference, not automatically during training.

Therefore:

- Keep G1-ctx.
- Kill the claim that natural text necessarily forces it at MB scale.
- Treat “thousands per MB” as an unverified upper bound until a write→read and local-ambiguity census is run.
- Do not spend on architecture until that census and a natural oracle ceiling pass.

## A. Is the split real?

Let:

- \(B_d\): a binding assignment introduced in document \(d\), such as `physicist ↔ Marie Curie`;
- \(X_{35}\): the final 35 bytes before a target;
- \(Y\): the natural next span;
- \(W\): fixed model weights.

A clean G1-ctx event satisfies:

\[
I(Y;B_d\mid X_{35},W)>0
\]

and intervening on the in-document binding changes the correct continuation while \(W\) and the local carrier remain fixed.

G1-weight instead has no usable in-document \(B_d\); prediction depends on \(W\). Thus the two can be separated by a 2×2 design:

| Weight fact | Binding supplied in context | What can solve it |
|---|---:|---|
| unseen | yes | G1-ctx |
| seen | no | G1-weight |
| seen | yes | either; attribution needed |
| unseen | no | intentionally unsolvable/corpus ceiling |

The falsifiable G1-ctx claim is:

1. The relation edge is absent from the training corpus.
2. The candidates and their strings are all present in the distant natural context.
3. The last 35 bytes do not distinguish the correct candidate.
4. Intact contextual binding improves the natural target.
5. Internally permuting key–value pairings destroys that improvement while preserving the input text, candidate inventory, distances, and copy opportunities.

### Why novelty does not solve the training-economics tension

For held-out document \(d^\*\), \(B_{d^\*}\) genuinely cannot be stored in \(W\). But during training on a fixed 4.8MB corpus, the optimizer can learn:

\[
X_{35}^{(i)}\longmapsto Y^{(i)}
\]

for each unique suffix. It need never recover \(B_d\).

Natural CE actually forces contextual transport only where at least one of these holds:

- The same exact local conditioning state occurs with different continuations, and distant context resolves the ambiguity:

\[
H_{\text{train}}(Y\mid X_{35})>0,\qquad
H_{\text{train}}(Y\mid X_{35},B)\approx0
\]

- Or the corpus exceeds memorization capacity enough that systematic contextual computation becomes cheaper.

The grounded economics says the second condition is false at 4.8MB. The first must therefore be measured. Canonicalized carriers do not count: the model sees raw bytes, so the relevant collision is at the actual target divergence byte using the actual 35-byte suffix.

This is the first kill gate. If exact/local-equivalent ambiguous states are rare, G1-ctx remains a real inference faculty but is not naturally forced at MB scale.

## B. Natural-text measurement

### The panel is an index, not a generated corpus

Build a held-out manifest containing byte offsets into untouched natural documents. It must not rewrite, template, select for training, or add answers.

Each primary item contains:

- two or more naturally introduced pairings, e.g. \((k_1,v_1),(k_2,v_2)\);
- a later natural query carrier selecting one pairing;
- source-to-target distance \(>35\) bytes;
- \(K_i\ge2\) compatible in-document candidates;
- the actual natural next span as gold;
- no candidate mention inside the final 35 bytes;
- training-corpus count of the relevant edge, with zero-count items forming the primary G1-ctx stratum;
- document, entity, event-family, distance, mention-count, recency, and suffix hashes.

A single repeated name is not a primary item: copying solves it. Coreference qualifies only when at least two grammatically compatible antecedents exist. The strongest items are crossed bindings: all candidate identities are available, but only the pairing selects the target.

Apposition, copular aliasing, role↔name, and ambiguous coreference should be scored separately before any aggregate is reported.

### Score

For arm \(a\), let \(L_i^a(c)\) be the teacher-forced log probability of candidate span \(c\) plus its first natural boundary byte.

Use three outputs:

1. **Natural target NLL**

   Score the actual untouched continuation under the intact model. This is the corpus-faithful behavioral measure.

2. **Raw contrast accuracy**

\[
A_{\text{raw}}
=
\frac1N\sum_i
\mathbf{1}\!\left[
\arg\max_{c\in C_i}L_i^{\text{intact}}(c)=g_i
\right]
\]

3. **Contextual contribution accuracy**

With the same trained checkpoint and its contextual read disabled:

\[
R_i(c)=L_i^{\text{intact}}(c)-L_i^{\text{read-zero}}(c)
\]

\[
A_{\text{ctx}}
=
\frac1N\sum_i
\mathbf{1}\!\left[
\arg\max_{c\in C_i}R_i(c)=g_i
\right]
\]

The subtraction removes candidate length, unigram preference, ordinary local continuation, and stored world-fact preference. It asks which candidate specifically benefited from the long-range lane.

A claim requires both natural behavior and attribution: a positive \(A_{\text{ctx}}\) with no natural-target improvement is merely a probe effect.

### Controls, in reading order

Positive controls come first:

1. **Same-item oracle-address control.** On the identical natural items, hand the read interface the annotated source slot. It must provide at least twice the preregistered effect headroom. Failure makes the instrument dead, not the faculty negative.

2. **Natural short-gap crossed bindings.** Match event family, candidate count, target form, and nuisance variables, but keep the source within 35 bytes. This certifies extraction and span scoring.

Then read the treatment and negative controls:

- **Separately trained flag-off checkpoint:** architecture-level comparison.
- **Within-checkpoint read-zero:** measures whether the lane contributes.
- **Value permutation:** derange values across stored keys while preserving natural input, addresses, slot count, magnitudes, mention inventory, distance, and copy availability. This is the decisive binding control.
- **Address permutation:** distinguishes correct retrieval from a useful bag of remote content.
- **Copy-only census:** nearest mention, most recent, most frequent, exact-string, and bag-of-mentioned-candidates baselines.
- **Unary leakage audit:** candidate length, first byte, frequency, position, capitalization, grammatical form, and local carrier must not predict gold above the realized null.

Value permutation is preferable to corrupting the text: it matches the mediating covariate and keeps every scored byte natural.

A G1-ctx result requires:

- intact natural performance above realized chance;
- improvement over the separately trained flag-off arm;
- within-checkpoint intact > read-zero;
- value- and address-permute collapse;
- no unary/copy control explaining the result;
- whole-corpus held-out CE inside a frozen non-inferiority band.

### Chance

Never assume 0.5.

If item \(i\) has \(K_i\) candidates and \(G_i\) acceptable gold aliases:

\[
p_{0,i}=\frac{G_i}{K_i},\qquad
p_0=\frac1N\sum_i p_{0,i}
\]

The exact null is the Poisson-binomial distribution induced by the realized \(p_{0,i}\), clustered by document. For binding-lift and permutation contrasts, enumerate or sample valid within-item edge derangements and calculate the null from those realized partitions. Ties receive fractional credit and remain counted.

### Power

Freeze a minimum interesting effect before examining checkpoints. For a 10-point lift over binary chance, two-sided \(\alpha=.01\), power .90 requires about 367 independent items under the optimistic IID approximation. Use at least 400 independent documents; approximately 600 is safer once document/entity clustering and event-family stratification are included.

For reference, 212 IID binary items are powered only for roughly a 13-point effect at those settings, and less after clustering. Three training seeds are also required, but seed replication is not a substitute for item-level power.

If the realized candidate partitions cannot supply the required exact-null power, the result is **UNPOWERED**, never negative.

## C. The lane

The bare causal-convolution mouth cannot express dependence beyond 35 bytes. However, the repository already contains an optional causal-bank mouth binder in [core/model.py](/Users/mini/dancinlab/anima/core/model.py:142) and [core/mbnd.py](/Users/mini/dancinlab/anima/core/mbnd.py:1). Its synthetic G6 result was negative, recorded in [H_9698](/Users/mini/dancinlab/anima/HYPOTHESES/cards/H_9698_mouth_bilinear_binder.md:1). Under p9 that is not a natural G1-ctx verdict, but rebuilding the same post-readout binder would plainly restate a killed lineage.

If the natural screen shows a real pressure surface and the current optional binder cannot exploit it, the minimum admissible new flag is:

```text
--ctx-store l3-kv
```

Semantics:

- At every position, form keys and values from the L3-class activation.
- Maintain a causal per-document bank; reset only at true document boundaries.
- Query the bank from the current L3 activation.
- Add the retrieved residual before the final trunk layer, not through `emit_drive`, `_hf_mean`, or a task-specific output override.
- Train solely with ordinary next-byte CE on the unchanged natural corpus.
- No entity labels, markers, target slots, binding loss, answer weighting, curated passages, or store manifest enter the treatment.

Conceptually:

\[
k_i=W_kh_i^{(3)},\quad v_i=W_vh_i^{(3)},\quad q_t=W_qh_t^{(3)}
\]

\[
a_{ti}=\operatorname{softmax}_{i<t}
\left(q_t^\top k_i/\sqrt r+b_{t-i}\right)
\]

\[
h_t^{(3)}\leftarrow h_t^{(3)}
+g_tW_o\sum_{i<t}a_{ti}v_i
\]

H_9720 says the key/query interface should start at the early L3-class representation, with a parameter-matched penultimate-tap control. It does not license a sweep over tap depths. The early tap is primary; penultimate is the frozen depth control.

H_9775 supports reusing the content-addressed value-transport lineage, including value-permute causality, but not its literal `g↔b` pairodd output permutation. That permutation is task FORM and cannot serve natural 256-byte prediction.

### The first $0 kill

Before implementing the flag, census the unchanged training corpus:

1. Count natural write→read episodes beyond 35 bytes.
2. Count crossed, locally ambiguous episodes.
3. Group target divergence points by their exact 35-byte suffix.
4. Measure the mass where \(H(Y\mid X_{35})>0\) and distant binding reduces it.
5. Count independent held-out documents satisfying the natural panel rules.

Kill the MB-scale lane if either:

- the natural panel cannot reach the frozen power requirement; or
- locally ambiguous binding pressure is negligible, meaning the fixed-corpus memorization shortcut remains available almost everywhere.

This cheap screen may only kill. A positive census authorizes the natural oracle-ceiling screen; it does not establish faculty.

## D. The 212-panel

Archive the existing items as **G1-weight-212**. They measure whether facts distributed across documents have been stored and recombined from weights. They should no longer be called a general G1 panel.

The replacement G1-ctx standard is not “another 212 prompts.” It is the natural byte-offset event manifest and its intact/read-zero/value-permute scorer described above. Its size is determined by the realized power calculation, not inherited numerology.

Past negatives remain valid but narrow:

- They are evidence against G1-weight at the tested corpus, scale, and optimization regime.
- They are not evidence against G1-ctx.
- Synthetic drill positives certify expressibility or instrumentation only.
- Synthetic G6/MBND negatives do not become natural G1-ctx negatives.
- No historical result proves that natural text supplies sufficient G1-ctx optimization pressure; that remains the census question.

Do not combine G1-ctx and G1-weight with an OR gate. Report them as separate axes until both have their own standards.

## E. Refusals

I would refuse:

- Selecting or reweighting binding-rich training passages.
- Synthetic drills, nonce referents, templated counterfactual corpora, replay, or self-generated consolidation as faculty evidence.
- Canonicalized carrier collisions as proof of training pressure; the model sees raw bytes.
- A single-name repetition DV as binding—it is copying.
- A panel whose answer can be recovered from length, byte form, position, or candidate frequency.
- Text corruption as the primary control when internal value permutation is available.
- Any negative read before same-item natural oracle and short-gap positive controls pass.
- Fixed 0.5 chance or IID item power.
- Auxiliary binding, addressing, target-slot, or answer-weighted losses.
- VSA, HRR, TPR, untrained recurrence, or a rebuilt H_9698 post-readout mouth binder.
- Literal pairodd `g/b` symmetry as a natural-language faculty mechanism.
- `_hf_mean`, `emit_drive`, or the rank-one write field.
- Hyperparameter or tap-depth sweeps after seeing the panel.
- Calling the 65.7% entity-meeting rate “G1-ctx supervision density.” It is an upper bound until write→read, ambiguity, and local-shortcut filters are applied.
- Demanding facts or continuations not licensed by the natural corpus.
- Reading a 212-item null as a small-effect null when it is not powered.

## Depletion log

1. **Task-ontology lens:** established an interventionally real G1-ctx/G1-weight distinction.  
   Next unused lens: training economics.

2. **Training-economics lens:** refuted “novel per document means unmemorizable during fixed-corpus training”; introduced the exact-local-collision forcing criterion.  
   Next unused lens: causal identification.

3. **Causal-identification lens:** added crossed natural events, read-zero, value-permute, and address-permute controls.  
   Next unused lens: statistical power.

4. **Statistical-power lens:** derived chance from realized \(K_i\), required document clustering, and showed why 212 is insufficient for a 10-point effect.  
   Next unused lens: architectural placement.

5. **Architectural-placement lens:** located autonomous key/value storage at the L3 interface and excluded output FORM paths.  
   Next unused lens: adversarial shortcut analysis.

6. **Adversarial-shortcut lens:** excluded copy, recency, unary form, weight facts, and corpus-selection explanations.  
   Next unused lens: corpus heterogeneity.

7. **Corpus-heterogeneity lens:** required byte-distance accounting and separate EN/KO and event-family reporting before aggregation.  
   Next unused lens: calibration.

8. **Calibration lens:** added nothing; candidate-local subtraction, realized nulls, and natural NLL already cover it.  
   Next unused lens: serialization/provenance.

9. **Serialization/provenance lens:** added nothing; flag-off byte identity, train/decode parity, lane-fire telemetry, and causal arm separation are already required by the lane contract.  
   Next unused lens: none.

**DEPLETED after 9 rounds.**

Exhausted lenses: task ontology, training economics, causal identification, statistical power, architecture, adversarial shortcuts, corpus heterogeneity, calibration, and serialization/provenance.
[32mlab full: both sections saved → /Users/mini/.sidecar/lab/2026-07-22T08-26-35-806Z-full.md[0m
