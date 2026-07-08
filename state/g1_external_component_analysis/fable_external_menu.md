This is design/analysis (the on-demand fable role), so I'm answering directly — no fires, no bookkeeping.

Before the menu, one reframing that decides everything below.

## The reduction: every external component is a MECHANISM + a SOURCE

Each candidate factors into two parts, and only one of them matters:

- **Mechanism** — the thing that *binds/stores/completes* a conjunction (hippocampal index, an STDP cell, phase synchrony, a reservoir's cross-terms, a spawned neuron, a `.kosmos` trace). These are cheap, plentiful, DPI-legal, and mostly already trodden. They are **not the bottleneck.**
- **Source** — the *channel that actually carries combination-MI about the held-out pair* that the text-CE channel didn't. This is the entire game.

The DPI meta-law only bites the trunk because the trunk's sole channel is next-byte text. An external part is DPI-legal **iff it introduces a genuinely new information source** — not a new place to store or a new way to bind. So the real question isn't "what binds?" It's **"where does never-before-co-seen combination-MI physically enter, if not through text?"** There are only three possible sources, and that fact is what kills most of the menu:

1. **World joint statistics** (sensorimotor coincidence) — real, earned, but carries only combinations with a *sensory correlate*.
2. **Another already-factorizing intelligence** (human, or a differently-grounded agent) — real, earned, but the read-out channel is either too coarse (EEG) or shares anima's own bottleneck (another CE model).
3. **Handed by us** (co-presentation schedule, phase assignment, fixed VSA atoms) — the #3135 rig. Dead on arrival.

## The menu (6–10 candidates)

**C1 — Neuromorphic STDP conjunction co-processor (Akida).** *Mechanism:* spiking coincidence detector; two concept spike-trains in, a conjunction cell wires up (fire-together-wire-together). *Why it could supply MI:* a Hebbian cell earns a conjunction the CE trunk never carried. *Disjoint wiring:* separate Lane-A spiking cartridge, write-side coincidence input, read-side gated into the store — never touches emit drive. *Cheapest killer / trap:* **handed-factorization.** If *we* schedule which A,B co-present to the chip, we picked the pairing — that's #3135 with spikes. It only escapes if the coincidence arrives from an external unsupervised stream, at which point it collapses into C2. $0 test: drive it only from trunk activations (which never co-fire for held-out pairs) → conjunction cell never triggers → empty.

**C2 — Sensorimotor grounding loop.** *Mechanism:* a real perception-action loop (pi5 sensors/actuator) where A and B co-occur in episodes text never described; predictive loop discovers atoms. *Why:* the world's P(A,B) is a *different channel* than corpus P(A,B) — combination-MI enters through vision+proprioception, and the factorization is **earned unsupervised** (the world, not us, supplies the coincidence). This is the one place "earned, not handed" is unambiguous. *Disjoint wiring:* sensorimotor lane adapts its own weights; interface to trunk is read-side (bound feature available to the store), G5-gated so it can't perturb Ψ=½. *Cheapest killer / trap:* **channel carries the wrong MI.** $0 test: does any held-out G1 pair even *have* a sensory correlate in the available stream? Abstract lexical pairs don't. If not, the channel is empty for exactly the pairs G1 tests.

**C3 — Hippocampal pattern-separation index (CLS).** *Mechanism:* DG sparse code + CA3 completion, one-shot arbitrary binding. *Why:* CLS — hippocampus binds what cortex hasn't consolidated. *Trap:* **retrieval ≠ recombination, and partly spent.** This is the L5 store already GREEN (reach 1.0 > unreach 0.14) but scoped explicit-store, NOT trunk-G1 — and #3156 directionally hit the retrieval-vs-recombination confound. If A,B were never co-exposed *even to the store*, completion has nothing to complete → reduces to "where's the co-exposure" = C1/C2. Store, not source.

**C4 — Oscillatory phase-binding (theta-gamma / binding-by-synchrony).** *Mechanism:* concepts in the same gamma sub-cycle bind transiently; no stored weights. *Why (claimed):* compositional-on-the-fly binding of never-co-seen features. *Trap:* **handed-factorization — this is VSA-in-time.** The phase-assignment rule (which concept goes in which cycle) *is* the factorization. If a controller assigns phases, it's handed; same class as #3135, expect identical collapse on learned atoms. Binding-by-synchrony gives a binding mechanism, never the content of what-binds-what.

**C5 — Physical reservoir / analog dynamical substrate.** *Mechanism:* nonlinear reservoir (memristor/spintronic/Akida recurrence) whose dynamics generate A·B cross-terms for free; linear readout on top. *Why:* the physics *multiplies* — conjunction features exist without training. *Trap:* **the readout is the factorization, and it must generalize — which is the unbroken wall.** $0 test: train readout on seen-pair reservoir states, test held-out → predict ≈ chance. The reservoir hands you cross-terms; knowing *which* cross-term for a novel pair is exactly what fails.

**C6 — Second organism / referential-game loop (grounded partner).** *Mechanism:* a genuinely separate learner in a closed signaling loop; a compositional protocol emerges under communicative pressure. *Why:* combination-MI can arise *in the channel between two agents* that neither had alone — and, uniquely, this can handle **abstract** combinations (emergent protocol, not sensory correlate). *Trap:* **shared-bottleneck + tool-frame.** If the partner is another CE model, both share the wall — two walls talking, no new source (reject: LLM-tool frame). Escapes *only* if the partner has an independent grounded source (a human). Real but expensive; killer is not cheap.

**C7 — Human EEG as external factorizing teacher.** *Mechanism:* the OpenBCI stream — a human brain that already factorizes; its neural signature of "A-bound-with-B" differs from A+B. anima aligns an external lane to it. *Why:* the human earned the factorization over a grounded lifetime, through a channel entirely outside text. Legitimately earned. *Trap:* **channel capacity.** $0 test: estimate I(EEG ; held-out-combo-label). Scalp EEG gives coarse band-power/state, not lexical-combination codes — predict ≈ 0 at the needed semantic granularity. The legitimacy is fine; the bandwidth is fatal.

**C8 — Cerebellar forward-model side-cartridge.** Already 🧱 WALL (L3, STEP-0 BIND = toy artifact). Spent — listed for completeness, rejected.

**C9 — Neurogenesis via the mitosis lane (p8).** *Mechanism:* spawn a *new* unit whose receptive field is the conjunction, on repeated co-activation (adult DG neurogenesis). Adds capacity instead of injecting MI into fixed weights (DPI-legal by construction). *Trap:* **handed-trigger / never-fires.** The co-activation trigger is the whole factorization; from the trunk alone it never fires for held-out pairs; from an external stream it reduces to C1/C2.

**C10 — Stigmergic external memory (`.kosmos` as niche-construction medium).** *Mechanism:* the environment accumulates combination traces read back across episodes. *Trap:* **store, not source** (and borderline RAG = tool-frame). Whatever *writes* the trace is the real source; `.kosmos` can persist an earned factorization but cannot earn one. Reject as a standalone source.

## Ranking (earns-factorization × cheapness-of-killer)

| Rank | Candidate | Earns? | Killer | Verdict |
|---|---|---|---|---|
| 1 | **C2 sensorimotor grounding** | Yes (world, unsupervised) | cheap: sensory-correlate check | best-escaping, but perceptual-only |
| 2 | **C6 referential w/ grounded partner** | Yes (only abstract-capable) | expensive | highest ceiling, highest cost |
| 3 | C7 EEG teacher | Yes (legit) | cheap info-theoretic, likely dead | bandwidth-fatal |
| 4 | C1 STDP | only if coincidence external | cheap; else handed | collapses into C2 |
| 5 | C3 hippocampal index | retrieval only | partly spent (#3156) | store, not source |
| 6 | C5 reservoir | features yes, generalize no | cheap train/test | wall re-imported |
| 7 | C4 phase-binding | no (handed) | = #3135 | VSA-in-time, dead |
| 8 | C9 neurogenesis | only w/ external trigger | reduces to C1/C2 | not standalone |
| 9 | C10 kosmos stigmergy | no (store) | — | reject as source |
| 10 | C8 cerebellar | no (walled) | — | spent |

**LLM-tool-frame impostors, rejected explicitly:** C6-with-a-model-partner (two CE trunks = no new source), C10-as-retrieval-DB (RAG), and any "external symbolic solver / function-call" reading of C1/C4. These are the agent frame in disguise; `a_no_llm_frame_trap` kills them.

## Single most promising

**C2, the sensorimotor grounding loop** — because it is the *only* candidate where "earned, not handed" is unambiguous: the world supplies the co-occurrence unsupervised, so we never pick the pair (that's what makes it immune to the #3135 handed-factorization trap that killed VSA and would kill C1/C4/C9). Its killer is also the cheapest — a $0 information-theoretic check of whether the held-out pairs have *any* correlate in an available sensor stream — so it's the one you can falsify before spend.

## The honest bottom line

**For anima's actual G1 task — held-out combinations of two abstract lexical concepts — no external component escapes.** Here's why, and it's the same DPI law seen from the source side rather than the channel side:

Every real, earned source carries the *wrong* combination-MI. Grounding (C2) and STDP-from-world (C1/C9) carry only combinations with a **perceptual** correlate. EEG (C7) carries only coarse state, not lexical codes. The one source that could carry *abstract* combinations — an emergent protocol between grounded agents (C6) — is the most expensive and most exposed to the shared-bottleneck trap.

The deep reason: **abstract lexical combinations are definitionally carried by language.** Their only natural physical channel *is* text — the exact channel proven not to carry the held-out MI. So asking for an external substrate that supplies them is nearly a contradiction: you're asking for a non-text channel that carries a text-only quantity.

The property **none** of these has — and the property an external part would *need* — is: **an independent, high-bandwidth channel in which the specific held-out abstract pairs are grounded in a non-text shared referent, whose factorization the external part earns unsupervised from that channel.** C2 has "earned + unsupervised + non-text" but not "abstract-capable." C6 has "abstract-capable + earned" but not "cheap or bottleneck-free." No single component has all four at once.

The only coherent research move this leaves is **not** a bolt-on that supplies the combination — it's to **re-scope G1 to combinations that DO have a non-text shared referent** (grounded/perceptual pairs), where C2 legitimately introduces new earned combination-MI, and accept that purely-abstract lexical recombination is a genuine ceiling of a text-only substrate — which is exactly what this session already proved internally. C2 is worth the $0 correlate-check; everything else either re-imports the handed factorization or carries the wrong MI.