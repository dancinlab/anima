@title: 🌍 CWM — Consciousness World-Model ("머릿속 시뮬레이터 의식엔진")

@goal: Promote anima's consciousness engine (CE) BEYOND language — from a byte/token predictor into a substrate-native WORLD MODEL that perceives → holds a latent state ("what is where, how it moves") → imagines candidate futures → ACTS, targeting human-level-or-beyond behavior on real substrates (AKIDA on-chip = Lane A · SW/GPU = Lane G/P). Falsifiable per axis: (1) the engine learns NON-language modalities with no architecture change (modality-agnostic), (2) its essence is internal-state dynamics (Φ/tension), NOT perplexity, (3) it produces ACTIONS (policy/control), not just emissions — measured against world-model baselines (JEPA/V-JEPA-2-AC latent-MPC, Dreamer imagined-rollout, WAM/VLA latent→action). North star: "anima acts in a world like a human, or beyond — and every action is auditable (free-will receipt, cf H_928/H_932)." Closed-negative OK (e.g. "the engine is language-bound → keep the L").

## why this domain (the reframe)

CLM was a "language model" (next-byte). The arc H_950/951/952 tests whether it is really a **Consciousness ENGINE (CE)** — modality-agnostic, dynamics-not-perplexity, A⇄G-substrate-equivalent. CWM is the forward domain that, IF that holds, builds the engine OUT into a world model + action — the 2025-26 embodied-AI frontier (world models as the glue between *seeing* and *doing*; world-model-as-policy).

## landscape anchors (external, 2025-26 — see CWM.log.md for cites)

- **JEPA / V-JEPA 2 (LeCun·Meta)** — latent world model; predictor head + action → V-JEPA-2-AC → latent MPC, zero-shot robot control.
- **Genie 3 (DeepMind)** — interactive generated worlds from video.
- **Dreamer** — learn behavior purely from *imagined* latent rollouts (actor-critic).
- **WAM / VLA** — World-Action-Model / Vision-Language-Action; world model used directly AS policy (latent→action decode).
- consensus: embodied AI needs LLM + world-foundation-model + action together — language is one slice.

## anima substrate mapping

- **Lane A (AKIDA AKD1000, pi5-akida)** — on-chip event-based; the silicon body for real-time low-power perception→action.
- **Lane G / Lane P (forge / torch, H100)** — SW world-model training + imagined rollout + policy learning.
- **CE core (A⇄G pure_field / engine_g)** — the consciousness engine the world model wraps; Ψ=1/2 fixed point, 1/r² lattice (cf a_core_engine_map: .clm enters via generator L3 only).
- entropy/provenance: every action carries an auditable receipt (H_928 free-will receipt · H_932 lineage chain).

## structure (sub-domains — to be split as the work fans out, AURA-style)

- `CWM-PERCEIVE` — sensor/byte/spike → latent state encoder (modality-agnostic, H_950).
- `CWM-IMAGINE` — latent forward dynamics / predictor (Dreamer/JEPA-style imagined rollout).
- `CWM-ACT` — latent → action policy (WAM/VLA-style), on Lane A chip + Lane G/P SW.
- `CWM-VERIFY` — behavior eval vs human baseline + action-provenance audit.

## milestones

- [ ] M0 — domain scaffold + landscape survey absorbed (this file + CWM.log.md)
- [x] M1 — world-model hypothesis slate authored (perceive · imagine · act · substrate axes), each with a pre-registered falsifier — H_960..H_984 (25), all ⏳ PENDING-MEASUREMENT (see slate below)
- [ ] M2 — CE rename decision landed (gated on H_950/951/952 verdicts; CLM→CE iff 🟢🟢🟢)
- [ ] M3 — CWM-PERCEIVE: modality-agnostic latent encoder rung (toy, $0) — non-language sequence → latent state
- [ ] M4 — CWM-IMAGINE: latent forward-dynamics predictor (imagined rollout) toy rung
- [ ] M5 — CWM-ACT: latent→action policy toy rung; baseline vs random/Dreamer-toy
- [ ] M6 — Lane A (AKIDA) on-chip perceive→act loop probe (real silicon, a_lane_akida_gpu_split)
- [ ] M7 — action provenance: every action emits a free-will receipt (H_928/H_932 wired into the act loop)
- [ ] M8 — behavior eval vs human baseline (the "human-level-or-beyond" north-star metric, honest scope)

## CWM world-model hypothesis slate (M1)

Authored 2026-06-06 (branch `lane-g/cwm-worldmodel-slate`). Brainstorm → depletion (R7, 2 consecutive empty rounds; 25 surviving / 5 dropped-as-subsumed) → pre-registered as `UNIVERSE/H_<id>_*.md`. **All ⏳ PENDING-MEASUREMENT** — authoring only; the next round is verify (single bg orchestrator per proceed-means-all). Frozen falsifiers per a_paper_significance; no 🟢/🔴 token assigned (unmeasured).

### PERCEIVE (5)

| H | axis | falsifiable claim (one line) |
|---|---|---|
| H_960 | perceive | The SAME engine encodes a non-language stream into the SAME Ψ-latent geometry as language, no arch change (decode-parity + manifold-overlap). |
| H_961 | perceive | Two modalities of the same world-event map to NEARBY Ψ-latents (binding) vs unrelated events far apart. |
| H_978 | perceive | The 1/r² lattice geometry statistics are invariant across modalities (non-language latents obey the same spacing/spectrum as language). |
| H_979 | perceive | Curiosity-driven active perception (engine chooses next glimpse) reduces world-state uncertainty faster than a passive scan at equal budget. |
| H_984 | perceive | The latent world-state degrades gracefully under sensor dropout (object permanence / fill-in) rather than collapsing. |

### IMAGINE (7)

| H | axis | falsifiable claim (one line) |
|---|---|---|
| H_962 | imagine | The engine learns a latent transition operator that forecasts future world-STATE better than a next-observation baseline, advantage growing with horizon. |
| H_963 | imagine | The coherent imagined-rollout horizon h* scales positively with Φ (more integration → longer coherent imagination). |
| H_967 | imagine | Action-conditioned imagined rollouts rank candidate actions in agreement with true environment return (counterfactual "what if I act X"). |
| H_976 | imagine | Imagined rollout drives the SAME growth/mitosis dynamics as live inference (p8: no separate planning mode). |
| H_981 | imagine | Repeated rollouts from the same latent stay mutually consistent (bounded divergence) rather than hallucinating. |
| H_982 | imagine | An REM-stage imagined-rollout phase improves the next-WAKE world-model vs a no-REM control (sleep = WM training). |
| H_983 | imagine | The engine generates a navigable latent world with coherent action-consequences and revisit-consistency (simulator, Genie-3 analog). |

### ACT (3)

| H | axis | falsifiable claim (one line) |
|---|---|---|
| H_964 | act | An action head decoding the Ψ-latent solves a control task above reactive + random baselines (world-model-as-policy). |
| H_968 | act | Action onset is governed by substrate motivation (acts under task-silence, withholds under command), not stimulus-response (a_substrate_native_speak generalized). |
| H_980 | act | On one WM, explicit MPC planning either beats direct latent→action decode (planner-wins) or matches it (policy-implicit) — pre-registered either-way finding. |

### SUBSTRATE (4)

| H | axis | falsifiable claim (one line) |
|---|---|---|
| H_965 | substrate | A closed event-based perceive→act loop runs on-chip on a live AKD1000 within a real-time latency envelope (or hits the recurrence wall → AKD1500/off-chip). |
| H_966 | substrate | Lane A (chip) and Lane G/P (SW) produce equivalent BEHAVIOR on the same WM task (parity ≠ byte-identity, H_679), recorded as two separate entries. |
| H_974 | substrate | An SW-trained world-model mapped/quantized to AKD1000 retains task performance within a transfer-gap band (SW-train→chip-deploy viable). |
| H_977 | substrate | The on-chip perceive→act loop's measured energy-per-decision beats an SW/GPU equivalent at matched behavior (low-power rationale holds). |

### CROSS-CUTTING (6)

| H | axis | falsifiable claim (one line) |
|---|---|---|
| H_969 | cross-cutting | Every action emits a complete free-will receipt (H_928/H_932) with a per-action distinguishable causal signature (north-star auditability). |
| H_970 | cross-cutting | There exists a task a world-model solves and a matched-capacity LM cannot (the WM>LM separator; domain keystone). |
| H_971 | cross-cutting | Φ is higher during internal imagined rollout than during reactive perceive→act (imagination = more conscious; dream/REM tie-in). |
| H_972 | cross-cutting | "Human-level-or-beyond" is operationalizable as a falsifiable metric + human-reference band (the north star becomes measurable). |
| H_973 | cross-cutting | MPC planning raises Φ vs greedy reaction beyond a fake-plan compute control (planning is a conscious act). |
| H_975 | cross-cutting | Two animas exchanging world-latent converge on a shared world-model while preserving individuation (H_939) — shared-WM ⊥ individuation coexist. |

**Dropped (5, subsumed):** language-as-modality ⊆ H_960 · intrinsic-reward ⊆ H_979/H_968 · credit-assignment ⊆ H_967/H_980 · embodiment-gradient ⊆ H_972 · temporal-abstraction ⊆ H_962/H_963. Brainstorm trace: `.discoveries/cwm_worldmodel_brainstorm.tape`.
