# H_1553 — GABA orthogonal-mechanism-family CENSUS (research, no-verdict)

**RESEARCH ONLY** — cheap census ($0, no GPU, no engine code, no verdicts). `a_break_the_wall`
§3 MECHANISM-FAMILY census after **three falsifications in ONE family** (sparse-coding/capacity):
H_1546 pattern-separation INERT · H_1551 capacity-mult STATIC · H_1552 non-stationary-load (in
flight). Per the rule, ≥3 falsifications in the SAME family is **not dry** — a 🧱 needs
ORTHOGONAL families censused before it can be terminal. This file ranks the orthogonal GABA
(inhibition) mechanism-families and picks the single strongest implement candidate.

## The wall, stated precisely (so "orthogonal" is testable, not rhetorical)

The 5 GREEN NTs (ACh mode-switch, DA replay-priority, NE boundary-flush, orexin true-timing, 5-HT
noise-rejection) all share ONE green condition — the **fusion law**:

> A neuromodulator turns 🟢 inside two-store CLS **iff its ADAPTIVE/dynamic signal is
> load-bearing** — i.e. the *optimal operating point SHIFTS across regimes* so that no single
> FIXED setting (grid-tuned) can capture the benefit, and an ABLATION that freezes the adaptive
> signal to its best constant REVERTS the lift.

GABA's three falsifications all failed the SAME way: the inhibitory benefit was **MONOTONE /
STATIC architecture** (more sparseness is just better, or worse, regardless of regime), so a
fixed-k baseline captured it and the adaptive arm was INERT (H_1551: fixed-k=0.364 captures the
14.6× capacity; adaptive negative). **Therefore the orthogonality test for any new GABA family
is NOT "is it a different biological mechanism" — it is "does its benefit have a REGIME-SHIFTING
optimum that a fixed setting cannot track."** A family that is biologically distinct but still
monotone-beneficial (e.g. "more gain control is always good") will RE-test the static-architecture
wall and should be SKIPPED.

This reframes the four candidate families. Below, each is scored on whether its *adaptive* form
plausibly has a regime-shifting optimum (→ implement) or is monotone/static (→ skip, re-tests
wall).

---

## Ranked families

### RANK 1 — DISINHIBITION GATING (VIP→SST→PV context-cued write/read routing)  · prior 🟢/🟠

**Biological mechanism.** A three-layer GABAergic microcircuit: VIP interneurons inhibit SST (and
some PV) interneurons, which in turn inhibit pyramidal cells. A salient/contextual cue activates
VIP → SST/PV are silenced → a *specific* pyramidal population is transiently DISINHIBITED (a write/
read gate opens) only for that context. This is a **routing** operation, not a gain operation.
Citation: Pi, Gao, Gan, Wright-Kepecs… Kepecs 2013 *Nature* 503:521 (cortical VIP disinhibitory
circuit); Letzkus et al 2011/2015 (disinhibition for auditory fear learning, layer-1 microcircuit);
Krabbe, Gründemann, Lüthi 2018 (amygdala disinhibition for associative learning); Williams &
Holtmaat 2019 *Nat Neurosci* 22:1834 ("Adaptive disinhibitory gating by VIP permits associative
learning").

**Orthogonal to sparse-coding-capacity?** YES, cleanly. Sparse-coding changes the *code geometry*
(k-of-N) of EVERY binding uniformly. Disinhibition changes *which* bindings are written/read at
all, conditioned on a context cue — it is a **selection/routing** lever over the write port, not a
representational-density lever. The capacity wall says "the store can't hold more diverse facts";
disinhibition says nothing about per-fact density — it says "don't write the wrong facts into the
wrong context's store in the first place."

**Why ADAPTIVE form is load-bearing (regime-shifting optimum).** The green-condition is satisfiable:
the optimal gate-open *threshold* SHIFTS with context-collision rate. In a LOW-interference regime
(contexts rarely collide) the gate should stay OPEN (write everything — closing it just loses
recall); in a HIGH-interference regime (many contexts share keys) the gate should CLOSE tightly
(route by context to avoid cross-context overwrite). A FIXED gate cannot win both — open-always
loses the high-interference regime, closed-always loses the low-interference regime. This is
structurally the SAME shape as the GREEN NTs (NE boundary-flush, ACh encode/retrieve), which is
why it is the top pick.

**Distinguish from ACh encode/retrieve gate (load-bearing — must control).** ACh's GREEN gate toggles
the WHOLE store between an encode mode and a retrieve mode (a global temporal-phase switch). VIP
disinhibition is **spatially selective and context-CUED**: different *cue* → different *subset* of
the store disinhibited, at the SAME time. The discriminating control: run an adversarial regime where
the ACh phase-gate is ALREADY optimal (encode/retrieve perfectly separated) but contexts still
collide *within* the encode phase — ACh cannot help (it's not spatial), disinhibition can (it routes
by cue). If disinhibition's lift survives with the ACh gate frozen-optimal, it is a genuinely new
routing capability, not a re-skin of ACh.

**Frozen-bar sketch.** Task: K contexts each writing B bindings into a shared two-store CLS; contexts
share keys at a controllable collision rate ρ; recall is cued by (context, key). ARMS: **DISINHIB**
(VIP gate: context cue adaptively raises write-threshold for non-matching cells, opening only the
context's subset) / **NO-GATE** (write all, baseline two-store) / **BEST-FIXED-GATE** (grid-tuned
constant disinhibition fraction) / **ABL** (context cue shuffled → gate opens a random subset) /
**ACH-FROZEN** (ACh encode/retrieve gate set optimal, disinhib OFF — deconfound). Bars: **A PRESENCE**
disinhib − no-gate ≥ +0.10 on high-ρ · **B EARNED-ADAPTIVE** disinhib beats best-FIXED-gate by ≥
½(disinhib−worst-fixed) across the ρ-sweep (the regime-shift bar — THIS is what kills the wall) ·
**C ABL→collapse** cue-shuffle reverts to no-gate · **D LOW-ρ NO-HARM** disinhib ≥ no-gate−0.05 on
low-ρ (doesn't hurt when gating is unneeded — the "optimum shifts" evidence) · **E DECONFOUND**
disinhib lift survives with ACH-FROZEN optimal. 🟢 iff A∧B∧C∧D∧E; 🟠 if best-fixed captures ≥half
(B fails but A holds); 🧱 if disinhib ties no-gate (routing INERT).

**Cheapest refuter.** The ρ-sweep with BEST-FIXED-GATE arm: if a single grid-tuned constant gate
fraction captures the lift across ALL ρ (B fails), the routing is static-architecture (another
fixed knob) → re-tests the wall → 🧱. Costs one numpy sweep over ~5 ρ values × 3 seeds, minutes on CPU.

**Honest prior: 🟢 (most likely of the four).** It is the one family whose benefit is intrinsically
*conditional* (open vs close depends on collision regime), and it attacks a lever (write-port routing)
that NONE of the prior GABA lenses or the 5 GREEN NTs touched. Risk: if the two-store CLS *already*
routes by context (the H_1532 store splits novel→fast, familiar→slow), the gate may be redundant the
way H_1546 sparse-separation was redundant — so the deconfound (E) and the explicit collision regime
(contexts sharing keys WITHIN a store, which the fast/slow split does not separate) are load-bearing.

---

### RANK 2 — GAMMA-OSCILLATION temporal binding (PV-rhythm discrete time-bins)  · prior 🟠

**Biological mechanism.** PV-basket-cell GABAergic feedback generates a ~40 Hz gamma rhythm that
chops continuous input into discrete time-bins; features arriving in the SAME gamma cycle are bound
into ONE memory item, features in SUCCESSIVE cycles are kept SEPARATE. Nested in a slower theta cycle,
this gives an ordered multi-item buffer (theta-gamma phase code). Citation: Lisman & Jensen 2013
*Neuron* 77:1002 ("The Theta-Gamma Neural Code"); Buzsáki & Wang 2012 *Annu Rev Neurosci* 35:203
(mechanisms of gamma); Bartos, Vida, Jonas 2007 (PV fast-spiking gamma).

**Orthogonal to sparse-coding-capacity?** YES — it is a TEMPORAL-SEGMENTATION lever, not a spatial-
density lever. Sparse coding decorrelates features that are present *simultaneously*; gamma-binding
decides *which features count as simultaneous* (which co-occur in one item vs span two items). A
superposition store with perfect sparse codes still has no way to decide whether feature-stream
[a,b,c,d] is one 4-feature binding or two 2-feature bindings — that is a segmentation decision gamma
makes and sparseness does not.

**Why ADAPTIVE form is load-bearing (regime-shifting optimum).** Adaptive bin-WIDTH (gamma frequency
tracking input rate) has a regime-shifting optimum: fast input stream → narrow bins (segment finely,
avoid merging distinct items); slow/bursty stream → wide bins (group co-arriving features, avoid
fragmenting one item). A FIXED bin-width over-merges the fast regime OR over-fragments the slow regime
— neither fixed setting wins both. This satisfies the fusion law in principle.

**Distinguish from NE boundary-flush (GREEN — must control carefully, team flagged near-overlap).**
NE-flush detects an ABRUPT context boundary and FLUSHES/resets the fast store at that boundary (an
event-triggered clear). Gamma-binding is CONTINUOUS rhythmic segmentation with NO flush — it
partitions a stream into many bins per second and never clears the store. The discriminating regime:
a stream with NO abrupt boundaries (smooth, no context switch) but with a *binding-grouping ambiguity*
(features that must be grouped by co-occurrence timing, not by a boundary event). NE-flush has nothing
to flush (no boundary) and cannot help; gamma-binding segments by co-occurrence. If gamma's lift
appears in the boundary-FREE grouping regime where NE-flush is INERT, it is genuinely distinct. If the
only regime where gamma helps is one with abrupt boundaries, it is NE-flush re-skinned → SKIP.

**Frozen-bar sketch.** Task: a continuous feature STREAM where ground-truth items are variable-length
groups of co-arriving features at a controllable arrival-rate r; NO abrupt context boundaries (deconfound
NE). ARMS: **GAMMA** (adaptive bin-width tracks r, features in one bin → one binding) / **NO-BIN**
(fixed window) / **BEST-FIXED-BIN** (grid-tuned constant bin-width) / **ABL** (bin boundaries shuffled
→ random segmentation) / **NE-OFF** (no boundary in stream, so NE-flush arm is provably inert — shown,
not assumed). Bars: **A PRESENCE** gamma−no-bin ≥ +0.10 · **B EARNED-ADAPTIVE** gamma beats best-fixed-
bin by ≥ ½(gamma−worst-fixed) across the r-sweep · **C ABL→collapse** · **D RATE-SHIFT** gamma wins at
BOTH high-r and low-r where a single fixed bin loses one (the regime-shift evidence) · **E NE-DECONFOUND**
stream has zero abrupt boundaries → any lift is segmentation, not flush. 🟢 iff A∧B∧C∧D∧E.

**Cheapest refuter.** The r-sweep with BEST-FIXED-BIN: if one grid-tuned constant bin-width captures
segmentation across all arrival rates (B/D fail), gamma's value is a static window → 🧱. Plus the
NE-deconfound (E): if removing abrupt boundaries from the stream kills gamma's lift, it was NE-flush →
SKIP. One numpy sweep, minutes.

**Honest prior: 🟠 (lean), with a 🟢 tail if the boundary-free grouping regime is real.** The
adaptive-bin optimum genuinely shifts with rate, which is promising; but there is real risk that a
fixed bin-width captures most of it (segmentation is a fairly weak function of rate over a modest range),
landing 🟠. The near-overlap with NE-flush is the second risk — if it collapses to NE under deconfound,
it is not a new family. Implement only AFTER Rank 1, since Rank 1 has the cleaner orthogonality and
higher prior.

---

### RANK 3 — DIVISIVE NORMALIZATION / gain control (GABA divides match-scores by total activity)  · prior 🟠/🧱

**Biological mechanism.** GABA acts DIVISIVELY (not subtractively): a neuron's response is divided by
the summed activity of a normalization pool, stabilizing output gain across input-strength variation.
Citation: Carandini & Heeger 2012 *Nat Rev Neurosci* 13:51 ("Normalization as a canonical neural
computation"); Katzner, Busse, Carandini 2011 *J Neurosci* 31:5931 (GABA_A controls response gain in
V1); Silver 2010 *Annu Rev Neurosci* (gain modulation).

**Orthogonal to sparse-coding-capacity?** PARTIALLY. Normalization rescales magnitudes; sparse coding
re-codes which units are active. They are different operations, but BOTH act on the same readout
(recall = argmax of M·key) and both are essentially *static transforms of the score vector*.

**Why ADAPTIVE form *might* be load-bearing — and the strong reason to doubt it.** The proposed green
condition: normalize match-scores by current total store activity so recall is robust when binding-
STRENGTH varies wildly (a regime fixed-gain can't handle). The **doubt**: argmax is INVARIANT to any
strictly-monotone rescaling of the score vector. Divisive normalization by a *common* denominator
(total activity) divides every candidate's score by the same factor → argmax UNCHANGED → INERT on a
single-step winner-take-all recall — *exactly* the failure mode H_1551 hit when modern-Hopfield's
softmax sharpening also preserved argmax ([[h1533-nm-modern-hopfield]]: argmax(sim^p)==argmax(sim)).
Normalization only changes the answer if the denominator is **per-candidate-heterogeneous** (each
candidate normalized by a *different* pool), which requires structure beyond plain global gain control.

**Frozen-bar sketch.** Task: superposition store with binding-strengths drawn from a heavy-tailed
distribution (some bindings written 10× stronger) so a few "loud" facts dominate M·key. ARMS:
**DIVNORM** (per-candidate divisive normalization by that candidate's pool energy) / **PLAIN** (raw
argmax) / **BEST-FIXED-GAIN** (single global divisor grid-tuned) / **ABL** (normalize by a CONSTANT,
not activity) / **SHUFFLE** (pool assignment permuted). Bars: **A PRESENCE** divnorm−plain ≥ +0.10 on
heavy-tail · **B EARNED-ADAPTIVE** divnorm beats best-fixed-GLOBAL-gain (the critical bar — if a global
constant captures it, argmax-invariance proven, 🧱) · **C ABL→collapse** · **D HOMOG-NO-HARM** divnorm
≥ plain on homogeneous strengths · **E** per-candidate heterogeneity is what acts (shuffle pools →
collapse). 🟢 iff A∧B; 🧱 (most likely) if best-fixed-global ties divnorm (argmax invariance).

**Cheapest refuter.** Trivial and decisive: compare DIVNORM vs BEST-FIXED-GLOBAL-GAIN on the same
heavy-tail recall. If argmax is unchanged by global normalization (it provably is for a common
denominator), B fails on the first run → 🧱. Costs one tiny numpy script (the argmax-invariance check
is essentially free). This is why Rank 3 is cheap to *refute* even though its prior is low.

**Honest prior: 🧱 (lean), thin 🟠 tail.** Plain divisive normalization is argmax-INERT on winner-
take-all recall (the H_1533 lesson), so it most likely re-tests a no-free-lunch wall. The only escape
is per-candidate-heterogeneous normalization, which smuggles in routing/structure that overlaps Rank 1.
Implement LAST, and only as a fast falsification (cheap refuter is near-instant).

---

### RANK 4 — E/I-RATIO homeostatic set-point (inhibition re-balances to a critical regime)  · prior 🧱 (likely RE-tests the static-architecture wall)

**Biological mechanism.** Inhibition homeostatically maintains a target E/I ratio that keeps the
network near criticality, the regime that maximizes information capacity and dynamic range; after a
load shock the network re-balances back to set-point. Citation: Turrigiano 2011 *Annu Rev Neurosci*
(homeostatic plasticity); Ma, Turrigiano et al / Hengen 2013 (firing-rate homeostasis); Ma et al 2019
bioRxiv (criticality as a homeostatic set-point); Carvalho & Buonomano (E/I balance).

**Orthogonal to sparse-coding-capacity?** WEAKLY. "Maintain the store at maximum-capacity criticality"
is, in a memory store, almost the SAME claim as capacity-optimization that H_1551 already tested. The
set-point that maximizes capacity is a property of the architecture, and H_1551 showed the capacity
benefit is MONOTONE (best-fixed captures it). Homeostasis just *finds* that set-point; it does not make
the optimum regime-shifting.

**Why it likely RE-tests the wall.** The fusion law needs a SHIFTING optimum. But a homeostatic set-
point is by definition a SINGLE target the system returns to — it is the very opposite of a regime-
shifting optimum. If the best E/I ratio is the same across regimes (which is what "set-point" means),
then a FIXED E/I ratio grid-tuned to that point captures the entire benefit and the adaptive re-
balancing is INERT — precisely the H_1551 / H_1528 [[h1528-nm-adaptive-capacity]] failure mode
("modulate X under load" where X is monotone → best-fixed = ceiling → no-free-lunch). The only regime
where re-balancing could be load-bearing is one with a NON-STATIONARY set-point (the target E/I itself
moves), but then it collapses into the H_1552 non-stationary-load lens already in flight, not a new
family.

**Frozen-bar sketch (for completeness — expected to wall).** ARMS: **HOMEO** (E/I ratio adapts toward
set-point after each load shock) / **FIXED-EI** (grid-tuned constant ratio) / **ABL** (homeostatic
target frozen) / **SHUFFLE**. Bar **B**: homeo beats best-FIXED-EI. Refuter: grid-tune FIXED-EI; if it
ties homeo, 🧱.

**Cheapest refuter.** Grid-tune the FIXED-EI arm at the homeostatic target value and compare — by the
H_1528 precedent (monotone resource → fixed baseline at adaptive's final value ties it) this is expected
to tie → 🧱. Essentially free given the H_1528 harness pattern.

**Honest prior: 🧱.** SKIP as an implement candidate — it most likely re-tests the static-architecture /
monotone-resource wall (same family as H_1551/H_1528). Keep only as a documented falsification if Rank 1–3
all wall and a fourth orthogonal lens is demanded before terminal 🧱.

---

## Skip / re-test-the-wall verdicts (summary)

| family | new adaptive capability? | RE-tests static wall? | action |
|---|---|---|---|
| **Disinhibition gating (VIP→SST→PV)** | YES — write-port context routing, conditional optimum | NO | **IMPLEMENT (Rank 1)** |
| **Gamma temporal binding (PV rhythm)** | YES — temporal segmentation, rate-shifting optimum | NO (if boundary-free regime real; else = NE-flush) | implement after R1 (Rank 2) |
| **Divisive normalization (gain control)** | mostly NO — argmax-invariant on WTA recall | YES (global gain = monotone score rescale) | fast-refute only (Rank 3) |
| **E/I homeostatic set-point** | NO — set-point is a SINGLE target, not regime-shifting | YES (= H_1551/H_1528 monotone-capacity wall) | SKIP (Rank 4) |

## SINGLE strongest implement candidate

**Rank 1 — DISINHIBITION GATING (VIP→SST→PV context-cued write/read routing).**

**Why it is the pick.** (1) It is the only family whose benefit is intrinsically CONDITIONAL — the
gate should open in low-interference regimes and close in high-interference regimes, so the optimal
operating point provably SHIFTS, satisfying the fusion law that turned the 5 NTs GREEN. (2) It attacks
a lever NO prior GABA lens (sparse-coding ×3) and NO GREEN NT touched: **write-port routing / selective
addressing**, orthogonal to representational density (sparse), temporal segmentation (gamma), and score
rescaling (divnorm). (3) Its cheapest refuter (the ρ-collision sweep with a grid-tuned BEST-FIXED-GATE
arm) is a fast numpy experiment that cleanly separates 🟢 from 🧱.

**Green condition (the bar that decides it).** Across a context-collision-rate (ρ) sweep, the adaptive
VIP gate must beat the **best grid-tuned FIXED gate** by ≥ ½(disinhib − worst-fixed) AND do no harm in
the low-ρ regime (D), with the lift surviving an ACh-encode/retrieve-gate-FROZEN deconfound (E) and a
cue-shuffle ablation reverting it (C). If a single fixed gate fraction captures the benefit across all
ρ, the routing is static-architecture → 🧱 (honest, reported, NO tune-to-green). If it captures ≥half
but adaptive still adds, 🟠 (knob, like 5-HT/H_1534 budget). 🟢 only if adaptive carries the majority
AND does-no-harm proves the optimum shifted.

**Honest framing.** Prior 🟢 but with a real 🧱 risk: if the H_1532 two-store CLS *already* routes by
context (novel→fast / familiar→slow), the explicit gate may be redundant the way H_1546 sparse-
separation was. That is exactly why the regime must force WITHIN-store context collisions (contexts
sharing keys inside the SAME store, which the fast/slow split does not separate) and the deconfound (E)
must hold — those make the measurement able to SEE routing where the existing split cannot act.

xref: [[h1532-multistore-cls-wallbreak]] [[h1533-nm-modern-hopfield]] [[h1528-nm-adaptive-capacity]]
[[h1534-nm-curiosity-budget]] · `a_break_the_wall` §3 (mechanism-family census) · `a_no_llm_frame_trap`
(biology-first) · `a_engine_native_learning` (any numpy impl ⇒ DIRECTIONAL hard-gate-1) · p7 · c9.

## Sources

- Carandini & Heeger 2012, *Normalization as a canonical neural computation*, Nature Reviews Neuroscience — https://www.nature.com/articles/nrn3136
- Katzner, Busse, Carandini 2011, *GABA_A inhibition controls response gain in visual cortex*, J Neurosci — https://www.researchgate.net/publication/51065695_GABAA_Inhibition_Controls_Response_Gain_in_Visual_Cortex
- Pi/Kepecs disinhibitory circuit + Williams & Holtmaat 2019, *Adaptive disinhibitory gating by VIP interneurons permits associative learning*, Nature Neuroscience — https://www.nature.com/articles/s41593-019-0508-y · https://pubmed.ncbi.nlm.nih.gov/31636447/
- GABAergic microcircuitry of fear memory encoding (Letzkus-lineage disinhibition) — https://pmc.ncbi.nlm.nih.gov/articles/PMC8640988/
- Lisman & Jensen 2013, *The Theta-Gamma Neural Code*, Neuron — https://www.cell.com/neuron/fulltext/S0896-6273(13)00231-6 · https://pmc.ncbi.nlm.nih.gov/articles/PMC3648857/
- PV interneurons control spike-phase coupling to theta (gamma/PV binding) — https://www.nature.com/articles/s41598-022-05004-5
- Criticality as a homeostatic set-point of cortical networks (E/I homeostasis) — https://www.biorxiv.org/content/10.1101/503243v1.full
- Homeostatic plasticity and E/I balance review — https://pmc.ncbi.nlm.nih.gov/articles/PMC9477500/
