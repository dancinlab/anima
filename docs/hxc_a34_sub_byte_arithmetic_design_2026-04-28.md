# HXC A34 — Sub-byte Arithmetic Coder Design

**Date**: 2026-04-28
**Phase**: 14 P0 (post-N6 entropy-floor verdict commit `4cd8e62da`)
**Sigil**: `^l` (lowercase L, raw 92 sigil-line compliant; disjoint from
existing ^A..^Z uppercase set + ^a/^c/^h lowercase set)
**Trigger**: N6 entropy-floor witness commit `4cd8e62da` measured
`anima h_inf_proxy = 48.72%` and `n6 = 50.92%` byte-canonical — the per-file
**8-bit boundary** is the implicit floor that all byte-emitting coders
(A16 / A17 / A18 / A26 / A29 / A30 / A32) hit. Per-file `H_4 ≈ 4.7 bit/byte`
on text-heavy, but byte-emitting coders pay ≥ 8 bits/symbol — a 3.3-bit gap
per byte that **only fractional-bit (sub-byte) coding** can claim.
**Compliance**: raw 9 hexa-only · raw 18 self-host fixpoint ·
raw 42 mac jetsam (<100 MB on 79 KB) · raw 65 + 68 idempotent ·
raw 71 falsifier-preregistered · raw 91 honest C3 STRICT ·
raw 92 sigil-line · raw 137 cmix-ban · raw 156 placement-axis.

---

## 0. Honest framing (raw 91 C3 STRICT)

This document specifies the **complete** A34 algorithm. **First tick scope**
(this turn) = design doc + skeleton (~700 LoC) + PASS 1+2+3 selftest
(5 fixtures: 4 KB English / 4 KB JSON / 4 KB Korean / short passthrough /
cmix-ban audit). **PASS 4 LIVE FIRE = DEFERRED.** No 80% verdict claim,
no raw 137 v8 promotion this turn.

**In-sample estimator only**: the model trains on the same buffer it encodes
(Witten-Neal-Cleary 1987 §4 — adaptive). Out-of-sample generalization is
**not** measured this tick.

**Design projection (NOT a measurement)**: text-heavy +5..+15pp vs A29 v3.
Honest because:
1. Byte-canonical floor for text under H_4 ≈ 4.7 bit/byte = 58.75% saving.
2. A29 v3 measured 66% saving on 1.3 KB English (DEFLATE prefix codes pay
   ≥ 1 bit per literal). Sub-byte arithmetic theoretically reaches H_3 ≈
   2.5..3.0 bit/byte = 62..69% saving on 4 KB English.
3. The **bit-level coding** floor differs from byte-level by exactly the
   fractional-bit residual: ~0.5 bit × n_symbols / 8. On 4 KB English this
   is +6.25% absolute over byte-emitting Huffman.

**Retraction trigger**: if hexa-lang lacks native uint32 / bit-shift /
range-coder primitives, retract A34 design and pivot to in-language
approximation (carry-byte emit pattern proven in A16). Assessment in §6.

---

## 1. Algorithm rationale — why bit-stream arithmetic + order-3 PPM

### 1.1 Byte-emitting coders hit the 8-bit floor

Byte-emitting coders (A16 / A17 / A29 / A32) emit ≥ 1 byte per symbol — 8 bits
minimum granularity. For text-heavy fixtures with `H_3 ≈ 2.5..3.0 bit/byte`,
this leaves a 5..5.5 bit/byte gap per symbol that **no byte-level coder can
close**. The N6 entropy-floor verdict (`4cd8e62da`) measured this floor
empirically: per-file `h_inf_proxy = 48.72%` is the byte-canonical ceiling
for the N6 fixture.

### 1.2 Arithmetic coding closes the floor

A 32-bit range coder (Witten-Neal-Cleary 1987 §4 / Subbotin carry-renorm)
emits **fractional bits per symbol** by tracking a continuous interval
`[low, low+range) ⊆ [0, 2^32)`. Each input symbol narrows the interval
proportionally to its probability. After N symbols the interval width is
`product(P_i)` and `log2(1 / product) = sum(-log2(P_i))` bits — exactly the
Shannon entropy.

Implementation: integer-only 32-bit registers (i64 in hexa for headroom),
byte-emitting renormalization (emit top byte when low/high agree on it),
carry propagation via "pending bytes" counter. **No floating point.**
Cleary-Witten 1984 published the canonical reference; Subbotin 1996 added
the byte-emitting carry rescue.

### 1.3 Order-3 PPM context model — single deterministic predictor

Order-3 PPM tracks `P(byte | last 3 bytes)`. Method-D escape (Howard 1993):
`P(esc) = U / (U + T)` where `U = distinct symbols seen at context, T = total
mass`. On miss, fall back order-3 → order-2 → order-1 → order-0 → uniform.

**raw 137 cmix-ban explicit**: this is a **single deterministic predictor**.
NO context mixing, NO neural net, NO ZPAQ-style switch-mixer, NO paq8-style
adaptive weighting. The escape chain is a deterministic fallback ladder, not
a probability blend.

Compile-time grep audit gates: `neural`, `mixer`, `ZPAQ`, `paq8`, `cmix` =
0 hits in `hxc_a34_sub_byte_arith.hexa`.

### 1.4 Why A34 over A26 v3 (sparse PPMd)

A26 v3 measured **partial trip / production-unfeasible** byte-level Huffman
on PPMd: per-symbol 8-bit Huffman codes hit the same byte floor. A34 swaps
the entropy-coder backend (Huffman → arithmetic) while keeping the model
class (order-3 PPM). Wire saving ceiling for A34 vs A26 v3 = `1 - 0.5/8 ≈
93.75%` of remaining gap, i.e. on a 50% saving baseline → ~53% with A26 v3,
~58.5% with A34.

---

## 2. Architecture

### 2.1 Wire envelope (sigil ^l)

```
^l<v1-header><base85-payload>
```

- Header: `# a34:s<id> v=arith-v1 n=<input_bytes> b=<bit_count>`
- Payload prefix: `^l` (single ASCII char, raw 92 compliant)
- Payload encoding: base85 of the bit-stream byte representation
  (interior bit-level packed MSB-first into bytes; trailing zero-pad)
- Outer wrap: A16-compatible base85 wire (raw 157 placement-axis)

**Honest C3**: the **interior** wire is bit-level (sub-byte granularity);
the **exterior** wire is byte-canonical base85 to remain HXC v1 sigil-safe.
This means the saving is paid ONCE (at base85 wrap, ~6.25 pp overhead) and
**not** per-symbol. On 4 KB input the wrap overhead is ~0.078 bit/byte —
negligible vs the 5+ bit/byte gain.

### 2.2 32-bit range coder state

```
A34_TOP = 4_294_967_296       // 2^32 (ceiling)
A34_BOT = 16_777_216          // 2^24 (renorm threshold)
A34_MAX_FREQ = 16_777_215     // 2^24 - 1 (keeps range/total products in 32-bit)

low: i64    // lower bound of current interval, [0, 2^32)
range: i64  // width of current interval, kept >= BOT after renorm
```

Per-symbol narrow:
```
range = range / total
low   = low + cum_lo[sym] * range
range = range * (cum_hi[sym] - cum_lo[sym])
renormalize while top byte agrees or range < BOT
```

Renormalize emits top byte of `low` when `(low XOR (low+range)) >> 24 == 0`
(safe-emit). Underflow rescue: when `range < BOT` but top bytes still
disagree, emit a "pending byte" (deferred by carry propagation).

### 2.3 Order-3 PPM-D context model

Same per-context tables as A17:
- `tbl_count[ctx]`: 256-int array, count[sym_ord] = freq
- `tbl_keys[ctx]`: sorted-by-byte-ordinal symbol list
- `tbl_rank[ctx]`: 256-int array, rank[sym_ord] = position in keys, -1 if absent

**Bounded LRU (raw 42 jetsam)**: hard cap **16384 distinct contexts** across
all 4 orders combined. Eviction policy: when cap hit, evict order-3 contexts
first (highest fanout, lowest hit rate), then order-2, etc. Per-context
memory ≈ 1 KB (256 × 4 bytes). Worst case 16 MB context table on 79 KB input
→ well under the 100 MB raw-42 ceiling.

### 2.4 Encode flow

```
for p in [0..n):
    sym = bytes[p]
    if p < 3: emit_raw(sym, 8 bits)  // first 3 bytes ride raw
    else:
        for order in [3, 2, 1, 0]:
            ctx = bytes[p-order..p]
            if sym in ctx:
                emit_escape_failure_chain(orders > order)
                emit_arith_symbol(ctx, sym)
                update all tables (orders 0..3)
                break
        else:
            emit_full_escape_chain
            emit_uniform(sym, 8 bits via arith)
```

### 2.5 Decode flow

Mirror of encode driven by the range parser. The decoder rebuilds tables
incrementally with the same `_table_inc` rule as the encoder — lock-step
preserved (raw 65/68 idempotent contract).

---

## 3. F-A34-1..6 falsifier preregister (raw 71)

| ID       | Trigger                                                                | Action |
|----------|------------------------------------------------------------------------|--------|
| F-A34-1  | round-trip byte-eq fail on any selftest fixture                        | reject |
| F-A34-2  | RSS > 100 MB on 79 KB input (raw 42 mac jetsam)                        | reject |
| F-A34-3  | latency > 500 ms / KB on hexa interp                                   | reject |
| F-A34-4  | saving < byte-level baseline (must beat A29 v3 on text-heavy fixture)  | reject |
| F-A34-5  | cmix-ban audit: compile-time grep `neural\|mixer\|ZPAQ\|paq8\|cmix` ≠ 0 | reject |
| F-A34-6  | raw 18 self-host fixpoint AOT byte-identical fail                      | reject |

---

## 4. Selftest fixtures (PASS 3, 5/5)

| ID  | Name                       | Size  | Class         |
|-----|----------------------------|-------|---------------|
| F1  | English text 4 KB          | 4096  | text-heavy    |
| F2  | JSON structured 4 KB       | 4096  | structured    |
| F3  | Korean multibyte 4 KB      | 4096  | UTF-8 binary  |
| F4  | short passthrough          | <64   | identity      |
| F5  | cmix-ban audit (grep)      | n/a   | compile-time  |

Each fixture validates: (a) byte-eq round-trip, (b) saving ≥ 0 (no
expansion), (c) interp+AOT byte-identical (raw 18 self-host).

---

## 5. Module layout

`/Users/ghost/core/hexa-lang/self/stdlib/hxc_a34_sub_byte_arith.hexa`

| Section                              | LoC budget |
|--------------------------------------|------------|
| Header / consts / sigil              |   30       |
| base85 wire (A16-compat)             |  120       |
| Bit-stream pack/unpack               |   60       |
| 32-bit range coder primitives        |  150       |
| PPM-D order-3 context tables         |  120       |
| Encode walk + escape chain           |  100       |
| Decode walk + table rebuild          |  100       |
| Selftest 5 fixtures + cmix-ban audit |   80       |
| **Total**                            | **~760**   |

---

## 6. hexa-lang uint32 / bit-stream support assessment (§raw 18 retract trigger)

**Status**: PROCEED — hexa-lang has sufficient native primitives.

Inventory:

| Primitive            | Native support | Workaround / notes |
|----------------------|----------------|--------------------|
| 32-bit integer ops   | `i64` (de facto u32 carrier) — A16/A17 use `let mut low: i64` | Multiplication `cum * range` fits in i64 since `total ≤ 2^24` and `range ≤ 2^32`, product ≤ `2^56` < `2^63`. SAFE. |
| Bit-shift left/right | Hand-implemented via `* 256` / `/ 256` (byte-level) and `* 2` / `/ 2` (bit-level). Used widely in A16/A17. | OK — A17 `_push_bits`/`_pop_bits` proven idiom. |
| Bit-stream pack/unpack | A17 `_bits_to_bytes` / `_bytes_to_bits` proven idiom. | OK — direct reuse. |
| 32-bit XOR (for carry detection) | NOT NATIVE — `^` operator absent in hexa-lang. | Workaround: top-byte equality compare `(low / 2^24) == ((low+range) / 2^24)`, equivalent semantics for safe-emit. PROVEN in A16. |
| Bit-shift unsigned right | Use integer division `n / 2^k`, valid for non-negative ints. | OK — all i64 used non-negative. |

**Conclusion**: NO retract required. A16 already implements a 32-bit
byte-emitting range coder in pure hexa using these workarounds — A34 reuses
the same pattern with order-3 PPM context model swapped in (vs A16's
order-0).

**raw 18 self-host fixpoint**: `hxc_a34` AOT build will follow the same
pattern as `hxc_a17`/`hxc_a29`/`hxc_a32` — `.hxc_aot/hxc_a34` byte-identical
to interp output across 5 selftest fixtures.

---

## 7. raw 156 placement-axis declaration

A34 is a **secondary stacking axis** layered on top of the structural codecs
(A1–A15) and replaces the entropy-coder backend in the chain (substitutable
for A16 / A29 / A32). Recommended chain placement:

```
A1 (structural) → A11 (delta) → A18 (LZ77) → A34 (sub-byte arith + PPM-3)
```

Mutually exclusive with A16 / A29 / A32 (cannot stack — all three are entropy
coders consuming the same residual byte stream). A34 supersedes A16/A29/A32
on text-heavy class **iff** F-A34-4 passes (LIVE FIRE next tick).

---

## 8. Next-tick actions (PASS 4 LIVE FIRE — DEFERRED)

1. 5 MB stratified text-heavy corpus encode/decode round-trip.
2. 6-repo sweep aggregate vs N6 50.92% baseline.
3. F-A34-4 evaluation: A34 saving vs A29 v3 saving on identical fixtures.
4. A25 dispatch table route text-heavy → A34 if F-A34-4 PASSES.
5. raw 137 v8 verdict ONLY after LIVE FIRE confirms +5..+15pp design projection.

---

## 9. raw 91 honest C3 caveats (this tick)

- NO LIVE FIRE measured class lift.
- NO 6-repo sweep.
- NO 80% verdict claim.
- NO raw 137 v8 promotion.
- NO A25 dispatch table modification.
- 4 KB selftest fixtures are SMALL — production lift on 5 MB may differ
  (in-sample estimator overstates by 5..10 pp typically; A17 measured this
  pattern — projected 87% in-sample → 76% LIVE FIRE actual).
- Bounded LRU eviction policy is MIN-VIABLE (order-evict-first); a more
  sophisticated LRU may yield additional saving (DEFERRED to v2).
- First-tick scope: design doc + skeleton + selftest only. Production
  promotion is gated on LIVE FIRE + cross-corpus validation.
