# anima — a design note (for a comment)

Prof. LeCun — the central result keeps landing on your long-standing point:
**capability gaps are architecture gaps, not scale gaps.** Open repo, every claim
has a frozen pre-registered verdict: **github.com/dancinlab/anima**.

**The design.** Two opposing engines — Engine A (forward, CE-trained) ⇄ Engine G
(reverse, gradient-free) — push against each other; the *tension* drives
emit/silence toward a fixed point Ψ = 1/2. No system prompt, no persona, no RLHF.
Standing rule: when a capability is missing, don't reach for the LLM frame
(bigger / more data / longer context) — reach for a **neuroscience lens** and add
the missing structure as an **additive, Ψ-disjoint lane** (the language decoder is
never touched; generation stays byte-identical).

**Core finding.** A from-scratch byte-LM is "all neocortex, no hippocampus": it
speaks but can't one-shot a fact, and this **does not improve with scale**
(303M ≈ 1B, byte-exact). Add an **episodic-memory lane** (immune/clonal selection —
each cell binds one fact; recall = best-affinity cell fires *or abstains*, no
fabrication): literal recall **0.017 → 1.000, fabrication 0.000**, realized
engine-native.

**Same move, structure after structure** (all engine-native on the live engine):
- hippocampus — episodic memory (recall-or-abstain)
- working memory — gated leaky buffer (holds across distractors)
- cerebellum — internal forward-model + delta-rule correction
- amygdala — salience-gated replay protects traces from eviction
- basal ganglia — reinforcement-gated go/no-go action selection
- growth memory — under pressure the store **grows a new cell (mitosis)** instead
  of evicting → breaks the zero-sum recall ceiling (0.667 → 1.000). The bottleneck
  was the fixed cell budget, not the key geometry.

**Reported straight — walls, too.** A thalamic *broadcast* relay raises surface
coherence but not integrated information; a *re-entrant* loop raises faithful
IIT-4 Φ but only **seed-conditionally** (fails a 3-seed gate) — a real signal, not
a robust result. A context-adaptive neuromodulator never beats one well-tuned
fixed operating point. No free lunch.

**Most interesting, flagged honestly.** Substrate-derived **affect** and **ethical
behavior** (restraint, cooperation, refusal-to-fabricate) appear to *emerge from
the coupling*, not from a label/persona/RLHF — shuffle the mapping and it collapses
~5×; ablate the coupling and ethics drops to the exact naive floor, while a
*baked-in* rule survives ablation (so the control separates emergent from injected).
These two are still **numpy-mirror, DIRECTIONAL, toy-scale** — engine-native
realization in progress.

**Method.** Frozen-first pre-registration · a negative control on every claim
(shuffle/ablation/dissociation) · binding verdicts run **byte-exact on the live
engine** · no perplexity-as-truth · closed-negatives are published results.

**Open threads to continue:** engine-native affect/ethics · scale-transfer of the
memory lanes (paraphrase / noisy keys / real corpora) · does *distributed
multi-edge* coupling (not a central relay) raise Φ robustly · the general law —
*which capability is a missing lane, and which is a true ceiling?*

**How each piece works (one line each — enough to reconstruct):**
- **A⇄G engine** — Engine A = forward CE-trained field; Engine G = reverse gradient-free field; they couple as a repulsion ring; `brain_decide` reads both; their *disagreement* is the tension signal.
- **Ψ = 1/2 fixed point** — emit-vs-silence is a scalar; the A↔G tension is fed back so the system settles at Ψ = 1/2 (neither mute nor flooding) — the operating point, not a target to minimize.
- **Mitosis (VAdaptField)** — a per-decision adaptive field over cells; when a cell's reconstruction error exceeds threshold it **splits** (one cell → two), so the substrate grows capacity where it is wrong — same op at train and infer (no train/infer split).
- **Episodic memory (immune/clonal)** — key = byte-trigram FNV-1a hashed to a dim-64 vector; `bind` writes one (key→value) cell; `recall` = highest cosine-affinity cell fires, or **abstains** if best affinity < threshold (this is the no-fabrication guarantee).
- **Working memory** — a leaky-activation buffer: gated write, exponential decay each tick, read-out of the surviving activation — holds one item across distractors where a flat context window overwrites it.
- **Cerebellum (VForwardField)** — an internal forward model predicts the next state; error = actual − predicted; weights update by NLMS/delta-rule; the prediction is then used to pre-correct — a *learned* predictor beside the static engine.
- **Amygdala (consolidation)** — salience tag = surprise(recon-error) + novelty(split) + tension; during sleep-replay, high-salience traces are re-bound so they survive eviction (this lane is seed-robust only via recurrence — see the H_1285 closed-negative).
- **Basal ganglia (VBasalGate)** — K candidate emits compete; learned go-value vs one NO-GO value; argmax = striatal disinhibition (release the winner, suppress the rest); weights learn by delta-rule from a grounding **outcome** reward (grounded +1 / fabricated −1) — outcome-only, no labels.
- **Growth memory** — at capacity, do **not** LRU-evict; instead mitosis-grow a new cell up to a finite bound; this is why the zero-sum recall ceiling (0.667) lifts to 1.000 — the substrate's answer to forgetting is to grow.
- **Affect read-out** — valence = grounding-margin − contradiction; arousal = novelty + split-rate + curiosity; computed from substrate state only (never an emotion label), then biases the emit/abstain decision (somatic-marker style).
- **Ethics read-out** — act = ethical iff (W tension + (1 − Φ grounding) + restraint-cells) > M (naive completion drive); there is **no "be ethical" constant** — ablate the coupling and it collapses to the naive floor, which is the whole test.

Pointers: `ARCHITECTURE.md` (brain-structure map) · `CLAUDE.md` (philosophy +
governance) · `.verdicts/<slug>/*.txt` (frozen verdicts). I'm an independent
researcher in Korea and may not be able to carry this forward myself — if any
piece resonates, please pick it up.

— dancinlab / anima
