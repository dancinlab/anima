# P9 Path A LoRA retrain v2 — catastrophic forgetting fix DESIGN spec

- **ts_utc**: 2026-05-04T_BG-Φ_design
- **predecessor**: Path A v1 step-8k LoRA (HF commit `5a9b4584`, training cycle `state/p9_path_a_llama_lora_2026_05_03/`)
- **driver**: BG-Ρ Mode 1 LoRA eval (commit `fa7db7bc`) → INFRASTRUCTURE_PASS / SCIENCE_FAIL: ALL 3 benchmarks (HellaSwag/MMLU/TriviaQA) show negative Δ vs Llama-3.2-3B base; catastrophic forgetting signature confirmed.
- **pre-registration policy (raw#71)**: All §4 PASS thresholds, §6 hyperparameters, §8 falsifiers F-PA-RETRAIN-v2-1~4 are LOCKED at this spec landing. Post-eval threshold tweaks are a verdict-invalidation — must be re-pre-registered in a follow-up amendment cycle.
- **scope**: spec / DESIGN ONLY. $0. No pod boot. No code edit. Retrain EXEC requires explicit USER ACK in a separate cycle.
- **non-overlap**: BG-Χ (`state/p9_path_a_step10k_recovery_2026_05_04/`) and BG-Ψ (`state/p9_lora_mode1_instruct_eval_2026_05_04/`) untouched. External r=16 retrain pods (`nzw0btc8br78yy`, `0jetjpvlm51zoy`, omnibus `11331fe4`) are a **competing strategy S4** — this spec is **S1+S3**, not S4.

---

## §1 — Problem statement

### Evidence (from BG-Ρ verdict `state/p9_lora_mode1_eval_2026_05_04/verdict.json`)

| Benchmark | Llama base (BG-Ο anchor) | LoRA step-8k | Δ (LoRA−base) pp | c3 2σ threshold | c3 |
| --- | --- | --- | --- | --- | --- |
| HellaSwag (acc_norm, 0-shot) | 0.654 | 0.642 | **−1.2** | 4.29 | within-noise |
| MMLU (acc, 5-shot) | 0.5796 | 0.5301 | **−4.95** | 0.87 | sig DEGRADED |
| TriviaQA (EM, 0-shot) | 0.396 | 0.302 | **−9.4** | 4.38 | sig DEGRADED |

ALL three deltas are negative; two of three are statistically significant degradation at 2σ. This validates the F1_v3 falsifier framework (separation IS detectable) but the trained LoRA is a **regression** on academic benchmarks.

### Root-cause hypothesis (per BG-Ξ omnibus `11331fe4` hint)

SFT corpus distribution mismatch:

- **v1 corpus** (`state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`): 50k axis-conditioned anima recipes — chat dialogue + paper refs + cell-language + N-22 axes + TRIBE stimulus + auto-augment. ZERO academic factual / MC content.
- **v1 hyperparams**: LoRA r=64 α=64 dropout=0.05, lr=1e-4 (later doc says 2e-4 — verified 1e-4 in spec, but high regardless), max_steps=10000, save_steps=2000 (anchor at step-8k after final-save flush failure per `.roadmap.p9_sft cond.path_a_lora_train_complete` honest C3).
- **mechanism**: 8000 high-LR adapter steps on a corpus with no factual/MC content overwrote pretrained representations critical for MMLU 5-shot recall and TriviaQA 0-shot EM. HellaSwag commonsense degraded only marginally (within-noise) — most robust of the three.

### Auxiliary: instruct/non-instruct mismatch (BG-Ψ probe)

LoRA was trained against `Llama-3.2-3B-Instruct`'s chat-templated representation (per `state/p9_path_a_naming_2026_05_03/README_canonical.md` substrate); BG-Ρ composed onto non-Instruct `Llama-3.2-3B`. BG-Ψ Mode 1' (parallel to this BG, Instruct-base eval) will quantify how much of the Δ is template-mismatch vs true forgetting. **This spec assumes ~5pp of the −9.4pp TriviaQA Δ may be recoverable just by composing onto Instruct**; the rest is genuine forgetting.

---

## §2 — Strategy taxonomy

| ID | Name | Description | H100 hr | $ band | Implementation complexity | Expected forgetting reduction (qualitative) |
| --- | --- | --- | --- | --- | --- | --- |
| **S1** | Rehearsal SFT mix | 60% anima + 30% academic distillation + 10% chat-template alignment | ~6-8h | $20-25 | LOW (data prep only) | HIGH — best-established |
| **S2** | Replay buffer | K% pretraining data + new SFT, interleaved batches | ~10-15h | $35-50 | MEDIUM (need pretrain shard access) | HIGHEST — but cost++ |
| **S3** | Lower LR / early stop | lr 1e-4→5e-5 (4x↓), steps 10k→6k, intermediate eval | ~4-6h | $15-20 | LOW (config only) | MEDIUM — may underfit anima |
| **S4** | LoRA rank reduction | r=64 → r=16 (already in flight externally per `11331fe4`) | (external) | (external) | (external) | MEDIUM — competing track |
| **S5** | Knowledge distillation | Train against Llama base soft logits (paradigm D logit-axis) | ~8-12h | $30-50 | HIGH (KL loss + teacher inference) | HIGH — but novel infra |
| **S6** | Multi-task heads | Separate adapters for academic vs anima; route at inference | ~12-20h | $50-80 | HIGH (router + dual training) | HIGHEST — but spec/eval complexity++ |

---

## §3 — Recommended strategy (ranked by 완성도 lens × cost × magnitude)

### Rank 1 (RECOMMENDED): S1 + S3 combined — rehearsal mix + lower LR

- **완성도**: HIGH — both individually established in literature (Chen et al. 2020 on rehearsal; LR-decay anti-forgetting common across PEFT). Combination addresses both the corpus-side cause (mix) and the optimizer-side cause (over-fitting via high LR).
- **cost**: $20-30 H100 (6000 steps × ~3-5 min/100-step block at batch=32 effective).
- **expected magnitude**: parity OR small improvement on academic benchmarks while preserving anima axis behavior. Likely outcome based on literature: HellaSwag flat (already within-noise), MMLU recovery to within −1pp of base, TriviaQA recovery to within −2pp of base.
- **risk**: rehearsal mix may dilute anima-axis signal — guarded by F-PA-RETRAIN-v2-4.

### Rank 2 (alternative if budget allows): S5 — paradigm D distillation

- **완성도**: MEDIUM — paradigm D infra already specced (`docs/p9_paradigm_d_distill_spec_2026_05_03.md`); distillation against Llama base soft logits theoretically prevents drift.
- **cost**: $30-50 H100.
- **expected magnitude**: HIGH — but requires teacher logit inference pass (Top-K K=64 KL at T=4 per paradigm D spec). Adds infra complexity.

### Rank 3: S2 — replay buffer

- **완성도**: HIGHEST — most rigorous anti-forgetting. But cost++ ($35-50) and requires pretrain data shard access (not currently in repo). Defer.

### Not recommended

- **S4** — competing track, already in flight externally; not duplicating.
- **S6** — too much eval-side complexity for v2 retrain (F1_v3 framework assumes single LoRA). Defer to a v3 cycle.

---

## §4 — Pre-registered F1_v3 V2 PASS thresholds for retrained LoRA (LOCKED 2026-05-04)

Anchor: BG-Ο `state/p9_base_validation_llama_anchor_2026_05_04/verdict.json` (Llama-3.2-3B non-Instruct, limit=500, seed=42, bf16, lm-eval 0.4.11).

| Benchmark | Llama base | Required (parity floor) | Bonus (improvement) |
| --- | --- | --- | --- |
| HellaSwag acc_norm | 0.654 | ≥ 0.644 (base − 1pp) | ≥ 0.674 (base + 2pp) |
| MMLU 5-shot acc | 0.5796 | ≥ 0.5696 (base − 1pp) | ≥ 0.5996 (base + 2pp) |
| TriviaQA EM | 0.396 | ≥ 0.376 (base − 2pp) | ≥ 0.416 (base + 2pp) |

**PASS criterion (overall)**:

- **C-RV-1**: ALL 3 benchmarks at parity-floor (within −1pp / −1pp / −2pp respectively)
- **C-RV-2**: AT LEAST 1 benchmark IMPROVES on base by ≥ 2pp (proves SFT added something positive, not just preserved)
- **OVERALL**: C-RV-1 AND C-RV-2 → V2 PASS. C-RV-1 only → V2 PARTIAL (forgetting fixed, anima axis unverified). Either fails → V2 FAIL.

These thresholds are LOCKED. If the retrain produces e.g. HellaSwag 0.640 / MMLU 0.575 / TriviaQA 0.380 (parity-ish but no improvement), verdict = PARTIAL not PASS. raw#71 forbids post-eval threshold relaxation.

---

## §5 — SFT corpus mix proposal (recommended S1)

Total target: 50,000 examples (matches v1 cardinality for budget parity).

| Slice | Pct | Examples | Source |
| --- | --- | --- | --- |
| **A — anima axis** | 60% | 30,000 | sub-sample of v1 `sft_data_full_50k_augmented.jsonl` (deterministic seed=20260504) |
| **B — academic distillation** | 30% | 15,000 | 5,000 MMLU train split (auxiliary_train, 5-shot rendered) + 5,000 TriviaQA train EM pairs + 5,000 Wikipedia subset (CC-BY-SA, paragraph→summary) |
| **C — chat-template alignment** | 10% | 5,000 | 2,500 OpenOrca subset (Apache 2.0, instruct-following) + 2,500 ShareGPT-style chat (deduplicated, license-mixed) |

### Rationale

- 60% anima keeps the axis-conditioning signal dominant — F-PA-RETRAIN-v2-4 verifies preservation.
- 30% academic = direct rehearsal against the v2 verdict surface (MMLU/TriviaQA train splits) + general factual (Wikipedia). The MMLU/TriviaQA train splits are train-side, NOT test-set leakage — verifier check `dataset.disjoint(train_idx, test_idx)` to be added in retrain config.
- 10% chat-template = preserves Instruct-base chat-following behavior (lost in v1 due to aggressive single-task SFT). OpenOrca is a strong instruction-following baseline.

### Honest C3 on mix

- 60/30/10 ratio is heuristic. Ablation across {70/20/10, 60/30/10, 50/40/10} would be ideal but ~3x cost. Recommended single-config v2 first; ablation reserved for v3 if v2 PASS.
- MMLU train split has 99,842 examples; 5,000 sub-sample at seed=20260504 is uniform. Distribution may not match 57-subject 5-shot test composition — this is a known limitation; alternative would be stratified by subject.
- TriviaQA train has 78,785 question-answer pairs; 5,000 sub-sample. Domain skews toward Wikipedia-derived, which overlaps with Wikipedia subset slice — mild redundancy but not contamination.

---

## §6 — Hyperparameter changes from v1 (LOCKED 2026-05-04)

| Param | v1 | v2 | Rationale |
| --- | --- | --- | --- |
| LoRA r | 64 | 64 | keep — not the cause; r=16 is competing S4 track |
| LoRA alpha | 64 | 64 | keep — alpha/r=1.0 standard |
| LoRA dropout | 0.05 | 0.05 | keep |
| Target modules | q_proj,k_proj,v_proj,o_proj | q_proj,k_proj,v_proj,o_proj | keep |
| Base model | Llama-3.2-3B-Instruct | Llama-3.2-3B-Instruct | keep (consistent w/ v1 chat-template assumption) |
| Optimizer | AdamW (b1=0.9, b2=0.999, wd=0.01) | AdamW (b1=0.9, b2=0.95, wd=0.01) | b2=0.95 standard for SFT (less momentum) |
| **LR** | **1e-4** | **5e-5** | **2x reduction** — primary anti-forgetting lever (S3) |
| LR schedule | cosine, warmup 500 | cosine, warmup 300 | shorter warmup for shorter run |
| **max_steps** | **10000** | **6000** | **40% reduction** — early stop |
| **save_steps** | **2000** | **500** | **4x finer** — granular early-stop signal |
| **Eval intermediate** | none | every 2000 steps | run lm-eval HellaSwag limit=200 (fast ~5min) — early-stop signal if Δ < −5pp |
| micro_batch | 4 | 4 | keep |
| grad_accum | 8 | 8 | keep |
| effective_batch | 32 | 32 | keep |
| max_grad_norm | 1.0 | 1.0 | keep |
| seed | 20260502 | 20260504 | new run, new seed |
| max_seq_len | 2048 | 2048 | keep |
| dtype | bf16 | bf16 | keep |

---

## §7 — Cost band

- **Pod**: 1× H100 SXM RunPod on-demand $2.99/hr (ref BG-Ρ rate).
- **Wall estimate**: 6000 steps × ~3.5 min / 100-step block = ~210 min training + ~30 min boot/scp/eval-intermediate × 3 = ~5 min × 3 = 15 min eval breaks → ~225 min ≈ 3.75 h.
- **Eval-intermediate cost embedded**: 3 × HellaSwag-200 ~ 3 × 5 min = 15 min counted above.
- **Final eval cost**: separate cycle, ~$1.10 per BG-Ρ — not in this band.
- **Cost band**: **$11-23 H100** (3.75 h × $2.99/h = $11.21 floor; 7h hard cap × $2.99 = $20.93 ceiling; budget envelope $20-30 to allow 30% slack).
- **Budget hard cap**: $30 (auto-trap if pod cost-guard exceeds).

### Side-by-side vs v1

| Item | v1 | v2 |
| --- | --- | --- |
| Steps | 10000 | 6000 |
| Wall | ~10-20h | ~3.75-7h |
| Cost actual | $22.18 | $11-23 (target) |

---

## §8 — Falsifier set (raw#71)

### F-PA-RETRAIN-v2-1 — Training loss converges (no diverge)

- **metric**: train_loss at step ≥ 1000 monotone-or-flat across 500-step windows; no NaN/Inf
- **observable**: pod-side `trainer_state.json` log
- **PASS**: max_window_increase < 0.1 absolute loss within last 4 windows
- **FAIL action**: ABORT pod; bug-fix LR or batch size

### F-PA-RETRAIN-v2-2 — Intermediate eval at step 2000 ≤ 5pp drop on any benchmark vs Llama base

- **metric**: HellaSwag-200 limit=200 acc_norm at step 2000 ≥ 0.604 (= Llama base 0.654 − 5pp)
- **observable**: intermediate eval JSON emitted at step 2000
- **PASS**: acc_norm ≥ 0.604
- **FAIL action**: EARLY-STOP retrain; treat as v2-FAIL_EARLY; do not proceed to step 6000; save adapter as `step-2000-aborted` for post-mortem

### F-PA-RETRAIN-v2-3 — Final eval V2 PASS criterion (§4)

- **metric**: §4 C-RV-1 AND C-RV-2 on full Mode 1 eval (Llama-3.2-3B + LoRA, limit=500, lm-eval 0.4.11)
- **observable**: post-train Mode 1 eval verdict.json (separate cycle ~$1.10)
- **PASS**: C-RV-1 (all 3 within parity floor) AND C-RV-2 (≥1 improves by 2pp)
- **FAIL action**: v2-FAIL → escalate to S5 (distillation) OR S2 (replay buffer)

### F-PA-RETRAIN-v2-4 — Anima-axis preservation

- **metric**: BLEU-1 on holdout-500 axis-conditioned prompts (per `state/p9_p1_holdout500_reeval_2026_05_03/`) ≥ v1 step-8k LoRA BLEU-1
- **observable**: post-train holdout BLEU eval (~$1, separate cycle)
- **PASS**: v2 BLEU-1 ≥ v1 BLEU-1 (i.e. mix did not dilute axis signal below baseline)
- **FAIL action**: v2-PARTIAL (forgetting fixed but axis lost); reduce academic % from 30→20 in v3

---

## §9 — Honest C3 (raw#10, ≥5)

1. **Rehearsal mix may dilute anima-axis signal** — 60% anima vs v1 100% means each anima gradient step covers 0.6x as many tokens. F-PA-RETRAIN-v2-4 guards this but does not fully bound the dilution; if v1 BLEU-1 was barely above noise floor, v2 may dip below. A v2-PARTIAL is a real possibility.

2. **60/30/10 ratio is heuristic, no sensitivity analysis** — literature suggests 50-70% target-task / 30-50% rehearsal range; we picked the midpoint. Optimal for THIS corpus + benchmark mix unknown; would need 3x cost to ablate. Cost-vs-coverage tradeoff accepted.

3. **External r=16 retrain (pods `nzw0btc8br78yy`, `0jetjpvlm51zoy`, omnibus `11331fe4`) is competing strategy S4** — this spec is S1+S3. If r=16 produces V2 PASS first, this spec MAY be SUPERSEDED before EXEC. User policy decision: run both for comparison, OR sequence S1+S3 only after S4 result, OR cancel one.

4. **LR reduction 1e-4 → 5e-5 is rule-of-thumb** — standard "reduce LR for forgetting" heuristic; optimal LR for this corpus + base + adapter is unknown without an LR sweep. 5e-5 is a single point on the 1e-5...1e-4 axis; could under- or over-shoot. v2 single-config; ablation deferred.

5. **Mode 1 F1_v3 V2 SUCCESS thresholds (§4) are this BG's pre-registration; not binding for future amendments** — if downstream context shifts (e.g., new benchmark added, base anchor updated), §4 must be re-pre-registered. The current LOCKED state covers ONLY this v2 retrain cycle.

6. **Instruct/non-Instruct base mismatch is partially confounded with forgetting** — BG-Ψ (parallel to this BG) is measuring how much of v1's −9.4pp TriviaQA Δ is template-mismatch vs true forgetting. v2 retrains on Instruct base same as v1, so the mismatch persists at eval-time UNLESS BG-Ψ confirms Instruct-base eval recovers some Δ. If BG-Ψ result lands BEFORE v2 EXEC, §4 thresholds may need re-anchoring against Instruct base (separate amendment).

7. **MMLU/TriviaQA train splits used for rehearsal — train-test disjoint must be enforced** — MMLU has well-defined dev/test/auxiliary_train splits; we use auxiliary_train only. TriviaQA has train/validation/test; we use train only. The verifier check is mandatory pre-launch; failure to enforce = test-set leakage = invalid V2 verdict.

8. **Wikipedia subset slice license is CC-BY-SA, but anima v1 already mixes CC-BY-SA — license stack OK** — but a Wikipedia-derived dataset choice (e.g., Wikitext-103 subset) must be made + documented at EXEC; this spec leaves the exact subset open.

---

## §10 — Roadmap update proposal (JSONL line for `.roadmap.p9_sft`)

Proposed (not edited by this BG; user/separate cycle to land):

```jsonl
{"type":"entry","id":"p9_sft.cond.path_a_retrain_v2","kind":"cond","title":"Path A LoRA retrain v2 — catastrophic forgetting fix (S1+S3 rehearsal mix + lower LR + early-stop)","desc":"Retrain Path A LoRA with 60/30/10 anima/academic/chat mix, lr=5e-5, max_steps=6000, save_steps=500, intermediate HellaSwag-200 eval at step 2000/4000/6000. Pre-registered F1_v3 V2 PASS = parity-floor on all 3 benchmarks AND ≥1 improvement by 2pp. Cost $20-30 H100.","status":"spec_landed","substrates":["p9","sft","path_a","lora","retrain","v2"],"verifier":{"type":"manual_review","manual_override_path":"state/markers/p9_path_a_retrain_v2_spec_landed.marker","status_emit":"__P9_PATH_A_RETRAIN_V2__ <SPEC_LANDED|EXEC_RUNNING|V2_PASS|V2_PARTIAL|V2_FAIL>"},"evidence":["docs/p9_path_a_retrain_v2_spec_2026_05_04.md","state/p9_path_a_retrain_v2_spec_2026_05_04/decision_matrix.json","state/p9_path_a_retrain_v2_spec_2026_05_04/falsifier_set.md","state/p9_path_a_retrain_v2_spec_2026_05_04/sft_corpus_mix.json","driver: state/p9_lora_mode1_eval_2026_05_04/verdict.json (INFRASTRUCTURE_PASS / SCIENCE_FAIL)","BG-Ξ omnibus 11331fe4 catastrophic-forgetting hint","BG-Ο anchor state/p9_base_validation_llama_anchor_2026_05_04/verdict.json"],"ts":"2026-05-04","cross_link":{"sister_strategy_S4":"external r=16 retrain pods nzw0btc8br78yy + 0jetjpvlm51zoy (omnibus 11331fe4) — competing not blocking","predecessor_v1":"p9_sft.cond.path_a_lora_train_complete (status partial_verified_8k)","verdict_surface":"p9_sft.cond.3 F1_v3 V2","cost_band":"$20-30 H100 (6000 steps × ~3.75h)","exec_gate":"USER ACK required"}}
```

---

## §11 — Exec gate (NEXT-CYCLE)

**This BG produces SPEC ONLY. Retrain EXEC requires:**

1. USER ACK on $20-30 cost band + 3.75-7h wall
2. USER policy decision on competing S4 (run both? sequence? cancel?) per honest C3 #3
3. Optional pre-EXEC: wait for BG-Ψ Instruct-base eval result (per honest C3 #6) to re-anchor §4 if needed
4. Separate BG cycle to:
   - emit retrain orchestrator hexa (raw#9 — no new .py)
   - launch H100 pod with rehearsal-mix corpus + new HP grid
   - run intermediate evals + final F-PA-RETRAIN-v2-3 + F-PA-RETRAIN-v2-4
   - emit verdict.json + landing doc + marker
