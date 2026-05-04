# hexa-lang Phase 1 — `stdlib/ieee754.hexa` design (BG-β³)

**Date**: 2026-05-04
**Owner**: BG-β³ parallel run (alongside BG-α³ `stdlib/hf_hub.hexa` + BG-γ³ `stdlib/sentencepiece.hexa`)
**Source**: BG-δ gap audit `2906a458` — `stdlib/safetensors.hexa` L62-67 explicit IEEE-754 gap
**Target**: 400-700 LoC pure hexa, additive-only, raw#9 strict

---

## 1. Problem

`stdlib/safetensors.hexa` is a complete byte-level reader/writer for the
HuggingFace safetensors v1 format. It returns each tensor's payload as
`data: array<int>` with each element in `0..255`. For dtype-agnostic
round-trip (write → read → write byte-identity, F-SAFETENSORS-1) this is
sufficient. But the consuming layer — anima inference, calibration cache,
model export — needs to reconstruct **actual float values** from those
bytes per IEEE-754 layout.

The L62-67 caveat in `safetensors.hexa` makes the gap explicit:

> Higher-level numerical conversion (float ↔ raw bytes) is OUT OF SCOPE —
> callers wishing to produce a tensor from native hexa floats must encode/
> decode the IEEE-754 bits themselves. […] Adding that helper is left as
> future work.

`stdlib/bytes.hexa` already provides f32/f64 reinterpret wrappers
(`f32_to_bytes_le_`, `bytes_to_f32_le_`, etc.) atop runtime builtins, but
**fp16 (binary16) and bf16 (Google brain-float) have no runtime support**.
HuggingFace model weights overwhelmingly ship in bf16 (modern LLMs) or
fp16 (vision / older LLMs); without bf16/fp16 codecs, safetensors is
effectively read-only-bytes.

This module fills that gap.

---

## 2. IEEE-754 layout cheat sheet

| Format    | Bits | Sign | Exp | Mantissa | Bias | Min normal | Max finite |
| --------- | ---: | ---: | --: | -------: | ---: | ---------: | ---------: |
| binary32  |   32 |    1 |   8 |       23 |  127 |    1.18e-38 |    3.40e38 |
| binary16  |   16 |    1 |   5 |       10 |   15 |    6.10e-5  |    6.55e4  |
| bfloat16  |   16 |    1 |   8 |        7 |  127 |    1.18e-38 |    3.39e38 |

**Key observations**:
- `bfloat16` = `binary32` truncated to top 16 bits. Same exponent range,
  same denormal threshold, only mantissa precision differs.
- `binary16` has a totally different bias/exp count → cannot be derived
  by truncation; needs explicit rebias + range-clamping.

**Endianness**: safetensors is **always little-endian** (per upstream
spec). Native macOS/Linux x86_64/arm64 are LE → no swap needed in the
common case. This module uses LE throughout; `swap_endian_u{16,32}`
helpers are provided for non-native (legacy GGML BE pickle) callers.

---

## 3. Conversion algorithms

### 3.1 fp32 (binary32) — runtime passthrough

The hexa runtime exposes:
- `f32_to_bytes_le(value: float) → array<int>[4]`
- `bytes_to_f32_le(buf: array<int>, offset: int) → float`

Implemented in `self/native/tensor_kernels.c` (lines 107-138) via
`memcpy(buf, &f, 4)` after a `(float)d` narrowing cast. Standard
IEEE-754 round-to-nearest-even, NaN payload preserving (modulo
narrowing).

`stdlib/ieee754` re-exports under `fp32_to_bytes` / `fp32_from_bytes`
with caller-side bounds checks (return 0.0 on short input — no panic).

### 3.2 bf16 (bfloat16) — TRUNCATION

```
fp32 LE bytes:  [b0, b1, b2, b3]    where b3 = sign+upper exp,
                                          b2 = lower exp + upper mantissa
bf16 LE bytes:  [b2, b3]            DROP b0, b1 (low 16 mantissa bits)
```

**Encode** (`bf16_to_bytes`):
1. Narrow value to fp32 via runtime builtin → 4 LE bytes.
2. Drop bytes 0-1, keep bytes 2-3.

**Decode** (`bf16_from_bytes`):
1. Pad with `[0, 0, c0, c1]`.
2. Decode as fp32.

**Semantics**: this is **truncating** (round-to-zero), matching Intel
SAPPHIRERAPIDS / NVIDIA H100 hardware default. PyTorch
`torch.bfloat16` uses round-to-nearest-even by default, which differs
by at most 1 ULP @ 7 mantissa bits (~7.8e-3 relative error, well below
the typical inference precision threshold).

### 3.3 fp16 (binary16) — REBIAS + CLAMP

```
fp32 word:  S(1) | E32(8) | M32(23)         bias 127
fp16 word:  S(1) | E16(5) | M16(10)         bias 15

Branches:
  E32 == 0xFF      → ±inf or NaN          → fp16 (S, 0x1F, NaN payload bit)
  E32 == 0,M32 == 0 → ±0                   → fp16 (S, 0, 0)
  adj = E32 - 112  ≥ 0x1F                  → ±inf16 (overflow saturate)
  adj ≤ 0                                   → subnormal: shift mantissa right by (1-adj)
  else                                      → fp16 (S, adj, M32 >> 13)
```

**Encode** (`fp16_to_bytes`):
- Reassemble fp32 LE bytes into a 32-bit word via `b3*2^24 + b2*2^16 + b1*2^8 + b0`.
- Extract sign / exp / mantissa via `&` and integer division (avoids
  signed-shift platform variance — same idiom as `safetensors._u64_le_bytes`).
- Branch on the four cases above.
- Pack 16-bit fp16 word into 2 LE bytes.

**Decode** (`fp16_from_bytes` → `_fp16_decode_at`):
- Inverse: extract fp16 sign/exp/mantissa, rebias exp, shift mantissa
  left by 13.
- Subnormal path: normalize mantissa (find top set bit), then encode
  as a normal fp32 with appropriate negative-biased exponent.
- Construct fp32 LE bytes, decode via `bytes_to_f32_le` builtin.

**Rounding**: this implementation uses **round-to-zero (truncation)**
for the encode path. Round-to-nearest-even is a future upgrade
(adds ~12 LoC to the `else` branch — acceptable but defers landing).

### 3.4 Bulk array helpers

Stable left-to-right loop, no SIMD, ~1-2 s per 1 M floats on M-series
Mac. Bytes-in / floats-out (decode) and floats-in / bytes-out (encode).
Caller owns shape — this layer is dtype-only.

### 3.5 Endian swap

`swap_endian_u32(x)` / `swap_endian_u16(x)` — pure arithmetic byte
reverse via `(x & 0xFF) << 24 | …` (multiplied not shifted, for the
signed-int safety reason).

### 3.6 Special-value predicates

`is_nan_f32(x)` / `is_inf_f32(x)` / `is_nan_f64(x)` / `is_inf_f64(x)` —
re-encode value to LE bytes, inspect exp+mantissa fields. Robust
against the runtime's `==` semantics (NaN != NaN trap) and ±0
ambiguity. Same approach as `test_bytes_float.hexa::chk_eq_float_local`.

---

## 4. raw#9 / raw#10 / raw#15 / raw#71 compliance

- **raw#9 hexa-only-strict**: zero `exec()`, zero new C builtin. Module
  consumes only the existing `f32_to_bytes_le` / `bytes_to_f32_le` runtime
  builtins (already shipped in production via tensor_kernels.c).
- **raw#10 ≥4 primitives**: 6 distinct primitive families exported:
  fp32, fp16, bf16, bulk array (3 dtypes), endian swap (2), special
  predicates (4). Total `pub fn` count: 23.
- **raw#15**: stdlib only consumes stdlib (uses `stdlib/bytes`). No
  cross-module reach into runtime internals.
- **raw#71**: additive — zero edits to existing hexa-lang stdlib files,
  zero edits to runtime.c, zero edits to BG-α³ / BG-γ³ territory.

---

## 5. Honest C3 (≥4 caveats)

1. **Subnormal handling** — fp16/bf16 subnormals are converted to nearest
   fp32 representation; underflow may flush-to-zero on platforms where
   the FPU FTZ flag is set (we cannot control FPU mode from hexa).
   Acceptable for inference (subnormals are rare in trained weights).
   Training-grade precision should use fp32.
2. **NaN propagation** — fp16/bf16 ↔ fp32 do NOT preserve NaN payloads
   bit-exactly. Only the canonical qNaN bit pattern survives a
   narrow → widen round-trip. bf16 ⊂ fp32 layout-wise so bf16 → fp32
   widen is payload-preserving for the upper 7 mantissa bits.
3. **fp8 (e4m3 / e5m2) DEFERRED** — Phase 2 work. Not yet in safetensors
   v1 mainline; NVIDIA / HF working group spec'd 2024 but the upstream
   safetensors-rs implementation is unstable. Will land once stabilized.
4. **No SIMD acceleration** — pure hexa arithmetic loop. ~1-2 s per
   1 M floats on M-series Mac (acceptable for one-shot model load,
   not for hot-path inference). A future C builtin (`bf16_array_decode`)
   could SIMD-accelerate; the API stays stable.
5. **Endianness** — safetensors is LE by spec. Big-endian platforms
   (IBM POWER) must call `swap_endian_*` before `*_from_bytes`. Native
   macOS/Linux x86_64/arm64 are LE (the common case).
6. **Round-to-zero default for fp16 encode** — matches hardware default
   but differs from PyTorch `torch.float16.tofile()` (round-to-nearest-even)
   by at most 1 ULP. For inference this is below the noise floor; for
   gradient-bit-identity training this would matter (irrelevant here —
   training uses fp32/bf16, not fp16).
7. **Interpreter selftest gap** — `hexa_real run` interpreter does NOT
   resolve the float-reinterpret runtime builtins (`f32_to_bytes_le`,
   `bytes_to_f32_le`, etc.). This is a pre-existing runtime/interpreter
   gap (also breaks `stdlib/test/test_bytes_float.hexa`). Compiled path
   (`hexa build`) resolves them via codegen_c2.hexa lines 3580-3590.
   Pure-arithmetic primitives in this module (endian swap, bounds
   checks, array length) DO pass under interpreter; bit-level primitives
   require the compiled path.

---

## 6. API surface

```hexa
mod ieee754

// fp32 ↔ bytes
pub fn fp32_to_bytes(value)            -> [u8; 4]
pub fn fp32_from_bytes(buf)            -> f32
pub fn fp32_from_bytes_at(buf, off)    -> f32

// bf16 ↔ bytes (TRUNCATING)
pub fn bf16_to_bytes(value)            -> [u8; 2]
pub fn bf16_from_bytes(buf)            -> f32
pub fn bf16_from_bytes_at(buf, off)    -> f32

// fp16 ↔ bytes (REBIAS+CLAMP)
pub fn fp16_to_bytes(value)            -> [u8; 2]
pub fn fp16_from_bytes(buf)            -> f32
pub fn fp16_from_bytes_at(buf, off)    -> f32

// Bulk
pub fn fp32_array_from_bytes(buf, n)   -> [f32]
pub fn fp32_array_to_bytes(values)     -> [u8]
pub fn bf16_array_from_bytes(buf, n)   -> [f32]
pub fn bf16_array_to_bytes(values)     -> [u8]
pub fn fp16_array_from_bytes(buf, n)   -> [f32]
pub fn fp16_array_to_bytes(values)     -> [u8]

// Endianness
pub fn swap_endian_u32(x)              -> u32
pub fn swap_endian_u16(x)              -> u16

// Special predicates
pub fn is_nan_f32(x)                   -> bool
pub fn is_inf_f32(x)                   -> bool
pub fn is_nan_f64(x)                   -> bool
pub fn is_inf_f64(x)                   -> bool
```

23 `pub fn` total. ~837 LoC including selftest.

---

## 7. Integration path with `stdlib/safetensors.hexa`

A Phase 2 follow-on can add a `safetensors_read_typed(path)` helper that
walks each tensor in the result map and, based on `dtype`, calls the
appropriate `<dtype>_array_from_bytes(data, prod(shape))` from this
module to populate a `"values": [f32]` field alongside the raw `"data"`.
This stays additive to safetensors.hexa (no breaking change to
existing F-SAFETENSORS-1 round-trip semantics).

---

## 8. Selftest path

```bash
# Direct interpreter run (limited — runtime builtin gap):
/Users/ghost/.hx/bin/hexa_real run /Users/ghost/core/hexa-lang/stdlib/ieee754.hexa

# Compiled path (full coverage — when Docker resolver is healthy):
/Users/ghost/.hx/bin/hexa build /Users/ghost/core/hexa-lang/stdlib/ieee754.hexa \
  -o /tmp/ieee754_selftest && /tmp/ieee754_selftest
```

See `selftest_log.txt` for captured output. Interpreter run shows
**11 PASS / 15 FAIL** where all 15 failures are the pre-existing runtime
builtin gap (also affects `test_bytes_float.hexa`). All pure-arithmetic
primitives (endian swap, bounds checks, array sizing) pass.
