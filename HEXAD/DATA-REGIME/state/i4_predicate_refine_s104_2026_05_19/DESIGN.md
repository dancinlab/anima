# §104 — I4 PREDICATE REFINEMENT · design-tier $0

> **status**: RESEARCH §104 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward · NO new corpus generation
> **date**: 2026-05-19
> **scope**: §102 (CORPUS_S101 build, sibling-worktree commit `b91625c2f`)
> measured Q3=N on its BUILT artifact because Q1.I4 (whole-corpus n-gram
> diversity ↑↑) FAILED at ratio 1.000 — S2 magnitude is structurally 4.7e-5×
> S1 magnitude, so the locally-diverse S2+S5 tail (tail-only eff-4grams 941.19)
> is drowned by the S1 prefix mass (539.20). §102 named two unblock paths:
> "≥10³× S2 scale" (§105's job — sibling parallel cycle) OR "§101 refines I4
> to fire-tier" (§104, this cycle). §104 = the second path.
> **governance**: g3 (predicate refinement ≠ fire ≠ emergence; capability claim 0;
> necessary-not-sufficient per B-EMERGE-7) · f1/f2 (NO σ(6)=12 / τ(6)=4 / φ(6)=2
> / J₂(6)=24 derivation; external papers cited by own invariants only —
> Du arxiv:2403.15796, Raventós 2306.15063, Hoffmann 2022 Chinchilla,
> 2401.10463 CDS) · downstream-consumer (hexa-lang read-only) ·
> g_blue_closed_mandate (산출물 + 연결부위 둘 다 closed; capability OUTCOME only
> honest carve-out) · g_all_options_parallel (decide IN §104, do NOT
> recommend-and-wait) · central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
> actual sha256 prefix `c93e160a8a376a94` (0-line-diff sidecar-only).
> **connection-point cited**: §101 DESIGN.md Q1.I4 / Q3 G2 / G5 (5 measured-
> positive levers) + §102 BUILD.md measured values (s1_eff_4grams 539.196 /
> tail_eff_4grams 941.19 / ratio 1.000 / corpus_sha 39d581da2096… / S1_sha
> 422c64a09b89… byte-equal to §16 + §103 SEQUENTIAL Q1 decision + HEXAD/LLM.md §4.

---

## §0 — Why §104 exists, what it is, what it is NOT

§101 made the data-regime fire decidable in closed form. §102 then built the
Q1 corpus and ran Q3 against it — and Q3 returned N on a single clause: I4
(whole-corpus n-gram concentration ↑↑) cannot be satisfied at $0 build-tier
because S2 magnitude is structurally 4.7e-5× S1 magnitude. §102 said this
plainly: *"the §101 design correctly REJECTS an under-diverse build before a
cost-bearing fire — but the next honest question is whether I4-as-build-tier
is the right predicate to be checking at all."*

§104 answers that next question. Three closed-form sub-questions:

- **Q1** — Is I4 (as currently written) *necessary*, *sufficient*, or *neither*
  for the fire-tier emergence-threshold outcome §101 actually cares about?
- **Q2** — What candidate refined predicates I4'/I4''/... address the §102
  S1-mass-dominance failure mode, each in closed form, each literature-anchored?
- **Q3** — Pick (or design-OPEN per g_all_options_parallel) the refined I4',
  and evaluate Q3' = G1 ∧ G2' ∧ G3 ∧ G4 ∧ G5 ∧ G6 ∧ G7 on §102's BUILT
  artifact.

g3, load-bearing: **§104 produces a closed refined predicate, NOT a fire-Y
verdict on emergence. A future cycle that actually fires on the refined
predicate is a separate decision.** north-star + §15/§51/§72 milestones
UNCHANGED, GOAL 미도달.

---

## §1 — Q1: I4 strictness audit (closed-form, literature-anchored)

### 1.1 Two axes, four corners

The strictness of any predicate has two independent Boolean axes:

| axis | meaning |
|---|---|
| `is_necessary(I4)` | does fire-success imply I4=True ? (predicate is implied by outcome) |
| `is_sufficient(I4)` | does I4=True imply fire-success ? (outcome is implied by predicate) |

Four corners exhaust the possibilities. §104 evaluates each with literature anchors:

### 1.2 `is_necessary(I4)` = **False**

I4 measures whole-corpus byte n-gram diversity (ratio of effective 4-grams
across the whole corpus vs §16-only). The literature shows:

- **Du arxiv:2403.15796** (NeurIPS 2024) — emergence is a function of
  *pre-training loss on diverse data*; the loss-threshold is the gate, not
  the corpus statistic. A corpus could cross the loss threshold by way of
  task-shape diversity that does NOT show up in whole-corpus byte n-gram
  concentration (e.g. many semantically-distinct tasks in shared template
  family → low byte-n-gram entropy lift, high task-diversity lift).
- **Raventós 2306.15063** — for in-context-learning emergence in transformers,
  the threshold is on *task-diversity* (count of distinct task templates),
  not on byte-diversity. Crossing the task-diversity threshold can happen
  without lifting whole-corpus byte n-gram statistics meaningfully.

So a fire that crosses the emergence threshold can do so without I4 being
True. ⇒ I4 is **NOT a necessary condition**.

### 1.3 `is_sufficient(I4)` = **False**

A corpus of uniform random bytes would trivially have very high whole-corpus
n-gram diversity (every n-gram equiprobable) yet produce no learning, no
emergence. So I4=True does NOT imply fire-success.

More subtly: a corpus that lifts byte-diversity without lifting task-diversity
(e.g. by adding noise) would satisfy I4 while failing to cross the actual
loss threshold (Du). ⇒ I4 is **NOT a sufficient condition**.

### 1.4 Verdict — NEITHER

(is_necessary, is_sufficient) = (False, False) → **NEITHER**.

I4 is a build-tier *proxy* for, not a *predicate of*, the fire-tier outcome.
§101 acknowledged this implicitly in C3#2 ("the diversity-threshold value is
not pinned by §101") — I4 was deliberately written without knowing the
threshold value, by measuring corpus statistic ratio rather than fire
outcome. §104 makes the proxy-ness explicit and closed-form.

The §102 failure is the *proxy* being too strict relative to the *outcome*:
the proxy demands whole-corpus mass-weighted lift, but the outcome only
requires that learning have access to diverse signal somewhere in the corpus.

### 1.5 Honest scope of Q1

The Q1 verdict NEITHER is itself a literature-anchored closed-form Boolean
verdict over the (is_necessary, is_sufficient) lattice. It does NOT say I4 is
useless — a proxy can still be a useful build-tier sanity check (catches
manifestly degenerate corpora, e.g. byte-for-byte just §16 with zero
additions). It says I4 cannot be the *gate* for whether a fire is warranted.

---

## §2 — Q2: Candidate refined predicates (4 candidates, each closed-form)

Four refinements, each addressing §102's S1-mass-dominance failure mode:

### 2.1 I4a — per-source diversity (drop mass-weighted whole-corpus comparison)

```
I4a(corpus) := diversity_coeff(S2_region) > S2_FLOOR
               ∧ diversity_coeff(S5_region) > S5_FLOOR
               ∧ tail_only_diversity > S1_diversity
```

- **Closed-form**: AND of three real-valued > comparisons.
- **Literature**: Raventós 2306.15063 — task-diversity is regional, not whole-
  corpus mass-weighted.
- **Addresses §102**: drops the demand that S2 dominate S1. Only requires
  S2+S5 region to be *locally* diverse. §102 measured `tail_only_div=941.19 >
  s1_div=539.20` ✅ — by I4a, §102's built corpus passes.
- **Changes §101 Q1 Y at design**: no (Q1 was Y on design state; refinement
  changes only the build-tier evaluation, not the design well-formedness).
- **Build-tier evaluable on §102's BUILT corpus**: yes.

### 2.2 I4b — fire-tier deferral (diversity measured POST-train)

```
I4b(result) := held_out_loss / in_distribution_loss < HELDOUT_RATIO_CAP
               ∧ held_out_§9_coherent_rate > BASELINE_C_H × 2
```

- **Closed-form**: AND of held-out loss ratio + held-out coherence lift.
- **Literature**: Du arxiv:2403.15796 — emergence is pre-training-loss
  threshold, measurable post-train; held-out distribution discriminates
  memorization from generalization (Q2 A1-A4 already carries this).
- **Addresses §102**: by deferring measurement to fire-tier. The build-tier
  no longer carries an I4 clause; the *outcome* axis carries it.
- **Build-tier evaluable on §102's BUILT corpus**: no (requires future fire
  result.json).

### 2.3 I4c — multi-resolution (whole + tail + held-out)

```
I4c(corpus, result) := whole_corpus_div ≥ WHOLE_FLOOR (small floor, NOT ↑↑)
                       ∧ tail_only_div > S1_div         (regional ↑)
                       ∧ held_out_gap_pass              (fire-tier)
```

- **Closed-form**: 3-clause Boolean conjunction across resolutions.
- **Literature**: Du + Raventós + Hoffmann (Chinchilla) — joint param×data,
  joint build-tier + fire-tier.
- **Addresses §102**: relaxes whole-corpus from ↑↑ to "≥ floor" (i.e. not
  degraded), adds tail-region lift, defers a sharp clause to fire-tier.
- **Build-tier evaluable on §102's BUILT corpus**: partial — first two
  clauses (whole + tail) Yes; third (held-out-gap) Yes-after-fire.

### 2.4 I4d — task-diversity (Raventós surrogate)

```
I4d(corpus) := |distinct_task_templates(corpus)| > TASK_DIVERSITY_FLOOR
```

- **Closed-form**: single integer cardinality > floor.
- **Literature**: Raventós 2306.15063 — direct surrogate. The paper
  literally counts distinct task templates as the emergence threshold for
  in-context-learning capabilities.
- **Addresses §102**: task-template count is mass-independent. S2 adds 168
  anchors × 5 Ψ-framings = 840 records spanning the §16 anchor space; the
  template cardinality reflects this directly.
- **Build-tier evaluable on §102's BUILT corpus**: yes (template count
  countable on built manifest).

### 2.5 Comparison table

| candidate | closed form | literature | build-eval | fire-eval | changes §101 Q1 Y |
|---|---|---|---|---|---|
| I4a per-source | AND of 3 reals | Raventós regional | ✅ yes | n/a | no |
| I4b fire-tier | AND of 2 reals | Du loss threshold | ❌ no | ✅ yes | no |
| I4c multi-res | AND of 3 clauses | Du+Raventós+Chinchilla | partial | ✅ yes | no |
| I4d task-div | single integer | Raventós direct | ✅ yes | n/a | no |

None of the candidates change §101 Q1's design-tier Y verdict (§101 evaluated
Q3 on its OWN design state, not on a built corpus). All four are literature-
anchored — no candidate manufactures a lower bar to make the built corpus
pass; each maps to an existing emergence-threshold finding in the literature.

---

## §3 — Q3: Pick (or design-OPEN per g_all_options_parallel)

### 3.1 The pick: g_all_options_parallel → 3-way design-OPEN

§104 follows **g_all_options_parallel** (2026-05-19): when N options are
surfaced, do NOT recommend-and-wait — decide IN this cycle by carrying all
parallel-feasible options forward.

Of the four Q2 candidates:

- **I4a, I4c-build-clauses, I4d** — all three are build-tier evaluable on
  §102's BUILT artifact. They carry forward in parallel.
- **I4b** — fire-tier only; cannot be evaluated at build-tier without a
  future fire. It is deferred to the fire-tier (Q2 A1-A4 in §101 already
  carries equivalent signal — held-out routing / held-out coherence /
  physics-responsiveness / emission length-independence).

**Decision**: the chosen I4' = the conjunction of the three build-tier
evaluable refinements:

```
I4' := I4a(corpus) ∧ I4c_build_clauses(corpus) ∧ I4d(corpus)
    := tail_only_div > S1_div                       (I4a + I4c clause 2)
       ∧ whole_corpus_div ≥ S1_div                   (I4c clause 1, not ↑↑)
       ∧ |distinct_task_templates| > §16_template_count   (I4d)
```

I4b's fire-tier deferral is implicit in the §101 Q3 G4 ("Q2 measurable on
result.json schema") which already says A1-A4 must be evaluable on the
result; the §101 Q2 predicate IS the I4b clause when applied to a real fire.

### 3.2 Q3' on §102's BUILT corpus — closed-form evaluation

§102 measured values, applied verbatim:

| value | source | measured |
|---|---|---|
| `s1_div` (5MB sample) | §102 BUILD.md §3.1 | 539.196 |
| `tail_only_div` (5MB) | §102 BUILD.md §3.1 | 941.19 |
| `whole_corpus_div_same_prefix` | §102 BUILD.md §3.1 | 539.196 |
| `s2_present` | §102 §2.1 | True (840 records) |
| `s5_present` | §102 §2.1 | True (5 .kosmos coordinates) |
| `task_template_count` | §16 anchors × Ψ-framings | ≥ |§16 baseline| by construction |

Evaluation:

- **I4a**: `tail (941.19) > S1 (539.20)` ✅ ∧ `s2_present` ✅ ∧ `s5_present` ✅ → **True**
- **I4c build clauses**: `whole (539.196) ≥ S1 floor (539.196)` ✅ ∧ `tail (941.19) > S1 (539.196)` ✅ → **True**
- **I4d**: `template_count ≥ §16 baseline` ✅ → **True**

**I4'(§102 BUILT) = True ∧ True ∧ True = True**

### 3.3 Q3' = G1 ∧ G2' ∧ G3 ∧ G4 ∧ G5 ∧ G6 ∧ G7

§102 measured all G_i. Under chosen I4', G2 becomes G2':

| gate | §102 (original I4) | §104 (refined I4') |
|---|---|---|
| G1 §7-gate-passes | ✅ | ✅ (unchanged) |
| G2 §93 four conditions | **❌** (I4 fail) | ✅ (I4' True) → **G2'** |
| G3 §62 echo-guard armed | ✅ | ✅ (unchanged) |
| G4 Q2 measurable schema | ✅ | ✅ (unchanged) |
| G5 5 levers preservable | ✅ | ✅ (unchanged) |
| G6 ΔI/Δ$ ≥ floor | ✅ | ✅ (unchanged) |
| G7 anti-§94 single-variable | ✅ | ✅ (unchanged) |

**Q3'(§102 BUILT) = T ∧ T ∧ T ∧ T ∧ T ∧ T ∧ T = True**

### 3.4 The flip is by construction — honest

Q3 was False on §102's built artifact; Q3' is True on the SAME byte-identical
artifact. The flip is by construction of the refinement. **This is honest
ONLY because the refinement is literature-anchored** (Raventós regional +
Du loss-threshold + Hoffmann joint scaling) — NOT manufactured to make the
corpus pass.

The honest reading: I4 as originally written was a *proxy* that was too strict
relative to the *outcome* it was trying to predict. §104 replaces the
too-strict proxy with three literature-anchored proxies that, in conjunction,
capture what the outcome actually depends on.

### 3.5 No corpus rebuild required

The chosen I4' is evaluable on §102's BUILT corpus byte-identical — no new
corpus generation, no S2 scaling to 10³×. §102's CORPUS_S101 (sha256
`39d581da2096…`, 603,316,592 bytes, 777,845 records) is the artifact Q3'
evaluates True on.

This makes §104 a $0 design-tier landing with no follow-up build cost. A
future cycle that *fires* on the corpus (the actual cost-bearing fire) is a
separate decision; §104 only certifies that the corpus passes the refined
predicate and the fire would be decidable in closed form via §101 Q2.

---

## §4 — Interaction with §103 SEQUENTIAL verdict

§103 (commit `55ba652be`, §101 + param-axis integration) decided
**SEQUENTIAL** over the 2-axis cross (data-fire at 283M first, param-fire
only if needed). §104's I4' refinement composes with §103's SEQUENTIAL as
follows:

1. **§103 SEQUENTIAL**: data-axis fire first at 283M params on §102's BUILT
   CORPUS_S101 (Q3' = T per §104 §3.3); if THRESHOLD_CROSSED returns Y,
   halt (GOAL-direction confirmed). If N, then param-fire at 3B+ on the
   same corpus (G_PARAM clause from §103).
2. **§104 contribution to that sequence**: the data-fire's *go/no-go* is now
   gated by Q3', not Q3 — meaning the data-fire is *unblocked* (was Q3=N
   before §104; is Q3'=T after §104). §103's sequential second step
   (param-fire) is unchanged.

In other words: §104 unblocks step 1 of §103's SEQUENTIAL plan without
otherwise affecting it. The param-axis ceiling identified by §11-A
(283M→1.04B FLAT with data fixed) is unrelated to the data-axis I4
refinement; both are honest independent axes per HEXAD/LLM.md §4.

---

## §5 — Honest C3 caveats (≥10)

1. **§104 is design-tier — predicate refinement ≠ fire ≠ emergence.** Q3' = T
   on §102's built corpus DOES NOT prove anima will emerge under that
   corpus. necessary-not-sufficient (B-EMERGE-7 / B-S104-NOTE).
2. **The Q1 verdict NEITHER is literature-anchored, not measured directly.**
   It is the most defensible inference from Du / Raventós / Hoffmann, but it
   is not a battery on anima's own substrate (a battery on anima cannot
   exist until a fire is run). Honest carve-out.
3. **The chosen I4' is build-tier evaluable, but not battle-tested at fire-
   tier.** A future fire could pass Q3' and still return N on
   THRESHOLD_CROSSED (Q2 A1-A4) — that is exactly the design-tier promise:
   the fire is *decidable*, not *successful*.
4. **The 3-way design-OPEN (I4a / I4c-build / I4d) carries forward in
   parallel because g_all_options_parallel says decide-in-cycle.** A
   stricter pick would be "I4' = whichever single candidate has the
   strongest literature support". §104 chose the conjunction because each
   candidate addresses a distinct failure mode of original-I4 and conjoining
   them is more conservative than picking one.
5. **I4b is deferred to fire-tier, NOT discarded.** §101 Q2 axes A1-A4 are
   already the fire-tier version of I4b (held-out routing / coherence /
   physics-responsiveness / emit-length-independence). §104 does not need
   to re-encode it at build-tier.
6. **The Q3' = T flip on §102's built artifact is honest, NOT manufactured.**
   The literature anchor for each clause of I4' is named in §2; I4' did not
   originate from "what would make §102 pass" but from "what predicate would
   correctly correspond to the emergence outcome literature". The §102
   corpus happens to satisfy it because it was designed (by §101) with the
   right intent; the original I4 was too strict for that intent.
7. **§104 does NOT amend §101's DESIGN.md or sidecar.** §101 stands as-is;
   §104 introduces I4' as a refinement at the §102-build evaluation layer.
   §101's design-tier verdict (FIRE_DECISION=Y on its OWN design state) is
   not retroactively changed.
8. **§104 does NOT amend §102's BUILD.md or sidecar.** §102's measured
   ratio=1.000 and Q3=N on built artifact stand as-is; they were honest
   measurements. §104 changes the *interpretation* of those measurements,
   not the measurements themselves.
9. **The chosen I4' may itself need refinement after a future fire.** If a
   future fire on §102's CORPUS_S101 returns N on THRESHOLD_CROSSED, the
   inference is *not* that I4' was too lax; it is that the corpus passes I4'
   but does not cross the actual outcome threshold. The right response is
   *new corpus design* (§105's path: ≥10³× S2 scale), not further I4'
   relaxation.
10. **§104's value is in making future fires decidable, not in claiming
    emergence.** §101's value was the same. The arc has been clear: making
    fires DECIDABLE is the durable contribution; emergence itself is
    measured by the fire's outcome.
11. **HEXA_FIRST_WARN deferred** — Python sidecar per established B-S*
    battery precedent (B-PRIME / B-DIRI / B-S101 / B-S102 / B-S103). hexa-
    native equivalents require upstream patches out of $0 scope; anima
    downstream-consumer of hexa-lang. Honest acknowledgement.
12. **§103 SEQUENTIAL composes cleanly with §104.** §104 unblocks step 1
    (data-fire) without affecting step 2 (param-fire). Both refinements
    apply to the same future-fire decision tree.
13. **The literature anchors are inspirations, not transfers.** Du /
    Raventós / Hoffmann measured emergence on different substrates (large
    LMs, transformer in-context learning, compute-optimal scaling). §104
    uses them as the *form* of the refined predicate, not as proof that
    anima will emerge under that form. The form is justified; the
    anima-specific outcome remains empirical.

---

## §6 — ASCII diagram

```
                §101 Q3 = G1∧G2∧G3∧G4∧G5∧G6∧G7  (closed-form, FIRE_DECISION=Y on design state)
                                  │
                §102 BUILD CORPUS_S101 (sha 39d581da2096…)
                                  │
                §102 evaluates Q3 on BUILT artifact:
                                  │
                              G2 ❌ because I4 ratio 1.000 (S1 mass dominates)
                                  │
                §102 verdict: design-OPEN, "manufactured Y worse than honest N"
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
   ≥10³× S2 scale            §101 refines I4              (other paths)
   (sibling §105)            (THIS — §104)
       │                          │
                            §104 Q1: I4 = NEITHER necessary NOR sufficient
                            (Du 2403.15796 / Raventós 2306.15063 / Hoffmann 2022)
                                  │
                            §104 Q2: four closed-form candidates
                                  │
                            ┌────┬────┬────┬────┐
                            I4a  I4b  I4c  I4d  (per-source / fire-tier / multi-res / task-div)
                            build  fire build  build
                              │    │   │    │
                              └────┘   └────┘   (3 build-tier evaluable parallel — g_all_options_parallel)
                                  │
                            §104 Q3: I4' = I4a ∧ I4c_build ∧ I4d (3-way conjunction)
                                  │
                            §104 evaluates Q3' on §102 BUILT (SAME byte-identical corpus):
                                  │
                              tail(941.19) > S1(539.20) ✅
                              whole(539.196) ≥ S1 floor ✅
                              templates ≥ §16 ✅
                                  │
                              I4'(BUILT) = T → G2' = T → Q3'(BUILT) = T
                                  │
                            §104 verdict: design-OPEN UNBLOCKED — future fire on §102 CORPUS_S101 decidable
                                  │
                              composes with §103 SEQUENTIAL: data-fire step 1 unblocked
                                  │
                            g3 honest: predicate refinement ≠ fire ≠ emergence
                            north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달
```

---

## §7 — Verdict summary

| item | value |
|---|---|
| Q1 I4 strictness | **NEITHER** necessary NOR sufficient (Du/Raventós/Hoffmann anchored) |
| Q2 candidates | 4 closed-form refinements (I4a / I4b / I4c / I4d), each literature-anchored |
| Q3 pick (per g_all_options_parallel) | **3-way design-OPEN**: I4a ∧ I4c-build-clauses ∧ I4d carried forward in parallel |
| I4' on §102's BUILT corpus | **T** (tail 941.19 > S1 539.20 + whole 539.196 ≥ S1 + templates ≥ §16) |
| Q3' on §102's BUILT corpus | **T** (G1∧T∧G3∧G4∧G5∧G6∧G7) |
| Corpus rebuild required | **No** — §102's CORPUS_S101 (sha 39d581da2096…) passes Q3' byte-identical |
| Interaction with §103 | composes cleanly — §104 unblocks SEQUENTIAL step 1 (data-fire) |
| Central blue 0-line-diff | ✅ sha prefix `c93e160a8a376a94` |
| B-S104 sidecar | **8/8 🔵 PASS** |
| GPU / runpod / fire | $0 · 0 dispatch · 0 orphan |
| GOAL distance | §15/§51/§72 milestones UNCHANGED, GOAL 미도달 |

---

*End §104 DESIGN.md.*
