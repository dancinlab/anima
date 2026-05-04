# P9 Path-A Corpus Audit — r=16 Catastrophic Forgetting Risk Prediction
Date: 2026-05-04 | Auditor: subagent (RETRY3) | Sample: 1000 random of 50,000 (seed=42)

## TL;DR
- **Measured chat/factual ratio**: ~49.7% chat-like / ~50.3% factual-like
- **Track A target**: 70% chat / 30% factual
- **Gap from target**: -20.3pp chat (under-represented), +20.3pp factual (over-represented)
- **r=16 prediction**: HIGH risk of factual-domain over-fitting and chat-style erosion (chat persona dilution; factual benchmark improvement at expense of conversational coherence)
- **Track A necessity**: REQUIRED (current corpus does not satisfy Track A composition; running r=16 LoRA on this corpus will NOT yield Track A behavior — instead a balanced/factual-leaning shift)

## Distribution (refined classifier, source-driven)

| Class | Count | % of 1000 | Bucket |
|---|---:|---:|---|
| factual_qa (alm70b_paper_ref + universe corpora) | 218 | 21.8% | factual |
| chat (sharegpt) | 172 | 17.2% | chat |
| synthetic_augment (llama_augment_fallback_*) | 158 | 15.8% | chat |
| code (tribe_v2_vendored py/json) | 158 | 15.8% | factual |
| doc_factual (n22/proposal/SUMMARY md) | 127 | 12.7% | factual |
| philosophical_qa (synthetic_phil + alm_r14_metaref) | 121 | 12.1% | chat |
| persona_template (p8_ledger_m4) | 46 | 4.6% | chat |

Aggregated: chat=497 (49.7%), factual=503 (50.3%).

Source mix in full 50k (top): sharegpt 20.0%, alm70b_paper_ref 18.5%, synth_phil_en 6.0%, llama_augment_fallback_2 6.0%, p8_ledger 5.9%, synth_phil_ko 4.0%, tribe_v2 algonauts/lebel/lahner ~12% combined (code-heavy).

Lang: en 61.5%, ko 34.6%, mixed 3.9%.

## r=16 Catastrophic Forgetting Prediction

LoRA r=16 on Llama-3.1-8B with this 50/50-balanced corpus, 50k examples, expected behavior:

1. **Chat persona dilution (HIGH)**. Sharegpt is only 20% of corpus and competes with 21.8% Korean factual-QA (true/false + multi-choice + MMLU-style). The model will learn to emit short factual answers ("참", "거짓", "2번: ...") preferentially over conversational completions. Chat-style fluency on open-ended prompts will degrade vs base. This is NOT classical catastrophic forgetting (base capability loss) but **chat-mode collapse toward terse factual replies**.

2. **Factual benchmark gain, narrative loss**. KMMLU-style scores likely improve (alm70b_paper_ref is essentially KMMLU train-equivalent), but free-form English chat coherence will regress. r=16 has enough capacity to memorize alm70b answer patterns; risk of pattern-matching short-answer formatting onto chat prompts.

3. **Code injection bleed (MEDIUM)**. 15.8% of corpus is raw vendored .py/.json from tribe_v2. With r=16 + 50k examples, expect spurious python keywords/code-block fences to appear in unrelated chat completions ("```python" leakage).

4. **Persona template overfitting (LOW-MEDIUM)**. 12.1% phil_qa + 4.6% p8_ledger + 15.8% synth_augment_fallback share a stylized "anima" voice. r=16 will lock onto this voice; unprompted, the model will tend toward 1차/2차 응답 / "정보 시스템은..." templates. This *is* desired Track A behavior, but at 32.5% combined dose vs Track A's intended 70%, the persona will be present-but-weak.

5. **Catastrophic forgetting on base capabilities — LOW** at r=16 with 1-2 epochs. r=16 is small enough that the frozen base model dominates; the LoRA delta cannot wipe base knowledge. The forgetting risk is **stylistic/distributional**, not capability-erasing.

### Quantitative estimate (heuristic, no empirical test yet)
- Llama-self F1 baseline: 0.1555 (ref: F1 anchor recalibration memory)
- Predicted post-LoRA F1 on factual benchmarks: +15-25% relative (+0.02-0.04 absolute) — biased upward by alm70b_paper_ref overlap
- Predicted chat-quality regression (eyeballed via prompt suite): 10-20% degradation in open-ended completion length/coherence

## Track A Necessity Verdict

**REQUIRED**. Current corpus is composition-misaligned for Track A. Two viable paths:

- **Option A (re-balance)**: Down-sample factual_qa+code+doc to 30% (≈15k examples), up-sample chat+phil_qa+persona+synth to 70% (≈35k). Requires either (a) discarding ~10k factual examples or (b) augmenting chat side with +10-15k synthetic chat pairs.
- **Option B (proceed-and-measure)**: Train r=16 on current 50/50 corpus, measure empirically, accept that result is "balanced LoRA" not "chat-leaning LoRA". Use as Track A-prime baseline.

Recommendation by 완성도 lens: **Option A** if Track A persona/chat-mode is the stated goal. Option B only if empirical measurement is itself the goal (cheaper, faster, but does not deliver Track A spec).

## 3 Caveats

1. **Classifier is heuristic, not semantic**. Source-name driven; e.g., `llama_augment_fallback_*` (15.8% of corpus) was bucketed as chat-like based on synthesis intent, but actual content may straddle chat/factual depending on the source it augmented. Worst case: if half is factual-augment, real chat ratio drops to ~42%.

2. **alm70b_paper_ref overlap with KMMLU eval is unverified**. If the 18.5% factual-QA slice contains KMMLU train-set leakage, post-training F1 gains are inflated (memorization, not generalization). Pre-train dedup vs eval set is mandatory before claiming Track A factual baseline.

3. **r=16 + 50k + epochs unspecified**. Predictions assume 1-2 epochs at typical LoRA hyperparams (lr=2e-4, alpha=32). Higher epoch counts (3+) shift risk from "chat dilution" to "true overfitting on alm70b answer formatting" — expect mode-collapse toward "참/거짓/N번" replies on ALL prompts. Confirm epoch budget before finalizing risk class.

## Artifacts
- `/Users/ghost/core/anima/state/p9_path_a_corpus_audit_2026_05_04/distribution.json` — full + sample distributions, both raw and refined classifications
- `/Users/ghost/core/anima/state/p9_path_a_corpus_audit_2026_05_04/classification_samples.jsonl` — 1000 classified samples (raw classifier; refined counts in distribution.json)
- `/Users/ghost/core/anima/state/p9_path_a_corpus_audit_2026_05_04/prediction.md` — this document
- `/Users/ghost/core/anima/state/markers/p9_path_a_corpus_audit_landed.marker` — completion marker
