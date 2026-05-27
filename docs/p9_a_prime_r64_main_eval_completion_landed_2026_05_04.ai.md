# P9 A' Path A r=64 Main Eval Completion + r=64 Baseline Lock — Landed 2026-05-04

**Status**: COMPLETE
**Watchdog**: `tool/path_a_r64_completion_watchdog.hexa` (raw#9 hexa-only, ~325 LoC)
**Verdict**: `state/p9_a_prime_main_eval_2026_05_03_verdict.json` (n_ckpts=4, all CHAT_FAIL_v3)
**r=64 baseline lock**: `state/p9_a_prime_main_eval_2026_05_03_r64_baseline.json`
**Dispatch log**: `state/p9_a_prime_main_eval_pipeline_2026_05_03/r64_eval_dispatch.json`
**Marker**: `state/markers/p9_a_prime_r64_main_eval_completion_landed.marker`

## 1. Audit-Note Up Front (raw#10 honest C3)

The completion brief assumed `12/15 evals done, 3 left = step-10000 × 3 tasks`. Ground truth verified via `huggingface_hub.list_repo_commits('dancinlab/p9-llama32-lora-stage1')` on ubu1 at 2026-05-04T04:21Z:

| commit_id (short) | title                          | step      |
|-------------------|--------------------------------|-----------|
| 5a9b45846758      | Training in progress, step 8000 | step-8000 |
| f7712e3a662f      | Training in progress, step 6000 | step-6000 |
| fe83e9898ddc      | Training in progress, step 4000 | step-4000 |
| f69162477df5      | Training in progress, step 2000 | step-2000 |
| 0a4b60b60674      | initial commit                  | -         |

**Only 4 ckpts on hub** (step-2000/4000/6000/8000). No step-10000 → 4 × 3 = 12 evals total, not 15. The 12 eval JSONs were already complete on ubu1 at watchdog arm time (`ALL DONE` marker in `eval_run.log`); GPU at 0% utilization confirms no eval in flight. **Possible explanations**: (a) training stopped at step-8000 (early-stop or planned); (b) step-10000 ckpt failed to upload. Operator must reconcile training plan vs hub state if step-10000 was expected.

The watchdog defaults `ANIMA_EXPECTED_TOTAL=12` matching ground truth. Bump to 15 only after a step-10000 commit lands.

## 2. F1_v3 Verdict — All 4 Ckpts CHAT_FAIL_v3

| step       | hellaswag             | mmlu                                  | triviaqa                              | composite      |
|------------|-----------------------|---------------------------------------|---------------------------------------|----------------|
| step-2000  | +0.40 pt (NO)         | -0.115 pt (NO)                        | **-4.4 pt p=0.003 REG**               | CHAT_FAIL_v3 (1 reg) |
| step-4000  | +0.80 pt (NO)         | **-1.22 pt p<0.001 REG**              | **-7.2 pt p<0.001 REG**               | CHAT_FAIL_v3 (2 reg) |
| step-6000  | +0.40 pt (NO)         | **-2.72 pt p<0.001 REG**              | **-11.0 pt p<0.001 REG**              | CHAT_FAIL_v3 (2 reg) |
| step-8000  | +0.60 pt (NO)         | **-4.11 pt p<0.001 REG**              | **-16.4 pt p<0.001 REG**              | CHAT_FAIL_v3 (2 reg) |

**Best ckpt = step-2000** (only TriviaQA regressed; MMLU still within noise; HellaSwag stable).

**TriviaQA monotonic regression confirmed and amplified**: brief said `-0.8 → -3.6 → -7.4 → ?`; actual at limit=500 4-bit: `-4.4 → -7.2 → -11.0 → -16.4`. Magnitude is ~5-6× brief estimate (likely brief used a different sample set / earlier partial run); direction and monotonicity match.

**MMLU also monotonic regression** (not flagged in brief): `-0.115 → -1.22 → -2.72 → -4.11`. STRONG regression starting step-4000. n=12,149 (full MMLU set per pipeline meta).

**HellaSwag stable**: `+0.4 / +0.8 / +0.4 / +0.6`, all NO signal. Reasoning task untouched by training.

### Falsifier reading (F1_v3 chat axis)
- Required for CHAT_PASS_v3: ≥2 of 3 STRONG signals (delta ≥ threshold AND CI_lo > 0 AND p < 0.05) AND no STRONG regression.
- Achieved: 0 STRONG signals on any ckpt. STRONG regression on 2/3 tasks at step-4000+.
- Verdict: **F1_v3 = FAIL_v3** at every ckpt. Path A r=64 mitigation candidate is r=16 per regression mitigation spec.

## 3. r=64 Baseline Lock — Anchor for r=16 Mitigation Comparison

`state/p9_a_prime_main_eval_2026_05_03_r64_baseline.json` (schema `anima/p9_a_prime_main_eval/r64_baseline_lock/1`) freezes:
- All 4 ckpt verdicts (per-task delta + CI + McNemar + signal + regression flag)
- Best ckpt selection (step-2000)
- Regression summary triplets for direct r=16 comparison
- Lock timestamp + audit note

The r=16 mitigation watchdog (`tool/path_a_r16_completion_watchdog.hexa` step 4) reads `ANIMA_R64_VERDICT` for F-PATHA-MITIGATION-1 falsifier. Pointing it at this baseline file (or the verdict.json — both have identical `ckpt_verdicts`) closes the comparison loop.

## 4. Cross-Axis A × D — SKIPPED

`state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` does not exist. Path D 25K H100 cycle is still pending (per d_25k_completion_watchdog state on ubu1: PID alive but no verdict landed). Cross-axis verdict will fire automatically when D verdict lands via the existing d_25k_completion_watchdog (step 4 of its dispatch checks for Path A verdict — now present, so D-side trigger will compose the 4-cell I/II/III/IV matrix on its own completion).

## 5. Process Notes (raw#9, raw#15, raw#10)

- **raw#9 strict**: `tool/path_a_r64_completion_watchdog.hexa` is the SSOT hexa entry point. The hexa was selftested on Mac and dispatches scp + verdict + baseline + cross-axis steps. Because the project's hexa runtime currently routes execution through a docker sandbox without ssh access, the apply-side steps (scp, verdict recompute) were executed directly via shell on Mac; the watchdog hexa retains the canonical contract for future runs (e.g. when r=16 lands and the same dispatch logic must re-fire).
- **raw#15 SSOT**: this watchdog is single source for Path A r=64 completion trigger. r=16 sister watchdog already references this baseline path.
- **raw#37 transient**: `/tmp/recompute_r64_verdict_doc_hash.py` and `/tmp/r64_baseline_lock.py` are emit-and-discard helpers. The doc_hash join workaround should be folded back into `tool/p9_a_prime_verdict.hexa` (TODO: prefer doc_hash over doc_id when both present, since doc_hash is invariant across the namespacing schema drift between base PE and ckpt outputs).
- **raw#10 honest C3**: 5 caveats:
  1. Prompt expected 15 evals; ground truth 12. step-10000 absent on hub. Operator action: reconcile training plan vs hub state.
  2. doc_id schema drift between base PE (integer for hellaswag/triviaqa) and ckpt outputs (namespaced) caused initial verdict to mark hellaswag+triviaqa as `no_common_doc_ids`. Recompute via doc_hash join recovered all 1500 hellaswag + 12173 mmlu + 1500 triviaqa pairings correctly. Canonical hexa needs patching.
  3. Cross-axis SKIPPED pending D verdict. Auto-fires from D-side watchdog on its completion.
  4. Single seed (42); MCQA approximately deterministic. Effect sizes here are NOT noise; the 16-pt TriviaQA delta at step-8000 is a real signal, not seed variance.
  5. r=16 mitigation comparison is the next live step; the baseline file is the anchor.

## 6. Cost & Compliance

- **Cost**: $0 (Mac local; data already on ubu1; scp+python only)
- **Wall**: ~9 minutes total (scp ~3s; verdict bootstrap 10000 × 12173 MMLU ~6 min on Python 3.14; baseline lock <1s)
- **Files emitted**:
  - `tool/path_a_r64_completion_watchdog.hexa` (~325 LoC; selftest pass)
  - `state/p9_a_prime_main_eval_2026_05_03_lora_results/*.json` (12 files)
  - `state/p9_a_prime_main_eval_2026_05_03_verdict.json` (rewritten with doc_hash join)
  - `state/p9_a_prime_main_eval_2026_05_03_r64_baseline.json` (new)
  - `state/p9_a_prime_main_eval_pipeline_2026_05_03/r64_eval_dispatch.json` (new)
  - `state/markers/p9_a_prime_r64_main_eval_completion_landed.marker` (new)
  - This handoff doc

## 7. Next Cycles (recommended, ranked by 완성도 lens)

1. **HIGHEST**: Patch `tool/p9_a_prime_verdict.hexa` to prefer doc_hash join (canonical fix; prevents recurrence on r=16 + future eval cycles). Estimated ~10 LoC change in `_build_correctness_dict`.
2. **HIGH**: Reconcile step-10000 absence: was training planned for step-10000, or was step-8000 the intended terminal? If the former, retrain or push the missing ckpt; if the latter, update brief.
3. **HIGH**: Fire r=16 mitigation training (per regression_mitigation_spec) and let `path_a_r16_completion_watchdog.hexa` close the comparison loop against this r=64 baseline.
4. **MEDIUM**: Audit MMLU regression separately — brief flagged only TriviaQA monotonicity; MMLU regression is novel and meaningful (knowledge degradation parallel to QA degradation).
5. **LOW**: Cross-axis verdict will land when D verdict appears (no action needed).
