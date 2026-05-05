---
title: anima Llama Path A v2 HF release prep LANDED — 1-page handoff (2026-05-05)
cycle: BG-LLAMA-PA-V2-HF-RELEASE-PREP
ts_utc: 2026-05-05
status: LANDED — SPEC_READY_AWAITING_USER_DECISIONS
mode: spec-only ($0 mac, no exec, no commit, no upload, no .roadmap mutation)
spec_doc: docs/anima_llama_path_a_v2_hf_release_prep_spec_2026_05_05.md
type: ai_native_landed
own_compliance: own 14 (HF Hub only) + own 15 (PRIVATE → 6 gates → PUBLIC) + own 16 (N/A — no compute)
sister_release: clm-v4-mk2-v1 (PRIVATE 2026-05-04, review window 2026-05-06T23:26:12Z)
adapter_sha256: 393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c
raw_invariants: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive structure-preserve"]
---

## §1 5-bullet summary

- **Llama-3.2-3B Path A v2 = chat-capability winner of 2026-05 anima SFT lattice.** TRUE_PASS verdict (`state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`): HellaSwag 0.645 (parity), MMLU 0.575 (parity), TriviaQA 0.455 (**+5.9 pp above Llama base**), composite 0.5584 vs CLM v4 + LoRA SFT v1 composite 0.196 = **+36.298 pp advantage**. Adapter: 98.6 MB PEFT LoRA rank 64, sha256 `393eb7530f...`, saved at `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/`. Forgetting_index = −0.028 (slight net improvement).
- **Separate HF release lane required from CLM v4 mk2-v1.** CLM v4 + LoRA SFT v1 = F-CLM-LORA-2 FAIL_REGRESSION (`#115` architectural — substrate measurement, not chat). Pβ Paradigm D 50K = F-Pβ-3 FAIL_TRUE (same `#115`). Llama Path A v2 is the *only* production-eligible chat-capability artifact; honest answer to "is anima production-ready for chat?" requires this release as a separate lane from CLM v4 substrate research.
- **own 14 + own 15 compliance — 6 verification gates mapped.** G1 benchmark suite **PASS** (TRUE_PASS verdict); G2 falsifier pre-register **PASS_W_F4_DEFERRED_TO_CLM2** (substrate-aware amendment per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`); G3 shim compatibility **N/A_LLAMA_HF_CANONICAL** (no custom modeling — Llama is HF-stock); G4 24-48h review window **TBD at upload**; G5 honest C3 model card **READY** (5 caveats finalized in spec §4.2 README skeleton); G6 cross-substrate **PASS_VIA_CROSS_LINK** to clm-v4-mk2-v1 + Pβ failed sibling. PUBLIC promote BG verdict.json template provided in spec §3.2.
- **Naming proposal — default recommendation `need-singularity/llm-v3-paradigm-a-prime-lora-r64-y3`** (PASS-CANON under HF naming spec mk2 §10.2 regex; 38 chars; encodes Llama lineage via `llm` family + path-A-prime paradigm slot + LoRA rank + sweep arm). Three alternatives surfaced in spec §2.2 (Option A-full / B HF-discoverable / C short umbrella). User decision Q1 in spec §7.
- **4-phase implementation plan, all $0.** Phase 1 ($0 mac, ~30 min): naming + manifest + README draft + validate. Phase 2 ($0 ubu1, ~10 min): pre-push smoke + adapter staging + dry-run. Phase 3 ($0 ubu1, ~30 min, gated on user authorization): actual PRIVATE upload + 24-48h review window starts. Phase 4 ($0 user-gated, ~30 min): PUBLIC promote with 6-gate verdict.json. Concurrent with CLM v4 mk2-v1 review window OK (independent gates).

## §2 5 user decision questions

- **Q1 Repo name** — default `need-singularity/llm-v3-paradigm-a-prime-lora-r64-y3` (PASS-CANON, 38 chars). Alternatives: A-full `llm-v3-paradigm-a-prime-lora-r64-rehearsal-y3` (54 chars, requires §3.7 amendment) / B `llama-3.2-3b-anima-rehearsal-pa-v2-mk2-v1` (HF-discoverable, requires mk2 spec amendment) / C `llm-v3-pa-v2-mk2-v1` (short, ambiguous).
- **Q2 PEFT adapter only vs merged model** — default PEFT-only v1 (98.6 MB, faster iteration, consumer obtains Llama base separately). Alternative: merged ~6.4 GB self-contained.
- **Q3 Llama 3 license attribution detail** — default dual-license declaration `license: llama3.2 + license_name: llama-3.2-community-license-additive-mit`. Alternative: single `license: other` with custom combined text.
- **Q4 Dataset attribution scope (rehearsal mix sources)** — default recipe doc only in main repo + manifest.json source list with sha256 + redistribution audit. Alternative: full data slice release as sibling dataset repo.
- **Q5 PUBLIC promote timing** — default independent timing (Llama PA v2 promote when its own gates PASS, regardless of CLM v4 mk2-v1 promote status; concurrency OK). Alternatives: sequence after CLM v4 mk2-v1 / before / simultaneous.

## §3 Honest C3 (≥5)

1. **Llama Path A v2 is anima-derivative not anima-native (architectural).** Bulk weights (~6.4 GB) are Meta's IP; anima contribution is the 98.6 MB LoRA delta + rehearsal-mix recipe + validation cycle. Fundamentally different substrate identity from `clm-v4-mk2-v1` (anima-authored from pretrain). Both are legitimate releases but model card must not blur the distinction.
2. **"Chat-capability winner" claim rests on parity + ONE substantive gain, not uniform improvement.** HellaSwag −0.9 pp / MMLU −0.4 pp (within 1-σ of zero, parity not improvement); only TriviaQA +5.9 pp is above-noise. Honest framing: "rehearsal mix preserves Llama general capability and adds factual-recall depth from anima axis component." Composite +36.298 pp vs CLM v4 reflects CLM v4's structural-not-recoverable chat-incapability per #115, NOT "Llama is 36 pp better at chat than CLM trained on same data."
3. **Llama 3 Community License blocks unrestricted commercial path.** 700M MAU restriction (Meta authorization required → effectively blocks hyperscaler integration); "Built with Llama" attribution mandatory. Research-grade only; commercial product path requires separate evaluation cycle. MIT-additive on adapter delta is non-binding for the base license constraint.
4. **PEFT adapter consumer overhead (Llama base download required).** Consumers must accept Meta's gated Llama 3 license + download Llama-3.2-3B (~6.4 GB) + install `peft` + load via `PeftModel.from_pretrained`. Trade-off vs merged (~6.4 GB self-contained, no base-acceptance gate but still license-bound). Q2 surfaces this.
5. **own 15 G2 PASS_W_F4_DEFERRED carve-out is interpretation not measurement.** F-PA-RETRAIN-v2-4 strict reading 0.7871 (FAIL strict against 0.85 PARTIAL); substrate-aware amendment re-interprets but does not re-measure. PUBLIC promote verdict.json must cite both views (strict-FAIL + substrate-aware-DEFERRED) + BG-CLM-2-EXEC F-CLM-LORA-4 outcome before substrate-correct F4 question can be claimed closed. Consumers reading model card §F4 caveat must understand the interpretation, not just bottom-line.
6. **Composite metric (0.5584) is anima-internal aggregation, not industry-standard.** "+36.298 pp advantage" rests on custom mean-of-normalized HS/MMLU/TQ scores; no public benchmark uses this exact aggregation. Constituent benchmark deltas (−0.9 / −0.4 / +5.9 pp) are externally verifiable. Composite-only marketing-style summaries should be avoided.
7. **F4 substrate-deferred status creates long-tail dependency.** If BG-CLM-2-EXEC F-CLM-LORA-4 verdict lands FAIL on the rehearsal-mix recipe, release inherits substantive (not just deferred-unknown) F4 caveat. Mitigation: hold PUBLIC promote (Phase 4) until BG-CLM-2-EXEC verdict.json lands. own 15 honest-c3 admits PUBLIC→PRIVATE revert is pathological — never premature-promote.
8. **Single-seed eval (seed=42) limit=200, no multi-seed bootstrap.** stderr ~3.5 pp HS/TQ, ~1.0 pp MMLU. 5-seed ensemble bootstrap precedent (`p9_p1_5_ensemble_4seed_landed_2026_05_03.ai.md`) NOT executed for this lane. Point-estimate ships in v1; consumers seeking robust CIs must run their own bootstrap. Model card cites "PASS_TRUE@seed=42,limit=200" not "PASS_TRUE_BOOTSTRAPPED".

## §4 Status

- **chat-capability production winner = Llama Path A v2 — formally specified for separate HF release lane.** Not yet uploaded; PRIVATE upload gated on user Q1-Q5 decisions + Phase 1-2 mac/ubu1 prep work.
- **Sister release status**: `clm-v4-mk2-v1` PRIVATE 2026-05-04T23:26:12Z, 48h review window ends 2026-05-06T23:26:12Z, PUBLIC promote queued NOT executed pending b.1-b.6 gate verdict.json.
- **No `.roadmap.p9_sft` mutation in this cycle.** `cond.path_a_lora_train_complete` already carries `eval_fix_amendment_2026_05_05` + `f4_axis_amendment_2026_05_05` blocks (per `docs/p9_path_a_retry_3_true_pass_lane_closure_landed_2026_05_05.ai.md` + `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`); HF release lane is downstream of those amendments and lands in a separate roadmap update cycle (NOT this spec).

## §5 Files

- spec: `docs/anima_llama_path_a_v2_hf_release_prep_spec_2026_05_05.md`
- handoff: `docs/anima_llama_path_a_v2_hf_release_prep_landed_2026_05_05.ai.md` (this file)
- adapter source: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/adapter_model.safetensors`
- TRUE_PASS verdict: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- F4 amendment doc: `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`
- own 15 SSOT: `docs/anima_own_15_hf_release_lifecycle_landed_2026_05_05.ai.md` + `.own` line 514
- naming spec SSOT: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (§3.1 `llm` family + §10.2 regex)
- upload pipeline: `tool/hf_upload_mk2.hexa` + `tool/hf_upload_mk2_pre_push_hook.hexa` + `tool/hf_readme_template.md`
- sister release precedent: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md`
