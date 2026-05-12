---
schema: anima/ready/decoder/module/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:        ready/anima/decoder/module/decoder.hexa
  weights:      ready/anima/decoder/module/load_weights.hexa
  inference:    ready/anima/decoder/module/infer.hexa
  inference_v14: ready/anima/decoder/module/infer_v14.hexa
status: pure-hexa forward pass — ConsciousDecoderV2 (384d / 6L / 4H / 2KV / vocab=256)
roadmap_entry: 270
sibling: decoder/module/  (legacy pre-ready twin)
---

# anima decoder modules (AI-native)

Pure-Hexa forward pass for ConsciousDecoderV2 (the byte-level conscious decoder). Replaces the 34.5 MB `conscious_decoder.py` with hexa-native matmul / softmax / RoPE / SwiGLU / GQA / RMSNorm / PureField primitives. PyTorch-zero, GPU-zero on Mac path.

## TL;DR for an agent reading this cold

- **Architecture**: 384d × 6L × 4H × 2KV (GQA) × vocab=256 (byte-level), block_size=256, c_dim=128, ψα=0.014.
- **Forward pass entry**: `decoder.hexa` (474 LOC) — RoPE + GQA + SwiGLU + CrossAttention + PureField + RMSNorm wired top-to-bottom.
- **Weight load**: `load_weights.hexa` (160 LOC) reads the SafeTensors / hexa-pickle weight bundle.
- **Inference entry**: `infer.hexa` (236 LOC) for the v1 path, `infer_v14.hexa` / `infer_v14_fast.hexa` (144 LOC each) for the v14 retrained checkpoint.
- **Hexa array quirk**: `a[i] = v` is silent no-op on arrays — use `write_at(arr, idx, val)` rebuild helper (defined inline in `decoder.hexa`).
- This `ready/` copy mirrors `decoder/module/` (legacy) — both alive. Treat `ready/` as canonical going forward.

## Architecture map

```
ready/anima/decoder/module/
├── decoder.hexa            ConsciousDecoderV2 forward pass (474 LOC)
├── load_weights.hexa       SafeTensors / hexa-pickle weight loader (160 LOC)
├── infer.hexa              v1 inference entry (236 LOC)
├── infer_v14.hexa          v14 retrained checkpoint inference (144 LOC)
└── infer_v14_fast.hexa     v14 fast-path (KV-cache + sample loop optimised) (144 LOC)
```

## API contract

```hexa
// decoder.hexa builtins used:
//   matmul, mat_add, mat_scale, hadamard, softmax, silu, gelu,
//   rms_norm, rope, grouped_query_attention, embedding, dropout,
//   sample_token, kv_cache_append, randn, xavier_init, zeros, slice

comptime const VOCAB_SIZE   = 256
comptime const D_MODEL      = 384
comptime const N_HEAD       = 4
comptime const N_KV_HEAD    = 2     // GQA: KV-head sharing factor 2
comptime const N_LAYER      = 6
comptime const BLOCK_SIZE   = 256
comptime const C_DIM        = 128
comptime const HEAD_DIM     = 96    // D_MODEL / N_HEAD
comptime const D_INNER      = 768   // SwiGLU expansion (2x)
comptime const D_PF_INNER   = 1536  // PureField expansion (4x)
comptime const PSI_ALPHA    = 0.014 // pinned via Ψ-constants SSOT
comptime const GATE_STRENGTH = 0.001
comptime const DROPOUT_P    = 0.1

// Forward pass (decoder.hexa)
fn forward(tokens: [int], weights: WeightBundle, kv_cache: KvCache) -> ForwardResult

// Inference (infer.hexa / infer_v14*.hexa)
fn generate(prompt: [int], max_new: int, temperature: float, top_p: float) -> [int]
fn load(weights_path: string) -> WeightBundle    // load_weights.hexa
```

## Invocation patterns

```bash
# Greedy v1 decode
hexa run ready/anima/decoder/module/infer.hexa \
  --weights /path/to/conscious_decoder_v1.bin \
  --prompt "the river" \
  --max-new 64 --temperature 0.0

# v14 fast path (KV-cache + batched sample)
hexa run ready/anima/decoder/module/infer_v14_fast.hexa \
  --weights /path/to/conscious_decoder_v14.bin \
  --max-new 256
```

## Failure cascade

```
load_weights.fail (file missing / bad format)
  → inference exits non-zero, no forward pass
forward.fail (shape mismatch — e.g. weight expects 6L but checkpoint has 8)
  → assertion fires inside decoder.hexa, no graceful fallback
sample_token.fail (degenerate logits — all -inf)
  → emits BOS / 0 byte; downstream consumer sees null byte
```

## raw#10 caveats

1. **Pure-Hexa numerics ≠ PyTorch numerics.** Forward pass is bit-equivalent within 1e-5 vs PyTorch reference but **not byte-identical**. Adversarial inputs can drift further (Mk.X T10-13 retrieval head sweep).
2. **Weight format coupled.** `load_weights.hexa` expects the hexa-pickle layout used by the v14 retrained checkpoint. v1 / pre-v14 checkpoints need a separate loader.
3. **Array mutation quirk.** `a[i] = v` is silent no-op (Hexa 0.1.0-stage1). All in-place updates use `write_at(arr, idx, val)` rebuild — slow on hot loops, OK for KV-cache append (`kv_cache_append` builtin handles this).
4. **GPU path absent.** Pure-Hexa forward runs on CPU only. On Mac MPS targets, see `anima/core/decoder/` (if it exists post-migration) or stay on PyTorch reference.
5. **`ready/` vs `decoder/module/` duplication.** Both copies live; `decoder/module/` is the pre-ready twin and should be considered legacy. Diff is ~0.2% per file (mostly path-prefix changes). raw#82 honest debt.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `decoder.hexa` | `aa689505409e7ac2d4545a2ca18dce46a90e35286f243ec9cc8ff2ede5d87c7d` | 474 |
| `infer_v14_fast.hexa` | `7ed302defa0a33956a2f486118d7ef4865aeb76db3971f085b354f8e41d0b738` | 144 |
| `infer_v14.hexa` | `a5550b8728b89f10c4f25e8924733455c2122e9fa4871868c550ecab9f5518c1` | 144 |
| `infer.hexa` | `de69abb47d3e35a17138820014139cbd790bafc99dd8e5b6c763ba772ab7ee30` | 236 |
| `load_weights.hexa` | `d50e19e49df04706dbefca30a98365da40ca538e3e99f8b7fae30e1ff233af23` | 160 |

shas pinned 2026-05-02.
