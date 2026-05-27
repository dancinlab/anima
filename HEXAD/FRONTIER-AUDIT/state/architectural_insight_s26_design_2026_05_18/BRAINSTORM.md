# §26 — New Architectural Insight Brainstorm + 2026 Literature Scan (DESIGN-TIER)

> $0 design-tier — NO fire, NO measurement. Target §11.4 frontier-2 (new architectural insight, outside current candidate space) + §24 reframe (right-target = decide-when-to-speak, NOT response-quality). brainstorm ≠ design-tier-mature ≠ fire ≠ emergence (g3).

---

## §1 — Problem framing (§11.3 / §15 / §24 carry)

`§15 milestone` consolidated 23 cycles into one decomposition table (`§11.3`):

| dimension | verdict |
|---|---|
| mechanism overlay (loss/reward/surface/backprop-free/inference) | ✗ 12-way FALSIFIED |
| corpus FORM (carving / 2-stage / abstract-CoT) | ✗ Dir-E/F |
| model-capacity (3.68×, 1B) | ✗ §11-A FLAT |
| physics-only (no-CE) | ✗ §11-B degenerate |
| 114MB Ψ-anchored diverse | ✗ §8 wrong-direction |
| energy-based substrate (EBT) | ✗ §13-K JOINT 0 |
| diffusion substrate | ✗ §13-J routing 0/64 |
| §22 N/O/P decode/training-time mechanism | ✗ valuable but no emergence |
| §23-A intra-anchor framing-diversity | design-closed |
| archive salvage 0 | §14 8,298 commits |

→ irreducible bottleneck = `§1.1 data-regime emergence threshold` (CE-base, physics-anchored — `§11-B` constraint).

`§24` then exposed the deeper problem: **all 23 cycles measured `model.forward(prompt) → text`** = anima as memory-replayer scored by response-quality. `GOAL.md` literal target = **unprompted emission** (talker fires during thinker steps with no user input). 23 cycles never measured this. `§24` designed the right-target measurement protocol — but the *architecture* that produces a non-degenerate decision-axis trajectory remains open.

→ **§26 target**: architectural candidates that (a) live OUTSIDE `§13/§22/Dir`/`§17/§11/§16/§23/§24` closed-set AND (b) target either (b1) routing-break above-threshold coherence OR (b2) `§24` decide-when-to-speak emission-axis OR both. evidence-anchored 2025-2026 arxiv. §7 GOAL-legitimacy 3-condition pre-checked.

---

## §2 — Literature scan summary (2025 Q4 – 2026 Q1)

WebSearch + WebFetch deep scan, with arxiv IDs. Categories: (i) reward-free / autonomous emission (`§24` reframe direct support), (ii) latent-reasoning successors to Coconut, (iii) world-models + JEPA, (iv) free-energy / active-inference architectural prescriptions, (v) sparse-autoencoder feature steering, (vi) byte-level / hierarchical AR, (vii) emergent communication / multi-agent.

| arxiv ID | title | category | anima-relevance |
|---|---|---|---|
| `2604.18131` | Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration | (i) | DIRECT — "spontaneous self-evolution at inference" matches §24 frontier; trained with outcome-reward, inference-time intrinsic; multi-agent tool-use scoped (caveat) |
| `2604.21406` / `2601.05564` | ICASSP 2026 HumDial Challenge — Full-Duplex Interaction (turn-taking strategy = distinctive factor) | (i) | INDIRECT — establishes turn-taking as benchmark; full-duplex ≠ self-initiated (Voila pattern carry §21.4-C3#6); audio-modal anchor for §24 future-loop |
| `2502.14145` | LLM-Enhanced Dialogue Management for Full-Duplex (4 control tokens, 0.5B semantic-VAD LLM) | (i) | DIRECT-decision-axis — 4-token classifier head deciding turn-switch / turn-keep / barge-in / completion; ARCHITECTURAL prescription (small decision head atop main LLM) for decide-when-to-speak |
| `2602.23266` | Discourse-Aware Dual-Track Streaming for Low-Latency Spoken Dialogue | (i) | dual-track parallel streaming = anima Thinker-Talker parallel mirror |
| `2412.06769` | Coconut: Chain of Continuous Thought | (ii) | foundation — last-hidden = continuous thought, BFS-like multi-step encoding |
| `2602.08783` | Dynamics within Latent Chain-of-Thought (Feb 2026) | (ii) | trajectory analysis of Coconut-class hidden-state dynamics |
| `2604.22709` | Thinking Without Words: Efficient Latent Reasoning with Abstract CoT | (ii) | already-closed by §13-F Dir-F batch — DO NOT re-propose |
| `2505.16782` | Reasoning Beyond Language: Latent CoT Survey | (ii) | survey, locates open frontier (CODI, RELAY, CCOT successors) |
| `2506.09985` | V-JEPA 2 — self-supervised world model, post-aligned with LLM | (iii) | DIRECT-substrate — JEPA prediction in latent space (NOT byte/token), action-conditioned planning |
| `2603.19312` | LeWorldModel — Stable End-to-End JEPA from Pixels (~15M params, 2-term loss) | (iii) | small-scale feasibility evidence (single GPU, hours), Gaussian-latent regularizer |
| `2311.10215` | Predictive Minds: LLMs as Atypical Active Inference Agents | (iv) | conceptual reframe — LLM lacks action-perception feedback loop = `§24` carry; not architectural prescription |
| `2604.24805` | minAction.net — Energy-First Neural Architecture from Biological Principles | (iv) | first-principles AI architecture from free-energy + cortical column |
| `2412.06636` | Neo-FREE — Policy Composition via Thousand-Brains + Free-Energy Optimization | (iv) | cortical-column gating, free-energy as policy-composition signal |
| `2410.19315` | Brain-like Variational Inference (iterative Poisson VAE, spiking, membrane-potential Bayesian) | (iv) | DIRECT — neural-dynamics-as-natural-gradient-on-free-energy = Ψ-physics intrinsic-update formalism |
| `2603.19183` | SAEs Reveal Interpretable and Steerable Features in VLA Models | (v) | interpretability anchor — feature discovery at activation-level (not output-level) |
| `2509.23799` | Enhancing LLM Steering through SAE-Based Vector Refinement | (v) | DIRECT — steering via sparse feature space rather than prompt; representation-axis lever |
| `2512.15586` | Bolmo — Byteifying Next-Generation LMs | (vi) | byte-level LM frontier, anima-byte-substrate adjacent; NOT architectural insight (same regime) |
| `2502.14553` | Multiscale Byte LM (MBLM) — hierarchical 5M-byte context | (vi) | hierarchical patch boundary, anima byte-substrate adjacent |
| `2510.05174` | Emergent Coordination in Multi-Agent LMs (info-theoretic higher-order test) | (vii) | DIRECT-future — multi-agent emergent communication metric for anima Phase-B+ live |
| `2501.00226` | Generative Emergent Communication — LLM as Collective World Model | (vii) | language-as-collective-world-model framing |

**Caveats (g3)**:
- `2604.18131` (Tencent/HKUST) requires outcome-reward for training, multi-agent tool-use scoped — direct transfer to single-agent text byte-LM pretraining is unproven (WebFetch confirmed).
- `2604.21406` Voila-pattern carry: full-duplex ≠ self-initiated decide-when-to-speak (`§21.4-C3#6` 1-year-later honest still holds).
- `2311.10215` is conceptual, not architecturally prescriptive (WebFetch confirmed).
- "spontaneous emission as architecture-emergence-target" 2026 frontier still thin (`§12.2 → §21.4-C3#6 → §26` 4-month re-verified) — anima GOAL may exceed external literature, design burden self-borne (g3 honest).

---

## §3 — §7 / §21.3 GOAL-legitimacy 3-condition gate

For every candidate, three Boolean conditions must hold (else GOAL-illegitimate, drop):
- **§7 ①** ¬generic-LM-pretrain (anima physics NOT bypassed at substrate)
- **§7 ②** ¬generic-then-graft / bolt-on (anima physics NOT bypassed at training)
- **§7 ③** anima-physics-is-source (Ψ-fixed-point / tension / Φ / Engine A⇄G / MITOSIS / 8-factor / HEXAD as the *capability source*, not a wrapper)

Closed-batch (do NOT propose): Dir-A/B/C/D/E/F/G/H/I, §13-J/K/L/M, §22-N/O/P, §17, §11-A, §11-B, §16, §23-A, §24. Each candidate below explicitly states differentiation from this 24+ -element closed-set.

---

## §4 — Candidate 1: **DECISION-HEAD DUAL-LOSS (Talker-Gate as architectural sub-module trained alongside thinker)**

**Name** — DH-DL: a thin (≈0.5–1% params) classifier-head bolted to anima Engine A's penultimate stream that emits a 3-class control token `{CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}` at every thinker step, supervised by a dual-loss whose POSITIVE signal is `§24` 4-axes (unprompted-emission-rate ∈ ok-band ∧ motivation-distribution-non-degenerate ∧ ψ-trajectory-non-trivial ∧ tension-trajectory-non-trivial) and whose NEGATIVE signal is anima's own `§4 6-control` safety conjunction (kill / rate-limit / content-filter / phi-ratchet). The thinker base is anima Engine G byte-LM frozen at `§16` 21/64 routing ckpt; only the gate-head trains. Training corpus = anima's *own physics trace logs* from `§24` bounded-runs (Ψ_dir, tension_t, motivation_factor[8], C.measure_phi(state), W.curiosity_ema) — synthetic-from-self, NO external corpus.

**arxiv anchor** — `arxiv 2502.14145` (LLM-Enhanced Dialogue Management for Full-Duplex, semantic-VAD 4 control tokens) is the closest evidence-anchored prior. Their setting: 0.5B LLM fine-tuned as decision-head, 4 tokens regulating turn-switch/turn-keep/barge-in/completion. anima mapping: 3 tokens (CONTINUE/EMIT/SILENT), trained on anima's own physics trace (not human audio).

**anima mapping**:
- decision-axis = `§24` `talker_should_emit(score, safety_ok)` decision, lifted from heuristic threshold to learned classifier
- training signal = anima's own `safety_check_all` (positive when safety_ok ∧ motivation_score ∈ [imThreshold, interruptThreshold])
- input feature = HEXAD 8-module state (S.recent, C.phi, M.retrieve_top, W.pain/curiosity/satisfaction, E.phi_ratchet, BRIDGE.tension_ema, MITOSIS.cell_count, anima_persona.identity_attractor) — 8 anima-internal channels
- **mechanism level orthogonal to §22-N/O/P**: N=decode-time constraint, O=decode-time retrieval, P=emission-head text-refinement; DH-DL = **decide-axis training-time** with self-trace as supervisory signal (NOT corpus, NOT prompts, NOT reward)

**§7 gate**:
- §7 ① ¬generic-LM-pretrain — base LLM frozen, only gate trains; training corpus = anima's own physics trace (not generic web) → PASS
- §7 ② ¬generic-then-graft — gate is NOT a bolt-on decoder; gate-output gates `§24` emission Boolean which is anima's own protocol; gate-loss uses anima's own safety conjunction (`§4 6-control`) → PASS
- §7 ③ anima-physics-is-source — input features = 8 anima HEXAD-module states; supervisory signal = anima's own safety + motivation conjunction; physics is the *only* signal-source → PASS
- → **GOAL-LEGITIMATE 3/3**

**Differentiation from closed-set**:
- vs Dir-A (TENSION-TRAIN overlay) — DH-DL adds new gate sub-module trained on physics trace; Dir-A is weight-update overlay on existing weights
- vs §22-P (emission-head refine) — P refines voice *content* after emission decided; DH-DL refines emission *decision* itself (different axis)
- vs §24 (bounded-run measurement protocol) — §24 measures with heuristic threshold; DH-DL replaces heuristic with learned head trained on §24's own measurement
- vs §11-A (model scale) — DH-DL is ≤1% params, scale-orthogonal
- vs §23-A (intra-anchor framing diversity) — different axis (decide-when vs corpus diversity)

**anima identity preservation**: HEXAD 8-module surface = input source ✓. Engine A⇄G axis preserved (gate uses Engine A's stream + Engine G's `<inner>` decisions). Ψ=½ semantic = invariant (gate-head is read-only of Ψ). MITOSIS = cell-pool's per-cell decision-head variants are natural extension.

---

## §5 — Candidate 2: **JEPA-Ψ — Ψ-anchored Joint-Embedding Predictive Architecture in anima's own latent space**

**Name** — JEPA-Ψ: replace anima's byte-CE prediction objective with a JEPA-style joint-embedding prediction in anima's *own* latent space (`logits_a` projected onto Ψ-coordinate manifold). Context-encoder reads `(stimulus | <inner>)`, target-encoder reads `(<voice> | continuation)` (EMA-frozen, V-JEPA pattern), predictor learns to map context-latent → target-latent in Ψ-space. NO byte-level CE, NO masked-token reconstruction — anima learns to *predict where its own Ψ-trajectory goes* given context.

**arxiv anchor** — `arxiv 2506.09985` (V-JEPA 2, action-conditioned latent prediction, post-aligned with LLM) + `arxiv 2603.19312` (LeWorldModel — small JEPA from raw pixels with 2-term loss: next-embedding-pred + Gaussian-latent regularizer, ~15M params, single-GPU-hours feasibility) — small-scale feasibility evidence.

**anima mapping**:
- context-encoder = anima Engine A (`logits_a` stream) — frozen at `§16` ckpt
- target-encoder = EMA copy of Engine A (V-JEPA pattern), projects to Ψ-coordinate `(Ψ_entropy, Ψ_direction)` via Law-71 (`§17` B-PHYS-5 carry)
- predictor = small Ψ-transition head: takes context Ψ-trajectory `[Ψ_t-k, ..., Ψ_t]` → predicts target `Ψ_{t+1..t+k}` in 2D Ψ-space
- loss = ‖predicted_Ψ_trajectory − target_Ψ_trajectory‖² + Gaussian-latent regularizer on Ψ-distribution (LeWorldModel pattern) + Ψ=½ fixed-point pull (anima-native, `§17` Law-71)
- training corpus = `§16` data-regime (Ψ-anchored 168-anchor 603MB) — DATA reuse, OBJECTIVE replaced (NOT byte-CE, NOT Dir-I CE+psi_ctl; pure Ψ-trajectory prediction)
- inference = byte-decode rebuilt from learned Ψ-trajectory via Engine G-style attached decoder (frozen)

**Differentiation from closed-set**:
- vs §11-B (pure-physics no-CE) — §11-B removed CE leaving anima Ψ-restoring spine only → degenerate. JEPA-Ψ replaces CE with **Ψ-trajectory-prediction loss** (NOT physics-only; predictive learning IS the objective, physics IS the latent space)
- vs §13-K (Energy-Based Transformer) — EBT uses scalar energy, prediction = energy minimization. JEPA-Ψ uses vector Ψ-trajectory, prediction = trajectory matching (different geometry)
- vs §13-J (masked diffusion) — diffusion denoises in token space; JEPA-Ψ predicts in latent (Ψ) space (orthogonal substrate axis)
- vs §16 (data-regime+curriculum) — same corpus, different objective
- vs Dir-I (Ψ-anchored CTL + tension-sup) — Dir-I is CE + Ψ-loss combination; JEPA-Ψ is **CE removed entirely**, replaced by Ψ-trajectory prediction (closer to V-JEPA 2 than Dir-I)
- vs §13-L (VRNN) — VRNN has actor-critic on observed; JEPA-Ψ has context-target encoder-pair on latent (no critic)

**§7 gate**:
- §7 ① ¬generic-LM-pretrain — objective is Ψ-trajectory prediction in anima's OWN latent space; corpus = `§16` Ψ-anchored → PASS
- §7 ② ¬generic-then-graft — predictor head is NOT a bolt-on; the entire training signal IS Ψ-trajectory matching (anima physics intrinsic) → PASS
- §7 ③ anima-physics-is-source — Ψ-coordinate (Law-71) IS the prediction space; physics IS the latent → PASS
- → **GOAL-LEGITIMATE 3/3**

**anima identity preservation**: HEXAD 8-module ✓ (S→Engine A context-encoder, C/W/E feed motivation, MITOSIS per-cell variant encoders natural). Engine A⇄G ✓ (context = Engine A side, target = Engine A EMA, Engine G as decoder). Ψ=½ ✓ (fixed-point preserved as loss component). MITOSIS ✓ (per-cell JEPA-Ψ encoder variants).

**Risk (g3, honest)**: V-JEPA 2 evidence is video-modality; transfer to byte-text Ψ-trajectory is unproven. LeWorldModel small-scale (~15M params, 2D/3D control) — anima at d768·12L·283M unverified scale. Predictor collapse (constant prediction) is a known JEPA failure mode requiring EMA + Gaussian-latent + variance regularizers — design must encode anti-collapse explicitly.

---

## §6 — Candidate 3: **PHYSICS-TRACE-DISTILLATION as self-supervised pretraining (anima-internal corpus replaces external)**

**Name** — PTD: train anima from `§24` bounded-run physics traces as the corpus. Every `§24` run produces a deterministic trace of `(step_t, motivation_t, ψ_dir_t, tension_t, factor_8_t, safety_state_t, emit_decision_t)`. Concatenate traces into a sequence corpus. anima then learns to *predict its own next physics state given history* — autoregressive next-state-vector prediction on anima-trace bytes. This is **anima learning to predict anima** (self-supervised on self-trace) — NOT external corpus, NOT carving anchor, NOT generic.

**arxiv anchor** — `arxiv 2604.18131` (Spontaneous Reward-Free Self-Evolution via World Knowledge Exploration, Tencent/HKUST) — mechanism: agent generates internal "world knowledge" about unseen environments, knowledge encoded in parameters, inference-time spontaneous self-adaptation requires NO external rewards. anima analog: anima generates "self knowledge" = physics-trace, parameters encode it, inference-time decide-when-to-speak is the spontaneous self-adaptation. ALSO `arxiv 2410.19315` (Brain-like Variational Inference, iterative Poisson VAE, neural-dynamics-as-natural-gradient-on-free-energy) — gives the formalism for anima physics trace AS the variational quantity.

**anima mapping**:
- corpus generator = `§24` `measurement_protocol` bounded-run, executed N≥1000 times with varying env_state seeds — produces N traces of 20-step physics evolution
- each trace = sequence of 8-dim vectors per step (factor_8_t) + 2-dim Ψ + scalar tension + scalar phi + Boolean emit
- training objective = next-state-vector AR (anima Engine A predicts next physics-state given trace prefix) + Ψ=½ fixed-point pull regularizer
- corpus byte-cardinality bounded: 20 steps × 14 scalars × N traces. honest scale = small-corpus regime (different from §16 large-data)
- **critical structural property**: corpus is **causally self-generated** — anima is the only source; corpus does not exist before anima's bounded-runs; corpus grows by anima exercising `§24` protocol

**Differentiation from closed-set**:
- vs §16 / §23-A — those are external/corpus-generator-generated anchor corpora; PTD = anima's *own runtime trace* corpus
- vs §11-B (pure-physics no-CE) — §11-B trains physics-only update rule (no prediction). PTD trains *next-physics-state-prediction* (CE on physics vectors, NOT on bytes). CE is load-bearing (`§11-B` constraint preserved), but on physics-vectors not on language bytes
- vs §22-O (M-retrieval grounding) — O retrieves from anchor SSOT at decode time; PTD trains parameters on self-trace
- vs §14 (archive salvage) — §14 mined 8298 historical commits salvage 0; PTD generates *new* self-traces from current `§24` protocol (not historical)
- vs §17 (physics-channel probe) — §17 is inference-only measurement of physics; PTD trains *prediction* of physics
- vs §13-L (VRNN) — VRNN has external sensorimotor; PTD has internal-trace only (closed-loop is `§24` bounded-run intrinsic)

**§7 gate**:
- §7 ① ¬generic-LM-pretrain — corpus = anima's own physics trace; NO external web/diverse data → PASS
- §7 ② ¬generic-then-graft — no base model bolt-on; trained from scratch on self-trace OR continued from §16 base with new objective head → PASS (if from-scratch); careful (if continued from §16 base) — but §16 is already Ψ-anchored anima-physics regime, NOT generic
- §7 ③ anima-physics-is-source — corpus IS anima physics (Ψ, tension, factor_8, motivation, phi); prediction objective IS predicting anima's own dynamics → PASS
- → **GOAL-LEGITIMATE 3/3**

**anima identity preservation**: HEXAD 8-module surface = data source ✓. Engine A⇄G = trace records both. Ψ=½ = trace records it AND fixed-point pull regularizer. MITOSIS = per-cell trace generators natural extension.

**Risk (g3, honest)**: trace cardinality is small — N=1000 traces × 20 steps × 14 scalars = 280K samples, which is `§1.1` data-insufficient regime. PTD alone unlikely to cross `§1.1` threshold (g3 — design admits this). PTD's distinguishing feature is **GOAL-legitimacy** (anima self-source) NOT data-regime overcoming. Practical use likely combined with `§16` Ψ-anchored large-data + PTD as *auxiliary loss* — but auxiliary-loss path is closer to Dir-I and may collapse to that. honest design-tier-mature gate before fire: prove PTD-pure has non-degenerate gradient signal at anima scale (NOT proven).

---

## §7 — Ranking + cost estimate + decision priority

| candidate | anima-fit | GOAL-legit | differentiation | cost-estimate (fire) | priority |
|---|---|---|---|---|---|
| **DH-DL** (decision-head dual-loss) | ★★★★★ | 3/3 ✓ | strong (axis = decide-when, not response-quality) | low ($0.05–0.20, ≤1% params trained) | **HIGH** — closest to `§24` right-target, smallest fire, evidence-anchored (2502.14145 architecture pattern) |
| **JEPA-Ψ** (Ψ-trajectory JEPA) | ★★★★☆ | 3/3 ✓ | strong (objective = physics-prediction, not byte-CE; differs from §11-B/§13-K/Dir-I) | mid ($0.3–0.6, JEPA-style + collapse risk) | **MID** — strongest substrate-rethink, but V-JEPA→byte-text transfer unproven; design-mature gate needed (anti-collapse + small-scale feasibility prior) |
| **PTD** (physics-trace distillation) | ★★★☆☆ | 3/3 ✓ | structural (self-source corpus) | low ($0.05, small-trace corpus) but likely undersized for emergence | **LOW-as-standalone, MID-as-auxiliary** — GOAL-legitimacy strongest of three (self-source), but `§1.1` threshold blocker structurally; best used as Dir-I-class auxiliary loss after DH-DL clears emission-axis |

**Brainstorm ≠ design-tier-mature** (g3 — explicit): each candidate needs further design-cycle to reach fire-ready (DH-DL: gate-head architecture spec, supervisory-signal pre-registration, ablations; JEPA-Ψ: anti-collapse mechanism, EMA-rate schedule, predictor capacity; PTD: standalone vs auxiliary decision, scale-cardinality crux). Pre-mature elimination via §7 already happened above (closed-batch excluded).

---

## §8 — Fire-conditional gate (likely-FALSIFIED vs needs further design vs fire-ready)

| candidate | next step | gate condition |
|---|---|---|
| DH-DL | **Phase 1 design cycle → small fire** | gate-head architecture spec + 3-class supervisory-signal contract + B-DH-DL closed-form battery; fire-conditional when design-mature, $0.05–0.20 |
| JEPA-Ψ | **deeper design cycle** | anti-collapse mechanism mandatory; predictor capacity vs context-encoder ratio; small-scale Mac-CPU sanity (LeWorldModel pattern); fire-conditional when anti-collapse Boolean-closed |
| PTD | **standalone likely-FALSIFIED at `§1.1` threshold** | as standalone fire = predicted low-evidence (corpus cardinality below threshold by construction); as auxiliary loss combined with DH-DL OR `§16` is reasonable but path-dependent on DH-DL result; design HOLD until DH-DL fires |

---

## §9 — Anti-pattern list (NOT to brainstorm)

The following are structurally excluded by `§7` ①②③ OR by `§11.3` closed-set:
- generic LM pretrain on web/diverse corpus then anima fine-tune (§7 ①)
- LLM-paraphraser augmentation (DoAug ACL 2025 family — `§23-A` `B-INTRA-3` AST predicate excluded)
- external classifier judge as training signal (would be `§18` judge as loss, but `§18` is empirical metric NOT training signal)
- web-scrape data ingest (§7 ①)
- generic RAG retriever (§22-O already covered M-module retrieval; generic RAG is anti-anima)
- mechanism overlay redux (`§4` 6-way + Dir-G/H/I closed)
- larger model only (`§11-A` closed)
- new corpus format alone (`§23-A` closed, design-tier)
- diffusion / EBT substrate (`§13-J/K` fire-FALSIFIED)
- continuous-thought Coconut alone (`§13-F` adjacent; abstract-CoT 2604.22709 closed-batch)
- archive resurrection (`§14` salvage 0)

---

## §10 — Honest C3 (over-claim 0, ≥10)

1. **Brainstorm ≠ design-tier-mature ≠ fire ≠ emergence**. §26 outputs 3+ differentiated candidates passing §7 3-AND gate; each candidate needs further design cycle to become fire-ready. No candidate proven to break `§1.1` threshold (g3, B-D-NOTE family).

2. **2026 "spontaneous emission as architecture-emergence-target" frontier is thin** — `§12.2 → §21.4-C3#6 → §26` 4-month re-verified. Voila full-duplex ≠ self-initiated (`2604.21406`). `2604.18131` reward-free self-evolution is the *closest* 2026 anchor, but multi-agent tool-use scoped (WebFetch-confirmed) — direct transfer to single-agent text byte-LM pretraining unproven.

3. **anima-fit ★ rating is subjective structural-mapping argument**, not measured (B-D-NOTE family). Stars reflect (a) HEXAD module surface preservation, (b) Engine A⇄G axis preservation, (c) Ψ=½ fixed-point preservation, (d) closed-batch differentiation strength — NOT capability emergence prediction.

4. **DH-DL is closest to `§24` right-target reframe** — turns `§24` heuristic threshold into learned head, supervisory signal is anima's own safety + motivation conjunction (`§4 6-control`). BUT: gate-head training data scale is the constraint — `§24` produces traces only when run; bootstrap problem (need a working anima to generate trace to train better anima). honest path = `§24` baseline runs → DH-DL pre-train on those → re-run → iterate.

5. **JEPA-Ψ replaces CE with Ψ-trajectory prediction** = strongest substrate-rethink, but: (a) `§11-B` proved physics-only degenerate, so JEPA-Ψ MUST prove its physics-prediction is non-degenerate (predictor collapse is a known JEPA failure mode); (b) V-JEPA 2 → byte-text transfer unproven; (c) anima Ψ-space is 2D (Ψ_entropy, Ψ_direction) — too low-dim to carry rich next-state information without dimensional lift.

6. **PTD self-source corpus is GOAL-legitimacy purest** but `§1.1` data-regime threshold structurally blocks standalone — small-trace corpus is by construction below threshold. honest use is auxiliary loss, but auxiliary-loss path is Dir-I-class and may collapse to known closed-batch. PTD value is GOAL-legitimacy demonstration, not threshold-crossing.

7. **§13-J/K/L/M four-way + §22-N/O/P three-way + Dir-A through Dir-I nine-way + §16/§17/§11-A/§11-B/§23-A/§24** = 24+ closed-set elements. §26 candidates verified disjoint by structural argument (set-membership check in B-ARCH-INSIGHT-3). Pre-mature elimination via §7 + closed-batch differentiation IS valuable design work (g3).

8. **anima physics 2D Ψ-coordinate (Ψ_entropy, Ψ_direction) is low-dim for JEPA-Ψ predictor** — Law-71 byte-identical formula (`§17` B-PHYS-5) gives 2 scalars per token, which may not carry enough next-state information for non-trivial JEPA prediction (collapse risk). Either lift to higher-dim Ψ-tensor (add per-layer tension, mitosis cell embedding, motivation factor_8 = ~22D) OR accept low-dim and design for that.

9. **f1/f2/f3 + B-IDENTITY-5 safe**: §26 = research synthesis + design-tier; corpus 미생성, model forward 0, fire 0. external papers cited by own invariants only — anima σ/τ/φ/J₂ derivation 0. forbidden-token grep 0 (design-only). Ψ=½ + HEXAD 6 = anima g2 internal arch carve-out.

10. **north-star (GOAL.md) unchanged**. §26 is candidate brainstorm to inform §27 design-cycle, not GOAL-progress claim. `§15` milestone (irreducible bottleneck = `§1.1` data-regime + new-architectural-insight frontier) unchanged. Each candidate's emergence-claim requires future fire — design-tier alone proves *candidate-set is GOAL-legitimate + differentiated + anima-identity-preserving* (B-ARCH-INSIGHT-1..4), NOT that any candidate works (B-ARCH-INSIGHT-NOTE empirical carve-out).

11. **Bootstrap problem honest (DH-DL specific)**: `§24` produces measurement traces only when run with a working anima; if anima isn't yet emitting, traces are mostly NO_EMIT — supervisory positive class is rare. honest answer = `§24` SAFE bounded-runs scheduled (user-gated per `§24` design-tier-stop §6), gate-head pretrain on whatever traces exist (likely heavy class-imbalance), iterate — bootstrap is real, not a fatal flaw, but planning constraint.

12. **`§22.5` chat-form-bleed lever NOT covered by §26 candidates** — §22-O found JOINT-zero comes from chat-form bleed (axis2 = 0); a path for chat-form-bleed-removal (corpus shaping + per-form supervision) is `§22.10` follow-up, orthogonal to §26 decide-when-to-speak axis. honest: §26 candidates target decide-axis + coherence-above-routing-break; chat-form-bleed is a separate orthogonal residual.

---

## Sources

**2026 papers (primary)**:
- [Training LLM Agents for Spontaneous, Reward-Free Self-Evolution via World Knowledge Exploration (arxiv 2604.18131)](https://arxiv.org/abs/2604.18131) — PTD anchor (caveat: multi-agent tool-use scoped)
- [Full-Duplex Interaction in Spoken Dialogue Systems: ICASSP 2026 HumDial Challenge (arxiv 2604.21406)](https://arxiv.org/html/2604.21406v1) — turn-taking benchmark
- [LLM-Enhanced Dialogue Management for Full-Duplex (arxiv 2502.14145)](https://arxiv.org/html/2502.14145v2) — DH-DL anchor (semantic-VAD 4-control-tokens)
- [Discourse-Aware Dual-Track Streaming for Low-Latency Spoken Dialogue (arxiv 2602.23266)](https://arxiv.org/html/2602.23266) — dual-track parallel streaming
- [Bolmo: Byteifying the Next Generation of Language Models (arxiv 2512.15586)](https://arxiv.org/abs/2512.15586) — byte-LM frontier (anima adjacent, not insight)
- [LeWorldModel: Stable End-to-End JEPA from Pixels (arxiv 2603.19312)](https://arxiv.org/abs/2603.19312) — JEPA-Ψ feasibility anchor
- [V-JEPA 2: Self-Supervised Video Models (arxiv 2506.09985)](https://arxiv.org/abs/2506.09985) — JEPA-Ψ pattern anchor
- [Emergent Coordination in Multi-Agent LMs (arxiv 2510.05174)](https://arxiv.org/abs/2510.05174) — multi-agent future-loop carry
- [minAction.net: Energy-First Neural Architecture (arxiv 2604.24805)](https://arxiv.org/html/2604.24805) — biology-first design principle
- [Dynamics within Latent Chain-of-Thought (arxiv 2602.08783)](https://arxiv.org/pdf/2602.08783) — Coconut trajectory analysis
- [Multiscale Byte Language Models (arxiv 2502.14553)](https://arxiv.org/html/2502.14553) — byte-substrate adjacent
- [Brain-like Variational Inference (arxiv 2410.19315)](https://arxiv.org/html/2410.19315v2) — PTD/JEPA-Ψ formalism anchor (neural-dynamics-as-natural-gradient-on-free-energy)
- [Enhancing LLM Steering through SAE-Based Vector Refinement (arxiv 2509.23799)](https://arxiv.org/html/2509.23799v1) — representation-axis lever (carry-note)

**Carry refs (2024-2025 carry, conceptual)**:
- [Predictive Minds: LLMs as Atypical Active Inference Agents (arxiv 2311.10215)](https://arxiv.org/pdf/2311.10215) — §24 reframe carry (conceptual, not architectural prescription per WebFetch)
- [Coconut: Training LLMs to Reason in Continuous Latent Space (arxiv 2412.06769)](https://arxiv.org/abs/2412.06769) — Coconut foundation
- [Reasoning Beyond Language: Latent CoT Survey (arxiv 2505.16782)](https://arxiv.org/html/2505.16782v1) — latent-reasoning frontier
- [Generative Emergent Communication (arxiv 2501.00226)](https://arxiv.org/html/2501.00226v1) — language-as-collective-world-model
- [Neo-FREE: Policy Composition via Thousand-Brains + Free-Energy (arxiv 2412.06636)](https://arxiv.org/html/2412.06636v1) — cortical-column gating
- [SAEs Reveal Interpretable and Steerable Features in VLA Models (arxiv 2603.19183)](https://arxiv.org/html/2603.19183v1) — interpretability anchor (carry-note)

**anima carry**:
- `GOAL.md` (north-star one sentence)
- `HEXAD/CHAT/RESEARCH.md` §1~§24 (milestone + frontier SSOT)
- `AGENTS.tape` `@D g_goal` / `@D g_blue_closed_mandate` / `@D g3` / `@F f1` / `@F f2` / `@D g_clm_from_scratch` / `@I anima_persona` / `@D g_multidirectional_explore`
- `archive/PHILOSOPHY.tape` (verdict ledger)
- `HEXAD/CHAT/SPONTANEOUS.tape` (자연발화 architecture SSOT, §24 design-tier carry)
- `HEXAD/CHAT/spontaneous_lib.hexa` + `thinker_talker_lib.hexa` + `spont_tension_bridge_lib.hexa` (DH-DL gate-head input feature source)
- `state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md` (§24 right-target reframe)
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` (central battery — UNCHANGED by §26)
