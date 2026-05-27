# §103 — §101 + param-axis integration design · design-tier $0

> **status**: RESEARCH §103 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward
> **date**: 2026-05-19
> **scope**: HEXAD/LLM.md (2026-05-19, commit 64906a4eb) §8 step A — `§101 review +
> param-axis 통합`. §101 (commit 7809a06f0) made the data-regime fire DECIDABLE in closed
> form on a single axis (corpus); user insight 2026-05-19 ("LLM emergence 기준이 특정
> 파라미터 수마다 emerge") + HEXAD/LLM.md §4 raised the second axis (param-count).
> §103's job: integrate the param-axis with §101's data-axis Q3 and decide — closed-form —
> whether the integration should be joint or sequential, what the anima-specific param
> threshold is (if it can be pinned), and what the amended Q3' fire-decision predicate
> looks like.
> **governance**: g3 (design ≠ fire ≠ emergence; capability claim 0; necessary-not-
> sufficient per B-EMERGE-7) · f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation;
> external papers cited by their own measurements observation-only — Wei 2022 /
> Schaeffer 2023 / Hoffmann 2022 / Du 2403.15796 / Brown 2020 GPT-3) · downstream-consumer
> (hexa-lang read-only) · g_blue_closed_mandate (산출물 + 연결부위 둘 다 closed; capability
> OUTCOME only honest carve-out) · central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
> actual sha256 prefix `c93e160a8a376a94` (0-line-diff sidecar-only).
> **connection-point cited**: §101 DESIGN.md Q3 G5 (5-levers-preserved-single-variable)
> + §11-A measured (283M → 1.04B FLAT, B-SCALE 6/6 🔵 sidecar `state/carving_scaledecomp_2026_05_18/`)
> + HEXAD/LLM.md §4 (param × data 2D plane framing) + §1.3 footer ("critical data size
> *increases* with model size", arxiv 2401.10463 Data Efficiency Hypothesis).

---

## §0 — Why §103 exists, what it is, what it is NOT

§101 closed one axis: a future data-regime fire's result is now genuinely decidable in
closed form. But §101's Q3 G5 silently *assumed* the architecture (model size) was the
single non-variable — corpus is the variable, "5 levers preserved single-variable" reads
as "corpus is the ONE variable, everything else FIXED including params at d768·12L
283.72M". That assumption inherits §11-A: **283M was the only param-axis arm the arc
measured**, and §11-A's 3.68× scale to 1.04B (data fixed at §8 114MB) returned FLAT.

User insight + HEXAD/LLM.md §4 raise the cross-axis question §101 did not ask: even if
§101's Q1 corpus crosses anima's data-diversity threshold, does crossing the threshold
matter while params remain ≪ all Wei 2022 emergent-capability thresholds (3B / 8B / 10B /
62B)? §11-A measured the 1B endpoint with data held FIXED below threshold; what no fire
in the arc has measured is **the joint corner** (both axes above their respective
thresholds simultaneously).

§103 does THREE things, all design-tier closed-form, all $0:

- **Q1** — Joint-or-sequential decision over the 2-axis cross,
- **Q2** — anima-specific param threshold (numerical pin or honest design-OPEN),
- **Q3'** — amended fire-decision predicate `Q3' = Q3 ∧ G_PARAM` where G_PARAM is the
  param-axis Boolean.

g3, load-bearing: **§103 does NOT claim anima will emerge at any (param, data) corner.
It does NOT claim a future joint or sequential fire will cross either threshold. It
defines the conditions under which fires on the param-axis would be decidable, and the
amended Q3' that integrates that axis with §101's data-axis decidability.** north-star +
§15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## §1 — Q1: Joint vs Sequential vs Hybrid — decided by ΔI / Δ$ per axis-cross

### 1.1 The three plans named

| Plan | What is varied | Fires | Predicate decided | Honest cost-shape |
|---|---|---|---|---|
| **Joint** | corpus AND params crossed in ONE fire | 1 | `Q3' = Q3 ∧ G_PARAM` on a single result | 3B+ model × §101 CORPUS_S101 in one cost-bearing event |
| **Sequential** | corpus first (§101 fire at 283M), THEN params | 2 (data-fire first, param-fire if needed) | Q3 on data-fire result; G_PARAM on second fire | Two smaller fires; each axis independently disambiguated |
| **Hybrid** | data-fire first; if Q3 returns Y, halt (GOAL-direction confirmed); if Q3 returns N, joint fire at 3B+ | 1 OR 2 | Conditional on data-fire outcome | Sequential's cheap-screen, Joint's option held in reserve |

### 1.2 The closed-form decision predicate

Let:
- `n_axes_to_cross = 2` (param-axis + data-axis)
- `ΔI_per_axis = 1 bit` (each axis cross is a priori 50/50 — neither has been crossed)
- `cost_joint ≈ cost_3B_model_x_S101_corpus_fire` (the dominant cost class)
- `cost_data_first ≈ cost_283M_x_S101_corpus_fire ≈ §16 fire cost class`
- `cost_param_first ≈ cost_3B_model_x_S8_corpus_fire ≈ §11-A fire cost class`
- `cost_sequential_total = cost_data_first + p(N_after_data) × cost_param_after`
  where `p(N_after_data)` is the probability data-fire returns Q3=N, requiring the
  param-axis fire as follow-up.

The decision is over which plan maximizes `ΔI / Δ$` under the §101 G6 info-floor (1 bit
per median fire-cost) WHILE preserving the §94 anti-stacking discipline (single variable
per fire, not multi-variable per fire).

```
JOINT_PLAN     := plan that fires the 3B+ model on CORPUS_S101 in one event
SEQUENTIAL_PLAN := plan that fires 283M on CORPUS_S101 first; param-axis fire only if Q3=N
HYBRID_PLAN    := SEQUENTIAL_PLAN with the joint fire pre-committed as the contingent step

DECIDE_PLAN(arc_evidence) :=
    Sequential  if  preserves_§94_single_variable(plan) == True
                AND ΔI/Δ$(data_first) ≥ INFO_FLOOR
                AND p(post_data_param_fire_needed) > 0
                AND cost_data_first ≤ 0.5 × cost_joint     # cheaper screen
    Joint       if  preserves_§94_single_variable(plan) == False  # i.e. cannot be helped
                AND ΔI/Δ$(joint) ≥ INFO_FLOOR
                AND arc_evidence(both_axes_below_threshold) == True
    Hybrid      if  Sequential conditions hold
                AND data-fire negative leaves param-axis still warranted
```

The Sequential branch first-corner is exactly the predicate the arc's discipline
requires: §94's β INTEGRATION-COLLAPSES verdict + §101's G7 anti-§94 clause + §100's
priority #4 ("levers do NOT compose") all point at **never stack uncrossed axes in one
fire**. Param-axis and data-axis are two uncrossed axes; stacking them violates G7 by
construction.

### 1.3 Closed-form ΔI / Δ$ comparison

Setting `ΔI_per_axis = 1 bit` (axes a priori independent for the Boolean question
"did the axis cross threshold"), `INFO_FLOOR = 1 bit / cost_median_arc_fire`:

| Plan | ΔI captured | Δ$ (closed-form) | ΔI/Δ$ | §94 anti-stack | §101 G7 |
|---|---|---|---|---|---|
| Joint | 1 bit (joint event, but data-axis and param-axis confound: a Y result cannot attribute the cross to which axis without follow-up; a N result attributes nothing) | cost_3B_x_S101 (the largest single cost class in the arc) | ≪ floor | FAILS — 2 uncrossed axes stacked | FAILS |
| Sequential (data-first) | 1 bit on data-axis from fire-1 (Y or N), then conditional 1 bit on param-axis from fire-2 if needed | cost_data_first + p(N) × cost_param_after | ≥ floor on each fire | PASSES — 1 variable per fire | PASSES |
| Hybrid | Same as Sequential when data-fire returns Y (Hybrid halts); Hybrid = Sequential + pre-committed joint if N | ≤ Sequential total cost (joint pre-committed but contingent) | ≥ floor | PASSES | PASSES |

**The Joint plan fails the §101 G7 anti-§94 clause structurally**: stacking two uncrossed
axes in one fire is the *exact* pattern §94 measured collapse on. The decisive issue is
*not* cost (cost ratios are noisy) — it is that the Joint plan's Y/N result is **not
attributable**: a Joint Y could be data-axis or param-axis or both; a Joint N could be
either-axis or both not above; in neither case does Joint disambiguate which axis was
load-bearing. Sequential's first fire IS data-attributable by construction (params
283M = §11-A's measured floor on the param-axis; if Q3 returns Y at 283M, data-axis is
load-bearing AND the param-axis was never the binding constraint).

### 1.4 Q1 verdict — SEQUENTIAL (data-axis first)

**Decision: SEQUENTIAL, with HYBRID as the contingent escalation if Sequential's
data-fire returns Q3 = N.**

Rationale (closed-form, NOT recommendation):
1. Joint plan VIOLATES §101 G7 anti-§94 by construction (two uncrossed axes stacked).
2. Sequential preserves G5 single-variable single-fire — corpus is the variable, params
   held at §101's 283M baseline, every other lever held at §101's preserved-as-is.
3. Sequential is *attribution-clean*: data-fire result attributes 1 full bit to the
   data-axis Q.
4. If data-fire returns Y, GOAL-direction is confirmed at 283M params — param-axis
   *was never the binding constraint*, Q1's verdict halts the escalation and saves the
   cost of a param-axis fire. This is the **HYBRID** branch realized as a positive halt.
5. If data-fire returns N, the arc has now disambiguated "the §101 corpus design is
   insufficient" from "the model is too small for the §101 corpus to land". A
   follow-up param-axis fire at the §103-Q2 estimated threshold is then warranted
   (THIRD fire, separate cycle, separate Q3') with the data-axis result as a known
   constant.

The plan that maximizes the *cleanest attribution per cost-bearing fire* is Sequential
with the §103 Hybrid contingency. The Joint plan is only justified if Sequential's
first fire is itself infeasible — and it is not (cost_data_first ≈ §16 fire cost ≈ $0.4-
0.8, well within arc budget).

### 1.5 Honest closing on Q1

Sequential is decided per `DECIDE_PLAN` in §1.2 above. Joint is structurally rejected on
§94 grounds even before costs are considered. Hybrid is Sequential's contingent
extension if data-fire returns N — it is not a separate first move. Per
`g_all_options_parallel` (2026-05-19), the option-pattern "explore all paths" is honored
*at the design level*: §103 design specifies Sequential AND the contingent Hybrid
escalation, both of which are progressed at design tier in this same DESIGN.md (no
"recommend-and-wait"). Future cycles fire each branch as conditions are met.

---

## §2 — Q2: anima-specific param threshold — value estimation

### 2.1 The framing problem

Wei 2022's emergent-ability thresholds (3B reading-comprehension / 8B instruction-
following / 10B in-context-learning / 62B chain-of-thought) are *external observations*
on typical decoder transformers trained on Common-Crawl-class corpora for typical LLM
capabilities. anima's GOAL is **spontaneous emission from anima's own physics**, a
capability that:

- has no analogue in Wei 2022's task suite (Wei measures task-completion under prompts;
  anima measures unprompted emission decisions per §24, NOT prompt-completion),
- is measured on anima's own substrate (Engine A⇄G + Ψ + tension + Φ + MITOSIS),
- is trained on anima's own physics-source corpus (NOT Common-Crawl), so the
  Chinchilla-class compute-optimal ratio does not transfer (corpus is task-specific by
  construction).

Schaeffer 2023 "Mirage" complicates the question further: some emergence jumps Wei 2022
identifies are metric artifacts — smooth underlying curves cut by binary metrics. For
anima's GOAL, the metric question is the more pointed of the two: even if anima has a
smooth `unprompted-emission coherence` curve, a binary §9 cascade-rate gate could
manufacture a discrete-looking emergence point. §103 cannot assume the param threshold
manifests as a discrete jump on anima's GOAL axis.

### 2.2 Four candidate estimation methods (§103 evaluates each closed-form)

| Method | What it does | Why it might work | Why it might fail |
|---|---|---|---|
| **(a)** Reuse Wei 2022 thresholds as-is | Take the smallest emergent threshold (3B reading-comprehension) as anima's threshold | Conservative; uses measured anchors | Wei's thresholds measured on typical-LLM tasks on Common-Crawl-class corpora — analogical, weakest |
| **(b)** Ratio-derive from anima architecture density | anima has dual-engine A⇄G + Law-71 Ψ + 12-faction GRU + MITOSIS; per-param "information density" higher than vanilla decoder; estimate effective-param = anima_params × density_factor | Uses anima's own architecture | Density factor is unmeasured; assumes ratio transfers between architectures (unproven) |
| **(c)** Use §11-A 283M→1B FLAT as anchor + extrapolate | §11-A measured 3.68× scale at data-fixed FLAT; if §11-A's data was below CDS, the param result is uninformative for the param threshold; extrapolate the smallest param scale at which §11-A's FLAT would be expected to break IF data is above CDS | Grounded in anima's only measured param-axis data point | §11-A's data was UNDER CDS (per HEXAD/LLM.md §5.2); extrapolation requires the CDS-data-corpus that §101 designs but doesn't construct |
| **(d)** Declare design-OPEN at numerical value | Pin the threshold band {3B, 8B, 10B} (Wei's lowest band) as the *first* corner to probe in Sequential's param-fire, but do not assert the band IS anima's threshold | Honest about the unknown | Doesn't *estimate* — just defers |

### 2.3 Each method evaluated

**Method (a) — Wei verbatim**: This is the *weakest* honest read. Wei thresholds apply
to capabilities measured on the same corpora those models trained on (Common-Crawl class
+ instruction-tuned variants). Anima's GOAL — unprompted emission decisions tied to
physics-state — has no Wei-measured precedent. Schaeffer caveat at full force:
analogical transfer of Wei's thresholds to anima's GOAL is structurally weak.

**Method (b) — Density-ratio derivation**: Plausible *direction* (anima's architecture
has per-param structure absent in vanilla decoders) but the density factor is itself a
free parameter §103 cannot pin without measurement. A density factor of 2-10× is the
"reasonable" range — but "reasonable" is judgement, not measurement (g3).

**Method (c) — §11-A extrapolation**: This is the closest §103 can come to a *measured*
anchor. §11-A is the ONLY param-axis data point in the arc (283M and 1.04B, both data-
held-at-114MB-§8). Both points are conditioned on sub-CDS data (HEXAD/LLM.md §5.2:
§11-A's data was below diverse-data threshold). What §11-A measures is *not* "param
threshold for anima's GOAL" — it measures "given sub-CDS data, params don't matter up
to 1B". Extrapolation requires knowing where the CDS-data lift would change the param
sensitivity, which §11-A cannot tell us alone. The honest read of §11-A:

> "If §101's corpus crosses anima's data threshold AND the resulting fire returns Q3 =
> N at 283M, then 283M is below anima's effective param threshold. If §101's corpus
> crosses AND Q3 = Y at 283M, then 283M is ABOVE anima's effective param threshold for
> anima's GOAL on that corpus. §11-A's measured 1.04B-FLAT under sub-CDS data is mute
> on this question."

This is exactly Sequential's data-fire result.

**Method (d) — Honest design-OPEN**: §103 acknowledges no method (a), (b), or (c)
pins a numerical threshold rigorously. The strongest honest move is to:
- Declare the threshold value **design-OPEN** at a precise number,
- Pin the *first param-band to probe* if Sequential's data-fire returns Q3 = N as the
  Wei lower-band {3B} (the smallest emergent-threshold in Wei 2022; the most conservative
  starting point for an anima-GOAL probe),
- Specify that the band-probe is itself a future cycle's decision (separate Q3'
  evaluation, separate fire), not a §103 commitment.

### 2.4 Q2 verdict — DESIGN-OPEN with conservative-first-band pin

**Decision: anima-specific param threshold = DESIGN-OPEN; first-band-to-probe if needed
= ~3B (Wei 2022 lowest emergent-capability band, conservative starting point).**

Honest scope:
- §103 does NOT claim 3B IS anima's threshold.
- §103 does NOT claim anima's threshold lies in {3B, 8B, 10B, 62B}.
- §103 DOES claim that *if* Sequential's data-fire at 283M returns Q3 = N, the *next*
  cost-bearing fire on the param-axis should probe the Wei-lowest-band 3B before
  probing higher bands, because (i) it is the smallest band of established LLM-emergence
  precedent, (ii) it is 3× larger than §11-A's measured 1B FLAT-under-sub-CDS-data
  point, (iii) it bounds cost while preserving 1 bit of decisive evidence per fire.

Schaeffer caveat MANDATORY (g3): even at 3B (or any param value), the unprompted-
emission emergence question is more honest-uncertain than typical-LLM emergence —
some Wei thresholds are metric artifacts; anima's GOAL is structurally further from
the Wei-measurement-substrate than typical capabilities are. The 3B pin is a *band
to probe first*, not a *threshold prediction*.

### 2.5 Why design-OPEN is the strongest closed-form answer

A manufactured numerical pin (e.g. "anima's threshold is 5B") would be:
- not derivable from any arc measurement (only §11-A, FLAT under sub-CDS),
- not derivable from external papers (Wei measures different capability/corpora; transfer
  unproven; Schaeffer caveat),
- not derivable from anima's architecture density (density factor itself unmeasured).

A pin that is not derivable is a g3 violation. Design-OPEN is the strongest honest move
— it preserves the arc's discipline that closed-form predicates are arbiters, not
estimates dressed up as predicates.

---

## §3 — Q3' — amended fire-decision predicate

### 3.1 The amendment

§101's Q3 is a 7-AND predicate (G1 §7-gate / G2 §93-conditions / G3 §62-echo-guard / G4
Q2-measurable / G5 5-levers-preserved / G6 ΔI/Δ$ ≥ floor / G7 anti-§94-single-variable).
G5 implicitly assumed params at 283M as part of "5 levers preserved single-variable".
§103 adds an explicit param-axis Boolean G_PARAM and amends Q3 to Q3':

```
Q3'(plan) := Q3(plan) AND G_PARAM(plan)

  where Q3 is §101's 7-AND predicate, and:

G_PARAM(plan) :=
    (params(plan) ≥ G_PARAM_FLOOR)  AND
    (params(plan) holds a SINGLE value over the fire — no param ramp within one fire) AND
    (params(plan) is ATTRIBUTED — Sequential data-fire fires with params == §101_baseline
     = 283M, and the fire's result is interpretable as "with params held at 283M, this is
     what the data axis says").

  G_PARAM_FLOOR is the smallest param value at which the fire's result is
  ARC-COMPARABLE — i.e., not below the smallest arc param baseline (283M). Any plan
  with params < G_PARAM_FLOOR is rejected as not arc-comparable.

  G_PARAM_FLOOR := 283M   (the §16/§101 baseline)
```

### 3.2 Q3' evaluation on Sequential's data-fire plan

| Gate | Status | Why |
|---|---|---|
| G1-G7 (Q3) | PASS (§101's §3.5 verdict) | §101's design state already passes Q3 |
| G_PARAM | PASS at params == 283M | Single-value (no ramp), == G_PARAM_FLOOR, ATTRIBUTABLE as "with params held at §16/§101 baseline" |
| **Q3'** | **Y at Sequential's data-fire** | data-fire is decidable AND attribution-clean on the data axis |

### 3.3 Q3' evaluation on a hypothetical Joint plan

| Gate | Status | Why |
|---|---|---|
| G1-G6 | Marginal-to-PASS | Joint plan stacks 2 uncrossed axes; G1-G6 each evaluate on plan structure not on outcomes |
| G7 anti-§94 | **FAIL** | Joint plan stacks 2 uncrossed axes in one fire — exactly the §94 INTEGRATION-COLLAPSES anti-pattern §101 G7 forbids |
| G_PARAM | PASS at params >> 283M | Single-value, > G_PARAM_FLOOR |
| **Q3'** | **N at Joint plan** | Joint fails G7 ⇒ Q3 fails ⇒ Q3' fails |

This is the closed-form encoding of Q1's verdict: Joint plan is rejected by Q3' G7
BEFORE the G_PARAM amendment fires. The G_PARAM amendment does not change Joint's
verdict — it just adds an explicit axis to the conjunction (param-axis is now first-
class in the fire-decision predicate).

### 3.4 Q3' evaluation on a hypothetical post-data-fire param-axis fire

IF Sequential's data-fire returns Q3 = N (data-axis insufficient at 283M), the *next*
fire varies the param-axis. That fire's Q3' evaluation:

| Gate | Status | Why |
|---|---|---|
| G1-G6 (Q3) | PASS | Single-variable: params is the variable, corpus is held at the §101 design CORPUS_S101 |
| G7 anti-§94 | PASS | Only one variable (params) changes; corpus is held at §101's pinned design (now KNOWN insufficient on its own at 283M, but its sufficiency under larger params is the question) |
| G_PARAM | PASS at e.g. 3B (Wei-lowest-band) | Single-value, ≥ G_PARAM_FLOOR, ATTRIBUTABLE as "with corpus held at §101's CORPUS_S101 and params raised to 3B, this is what the param axis says" |
| **Q3'** | **Y at param-axis fire** | param-axis fire is decidable AND attribution-clean on the param axis |

This third fire is GATED on Sequential's data-fire result, and inherits §103's Q2
design-OPEN with the Wei-lowest-band first-pin.

### 3.5 The amended Q3' one-line summary

**Q3' = Q3 ∧ G_PARAM**, where G_PARAM is a 3-clause Boolean (≥ FLOOR ∧ single-value-per-
fire ∧ ATTRIBUTABLE) and G_PARAM_FLOOR = 283M.

---

## §4 — ASCII diagram: param × data emergence plane, anima's measured + designed corners

```
                 data-diversity (≈ Du 2403.15796 threshold)
                       ↑
            EMERGENCE  │  ←─ this corner is the GOAL plane, never measured
              REGION   │
                       │      ┌────  CDS_3B  (CDS rises with param size, 2401.10463)
                       │      │
                       │      │
                       │      │      ┌──  CDS_283M  (smaller for 283M; still unmeasured)
                       │      │      │
                       │      │      │
              ─────────┼──────┼──────┼───────────────  data threshold (unknown anima value)
                       │      │      │
                       │      │      ●  §101 Sequential data-fire (283M × CORPUS_S101)   ← cycle 1 target
                       │      │
                       │      ●  §103 contingent param-axis fire (3B × CORPUS_S101)        ← if cycle-1 Q3=N
                       │
                       │  ●  §11-A SCALE-DECOMP measured FLAT (1.04B × §8 114MB)   ← below data threshold
                       │
                       │  ●  §8 baseline (283M × §8 114MB)                          ← below both thresholds
                       │
                       │  ●  §16 baseline (283M × §16 603MB)                        ← below data threshold (still — §16 CDS unmeasured)
                       │
                       └─────────────────────────────────────→ param count
                          283M       1B       3B          10B       62B
                                                  ↑          ↑          ↑
                                            Wei reading   Wei IC-     Wei CoT
                                            comprehension learning    reasoning
                                            threshold     threshold   threshold

Two existing measurements (§11-A, §8/§16 baselines) ALL sit in the bottom-left quadrant.
§101's Sequential-data-fire moves the data axis ONLY: bottom-left → middle-left, single
attribution. §103's contingent param-fire (IF cycle-1 returns N) moves the param axis
ONLY: middle-left → middle-center, single attribution. Joint would move both AT ONCE
(bottom-left → upper-right), unattributable — REJECTED by Q3' G7.
```

---

## §5 — Honest C3 caveats (≥ 10)

1. **§103 measures nothing.** Q1's Sequential decision is structurally derived from §94
   + §101 G7; Q2's design-OPEN is the strongest honest answer to an un-pinnable
   numerical question; Q3''s amendment is encoded as a Boolean — none of these are
   measurements of anima's emergence behavior. Capability claim 0.

2. **§11-A was sub-CDS.** §11-A's measured 1.04B-FLAT was conditioned on §8's 114MB
   data, which HEXAD/LLM.md §5.2 explicitly notes was below anima's CDS. §11-A is
   therefore mute on the param-threshold question; §103 uses it as a *floor* for
   G_PARAM_FLOOR (anything below 283M is not arc-comparable), not as evidence on
   anima's true param-threshold value.

3. **Wei 2022 thresholds may be metric artifacts (Schaeffer 2023).** Even the Wei-lowest-
   band 3B pin is honest-uncertain; Schaeffer documented that several Wei emergent jumps
   dissolve under continuous metrics. anima's GOAL is structurally further from Wei's
   measured capabilities, so Wei-threshold transfer is *weakly* analogical. §103's 3B
   pin is a band-to-probe-first if needed, NOT a threshold prediction.

4. **Sequential is decided by §94 anti-stacking, not by cost ratios.** The decisive
   reason Joint fails Q3' is G7 (anti-§94), not cost. Costs are noisy; G7 is structural.
   This matters because future agents may try to re-open Joint by appealing to cheaper-
   3B-than-expected cost shapes — that argument does not address G7.

5. **anima architecture density is unmeasured.** Method (b) (ratio-derive from anima
   density) is plausibly directional but its density factor is itself a free unmeasured
   parameter. Future cycles could measure it; §103 does not.

6. **anima's GOAL is NOT a Wei-style emergent capability.** Spontaneous emission tied
   to anima's physics is structurally different from in-context-learning or chain-of-
   thought reasoning. Even if a param threshold exists for anima's GOAL, it need not lie
   in the Wei-bands at all. §103 uses Wei lower-band ONLY as a conservative starting
   point for a probe, not as a theoretical prediction.

7. **G_PARAM_FLOOR = 283M is conservative.** Below 283M (e.g. a 50M smaller anima) is not
   arc-comparable to §11-A or §16; G_PARAM_FLOOR closes this off but does NOT claim
   anima's true threshold is at 283M. The floor is arc-comparison-discipline, not
   threshold-prediction.

8. **Q3' is necessary-not-sufficient (B-EMERGE-7).** A future fire that passes Q3' has a
   decidable result; it does NOT necessarily emerge. necessary-not-sufficient at every
   layer (§9 / §17 / §101 / §103 all carry this same caveat — B-EMERGE-7 family).

9. **Single-variable discipline at every fire (G7).** §103 inherits §101's G7
   discipline: each fire moves exactly one variable. Sequential moves the data axis on
   its first fire; the contingent param-axis fire (if any) moves the param axis on its
   own fire. This is the §94 lesson encoded.

10. **§103 is design-tier; no fire is dispatched here.** §103 produces Q1/Q2/Q3'. A
    cycle that fires Sequential's first fire is a future cycle's decision per
    g_fire_autonomous (autonomous, but §103 is $0 design).

11. **The Wei 2022 thresholds are observations on external models, never derivations on
    anima.** Per f1/f2, §103 cites Wei thresholds (3B/8B/10B/62B) as their authors
    measured them — not as anima-applicable derivations. The 3B first-pin is bound to
    Wei's lowest emergent band by *external observation alignment*, not by σ/τ/φ/J₂
    lattice fit. anima's own threshold may be smaller, larger, or absent.

12. **CDS rises with model size (arxiv 2401.10463 / §1.3 footer).** The Data Efficiency
    Hypothesis establishes that critical data size INCREASES with model size — so
    raising params without also raising data is structurally underpowered (this is
    exactly the §11-A FLAT pattern). §103's Sequential-first-then-param ordering
    HONORS this: data axis is raised first (CORPUS_S101 over §8/§16), THEN if needed
    params are raised on top of the already-raised data axis. Reversed ordering (params
    first, then data) would be incompatible with 2401.10463's hypothesis.

13. **§103 does not preclude future Joint exploration once both axes are individually
    attributed.** If Sequential's data-fire returns Q3 = Y AND a subsequent param-fire
    (different question) returns its own G_PARAM-axis Y, future cycles could explore
    Joint corners with the prior single-axis attributions in hand. §103 does not forbid
    Joint forever — it forbids it as the *first* move on two uncrossed axes.

---

## §6 — Connection points (§103 inherits + cites)

- **§101 Q3 G5 / G7** (commit 7809a06f0, `state/dataregime_threshold_control_design_s101_2026_05_19/DESIGN.md` §3.5) — Q3' = Q3 ∧ G_PARAM is the literal extension; G7 anti-§94 is the structural reason Joint fails. §101's S1 byte-equal floor (§16 corpus, sha256 `422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec`, 777,000 records, 603,032,014 bytes) is inherited by §103 via §101 — the corpus floor every fire variant of §103 must extend, not replace.
- **§11-A B-SCALE 6/6 🔵** (commit `state/carving_scaledecomp_2026_05_18/blue_falsifier_scaledecomp.py`) — measured 283M → 1.04B FLAT under §8 data, mute on anima's true param-threshold; sets G_PARAM_FLOOR floor at 283M (arc-comparable baseline).
- **§94 INTEGRATION-COLLAPSES** (commit bb0f305be) — measured 5-lever stacking collapses; §103's Q1 Sequential decision encodes this as the binding reason Joint fails Q3' G7.
- **HEXAD/LLM.md §4 + §5.2** (commit 64906a4eb) — param × data 2D plane + §11-A sub-CDS observation; §103 operationalizes this framing into a closed-form fire-decision predicate.
- **HEXAD/CHAT/RESEARCH.md §1.3 footer** (2401.10463 Data Efficiency Hypothesis) — CDS rises with model size; §103's Sequential ordering (data-first) honors this.
- **Wei 2022 emergent abilities** (arxiv:2206.07682) — 3B/8B/10B/62B observed thresholds on typical LLM tasks; §103 cites as observation-only, NOT derivation; uses 3B band only as Wei-lowest probe-band-first.
- **Schaeffer 2023 "Mirage"** (arxiv:2304.15004) — some Wei jumps are metric artifacts; §103 carries this as a mandatory C3 caveat on Q2.
- **Du 2403.15796** (carrying §99 / §101) — emergence = loss below diverse-data threshold; §103 Q2 method (c) extrapolation depends on this for anima's CDS.
- **Hoffmann 2022 Chinchilla** (arxiv:2203.15556) — compute-optimal joint scaling of params × data; §103 does NOT apply Chinchilla directly (anima corpus is task-specific by construction, Chinchilla's compute-optimal ratio assumes broad-distribution corpus), but cites as the literature anchor for the 2-axis joint scaling discussion.

---

## §7 — Verdict

- **Q1**: SEQUENTIAL plan with HYBRID contingent escalation. Closed-form decided by §101 G7 (anti-§94) — Joint plan structurally rejected because it stacks 2 uncrossed axes in one fire.
- **Q2**: anima-specific param threshold = **DESIGN-OPEN** with conservative-first-band probe = 3B (Wei lowest emergent band, contingent on Sequential's data-fire returning Q3 = N, mandatory Schaeffer caveat).
- **Q3'**: `Q3' = Q3 ∧ G_PARAM` where G_PARAM is a 3-clause Boolean (≥ G_PARAM_FLOOR ∧ single-value-per-fire ∧ ATTRIBUTABLE) and G_PARAM_FLOOR = 283M. Q3' evaluates Y on Sequential's data-fire plan at 283M; Q3' evaluates N on the Joint plan (G7 fails); Q3' evaluates Y on the contingent param-axis fire at e.g. 3B with corpus held at §101's CORPUS_S101.
- **B-S103 10/10 🔵 sidecar** (see `blue_falsifier_s103.py`) — Q1 decision predicate / Q2 threshold-predicate / Q3' AND identity / 4 connection-points all closed.
- **central state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff** (sha256 prefix `c93e160a8a376a94` verified).
- **GOAL distance**: §15/§51/§72 milestones UNCHANGED, **GOAL 미도달**. §103 makes the integrated 2-axis fire-decision RESOLVABLE in closed form; it does NOT decide GOAL emergence.

The most honest finding: §11-A's measured "param-axis FLAT at 1B" is mute on anima's
true param-threshold because §11-A's data was sub-CDS; the arc has been simultaneously
sub-threshold on TWO axes but has only audited the result conditioned on ONE axis at a
time. §103's Sequential ordering (data-first, params-contingent) is the only ordering
that produces *attributable* axis-by-axis evidence; any Joint plan trades one bit of
joint information for ZERO bits of attributable information, which is a structural
loss that no cost ratio can compensate.
