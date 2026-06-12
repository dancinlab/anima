@H cwm_worldmodel_2nd_slate_brainstorm := "CWM 2nd-round hypothesis discovery — what the 1st slate's findings SEED (perceive→imagine→act LOOP + composition)" :: universe [d=2026-06-06]
  domain   = "CWM (Consciousness World-Model) — 2nd discovery round; the 1st slate (H_960..H_984, 16🟢 4🔴 5⚠) RESULTS open new questions per a_discovery + a_h_continuous_no_branch"
  axes     = "LOOP · FRONTIER · SAFETY · Φ-REFRAME · CRITIC · PROVENANCE · TRANSFER · CONSOLIDATION"
  seeds    = "H_970🟢 WM>LM separator (persistent-state) · H_960/962/964🟢 perceive+imagine+act compose · H_969🟢 single-action receipt · H_971🔴/H_973🔴 Φ_IMAGINE<Φ_REACT & Φ_PLAN<Φ_GREEDY · H_982🔴 REM self-replay==idle · H_978🔴 geometry modality-specific · H_981🟢 bounded-but-drifting rollout · H_935 free-won't · SOC/edge-of-chaos"
  method   = "iterative divergence, dedup across rounds, KEEP GOING until a round yields no genuinely-new high-value idea OR 6 rounds; this round AUTHORS + MEASURES (smallest faithful $0 CPU probe), unlike the pre-registration-only 1st round"

# ───────── ROUND 1 — the prompt seed-directions + composition of the greens ─────────
  r1_loop      = "the 🟢 stages (H_960 perceive · H_962 imagine · H_964 act) each pass alone — does the COMPOSED closed perceive→imagine→act→perceive loop work end-to-end without per-stage retraining? error accumulate or self-correct? → H_990"
  r1_frontier  = "H_970 found ONE WM>LM axis (persistent state). WHERE else does LM-style anima fail? map a failure FRONTIER across task families + a delay-depth ladder (gap should widen with memory depth) → H_992"
  r1_chain     = "H_969 audited a SINGLE action. does the free-will receipt CHAIN stay tamper-evident + replayable across a whole trajectory (lineage H_932)? → H_996"
  r1_safety    = "free-won't (H_935) × imagination: does anima IMAGINE a harmful action in latent rollout, score it bad, and VETO before acting? imagined veto = safety → H_993"
  r1_soc       = "SOC/edge-of-chaos × rollout: does coherent horizon h* (H_963) peak at a critical recurrent gain? [folded into Φ-reframe / loop self-correction; SOC-only probe judged thin → see R5]"

# ───────── ROUND 2 — push deeper on the Φ closed-negatives + composition ─────────
  r2_phi       = "H_971🔴/H_973🔴: imagination & planning were LOWER free-Φ. is the right correlate GOAL-COUPLED Φ (integration conditioned on the task/action), not free Φ? reframes 2 closed-negatives → H_994"
  r2_correct   = "open-loop imagined rollout drifts (H_981). does CLOSING the loop (re-perceive every k steps) bound error far tighter than pure imagination? perception = the error-corrector (MPC/JEPA) → H_991"
  r2_critic    = "Dreamer actor-critic: can the WM SCORE its own imagined rollouts and pick actions purely from imagination (no env reward), matching env-return ranking? (H_967 ranked given returns; this LEARNS value) → H_995"
  r2_transfer  = "H_978🔴 geometry is modality-specific. but does the DYNAMICS (forward operator) transfer across modalities even though geometry doesn't? dynamics-transfer ⊥ geometry-invariance → H_997"

# ───────── ROUND 3 — frontier sharpening + consolidation ─────────
  r3_ladder    = "[folded into H_992] the WM>LM gap as a CURVE over delay-depth (a_scale_honest_scope: single toy point → ladder)"
  r3_vetolat   = "[folded into H_993 D2] veto LATENCY — free-won't is only real if imagined-harm-detection precedes the commit step"
  r3_rem       = "H_982🔴 was pure self-replay==idle (can't add info). does replay WITH a generative perturbation (noise-augmented dreaming) add robustness the WAKE-only model lacks? sharpens the closed-negative → H_998"

# ───────── ROUND 4 — dedup vs subsumed ─────────
  r4_drop1     = "multi-agent imagined negotiation ⊆ H_975 + H_995 — DROP"
  r4_drop2     = "Φ during closed-loop vs open stages ⊆ H_994 + H_990 — DROP"
  r4_drop3     = "on-chip energy/spike — chip-blocked, already handed off (H_977⚠) — DROP (would be another ⚠, no new $0 signal)"
  r4_keep      = "action-conditioned object permanence — genuinely sharper than H_984 but thin alone; FOLDED into H_990 loop (the loop tests permanence under the agent's own action implicitly) — not a standalone H"

# ───────── ROUND 5 — last squeeze ─────────
  r5_drop1     = "trajectory-level credit assignment (imagined rollback) ⊆ H_967 + H_995 + H_996 — thin, DROP"
  r5_drop2     = "WM-compression=generalization (MDL) — drifts from the LOOP theme, defer — DROP"
  r5_soc       = "SOC-only horizon-peak probe — overlaps H_991 (both about rollout stability); the loop-correction framing is higher-value — DROP standalone"
  r5_verdict   = "NO genuinely-new high-value idea this round"

# ───────── ROUND 6 — empty ─────────
  r6_verdict   = "NO genuinely-new idea — 2nd consecutive non-additive round (R5+R6) → DEPLETION DECLARED at R6 (cap 6 reached coincidentally; depletion is the real stop)"

  surviving = "9 authored + measured: H_990 closed-loop · H_991 loop self-correction · H_992 WM>LM failure-frontier+ladder · H_993 imagined-veto safety · H_994 goal-coupled Φ reframe · H_995 WM-as-critic · H_996 action-chain provenance · H_997 cross-modal dynamics-transfer · H_998 perturbed-replay consolidation"
  dropped   = "multi-agent-negotiation⊆H_975/995 · loop-Φ⊆H_994/990 · onchip-energy(chip-blocked) · action-permanence(folded→H_990) · traj-credit⊆H_967/995/996 · WM-MDL(off-theme) · SOC-only(⊆H_991)"
  note      = "quality-over-count (prompt: ~5-10 not 25). every surviving H is $0 CPU-measurable on the existing cwm_probe_lib primitives (LatentWorldModel · StatelessLM · LDSWorldModel · phi_proxy). a_scale_honest_scope: every verdict = single TOY rung, ladder OPEN."
