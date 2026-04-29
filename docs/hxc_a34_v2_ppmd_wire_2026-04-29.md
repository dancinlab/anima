# HXC A34 v2 — PPM-D Escape Chain Wire (Routing Delta)

**Date**: 2026-04-29
**Phase**: 14 P0 (post-A34 v1 first-tick)
**Sigil**: `^l` (UNCHANGED — v2 is a routing modification, not a new module)
**Module path**: `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a34_sub_byte_arith.hexa`
**Wire version**: `v=arith-v1` (preserved — v2 is encoder-side only; decoder
must remain backward-compatible since the on-wire bit-stream is what changes)
**v1 baseline (in-sample 4 KB fixtures)**: F1 English 5%, F2 JSON 8%,
F3 Korean -4%
**v1 honest C3 caveat (quote)**: "PASS 3 ships order-0 cumulative arithmetic
coding only; PPM-D escape chain (PASS 2 tables built+exercised) is **not
yet routed into the coder narrow** — DEFERRED to v2".

**Compliance preserved**: raw 9 hexa-only · raw 18 self-host fixpoint ·
raw 42 mac jetsam (LRU 16384 retained) · raw 65 + 68 idempotent ·
raw 71 falsifier-preregistered · raw 91 honest C3 STRICT · raw 92 sigil-line
(^l unchanged) · raw 137 cmix-ban (single deterministic Howard escape, NO
mixing) · raw 156 placement-axis.

---

## 0. Honest framing (raw 91 C3 STRICT)

This is **scope-locked to in-sample 5/5 fixture selftest**. NO 6-repo LIVE
FIRE sweep this tick. NO 80% verdict claim. NO raw 137 v8 promotion. NO
A25 dispatch promotion. The design projection of +5..+15pp text-heavy vs
A29 v3 is **reachable only after v2 wires the escape chain** and remains
non-claimed at LIVE FIRE level until measured next tick.

**v1 → v2 lift measurement**: in-sample only on the 4 KB selftest fixtures
F1/F2/F3. v2 saving must be **≥ v1 saving** on every fixture or raw 142 D2
try-revert engages (v1 baseline remains the ship).

---

## 1. v1 → v2 routing delta (the only change)

### 1.1 v1 (current) — order-0 cumulative narrow, PPM tables built but unused

```
v1 a34_encode body:
  build PPM tables c0/c1/c2/c3 (PASS 2 lookup loop, 4 orders)
  build_order0_freq(buf) -> freq[256]
  build_cum(freq) -> cum[257]
  for q in 0..n:
    rc_encode_sym(state, bits, cum[byte], cum[byte+1], total)   <-- ORDER-0 ONLY
  rc_finish; bits_to_bytes; b85; emit "^l<header><payload>"
```

PPM tables `c1/c2/c3` are populated and `_table_inc` runs every byte, but
the range-coder narrow consumes `cum[]` which is **order-0 frequency**.
Ship saving on 4 KB English = 5%, 4 KB JSON = 8%, 4 KB Korean = -4%.

### 1.2 v2 (this tick) — full Howard escape chain into coder narrow

```
v2 a34_encode body:
  init c0/c1/c2/c3 EMPTY (build incrementally to match decoder state)
  for q in 0..n:
    sym = bytes[q]
    if q < 3:
      // bootstrap — uniform [0,256) order-0 narrow
      rc_encode_sym(state, bits, sym*BOOT, (sym+1)*BOOT, BOOT*256)
      _ppm_update_all_orders(c0/c1/c2/c3, q, sym)
      continue

    encoded = false
    for order in [3, 2, 1, 0]:
      ctx = ctx_key(bytes, q, order)
      if _table_count(ctx, sym) > 0:
        // HIT — encode in this order's narrow
        T = _table_total(ctx)
        U = _table_distinct(ctx)
        // Howard method-D: per-symbol mass = count(s); escape mass = U
        // total mass = T + U
        cum_lo, cum_hi = _ppm_cum_for_sym(tbl, ctx, sym)
        rc_encode_sym(state, bits, cum_lo, cum_hi, T + U)
        encoded = true
        break
      else:
        // MISS — emit escape symbol over (T, T+U, T+U) i.e. last U/(T+U) mass
        T = _table_total(ctx)
        U = _table_distinct(ctx)
        if T > 0:
          rc_encode_sym(state, bits, T, T + U, T + U)
        // else: empty context contributes no escape bit, fall through
        // (Howard exclusion: symbols seen at higher order are excluded
        // from lower order's mass — first-tick v2 ships WITHOUT exclusion;
        // exclusion is a v3 enhancement)

    if not encoded:
      // full miss to order-(-1) — uniform [0, 256)
      rc_encode_sym(state, bits, sym*BOOT, (sym+1)*BOOT, BOOT*256)

    _ppm_update_all_orders(c0/c1/c2/c3, q, sym)

    // raw 42 LRU cap — preserved from v1
    if q % 4096 == 0 and _ctx_size(c0,c1,c2,c3) > A34_LRU_CAP: BREAK
```

### 1.3 Decoder mirror

Decoder rebuilds tables incrementally using the same `_ppm_update_all_orders`
rule, walking the same order-3 → 0 cascade and using `_rc_decode_target` per
order to disambiguate "hit at this order" vs "escape to next order" by
inspecting whether the target lands in the symbol mass `[0, T)` or escape
mass `[T, T+U)`.

```
v2 a34_decode body:
  init c0/c1/c2/c3 EMPTY (mirror encoder)
  state = rc_dec_new(bits)
  for q in 0..n_bytes:
    if q < 3:
      target = rc_decode_target(state, BOOT*256)
      sym = target / BOOT
      rc_decode_advance(state, bits, sym*BOOT, (sym+1)*BOOT, BOOT*256)
    else:
      decoded = false
      for order in [3, 2, 1, 0]:
        ctx = ctx_key(bytes_decoded, q, order)
        T = _table_total(ctx); U = _table_distinct(ctx)
        if T == 0: continue   // empty context — fall through
        target = rc_decode_target(state, T + U)
        if target < T:
          // hit
          sym = _ppm_sym_for_target(ctx, target)
          cum_lo, cum_hi = _ppm_cum_for_sym(ctx, sym)
          rc_decode_advance(state, bits, cum_lo, cum_hi, T + U)
          decoded = true
          break
        else:
          // escape
          rc_decode_advance(state, bits, T, T + U, T + U)
      if not decoded:
        target = rc_decode_target(state, BOOT*256)
        sym = target / BOOT
        rc_decode_advance(state, bits, sym*BOOT, (sym+1)*BOOT, BOOT*256)
    out_bytes.push(sym)
    _ppm_update_all_orders(c0/c1/c2/c3, q, sym)
```

### 1.4 Header impact

**Header is unchanged shape** — no `freq=<b85>` field is needed in v2 since
the model is built incrementally on decode (mirrors encode). For backward
parser compatibility in this tick we **keep** the `freq=` field but populate
it with order-0 marginal stats from the input buffer; decoder ignores it
when present. v2 rewrite header optimization (drop freq= field) deferred
to v3 to avoid wire-version churn.

Wire string remains:
```
# a34:s1 v=arith-v1 n=<input_bytes> b=<bit_count> freq=<base85>\n^l<payload>
```

### 1.5 LoC delta budget

- v1: 928 lines
- v2 estimated: ~1100 lines (+170)
- New helpers: `_ppm_cum_for_sym`, `_ppm_sym_for_target`, `_ppm_update_all_orders`,
  encoder/decoder rewrite (~120 lines), boot constant `A34_BOOT = 65535`
  (uniform mass per symbol for order--1 fallback; chosen so total = 256 * 65535
  ≤ 2^24 frequency cap).

---

## 2. Howard escape mass — explicit math (raw 137 reaffirmation)

For each context `ctx` with `U` distinct symbols seen and `T` total mass:

- For symbol `s` with `count(s) > 0`:
  - `cum_lo(s) = sum( count(s') for s' < s )`
  - `cum_hi(s) = cum_lo(s) + count(s)`
  - emitted over total `T + U`
  - **decoded mass**: `count(s) / (T + U)` ← Howard method-D
- Escape symbol: emitted over `[T, T + U)` i.e. mass `U / (T + U)`.

**This is a SINGLE deterministic predictor.** Each byte is encoded under
exactly ONE (order, ctx) pair's distribution — the first cascade level
where the symbol appears, OR the order-(-1) uniform fallback. No two
predictions are ever blended, switched, or mixed. **raw 137 cmix-ban
envelope (2026-04-27 strengthening) is satisfied**:

- NO context blending (no weighted sum across orders)
- NO neural net component
- NO ZPAQ-style switch-mixer
- NO paq8-style adaptive blend
- NO switching predictors
- Cleary-Witten 1984 + Howard 1993 textbook = pure deterministic integer math

The cascade order-3 → order-2 → order-1 → order-0 → uniform is **not**
mixing — it is **fall-through**, and at each cascade level only the symbol
mass OR the escape mass is consumed, never a convex combination.

---

## 3. F-A34-v2 falsifier preregistration (raw 71)

| ID | Trigger | Evaluated this tick |
|---|---|---|
| F-A34-V2-1 | round-trip byte-eq fail on any of 5/5 fixtures | YES (selftest) |
| F-A34-V2-2 | v2 saving < v1 saving on F1 OR F2 OR F3 (text-heavy) | YES (selftest comparison) |
| F-A34-V2-3 | RSS > 100 MB on 79 KB input (raw 42 jetsam) | NO — DEFERRED LIVE FIRE |
| F-A34-V2-4 | cmix-ban audit `grep neural\|mixer\|ZPAQ\|paq8\|cmix` ≠ 0 implementation hits | YES |
| F-A34-V2-5 | raw 18 self-host AOT byte-identical fail | YES (post-build sha256 cross-check) |
| F-A34-V2-6 | latency > 500 ms / KB on hexa interp | NO — DEFERRED LIVE FIRE |

Failure on F-A34-V2-1 / -2 / -4 / -5 = **immediate raw 142 D2 try-revert**,
v1 module restored, no commit.

---

## 4. Saving target reachability (in-sample fixtures only — NOT a claim)

| Fixture | v1 saving | v2 in-sample target | rationale |
|---|---|---|---|
| F1 English 4 KB | 5% | 15..20% | "the quick brown fox" repeats — order-3 ctx hit rate ~70% after warmup (`the ` → `q`/`b`/`f` deterministic); per-symbol mass concentrates near 1.0 mass |
| F2 JSON 4 KB | 8% | 25..40% | Field name repetition — order-3 ctx like `"id`/`"na`/`alu` has nearly deterministic next byte; high P(hit) → narrow interval |
| F3 Korean 4 KB | -4% | ~10% (near-zero) | UTF-8 multibyte E1-EF prefix → 80-9F continuation pattern (order-3 catches the prefix→continuation transition); NOT projected near +5..+15pp territory because Korean Unicode code points have ~14 bits/sample entropy already |
| F4 short 5B | 0% (passthrough) | 0% (passthrough) | raw 65/68 idempotent guard — `< MIN_BYTES = 64` |
| F5 cmix-ban audit | PASS | PASS | grep gate over body |

**These numbers are reachability targets, not measurements.** Actual v2
saving is reported by the selftest output and recorded in §5 of the
witness ledger — only in-sample, and only on these 4 fixtures. The
+5..+15pp design projection vs A29 v3 is **5 MB stratified LIVE FIRE**
territory and remains DEFERRED.

---

## 5. Non-overlap with in-flight work

- **A33** (cross-repo dict, sigil ^h, owner: in-flight) — module
  `hxc_a33_cross_repo_dict.hexa` is **NOT modified** this tick.
- **A35** (source-transform, sigil ^o, first-tick yesterday) — not touched.
- **A25 dispatch table** — NOT promoted this tick. v2 lift is in-sample
  only; promotion requires LIVE FIRE.

---

## 6. Implementation plan (PASS 2 of this tick)

1. Replace `a34_encode` body with v2 cascade encoder (order-3 → 0 → uniform).
2. Replace `a34_decode` body with v2 cascade decoder mirror.
3. Add `_a34_encode_force` v2 update (selftest path — same cascade).
4. Add `_a34_decode_to_bytes` v2 update (Korean fixture path).
5. Add `_ppm_cum_for_sym(ctx, sym, tbl_count, tbl_keys, tbl_rank) -> [lo,hi]`.
6. Add `_ppm_sym_for_target(ctx, target, tbl_count, tbl_keys, tbl_rank) -> int`.
7. Add `_ppm_update_all_orders(c0/c1/c2/c3, k0..k3, r0..r3, bytes, q, sym)`.
8. Constant `A34_BOOT = 65535` for order--1 fallback.
9. Selftest: 5/5 fixtures unchanged; new assertion v2 saving ≥ v1 saving.
10. AOT rebuild: same pipeline `hexa_v2 → clang -O2`; sha256 cross-check.

---

## 7. Witness ledger plan (PASS 3 of this tick)

`/Users/ghost/core/anima/state/format_witness/2026-04-29_a34_v2_ppmd_wire.jsonl`

Keys: `event`, `verdict` (FIRST_TICK_V2_BUILD_PASS or REVERT_TO_V1),
`module_path`, `module_sha256_v1`, `module_sha256_v2`,
`aot_path`, `aot_sha256_v2`, `selftest_5_5`, `v1_v2_saving_lift`,
`compliance` (raw 9/18/42/65/68/71/91/92/137/156),
`F_A34_V2_1..6` evaluations, `next_tick_actions` (LIVE FIRE deferred).

NO 6-repo sweep field. NO 80% verdict field. NO raw 137 v8 field.
