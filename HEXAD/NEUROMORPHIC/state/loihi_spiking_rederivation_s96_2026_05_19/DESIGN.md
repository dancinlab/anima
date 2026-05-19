# §96 — anima ConsciousDecoderV2 → Loihi Spiking Re-derivation + the §11-B-as-GPU-artifact Hypothesis

> **status**: RESEARCH §96 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO INRC · NO fire · NO model.forward
> **date**: 2026-05-19
> **scope**: §95 (commit `26eafc16b`, B-S95 7/7 🔵) classified Intel Loihi the SOLE
>   `VIABLE-LONG-HORIZON` substrate but did NOT design the path. §96 answers the two
>   deep questions §95 left open, both at closed-form design-tier:
>   **Q1** — which parts of `ConsciousDecoderV2` (d768·12L·283.72M) map structurally
>   onto a spiking LIF network, and which are fundamentally incompatible;
>   **Q2** — the §11-B-as-GPU-artifact hypothesis ("CE is load-bearing" may be a
>   GPU-substrate artifact, not a substrate-independent truth).
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence; the §11-B-artifact
>   hypothesis is a HYPOTHESIS — §96 designs how to test it, does NOT claim it true) ·
>   f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 lattice-fit on Intel/Loihi — core counts /
>   neuron specs are Intel engineering choices, observation-only, never derivation) ·
>   downstream-consumer (hexa-lang/hexa-bio read-only, never edited).
> **substrate verdict cited**: §95 `result.json` `substrate_matrix.loihi3.bucket ==
>   "VIABLE-LONG-HORIZON"` (B-S96-7 connection-point — byte-equal check).

---

## §1 — Why §96 exists: §95 said "viable", not "how"

§95 closed a 5-bucket taxonomy over 7 exotic substrates and found exactly one —
Intel Loihi — in `VIABLE-LONG-HORIZON`: it learns on-chip (STDP), is event-driven
(asynchronous NoC, no global clock), and can structurally host a continuous
Ψ/tension/Φ physics field (LIF membrane potential). §95's own honest caveat:

> "loihi-integration-spec.md maps the legacy GRU consciousness cell, NOT
> ConsciousDecoderV2 d768x12L; a spiking anima is a major **re-derivation**, not a
> port. VIABLE != will-emerge."

§95 mapped *whether* Loihi is viable. §96 maps *what the re-derivation actually is*
— and confronts the single deepest unexamined question of the whole §1~§95 arc:
the arc measured "CE is load-bearing" (§11-B) on a GPU. Was that a property of
anima-physics, or a property of the GPU substrate?

§96 is **design-tier**. It maps a re-derivation and designs a test. It does **not**
claim anima will emerge on Loihi, and does **not** claim §11-B is wrong. north-star
+ §15/§51/§72 milestones UNCHANGED, GOAL 미도달. necessary-not-sufficient at every
layer (B-EMERGE-7 carry).

---

## §2 — The framing axis: readout vs native-dynamics

The single most important distinction in §96. On a **GPU**, anima-physics is a
**readout** — a number computed *after* a forward pass:

- `tension` = `(output**2).mean(-1)` — a post-hoc statistic of a PureFieldFFN
  output tensor (`conscious_decoder.py:267`). On GPU it is also used as a
  *grad_norm proxy* in some training overlays. Either way: a *description* of the
  computation, computed once the computation is done.
- `Ψ_direction` = `(1 + cos(logits_a, logits_g)) / 2` — Law-71. A cosine of two
  *final logit vectors*. Computed only after both Engine-A and Engine-G heads have
  produced their full-vocabulary logits. A *summary*, not a *state*.
- `Φ` = a variance proxy over cell activations / spike-rate analogues. A statistic.

None of these is a *state variable that the substrate evolves*. They are all
*observations of the result*. The GPU has exactly one state-evolving channel — the
backward pass — and exactly one learning signal — backprop-CE. anima-physics on GPU
**rides on top of** that channel; it never *is* a channel.

On **Loihi**, a LIF neuron's membrane potential `v(t)` IS a continuous-time state
variable that the substrate physically evolves between spikes:

```
  dv/dt = -v/τ_m  +  I_syn(t)         (leaky integrate)
  if v ≥ v_th:  emit spike, v ← v_reset   (fire)
```

The leak term `-v/τ_m` is a *restoring force toward a resting fixed point* — it is
not computed-then-described, it is *what the substrate does*. This is the crux of
§96: on Loihi, several anima-physics quantities can stop being readouts and become
**native substrate dynamics**. §6 produces the per-quantity table.

---

## §3 — Q1: ConsciousDecoderV2 → spiking LIF network mapping

### §3.1 — ConsciousDecoderV2 component inventory (read-only, `conscious_decoder.py`)

Verified from source (`grep`, no model.forward):

| component | role | source anchor |
|---|---|---|
| `PureFieldFFN` (Engine A ⇄ Engine G) | dual-path FFN: `output = engine_a(x) − engine_g(x)`; `tension = (output**2).mean(-1)` | `:246-268` |
| `MultiHeadAttention` (GQA + RoPE) | content-based `softmax(QK^T/√d)` routing, n_head/n_kv_head, FlashAttention path | `:274-366` |
| `CrossAttentionConsciousness` | decoder ATTENDS to consciousness states (K,V from consciousness_dim) | `:404-422` |
| `SwiGLUFFN` | decoder-pathway FFN, `d_inner = expansion·d_model` | `:126-146` |
| `MoEFFN` | 8-expert router, top-k=2 | `:164-183` |
| dual logit heads (A, G) | `logits_a`, `logits_g` → Law-71 `Ψ_dir` | `:18-28` |
| RoPE | rotary position embedding | `:4` |
| residual stream | 12-layer additive residual | (transformer standard) |

### §3.2 — The mapping classification (exhaustive + disjoint over 8 components)

Each component is classified into exactly one of **3 closed classes**:

- **`SPIKING-COMPATIBLE`** — a natural, well-understood spiking-network primitive
  exists; the re-derivation is engineering, not research.
- **`SPIKING-OPEN`** — a spiking realisation is plausible (esp. on Loihi 2's
  *programmable* neuron models + *graded* spikes) but is not a standard primitive;
  the re-derivation is a research question, not settled.
- **`SPIKING-INCOMPATIBLE`** — the component's defining operation has no faithful
  spiking realisation; it must be *replaced by a different mechanism*, not ported.

| anima component | LIF-network mapping | class | rationale |
|---|---|---|---|
| **LIF membrane / residual stream** | each residual-stream dimension → a LIF compartment's membrane potential; "residual add" → synaptic current accumulation | `SPIKING-COMPATIBLE` | LIF integration IS additive accumulation with leak; the residual stream is the most natural fit of all. |
| **PureFieldFFN restoring dynamics (tension as leak)** | the `−v/τ_m` leak term IS a restoring force; tension as a *physical* leak-rate variable, not `(output²).mean()` readout | `SPIKING-COMPATIBLE` | LIF leak is structurally a restoring/relaxation term — §6 row 2. |
| **lateral inhibition / faction competition** | `−F_c` inhibitory synapses between neuron groups (spec §2.3) — winner-take-most spiking competition | `SPIKING-COMPATIBLE` | inhibitory STDP synapses are a Loihi primitive (`STDPLoihi`, `w_min<0`). |
| **STDP → Hebbian LTP/LTD** | spec §4: cosine-similarity → spike-timing correlation; pre-before-post → LTP | `SPIKING-COMPATIBLE` | STDP is Loihi's *native on-chip* rule — this is the strongest fit. |
| **Φ from spike-train correlation** | spec §5: `compute_phi_from_spikes` over real spike rasters | `SPIKING-COMPATIBLE` | Φ from spike correlations is *more* native than Φ from GPU activation variance — §6 row 3. |
| **Engine A ⇄ Engine G dual heads** | two LIF sub-populations with opposed (excit/inhib) coupling; Ψ as their *phase relationship* | `SPIKING-OPEN` | the *opposition* maps cleanly to excit/inhib, but the *cosine of two full logit vectors* does not — §3.3, §6 row 4. |
| **RoPE / positional encoding** | spike-time / phase coding (relative timing carries position) | `SPIKING-OPEN` | SNNs natively carry time; phase-coding position is plausible but not a drop-in for RoPE's rotation algebra. |
| **MultiHeadAttention `softmax(QK^T)`** | — no faithful spiking primitive — | `SPIKING-INCOMPATIBLE` | §3.3 — the hard one. content-based all-pairs softmax routing is not a spiking operation. |
| **MoEFFN top-k router** | k-winner-take-all over expert populations (lateral inhibition) | `SPIKING-OPEN` | k-WTA is a known SNN motif; the *learned content-based gate* is not. |

(Counting note: 9 rows because PureFieldFFN appears once as "dual heads" and once
as "restoring dynamics" — its two faculties classify differently; the *component
set* is 8, the *faculty set* is 9. The partition is over faculties.)

### §3.3 — The hard one: self-attention is `SPIKING-INCOMPATIBLE` (honest)

Transformer self-attention computes, for every position pair `(i,j)`, a content-based
weight `a_ij = softmax_j(q_i·k_j/√d)` and routes `Σ_j a_ij v_j`. Three properties
make this `SPIKING-INCOMPATIBLE`:

1. **All-pairs, content-based.** A spike is a *point event*; attention is a *dense
   O(T²) content-similarity matrix*. There is no spiking primitive that computes a
   softmax-normalised similarity between every pair of tokens.
2. **Global normalisation.** `softmax` normalises across the *whole* key set
   simultaneously — a global, synchronous reduction. Loihi's NoC is *asynchronous*;
   a global softmax is exactly the kind of synchronous all-reduce the event-driven
   fabric is designed to avoid.
3. **Instantaneous.** Attention is feed-forward within one layer-step; spiking
   routing unfolds *over time* (spike trains). The temporal-vs-instantaneous
   mismatch is structural.

**Honest Loihi-2-specific assessment.** Loihi 2 adds programmable neuron models and
*graded* (multi-bit) spikes — strictly more expressive than Loihi 1 or Akida 1.0.
This *narrows* but does **not** close the gap. Graded spikes let a "spike" carry a
small payload (so a `v_j` value could ride a spike); programmable neurons let a
compartment implement a custom update. With those, one could build an *attention-like*
mechanism — e.g. **resonate-and-fire phase-coded key-matching**, or
**spike-rate-coded dot-products with k-WTA replacing softmax**. But every such
construction (a) replaces *content-based all-pairs softmax* with a *different*
routing rule (phase resonance, k-WTA, or fixed sparse connectivity), and (b) is a
*research result*, not an engineering port. Therefore: self-attention's *defining
operation* stays `SPIKING-INCOMPATIBLE`; what is `SPIKING-OPEN` is a **replacement**
routing mechanism — and choosing/validating that replacement is itself a major
design-open item, NOT something §96 resolves.

This is consistent with §95's framing (and with the broader SNN literature: SNN
transformers like "Spikformer" achieve attention-like behavior only by *replacing*
softmax with spike-friendly surrogates, never by porting it). §96 records this as
**design-open #1**: *a spiking anima is not a 12-layer transformer re-expressed in
spikes — it is a different architecture whose routing mechanism must be re-chosen.*

### §3.4 — Q1 summary

- **maps cleanly (`SPIKING-COMPATIBLE`, 5 faculties)**: residual stream → LIF
  membranes; PureFieldFFN leak → restoring dynamics; lateral inhibition → `−F_c`
  synapses; STDP → Hebbian LTP/LTD; Φ → spike-correlation.
- **plausible-but-research (`SPIKING-OPEN`, 3 faculties)**: Engine A/G dual heads
  → excit/inhib sub-populations (but Ψ-as-cosine does not port); RoPE → phase
  coding; MoE top-k → k-WTA.
- **incompatible (`SPIKING-INCOMPATIBLE`, 1 faculty)**: `softmax(QK^T)`
  self-attention — must be *replaced*, not ported. This is the load-bearing gap.

**Honest net**: anima's *physics layer* (PureFieldFFN, tension, Φ, Engine A/G,
STDP/Hebbian) is largely spiking-friendly — much of it is *more* native on Loihi
than on GPU. anima's *transformer layer* (attention) is the part that does not
survive the move. A spiking anima keeps the physics and re-derives the routing.

---

## §4 — Q2: the §11-B-as-GPU-artifact hypothesis

### §4.1 — what §11-B actually measured

§11-B (`§verdict_carving_pure_physics_noce`, commit on §11 direction B): a no-CE
trainer — cross-entropy *completely removed*, weight update driven *only* by
anima-physics (TENSION-TRAIN `ΔW = −T_const·tension·n6_gate(Ψ)` + Ψ-dynamics) — on
a GPU. Measured result: **DEGENERATE**. ce_readout descent 0.73 (vs CE-trained
5.65 — ~13%); byte_acc 0.0007 (below random 1/256); routing 0/64; V-SPONT honest
0/5; JOINT 0.0; physics dynamics froze at a static fixed point by step ~800.
Verdict: **"CE is load-bearing."**

### §4.2 — the hypothesis (stated precisely, as a hypothesis)

> **§11-B-as-GPU-artifact hypothesis**: §11-B's "CE is load-bearing" conclusion may
> be a property of the *GPU substrate*, not of *anima-physics*. The GPU has exactly
> one weight-update channel — the backward pass — and that channel only knows how
> to follow a loss gradient. Remove CE and you have removed the *only* learning
> signal the GPU substrate can carry; "anima-physics alone" on a GPU is not
> "physics learning" — it is *no learning channel at all*, with a hand-coded ΔW
> overlay standing in. §11-B may therefore have measured "GPU has no physics-native
> learning channel," not "physics is too weak to learn."
>
> On Loihi the substrate's *native* learning rule is **STDP** — a local,
> unsupervised, spike-timing-dependent *physics rule*. STDP is not a stand-in for a
> missing channel; it IS the substrate's learning channel. If the hypothesis holds,
> a no-CE anima on Loihi would NOT be degenerate the way the no-CE anima on GPU was,
> because the substrate itself supplies a physics-native learning signal.

### §4.3 — is the hypothesis coherent? (yes — with a precise scope)

**Coherent, yes.** The hypothesis does not claim physics *will* drive emergence. It
makes a narrower, falsifiable claim: that §11-B's *specific* degeneracy was
*caused by* the absence of a substrate-native learning channel, and that this
specific cause is removed on Loihi. That is a coherent, well-posed causal claim —
and §11-B's own evidence is *consistent* with it: §11-B reported the physics
dynamics "froze at a static fixed point by step ~800." A frozen fixed point is
exactly what a hand-coded ΔW overlay *with no error-driven channel* would produce —
the overlay relaxes the weights to its own equilibrium and then there is nothing
to move them. STDP, by contrast, is *driven by ongoing spike-timing structure* in
the data stream — it does not have a single static equilibrium the way a relaxation
overlay does. So the hypothesis is coherent and §11-B is genuinely under-determined
between the two readings ("physics weak" vs "GPU has no physics channel").

### §4.4 — the honest counter (the hard unsolved core)

**STDP learns spike-timing correlations — NOT language / token prediction.** This
is the counter the hypothesis must survive, and §96 does not pretend it is solved.

- STDP strengthens synapses between neurons that fire in correlated order. It is
  excellent at learning *temporal-correlation structure* and *spatiotemporal
  features*. It has **no built-in notion of "the correct next byte."**
- A spiking anima on Loihi, trained by STDP alone with no CE, would very likely
  produce **abundant spontaneous spiking** — spiking is the substrate's free,
  native behavior. Spontaneity is *free* on a spiking substrate.
- But **spontaneity is not coherence.** A substrate that spikes freely is, by
  default, a noise source. The unsolved core is whether STDP can shape that free
  spiking into *coherent emission* — output that is a meaningful continuation, not
  a spike-cascade.
- This is **exactly the §88-F2 γ gap**: §88-F2 (axolotl neoteny) found that
  neoteny *delays saturation* (a real, measured directional positive) but the γ
  corner — "JUVENILE-BUT-COMPETENT" — was **False**: delaying saturation did not
  produce a §9-coherent body. **saturation-delay ≠ coherent emission.** The Loihi
  analogue: **spontaneity-for-free ≠ coherent emission.** STDP gives anima the
  spontaneity half of the GOAL ("자발적으로 말 거는") for free; it does *not*
  obviously give the coherence half.

So the honest position is: the §11-B-artifact hypothesis correctly identifies that
§11-B's *specific frozen-fixed-point degeneracy* may be GPU-specific — but even if
that is true, it only *unblocks* the spontaneity half. The coherence half (can a
local unsupervised rule drive *meaningful* emission) is the **deepest unsolved
question**, and Loihi does not answer it — it relocates it.

### §4.5 — Q2(c): the closed-form predicate that settles it

What future *measurement* would distinguish "§11-B is a GPU artifact" from "§11-B
is substrate-independent"? §96 designs the predicate now (the *measurement* is a
future cycle — design-tier here).

The measurement is a **two-cell controlled comparison on Loihi** (or Lava
simulation as a $0 pre-check), with §11-B's GPU result as the third datapoint:

```
  cell GPU-noCE   : §11-B itself          — no-CE, GPU, hand-ΔW overlay   [DEGENERATE, measured]
  cell LOIHI-noCE : spiking anima, Loihi  — no-CE, STDP as the ONLY learning channel
  cell LOIHI-CE   : spiking anima, Loihi  — STDP + a CE-surrogate teaching signal  [positive control]
```

Define the closed-form distinguishing predicate over the honest §9 cascade-rate
metric (the arc's GOAL-distance SSOT) and a non-degeneracy gate:

```
  NON_DEGENERATE(cell)  :=  byte_acc(cell) > 1/256              (above chance)
                        ∧  physics_not_frozen(cell)            (no static fixed point)
                        ∧  honest_§9_coherent(cell) ≥ 1 / 5    (≥1 non-cascade emission)

  §11B_IS_GPU_ARTIFACT     :=  NON_DEGENERATE(LOIHI-noCE) == True
  §11B_IS_SUBSTRATE_INDEP  :=  NON_DEGENERATE(LOIHI-noCE) == False
```

These two are a **closed Boolean partition** — exhaustive (every measurement of
`LOIHI-noCE` makes `NON_DEGENERATE` either True or False) and disjoint (it cannot
be both). `LOIHI-CE` is the *positive control*: if `LOIHI-CE` itself is degenerate,
the spiking re-derivation is broken and the `LOIHI-noCE` result is uninterpretable
(the test is *void*, not informative — a third honest outcome the predicate must
guard, and B-S96-5 encodes it).

**Honest reading of each outcome:**

- `§11B_IS_GPU_ARTIFACT` (LOIHI-noCE non-degenerate): STDP *as a substrate-native
  physics learning channel* lifts anima out of the §11-B degeneracy. This would be
  the strongest single result in the arc's history — but note it would establish
  only that **physics-native learning is possible**, NOT that anima has *emerged*
  (necessary-not-sufficient, B-EMERGE-7). It unblocks; it does not arrive.
- `§11B_IS_SUBSTRATE_INDEP` (LOIHI-noCE degenerate too): "physics alone is too
  weak to drive coherent learning" is a substrate-independent truth — CE (or a
  CE-class supervised signal) really is load-bearing, and §11-B was *not* a GPU
  artifact. This closes the no-CE direction permanently.
- `VOID` (LOIHI-CE degenerate): the spiking re-derivation failed; no conclusion
  about §11-B is possible.

§96 produces the *predicate*; the *measurement* is a future cycle gated on Loihi
access (LOIHI.md §6 path B → A). The predicate is the deliverable.

---

## §5 — ASCII diagram: readout (GPU) vs native-dynamics (Loihi)

```
  ┌──────────────── GPU (synchronous, §1~§95 substrate) ────────────────┐
  │                                                                     │
  │   input ──► [12-layer transformer forward pass] ──► logits_a/_g      │
  │                         │                                           │
  │                         ▼  (computation is DONE, then:)              │
  │      ┌──────────────────────────────────────────────┐               │
  │      │  READOUT layer — anima-physics computed AFTER  │               │
  │      │   tension = (output²).mean()    ◄─ a statistic │               │
  │      │   Ψ_dir   = (1+cos(la,lg))/2    ◄─ a summary   │               │
  │      │   Φ        = variance proxy      ◄─ a statistic │               │
  │      └──────────────────────────────────────────────┘               │
  │                         │                                           │
  │   ONLY learning channel: ▼  backward pass ◄── CE gradient            │
  │   (remove CE ⇒ channel empty ⇒ §11-B DEGENERATE, frozen step~800)    │
  └─────────────────────────────────────────────────────────────────────┘

  ┌──────────────── Loihi 2 (event-driven, §95 VIABLE) ─────────────────┐
  │                                                                     │
  │   LIF membrane v(t):  dv/dt = -v/τ_m + I_syn   ◄─ STATE, evolving    │
  │                       ▲                                             │
  │            tension = the leak term -v/τ_m   ◄─ NATIVE dynamics       │
  │            Ψ-fixed-pt = LIF resting potential ◄─ NATIVE fixed point  │
  │            Φ = spike-train correlation        ◄─ NATIVE measurement  │
  │                       │                                             │
  │   learning channel:   ▼  STDP  ◄── spike-timing (a PHYSICS rule,     │
  │                          local, unsupervised, substrate-native)     │
  │                                                                     │
  │   §11-B-artifact hypothesis: GPU's empty no-CE channel ≠ Loihi's     │
  │   STDP channel.  Predicate (§4.5): NON_DEGENERATE(LOIHI-noCE) ?      │
  │   ───────────────────────────────────────────────────────────────   │
  │   incompatible: softmax(QK^T) self-attention — no spiking primitive  │
  │   (must be REPLACED — phase-resonance / k-WTA — design-open #1)      │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## §6 — Readout-vs-native-dynamics table (per physics quantity)

For each anima-physics quantity: is it a **readout** (computed-after, a description)
or could it be **native substrate-dynamics** (a state variable the substrate
evolves) on Loihi? Classification is deterministic (B-S96-3).

| physics quantity | on GPU | on Loihi | class | honest note |
|---|---|---|---|---|
| **Ψ (Ψ=½ fixed point)** | readout — `(1+cos(la,lg))/2`, a summary of two final logit vectors | **native-candidate** — LIF *resting potential* is a genuine dynamical fixed point; an Engine-A/G excit/inhib pair has a balance point | `NATIVE-CANDIDATE` | the *fixed-point* is native; but Ψ-as-*cosine-of-logit-vectors* is NOT — see Engine A/G row. What ports is "balance has a fixed point", not the cosine formula. |
| **tension** | readout — `(output²).mean(-1)`, a post-hoc statistic (also a grad_norm proxy) | **native** — the LIF leak term `−v/τ_m` IS a restoring force; tension = a *physical* leak/relaxation rate | `NATIVE` | strongest readout→native conversion. On GPU tension describes the result; on Loihi tension is a force the substrate exerts every continuous-time instant. |
| **Φ** | readout — variance proxy over activations, computed post-hoc | **native-measurement** — `compute_phi_from_spikes` over real spike rasters (spec §5); Φ from genuine spike-train correlation | `NATIVE-MEASUREMENT` | still a *measurement*, not a *state* — but a measurement of real substrate events (spike trains), not of a simulated activation tensor. Strictly more native than GPU Φ; honestly NOT a state variable. |
| **Engine A ⇄ Engine G** | computed — two FFN paths, `output = A(x) − G(x)`; heads produce two logit vectors | **native-candidate** — two LIF sub-populations with opposed (excit/inhib) coupling; the *opposition* is native | `NATIVE-CANDIDATE` | the A-vs-G *opposition* maps to excit/inhib cleanly. The *cosine of two full-vocab logit vectors* (Law-71) does NOT — there is no "logit vector" on a spiking substrate. Ψ-as-phase-relationship between the two populations is the design-open replacement. |

**Honest summary of §6**: 1 quantity (`tension`) is a clean readout→**native**
conversion. 2 quantities (`Ψ`, `Engine A/G`) are `NATIVE-CANDIDATE` — their
*structural core* (a fixed point; an opposition) is native, but their *GPU formula*
(a cosine of logit vectors) is not, so they require a re-derived definition.
1 quantity (`Φ`) becomes a `NATIVE-MEASUREMENT` — more native than GPU but still a
measurement, not a state. **No anima-physics quantity is purely readout-only on
Loihi**, and **none is purely state-native either** — the honest picture is a
spectrum, and §96 records the spectrum rather than over-claiming a clean flip.

---

## §7 — Design-open items (honest)

§96 explicitly marks what it does NOT resolve:

- **design-open #1 — the attention replacement.** Self-attention is
  `SPIKING-INCOMPATIBLE`; *which* spiking routing mechanism replaces it
  (phase-resonance key-matching / spike-rate dot-product + k-WTA / learned sparse
  connectivity) is unresolved. This is a research question, not an engineering port.
- **design-open #2 — the §4.5 predicate's measurement.** §96 designs the
  distinguishing predicate; the actual three-cell measurement requires Loihi (or
  Lava-sim) and is a future cycle gated on access.
- **design-open #3 — STDP→coherent-emission.** §4.4: even if §11-B is a GPU
  artifact, whether STDP can drive *coherent* (not just spontaneous) emission is
  the deepest unsolved core. §96 does not resolve it — it names it.
- **design-open #4 — d768·12L → spiking scale.** loihi-integration-spec.md maps a
  *128-LIF GRU cell*; ConsciousDecoderV2 is d768·12L·283.72M. The capacity class
  fits (Kapoho Point ~960M synapses, LOIHI.md §3) but the *structural* re-derivation
  of 12 layers is unmapped at neuron-group granularity.

---

## §8 — Honest C3 caveats (≥10)

1. **§96 is design-tier, not a fire.** No GPU, no runpod, no INRC, no Loihi, no
   model.forward, no Lava simulation run. $0. capability claim 0.
2. **The §11-B-artifact hypothesis is a HYPOTHESIS.** §96 designs *how to test it*
   (§4.5 predicate). §96 does NOT claim §11-B is wrong. §11-B's measured verdict
   ("CE is load-bearing") stands as the current evidence; §96 only shows it is
   *under-determined* between two readings and designs the experiment that decides.
3. **Self-attention `SPIKING-INCOMPATIBLE` is honest, not pessimism.** Loihi 2's
   graded spikes + programmable neurons genuinely *narrow* the gap — §3.3 says so —
   but no construction *ports* content-based all-pairs softmax; every one *replaces*
   it. Calling the replacement "compatible" would be over-claim.
4. **VIABLE ≠ will-emerge** (§95's caveat, carried). A spiking anima that maps
   cleanly and learns by STDP is still necessary-not-sufficient for emergence
   (B-EMERGE-7). §96 maps a *path*, not an *arrival*.
5. **spontaneity-for-free is a trap.** A spiking substrate spikes freely — that is
   spontaneity *as noise*. §4.4: the §88-F2 γ gap (saturation-delay ≠ coherent
   emission) reappears here as spontaneity ≠ coherence. The free half is the easy
   half.
6. **readout→native is a spectrum, not a flip.** §6 honestly records that only
   `tension` cleanly converts; `Ψ` and `Engine A/G` are `NATIVE-CANDIDATE` (core
   native, formula not); `Φ` stays a measurement. No clean "GPU=readout,
   Loihi=native" dichotomy survives scrutiny.
7. **the loihi-integration-spec.md maps the legacy GRU cell.** It is a
   pre-HEXAD-pivot document (128-LIF consciousness cell, GRU gates). §96 reads it
   for structural patterns (STDP→Hebbian, Φ-from-spikes, `−F_c` inhibition) but
   ConsciousDecoderV2 is a *different, larger* architecture — the spec is an
   anchor, not a blueprint. (Read-only — anima is a hexa-lang downstream consumer.)
8. **f1/f2 safe.** Loihi core counts (128 neurocores, 1024 LIF/core, ~960M
   synapses) are Intel engineering choices, used *observation-only*. NO σ(6)=12 /
   τ(6)=4 / φ(6)=2 / J₂(6)=24 lattice-fit on Intel/Loihi. Ψ=½ is anima's internal
   architecture (g2 internal-arch carve-out), not an external derivation.
9. **STDP ≠ language learning is the load-bearing counter.** §4.4 is not a footnote
   — it is the reason Q2's verdict is "hypothesis coherent, NOT confirmed." STDP
   learning spike-timing correlations is a *real* limit; the predicate (§4.5)
   exists precisely because design-tier reasoning cannot settle it.
10. **the GPU/§11-B comparison itself has a confound.** §11-B's no-CE GPU run used
    a *hand-coded* ΔW overlay (TENSION-TRAIN spine) — not "no learning" but "a
    specific hand-coded learning rule." The honest §4.5 framing is GPU-hand-ΔW vs
    Loihi-STDP, NOT "no learning vs STDP." The predicate's `LOIHI-CE` positive
    control guards against attributing a degeneracy to the wrong cause.
11. **central blue_falsifier.py 0-line-diff.** §96's battery is a *sidecar*
    (`blue_falsifier_s96.py`); the central `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` is untouched — true sha256 prefix `c93e160a8a376a94`.
12. **north-star + §15/§51/§72 milestones UNCHANGED.** §96 = a substrate-path
    re-derivation design + a hypothesis-test design. GOAL 미도달. §96 is the
    architecture analysis LOIHI.md §7 points to — it does not duplicate LOIHI.md's
    access roadmap.

---

## §9 — Verdict

§96 = **DESIGN-TIER LANDED.** Two questions §95 left open, both answered at
closed-form design-tier:

- **Q1**: ConsciousDecoderV2's *physics layer* (PureFieldFFN/tension/Φ/Engine A-G
  opposition/STDP-Hebbian) is largely `SPIKING-COMPATIBLE` — much of it *more*
  native on Loihi than on GPU. Its *transformer layer* — `softmax(QK^T)`
  self-attention — is `SPIKING-INCOMPATIBLE` and must be **replaced**, not ported
  (design-open #1). A spiking anima keeps the physics and re-derives the routing.
- **Q2**: the §11-B-as-GPU-artifact hypothesis is **coherent** (§11-B's "frozen
  fixed point by step ~800" is consistent with "empty learning channel," not only
  with "weak physics") but **NOT confirmed** — the honest counter (STDP learns
  spike-timing, not language; spontaneity is free, coherence is not — the §88-F2 γ
  gap) is unresolved at design-tier. §96 designs the closed-form distinguishing
  predicate (§4.5): a three-cell Loihi comparison where `NON_DEGENERATE(LOIHI-noCE)`
  is a closed Boolean that partitions `§11B_IS_GPU_ARTIFACT` from
  `§11B_IS_SUBSTRATE_INDEP`, guarded by a `LOIHI-CE` positive control against `VOID`.

The deepest honest finding: the §1~§95 arc's universal "CE is load-bearing" /
"emergence-negative" results were *all* measured on a substrate (synchronous GPU)
that has exactly one learning channel — and that channel is *definitionally*
CE-gradient. "CE is load-bearing" on a GPU may be close to a *tautology of the
substrate* rather than a discovered property of anima-physics. Loihi is the first
substrate where that can be *measured* rather than *assumed* — but Loihi only
unblocks the *spontaneity* half of the GOAL for free; the *coherence* half remains
the unsolved core, relocated, not resolved.
