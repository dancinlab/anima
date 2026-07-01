# Engine-Native Parity FIX — 303M ByteGPT (2026-06-17)

**Result:** byte-exact CORE↔torch parity restored. CORE forward via the hexa C-transpile
(dispatch) engine path now matches the torch golden EXACTLY for prompt "The quick brown".

| metric | CORE (fixed) | torch golden | match |
|---|---|---|---|
| argmax | 32 | 32 | ✓ |
| maxval | 29.689789 | 29.689796 | ✓ (~1e-5 fp) |
| top5 | 32 44 10 63 46 | 32 44 10 63 46 | ✓ |

(Before the fix: CORE argmax=227, maxval=20.0089 — a hard divergence.)

## Root cause — per-layer activation bisect

Instrumented the last-token residual-stream checksum (sum / max_abs) after embedding (k=0)
and each of the 24 blocks; torch reference computed FROM chat_full.bin (byte-identical weights).

| k | TORCH sum | CORE(buggy) sum | TORCH maxabs | CORE maxabs |
|---|---|---|---|---|
| 0 (embed) | 1.060572 | 24.329727 | 4.539062 | 4.523438 |
| 1 | 39.915115 | 19.288711 | 9.042029 | 7.362897 |
| 24 | 294.905518 | 247.618779 | 891.716064 | 816.836459 |

**First divergence = k=0 (embedding), before ANY transformer block** → weight-load/id-read
bug, not transformer math. Localized: CORE resolved the last-token id as 0 (torch=110);
position embedding read CORRECT, token id ALL ZEROS. The `ids` float-array was all-zeros at
forward entry.

## The bug (4-line minimal repro, deterministic, hexa C-transpile dispatch path)

```
let pb = [84, 104, 110]                 // int LITERAL array → i64-specialized backing
let ids = farr_zeros(3)
let mut i = 0
while i < 3 { let _ = farr_set(ids, i, to_float(pb[i])); i = i + 1 }   // stores 0 0 0  (BUG)
```
`farr_set(ids, i, to_float(pb[i]))` writes **0**. Hoisting the subscript fixes it:
```
while i < 3 { let bi = pb[i]; let _ = farr_set(ids, i, to_float(bi)); i = i + 1 }  // 84 104 110
```

Op-granular bisect (all on the dispatch path, deterministic across runs):
- `farr_set(a,i, 7.0)` → OK ; `farr_set(a,i, to_float(i))` → OK ; `farr_set(a,i, farr_get(src,i))` → OK
- `farr_set(a,i, to_float(pb[i]))` → **0 BUG** ; `+ 0.0` does NOT rescue ; hoist DOES.
- A single `to_float(pb[i])` PRINTED is correct; only the STORE drops it. Re-reading `pb[i]`
  after a store in the same scope makes `to_string(pb[i])` print `<value>` = hexa_to_string's
  fallback for TAG_ARRAY/MAP/FN/CHAR/CLOSURE → the i64-array element read returned a
  mis-tagged value → __hx_to_double → 0.

## Where it lives
- Emitted C is correct: `hexa_farr_set(ids, i, hexa_float(__hx_to_double(hexa_index_get(pb, i))))`.
- Fault is RUNTIME, in `self/runtime_core_emit.hexa`: `hexa_index_get` on an i64-SPECIALIZED
  array (`hexa_arr_i64_new/push` backing) dispatches to `hexa_array_get` (generic HexaVal-array
  reader) → returns a wrong-tagged element → 0 when to-doubled into the farr store.
- DISTINCT from the Lane-B fn-arena use-after-free (HX_TAG=24 crash): arena-disable
  (HEXA_VAL_ARENA=0 / HEXA_ARRAY_ARENA=0 / HEXA_ARRAY_PUSH_ARENA=0) does NOT fix this
  (303M forward stays argmax=227). Same module + class, two separate fixes.
- NOT #3491 (x86_64 native-asm float-cmp — off the dispatch path), NOT libm, NOT model math,
  NOT serialization.

## Engine-side workaround (verified, in parity_probe_HOISTED.hexa)
Hoist every inline `arr[idx]` out of farr_set / store value-args. The forward's
`x = tok[id] + pos[t]` loop already hoists `id`, so CORE/bytegpt_decode.hexa itself is safe;
only the probe's id-setup loop needed the hoist. With it: argmax=32 byte-exact.

## Compiler root fix (filed to hexa-lang)
`hexa_index_get` must detect an i64-specialized array and return a TAG_INT element (or
`hexa_array_get` must unwrap the i64 backing). Depletion: the 4-line repro stores 84 104 110
with the arena ON.

Files here: parity_probe_HOISTED.hexa (the corrected probe), torch_bin_layerdump.py (the
per-layer torch reference from chat_full.bin), LANE_A_RESULT_full.txt (full r1-r4 evidence).
