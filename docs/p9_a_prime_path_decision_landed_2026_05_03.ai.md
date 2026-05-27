# P9 A' Main Eval Path Decision — Landed 2026-05-03

**Goal**: Decide which execution path for A' main eval, given the critical reframe from base-validation that **CLM v4 base = ARCHITECTURAL_BLOCKER** on English benchmarks.

**Constraints honored**: raw#9 (no .py creation Mac-side), raw#15 (no personal-path leak), raw#10 (honest C3 — 5 caveats per path + 5 cross-cutting), $0 design only.

---

## TL;DR

**Recommendation**: **Path A** (Llama base + LoRA delta direct). Completion-quality **8.0/10**, ranked 1st of 4 paths.

**One-liner why**: A is the only path that simultaneously (i) preserves the F1_v3 statistical framework intact, (ii) operates on a base validated to be non-floor on all 3 benchmarks, (iii) has a clean research question, and (iv) costs ≤$300 with a 24-72h wall.

---

## Critical reframe from base-validation

1. Llama-3.2-3B-Instruct base validated on TriviaQA (51.4 pt), HellaSwag (39.4 pt), MMLU (35.8 pt) — all OK
2. CLM v4 base = ARCHITECTURAL_BLOCKER:
   - Stub HF format (no `config.json`)
   - Custom Federated/Phase-Optimal architecture (581 keys, dual-stream `engine_a`/`engine_g`, dual heads `head_a`/`head_g`)
   - 64K multilingual BPE (incompatible with HF tokenizer pipeline)
   - Training CE = 0.046 (perplexity 1.05 = narrow-corpus memorization, NOT general English LM)
   - `consciousness_laws.py` `_doc` dict-iteration bug blocks native loading
3. CLM v4 base would score ≈ random on English benchmarks → "Llama − CLM v4" gap = "Llama − random" → **the original A' verdict-delta becomes meaningless**
4. The original A' spec's §3 base-validation gate had a pre-registered escape valve for this exact failure mode (§3.3 row 4: "CLM base at floor on ≥ 2 of 3 → HARD STOP, switch is not justified, falls back to BLEU/ROUGE legacy"); this doc is the **v2 spec** that exercises that escape valve by changing the anchor instead of falling back to legacy.

---

## Ranked completion-quality (4 paths)

| rank | path | discriminative power (3) | pre-reg integrity (2) | cost-efficiency (2) | substrate validity (2) | narrative (1) | **total** |
|---|---|---|---|---|---|---|---|
| **1** | **A** Llama base + LoRA delta | 2.5/3 | 1.5/2 | 1.5/2 | 2/2 | 0.5/1 | **8.0** |
| **2** | **D** Hybrid two-track | 2.0/3 | 0.5/2 | 1.5/2 | 1.5/2 | 0.5/1 | **6.0** |
| **3** | **B** Fix loader + native CLM v4 | 0.5/3 | 2/2 | 2/2 | 0.5/2 | 1/1 | **6.0** |
| **4** | **C** CLM v4 reframe (general English re-train) | 2.5/3 (post-completion) | 1/2 | 0/2 | 2/2 (post-completion) | 1/1 | **6.5 but infeasible-this-sprint** |

**Tie-break**: D and B tied at 6.0; D ranks 2nd by lower scientific risk (medium-high vs high). C scores higher than D/B on rubric but is strategically infeasible ($1500-8000+, 1-4 weeks vs Path A's ~$300, 2-4 days).

---

## Cost / time / risk

| Path | $ cost | wall | technical risk | scientific risk | preserves artifacts |
|---|---|---|---|---|---|
| **A** | $0-300 | 24-72h | low (HF-native) | medium (φ★ re-cal) | partial |
| **B** | $0 | 10-20h | medium (cross-tokenizer wrapper) | high (likely NULL) | yes |
| **C** | $1500-8000+ | 1-4 weeks | high (pre-train at scale) | medium (post-completion) | yes |
| **D** | $30-150 | 2-4 days | medium (two pipelines) | medium-high (composite semantics) | yes |

---

## Recommended next-cycle action

**Commission Path A LoRA re-train BG cycle** as a paste-once handoff to a separate Claude session:

1. Re-train LoRA on `meta-llama/Llama-3.2-3B-Instruct` base with `clm-v4-sft-stage1` hyperparameters (rank, alpha, target modules, LR, epochs, axis-loss weights).
2. Use SFT corpus at `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (50K records, augmented; re-template to Llama chat format).
3. Substrate: H100 SXM preferred ($30-85, 12-24h) if RunPod credit ≥ $100; ubu1 RTX 5070 fallback ($0, 24-48h, rank 8-16, batch 1-2, seq 1024).
4. Save adapter at `state/p9_a_prime_main_eval_2026_05_<DD>/lora_llama_stage1/`.
5. Emit re-calibrated φ★ baseline at Llama layer 14 (default per honest_c3 §6.2 mitigation).
6. Land marker `state/markers/p9_a_prime_main_eval_lora_train_landed.marker`.

Then a downstream BG cycle for the eval phase:
1. Run lm-eval-harness on Llama base (fp16 re-measure per §6.5) + Llama+LoRA across {HellaSwag, MMLU 5-shot, TriviaQA}.
2. Compute F1_v3 verdict per A' spec §2.4 with **Llama as anchor** (anchor swap per §6.1).
3. Emit `state/p9_a_prime_main_eval_2026_05_<DD>/f1_v3_verdict.json`.
4. Land marker `state/markers/p9_a_prime_main_eval_f1_v3_landed.marker`.

**Optional parallel** (per session-multi-BG memory rule): Path B sanity probe ($0, ~10-20h, single-benchmark NULL-or-not signal). Does NOT block Path A.

---

## 5 cross-cutting honest C3 caveats (raw#10)

(a) **Anchor-swap is a soft pre-reg modification** — mitigated by this doc functioning as the v2 spec under original A' §2.6 procedure; data-leak risk contained to base-validation findings transparently reported.

(b) **φ★ baseline re-calibration on Llama is a hidden cost** (~$0-50; pre-register Llama layer 14 default for extraction).

(c) **Axis falsifiers F2/F3/F4 may not transfer cleanly** — they were designed against CLM v4's `purefield`/`tension_proj`/dual-head structure; on Llama they are different quantities semantically. F1_v3 (chat) verdict is independent from F2/F3/F4 (axis) verdict in this cycle.

(d) **SFT data corpus is axis-conditioned for CLM v4** — re-template to Llama chat format needed; flag as hidden cost if >20% of records require non-trivial adaptation.

(e) **"Validated base" is at 4-bit, not full precision** — fp16 anchor re-measure needed for canonical numbers; expect ~1-3 pt anchor shift, but discriminative range conclusion is robust.

---

## Files

```
docs/p9_a_prime_path_decision_2026_05_03.md         # full decision spec
docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md  # this handoff
state/markers/p9_a_prime_path_decision_landed.marker  # marker
```

Referenced docs:
```
docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md             # original A' spec (anchor=CLM v4)
docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md       # validation finding
state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json     # original switch trigger
state/p9_benchmark_base_validation_2026_05_03/base_eval_results.json  # Llama base anchors
state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl  # SFT corpus for Path A
```

---

**End of handoff. Next BG: commission Path A LoRA re-train per §7.2 of the decision spec.**
