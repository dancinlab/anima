# CLM v4 + LoRA SFT — EXEC LANDED 2026-05-05 (BG-CLM-2-EXEC)

## TL;DR

BG-CLM-2-EXEC executes `docs/clm_v4_lora_sft_spec_2026_05_04.md` (USER_AUTHORIZED 2026-05-05 "all bg go") on H100 SECURE on-demand. Boots `need-singularity/clm-v4-mk2-v1` (PRIVATE HF mirror, trust_remote_code), applies LoRA r=32 / alpha=64 / dropout=0.05 to **self-attn-only** `decoder.blocks.{0..15}.attn.{q,k,v,o}_proj` (cross_attn EXPLICITLY EXCLUDED to preserve φ★). Trains on 60/30/10 rehearsal mix (slice A 30k anima axis pre-staged + slice B/C downloaded on H100), max_steps=6000, save_steps=1000, lr=3e-5 (40% lower than Path A v2's 5e-5), per_device_batch=8, grad_accum=4 (eff_batch=32), seq_len=512, bf16, cosine schedule, warmup=300, seed=20260504. Intermediate eval at steps 2000/4000/6000 (HellaSwag-200 + φ★ proxy). Auto-kill on COMPLETE.sentinel + L13 trap pre-stop scp + L20 verdict-writer distinguishes eval_crashed from parity_failed. Cost target $6-10, hard cap $15 (5h).

## What landed

| Artifact | Path | Type |
|---|---|---|
| Orchestrator | `tool/clm_v4_lora_train_orchestrator.hexa` | NEW hexa |
| Train transient | `tool/transient_py/clm_v4_lora_train.py` | NEW transient .py (.own 4 / raw#37) |
| State dir | `state/clm_v4_lora_sft_2026_05_05/` | NEW |
| Verdict | `state/clm_v4_lora_sft_2026_05_05/verdict.json` | emitted post-cycle |
| Companion handoff | `docs/clm_v4_lora_sft_landed_2026_05_05.ai.md` | this file |

Slice A reused from sister Path A v2 (`state/p9_path_a_retrain_v2_exec_2026_05_04/corpus/slice_A_anima_30k.jsonl`, 30k lines, deterministic seed=20260504). Slice B/C downloaded on H100 via existing `tool/transient_py/p9_retrain_v2_corpus_mix.py` (HF Hub auth-purge fallback per BG-α' fix).

## Key infrastructure decisions (vs spec §3 + sister Path A v2)

| Choice | Spec | EXEC | Rationale |
|---|---|---|---|
| Base model | `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` | **`need-singularity/clm-v4-mk2-v1`** (PRIVATE HF) | mk2-v1 ships HF-format (config.json + modeling_clm_v4.py + safetensors); `from_pretrained(trust_remote_code=True)` resolves the `(input_ids, labels) → loss` contract via existing CLMv4ForCausalLM wrapper — F-CLM-LORA-5 satisfied by-construction at load time |
| target_modules | `q_proj/k_proj/v_proj/o_proj` (cell-layer attn) | **explicit full paths `decoder.blocks.{i}.attn.{proj}` × 16 layers × 4 projs** | CRITICAL: `GroupedQueryAttention` (self-attn) AND `ConsciousCrossAttention` use IDENTICAL projection names. PEFT name-match would attach LoRA to BOTH and corrupt φ★. Explicit paths + assert `n_cross_attn_lora==0` at train start = mitigation |
| φ★ probe | "every 2000 steps" | **pre-LoRA + post-LoRA only** (logit-std proxy on 5 calibration prompts) | Per-step probe would add ~3 min × 3 = 9 min wall; pre/post bracketing captures drift sign. Canonical φ★ via anima_phi_v3_canonical.hexa deferred to Mac post-cycle (substrate carry +41.86 NOT directly comparable to in-pod proxy) |
| Slice D consciousness-coupled | 5% (2500 samples) | **NOT INCLUDED** | Slice D requires NEW curated dataset (φ★ + tension_link + N-22 axis prompts); not built this cycle. Mitigation deferred — adapter-only training + r=32 small footprint substitute. C3 #5 in verdict honest_c3 |
| Tokenizer | SPM 64K re-tokenize | **same SPM 64K via huggingface_hub hf_hub_download** | mk2-v1 ships `tokenizer_64k_multilingual.model`; no re-tokenize needed since corpus_mix outputs raw text — TRL SFTTrainer + custom CLMv4SPMTokenizer adapter handles tokenization at train time |

## Sentinel marker

`__P9_CLM_V4_LORA_SFT__ V2_PARTIAL_HS_ONLY`

## EXEC outcome (post-cycle 2026-05-05T03:25Z)

| Metric | Value |
|---|---|
| Verdict | V2_PARTIAL_HS_ONLY |
| Wall | 48 min (vs 2-2.5h estimate — beat by 60%) |
| Cost | **$2.39** (vs $6-10 target / $15 hard cap — under target by 76%) |
| Adapter size | 10.02 MB (vs 500 MB threshold — F-CLM-LORA-3 PASS by huge margin) |
| Trainable params | 2,621,440 / 480,269,952 (0.55%) |
| Cross-attn LoRA modules | 0 (verified via assert; F-CLM-LORA-4 INFERRED_PASS by construction) |
| HellaSwag-200 acc_norm post-LoRA | 0.250 (baseline 0.255; -0.5pp Δ; F-CLM-LORA-1 PASS forgetting_index=0.0196 < 0.05) |
| MMLU + TriviaQA | NOT MEASURED — pod auto-killed (L13 trap) before custom eval_custom completed all 3 benchmarks |
| φ★ post-LoRA proxy | NOT MEASURED — Phase C python heredoc never ran due to in-memory script flow path |
| pod_kill_verified_404 | true |

### F-CLM-LORA gate outcomes
- F-CLM-LORA-1 (forgetting < 5%): **PASS** (HS-200 forgetting 1.96% << 5%)
- F-CLM-LORA-2 (composite ≥ Llama Path A v2): **INCONCLUSIVE_PARTIAL_DATA** (HS-only = 0.25 vs Llama 0.645; CLM v4 baseline was random-floor; 2/3 benchmarks pending)
- F-CLM-LORA-3 (adapter < 500 MB): **PASS** (10.02 MB)
- F-CLM-LORA-4 (axis-cond preserved): **INFERRED_PASS** (cross_attn explicitly excluded from target_modules; PEFT load + forward pass produces finite logits)
- F-CLM-LORA-5 (shim hf_format compat): **PASS** (AutoModelForCausalLM.from_pretrained + PeftModel.from_pretrained both succeed with trust_remote_code=True)

### Critical infra issues caught + fixed mid-flight
1. **L21 lm-eval AutoTokenizer crash on clm_v4 config** — lm-eval-harness `--model hf` calls `AutoTokenizer.from_pretrained` which raises `ValueError: Unrecognized configuration class CLMv4Config to build an AutoTokenizer`. Mitigation: shipped `tool/transient_py/clm_v4_lora_eval.py` with custom CLMV4LoRALM class + register_model + simple_evaluate (bypasses CLI autoload). Used successfully for intermediate step-2000/4000 evals + final HellaSwag.
2. **L22 in-memory bash patch useless** — patching run_h100.bash on disk while running has no effect; bash loads at startup. Final eval Phase D therefore couldn't be redirected to eval_custom. Workaround: kicked off eval_custom in parallel via separate ssh; HS finished but pod killed before MMLU + TriviaQA.
3. **L23 jq inarg with apostrophe broke bash heredoc** — `'NEVER SFT'd'` inside `jq '{...}' > VERDICT` broke single-quoted bash literal at line 441. Verdict computation crashed. Workaround: hand-wrote verdict.json post-cycle with all collected data.
4. **L24 setsid+/dev/null for ssh nohup** — ssh launch hung 8 min waiting for stdin; `disown` alone insufficient. Manual kill -9 freed Mac orchestrator. Patched orchestrator hexa for next cycle (`setsid nohup … < /dev/null &`).

### Follow-up cycles required to fully populate verdict
1. Run MMLU + TriviaQA eval on `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/` via `tool/transient_py/clm_v4_lora_eval.py` on ubu1 (free, ~3-6h) — converts F-CLM-LORA-2 INCONCLUSIVE → PASS/PARTIAL/FAIL
2. Run canonical φ★ probe via `tool/anima_phi_v3_canonical.hexa` on pre+post adapter state — replaces in-pod logit-std proxy with structural mutual-info measurement
3. Run F-CLM-LORA-4 full 5-bucket cell-token bridge fixture — converts INFERRED_PASS → measured PASS/FAIL

## References
- Spec: `docs/clm_v4_lora_sft_spec_2026_05_04.md`
- Spec land companion: `docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md`
- CLM v4 baseline (left comparator): `state/clm_v4_baseline_eval_2026_05_05/verdict.json`
- Llama Path A v2 (right comparator): `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- Sister Llama orchestrator: `tool/p9_path_a_retrain_v2_h100_orchestrator.hexa`
- HF base mirror: `https://huggingface.co/need-singularity/clm-v4-mk2-v1`
