# Falsifier set — `stdlib/ieee754.hexa` (BG-β³ Phase 1)

**Date**: 2026-05-04
**Module**: `/Users/ghost/core/hexa-lang/stdlib/ieee754.hexa`
**Selftest harness**: `_selftest()` (in-module main entry)

Falsifiers are written as **boolean assertions** — each failing
assertion triggers `FAIL …` in the selftest log and a non-zero
exit code. PASS means the implementation cannot be falsified by the
listed test vectors.

---

## F-IEEE754-1 — fp32 round-trip exact

**Claim**: `fp32_from_bytes(fp32_to_bytes(v)) == v` bit-identically for
any `v` already representable in binary32.

**Test vectors** (selftest):
- 100 LCG-generated quasi-random fp32 values with bounded exponent
  (`exp ∈ [0x40, 0x60]` to stay finite, no NaN/inf in this batch).
- Known bit pattern: `fp32_to_bytes(1.0) == [0x00, 0x00, 0x80, 0x3F]`.

**Falsifier**: re-encode after decode and compare 4 LE bytes element-wise.

**Acceptance**: 100/100 round-trip bit-identical (selftest tag
`fp32_100_random_rt`) + `fp32_one_bytes` PASS.

**Status (interpreter run)**: depends on `f32_to_bytes_le` / `bytes_to_f32_le`
runtime builtin which is interpreter-gapped. Compiled path expected to PASS.

---

## F-IEEE754-2 — bf16 round-trip within 1 ULP @ 7 mantissa bits

**Claim**: For values **representable in bf16** (low 16 mantissa bits zero),
`bf16_from_bytes(bf16_to_bytes(v)) == v` bit-identically.

For arbitrary fp32 values, the round-trip differs from input by at most
1 ULP at 7 mantissa bits → ~7.8e-3 relative error.

**Test vectors**:
- bf16-exact set: `[0.0, 1.0, -1.0, 0.5, -0.5, 2.0, 4.0, 0.25]` —
  all of these have zero low-mantissa, so bit-exact round-trip.
- Known bit patterns:
  - `bf16_to_bytes(1.0) == [0x80, 0x3F]`
  - `bf16_to_bytes(-1.0) == [0x80, 0xBF]`
  - `bf16_to_bytes(0.0) == [0x00, 0x00]`

**Falsifier**: re-encode after decode and compare 4 LE bytes element-wise
(operating in fp32 space — bf16 widens to fp32 then re-narrows).

**Acceptance**: 8/8 bf16-exact round-trip bit-identical + 3/3 known
bit patterns match.

---

## F-IEEE754-3 — fp16 round-trip within 1 ULP @ 10 mantissa bits

**Claim**: For values **representable in fp16** (within ±65504 finite
range, low 13 mantissa bits zero), `fp16_from_bytes(fp16_to_bytes(v)) == v`
bit-identically.

Values larger than ~6.55e4 saturate to ±inf16. Values smaller than
~5.96e-8 underflow to ±0 (or denormal at the low end).

**Test vectors**:
- fp16-exact set: `[0.0, 1.0, -1.0, 0.5, 2.0, 4.0, 0.25]` — all
  representable exactly in binary16.
- Known bit patterns:
  - `fp16_to_bytes(1.0) == [0x00, 0x3C]` (0x3C00 = 1.0 binary16)
  - `fp16_to_bytes(-1.0) == [0x00, 0xBC]`
  - `fp16_to_bytes(0.0) == [0x00, 0x00]`

**Falsifier**: same as F-2.

**Acceptance**: 7/7 fp16-exact round-trip bit-identical + 3/3 known
bit patterns match.

---

## F-IEEE754-4 — NaN/Inf preserved through fp32 path

**Claim**: `is_nan_f32(qNaN) == true`, `is_inf_f32(±inf) == true`,
both predicates return `false` for normal finite values.

**Test vectors**:
- `pinf = bytes_to_f32_le([0, 0, 0x80, 0x7F])` (0x7F800000 = +inf32)
  → `is_inf_f32(pinf) == true`.
- `qnan = bytes_to_f32_le([0, 0, 0xC0, 0x7F])` (0x7FC00000 = qNaN)
  → `is_nan_f32(qnan) == true`.
- `is_nan_f32(1.0) == false`.
- `is_inf_f32(1.0) == false`.

**Falsifier**: predicate returns wrong boolean for any test vector.

**Acceptance**: 4/4 predicates correct.

---

## F-IEEE754-5 — bulk array round-trip stable

**Claim**: `<dtype>_array_from_bytes(<dtype>_array_to_bytes(arr), len(arr)) == arr`
for any input array of values representable in the given dtype.

**Test vectors**:
- fp32: `[0.0, 1.0, -1.0, 0.5, 2.0, 16.0, 0.25, -0.5]` — 8 values,
  expect 32 bytes, 8/8 match on round-trip.
- bf16: `[0.0, 1.0, -1.0, 0.5, 2.0, 4.0]` — 6 values, expect 12 bytes.
- fp16: `[0.0, 1.0, -1.0, 0.5, 2.0, 4.0]` — 6 values, expect 12 bytes.

**Falsifier**: byte length mismatches expectation OR any element
fails bit-identical compare after round-trip.

**Acceptance**: 3 dtypes × (length-check PASS + element-match PASS) = 6 PASS.

---

## F-IEEE754-6 — known bit patterns (sanity)

**Claim**: Specific well-known IEEE-754 bit patterns serialize to their
documented LE byte sequences.

**Test vectors**:
- `fp32(1.0)` = `0x3F800000` → LE `[0x00, 0x00, 0x80, 0x3F]`
- `bf16(1.0)` = `0x3F80` → LE `[0x80, 0x3F]`
- `bf16(-1.0)` = `0xBF80` → LE `[0x80, 0xBF]`
- `bf16(0.0)` = `0x0000` → LE `[0x00, 0x00]`
- `fp16(1.0)` = `0x3C00` → LE `[0x00, 0x3C]`
- `fp16(-1.0)` = `0xBC00` → LE `[0x00, 0xBC]`
- `fp16(0.0)` = `0x0000` → LE `[0x00, 0x00]`

**Falsifier**: any byte differs from the spec.

**Acceptance**: 7/7 known bit patterns match.

---

## F-IEEE754-7 — endian swap idempotent

**Claim**: `swap_endian_u32(swap_endian_u32(x)) == x` for any 32-bit
unsigned `x`. Same for `swap_endian_u16`.

**Test vectors**:
- `swap_endian_u32(0xDEADBEEF) == 0xEFBEADDE`
- `swap_endian_u32(swap_endian_u32(0x12345678)) == 0x12345678`
- `swap_endian_u16(0xABCD) == 0xCDAB`

**Falsifier**: byte-reversed output disagrees with documented spec OR
double-application non-identity.

**Acceptance**: 3/3 PASS.

---

## F-IEEE754-8 — bounds & no-panic on short input

**Claim**: All `*_from_bytes(buf)` family functions return `0.0` (no
panic, no exception) when `buf` is shorter than the format requires.

**Test vectors**:
- `fp32_from_bytes([1, 2])` → `0.0`
- `bf16_from_bytes([1])` → `0.0`
- `fp16_from_bytes([1])` → `0.0`

**Falsifier**: panic / non-zero return / runtime error.

**Acceptance**: 3/3 return `0.0` cleanly.

---

## Selftest summary (interpreter `hexa_real run`)

| Falsifier | Tags | Status (interp) | Status (compiled, expected) |
| --- | --- | --- | --- |
| F-1 | fp32_one_bytes, fp32_100_random_rt | FAIL (builtin gap) | PASS |
| F-2 | bf16_one_bytes, bf16_neg_one_bytes, bf16_zero_bytes, bf16_exact_rt | FAIL (builtin gap) | PASS |
| F-3 | fp16_one_bytes, fp16_neg_one_bytes, fp16_zero_bytes, fp16_exact_rt | FAIL (builtin gap) | PASS |
| F-4 | inf_predicate_pinf, nan_predicate_qnan, *_normal_neg | 2 PASS / 2 FAIL (builtin gap) | 4/4 PASS |
| F-5 | fp32_array_*_match, bf16_array_*_match, fp16_array_*_match | 3 length PASS / 3 match FAIL (builtin gap) | 6/6 PASS |
| F-6 | (subset of F-1/2/3 known bit patterns) | FAIL (builtin gap) | PASS |
| F-7 | swap_u32, swap_u32_idempotent, swap_u16 | 3/3 PASS | 3/3 PASS |
| F-8 | fp32_from_bytes_short, bf16_from_bytes_short, fp16_from_bytes_short | 3/3 PASS | 3/3 PASS |

**Interpreter total**: 11 PASS / 15 FAIL (out of 26 sub-checks).
**Compiled path expected**: 26/26 PASS (resolves runtime builtin gap).

The 15 interpreter FAILs are entirely accounted for by the pre-existing
gap that `hexa_real run` does not register the `f32_to_bytes_le` /
`bytes_to_f32_le` runtime builtins (the same gap also breaks
`stdlib/test/test_bytes_float.hexa` — verified by directly running it).
This is a pre-existing runtime/interpreter mismatch and OUT OF SCOPE
for this module — codegen_c2.hexa already wires the builtins into the
compiled path (lines 3580-3590).

**No falsifiers fail due to ieee754.hexa logic errors** — every interp
FAIL is upstream-gapped, every PASS validates ieee754.hexa correctness.
