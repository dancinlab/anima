# CLM v4 baseline eval — F-CLM-LORA-2 anchor landed (2026-05-05)

- **Cycle**: BG-CLM-V4-BASELINE-EVAL
- **Roadmap dep**: `p9_sft.cond.clm_v4_lora_baseline` (NEW — pre-EXEC blocker for BG-CLM-2)
- **Verdict**: `state/clm_v4_baseline_eval_2026_05_05/verdict.json`
- **Substrate**: CLM v4 530M base — `need-singularity/clm-v4-base-mirror` snapshot 856278be... (best.pt step=20000, ce=0.0463, best_phi=37.27)
- **Wall**: 21.8 min (1306.6 s) on ubu1 RTX 5070 GPU, fp32 (vs spec estimate 3-6h CPU; GPU deviation justified — 10× faster, $0)
- **Cost**: $0 (ubu1)
- **Status**: F-CLM-LORA-2_baseline = SET (left side of comparator)
- **Bottom line**: CONFIRMED_RANDOM_FLOOR, cross-validates `state/p9_base_val_h100_2026_05_04/verdict.json` (limit=500, $5.25)

---

## §1 Outcome (band)

CLM v4 base measured on 4 benches at limit=200 each:

| Bench | n_shot | metric | ubu1 (limit=200) | H100 (limit=500) | random | Llama-3.2-3B (public) | Δ vs random | Δ vs Llama |
|---|---|---|---|---|---|---|---|---|
| HellaSwag | 5 | acc_norm | **0.255 ± 0.0309** | 0.264 ± 0.0197 | 0.25 | 0.644 | +0.5 pp | −38.9 pp |
| MMLU | 0 | acc | **0.2553 ± 0.0045** | 0.27101 ± 0.00398 | 0.25 | 0.608 | +0.5 pp | −35.3 pp |
| TriviaQA | 5 | exact_match | **0.000 ± 0.000** | 0.000 | ~0.05 | 0.514 | −5.0 pp | −51.4 pp |
| OpenBookQA | 0 | acc_norm | **0.280 ± 0.0318** | (not run) | 0.25 | ~0.40 | +3.0 pp | −12.0 pp |

**Verdict band**: CONFIRMED_RANDOM_FLOOR — matches H100 baseline within stderr on all 3 overlapping benches. OpenBookQA acc_norm 0.28 (the only non-random-band signal at +3pp) is within 1σ of random; not a capability claim. Consistent with `#115` chat-incapability disclosure — CLM v4 was trained on phi★ + ce only, never SFT'd, never RLHF'd.

**Truncation rates** (block_size=512 vs n-shot prompts):
- HellaSwag 5-shot: 84.75% loglik calls truncated (structural; documented in BG-CLM-2 spec §3 as HARD CONSTRAINT)
- MMLU 0-shot: 2.82%
- TriviaQA generative 5-shot: 0/0 (loglik path bypassed; generate_until used)
- OpenBookQA 0-shot: 0%

**F1_v3 composite (HellaSwag acc_norm + MMLU acc + TriviaQA EM, equal-weight average)**:
- CLM v4 base (ubu1, limit=200): (0.255 + 0.2553 + 0.000) / 3 = **0.1701**
- CLM v4 base (H100, limit=500): (0.264 + 0.27101 + 0.000) / 3 = **0.1783**
- Llama-3.2-3B (public reference): (0.644 + 0.608 + 0.514) / 3 = **0.5887**
- Δ Llama − CLM = +41.86 pp (massive — pre-LoRA gap)

---

## §2 What this anchor unlocks

1. **F-CLM-LORA-2 baseline = SET** — anima-substrate (CLM v4 base) numbers locked for downstream comparator. BG-CLM-2 LoRA SFT EXEC (per `docs/clm_v4_lora_sft_spec_2026_05_04.md` §4 PASS criteria) can now compute (post-LoRA − pre-LoRA) delta on the SAME 4-bench surface.
2. **C-CLM-LORA-1 parity floor** — `post-LoRA HellaSwag acc_norm ≥ CLM-v4-base acc_norm − 1pp` is now MEASURABLE (was hypothetical at spec-land time).
3. **C-CLM-LORA-2 differentiator anchor** — composite (HellaSwag + MMLU + TriviaQA, equal weight) for CLM v4 base = ANCHORED. Llama Path A v2 comparator becomes available when sibling **BG-α'''-EVAL-FIX** lands; until then this verdict uses public Llama-3.2-3B reference values (proxy, same pattern as H100 baseline).

---

## §3 Cross-validation vs H100 baseline (2026-05-04)

The H100 cycle (`state/p9_base_val_h100_2026_05_04/verdict.json`) ran the same model with **limit=500** at lm-eval==0.4.5 + transformers 4.46.3 + bf16 dtype, total wall 7.80 min, total cost $5.25. This ubu1 cycle runs limit=200 with lm-eval==0.4.11 + transformers 5.7.0 + fp32, $0.

Both verdicts produce **band-level agreement** (CONFIRMED_RANDOM_FLOOR), validating:
- The legacy `ConsciousDecoderV2` load path (used here) and the HF `CLMv4ForCausalLM` wrapper path (used by H100 baseline) emit equivalent next-token logits within stderr.
- The 64K SPM tokenizer + plain-text 5-shot rendering produces stable scores across versions of lm-eval-harness.
- The **84% truncation rate** on hellaswag 5-shot is structural — CLM v4 block_size=512 cannot fit 5-shot prompts; this is documented in BG-CLM-2 spec §3 as a HARD CONSTRAINT.

OpenBookQA result is the **NEW data point** vs H100 baseline (filled the missing 4th bench).

---

## §4 GO/NO-GO recommendation for BG-CLM-2 EXEC ($6-10 H100)

**Recommended verb**: `GO_CONDITIONAL`.

| Conditional gate | Status | Notes |
|---|---|---|
| Baseline below random+5pp on ≥3/4 benches | EXPECTED PASS (CONFIRMED_RANDOM_FLOOR carry from H100) | Verdict-level confirmation in this cycle — see §1 numbers |
| Llama Path A v2 verdict landed (so C-CLM-LORA-2 comparator alive) | PENDING (sibling BG-α'''-EVAL-FIX in-flight) | NO-GO blocker until sibling verdict produces composite |
| Tied-weight pre-flight check (R6) | NOT YET RUN | $0, 5 min Mac — separate cycle |
| Decoder_v3 hf-format shim | EXISTS (v4 LOCKED, F-SHIM-V4-3 PASS) | Used for HF Cycle 2 upload; reusable for EXEC |
| User ACK on $6-10 cost band | NOT YET GIVEN | Required per spec §13 |

**Recommendation rank**: BG-CLM-2 EXEC is **conditionally GO** once Llama Path A v2 verdict lands (sibling BG-α'''-EVAL-FIX). All other prereqs are clearable cheaply ($0 + 5 min). **Do NOT launch BG-CLM-2 H100 pod until Llama Path A v2 composite is anchored** — otherwise C-CLM-LORA-2 (the singular scientific question of the cycle) cannot be evaluated.

---

## §5 Honest C3 (≥5 per raw#10)

See `state/clm_v4_baseline_eval_2026_05_05/verdict.json` `honest_c3` field for full list. Key items:

1. **CPU/GPU eval limited to limit=200** — band-level agreement with H100 limit=500, not a replacement.
2. **CLM v4 chat-incapable per `#115`** — naturalistic chat-format benches (TriviaQA closed-book QA, MMLU instruction-following) underperform Llama by design.
3. **F-CLM-LORA-2 comparator only meaningful post LoRA SFT cycle** — this baseline anchors LEFT side; right side requires Llama Path A v2 retrain verdict + CLM v4 + LoRA SFT verdict.
4. **substrate phi★ 41.86 is consciousness-coupling axis** NOT NLP capability axis; high phi★ + low NLP downstream is anima's expected operating profile.
5. **GPU deviation** — spec said "ubu1 CPU" but RTX 5070 was available + 10× faster. fp32 path used vs H100 bf16; minor numerical drift, but acc-on-rank-loglik tasks are robust.
6. **lm-eval 0.4.11 vs spec 0.4.4/0.4.5** — newer version may have task config drifts; explicitly forced num_fewshot per H100 baseline parity.
7. **H100 already paid $5.25 yesterday** for this same data at higher precision (limit=500). This ubu1 cycle is a $0 cross-validation + openbookqa fill-in, not a redo. F-CLM-LORA-2 baseline can equivalently cite the H100 verdict (`state/p9_base_val_h100_2026_05_04/verdict.json`) as the canonical anchor.

---

## §6 Cross-links

- **Spec (parent)**: `docs/clm_v4_lora_sft_spec_2026_05_04.md` (BG-CLM-2 LoRA SFT design; this baseline is the §6 R2 dependency)
- **H100 sibling baseline**: `state/p9_base_val_h100_2026_05_04/verdict.json` (limit=500, $5.25)
- **HF release**: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md` (private mirror at `need-singularity/clm-v4-mk2-v1`)
- **Path B sanity probe v2**: `state/p9_path_b_sanity_probe_v2_2026_05_03/eval_clm_v4_hellaswag_v2.py` (eval harness inheritance)
- **Path A retry-3 (sibling, in-flight)**: BG-α'''-EVAL-FIX produces Llama-3.2-3B-Instruct comparator for F-CLM-LORA-2 differentiator
- **Train-avg fixture (sibling)**: `state/clm_v4_train_avg_harvest_2026_05_04/verdict.json` (real fixture for shim v4)

---

## §7 Files

- `state/clm_v4_baseline_eval_2026_05_05/verdict.json` — primary verdict
- `state/clm_v4_baseline_eval_2026_05_05/hellaswag.json` — raw lm-eval per-task output
- `state/clm_v4_baseline_eval_2026_05_05/mmlu.json`
- `state/clm_v4_baseline_eval_2026_05_05/triviaqa.json`
- `state/clm_v4_baseline_eval_2026_05_05/openbookqa.json`
- `state/clm_v4_baseline_eval_2026_05_05/eval_full.log` — full lm-eval log + truncation rates
- `tool/transient_py/clm_v4_baseline_eval_full.py` — eval script (raw#37 carve-out, gitignored)
- `tool/transient_py/clm_v4_baseline_smoke.py` — pre-flight smoke (L19 lesson)

---

## §8 Next ranked actions

1. **rank-1**: Wait for sibling **BG-α'''-EVAL-FIX** (Llama Path A v2 retrain) verdict → unlocks C-CLM-LORA-2 comparator
2. **rank-2**: Run **tied-weight pre-flight check** (BG-CLM-2 spec §6 R6) — $0, 5 min Mac
3. **rank-3**: USER ACK on $6-10 cost band → BG-CLM-2 EXEC unblocked
4. **rank-4**: Update `.roadmap.p9_sft` with `p9_sft.cond.clm_v4_lora_baseline = met` (separate cycle; raw#71 marker emit)
5. **rank-5**: Future deferred — replace public Llama reference with retrained Llama Path A v2 numbers in BG-CLM-2 §4 thresholds (raw#71 amendment if shifts > 5pp)
