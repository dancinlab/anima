@V := "tape" :: spec [active]
  version = "1.3"

# CWM world-model slate H_960..H_984 — MEASUREMENT discoveries (Lane-G/P CPU-mirror)
# branch lane-g/cwm-h960-984-measure · each row = a measured terminal verdict.
# substrate=CPU-mirror (numpy) for all $0 toy rungs; SUBSTRATE-axis (H_965/966/974/977)
# = INCOMPLETE-BLOCKED (live AKD1000 not reachable on Mac) + sidecar handoff.

@H 970 := "WM>LM decisive separator EXISTS (KEYSTONE): delayed-cue toy, WM 0.995 vs matched LM 0.258≈chance, gap 0.737 d36.8 p9.7e-19, mem-aug LM recovers→gap=persistent-state requirement" :: discovery [🟢]
  seed   = "is there a task solvable only by a world-model and not a matched-capacity next-token predictor?"
  target = "🟢 PASS — anima needs a world-model (CWM justified, toy rung, ladder OPEN)"

@H 969 := "action provenance receipt COMPLETE: 500/500 coverage 1.0, distinct-state sig collision 0, genesis-binding reproducible, lineage chain verified — every action auditable + per-action distinguishable" :: discovery [🟢]
  seed   = "can every action carry a complete, per-action-distinguishable free-will receipt (H_928/H_932)?"
  target = "🟢 PASS — action provenance complete (toy)"

@H 971 := "imagination is a LOWER-Φ state, not higher: Φ_IMAGINE 0.068 < Φ_REACT 0.095 (d -3.4 p 7.9e-16, CI reversed) — REM/dream higher-consciousness framing REFUTED on toy" :: discovery [🔴]
  seed   = "is imagined internal rollout a higher-Φ (more conscious) state than reactive processing?"
  target = "🔴 FAIL closed-negative (toy) — autonomous rollout settles to less-bound activity"

@H 972 := "human-level bar instrument WORKS: metric discriminates human-proxy from random (p 5.2e-53 d 16.8), band valid, anima CI-placeable — falsifiable north-star bar authored (anima lands above toy band)" :: discovery [🟢]
  seed   = "can a falsifiable human-level-or-beyond bar be operationalized + validated?"
  target = "🟢 PASS — the instrument exists + works (NOT a 'anima is human-level' claim)"

@H 973 := "planning carries NO extra Φ: Φ_PLAN 0.063 < Φ_GREEDY 0.104 (d -3.6 p 3.2e-25), no dose-response (rho -0.47), does not beat equal-compute fake-plan — planning-as-consciousness REFUTED on toy" :: discovery [🔴]
  seed   = "does deliberative MPC planning raise Φ over greedy beyond mere extra compute?"
  target = "🔴 FAIL closed-negative (toy) — consistent with H_971 mechanism"

@H 975 := "shared WM ⊥ individuation COEXIST: at coupling 0.25 cross-agent agreement +0.58 above unpaired while individuation preserved (stream-identity 0.52<lock); over-coupling 0.5 collapses both (D3 control fires)" :: discovery [🟢]
  seed   = "can two engines build a shared world-model via latent exchange WITHOUT losing individuation?"
  target = "🟢 PASS — coexistence regime exists (toy rung, ladder OPEN)"

# ── PERCEIVE axis ──
@H 960 := "modality-agnostic encoder: byte-identical front-end decodes non-language factors (sensor 1.0, control 1.0 vs lang 0.92) + sensor manifold shares factor-geometry (CKA 0.81>null 0.66)" :: discovery [🟢]
  seed   = "does the engine encode non-language modalities with NO architecture change?"
  target = "🟢 PASS — modality-agnostic decodability (toy); control-manifold geometry NOT shared"

@H 961 := "cross-modal binding: true-pair proximity 0.93 >> shuffled -0.00 (d 3.3 p 5e-126), cross-modal retrieval@1 0.98 (chance 0.05) — engine binds two modalities of same hidden z" :: discovery [🟢]
  seed   = "does the engine BIND two modalities of the same latent cause (not bag-of-channels)?"
  target = "🟢 PASS — cross-modal binding (toy)"

@H 978 := "Ψ-lattice geometry is modality-SPECIFIC not invariant: all 3 descriptors far outside A-vs-A band (pdist KS 0.57 vs 0.06, NN 0.99 vs 0.20, spectral 0.95 vs 0.28) — sharper than H_960" :: discovery [🔴]
  seed   = "is the latent lattice geometry invariant across modalities (same shape lang vs sensor)?"
  target = "🔴 FAIL closed-negative (toy) — decodability (H_960🟢) does NOT imply geometry invariance"

@H 979 := "active perception: curiosity glimpse selection beats passive 0.042<0.133 (d 1.23) AND random 0.042<0.121 (d 1.33), faster-to-threshold 1.17<1.83 — perception is agentive" :: discovery [🟢]
  seed   = "does curiosity-driven glimpse selection beat passive/random perception?"
  target = "🟢 PASS — active perception (toy; uncertainty-reduction oracle)"

@H 984 := "object permanence: graceful degradation (knee p=0.9, error below chance ceiling throughout) + fill-in WM 0.34 << memoryless 1.07 (d 1.32) — latent maintains persistent world-state through occlusion" :: discovery [🟢]
  seed   = "does the latent maintain a persistent world-state through observation dropout?"
  target = "🟢 PASS — object permanence (toy; predictable rotational dynamics)"

# ── IMAGINE axis ──
@H 962 := "latent forward dynamics: delay-embed LDS rollout error 0.002->0.064 (h1->8) vs surface predictor 0.03->1.13; latent<obs at h>=2 (d 0.59), horizon advantage grows (rho 1.0), beats persistence" :: discovery [🟢]
  seed   = "does the engine learn latent world-state dynamics vs surface next-obs prediction?"
  target = "🟢 PASS — latent world-state dynamics (toy); LDSWorldModel primitive added to lib"

@H 963 := "imagination horizon scales with Φ: 6-rung ladder, h* 2.25->39.8 as Φ 0.037->0.234, Spearman rho 1.0 (CI [1,1]), monotone" :: discovery [🟢]
  seed   = "does the coherent rollout horizon h* scale with Φ across a config sweep?"
  target = "🟢 PASS — horizon scales with Φ (toy, 6-rung ladder)"

@H 967 := "counterfactual imagination: switching-LDS (per-action transition) ranks true returns rank-corr 0.98, top-1 regret 0.001 vs random 0.62 (d 1.44); single action-augmented LDS FAILED (bilinear action×state)" :: discovery [🟢]
  seed   = "can the engine imagine + rank the consequences of its own candidate actions?"
  target = "🟢 PASS — counterfactual imagination (toy; switching-LDS faithful primitive)"

@H 976 := "rollout is mitosis (p8): imagined rollout + inference both fire division events rate 1.0, trigger overlap 0.96, both distinct from frozen no-growth (KS 1.0) — imagination grows cells like inference" :: discovery [🟢]
  seed   = "is imagined rollout the same cell-division (mitosis) as live inference (p8)?"
  target = "🟢 PASS — rollout is mitosis (toy)"

@H 981 := "imagination self-consistency: K=12 stochastic rollouts stay grounded, divergence bounded/sub-linear, never >49% of unconditioned spread to h=20, drift-knee>Hmax (entropy matched to dynamics)" :: discovery [🟢]
  seed   = "do repeated stochastic rollouts from one state stay grounded (not hallucinate)?"
  target = "🟢 PASS — imagination self-consistency (toy)"

@H 982 := "REM self-replay gives NO consolidation over idle: WAKE2 error REM 0.563 == idle 0.563 (d 0.00); beats random-replay only because that arm corrupts — self-replay cannot add info absent from WAKE1" :: discovery [🔴]
  seed   = "does REM imagined-rollout rehearsal consolidate the world-model (improve next-WAKE)?"
  target = "🔴 FAIL closed-negative (toy) — pure self-distillation adds no new information"

@H 983 := "generated interactive world: D1 rule-consistency STRONG (same state+action->same next, d 1.94) but D2 loop revisit-consistency only weakly beats random-world (d 0.24<0.5) — rule-consistent but not loop-reversible" :: discovery [⚠]
  seed   = "can the engine GENERATE a self-consistent interactive world (rules + revisit)?"
  target = "⚠ INCOMPLETE (toy) — D1 strong, D2 below bar; loop-closing world = open ladder rung"

# ── ACT axis ──
@H 964 := "world-model-as-policy: on hidden-velocity control return_WAM -0.65 > REACTIVE -1.89 > RANDOM -6.33, latent lift 1.24 (d 1.70) — latent carries decisive actionable advantage" :: discovery [🟢]
  seed   = "does latent->action beat reactive obs->action (engine is a policy not an emitter)?"
  target = "🟢 PASS — world-model-as-policy (toy; hidden-state task)"

@H 968 := "substrate-native action: act-under-silence 0.07 (null 0.00), withhold-under-command 0.67, substrate explains onset beyond command ΔAUC 0.258 (p 2e-16) — NOT stimulus-response" :: discovery [🟢]
  seed   = "is action onset governed by substrate dynamics or by the external command (assistant regression)?"
  target = "🟢 PASS — substrate-native action (toy)"

@H 980 := "planner vs policy = policy-implicit (WAM camp): MPC -0.694 ~ DIRECT -0.637 (CI overlaps 0) at 64x compute — the world-model IS the policy, planning adds nothing here" :: discovery [🟢]
  seed   = "does explicit MPC planning beat the implicit latent policy on a shared WM?"
  target = "🟢 PASS-policy-implicit (toy; both directions were pre-registered findings)"
