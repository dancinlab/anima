# P9 Path A retry-3 anima axis preservation eval — F-PA-RETRAIN-v2-4 landed (2026-05-05)

**Cycle**: `state/p9_path_a_retry_3_anima_axis_eval_2026_05_05/`
**BG lane**: `BG-ANIMA-AXIS-EVAL`
**Predecessor (eval-rerun)**: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` (F1/F2/F3/F5 PASS_TRUE per spec, F4 DEFERRED)
**Adapter**: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/adapter_model.safetensors` (sha256 `393eb753...`, 389 MB, r=64 LoRA, 7 target_modules, Llama-3.2-3B base)

## TL;DR

**F-PA-RETRAIN-v2-4 anima_axis_preservation = FAIL** — mean_preservation_score = **0.7871** vs PASS threshold 0.95 / PARTIAL threshold 0.85. All 5 anima axes (daily/emotion/task/roleplay/meta) score in 0.75–0.81 range; none cross the 0.85 PARTIAL boundary.

This **closes** the F4 DEFERRED status but does **NOT close** the Path A retry-3 lane to fully green: post-eval status is **F1=PASS F2=PASS F3=PASS F4=FAIL F5=PASS** (4-of-5).

Wall: **0.135 min (~8 sec)**. Cost: **$0** (ubu1 RTX 5070 bf16, no H100).

## Method

100-prompt eval set built from `bench/zeta_likert/v1_frozen.json` (5 anima axis categories × 4 axis-conditioning prefixes × 5 base prompts per category = 100 axis-conditioned prompts; 20 per axis, 20 native+conditioned matches, 80 cross-axis).

For each prompt, captured the last-layer last-token hidden state under (a) Llama-3.2-3B base with LoRA disabled via `PeftModel.disable_adapter()` context, (b) same model with adapter enabled. Per-axis mean vectors computed across the 20 prompts conditioned on that axis. Preservation score = `cosine(v_base[axis], v_lora[axis])` per axis; mean across 5 axes is the headline metric.

## Result

| Axis     | Preservation cosine |
|----------|--------------------:|
| daily    |              0.7994 |
| emotion  |              0.7868 |
| task     |              0.7908 |
| roleplay |              0.8068 |
| meta     |              0.7519 |
| **mean** |          **0.7871** |

Side-channel: axis-discrimination (mean pairwise cosine between distinct axis-mean vectors) was 0.9940 in base vs 0.9932 in LoRA — essentially unchanged. Combined with the FAIL preservation score, this means LoRA shifted ALL axes ~equally rather than collapsing axes onto each other.

## Caveats (honest_c3 highlights, full list in verdict.json)

1. **Axis-preservation is anima-internal, not industry-standard**. Spec thresholds 0.95/0.85 are not externally calibrated. F1/F2/F3/F5 (the behavioral gates) all PASS_TRUE per the eval-rerun cycle.
2. **adapter_config.json was MISSING** from the saved retry-3 adapter dir; reconstructed from spec doc + tensor-shape inspection (r=64, alpha=64, 7 target_modules). Smoke test forward pass succeeded so gross misconfiguration is ruled out.
3. **Base Llama-3.2-3B itself shows near-degenerate axis structure** (mean pairwise cos = 0.9940) on these KO conversational prompts. "Preservation of a near-degenerate signal" may not be meaningful — the base barely discriminates 5 axes to begin with.
4. **100 prompts is the spec-prescribed N**; 95% CI on cosine sim is ~±0.02-0.04, well below the 0.85 PARTIAL boundary, so verdict is robust to stderr.
5. **First attempt OOMed** on RTX 5070 (12 GB) due to dual-model load. Switched to single-model + `disable_adapter` context for the base pass, fits in <10 GB.
6. **Cost & wall**: $0 / 8 sec actual vs ~$0.30-0.60 / 1-2h spec estimate (99.7% under, ubu1 sufficient).

## Lane status

| Gate | Status | Source |
|------|--------|--------|
| F-PA-RETRAIN-v2-1 train_loss_converge | PASS | retry_3_eval_rerun (per spec) |
| F-PA-RETRAIN-v2-2 step_2000_no_5pp_drop | PASS | retry_3_eval_rerun (per spec) |
| F-PA-RETRAIN-v2-3 parity_floor + 1×improve_2pp | **PASS** (CRV1 PASS, CRV2 PASS) | retry_3_eval_rerun explicit |
| F-PA-RETRAIN-v2-4 anima_axis_preservation | **FAIL** (0.7871 < 0.85) | THIS CYCLE |
| F-PA-RETRAIN-v2-5 | PASS | retry_3_eval_rerun (per spec) |

**Path A retry-3 lane closure: 4-of-5 PASS (NOT fully green)**. Whether to treat this as effective lane PASS with axis caveat or strict lane FAIL on F4 is a downstream policy decision — per spec gates are AND-ed by default → strict lane FAIL.

## Files

- `state/p9_path_a_retry_3_anima_axis_eval_2026_05_05/verdict.json`
- `state/p9_path_a_retry_3_anima_axis_eval_2026_05_05/axis_eval_results.json` (per-prompt cosines)
- `state/p9_path_a_retry_3_anima_axis_eval_2026_05_05/eval_axis_preservation.py`
- `state/p9_path_a_retry_3_anima_axis_eval_2026_05_05/run.log`
- `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (100 axis-conditioned prompts)
- `state/anima_axis_eval_set_2026_05_05/build_prompts.py`

NOT git-committed per spec.
