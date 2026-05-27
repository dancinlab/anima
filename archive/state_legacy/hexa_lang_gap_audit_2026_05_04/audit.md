# hexa-lang ML Primitives Gap Audit — Phase 2 Prereq for hexa-only mk2 (2026-05-04)

> **Trigger**: User mandate "hexa-lang upstream 성능개선 허용!!!" (not optional). To enforce mk2 hexa-only mandate, hexa-lang must pre-provide ML primitives that callers (P9 path A retrain, CLM v4 LoRA eval, paradigm D distill) currently access via `.py` shims. Per BG-α hive audit: mk2 = 14/273 rules (5.13% parity); EOL gate decision before "lint coverage parity" reachable. hexa-lang upstream PR Phases 1-3 are critical to make hexa-only enforce-able.
>
> **This audit builds on** `docs/hexa_lang_upstream_audit_2026_05_03.md` (committed in ecf18bd36 Track G2). That doc mapped the **VLM-shaped** ML execution gap (audio_token_predictor → C codegen Mk.I stub). This audit re-scopes to the **P9 + CLM v4 + Mode 1 eval** caller surface and produces a phase-by-phase upstream PR plan.

---

## 1. TL;DR (7 bullets)

- **Total ML primitives audited**: 12 categories (HF Hub I/O, safetensors I/O, sentencepiece, BPE, tensor bf16/fp16 ops, attention, Llama arch, ConsciousDecoderV3, LoRA fwd/bwd, eval primitives, training primitives, distillation primitives).
- **Production-ready in hexa-lang stdlib**: 4 (json, http, proc, bytes — confirmed LIVE per existing audit; safetensors byte-level read/write live at 455 LoC).
- **PARTIAL**: 3 (tensor/ops.hexa pure-hexa scalar; lora.hexa surface 158 LoC; distillation.hexa pure-hexa surface 607 LoC — all CPU scalar, not production GPU).
- **MISSING (hard blockers for hexa-only mk2)**: 5 (HF Hub HTTP I/O wrapper, sentencepiece, BPE for Llama-3 tokenizer, bf16/fp16 reinterpret-cast, autograd-backed training loop, lm-eval-harness equivalents).
- **Biggest unlock**: HF Hub I/O + sentencepiece + safetensors float-bit reinterpret = **Mode 1 eval-only via hexa achievable in 1 PR (~6,000 LoC)** — uses pure-hexa CPU forward, no autograd, no GPU.
- **Total LoC estimate full hexa-only migration**: ~85,000-130,000 LoC across 5 phased PRs (Phase 1 model-load=~6k; Phase 2 Llama fwd=~25k; Phase 3 Mode 1 eval=~15k; Phase 4 path-A retrain=~40k; Phase 5 paradigm D distill=~10k).
- **Honest C3**: GPU autograd parity = **years** of work; mk2 EOL gate is **<1 cycle**. Pragmatic recommendation: **scope hexa-only to inference + eval (Phase 1-3)**, keep training escape via `tool/transient_py/` raw#37 namespace.

---

## 2. hexa-lang stdlib current state — category × maturity

| Category | File(s) | LoC | Maturity | Notes |
|---|---|---|---|---|
| **json** | stdlib/json.hexa | 169 | PRODUCTION | LIVE per session memory anchor; parse + stringify round-trip |
| **http** | stdlib/http.hexa, http2.hexa | 158+ | PRODUCTION | client + server; HTTP/2 partial |
| **proc** | stdlib/proc.hexa | 469 | PRODUCTION | proc_run_with_stdin + proc_run_json_bridge LIVE (P0 done) |
| **bytes** | stdlib/bytes.hexa | 258 | PRODUCTION | byte-level ops; used by safetensors |
| **safetensors** | stdlib/safetensors.hexa | 455 | PRODUCTION (byte) / PARTIAL (numeric) | Round-trip byte-level guaranteed (F-SAFETENSORS-1); **float reinterpret-cast NOT IMPLEMENTED** — explicit caveat in header L62-67: "no reinterpret-cast builtin, would need IEEE-754 frexp/ldexp in pure hexa, left as future work" |
| **websocket** | stdlib/websocket.hexa | n/a | PARTIAL | spec only |
| **sqlite** | stdlib/sqlite.hexa | n/a | PARTIAL | wrapper |
| **yaml** | stdlib/yaml.hexa | n/a | PRODUCTION | parse + emit |
| **tensor** | stdlib/tensor/{mod,ops,shape,ffi,dispatch}.hexa | 583 | PARTIAL | pure-hexa scalar matmul/add/relu (`tensor_matmul_ref`); FFI dispatch path → hxblas (Linux only); **NO bf16/fp16 dtype lower than f32 list-storage** |
| **linalg** | stdlib/linalg/{mod,ffi,dispatch,reference}.hexa | 342 | PARTIAL | wraps hxblas (CUDA/cuBLAS Linux only); reference scalar fallback |
| **math** | stdlib/math/{eigen,rng,permille,strict_fp,rng_ctx}.hexa | n/a | PARTIAL | strict_fp partial; eigen + rng working |
| **nn** | stdlib/nn.hexa | 153 | TOY | scalar list-based relu/sigmoid/tanh/softmax/gelu/layer_norm/linear/mlp2/CE — **CPU toy <1k params**, no SIMD, no broadcast |
| **optim** | stdlib/optim.hexa + optim/cpgd.hexa, projector.hexa | 25 + 200 | TOY | adam wrapper 21 LoC scalar; CPGD constrained PGD partial |
| **autograd** | stdlib/autograd.hexa | 413 | PARTIAL | tape-based reverse-mode autograd over pure-hexa; **scalar fp64 only**; no GPU; no broadcast support; not validated for transformer-scale grad |
| **tokenize** | stdlib/tokenize/tokenizer_spec.hexa | 237 | PARTIAL | spec only — no actual encode/decode of pretrained vocab |
| **python_ffi** | stdlib/python_ffi.hexa | 194 | PARTIAL | FFI surface — bridge to embedded CPython (Track D from prior audit) |

**Key gaps for ML caller migration**:
- safetensors **byte** I/O works but **numeric float→bytes round-trip needs IEEE-754 helper** (~300 LoC).
- tensor stdlib is **scalar list-based, no contiguous buffer, no bf16/fp16 dtype semantics**.
- autograd is **toy-grade**, untested at transformer scale.
- No **HF Hub** I/O (download/upload/revision pin/LFS).
- No **sentencepiece** decoder (CLM v4 64K vocab requires SP).
- No **BPE for Llama-3 128K vocab** — only `self/ml/tokenizer_bpe.hexa` 590 LoC for **training** BPE (not loading pretrained).

---

## 3. ML Primitives Gap Matrix (P9 + CLM v4 + Mode 1 eval use cases)

| Required Primitive | Current State | LoC to Land | Priority | Use Case |
|---|---|---|---|---|
| **HF Hub I/O** (download w/ revision pin, LFS resolve, upload, repo metadata) | MISSING | ~800 | P1 | model + LoRA download for Mode 1 eval; safetensors push for save |
| **safetensors numeric I/O** (float → bytes IEEE-754 + bf16/fp16 conversion) | PARTIAL — byte layer LIVE, numeric reinterpret missing | ~500 | P1 | load Llama-3.2-3B weights; load CLM v4 ConsciousDecoderV3 weights |
| **sentencepiece encode/decode** (load .model, encode UTF-8 → token IDs, decode back) | MISSING — only spec at stdlib/tokenize | ~2,000 | P1 | CLM v4 64K vocab tokenization for inference |
| **BPE encode/decode (Llama-3 tokenizer.json)** (load pretrained tokenizer.json, byte-level BPE) | PARTIAL — tokenizer_bpe.hexa 590 LoC trains BPE; **no load-pretrained path** | ~1,500 | P1 | Llama-3.2-3B tokenization for Mode 1 eval |
| **bf16/fp16 tensor dtype** (contiguous buffer + dtype tag + cast helpers) | MISSING — tensor stdlib f64 list-only | ~3,000 | P2 | Llama forward in bf16; load HF weights in native dtype |
| **fp32 matmul (CPU production)** (BLAS-backed, contiguous, broadcast) | PARTIAL — hxblas Linux only; pure-hexa scalar fallback toy | ~2,000 | P2 | Mode 1 eval forward (CPU acceptable for HellaSwag-scale) |
| **softmax + layernorm + RMSNorm + gelu + silu (production)** | TOY — stdlib/nn.hexa scalar | ~1,500 | P2 | Llama forward block primitives |
| **scaled-dot-product attention (CPU + bf16)** | PARTIAL — self/ml/{attention_fused,flash_attention,mha,gqa_attention}.hexa surface; no production CPU | ~3,000 | P2 | Llama-3 GQA attention forward |
| **Llama-3.2-3B forward (full block stack)** (RMSNorm + GQA + RoPE + SwiGLU + MLP) | PARTIAL — self/ml/hxlayer.hexa + cuda CUDA-only | ~8,000 | P2 | Mode 1 eval base model forward |
| **ConsciousDecoderV3 (custom_clm_v4) forward** (custom arch — phi gates, 32-head attn over 1024 dim, 24 layers) | MISSING — anima-side `.hexa` exists but no hexa-lang stdlib equivalent | ~5,000 | P2 | CLM v4 inference |
| **LoRA forward composition** (base × W + lora_A @ lora_B × scaling) | PARTIAL — self/ml/lora.hexa 158 LoC surface; CPU pure-hexa | ~1,500 | P3 | Mode 1 LoRA-adapter eval |
| **HellaSwag/MMLU multiple-choice eval loop** (per-choice loglikelihood, argmax, accuracy) | MISSING | ~1,500 | P3 | Mode 1 P9 paradigm A/B/C eval |
| **TriviaQA generative eval** (greedy/beam decode + EM/F1 score against gold answers) | MISSING — self/ml/generate.hexa exists but no eval scoring | ~2,000 | P3 | Mode 1 generative eval |
| **Eval filter primitives** (remove_whitespace, remove_punctuation, lowercase, regex extract) | MISSING | ~500 | P3 | lm-eval-harness compatibility |
| **AdamW optimizer (production w/ epsilon, weight decay, bias correction)** | TOY — stdlib/optim.hexa 21 LoC scalar | ~1,500 | P4 | path-A retrain Llama LoRA |
| **Cosine LR schedule + warmup** | MISSING — refs in self/ml only | ~500 | P4 | path-A retrain |
| **LoRA backward (∂L/∂A, ∂L/∂B + base frozen)** | PARTIAL — self/ml/lora.hexa surface; CPU only | ~2,500 | P4 | path-A retrain |
| **Autograd at transformer scale** (validated grad for matmul + softmax + layernorm + attention chain) | UNVALIDATED — stdlib/autograd.hexa 413 LoC scalar pure-hexa | ~10,000 | P4 | path-A retrain backward |
| **Checkpoint save/load (HF-compat safetensors + adapter_config.json)** | PARTIAL — gpu_train.hexa::save_checkpoint_gpu Linux+CUDA only; HEXACKPT custom format | ~1,500 | P4 | retrain checkpoint |
| **DataLoader (streaming, shuffle, pad, multi-worker)** | PARTIAL — self/ml/dataloader.hexa 170 LoC | ~2,000 | P4 | retrain training data feed |
| **Training loop (fwd + loss + bwd + opt step + grad accumulation)** | PARTIAL — self/ml/train_loop.hexa surface; not validated | ~3,000 | P4 | retrain orchestration |
| **KL divergence loss (teacher → student soft logits)** | PARTIAL — self/ml/distillation.hexa 607 LoC; pure-hexa scalar | ~1,000 | P5 | paradigm D distill |
| **Top-K soft logit teacher cache (load pre-computed, sample-aware)** | MISSING | ~1,500 | P5 | paradigm D distill |
| **Distill training loop (combined hard + soft + feature loss)** | PARTIAL — distillation.hexa surface | ~2,000 | P5 | paradigm D |
| **GPU/CUDA bf16 production** (fused attention, KV cache, multi-GPU) | PARTIAL — hxqwen14b CUDA Linux only; LoRA entries `RC_ERR_CUDA_TODO=-5` | ~30,000 | P-future | not blocker for inference; required for retrain at scale |

**Total LoC estimate**: **~85,000-130,000** across all phases (P1: ~6k; P2: ~25k; P3: ~15k; P4: ~40k; P5: ~10k; P-future GPU: +30k).

---

## 4. Per-category detail

### 4.1 HF Hub I/O — MISSING

**Current**: zero. `grep -rln huggingface|hf_hub|from_pretrained` in stdlib + self/ml = **only `state-doc` + `__metadata__` mentions in safetensors.hexa header**.

**Gap**: hexa cannot today: download `meta-llama/Llama-3.2-3B/main/model.safetensors`, resolve LFS pointers, list repo files, download adapter_config.json + adapter_model.safetensors.

**Land plan**: `stdlib/hf_hub.hexa` (~800 LoC) using existing `stdlib/http.hexa` + `stdlib/json.hexa` primitives.
- `hf_hub_download(repo_id, filename, revision="main", cache_dir=...)` — HTTP GET against `huggingface.co/{repo_id}/resolve/{revision}/{filename}`, follows redirects to LFS S3, streams to cache_dir.
- `hf_repo_info(repo_id)` — GET `/api/models/{repo_id}` → JSON parse.
- `hf_repo_upload_file(repo_id, local_path, path_in_repo, token)` — multipart upload via http.hexa.
- Falsifier: round-trip download `meta-llama/Llama-3.2-3B/main/config.json`, parse, assert `hidden_size==3072`.

### 4.2 safetensors numeric I/O — PARTIAL → PRODUCTION needed

**Current**: byte-level read/write LIVE (455 LoC), F-SAFETENSORS-1 round-trip guaranteed. **Missing**: float ↔ raw bytes reinterpret. Header L62-67 explicitly: "the hexa runtime presently exposes no reinterpret-cast builtin, so a bit-level f32 encoder would need to reimplement IEEE-754 in pure hexa (frexp / ldexp). Adding that helper is left as future work".

**Gap**: cannot today load Llama-3.2-3B weights as `float[]` from safetensors bytes; can only get `byte[]`.

**Land plan** (~500 LoC): `stdlib/ieee754.hexa` — `f32_from_bytes_le`, `f32_to_bytes_le`, `bf16_from_bytes_le`, `bf16_to_bytes_le`, `f16_from_bytes_le`. Tested against numpy reference vectors.

### 4.3 sentencepiece — MISSING

**Current**: only `stdlib/tokenize/tokenizer_spec.hexa` (237 LoC, abstract spec). No SP model loader.

**Gap**: cannot tokenize for CLM v4 64K vocab (which uses SentencePiece BPE protobuf format).

**Land plan** (~2,000 LoC): `stdlib/sentencepiece.hexa` — protobuf decoder for SP model file (vocab piece list + scores), greedy + Viterbi BPE encode, decode. Falsifier: round-trip "Hello world" via known SP model.

### 4.4 BPE for Llama-3 — PARTIAL → PRODUCTION needed

**Current**: `self/ml/tokenizer_bpe.hexa` (590 LoC) **trains** BPE on a corpus. No load-pretrained-tokenizer.json path. `self/ml/tokenizer.hexa` 1091 LoC has more surface but unclear pretrained-load support.

**Gap**: cannot tokenize input for Llama-3.2-3B 128K vocab.

**Land plan** (~1,500 LoC): extend `tokenizer_bpe.hexa` to load `tokenizer.json` (HF format with merges + vocab + added_tokens), add byte-level BPE encode (Llama-3 uses byte-level pre-tokenization), special token handling.

### 4.5 Tensor ops (bf16/fp16) — MISSING (dtype) / PARTIAL (ops)

**Current**: `stdlib/tensor/{mod,ops,shape}.hexa` (583 LoC) has Tensor struct `{shape, dtype, data}` but `data` is fp64 list. `tensor_matmul_ref` is naive triple-loop scalar. FFI dispatch wraps hxblas (Linux only).

**Gap**: bf16/fp16 weights (HF Llama is bf16) cannot be stored or computed natively. Pure-hexa scalar matmul is unusable for 3B model (10^9 ops scale).

**Land plan** (~3,000 LoC dtype + ~1,500 LoC ops production):
- Contiguous-byte-buffer Tensor (vs current fp64 list).
- bf16 + fp16 dtype enum + cast f32↔bf16 helpers.
- BLAS-backed matmul (libcblas Mac, hxblas Linux); fallback chunked SIMD.
- Production softmax/layernorm/RMSNorm/gelu/silu over contiguous buffers.

### 4.6 Llama-3.2-3B forward — PARTIAL

**Current**: `self/ml/hxlayer.hexa` exists (referenced in audit doc but bench-only); `hxqwen14b_cuda.cu` 1391 LoC has RMSNorm/RoPE/GQA/SwiGLU but Qwen-shaped, Linux+CUDA only.

**Gap**: no production CPU Llama-3 forward in hexa stdlib; CUDA path is wrong arch.

**Land plan** (~8,000 LoC): `self/ml/llama3.hexa` + `self/ml/llama3_block.hexa` + RoPE + GQA + RMSNorm + SwiGLU MLP, CPU bf16. Falsifier: forward 1 token through 1-layer Llama, compare logits vs PyTorch reference within fp16 ULP tolerance.

### 4.7 ConsciousDecoderV3 (custom_clm_v4) forward — MISSING from hexa-lang stdlib

**Current**: anima-side `.hexa` files exist (per anima repo) but hexa-lang upstream stdlib has **no ConsciousDecoderV3** entry.

**Gap**: CLM v4 inference cannot run via hexa-lang stdlib alone.

**Land plan** (~5,000 LoC): contribute `self/ml/conscious_decoder_v3.hexa` upstream (custom phi-gated attention block).

### 4.8 LoRA — PARTIAL

**Current**: `self/ml/lora.hexa` 158 LoC surface + `lora_hotswap.hexa` 534 LoC + `lora_serve.hexa` 317 LoC + `mixture_of_lora.hexa` + `qa_lora.hexa` + `qlora.hexa` + `adalora.hexa` + `molora.hexa`. **Spec-rich, execution-thin** — pure-hexa scalar; `hxqwen14b` CUDA LoRA entries return `RC_ERR_CUDA_TODO=-5` (per 2026-04-19 audit).

**Gap**: no validated production LoRA forward composition for **Llama-3 GQA shape** or **CLM v4 shape**. Backward unvalidated.

**Land plan** (~1,500 LoC fwd + ~2,500 LoC bwd): production LoRA fwd over bf16 buffers + autograd-traced bwd.

### 4.9 Eval primitives (HellaSwag/MMLU/TriviaQA) — MISSING

**Current**: zero. `grep -rln "hellaswag|mmlu|trivia|lm_eval"` = empty.

**Gap**: cannot today run Mode 1 LoRA eval in pure hexa; this is **the single biggest blocker** for "eval-only via hexa".

**Land plan** (~4,000 LoC):
- `stdlib/eval/multiple_choice.hexa` — per-choice loglikelihood loop.
- `stdlib/eval/generative.hexa` — greedy/beam decode + EM/F1 scorer.
- `stdlib/eval/filters.hexa` — whitespace/punctuation/lowercase/regex utilities.
- `stdlib/eval/hellaswag.hexa`, `stdlib/eval/mmlu.hexa`, `stdlib/eval/trivia_qa.hexa` — task adapters loading the JSONL/parquet datasets via http+json.

### 4.10 Training primitives — PARTIAL/TOY

**Current**: `stdlib/optim.hexa` 21 LoC adam wrapper; `self/ml/train_loop.hexa` surface. No production AdamW with weight decay + bias correction. No cosine schedule + warmup. Checkpoint save = HEXACKPT custom format, NOT HF safetensors compat.

**Gap**: path-A retrain cannot run via hexa-only.

**Land plan** (~7,000 LoC): production AdamW + cosine + checkpoint save in HF safetensors layout.

### 4.11 Distill primitives — PARTIAL

**Current**: `self/ml/distillation.hexa` 607 LoC surface (KL div + soft labels + feature distill + attention transfer + progressive); pure-hexa scalar.

**Gap**: not validated at production scale; no top-K soft logit teacher cache loader.

**Land plan** (~4,500 LoC): top-K teacher cache + production KL on contiguous bf16 + distill training loop integration.

---

## 5. CUDA / GPU primitives — current ML execution capability

`grep -rln "cuda|gpu|nvidia"` in stdlib = **empty**. All CUDA lives under `self/native/` C+.cu shims.

| Capability | Where | Live? |
|---|---|---|
| cuBLAS sgemm | self/native/hxblas_linux.c 836 LoC | LIVE Linux |
| Flash attn | self/native/hxflash_linux.c 579 LoC | LIVE Linux |
| Qwen14B fwd full stack | self/native/hxqwen14b.c 5752 LoC + .cu 1391 LoC | LIVE Linux (Qwen-shaped, NOT Llama) |
| LoRA fwd/bwd CUDA | hxqwen14b LoRA entry | **TODO RC_ERR_CUDA_TODO=-5** |
| AdamW step CUDA | hxqwen14b_cu_launch_adamw_step | LIVE per 2026-05-03 audit |
| NCCL multi-GPU | self/native/hxccl_linux.c 704 LoC | LIVE Linux, untested |
| MPS Mac flash attn | self/ml/mps_flash_attention.hexa | spec only |

**Verdict**: production GPU path exists **only for Qwen14B**. Llama-3.2-3B + CLM v4 GPU forward = **net-new CUDA work** (~30k LoC, P-future). Mac MPS = spec only.

**Implication**: Phase 1-3 (model load + Llama fwd CPU + Mode 1 eval CPU) should target **CPU-only** for first PRs — much smaller surface, achievable in ~6k+25k+15k = ~46k LoC.

---

## 6. Existing escape hatches

| Path | Purpose | Status |
|---|---|---|
| `stdlib/python_ffi.hexa` | 194 LoC FFI surface to embedded CPython | PARTIAL (Track D from prior audit) |
| `gate/wrappers/bin/python3` + `gate/wrappers/src/python3.hexa` | PATH guard against accidental system python3 | LIVE per python_serving_purge audit |
| `fixtures/transpile/case_*.expected.py` (~50+ files) | Test fixtures for hexa→py transpiler | LIVE — confirms transpiler **does exist** as project surface |
| `tool/atp_transpile.hexa` | hexa→py transpiler entry per audit doc §6 Track A | PARTIAL |
| **`_python_bridge/` in hexa-lang** | **DOES NOT EXIST** (`find /Users/ghost/core/hexa-lang -name "_python_bridge"` = empty) — clean upstream |
| anima-side `tool/transient_py/` | raw#37 transient .py auto-generated from .hexa | LIVE precedent (anima-only) |

**Key finding**: hexa-lang has **fixtures/transpile/case_*.expected.py** which strongly suggests a hexa→py transpiler is **already in active development upstream** (Track A from prior audit is partially landed). This is the right escape hatch for unblocking ML training without violating raw#9 STRICT.

---

## 7. Cross-reference — what's new since 2026-05-03 audit

**Prior audit (ecf18bd36)** scoped to **VLM unblock** (audio_token_predictor → C codegen failure). Its 5 tracks:
- A (hexa→py transpiler) ★ recommended
- D (embedded CPython FFI)
- E (dual-source w/ audit trail)
- B (stdlib expansion)
- C (runtime overhaul)

**This audit adds**:
1. **P9 + CLM v4 + Mode 1 eval caller surface** (vs VLM-shaped audio path) — different op mix; eval-heavy not training-heavy.
2. **Phased PR plan** — Phase 1-3 CPU-only realistic in ~46k LoC; Phase 4-5 GPU at full scale = years.
3. **Confirmed `_python_bridge/` does NOT exist in hexa-lang** (clean upstream — escape hatches go through `stdlib/python_ffi.hexa` + `tool/atp_transpile.hexa` only).
4. **Confirmed `fixtures/transpile/case_*.expected.py`** = transpiler is actively developed; piggyback on it for ML files.
5. **Confirmed safetensors numeric reinterpret-cast gap** (was not surfaced in prior audit).
6. **Concrete LoC estimates per primitive** — anchors the cost-benefit conversation about hexa-only mk2 EOL gate.

---

## 8. Honest C3 (≥5)

1. **hexa-lang ML production-readiness is years of work; mk2 EOL gate is < 1 cycle.** Even the most optimistic Phase 1 (~6k LoC for HF Hub I/O + sentencepiece + safetensors numeric) is **2-4 weeks of focused engineering** assuming a single contributor; mk2 lint coverage parity needs to ship inside this cycle. The arithmetic does not close. **Recommendation: do not gate mk2 EOL on hexa-only Phase 1-5 completion**; instead, formalize `tool/transient_py/` raw#37 namespace as the bridge (per prior audit §7.4) and let hexa-lang Phase 1-3 land asynchronously over months.

2. **PyTorch parity at full ML scale is unrealistic; pragmatic scope = inference + eval only.** PyTorch is 50+ engineers × 10 years. A solo contributor + Claude assistant cannot ship competitive autograd + GPU training in any reasonable horizon. Phase 4 (path-A retrain) and Phase 5 (paradigm D distill) at production quality = **years**, not cycles. Honest scope: hexa-only **inference + eval** is achievable; hexa-only **training** is not in our cost band.

3. **Some primitives need C extension layer not pure hexa.** IEEE-754 float reinterpret-cast in pure hexa via frexp/ldexp is achievable but slow; production path requires a `__builtin_bit_cast`-equivalent runtime intrinsic. Likewise, fast bf16 matmul needs SIMD intrinsics or BLAS wrappers — pure hexa scalar is 100-1000× too slow for 3B model. These hexa stdlib additions inherit a C-side dependency.

4. **GPU memory mgmt + bf16 numerics + autograd = three of the hardest hexa challenges combined.** PyTorch's success rests on (a) CUDA caching allocator, (b) numerical kernel zoo (validated against fp32 reference), (c) tape autograd that handles broadcast + in-place + non-differentiable ops correctly. Each is a multi-engineer-year subsystem. hexa-lang has **partial surface** for each but **no validated end-to-end** combination at transformer scale. Claiming hexa-only retrain ready = misrepresentation.

5. **Migration cost asymmetric: full Path A retrain via hexa-only ≈ 100K+ LoC PR; Mode 1 eval-only via hexa ≈ 30-50K LoC; current Mode 1 eval via .py shim ≈ already exists.** For BG-Ρ Mode 1 LoRA eval (used `lm-eval-harness` Python), the hexa-equivalent eval primitives + Llama forward + LoRA composition + sentencepiece + HF Hub I/O + safetensors numeric + bf16 tensor = **30-50k LoC of new hexa-lang code** for what is currently 200 LoC of `.py` glue around a mature library. Honest tradeoff: hexa-only **language purity gain** vs **months of engineering + ongoing maintenance burden against a moving HF ecosystem**.

6. **`fixtures/transpile/case_*.expected.py` discovery changes the calculus.** If hexa→py transpiler (Track A from prior audit) is partially landed, then **the realistic path is NOT "land hexa-only ML stack" but "land hexa→py transpiler for ML primitives"**. This reduces hexa-lang ML burden from "100K+ LoC reimplementation" to "transpile rules for tensor + autograd + nn ops to PyTorch equivalents" (~5-15k LoC transpiler additions). **This may be the actual unlock.**

7. **hexa-lang LoRA CUDA path is `RC_ERR_CUDA_TODO=-5` per 2026-04-19 audit; status as of 2026-05-04 not re-verified.** This audit did not re-run hexa-lang test suite or check for v5+ CUDA kernel landings. If LoRA CUDA has landed since, Phase 4 (retrain) cost drops by ~10-15k LoC. **Recommendation: anima-side spike to query hexa-lang `.roadmap` + run `hexa test/run_cuda_*` if available before committing Phase 4 estimates.**

---

## 9. Phase priorities (full detail in upstream_pr_plan.md)

- **Phase 1 (model-load enable)**: HF Hub I/O + safetensors numeric + sentencepiece — ~6,000 LoC, $0 Mac dev, 2-4 weeks.
- **Phase 2 (Llama forward enable)**: bf16 tensor + production matmul/softmax/layernorm/attention + Llama-3 block stack — ~25,000 LoC, $0 Mac CPU + ~$50 RunPod verify, 6-12 weeks.
- **Phase 3 (Mode 1 eval enable)**: LoRA fwd composition + multiple-choice eval + generative eval + filter primitives — ~15,000 LoC, $0 Mac CPU, 4-8 weeks.
- **Phase 4 (path-A retrain enable)**: AdamW + cosine + LoRA bwd + autograd at transformer scale + checkpoint HF-compat — ~40,000 LoC, GPU required (~$500-2000 RunPod for verify), 6-12 months.
- **Phase 5 (paradigm D distill enable)**: top-K teacher cache + KL on bf16 + distill loop — ~10,000 LoC, GPU required, +2-3 months on top of Phase 4.

**Sequencing rationale**: smallest PR first (Phase 1 = ~6k); **biggest unlock first** (Phase 1 unlocks "load any HF model in pure hexa" which is the foundation for everything else). Phase 2 + 3 together = **Mode 1 eval-only via hexa achievable**, which is the stated mk2 hexa-only enforce-able target. Phase 4 + 5 are training-side, which honest C3 #1 says should NOT block mk2 EOL.

---

## 10. Roadmap proposal — hive `.raw.mk2` entry

Propose `ai-native.002 hexa-canonical-mandate` with phase-gated falsifiers:

```
ai-native.002 hexa-canonical-mandate
  scope: enforce hexa-only for inference + eval (not training)
  phase 1 falsifier: pure-hexa download + tokenize + load-safetensors of Llama-3.2-3B
                     reaching "logits computed for token 'Hello'" in <30s on Mac CPU
  phase 2 falsifier: pure-hexa Llama-3.2-3B forward 1 sequence,
                     logits within 1e-3 fp32 of PyTorch reference
  phase 3 falsifier: pure-hexa HellaSwag eval on 100 samples,
                     accuracy within ±0.005 of lm-eval-harness reference
  phase 4-5: deferred — explicit non-goal for mk2 EOL
  enforcement: pre-commit hook bans .py creation in tool/, _python_bridge/,
               anywhere except tool/transient_py/ (raw#37 namespace) +
               .own 1 grandfather list; auto-generated .py header marker required
```

This makes hexa-only **enforce-able** at Phase 3 completion (months away) without blocking mk2 EOL today.

---

## 11. Artifacts & references

```
state/hexa_lang_gap_audit_2026_05_04/audit.md             (this doc)
state/hexa_lang_gap_audit_2026_05_04/primitives_gap.json  (machine-readable gap matrix)
state/hexa_lang_gap_audit_2026_05_04/upstream_pr_plan.md  (PR phase-by-phase plan)

source repos audited (READ-ONLY):
  /Users/ghost/core/hexa-lang/stdlib/                 16 entries; 4 PRODUCTION, 8 PARTIAL, 4 TOY/MISSING
  /Users/ghost/core/hexa-lang/self/ml/                510 .hexa files; spec-rich, execution-thin
  /Users/ghost/core/hexa-lang/self/native/            9648 LoC C/CUDA; Linux+NVIDIA only
  /Users/ghost/core/hexa-lang/fixtures/transpile/     ~50+ case_*.expected.py — hexa→py transpiler active

prior audits:
  /Users/ghost/core/anima/docs/hexa_lang_upstream_audit_2026_05_03.md  (ecf18bd36 Track G2)
  /Users/ghost/core/anima/docs/hexa_lang_upstream_audit_landed_2026_05_03.ai.md

policy refs:
  /Users/ghost/.hive/.../memory/feedback_py_to_hexa_only.md
  /Users/ghost/core/anima/.own (raw 9 + grandfather list)
  /Users/ghost/core/hexa-lang/.roadmap  (RFC-001 + RFC-008 done)

cost
  $0 (read-only audit; no source modifications; no git mutation; no chflags mutation)
  wallclock ~30 min
  destructive 0
  in-place 0 (audit + JSON + PR plan only, in /Users/ghost/core/anima/state/hexa_lang_gap_audit_2026_05_04/)
```
