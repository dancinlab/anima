# OPT-B Phase 1+2 prep — LANDED mac+ubu1 zero cost

bg_lane: OPT-B-PHASE-1-2-PREP
status: PHASE_1_PASS_PHASE_2_FAIL_GRADIENT_FLOW_BLOCKED_PHASE_3_HOLD
parent spec: docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_2026_05_05.md
verdict: state/clm_v4_lora_sft_opt_b_phase_1_2_prep_2026_05_05/verdict.json

## TL;DR

Phase 1 PASS, Phase 2 FAIL gradient flow, Phase 3 HOLD. Sibling train script and sibling orchestrator authored without touching v1 originals. Phase 2 smoke on ubu1 RTX 5070 confirmed cross attn LoRA receives zero gradient because cross attn forward is gated by consciousness states upstream of LoRA injection. Self attn positive control passes. F-OPT-B-2 pre-falsified in expectation. Saved up to fifty USD H100 spend at zero Mac+ubu1 cost.

## Phase 1 details

Train script sibling at tool/transient_py/clm_v4_lora_train_opt_b.py, ~600 lines. Hyperparameter locks per spec section 3: Q1-B wide cross attn qkvo (16 layers x 8 projections = 128 modules total), Q2-A learning rate 5e-6 (10x lower vs v1 3e-5), Q3-A max steps 3000 (50% of v1 6000), Q4-A abort threshold -10pp drift from in-pipeline base 35.81. LoRA dropout 0.10 (2x v1), save and phi probe every 500 steps. Orchestrator sibling at tool/clm_v4_lora_train_orchestrator_opt_b.hexa with hooks: boot register, heartbeat during poll, trap pre stop EXITING marker, 404 verify 3 retries, deregister after 404. All 5 verdict schema fields in emitted exec.bash: pod_kill_verified_404, watchdog_deregistered, cost_target_usd, cost_actual_usd, cost_overrun_2x_alerted. BG_LANE=OPT-B-CROSS-ATTN-RETRAIN, TARGET_USD=30. Selftest PASS, emit produces exec.bash and run_h100.bash.

## Phase 2 details

Smoke ran on ubu1 RTX 5070 sm_120, /home/aiden/venv_orchestrator/bin/python, torch 2.11.0+cu128, peft 0.19.1, transformers 5.7.0, trl 1.3.0 (newly installed). 10 smoke steps with synthetic 32-sample dataset, fp32 dtype, batch size 2 ctx 64. Trainable params 5.18M (0.97 percent of 532M total). Train wall 0.71 sec, loss 16.74 to 16.78, grad_norm range 8.1 to 15.2 (non-zero so gradients flow somewhere). target_modules audit: 128 total (64 self attn + 64 cross attn), per layer 8, lora A and B per target = 2 trainable param tensors. Initial assertion bug fixed: PEFT named_modules over-counts by 2x because it exposes both lora_A ModuleDict and lora_A.default inner Linear. Canonical metric is parameter count via .lora_A.default.weight and .lora_B.default.weight suffix.

## Phase 2 gradient flow result

Self attn lora B post-train: 64 of 64 non-zero, max norm 3.59e-3 (positive control PASS). Cross attn lora B post-train: 0 of 64 non-zero, max norm 0.0 (FAIL). gradient_flow_to_cross_attn_lora_b_pass = false. Inspection of modeling_clm_v4.py block forward confirms the gating: cross_attn invocation is conditional on consciousness_states being non-None. SFT data has no consciousness_states fed, so cross_attn forward is never called, so backward never produces gradients for cross_attn LoRA adapters. Pre-train cross_attn.o_proj std mean 0.019905, post-train 0.019905 (identical to 6 decimals after 10 steps). F-OPT-B-2 (post_train_std diverges from init floor 0.02 by at least 1e-3) is pre-falsified: zero gradient does not scale with steps, so 3000 H100 steps would produce identical FAIL.

## Decisions section

D1 proceed with OPT-B prime amendment cycle. Recommendation A. Author docs/clm_v4_lora_sft_opt_b_prime_amendment_2026_05_05.md adding consciousness_states feed mechanism to SFT pipeline, then re-run Phase 2 smoke at zero cost.

D2 consciousness_states feed source. Option A pre-computed fixture. Option B dynamic from decoder.tension_proj output. Recommendation A.

D3 amendment doc vs spec re-author. Recommendation A amendment doc additive.

D4 Phase 2 re-smoke scope. Recommendation 10-step ubu1 smoke or 1-step Mac CPU smoke.

D5 Phase 3 cost ACK timing. Recommendation ACK after amendment plus re-smoke PASS.

C5 sibling additive only preserved. v1 train script untouched. v1 orchestrator untouched. OPT-B orchestrator selftest pass on Mac.

C6 hooks all five verdict schema fields present in emitted exec.bash. BG_LANE OPT-B-CROSS-ATTN-RETRAIN, TARGET_USD 30. Boot register, heartbeat, trap pre-stop EXITING marker, 404 verify, deregister-on-404 all replicated from v1.

C7 Phase 1 plus 2 came in at zero actual cost. Wall ~90min within ~1.5h spec target. Saved up to 50 USD H100 spend by surfacing gate 3 blocker pre-Phase-3.

C8 F-OPT-B-2 pre-falsified in expectation. Failure mode (zero gradient to zero weight update) does not scale with steps. 3000 H100 steps would produce same outcome.

## Trigger condition for next dispatch

OPT-B prime amendment cycle dispatch needs no new gate (free Mac authoring). The dispatch chain after Phase 2 re-smoke PASS:

1. OPT-B prime amendment lands. Phase 2 re-smoke runs. Gate 3 PASS (cross_attn lora_B non-zero post-train with consciousness_states fed).
2. User cost ACK 20-50 USD. Gate 2 PASS.
3. Phase 3 H100 dispatch via hexa run tool/clm_v4_lora_train_orchestrator_opt_b.hexa --launch --launch-confirmed.
4. Phase 4 eval (separate dispatch; F-OPT-B-3, F-OPT-B-4, F-OPT-B-5 measured).
5. Phase 5 promote conditional on F-OPT-B-1 to F-OPT-B-5 ALL PASS.

Until gate 3 PASS, Phase 3 is HOLD even with user cost ACK.

## Artifacts landed

- Train script sibling Mac: tool/transient_py/clm_v4_lora_train_opt_b.py (~27KB, ~600 lines)
- Train script sibling ubu1: /home/aiden/anima/tool/transient_py/clm_v4_lora_train_opt_b.py (rsync OK)
- Orchestrator sibling: tool/clm_v4_lora_train_orchestrator_opt_b.hexa (~700 lines)
- Orchestrator selftest: PASS
- Orchestrator emit: state/clm_v4_lora_sft_opt_b_2026_05_05/exec.bash plus run_h100.bash
- ubu1 smoke artifacts: /tmp/clm_v4_lora_opt_b_smoke/ on ubu1
- Verdict: state/clm_v4_lora_sft_opt_b_phase_1_2_prep_2026_05_05/verdict.json
- Companion handoff: this file
- v1 train script: tool/transient_py/clm_v4_lora_train.py UNTOUCHED
- v1 orchestrator: tool/clm_v4_lora_train_orchestrator.hexa UNTOUCHED
- OPT-B parent spec: docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_2026_05_05.md UNTOUCHED

## Honest C3

C1 OPT-B premise FALSIFIED at zero. Spec Q1-B target_modules patch alone is empirically insufficient. cross_attn LoRA receives zero gradient because forward path is gated by consciousness_states upstream of LoRA injection.

C2 self_attn positive control PASSED. 64 of 64 lora_B non-zero post-train (max norm 3.59e-3) confirms PEFT LoRA + backward + smoke methodology is sound. cross_attn ZERO is not artifact.

C3 phi-drift estimate is informational placeholder. Logit-std proxy 0.91 is on different scale than canonical phi 35.81. Direct subtraction meaningless. Canonical phi probe deferred to post-Phase-3 Mac side.

C4 Phase 3 dispatch BLOCKED on three gates. Gate 1 substrate differential PASS already. Gate 2 user cost ACK pending. Gate 3 Phase 2 smoke PASS NEW FAIL surfaced by this work. Recommended path: amendment plus re-smoke plus gate 2 ACK.
