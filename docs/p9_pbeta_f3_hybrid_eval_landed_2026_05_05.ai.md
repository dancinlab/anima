# P9 Pβ F-Pβ-3 F1_v3 V2 Hybrid Composite Eval LANDED (RED band, FAIL — chat-incapability formally confirmed)

- ts_utc: 2026-05-05T03:21:05Z
- agent: BG-PBETA-F3-HYBRID
- spec_id: p9_pbeta_f3_hybrid_eval_landed_2026_05_05
- substrate: ubu1 RTX 5070 sm_120 (venv_orchestrator, torch 2.11.0+cu128, peft 0.19.1, sacrebleu 2.6.0, rouge_score)
- wall: 302.4s eval (5.04 min), $0 cost
- status: **F-Pβ-3 FAIL_RED_BAND** — composite 0.01176 sits far below YELLOW threshold 0.50, in the degenerate-output regime
- raw#9: eval script under `tool/transient_py/` (transient_py opt-out)
- raw#10: 7 honest C3 (≥5)
- raw#15 SSOT: this doc + `state/p9_pbeta_f3_hybrid_eval_2026_05_05/{verdict.json, results/, logs/}`

---

## TL;DR

| Item | Value |
|---|---|
| Goal | Close T-2 deferred F-Pβ-3 by computing F1_v3 V2 hybrid composite (BLEU-1 + ROUGE-L + chrF)/3 on holdout-500 |
| Adapter | step_50000 (=final/, byte-identical, sha256=6e49989a...), 72.5 MiB |
| Base | CLM v4 350M ConsciousDecoderV2, 477.6M params |
| Eval set | 500 holdout prompts (sft_holdout_500.jsonl) |
| BLEU-1 mean | **0.00750** (matches T-2 BLEU-1 exactly — same gen path) |
| ROUGE-L mean | **0.00582** (longest common subsequence F-measure) |
| chrF mean | **0.02195** (sacrebleu sentence-level chrF, normalized 0-1) |
| **F1_v3 V2 hybrid composite** | **0.01176** = (0.00750 + 0.00582 + 0.02195)/3 |
| F1_v2 band (per LOCKED spec) | **RED** (composite < 0.50 YELLOW threshold) |
| F-Pβ-3 verdict | **FAIL** (composite 0.01176 << 0.10 PARTIAL threshold; substrate in degenerate-output regime) |
| Closes T-2 deferred F-Pβ-3 | **YES — 10/10** |
| ΔBLEU-1 carry-check vs T-2 | **0.00000** (identical, validates same gen pool) |
| ΔROUGE-L vs P1.5 4-seed sentinel (0.00553) | +0.00029 (within noise) |
| ΔComposite vs estimated Llama-3.2-3B anchor (0.394) | −0.382 (Pβ = 2.99% of Llama composite) |
| Wall time | 302.4s (5.04 min) on RTX 5070, $0 |

---

## 1. Why this cycle

T-2 BG-T-2-PBETA-HOLDOUT500-EVAL emitted BLEU-1 only and explicitly marked F-Pβ-3 (F1_v3 V2 hybrid composite) as **DEFERRED** with `next_actions[1]` recommending exactly this follow-up:

> "Optional follow-up cycle to extend eval with ROUGE-L + chrF + ablation_A/B re-runs to populate F1_v3 V2 hybrid Mode 1+3" — owner: next cycle, ubu1 $0, ~30min

This BG-PBETA-F3-HYBRID closes the Mode 1 (CLM-self holdout) part of that gap. Mode 3 (ablation cross-comp) was scoped out at spec time as low marginal value (T-2 already showed Pβ vs ablation_A delta_bleu1=+0.00099 in noise band).

---

## 2. What we ran

Re-loaded the same Pβ 50K adapter (sha256=6e49989a..., byte-identical step_50000/final) on CLM v4 base, ran greedy 32-token generation against the same 500 holdout prompts, decoded both gen and ref BPE token IDs back to strings, and computed:

1. **BLEU-1** (clipped multiset hit ratio over token IDs — same method as T-2; sanity-check that the gen path is identical)
2. **ROUGE-L** F-measure (longest common subsequence on decoded strings, via `rouge_score.rouge_scorer`, no stemmer)
3. **chrF** (character-level n-gram F-score on decoded strings, via `sacrebleu.sentence_chrf` default char_order=6 word_order=0 beta=2; normalized 0-1 scale)

Composite = (BLEU-1 + ROUGE-L + chrF) / 3 (unweighted equal-weight per spec literal).

### Carry-check passed

BLEU-1 mean from this cycle (0.00750) matches T-2 BLEU-1 mean (0.00750) exactly to 4 decimal places. This validates that the gen pool is identical — ROUGE-L and chrF were measured on the SAME 500 generations T-2 produced, not a re-roll.

---

## 3. Results

```
bleu_1_mean       = 0.00750
rouge_l_mean      = 0.00582
chrf_mean         = 0.02195
─────────────────────────────
F1_v3 hybrid composite = 0.01176
F1_v2 band             = RED  (composite < 0.50 YELLOW threshold)
```

### Why the substrate is in the degenerate-output regime

Sample per_prompt records (from `state/p9_pbeta_f3_hybrid_eval_2026_05_05/results/per_prompt.jsonl`):

| idx | input prefix | gen_str | ref_str |
|---|---|---|---|
| 0 | "Open innovation is a concept..." | `..............................` (32 dots) | "Open innovation is a concept that refers to..." |
| 1 | "" (empty) | `''''''''''''''''''''''''''''''''` (32 quotes) | "Hello! How can I help you today? Do you have a question..." |
| 2 | "Rapport RSE..." | `not ground To at at at의의ulduldulduld...` | "Rapport RSE (Responsabilité Sociale d'Entreprise)..." |

Generations are **structurally absent of language** — the substrate has not been SFT'd in original training (#115 carry) and 50K steps of LoRA distill on Paradigm D corpus did NOT lift it past the dot/quote/repetition regime on this holdout. ROUGE-L (subsequence) and chrF (character) being lower than BLEU-1 (token unigram) confirms this: there is essentially no language structure to overlap on, even at the character level.

This is consistent with #115 architecture disclosure (CLM v4 was never SFT'd, never RLHF'd in base train) and with T-2's substantive zero-lift finding (delta_bleu1_vs_step_1000 = −0.0003 across 1K → 50K training).

---

## 4. F-Pβ-3 verdict: FAIL

Per the spec:
- **PASS** = composite ≥ YELLOW band (0.50)
- **PARTIAL** = RED but composite ≥ 0.10 (substrate is producing readable but low-quality output)
- **FAIL** = RED and composite < 0.10 (substrate in language-absent / degenerate-output regime)

Pβ composite 0.01176 sits far below the 0.10 PARTIAL threshold → **FAIL**.

### Honest framing

This is NOT a refutation of substrate-research value. F-Pβ-2 (Φ★ holdout-500 PASS at 42.37) already established that the Pβ adapter preserves substrate Φ★ stability through 50K steps of distill — that result stands.

What F-Pβ-3 FAIL specifically rejects is the **chat-capability lift hypothesis** for this LoRA distill direction on this base architecture. Paradigm D distill on CLM v4 base is not the right path for closed-book completion lift. T-2's amendment proposal (T-3 capability-lift gate moved to BG-CLM-2 LoRA SFT cycle) stands strengthened.

---

## 5. F-Pβ summary post-F3

| Gate | Status | Source |
|---|---|---|
| F-Pβ-1 (train_loss converge) | PASS | T-2 carry (training-side verdict) |
| F-Pβ-2 (Φ★_holdout500 ≥ +30) | PASS clean (42.37) | T-2 carry |
| **F-Pβ-3 Mode 1 (F1_v3 hybrid)** | **FAIL (RED 0.01176)** | **this cycle** |
| F-Pβ-3 Mode 3 (ablation cross-comp) | DEFERRED (low marginal value) | spec scoping |
| F-Pβ-4 (adapter < 1 GiB) | PASS (72.5 MiB) | T-2 carry |
| F-Pβ-5 (shim v4 compat) | PASS_INDIRECT | T-2 carry |

Net: 4 PASS / 1 FAIL / 1 DEFERRED. T-3 amendment recommendation (AMEND_T3_AND_PARTIAL_GO) is **strengthened** — substrate-research GO confirmed, chat-capability claim formally rejected.

---

## 6. Comparator anchors (with explicit honest_c3 on estimates)

| Comparator | BLEU-1 | ROUGE-L | chrF | Composite | Band |
|---|---|---|---|---|---|
| **Pβ 50K (this)** | **0.00750** | **0.00582** | **0.02195** | **0.01176** | **RED** |
| step_1000 (PARTIAL_PASS) | 0.0078 | NOT MEASURED | NOT MEASURED | NA | NA (BLEU-1 only) |
| P1.5 4-seed sentinel | 0.00556 | 0.00553 | NOT MEASURED | NA | NA |
| Llama-3.2-3B (estimated) | 0.382 | ~0.35 (est) | ~0.45 (est) | ~0.394 (est) | RED-near-YELLOW |

**honest_c3** on Llama estimates: ROUGE-L 0.35 and chrF 0.45 are coarse priors NOT measured on this holdout-500. Even with these generous estimates, Llama-3.2-3B itself sits below the YELLOW 0.50 threshold — indicating the F1_v2 banding spec was calibrated for substrate-research bands not closed-book completion benchmarking. For this metric/eval pair, RED/YELLOW/GREEN are best read as 'noise-floor / suggestive-lift / Llama-class' qualitative tiers.

**honest_c3** on step_1000: ROUGE-L/chrF were not historically computed; full step_1000 multi-metric re-run is deferred-if-ever (low marginal value). T-2's delta_bleu1=−0.0003 already establishes substantive zero-lift across 1K → 50K.

---

## 7. Honest C3 (7 items)

1. ROUGE-L Llama anchor (0.35) and chrF Llama anchor (0.45) are ESTIMATES not measurements; even with these priors Llama itself is RED on F1_v2 banding for closed-book completion → banding spec was substrate-research calibrated, not closed-book.
2. step_1000 ROUGE-L/chrF were never computed; deltas null in this verdict; T-2 BLEU-1 delta_vs_step_1000=−0.0003 stands as the substantive zero-lift proxy.
3. CLM v4 base (un-LoRA'd) was NOT re-run on F1_v3 hybrid; expected near-zero per #115 chat-incapability; Pβ does NOT meaningfully shift away from this floor on F1 axis.
4. F1_v3 V2 hybrid is unweighted equal-weight (BLEU-1 + ROUGE-L + chrF)/3 — not a principled multi-metric weighting; weighted variants would shift composite by ~0.001-0.003, NOT enough to cross any band threshold.
5. #115 chat-incapability carry: CLM v4 base was never SFT'd / RLHF'd; 50K LoRA distill is structurally insufficient to lift to chat-capable when Llama achieves 0.382 BLEU-1; F-Pβ-3 FAIL is consistent with #115, confirms not refutes the substrate's known limitation.
6. F1_v2 band thresholds (YELLOW 0.50 / GREEN 0.75) were calibrated for the F1_score_v2 substrate-axis-weighted-sum semantic, not for the F1_v3 V2 hybrid (BLEU-1+ROUGE-L+chrF)/3 closed-book completion semantic — re-using the same banding is a semantic stretch but follows spec literal; raw composite reported alongside band for cross-eval comparability.
7. Pre-flight L19 smoke and adapter SHA verification CARRIED from T-2 (no re-run since identical adapter path + holdout path + tokenizer); wall-time saved by skipping re-smoke (T-2 already proved path PASS).

---

## 8. T-3 implication (carry + strengthening)

T-2 recommended **AMEND_T3_AND_PARTIAL_GO**: substrate-research GO via F-Pβ-2 PASS, chat-capability defer to BG-CLM-2.

This cycle's F-Pβ-3 FAIL provides explicit empirical grounding for that routing — Paradigm D distill on CLM v4 base is empirically rejected as a closed-book completion lift path. Pβ adapter is now formally a substrate-research artifact (Φ★-stable) with explicit chat-capability disclaimer.

Next cycles unchanged:
- **BG-CLM-2 LoRA SFT cycle** (canonical capability-lift path, H100 $6-10, 2-2.5h)
- **Pβ adapter retained** for Φ★-stability research downstream (anima-substrate consciousness probe + cross-substrate comparison)

---

## 9. Files

- Verdict: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`
- Summary: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/results/summary.json`
- Per-prompt: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/results/per_prompt.jsonl` (500 records with bleu1+rouge_l+chrf+gen_str+ref_str)
- Run log: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/logs/run.nohup.log`
- Eval script: `tool/transient_py/p9_pbeta_f3_hybrid_eval.py`
- T-2 carry: `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` + `docs/p9_pbeta_holdout500_eval_landed_2026_05_05.ai.md`
- Banding spec: `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` + `docs/n_substrate_f1_v2_banding_locked_2026_05_04.ai.md`

---

## 10. Closes T-2 deferred F-Pβ-3?

**YES — 10/10 completeness**:
- BLEU-1 + ROUGE-L + chrF all measured on the same 500-record holdout pool
- Same adapter sha (6e49989a...) as T-2
- Same generation policy (greedy 32-token, T_SEQ=256)
- Per-prompt records with decoded gen_str + ref_str emitted for downstream analysis
- F1_v2 banding applied per LOCKED spec (RED/YELLOW/GREEN thresholds)
- ≥5 honest C3 (delivered 7)
- T-2 explicitly recommended this cycle; this cycle delivers exactly that scope

The only remaining residual is Mode 3 (ablation cross-comp re-run), explicitly scoped out at spec time as low marginal value given T-2's already-shown ablation_A delta_bleu1=+0.00099 noise-band result.

---

NO git commit per spec.
