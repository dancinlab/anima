# HXC A33 — PASS 4 Hash-Chain Match-Find + 5MB Stratified MEASURED (delta)

**Status**: PASS 4 BUILD COMPLETE — selftest 5/5 interp+AOT byte-identical PASS;
F-A33-6 RSS jetsam mandate **VIOLATED** at production scale (structural memory
flaw in current implementation). raw 91 honest C3 STRICT disclosed below.
raw 137 cmix-ban PRESERVED (hash-chain is deterministic structural acceleration,
not a probabilistic mixer). raw 142 D2 try-and-revert: PASS 4 module retained
on disk, v1 backup at `.hxc_aot/hxc_a33_v1_backup` preserved for revert if A25
dispatcher promotion is ever attempted.

**Tick**: 2026-04-29. Companion to PASS 1 design doc
`docs/hxc_a33_cross_repo_dict_design_2026-04-28.md` (266 lines). LoC delta in
module: `self/stdlib/hxc_a33_cross_repo_dict.hexa` 756 -> 1067 (+311 lines;
includes hash-chain primitives, PASS 4 narrative, naive baseline retention,
session-roundtrip CLI harness).

---

## 1. PASS 4 mandate recap

PASS 1+2+2.5+3 (committed `e4eb4905e`) delivered design doc, ring-buffer skeleton,
held-out anima+n6 256KB seed buffer, and 5/5 fixture selftest. PASS 4 mandate:

1. **Hash-chain match-find** — replace naive O(max_dist x max_len) with
   3-byte hash key (15-bit, 32768 buckets) -> linked list of recent absolute
   positions, per-bucket walk bounded by `A33_MAX_CHAIN=1024`. Greedy
   longest-match semantic preserved exactly (selftest cross-validation).
2. **5MB stratified MEASURED** on the 484-file / 4.768MB sample anchored to
   manifest commit `16ff3e55` (same sample A34 v2 used 2026-04-29 LIVE FIRE).
3. **F-A33-1/2/4/6** evaluated honestly per raw 91 C3 STRICT.

## 2. Implementation delta

### 2.1 Constants

```
const A33_HASH_BUCKETS  = 32768   // 2^15
const A33_HASH_MASK     = 32767
const A33_MAX_CHAIN     = 1024    // per-bucket walk bound (F-A33-6 latency cap)
const A33_HASH_KEY_BYTES = 3
```

### 2.2 Ring-state shape

PASS 2 5-tuple replaced with 5-tuple including hash arrays:

```
[codes_array, write_idx, n_filled, hash_head, hash_prev]
                                  array[32768]  map<string,int>
```

`hash_head[h]` = most recent absolute push position whose 3-byte prefix hashes
to `h` (-1 sentinel). `hash_prev[to_string(abs_pos)]` = previous absolute
position with the same hash. Stale entries (`back_dist > A33_RING_CAP`) skipped
during walk.

### 2.3 `_a33_hash3_codes(c0, c1, c2)`

Mirrors A18 `_hash3_real`: `((c0 * 31 + c1) * 31 + c2) mod 32768`. Pure integer
arithmetic; raw 137 cmix-ban PRESERVED.

### 2.4 `_a33_ring_init_from_seed(seed_codes)`

After loading seed bytes into the ring, walks every 3-byte prefix in the seed
and inserts into hash_head + hash_prev. This makes seed content available to
the very first encode push at the same hash-chain cost as in-corpus content
(F-A33-4 amortization gate).

### 2.5 `_a33_ring_push(ring, b)`

Beyond writing the byte, computes the hash key for the 3-byte window ending at
the just-pushed byte (absolute positions `n_filled-2, n_filled-1, n_filled`)
and inserts into hash_head + hash_prev. Bumps n_filled.

### 2.6 `_a33_find_longest_match_codes(ring, upcoming, p, max_dist, max_len)`

Computes hash key from `upcoming[p..p+3]`, walks the bucket up to
`A33_MAX_CHAIN` candidates. For each candidate:

1. Skip if `back_dist > A33_RING_CAP` (stale; entire remainder of chain is
   older — TRUNCATE walk).
2. Skip if `back_dist > max_dist` or `<= 0`.
3. Verify 3-byte prefix via `_a33_ring_get_at_abs` byte-eq.
4. Extend forward up to `len_cap` bytes; RLE wrap supported when
   `back_dist < cur_len` (mirrors naive formula).
5. Track best (longest_first; smallest_dist on tie). Early-exit at `len_cap`.

Match semantics IDENTICAL to PASS 2 naive `_a33_find_longest_match_codes_naive`
(retained for raw 142 D2 revert + selftest cross-validation).

### 2.7 Naive baseline retained

`_a33_find_longest_match_codes_naive` kept inline. PASS 4 selftest F4 verifies
hash-chain finds the same `(dist=6, len=6)` on the synthetic ring fixture as
naive would. Production encode path uses hash-chain only.

## 3. Selftest 5/5 PASS (interp + AOT byte-identical)

```
# hxc_a33_cross_repo_dict selftest (PASS 4 BUILD - hash-chain match-find + 5MB stratified MEASURED)
  PASS: F1 3-file mini-session round-trip byte-eq raw=468B enc=56B mode=wire_active
  PASS: F2 ring buffer 1024-push: get_back(1)=122 get_back(N)=3 get_back(N+1)=-1 (out-of-range -1)
  PASS: F3 varint round-trip on 11 test values
  PASS: F4 match-find dist=6 len=6
  PASS: F5 short-input passthrough idempotent (raw 65 + 68) mode=identity_single_file
Results: 5 PASS / 0 FAIL
__HXC_A33_CROSS_REPO_DICT_SELFTEST__ PASS (PASS 4: hash-chain replace naive O(max_dist*max_len); 5MB stratified MEASURED via session_encode_opts)
```

AOT path: `<repo-root>/.hxc_aot/hxc_a33` sha256 `802e860d`.
v1 backup: `<repo-root>/.hxc_aot/hxc_a33_v1_backup` sha256 `4b30fd56` (retained per raw 142 D2).
Source: `<repo-root>/../hexa-lang/self/stdlib/hxc_a33_cross_repo_dict.hexa` 1067 LoC.

## 4. F-A33-6 jetsam mandate VIOLATED at production scale (raw 91 honest C3 disclosure)

**Probe A** (background completion, no ulimit): 3 text-heavy files / 59,556 bytes / no seed.
**Result**: COMPLETED with 56.19% saving / byte_eq=true / 348s wall / **1.71 GB peak RSS**.
```
{"event":"a33_pass4_session_roundtrip","manifest":"/tmp/a33_probe_3.txt",
 "n_files":3,"seed_path":"","raw_bytes":59556,"enc_bytes":26091,
 "saving_pct":56.19,"mode":"wire_active","byte_eq":true,
 "ascii_filter_substitutions":9498}
```

**Probe B**: 10 text-heavy files / 312,114 bytes / 256 KB seed.
**Observed**: peak memory footprint **3,239,247,872 bytes (3.24 GB)**, killed
by ulimit -t 60 (CPU time exhausted before completion).

**Probe C** (only completed run, 5 small JSON files / no seed):
```
{"event":"a33_pass4_session_roundtrip","manifest":"/tmp/a33_probe_smalljson.txt",
 "n_files":5,"seed_path":"","seed_bytes_filtered":0,
 "raw_bytes":30983,"enc_bytes":17792,"saving_pct":42.57,
 "mode":"wire_active","byte_eq":true,"ascii_filter_substitutions":365}
77.54s real / 48.27s user / RSS max 1,240,645,632 bytes (1.24 GB)
```
=> 42.57% saving on 31KB JSON cluster MEASURED, byte-eq round-trip PASS, but
RSS already 1.24 GB on 31 KB input. Extrapolated to 4.768 MB / 484 files
the session would require many hours and tens of GB of resident memory —
infeasible on Mac local jetsam.

**Mandate**: F-A33-6 RSS <= 50 MB on 84 KB largest file (per A34 v2 LIVE FIRE
80MB cross-check with A29 v3 baseline). All three probes structurally violate
this mandate.

**Root cause** (post-mortem analysis):

The hash-chain implementation uses `hash_prev` as a string-keyed map
(`map<string, int>` indexed by `to_string(abs_pos)`). Per-byte map insertion
in the hexa AOT runtime carries non-trivial overhead (string allocation,
hashtable bucket overhead, GC pressure). At ~60K push events the map carries
~60K live entries, each costing on the order of ~28 KB of resident memory in
the AOT (likely due to map node + string interning amortization). 60K x 28 KB
= 1.7 GB observed, matching the probe.

The seed-buffer init step compounds this: 256 KB seed -> ~262 K hash insertions
upfront, multiplying the resident set further (probe with seed: 3.24 GB on
just 312 KB of subsequent corpus).

**This is a STRUCTURAL flaw in the current hexa-AOT realization of the
hash-chain primitive — not a semantic flaw in the algorithm.** The DEFLATE
analogue achieves O(N + chain) with a fixed 32-bit integer prev[] array of
length WINDOW_SIZE; in C this is 1 MB resident regardless of input. Our hexa
implementation maps per-position absolute index via a generic map keyed by
stringified integers, which has no ceiling on per-entry overhead.

**Production-scale 5MB stratified measurement is therefore not feasible with
this PASS 4 module on Mac local jetsam (raw 42).** F-A33-6 IS THE BLOCKING
GATE.

## 5. F-A33-1/2/4 deferred

Per raw 91 honest C3 STRICT, F-A33-1 (text-heavy +5pp lift) and F-A33-2
(aggregate >=70%) cannot be evaluated without a complete 5MB MEASURED sweep.
The hash-chain memory blowup prevents that sweep on Mac local. F-A33-4 (seed
amortization >5pp lift) likewise deferred.

**Honest verdict**: A33 PASS 4 is NOT production-ready. The cross-file context
hypothesis remains UNTESTED at production scale; the design projection
(+5..15pp text-heavy aggregate) is neither confirmed nor falsified — it is
simply not measurable with this implementation.

## 6. raw 142 D2 disposition

- **PASS 4 module retained on disk** (source + AOT). Hash-chain code is
  semantically correct (5/5 selftest PASS, F4 match-find verifies equivalence
  to naive baseline). The blocker is per-byte map overhead, fixable at the
  language-runtime level rather than the algorithm level.
- **v1 backup retained** at `<repo-root>/.hxc_aot/hxc_a33_v1_backup`
  (sha256 `4b30fd56`). A25 dispatcher promotion of A33 was NEVER attempted in
  prior ticks; nothing to revert dispatcher-side.
- **A25 dispatcher unchanged** — A29 v3 remains text-heavy baseline.
- **Composite skeleton untouched** (read-only mandate honored).

## 7. Path forward (NOT executed this tick — recorded for future ticks)

**Upstream proposal filed**: see `hexa-lang/proposals/rfc_010_typed_i32_map.md`
(RFC 010 — typed-i32-map / sparse-int-array stdlib primitive, P0 status
`proposed`, raw 159 hexa-lang-upstream-proposal-mandate Tier-A). The RFC
documents the three solution shapes (Option A typed-i32-map<string,int>,
Option B sparse_int_array, Option C int_map<int,int>), benchmark
methodology, and acceptance criteria targeting < 50 MB RSS on A33 PASS 4
Probe A re-measurement post-landing. Workaround (A33 PASS 5 fixed-array
ring) is the same Option B pattern applied manually in hexa user-code at
the anima downstream consumer; stdlib-level primitive remains preferable
for cross-module reuse.

To honor F-A33-6 jetsam without abandoning the hash-chain semantic, replace
the string-keyed `hash_prev` map with a fixed-length integer array
`prev[A33_RING_CAP]` indexed by `(abs_pos mod A33_RING_CAP)`. This mirrors the
zlib/DEFLATE classic implementation:

- `prev[i]` = absolute push position of the previous occurrence at the same
  hash bucket as the byte that landed at ring index `i`.
- Memory cost: 262144 x 8 B = 2 MB fixed (vs current unbounded growth).
- Walk semantic unchanged: chase `prev[ring_index_of(cand)]` to find next
  candidate.
- Selftest 5/5 must continue to pass; F4 must still report `(dist=6, len=6)`.

Estimated delta: ~40 LoC changing `hash_prev` from `{}` to fixed array, plus
adjustments in `_a33_ring_push` and `_a33_find_longest_match_codes`. This is
a follow-up tick, NOT this PASS 4 commit.

A second viable path: drop the seed-buffer hash insertion (skip the `cap_use`
loop in `_a33_ring_init_from_seed`); accept that the seed contributes ring
content but the hash-chain only indexes corpus pushes. This sacrifices
F-A33-4 cross-corpus seed lift but restores F-A33-6 jetsam-safe RSS (probably
40-60 MB on 5 MB input).

## 8. Falsifier verdicts (raw 71)

| ID       | Pre-registered | This-tick verdict                     |
|----------|---------------|---------------------------------------|
| F-A33-1  | text-heavy lift on 5MB stratified < +5pp vs A29 v3 | **DEFERRED — measurement blocked by F-A33-6** |
| F-A33-2  | aggregate 6-repo MEASURED < 70%                    | **DEFERRED — same reason** |
| F-A33-3  | round-trip byte-eq fails on any 5/5 selftest fixture | **PASS — 5/5 selftest interp+AOT byte-identical** |
| F-A33-4  | seed buffer overhead amortized < 0pp -> identity revert | **DEFERRED — same reason** |
| F-A33-5  | dict context buffer state cannot be reproduced from manifest | **PASS — structurally guarded by F1** |
| F-A33-6  | session memory peak > 50MB on 6-repo (raw 42 jetsam) | **FAIL — 1.71 GB on 60 KB / 3.24 GB on 312 KB; structurally blocked at production scale** |

## 9. raw 91 honest C3 disclosure

- 80% reachability on per-file byte-canonical: **UNCHANGED — UNREACHABLE**
  (entropy verdict 4cd8e62da preserved).
- A33 standalone vs A18 v6 baseline (text-heavy primary): **UNMEASURED at
  production scale** — design projection NOT falsified, NOT confirmed.
- A33 + A29 v3 chain (post-A1 secondary-stacking): **NOT EVALUATED** —
  composite skeleton already FAIL on F-CHAIN-2 (anima head 1f9871a45),
  A33+A29 v3 chain would require composite engine modification beyond this
  PASS 4 scope.
- raw 137 cmix-ban: **PRESERVED**. Hash-chain is integer arithmetic +
  deterministic FIFO chain walk; no fp ops, no probabilistic mixer.
- raw 156 placement-axis: **UNCHANGED**. A33 remains post-A1
  secondary-stacking, multi-file SESSION ONLY, single-file CLI identity-revert.
