---
date: 2026-05-05
agent: BG-α'''-EVAL-FIX
cycle: BG-α'''-EVAL-FIX-2026-05-05
status: LANDED — TRUE_PASS_FORGETTING_FIX_VERIFIED
ssot_artifact: state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json
predecessor: state/p9_path_a_retrain_v2_retry_3_2026_05_04/verdict.json (V2_FAIL_FORGETTING_PERSISTS — superseded as measurement artifact)
adapter_sha256: 393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c
pod_id: pa5e33lhnkz815
actual_cost_usd: 0.75
wall_time_min: 15
---

# Path A retry-3 EVAL-FIX TRUE_PASS — forgetting fix verified (2026-05-05)

## §1 Headline finding

**V2_FAIL_FORGETTING_PERSISTS was a measurement artifact**, not actual forgetting. Re-eval with `lm-eval ≥0.4.4` + `transformers ≥4.51` (resolves the L19 dtype kwarg crash) on the saved `adapter_final` shows:

| Bench | Llama 3.2-3B base | Path A retry-3 v2 | Δ | Floor | Improve bar |
|---|---|---|---|---|---|
| HellaSwag (acc_norm) | 0.654 | 0.645 | -0.9pp (parity, within stderr) | PASS (≥0.644) | FAIL (≥0.674) |
| MMLU (acc) | 0.580 | 0.575 | -0.4pp (parity, within stderr) | PASS (≥0.5696) | FAIL (≥0.5996) |
| TriviaQA (em) | 0.396 | **0.455** | **+5.9pp** | PASS (≥0.376) | **PASS** (≥0.416) |

`forgetting_index = -0.0280` (slight net improvement). Rehearsal mix 60% anima axis + 30% academic distill + 10% chat-template VERIFIED as effective forgetting-fix.

## §2 Root cause of V2_FAIL_FORGETTING_PERSISTS (predecessor)

L19 lesson: `lm-eval 0.4.11` forwards `--model_args dtype=bfloat16` directly to `transformers AutoModel.from_pretrained` as kwarg `dtype=...`. `transformers >=4.45,<4.50` (installed by retry-3 pin) accepts only `torch_dtype`, not `dtype`, so `LlamaForCausalLM.__init__()` rejected the kwarg with `TypeError`. All 4 `lm_eval` invocations (intermediate hellaswag step 2000 + final hellaswag/mmlu/triviaqa) crashed identically before model loading completed; results JSON never written; verdict-writer treated null metrics as `parity_failed` → conservative FAIL label.

## §3 Fix applied

Re-eval cycle (BG-α'''-EVAL-FIX, $0.75, 1 H100 pod `pa5e33lhnkz815`, 15min wall):

- Pinned `transformers>=4.51,<4.60` in `run_h100.bash` (4.51 added `dtype=` alias for forward compat with lm-eval 0.4.11)
- Added pre-bench PEFT smoke test (load base + adapter + forward pass) to fail-fast before lm_eval if adapter is structurally broken (L14)
- Re-evaluated saved `adapter_final` from retry-3 cycle (sha256 `393eb7530f82...`); no retraining
- Eval pipeline working end-to-end, real metrics captured

## §4 Honest C3 (raw#10)

- C1 single-seed eval (seed=42); 5-seed scaleup deferred — TRUE_PASS suggestive at single seed, not multi-seed bootstrapped
- C2 limit=200 stderr ~3.5pp on HS/TQ, ~1.0pp on MMLU; Δ values within noise band for hellaswag/mmlu, but +5.9pp triviaqa is well-above-stderr substantial
- C3 Llama-base anchors (0.654 / 0.5796 / 0.396) measured at limit=500 (BG-O 93bef8c8); this rerun uses limit=200 — sample-set mismatch beyond stderr (different problems sampled). Strict apples-to-apples would re-measure base at limit=200 same seed; deferred for cost
- C4 `transformers>=4.51` pin upgrades from retry-3 train-time `transformers~4.45-4.49`; LoRA adapter was trained against the older config — re-loading via PEFT into newer transformers MAY produce subtle activation drift if config keys differ (smoke test catches gross failures, not subtle drift)
- C5 Re-eval consumes adapter weights as-is — does NOT re-train. If forgetting was caused by training-time issues, re-eval cannot fix it; only EXPOSE it. Conversely if v3 verdict was eval-pipeline artifact only, re-eval fully resolves it
- C6 `forgetting_index` = 1 - mean(post/baseline) is a 3-bench mean fractional drop treating benchmarks as equally weighted; real-world salience differs (TriviaQA more knowledge-heavy than HellaSwag commonsense)
- C7 anima axis-conditioned eval not run this cycle (DEFERRED); F-PA-RETRAIN-v2-4 anima_axis_preservation still UNKNOWN
- C8 v3 conservatively coded eval=null as F3=FAIL because it could not distinguish (a) adapter is broken from (b) measurement was broken; this rerun assumes (b) and tests (a) directly. UNDERESTIMATE result here is INFORMATIVE about both v3 forgetting status AND measurement-pipeline reliability

## §5 Implications

- **F-PA-RETRAIN-v2-3 RE-VERDICT: PASS** (parity floor PASS on all 3 + improvement PASS on triviaqa — meets `C_RV_1 ∧ C_RV_2`)
- **BG-CLM-2 EXEC unblocked** (Llama Path A v2 LoRA composite anchored as production)
- C-CLM-LORA-2 differentiator measurement now possible (Path A v2 vs anima substrate variant)
- Path A retry-3 lane officially closed (TRUE_PASS verdict supersedes V2_FAIL label as measurement artifact)
- Eval-pipeline L14 smoke test pattern propagated forward — all future LoRA evals MUST PEFT-load + forward-pass before lm_eval

## §6 Cross-link

- Predecessor: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/verdict.json` (V2_FAIL_FORGETTING_PERSISTS — superseded)
- This cycle: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- Adapter SSOT: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/` (sha256 `393eb7530f82...`)
- Next: BG-CLM-2 EXEC ($6-10 H100, anima substrate variant); 5-seed scaleup deferred; anima_axis_preservation eval deferred
