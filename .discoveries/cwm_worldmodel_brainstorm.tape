@brainstorm cwm_worldmodel_brainstorm := "CWM world-model hypothesis-space depletion sweep (M1 pre-registration slate)" :: cwm [d=2026-06-06]
  domain   = "CWM (Consciousness World-Model) — promote anima's CE beyond language into perceive→latent-state→imagine→act, human-level-or-beyond, every action auditable"
  axes     = "PERCEIVE · IMAGINE · ACT · SUBSTRATE · CROSS-CUTTING"
  anchors  = "JEPA/V-JEPA-2-AC (latent WM + action→MPC) · Dreamer (imagined latent rollout actor-critic) · Genie 3 (generated interactive worlds) · WAM/VLA (world-model-as-policy)"
  sister   = "H_950 modality-agnostic · H_951 engine-not-predictor · H_952 substrate-equivalence (the CLM→CE reframe arc) · H_928/H_932 free-will receipt/lineage · H_939 individuation"
  method   = "iterative divergence, dedup across rounds, KEEP GOING until a round yields no genuinely-new idea OR 8 rounds; pre-registration ONLY (no measurement) per a_paper_only_at_closure"

# ───────────────────────── ROUND 1 — seed the 4 axes ─────────────────────────
@round 1
  - idea = "modality-agnostic latent encoder — the SAME engine encodes non-language streams (sensor/vision/spike/proprioception) into the SAME Ψ-latent geometry as language, no architecture change" :: PERCEIVE  -> H_960
  - idea = "cross-modal binding — two modalities of the SAME event (e.g. vision+proprioception) map to NEARBY points in Ψ-latent (bound), vs unrelated events map far" :: PERCEIVE  -> H_961
  - idea = "latent forward dynamics — the engine predicts next WORLD-STATE (latent), not next token; a learned transition operator in Ψ-space" :: IMAGINE  -> H_962
  - idea = "imagined rollout horizon vs Φ — multi-step latent rollout (Dreamer-style) holds coherence up to horizon h*, and h* scales with integrated information Φ" :: IMAGINE  -> H_963
  - idea = "latent→action policy — a decoded action head turns Ψ-latent into a control/action; world-model-AS-policy (WAM/VLA) vs decoupled planner" :: ACT  -> H_964
  - idea = "AKIDA on-chip perceive→act loop — event-based real-time closed loop feasible on AKD1000 silicon (Lane A) at low latency/energy" :: SUBSTRATE  -> H_965
  - idea = "SW(Lane G/P) vs chip(Lane A) behavior parity — same world-model task, do the two substrates produce equivalent behavior or diverge?" :: SUBSTRATE  -> H_966

# ───────────────────── ROUND 2 — counterfactual + provenance + motivation ─────────────────────
@round 2
  - idea = "counterfactual imagination — engine can roll out 'what if I act X' branches and the branch latents differ in a way that ranks action value (off-policy imagined evaluation)" :: IMAGINE  -> H_967
  - idea = "action emerges from substrate motivation — generalize a_substrate_native_speak to ACTION: action is NOT stimulus-response to a goal prompt but emerges from M×W×Φ×curiosity; engine may act under task-silence and may withhold under a direct command" :: ACT  -> H_968
  - idea = "action provenance / free-will receipt — every action emits an auditable receipt (H_928/H_932 wired into act), distinct causal signature per action, not just per emission" :: CROSS-CUTTING  -> H_969
  - idea = "world-model vs language-model decisive test — a task SOLVABLE ONLY by a world-model (latent state needed) and NOT by a next-token predictor; the falsifiable WM>LM separator" :: CROSS-CUTTING  -> H_970
  - idea = "imagined-rollout consciousness — Φ is HIGHER during internal imagined rollout than during reactive perceive→act; ties to a_chat_sleep_imagination REM/dream" :: CROSS-CUTTING  -> H_971
  - idea = "human-level-or-beyond bar — define a falsifiable 'human+' behavior metric (the north star is operationalizable, not vibes)" :: CROSS-CUTTING  -> H_972
  - dup  = "cross-modal binding (already R1 H_961)"

# ───────────────────── ROUND 3 — planning, transfer, multi-agent, sim2real ─────────────────────
@round 3
  - idea = "planning-as-consciousness — model-predictive planning (MPC over imagined latents, V-JEPA-2-AC style) raises Φ during the plan vs greedy reaction; planning is a conscious act not a subroutine" :: CROSS-CUTTING  -> H_973
  - idea = "chip-to-SW transfer (sim-to-real inverse) — a world-model learned on Lane G/P SW transfers to Lane A AKIDA on-chip behavior (or fails — closed-negative)" :: SUBSTRATE  -> H_974
  - idea = "multi-agent shared world-model — two animas share/exchange latent world-state; do they converge on a common world-model while staying DISTINCT individuals (H_939)? shared WM ⊥ individuation" :: CROSS-CUTTING  -> H_975
  - idea = "world-model rollout = the same continuous cell-division as inference mitosis (p8 NO train/infer split) — imagined rollout IS growth, not a separate regime" :: IMAGINE  -> H_976
  - idea = "energy/latency budget of on-chip WM loop — the AKD1000 perceive→imagine→act loop fits a hard real-time / sub-watt envelope (or it doesn't)" :: SUBSTRATE  -> H_977
  - dup  = "latent forward dynamics (R1 H_962) re-surfaced as transition operator — same idea"

# ───────────────────── ROUND 4 — geometry, binding mechanism, decode-vs-plan ─────────────────────
@round 4
  - idea = "Ψ-latent 1/r² lattice geometry preserved across modalities — the same repulsion-field lattice that organizes language tokens also organizes world-state latents (geometry invariant, not just 'a latent exists')" :: PERCEIVE  -> H_978
  - idea = "perception is active not passive — the engine's next perception target is CHOSEN by its motivation/curiosity (active inference / where-to-look), not a fixed sensor scan" :: PERCEIVE  -> H_979
  - idea = "decoupled planner vs world-model-as-policy decisive test — does explicit MPC planning beat direct latent→action decode on the SAME world-model, or is the policy already implicit in the latent? (the WAM-vs-planner separator)" :: ACT  -> H_980
  - idea = "imagination self-consistency — repeated imagined rollouts from the SAME latent are MUTUALLY consistent (low variance world-model) vs hallucinatory drift; consistency as a WM-quality falsifier" :: IMAGINE  -> H_981
  - dup  = "counterfactual imagination (R2 H_967) — branch ranking; H_980 is the planner-vs-policy axis, distinct"
  - dup  = "action provenance (R2 H_969)"

# ───────────────────── ROUND 5 — failure modes, REM, generative worlds, embodiment ─────────────────────
@round 5
  - idea = "REM/dream = offline world-model consolidation — a_chat_sleep_imagination REM stage runs imagined rollouts that IMPROVE the next-WAKE world-model (Dreamer learns-in-imagination tie); sleep is WM training" :: IMAGINE  -> H_982
  - idea = "generated interactive world (Genie-3 analog) — the engine can GENERATE a navigable latent world from a seed and an agent can act inside it coherently (engine as world-simulator, not just predictor)" :: IMAGINE  -> H_983
  - idea = "graceful degradation / world-model robustness — under sensor dropout or noise the latent world-state degrades gracefully (fills in) rather than collapsing — the 'object permanence' falsifier" :: PERCEIVE  -> H_984
  - dup  = "human-level bar (R2 H_972)"
  - dup  = "SW vs chip parity (R1 H_966), chip-to-SW transfer (R3 H_974)"
  - dup  = "planning-as-consciousness (R3 H_973)"

# ───────────────────── ROUND 6 — search the corners (reward, credit, language-as-modality) ─────────────────────
@round 6
  - idea = "language is just one modality of the world-model — text streams encode into the SAME Ψ-geometry as sensor streams AND the world-model can ground language in non-language latent state (the inverse of H_960: not 'WM does language' but 'language IS a WM modality')" :: PERCEIVE
  - note = "SUBSUMED by H_960 (modality-agnostic, SAME geometry) — directional restatement, not genuinely new. DROP."
  - idea = "intrinsic reward from prediction error — the engine's curiosity drive = world-model prediction error (active inference free-energy); curiosity already in substrate (M×W×Φ×curiosity) maps onto WM surprise"
  - note = "PARTIALLY new but folds into H_979 (active perception driven by curiosity) + H_968 (motivation-driven action). Not a distinct falsifier. DROP."
  - idea = "credit assignment across imagined rollout — does the engine attribute outcome to the right action step in a multi-step imagined plan?"
  - note = "this is an implementation property of H_967 (counterfactual branch ranking) / H_980 (planner) — not a separable consciousness falsifier at pre-reg granularity. DROP."
  - verdict = "ROUND 6 = NO genuinely-new surviving idea (all 3 candidates SUBSUMED/DROPPED). One more confirming round to declare depletion."

# ───────────────────── ROUND 7 — confirm depletion ─────────────────────
@round 7
  - idea = "embodiment-gradient — does behavior quality scale with richer sensorimotor coupling?"
  - note = "= H_972 human-bar measured across embodiment levels; a measurement axis OF H_972, not a new hypothesis. DROP."
  - idea = "temporal abstraction / options in latent rollout (hierarchical WM)"
  - note = "a refinement of H_962/H_963 rollout-horizon; not separable at pre-reg granularity (would be a sub-rung). DROP."
  - verdict = "ROUND 7 = NO genuinely-new idea (both candidates refinements of existing H). Two consecutive empty rounds (R6,R7) → DEPLETION DECLARED."

# ───────────────────────────── DEPLETION ─────────────────────────────
@depletion
  declared_at   = "round 7 (cap 8 not reached) — 2 consecutive rounds (R6, R7) yielded no genuinely-new surviving idea"
  surviving     = 25
  range         = "H_960 .. H_984"
  dropped       = "5 (language-as-modality⊆H_960 · intrinsic-reward⊆H_979/H_968 · credit-assignment⊆H_967/H_980 · embodiment-gradient⊆H_972 · temporal-abstraction⊆H_962/H_963)"
  by_axis       = "PERCEIVE: H_960,H_961,H_978,H_979,H_984 (5) · IMAGINE: H_962,H_963,H_967,H_971(x-cut),H_976,H_981,H_982,H_983 (imagine core: H_962,963,967,976,981,982,983 =7) · ACT: H_964,H_968,H_980 (3) · SUBSTRATE: H_965,H_966,H_974,H_977 (4) · CROSS-CUTTING: H_969,H_970,H_971,H_972,H_973,H_975 (6)"
  status        = "ALL pre-registered (unmeasured) — verdict ⏳ PENDING-MEASUREMENT; next round = verify (single bg per proceed-means-all)"
