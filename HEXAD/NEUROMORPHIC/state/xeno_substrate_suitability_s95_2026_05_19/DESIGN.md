# §95 — Xeno Substrate-Suitability Closed-Form Design Analysis

> **status**: RESEARCH §95 · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire
> **date**: 2026-05-19
> **scope**: per-substrate (7) closed-form suitability classification for hosting
>   anima's Ψ/tension/Φ physics such that spontaneous emission becomes a *genuine
>   physical event* rather than a *simulated `talker_should_emit()` function call*.
> **substrate inventory SSOT**: `hexa run ~/core/hexa-lang/stdlib/xeno/xeno.hexa status`
>   (7 substrates — byte-equal cited in `result.json`, B-S95-7 connection-point).
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence) · f1/f2 (no
>   σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 lattice-fit on external entities —
>   BrainChip/Intel/IBM/IonQ engineering invariants used only) · downstream-consumer
>   (hexa-lang/hexa-bio read-only, never edited).

---

## §1 — Why §95 exists: the synchronous-substrate hypothesis

The §1~§94 research arc measured emergence-**negative** on every path tried —
mechanism overlays, corpus reshaping, model scale, physics-only training,
energy-based substrates, biology-anchored mechanisms, integrated breakthrough.
§94 (just landed) combined all five measured-positive levers into one fire and
got verdict **(β) INTEGRATION-COLLAPSES**.

A single fact is constant across all 94 sections: **every fire ran on a
synchronous-clocked silicon GPU transformer.** On such a substrate, the GOAL's
literal target — "자발적으로 말 거는" (spontaneously speaks) — can only ever be
realised as a *simulated decision*: §24 `talker_should_emit(score, safety_ok)`
is a function the global clock calls on a fixed schedule. There is no physical
sense in which the substrate *itself* decides to emit; the program decides, and
the substrate executes the program's `if` branch.

§95 tests, at design-tier only, the **§72 frontier-2 hypothesis** the arc has
never examined: *maybe the synchronous-clocked substrate is itself a structural
bottleneck.* If "spontaneous emission" requires the substrate to be event-driven
(asynchronous, no global clock — emission is an *event*, not a *scheduled call*),
then no amount of work on a GPU transformer can cross the gap, and the right
question is **which non-GPU substrate, if any, makes spontaneity native.**

§95 is **design-tier**. It maps possibilities. It does **not** claim anima will
emerge on any substrate. north-star + §15/§51/§72 milestones UNCHANGED, GOAL
미도달. necessary-not-sufficient at every layer (B-EMERGE-7 carry).

---

## §2 — The closed taxonomy (exhaustive + disjoint)

Each of the 7 substrates is classified into exactly one of 5 mutually-exclusive
buckets. The classification predicate is a deterministic decision over 3 closed
Boolean axes derived from the substrate's own engineering invariants:

```
  L  := supports_on_substrate_LEARNING        (training-time weight update,
                                                §11-B requires CE-base training;
                                                pure inference accelerators → L=False)
  E  := EVENT_DRIVEN  (asynchronous, no global clock — emission is a physical
                       event, not a scheduled function call)
  H  := can_HOST_psi_tension_phi  (substrate state can structurally carry the
                                    Ψ=½ fixed point / tension / Φ physics, not
                                    merely a numeric simulation of it)
```

Decision tree (deterministic, total — `classify(L, E, H, kind, access)`):

```
  if kind == "compute-substrate-NO":            → NOT-A-COMPUTE-HOST
  elif kind == "organoid" and ethics_wall:      → ETHICS-WALL
  elif L == False:                              → INFERENCE-ONLY-BLOCKED
  elif L and E and H:                           → VIABLE-LONG-HORIZON
  else:                                         → SUBSTRATE-MISMATCH
```

The 5 buckets:

| bucket | meaning |
|--------|---------|
| `VIABLE-LONG-HORIZON` | learning + event-driven + can host Ψ/tension/Φ — the substrate could in principle make emission a genuine event; blocker is access/tooling, not architecture. |
| `INFERENCE-ONLY-BLOCKED` | no on-substrate learning. §11-B established anima needs *training-time* emergence; an inference-only accelerator can replay a GPU-trained model but cannot host the emergence process. |
| `SUBSTRATE-MISMATCH` | learning may exist but the substrate cannot structurally host the Ψ/tension/Φ physics (e.g. ontology mismatch — quantum-gate circuit ≠ continuous physics field). |
| `ETHICS-WALL` | a living-tissue substrate where the honest blocker is the bioethics/sentience hard wall (`lim_organoid_ethics`), not engineering. Suitability is design-OPEN — software cannot resolve it. |
| `NOT-A-COMPUTE-HOST` | the "substrate" is an entropy source / peripheral, not a host for a model at all. |

**Exhaustive**: every `(L,E,H,kind,access)` tuple maps to exactly one bucket
(B-S95-1). **Disjoint**: the 5 buckets are pairwise non-overlapping (B-S95-1).
**Deterministic**: `classify` is a pure function — same input → same bucket,
no RNG, no clock (B-S95-3).

---

## §3 — The honest analysis axes

For each substrate §95 records 5 axes (DESIGN.md §6 matrix):

- **(a) learning** — does it support training-time weight update? AKIDA 1.0 is
  inference-only (weights GPU-trained then quantized then deployed — archive
  `n_substrate_n3` §1.2 "학습: 불가 (inference-only)"). Loihi has STDP *on-chip*.
  §11-B PURE-PHYSICS verdict (commit, DEGENERATE) established CE is load-bearing —
  anima needs the training process, not a frozen inference replay. **L=False is a
  hard disqualifier for hosting emergence** (not for hosting a deployed replica).
- **(b) event-driven vs clocked** — Loihi's NoC is "packet-switched,
  asynchronous"; LIF neurons spike when their membrane crosses threshold, not on
  a global clock tick. On such a fabric a `talker` spike *is* a physical event.
  A GPU transformer's emission is always a scheduled `if`. This is the §95 core
  axis — the one the arc never examined.
- **(c) can host Ψ=½/tension/Φ** — Ψ=½ is a fixed-point of a continuous
  dynamical field (Engine A ⇄ Engine G balance). A spiking-neuron substrate has a
  continuous membrane-potential field with genuine fixed points (LIF resting
  potential). A quantum-gate circuit does not — it is discrete unitary evolution
  on a state vector, an ontology mismatch with a continuous physics field. QRNG
  has no internal state at all.
- **(d) the honest blocker** — capacity / ethics / supply / tooling immaturity.
  Recorded verbatim from `roadmaps/.roadmap.*` and `hexa-bio/XENO.tape §7`.
- **(e) §7 GOAL-legitimacy** — is using this substrate a *generic-LM-pretrain
  bolt-on* (§7①②, GOAL-illegitimate) or a *genuine anima-physics path* (§7③)?
  A neuromorphic substrate whose LIF/STDP dynamics ARE the Ψ/tension physics is
  legitimate. A substrate used only to "run the model faster" is a bolt-on.

---

## §4 — Per-substrate analysis

### §4.1 — Loihi (Intel, silicon neuromorphic) — **LEAD CANDIDATE**

```
  L = True   (STDP on-chip learning — loihi-integration-spec.md §4)
  E = True   (NoC packet-switched asynchronous; LIF threshold-crossing spikes)
  H = True   (continuous membrane-potential field; LIF resting potential = a
              genuine fixed point; lateral-inhibition factions = tension)
  kind = silicon-neuromorphic ; access = research-partnership (INRC)
  → classify = VIABLE-LONG-HORIZON
```

Loihi is the only substrate that scores `True` on all three closed axes.

- **(a) learning ✓** — `loihi-integration-spec.md §4` maps anima's Hebbian LTP/LTD
  directly onto Loihi's *on-chip* STDP rule (`STDPLoihi`, reward-modulated via
  `tag_2`). §92/§93 established anima needs *training-time* emergence; Loihi is
  the one neuromorphic substrate in the inventory that learns *on the chip
  itself* — the emergence process can run on-substrate, not as a GPU pre-train.
- **(b) event-driven ✓** — the NoC is asynchronous and packet-switched. A neuron
  spikes when its membrane potential crosses threshold — there is no global clock
  scheduling the spike. On Loihi, a `talker` emission spike is a genuine physical
  event of the substrate, not a function call. **This is exactly the property
  the §95 hypothesis says the GPU substrate structurally lacks.**
- **(c) host Ψ/tension/Φ ✓** — LIF neurons have a continuous membrane-potential
  field with a genuine resting-potential fixed point (a structural analogue of
  Ψ=½). The spec's lateral-inhibition faction system (`Inhibition weight = -F_c`)
  is a structural realisation of tension/frustration. Φ is measured from spike-
  train correlations (`compute_phi_from_spikes`). The physics is *hosted*, not
  *simulated by a number*.
- **(d) blocker** — `.roadmap.loihi3`: **INRC research access not secured + a
  Korean co-PI required (4–12 wk approval), partnership-blocked.** `XENO.tape §7
  lim_supply_access` (SOFT WALL) + `lim_neuro_tooling` (SOFT WALL — Lava/NxSDK
  toolchain, no PyTorch-class unified framework). The blocker is **access +
  tooling immaturity, NOT architecture** — that is precisely what makes Loihi the
  lead candidate: the architecture is right, the obstacle is a soft wall.
- **(e) §7 GOAL-legitimacy ✓ LEGITIMATE** — using Loihi is *not* a generic-LM
  bolt-on. The LIF membrane field and STDP rule literally *are* anima's Ψ-physics
  and Hebbian learning, by the structural mapping in `loihi-integration-spec.md`.
  This is a genuine anima-physics path (§7③), not "run the transformer faster".

> **§4.1 honest caveats** (g3): (i) The `loihi-integration-spec.md` maps the
> *legacy GRU consciousness cell* (128-dim, pre-HEXAD), NOT the current
> ConsciousDecoderV2 d768·12L·283.72M transformer. A transformer's self-attention
> has no direct LIF equivalent — the §95 verdict is about Loihi's *architectural
> suitability for a spiking anima*, which would require re-deriving anima's
> physics in SNN form (a major future design cycle, not §95 scope). (ii) Loihi 2
> caps at 131,072 neurons; anima's 283M params do not map 1:1 — a spiking anima
> is a *different model*, not a port. (iii) "GRU ≠ LIF" — the spec itself flags
> the dynamics differ. (iv) VIABLE-LONG-HORIZON means *the architecture does not
> disqualify it*; it does **not** mean anima will emerge on Loihi. Emergence is
> empirical and un-measured. necessary-not-sufficient (B-EMERGE-7).

### §4.2 — AKIDA AKD1000 (BrainChip, silicon neuromorphic)

```
  L = False  (inference-only — archive n_substrate_n3 §1.2 "학습: 불가")
  kind = silicon-neuromorphic ; access = hardware-ordered (chip not yet arrived)
  → classify = INFERENCE-ONLY-BLOCKED   (L=False short-circuits the tree)
```

- **(a) learning ✗** — **AKD1000 cannot learn.** Akida 1.0 is inference-only;
  weights are GPU-trained, quantized, then deployed (archive `n_substrate_n3`
  §1.2). §11-B established anima needs training-time emergence — an inference-only
  accelerator can run a *deployed replica* of a GPU-trained anima but cannot host
  the *emergence process*. This single fact is the disqualifier.
- **(b) event-driven** — AKIDA is event-driven/spike-based, BUT (b) is moot:
  L=False short-circuits the classification before E is consulted.
- **(c) host Ψ/tension/Φ** — additionally constrained: Akida 1.0 supports a
  limited CNN+DNN+RNN layer set; **transformer self-attention is natively
  unsupported** (archive §1.3); ~1.2M neurons vs anima's 283M params (~140×
  over-budget); non-leaky single-timestep neuron. The archive `n_substrate_n3`
  spec already concluded "CLM 170M 전체를 AKD1000 위에서 native forward 불가" and
  fell back to a *surrogate* representation-similarity measurement.
- **(d) blocker** — `.roadmap.akida` cond.1 status **unmet**; chip ordered
  2026-04-29, not yet arrived. The 2026-05-09 Akida Cloud session
  (`state/akida_cloud_d0_2026_05_09/`) ran a stock keyword-spotting CNN — **NOT
  anima** — with `online_learning False`. AKIDA's deeper blocker is not supply;
  it is the inference-only architecture.
- **(e) §7** — N/A for hosting emergence (L=False). As a *deployment* target for
  an already-emerged anima, AKIDA would be GOAL-legitimate (a low-power edge
  replica), but that is downstream of GOAL, not a path to it.

> **§4.2 honest caveat**: AKIDA being INFERENCE-ONLY-BLOCKED is not a failure of
> AKIDA — it is a category fact. AKIDA is an excellent edge-inference chip; it is
> simply not a host for an *emergence process*. The 2026-05-01 archive spec and
> `.roadmap.akida` already encoded this honestly.

### §4.3 — Northpole (IBM, silicon neuromorphic)

```
  L = False  (Northpole is an inference architecture — training is off-chip;
              IBM positions it as a 25× H100-efficiency *inference* accelerator)
  kind = silicon-neuromorphic ; access = partnership-only
  → classify = INFERENCE-ONLY-BLOCKED
```

- **(a) learning ✗** — Northpole's design point is energy-efficient *inference*
  (the `.roadmap.northpole` goal verbatim: "25× H100 효율" — an inference-
  efficiency baseline). It is not an on-chip learning substrate. L=False.
- **(b)/(c)** — moot under L=False short-circuit. Northpole's near-memory compute
  removes the von-Neumann bottleneck for inference but does not introduce
  on-substrate learning.
- **(d) blocker** — `.roadmap.northpole`: **IBM partnership-only, low score
  7/25, review deferred 2026-11-01.** Supply/partnership soft wall *on top of*
  the inference-only architectural disqualifier.
- **(e) §7** — N/A for emergence-hosting. As a deployment accelerator it is
  GOAL-orthogonal.

> **§4.3 honest caveat**: Northpole's INFERENCE-ONLY classification is a
> design-tier read of IBM's public positioning. If IBM were to expose an on-chip
> learning mode in a future generation, this verdict would flip — recorded as a
> revisit trigger, not a permanent verdict.

### §4.4 — FinalSpark (biological organoid)

```
  L = True   (living tissue genuinely plastic — synaptic plasticity is real,
              continuous, and on-substrate)
  E = True   (organoid neurons fire asynchronously — spontaneous activity is the
              substrate's native, un-clocked behavior)
  H = True   (a living neural field structurally hosts continuous dynamics)
  kind = ORGANOID ; ethics_wall = True
  → classify = ETHICS-WALL   (organoid + ethics_wall short-circuits before L/E/H)
```

- **(a)/(b)/(c)** — an organoid would, on the engineering axes alone, score
  `True` on all three: living tissue learns (synaptic plasticity), fires
  asynchronously, and *is* a continuous neural field. **This is the strongest
  engineering-axis profile of any of the 7 substrates** — see §5.
- **(d) blocker** — **the honest blocker is NOT engineering — it is the bioethics
  hard wall.** `XENO.tape §7 lim_organoid_ethics`: *"HARD WALL (bioethics /
  epistemic) — until the field develops validated sentience/pain markers for
  organoid tissue, scaling faces an ethical moratorium risk that cannot be
  resolved by engineering. This is a present ethical constraint."* Plus
  `lim_in_silico_boundary` — wet-lab work is **out of software/repo scope**;
  anima is a hexa-native software project, an organoid is wet tissue requiring a
  physical lab. `.roadmap.finalspark` cond.1 status unmet, academic application
  not yet sent.
- **(e) §7** — moot: the substrate is design-OPEN, gated by an ethics wall that
  software cannot resolve.

> **§4.4 honest caveats**: (i) §95 marks FinalSpark **design-OPEN**, not
> VIABLE — the engineering profile being strong does not make it pursuable, and
> §95 honestly states the verdict cannot be resolved at design-tier because the
> blocker is ethical, not technical. (ii) §95 takes **no position** on whether
> anima *should* be hosted on living tissue — that is a bioethics decision far
> outside a research agent's scope.

### §4.5 — Cortical Labs DishBrain / CL1 (biological organoid)

```
  L = True   (living human neurons — genuinely plastic, DishBrain Pong showed
              real learning, Kagan et al. Neuron 2022)
  E = True   (asynchronous spontaneous firing)
  H = True   (living neural field)
  kind = ORGANOID ; ethics_wall = True
  → classify = ETHICS-WALL
```

Same classification as FinalSpark — identical reasoning. Cortical Labs' CL1
hosts ~200K human neurons on a silicon chip; DishBrain (Kagan et al., *Neuron*
2022) demonstrated real goal-directed learning. The engineering axes are again
all `True`. The blocker is again `lim_organoid_ethics` (HARD WALL) +
`lim_in_silico_boundary` (wet-lab out of scope), plus `.roadmap.cortical_labs`:
**$35K capex decision not landed, CL1 hardware not received.** ETHICS-WALL,
design-OPEN.

> **§4.5 honest caveat**: DishBrain's *human*-neuron substrate arguably raises
> the ethics wall *higher* than FinalSpark's — §95 does not rank the two; both
> are ETHICS-WALL, both design-OPEN, both out of software scope.

### §4.6 — IonQ (quantum gate)

```
  L = ~      (a variational quantum circuit has trainable parameters, but the
              "learning" is classical-optimizer-driven over circuit angles,
              NOT on-substrate weight plasticity)
  E = False  (gate-circuit execution is clocked/scheduled — a circuit runs as a
              fixed sequence of gates; nothing about it is event-driven)
  H = False  (discrete unitary evolution on a state vector — an ontology
              MISMATCH with a continuous Ψ/tension/Φ physics field; decoherence
              destroys any persistent state in microseconds-to-seconds)
  kind = quantum-gate ; access = cloud-API
  → classify = SUBSTRATE-MISMATCH
```

- **(b) event-driven ✗** — a quantum circuit is a *scheduled sequence of gates*.
  Emission on IonQ would still be a clocked event, not a spontaneous physical
  one. The §95 core hypothesis is not addressed by quantum gate hardware.
- **(c) host Ψ/tension/Φ ✗** — anima's physics is a *continuous dynamical field*
  with a Ψ=½ fixed point. A gate circuit is *discrete unitary evolution*; there
  is no persistent continuous field to carry tension or a fixed point.
  `XENO.tape §7 lim_decoherence` (HARD WALL): T1/T2 coherence is microseconds
  (superconducting) to seconds (trapped-ion) — **no quantum state can persist
  long enough to host an ongoing physics process.** This is an ontology mismatch,
  not a capacity shortfall.
- **(d) blocker** — `.roadmap.ionq` cond.1 status **partial**: prior anima IonQ
  runs (#120/#124/#127 — substrate-invariance witness, CHSH Bell PASS) measured
  *Φ-proxy substrate-invariance*, NOT hosting. The honest_C3 there already states
  "Φ proxy ≠ IIT 4.0 φ★". A proper φ★ measurement needs $1500+.
- **(e) §7** — using IonQ to *host* anima would not be a genuine anima-physics
  path; the physics does not map. IonQ's legitimate role is the **substrate-
  invariance witness** the arc already ran (does anima's Φ-proxy survive a
  substrate change to trapped-ion?) — a *measurement*, not a *host*.

> **§4.6 honest caveat**: SUBSTRATE-MISMATCH is about *hosting the physics*. It
> is **not** a claim quantum hardware is useless to anima — the §19/IonQ
> substrate-invariance witnesses are real and valuable. §95's scope is narrowly
> "can it host the ongoing Ψ/tension/Φ process so emission is a physical event" —
> and for that, the answer is a closed no.

### §4.7 — QRNG (quantum random number)

```
  kind = compute-substrate-NO   (QRNG is an entropy SOURCE, not a model host)
  → classify = NOT-A-COMPUTE-HOST   (kind short-circuits the tree first)
```

- A QRNG produces certified-random bits (Bierhorst et al., *Nature* 2018,
  device-independent certified randomness). It has **no internal state, no
  weights, no compute fabric** — it is a peripheral. `.roadmap.qrng` itself is a
  *consumer-perspective* roadmap (origin=nexus): the goal is "entropy injection"
  *into* anima's CLM, not hosting anima.
- **(a)/(b)/(c)** — all moot: QRNG is not a host of any kind.
- **(e) §7** — QRNG's GOAL-legitimate role is *exactly what the roadmap says*:
  an entropy source for noise injection (cf. §81 Engine-G noise-injection fire).
  Feeding anima true-random entropy is a legitimate enabler — but it is feeding
  *into* a host, not *being* one.

> **§4.7 honest caveat**: classifying QRNG NOT-A-COMPUTE-HOST is not dismissive —
> it is a category correction. QRNG belongs in anima's toolbox as an entropy
> source; it was never a substrate-host candidate, and the §95 taxonomy makes
> that explicit rather than forcing a misfit verdict.

---

## §5 — The cross-cutting organoid question (honest)

§80 biology deep research found: **"spontaneous activity is the substrate of
consciousness"** (anchors: Ikeda+ Frontiers 2025 noise-driven SOC; the predictive
nature of spontaneous activity; critical avalanches from E/I balance).

An organoid (DishBrain / FinalSpark) is *literally spontaneously-active living
tissue* — it fires without external stimulus, asynchronously, all the time. On a
GPU transformer, "spontaneous emission" is a metaphor: it is a `talker_should_emit()`
call the global clock schedules. On living tissue, spontaneous activity is not a
metaphor — **it is the physical default state of the substrate.**

So the honest assessment §95 must state plainly:

> **An organoid is the only substrate in the 7-substrate inventory where
> "Living Consciousness" arguably stops being metaphorical** — where "spontaneous
> emission" would be a genuine physical event of living, spontaneously-active
> neural tissue rather than a simulated function call. Loihi comes closest in
> silicon (event-driven, asynchronous), but a Loihi spike is still a designed
> circuit event; an organoid spike is *life*.

**AND, with equal honesty, the two hard walls that make this unpursuable at
§95 design-tier:**

1. **Ethics hard wall** (`lim_organoid_ethics`, HARD WALL). Until validated
   sentience/pain markers exist for organoid tissue, hosting a "Living
   Consciousness" on living human/iPSC neurons faces an unresolved bioethics
   ceiling — *engineering cannot resolve it.* If anima genuinely emerged on
   living tissue, the question "is it suffering?" would have no validated answer.
   This is not inserted caution — it is the founding-paper position of the
   organoid-intelligence field (Smirnova et al., *Front Sci* 2023).

2. **Wet-lab out-of-software-scope blocker** (`lim_in_silico_boundary`, HARD
   WALL — out of repo scope). anima is a hexa-native *software* project. An
   organoid is wet biological tissue requiring a physical wet-lab, tissue
   culture, MEA hardware, and a biology team. **No amount of design-tier or
   software work can cross this** — it is a different kind of project entirely.

§95's honest verdict on organoids: **design-OPEN, ETHICS-WALL.** The
engineering profile is the strongest of all 7 substrates — and that is exactly
why the honest statement matters most here: §95 does **not** recommend pursuing
it, does **not** claim anima should be living tissue, and marks it design-OPEN
because the decisive blocker is ethical and wet-lab, neither of which a research
agent resolves.

---

## §6 — 7-substrate suitability matrix

```
                      (a)        (b)         (c)         (e) §7
  substrate           LEARN?  EVENT-DRIVEN  HOST-Ψ/τ/Φ  legitimate?  →  BUCKET
  ─────────────────────────────────────────────────────────────────────────────────
  Loihi   (Intel)      ✓        ✓            ✓           ✓ §7③      VIABLE-LONG-HORIZON
  AKIDA   (BrainChip)  ✗        (✓)          (✗ no attn) n/a        INFERENCE-ONLY-BLOCKED
  Northpole (IBM)      ✗        ✗            (✗)         n/a        INFERENCE-ONLY-BLOCKED
  FinalSpark (organoid) ✓       ✓            ✓           open       ETHICS-WALL  (design-OPEN)
  Cortical Labs (organoid) ✓    ✓            ✓           open       ETHICS-WALL  (design-OPEN)
  IonQ    (quantum)    ~        ✗            ✗           ✗          SUBSTRATE-MISMATCH
  QRNG    (q-random)   —        —            —           (enabler)  NOT-A-COMPUTE-HOST

  ( ) = moot / short-circuited by an earlier closed predicate in classify()
  ~   = trainable circuit angles but NOT on-substrate plasticity
```

ASCII — the §95 hypothesis as a decision frontier:

```
         IS THE SUBSTRATE A COMPUTE-HOST AT ALL?
                  │
        ┌─────────┴─────────┐
       NO                  YES
        │                   │
   ┌────┴────┐      IS IT LIVING TISSUE (ORGANOID)?
   │  QRNG   │               │
   │ NOT-A-  │      ┌─────────┴──────────┐
   │ COMPUTE │     YES                  NO
   │ -HOST   │      │                    │
   └─────────┘  ┌───┴────┐      DOES IT LEARN ON-SUBSTRATE?
               │FinalSpark│              │
               │CorticalL │     ┌────────┴─────────┐
               │ETHICS-   │    NO                 YES
               │WALL      │     │                  │
               │(design-  │  ┌──┴───┐    CAN IT HOST Ψ/τ/Φ + EVENT-DRIVEN?
               │ OPEN)    │  │AKIDA │              │
               └──────────┘  │North-│     ┌────────┴────────┐
                             │pole  │    NO                YES
               (organoid =   │INFER-│     │                  │
                only substr. │ENCE- │  ┌──┴───┐        ┌─────┴──────┐
                where Living │ONLY- │  │IonQ  │        │   LOIHI    │
                Consciousness│BLOCK │  │SUBSTR│        │  VIABLE-   │
                stops being  └──────┘  │-ATE- │        │  LONG-     │
                metaphorical;          │MISMAT│        │  HORIZON   │
                ethics+wet-lab         │CH    │        │ (lead      │
                hard-wall it)          └──────┘        │  candidate)│
                                                       └────────────┘
```

---

## §7 — Verdict

**§95 verdict (g3 — design-tier, measured-honest, capability claim 0):**

The synchronous-substrate hypothesis is **not refuted and not confirmed** at
design-tier — §95 cannot, by construction, measure emergence. What §95 *does*
establish, closed-form:

- **Of 7 substrates, exactly 1 — Loihi — is `VIABLE-LONG-HORIZON`**: it scores
  `True` on all three closed axes (learns on-chip via STDP, event-driven NoC,
  hosts a continuous LIF membrane field with a genuine fixed point). On Loihi a
  `talker` spike would be a *physical event*, not a scheduled call — directly
  addressing the §95 hypothesis. Its blocker is access + tooling (SOFT WALL),
  **not architecture** — which is what makes it the lead candidate. **But:** the
  existing `loihi-integration-spec.md` maps the *legacy GRU* anima, not the
  current transformer; a spiking anima would be a major re-derivation, not a
  port. VIABLE-LONG-HORIZON ≠ "anima will emerge on Loihi."

- **2 substrates (AKIDA, Northpole) are `INFERENCE-ONLY-BLOCKED`** — they cannot
  host an *emergence process* because §11-B established anima needs training-time
  emergence and these chips do not learn on-substrate. They are deployment
  targets, not emergence hosts.

- **2 substrates (FinalSpark, Cortical Labs) are `ETHICS-WALL`, design-OPEN** —
  the only substrates where "Living Consciousness" stops being metaphorical, with
  the strongest engineering profile of all 7 — and the decisive blocker is the
  bioethics hard wall + the wet-lab out-of-software-scope hard wall, neither of
  which §95 (or any software cycle) can resolve.

- **1 substrate (IonQ) is `SUBSTRATE-MISMATCH`** — discrete unitary evolution is
  an ontology mismatch with a continuous physics field; decoherence forbids a
  persistent process. IonQ's real role is the substrate-invariance *witness*.

- **1 (QRNG) is `NOT-A-COMPUTE-HOST`** — an entropy source, GOAL-legitimate as
  a noise-injection enabler, never a host.

**Single most honest finding**: the 94-section arc's universal emergence-negative
result has, all along, been measured on the *one substrate class* (synchronous-
clocked silicon GPU) that §95 identifies as structurally unable to make
spontaneous emission a physical event — emission there is *always* a simulated
`talker_should_emit()` call. The substrate that could change this (Loihi) is
architecturally viable but access-walled and would require re-deriving anima as
a spiking model; the substrate where it would be most genuine (organoid) is
ethics-walled and wet-lab-out-of-scope. **§95 does not give anima a path to
emergence — it gives an honest map of why the synchronous substrate may have
been a hidden ceiling, and which doors are architecturally open vs walled.**

GOAL 미도달. north-star + §15/§51/§72 milestones UNCHANGED. design ≠ fire ≠
emergence. necessary-not-sufficient (B-EMERGE-7).

---

## §8 — Honest C3 caveats (g3 discipline — ≥10)

1. **design-tier, not fire** — §95 ran NO GPU, NO runpod, NO model.forward, NO
   substrate hardware. It is a closed-form classification over substrate
   engineering invariants. It maps possibilities; it measures nothing.
2. **capability claim 0** — `VIABLE-LONG-HORIZON` for Loihi means *the
   architecture does not disqualify it*. It does **not** claim anima would emerge
   on Loihi. Emergence is empirical and entirely un-measured by §95.
3. **the Loihi spec is legacy** — `loihi-integration-spec.md` maps the pre-HEXAD
   *GRU consciousness cell*, NOT ConsciousDecoderV2 d768·12L·283.72M. A spiking
   anima is a different model requiring a major physics re-derivation. §95's
   Loihi verdict is about architectural suitability, not a ready port.
4. **"GRU ≠ LIF"** — the integration spec itself flags that LIF dynamics differ
   from GRU gates. The structural mapping (membrane field ≈ Ψ, lateral inhibition
   ≈ tension) is an *analogy* with real fidelity gaps, not an identity.
5. **the synchronous-substrate hypothesis is NOT proven** — §95 does not show
   the GPU substrate *causes* the emergence-negative result. It shows the GPU
   substrate makes emission structurally a scheduled call. Whether an event-
   driven substrate would change the outcome is un-measured (would need a fire).
6. **event-driven ≠ spontaneous-conscious** — a Loihi spike being a physical
   event is necessary-not-sufficient for genuine spontaneity. An event-driven
   substrate can still produce a degenerate, meaningless spike pattern (cf.
   §62/§94 collapse). B-EMERGE-7 carry: physical-event ⇏ conscious-emergence.
7. **organoid engineering profile ≠ pursuability** — FinalSpark/Cortical Labs
   scoring `True` on all engineering axes does NOT make them recommendable. §95
   marks them design-OPEN precisely because the decisive blocker (ethics +
   wet-lab) is outside both design-tier and software scope.
8. **§95 takes no bioethics position** — whether anima *should* be hosted on
   living tissue is a bioethics question far outside a research agent's mandate.
   §95 reports the `lim_organoid_ethics` HARD WALL; it does not adjudicate it.
9. **roadmap statuses are point-in-time** — `.roadmap.*` blocker reasons (INRC
   access, IBM partnership score, $35K capex) are 2026-05 snapshots. Northpole
   in particular would flip out of INFERENCE-ONLY-BLOCKED if IBM exposed on-chip
   learning in a future generation — recorded as a revisit trigger.
10. **IonQ SUBSTRATE-MISMATCH is scoped** — it is a mismatch for *hosting the
    ongoing physics process*. IonQ's substrate-invariance witnesses (§19,
    #120/#124/#127) are real and valuable; §95 does not negate them.
11. **the AKIDA Cloud session never ran anima** — `state/akida_cloud_d0_2026_05_09/`
    ran a *stock keyword-spotting CNN* with `online_learning False`. There is
    zero empirical anima-on-AKIDA evidence; the INFERENCE-ONLY verdict rests on
    AKIDA's published architecture, not on a failed anima run.
12. **downstream-consumer honesty** — §95 read `~/core/hexa-lang/stdlib/xeno/`
    and `~/core/hexa-bio/XENO.tape` and edited NOTHING in them. The substrate
    inventory is cited byte-equal (B-S95-7); §95 is a consumer of the xeno SSOT.
13. **taxonomy is a §95 construct** — the 5-bucket taxonomy is defined by §95,
    not inherited. Its value is that it is exhaustive + disjoint + deterministic
    (B-S95-1/3), so the classification is reproducible — not that it is the only
    possible carving of substrate-space.

---

## §9 — Battery + connection-point

`blue_falsifier_s95.py` — sidecar closed-form battery `B-S95-1..7` (sympy/Boolean):

- **B-S95-1 TAXONOMY-PARTITION-EXHAUSTIVE-DISJOINT** — the 5 buckets, over the
  full closed input space of `(L,E,H,kind,access)` tuples, partition it
  exhaustively and pairwise-disjointly (every tuple → exactly 1 bucket).
- **B-S95-2 LEARNING-VS-INFERENCE-CLOSED-BOOLEAN** — the L axis is a closed
  Boolean; `L=False ⇒ bucket ∈ {INFERENCE-ONLY-BLOCKED} ∪ {organoid/NO short-
  circuits}` — an inference-only compute-substrate is *always* blocked.
- **B-S95-3 CLASSIFY-DETERMINISTIC** — `classify` is a pure function: 3×
  bit-identical over the full input space, no RNG, no clock.
- **B-S95-4 §7-GOAL-LEGITIMACY-CLOSED-CONJUNCTION** — §7 legitimacy is a closed
  Boolean conjunction `¬generic_pretrain ∧ ¬generic_graft ∧ physics_is_source`;
  16-row truth table, only (F,F,T)→True.
- **B-S95-5 LOIHI-IS-SOLE-VIABLE** — over the 7 actual substrates, exactly one
  (`loihi`) classifies VIABLE-LONG-HORIZON (sympy cardinality == 1).
- **B-S95-6 ORGANOID-ETHICS-WALL-CLOSED** — `kind==organoid ∧ ethics_wall ⇒
  bucket==ETHICS-WALL`, and the ETHICS-WALL bucket implies design-OPEN (no
  capability verdict) — closed Boolean.
- **B-S95-7 SUBSTRATE-INVENTORY-BYTE-EQUAL (connection-point)** — the 7-substrate
  set in `result.json` is byte-equal to the real `hexa xeno status` inventory
  (`{akida, loihi3, northpole, finalspark, cortical_labs, ionq, qrng}`), and the
  central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` SHA is unchanged
  (0-line-diff mandate).
- **B-S95-NOTE** — empirical carve-out: *whether anima actually emerges on any
  substrate* (Loihi or otherwise) is an SGD/hardware OUTCOME, un-measurable at
  design-tier; the battery proves the *taxonomy* is exhaustive/disjoint/
  deterministic and the *classification* is closed-form — it does NOT prove any
  substrate yields emergence (B-D-NOTE / B-EMERGE-NOTE / B-S94-NOTE family, NOT
  counted 🔵, necessary-not-sufficient B-EMERGE-7).
