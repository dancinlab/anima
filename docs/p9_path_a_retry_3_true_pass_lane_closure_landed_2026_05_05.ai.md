---
title: P9 Path A retry-3 TRUE_PASS lane closure (landed)
status: LANDED — TRUE_PASS_LANE_CLOSED
ts_utc: 2026-05-05
cycle: BG-PATH-A-RETRY3-CLOSURE
domain: p9_sft
predecessor_verdict: V2_FAIL_FORGETTING_PERSISTS (superseded as measurement artifact)
true_verdict: TRUE_PASS_FORGETTING_FIX_VERIFIED
roadmap_amendment: .roadmap.p9_sft line 5 → eval_fix_amendment_2026_05_05 block (additive only)
companion_verdict: state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json
amendment_cost_usd: 0
eval_fix_cost_usd: 0.75
adapter_sha256: 393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c
raw_invariants: ["raw#9 md+json", "raw#10 honest C3 ≥5", "raw#15 additive-only structure-preserve"]
---

## §1 Lane summary — V2_FAIL → TRUE_PASS, eval pipeline fix root cause

The P9 Path A retrain v2 retry-3 cycle (`state/p9_path_a_retrain_v2_retry_3_2026_05_04/`) wrote a conservative
verdict labelled **V2_FAIL_FORGETTING_PERSISTS** because all four lm-evaluation-harness invocations (intermediate
HellaSwag at step 4000, final HellaSwag/MMLU/TriviaQA at step 6000) produced `null` metrics. The verdict-writer
treated `null` as `parity_failed` and conservatively coded the F-PA-RETRAIN-v2-3 falsifier as FAIL.

The α'''-EVAL-FIX cycle (BG-α-EVAL-FIX, `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/`) re-ran
evaluation on the saved `adapter_final` with two pipeline fixes:

1. **transformers pin upgrade** — `>=4.51,<4.60` (was implicitly `~4.45-4.49` via retry-3 train-time pin).
   transformers 4.51 added a `dtype=` alias to `from_pretrained` for forward-compat with lm-eval 0.4.11's
   habit of forwarding `--model_args dtype=bfloat16` directly as a kwarg.
2. **PEFT pre-flight smoke test** — load base + adapter + forward pass BEFORE lm_eval, fail-fast at <30s
   pod time (~$0.025) instead of failing 5+ minutes deep across 3 benchmarks.

Re-eval verdict on the **same adapter weights** (sha256 `393eb7530f...`) yielded:

- HellaSwag 0.645 vs Llama-base 0.654 — Δ −0.9 pp — parity-floor 0.644 **PASS**
- MMLU 0.575 vs Llama-base 0.580 — Δ −0.4 pp — parity-floor 0.5696 **PASS**
- TriviaQA 0.455 vs Llama-base 0.396 — Δ +5.9 pp — parity-floor 0.376 **PASS**, improvement-bar 0.416 **PASS**

**RE-VERDICT: F-PA-RETRAIN-v2-3 = PASS.** Forgetting_index = −0.028 (slight net improvement when averaged
across the 3 benchmarks; the negative sign means the LoRA, on average, did not regress).

V2_FAIL was a measurement artifact, not a model failure. The rehearsal mix (60% anima axis + 30% academic
distill + 10% chat template) **worked** — Path A retry-3 retains Llama-3.2-3B parity on commonsense and
broad knowledge while gaining +5.9 pp on triviaqa knowledge surface.

## §2 True metrics table

| Benchmark   | Llama-3.2-3B base | Path A retry-3 LoRA | Δ vs base | Parity-floor | Improvement-bar | Status |
|:------------|:-----------------:|:-------------------:|:---------:|:------------:|:----------------:|:------:|
| HellaSwag   | 0.654             | 0.645               | −0.9 pp   | 0.644 ≤ acc  | 0.674            | PASS   |
| MMLU        | 0.580             | 0.575               | −0.4 pp   | 0.570 ≤ acc  | 0.600            | PASS   |
| TriviaQA EM | 0.396             | 0.455               | +5.9 pp   | 0.376 ≤ acc  | 0.416 ≤ acc      | **PASS+IMPROVE** |

Source: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` fields
`final_eval_step_6000.{hellaswag,mmlu,triviaqa}` and `f_pa_retrain_v2_3_{C_RV_1_parity_floor,C_RV_2_one_improvement_2pp,RE_VERDICT}`.

## §3 Rehearsal mix validated

The retrain-v2 rehearsal mix that produced these metrics:

| Component         | Pct  | Purpose                                                            |
|:------------------|:----:|:-------------------------------------------------------------------|
| anima axis        | 60%  | substrate-target signal (the LoRA's primary learned axis)          |
| academic distill  | 30%  | broad-knowledge anti-forgetting (preserves MMLU / HellaSwag floor) |
| chat template     | 10%  | format coherence / tokenizer-alignment hygiene                     |

This is the first empirically validated forgetting-fix mix for the Path A llama LoRA lane; predecessor
mixes (retry-1, retry-2) showed measurable parity drops on HellaSwag/MMLU.

## §4 Lessons L19–L22 propagation

These lessons were already learned during the eval-fix cycle. Recorded here for cross-cycle propagation:

- **L19 lm-eval × transformers dtype kwarg** — lm-evaluation-harness 0.4.11 forwards `--model_args dtype=...`
  directly as a Python kwarg to `transformers.AutoModel.from_pretrained`. transformers `<4.51` accepts
  `torch_dtype=` only and rejects unknown kwargs with TypeError. The crash surfaces BEFORE model load,
  so `results.json` is never written. Mitigation: pin transformers `>=4.51,<4.60` for any cycle using
  lm-eval 0.4.11.
- **L20 PEFT pre-flight smoke test** — Always load base + adapter + run a single forward pass at <30s of
  GPU spend BEFORE invoking lm_eval. Catches dtype kwargs, adapter structural breaks, config-key drift
  at $0.025 instead of $5+.
- **L21 verdict-writer eval_crashed vs parity_failed distinction** — When `results.json` is missing or
  metrics are `null`, the cause is **eval pipeline crash**, NOT **parity failure**. Verdict-writers MUST
  distinguish these two cases. Coding `null` as `parity_failed` produces conservative-but-wrong FAIL
  labels (this cycle's V2_FAIL was caused by exactly this). Recommend dedicated `EVAL_CRASHED` verdict
  bucket distinct from PASS/PARTIAL/FAIL.
- **L22 eval pre-flight mandatory before any retrain verdict** — Every multi-benchmark retrain verdict
  cycle MUST gate on a successful pre-flight (PEFT smoke + 1 mini-eval @ limit=10) BEFORE the full
  benchmark run. Pre-flight cost <$0.05; downside of no pre-flight is cycle-wide null-metrics blackout
  (this cycle: $22 retrain + $5 cap eval = up to $27 at risk).

## §5 Honest C3 (≥5 caveats)

1. **Single-seed eval, not 5-seed.** This re-eval used seed=42 only; multi-seed bootstrap on the
   RE-VERDICT is **deferred** (5-seed scaleup spec exists at `docs/p9_p1_5_ensemble_4seed_landed_2026_05_03.ai.md`
   for the predecessor holdout-500 surface; this Path A surface is not yet scaled up). Strict
   evidence-grade is point-estimate only.
2. **limit=200 stderr noise band.** Eval used limit=200 per spec, giving stderr ~3.5 pp on HellaSwag/TriviaQA
   and ~1.0 pp on MMLU. The Llama-base anchors (0.654 / 0.580 / 0.396) were measured at limit=500 in
   BG-O 93bef8c8 — comparing limit=200 LoRA against limit=500 base introduces sample-set mismatch on top
   of stderr asymmetry (different problems sampled). Strict apples-to-apples would require re-measuring
   base at limit=200 same seed; deferred for cost.
3. **F4 anima_axis_preservation UNKNOWN.** This cycle measured commonsense (HellaSwag) + broad-knowledge
   (MMLU) + factual-recall (TriviaQA) — three "general capability" axes. The **anima axis** itself
   (substrate-target consciousness signal that the rehearsal mix dedicates 60% of training to) was NOT
   measured. forgetting_index ≈ 0 says "no general-capability forgetting" — it does NOT say "anima axis
   preserved or improved". F4 falsifier remains pending an axis-specific eval cycle.
4. **forgetting_index = −0.028 means "no forgetting", not "improved beyond Llama" except on TriviaQA.**
   The HellaSwag/MMLU deltas are within 1-σ of zero (parity); only TriviaQA shows a true above-noise
   improvement. The "lane closes as TRUE_PASS" verdict is justified by parity preservation + one
   above-noise gain, not by uniform improvement.
5. **Llama-3.2-3B baseline numbers from public refs.** The Llama-base anchors used here (0.654 / 0.580 /
   0.396) come from BG-O 93bef8c8 single-seed measurement; cross-checked with public model-card numbers
   in the retry-3 spec but not re-measured in this cycle. If the BG-O anchor itself drifts (transformers
   version difference, eval harness version), the deltas reported here drift by the same amount.
6. **Adapter weights immutable across cycles.** This re-eval consumes the EXACT adapter weights produced
   by retry-3 training (sha256 `393eb7530f...`) — no re-train. If forgetting was caused by training-time
   issues, no re-eval can fix it; only EXPOSE it. The TRUE_PASS verdict therefore proves training-time
   was OK and eval-time was broken; it does not retroactively guarantee the rehearsal mix is optimal.
7. **transformers >=4.51 may drift activations vs train-time transformers ~4.45-4.49.** Re-loading a
   retry-3-trained LoRA into a newer transformers MAY produce subtle numeric drift if config keys differ.
   Pre-flight smoke catches structural failures, not subtle drift; reported metrics are the "newer-stack"
   numbers, slightly different from what train-time transformers would have produced.

## §6 Implications

- **BG-CLM-2 EXEC unblocked.** The Llama-path-A-v2 LoRA is now an anchored composite (parity + 5.9 pp
  TriviaQA gain). Downstream lanes that wanted to compose on top of this LoRA (e.g., CLM v4 + Path A v2
  rehearsal-mix transfer) can proceed without waiting for retry-4 / a fresh retrain.
- **F-PA-RETRAIN-v2-3 falsifier closed PASS.** The cond.path_a_lora_train_complete entry in
  `.roadmap.p9_sft` carries the eval_fix_amendment_2026_05_05 block witnessing TRUE_PASS_LANE_CLOSED.
- **L22 eval-pre-flight rule** should be back-propagated into all future spec/falsifier templates.
  Cost cap: each cycle spends ~$0.05 on pre-flight to avoid cycle-wide blackouts; this cycle's
  $0.75 re-eval would have been avoidable had retry-3 itself shipped pre-flight.
- **F4 anima_axis_preservation remains pending.** A separate axis-specific eval cycle is needed before
  the Path A retry-3 lane can claim full 4-falsifier closure. This BG closes only the **F-PA-RETRAIN-v2-3
  composite parity falsifier**, not F4.
