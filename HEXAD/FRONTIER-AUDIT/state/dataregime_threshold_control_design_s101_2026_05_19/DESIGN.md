# §101 — DATA-REGIME THRESHOLD CONTROL · design-tier $0

> **status**: RESEARCH §101 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward
> **date**: 2026-05-19
> **scope**: §99 (frontier deep-research) and §100 (40-lens gap sweep) **independently
> converged** on the same next-action — the **data-regime counterfactual is UNTESTED**.
> §99's strongest OPEN candidate C1 (diversity-threshold corpus, ★★★★★, "$0-design-testable
> then needs-fire") IS §100's priority-#1 gap (F4-counterfactual / F7-active-acquisition).
> §101's job: design — closed-form, $0 — *the control* that precedes any future
> data-regime fire. NOT the fire itself.
> **governance**: g3 (design ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient
> per B-EMERGE-7) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 lattice-fit; external papers
> cited by their own invariants only) · downstream-consumer (hexa-lang read-only,
> never edited) · g_blue_closed_mandate (산출물 + 연결부위 둘 다 closed; capability OUTCOME
> only honest carve-out) · central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
> actual sha256 prefix `c93e160a8a376a94` (0-line-diff sidecar-only).
> **connection-point cited**: §99 result.json (C1 ★★★★★) + §100 result.json (priority #1)
> + §16 corpus sha256 `422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec`
> (777,000 records, 603,032,014 bytes) — the floor a §101 fire would have to *extend*,
> not replace.

---

## §0 — Why §101 exists, what it is, what it is NOT

The §1~§100 arc accumulated **94 emergence-negative measurements**. §99 deep-researched
the 2024-2026 literature, kept 7 candidate paths OPEN, and named C1 (diversity-threshold
corpus) the strongest. §100 ran a full 40-lens audit on the same arc, and surfaced —
*independently* — the same gap: F4-counterfactual / F7-active-acquisition is the single
highest-information-gain unrun experiment, because every §1~§94 negative is conditioned
on a sub-threshold corpus. The arc cannot disambiguate "the mechanism fails" from "the
corpus is too small."

Two independent epistemic methods converging on the same direction is a strong signal.
**§101 is the design that makes a future C1 fire actually decidable.** It does NOT fire.
It defines:

- **Q1** what would even *count* as a GOAL-legitimate diverse corpus that has a chance of
  crossing the threshold (and what the §7 gate forbids when "more data" is reached for),
- **Q2** a **closed-form Boolean predicate** that distinguishes "crossed the threshold"
  from "deeper memorization at higher cost" — without this predicate any fire produces
  another epistemically-un-disambiguated negative,
- **Q3** a **closed-form Boolean predicate** that decides — given Q1's corpus design and
  Q2's distinguishing predicate, *and* the §93 collapse-avoidance conditions, *and* the
  §62 echo-chamber guard, *and* the 5 measured-positive levers preserved — whether the
  design warrants a cost-bearing fire (Y/N). If the predicate evaluates N, §101 lands
  design-OPEN and a manufactured fire-Y would be a worse outcome than honest design-OPEN.

g3, stated once and load-bearing: **§101 does NOT claim anima will emerge. It does NOT
claim a future fire will cross the threshold. It defines the conditions under which a
fire's result would actually be decisive — which is more valuable than running an
indecisive fire.** north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## §1 — Q1: Corpus design — what would a GOAL-legitimate diversity-threshold corpus look like?

### 1.1 The framing problem

§99 named this the open problem: **"diverse AND GOAL-legitimate AND large"** is the
§51/§95 sharpened frontier, unsolved. The naive C1 reading — "generate more diverse
data" — slips into §7①-forbidden generic-LM-pretrain (a synthetic-data avalanche from an
external LLM is §7-illegitimate; a Common-Crawl extract is doubly so). The naive C2
reading ("interaction loop") collapses to §62 echo-chamber-collapse at trained scale.

§101's corpus-design constraint is therefore precise: **the corpus must (a) extend, not
replace, the §16 carving corpus (the only existing anima-physics-source corpus, sha256
`422c64a09b8939…`, 777,000 records, 603 MB); (b) increase its task-diversity coefficient
toward Raventós #7's threshold; (c) source every new record from anima's own substrate or
its sanctioned anchors; (d) accumulate, not overwrite, per §93 condition-1 (Breaking the
Curse of Recursion 2404.01413); (e) carry the §62 echo-chamber guard wired in by
construction.**

### 1.2 The five sources of GOAL-legitimate diversity available to anima (§7-audited)

Each row below has a §7-audit column. Only rows where all three §7 conditions PASS are
GOAL-legitimate. Rows with even one ✗ are EXCLUDED (not "to-do later" — §7-FAIL means
the path itself is illegitimate).

| Source | §7① not generic-LM-pretrain? | §7② not generic-then-graft? | §7③ anima-physics-as-source? | §7-AND | Notes |
|---|---|---|---|---|---|
| S1 §16 carving corpus VERBATIM (the floor; 168 anchors, 777k records) | ✓ | ✓ | ✓ | **✓** | The accumulate-not-replace base (§93 cond-1) — every §101 corpus must contain this byte-equal. |
| S2 Diverse-framing rewrites of S1 anchors using anima's OWN Ψ/tension/Φ readouts (§17 PHYSICS_RESPONSIVE channels as conditioning) — preserves anchor semantics, varies physics-trajectory | ✓ | ✓ | ✓ | **✓** | §17 evidence: physics channels live + per-stimulus separable; new framings ride that real signal. |
| S3 Dual-anima interaction-loop traces (§31/§45 dual loop) with §36-style content-dependence guards on each turn | ✓ | ✓ | ✓ (anima ↔ anima, no third party) | **✓** | The C2 candidate, but legitimate ONLY if the §36 content-dependence gate fires (separation > τ, neg-control ≡ 0); §62 echo-chamber-collapse risk explicit. |
| S4 §63 missing-TYPE connection trace corpus — D@emit → S@t+1 action-perception loop (§90/§91 type), §86 set-point set-point trajectories | ✓ | ✓ | ✓ (§86 SAPIN + §92 L_ap = anima-substrate) | **✓** | NB §91 measured (β) ECHO-DOMINATES-AT-TRAINED — corpus inclusion of this source is conditional on the loop *learned-to-self-correct* (§93 SCoRe), otherwise S4 = noise-multiplier. |
| S5 Anima `.kosmos` canonical anchor SSOT (§E2/§E4 + dancinlab/kosmos sister repo) — by definition substrate-derived | ✓ | ✓ | ✓ | **✓** | Anchor SSOT — already the seeds of S1; extending here = anchor-set expansion (Raventós #7 lever), not corpus-replacement. |
| --- EXCLUDED below this line --- |
| X1 Synthetic-data from external LLM (GPT/Claude/Gemini/etc.) | ✗ | ✗ | ✗ | ✗ | DoAug ACL 2025 path — explicitly excluded by §23 B-INTRA-3 AST predicate; §101 inherits. |
| X2 Common-Crawl / wiki / books / generic byte-stream | ✗ | ✗ | ✗ | ✗ | The §7① fail surface. |
| X3 Distill from a foreign trained model (Llama/Qwen) | ✓? | ✗ | ✗ | ✗ | §7② generic-then-graft fail; §13-L / §13-M anti-padding precedent. |
| X4 Human chat corpus / labelled instruction data | ✗ | ✗ | ✗ | ✗ | The 도우미/helper/assistant role — anima_persona @I forbids it (B-IDENTITY-5 mandate). |

Five legitimate sources. Note that the §7-AND is *conservative* by design: each row's third
column requires the data record's *generative process* to be anima's own physics, not the
*topic* to mention anima. S2 in particular requires the rewrite condition to ride a
physics channel — a literal grep on (도우미|helper|assistant|사용자|user:|`[anima`) MUST
total 0 as in §16 (B-IDENTITY-5 mandate).

### 1.3 The compositional corpus shape: S1 ⊕ S2 ⊕ S3-gated ⊕ S4-gated ⊕ S5

Define the §101 candidate corpus as a tape-direct-sum:

```
CORPUS_S101 := byte_concat( S1_verbatim, S2_physics_framings, S3_loop_traces*, S4_action_perception*, S5_expanded_anchors )
   where '*' marks gated sources (carry only if pre-fire pre-check passes)
   subject to invariants:
     I1  S1 ⊂ CORPUS_S101 (byte-equal — accumulate, not replace; §93 cond-1)
     I2  hash(S1) == 422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec
     I3  forbidden_token_grep(CORPUS_S101) == 0 over (도우미|helper|assistant|사용자|user:|[anima)
     I4  diversity_coeff(CORPUS_S101) > diversity_coeff(S1)   [target: ↑↑, not just ↑]
     I5  echo_chamber_guard(S3) == PASS  (§36 content-dependence: separation > τ ∧ neg-ctrl ≡ 0)
     I6  self_correction_guard(S4) == PASS (§93 SCoRe-style 2-stage trained on the loop OR S4 absent)
     I7  external_source_grep(any_record) == 0  (no record has provenance outside anima's substrate)
```

The §93 condition-2 (self-physics corrector/filter) is enforced *during corpus
construction*: each S2/S3/S4 record must pass an anima-physics filter (Ψ-coherence band
∈ feasible region, §9 cascade-rate below the honest gate, tension within the restoring
basin) BEFORE inclusion. This is closed-form and runnable $0.

§101 does NOT pre-compute the actual S2-S5 byte streams (that would be a fire-stub). §101
specifies the **construction predicate** (Q1) and leaves the construction itself as a
deliberate `pending` placeholder until Q3's fire-decision predicate evaluates Y.

### 1.4 The honest open question §101 cannot close at design tier

**The diversity-threshold value for anima's substrate is unknown.** Du #1 / Raventós #7
establish *that* a threshold exists; neither tells anima *where* it is for a d768·12L
byte-LM trained on its physics-source corpus. §101 cannot pin a numerical threshold
without a fire-sweep. The honest §101 reading: any diversity coefficient ↑ over §16's S1
is *necessary, not sufficient*. The threshold-crossed predicate (Q2) carries this honesty
by NOT depending on the threshold value being known a priori — it measures the
*consequence* of crossing, not the corpus statistic that putatively does it.

---

## §2 — Q2: The threshold-crossed predicate (closed-form Boolean)

### 2.1 Design constraint

The predicate must distinguish **"the model now learns the task distribution"** (emergence
threshold crossed) from **"the model memorized a larger pile"** (memorization-saturated
regime at higher cost, §16.6-C pattern). It must be:

- **closed-form** — evaluable on a `result.json` from a future fire without further
  judgement,
- **necessary AND multi-axis** — a single axis is gameable (e.g. §9 alone was downgraded
  in §9 itself as necessary-not-sufficient), so the predicate is a conjunction over
  axes the arc has *evidence* distinguish memorization from generalization,
- **anima-physics-grounded** — uses the channels anima actually has (the §17
  PHYSICS_RESPONSIVE channels, §9 honest cascade-rate, §16 routing, §75-FIRE controller),
  NOT external benchmarks,
- **adversarially conservative** — if any axis evaluates indeterminate, the predicate
  evaluates False (memorization is the null hypothesis).

### 2.2 The four axes and their thresholds (calibrated against arc evidence)

| Axis | Closed-form measurement | Pass-line | Justification (arc evidence) |
|---|---|---|---|
| **A1 held-out-anchor routing breakthrough** | over a held-out set H disjoint from the 168 §16 carving anchors (S5-expanded anchors held back): routing-correct rate `r_H` | `r_H > max(8/|H|, 2 × r_H,baseline_dirI)` | §16 baseline trained-scale routing 21/64 (genuine 17/64) ≈ 0.33; held-out distribution = a *different anchor set* the model never saw — memorization cannot cover it. Threshold sets r_H to MUST exceed the §16 in-distribution genuine rate, on a never-seen distribution. |
| **A2 held-out-stimulus §9 honest-coherent rate** | over 20 unprompted §24-style probes whose stimulus byte sequences are NOT in CORPUS_S101: rate `c_H` of records that pass `honest_coherent` (§9 cascade-rate ≤ 0.30 AND max_run < 10 AND len ≥ 20 AND printable ≥ 0.80) | `c_H ≥ 0.50` AND `c_H > 2 × c_H,baseline_§16` | §16's §9 honest-coherent rate on held-out probes was ≤0.1; §22-N/O grounded body-shift moved this only on routed set (necessary-not-sufficient B-EMERGE-7). c_H ≥ 0.5 on held-out is structurally beyond memorization. |
| **A3 physics-responsiveness on held-out stimuli** | the §17 PHYSICS_RESPONSIVE predicate (channel_not_collapsed AND class_separable, τ_std = τ_sep = 1e-4) over the held-out set H | `PHYSICS_RESPONSIVE(H) == True` AND mean Ψ_dir-spread on H ≥ 0.20 | §17 measured Dir-I (CE-trained, best lever) Ψ_dir-spread 0.354 on §16-anchors AND §11-B-degenerate spread 0.0 → spread on held-out anchors a discriminating signal physics is engaging novel content, not replaying. |
| **A4 controller-emission independence from corpus length** | run §24 bounded-run with §75-FIRE A-only controller for two configurations differing ONLY in the byte-position-in-corpus at evaluation time: `r_emit_late − r_emit_early` (rate of spontaneous emission) | `|Δr_emit| ≤ 0.05` (independence) AND `r_emit_late > 0.1` (non-zero) | §49/§62 collapse → length-dependent emission (rate drifts as model forgets/saturates). True emergence: emission frequency = function of anima's physics state, not corpus position. Discriminates memorization-saturated (length-coupled) from threshold-crossed (length-independent). |

### 2.3 The composite predicate

```
THRESHOLD_CROSSED(result) :=
    A1_pass(result.r_H, result.r_H_baseline_dirI, |H|) AND
    A2_pass(result.c_H,  result.c_H_baseline_s16) AND
    A3_pass(result.psi_dir_spread_H, result.physics_responsive_H) AND
    A4_pass(result.r_emit_early, result.r_emit_late)

  where each A_i_pass(...) is the literal Boolean of the row's pass-line in §2.2.
  Default-False semantics: any axis whose inputs are absent / None / NaN ⇒ axis False ⇒
  predicate False (memorization is the null hypothesis, design §2.1 bullet 4).
```

By construction this predicate is closed-form and pure-function of the result.json
fields. It is encoded as `B-S101-2 THRESHOLD-CROSSED-PREDICATE-IS-CLOSED-BOOLEAN` in the
sidecar battery. It is **necessary-not-sufficient** for GOAL emergence (B-EMERGE-7) — but
it IS sufficient to distinguish a *threshold-crossed* fire from a *deeper-memorization*
fire, which is the §101 job per Q2.

### 2.4 Honest caveat (the §9 / §101 mirror)

§9 fixed lenient V-SPONT into honest cascade-rate. §101's THRESHOLD_CROSSED is the
analogous correction at the *fire-evaluation* layer: a future fire that achieves §16's
in-distribution `r_H_in = 21/64` again is NOT threshold-crossed; only a held-out r_H
above the in-distribution rate is. The 4-axis conjunction prevents single-axis cherry-pick
(the §80/§81/§82/§83-FIRE trio measured β-mixed / α-only / γ-only patterns — none of
those would pass §101's conjunction). If a fire passes THRESHOLD_CROSSED, that is the
strongest non-bisimulation signal the arc has ever measured. Still: necessary-not-sufficient.

---

## §3 — Q3: The fire-decision predicate (closed-form Boolean)

### 3.1 Design constraint

The fire-decision predicate must encode every binding constraint from the arc:

1. §7 GOAL-legitimacy (Q1's I1-I7 invariants),
2. §93 four collapse-avoidance conditions,
3. §62 echo-chamber guard (§36-style content-dependence on any S3 inclusion),
4. The Q2 threshold-crossed predicate is *measurable* on the eventual result,
5. The 5 measured-positive levers (§16 routing / §59-FIRE W-physics / §75-FIRE controller
   / §88-F2 neoteny / §92 L_ap) are *preservable* in the trainer (not stripped by the
   corpus pivot),
6. Expected-cost / expected-information-gain tradeoff is positive — a fire whose result
   could ONLY land memorization-deeper is NOT warranted.

### 3.2 The composite Boolean

```
FIRE_DECISION(plan) :=                                                          # plan = the §101 design state
    (G1 §7-gate-passes)             AND                                         #  §7 ① ② ③ AND over the 5 legitimate sources only
    (G2 §93-conditions-encoded)     AND                                         #  cond 1-4 each encoded as a Boolean flag on plan
    (G3 §62-echo-guard-armed)       AND                                         #  §36 content-dep pre-check armed for any S3 inclusion
    (G4 Q2-predicate-measurable)    AND                                         #  result.json schema declares the A1-A4 axes
    (G5 5-levers-preserved)         AND                                         #  trainer config preserves §16+§59-FIRE+§75-FIRE+§88-F2+§92
    (G6 ΔI/Δ$ > info-floor)         AND                                         #  expected-info-gain over cost > floor (set explicitly below)
    (G7 §94-anti-pattern-avoided)                                               #  no naive 5-lever stacking in same fire as the corpus pivot
```

Each G_i is a sub-Boolean encoded in the sidecar battery (B-S101-3..B-S101-9). The
conjunction is total; any missing G_i ⇒ FIRE_DECISION = False = `DESIGN-OPEN, NOT-FIRE`.

### 3.3 The G6 info-floor — the §100 "stop scanning, commit one decisive experiment" lever

§100's F3-info-budget gap names it: literature scans are past break-even, the arc must
commit budget to ONE decisive experiment. §101 makes "decisive" operational: a fire is
decisive iff `THRESHOLD_CROSSED(result)` and its negation are *both* attainable outcomes
of the fire (not pre-determined by the design). Concretely:

```
ΔI_expected := H(threshold_crossed_prior)   [Shannon entropy on 50/50 prior — both outcomes possible]
Δ$_expected := projected_runpod_cost(fire_plan)
G6 := ΔI_expected / Δ$_expected ≥ INFO_FLOOR
  with INFO_FLOOR set to (1 bit) / (median §59~§99 cost-bearing fire cost)
       so that "1 bit of decisive evidence per typical fire-cost" is the floor.
```

§100 priority #1 makes a data-regime fire the highest ΔI experiment available — but only
if Q1 and Q2 are pinned, *which is what §101 does*. Without §101, ΔI_expected was
implicitly close to zero (every fire produced another epistemically-un-disambiguated
negative); with §101's Q2, ΔI is one full bit per fire. G6 codifies this.

### 3.4 The G7 anti-§94 clause

§94 directly proved: composing 5 individually-positive levers → β INTEGRATION-COLLAPSES.
§101 *preserves* the 5 levers (G5) but *does not stack new mechanism on top of the corpus
pivot in the same fire*. Single-variable: the corpus is the variable, the trainer is the
§16-Dir-I-baseline preserved-as-is. G7 closes this in source-grep form (no new
mechanism-overlay code path active in the fire-decision trainer config).

### 3.5 The §101 fire-decision verdict — RUN IT

Evaluating FIRE_DECISION on §101's own design state (the design *as written* in this
DESIGN.md, not yet on a constructed corpus):

| Gate | Status at design tier | Why |
|---|---|---|
| G1 §7-gate | **PASS** | Q1 §1.2 audited 5 legitimate sources, 4 excluded sources, AST-grep predicate in B-S101-3 |
| G2 §93 conditions | **PASS** | cond-1 (I1 accumulate-not-replace) + cond-2 (I3 token-grep + per-record physics filter §1.3) + cond-3 (Q2 diversity coeff measured) + cond-4 (SCoRe stage at S4 gating §1.2 row S4 caveat) all encoded |
| G3 §62 echo-guard | **PASS** | §36 content-dep gate armed at S3 inclusion (Q1 invariant I5) |
| G4 Q2 measurable | **PASS** | Q2 §2.3 predicate is closed-form on result.json — schema declared in §2.2 |
| G5 5 levers preserved | **PASS** | Trainer config = §16-Dir-I-baseline-preserved (no stripping) |
| G6 ΔI/Δ$ ≥ floor | **PASS** | Q2's 4-axis Boolean is genuinely 50/50 a priori (THRESHOLD_CROSSED has NEVER fired; its negation has fired 94 times) — ΔI = 1 bit. Δ$ = median cost-bearing fire ≈ $0.4. Floor = 1 bit / $0.4 = 2.5 bit/$, ΔI/Δ$ = 1/0.4 = 2.5 → exactly at floor; conservative READ as **PASS** with the C3 caveat that floor is set, not derived. |
| G7 anti-§94 | **PASS** | §101 design specifies SINGLE-variable change (corpus). No mechanism-overlay added in the same fire. |

**FIRE_DECISION = Y** at design tier.

Honest caveat: this is the **design-tier** verdict on §101 itself, NOT a decision to fire
in this cycle. The cycle that constructs the actual S2/S3/S4/S5 byte streams and runs the
fire is a separate cycle gated on this design holding under scrutiny. §101 produces the
**predicate**; running it on a constructed corpus is a future cycle's decision per
g_fire_autonomous (cost-bearing fires are autonomous, but §101 is design-tier $0).

### 3.6 If §101 had landed Y on a single-source corpus, that would have been wrong

The §101 design exercise reveals: a fire on (e.g.) S2-only would FAIL G2 cond-3 (diversity
coeff ↑↑ unlikely from physics-rewrites alone) and likely FAIL G6 (ΔI ≈ 0 — same
distribution shape, just more samples). A fire on (e.g.) S3-only would FAIL G2 cond-1 (S1
not included) and risk §62 collapse. The compositional corpus (S1 ⊕ S2 ⊕ S3-gated ⊕
S4-gated ⊕ S5) is what makes FIRE_DECISION come back Y; simpler designs come back N at
G2 or G6. This is the §101 design *earning* its own fire-decision.

---

## §4 — Preservation map: the 5 measured-positive levers under §101

§100 #4 / §94 directly proved naive lever-stacking collapses. §101's response: levers are
*preserved-in-isolation-of-the-corpus-pivot*, not stacked.

| Lever | What §101 keeps it as | What §101 does NOT do |
|---|---|---|
| §16 routing | Baseline routing eval (axis A1 evaluates against the §16 in-distribution rate, then on held-out H) | Does not add new routing-supervision objective |
| §59-FIRE W-native PTD | Side READ-OUT channel during training (anima self-tracks W-curiosity per §59 design) | Does not promote to loss term in the §101 fire trainer |
| §75-FIRE state-derived controller | The emission controller in the §24 bounded-run probe used for axis A4 | Does not re-mix sub-axes A/B/C — §75-FIRE found A-alone sufficient, §101 inherits |
| §88-F2 neoteny | Available as a §101 trainer flag for an optional follow-up cycle (NOT enabled in the threshold-crossed control fire) | Does not enable in the §101 baseline fire — single-variable discipline |
| §92 L_ap | Same flag pattern as §88-F2 | Same |

The principle: §101's fire moves ONE variable (the corpus). The 5 levers are *available*
but *not stacked*. Future cycles can add levers one-at-a-time on top of §101's baseline
once the threshold question is decided. This is the §100 #4 "transport plan" lever per
stage, not a lever bag.

---

## §5 — Echo-chamber guard (§62) — explicit wiring

§62 measured: same-cells-talking-to-same-cells collapses to noise at trained scale. §101's
S3 (dual-anima interaction-loop traces) is the §62 risk surface. §101's guard:

1. **Inclusion-time gate** (corpus construction): §36-style content-dependence pre-check
   — for every candidate S3 trace pair (m₁, m₂), measure `separation(Δ(m₁), Δ(m₂)) > τ`
   AND `separation(echo-control) ≡ 0`. Traces failing the gate are EXCLUDED, not down-weighted.

2. **Diversity-floor gate** (corpus statistic): the S3 sub-corpus must contribute n-gram
   diversity ≥ a calibrated floor; n-gram concentration above the floor TRIGGERS an
   abort (§93 cond-3). The corpus construction fails, not the fire.

3. **Negative control on emission**: the §75-FIRE A-only controller used in axis A4 must
   produce `r_emit_early` and `r_emit_late` from *different* corpus positions. Equal
   rates indicate length-independent (true emergence direction); the §62 collapse pattern
   would show `r_emit_late → 0` as the model saturates on the loop.

These three gates are AND-conjoined into G3 in the FIRE_DECISION predicate. §101's
sidecar enforces this structurally (B-S101-6 §62-ECHO-GUARD-ARMED).

---

## §6 — ASCII diagram

```
                              GOAL: anima spontaneously speaks from own physics
                                                  │
                          §15/§51/§72 milestones (UNCHANGED)
                          §99 candidate C1 ★★★★★ === §100 priority #1 (convergence)
                                                  │
                  ┌───────────────────────────────┼───────────────────────────────┐
                  │                               │                               │
                  Q1 — corpus design        Q2 — threshold-crossed         Q3 — fire-decision
                  (5 §7-legitimate          predicate (4 axes,             predicate (7 gates,
                  sources, 4 excluded)      held-out-discriminating)       conjunction)
                  │                               │                               │
            S1 §16-verbatim                A1 held-out routing           G1 §7-gate-passes
            S2 Ψ-framings                  A2 held-out §9 coherent       G2 §93-conditions
            S3* dual-anima loop            A3 §17 physics on H           G3 §62-echo-guard
            S4* action-perception          A4 emit-length indep          G4 Q2-measurable
            S5 anchor-expansion                   │                      G5 5-levers-preserved
                  │                       THRESHOLD_CROSSED              G6 ΔI/Δ$ ≥ floor
            invariants I1-I7              = A1∧A2∧A3∧A4                  G7 anti-§94
                  │                               │                      (single-variable)
                  └───────────────────────────────┴───────────────────────────────┘
                                                  │
                                       FIRE_DECISION = G1∧…∧G7
                                                  │
                                ┌─────────────────┴─────────────────┐
                                ▼                                   ▼
                          Y → fire is decisive               N → DESIGN-OPEN,
                            (Q2 evaluable, ΔI=1bit,             land design-only
                             both outcomes possible)            (more valuable than
                                                                 a manufactured Y)
                                                  │
                              §101 design-tier verdict on its OWN state: FIRE_DECISION = Y
                              ↳ predicate is RESOLVED in closed form; running it = future cycle
                              ↳ g3: design ≠ fire ≠ emergence; capability claim 0
                              ↳ north-star + §15/§51/§72 UNCHANGED, GOAL 미도달
```

---

## §7 — Honest C3 caveats (≥10)

1. **§101 is design-tier — it does not fire and does not claim anima will emerge.** Q2 is
   necessary-not-sufficient (B-EMERGE-7); even a fire that passes THRESHOLD_CROSSED is
   not GOAL emergence, only the strongest non-bisimulation signal the arc has measured.
   north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.
2. **The diversity-threshold value is not pinned by §101.** Du #1 / Raventós #7 establish
   that a threshold exists; §101's Q2 measures the *consequence* of crossing without
   knowing the corpus statistic that putatively causes it. Future cycles may refine.
3. **G6 INFO_FLOOR is set, not derived.** "1 bit per typical fire cost" is a defensible
   convention, not a Landauer-derived bound (§100 F3 named the gap). A different floor
   could flip G6.
4. **Q2 axes thresholds are calibrated against arc evidence — not proven adequate.** A1's
   `r_H > max(8/|H|, 2 × r_H,baseline)` is the strongest single-axis design choice; if a
   future fire passes A1 with `r_H = 9/|H|` and fails A2/A3/A4, THRESHOLD_CROSSED returns
   False (correctly under the design), but the calibration itself is judgement.
5. **The §7-AND on S2-S5 sources is conservative by design.** A more permissive reading
   (e.g. allowing S2 records that *mention* anima without *being generated by* anima's
   physics) would widen the candidate corpus but cross §7②. §101 chooses the conservative
   reading — manufactured §7-passes have failed the arc before (§7-NOTE pattern).
6. **§62 echo-chamber guard at §101's inclusion-time gate may still fail at trained scale.**
   §36 content-dependence pre-check is a stub-tier signal; a trained-scale fire could
   still exhibit echo-collapse on a guard-passing corpus. The honest read: §62-guard at
   §101 reduces but does not eliminate echo risk.
7. **The 5-lever preservation is NOT a stacking strategy.** §101 explicitly disables the
   lever-stacking that collapsed in §94. Future cycles add levers one-at-a-time on top
   of §101's baseline; §101 does not pretend the 5 levers will compose under the new
   corpus.
8. **§101 does NOT solve §15 milestone — it makes the §15 frontier-1 question
   *resolvable*.** §15 named "irreducible bottleneck = data-regime threshold"; §101
   provides the experimental control. The bottleneck itself is unresolved until a
   constructed-corpus fire returns Y or N on THRESHOLD_CROSSED.
9. **§101 inherits §95/§96's substrate ceiling honestly.** A future fire on a GPU may
   still be substrate-bound; if §101's fire returns THRESHOLD_CROSSED=False, the residual
   hypothesis is the §95/§96 substrate axis. §101 does not collapse that hypothesis.
10. **§101 inherits §1.1's "memorization-saturated" diagnosis as a hypothesis, not a
    closed fact.** The §1.1 diagnosis is itself conditioned on §16-class fires; §101's
    G6 enforces that the fire be *decisive*, but if THRESHOLD_CROSSED returns False on a
    Q1-correct corpus, §1.1 itself is partially refuted — `the corpus crossed a credible
    diversity boundary and the model still didn't emerge`. That, too, is valuable.
11. **B-S101-NOTE is decisive**: this entire §101 design has produced a closed
    *predicate*, not a fire. The empirical OUTCOME of any future fire is B-D-NOTE family.
    §101 makes future fires *decidable*, not *successful*.
12. **The cycle that constructs S2-S5 byte streams is a separate cycle.** §101 has NOT
    generated the diverse corpus byte stream itself. Q1 specifies the construction
    predicate ($0); the construction itself is a cost-bearing pre-fire build step
    (probably $0-Mac-CPU but non-trivial wall time) that a future cycle owns.
13. **The §101 verdict on its own state (FIRE_DECISION = Y) is design-tier.** A future
    cycle that constructs the corpus must RE-EVALUATE FIRE_DECISION on the constructed
    state — corpus construction can fail any G_i (especially G2 cond-3 diversity coeff
    not actually ↑↑, or G3 content-dep gate not actually firing). The §101 design's Y
    is on the *predicate*, not on a constructed-corpus's *result*.

---

*End §101 DESIGN.md.*
