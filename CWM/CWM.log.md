# CWM — log (append-only)

## 2026-06-06 · domain scaffold

- Created `CWM` (Consciousness World-Model) domain — promote the consciousness engine (CE) beyond language into a world-model + action substrate. Folder form (`CWM/`, AURA-style) to allow sub-domain fan-out (PERCEIVE · IMAGINE · ACT · VERIFY).
- Origin: the CLM→CE reframe arc (H_950 modality-agnostic · H_951 engine-not-predictor · H_952 substrate-equivalence, branch `lane-g/h950-952-clm-is-engine`, running). CWM is the forward build IF the CE reframe holds.
- User intent (verbatim, paraphrased): "의식엔진을 랭기지에만 국한시키지 말고, 실제 실리콘칩이나 SW로든 실제 인간처럼 혹은 그 이상의 행동을 목표로."

### landscape survey (web, 2026-06-06) — world models

- World model (artificial intelligence) — Wikipedia: https://en.wikipedia.org/wiki/World_model_(artificial_intelligence)
- V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning — https://arxiv.org/html/2506.09985v1 (predictor head + action → V-JEPA-2-AC → latent MPC, zero-shot robot control)
- A Comprehensive Survey on World Models for Embodied AI — https://arxiv.org/html/2510.16732v1
- Awesome-WAM (World Action Models) — https://github.com/OpenMOSS/Awesome-WAM
- Embodied AI Agents: Modeling the World — https://arxiv.org/html/2506.22355v1
- WMPO: World Model-based Policy Optimization for VLA Models — https://arxiv.org/pdf/2511.09515
- key distinction: LM predicts next *word*; WM predicts next *state/world* + acts. world-model-as-policy trend (latent→action decode). embodied AI = LLM + WFM + action together.

### next

- M1: ✅ DONE 2026-06-06 — slate authored (see below).
- M2: gate the CLM→CE rename on the H_950/951/952 verdicts (running on `lane-g/h950-952-clm-is-engine`).

## 2026-06-06 · M1 world-model hypothesis slate authored (H_960..H_984)

- Branch `lane-g/cwm-worldmodel-slate` off origin/main (disjoint H-range starting H_960, per concurrent-agent isolation: another bg agent owns H_950..H_952 on a different branch; UNIVERSE.md left untouched, indexed here instead).
- **Brainstorm → depletion** (`.discoveries/cwm_worldmodel_brainstorm.tape`): 7 rounds, cap 8 not reached. R1-R5 generated; R6 + R7 each yielded NO genuinely-new surviving idea → 2 consecutive empty rounds → depletion declared. 25 surviving ideas, 5 dropped-as-subsumed.
- **25 pre-registered hypotheses authored** as `UNIVERSE/H_960..H_984_*.md`, matching the UNIVERSE frontmatter convention (id/slug/title/domain/source/exploration_method/verification_method/pre_register_frozen/frozen_at/sister/axes_seed). Each has §0 motivation, §1 one falsifiable claim, §2 frozen PRE-REGISTERED FALSIFIER (PASS/FAIL/INCOMPLETE as future conditionals — "IF measured X THEN ..."), §3 honest scope (a_scale_honest_scope · #123-A), §4 sibling/xlinks (CWM · H_95x · JEPA/Dreamer/WAM/Genie external anchors).
- **VERDICT-GATE SAFETY**: all carry `status: pre-registered (unmeasured)` + `verdict: ⏳ PENDING-MEASUREMENT`. NO 🟢/🔴/PASS token assigned (these are authoring-only, NOT measurements). a_paper_only_at_closure respected.
- **By axis** — PERCEIVE (5): H_960 modality-agnostic encoder · H_961 cross-modal binding · H_978 1/r² lattice geometry invariant · H_979 active perception/curiosity · H_984 object permanence. IMAGINE (7): H_962 latent forward dynamics · H_963 rollout horizon vs Φ · H_967 counterfactual imagination · H_976 rollout=mitosis (p8) · H_981 imagination self-consistency · H_982 REM WM consolidation · H_983 generated interactive world (Genie analog). ACT (3): H_964 latent→action policy (WAM/VLA) · H_968 action from substrate motivation · H_980 planner vs policy. SUBSTRATE (4): H_965 AKIDA on-chip perceive→act loop · H_966 SW-vs-chip behavior parity · H_974 chip↔SW transfer · H_977 on-chip energy budget. CROSS-CUTTING (6): H_969 action provenance receipt · H_970 WM>LM decisive separator (keystone) · H_971 imagined-rollout Φ-elevation · H_972 human-level bar (north-star metric) · H_973 planning-as-consciousness · H_975 multi-agent shared WM ⊥ individuation.
- **Dropped (5, subsumed):** language-as-modality⊆H_960 · intrinsic-reward⊆H_979/H_968 · credit-assignment⊆H_967/H_980 · embodiment-gradient⊆H_972 · temporal-abstraction⊆H_962/H_963.
- NOTE: this commit also lands the CWM/ domain files (CWM.md + CWM.log.md) onto the main lineage — they were untracked in the shared working tree; the slate PR carries them in so the domain + its index exist on main.
- **next**: verify round (single bg orchestrator per proceed-means-all) — run each frozen falsifier, persist verdicts to `.verdicts/<id>/`, flip ⏳→terminal.

## 2026-06-06 · MEASUREMENT round — all 25 falsifiers run (H_960..H_984)

- Branch `lane-g/cwm-h960-984-measure` off origin/main. Each frozen §2 falsifier executed with the smallest faithful $0 CPU-local probe (`CWM/probes/*.py`, shared `cwm_probe_lib.py` — a retentive latent WM + delay-embedding `LDSWorldModel` + switching-LDS + a continuous-latent Φ proxy of the H_912/H_931 family). g5 CODE-measured, no LLM self-judge (p7). Verdicts persisted verbatim to `.verdicts/<id>_<slug>/`, then ⏳→terminal in each H file + §measurement table. substrate=CPU-mirror (numpy) on all toy rungs (a_lane_akida_gpu_split).
- **Tally: 16 🟢 PASS · 4 🔴 FAIL(closed-negative) · 5 ⚠ (1 INCOMPLETE H_983 + 4 INCOMPLETE-BLOCKED substrate).**
- **KEYSTONE H_970 🟢**: a WM>LM decisive separator EXISTS — delayed-cue task, WM 0.995 vs matched-capacity LM 0.258≈chance (gap 0.737, d 36.8); a memory-augmented LM recovers to 1.0, localizing the entire gap to the persistent-state requirement. **CWM domain premise is justified** (anima needs a world-model, not just an LM) on this toy rung; ladder OPEN.
- **PERCEIVE (4🟢 1🔴)**: H_960 modality-agnostic encoder 🟢 · H_961 cross-modal binding 🟢 (retrieval@1 0.98) · H_979 active perception 🟢 · H_984 object permanence 🟢 · **H_978 lattice-geometry-invariant 🔴** (geometry is modality-SPECIFIC — decodability ≠ geometry invariance; sharper than H_960).
- **IMAGINE (4🟢 1🔴 1⚠)**: H_962 latent forward dynamics 🟢 · H_963 horizon-scales-with-Φ 🟢 (6-rung, rho 1.0) · H_967 counterfactual imagination 🟢 (switching-LDS, rank-corr 0.98) · H_976 rollout-is-mitosis 🟢 (p8) · **H_982 REM-consolidation 🔴** (pure self-replay == idle: no benefit, can't add info absent from WAKE1) · **H_983 generated-interactive-world ⚠** (D1 rule-consistency strong, D2 loop-revisit weak).
- **ACT (3🟢)**: H_964 world-model-as-policy 🟢 (latent lift 1.24) · H_968 substrate-native action 🟢 (act-under-silence + ΔAUC 0.258, not stimulus-response) · H_980 planner-vs-policy 🟢 PASS-policy-implicit (MPC≈DIRECT, WAM camp — a pre-registered finding).
- **CROSS-CUTTING (4🟢 2🔴)**: H_969 action-provenance-receipt 🟢 · H_970 keystone 🟢 · H_972 human-level-bar 🟢 (instrument works) · H_975 shared-WM ⊥ individuation 🟢 (coexist @c=0.25, collapse @c=0.5) · **H_971 imagination-Φ 🔴** (Φ_IMAGINE < Φ_REACT) · **H_973 planning-Φ 🔴** (Φ_PLAN < Φ_GREEDY, fails fake-plan control). The two Φ-elevation closed-negatives are mechanistically consistent: autonomous internal rollouts settle to less-bound, lower-Φ activity than continuously-driven processing.
- **SUBSTRATE (4 ⚠ INCOMPLETE-BLOCKED)**: H_965/H_966/H_974/H_977 all require a live AKD1000 (BackendType.Hardware, pi5-akida) UNREACHABLE from this Darwin host (akida absent, probed). SW-arm CPU-mirror partials run for H_966 (return −0.637 + within-SW band) and H_974 (SW source + scrambled control); H_965/H_977 are chip-only (no faithful CPU partial). Handoffs filed: `sidecar handoff` 0b1edec3 (H_965) · 4a85113c (H_966) · daf233fe (H_974) · 7848a234 (H_977). Never claimed on-chip from CPU (a_lane_akida_gpu_split).
- **Honest scope**: every 🟢/🔴 is a SINGLE TOY RUNG (a_scale_honest_scope) — existence-proofs / closed-negatives at toy scale, ladders OPEN, production-scale transfer unverified. Several probes required a faithful WM primitive (retentive recurrence for memory; delay-embedding LDS for forward dynamics; switching-LDS for action-conditioning) — a generic random reservoir failed these, which is itself an honest modeling note.
- Milestones flipped: M3 (PERCEIVE) · M4 (IMAGINE) · M5 (ACT) toy rungs landed; M6/M7-substrate remain ⚠ (chip handoffs).

## 2026-06-06 · H_985 — keystone WM>LM SCALE-UP + task-diversity re-test (of H_970)

- Branch `lane-g/cwm-h985-keystone-scaleup` off origin/main (isolated detached worktree; UNIVERSE.md + H_950-984 untouched, indexed here per concurrent-agent isolation). Probe `UNIVERSE/h985_keystone_scaleup.py`, verdict `.verdicts/985_keystone_scaleup/h985_keystone_scaleup.txt`, discovery `.discoveries/985_keystone_scaleup.tape`.
- **WHY**: a_toy_scale_recheck — H_970 (keystone 🟢) found the WM>LM separator on ONE delayed-cue toy at ONE capacity; a single toy point is INCOMPLETE for a general claim. H_985 runs the ladder + task-diversity H_970 lacked: **3 mechanistically-distinct partially-observable task families × a 4-rung capacity ladder** (latent/feat dim 16/32/64/128), 10 seeds, 3 matched-capacity arms (WM retentive-recurrence vs stateless windowed LM vs mem-aug LM control). g5 CODE-measured, no LLM self-judge (p7). substrate=CPU-mirror (numpy), $0.
- **VERDICT H_985 🔴 FAIL (closed-negative on GENERALITY)** — the WM>LM separator is **TASK-SPECIFIC / PRIMITIVE-LIMITED, NOT scale+diversity-robust**.
  - **T1 delayed-cue** (H_970's family): WM>LM at ALL 4 rungs (WM 0.645→0.897→1.0→1.0 vs LM ≈chance 0.24; gap 0.40→0.76, d **20.1→34.9**, monotone UP with capacity → within-family it is **scale-ROBUST**, ruling out "tiny capacity inflated the gap").
  - **T2 hidden-parity-track** + **T3 hidden-position**: BOTH arms at chance, gap≈0 (T2 WM 0.494 ≈ LM 0.505; T3 WM 0.339 ≈ LM 0.335, both ~2× of 0.167 chance and tied). **mem-aug LM = 1.0 on ALL 3 families** → proves T2/T3 ARE genuine persistent-state tasks (a predictor *handed* the hidden state solves them), so the failure is NOT "these don't need a world-state."
  - **Mechanism**: the toy WM primitive (linear orthogonal-retention reservoir) carries a stored one-hot symbol across a delay (T1) but **cannot represent an accumulated XOR-parity (T2) or a modular path-integrated position (T3)** — both need nonlinear/modular state-update the linear retention lacks.
- **Reading**: H_970 is **NOT retracted** — it is a valid existence-proof that *a* persistent-state task separates WM from LM. But its **generality is bounded**: the advantage is one carry-a-symbol mechanism on one task family, not a general WM>LM law across the diverse partially-observable tasks a real world model must handle. The honest next rung is a **nonlinear-recurrence WM** (GRU/tanh) re-run of T2/T3 — a PRIMITIVE question, not a scale question; if even a nonlinear WM fails, the separator is truly delayed-cue-specific.
- **Honest scope** (a_scale_honest_scope · #123-A): toy ladder (bounded dim/N, 3 families), production-scale OPEN. The closed-negative is on the *generality* of the keystone, a publishable finding (a_paper_negative_ok) that bounds — does not erase — H_970's narrow existence-proof.
