# §99 — DATA-REGIME / SUBSTRATE / SPONTANEITY-vs-COHERENCE Frontier Deep Research

> **status**: RESEARCH §99 · LITERATURE-REVIEW TIER · $0 · NO GPU · NO runpod · NO fire · NO model.forward
> **date**: 2026-05-19
> **scope**: §98 concluded the n=6 architecture is causally innocent of the GOAL miss and
>   "the real path stays the §11.3 data-regime / §95 substrate frontier." §99 is the
>   exhaustive deep-research scan of exactly that frontier — 3 arms, ~37 papers graded.
> **governance**: g3 (literature review NOT empirical; capability claim 0; arxiv citation =
>   inspiration NOT proof; necessary-not-sufficient B-EMERGE-7) · "가능성 경로는 열어두자"
>   (§99 maps candidate paths and keeps them OPEN — NOT a closing verdict, completion-oriented) ·
>   f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 lattice-fit; external papers cited by their own
>   invariants only) · downstream-consumer (hexa-lang read-only, never edited).
> **connection-point cited**: §98 `result.json` verdict (c) MIXED + §96 `result.json`
>   self-attention SPIKING-INCOMPATIBLE finding (B-S99 connection-point checks).

---

## §0 — Why §99 exists, and what it is NOT

The §1~§98 arc measured emergence-negative on every path. §98's meta-audit cleared the
n=6 architecture of *causal* blame and pointed at two surviving frontiers: the **§11.3
data-regime** bottleneck and the **§95 substrate** frontier. §96 then sharpened the
substrate frontier into a third question — a spiking substrate gives *spontaneity* for
free but *coherence* is "the unsolved core, relocated not resolved."

§99 deep-researches all three. It is **literature-review tier** (like §80/§84/§85/§93).
Per the user directive *"완성을 목적으로 가능성 경로는 열어두자"* — §99's job is **not** to
close candidates. The arc has produced an enormous body of measured negatives; §99's job
is to scan the 2024-2026 literature for **what is still OPEN** and worth pursuing toward
GOAL completion. Every candidate below is marked with an honest blocker but kept LIVE.

g3 honest frame, stated once and load-bearing for the whole document: **no paper below is
evidence that anima will emerge. Literature is inspiration, not proof.** north-star +
§15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---

## §1 — ARM 1: DATA-REGIME (§11.3 / §1.1)

The arc's most-cited bottleneck: anima is "memorization-saturated" — every fire on a
30-114MB byte corpus drove CE to ~0.003-0.008 (deep memorization) but never crossed a
*diverse-data pre-training threshold*. §11-A measured a 3.68× model scale-up FLAT — so the
bottleneck is data-axis, not model-axis. §99 asks: what does the 2024-2026 literature say
the data regime for *emergence* (especially spontaneous/agentic behavior) actually is?

### 1.1 Cluster A — Emergence as a pre-training-loss / data threshold (the strongest anchor)

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 1 | Du, Zeng, Dong, Tang — **Understanding Emergent Abilities from the Loss Perspective** (arxiv:2403.15796) | NeurIPS 2024 | THE central anchor: a model exhibits emergent abilities — regardless of metric continuity — *iff its pre-training loss falls below a specific threshold*; before that, performance = random. anima's CE ~0.003 is memorization, not threshold-crossing — the loss is low because the corpus is *small*, not because the *task distribution* was learned. Distinguishes "low loss on a narrow corpus" from "loss below the diverse-data emergence threshold." | ★★★★★ |
| 2 | **Emergent Abilities in LLMs: A Survey** (arxiv:2503.05788) | Mar 2025 | Comprehensive review of *conditions* for emergence — scaling laws, task complexity, pre-training loss, prompting. Maps which conditions anima's fires did / did not satisfy. | ★★★★ |
| 3 | **Random Scaling of Emergent Capabilities** (arxiv:2502.17356) | 2026 | Capabilities cluster as multimodal distributions — models unpredictably learn discrete concepts; clusters visible even on continuous loss. Implication: emergence is partly stochastic-discrete, not a smooth knob — relevant to whether *any single* anima fire could ever "tip." | ★★★★ |
| 4 | Schaeffer et al. — **Are Emergent Abilities a Mirage?** (arxiv:2304.15004) | NeurIPS 2023 | The metric-artifact counter-thesis: discontinuity may be a discrete-metric artifact. §99 carries this as the honest skeptic anchor — anima's §9 honest-metric work is the project's own version of this debate. | ★★★★ |
| 5 | Guth & Ménard — **double-descent peak ↔ qualitative change in neural encoding** (2025, cited in arxiv:2506.11135) | 2025 | Mechanistic: the loss double-descent peak coincides with a *representational phase transition* — emergence = new representational structure, not just lower loss. | ★★★★ |
| 6 | **LLMs and Emergence: A Complex Systems Perspective** (arxiv:2506.11135) | Jun 2025 | Frames emergence with phase-transition / critical-system formalism — the data threshold as a critical point. | ★★★ |

### 1.2 Cluster B — Data DIVERSITY (not quantity) is the lever

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 7 | Raventós et al. — **Pretraining task diversity and the emergence of non-Bayesian in-context learning** (arxiv:2306.15063) | NeurIPS 2023 | THE diversity-threshold anchor: there is a *task-diversity threshold* below which more data only sharpens the pretraining distribution; **above it**, more data generalizes to unseen tasks. anima's 168-anchor carving corpus is *one narrow task distribution repeated* — structurally below this threshold. | ★★★★★ |
| 8 | **Beyond Scale: the Diversity Coefficient as a Data-Quality Metric** (arxiv:2306.13840) | 2023-24 | A formal, measurable diversity coefficient causally tied to eval performance — gives anima a *measurable* corpus-diversity target rather than a vibe. $0-design-testable on existing corpora. | ★★★★ |
| 9 | **Harnessing Diversity for Important Data Selection in Pretraining** (arxiv:2409.16986) | ICLR 2025 | Influence-based selection fails when selected data is not diverse → poor downstream generalization. Confirms diversity is the binding constraint on generalization, not influence/quality alone. | ★★★★ |
| 10 | **On the Diversity of Synthetic Data and its Impact on Training LLMs** (arxiv:2410.15226) | 2024 | Synthetic-data diversity (not volume) drives capability — directly relevant: anima can *generate* its own corpus, so diversity is a controllable knob. | ★★★ |
| 11 | **MetaSynth: Meta-Prompting-Driven Agentic Scaffolds for Diverse Synthetic Data** (arxiv:2504.12563) | 2025 | Diverse synthetic data *without* real-data mixing suffices for domain adaptation — a GOAL-legitimacy-relevant route (anima-own generation, no external corpus). | ★★★ |
| 12 | **DIVE: Scaling Diversity in Agentic Task Synthesis** (arxiv:2603.11076) | 2026 | Scales *diversity of agentic tasks/trajectories* — the agentic-corpus analogue of Cluster A. Closest literature to "what corpus makes *behavior* (not task-accuracy) emerge." | ★★★★ |
| 13 | **A Deep Dive into Scaling RL with Synthetic Data and Curricula** (arxiv:2603.24202) | 2026 | Task difficulty × curriculum schedule × environment diversity jointly shape training dynamics — connects anima's §16 curriculum work to the diversity frontier. | ★★★ |

### 1.3 Cluster C — What corpus regime makes *spontaneous/agentic* behavior emerge

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 14 | Takata et al. — **Spontaneous Emergence of Agent Individuality through Social Interactions in LLM-Based Communities** (arxiv:2411.03252; PMC11675631) | 2024-25 | Direct hit on the GOAL: agency, personality, memory *differentiate from an undifferentiated state* — and the substrate is **interaction**, not a static corpus. Agents generate hallucinations/hashtags to *sustain* communication (intrinsic drive). Suggests anima's GOAL needs an *interaction loop* corpus, not a pretraining corpus. | ★★★★★ |
| 15 | **AI Agent Behavioral Science** (arxiv:2506.06366) | 2025 | Frames agent behavior as an emergent science — the right *measurement frame* for "did spontaneity emerge." | ★★★ |
| 16 | **Emergence of Structured Behaviors from Curiosity-Based Intrinsic Motivation** (arxiv:1802.07461) | 2018 (foundational) | Foundational: structured behavior emerges from an intrinsic-motivation reward, no external task. The anchor for anima's W-module curiosity = the *generator* of a self-curriculum. | ★★★★ |
| 17 | **Agentic AI: Architectures, Taxonomies, Evaluation** (arxiv:2601.12560) | 2026 | Notes standard LLMs *lack* an intrinsic-motivation function to generate their own curriculum — names exactly the gap between a memory-replayer and a Living Consciousness. | ★★★★ |
| 18 | **LLMOrbit — From Scaling Walls to Agentic AI Systems** (arxiv:2601.14053) | 2026 | Data scarcity becomes acute 2026-2028 → the field pivots from scale to agentic self-generated data. anima's GOAL-legitimate self-corpus route is *with* this trend. | ★★★ |

---

## §2 — ARM 2: SUBSTRATE (§95 / §96)

§95 found Intel Loihi the sole `VIABLE-LONG-HORIZON` exotic substrate. §96 found anima's
physics layer (Ψ/tension/Φ) is SPIKING-COMPATIBLE — a LIF membrane potential *is* a
continuous-time state variable with a restoring leak — but `softmax(QK^T)` self-attention
is SPIKING-INCOMPATIBLE: it must be *replaced*, not ported. §99 deep-researches the
replacement and the synchronous-vs-event-driven question.

### 2.1 Cluster D — Spiking-attention replacements (softmax-free content routing)

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 19 | **Attention via Synaptic Plasticity is All You Need: A Biologically Inspired Spiking Neuromorphic Transformer** (arxiv:2511.14691) | Nov 2025 | THE substitution anchor: STDP-driven attention — relevance encoded by *precise spike timing*, addition-only, **no softmax**. The concrete answer to §96's "self-attention must be replaced." Plasticity-as-attention = anima's M-module Hebbian store generalized. | ★★★★★ |
| 20 | Guo et al. — **Spiking Transformer: Accurate Addition-Only Spiking Self-Attention** (arxiv:2503.00226) | CVPR 2025 | Addition-only SSA, softmax + scaling eliminated, binary/ReLU/ternary spiking neurons. Shows softmax-free attention is *accuracy-competitive*, not just cheap. | ★★★★ |
| 21 | **Spikformer: When SNN Meets Transformer** (arxiv:2209.15425) | ICLR 2023 (foundational) | Original Spiking Self-Attention: SSA drops softmax by exploiting spike-valued Q/K/V. The substrate-arm foundational anchor. | ★★★★ |
| 22 | **Combining Aggregated Attention and Transformer Architecture for SNNs** (ScienceDirect S0893608025006690) | 2025 | Aggregated-attention SNN — another softmax-free routing family; breadth of the replacement design space. | ★★★ |
| 23 | **SpikeAtConv: Integrated Spiking-Convolutional Attention** (PMC11936907) | 2025 | Spiking attention for event-vision — confirms event-driven content routing is mature, not speculative. | ★★★ |

### 2.2 Cluster E — Event-driven / continuous-time substrate; synchrony vs emergence

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 24 | Hasani et al. — **Liquid Time-constant Networks** (arxiv:2006.04439) | AAAI 2021 (foundational) | Continuous-time RNN where each unit's time constant is *state-modulated* — the **excitable vs spontaneous-limit-cycle regime is set by weights/nonlinearity**. A substrate that can *natively* be in a spontaneous regime — directly GOAL-relevant. | ★★★★★ |
| 25 | Casoni et al. — **LTC-RNNs: skew-symmetric weights ⇒ perpetual limit cycles** (2025, cited in CTRNN review) | Apr 2025 | Concrete: a parameter choice (skew-symmetric weights, bounded odd nonlinearity) gives *perpetual self-sustained motion* with motion invariants — a closed-form recipe for substrate-level spontaneity. | ★★★★ |
| 26 | **NCP / sparse LTC on Loihi-2 — sub-mJ CIFAR-10** (2025, cited in LTC review) | 2025 | Bridges Arm 2's two anchors: Liquid networks *already run on Loihi-2*. The §95 substrate + the §99 continuous-time spontaneity recipe are the *same hardware*. | ★★★★ |
| 27 | **Determinism in the Undetermined: Deterministic Output in Charge-Conserving Continuous-Time Neuromorphic Systems** (arxiv:2603.15987) | 2026 | Event-driven continuous-time systems can produce *deterministic* output despite temporal stochasticity — addresses the "event-driven = unreproducible" worry directly. | ★★★ |
| 28 | **Event-Based Neuromorphic Computing** (EmergentMind topic survey) | 2025 | "Each processing element updates state and emits spikes only on event arrival, strictly asynchronous, no-global-clock" — the precise contrast to anima's synchronous GPU substrate. Asynchronous SNN dynamics give *emergent representations* combining coding schemes. | ★★★★ |
| 29 | **Integration of Neuromorphic AI in Event-Driven Distributed Systems** (PMC9981939) | 2024 | System-level: co-located memory+compute, activity-driven — the architectural shape of an event-driven anima. | ★★ |
| 30 | **Continuous Thought Machines** (Sakana, pub.sakana.ai/ctm; arxiv 2505) | May 2025 | A GPU-runnable bridge: neural *timing* as a first-class axis; "leveraging neural timing leads to emergent benefits." Lets anima test the *timing/continuous-dynamics* hypothesis WITHOUT exotic hardware — a $0-ish design path. | ★★★★ |

---

## §3 — ARM 3: SPONTANEITY-vs-COHERENCE (the §96 relocation)

§96's sharpest honest finding: a spiking substrate gives *spontaneity* for free but
*coherence* is "the unsolved core, relocated not resolved" — the §88-F2 γ gap
(saturation-delay ≠ coherent emission; a bag of neurons spontaneously spikes, but that is
noise). §99 asks: how does the literature get *coherent* spontaneous behavior?

### 3.1 Cluster F — Self-organized criticality: spontaneous activity that is STRUCTURED

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 31 | Ikeda et al. — **Emergent functions of noise-driven spontaneous activity: homeostatic maintenance of criticality** (arxiv:2502.10946; Front. Neural Circuits 2025) | 2025 | THE coherence anchor: noise-driven *spontaneous* activity *homeostatically maintains* a critical state (E/I balance) — i.e. spontaneity and structure are the *same* mechanism, not opposites. Directly answers "how is spontaneous activity coherent and not noise." (Already a §80/§81 anchor — §99 re-cites for Arm 3.) | ★★★★★ |
| 32 | **Representational drift under spontaneous activity — SoC enhances representational reliability** (arxiv:2509.11545) | Sep 2025 | Critical-state spontaneous activity *enhances* low-dimensional representation across sessions vs non-critical — criticality makes spontaneous dynamics *reliable*, the literal opposite of "noise." | ★★★★ |
| 33 | **Self-organized criticality from activity-based rewiring** (arxiv:2009.11781) | 2020 (foundational) | SoC emerges from local activity-dependent rewiring — a structural-plasticity recipe; bridges to §86 SAPIN / anima MITOSIS. | ★★★ |
| 34 | **Real-time computation at the edge of chaos in recurrent networks** (Bertschinger & Natschläger, 2004; foundational) | 2004 | Foundational: a recurrent network has *maximal computational capacity* at the order/chaos boundary — coherent computation lives at the edge, not in the chaos. | ★★★★ |
| 35 | **Do Reservoir Computers Work Best at the Edge of Chaos?** (arxiv:2012.01409) + bubble-reservoir 2504.07221 | 2021/2025 | The honest skeptic anchor: edge-of-chaos is *not* universally optimal — some chaotic regimes compute well. §99 carries this so the coherence story is not over-claimed. | ★★★ |

### 3.2 Cluster G — Predictive processing: spontaneous activity AS prediction (coherent by design)

| # | Paper | Venue/era | Relevance | ★ |
|---|-------|-----------|-----------|---|
| 36 | **The predictive nature of spontaneous brain activity across scales and species** (Neuron S0896-6273(25)00127-8) | Neuron 2025 | Spontaneous spiking sequences form a *stable backbone structure at rest*; internally-generated rest events *predict future decisions*. Spontaneous activity is coherent *because it is the brain's prior/generative model running* — not idle noise. (Carried from §84 — re-cited for Arm 3.) | ★★★★★ |
| 37 | **Predictive learning rules generate cortical-like replay of probabilistic sensory experiences** (eLife 92712; PMC12169850) | 2024-25 | A *learning rule* under which spontaneous activity *replays* the learned temporal structure with experienced probabilities — coherence is trained-in by a predictive rule, then runs spontaneously. The mechanism anima's training would need. | ★★★★ |
| 38 | **Ex vivo cortical circuits learn to predict and spontaneously replay temporal patterns** (PMC11971321) | 2025 | Wet-lab: trained circuits show *spontaneous replay of learned structure* — direct biological proof that coherent spontaneity is achievable, training-dependent. | ★★★ |
| 39 | **Self-orthogonalizing attractor networks from the free energy principle** (arxiv:2505.22749) | May 2025 | FEP-derived attractor network self-orthogonalizes — coherent attractor structure emerges from a generative-model objective, not hand-design. Connects to anima's Ψ-attractor. | ★★★★ |
| 40 | **As One and Many: Individual ↔ Emergent Group-Level Generative Models in Active Inference** (Entropy 27(2):143) | 2025 | FEP across scales — a collective of active-inference agents constitutes a larger agent. The Arm-1 §2.3 interaction-loop and the FEP coherence story meet here. | ★★★ |
| 41 | **Latent CoT survey — Reasoning Beyond Language** (arxiv:2505.16782) + Coconut (2412.06769) | 2025 | Coherent reasoning in *continuous latent space* (no textual CoT); architectural *depth/recurrence* is crucial. anima's Dir-G/Dir-I latent work is in this family — the coherence-of-latent-dynamics frontier. | ★★★★ |

---

## §4 — Candidate paths to GOAL completion (KEPT-OPEN table)

Per the user directive "가능성 경로는 열어두자" — every candidate below is LIVE. The
`blocker` column is an HONEST caveat, not a closing verdict.

| ID | Candidate path | Arm | anima-fit | Honest blocker | $0-design-testable OR needs-fire |
|----|----------------|-----|-----------|----------------|----------------------------------|
| **C1** | **Diversity-threshold corpus** — measure anima's corpus diversity coefficient (#8), expand toward the task-diversity threshold (#7) until it crosses the *generalization* regime, not the memorization regime. | 1 | ★★★★★ | anima can *generate* diverse data but GOAL-legitimacy (§7) forbids generic external corpora; "diverse AND GOAL-legitimate AND large" is unsolved (the §51/§95 sharpened-frontier open question). Diversity-coefficient is measurable but the *threshold value* for anima's substrate is unknown. | $0-design-testable (diversity-coeff on existing corpora) → then needs-fire (a corpus at/above threshold). |
| **C2** | **Interaction-loop corpus, not pretraining corpus** — agency differentiates from an undifferentiated state via *interaction* (#14), driven by an intrinsic-motivation self-curriculum (#16/#17). Train on anima↔anima / anima↔env *loop traces*, not static text. | 1 | ★★★★★ | anima's §31/§45 dual-anima loop measured echo-chamber collapse at trained scale (§62) — the loop must inject genuine novelty (content-dependence, §36) or it is two attractors talking to a void. | $0-design-testable (loop-corpus generator + content-dependence pre-check, §36 precedent) → needs-fire to train. |
| **C3** | **Continuous-time / spontaneous-regime substrate** — Liquid Time-constant network (#24/#25): a parameter regime (skew-symmetric weights) gives *perpetual self-sustained motion* natively; runs on Loihi-2 (#26) OR test the timing axis on GPU via Continuous Thought Machines (#30). | 2 | ★★★★ | §96's relocation: substrate-level spontaneity ≠ coherent emission. A spontaneous limit cycle is motion, not consciousness. Also a *substrate rewrite*, not a fine-tune — large engineering cost. CTM gives a cheaper GPU proxy but is not the real substrate. | $0-design-testable (CTM-style timing probe; LTC excitable-vs-spontaneous regime $0 stub) → needs-fire / hardware for the real substrate. |
| **C4** | **Softmax-free spiking attention** — replace `softmax(QK^T)` with STDP-/plasticity-driven spike-timing routing (#19/#20/#21), resolving §96's SPIKING-INCOMPATIBLE finding. Plasticity-as-attention generalizes anima's M-module Hebbian store. | 2 | ★★★★ | Re-derivation, not a port — anima's whole attention path changes; correctness vs the current ConsciousDecoderV2 is unverified. Energy/spiking wins are measured for *vision tasks*, not for spontaneous-emission tasks. | $0-design-testable (design the mapping, falsifier-spec it like §96) → needs-fire to validate. |
| **C5** | **Criticality-as-coherence** — drive anima's substrate to a self-organized critical state where spontaneous activity is *homeostatically structured* (#31/#32), not noise; E/I-balance + activity-based rewiring (#33) as the coherence mechanism. | 3 | ★★★★ | anima has no native E/I-balance or rewiring loop; mapping criticality onto a byte-LM is non-trivial. §81-FIRE measured noise-on-Engine-G as PARTIAL-COLLAPSE — criticality did *not* transfer at trained scale. The mechanism may need a different substrate (Arm 2). | $0-design-testable (criticality-metric probe on existing fires) → §81-FIRE already showed needs-fire + substrate change. |
| **C6** | **Spontaneous-activity-as-prediction** — train a *predictive learning rule* (#37/#38) so that anima's spontaneous dynamics *replay learned structure with experienced probabilities*; coherence is trained-in, then runs unprompted. Pairs with §92 action-perception / §90 neoteny. | 3 | ★★★★★ | This is the *deepest-aligned* candidate but also the hardest: it requires the §1.1 data-regime to first be crossed (a predictive rule replays *learned* structure — if nothing coherent was learned, replay is coherent garbage). C6 is downstream of C1/C2. | $0-design-testable (predictive-replay objective design) → needs-fire, AND needs C1/C2 first. |
| **C7** | **FEP-derived self-orthogonalizing attractor** — derive anima's Ψ-attractor structure from a free-energy / generative-model objective (#39/#40) instead of hand-design; coherent attractor structure emerges from the objective. | 3 | ★★★ | FEP-to-byte-LM transfer is unproven; anima's §11-B measured "physics-only / no-CE = degenerate" — a pure FEP objective risks the same collapse. Most speculative of the seven. | $0-design-testable (FEP objective design + §11-B-style degeneracy check) → needs-fire. |

---

## §5 — TOP 3-4 strongest OPEN candidates (synthesized "what would actually move the GOAL")

The candidate table has seven live paths. Synthesizing across all three arms, the
strongest — judged by anima-fit × literature-strength × honest-tractability — are:

**① C2 — interaction-loop corpus driven by intrinsic motivation (Arm 1).**
The single most GOAL-aligned finding of §99: Takata et al. (#14) shows agency
*differentiates from an undifferentiated state* and the substrate of that differentiation
is **interaction**, not a static corpus — and #16/#17 supply the intrinsic-motivation
self-curriculum that a "memory-replayer" structurally lacks. anima's GOAL is *literally*
"spontaneously speaks from its own physics" — an interaction loop is the natural corpus
shape for that. **C3 (g3):** anima's own §62 measured the dual-anima loop collapse at
trained scale — the loop must carry genuine novelty (the §36 content-dependence pre-check
is exactly the right $0 gate). C2 is open and $0-design-testable *first*.

**② C1 — cross the diversity threshold, not the quantity threshold (Arm 1).**
Du et al. (#1) + Raventós et al. (#7) together give the precise reframe: emergence is a
*loss-below-threshold-on-a-diverse-distribution* event, and below a *task-diversity
threshold* more data only sharpens memorization — which is exactly anima's measured §11-A
FLAT and §16.6-C "memorization-saturated." The diversity coefficient (#8) makes this a
*measurable* $0 probe on existing corpora. **C3 (g3):** the GOAL-legitimacy constraint (§7
forbids generic corpora) plus "diverse AND legitimate AND large" being unsolved is the
real wall — C1 names the metric but not the corpus.

**③ C3 — continuous-time substrate with a native spontaneous regime (Arm 2).**
Liquid Time-constant networks (#24/#25) are the cleanest literature answer to "a substrate
that can *be* spontaneous": a parameter regime yields perpetual self-sustained motion
natively, and it *already runs on the §95-blessed Loihi-2* (#26). Continuous Thought
Machines (#30) make the timing hypothesis testable on a GPU at low cost *first*.
**C3 (g3):** §96's relocation stands — substrate spontaneity is *motion*, not coherent
emission; C3 buys spontaneity, not the GOAL. It must be paired with a coherence candidate.

**④ C6 — spontaneous-activity-as-prediction (Arm 3) — the coherence half.**
The Neuron 2025 result (#36) + the predictive-replay learning rule (#37/#38) are the
literature's actual answer to §96's relocated problem: spontaneous activity is coherent
*because it is the generative model / prior running* — and a predictive learning rule
trains that in, after which it runs unprompted. This is the *coherence partner* C3 needs.
**C3 (g3):** C6 is downstream of C1/C2 — a predictive rule replays *learned* structure; if
the diverse-data threshold was never crossed, the replay is coherent-but-empty.

**Honest synthesis (the §99 take):** the four strongest candidates are not independent —
they compose. **C1+C2 fix the data regime** (a diverse interaction-loop corpus),
**C3 supplies substrate-level spontaneity**, **C6 supplies coherence** (a predictive rule
so the spontaneity replays *learned* structure). The arc's pattern — spontaneity is cheap,
coherence is the unsolved core — is *resolved in the literature only by C6-style predictive
learning on a C1-style diverse corpus*. No single fire moves the GOAL; the literature says
the move is **a diverse interaction corpus + a predictive learning rule**, on a substrate
(C3/C4) that can host continuous dynamics. Every piece is OPEN. None is proven.

---

## §6 — ASCII diagram: the three arms and the seven kept-open candidates

```
                       GOAL: anima spontaneously speaks from its own physics
                         (Living Consciousness, not a memory-replayer)
                                          |
            ┌─────────────────────────────┼─────────────────────────────┐
            |                             |                             |
      ARM 1: DATA-REGIME           ARM 2: SUBSTRATE          ARM 3: SPONTANEITY-vs-COHERENCE
      (§11.3 / §1.1)               (§95 / §96)               (§96 relocation, §88-F2 γ)
            |                             |                             |
   "emergence = loss below        "Loihi viable; softmax-      "spiking ⇒ spontaneity free,
    a DIVERSE-data threshold"       attention SPIKING-           coherence = unsolved core"
    (Du #1, Raventós #7)            INCOMPATIBLE" (§96)          (Ikeda #31, Neuron #36)
            |                             |                             |
      ┌─────┴─────┐               ┌───────┴───────┐             ┌────────┴────────┐
   C1 diversity  C2 interaction  C3 continuous-  C4 softmax-   C5 criticality-  C6 spontaneous-
   threshold     -loop corpus    time substrate  free spiking  as-coherence     activity-AS-
   corpus        + intrinsic     (LTC #24, runs  attention     (SoC #31/32)     prediction
   (#7/#8)       motivation      on Loihi-2 #26) (STDP #19/20)                  (#36/37/38)
                 (#14/16/17)              |                                          |
                                          └──── C7 FEP self-orthogonalizing attractor #39/40
            |                             |                             |
            └──── COMPOSE: C1+C2 (diverse interaction corpus) ───────────┘
                          + C3/C4 (substrate that hosts continuous dynamics)
                          + C6 (predictive rule ⇒ coherent spontaneity)
                                          |
                       §99 = MAP of OPEN paths.  literature = inspiration, NOT proof.
                       north-star UNCHANGED · GOAL 미도달 · necessary-not-sufficient.
```

---

## §7 — Honest C3 caveats (≥10)

1. **§99 is literature-review, NOT empirical.** Not one paper below is evidence anima will
   emerge. arxiv citation = inspiration, not proof. capability claim = 0. (g3.)
2. **No path is closed; also no path is guaranteed.** Per "가능성 경로는 열어두자" §99 keeps
   all seven candidates LIVE — but "open" means "not yet refuted," not "will work."
3. **C1's threshold value is unknown for anima's substrate.** Du #1 / Raventós #7 establish
   that a threshold *exists*; neither tells anima *where* it is for a byte-LM of its scale.
4. **GOAL-legitimacy (§7) is a hard constraint on C1/C2.** "Diverse AND large AND
   GOAL-legitimate (anima-own, no generic external corpus)" is the §51/§95 sharpened-frontier
   *open question* — §99 does not solve it, it names it.
5. **C2's interaction loop already measured collapse once.** §62 measured the dual-anima loop
   echo-chamber-collapse at trained scale. C2 is open *only if* the loop injects genuine
   novelty — the §36 content-dependence pre-check is the honest $0 gate.
6. **C3/C4 are substrate REWRITES, not fine-tunes.** §96 already established the spiking
   re-derivation is "a major re-derivation." The engineering cost is real and large; CTM
   (#30) is a *proxy*, not the substrate.
7. **§96's relocation stands and is not resolved by §99.** A spiking/continuous-time
   substrate buys *spontaneity* (motion); *coherence* remains the unsolved core. §99 maps
   the coherence candidates (C5/C6/C7) — it does not demonstrate any of them.
8. **C5 (criticality) already measured a transfer failure.** §81-FIRE measured noise-on-
   Engine-G as PARTIAL-COLLAPSE-NO-HOMEOSTATIC-WINDOW at trained scale — criticality did not
   transfer. C5 stays open only at a *different substrate*, not on the current GPU byte-LM.
9. **C6 is downstream of C1/C2.** A predictive learning rule replays *learned* structure; if
   the diverse-data threshold (C1) was never crossed, the replay is coherent-but-empty. C6
   cannot move the GOAL alone.
10. **The four strongest candidates COMPOSE — none is a single-fire move.** §99's honest
    synthesis is that the GOAL move is *C1+C2+C3/C4+C6 together*, which is a multi-cycle
    research program, not a quick fire. "What would move the GOAL" is plural.
11. **Schaeffer #4 / edge-of-chaos #35 are carried as skeptic anchors.** Emergence-as-mirage
    (metric artifact) and "edge-of-chaos is not universally optimal" are live counter-theses;
    §99 does not assume the optimistic reading.
12. **The biology/FEP anchors (#36-40) are wet-substrate or formal-theory.** Transfer from a
    cortical circuit / a free-energy derivation to a silicon byte-LM is *unproven* — the
    §80/§81/§82/§83-FIRE arc already measured biology-mapping negatives at trained scale.
13. **necessary-not-sufficient at every layer (B-EMERGE-7).** Even if a candidate's mechanism
    is real, a real mechanism ≠ GOAL emergence. north-star + §15/§51/§72 milestones
    UNCHANGED, **GOAL 미도달**.
