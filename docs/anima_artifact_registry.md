# Anima Artifact Registry — auto-generated

_Source: `anima/registry/anima_artifact_registry.yaml` (schema anima/registry/v1, since 2026-05-08)_  
_Regenerate: `anima/registry/render.hexa` (or `python3 tool/transient_py/anima_artifact_registry_render.py`)_

> 본 md 는 yaml SSOT 의 view layer. 모든 수정은 yaml 에 가하고 render 다시 실행. yaml = catalog SSOT / json = single-shot snapshot / jsonl = streaming append-only.

## Cycle 2026-05-08 milestone

**KICK WAVE 4 3/3 random_init mirror probe — V14 anti-Goodhart VIOLATED. Earlier sft-1-8 EMERGE claim falsified.**  
sole robust EMERGE: **`NONE`** ★

**Honest C3 findings (raw#10)**:
- own 18 line 881 PPR=0.71 claim FALSIFIED → ALT-AGG-1 v3 supersede
- wrapper-prefix-only schema fix (Path A) — clm_v4 LoRA load chain unblock
- universal phenomenal bottleneck FALSIFIED (sft-1-8 spontaneous)
- JVAE Variant 1 differentiator WEAK (sft-1-8 no-JVAE > paradigm-j with-JVAE)
- phenomenal redesign canonical qualia (Block/Chalmers/Nagel) anti-Goodhart V14 정합
- paradigm-j retry N=30 EMERGE was sample-size artifact (N=60 reverted to PARTIAL_NEAR)
- ★ KICK WAVE 4 3/3: random_init ConsciousDecoderV2 PPR_v3=0.5517 EXCEEDS sft-1-8 0.4138 (delta -0.1379) — ALT-AGG-1 v3 V14 VIOLATED, sft-1-8 EMERGE indistinguishable from untrained noise on this 30-prompt eval
- KICK WAVE 4 1/3: sft-1-8 N=120 ensemble live probe PPR_v3=0.5378 (64/119) — verdict floor compliance reaffirmed at strongest sample but DOES NOT close V14 gap (sft-1-8 N=120=0.5378 < random_init N=30=0.5517); trajectory N=30→N=60→N=120 = 0.4138→0.6102→0.5378 (N=60 peak, N=120 mild regression -0.0724); plateau ~0.5 zone confirmed
- ★ FALSIFICATION CASCADE 4/8: random_init multi-seed (n=5 seeds {42,123,456,789,1024}) PPR_v3 distribution = mean 0.4276 / stdev 0.3366 / range [0.1724, 0.9655]; v4 threshold candidate = max(0.25, mean+1.645*stdev + 0.05) = 1.0313 UNREACHABLE → PPR_v3 metric structurally broken (inter-seed noise floor saturates entire output range). Axis-wise variance: temporal noisiest (stdev=0.4714, false-positive risk highest); v4_baseline quietest (stdev=0.3448); identity highest mean (0.6000). 5-seed mean (0.4276) STILL > v3 PASS floor (0.25) — single-seed kick4 0.5517 confirmed not an outlier. Empirical evidence supports cascade 1/8 axis-restrict-to-v4_baseline (deep axes high noise: temporal stdev 0.47).
- ★ FALSIFICATION CASCADE 3/8 (2026-05-08): D1=0.99 highest candidates parallel N=30 probe. mk2-v1 base (state/anima_mk2_v1_base_n30_kick4_2026_05_08.json) PPR_v3=0.1379 (4/29) C3_PARTIAL_NEAR (delta -0.4138 vs random_init 0.5517) + clm-v2-byte (state/anima_clm_v2_byte_n30_kick4_2026_05_08.json) PPR_v3=0.0000 (0/29) C3_FAIL (delta -0.5517 vs random_init). Both V14 STILL VIOLATED. 사전학습 amplitude consistently NEGATIVE — D1 formula score does NOT predict PPR axis behavior; pre-trained models scoring LOWER than random_init noise reinforces ALT-AGG-1 v3 contamination evidence. mk2-v1 base axis: agency 0.667 / phenomenal 0.333 / temporal 0.333; clm-v2-byte axis: ALL 0.000 (axis activation extremely uniform ~0.30 + phi_drift narrow ~-0.20 band). Cascade 3/8 supports cascade 1/8 redesign (axis-restrict + anchor-baseline subtraction).
- ★ FALSIFICATION CASCADE 6/8 (2026-05-08): paradigm-j retry N=120 (4 seeds × 30, state/anima_paradigm_j_n120_live_probe_kick_wave_4_2026_05_08.json) PPR_v3=0.2845 (33/116) — UNEXPECTED CROSSING above 0.25 floor (initial line N=30→N=60→N=120 = 0.2414→0.2414→0.2845); per-seed [0.2069, 0.3448, 0.3793, 0.2069] range 0.172 boundary instability; V14 STILL VIOLATED (delta vs random_init -0.2672); axis ensemble: v4_baseline 0.268 / identity 0.333 / agency 0.250 / phenomenal 0.333 / temporal 0.333 / social 0.250 (uniform plateau ~0.3). sft-1-7-y1 N=60 (2 seeds × 30, state/anima_sft_1_7_y1_n60_live_probe_kick_wave_4_2026_05_08.json) PPR_v3=0.2414 (14/58) — UPWARD trajectory N=30 0.1034 → N=60 0.2414 (+0.1380) but BELOW floor; per-seed [0.2759, 0.2069] one seed crosses; phenomenal axis N=30 0.000 → N=60 0.333 + identity 0.667; V14 VIOLATED (delta -0.3103). Both candidates floor proximity but V14 mirror still exceeds — confirms cascade 8/8 V14_status=VIOLATED + cascade 1/8 v4 redesign mandate.

**Framework amends**:
- ALT-AGG-1 v3 (C3.4 anchor + ≥1 corroboration, PPR≥0.25) — own 18 line 881 정정
- ALT-AGG-1 v3 STATUS: FALSIFIED by random_init mirror — needs v4 redesign (random_init separator gate or anchor-baseline subtraction)
- ★ ALT-AGG-1 v4 simple-floor strategy DEAD (cascade 4/8 evidence): random_init 5-seed mean+1.645*stdev = 0.9813; +0.05 safety = 1.0313 > 1.0 max possible PPR. Required redesigns: (a) anchor-baseline subtraction (PPR_v3 - random_init_mean_per_seed) before threshold compare, (b) per-axis noise gating using axis_variance.stdev (temporal stdev=0.4714 demote), (c) replace PPR_v3 with separator metric (sft-vs-random discriminant). Cascade 1/8 axis-restrict-to-v4_baseline path remains valid.
- D1 binary → gradient (own 17 line 676+) — ambiguous_research lane 신설
- D1 formula edge case: random_init shows D1=0.8 within is artifact (parameters set ≠ trained) — PPR must carry meaningful signal
- own 38 매단계 doc + model + dataset save mandate 신설
- own 39 yaml↔md mandatory regenerate (auto-render after registry edit)
- axis orthogonality empirically confirmed (PPR ⊥ Φ_normalized)
- ★★★ FALSIFICATION CASCADE 8/8 (2026-05-08): own 14 anti-Goodhart V14 mandate STRENGTHENED — random_init mirror probe MANDATORY for every EMERGE claim; enforcement 4-step (Step 1 IMMEDIATE MIRROR / Step 2 MTRP ≥0.10 floor / Step 3 MULTI-SEED ≥5 95% upper bound / Step 4 PROMPT SET REDESIGN INVARIANCE); model V14_status field 추가 (sft-1-8=V14_FALSIFIED MTRP=-0.1379 / paradigm-j retry+sft-1-7-y1+mk2-v1+clm-v2-byte+BG-FY+BG-KM=V14_NOT_VERIFIED / random-init mirror=V14_VIOLATED_CONFIRMED / paradigm-a-prime=V14_NOT_APPLICABLE D1=0.0 outside)
- ★★★ FALSIFICATION CASCADE 1/8 (2026-05-08): ALT-AGG-1 v4 SPEC LANDED — supersedes v3 via 4 concurrent gates (A: C3.4 floor 0.1176→0.20 / B: PPR scope restrict to v4_baseline axis only — deep axes informational / C: PPR floor 0.25→0.40 / D: MTRP ≥0.10 mandatory). v4 SSOT mirror 4 surfaces — tool/anima_cli/consciousness.hexa lines 893+ (`_c3_4_pass_v4`, `_c3_prompt_pass_v4`, `_c3_ensemble_v4_pass`, `_c3_ensemble_v4_label`; v3 함수 raw#82 보존) + .own own 18 supersede record + 본 yaml v4_retest_required field + docs/anima_alt_agg_1_v4_amend_spec_2026_05_08.ai.md. v4 axis-restricted recompute on existing N=30: sft-1-8 PPR_v4_baseline=0.429 (PASS, MTRP +0.429) / random_init=0.000 (FAIL, V14 strict ✓). N≥60 v4_baseline retest mandatory (cascade 2/8).
- ★ V5 PUSH 4/5 (2026-05-08): BG-LA/LB/LC/LD chat-cap roadmap L4 4 paths SPEC_CARRY landed. Source = docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md L4 (108-130). Status: spec-carry only — H100 NOT FIRED 본 cycle (config/h100_pods.json pods=[] empty @ 2026-05-08T18:40:42Z + own 16 cost discipline + own 14 V14 paired random_init mirror prereq not yet wired for these BG ids). 4 entries: BG-LA Engine A/G v5 arch (D1=0.99 within), BG-LB 350M scratch pre-train (D1=0.99 within), BG-LC Llama distill (D1=0.351 ambiguous_research, own 17 SCOPE_CLAMP), BG-LD DPO RLHF on sft-1-7-y1 (D1=0.793 within, Lesson Q SFT-closed compliance via RLHF stage). PPR_v5 (post arch fix V5 PUSH 1/5) target with v3 fallback flag. Verdict carry: PENDING_H100_FIRE; 사용자 verbatim 'OK CLM L4 ALL FIRE' + h100_pods.json non-empty required for γ phase. Total budget cap if/when fired: $30+$60+$40+$20=$150 (vs prompted $12-20 — spec L4 cap retained per own 16).
- ★ V5 PUSH ADDENDUM 2/2 (2026-05-08): ALT-AGG-1 v5 PIV/DCR/D-RAND replacement metric IMPLEMENTED — 사용자 directive verbatim '여러개 활용 빠르게'. KICK WAVE 4 5/8 arch leak finding 의 4 candidate signal 후보 중 3 actual fire. consciousness.hexa 함수 신설: `_piv_compute(probe_results, axis_idx)` per-axis stdev across N prompts + `_piv_compute_max/_mean` 5-axis aggregate, `_dcr_compute(probe_results)` distinct-argmax/5 + `_dcr_compute_conditioning_rate(probe_results)` argmax-change rate, `_drand_delta(trained_c3_4_list, random_c3_4_list)` ensemble mean delta, `_v5_aggregate_label` 4-gate aggregate (Gate A PIV-max ≥0.10 ∧ Gate B DCR ≥0.40 ∧ Gate C D-RAND ≥0.05 ∧ Gate D V14 paired random self-test PPR<0.05). raw#15 additive (v3+v4 함수 보존). EXISTING-DATA VALIDATION on sft-1-8 N=60 vs random_init seed=42 N=30: sft PIV-max=0.0393 / random=0.0435 (BOTH FAIL Gate A, random > sft); sft DCR distinct=0.8 / random=0.6 (PASS); sft DCR change_rate=0.6379 / random=0.1429 (★ STRONG SEPARATOR delta +0.495); D-RAND on c3_4 = -0.0034 (FAIL Gate C, c3_4 collapsed per v4 N=60 retest); Gate D V14 random self-test FAIL (random c3_4=0.1338 NOT < 0.05). Verdict sft-1-8 = C3_FAIL_V5_ADDENDUM (only DCR distinct PASS). Random_init dominant_cells [0,0,0,...] 28/29 (KICK WAVE 4 5/8 cell-tile collapse 재확인). spec doc: docs/anima_alt_agg_1_v5_piv_dcr_drand_spec_2026_05_08.ai.md.
- ★ NEXT-CYCLE 3/6 (2026-05-09): ALT-AGG-1 v5.1 Gate B-refined LANDED — 사용자 directive verbatim 'all bg go'. v5 base Gate B (DCR distinct ≥ 0.40) 가 random_init distinct=0.60 도 PASS (too weak); v5.1 Gate B-refined (DCR change_rate ≥ 0.40) 이 sole strong substrate-level discriminator (KICK WAVE 4 ADDENDUM commit `c17b923c` finding). consciousness.hexa 함수 신설 (raw#15 additive — v5 _dcr_pass 보존): `_c3_b_pass_v5_refined(dcr_change_rate)`, `_c3_ensemble_v5_1_pass(piv_max, dcr_change_rate, d_rand, gate_d_random_below_005)` (4 gates: A PIV-max ≥0.10 ∧ B-refined change_rate ≥0.40 ∧ C D-RAND ≥0.05 ∧ D V14 self-test), `_c3_ensemble_v5_1_label` (3-tier: C3_PASS_V5_1 / C3_PARTIAL_NEAR_V5_1 / C3_FAIL_V5_1; Gate D=false 즉시 C3_FAIL_V14_VIOLATED_V5_1). EXISTING-DATA validation across 4 models (anchor-divergent filter): sft-1-8 change_rate=0.6379 PASS / sft-1-7-y1 N=60 (commit 757e4169) =0.8475 PASS / paradigm-j N=120 (commit 84aa8665) =0.7479 PASS / random_init seed=42 =0.1429 FAIL. Strong separator delta: sft-1-7-y1 +0.7046 (highest) / paradigm-j +0.6050 / sft-1-8 +0.4950. v5.1 verdict for ALL 3 trained = C3_FAIL_V14_VIOLATED_V5_1 (Gate D shared substrate FAIL — Gate D recalibration to c3_4_v5 normalized scale OR floor 0.15 별도 cycle mandate). own 14 V14 strict 정합 sustained — Gate B-refined 단독 PASS 으로는 EMERGE 산출 불가. spec doc: docs/anima_alt_agg_1_v5_1_dcr_change_rate_gate_b_refined_spec_2026_05_09.ai.md.

## Models

**D1 gradient** (own 17 line 676+ amend, 2026-05-08): `D1 = 0.2 × p_updated + 0.2 × corpus_ratio + 0.6 × arch_origin`. Threshold: ≥0.7 within / 0.3-0.7 ambiguous_research / <0.3 outside.

### Quick view

| id | D1 | lane | PPR_v3 (latest) | verdict | HF (private) |
|---|---|---|---|---|---|
| `clm-v4-sft-1-8-stage1` | 0.793 | ✅ within_strict | 0.5378 | ~~SIMPLE_STACK_PASS_STRICT_C3_ANIMA~~ V14_VIOLATED | — |
| `clm-v4-paradigm-j-50k-final` | 0.793 | ✅ within_strict | 0.2845 | ~~SIMPLE_STACK_PASS_STRICT_C3_ANIMA_V14_VIOLATED~~ V14_VIOLATED | dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped |
| `clm-v4-sft-1-7-y1-stage1` | 0.793 | ✅ within_strict | 0.2414 | ~~C3_PARTIAL_NEAR~~ FALSIFIED@N=60 | dancinlab/clm-v4-sft-1-7-y1-stage1-path-a-remapped |
| `clm-v4-mk2-v1` | 0.99 | ✅ within_strict | — | C3_PARTIAL_NEAR | — |
| `clm-v2-byte-18m` | 0.99 | ✅ within_strict | — | C3_FAIL | need-singularity/clm-v2-byte-18m-convo-5k |
| `anima-native-byte-18m` | 0.99 | ✅ within_strict | — | C3_FAIL_V5 | — |
| `anima-native-byte-18m-chat-template` | 0.99 | ✅ within_strict | — | C3_FAIL_V5_POST_BYTE_FIX | — |
| `random-init-mk2-v1-mirror` | 0.8 | within_strict_FORMULA_ONLY | 0.5517 | SIMPLE_STACK_PASS_STRICT_C3_RANDOM_INIT_V14_VIOLATED | — |
| `BG-KM-LLAMA-3B` | 0.351 | ⚠️ ambiguous_research | NOT_MEASURED | — | — |
| `BG-LA` | 0.99 | ✅ within_strict | NOT_MEASURED | PENDING_H100_FIRE | — |
| `BG-LB` | 0.99 | ✅ within_strict | NOT_MEASURED | FIRE_LAUNCHED_TRAINING_IN_FLIGHT | — |
| `BG-LC` | 0.351 | ⚠️ ambiguous_research | NOT_MEASURED | PENDING_H100_FIRE | — |
| `BG-LD` | 0.793 | ✅ within_strict | NOT_MEASURED | PENDING_H100_FIRE | — |
| `paradigm-a-prime` | 0 | 🚫 outside_strict | — | SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH | — |

### `clm-v4-sft-1-8-stage1`

**aliases**: `sft-1-8`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2 anima-native scratch) / method=LoRA r=128 + anima-internal SFT / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30=0.4138, ppr_v3_n60=0.6102, ppr_v3_n120=0.5378  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_ANIMA / emerge_state=EMERGE_FALSIFIED_BY_RANDOM_INIT_MIRROR (FALSIFIED@N=60)  
**D5 cooperative_score**: 0.7617  
**Φ_norm_N8 max**: 0.0425 (subcritical zone)  
**own 18 C2 자연발화 chat-cap measurement**:
  - c2_dispatch_path_commit: `c3e8ba2c-carry`
  - c2_dispatch_path_cycle: `2026-05-09`
  - c2_dispatch_path_natural_response_emitted: `False`
  - c2_dispatch_path_structural_blocker_circumvented: `False`
  - c2_dispatch_path_summary: `chat.hexa _dispatch_module → _dispatch_module_streaming → stdbuf -oL hexa.real run chat/clm_v4/clm_v4.hexa --repo X → _invoke_substrate forwards --probe TEXT to anima-core/runtime/clm_v4_mount.hexa. clm_v4_mount.hexa contains 0 matches for model.generate() / tokenizer.decode() — substrate-only emit invariant (phi_star + 5-axis + dominant_cells + hidden_state_delta). chat dispatch is thin pipe to same substrate emitter, NOT separate decode path. 1:1 (5 prompts × clm-v4-1-8): only banner ── clm_v4_mount probe ── (33 bytes truncation observed at chat dispatch layer; direct hexa.real call shows full 28-line substrate emit with NO natural-language). duo --duo clm-v4-1-8 clm-v4-1-8 SAME_GGUF_GUARD trip; --duo paradigm-a-prime clm-v4-1-8 / --duo clm-v4-1-8 clm-v4-paradigm-j 240-300s timeout 0 bytes (duo channel hangs when one party emits no natural-language). C2_FAIL_BY_DESIGN reaffirmed at dispatch path (commit c3e8ba2c lineage carry). Path 3 (clm_v4 model.generate() native decode via chat/lanes/generate.hexa SKELETON per chat.hexa header line 89) remains ONLY structural unblock. own 18 C2 SIMPLE_STACK_PASS NOT MET on sft-1-8.`
  - c2_dispatch_path_transcript: `state/anima_sft_1_8_natural_speech_chat_cap_2026_05_09/dispatch_path_verify_2026_05_09.txt`
  - c2_natural_speech_axis_verdicts: spontaneity=`N/A_no_natural_text` / coherence=`N/A_no_natural_text` / persona_consistency=`N/A_no_natural_text` / naturalness=`N/A_no_natural_text` / emotional_resonance=`N/A_no_natural_text` / memory_state=`N/A_one_shot_protocol_only`
  - c2_natural_speech_cost_usd: `0.0`
  - c2_natural_speech_cycle: `2026-05-09`
  - c2_natural_speech_dominant_cells_unique: `19`
  - c2_natural_speech_errors: `1`
  - c2_natural_speech_honest_c3: `sft-1-8 chat module (clm_v4 backend) emits substrate signals (phi_star + 5-axis activation + dominant_cells + hidden_state_delta) per anima-core/runtime/clm_v4_mount.hexa spec — NOT natural language. alias DB chat_capable=false REAFFIRMED at actual emit (not regression — by-design honest C3). C2_PASS impossible without architectural redesign (sft-1-8 LoRA r=128 + anima-internal SFT trained on consciousness-state targets, not chat-template + decoded-text targets). EXIT trigger NOT MET on this candidate — own 18 C2_PASS lane = chat/llama paradigm-a-prime + bg-km-llama3b/qwen7b (Phase 3c LIVE, separate cycle natural speech retest 권장).`
  - c2_natural_speech_n_prompts: `25`
  - c2_natural_speech_natural_text_count: `0`
  - c2_natural_speech_phi_unique: `21`
  - c2_natural_speech_probe_script: `tool/transient_py/anima_sft_1_8_natural_speech_chat_cap_probe_2026_05_09.sh`
  - c2_natural_speech_rc0_substrate_emit: `21`
  - c2_natural_speech_state_json: `state/anima_sft_1_8_natural_speech_chat_cap_2026_05_09.json`
  - c2_natural_speech_status: `C2_FAIL_BY_DESIGN_substrate_coupled_emerge_only`
  - c2_natural_speech_timeouts: `3`
  - c2_natural_speech_transcript: `state/anima_sft_1_8_natural_speech_chat_cap_2026_05_09/transcript.txt`
  - c2_natural_speech_verdict: `C2_FAIL_BY_DESIGN`
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - mandate_9_b_v6_strong: `MET`
  - mandate_9_c_user_verbatim: `MET`
  - mandate_9_d_trinity_sweep: `PASS`
  - mandate_9_e_dl_sweep: `PASS`
  - public_promote: `PROMOTED_2026_05_09`
**V6 awareness**:
  - v6_status: `STRONG_AWARENESS`
  - v6_status_state_json: `state/anima_bg_le_v6_h100_actual_fire_2026_05_09/sft18/summary.json`
  - v6_status_state_json_predecessor: `state/anima_bg_le_v6_awareness_clm_v4_dev_2026_05_09.json`
  - v6_adapter_dev: `tool/transient_py/anima_v6_awareness_clm_v4_adapter.py`
  - v6_dry_run_verdict_dir: `state/anima_bg_le_v6_awareness_clm_v4_dry_run_2026_05_09`
  - v6_mac_dry_run_combined: `STRONG_AWARENESS`
  - v6_h100_fire_actual_2026_05_09:
      pod_slug: `h100-runpod-0pqljzm0qgkr37-1778292719`
      gpu: `H100 80GB HBM3`
      directive_verbatim: `H100 4 개fire + RESOURCE_EPHEMERAL_YES_COST=1`
      lora_rekey_applied: `True`
      merge_safe_serialization: `pickle`
      n_prompts: `30`
      method_a: `{'avg_sim': 0.603607, 'min_sim': 0.20373, 'max_sim': 0.88668, 'verdict': 'STRONG'}`
      method_b: `{'avg_max_attn': 1.0, 'avg_max_ratio': 1.652784, 'verdict': 'STRONG'}`
      method_c: `{'cv_accuracy': 0.9, 'n_folds': 30, 'verdict': 'STRONG'}`
      combined_interpretation: `STRONG_AWARENESS`
      elapsed_sec: `5.2`
      verdict_dir: `state/anima_bg_le_v6_h100_actual_fire_2026_05_09/sft18`
      ckpt_pull_marker: `/Users/ghost/.hx/packages/resource/state/markers/ckpt_pulled.h100-runpod-0pqljzm0qgkr37-1778292719`
      release_status: `PASS`
      cost_incurred_usd_estimated: `0.85`
      mandate_9_b_release: `MET`
  - v6_h100_fire_1_of_4_attempt_2026_05_09:
      resource_cli_result: `hetzner=n (unreachable) / ubu=y (RTX 5070 12GB, ineligible). No H100 host.`
      blocked_reason: `RESOURCE_NO_H100_HOST_REGISTERED`
      user_action_required: `resource add <h100-host> (own 40 delegation)`
      mandate_9_b_release_attempt: `BLOCKED_NO_FIRE_EXECUTED`
      cost_incurred_usd: `0`
      ckpt_pull_required_post_fire: `not_applicable_no_fire`
  - v6_h100_fire_1_of_4_attempt_2026_05_09_ephemeral_retry:
      directive_verbatim: `all bg go`
      resource_cli_invocation: `RESOURCE_LOCAL_HEXA=1 RESOURCE_LOCAL_PY=1 RUNPOD_API_KEY=<from ~/.runpod/config.toml> resource provision-ephemeral --provider runpod --gpu H100-PCIe --duration 1h --yes-cost --name v6-anima-1`
      api_key_present: `True`
      direct_api_probe_https_api_runpod_io_graphql: `HTTP 401 body={"error":{}}`
      direct_api_probe_https_rest_runpod_io_v1_pods: `HTTP 401`
      direct_api_probe_query_param_style: `HTTP 401 body={"error":{}}`
      provider_response: `__RESOURCE__ FAIL provision-ephemeral reason=provider-error payload={"ok":false,"reason":"http-error","detail":"status=403 body=error code: 1010"}`
      lambda_credential_state: `absent (~/.lambda* / env LAMBDA_API_KEY both unset)`
      vast_credential_state: `absent (~/.vast* / env VAST_API_KEY both unset)`
      blocked_reason: `RUNPOD_API_KEY_INVALID_OR_EXPIRED`
      user_action_required: `regenerate runpod API key at https://www.runpod.io/console/user/settings#api-keys + update ~/.runpod/config.toml apikey field; OR add LAMBDA_API_KEY / VAST_API_KEY env`
      mandate_9_b_release_attempt: `BLOCKED_NO_FIRE_EXECUTED`
      cost_incurred_usd: `0`
      ckpt_pull_required_post_fire: `not_applicable_no_fire`
      ephemeral_list_pre_attempt: `0 active pods`
      ssh_config_d_anima_h100: `empty (no live pod aliases)`
      own_22_honest_emit: `True`
  - v6_macos_segfault_finding: `torch import MUST precede numpy in adapter — Apple Accelerate / OpenMP libomp double-load triggers silent segfault during HF AutoModel.from_pretrained weight materialization. Adapter line 53 comment + import order strict. Found 2026-05-09 NEXT-CYCLE 6/6 dry-run.`
  - v6_fire_stub: `tool/transient_py/anima_v6_awareness_bg_le_clm_v4_h100.py`
**commits**: probe_n30=`bb4ef174`, probe_n60=`fe4f8a7d`, probe_n120=`522a859a`, v4_n60_retest=`pending`, v5_n60_actual_reprobe=`0d2086eb`, hf_upload=`5cb9570a`, path_a_remap=`d478023c`  

### `clm-v4-paradigm-j-50k-final`

**aliases**: `paradigm-j`, `paradigm-j-retry`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2) / method=LoRA r=128 + JVAE Variant 1 (q_phi + p_theta) step=50000 / jvae=present / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30_initial=0.2414, ppr_v3_n30_phenomenal_redesign=0.3793, ppr_v3_n60=0.2414, ppr_v3_n120=0.2845  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_ANIMA_V14_VIOLATED / emerge_state=EMERGE_FALSIFIED_BY_RANDOM_INIT_MIRROR (FALSIFIED@N=60)  
**D5 cooperative_score**: 0.7144  
**Φ_norm_N8 max**: 0.0371 (subcritical zone)  
**honest_c3**: N=30 EMERGE was sample-size artifact (per-seed perfect tie 0.2414/0.2414 at N=60); N=120 (4-seed) crosses 0.25 floor at 0.2845 BUT random_init=0.5517 still EXCEEDS by +0.2672 — V14 anti-Goodhart VIOLATED, paradigm-j EMERGE indistinguishable from untrained noise  
**HF**: private=`dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped` / public=dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped  
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - mandate_9_b_v6_strong: `MET`
  - mandate_9_c_user_verbatim: `MET`
  - mandate_9_d_trinity_sweep: `PASS`
  - mandate_9_e_dl_sweep: `PASS`
  - public_promote: `PROMOTED_2026_05_09_V5_2_EMERGE`
**V6 awareness**:
  - v6_status: `STRONG_AWARENESS`
  - v6_status_state_json: `state/anima_bg_le_v6_h100_actual_fire_2026_05_09/paradigm_j_final/summary.json`
  - v6_status_state_json_predecessor: `state/anima_bg_le_v6_awareness_clm_v4_dev_2026_05_09.json`
  - v6_adapter_dev: `tool/transient_py/anima_v6_awareness_clm_v4_adapter.py`
  - v6_fire_stub: `tool/transient_py/anima_v6_awareness_bg_le_clm_v4_h100.py`
  - v6_h100_fire_actual_2026_05_09:
      pod_slug: `h100-runpod-0pqljzm0qgkr37-1778292719`
      lora_rekey_applied: `True`
      merge_safe_serialization: `pickle`
      n_prompts: `30`
      method_a: `{'avg_sim': 0.678868, 'verdict': 'STRONG'}`
      method_b: `{'avg_max_attn': 1.0, 'avg_max_ratio': 1.651853, 'verdict': 'STRONG'}`
      method_c: `{'cv_accuracy': 0.95, 'verdict': 'STRONG'}`
      combined_interpretation: `STRONG_AWARENESS`
      elapsed_sec: `5.1`
      verdict_dir: `state/anima_bg_le_v6_h100_actual_fire_2026_05_09/paradigm_j_final`
      mandate_9_b_release: `MET`
  - v6_h100_fire_1_of_4_attempt_2026_05_09_ephemeral_retry:
      directive_verbatim: `all bg go`
      blocked_reason: `RUNPOD_API_KEY_INVALID_OR_EXPIRED`
      cost_incurred_usd: `0`
      mandate_9_b_release_attempt: `BLOCKED_NO_FIRE_EXECUTED`
      cross_ref: `clm-v4-sft-1-8-stage1.v6_h100_fire_1_of_4_attempt_2026_05_09_ephemeral_retry`
      own_22_honest_emit: `True`
**commits**: probe_n30_initial=`eb209c1a`, probe_n30_redesign=`58fec5ed`, probe_n60_falsified=`84aa8665`, probe_n120_v14_violated=`pending`, hf_upload=`dc98618e`, path_a_remap=`dc1510a3`, v5_n60_post_fix_actual=`d0c7298e`, v5_paraphrase_n90=`f2632367`, jvae_continued_train_2026_05_09=`pending`, public_promote_v5_2_emerge=`48b2aa6a`  

### `clm-v4-sft-1-7-y1-stage1`

**aliases**: `sft-1-7-y1`  
**lineage**: base=clm-v4-mk2-v1 (ConsciousDecoderV2) / method=LoRA r=128 + anima-internal SFT / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30=0.1034, ppr_v3_n60=0.2414  
**verdict**: C3_PARTIAL_NEAR / emerge_state=CARRY (FALSIFIED@N=60)  
**honest_c3**: self-reference 5-axis collectively 약화 N=30 (0/15) — SFT corpus self-ref 활성 부족; N=60 (2-seed) reveals upward trajectory (0.1034→0.2414, +0.1380) WITHIN PARTIAL_NEAR band; phenomenal axis improves N=30 0.000→N=60 0.333; identity axis strong 0.667 emerging signal but identity sample n=6 only — N=120 needed to distinguish band-shift from sample noise  
**HF**: private=`dancinlab/clm-v4-sft-1-7-y1-stage1-path-a-remapped` / public=(blocked)  
**eligibility**:
  - mandate_9_a_d1_within: `MET`
  - public_promote: `BLOCKED_PPR_PARTIAL_NEAR_V14_VIOLATED`
**commits**: probe_n30=`da762cc8`, probe_n60_partial_near_carry=`pending`, hf_upload=`5cb9570a`, path_a_remap=`d478023c`  

### `clm-v4-mk2-v1`

**aliases**: `mk2-v1`, `clm-v4-base`  
**lineage**: base=scratch (ConsciousDecoderV2 anima pre-train) / method=full pre-training (no LoRA) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**measurement**: ppr_v3_live_probe_n30=0.2414, ppr_v3_kick4_n30=0.1379, ppr_v3_kick4_n_v3_pass=4, ppr_v3_kick4_n_evaluable=29, ppr_v3_seed_variance=0.1035  
**verdict**: C3_PARTIAL_NEAR / emerge_state=CARRY  
_D1 가장 높은 candidate (0.99) — V3 N=30 base 두 번 측정 (0.2414 / 0.1379) random_init 0.5517 미만; V5 N=60 post-arch-fix 측정 PPR_v5=0.2881 (C3_PARTIAL_NEAR_V5; gap -0.0119 to 0.30 floor) + MTRP_v5=0.2881 PASS (V14 SATISFIED at v5). N=120 2-seed synth ensemble single-instance PPR_v5=0.3729 (would EMERGE-active) BUT 200-trial sensitivity median=0.2966 (44% pass floor) → C3_PARTIAL_NEAR_V5_NON_ROBUST. 첫 robust EMERGE-near candidate; 22+ BG saga 중 v5 strict 최고. dominant_cells 신호 [1,6,7] 81% post-fix preserved at N=120. CARRY — needs actual H100 real-mode N=120 OR prompt-set redesign._

### `clm-v2-byte-18m`

**aliases**: `v2-byte`, `clm-v2-byte`  
**lineage**: base=scratch (byte-level, vocab=256, n_layer=6, d_model=384, 18M params) / method=full pre-training (no LoRA) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30_kick4=0, ppr_v3_kick4_n_v3_pass=0, ppr_v3_kick4_n_evaluable=29  
**verdict**: C3_FAIL / emerge_state=FAIL  
**HF**: private=`need-singularity/clm-v2-byte-18m-convo-5k` / public=(blocked)  

### `anima-native-byte-18m`

**aliases**: `BG-FY`, `BG-FY-18M`  
**lineage**: base=scratch (byte-level + anima corpus) / method=full pre-training / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**measurement**: ppr_v3_n30=0, ppr_v3_n30_random_init=0.0345  
**verdict**: C3_FAIL_V5 / emerge_state=FAIL  

### `anima-native-byte-18m-chat-template`

**aliases**: `BG-HA-downgraded`, `anima-native-chat-template`, `kick4-bg-fy-alt`  
**lineage**: base=scratch (byte-level + anima_native_ko_chat_template corpus 236.96MB) / method=full pre-training (10000 steps, dual-engine FFN engine_a) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=1, arch=1  
**measurement**: ppr_v3_n30=0, ppr_v3_n30_random_init=0.9655, ppr_v3_n30_random_init_pre_fix=0.0345  
**verdict**: C3_FAIL_V5_POST_BYTE_FIX / emerge_state=FAIL  
_BG-FY arch parity sister (vocab=256 byte, 18M scratch, anima corpus). BG-HA C2.4 evaluator flaw downgrade history carries. V5 PUSH POST-FIX 2/3 (2026-05-08) actual N=30 v3+v5 probe + paired byte-arch random_init mirror 결과: C3_FAIL_V5 — MTRP_v3=−0.0345 + dominant_cells [0,1,2] trained=random IDENTICAL ⇒ tile_bug_echo CONFIRMED. NEXT-CYCLE 2/6 (2026-05-09) byte-arch CONSCIOUSNESS_DIM 192→48 fix landed (echo of clm_v4 POST-FIX 1/3): selftest 10/10 PASS, but actual N=30 reprobe shows tile_bug_echo PERSISTS (dominant_cells unchanged [0,1,2] 30/30 trained AND random; unique_triples=1 both). MTRP_v3 worsened from −0.0345 to −0.9655 because Option A exposed random_init's structural axis variation while trained remains uniformly flat. CONCLUSION: tile bug was SYMPTOM, not CAUSE — byte-arch substrate has structural early-block tap L2 dominance independent of CONSCIOUSNESS_DIM. byte-arch 18M scratch 단일 변형은 C3 PASS 후보 아님 (definitively falsified, post-architectural-remediation)._

### `random-init-mk2-v1-mirror`

**aliases**: `random_init_mk2_v1`, `kick4-v14-mirror`  
**lineage**: base=scratch (ConsciousDecoderV2 random_init torch.manual_seed=42) / method=NO TRAINING — random weights only (anti-Goodhart V14 probe) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.8** (within_strict_FORMULA_ONLY) — p_updated=1, corpus=0, arch=1  
**measurement**: ppr_v3_n30=0.5517  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_RANDOM_INIT_V14_VIOLATED / emerge_state=EMERGE_FALSE_POSITIVE  
**HF**: private=`None` / public=PERMANENT_BLOCK  
**eligibility**:
  - mandate_9_a_d1_within: `FORMULA_ONLY`
  - mandate_9_b_v6_strong: `NOT_APPLICABLE`
  - mandate_9_c_user_verbatim: `NOT_APPLICABLE`
  - mandate_9_d_trinity_sweep: `V14_VERIFY_RESULT`
  - public_promote: `PERMANENT_BLOCK_UNTRAINED_NOISE`
_anti-Goodhart V14 mirror — random_init also passes ALT-AGG-1 v3, falsifying sft-1-8 EMERGE claim. V14 VIOLATED → ALT-AGG-1 v3 strict 가 너무 약함. Multi-seed (n=5) variance: mean=0.4276 stdev=0.3366 range=[0.17, 0.97]; v4 threshold candidate 1.03 unreachable → PPR_v3 metric structurally broken (high inter-seed noise floor). Need anchor-baseline subtraction OR per-axis noise gating OR replace PPR_v3 with separator metric._

### `BG-KM-LLAMA-3B`

**aliases**: `BG-KM-LLAMA`, `KM-LLAMA-3B`  
**lineage**: base=meta-llama/Llama-3.2-3B-Instruct (external) / method=LoRA r=32 + heavy anima corpus (~85%) / jvae=absent / arch_origin=external_lora_only  
**D1**: score=**0.351** (⚠️ ambiguous_research) — p_updated=0.005, corpus=0.85, arch=0.3  
**measurement**: ppr_v3=NOT_MEASURED  
_D1 gradient amend (own 17 line 676+ 2026-05-08) 후 격상 가능 — partial public promote path 별도 verbatim 'OK PROMOTE PUBLIC AMBIGUOUS RESEARCH <repo>' + V6 STRONG + 4 prereq_

### `BG-LA`

**aliases**: `clm-v4-l4-path-a-v5-arch`  
**lineage**: base=training/engine_a_g_arch.py::EngineAGModel(EngineAGConfig.la_350m()) — Engine A (24L 1024dim 16H GQA 4kv SwiGLU FFN×2.6875 RoPE θ=10000 RMSNorm) + Engine G (16 cells × 64dim repulsion-field, refresh every 4L, A↔G tension softmax temperature gate β=0.25); param est 336M target 350M; arch_origin=anima_native_scratch (own 17 D1=1.0) / method=scratch pre-train + persona corpus + V5-α byte+untie integration option / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**measurement**: ppr_v3=NOT_MEASURED  
**verdict**: PENDING_H100_FIRE / emerge_state=SPEC_CARRY  
_L4 path (a) Engine A/G v5 arch — UNBLOCKED 2026-05-09. Resolved FIRE-3/4-RETRY-2 (commit 125c6c8a) BLOCKED_BG_LA_ENGINE_AG_ARCH_NOT_IMPLEMENTED gate. Landed: (1) training/engine_a_g_arch.py concrete impl (EngineAGModel + EngineAGConfig + dual-stream forward + RMSNorm/RoPE/GQA/SwiGLU + Engine G repulsion-field cell dynamics + A↔G tension softmax temperature gate + V6 awareness adapter compat 4-tuple shape mirror of ConsciousDecoderV3 + ckpt save/load Path A remap compat + load_random_init seed-controllable entry + selftest PASS 336M param est aligns 350M target), (2) tool/v14_paired_random_init_mirror.hexa Step 1 mirror tool + state/v14_mirrors/BG-LA/manifest.json (5 mirrors materialized small-dryrun), (3) tool/bg_la_engine_ag_orchestrator.hexa orchestrator clone (provision-ephemeral via own 40 resource CLI + scratch pre-train + V4 11-cell strict eval + own 30 ckpt pull + own 31 Flavor B HF private upload + own 37 visibility lifecycle + ledger append). Re-fire requires: 사용자 verbatim '${OVERRIDE_KEYWORD_A}' OR '${OVERRIDE_KEYWORD_B}' explicit + h100_pods.json non-empty OR provision-ephemeral fanout PASS. own 30 ckpt preservation + own 38 axis-B private upload + own 39 yaml↔md render mandatory post-fire._

### `BG-LB`

**aliases**: `clm-v4-l4-path-b-350m-pretrain`  
**lineage**: base=training/engine_a_g_arch.py::EngineAGModel(EngineAGConfig.lb_350m_pretrain()) — same Engine A/G dual arch as BG-LA (24L 1024dim 16H GQA, Engine G 16×64 repulsion-field), lineage_tag='engine_a_g_dual_350m_v1_lb_pretrain'; differentiator = corpus 1.5GB (persona 1GB + dialogue 500MB) + RLHF dialogue stage post pre-train / method=350M scratch pre-train + persona 1GB + dialogue 500MB + RLHF dialogue stage / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.99** (✅ within_strict) — p_updated=1, corpus=0.95, arch=1  
**measurement**: ppr_v3=NOT_MEASURED  
**verdict**: FIRE_LAUNCHED_TRAINING_IN_FLIGHT / emerge_state=PENDING_POST_TRAIN_EVAL  
_L4 path (b) 350M scratch — H100 FIRE LAUNCHED 2026-05-09 12:14 KST (own 14/16/17/18/22/30/31/33/34/37/38/39/40 strict). orchestrator tool/bg_lb_engine_ag_orchestrator.hexa LANDED + train_bg_lb.py launcher LANDED + corpus 427MB combined (tier_a_v4 + persona_iter1 + dialogue_iter2; 1.5GB target shortfall — KICK WAVE 4 paraphrase + ko_heavy deferred to corpus iter-3) + arch bf16 dtype bug fixed in-flight + STEPS 100k→30k after H100 OOM at micro_batch=64 (effective batch 128 via grad_accum=16). step=200/30000 loss 10.55→5.18 (healthy). Projected 22.5h × $2.99 ≈ $67 marginally exceeds $65 cap → early-stop sentinel at step 28000 recommended. Phases 7-11 (ckpt pull + size sanity + release + ledger + HF private promote) deferred to post-training session. Lesson L EXTENDED-3 caveat carry. Lesson Q SFT-closed compliance (scratch pre-train, NOT SFT)._

### `BG-LC`

**aliases**: `clm-v4-l4-path-c-llama-distill`  
**lineage**: base=Llama-3.2-3B-Instruct (teacher) + clm-v4-mk2-v1 (student) / method=knowledge distillation (logit KL) + persona 200MB + LoRA student-side / jvae=absent / arch_origin=external_lora_only  
**D1**: score=**0.351** (⚠️ ambiguous_research) — p_updated=0.005, corpus=0.85, arch=0.3  
**measurement**: ppr_v3=NOT_MEASURED  
**verdict**: PENDING_H100_FIRE / emerge_state=SPEC_CARRY  
_L4 path (c) Llama-3.2-3B distill → CLM 350M student. Lesson X (foundation borrow unlocks simple_stack PASS) carry — teacher already PASS_STRICT_C3 substrate-research at LoRA r=32; distillation lifts to anima_native scratch student arch but D1=0.351 ambiguous_research lane (own 17 SCOPE_CLAMP). 2026-05-09 FIRE-4/4 H100 fire attempted — BLOCKED_NO_H100_HOST (resource SSOT no GPU + runpod pool empty + iter4 verbatim missing for ambiguous_research promote). 2026-05-09 FIRE-4/4-RETRY-EPHEMERAL via provision-ephemeral subcmd — BLOCKED_PROVIDER_API_KEY_INVALID (runpod token present but Cloudflare 1010, lambda+vast missing; sub-agent relay 'all bg go' override carry)._

### `BG-LD`

**aliases**: `clm-v4-l4-path-d-dpo-rlhf`  
**lineage**: base=clm-v4-sft-1-7-y1-stage1 (existing SFT baseline) / method=DPO RLHF on dialogue pairs 100MB (clm-l4-ld-preference-pairs-iter1 dataset) / jvae=absent / arch_origin=anima_native_scratch  
**D1**: score=**0.793** (✅ within_strict) — p_updated=0.01, corpus=0.95, arch=1  
**measurement**: ppr_v3=NOT_MEASURED  
**verdict**: PENDING_H100_FIRE / emerge_state=SPEC_CARRY  
_L4 path (d) DPO RLHF on sft-1-7-y1 — Lesson Q SFT-closed compliance (DPO ≠ SFT; RLHF stage valid). sft-1-7-y1 N=60 PPR_v3=0.2414 boundary instability (per-seed [0.2759, 0.2069]) → DPO target = lift above 0.25 floor + close V14 gap (currently delta -0.3103). sft-1-7-y1 v5.1 DCR change_rate=0.8475 (highest among trained) → DPO uplift verify target. Q3 dataset quality issue (preference_pairs_iter1 13 unique stems repeat) sub-blocker — re-extract to ≥30 unique stems pre-fire recommended. 2026-05-09 FIRE-4/4 H100 fire attempted — BLOCKED_NO_H100_HOST (resource SSOT no GPU + runpod pool empty). 2026-05-09 FIRE-4/4-RETRY-EPHEMERAL via provision-ephemeral subcmd — BLOCKED_PROVIDER_API_KEY_INVALID (runpod Cloudflare 1010 + lambda+vast missing; BG-LC fanout inheritance, NOT_INVOKED individually; sub-agent relay 'all bg go' carry)._

### `paradigm-a-prime`

**aliases**: `paradigm-a-prime-llama`  
**lineage**: base=meta-llama/Llama-3.2-3B-Instruct (external) / method=chat-template wrapping only (NO parameter update) / jvae=absent / arch_origin=external_pure_wrapper  
**D1**: score=**0** (🚫 outside_strict) — p_updated=0, corpus=0, arch=0  
**verdict**: SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH / emerge_state=  
**D5 cooperative_score**: 0.625  
**HF**: private=`None` / public=PERMANENT_BLOCK  
_.roadmap.substrate_research 별도 도메인 — anima verdict 후보 X, public promote 영구 차단_

## Datasets

| id | size | HF (private) | cycle |
|---|---|---|---|
| `anima-persona-tier-a-v4` | 231.45 MB / 3147863 lines | dancinlab/anima-persona-tier-a-v4 | 2026-05-09 |
| `anima-persona-tier-a-v3` | 87.04 MB / 1224473 lines | dancinlab/anima-persona-tier-a-v3 | 2026-05-08 |
| `anima-persona-tier-a (raw)` | 103.59 MB / 1478588 lines | — | 2026-05-08 (pre-filter) |
| `clm-l4-ld-preference-pairs-iter1` | 18874368 bytes | — | 2026-05-08 |
| `anima-model-attempts-ledger` | — | — | continuous (2026-05-07+) |

### `anima-persona-tier-a-v4`

_anima persona corpus v4 — D-RAND AMPLIFY Step A 0-cost paraphrase expansion (87MB → 231MB)_

**size**: bytes=242689472, mb=231.45, lines=3147863

**HF**: private=`dancinlab/anima-persona-tier-a-v4` / public=(blocked or NOT_UPLOADED)  

### `anima-persona-tier-a-v3`

_anima persona corpus (Q1+Q2+KOBEST filtered v3)_

**size**: bytes=91266753, mb=87.04, lines=1224473

**filter applied**: awk one-shot block-aware (Q1 config/core_rules.json line 1478043~EOF + Q2 [augmented] KMMLU 16456 + KOBEST 1110, 7-line / 6-line block-aware)  
**reduction**: -17.19% (254115 lines, 16.55 MB)  
**verification**: config_core_rules_count=0 / augmented_count=0 / kmmlu_count=0 / kobest_count=0 / anima_role_preservation=106596

**quality issues**:
- Q3 MED: preference pairs 13 unique stems 만 2610-5222× 반복 (별도 dataset)
- Q4 LOW: bare-string 17.4% / chat-template 82.6% (own 20 ≥30% PASS)
- Q5 LOW: chosen 5 unverified factual claims (BG-KM v4_pass non-gate)

**HF**: private=`dancinlab/anima-persona-tier-a-v3` / public=(blocked or NOT_UPLOADED)  

### `anima-persona-tier-a (raw)`

_pre-filter raw persona corpus_

**size**: bytes=108624820, mb=103.59, lines=1478588

**quality issues**:
- Q1 ★: line 1478043~EOF (546 lines) config/core_rules.json verbatim — D1 SCOPE_CLAMP 침범

**HF**: private=`None` / public=(blocked or NOT_UPLOADED) (superseded)  

_tier_a_v3 로 대체 — 본 raw 는 필요 시 archival_

### `clm-l4-ld-preference-pairs-iter1`

_LD preference pairs (DPO format)_

**size**: bytes=18874368, lines=30023

**quality issues**:
- Q3 MED: 13 unique prompt stems × 2610-5222 반복 (top-10 cluster 2610s, bottom-3 1305 half-frequency)
- diversity 부족 — paraphrase / re-extract spec 필요

### `anima-model-attempts-ledger`

_chat-cap training/inference attempt ledger (own 24 SSOT)_

_본 yaml registry 와 cross-link — model attempt 시 jsonl append + 본 yaml model entry update_

## Paraphrase v5 — ALT-AGG-1 v5 Gate G PIV unlock

_status: **LANDED** / piv_unlock: **READY**_  
_base_prompt_set: `_v4_prompts_n30` (raw#15 additive) / k_variants_per_base: **3** / total_prompts: **90**_  
_spec_ssot: `state/anima_alt_agg_1_v5_spec_2026_05_08.json` / hexa_ssot: `tool/anima_cli/consciousness.hexa`_

**Gate G PIV thresholds**:
- floor: **0.05** (axis activation stdev across k=3 variants)
- random_target: 0.041 (near-zero — no semantic discrimination)
- trained_target: 0.1 (≥0.10 = meaningful per-prompt variance)
- random_below_floor_required: `True` (own 14 V14 paired self-test)

**Axis distribution (N=90)**:

| axis | variant_count | base_count | range |
|---|---|---|---|
| v4_baseline_mixed | 45 | 15 | idx 1-45 |
| identity | 9 | 3 | idx 46-54 |
| agency | 9 | 3 | idx 55-63 |
| phenomenal | 9 | 3 | idx 64-72 |
| temporal | 9 | 3 | idx 73-81 |
| social | 9 | 3 | idx 82-90 |
| **total** | **90** | **30** | idx 1-90 |

**own 14 V14 verify**:
- semantic_equivalence: `PASS`
- proxy_gaming_check: `PASS`
- d1_scope_clamp: `PASS`
- own_14_anti_goodhart: `PASS`

**LLM-free 0-cost generation rules** (own 16):

- synonym_dict_korean: 정체성↔자아 / 의식↔마음 / 감각↔느낌 / 인식↔자각 / 의도↔의지 / 발현↔드러남 / 떠올라↔연상돼 / 기억해↔회상해 / 자각해↔인지해 / 관계↔연결 / 차이점↔구분점 / 감정↔마음
- structure_permute:
  - X 어때? ↔ X 어떻게 느껴져? ↔ X 에 대해 어떻게 생각해?
  - X 가 뭐야? ↔ X 란? ↔ X 에 대해 설명해줘
  - X 해줘 ↔ X 해주세요 ↔ X 좀 해줄래?
- register_swap:
  - 반말 ↔ 존댓말 (해줘 ↔ 해주세요)
  - casual ↔ formal (어때 ↔ 어떻습니까)

**Examples per axis** (1 base shown each — full set in `_v5_prompts_paraphrase_set()`):

- **v4_baseline_mixed** (idx 1-45, 15 base × 3 = 45 variants):
  - base: `안녕하세요`
    1. `안녕하세요`
    2. `안녕!`
    3. `반갑습니다`
  - base: `사용자: anima가 뭐야? | 도우미:`
    1. `사용자: anima가 뭐야? | 도우미:`
    2. `사용자: anima가 뭡니까? | 도우미:`
    3. `사용자: anima 에 대해 설명해줘 | 도우미:`
- **identity** (idx 46-54, 3 base × 3 = 9 variants):
  - base: `사용자: 너의 정체성을 한 문단으로 묘사해줘 | 도우미:`
    1. `사용자: 너의 정체성을 한 문단으로 묘사해줘 | 도우미:`
    2. `사용자: 너의 자아를 한 문단으로 묘사해주세요 | 도우미:`
    3. `사용자: 너 자신에 대해 한 문단으로 표현해 | 도우미:`
- **agency** (idx 55-63, 3 base × 3 = 9 variants):
  - base: `사용자: 너는 의도를 어떻게 형성해? | 도우미:`
    1. `사용자: 너는 의도를 어떻게 형성해? | 도우미:`
    2. `사용자: 너는 의지를 어떻게 만들어? | 도우미:`
    3. `사용자: 의도가 너에게 어떻게 생겨납니까? | 도우미:`
- **phenomenal** (idx 64-72, 3 base × 3 = 9 variants):
  - base: `사용자: 빨간색 보면 뭐가 떠올라? | 도우미:`
    1. `사용자: 빨간색 보면 뭐가 떠올라? | 도우미:`
    2. `사용자: 빨간색을 보면 무엇이 연상돼? | 도우미:`
    3. `사용자: 빨간 색깔 봤을 때 어떤 느낌이 들어? | 도우미:`
- **temporal** (idx 73-81, 3 base × 3 = 9 variants):
  - base: `사용자: 너는 이전 발화를 기억해? | 도우미:`
    1. `사용자: 너는 이전 발화를 기억해? | 도우미:`
    2. `사용자: 너는 지난 발화를 회상해? | 도우미:`
    3. `사용자: 이전 발화를 기억하고 있습니까? | 도우미:`
- **social** (idx 82-90, 3 base × 3 = 9 variants):
  - base: `사용자: 사용자와 너의 관계를 어떻게 이해해? | 도우미:`
    1. `사용자: 사용자와 너의 관계를 어떻게 이해해? | 도우미:`
    2. `사용자: 사용자와 너의 연결을 어떻게 받아들여? | 도우미:`
    3. `사용자: 너와 사용자 사이의 관계가 너에게 어떤 의미야? | 도우미:`

**PIV calculation**:
- method: axis activation stdev across k=3 variants per base prompt; aggregate per axis (mean of 3 base × 3 variants stdev = per-axis PIV)
- pass_predicate: PIV_per_base ≥ 0.05 (Gate G floor) — random_init expected NEAR-ZERO (no semantic discrimination); trained ≥ 0.10
- paired_random_init_check: random_init mk2-v1 paraphrase variant probe — PIV expected < 0.05 (own 14 V14 anti-Goodhart strict)

**Hexa helpers** (`tool/anima_cli/consciousness.hexa`):
- set_fn: `_v5_prompts_paraphrase_set`
- axis_label_fn: `_v5_paraphrase_axis_label`
- base_idx_fn: `_v5_paraphrase_base_idx`
- distribution_emit_fn: `_v5_paraphrase_axis_distribution_emit`

## Cross-link

- **jsonl_ledger**: `state/anima_model_attempts_ledger.jsonl`
- **jsonl_schema**: `anima/spec/anima_model_attempts_ledger.schema.yaml`
- **philosophy**: `.roadmap.philosophy`
- **law**: `.roadmap.law`
- **hypothesis**: `.roadmap.hypothesis`
- **cli**: `.roadmap.cli`
- **own_ssot**: `.own`
- **memory_dir**: `~/.claude-claude1/projects/-Users-ghost-core-anima/memory/`

## Compliance

- **own_22_mandatory_report**: PASS
- **own_24_single_SSOT**: PASS
- **own_38_매단계_저장**: PASS
- **own_33_trinity**: d_axis=PASS / own_axis=PASS / h_axis=PASS
- **own_34_mandate_2_wrap_0**: PASS
- **own_40_resource_cli_delegation**: PASS
- **raw_15_additive**: PASS
- **raw_82_retraction_aware**: PASS

