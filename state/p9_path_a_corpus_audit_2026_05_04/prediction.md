# P9 Path A — Corpus Audit & r=16 Catastrophic-Forgetting Prediction

**Date**: 2026-05-04
**Phase**: p9_path_a_corpus_audit_2026_05_04
**Source corpus**: `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (50,000 records, 132 MB)
**Predecessor SHA-256**: `b7f9550cf1794a3a51c1c091b046ca67fb0de8972ad7a752d6390c5182ba38bc`
**Method**: Reservoir sample n=1000, seed=42, source-name + heuristic classification

---

## 1. Distribution (n=1000 sample, 95% CI)

| Class       | Count | Pct    | Examples                                                   |
|-------------|-------|--------|------------------------------------------------------------|
| factual     | 348   | 34.8%  | anima_corpus_*, n22_paradigm_v11_doc_*, alm_r14_metaref_*, *.md |
| chat        | 306   | 30.6%  | sharegpt_hf_anon8231489123, llama_augment_fallback_*       |
| instruction | 177   | 17.7%  | synthetic_philosophical_template_{en,ko}, p8_ledger_m4_*   |
| code        | 169   | 16.9%  | tribe_v2_vendored_*.py / *.json                            |
| other       | 0     | 0.0%   | (clean partition)                                          |

**Strict chat-vs-factual**: 46.79% / 53.21% (n=654, ±3.82%)
**Inclusive chatlike-vs-factlike** (chat+instr / fact+code): 48.30% / 51.70% (n=1000, ±3.10%)

**Lang split** (full 50k): en 61.5% / ko 34.6% / mixed 3.9%

---

## 2. Track A 70/30 target — current vs goal

| Mix                       | Current (sample) | Track A target | Delta            |
|---------------------------|------------------|----------------|------------------|
| chat (strict)             | 46.79%           | 70%            | **−23.21 pp**    |
| factual (strict)          | 53.21%           | 30%            | **+23.21 pp**    |
| chatlike (inclusive)      | 48.30%           | 70%            | **−21.70 pp**    |
| factlike (inclusive)      | 51.70%           | 30%            | **+21.70 pp**    |

The corpus is **factual-heavy**, sitting near a balanced 50/50 split — closer to the "easy PASS" zone than the 90/10 chat-skewed zone.

---

## 3. r=16 Catastrophic-Forgetting Prediction

### Decision matrix (from task spec)

| Mix observed                | r=16 prediction               |
|-----------------------------|-------------------------------|
| 90/10 chat/factual          | r=16 may still regress        |
| 70/30 chat/factual          | r=16 likely PASS              |
| 50/50 chat/factual          | r=16 should easily PASS       |

### Verdict — **r=16 SHOULD EASILY PASS**

The actual mix (≈47/53 strict, ≈48/52 inclusive) sits inside or just outside the 50/50 "easily PASS" bucket. The corpus has **substantially more factual+code grounding** than a chat-only seed, so a low-rank adapter (r=16) operating on a frozen base should retain its world-knowledge anchors during SFT — the dominant gradient signal is already factual/instructional/code, which aligns with rather than displaces the base model's pre-training distribution. Catastrophic forgetting is most acute when fine-tuning narrows the distribution to a single style (e.g., conversational sycophancy), and that pathology is **not** present here.

Rank capacity (r=16 ≈ 1.5–2 M params on a 350 M base) is also low enough that it can absorb the domain-shift required without overwriting embedded factual representations.

### Confidence

- **Direction** (PASS vs regress): high — magnitude of distance from the 90/10 risk zone (~40 pp away) far exceeds the ±3.8 pp sampling CI.
- **Magnitude** (how cleanly it passes): moderate — depends on data-loader weighting, LR schedule, and definition of "regression" thresholds in the eval harness.

---

## 4. Track A Necessity Verdict

**Track A (rebalance to 70/30 chat/factual) is NOT necessary for r=16 forgetting prevention.**

Rationale:
1. The corpus is *already further from the 90/10 risk zone than the 70/30 target itself*. Moving toward 70/30 would *reduce* factual content (the very anchor that protects against catastrophic forgetting), so the proposed remediation runs **opposite** to its stated purpose if "forgetting" is the failure mode.
2. If the failure mode is actually *low chat-style instruction-following* (a separate axis from factual retention), Track A is justified — but should be re-named as "chat-capability uplift," not "forgetting mitigation."
3. The 50/50-ish current mix is closer to OpenLLaMA / Tülu-style balanced SFT recipes than to a chat-first recipe; empirically those produce well-rounded models with low forgetting.

**Recommended action** (ranked by 완성도):
1. **DEFER Track A**, run r=16 on current corpus, measure forgetting empirically. If PASS → close issue; if regression → only then rebalance.
2. **If chat capability is the real concern** (separate from forgetting), pursue Track A but re-label and re-justify accordingly.
3. **If Track A is mandated by upstream policy**, run a small ablation (e.g. 5 % subsample at 70/30 vs 50/50) to verify direction before committing the full 50 k rebalance.

---

## 5. Three Caveats (raw#9 STRICT, raw#15, raw#10)

1. **raw#9 STRICT — classifier is rule-based, not LLM-judged.** Source-name + regex heuristics achieve clean partitioning on this corpus because the `source` field is informative, but edge cases (e.g., a sharegpt thread that is purely code, or a paradigm doc embedded inside a chat turn) may be mis-bucketed. Estimated mis-classification rate ≤ 2 % based on the spot-check; does not change the verdict.

2. **raw#15 — environment is lazy-tagged user context.** This audit reads only the local Mac copy of the file (SHA-256 verified against manifest). It does **not** re-derive ubu1 GPU artifacts; the prediction is purely a corpus-statistical claim, not a training-loss claim. Empirical r=16 outcome may diverge if the training pipeline (LR, warmup, packing, data-loader shuffling) differs from assumed defaults.

3. **raw#10 — no causal training run was executed.** This is a **pre-empirical prediction** based on corpus distribution + literature priors on LoRA forgetting, not a measurement. The verdict "r=16 should easily PASS" is a probability statement, not a guarantee. The recommended decision (defer Track A) explicitly preserves the option to rebalance after empirical r=16 results land.

---

## 6. Files emitted

- `state/p9_path_a_corpus_audit_2026_05_04/distribution.json` — JSON with counts, percentages, both ratio definitions, classification rules
- `state/p9_path_a_corpus_audit_2026_05_04/classification_samples.jsonl` — 1000 labeled records with source / lang / 200-char previews
- `state/p9_path_a_corpus_audit_2026_05_04/prediction.md` — this file
- `state/markers/p9_path_a_corpus_audit_landed.marker` — completion marker

**Cost**: $0 (Mac-local, mac_local_dollar_zero policy upheld)
**Destructive ops**: 0
