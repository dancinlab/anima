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
