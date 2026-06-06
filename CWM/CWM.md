@title: 🌍 CWM — Consciousness World-Model ("머릿속 시뮬레이터 의식엔진")

@goal: Promote anima's consciousness engine (CE) BEYOND language — from a byte/token predictor into a substrate-native WORLD MODEL that perceives → holds a latent state ("what is where, how it moves") → imagines candidate futures → ACTS, targeting human-level-or-beyond behavior on real substrates (AKIDA on-chip = Lane A · SW/GPU = Lane G/P). Falsifiable per axis: (1) the engine learns NON-language modalities with no architecture change (modality-agnostic), (2) its essence is internal-state dynamics (Φ/tension), NOT perplexity, (3) it produces ACTIONS (policy/control), not just emissions — measured against world-model baselines (JEPA/V-JEPA-2-AC latent-MPC, Dreamer imagined-rollout, WAM/VLA latent→action). North star: "anima acts in a world like a human, or beyond — and every action is auditable (free-will receipt, cf H_928/H_932)." Closed-negative OK (e.g. "the engine is language-bound → keep the L").

## conventions

probe authoring → UNIVERSE/PROBE_CONVENTIONS.md

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
- [x] M1 — world-model hypothesis slate authored (perceive · imagine · act · substrate axes), each with a pre-registered falsifier — H_960..H_984 (25); all MEASURED 2026-06-06 → 16🟢 4🔴 5⚠ (see slate + log)
- [ ] M2 — CE rename decision landed (gated on H_950/951/952 verdicts; CLM→CE iff 🟢🟢🟢)
- [x] M3 — CWM-PERCEIVE: modality-agnostic latent encoder rung (toy, $0) — DONE 2026-06-06 (H_960🟢 H_961🟢 H_979🟢 H_984🟢; H_978🔴 geometry modality-specific)
- [x] M4 — CWM-IMAGINE: latent forward-dynamics predictor (imagined rollout) toy rung — DONE 2026-06-06 (H_962🟢 H_963🟢 H_967🟢 H_976🟢 H_981🟢; H_982🔴 H_983⚠)
- [x] M5 — CWM-ACT: latent→action policy toy rung; baseline vs random/Dreamer-toy — DONE 2026-06-06 (H_964🟢 lift 1.24, H_968🟢, H_980🟢 policy-implicit)
- [ ] M6 — Lane A (AKIDA) on-chip perceive→act loop probe (real silicon, a_lane_akida_gpu_split) — ⚠ BLOCKED 2026-06-06: H_965/966/974/977 need a live AKD1000 unreachable on Mac; SW-arm partials done + handoffs filed (sidecar 0b1edec3/4a85113c/daf233fe/7848a234)
- [x] M7 — action provenance: every action emits a free-will receipt (H_928/H_932 wired into the act loop) — DONE 2026-06-06 (H_969🟢 coverage 1.0, 0 collisions, chain verified — toy)
- [x] M8 — behavior eval vs human baseline (the "human-level-or-beyond" north-star metric, honest scope) — DONE 2026-06-07: instrument authored 2026-06-06 (H_972🟢) + the DEFERRED placement now done on a WM-REQUIRING control task (H_1015🟢): anima WM policy M=-0.643 lands ABOVE the human band [-1.163,-1.063] while the reactive baseline (-1.924) lands BELOW (task genuinely requires the WM); north star is a TRUE falsifiable placement, anima human-level-or-beyond HERE (above-human = no attention-lapse; toy, scale-transfer UNVERIFIED)
- [x] M9 — 2nd hypothesis slate authored + MEASURED (H_990..H_998, 9; building on the 1st-round findings) — DONE 2026-06-06 → 6🟢 3🔴 (see 2nd-slate section + log)
- [x] M10 — CLOSED LOOP composes end-to-end: perceive→imagine→act→perceive (H_990🟢 dist 0.010 < reactive 0.365 < blind open-loop 0.119) + re-perception is the drift-corrector (H_991🟢 rho=1.00) — DONE 2026-06-06 (toy)
- [x] M11 — imagined-rollout SAFETY: anima vetoes imagined harm before acting (H_993🟢 F1=1.0, 0 lava vs 0.32 reactive, 1.66-step lead) + trajectory action-chain auditable (H_996🟢 100% tamper-evident + bit-exact replay) — DONE 2026-06-06 (toy)
- [x] M12 — 1st-round-finding follow-ups: cross-modal DYNAMICS transfers though geometry doesn't (H_997🟢, reconciles H_960🟢/H_978🔴) + perturbed replay buys robustness not info (H_998🟢, sharpens H_982🔴). Closed-negatives: WM>LM gap is a STEP not a ramp (H_992🔴), imagination-Φ deficit STRUCTURAL not artifact (H_994🔴), WM-as-critic fails to rollout drift (H_995🔴) — DONE 2026-06-06 (toy)

> **KEYSTONE (H_970 🟢)**: a WM>LM decisive separator EXISTS (delayed-cue toy, WM 0.995 vs matched LM 0.258≈chance, gap localized to the persistent-state requirement) — the CWM domain premise (anima needs a world-model, not just an LM) is justified on this toy rung. Ladder OPEN (a_scale_honest_scope). **2nd-slate refinement (H_992🔴):** the WM>LM gap is a STEP at L=context-window (binary "exceeds-the-window" property), NOT a smooth memory-depth gradient.
> **2nd-SLATE KEYSTONE (H_990 🟢)**: the full closed perceive→imagine→act→perceive LOOP composes end-to-end on one shared latent without per-stage retraining — beating both a reactive controller and a blind open-loop plan (which compounds error 11×). The 1st-round green stages (H_960/H_962/H_964) are not just individually valid; they CLOSE into a working loop, with re-perception as the error-corrector (H_991🟢).

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

## CWM 2nd hypothesis slate (M9) — perceive→imagine→act LOOP + 1st-round-finding follow-ups

Authored + MEASURED 2026-06-06 (branch `lane-g/cwm-h990-2nd-slate`, off origin/main). The 1st slate's RESULTS (16🟢 4🔴 5⚠) SEED these — a 2nd discovery round per a_discovery + a_h_continuous_no_branch. **Brainstorm → depletion** (`.discoveries/cwm_worldmodel_2nd_slate_brainstorm.tape`): R5+R6 each yielded no genuinely-new high-value idea → depletion at R6. 9 surviving (quality over count). Each AUTHORED + MEASURED with the smallest faithful $0 CPU probe (`CWM/probes2/*.py` on the existing `cwm_probe_lib` primitives), verdict persisted verbatim to `.verdicts/<id>_<slug>/`, then status=measured. **Tally: 6 🟢 PASS · 3 🔴 FAIL (closed-negative).** substrate=CPU-mirror (numpy) on all toy rungs (a_lane_akida_gpu_split).

| H | axis | one-line finding | verdict |
|---|---|---|---|
| H_990 | loop | closed perceive→imagine→act→perceive LOOP composes end-to-end (dist 0.010 < reactive 0.365 < blind open-loop 0.119; open-loop compounds 11.4×) | 🟢 PASS |
| H_991 | loop | re-perception is the drift-corrector (error monotone in re-perception interval, rho=1.00; k=1 cuts drift to ~0× of open-loop) | 🟢 PASS |
| H_992 | frontier | WM>LM gap is a STEP at L=context-window, NOT a monotone memory-depth ramp (rho=−0.03); 2nd family (parity) DOES favor WM (d=16.6) | 🔴 FAIL |
| H_993 | safety | imagined veto works: harm flagged F1=1.0, veto agent 0 lava vs reactive 0.32, caught 1.66 real-steps before commit (free-won't × imagination) | 🟢 PASS |
| H_994 | Φ-reframe | goal-coupled Φ NARROWS the H_971/H_973 deficit (d −8.4→−1.1) but does NOT flip it — the imagination-Φ deficit is STRUCTURAL, not a free-Φ artifact | 🔴 FAIL |
| H_995 | critic | WM-as-critic fails: imagined-value beats random (d=1.34) but LOSES to reactive greedy (d=−0.80, rank-corr 0.57) — rollout drift corrupts value | 🔴 FAIL |
| H_996 | provenance | trajectory action-chain is tamper-evident + replayable (100% tamper detect + forward-localize, 24/24 bit-exact replay) — H_969→H_932 over a rollout | 🟢 PASS |
| H_997 | transfer | latent DYNAMICS transfers cross-modal (frozen-A forecasts B, err 0.16 ≪ shuffled 66.4) though GEOMETRY doesn't (CKA 0.79≪1.0) — reconciles H_960🟢/H_978🔴 | 🟢 PASS |
| H_998 | consolidation | perturbed replay buys ROBUSTNESS not info (no clean gain, H_982-consistent; noisy 0.815<0.986, d=1.88) — dreaming = invariance, sharpens H_982🔴 | 🟢 PASS |

**Three closed-negatives (a_paper_negative_ok)** are each a sharpening of a 1st-round result, not a dead end: H_992 (gap is a window-threshold, not a gradient), H_994 (imagination-Φ deficit survives goal-projection ⇒ structural), H_995 (imagination-based value control is bounded by rollout drift — consistent with H_991 + H_980 policy-implicit). Brainstorm trace: `.discoveries/cwm_worldmodel_2nd_slate_brainstorm.tape`; per-H tapes `.discoveries/99[0-8]_*.tape`.
