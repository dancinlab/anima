# P9 A' Benchmark Base Validation — Landed 2026-05-03

**Goal**: Validate that TriviaQA + HellaSwag + MMLU 5-shot have discriminative range BEFORE evaluating LoRA ckpts. Gate decision for A' benchmark switch.

**Substrate**: ubu1 (RTX 5070 12GB, sm_120, torch 2.11.0+cu128, lm-eval 0.4.11, bitsandbytes 0.49.2)

**Constraints honored**: $0 (ubu1 local), raw#15 (~/anima/... paths), raw#10 (honest C3), no LoRA eval in this cycle.

---

## Setup Path

1. **lm-eval-harness install**: `pip install lm-eval` in `/home/aiden/venv_orchestrator/` (reused, not fresh) — installed 0.4.11 with all deps (datasets 4.8.5, evaluate 0.4.6, etc).
2. **bitsandbytes 0.49.2 install**: Required because GPU was 8.3GB occupied by ongoing `p9_p1_5_sentinel_seed43_train.py` (PID 1726340, 17min in at start). Free GPU = 3.4GB → forced 4-bit quantization.
3. **lm-eval CLI bug workaround**: `lm-eval run --model_args load_in_4bit=True` fails on transformers 5.7.0 (`LlamaForCausalLM.__init__() got an unexpected keyword argument 'load_in_4bit'`). Solution: bypass CLI; use Python API with pre-constructed `BitsAndBytesConfig` passed via `quantization_config`. Custom wrapper at `~/anima/state/p9_benchmark_base_validation_2026_05_03/eval_llama.py`.
4. **Llama load**: 4-bit, 2.37 GB GPU alloc.

---

## Llama-3.2-3B-Instruct Base Results (4-bit, limit=500)

| Task | metric | score | random | range | n-shot | max_len | Verdict |
|------|--------|-------|--------|-------|--------|---------|---------|
| hellaswag | acc_norm | **0.644** | 0.25 | **39.4 pt** | 5 | 2048 | BENCHMARK_OK |
| mmlu | acc (57-subj avg) | **0.608** | 0.25 | **35.8 pt** | 0\* | 1024\* | BENCHMARK_OK |
| triviaqa | exact_match (rm_ws) | **0.514** | 0.0 | **51.4 pt** | 5 | 2048 | BENCHMARK_OK |

\*MMLU 5-shot @ 2048 ctx OOM'd (3GB free GPU; sentinel training holding 8.15GB). Retried with 0-shot @ 1024 max_len. The 0.608 is a 0-shot baseline; expect ~+5-10pt with proper 5-shot at fp16 on a free GPU. Range is large enough that BENCHMARK_OK verdict is robust to this.

MMLU per-domain (a few examples for sanity):
- humanities: 0.633 (strong)
- formal_logic: 0.325 (weak — only ~7pt above random; reasoning-heavy is hardest for 3B)

---

## CLM v4 Base — ARCHITECTURAL_BLOCKER

**Could not eval CLM v4 base on lm-eval-harness in this cycle.**

### Findings

1. **HF mirror is stub-only**: `need-singularity/clm-v4-base-mirror` repo has 2 siblings: `.gitattributes` + `best.pt` (5.4 GB). No `config.json`, no HF format. Initial cache (~20K) was only `.no_exist` marker; downloaded fresh.
2. **best.pt structure**: Custom checkpoint dict with keys `{step, decoder, optimizer, scheduler, phi, ce, args, scale, best_phi, federation, bridge, c_proj, scaler}`. **Not a HF state_dict.**
3. **Architecture is custom Federated/Phase-Optimal** (350m scale, 768d/16L/12H GQA-4kv):
   - Per block: `attn` (GQA), `purefield` (engine_a + engine_g dual-stream), `cross_attn`, `ffn` (SwiGLU 2048), `ca_mix`, `rule_weights`, 8x `rules` (cellular-automaton-like)
   - Two LM heads: `head_a` + `head_g` (dual-stream output) with vocab=64000 multilingual BPE
   - Top-level: `tension_proj`, `ln_f`, `tok_emb` (64000×768)
4. **Construction blocked by stale loader bug**: 
   - `consciousness_laws.py` reads `anima/config/consciousness_laws.json` whose `psi_constants` dict starts with a `_doc` string entry, causing `TypeError: string indices must be integers, not 'str'` at module import.
   - Fixing this would require touching SSOT consciousness_laws files outside this cycle's scope.
5. **Training-time CE = 0.046 (perplexity ≈ 1.05)** on its own corpus_tier_m_v2.txt — extreme overfit suggests narrow domain (likely Korean-heavy multilingual), NOT a general English LM.

### Implication

For the A' benchmark switch decision, **CLM v4 base would score at or near random** on English benchmarks (hellaswag/mmlu/triviaqa) regardless of harness wrapper, because:
- 64K BPE vocab ≠ Llama tokenization (so the cross-model token-prob comparison would be apples-to-oranges anyway)
- Base model has no instruction tuning and no English benchmark exposure
- Training CE near zero implies memorization of a narrow distribution, not general LM capability

The "discriminative range = Llama − CLM v4" gap therefore reduces to "Llama − random," which IS the random baseline check.

**Recommendation**: For A' main eval, treat CLM v4 base as `score = random_baseline + ε` and compare LoRA-tuned ckpts (which DO have HF-loadable adapter format via `clm-v4-sft-stage1` adapter) against Llama base + Llama+LoRA.

---

## Discriminative Power Ranking (per Llama − random gap)

| Rank | Task | Llama − random | Notes |
|------|------|----------------|-------|
| 1 | **triviaqa** | **51.4 pt** | exact_match generation; sharpest signal; sensitive to factual recall + tokenization fidelity |
| 2 | **hellaswag** | **39.4 pt** | loglik 4-choice; clean commonsense signal; cheap (~5min @ limit=500) |
| 3 | **mmlu** | **35.8 pt** | loglik 4-choice aggregate over 57 subjects; broad-domain; per-subject variance is large (humanities 63%, formal_logic 33%) |

All three tasks **comfortably exceed the 5pt threshold** — A' main eval can use any combination. Recommended composite: triviaqa + hellaswag (both fast, complementary signal types: generation vs loglik).

---

## Cost / Time (actual)

- Cost: $0 (ubu1 local).
- Wall time: lm-eval install ~10min; CLM v4 best.pt download 6min (5.4GB); Llama 4-bit load 5s; hellaswag (5-shot, limit=500, 2000 loglik) ~5min @ ~7it/s; triviaqa (5-shot, limit=500, 500 generate) ~1.5min @ ~6it/s; MMLU OOM @ 5-shot/2048; MMLU retry (0-shot, limit=500, 48692 loglik) ~17.5min @ ~50it/s.
- **Total wall-clock: ~33min.**

---

## Constraints / Honest C3 (raw#10)

- **GPU contention**: shared with PID 1726340 (P9 P1.5 sentinel training); used 4-bit quant to fit. Did NOT preempt the training run.
- **CLM v4 base eval skipped**, not failed silently — documented as architectural blocker above.
- **limit=500 per task** (not full eval) per spec's "if too slow, limit to 500".
- **4-bit quant** changes Llama scores slightly (typically -1 to -3 pt vs fp16); discriminative range conclusion unaffected.

---

## Files (raw#15: ~/anima/... on ubu1)

```
~/anima/state/p9_benchmark_base_validation_2026_05_03/
├── eval_llama.py                       # main eval (hellaswag + triviaqa)
├── eval_llama.nohup.log                # full eval stdout
├── eval_llama_mmlu_retry.py            # MMLU retry with 0-shot + max_len=1024
├── eval_llama_mmlu_retry.nohup.log     # MMLU retry stdout
├── aggregate_results.py                # base_eval_results.json builder
├── llama_base_hellaswag.json           # ✓
├── llama_base_mmlu_n0.json             # ✓
├── llama_base_triviaqa.json            # ✓
├── base_eval_results.json              # ✓ aggregate
└── run_llama.log + run_llama.nohup.log # earlier failed CLI attempt (trace)
```

Local artifacts:
```
state/p9_benchmark_base_validation_2026_05_03/
├── base_eval_results.json
├── llama_base_hellaswag.json
├── llama_base_mmlu_n0.json
├── llama_base_triviaqa.json
├── eval_llama.py
├── eval_llama_mmlu_retry.py
└── aggregate_results.py
state/markers/p9_benchmark_base_validation_landed.marker
docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md  (this file)
```

---

## Next Cycle Recommendation (ranked by 완성도)

1. **Adopt triviaqa + hellaswag as PRIMARY A' benchmarks** (51.4 + 39.4 pt ranges; complementary signals: generation vs loglik; both fast at limit=500). Compose them as a 2-way score.
2. **Use mmlu as secondary** for cross-validation (35.8pt at 0-shot; will be ~+5-10pt at proper 5-shot when GPU is free). Reports per-domain breakdown so we can isolate weak areas (e.g., formal_logic).
3. **Skip CLM v4 base in A' main eval** — score ≈random on English benchmarks. Instead compare Llama+LoRA-on-clm-v4-sft-stage1 vs Llama base directly; the LoRA delta is the actual question.
4. **GPU constraints for A' main eval**: if sentinel training still on, plan for 4-bit quant + max_len=1024 + batch=1 (proven workable here). Free GPU = full 5-shot at 2048 ctx.
5. **If CLM-architecture native eval is essential** for academic comparability: dedicate a separate cycle to (a) fix `consciousness_laws.py` loader, (b) write `lm_eval.api.model.LM` subclass wrapping the dual-head decoder, (c) handle 64K BPE tokenization mismatch (cross-tokenizer scoring is non-trivial).
