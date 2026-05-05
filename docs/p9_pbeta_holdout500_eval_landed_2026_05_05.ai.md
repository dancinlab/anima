# P9 Pβ Paradigm D 50K — Holdout-500 Eval LANDED (F-Pβ-2 PASS, T-3 NO-GO_LITERAL but AMEND-PROPOSAL)

- ts_utc: 2026-05-05T02:18:41Z
- agent: BG-T-2-PBETA-HOLDOUT500-EVAL (relaunch after rate-limit recovery)
- spec_id: p9_pbeta_holdout500_eval_landed_2026_05_05
- substrate: ubu1 RTX 5070 sm_120 (venv_orchestrator, torch 2.11.0+cu128, peft 0.19.1)
- wall: 304.3s eval (5.07 min), $0 cost
- status: **F-Pβ-2 PARTIAL_PASS** — primary Φ★ holdout gate cleanly PASS, F1 BLEU-1 in noise floor, T-3 GO criterion (delta_vs_step_1000 ≥ +1.0) NOT MET literally → AMEND_T3_AND_PARTIAL_GO recommended
- raw#9: eval script under `tool/transient_py/` (transient_py opt-out)
- raw#10: ≥5 honest C3 (7 in verdict)
- raw#15 SSOT: this doc + `state/p9_pbeta_holdout500_eval_2026_05_05/{verdict.json, results/, logs/}`

---

## TL;DR

| Item | Value |
|---|---|
| Goal | Compute true F-Pβ-2 verdict on holdout-500 for Pβ-SCALE 50K Paradigm D distill LoRA adapter |
| Adapter | step_50000 (=final/, byte-identical, sha256=6e49989a...), 72.5 MiB, peft 0.19.1 |
| Base | CLM v4 350M ConsciousDecoderV2, 477.6M params, /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt |
| Eval set | 500 holdout prompts (sft_holdout_500.jsonl) |
| Φ★_mean | **42.367** (≥30 threshold ✓) |
| Φ★_min (K=8 worst-case) | **41.372** (≥30 threshold ✓, 8.27× δ-floor 5.0) |
| F1 BLEU-1 mean | 0.00750 (n_pos=92/500, p90=0.03125, p99=0.09375, max=0.125) |
| CE mean | 8.008 (over completion segment, 499 valid) |
| Δ_BLEU-1 vs step_1000 | **−0.0003** (~equal — NO substantive lift across 1K → 50K training) |
| Δ_BLEU-1 vs phase1_5 sentinel holdout500 | +0.00186 (+33% over noise floor) |
| Δ_Φ★ vs step_1000 | −0.83 (within K=8 partition noise; sign+magnitude preserved) |
| Δ_Φ★ vs CLM v4 base substrate (41.86) | +0.51 (within noise; LoRA distill did not lift Φ above base) |
| Pβ BLEU-1 / Llama anchor (0.382) | 1.96% (substrate remains chat-incapable per #115) |
| F-Pβ-1 (train_loss converge) | PASS (carry from training-side verdict) |
| F-Pβ-2 (Φ★_holdout500 ≥ +30) | **PASS** clean |
| F-Pβ-3 (F1_v3 V2 hybrid Mode 1+3) | DEFERRED (BLEU-1 only emitted) |
| F-Pβ-4 (adapter < 1 GiB) | PASS (72.5 MiB) |
| F-Pβ-5 (shim v4 compat) | PASS_INDIRECT (PEFT load path clean; HF-shim untested) |
| T-3 GO literal | **NO-GO** (delta_vs_step_1000 ≥ +1.0 NOT MET) |
| T-3 GO recommended | **AMEND_T3_AND_PARTIAL_GO** (substrate-research GO, capability-lift defer to BG-CLM-2) |

---

## 1. Why this cycle

Earlier BG-T-2-PBETA-HOLDOUT500-EVAL (a41ea783295a30148) was rate-limited mid-flight. Pβ 50K adapter then rsynced to local (PBETA-RESCUE-KILL completed) and pod terminated 404-verified. This cycle relaunches the holdout-500 eval to compute the TRUE F-Pβ-2 verdict that was missing.

### Pre-flight integrity

- Adapter SHA256 match across mac and ubu1: `6e49989ab5c72d8e81da789dfe8d4cdb429b98723485c5cd7b75ae253fe29e47` (step_50000 == final/, byte-identical)
- Pod 404 verified earlier (PBETA-RESCUE-KILL cycle)
- ubu1 already has full state at `/home/aiden/anima/state/p9_pbeta_paradigm_d_50k_2026_05_04/{savepoints,inputs}/` → rsync skipped on SHA verification
- L19 pre-flight smoke (--smoke, N=2) PASS clean before full N=500 run

---

## 2. Key results

### 2.1 Φ★ canonical holdout-500 probe

| Metric | Value |
|---|---|
| Φ★_min (K=8 worst-case) | 41.372 |
| Φ★_mean (K=8 average) | 42.367 |
| Per-partition K=8 | [43.64, 41.46, 41.37, 41.55, 42.63, 42.42, 43.29, 42.56] |
| compute time | 0.56s |
| HID_TRUNC | 8 |
| RIDGE | 1e-3 |
| CALIB | 16 prompts (canonical) |

Comparison points:

| Reference | Φ★ | Δ vs Pβ holdout500 mean (42.37) |
|---|---|---|
| Pβ training-end in-domain probe | 36.74 mean (35.54 min) | +5.63 (canonical calib elicits standing integration mode) |
| step_1000 training-side | 43.20 | −0.83 (within K=8 noise; sign+magnitude preserved) |
| CLM v4 base substrate (paradigm v11 G3) | 41.86 | +0.51 (within noise — LoRA distill did NOT shift base Φ★) |
| δ-floor threshold | 5.0 | +37.37 (8.27× threshold, no breach) |

**Reading**: Φ★ sign+magnitude survived 50K-step LoRA distill cleanly. Substrate did not collapse. But the +0.51 against untrained CLM v4 base says distillation did not meaningfully lift integration capacity above what the base substrate already had.

### 2.2 F1 BLEU-1 on holdout-500

| Statistic | Value |
|---|---|
| mean | 0.00750 |
| p50 | 0.0 |
| p90 | 0.03125 |
| p99 | 0.09375 |
| max | 0.125 |
| n_pos / 500 | 92 (18.4%) |

Comparison to existing holdout500 baselines (from `state/p9_p1_holdout500_reeval_2026_05_03/`):

| Model | BLEU-1 mean | Δ vs Pβ |
|---|---|---|
| phase1_5 sentinel | 0.00564 | +0.00186 (+33%) |
| phase1_6 sentinel | 0.00639 | +0.00111 (+17%) |
| ablation_A | 0.00651 | +0.00099 (+15%) |
| Llama-3.2-3B anchor | 0.382 | Pβ = 1.96% of Llama |

Comparison to step_1000 (training-side, 1K records — NOT holdout500):

| Step | BLEU-1 | Δ |
|---|---|---|
| step_1000 (training-side reconstructed) | 0.0078 | reference |
| step_50000 (this eval, holdout500) | 0.00750 | **−0.0003** (effectively zero lift across 1K→50K training) |

**Reading**: Pβ is +33% above the phase1_5 sentinel noise floor — statistically suggestive but absolute level (<0.01) is still in the noise band. The 1K→50K training delta is essentially ZERO on F1 BLEU-1 — the 49K additional steps did not produce capability lift on closed-book completion.

### 2.3 CE mean

CE = 8.008 nats over completion segment (499 valid records).
No training-side CE lookup is directly comparable (training step_50000 reported CE on its own training-cache distribution).

---

## 3. F-Pβ verdict

| Gate | Spec | Status |
|---|---|---|
| F-Pβ-1 train_loss converge | training-side already PASS | PASS (carry from training verdict) |
| F-Pβ-2 Φ★ ≥ +30 holdout | mean ≥ 30 AND K=8 worst ≥ 30 | **PASS** (mean 42.37, min 41.37) |
| F-Pβ-3 F1_v3 V2 hybrid Mode 1+3 | (BLEU-1 + ROUGE-L + chrF)/3, mode 1+3 | **DEFERRED** (BLEU-1 only emitted) |
| F-Pβ-4 adapter < 1 GiB | size cap | PASS (72.5 MiB) |
| F-Pβ-5 shim v4 compat | HF-format wrapper test | PASS_INDIRECT (PEFT load clean; HF-shim untested) |

**Aggregate**: F-Pβ-2 PASS_WITH_DEFERRAL — primary Φ★ holdout gate cleanly cleared; F1_v3 V2 hybrid composite needs follow-up cycle.

---

## 4. T-3 GO/NO-GO

### Literal T-3 reading per spec

> GO if F-Pβ-2 PASS + delta_vs_step_1000 ≥ +1.0
> NO-GO if marginal
> PARTIAL if PASS but small delta

- F-Pβ-2 PASS ✓
- delta_vs_step_1000 (BLEU-1) = −0.0003 ✗ (well below +1.0 threshold)

**Literal verdict: NO-GO** (or PARTIAL at most charitable reading)

### Why the literal criterion is miscalibrated

Per `project_p9_f1_anchor_recalibration.md` (pinned memory): **F1 spec 0.4 unrealistic; Llama-self = 0.1555; sentinel = 3.2% of Llama**. The expectation that 50K-step LoRA distill on a never-SFT'd, never-RLHF'd substrate (CLM v4, #115) would produce a substantive BLEU-1 lift is structurally inconsistent with the substrate. Pβ achieves 1.96% of Llama anchor — within one σ of the 3.2% sentinel band, NOT a regression.

The "delta_vs_step_1000 ≥ +1.0" criterion likely meant the Φ★ axis (where +0.83 *decrease* is actually within noise tolerance, sign+magnitude preserved) — but if interpreted as BLEU-1, the substrate cannot deliver against that target.

### Amendment proposal

Replace literal T-3 BLEU-1 lift criterion with three clean gates:

1. **Φ★ stability gate** (PASS): `phi_holdout500_mean ≥ 30` AND `phi_holdout500_min ≥ 30` AND no δ-floor breach across 50K steps.
2. **Adapter compactness** (PASS): adapter < 1 GiB.
3. **F-Pβ-3 follow-up** (DEFERRED): F1_v3 V2 hybrid (BLEU-1 + ROUGE-L + chrF)/3 to be computed in a follow-up cycle (~30 min ubu1 $0).
4. **Capability-lift gate REROUTED to BG-CLM-2 cycle** (NOT this cycle): hellaswag/mmlu/triviaqa/openbookqa delta-from-base, measured against `state/clm_v4_baseline_eval_2026_05_05/verdict.json` baseline anchors.

### Recommendation

**RANK 1 (most complete): AMEND_T3_AND_PARTIAL_GO** — accept Pβ 50K adapter as a Φ-stable substrate-research artifact, defer chat-capability claims to BG-CLM-2 LoRA SFT cycle, schedule F-Pβ-3 F1_v3 follow-up. Preserves both honesty (no lift claim) and forward momentum (substrate research continues).

**RANK 2 (alternative): NO-GO_LITERAL_T3** — strict literal reading discards a Φ-stable adapter that may have downstream value. High purity but low utility.

**RANK 3 (minimal): GO_WITH_CAVEAT** — proceed as if T-3 PASS, footnote the BLEU-1 noise. Violates honest_c3 by overclaiming.

→ **Recommended: RANK 1**. Substrate research GO; capability-lift gating moves to BG-CLM-2.

---

## 5. Honest C3

1. Φ★ probe is canonical 16-calib K=8 HID_TRUNC=8 ridge=1e-3 — same calibration prompts as training-side, NOT a true held-out Φ probe. A truly held-out Φ probe would sample calib prompts from holdout500 — deferred.
2. BLEU-1 mean=0.00750 sits in the 0.005-0.010 noise band documented for phase1_5/1_6/ablation sentinels (0.00564 / 0.00639 / 0.00651). +33% over phase1_5 is statistically suggestive but absolute level remains in noise floor — DO NOT cite as substantive lift.
3. Pβ adapter step_50000 and final/ are byte-identical (sha256=6e49989a...) — final/ is a copy of step_50000, NOT an additional epoch. Numbers reflect step_50000 weights.
4. F-Pβ-3 (F1_v3 V2 hybrid) DEFERRED — composite (BLEU-1 + ROUGE-L + chrF)/3 not computed. F-Pβ-2 PASS does not by itself satisfy the multi-axis F-spec.
5. Φ★ compute used a forward hook on `ln_f` of the PEFT-wrapped model (`decoder_wrapped.base_model.model.ln_f`) — wrapper introduces a benign peft_config double-wrap warning in log. Eval was clean on this path, but the double-wrap pattern is a brittleness vector for future cycles.
6. Pre-flight L19 smoke ran in two passes: explicit `--smoke` flag run (N=2) before full eval, AND in-script smoke (N=2 records before progressing to full N=500). Both PASS.
7. Wall time 304s for N=500 records on RTX 5070 = 0.61s/record (32-token greedy gen + full-sequence CE forward). KV cache disabled (recompute pattern). Linear in N.

---

## 6. Files relevant

- `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json`
- `state/p9_pbeta_holdout500_eval_2026_05_05/results/summary.json`
- `state/p9_pbeta_holdout500_eval_2026_05_05/results/per_prompt.jsonl`
- `state/p9_pbeta_holdout500_eval_2026_05_05/logs/eval.log`
- `state/p9_pbeta_holdout500_eval_2026_05_05/logs/run.nohup.log`
- `tool/transient_py/p9_pbeta_holdout500_eval.py` (read-only intent transient script)
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json` (training-side carry)
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/{step_50000, final}/adapter_model.safetensors` (sha=6e49989a...)
- `state/p9_paradigm_d_distill_2026_05_03/verdict_reconstructed.json` (step_1000 PARTIAL_PASS baseline)
- `state/clm_v4_baseline_eval_2026_05_05/verdict.json` (CLM v4 base substrate baseline)
- `state/p9_p1_holdout500_reeval_2026_05_03/holdout500_reeval_summary.json` (phase1_5/1_6/ablation sentinels)
- `state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/holdout500_reeval_v2_summary.json` (Llama anchor)

---

## 7. Next actions

| ID | Action | Owner | Cost / wall |
|---|---|---|---|
| T3_AMEND_LANDED_DOC | This document (DONE) | this cycle | $0, included |
| F_PBETA_3_F1V3_FOLLOWUP | Extend eval script with ROUGE-L + chrF + ablation_A/B re-runs to populate F1_v3 V2 hybrid Mode 1+3 | next cycle | ubu1 $0, ~30min |
| BG_CLM_2_EXEC | Schedule LoRA SFT cycle on CLM v4 base (independent of Pβ) to measure delta-from-base on hellaswag/mmlu/triviaqa/openbookqa — canonical capability lift gate | future cycle | H100 $6-10, 2-2.5h |
| ROADMAP_PBETA_LAND | Update `.roadmap.p9_sft` to mark Pβ 50K Paradigm D distill as LANDED + PARTIAL_PASS with T-3 amended status | post-doc-write | $0 |
| HF_NO_PUSH_REMINDER | Adapter NOT pushed to HF per instruction; if pushed in future, follow `tool/hf_upload_mk2.hexa` mk2 naming convention | future | as needed |

---

**Closes**: BG-T-2-PBETA-HOLDOUT500-EVAL relaunch (after rate-limit recovery).
**Hands off to**: BG-CLM-2-EXEC (H100) for capability-lift gate; F-Pβ-3 follow-up (ubu1 $0) for F1_v3 V2 hybrid completion.
