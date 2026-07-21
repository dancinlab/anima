# Changelog

All notable changes to anima-v3. Append-only; newest on top.

## 2026-07-17 — H_013 root-cause → certified LV-C had a NULL BIAS (frame misalignment); fixed upstream; H_011 7B anchor SUSPENDED pending re-run

- H_013's first scripted run failed its own certification exactly as designed: P-DEAD (null env) read
  closure 0.667 at every dose — above the 0.60 gate — and the live curve was dose-flat. Root-caused
  ($0, deterministic, `state/h013_closure-dose-response_2026-07-17/probe_lvc_bias.py`): **the certified
  H_011 `lv_c` compared Closed's PRE-step obs `[o_0..o_{T-1}]` against ghosts built from POST-step obs
  `[o_1..o_T]`** — a one-tick frame misalignment that gives d(Closed, ghost) a shift term the
  ghost-ghost reference lacks. In a null env the two ghosts are bit-identical (d=0 exactly), so ANY
  exogenous digest drift across a 50-tick block scored a "closure" hit. The earlier "energy
  side-channel" reading of the 0.0152 residual is refuted (null skips `_apply_action` entirely; the
  residual is exactly the one-tick shift). The suspected asymmetric-control geometry (Closed special vs
  same-family ghosts) is NOT the operative mechanism.
- **Fix (upstream-fix, one line)**: `fC = obs_traj[1:]` in `run_h011.lv_c` + `run_h013.lv_c_dose`
  (features/blockmeans/gates untouched). Repaired: null env 0.000 at every dose; near-dead p=0.1 drops
  0.833→0.389 (refuses); full-dose plants unchanged (P-LIVE 0.750 / P-OPEN 0.417). H_013 scripted
  certification now PASSES (P-DOSE mono 0.6 · P-DEAD ok · P-LIVE 0.722); pre-repair record preserved as
  `result_scripted_pre-repair-biased-estimator.json`.
- **H_011 consequence (honesty)**: the 7B ANCHOR-ON-LV-C (0.7625) was measured with the biased
  estimator, whose measured null floor (0.667) exceeds the gate and exceeds the 7B's episode-1 closure
  (0.625). Registry tier moved to 🟠 ANCHOR-SUSPENDED; stage-A re-certified with the repaired estimator
  (`result_stageA_lvc-repair.json`, all plants pass), but the 7B must re-earn the anchor on summer
  (its action tape was not persisted, so the repaired closure cannot be recomputed offline). Full-dose
  scripted readings were repair-invariant, so survival is plausible — but unproven.
- Lesson (recurrence of run-h011-py-1 / H_009): **a certification suite must null-check EVERY gate it
  certifies** — H_011's P-DEAD refused on LV-W only; LV-C was never pointed at a dead env, so a
  null floor above its own gate passed unseen. H_013's P-DEAD plant is what caught it.

## 2026-07-17 — H_012A-c → 🟡 BLOCK-REFUSE: the refusal is robust across TIMESCALES too — the 2×2 (target × timescale) matrix all refuses

- The next objection: H_010/H_012A/H_012A-b are ALL one-step (U_t → R_{t+1}), yet the proxy's 7B ANCHORED at
  the BLOCK level (LV-C) and FAILED one-step (LV-W) — so the real-loop refusals could be at the WRONG
  TIMESCALE (the timescale analogue of the wrong-target artifact H_012A-b excluded). Delegated the design to
  Fable, which **factored the block level**: the sequence-CONTINGENCY component (yoked permuted-sequence
  ghost) is fundamentally interventional → H_012B-only; but the block-OUTCOME component is identified under
  the SAME per-step ignorability H_012A accepted. **Pre-registered H_012A-c** (frozen before touching real
  pairs): treatment = single utterance U_t (context-matched, M=60), outcome = blockmean(features(R_{t+1..t+k})),
  primary k=5.
- **Why distinct from one-step** (a block null is NOT implied by the three one-step nulls): INTEGRATION
  (per-step effects below the one-step floor accumulate over k — the campaign's OWN dissociation: H_011 7B +
  mid3bal both LV-W-fail 0.35 / LV-C-pass 0.76) and DELAY (U_t moves the owner at lag 2-5 with no lag-1
  trace — the natural Claude Code mode). Block-mean(R_{t+1..t+k}) is not a function of the lag-1 pair.
- **Estimator certified with FOUR block plants (in-regime M=60):** P-BLOCKPOS integration fires 0.792 > null
  0.647 and beats its own one-step 0.698; **P-DELAY** detects a lag-3 effect the one-step is blind to
  (0.65 > null 0.648, one-step does not); P-BLOCKNULL refuses; **P-BLOCKCONF** (a slow-drift latent driving
  BOTH the utterance and the owner window with NO U→R edge — the confound window-aggregation amplifies)
  correctly REFUSES. So a real BLOCK-REFUSE is trustworthy, not an instrument miss.
- **VERDICT = BLOCK-REFUSE.** On 9,454 block-windowed queries (k=5): **sign_base_full = 0.420 / 0.437 vs
  null_p95 0.403 / 0.421** (both replicates < 0.55) — even at the window level the proxy anchored on, a
  single utterance does NOT shift the owner's subsequent-window input. **The refusal is now ROBUST across a
  2×2 matrix — target (text H_010/H_012A · behavior H_012A-b) × timescale (one-step · window H_012A-c) — all
  four $0 lenses refuse; both the wrong-target and wrong-timescale artifacts are EXCLUDED.** Honest residue
  (pre-registered): the sequence-CONTINGENCY channel (LV-C proper, the yoked ghost) is interventional and
  stays H_012B-only — a pure order-code channel cannot be excluded at $0.
- Also amended H_012B's pre-registration: randomize LIVE/GHOST grounding over sustained WINDOWS + LV-C block
  statistic as CO-PRIMARY, so the paid RCT adjudicates the timescale question at rung 1. SSOT:
  `verification-h012` role refreshed (2×2 matrix) + child `h012ac-block`; REGISTRY H_012.

## 2026-07-17 — H_012A-b → 🟡 BEHAVIORAL-REFUSE: the owner-loop refusal is NOT a wrong-target artifact (robust across text AND behavior)

- The one live objection to "reframe C is refused on the real owner loop" was that H_010 + H_012A both used
  the SAME target — the owner's next-reply TEXT embedding — which is topic-ceilinged and could HIDE closure.
  Delegated the target-swap design to Fable; **pre-registered H_012A-b** (frozen before any labels computed):
  swap the target to a binary owner STANCE (CONTINUE on the agent's track vs CORRECT/redirect), a lower-dim
  projection of the same subsequent input.
- **Labeler reads the OWNER TURN ONLY** (a hard label-leak rule, EN+KO; certified by plant P4 = the
  signature is exactly `(rt1_bytes,)`). Estimator = the certified context-matched path with a scalar Brier
  target; drops zero-stance-variance strata. **Certified IN-REGIME first (M=60, applying `run-h011-py-1`):**
  P1 channel fires 0.867 ≫ null 0.496, P2 null refuses (0.354), P3 confound refuses (utterance can't beat
  context), P4 leak-safe; the P1 noise floor (0.66 @ 15 % label noise, 0.48 @ 30 %) calibrates the
  detectable-effect floor. (First cut FAILED — plants ran at M=14 vs real M=60, and a k/stride arithmetic
  alignment degenerated the shift-null; both fixed = the `run-h011-py-1` lesson applied twice more.)
- **VERDICT = BEHAVIORAL-REFUSE.** On 9,962 real pairs (stance rate 0.606, balanced; 1852/1775 informative
  strata): **sign_base_full = 0.245 / 0.226 vs null_p95 0.241 / 0.234** (both replicates < 0.55, at the null
  band) — adding the agent utterance predicts the owner's next-turn stance WORSE than context alone, far
  below even the 30 %-noise plant floor. **So the owner-loop refusal is ROBUST ACROSS TARGETS (text AND
  behavior) — NOT a wrong-target artifact.** The agent's specific utterance does not shift the owner's
  subsequent input, in either projection, beyond context. Further lowers the H_012B prior (still semi-
  interventional; cannot anchor — only the live H_012B can).
- SSOT: `verification-h012` role refreshed (both projections refuse) + child `h012ab-behavioral`; REGISTRY
  H_012 tier → both prechecks refuse. Artifacts: `run_h012ab.py`, `result_h012ab.json`.

## 2026-07-17 — H_012 owner-loop-rct PRE-REGISTERED + H_012A → 🟡 PRECHECK-REFUSE: the licensed exit, designed (deception dissolved) and cheaply screened

- H_011's 7B ANCHOR licensed reframe C's real exit — the interventional test on the ACTUAL owner loop.
  Delegated the design to Fable; the **deception problem is DISSOLVED by GROUNDING RANDOMIZATION**: per
  eligible turn a coin sets LIVE (agent replies from its true relationship-state) vs GHOST (same model/
  prompt/owner-message, but grounding replaced by a topic-matched snapshot of the owner's OWN past). Every
  reply is genuine — nothing false — so no deception; the randomized variable is do(grounding). GHOST is
  Watson's yoked control at the real-loop level, reproducing the certified LV-C structure.
- **H_012 pre-registered + frozen** (`cards/H_012_owner-loop-rct.md`, REGISTRY): H_012A = a $0 autonomous
  semi-interventional precheck; H_012B = the consent-gated live RCT (can ANCHOR). Privacy is a hard law:
  no owner content ever to the repo, only aggregate scalars.
- **H_012A (sampler-twin precheck) = PRECHECK-REFUSE.** Decode stochasticity is a local randomizer of the
  utterance given context; reusing H_010's certified estimator with the ONE change of restricting each
  query's k-NN pool to CONTEXT-MATCHED neighbors, on 10,170 real owner↔agent pairs (135 sessions, N=2000
  ×2 disjoint, matched-pool tightness 0.06): **sign_base_full = 0.424 / 0.423 < 0.55 (replicates)**. Even
  semi-interventionally the owner's next reply is governed by context/topic, not by the specific utterance —
  **strengthening H_010's observational 0.406** and LOWERING the prior that H_012B anchors. Cannot itself
  anchor (unidentified). Purpose-built WITHIN-CONTEXT plants certified the restricted estimator first
  (P-POS 0.68 channel / P-NULL 0.47 refuse / P-ECHO 0.67→0.51 echo-only).
- **Instrument re-certification (verdict-integrity · `run-h011-py-1` RECURRENCE).** Plants certified at
  M=12; real data runs at M=60 — a different regime, so I re-certified in-regime: `sign_base_full` separates
  cleanly (channel 0.81 vs null 0.515) and real 0.424 sits below the null → REFUSE trustworthy. The
  `rank_full` shift-null co-metric is UNRELIABLE at M=60 (a NULL plant scored rank 0/24 = false
  significance) — so the real data's rank_full=1 is a spurious artifact, not signal; the frozen AND-gate
  (`sign≥0.55` AND `rank≤2`) is robust to it. Second sighting of the metric-regime lesson (H_011 LV-W, now
  H_012A rank_full) — recorded on `convergence run-h011-py-1`.
- **H_012B = LAUNCH-PENDING-CONSENT** (not a terminal): designed + the autonomous stubs shipped
  (`h012b_stub.py`: blinded consent prompt, eligibility classifier, privacy-enforcing logger with a content
  guard that raises, pre-committed LIVE/GHOST coin — 구현됨·미배선). Wiring into the live loop + owner
  enrollment is the human gate; only the real randomization can ANCHOR or interventionally REFUSE reframe C.
- SSOT: new `verification-h012` (+4 children: grounding-randomization · precheck · regime · launch-pending);
  REGISTRY H_012 = 🟡 (H_012A REFUSE · H_012B launch-pending); `convergence run-h011-py-1` recurrence noted.

## 2026-07-17 — H_011 stage B (7B) → 🟢 ANCHOR-ON-LV-C: the FIRST brain to clear the certified closure anchor — the campaign's first live positive

- Escalated the stage-B brain to **Qwen2.5-7B-Instruct (nf4)** on summer ($0, detached via `pool on --bg`).
  Result is QUALITATIVELY STRONGER than the 3B: the 7B **reads its input** (LV-P CR = 0.400) AND its
  contingency **fingerprints the block trajectory above the yoked floor** — **LV-C closure = 0.7625 ≥ 0.60,
  all 5/5 episodes** (the 3B was 0.500 ≈ chance, 2/5). It is the **first brain to clear the certified closure
  anchor.**
- It misses the co-gated one-step channel (**LV-W base_full 0.353 < 0.55**), which routed the frozen
  LV-W∧LV-C gate to LOOP-REFUSED. But that miss is an **instrument artifact, not a no-channel verdict** — see
  the tiebreak.
- **Tiebreak (`verdict-integrity` — verify the ruler on metric divergence; `state/.../result_tiebreak_lvw.json`).**
  LV-C PASS while LV-W FAIL is a divergence, so before any terminal I ran a **$0 / no-GPU** sweep of KNOWN-LIVE
  contingent plants across action entropy, reusing the certified `lv_w`/`lv_c` verbatim. A known-live plant
  **`mid3bal`** (H ≈ 0.97 bits, ~2 distinct actions, collision 0.52) reproduces the 7B's signature **exactly** —
  LV-W base_full **0.358 FAIL**, LV-C closure **0.762 PASS**. Below H ≈ 0.6 plants lose BOTH; above H ≈ 1.8 both
  pass. ⇒ **LV-W is UNDER-POWERED in the moderate-entropy regime the 7B occupies; its fail is QUARANTINED**
  (`infra-wall-noneval`). LV-C is entropy-agnostic (yoked-ghost control) and alone rejects a dead env (null-env
  closure = chance, cf. P-DEAD), so it **stands alone as the valid anchor.**
- **VERDICT = the 7B demonstrates rung-1 closed-loop CONTINGENCY on the valid instrument** — NOT "aliveness"
  (a thermostat clears rung 1), but the campaign's **first positive on the certified anchor**, and it
  **LICENSES the owner-loop RCT that H_010 priced** (`decision-reframe-c`'s owner binary now has its go-signal).
- **Convergence `run-h011-py-1` (cogate-metric-regime-blindness)** — a recurrence of H_009's instrument-regime
  lesson: a co-gate metric certified in only one regime silently mismeasures the one the subject occupies; on
  gate divergence, audit the ruler with a known-live sweep and quarantine the failing gate.
- **LV-W repair attempted → PARTIAL** (`run_h011.lv_w` `*_r`, restricted to INFORMATIVE ticks where the A/B
  intervention actually changed the action, so obs⊥action). It correctly keeps the dead null env REFUSED
  (base_full_r 0.241 — no false channel) BUT does **not rescue the mid3bal/7B regime** (base_full_r 0.446 <
  0.55). So the 7B's one-step channel is **genuinely weak** there (diffuse/delayed effects), not merely a
  collision artifact — LV-C (the block timescale) captures the same causation LV-W misses one-step. **LV-W
  stays QUARANTINED; LV-C is valid AND sufficient** (it alone rejects P-DEAD). SSOT node `h011-lvw-repair`.
- **Code:** fixed the stale `else`-branch verdict string in `run_h011.py` (it hardcoded "Qwen2.5-3B" and a false
  "closure < 0.6" even when closure PASSED); it now distinguishes the closure-fail vs LV-W-fail modes. Added
  `state/.../tiebreak_lvw.py` (entropy sweep + repair validation) and the regime-robust `lv_w` `*_r` arm. SSOT:
  `verification-h011` role + children `h011-lvw-underpowered`/`h011-lvw-repair`; REGISTRY H_011 → 🟢
  ANCHOR-INDICATED; card Verdict extended with the 7B section + tiebreak + repair.

## 2026-07-16 — H_011 stage B → 🔴 LOOP-REFUSED (localized to Qwen2.5-3B): the first LIVE interventional result — reading input ≠ closing the loop

- The instrument (stage A) was CERTIFIED first (P-LIVE anchor / P-OPEN channel-only / P-DEAD refuse). Stage
  B put a real LLM (Qwen2.5-3B-Instruct) in the driver's seat of the micro-tenant loop, on summer, $0.
- **VERDICT = LOOP-REFUSED (localized to this agent).** The brain **READS its input** — LV-P contingency
  rate **CR = 0.410 ≥ 0.20** (its action depends on what it perceives) — **but its contingency leaves NO
  closure fingerprint** above the marginal-matched yoked floor: **LV-C closure = 0.500 ≈ chance** (only 2/5
  episodes clear 0.60). In the SAME env a 20-line scripted homeostatic policy (P-LIVE) anchored at 0.75, so
  the env CAN show closure — the LLM's contingency simply is not strong/consistent enough. The agent sits
  BETWEEN P-OPEN (channel-only) and P-LIVE (anchored): **reading input is NOT sufficient for closed-loop
  causation.** A terminal-grade negative for Qwen2.5-3B greedy/memoryless in this rig.
- **Verdict-integrity save.** The first stage-B run read CHANNEL-MISSING; diagnosed (suspect the instrument
  first) as a DEGENERATE brain — RAW action-scoring collapsed to a constant action (COMPACT 40/40, CR=0.0),
  dominated by each action's model PRIOR, not the state. Fixed with **CONTRASTIVE (PMI) scoring**
  s(a|state) − s(a|neutral) (the state-free baseline, scored once, cancels the prior); the re-run's CR=0.41
  confirms the brain now genuinely reads its input. The env channel is stage-A-certified, so a stage-B LV-W
  miss = brain-degeneracy, never an instrument fault (`convergence brain-py-1`).
- **The interventional INSTRUMENT is certified** — it converts H_010's priced exit into the owner-loop RCT
  the moment any brain ANCHORS. Pre-registered escalations remain (the negative is LOCALIZED, not the
  campaign terminal): Qwen3-8B-4bit (bitsandbytes present on summer), persistent agent memory (rig #2),
  a richer env.
- **Infra (upstream-fix, not worked around):** the first run died (exit 255) because `sidecar pool on`
  reaps the remote process GROUP when the ssh session drops (orphan fence pool-ts-1) — fatal for a long
  job. Fixed at the cause in dancinlab/sidecar: **`pool on --bg`** detaches the remote command (setsid, new
  session) so it survives an ssh drop (PR #418, merged; the re-run dogfooded it).
- SSOT: `verification-h011` + `h011-licenses` updated to the stage-B verdict; REGISTRY H_011 = 🔴 FALSIFIED
  (localized); `convergence brain-py-1` (llm-policy-prior-collapse → contrastive PMI). tool/: `features` +
  `sqdist`/`median` promoted (3rd use). Rig: `env.py` · `brain.py` · `run_h011.py` (stage A + B).


## 2026-07-16 — H_011 live-ab-closure PRE-REGISTERED: the owner's pool makes the paid live loop $0 → reframe C's first card that can ANCHOR

- The owner asked "pool 에서 가능?" after H_010 priced the exit. `sidecar pool` has **summer** — an IDLE
  NVIDIA RTX 5070 (11.7 GiB free), torch 2.11+cu130 CUDA verified working, python 3.12, 65 GB disk. So the
  paid live A/B loop H_010 priced runs at **$0** on the owner's own hardware (a local model as the brain,
  no cloud). The campaign's binary ("fund the live loop or declare the terminal") had its "fund" made free.
- Delegated the design to Fable (`sidecar lab fable`); ran a 실측전 research pass (`sidecar research arxiv`)
  that CONFIRMED + JUSTIFIED the build: **empowerment** (Salge/Polani — potential/capacity, continuous
  estimation known-hard → discrete ≤8 actions), **counterfactual causal influence** (Jaques 2018 — the
  loop-gain η), **yoked control** (Watson 1972 — the ghost arm, a 50-yr-old solved design), and the
  transfer-entropy critique literature that INDEPENDENTLY predicts H_010's observational LOOP-REFUSED.
- **H_011 pre-registered + frozen** (`HYPOTHESES/cards/H_011_live-ab-closure.md`). The key move: the anchor
  gate is **CLOSURE, not "actions have effects"** (the echo/tautology trap). LV-C = Watson's yoked control
  as an RCT — the agent's CONTINGENCY STRUCTURE (not its action marginal) must leave a distributional
  fingerprint on its own input, measured against marginal-matched permuted-action GHOSTS. Because the
  executed action is RANDOMIZED (true vs matched-shuffle), P(I|do(A)) is identified — so this card, unlike
  every observational one, can **ANCHOR** (rung 1 = closed-loop causation exists + is measurable), not
  only refuse.
- Substrate = a deterministic MICRO-TENANT world (inbox queue · store · energy · hidden regime), 8 discrete
  GBNF-forced actions, a text-digest observation where action names never appear (all influence via
  dynamics). Brain (default) = local Qwen3-8B-Q4 via llama.cpp on summer, an exogenous logged action source
  (verdict replays from the log). Estimator = the CERTIFIED H_009'/H_010 shift-null LOO k-NN reused. Arms
  BASE/FULL/SHUF on randomized ticks. Falsifiers LV-W/C/P/E/N/L/R/G with yoked + open-loop (P-OPEN) + dead
  (P-DEAD) controls and a scripted P-LIVE that must anchor.
- **Stage gating (non-negotiable, the H_009 two-INVALID lesson): stage A** (`--plants-only`, NO LLM, LOCAL
  $0) certifies the instrument FIRST; **stage B** (summer LLM, ~1.5 h, $0) fires only on a clean stage A.
- An ANCHOR licenses RUNG 1 only (NOT "aliveness found" — a thermostat passes by design) + certifies the
  interventional instrument, which converts H_010's priced exit into the **owner-loop RCT** (randomized
  true-vs-matched-wrong agent utterance to the real owner) — the real target the campaign has circled.
- SSOT: `verification.verification-h011` (+4) + `reframe-c-first-step` updated (build underway). REGISTRY:
  H_011 = ⚪ PRE-REGISTERED. Design seed: `state/h011_.../DESIGN_fable.md`. Build (env.py · brain.py ·
  run_h011.py · promote features+LOO-kNN into tool/) + stage-A local certification is the next arc; stage B
  on summer needs the owner's go (installs llama.cpp + a ~5 GB model, ~1.5 h GPU).


## 2026-07-16 — H_010 loop-granger-gate → 🔴 LOOP-REFUSED (instrument CERTIFIED): reframe (C)'s $0 entry is closed; the exit is priced

- reframe (C)'s FIRST card. The interventional thesis (fired by H_009) needed a real LOOP — the
  owner<->agent conversation transcript, where the owner READ U_t and typed R_{t+1}, unlike the passive
  streams the observational phase exhausted. **Substrate measured: 16.7k loop pairs / ~130 sessions**
  (`~/.claude/projects/*/*.jsonl`, genuine-owner-typing filter) — ~160x H_009's pair count.
- **ASYMMETRIC verdict semantics (Fable Q1, frozen).** P(R_{t+1}|do(U_t)) is NOT identifiable from
  observational logs (context confounds every U->R), so no $0 result can ANCHOR causation — but causation
  implies dependence (barring the forbidden faithfulness appeal), so its ABSENCE kills the $0 entry. A
  REFUSE-capable SPEND GATE, exactly like H_004/H_006/H_009: **GATE-OPEN** licenses a paid live A/B build;
  **LOOP-REFUSED** closes the $0 entry; **ECHO-ONLY** = copy channel; **INSTRUMENT-INVALID** = plant fail.
- **VERDICT = LOOP-REFUSED** ($0, GPU 0, N=2000 + disjoint replication). On BOTH strides the true utterance
  is the WORST predictor of the owner's next reply: **sign(err_TOPIC > err_FULL) = 0.366 / 0.346 << 0.55**
  — a topic-matched WRONG utterance predicts R_{t+1} BETTER than the true one (63-65% of pairs); even
  owner-state alone (BASE) beats FULL (sign_base_full 0.406/0.437). LC-1 + LC-2 fail; LC-3 shows the tiny
  unstripped/stripped gap is no echo effect. The agent's specific utterance carries NO utterance-specific
  predictive info about the owner's reply beyond the TOPIC — the owner replies on-topic to anything
  relevant. The L2 replacement / F3 topic-decoration pattern, now measured on a REAL interactive loop.
- **Instrument CERTIFIED** = the certified H_009' shift-null LOO k-NN reused (features, distRt+distU
  precompute; the 4 arms BASE/FULL/TOPIC/XSESS are a distU first-axis remap), echo-stripped primary target,
  within-session shift-null. C-5 three buried-signal plants PASS: **P-POS** gate-open 1.000, **P-NULL**
  refuse 0.523, **P-ECHO** echo-only 0.656 -> 0.516. Each fixed a distinct plant defect found in
  validation (Euclidean signal-dilution, action=sidx entanglement, recurring-quote clustering). **LC-4
  (XSESS)** was demoted from a hard gate to a reported diagnostic (pre-freeze) — it is confounded by query
  dimensionality (BASE 256 vs U-arms 512) and conversation-position correlation, and the 3-plant liveness
  already supplies the leak protection.
- **Consequence: the exit is PRICED, not the campaign terminated.** A $0 observational REFUSE is not the
  interventional null (`reframe-c-discipline`); it removes the free entry and forces a binary the OWNER
  must decide: **fund the minimal live A/B loop** (a sandboxed environment loop, true-action vs
  shuffled-action, ~1-2 days + <$20, research-gated) **or declare the budget-bounded terminal** — aliveness
  was not measurable as a static property on any $0 substrate (8 families) AND the interventional
  reformulation has no $0-anchorable form even in principle (`cr-interventional-entry-asymmetry`).
- SSOT: `verification.verification-h010` (+4) + `convergence.cr-interventional-entry-asymmetry`; updated
  `decision-reframe-c` + `reframe-c-first-step` (first move RAN = REFUSED). REGISTRY: H_010 = 🔴 FALSIFIED.
  No new tool/ primitive (reuses `run_h009` machinery). Note: the substrate live-appends the running
  session (~1-pair drift between runs); the verdict is miles from threshold and robust.


## 2026-07-16 — H_009 f3-continuous-oracle → 🔴 F3-CONTINUOUS-REFUSED (instrument CERTIFIED): the last F3 organ premise dies at $0 → reframe (C) FIRED

- Ran the (B)-gate card. Verdict = **F3-CONTINUOUS-REFUSED** ($0, GPU 0). The continuous rank-k code
  DOES capture the day→tomorrow ceiling (both streams clear the gate + the 0.25 anchor: anima
  capture(8)=**1.007**, hexa **0.849**) and beats the topic floor ON AGGREGATE (cap−topic **+0.29** /
  **+0.14** > ε_f) — **but the per-pair sign(err_topic > err_s) is ≈ 50%** (anima **23/43** < 28-needed;
  hexa fully-certified **52/101** < 60-needed). C-2 fires: the s-over-topic advantage is concentrated in a
  MINORITY of day-pairs = a *sometimes*-day-specific code, not a pervasive day-specific self (the L2
  replacement-not-coupling distinction C-2 was frozen to draw — the topic-nearest OTHER day predicts
  tomorrow as well as the day's own summary on ~half of days).
- **Instrument integrity (two INVALIDs caught + fixed BEFORE any verdict — verdict-integrity).** (1) The
  frozen byte-append path is decoder-blind (gzip/markov/ppm are literal byte models; an abstract
  projection code reads capture≈0 regardless of truth) — Fable Q1 CONFIRMED, corrected to FEATURE space.
  (2) The first feature-space instrument returned INVALID from two estimator defects Fable root-caused:
  **A** — when k ≥ n_train−1 the top-k axes span the training subspace, so a test query's orthogonal
  residual is a per-query constant that cancels in the k-NN argmin → err_s ≡ err_full → capture ≡ 1.0
  MECHANICALLY (verified exact at k=32,64); **B** — a constant-mean denominator + K=3 + a 60/40 split made
  err_full noisier than err_base (ceiling_strength < 0) → estimator variance, not substrate.
- **H_009′ fix (Fable design, I implemented + ran):** shift-null LOO capture — capture(k) =
  align_s(k)/align_full where align_X = median_shift err_X − err_X(aligned); the estimator's variance
  penalty is identical in aligned and shifted runs, so it cancels. LOO over ALL pairs, K=5, valid-k only.
- **Instrument CERTIFIED** (C-3′ liveness, 3 buried-delay-line arms, matched n): HIGH (planted-weak) PASS
  both n; FAIL (iid noise) gate-fails both n; **LOW** (20 delay-taps of one logistic scalar buried under 8
  higher-variance decoys — the orthogonal-plant negative control is UNBUILDABLE under Euclidean k-NN, and a
  rank-truncation plant is too) reads capture(k≤8) ≤ 0.25 PASS at n=102. 5/6 falsifiers PASS. RESOLUTION
  limit (measured, robust across constructions): LOW certifiable only at n≥~100 → **hexa-lang = PRIMARY**,
  anima = REPLICATION; the REFUSED basis (per-pair sign) is magnitude-blind, hence resolution-independent.
- **Twin NOT licensed.** Spending past a certified null is the forbidden "maybe the decoder finds it"
  appeal (pre-commitment · L8). cr-distributed-lesson held: the $0 precursor killed the ~$15 twin.
- **reframe (C) FIRED.** Both F3 operator classes are now dead at $0 (byte-selection H_006,
  distributional-projection H_009), and every observational family (F1–F8) tested aliveness as a STATIC
  property of a PASSIVE stream — that premise is terminally exhausted. **New ACTIVE thesis = INTERVENTIONAL
  closed-loop causation**: alive iff the agent's own utterance shifts its SUBSEQUENT INPUT statistics above
  a matched floor on a REAL loop. Both Fable delegations independently confirmed the REFUSED path.
- SSOT: added `verification.verification-h009` (+5 children) + `decision.decision-reframe-c` (+3 children:
  why · first-step · discipline); updated `decision-redecide-h008*` (pick/h009-spec/reframe → fired) and
  `components-selection-status` (all 8 families resolved). REGISTRY: H_009 = 🔴 FALSIFIED. tool: no change
  (used existing `principal_axes` / `singular_values`).


## 2026-07-16 — Campaign re-decision post H_008: the $0 phase is a TRUE terminal, but ONE $0 card remains → (B) gated spend

- Fable 5 re-decision (delegated) over the exhausted frontier. Verdict on the campaign SHAPE: the $0
  OBSERVATIONAL phase is a genuine terminal (every branch's liveness PASSED text-like; the refusals are
  STRUCTURAL — PR 1.75, direction +0.004, ppm −0.117 — not proxy-sensitivity failures), but sealing "no
  aliveness premise survives, period" would launder 3 UNMEASURED residuals into a verdict.
- Per-residual triage (belief-killed-or-earned per dollar): **F3 continuous-m ALIVE** (H_006 killed only
  the byte-SELECTION text bound; a learned DENSE code POOLS distributed MI — a different operator class,
  so the ~83KB-distributed-MI wall does not bound it); **F7/F5/F8 owner organ DEAD** by the frozen
  F7-kill (both grains measured — relitigating is the L8 disease; reopen = a NEW substrate, not compute);
  **F6 init-seed** killed by 실측전-research (deep-ensemble = known generic variance reduction); **F4
  curriculum-order** weak+generic (training-efficiency, not identity).
- **Decision = (B) gated spend** (complete+std champion): pre-register + run **H_009 f3-continuous-oracle**
  ($0, deterministic) — a k=64 continuous SVD day-summary vs shuffle floor AND a topic-matched other-day
  floor (folds in f5's last open $0 item as F3's decoration control). KILL over-floor ≤ 0.02 OR ≤
  topic-floor + 0.02 → campaign terminal + fire (C). ANCHOR ≥ 25% of the +0.27 ceiling AND beats the
  topic floor → licenses the ~10M continuous-m twin (~12h MPS / ≤$15 cloud).
- **(C) reframe PRE-REGISTERED** as the refusal terminal (verdict-before-run avoided): the 8 families
  shared a hidden premise — *aliveness = a static structural property of a passive existing stream,
  detectable without the agent acting*. If H_009/twin refuses, the next thesis is INTERVENTIONAL: alive
  iff the agent's own utterance measurably shifts the statistics of its subsequent INPUT stream above a
  matched no-agent/scrambled floor on a real loop.
- SSOT: added `decision.decision-redecide-h008` (+ 7 children: walls · f3-alive · f7-dead · f6f4-dead ·
  pick · h009-spec · reframe).


## 2026-07-16 — H_008 frontier-fanout → 🧱 FRONTIER-EXHAUSTED: the $0 structural-analysis phase is COMPLETE

- Fanned out (`/abg` → one Workflow, 4 isolated worktrees, GPU 0) the four live frontier families the
  F1/F3 terminals left, each a $0 premise-check with a text-like liveness control (the H_007 fix):
- **f7 owner-clean → 🔴 REFUSED** — RESOLVES + CORRECTS H_007's borderline. With the liveness rebuilt
  text-like (now PASSES: markov3 +0.224 / markov8 +0.476) and BOTH grains measured, the owner is
  **legible XOR high-dimensional, never both on the same grain**: per-session PR **2.29** but not
  legible; per-day legible (markov3 **+0.145**, markov8 **+0.176**) but PR **1.75** (one-bit). The
  F7/F5/F8 owner-substrate premise is REFUSED — the v1 `l1-one-bit-seam` re-measured on the real owner.
- **f5 trajectory → 🟡 F5-WEAK** — the recent past accumulates (growth **+0.106** > ε) but time is
  SYMMETRIC (direction signal **+0.004** ≤ ε): a topical window / smooth drift, not a directed
  arrow-of-time self. F5 adds a recency window over F7 but no directed trajectory.
- **f6 shard-ensemble → 🟡 BORDERLINE-leaning-REFUSED** — shuffle-corrected shard specialization is
  small and NON-ROBUST across capacity (4k **+0.048**, 16k **−0.086**, 64k **+0.050** — sign-flips);
  the raw oracle lift +0.159 exceeds the perfectly-separable ceiling +0.029 = mostly oracle-min
  artifact. The matched-capacity monolith in-context-adapts to the domain (the L11 superset argument).
- **f4 curriculum-headroom → 🔴 REFUSED (L11)** — raw selection headroom is real (+0.211 bpb) but
  decoration: markov6 (the selection estimator) says the oracle beats the frozen 6-gram retriever
  +0.117, but the INDEPENDENT ppm says **−0.117** (retriever ties/beats). Corpus selection is the L11
  frequency tautology in its corpus outfit — the F4 half of `fd-write-lever-pair`, exactly as warned.
- **Campaign result**: the **$0 structural-analysis phase is COMPLETE** (7 solo cards + 4 fan-out
  probes, GPU 0). Write-lever (F1/F4) terminated by L11 on both hands; owner families (F7/F5/F8)
  REFUSED; F3 diary spent; F6 borderline-refused. Remaining residue is compute-bearing and
  premise-weak — the honest next move is a campaign-level re-decision, not another $0 card.
- SSOT: added `verification-h008` (gate + 4 branch children + campaign result) and the convergence
  record `cr-zero-cost-frontier-exhausted`; corrected `verification-h007` to note it is superseded.
  New card `HYPOTHESES/cards/H_008_frontier-fanout.md`; registry H_008 added, H_007 marked superseded.


## 2026-07-16 — H_007: the owner-substrate is real + $0-checkable; F7/F5 premise reads borderline weak-positive

- Discovered a REAL owner-agent interaction stream on disk: `~/.claude/projects/*/*.jsonl`, ~51 MB of
  genuine owner typing across 769 sessions (241 usable ≥ 6144 B). This materially changes the campaign's
  resume: the remaining `fd-true-axes` families that live on the owner substrate (F7 curiosity, F5
  trajectory, F8 owner-model) are NOT compute-blocked — they are $0-checkable here.
- Pre-registered + ran `H_007 f7-owner-legibility` ($0): does the owner's message stream carry
  predictable, HIGH-DIMENSIONAL cross-session structure (the premise F7/F5 need)? Privacy-preserving —
  no owner content written to the repo, only aggregate bpb/rank numbers.
- Verdict **PENDING / BORDERLINE-WEAK-POSITIVE**: cross-session legibility (markov6 over-floor) =
  **+0.0207** (ε = 0.02) and owner-self participation ratio = **2.27** (floor 2.0) — both RIGHT AT
  their pre-registered thresholds. The owner (terse directive commands) is a legible, more-than-one-bit
  other, but barely — nowhere near anima's F3 signal (+0.22).
- PENDING (not ANCHORED) because the markov6 liveness control read negative on the high-entropy synthetic
  planted stream — diagnosed as an ESTIMATOR artifact (gzip liveness passes at +6.66; real text is
  low-entropy where markov6 works), not an owner finding. The liveness must be rebuilt TEXT-like before
  the markov6 owner number is fully trustworthy.
- Resume: rebuild the liveness as a text-like planted stream + ppm confirm + a finer temporal grain
  (per-day, not per-session-file); if the premise holds above threshold → F7/F5 LIVE (design the organ,
  which needs a trained owner-model = real compute); if it collapses → the owner-substrate corner joins
  the terminated pile.


## 2026-07-16 — H_006 RUN → 🔴 F3-BOUNDED-REFUSED: the diary twin cancelled at $0 (distributed MI)

- Fable designed the F3 diary twin (H_007) and — crucially — a $0 precursor that GATES its ~12h training
  spend: `H_006 f3-bounded-oracle`. Pre-registered, ran it, verdict **F3-BOUNDED-REFUSED**: the twin is
  CANCELLED before it cost anything. Research-before-real-measurement working a third time.
- Per day-pair, each line of day t was scored by marginal gzip lift; the hindsight top lines up to budget
  k were taken; ceiling(k) measured with markov6 (ppm confirm) vs the H_005 shuffle floor. Line-structured
  planted liveness PASSED (0.366). 144 oracle extracts emitted.
- **A hindsight k≤4096-byte text extract retains only ~4% of anima's +0.27 full-day ceiling** (over-floor
  +0.012 markov6 / +0.019 ppm at k=4096, both < ε=0.02; hexa-lang likewise below ε). The day-specific MI is
  DISTRIBUTED uniformly across the whole day (median 83 KB) — 5% of the bytes carries ~4% of the ceiling —
  not localizable into a small diary. A hindsight top-lines selector is a LOWER bound on any bounded diary,
  and it captures almost nothing.
- **Honest scope**: KILLS F3's PRIMARY formulation — a k-TOKEN readable-text diary (F3.how: "m hard-
  bottlenecked to k tokens"). Does NOT cleanly kill a CONTINUOUS learned bottleneck (the k-dim-vector
  variant, a higher bound not directly measured) — but the distributed-MI finding is a real headwind, and
  the twin as Fable designed it is undermined regardless (its oracle arm = these text extracts, now
  near-floor, so it could not anchor a meaningful delta_min).
- The F3 DIARY line is SPENT at $0 — the third campaign line terminated by cheap structural analysis (after
  F1's terminal and the write-lever axis). Recorded convergence law `cr-distributed-mi-not-bottleneckable`:
  an anchored UNBOUNDED MI does not imply a BOUNDED diary can capture it; always gate the bottlenecked
  mechanism with a $0 bounded-extract precursor before training.
- Bugs fixed en route (caught by controls): H_005's planted stream has no newlines so the line extractor
  couldn't test it → added a line-structured planted liveness (PASS 0.366); and the per-k re-ranking
  slowdown → rank lines once per pair, reuse across estimators.
- Two artifacts also saved: `NOTE_diary-size-precursor.md` (the $0 pre-check that motivated H_006) and
  `DESIGN_fable_twin.md` (the full H_007 twin design, now cancelled). Registry: H_006 🔴.


## 2026-07-16 — H_005 RESOLVED → 🟢 ANCHORED: F3 is licensed (the campaign's first pre-anchored effect size)

- Resolved H_005 from PENDING(instrument) to **ANCHORED (F3 licensed)** at $0, by building the efficient
  order-6 Markov estimator — the THIRD of the pre-registered battery. The mean-pooled `nlm.py` cannot
  represent a long-range token (wrong tool) and a higher-order PPM was intractable; the order-6 Markov is
  order-aware and runs at $0 (19s/stream). Substitution logged, not silent.
- **anima clears the STRICT pre-registered P-4** — all three estimators sign-agree AND over ε: gzip +0.031,
  ppm +0.221, markov6 +0.043 over-floor (all > ε=0.02, all positive). NO gzip exemption, no goalpost move —
  anima passes the original bar. hexa-lang confirms on the two order-aware estimators (gzip sits at its LZ
  resolution floor there — its 32KB window is insensitive to a single day-specific long-range token, exactly
  what the earlier PENDING correctly flagged and this estimator resolves). sidecar (21 days, thin) is flat —
  an under-powered null, not informative.
- **F3 is LIVE — the opposite of the F1 structural terminal.** A developer's stream carries a day-specific
  temporal self a diary could transport (a project's ongoing state lives across days, outside any single
  day's tail). The F3 twin escapes L11 structurally (the bottleneck m sits outside the context window).
- **First pre-anchored delta_min ever**: delta_min := ceiling/2. The sign (F3 live) is robust across all
  three estimators; the magnitude is estimator-dependent (anima over-floor 0.03–0.22 bpb), so delta_min is a
  range [~0.015, ~0.11] with a conservative floor ~0.02 bpb — the twin's own oracle arm pins the point.
- RESUME (live frontier): design + run the F3 DIARY TWIN — a diary bottlenecked to k tokens, loss =
  CE(tomorrow | today's diary), vs a no-diary control, delta_min ~0.02 bpb floor. This needs the campaign's
  first genuine training compute (a small causal LM), now justified by the anchored premise (실측전-research
  satisfied). Optional $0-cheap strengthening first: a causal-LM confirm on hexa-lang upgrades the anchor
  from "one strict + one order-aware" to "two strict".


## 2026-07-16 — H_005 RUN: F3's premise is LIVE ($0) — the opposite of the F1 terminal

- PRE-REGISTERED + FROZEN `H_005 f3-stream-mi-precheck` and RAN it ($0, deterministic, no GPU). Verdict
  **PENDING(instrument), scientifically LEANING ANCHORED** — F3 is LIVE, the opposite outcome to F1's
  structural terminal.
- Measured the oracle-diary ceiling (bpb of day t+1's prefix given day t's tail vs tail+full-summary)
  against a shuffle floor (day-adjacency broken) on three real developer git streams (hexa-lang 102 days,
  anima 44, sidecar 21), with two independent $0 estimators: gzip (LZ) and an order-4 adaptive byte model
  (PPM). The planted-latent liveness control read 7.79 bpb (instrument sees cross-boundary MI — PASS).
- Under the sensitive PPM estimator the two richer streams show a real day-specific cross-boundary lift
  above the shuffle floor (hexa-lang +0.143, anima +0.221 bpb), with positive day-specificity swap controls;
  sidecar (thin, 21 days) is flat. gzip sits at its noise floor and reads ~0 on hexa-lang → the pre-registered
  P-4 (estimator sign-agreement) trips → formal verdict PENDING(instrument).
- Honest reading: the disagreement is gzip's RESOLUTION floor, not a real conflict — its 32KB LZ window is
  insensitive to a single day-specific long-range token in a large context, where PPM sees it. The scientific
  lean is ANCHORED: a developer's stream plausibly carries a day-specific temporal self a diary could
  transport (a project's ongoing state lives across days, outside any single day's tail). That would license
  the F3 diary line with a pre-anchored delta_min = ceiling/2 — the campaign's first honestly-anchored effect
  size — and the F3 twin escapes L11 STRUCTURALLY (the bottleneck m sits outside the context window).
- Two bugs fixed en route (both caught by the pre-registered controls, not by luck): the git-day chunker
  parsed 106 days as 2 because hexa-lang's diffs carry binary null bytes that corrupt delimiter parsing —
  switched to messages + `--name-only` file paths (pure text, a faithful "what did the developer work on"
  stream); and the planted-latent liveness control initially read ~0 because the predictive block sat IN the
  tail, not beyond it — corrected, now reads 7.79 bpb.
- PARKED F1's restated verbal form as ABSTRACT card `H_A001 f1-codec-credit-span` (🜂, no run, no verdict):
  refit beats frozen on GENERATION only where a productive process's parameter lives outside any context
  window and the gap does not shrink with model scale — a falsifiable prediction that overlaps F3's escape.
- RESUME (live frontier, next session): decide the estimator question — accept PPM as authoritative →
  design the F3 diary twin, or run a small causal-LM tie-breaker (the mean-pooled nlm.py is the wrong tool)
  to satisfy P-4 formally. Either way F3 is not refuted.
- Artifacts: `run_h005.py` + `result.json` (dual-estimator, all streams, liveness). Registry: H_005 🟡, H_A001 🜂.


## 2026-07-16 — campaign re-decision: F1 yields, F3 promoted, L11 sealed

- The campaign re-decision (Fable) after the H_004 terminal: **F1 is done — spent as a measurable claim,
  not falsified as a metaphysical one** — and the WRITE-LEVER axis yields with it. Every proposed F1
  survivor (generation · refit-under-drift · long-range depth) is L11's frequency tautology in a costume;
  the restated verbal form is parked as an ABSTRACT card, not another rig.
- SEALED **L11 — fusability IS recoverability** (`salvage.l11-*`), the campaign's FIRST v3-earned law (earned
  here at $0, not inherited from v1): for any FIXED frequent pattern, the property that lets an adaptive codec
  dedicate a unit to it (frequency × fixedness) is the same property that lets a frozen system read it with a
  low-order n-gram. Corollary A (adaptivity only pays on non-fixed patterns / spans beyond reach — where
  adaptation also starves), B (measure the control's trivial-statistic ceiling BEFORE training — the lookup
  battery, extends L6), C (relabel: v1 measured low-order exposure, not atomicity), and the design consequence
  (a lever is isolable only via a STRUCTURAL BOUNDARY — info physically absent from the visible context —
  never inventory/frequency engineering).
- AXIS RE-DECISION (`decision-redecide-h004`): F3 (diary) — the pre-registered second card — is promoted to
  first, on belief-killed-per-dollar. F4 has a bad rig (repeats H_001's unanchored-null disease). F6 is DENTED
  (its reproduction mutates the codec = the non-separable lever) and SUSPENDED pending a new variation axis.
  F3's two known diseases now have H_004-shaped cures: measure the stream's MI FIRST (premise before organ),
  and the eventual twin escapes L11 structurally because the transported info sits OUTSIDE the context window.
- NEXT CARD: `H_005 f3-stream-mi-precheck` — $0-deterministic + cheap numpy proxy, measuring whether any
  available experience stream (dancinlab git history, owner logs) carries cross-boundary information for a
  diary to transport. The hindsight-optimal k-token summary is the oracle-diary CEILING, doubling as the
  campaign's first pre-anchored delta_min (institutionalizing the H_004 lesson). A null retires F3 + F8's
  diary premise for $0; a positive is the first honestly-anchored delta_min.
- Seed of record: `state/h004_static-anchor-pilot_2026-07-16/DESIGN_redecide.md`.


## 2026-07-16 — H_004 STRUCTURAL TERMINAL: atomicity is not isolable from n-gram binding ($0, no GPU)

- The F1 reframing analysis (Fable) + a $0 guard battery drove H_004 to a **structural terminal**:
  **TWIN-REFUSED**, reached without firing the torch/MPS run. This is research-before-real-measurement
  and break-walls working as intended — a GPU pilot pre-empted by deterministic analysis.
- HONESTY CORRECTION first: my earlier proxy claim "27/27 fragments neg-exclusive" was OVERSTATED
  (I checked plain affixes, not plain bodies). Fable's adversarial re-check + my re-verify: 25/27
  fragments are SHARED; the leak was POSITIONAL (a last-token Bayes lookup scores 0.9993), not
  type-exclusivity. Corrected in the SSOT (`h004-defect-exclusive`).
- REFRAMED F1's lever (`h004-reframe-*`): not "atomic token" nor "class-exclusive fragment" but the
  ORDER of the statistic needed to read the class. Raw utf-8 (~18-byte binding = high order) fails;
  a frozen codec concentrates class into order-1 (final token); an atomic codec is order-1 by
  construction. Atomicity is a special case of low-order class exposure.
- RELABELED MORPH-ATOM in the SSOT (`l4-morph-atom-relabel`): M=0.908 vs C1=0.617 STANDS as a
  measurement, but it established "class concentrated into a low-order feature is causal", NOT
  "single-token atomicity is the lever" — no arm ever contrasted atomic vs fragmented-but-low-order.
  Demoted `slot-not-address` (`l4-slot-transfer`): under a last-token lookup the decision never
  consults the stem, so C2's stem-deletion invariance is predicted by the shortcut.
- REPAIRED the generator (donor-pair novel allomorphs = two 1-syllable carried plains concatenated;
  frequency balancing; matched pos/neg final-token distributions). Frozen can never fuse the pair
  (never adjacent in phase 1) → atomicity deficit 1.0 GUARANTEED. genspec `2016a4ee`→`fbcf0c8`→`75b19bba`.
- The repair worked at order-1 (G-A 0.527, G-B 0.551) but the guard battery found the terminal:
  **G-C order-2 bigram lookup = 0.9954**. THEOREM (verified 12/12): **oracle-fusable ⟺
  n-gram-recoverable** — for the oracle to atomize an allomorph it must be a frequent FIXED sequence,
  whose terminal n-gram the frozen codec then recovers. Atomicity is NOT separable from n-gram binding
  for a fixed morpheme (a fact about BPE, not a rig defect). A transformer binds order-2 trivially, so
  Δ_pilot ≥ 0.20 is structurally impossible.
- CAMPAIGN RESULT (`cr-atomicity-not-isolable` in convergence): a static codec's order-≤2 fragment
  statistics already deliver the write-lever's RECEPTIVE value; a refit organ buys nothing measurable
  here. A synthetic drill can never prove "atomicity helps" against an n-gram-binding transformer. The
  honest F1 question moves to GENERATION / long-range credit / continual-interference, or F1 yields
  first place — per `rig-sequence-h004-kills`, a campaign re-decision, not a silent switch.
- Artifacts: `run_guards.py` + `guards_result.json` (the $0 verdict), `run_proxy.py` +
  `proxy_result.json` (the pre-check), `nlm.py` (validated numpy LM), `materialize.py`,
  `DESIGN_reframe.md` (verbatim Fable). H_004 card verdict = STRUCTURAL TERMINAL; registry = 🔴.


## 2026-07-16 — H_004 pre-registered; a $0 numpy pre-check BLOCKED the GPU run and reframed F1

- PRE-REGISTERED + FROZEN `H_004 f1-static-anchor-pilot` (Fable design): the campaign's first
  non-$0 measurement — Δ_pilot = F2(oracle codec) − F2(frozen codec) on held-out flips, the CEILING
  of the codec effect (oracle ≥ refit by construction). Δ_pilot ≥ 0.20 licenses the H_002′ twin with
  delta_min = Δ_pilot/2; below it the twin is REFUSED. 5 runs, 4.9M transformer, forced-choice mark
  prediction, 7 falsifiers. Fable's compute finding: **no GPU needed** — ~4 PFLOP total, MPS overnight
  at $0 (<$2 RTX-4090 fallback).
- Built the pieces every training path needs: `src/generator/materialize.py` (encode phase streams +
  eval items to token ids under a codec — establishes codec-fairness once), and a validated numpy
  neural LM (`state/h004…/nlm.py`, gradient-checked to 4e-11, learns a periodic seq to loss 0.037).
- **The $0 pre-check caught a rig-invalidating defect before any spend** (`run_proxy.py`, 55s):
  **Δ_proxy = −0.048** — the FROZEN arm (F2=0.971) BEAT oracle (F2=0.923), both far above chance. The
  expected oracle >> frozen did not appear. This is research-before-real-measurement working exactly as
  intended — the defect surfaced in 55 seconds of CPU, not after a GPU run producing a misleading
  Δ_pilot ≈ 0 that would have been misread as "F1 refuted".
- Root cause, verified two ways independent of the weak model: the 12 novel NEG allomorphs come from a
  DISJOINT inventory, so under the frozen codec they fragment into 27 tokens that are ALL neg-exclusive;
  the LAST token alone separates NEG from PLAIN with 0 overlap. So the held-out flip is solvable by
  FRAGMENT-LOOKUP — no recombination, no atomicity — at ANY scale. Δ_pilot ≈ 0 would be a RIG DEFECT
  (frozen control too strong), not evidence about F1.
- **This reframes F1 itself.** MORPH-ATOM measured codec vs RAW utf-8; raw utf-8 failed (C1=0.617)
  because bytes are MAXIMALLY shared — no sub-unit carries class. A frozen BPE that only FRAGMENTS the
  morpheme but keeps fragments class-exclusive recombines fine. So the lever L4(b) measured may be
  REPRESENTATION-NON-SHARING, not single-token ATOMICITY — which would demote F1's central thesis to a
  special case, and means a refit organ may buy little over a good static codec. Handed to a Fable
  reframing analysis (Q1-Q5: is F1 reframed · is the rig fixable · does the kill logic change · was
  MORPH-ATOM mislabeled · is F1-first still right).
- Recorded in the SSOT (`verification-h004`, `rig-pilot-frozen-control-invalid`) and the H_004 card's
  verdict (PRE-CHECK BLOCKED). The torch/MPS run is blocked pending the rig fix + reframing verdict; the
  card is repaired-in-place when they land (as H_003 was). Registry: H_004 = ⚪ blocked-on-rig-defect.


## 2026-07-16 — H_003 REPAIR → 🟢 rig = LICENSED (10/10): the N-2 wall broke, F1 has a substrate

- Broke the N-2 contrast wall and re-ran H_003 to **rig = LICENSED (10/10)**. The H_004 static-anchor
  pilot may now fire. The wall was NOT "atomicity can't be induced synthetically" — it was three concrete
  generator defects, each found by direct experiment (not argument) and each measured:
  1. **Short affixes atomize by accident.** A 1-syllable NEG allomorph is 2-3 jamo; its jamo recur so
     widely that the FROZEN codec fuses it unseen (the novel form `조` read single-token in phase-1). Fix:
     novel NEG allomorphs are now ≥2 syllables (≥6 jamo). Frozen 8/12 → 0/12.
  2. **The polarity mark was fusing with the affix** — the real refit blocker, hidden behind the frequency
     question. The mark was glued to the affix, so BPE fused `affix+mark` as one merge and the affix never
     became a single token — refit stalled at 3-5/12 at ANY K (unchanged at K=4096). Fix: the mark is a
     separate sentinel-delimited token. Refit → 12/12.
  3. **Novel allomorphs must be frequency-earned.** At their natural ~450/20k rate they are below BPE's
     merge threshold against 64 competing affixes. Fix: phase-2 over-weights novel allomorphs
     (`NOVEL_NEG_SHARE_P2 = 0.80`) — not a thumb on the scale but the drift itself (the phase-2 language
     uses its new negators heavily), which is v1's NAT-ATOM law that atomicity is earned by repetition.
- Result at K=512, real pipeline: frozen **0/12** (deficit 1.0), refit **12/12** (deficit 0.0), drift
  0.1256, leak 0, co-occurrence 0. Anchor half all green throughout (B-1..B-4). K lowered 2048 → 512 (the
  smallest passing the mechanism gate; the original 2048 could not produce the contrast at any value).
- **N-4 was never a corpus leak** (`leak_hits` always 0). The co-occurrence count was a detector defect in
  two layers: parse-ambiguity (fixed by keying off the emitted polarity mark — a NEG-marked word is ground
  truth), AND a **duplicate function definition** leaving a stale substring-based version shadowing the
  fixed one (Python uses the last def, so the fix appeared not to take until the stale copy was removed).
  Co-occurrence now 0 at 200k-line scan depth.
- Re-froze the card on the repaired spec (`genspec_sha256 fbcf0c8…`, was `2016a4ee…`) — the card's own
  rule is "REFUSED until the named defect is repaired", and this is that repair, logged not silently
  re-frozen. The prior REFUSED run is kept in the card for the record.
- Fable delegation for this repair returned only "waiting on the verification run" (no design) — the fix
  was derived and verified locally by direct experiment instead. Every claimed cause was reproduced before
  the fix and confirmed after (the mark-fusion cause via a marks-on/marks-off A/B; the duplicate-def cause
  via inline-vs-function disagreement).


## 2026-07-16 — H_003 RUN → 🔴 REFUSED (8/10): anchor GREEN, generator hits a real wall

- Built the synthetic drill generator (`src/generator/`, deterministic · stdlib · $0): jamo composition
  (`lang.py`, Hangul's algorithmic syllable block supplies the composition rule, vocabulary invented),
  a frozen `GenSpec` (`spec.py`, sha256 `2016a4ee…` pinned into the H_003 card — 512 stems, 128 held-out,
  64 phase-1 affixes / 4 NEG, phase-2 = 52 carried + 12 novel NEG allomorphs), phase streams + probes +
  eval items (`stream.py`), BPE-on-jamo codec + boundary/atomicity estimators (`codec.py`), leak audit
  (`audit.py`).
- PRE-REGISTERED + FROZEN `H_003 f1-anchor-recheck` (9 falsifiers B-1..B-4 anchor + N-1..N-5 generator),
  then RAN it. Verdict **rig = REFUSED (8/10)** — H_004 pilot BLOCKED. The two halves separated cleanly.
- **ANCHOR HALF ALL GREEN.** Correctly specified — test the treatment and liveness arms, keep
  control-at-chance as a SEPARATE leak test — MORPH-ATOM stands exactly as `salvage.l4(b)` claims:
  B-1 M=109/120 outside the band (p=1.9e-21) · B-2 C3=110/120 liveness · B-3 C1=74/120 inside band (no
  leak) · B-4 CEMENT replicate agrees. H_001's REFUSED-on-G-4 is now fully explained: the reading was
  backwards and the anchor was never in doubt. It is a two-seed result.
- **N-2 contrast is a genuine DESIGN WALL.** No K in {256,512,1024,2048} makes the frozen codec blind to
  the novel allomorphs AND the refit codec atomic on them — the refit deficit never reaches 0 (best 5/12
  at K=256). Cause: the affixes are 1-2 random jamo syllables, too rare in-stream for BPE to fuse into
  single tokens, so atomicity is not induced by the data in EITHER arm. The generator does not yet
  instantiate the mechanism it is meant to test. Recorded as `rig-atomicity-not-induced` with three forks.
- **N-4 co-occurrence = 2363 is an AUDIT false-positive, not a corpus leak** (`leak_hits = 0`). It is
  `parse()` finding an ambiguous (held-out stem + NEG) decomposition of a word the stream emitted as
  (non-held-out stem + PLAIN). Verified: `line()` emits 0 held-out+NEG words in 40k lines. The audit was
  moved from raw-substring → whole-word → parse-based over the session (each weaker form gave false
  positives); the residual is that an agglutinative language admits ambiguous parses, so the detector must
  score against the EMITTED parse, not any admissible one. An audit repair, not a leak.
- Deliberate deviation from the design spec, logged in `src/generator/CLAUDE.md`: boundaries are indexed
  in JAMO positions, not bytes — each conjoining jamo is exactly 3 UTF-8 bytes, so a byte-indexed matrix
  has 2/3 of its columns structurally zero and would deflate the boundary-shift rate ~3x. Jamo is the
  codec's base alphabet, so the index is still codec-independent (the actual requirement).
- Net: the anchor is settled (no future card re-litigates l4(b)); the pilot is blocked on a spec-design
  problem (make BPE-on-jamo actually induce atomicity). Handed to the successor spec design.


## 2026-07-16 — repair pass: three false premises corrected, a blind instrument fixed, a new salvage law

- **Corrected a FALSE PREMISE that the F1 selection rested on.** `rig-model` and H_001 both claimed 10M is
  "MORPH-ATOM scale, the scale at which the codec→recombination link was measured". The v1 verdict header
  reads `anima-py 303M CLMConvMoE d3784 L4 Emax4` — **nothing was ever measured at 10M-from-scratch**.
  H_001 read that header during G-5 and failed to connect it. `decision-attributability` is marked
  SUPERSEDED: its argument was false twice (wrong scale; and it anchored delta_min on the static half it
  had just declared common-mode).
- **`delta_min` = 0.15 has no valid lineage.** "Half of 0.291" transfers a number across three unbridged
  gaps: contrast (raw-vs-codec ≠ frozen-vs-adaptive), substrate (303M ≠ 10M), corpus (real Korean NSMC ≠
  synthetic). A null at N sized for 0.15 is therefore NOT attributable — H_001's REFUSED verdict was more
  correct than its own stated reasons.
- **An internal objection ("the static effect cancels between the arms, so the refit effect has no anchor
  anywhere") was itself REFUTED, and the refutation is recorded**: drift breaks the symmetry. The frozen
  codec's atomicity is a WASTING ASSET — phase-2's new affixes are absent from the phase-1 merge table, so
  on the drifted region the frozen arm IS a local C1 and the adaptive arm IS a local M. The costs
  (swap/retention/interference) are unanchored, and that is fine: they are what the twin ASKS, not a power
  assumption.
- **The rig has NO LIVENESS ARM** — a defect, not a gap. v1's precedent is direct: the S1 4-pod fire's
  C3 = 0.50 correctly converted four apparently-null arms into "four instrumentation bugs", which were then
  found. Fix recorded: a shared-ID collapse arm (C3′), rule F2(C3′) ≥ 0.90 else the run is INVALID not FAIL.
  The twin grows 11 → 12 runs.
- **Fixed a blind instrument, and the positive control that certified it.** `binom_pmf` computed
  `math.comb(n,k)` as an exact int and multiplied by a float → **OverflowError at n ≳ 1100**, so
  `chance_band(1178, …)` crashed — exactly the floor of the re-derived operating point. G-3 passed because
  its fixtures only ever exercised n=120, the regime already in use. **A positive control that only probes
  the regime you already trust certifies nothing.** Fixed in log space via `lgamma`; `chance_band` also made
  single-pass (it was O(n²) and unusable at panel scale). Fixtures 46 → 56, pinning n ∈ {1100, 1178, 2000,
  5000} and the degenerate rates. H_001 re-run under the fixed estimator: **byte-identical verdict** — the
  bug never touched it (verdict-integrity).
- **NEW SALVAGE LAW `l10-codec-swap-costs-the-embedding`**, recovered from the v1 record and missed by the
  divergence pass: a codec change makes the existing embedding an *actively wrong prior*, measurably worse
  than random init — gradient must first DESTROY the old alphabet's structure. 8k CPT across a swap bought
  discrimination but zero semantics (drill loss 0.009 with F1 = 0.50 = pure memorization); even the
  answer-handed C3 arm went dead. The fix that worked was reinit-embed surgery + ~20-25k gate-terminated
  steps. It is the sharpest live threat to F1 and it contradicts the design's ZeTT-based comfort.
- **Corrected the anchor: it is STRONGER than H_001 recorded, not weaker.** A CEMENT replication exists
  (2026-07-14, seed 7): M = 0.9167 vs C1 = 0.5750, **Δ = +0.3417** (original +0.291), M's replication
  deviation **0.009**, all arms V1 liveness PASS. H_001's "1 seed" limit was wrong. The replicate control
  0.5750 also sits inside the chance band — reinforcing that a control at chance is the expected reading.
  The C2 arm split the mechanism: the held-out stem **deleted from the CPT corpus** still scored 0.9167,
  so atomicity is a **structural slot, not a pretrained address** — the best reason to expect a 303M→10M
  transfer.
- **F1-first RE-DERIVED and SURVIVES**: the anchor defect is a rig disease, not an F1 disease, and F4 has the
  same disease with less immunity (equally unanchored effect, static v1-substrate evidence, plus the Goodhart
  probe-battery burden l6 flags as the jugular). F3 unchanged as the second card.
- **Revised sequence recorded** (≤ $35 total, each step with named kill-power): H_003 `f1-anchor-recheck`
  ($0, deterministic — bounds + generator + G-1 drift + G-2 emittability) → H_004 `f1-static-anchor-pilot`
  (≤$10, 5 runs — measures Δ_pilot = the hard upper bound on what refit can deliver, since oracle ≥ refit by
  construction; kill: Δ_pilot < 0.20 → the twin is REFUSED) → H_002′ (12 runs, delta_min = Δ_pilot/2). After
  the pilot, **no number transfers from MORPH-ATOM at all** — it serves only as the existence proof of the
  mechanism class.
- Power table re-derived from p0 = 0.50: delta_min 0.10 → N=1178/arm · 0.15 → N=510 · 0.20 → N=277. The
  fictitious 444 is retired. Compound rule pre-registered (pooled p < 0.01 AND median-over-seeds Δ ≥
  delta_min) because the item-level binomial ignores seed-level variance.
- Corrections logged onto the frozen H_001 card rather than edited into it — a frozen card that quietly
  rewrites its own limits is worth nothing.
- Seeds of record: `state/h002_f1-twin_2026-07-16/DESIGN_fable.md`,
  `state/h001_f1-codec-refit-gate_2026-07-16/NOTE_refit-tax.md`.

## 2026-07-16 — H_001 RUN → 🔴 rig = REFUSED (2/5), and the card caught its own defect

- RAN H_001's five falsifiers (`state/h001_f1-codec-refit-gate_2026-07-16/run_h001.py`,
  deterministic · stdlib · $0). Verdict **rig = REFUSED** — H_002 is blocked. A result, not a delay.
- **G-5 RESOLVED — the protocol was never lost.** The H_9288 recombination protocol is intact in the
  v1 repo (`anima`), the evidence trail the campaign itself designated. The card's claim that it was
  "specified nowhere" was true of *this* repo and false of the campaign — the blocker was a failure to
  look where the campaign said the evidence lives.
- The recovery **falsified two of the card's own frozen premises**: F2 is a FORCED-CHOICE flip accuracy
  with chance = 0.50, not a recombination F-score with an unknown chance rate; and n_items = 120,
  recovered exactly (the published rates are integer counts: 0.6167=74/120, 0.9083=109/120,
  0.9167=110/120). `chance_p0`/`n_items` were frozen as `?` pending G-5, so this is a legitimate
  resolution, not a post-hoc edit.
- **G-4 triggered — and its stated interpretation is a DEFECT IN THE CARD.** C1 control = 0.6167 sits
  inside the exact 99% chance band [0.3833, 0.6167] (p=0.0134), which G-4 reads as "L4(b) was never
  above floor". That inference is backwards: G-4 tests the CONTROL arm, and a control is supposed to
  sit at chance — a raw-utf8 baseline that could recombine would mean the setup leaks. **`salvage`
  l4(b) STANDS**: the claim rests on M = 0.9083 (p=1.9e-21) with C3 leak-ceiling liveness = 0.9167
  (p=1.9e-22) proving the harness can detect the effect. The write-lever axis is not demoted and F1
  remains correctly selected.
- The trigger still carries real information: since C1 is indistinguishable from chance, p_control =
  0.617 is not a baseline capability but noise, so G-2's operating point (p1=0.6167 → p2=0.7667,
  N ≥ 444/arm) is fictitious and must be re-derived from p0 = 0.50.
- **G-1/G-2 are UNEVALUABLE**: the jamo-drill generator the card presupposes does not exist. An
  unevaluable gate cannot return PASS (`break-walls` — under-invest is a wall, not a verdict).
- Recorded that the v1 anchor is WEAKER than the design assumed: 1 seed, n=120 (underpowered by its own
  admission and against its own spec's n≥400), synthetic drill, a custom non-canonical harness, and the
  CONFIRMED reading only appeared after four measurement bugs were fixed in that same harness.
  `delta_min` = 0.15 rests on that.
- Harness: added the closed-form primitives the run needs — `binom_pmf`/`binom_sf`/`binom_cdf`/
  `binom_two_sided_p` (exact, no normal approximation — near a band edge the approximation makes the
  verdict a property of the estimator), `chance_band`, `two_proportion_n`, `normal_quantile`. Fixtures
  extended to 46 known-answer cases, all PASS.
- Lesson recorded in the tree: a falsifier written against an unrecovered metric encodes a GUESS about
  that metric. The card froze `chance_p0` as `?` without noticing that G-4's LOGIC — not just its
  parameter — depended on the answer.

## 2026-07-16 — selection: F1 alone, and the gate that licenses its rig (H_001 pre-registered)

- SELECTED one family — **F1 codec-is-the-self** — closing the divergence stage. Criterion was
  belief-killed-per-dollar, not likelihood: an F1 null kills F1 + F6's variation axis + bounds
  `salvage.L4`(b) (the campaign's only green causal measurement) down to "static codec choice
  matters", for ≤$25. Recorded in `ARCHITECTURE.json` -> `decision`.
- SPLIT the campaign's "F1 substrate + F3 objective" bet into two SEQUENTIAL cards. Composing them
  is confounded twice: two levers move at once (a null can't be attributed, a win can't assign
  credit — un-confounding needs the 2×2 factorial), and F3's diary lives in token space, so an F1
  refit changes the diary's alphabet underneath it and both F3 controls go non-stationary. F3 is
  the second card, on whatever codec regime survives.
- PRE-COMMITTED, before any result exists: a drill-scale null on H_002 = F1 family-dead. Recorded
  in the tree so it cannot be relitigated after the numbers land (L8 — strict gates get bypassed).
- Made the two inherited gates OPERATIONAL for F1 (`ARCHITECTURE.json` -> `verification-inherited-gates`):
  L1's seam = the boundary-delta matrix B of the refit channel, estimator = participation ratio,
  gate = PR ≤ max(2.0, null₉₉); L2 is between-arm by construction (you can't ablate a vocabulary out
  of a model — it IS the input space), gate = Δbpb < max(5σ_seed, 0.004 bpb), where 0.004 bpb = 10×
  v1's OMEGA decoration signature.
- Replaced the harness placeholders with the estimators those gates need — `participation_ratio`,
  `effective_rank`, `stable_rank`, `singular_values`/`gram_matrix` (stdlib Jacobi eigensolver),
  `bits_per_byte`, `ablation_delta`, `ablation_fraction` (`tool/anima_v3.py`).
- Added `tool/test_anima_v3.py` — 30 closed-form known-answer fixtures, wired into `sidecar ci` as
  `estimator-fixtures` (new `harness.config.json`). This is falsifier G-3: a positive control on the
  instrument, not test hygiene. 30/30 PASS. It confirmed the estimator choice by measurement — on a
  weak-second-direction fixture PR reads 1.0002 where the entropy rank reads 1.057, i.e. PR is the
  stricter gate — and confirmed bpb's codec-invariance (a coarser codec halving tokens and doubling
  CE/token returns the identical bpb).
- PRE-REGISTERED + FROZEN `H_001` (`hypotheses/cards/H_001_f1-codec-refit-gate.md`, registry line
  added). Its verdict is about the RIG, not F1: LICENSED or REFUSED. Falsifiers G-1 drift existence ·
  G-2 closed-form power · G-3 estimator fixtures · G-4 salvage bounds check · G-5 protocol
  reconstruction. G-4 carries the card's own kill-power: if MORPH-ATOM's control 0.617 sits inside
  the 99% binomial chance band, L4(b) was never above floor and the write-lever axis is demoted.
- OPEN BLOCKER recorded honestly (G-5): the "H_9288 held-out recombination protocol" is cited in
  `salvage` but specified NOWHERE in this repo — v1 is discarded and `state/` holds only the
  divergence seed. G-2's power calc and G-4's chance band both depend on it. Unrecovered → H_001
  returns REFUSED, which is a result, not a delay.
- Research pass done before any compute (campaign rule 실측전-research): the exact twin has not been
  run; adjacent work raises F1's prior but measures one-shot adapt-then-finetune, never a refit organ,
  never recombination. Bottleneck studies document near-rank-1 redundancy on the write side — the L1
  gate is not paranoia.
- Preserved the verbatim design under `state/h001_f1-codec-refit-gate_2026-07-16/DESIGN_fable.md`.
- STAGE = PRE-REGISTRATION: one family selected, one card frozen, nothing run, no claim made.

## 2026-07-16 — divergence: where does aliveness live (8 families)

- Seeded the campaign from the `anima` (v1) autopsy: 9 measured, sealed verdicts imported into
  `ARCHITECTURE.json` -> `salvage` (L1 one-bit seam · L2 replacement-not-coupling · L3
  objective-not-readout · L4 write-side crack · L5 morphology decides learnability · L6
  measurement is the grave · L7 exotic substrate bought nothing · L8 strict gates get bypassed ·
  L9 the purity cage was causal). These pointers are the ONLY inheritance — v1's code, language,
  tree and purity list are discarded. The evidence trail stays in the `anima` repo.
- Ran a divergence pass (Fable 5) on the question "where does aliveness live", constrained to
  respect the salvaged laws. Recorded 8 mutually exclusive families (F1 codec-is-the-self ·
  F2 speech-economy · F3 diary-compressor · F4 corpus-farmer · F5 student-who-never-sleeps ·
  F6 swarm-drafts · F7 living-by-not-knowing-you · F8 tenant-organism) + 3 wildcards, each with
  its mechanism, L-check, minimal falsifier and the purity principle it breaks.
- Recorded the fake-diversity audit in the SSOT rather than leaving it to the reader: F2/F3/F7
  are one idea in three outfits (active inference); F1/F4 are two hands on the same write-side
  lever; F8 = F2 + a real world; W3 = F8 - learning. Only four genuinely distinct bets exist.
- Fixed the two non-negotiable falsifier gates (L1 effective-rank check · L2 ablation check) —
  the exact measurements whose absence killed v1. Retained exactly one v1 principle: p7
  (perplexity is never truth).
- Preserved the verbatim divergence + the brief that produced it under
  `state/diverge_aliveness_2026-07-16/` as the seed of record.
- STAGE = DIVERGENCE: no family selected, no code, nothing in the tree is a claim.

## 2026-07-15 — repo scaffold

- Initialized `anima-v3` from the sidecar `lab init` skeleton: `src/`, `state/`,
  `ARCHITECTURE.json` + `architecture.html` viewer + `serve.py`, `CLAUDE.md`,
  `README.md`, `CHANGELOG.md`, `.gitignore`, `.harness/`.
- Scaffolded the hypothesis-verification system `hypotheses/` (`CLAUDE.md`, empty
  `REGISTRY.jsonl`, `cards/_TEMPLATE.md`) + the repo-root shared harness
  `tool/anima_v3.py` (stdlib-only `Falsifier`/`evaluate` ledger).
- Authored a placeholder `ARCHITECTURE.json` SSOT (overview / components / data-flow /
  verification) — fill the tree from the campaign's design.
