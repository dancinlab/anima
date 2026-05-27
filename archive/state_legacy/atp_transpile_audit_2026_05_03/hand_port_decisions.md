# Hand-Port Decisions: audio_token_predictor.hexa → atp_pytorch.py

**Date**: 2026-05-03
**Source**: anima-voice/audio_token_predictor.hexa @ d290f1ae7 (Mk.III, 1576 LoC)
**Target**: tool/transient_py/atp_pytorch.py (.own 2 namespace, 645 LoC)
**Generator**: Claude Opus 4.7 BG subagent (Phase 1 of Track A2→A escalation)
**Reference**: docs/hexa_lang_upstream_audit_2026_05_03.md §7.3

---

## 1. Top-Level Strategy

**Choice**: HAND-PORT (Track A2 / Phase 1) over symbolic transpiler.

**Rationale**:
- VLM stage1 BLOCKED *today* (gate #1 of 5)
- Audit estimates A2 hand-port at 4-16h vs A subset transpiler 8-24h
- A2 immediately unblocks; A Phase 2 lands the transpiler in next cycle to kill drift
- Pattern proven first; generality second

**Side effect**: Hexa source remains the canonical Mac SSOT; the .py is treated as auto-generated transient (raw#37 sister rule: state/.X_helper.py precedent extended to tool/transient_py/*.py).

---

## 2. Type Mapping

| Hexa | PyTorch | Notes |
|---|---|---|
| `int` | `int` (Python) | scalars |
| `float` | `float` (Python) | scalars |
| `array` (flat list) | `torch.Tensor` | n-d native, autograd-enabled |
| `array of array` (nested) | `torch.Tensor` | reshape via view/transpose |
| `[0.0]` (1-elem array for typing) | `int / float` (config field) | dataclass replaces typed-array idiom |

---

## 3. Function-Level Lowering Decisions

### 3.1 PRNG (atp_prng_next / atp_prng_float → torch.Generator)
- **Decision**: drop LCG, use torch.Generator with manual_seed
- **Justification**: training never reads PRNG (uses nn.init); only `generate()` samples; sequence values differ from hexa but distribution is the same
- **Caveat**: byte-level reproducibility with hexa interpreter NOT preserved

### 3.2 Layer Norm (atp_layer_norm → nn.LayerNorm)
- **Decision**: use nn.LayerNorm with same eps (ATP_EPS = 1e-8)
- **Justification**: identical math (subtract mean, divide by sqrt(var+eps), affine)
- **Caveat**: hexa source has `var = sum(diff^2)/d`; nn.LayerNorm uses unbiased=False default (population variance) — matches.

### 3.3 SwiGLU FFN (atp_swiglu_ffn → SwiGLUFFN class)
- **Decision**: preserve 3-projection layout (w1=up, w_gate, w2=down) with no bias
- **Justification**: hexa source uses `atp_rand_vec(df_dm, ...)` for w1/w_gate/w2 (no separate bias); matches modern Llama/Mistral SwiGLU convention

### 3.4 RoPE (atp_rope_encode → RotaryPositionEmbedding)
- **Decision**: precompute cos/sin tables for all positions [0, ATP_CTX); apply per-call by indexing
- **Justification**: hexa loops compute pow(10000, 2i/d) every call (slow); torch precomputes once
- **Equivalence check**: same formula `theta_i = 1/10000^(2i/d)`, same rotation matrix `[cos -sin; sin cos]`
- **Odd dimension handling**: passthrough last element preserved (matches hexa L289-292)

### 3.5 KV-Cache (atp_kv_cache_* + atp_raw_kv_* → tuple[Tensor, Tensor])
- **Decision**: use tuple of tensors; each block returns `(k, v)` post-fwd; caller passes back next step
- **Justification**: 
  - hexa list-based cache (atp_kv_cache) requires O(n) rebuild on append (pass-by-value)
  - hexa raw KV-cache (atp_raw_kv) eliminates copy via alloc_raw
  - PyTorch tensor cache is the natural equivalent (mutable, contiguous, no copy)
- **Caveat**: KV-cache invariants (causal correctness across cache boundary) NOT unit-tested; relies on SDPA `is_causal=True` for training and trust on inference (single-token decode = no future leakage by construction)

### 3.6 Attention (atp_multi_head_attn / atp_flash_mha → CausalSelfAttention)
- **Decision**: use F.scaled_dot_product_attention (SDPA)
- **Justification**: 
  - SDPA dispatches to flash kernel on sm_80+ GPUs
  - matches hexa flash impl semantics (online softmax, tiled, numerical-equivalent)
  - is_causal=True applied during training (q_len == k_len)
- **Caveat**: when kv_cache is non-empty (decode step with q_len < k_len), `is_causal=False` is used; for T=1 single-token decode this is correct (no future to mask); for T>1 with cache, caller must construct explicit mask (NOT NEEDED for VLM stage1 which uses parallel teacher-forced fwd)

### 3.7 Decoder Block (atp_block_forward / atp_flash_block_forward → DecoderBlock)
- **Decision**: pre-norm topology preserved
  - x → ln1 → attn → +residual → ln2 → ffn → +residual
- **Justification**: matches hexa source comment "Pre-Norm" (L657)
- **11-array weight layout** in hexa collapsed to 4 nn.Linear + 2 nn.LayerNorm per block

### 3.8 Top-K Sampling (atp_sample_top_k → torch.topk + multinomial)
- **Decision**: use torch.topk (O(k log V)) instead of selection sort (O(k*V))
- **Justification**: same distribution; faster
- **Numerical**: temperature scaling identical; softmax identical

### 3.9 CFG Blend (atp_cfg_blend → inline)
- **Decision**: inline expression `logits_uncond + cfg_scale * (logits_cond - logits_uncond)`
- **Justification**: trivial; no function call needed

### 3.10 Delayed Pattern (atp_assemble_delayed_pattern → inline loop)
- **Decision**: nested loop over (frame, stage), tensor-indexed assignment
- **Justification**: small loop, output is integer indices [B, n_frames, rvq_stages]
- **Could be vectorized**: yes (deferred — clarity over micro-perf in audit-trail)

---

## 4. VLM-Specific Additions

Per `docs/vlm_cond3_blocker_landed_2026_05_03.ai.md` §4:

| Addition | Justification |
|---|---|
| `text_embed: nn.Embedding(32000, 384)` | VLM stage1 input is TEXT tokens (audio_embed retained for AR generation) |
| `text_head: nn.Linear(384, 32000)` | parallel to rvq_heads; loss = 0.5*audio_CE + 0.5*text_CE |
| `intent_proj: nn.Linear(d_model, d_model)` | matches hexa atp_decode_step L957 |
| `ATPConfig dataclass` | explicit config object; replaces 10-element model-array indexing |
| `ln_final: nn.LayerNorm` | standard pre-norm transformer convention; hexa omitted; set Identity if strict-parity needed |

---

## 5. Numerical Equivalence Status

**NOT VERIFIED**:
- random init differs (LCG vs nn.init.normal)
- this is acceptable: training re-initializes from data
- byte-level equivalence with hexa interpreter would require:
  1. Port LCG to torch
  2. Port hexa init scale (`(s % 10000) / 50000.0 - 0.1` = uniform in [-0.1, 0.1])
  3. Match hexa float order-of-operations
- Decision: deferred — not required for VLM unblock
- Future test: feed identical weights + input to both hexa interpreter and torch port; assert max-diff < 1e-4

---

## 6. Excluded From This Port

| Excluded | Reason | Where it lives |
|---|---|---|
| `self_test_audio_token_predictor` (7 unit tests) | Not VLM-blocking; smoke_test() covers F-VLM-TRANSPILE-1 only | hexa source self-test still runs |
| `atp_format_float` | hexa interpreter helper for println formatting | json.dumps replaces |
| `main()` print blocks | hexa demo only | smoke_test() prints minimal verdict |
| build_hxcuda_istft bridge | downstream vocoder; out of ATP scope | anima-voice/build_hxcuda_istft.hexa |
| rvq_codebook indices→latent→audio | downstream; out of ATP scope | anima-voice/rvq_codebook* |

---

## 7. Retire-When Criteria

This .py auto-gen file should be regenerated/replaced when ANY of:

1. **Track A transpiler lands** (`tool/atp_to_pytorch.hexa` per audit §10.3) — supersedes hand-port
2. **Hexa source bumped beyond Mk.III** (Mk.IV signal: rvq_stages != 8, n_layers != 3, or new architecture component) — port semantics drift
3. **VLM stage1 sentinel fail** traced to port semantic divergence — re-audit numerical equivalence
4. **30 days elapsed** with no transpiler landing — escalate Phase 2 priority

---

## 8. Honest C3 Caveats (raw#10)

1. **Hand-port may diverge from source semantics** in subtle ways: random init scale, RoPE precompute vs per-call, SDPA flash kernel vs naive attention edge-cases at very small d_head, multinomial vs LCG distribution shape at low temperatures. None of these affect a successful F-VLM-TRANSPILE-1 forward pass; all could affect generated audio quality at inference time.

2. **Smoke test ≠ correctness**: F-VLM-TRANSPILE-1 verifies shape + finiteness + no-exception; it does NOT verify that gradients flow correctly through all modules, that loss decreases on real data, or that generated audio is intelligible. Stage1 LoRA training will be the first real correctness signal.

3. **KV-cache invariants not verified**: causal correctness across cache-empty → cache-populated boundary, RoPE position consistency between training fwd and generate(), and SDPA `is_causal` semantics with q_len < k_len are documented in code but NOT unit-tested. VLM stage1 training uses parallel teacher-forced fwd (no cache) so this is low-risk for the current cycle; risk reappears if streaming inference is benchmarked.

4. **RVQ stage isolation not unit-tested**: 8 RVQ heads share the same hidden state; per-stage delayed-pattern assembly is implemented but not verified against MusicGen/SoundStorm reference outputs. The delayed-pattern offset semantics (stage s ← step (frame - s)) match the hexa source comment but a reference cross-check is deferred.

5. **Retirement criteria depends on source stability**: if `audio_token_predictor.hexa` mutates between this BG and the next VLM training cycle, the hand-port drifts silently. Mitigation: marker file records source SHA `d290f1ae7`; pre-training step should diff against current source SHA and fail if mismatch.
