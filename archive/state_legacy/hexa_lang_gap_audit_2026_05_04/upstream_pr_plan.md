# hexa-lang Upstream PR Plan — Phased Roadmap for hexa-only mk2 (2026-05-04)

> **Companion to** `audit.md` + `primitives_gap.json`. This doc sequences the upstream PRs into 5 phases, each with falsifier set + cost band + dependency graph + acceptance criteria.
>
> **Mandate**: User explicit "hexa-lang upstream 성능개선 허용!!!" (not optional). Phases 1-3 in scope for mk2 hexa-only enforce-ability; Phases 4-5 explicit non-goal for mk2 EOL gate (per audit.md §8 honest C3 #1).

---

## Sequencing rationale

1. **Smallest PR first** — Phase 1 (~6,300 LoC) lands fastest, reduces risk of stalled multi-phase commitment.
2. **Biggest unlock first** — Phase 1 unlocks "load any HF model + tokenize" which is the foundation under everything else (Phases 2-5 all depend on Phase 1 primitives).
3. **CPU-only first, GPU last** — Phases 1-3 target Mac CPU (zero infra cost, fast iteration). Phase 4-5 require GPU verification (RunPod), pushed to async/future.
4. **Inference-first, training-last** — inference path (Phases 1-3) has smaller surface than training (Phases 4-5: autograd + AdamW + checkpoint + dataloader + training loop). Honest C3: training at parity with PyTorch = years.
5. **Eval before retrain** — Phase 3 (Mode 1 eval) depends only on Phase 1-2 (model load + forward). Path-A retrain (Phase 4) requires autograd which is multi-month risk.

---

## Phase 1 PR — Model Load Enable

### Files
- `hexa-lang/stdlib/hf_hub.hexa` (NEW, ~800 LoC) — HuggingFace Hub HTTP I/O (download w/ revision pin, LFS resolve, upload, repo metadata).
- `hexa-lang/stdlib/ieee754.hexa` (NEW, ~500 LoC) — IEEE-754 float ↔ bytes reinterpret (f32, f16, bf16) — closes the explicit gap from `stdlib/safetensors.hexa` L62-67.
- `hexa-lang/stdlib/sentencepiece.hexa` (NEW, ~2,000 LoC) — SP protobuf decoder + greedy/Viterbi BPE encode + decode.
- `hexa-lang/self/ml/tokenizer_bpe.hexa` (EXTEND ~+1,500 LoC over existing 590) — load pretrained tokenizer.json (HF format with merges + vocab + added_tokens), byte-level BPE encode for Llama-3.
- `hexa-lang/stdlib/safetensors.hexa` (PATCH, ~+200 LoC) — wire ieee754 helpers into existing byte-level reader; add convenience `safetensors_read_typed(path) -> map<string, typed_tensor>` returning float arrays not byte arrays.
- `hexa-lang/test/t_phase1_*.hexa` (NEW, ~1,000 LoC) — Phase 1 falsifier suite.

### LoC estimate
- New: ~5,300 LoC
- Extension: ~1,000 LoC
- Tests: ~1,000 LoC
- **Total: ~6,300 LoC + tests**

### Falsifier set
1. `t_hf_hub_download_round_trip.hexa` — `hf_hub_download("meta-llama/Llama-3.2-3B", "config.json", revision="main")` succeeds; `json_parse(content)["hidden_size"] == 3072`.
2. `t_ieee754_round_trip.hexa` — for 1000 random f32 values: `f32_from_bytes_le(f32_to_bytes_le(x)) == x` to 0 ULP; bf16 to within 1 ULP after canonical truncation.
3. `t_safetensors_typed_load.hexa` — load Llama-3.2-3B `model-00001-of-00002.safetensors`, assert tensor count > 0, assert dtype == "BF16" for first weight, assert numeric values agree with numpy reference vectors within 0 ULP for f32 / 1 ULP for bf16.
4. `t_sentencepiece_encode_decode.hexa` — load known SP model (CLM v4 64K vocab), encode "Hello world" → token ids, decode → original string; matches SP reference impl.
5. `t_llama3_tokenizer_load.hexa` — load `meta-llama/Llama-3.2-3B/tokenizer.json`, encode "Hello world", first token id matches HF tokenizers reference.

### Cost band
- **$0 Mac dev** — pure hexa CPU; Mac M1/M2/M3 sufficient.
- HF Hub bandwidth: ~6.5 GB Llama-3.2-3B safetensors download (one-time, cached).
- ~10 MB Llama-3 tokenizer.json + CLM v4 SP model.
- Wallclock: 2-4 weeks focused engineering.

### Acceptance criteria
- All 5 falsifier tests pass green on Mac.
- No new Python dependencies in hexa-lang (pure hexa stdlib only).
- safetensors round-trip preserves byte-identical output (existing F-SAFETENSORS-1 not regressed).
- HF Hub I/O respects HTTP 302/redirect chains for LFS-stored files.

### Dependencies
- stdlib/http.hexa (LIVE) — for HF Hub HTTP.
- stdlib/json.hexa (LIVE) — for HF API responses.
- stdlib/bytes.hexa (LIVE) — for byte-level safetensors + SP protobuf.
- stdlib/safetensors.hexa byte layer (LIVE) — extending, not rewriting.

### Unlock
**"Load any HF model + tokenize input in pure hexa"** — foundation for Phase 2-5. Mode 1 eval prep step achievable.

---

## Phase 2 PR — Llama-3 Forward Enable

### Files
- `hexa-lang/stdlib/tensor/dtype.hexa` (NEW, ~1,500 LoC) — bf16/fp16 dtype enum + cast helpers + contiguous-byte-buffer Tensor variant (vs current fp64 list).
- `hexa-lang/stdlib/tensor/ops.hexa` (REWRITE ~+3,000 LoC over existing 108) — production matmul (BLAS-backed Mac libcblas + Linux hxblas), softmax, layernorm, RMSNorm, gelu, silu over contiguous bf16 buffers.
- `hexa-lang/stdlib/tensor/attention.hexa` (NEW, ~3,000 LoC) — scaled-dot-product attention CPU bf16; GQA variant; RoPE.
- `hexa-lang/self/ml/llama3.hexa` (NEW, ~5,000 LoC) — Llama-3 block stack (RMSNorm + GQA + RoPE + SwiGLU MLP); end-to-end forward.
- `hexa-lang/self/ml/llama3_block.hexa` (NEW, ~3,000 LoC) — single-layer Llama block.
- `hexa-lang/self/ml/conscious_decoder_v3.hexa` (NEW, ~5,000 LoC) — CLM v4 custom phi-gated 32-head attn over 1024 dim, 24 layers.
- `hexa-lang/test/t_phase2_*.hexa` (NEW, ~3,000 LoC) — Phase 2 falsifier suite.

### LoC estimate
- New: ~17,500 LoC
- Rewrite: ~5,000 LoC
- Tests: ~3,000 LoC
- **Total: ~25,500 LoC + tests**

### Falsifier set
1. `t_tensor_bf16_dtype.hexa` — Tensor with dtype=BF16 + contiguous buffer; cast f32↔bf16 round-trip within 1 ULP.
2. `t_tensor_matmul_production.hexa` — 1024×1024 bf16 matmul completes in <100ms on Mac M1+; result matches reference within fp32 ULP after cast.
3. `t_rmsnorm_match_pytorch.hexa` — RMSNorm output matches Llama-3 PyTorch reference within 1e-5 fp32 over 1000 vectors.
4. `t_gqa_attention_match_pytorch.hexa` — GQA attention (32 q-heads, 8 kv-heads) output matches Llama-3 PyTorch within 1e-3 fp32 on 1 layer.
5. `t_llama3_forward_match_pytorch.hexa` — Llama-3.2-3B forward 1 sequence; logits within 1e-3 fp32 of PyTorch reference (top-5 token argmax must match).
6. `t_conscious_decoder_v3_forward.hexa` — CLM v4 forward; logits match anima-side reference impl within 1e-3.

### Cost band
- **$0 Mac CPU dev** for primary development.
- **~$50 RunPod H100 hour** for PyTorch reference vector generation (one-time).
- Wallclock: 6-12 weeks focused engineering.

### Acceptance criteria
- All 6 falsifier tests pass.
- Llama-3.2-3B forward 1 sequence in <60s on Mac M1+ CPU (acceptable for Mode 1 eval; not training).
- bf16 matmul achieves ≥30% of theoretical Mac CPU FLOPS via BLAS path.
- No correctness regression on existing tensor/ops tests.

### Dependencies
- Phase 1 (model load + safetensors numeric + tokenizer).
- stdlib/linalg/ffi.hexa for BLAS dispatch (Mac libcblas + Linux hxblas).

### Unlock
**"Llama-3.2-3B + CLM v4 inference in pure hexa CPU"** — Mode 1 eval base model forward achievable.

---

## Phase 3 PR — Mode 1 Eval Enable

### Files
- `hexa-lang/stdlib/eval/multiple_choice.hexa` (NEW, ~1,500 LoC) — per-choice loglikelihood loop, argmax, accuracy.
- `hexa-lang/stdlib/eval/generative.hexa` (NEW, ~2,000 LoC) — greedy + beam decode + EM/F1 scorer.
- `hexa-lang/stdlib/eval/filters.hexa` (NEW, ~500 LoC) — remove_whitespace, remove_punctuation, lowercase, regex extract.
- `hexa-lang/stdlib/eval/hellaswag.hexa` (NEW, ~500 LoC) — task adapter loading dataset.
- `hexa-lang/stdlib/eval/mmlu.hexa` (NEW, ~500 LoC) — MMLU 57-subject task adapter.
- `hexa-lang/stdlib/eval/trivia_qa.hexa` (NEW, ~500 LoC) — TriviaQA generative task adapter.
- `hexa-lang/self/ml/lora.hexa` (REWRITE ~+1,500 LoC over existing 158) — production LoRA forward composition over bf16 buffers (base × W + lora_A @ lora_B × scaling).
- `hexa-lang/test/t_phase3_*.hexa` (NEW, ~2,000 LoC) — Phase 3 falsifier suite + comparison harness against lm-eval-harness.

### LoC estimate
- New: ~5,500 LoC
- Rewrite: ~1,500 LoC
- Tests: ~2,000 LoC
- **Total: ~9,000 LoC + tests** (compared to my pre-decomposition estimate of 15k — refined down once eval primitives surface clarified)

### Falsifier set
1. `t_lora_forward_match_peft.hexa` — LoRA forward output matches PEFT PyTorch within 1e-4 fp32.
2. `t_hellaswag_match_lm_eval_harness.hexa` — HellaSwag 100-sample accuracy within ±0.005 of lm-eval-harness reference.
3. `t_mmlu_subset_match_lm_eval_harness.hexa` — MMLU `mathematics_high_school` subject 100-sample accuracy within ±0.01.
4. `t_trivia_qa_em_f1_match.hexa` — TriviaQA 100-sample EM/F1 within ±0.01.
5. `t_filter_primitives_round_trip.hexa` — `lowercase + remove_punctuation` round-trip on 1000 strings matches Python `string.punctuation` reference.

### Cost band
- **$0 Mac CPU dev** — Mode 1 eval is intrinsically CPU-acceptable (not throughput-bound).
- HF dataset bandwidth: ~500 MB HellaSwag + MMLU + TriviaQA combined (one-time).
- Wallclock: 4-8 weeks focused engineering.

### Acceptance criteria
- All 5 falsifier tests pass.
- HellaSwag full 10042-sample run completes in <4 hours on Mac M1+ (acceptable for eval; bench against lm-eval-harness baseline).
- LoRA forward parity validated against P9 paradigm A/B/C/D adapters.

### Dependencies
- Phase 1 (HF Hub I/O for dataset download + safetensors numeric for adapter weights).
- Phase 2 (Llama-3 + CLM v4 forward).

### Unlock
**"Mode 1 LoRA eval (P9 paradigm A/B/C/D) entirely via hexa-lang"** — this is the **mk2 hexa-only enforce-able target**. Phase 3 completion = hexa-only inference path is real and validated.

---

## Phase 4 PR — Path-A Retrain Enable (DEFERRED — explicit non-goal for mk2 EOL)

### Files
- `hexa-lang/stdlib/optim.hexa` (REWRITE ~+1,500 LoC over existing 25) — production AdamW with weight decay + epsilon + bias correction.
- `hexa-lang/stdlib/optim/cosine.hexa` (NEW, ~500 LoC) — cosine LR schedule + warmup.
- `hexa-lang/self/ml/lora.hexa` (EXTEND ~+2,500 LoC) — LoRA backward (∂L/∂A, ∂L/∂B, base frozen).
- `hexa-lang/stdlib/autograd.hexa` (REWRITE ~+10,000 LoC over existing 413) — autograd validated at transformer scale (broadcast + in-place + non-differentiable handling).
- `hexa-lang/self/ml/checkpoint_hf.hexa` (NEW, ~1,500 LoC) — HF safetensors layout save + adapter_config.json.
- `hexa-lang/self/ml/dataloader.hexa` (REWRITE ~+2,000 LoC) — streaming + shuffle + pad + multi-worker.
- `hexa-lang/self/ml/train_loop.hexa` (REWRITE ~+3,000 LoC) — fwd + loss + bwd + opt step + grad accumulation.

### LoC estimate
- New: ~2,000 LoC
- Rewrite: ~19,000 LoC
- Tests: ~5,000 LoC (autograd validation suite is itself huge)
- **Total: ~26,000 LoC + tests**

### Falsifier set
1. AdamW step matches PyTorch optim.AdamW within 1e-6 fp32 over 1000 steps.
2. Cosine schedule LR values match PyTorch cosine_with_warmup within 0.
3. Autograd: gradient through 1-layer Llama block matches PyTorch autograd within 1e-4 fp32.
4. LoRA backward: ∂L/∂A and ∂L/∂B match PEFT within 1e-4 fp32.
5. Path-A retrain: 100-step LoRA training run on 1000-sample subset; loss decreases monotonically; final adapter matches PyTorch-trained adapter within 5% on HellaSwag accuracy.

### Cost band
- **GPU required** — Phase 4 cannot run pure-CPU at scale.
- **~$500-2000 RunPod H100** for end-to-end falsifier validation.
- Wallclock: **6-12 months** (autograd at transformer scale alone is multi-month).

### Acceptance criteria
- All falsifier tests pass.
- 100-step Llama-3.2-3B LoRA retrain matches PyTorch baseline within 5% accuracy on Mode 1 eval.

### Status
**EXPLICIT NON-GOAL for mk2 EOL gate.** Per audit.md §8 honest C3 #1: gating mk2 EOL on Phase 4 = years of work blocking < 1 cycle deadline. **Recommendation**: maintain `tool/transient_py/` raw#37 namespace as bridge for retrain workflows; Phase 4 lands async over months/years.

---

## Phase 5 PR — Paradigm D Distill Enable (DEFERRED)

### Files
- `hexa-lang/stdlib/loss/kl_div.hexa` (NEW, ~1,000 LoC) — KL divergence loss on bf16 contiguous buffers (production scale).
- `hexa-lang/self/ml/teacher_cache.hexa` (NEW, ~1,500 LoC) — top-K teacher logit cache loader (sample-aware).
- `hexa-lang/self/ml/distillation.hexa` (REWRITE ~+2,000 LoC over existing 607) — combined hard + soft + feature loss; production distill loop.

### LoC estimate
- New: ~2,500 LoC
- Rewrite: ~2,000 LoC
- Tests: ~1,000 LoC
- **Total: ~5,500 LoC + tests**

### Falsifier set
1. KL div matches PyTorch `F.kl_div` within 1e-5 fp32 on 1000 sample distributions.
2. Top-K teacher cache loads paradigm D 50K-step cache from disk; sample i lookup returns expected top-K logits.
3. Paradigm D distill 100-step run on 1000-sample subset; combined loss decreases monotonically; student adapter matches reference within 5% on Mode 1 eval.

### Cost band
- **GPU required** (depends on Phase 4 autograd + training infra).
- **~$200-500 RunPod H100** for distill validation.
- Wallclock: 2-3 months on top of Phase 4.

### Acceptance criteria
- All falsifier tests pass.
- Paradigm D distill matches PyTorch baseline within 5% accuracy.

### Status
**DEFERRED** — depends on Phase 4 (autograd + training loop). Same honest C3 logic: not in mk2 EOL scope.

---

## Cross-link to BG-α hive audit (mk2 14/273 — restore canonical layer urgent)

Per BG-α audit: mk2 = 14/273 rules (5.13% parity); bulk LIVE rules vanished. mk2 EOL decision before "lint coverage parity" gate reachable. **This phased plan addresses the orthogonal-but-related question**: even if mk2 lint catches up to legacy, hexa-only enforce-ability requires hexa-lang ML primitives that don't exist today.

**Recommendation alignment**: BG-α should evaluate mk2 EOL primarily on **lint parity restoration** (separate from this audit). hexa-only mandate enforce-ability is a **secondary mk2 concern**, deferred to Phase 1-3 completion (months async). **Do not couple the two decisions.**

---

## Roadmap proposal — hive `.raw.mk2` entry

```
ai-native.002 hexa-canonical-mandate
  scope: enforce hexa-only for inference + eval (Phase 1-3); training/distill DEFERRED
  status: PROPOSED 2026-05-04 (BG-δ audit)

  phase-1 falsifier (model-load enable):
    GIVEN  Mac CPU + hexa runtime + network access
    WHEN   pure-hexa download + tokenize + load-safetensors of Llama-3.2-3B
    THEN   "logits computed for token 'Hello'" reachable in <30s
    LoC    ~6,300 LoC
    cost   $0 + bandwidth

  phase-2 falsifier (Llama forward enable):
    GIVEN  Phase 1 complete
    WHEN   pure-hexa Llama-3.2-3B forward 1 sequence
    THEN   logits within 1e-3 fp32 of PyTorch reference (top-5 argmax matches)
    LoC    ~25,500 LoC
    cost   $0 Mac + ~$50 RunPod (one-time reference vectors)

  phase-3 falsifier (Mode 1 eval enable):
    GIVEN  Phase 2 complete
    WHEN   pure-hexa HellaSwag eval on 100 samples
    THEN   accuracy within ±0.005 of lm-eval-harness reference
    LoC    ~9,000 LoC
    cost   $0 Mac CPU + dataset bandwidth

  phase-4-5: explicit non-goal for mk2 EOL
    rationale: autograd + GPU training at transformer scale = years; gating mk2
               on this = guaranteed indefinite stall

  enforcement (when phase-3 lands):
    pre-commit hook bans .py creation in tool/, _python_bridge/, anywhere except:
      (a) tool/transient_py/ (raw#37 auto-gen namespace)
      (b) .own 1 grandfather list
    auto-generated .py header marker required for tool/transient_py/*.py
    drift auditor tool/hexa_py_drift_audit.hexa runs pre-commit
    human edit of any tool/transient_py/*.py = raw violation

  bridge (until phase-3 lands):
    tool/transient_py/ namespace formalized via .own update (anima-side)
    auto-gen .py from .hexa source allowed; human-authored .py banned
```

This makes hexa-only **enforce-able at Phase 3 completion** (months async to mk2 EOL) without blocking mk2 EOL today.

---

## Summary table — Phase-by-Phase

| Phase | Scope | LoC | Wallclock | Cost | Unlock | Status |
|---|---|---|---|---|---|---|
| 1 | Model load enable | ~6,300 | 2-4 weeks | $0 + bandwidth | Load any HF model + tokenize | RECOMMENDED |
| 2 | Llama-3 forward enable | ~25,500 | 6-12 weeks | $0 + ~$50 RunPod | Llama + CLM v4 inference CPU | RECOMMENDED |
| 3 | Mode 1 eval enable | ~9,000 | 4-8 weeks | $0 + bandwidth | mk2 hexa-only enforce-able target | RECOMMENDED |
| 4 | Path-A retrain enable | ~26,000 | 6-12 months | ~$500-2000 RunPod | Pure-hexa training | DEFERRED |
| 5 | Paradigm D distill enable | ~5,500 | +2-3 months on Phase 4 | ~$200-500 RunPod | Pure-hexa distill | DEFERRED |
| **Total Phase 1-3 (mk2 hexa-only inference scope)** | | **~40,800 LoC** | **3-6 months** | **<$100** | Mode 1 eval via hexa | RECOMMENDED |
| **Total Phase 1-5 (full hexa-only)** | | **~72,300 LoC** | **1-2 years** | **~$1k-3k** | All ML workflows | NOT mk2 scope |
| Phase-future GPU full stack | | ~30,000 LoC | years | ~$5k-20k | Production training scale | NOT mk2 scope |
