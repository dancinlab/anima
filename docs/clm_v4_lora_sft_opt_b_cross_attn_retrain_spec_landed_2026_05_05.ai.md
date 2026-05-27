# OPT-B cross_attn retrain spec — LANDED 2026-05-05 (companion handoff)

- parent spec: `docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_2026_05_05.md`
- bg lane: BG-SHIM-V5-OPT-B-PREP (mac, $0, ~45min spec land)
- status: SPEC_LANDED — exec DEFERRED; dispatch contingent on OPT-A + user cost ACK
- architectural anchor: `state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json` — Phase 2 selftest discovered cross_attn.o_proj never updates during SFT (init scale 0.02 = trained scale 0.0199 at step 20000)

---

## 5 bullets summarizing

1. Root cause: F-SHIM-V4-4 architectural FAIL is not fixture-quality — `cross_attn.o_proj` was effectively never trained during BG-CLM-2-EXEC SFT because cross_attn was EXCLUDED from LoRA target_modules per phi-flip mitigation, AND `ConsciousDecoderV3.__init__`'s `apply(_init_weights)` walk re-inits all `nn.Linear` to std~0.02, overwriting the local std=0.001 init at `conscious_decoder.py:420`. best.pt step 20000 `o_proj_std_mean` = 0.01990 ~= init floor 0.02.
2. Architectural fix: re-train SFT cycle with `cross_attn.{q,k,v,o}_proj x16` ADDED to LoRA target_modules (Q1-B wide variant, +0.137% trainable params). Gradient flow reaches cross-attn; weights diverge from init scale 0.02 during SFT.
3. phi-flip mitigations (cross_attn is highest-risk surface): LR 5e-6 (10x lower than v1's 3e-5), dropout 0.10 (2x v1's 0.05), max_steps 3000 (50% of v1's 6000), phi probe every 500 steps (4x denser), ABORT trigger on drift > -10pp from in-pipeline baseline 35.81.
4. 5 falsifier suite F-OPT-B-1..5 LOCKED: F-OPT-B-1 NO_FLIP (drift > -10pp), F-OPT-B-2 cross_attn trained (|std_post - 0.02| >= 1e-3), F-OPT-B-3 F-SHIM-V5-4 lift_pp >= +5pp (THE decisive gate), F-OPT-B-4 F-CLM-LORA-2 composite >= 0.30 (>=+50% lift over v1 baseline 0.196), F-OPT-B-5 forgetting_index < 0.05.
5. 5-phase plan, $20-100 envelope: Phase 1 ($0 mac, ~30min spec patch), Phase 2 ($0 mac+ubu1, ~1h smoke), Phase 3 ($20-50 H100, ~3-5h retrain — REQUIRES USER COST ACK), Phase 4 ($1-3 H100, ~30min eval), Phase 5 ($0 mac, conditional promote-gate amendment + HF release v2 prep).

---

## 5 decision questions

- Q1: cross_attn.o_proj only (16 modules) OR full cross_attn q/k/v/o (64 modules)? — Recommend B (wide). Training only o_proj while q/k/v stay at random init 0.02 means o_proj overfits to noisy upstream projections.
- Q2: LR 5e-6 OR 1e-5 OR 3e-5 (same as v1)? — Recommend A (5e-6, 10x lower). cross_attn is highest phi-flip risk surface; LR is dominant lever for excursion magnitude.
- Q3: max_steps 3000 OR 6000? — Recommend A (3000). Lower LR + narrower step count co-mitigate cumulative drift; v1 cycle showed HellaSwag plateau at step 4000.
- Q4: phi ABORT trigger -10pp OR -5pp (more conservative)? — Recommend A (-10pp). Matches CLM-2-EXEC's `phi_flip_threshold_pp` carry; -5pp would mis-fire on routine PARTIAL-band drift like v1's -4.46pp.
- Q5: H100 cost ACK $20-50 OR $20-100 OR $50-100? — Recommend B ($20-100). Tight $20-50 plans Phase 3 + Phase 4; $20-100 caps allow ABORT contingency + retry-once. EXPLICIT USER COST ACK REQUIRED before Phase 3 dispatch.

---

## Honest C3 (>= 5 per raw#10)

- C1 — cross_attn training is necessary for F-SHIM-V5-4 lift but NOT sufficient for F-CLM-LORA-2 Llama-parity. Both Pbeta and CLM-2-EXEC v1 adapters are architecturally chat-incapable per #115 (CLM v4 NEVER SFT'd, NEVER RLHF'd before BG-CLM-2). F-OPT-B-4 threshold 0.30 explicitly accepts partial-lift (>=+50% over v1 baseline 0.196).
- C2 — phi-flip is the dominant failure mode. CLM v4's substrate uniqueness (+41.86 carry) is the hardest constraint. Estimated outcome distribution: 30-60% PASS (drift > -5pp), 30-50% PARTIAL (drift -5 to -10pp), 10-20% FAIL_FLIP (drift > -10pp -> ABORT).
- C3 — cost band $20-100 wider than CLM-2-EXEC v1's $2.39 actual. Reflects (a) +0.137% trainable params, (b) 4x denser eval cadence, (c) ABORT contingency, (d) Phase 4 full 3-bench eval. Hard $100 cap.
- C4 — OPT-A result is the primary informer for OPT-B dispatch. If OPT-A redo Phase 2 fails to show v4 vs v5 substrate differential, OPT-B's premise weakens. Trigger: OPT-A Phase 2 redo PASS REQUIRED before OPT-B dispatch.
- C5 — OPT-C result is NOT an OPT-B informer. OPT-C confirms F-SHIM-V4-4 PREREQUISITE_BLOCKED diagnosis but provides no new info about OPT-B success likelihood. OPT-C is for Path B closure only, not OPT-B go/no-go.
- C6 — F-OPT-B-3 (F-SHIM-V5-4 lift_pp >= +5pp) is THE decisive gate. F-OPT-B-1 is prerequisite, F-OPT-B-2 is verification, F-OPT-B-4/5 are general-capability gates carried from v1. F-OPT-B-3 uniquely tests whether training cross_attn produces fixture-driven residual lift.
- C7 — Q1-B (wide) vs Q1-A (narrow) trade-off is small. phi-flip risk scales sub-linearly with target_modules count; dominant risk is whether ANY cross_attn parameter participates. Q1-A is a defensible safer-side variant if user prefers tighter risk envelope.
- C8 — Spec is exec-deferred; dispatch contingent on (1) OPT-A redo Phase 2 PASS, (2) explicit user $20-100 cost ACK. Each phase is a separate BG dispatch with its own gate.

---

## Trigger condition (DISPATCH GATE)

OPT-B Phase 1 amendment authoring may dispatch only when BOTH conditions are satisfied:

1. OPT-A redo Phase 2 PASS confirmed — `state/clm_v4_hf_format_shim_v5_phase2_redo_*` verdict shows v4 freshinit_o_proj_std_mean = 0.02 vs v5 freshinit_o_proj_std_mean >= 0.05 (or 0.10), demonstrating substrate-level differential is real.
2. Explicit user $20-100 H100 cost ACK — user message containing explicit cost acknowledgment for Phase 3 H100 retrain spend within $20-100 envelope (hard $100 cap).

If either condition is not met, OPT-B remains in DEFERRED status and no Phase 1 amendment work proceeds.

---

## Migration path (post-PASS scenario)

- shim v4 LOCKED: retained unchanged
- CLM-2 LoRA v1: retained as substrate-research artifact (post-PASS) OR primary chat candidate (post-FAIL)
- CLM-2 LoRA v2 (OPT-B output): NEW chat-capability primary candidate (post-PASS) OR discarded (post-FAIL_FLIP) OR substrate-research alternative (post-PARTIAL)
- shim v5 (OPT-A scope): orthogonal investigation continues regardless of OPT-B outcome
- Pbeta + CLM-2 v1 adapters: UNTOUCHED in all branches

---

## raw compliance

- raw#9 — md only; spec is .md, no .py mutation in this BG
- raw#10 — 8 honest C3 entries (C1-C8)
- raw#15 — additive only; no parent spec mutation, no `.roadmap.*` mutation, no shim v4/v5 mutation
- raw#71 — F-OPT-B-1..5 thresholds + hyperparameters + phase budget envelopes LOCKED at spec land
- CRITICAL flags — no git commit, no exec, no `.roadmap.*` mutation — ALL respected

---

END handoff — OPT-B spec is dispatch-ready; awaiting OPT-A confirmation + user cost ACK.
