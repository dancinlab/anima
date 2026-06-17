# BUG: i64-array element read dropped to 0 when nested in a farr_set store value-arg (C-transpile / dispatch path)

**Repro:** scripts/scratch/farr_set_i64index_drop_repro.hexa
```
hexa run scripts/scratch/farr_set_i64index_drop_repro.hexa
# EXPECT: BUG 84 104 110 / FIX 84 104 110
# ACTUAL: BUG 0 0 0       / FIX 84 104 110
```

**Symptom:** `farr_set(a, i, to_float(pb[i]))` where `pb = [84,104,110]` (an int LITERAL array)
silently stores 0. Hoisting `let v = pb[i]; farr_set(a, i, to_float(v))` stores the right value.

**Bisect (deterministic, dispatch path):**
- `farr_set(a,i, 7.0)` OK · `farr_set(a,i, to_float(i))` OK · `farr_set(a,i, farr_get(src,i))` OK (float-array source)
- `farr_set(a,i, to_float(pb[i]))` → 0 BUG (i64-array source) · `... + 0.0` does NOT rescue · hoist DOES
- `to_float(pb[i])` printed standalone is correct; only breaks when stored. Re-reading `pb[i]`
  after a store makes `to_string(pb[i])` print `<value>` (hexa_to_string fallback for
  TAG_ARRAY/MAP/FN/CHAR/CLOSURE) → the element read returned a MIS-TAGGED value.

**Emitted C (correct shape — fault is runtime, not codegen text):**
```c
HexaVal _ = hexa_farr_set(ids, i, hexa_float(__hx_to_double(hexa_index_get(pb, i))));
```
`pb` is built via `hexa_arr_i64_new` / `hexa_arr_i64_push` (int64-SPECIALIZED backing).
`hexa_index_get(pb, i)` falls to `hexa_array_get(pb, idx)` — the GENERIC HexaVal-array reader —
which mis-reads the i64-specialized backing and returns a wrong-tagged element; `__hx_to_double`
of that → 0.

**Suspected site:** `self/runtime_core_emit.hexa` — `hexa_index_get` / `hexa_array_get` do not
honor the i64-specialized array representation. Fix: detect an i64-specialized array in
`hexa_index_get` and return a `TAG_INT` element (or have `hexa_array_get` unwrap the i64 backing).

**NOT** the x86_64 native-asm float-cmp fix (#3491 — off the dispatch path), NOT the fn-arena
use-after-free (arena-disable HEXA_VAL_ARENA=0 / HEXA_ARRAY_ARENA=0 does NOT fix this).

**Impact:** broke anima 303M ByteGPT engine-native parity (token ids all read 0 →
embedding=tok[0] → argmax 227 vs torch golden 32). Engine-side workaround = hoist the subscript.

**Depletion test:** the repro prints `BUG 84 104 110` with the arena ON.

Found 2026-06-17 (anima Lane A codegen-parity).
