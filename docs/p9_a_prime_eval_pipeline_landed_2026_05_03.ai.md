# P9 A' Main Eval Pipeline — Landed 2026-05-03

**Goal**: Pre-build A' main eval pipeline so it's ready to run instantly when Path A LoRA ckpts arrive (Pod `29dhlqk508ugoc` training in flight, ETA 8-12h).

**Substrate**: ubu1 (RTX 5070 12GB, sm_120, torch 2.11.0+cu128, lm-eval 0.4.11, peft 0.19.1, bitsandbytes) + Mac hexa for verdict.

**Constraints honored**: raw#9 STRICT (Mac → hexa only, ubu1 .py OK), raw#15, raw#10, $0 (no LoRA eval triggered), no Path A pod preempt.

---

## Status Summary

| Deliverable | Path | Status |
|---|---|---|
| Loader smoke test | `~/anima/state/p9_a_prime_main_eval_2026_05_03/loader_smoketest.py` | PASS (7/7 stages) |
| Eval driver | `~/anima/state/p9_a_prime_main_eval_2026_05_03/eval_llama_lora_ckpt.py` | READY (group-task patch applied for MMLU) |
| Base per-example extractor | `~/anima/state/p9_a_prime_main_eval_2026_05_03/extract_base_per_example.sh` | COMPLETE (hellaswag=500 + mmlu=12173 + triviaqa=500 entries; 774s wall) |
| LoRA runner convenience | `~/anima/state/p9_a_prime_main_eval_2026_05_03/run_all_lora_ckpts.sh` | READY (idempotent, skips done) |
| Verdict hexa | `tool/p9_a_prime_verdict.hexa` | READY (selftest PASS, synthetic e2e PASS, real-base e2e PASS) |
| Pipeline meta | `state/p9_a_prime_main_eval_pipeline_2026_05_03/pipeline_meta.json` | EMITTED |
| Marker | `state/markers/p9_a_prime_eval_pipeline_landed.marker` | EMITTED |

---

## 1. Loader Smoke Test (PASS)

Verifies pipeline can:

1. Load Llama-3.2-3B-Instruct base in 4-bit nf4 (matches base validation cycle precision)
2. Construct synthetic LoRA (r=64, alpha=64, 7 target modules — matches Path A `train_llama_lora.py` spec at `state/p9_path_a_llama_lora_2026_05_03/train_llama_lora.py.txt`)
3. Save adapter to disk + roundtrip via `PeftModel.from_pretrained`
4. Wrap (base + LoRA) in lm-eval `HFLM`
5. Run lm-eval on 5 HellaSwag examples with `log_samples=True`
6. Extract per-example correctness array

**Result** (`loader_smoketest.json`):

```
verdict: PASS
stages_passed: 7/7
base_alloc_gb: 2.24
lora_trainable_params: 97,255,424 (5.12% of 1.9B total)
alloc_after_roundtrip_gb: 4.09
synthetic_lora_run_acc_norm: 0.8 (random init; only validates wiring)
per_example_correctness_extracted: [1, 1, 1, 1, 0]  (5/5 extracted with doc_id, target, acc, acc_norm)
total_wall_s: ~18.7 (load + attach + save + roundtrip + wrap + eval + extract)
```

**Δ-measurement framework confirmed well-defined**: each per-example entry contains `{doc_id, doc_hash, acc_norm, acc, target}`. Same doc_id set across (base, ckpt) eval runs → paired stats trivial.

## 2. Eval Driver

`eval_llama_lora_ckpt.py` — single (ckpt, task) pair eval.

**Args**:
- `--ckpt-repo` (HF Hub) OR `--ckpt-local-dir` (local) OR `--base-only` (re-anchor)
- `--ckpt-revision` (e.g. `step-2000` for Path A ckpts)
- `--task hellaswag|mmlu|triviaqa`
- `--limit 500` (default, matches base validation; `--limit 0` = full eval)
- `--load-in-4bit` (default true; `--no-4bit` for fp16)
- `--seed 42` (canonical per A' §2.5)
- `--output <path>`

**LOCKED config** (per A' spec §2.5):

| param | value |
|---|---|
| dtype | bf16 / 4bit nf4 (matches base validation) |
| device | cuda:0 |
| batch_size | 1 |
| seed | 42 |
| log_samples | true |
| num_fewshot | hellaswag=5, mmlu=0, triviaqa=5 |
| max_length | hellaswag=2048, mmlu=1024, triviaqa=2048 |

**Output schema**: `anima/p9_a_prime_main_eval/per_ckpt_per_task/1` — emits `aggregate`, `per_example_correctness` (list of `{doc_id, doc_hash, acc_norm, acc, target}`), `total_wall_s`, full `log_samples` JSON in adjacent `_log_samples/` dir.

## 3. Base Per-Example Extractor

`extract_base_per_example.sh` runs `eval_llama_lora_ckpt.py --base-only` for all 3 tasks (limit=500, 4-bit, seed 42) sequentially, then merges into `base_per_example_correctness.json`.

**Why pre-extract**: paired bootstrap + McNemar require parallel arrays of base + ckpt correctness on identical doc_ids. Re-extracting once now (at limit=500, seed=42) gives canonical reference for all 5 future LoRA-ckpt evals.

**Wall**: ~7-25 min total (matches base validation cycle: hellaswag ~2.5min, triviaqa ~1.5min, mmlu ~17min @ 0-shot).

**Output** (COMPLETE): `~/anima/state/p9_a_prime_main_eval_2026_05_03/base_per_example_correctness.json` (3.8 MB) with schema `anima/p9_a_prime_main_eval_pipeline/base_per_example/1`. Mirrored locally to `state/p9_a_prime_main_eval_pipeline_2026_05_03/base_per_example_correctness.json`.

**Actuals**:
- hellaswag: 500 per-example entries (`acc=0.498`, `acc_norm=0.648`, wall 151s)
- mmlu: 12,173 per-example entries across 57 subtasks (wall 567s) — driver patched mid-cycle to handle group-task sample keying
- triviaqa: 500 per-example entries (`exact_match=0.514`, wall 56s)
- total wall: 774s (~12.9 min)

**Mid-cycle fix (MMLU group-task)**: lm-eval emits MMLU samples keyed by `mmlu_<subject>` (57 subtasks), not by `mmlu`. The eval driver was patched to (a) match all keys starting with `task_`, (b) prefix `doc_id` with subtask name (`mmlu_abstract_algebra::0`) for global uniqueness across subtasks. MMLU was re-extracted under the patched driver. The patched driver is the canonical one shipped to the next cycle (LoRA evals will use the same code path).

## 4. Verdict Hexa

`tool/p9_a_prime_verdict.hexa` — Mac-side, raw#9 hexa-style (emits `/tmp/p9_a_prime_verdict_helper.py_tmp` via `_write_helper()`, executes as Python, mirrors the established `anima_r46_verdict_consolidator.hexa` pattern).

**Computes per (ckpt, task)**:
1. Common doc_id set (base ∩ ckpt)
2. Per-example 0/1 correctness arrays (paired)
3. Paired bootstrap: 10,000 resamples → 95% CI on Δ
4. McNemar continuity-corrected (n_discordant ≥ 25) or exact binomial (< 25)
5. Signal classification: STRONG (3/3 criteria), WEAK (2/3), NO (≤1/3)
   - criterion (a): point Δ ≥ task threshold
   - criterion (b): bootstrap 95% CI lower bound > 0
   - criterion (c): McNemar p < 0.05
6. STRONG regression: signal=STRONG with delta ≤ -threshold

**Composite F1_v3** (per A' spec §2.4):
- `CHAT_PASS_v3`: ≥2 of 3 STRONG, no STRONG regression
- `CHAT_PARTIAL_v3`: exactly 1 STRONG
- `CHAT_FAIL_v3`: 0 STRONG OR any STRONG regression

**Pre-registered thresholds** (per A' §2.2):
- hellaswag: acc_norm Δ ≥ 1.0 pt
- mmlu: acc Δ ≥ 0.5 pt
- triviaqa: exact_match Δ ≥ 0.5 pt

**Selftest**: PASS (`hexa run tool/p9_a_prime_verdict.hexa --selftest`).

**Synthetic e2e**: PASS (validated math via `/tmp/p9_verdict_test/` fixtures — n=5 hellaswag with delta=40pt correctly yielded NO signal because McNemar p=0.5 with only 2 discordant pairs and bootstrap CI lower=0).

**Real-base e2e**: PASS — fed real Llama base per-example (500+12173+500 docs) + simulated +2pt LoRA → all 3 tasks classified STRONG; composite CHAT_PASS_v3 (n_strong=3, no regression). Bootstrap CIs: HellaSwag [0.8, 3.4]pt, MMLU [1.75, 2.25]pt, TriviaQA [1.0, 3.2]pt. McNemar p ranged 0.0 (MMLU n=243 discordant) to 0.0019 (HellaSwag n=10 discordant). Math is sound.

## 5. Ranked Recommendation by 완성도 lens

When Path A LoRA ckpts arrive:

| rank | action | 완성도 score | rationale |
|---|---|---|---|
| **1** | Run all 5 ckpts × 3 tasks at limit=500 4-bit (matches base anchor) | 9.0/10 | apples-to-apples Δ; paired stats valid; ~1-3h total wall |
| 2 | Fp16 re-anchor + best-ckpt only at limit=0 (full eval) | 7.5/10 | canonical numbers but breaks 4-bit Δ continuity unless base re-extracted at fp16 too |
| 3 | Subset MMLU (STEM only) | 6.0/10 | ~5x faster but documented honest_c3 needed for variance shift |
| 4 | Limit=2000 (4x base validation limit) | 5.0/10 | tighter CIs but 8x wall; only justified if limit=500 verdict comes back inconclusive |

**Recommendation**: Rank 1 — at limit=500, 4-bit, the full 5-ckpt × 3-task panel runs in ~1-3h end-to-end (5 × ~21min + verdict ~30s). This is the pre-registered config from base validation; deviating now adds honest_c3 burden without bit gain.

## 6. When Path A LoRA Lands — Run Sequence

```bash
# 1. on ubu1: per-ckpt-per-task eval (15 calls, ~1-3h total)
ssh ubu1 'mkdir -p ~/anima/state/p9_a_prime_main_eval_2026_05_03/lora_results'
for STEP in 2000 4000 6000 8000 10000; do
  for TASK in hellaswag mmlu triviaqa; do
    ssh ubu1 "/home/aiden/venv_orchestrator/bin/python \
      ~/anima/state/p9_a_prime_main_eval_2026_05_03/eval_llama_lora_ckpt.py \
      --ckpt-repo need-singularity/p9-llama32-lora-stage1 \
      --ckpt-revision step-${STEP} \
      --task ${TASK} --limit 500 \
      --output ~/anima/state/p9_a_prime_main_eval_2026_05_03/lora_results/step${STEP}_${TASK}.json"
  done
done

# 2. pull results to Mac
mkdir -p state/p9_a_prime_main_eval_2026_05_03_lora_results
scp ubu1:~/anima/state/p9_a_prime_main_eval_2026_05_03/lora_results/*.json \
    state/p9_a_prime_main_eval_2026_05_03_lora_results/

# 3. pull base per-example to Mac
scp ubu1:~/anima/state/p9_a_prime_main_eval_2026_05_03/base_per_example_correctness.json \
    state/p9_a_prime_main_eval_pipeline_2026_05_03/

# 4. compute verdict (Mac, hexa)
hexa run tool/p9_a_prime_verdict.hexa
# emits state/p9_a_prime_main_eval_2026_05_03_verdict.json
```

## 7. Honest C3 (raw#10)

**(a) 4-bit precision differs from canonical fp16** by ~1-3 pt. Per A' decision §6.5, the discriminative-range conclusion is robust but anchor numbers shift. **Mitigation**: pre-extracted base anchor uses identical 4-bit precision as future LoRA evals → Δ remains valid; raw scores carry honest_c3 caveat.

**(b) Synthetic LoRA in smoke test = freshly-init random weights**. Validates wiring only. **Mitigation**: real Path A ckpts will use the identical PeftModel.from_pretrained code path validated in stage 4 of the smoke test.

**(c) Single seed (42)**. lm-eval-harness on MCQA + EM tasks is approximately deterministic per A' §2.5. If downstream observation reveals >0.3pt seed variance, spec amend to 3-seed required (this would require new dated spec doc per §2.6 lock).

**(d) Composite SUCCESS_v3 here is F1_v3 (chat) only.** F2 (φ★), F3 (tension MSE), F4 (BOLD pearson) axis falsifiers were designed against CLM v4 substrate; transferring to Llama+LoRA needs re-anchoring per A' decision §6.2. Out of scope for this verdict hexa; covered by separate Path D track if commissioned.

**(e) Bootstrap+McNemar require identical doc_id sets.** Eval driver uses fixed limit=500 + seed=42; lm-eval picks deterministic doc subset → base + all 5 LoRA ckpts share the same 500 docs per task. Verdict hexa auto-truncates to intersection if mismatch occurs (e.g. driver call with different limit), with `n_common_docs` logged.

**(f) Pod ID divergence.** User brief specifies pod `29dhlqk508ugoc`; state file `state/p9_path_a_llama_lora_2026_05_03/runpod_pod_info.json` records `cp5si6man99s33`. Both are noted in `pipeline_meta.json`. This pipeline does NOT touch either pod; read-only ops only. If user-specified pod is the in-flight one, state file may be stale (pre-restart).

## 8. Files

```
# ubu1 (raw#15: ~/anima/...)
~/anima/state/p9_a_prime_main_eval_2026_05_03/
├── loader_smoketest.py                  # smoke test driver
├── loader_smoketest.json                # smoke result (verdict=PASS)
├── smoketest.log
├── synthetic_lora_smoke/                # roundtrip-verified synthetic adapter
│   ├── adapter_config.json
│   └── adapter_model.safetensors
├── smoke_log_samples/                   # log_samples sanity dir
├── eval_llama_lora_ckpt.py              # main eval driver (READY)
├── extract_base_per_example.sh          # base pre-extract (running)
├── extract_base.log
├── base_per_example_hellaswag.json      # ✓
├── base_per_example_mmlu.json           # (in progress)
├── base_per_example_triviaqa.json       # (queued)
└── base_per_example_correctness.json    # final merged (after extract done)

# Mac local
state/p9_a_prime_main_eval_pipeline_2026_05_03/
├── loader_smoketest.json                # mirror
├── loader_smoketest.py.txt              # mirror
├── eval_llama_lora_ckpt.py.txt          # mirror
├── extract_base_per_example.sh.txt      # mirror
├── pipeline_meta.json                   # ✓
└── base_per_example_correctness.json    # mirror after extract done

tool/p9_a_prime_verdict.hexa             # ✓ (selftest PASS)
state/markers/p9_a_prime_eval_pipeline_landed.marker
docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md  (this file)
```

## 9. Cost / Wall

- **This cycle**: $0 (ubu1 local). Wall ~30 min (smoke test ~20s, base extraction ~7-25 min, hexa selftest <1s).
- **Next cycle (post Path A LoRA arrival)**: $0 ubu1, ~1-3h wall (15 evals × ~5-20 min) + ~30s verdict.

## 10. Constraints Honored

- **raw#9 STRICT**: Mac side = hexa only (`tool/p9_a_prime_verdict.hexa` follows established `anima_r46_verdict_consolidator.hexa` emit-helper pattern); ubu1 side = .py OK (eval driver, smoke test, extractor)
- **raw#15**: ubu1 paths use `~/anima/state/...` not `/Users/ghost/...`
- **raw#10 honest C3**: §7 covers (a)-(f) caveats including 4-bit precision drift, synthetic LoRA limitations, single seed, F1_v3-only scope, doc_id alignment, pod ID divergence
- **$0 design**: no LoRA eval triggered (ckpts not yet trained); base anchor pre-extraction is reuse of existing measurement profile from base validation cycle
- **No pod preempt**: Path A pod `29dhlqk508ugoc` (or `cp5si6man99s33` per state file) NOT touched

---

**End of P9 A' main eval pipeline landed handoff. Pipeline READY. Next BG cycle: when Path A LoRA ckpts publish to `need-singularity/p9-llama32-lora-stage1` Hub repo, run §6 sequence — output is `state/p9_a_prime_main_eval_2026_05_03_verdict.json` with F1_v3 composite per ckpt.**
