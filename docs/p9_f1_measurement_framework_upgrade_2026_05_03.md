# P9 F1 Measurement Framework Upgrade — BLEU-1 saturation contingency + composite F1_v3 spec

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-03
- **Phase**: P9 SFT EXEC — F1 measurement contingency (preemptive, ahead of holdout-500 re-eval)
- **Cost**: $0 (spec authorization only, NO execution, NO falsifier modification)
- **Status**: SPEC_DRAFT — landing spec gated on holdout-500 BLEU-1 re-eval verdict
- **Constraints**: HEXA-only · raw#9 NO .py · raw#10 honest C3 mandatory · raw#15 NO personal paths · raw#71 falsifier-bound

---

## §0 한 줄 verdict

**Anticipating BLEU-1 measurement floor at N=32 (4 distinct axis perturbations all clustered at 0.00586 = 6/1024 quantization band).** Doc proposes (a) 9-metric alternative inventory ranked by reliability-vs-cost, (b) composite F1_v3 = (BLEU-1 + ROUGE-L + BERTScore-F1) / 3 normalized to Llama anchor, (c) Phase 0/1/2 implementation roadmap, (d) F1 spec mk3 schema_history v3 entry draft. **Decision gate**: holdout-500 result confirms saturation → activate Phase 0 (BLEU-2/3 + ROUGE-1/L) within 1d at $0 cost. Falsifier spec (`falsifiers_preregistered.json`) **NOT modified** — append-only audit trail respected; v3 entry queued.

---

## §1 Why BLEU-1 may saturate (root-cause anticipation)

### §1.1 Quantization floor at N=32

- Holdout calib set N=32 prompts × T=64 tokens × greedy decode → unique 1-gram tokens per response capped at ~30-50
- 4 axis perturbations all reading 0.00586 = exactly 6/1024 → indicates n-gram overlap counter saturated at 6 hits across 1024-token reference window
- ±0.001 quantization band swallows real signal differences smaller than ~1 n-gram match per 500 tokens

### §1.2 N=500 expansion alone may not rescue

Even with holdout-500:
- Greedy decoding produces near-identical outputs across small LoRA perturbations → low n-gram diversity
- Short responses (T=64 ceiling) limit precision denominator headroom
- BLEU is **precision-only** — does not penalize missing reference content (no recall)
- BLEU ignores **semantic equivalence** — synonyms, paraphrase, word reorder all penalized
- Llama anchor 0.1555 itself is low (typical chat BLEU-1 is 0.20-0.40 on longer outputs) → confirms BLEU-1 ceiling effect already present in the anchor

### §1.3 Failure mode classification

| Failure mode | Symptom | Likelihood | Detection |
|---|---|---|---|
| **F-A quantization floor** | All variants ≈ 6/1024 | HIGH (already observed N=32) | variance across perturbations < 1e-3 |
| **F-B BLEU-anchor undershoot** | Llama 0.1555 itself near precision ceiling | MEDIUM | re-eval Llama on N=500 |
| **F-C semantic-blind** | Perturbations differ semantically but BLEU identical | HIGH | manual qualitative spot-check |
| **F-D recall-blind** | LoRA produces shorter responses, BLEU unchanged | MEDIUM | length distribution check |

---

## §2 Alternative metrics inventory (9-metric, ranked)

### §2.1 Ranking matrix (reliability × cost)

| Rank | Metric | Reliability | Cost (N=500) | Lib | Notes |
|---:|---|---|---|---|---|
| 1 | **BERTScore-F1** | HIGH (semantic, P+R+F) | ~30min GPU | `bert-score` (HF DeBERTa) | best semantic anchor; standard NLG eval |
| 2 | **ROUGE-L** | MED-HIGH (recall, longest common subseq) | ~5min CPU | `rouge_score` | recall-oriented, complements BLEU precision |
| 3 | **chrF / chrF++** | MED-HIGH (char-level F-score) | ~5min CPU | `sacrebleu` | tokenization-agnostic, robust on short text |
| 4 | **SBERT cosine** | MED (sentence embedding sim) | ~10min CPU/GPU | `sentence-transformers` (80MB MiniLM) | direct semantic sim |
| 5 | **METEOR** | MED (synonyms via WordNet, word order) | ~10min CPU | `nltk` + WordNet | synonym matching addresses BLEU recall blind |
| 6 | **BLEU-2/3/4** | LOW-MED (extends n-gram order) | ~5min CPU | `nltk` | partially mitigates 1-gram floor; same precision-only weakness |
| 7 | **GLEU** | MED (Google chat BLEU variant, P+R min) | ~5min CPU | `nltk` | designed for short chat; under-cited |
| 8 | **Perplexity-on-reference** | LOW-MED (model PPL on gold) | ~15min GPU | direct forward pass | requires Llama anchor PPL too; interpretation tricky |
| 9 | **LLM-as-judge** | HIGH (rubric scoring, pairwise win-rate) | ~1hr GPU | Llama-3.2-3B inference × 500 | gold standard but expensive + judge bias |

### §2.2 Top 3 selection (composite F1_v3 components)

**Selection criteria**: complementary signal (precision + recall + semantic) × independent failure modes × all reproducible at $0.

| # | Metric | Role in composite | Why |
|---|---|---|---|
| 1 | **BLEU-1** (kept) | precision baseline | back-compat with v2 spec, Llama anchor already measured |
| 2 | **ROUGE-L** | recall-oriented | catches missing reference content BLEU ignores |
| 3 | **BERTScore-F1** | semantic anchor | catches paraphrase + synonym variants both BLEU and ROUGE miss |

**Rejected for composite (reasoned)**:
- BLEU-2/3/4: same precision-only failure mode as BLEU-1, redundant
- chrF: high redundancy with BLEU-1 (both surface-form)
- METEOR: WordNet-dependent, weaker than BERTScore for semantic
- SBERT cosine: BERTScore-F1 strictly dominates (P+R+F decomposition)
- GLEU: under-validated on Korean/multilingual chat
- Perplexity: interpretation conflict (lower-is-better vs higher-is-better composite)
- LLM-as-judge: cost asymmetry (60× rest), reserve for Phase 2 verification

---

## §3 Composite F1_v3 metric proposal

### §3.1 Formula

```
F1_v3_raw = (1/3) · [ BLEU_1 + ROUGE_L + BERTScore_F1 ]

F1_v3_normalized = F1_v3_raw / Llama_anchor_F1_v3_raw

Pass condition: F1_v3_normalized >= 0.85
              equivalently F1_v3_raw >= 0.85 * Llama_anchor_F1_v3_raw
```

### §3.2 Component weighting (uniform 1/3 each, justified)

| Component | Weight | Rationale for uniform |
|---|---:|---|
| BLEU-1 | 0.333 | back-compat; surface precision floor |
| ROUGE-L | 0.333 | recall complement |
| BERTScore-F1 | 0.333 | semantic complement |

**Why uniform**: differential weighting requires preregistered evidence on relative importance per Anima domain — absent for chat coherence. Uniform = honest default, revisit at v4 with empirical calibration.

### §3.3 Llama anchor recomputation requirement

Before activating v3 gate, must measure Llama-3.2-3B-Instruct on holdout-500 for **all 3 components**:

| Component | Llama-3.2-3B anchor (placeholder, must measure) |
|---|---|
| BLEU-1 | 0.1555 (already measured 2026-05-03) |
| ROUGE-L | TBD (~0.20-0.30 expected per chat literature) |
| BERTScore-F1 | TBD (~0.85-0.90 expected per chat literature) |
| **F1_v3_raw anchor** | **TBD = mean of 3** |

### §3.4 Threshold calibration

- 0.85 ratio retained from v2 — preserves "strong-floor" semantics
- v3 may LOOSEN ratio (e.g. 0.75) if 3-component variance is higher than BLEU-1 alone (composite noise)
- Decision deferred until 3-component Llama anchor measured

---

## §4 Cost / wall budget per metric

| Metric | Lib install | Wall (N=500) | GPU | Notes |
|---|---|---|---|---|
| BLEU-1/2/3/4 | `nltk` | 5min | NO | already in pipeline |
| ROUGE-1/2/L | `rouge_score` | 5min | NO | trivial install |
| chrF / chrF++ | `sacrebleu` | 5min | NO | trivial install |
| METEOR | `nltk` + WordNet corpus | 10min | NO | WordNet 28MB download |
| BERTScore | `bert-score` (DeBERTa-v3-base) | 30min | YES | first-call model download ~440MB |
| SBERT cosine | `sentence-transformers` (MiniLM-L6-v2) | 10min | OPTIONAL | 80MB model |
| GLEU | `nltk` | 5min | NO | trivial |
| Perplexity-ref | direct forward | 15min | YES | reuse SFT model |
| LLM-as-judge | Llama-3.2-3B inference | ~1hr | YES | 500 prompts × 3-5s each |

**Budget envelopes**:
- Phase 0 (BLEU-2/3 + ROUGE-1/L): **$0, ~10min wall, no GPU**
- Phase 1 (+ BERTScore): **$0, ~40min wall, GPU 30min**
- Phase 2 (+ SBERT + LLM-judge composite): **~$1-3 RunPod, ~1.5hr wall, GPU 1hr**

---

## §5 Implementation roadmap

### §5.1 Phase 0 — cheapest, immediate (no decision dependency)

- **Trigger**: Holdout-500 BLEU-1 re-eval confirms saturation (variance < 1e-3 across perturbations)
- **Add**: BLEU-2, BLEU-3 (extend n-gram order), ROUGE-1, ROUGE-L (recall axis)
- **Deliverable**: `state/p9_f1_phase0_alt_metrics_2026_05_03/{metrics,trajectory,verdict}.json`
- **Cost**: $0, 10min wall on existing 32 or 500 holdout
- **Decision**: if ROUGE-L shows variance > 1e-2 across perturbations → v3 spec proceed; else escalate to Phase 1

### §5.2 Phase 1 — semantic anchor (BERTScore)

- **Trigger**: Phase 0 confirms recall axis insufficient OR semantic-blind suspected
- **Add**: BERTScore-F1 (P/R/F decomposition)
- **Deliverable**: `state/p9_f1_phase1_bertscore_2026_05_03/...`
- **Cost**: $0 (ubu1 RTX 5070), 40min wall
- **Decision**: compute composite F1_v3 = mean(BLEU-1, ROUGE-L, BERTScore-F1) → if Llama anchor recomputable and gate calibratable → write v3 spec

### §5.3 Phase 2 — full composite verification (SBERT + LLM-judge)

- **Trigger**: P9 verdict ambiguous (composite F1_v3 within ±10% of pass threshold)
- **Add**: SBERT cosine (independent semantic check), LLM-as-judge (rubric + pairwise win-rate)
- **Deliverable**: `state/p9_f1_phase2_composite_verify_2026_05_03/...`
- **Cost**: ~$1-3 RunPod (Llama-3.2-3B inference), 1.5hr wall
- **Decision**: full 5-metric inventory → final verdict on chat coherence; v4 schema entry candidate

---

## §6 F1 spec mk3 schema_history v3 entry draft

**NOTE**: Draft only. **NOT** to be appended to `falsifiers_preregistered.json` until:
1. Holdout-500 BLEU-1 re-eval confirms saturation (failure mode F-A or F-C)
2. Phase 0 ROUGE-L Llama anchor measured
3. Phase 1 BERTScore-F1 Llama anchor measured
4. Composite F1_v3 raw Llama anchor computed

```json
{
  "version": 3,
  "ts_utc": "2026-05-03TXX:XX:XX+00:00",
  "F1_pass_threshold": "F1_v3_raw >= 0.85 * llama_anchor_F1_v3_raw (composite of BLEU-1, ROUGE-L, BERTScore-F1, uniform 1/3 weights)",
  "calibration_basis": "BLEU-1 alone exhibited measurement floor on holdout-N (4 distinct LoRA axis perturbations all clustered at 0.00586 = 6/1024 quantization band). Composite F1_v3 introduces recall (ROUGE-L) and semantic (BERTScore-F1) axes with independent failure modes. Llama-3.2-3B-Instruct anchors measured on holdout-500: BLEU-1 0.1555 (carryover v2), ROUGE-L TBD, BERTScore-F1 TBD. F1_v3_raw anchor = mean(3) TBD. Component weights uniform 1/3 — differential weighting deferred to v4 pending empirical importance calibration. Threshold ratio 0.85 retained from v2; may LOOSEN to 0.75 if composite variance higher than BLEU-1 alone.",
  "components": {
    "BLEU_1": {"weight": 0.333, "llama_anchor": 0.1555},
    "ROUGE_L": {"weight": 0.333, "llama_anchor": "TBD"},
    "BERTScore_F1": {"weight": 0.333, "llama_anchor": "TBD"}
  },
  "deprecates_v2_threshold": false,
  "rationale_for_additive_not_replacement": "v2 BLEU-1 single-gate retained as a sub-component for back-compat; v3 wraps v2 in composite. F1 verdict reads v3 if all 3 anchors measured, else falls back to v2."
}
```

---

## §7 raw#10 honest C3 caveats (3 mandatory disclosures)

### §7.1 (C3-1) Metric arbitrariness — uniform 1/3 weighting is convention not evidence

Composite F1_v3 = (BLEU + ROUGE-L + BERTScore-F1) / 3 with uniform weights is a **default convention**, NOT empirically calibrated for chat coherence in the Anima domain. Differential weighting (e.g. 0.5 BERTScore + 0.3 ROUGE-L + 0.2 BLEU) might better reflect domain importance, but requires preregistered evidence absent at v3 cycle. Risk: composite may pass while semantically poor (BLEU + ROUGE high, BERTScore low) or fail while semantically good (BLEU low quantization, BERTScore high). Mitigation: report all 3 components separately alongside composite; v4 may shift weights.

### §7.2 (C3-2) Cost asymmetry — LLM-judge is 60× rest, biases toward cheaper-but-weaker proxies

Phase 2 LLM-as-judge (~1hr GPU, $1-3) is gold-standard but 60× more expensive than Phase 0 (10min CPU). This cost cliff biases practical evaluation toward BLEU/ROUGE/BERTScore even when LLM-judge would be more reliable for ambiguous cases. Furthermore: judge model (Llama-3.2-3B) has its own bias — same model family as anchor inflates self-similarity scoring. Mitigation: reserve LLM-judge for ambiguous verdicts (composite within ±10% of threshold), use distinct-family judge if budget permits (Mistral-7B / Qwen-2.5-7B).

### §7.3 (C3-3) Threshold calibration — 0.85 ratio inherited untested for composite

Threshold `F1_v3 >= 0.85 * llama_anchor` is inherited from v2 (BLEU-1 single-gate) with NO recalibration for composite noise characteristics. Composite metrics typically have HIGHER variance than single metrics (3-source noise sum), so 0.85 may be too STRICT for v3 (false-fail risk) or too LOOSE if BERTScore is highly stable and dominates (false-pass risk). Mitigation: measure Llama anchor 3 times on holdout-500 with seed variation, compute std, set threshold at `anchor_mean - k*anchor_std` where k=1 (loose) or k=2 (strict). v3 lands with k preregistered, NOT post-hoc.

---

## §8 Decision tree — when to write v3

```
Holdout-500 BLEU-1 re-eval
├─ variance > 1e-2 across perturbations → v2 BLEU-1 sufficient → NO v3 needed
└─ variance < 1e-3 (saturation confirmed)
   ├─ run Phase 0 (BLEU-2/3 + ROUGE-1/L)
   │  ├─ ROUGE-L variance > 1e-2 → write v3 with BLEU-1 + ROUGE-L only (skip BERTScore)
   │  └─ ROUGE-L variance < 1e-3 → run Phase 1
   │     ├─ BERTScore-F1 variance > 1e-2 → write v3 full composite
   │     └─ BERTScore-F1 variance < 1e-3 → escalate to Phase 2 (LLM-judge required)
```

---

## §9 비충돌 + 산출

- **WRITE**: this doc only (`docs/p9_f1_measurement_framework_upgrade_2026_05_03.md`)
- **DO NOT MODIFY**: `state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json` (v3 entry queued, not appended)
- **DO NOT EXECUTE**: no measurement runs (spec only)
- **DO NOT COMMIT**: per user constraint
- raw#9 NO .py: this is a markdown spec, no executable code attached
- raw#15 NO personal paths: all paths repo-relative
- raw#71 falsifier-bound: v3 schema draft preregistered before measurement

---

## §10 References

- v2 spec: `state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json` (schema v2, BLEU-1 ≥ 0.132 = 0.85 × 0.1555)
- F1 composite v2 (different domain, n-substrate verdict): `docs/strategic_f1_composite_v2_2026_05_02.md`
- Phase 0 warmup live: `docs/p9_p0_warmup_live_landed_2026_05_03.ai.md` (F1 BLEU-1 skipped per raw#10 honest)
- BERTScore: Zhang et al ICLR 2020, `https://arxiv.org/abs/1904.09675`
- ROUGE: Lin ACL 2004 workshop
- METEOR: Banerjee + Lavie ACL 2005 workshop
- chrF: Popović WMT 2015

---

**status**: P9_F1_MEASUREMENT_FRAMEWORK_UPGRADE_2026_05_03_SPEC_DRAFT
**verdict_key**: F1_V3_COMPOSITE_DRAFT · BLEU1_PLUS_ROUGEL_PLUS_BERTSCOREF1_UNIFORM_THIRD · PHASE_0_1_2_ROADMAP · LLAMA_ANCHOR_RECOMPUTE_REQUIRED · V3_SCHEMA_QUEUED_NOT_APPENDED · 3_HONEST_C3 · DECISION_GATE_HOLDOUT_500_RE_EVAL
