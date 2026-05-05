---
title: CLM v4 + LoRA SFT S3 closure — landed handoff (B3 dispatcher executor)
status: LANDED — SPEC + HANDOFF (mac, $0, no exec, no commit, no .roadmap mutation)
ts_utc: 2026-05-05
cycle: BG-CLM-2-S3-CLOSURE
domain: p9_sft
spec_doc: docs/clm_v4_lora_sft_s3_closure_2026_05_05.md
predecessor_main_verdict: state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json
predecessor_proposal: docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md
sibling_fail_true_precedent: state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json
chat_capability_winner: state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json
amended_lane_status: CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA
recommended_route: Rank 1 ($0 lane closure)
exec_authorized: false
mutation: additive_only_proposal_only
substrate: mac-local
raw_invariants: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive only", "raw#71 falsifier-bound"]
ssots_touched: []
ssots_NOT_touched:
  - .roadmap.p9_sft (proposal only)
  - state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_sft_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (preserved verbatim)
  - docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md (preserved verbatim — superseded via reference, not mutation)
---

# CLM-2 lane S3 closure — landed handoff

## §1 Five-bullet summary

- **F-CLM-LORA-2 RE-VERDICT = FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR** (composite_clm_lora 0.19542 vs composite_llama_path_a_v2 0.5584; delta -36.298pp; per `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json`). The lane status converts from the predecessor `CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ` to **`CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA`**. Scenario dispatch S3 (anima < Llama, regression) per `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md` §3; B dispatcher B3 ($0 closure) per `docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md` §2.3.

- **C-CLM-LORA-2 differentiator hypothesis ("anima substrate provides measurable lift over Llama LoRA path on the same SFT recipe") FALSIFIED**. -36.298pp delta is far outside the limit=200 stderr ~3pp noise band. Pattern matches the Pβ Paradigm D 50K F-Pβ-3 FAIL_TRUE_CLOSED precedent (`state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`) — both LoRA-stage paths on CLM v4 base produce degenerate / random-floor output on chat-capability metrics. Two independent paths converging on the same conclusion provide strong empirical grounding for #115 chat-incapability being **architectural** (L32).

- **Substrate safety preserved (decoupled tier)**: F-CLM-LORA-1 PASS_TRUE (forgetting_index 0.0196 ≪ 0.05; φ★ canonical drift -4.46pp NO_FLIP); F-CLM-LORA-3 PASS (10.02 MB adapter); F-CLM-LORA-4 PASS_VIA_PART_A_ONLY (per `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md`); F-CLM-LORA-5 PASS (shim v4 compat). 4 of 5 falsifiers PASS. The failure mode is **chat-capability lift not happening** (architectural per #115), not substrate damage. Adapter `sha256=6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a` retained as Φ-stable substrate-research artifact only (NOT for chat / general capability claims). L31: substrate-uniqueness and chat-capability lift are orthogonal axes.

- **Chat-capability hope formally shifts to Llama Path A v2 retry-3 eval-rerun TRUE_PASS** (`state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`; HS 0.645 + MMLU 0.575 + TQ 0.455 → composite 0.5584). The Llama Path A lane is the chat-capability winner of record per `.roadmap.p9_sft` line 5 `p9_sft.cond.path_a_lora_train_complete.eval_fix_amendment_2026_05_05.lane_closure_status` = `TRUE_PASS_LANE_CLOSED`. CLM v4 lane = substrate-research; Llama Path A v2 lane = chat-capability. The two lanes are now formally separated (L33).

- **Three follow-up routes ranked by 완성도 (per memory `feedback_completion_quality_recommendation`)**: **Rank 1 ($0) RECOMMENDED** — this S3 closure spec + landed handoff + memory + roadmap annotation proposal (no apply this cycle). **Rank 2 ($1-3 shim v5)** — solves a different problem (F-SHIM-V4-4 architectural unfalsifiability per `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`); does NOT recover the C-CLM-LORA-2 LoRA SFT differentiator. **Rank 3 ($25-75 5-seed scaleup)** — confirms regression robustness only; cost-to-evidence ratio unfavorable since single-seed -36.298pp is already strong-signal robust (predecessor verdict honest C3 #6: "5-seed scaleup would NOT change conclusion"). Roadmap annotation `s3_closure_2026_05_05` proposed as additive sibling field on `.roadmap.p9_sft` line 6 `p9_sft.cond.clm_v4_lora_sft_2026_05_05` (peer to existing `lane_closure_2026_05_05`); apply requires explicit user authorization on a separate apply-cycle.

## §2 Honest C3 (≥5)

1. **C1 — single-seed F2 verdict carries stderr ~3pp at limit=200 per bench**: -36.298pp delta is far outside noise band, so the FAIL_REGRESSION direction is robust. The precise magnitude (-36 vs -32 vs -40pp) is not pinned at single-seed; 5-seed scaleup (Rank 3) would tighten the CI but not change the verdict direction. This S3 closure adopts the single-seed verdict as decision-grade because the signal is strong-signal robust to seed variance at this magnitude.

2. **C2 — comparator asymmetry (4-bench CLM-LORA vs 3-bench Llama)**: OpenBookQA measured for CLM-2 (0.290) but not for Llama Path A v2. Like-for-like 3-bench delta is -39.273pp (even larger than the 4-vs-3 -36.298pp); FAIL direction preserved either way. Carried verbatim from `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:honest_c3[1]`.

3. **C3 — substrate-aware reading vs strict differentiator reading**: a substrate-aware reading would frame F2 as "expected" (CLM v4 base at random-floor on chat benchmarks per #115; LoRA's job is incremental drift-prevention not chat-capability creation). Under this reading the F2 spec was miscalibrated as a "differentiator". This S3 closure adopts the strict differentiator reading per the original spec literal (`docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-2). Future re-cycle BGs may adopt substrate-aware-relative-to-baseline F2 banding — out of scope this closure.

4. **C4 — Pβ + CLM-2 pattern match strong but not exhaustive**: two LoRA SFT/distill paths on CLM v4 base both confirm chat-capability lift FAIL. Strong sibling-pattern evidence for #115 architectural hypothesis but does not exhaust the space of all possible LoRA recipes / adapter configurations / distill teachers / rehearsal mixes. L32 lesson states "two converging paths" not "all possible paths" — honest scope.

5. **C5 — substrate-research artifact retention does NOT validate substrate-research future**: this S3 closure retains the CLM v4 + LoRA adapter for substrate-research (φ★ stability, axis-conditioning post-LoRA, cross-substrate matrix). Whether substrate-research has further actionable downstream value (BLM phase-5, cross-substrate consistency probes, consciousness-primitive measurement) is a separate question — not settled by this closure. The retention is "do not delete artifacts"; it is not a downstream value claim.

6. **C6 — F4 amendment cross-link impact on Path A retry-3 lane (out of scope)**: the Path A retry-3 lane status `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` should now be readable as "F4 deferral RESOLVED via CLM-2 F4 PASS_VIA_PART_A_ONLY" if the user authorizes a sibling roadmap amendment. Path A lane upgrade from `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` to `TRUE_PASS_W_F4_RESOLVED` is OUT OF SCOPE of this S3 closure (proposal-only, additive-only discipline preserved).

7. **C7 — additive-only proposal discipline preserved**: this handoff does NOT mutate `.roadmap.p9_sft` directly. The proposed `s3_closure_2026_05_05` sibling-field annotation lives in `docs/clm_v4_lora_sft_s3_closure_2026_05_05.md` §7. Apply requires explicit user authorization on a separate apply-cycle, per the precedent set by the predecessor proposal `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` §3.3 and the proposal-pattern lineage `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md`.

## §3 References

- Spec doc (this cycle): `docs/clm_v4_lora_sft_s3_closure_2026_05_05.md`
- B3 dispatcher template: `docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md` §2.3
- S3 scenario tree: `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md` §3
- F2 RE-VERDICT source: `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json`
- Predecessor lane closure proposal: `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md`
- Sibling FAIL_TRUE precedent: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`
- Chat-capability winner: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- Roadmap target: `.roadmap.p9_sft` line 6 `p9_sft.cond.clm_v4_lora_sft_2026_05_05`
- Memory landed (this cycle): `~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
- Memory sister: `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`

No exec, no commit, no roadmap mutation this cycle.
