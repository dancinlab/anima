# HXC A33 — Cross-Repo Dictionary LZ77 (rolling 256KB context buffer) Design

**Status**: DESIGN DOC + FIRST-TICK SKELETON (PASS 1+2+2.5+3 selftest only) — PASS 4 LIVE
FIRE + PASS 5 6-repo sweep DEFERRED. raw 91 honest C3 STRICT. raw 137 cmix-ban
NOT strengthened (no 80% verdict claimed at first tick).

**Author tick**: 2026-04-29 (post 4cd8e62da n6 entropy floor witness; post A29 v3
standalone 66.22% MEASURED ceiling; post A19 v2 +0.15pp slice / 0.00pp scale-out).

**Raw mandate scope**: raw 9 hexa-only / raw 18 self-host fixpoint / raw 47 cross-repo /
raw 65+68 idempotent byte-eq / raw 71 falsifier-preregister / raw 91 honest C3 STRICT /
raw 137 cmix-ban / raw 142 D2 try-and-revert / raw 156 placement-axis.

---

## 1. Motivation — entropy verdict path #1 mandate

The 2026-04-28 n6 entropy floor measurement
(`state/format_witness/2026-04-28_anima_n6_entropy_floor_measurement.jsonl`,
commit 4cd8e62da) reported the following on 22 sample files:

- per-file byte-canonical Shannon H_0/H_1/H_3/H_4 measurements MEASURED.
- 80% reachability verdict on per-file byte-canonical = **FALSE**.
- enumerated paths to 80%:
  1. **cross_repo_dictionary_LZ77** — 64KB+ window over concatenated corpus.
  2. context model order ≥ 5 (PPM-D class).
  3. cross-format chain composition.

**A33 attacks path #1 directly.** The hypothesis is that per-file algorithms cap
out near the per-file H_0..H_4 floor, but a CONCATENATED-CORPUS view exposes
inter-file redundancy that no per-file pass can capture. A19 v2 already attempted a
cross-corpus shared dictionary but operates on a different axis:

| dimension              | A19 v2 (existing)                       | A33 (this design)                              |
|------------------------|-----------------------------------------|------------------------------------------------|
| context model          | per-corpus shared dict (256-entry top-N)| LZ77 rolling 256KB ring buffer                 |
| reference scope        | top-N tokens 3..32 bytes                | arbitrary back-reference within window         |
| cross-file boundary    | dict is global; per-file substitution   | back-reference CAN span previous-N file content|
| wire format            | per-file `^Z<idx>` 2-byte ref           | per-stream `^h<dist><len>` LZ77 match          |
| amortization model     | 1 dict over N files                     | sliding window over concatenated corpus        |
| measurement on n6      | +0.15pp slice / 0.00pp scale-out        | PROJECTED text-heavy +5..15pp aggregate        |

A19 v2 saturated because top-N=125 (UTF-8-safe cap) cannot encode long literal
suffixes that share a prefix with an EARLIER file. A33 lifts this constraint via
a true LZ77 sliding window: every byte that occurred within the last 256KB of
the concatenated corpus is back-referencible.

---

## 2. A33 architecture spec

### 2.1 Concatenated-corpus rolling buffer model

**Invariant**: encode and decode share an IDENTICAL 256KB ring buffer state at
each file boundary. The buffer is a circular byte array of capacity
`A33_RING_CAP = 262144` bytes; new bytes overwrite the oldest position
modulo capacity.

**File ordering**: sub-stream within an A33 session is a sequence of files
processed in a manifest-declared order. The manifest is part of the wire
contract; without manifest reproducibility decode fails.

**Boundary semantics**: on transition from file_k to file_{k+1}, the ring
buffer state is preserved (NOT reset). File_{k+1}'s first byte may match a
substring inside file_{k-2}; the encoder emits a back-reference whose
distance crosses two file boundaries.

**Initialization**: first byte of first file in manifest sees an empty
window. To avoid pathological cold-start, A33 supports a SEED BUFFER —
a 256KB pre-loaded representative byte sequence (PASS 2.5 below).

### 2.2 LZ77 match semantics

- **Window**: previous 256KB of concatenated input.
- **Match length range**: `A33_MATCH_MIN = 4` .. `A33_MATCH_MAX = 258`
  (mirrors DEFLATE; below 4 bytes the reference cost dominates).
- **Distance range**: 1 .. 262144 (full ring window).
- **Wire reference**: `^h <dist:varint> <len:varint>` — sigil ^h is the
  match-anchor; varint format = continuation-bit LEB128 unsigned.
- **Reference cost (typical)**: dist varint 2-3 bytes + len varint 1-2 bytes
  + sigil 1 byte = 4-6 bytes per match. Net saving = match_len - ref_cost,
  which is non-negative iff match_len ≥ 5 (worst case) or ≥ 4 (best case).

### 2.3 Sigil ^h selection (raw 92, raw 156)

- ^V/^W (A23 sparse PPM), ^X (A24), ^Y (A26 v2), ^Z (A19 v2), ^\\ (A26 v3),
  ^a (A11 cross-row delta), ^b (A30 BWT), ^c (A32 static Huffman),
  ^L/^M/^N/^O/^P/^Q (A18 LZ-PPM family) all reserved.
- ^h is LOWERCASE alphabetic, distinct from all uppercase ^A..^Z reserved
  control characters AND from ^a..^c lowercase already in use. Selected
  for "history" mnemonic (LZ77 history buffer).
- Sigil byte value: chr(104) = 'h' — this is a PRINTABLE ASCII letter, NOT a
  control byte. A33 wire is therefore raw 92 / raw 157 sigil-line printable
  compatible WITHOUT base64 expansion of the body. Match references are
  encoded as printable escape `^h<dist_b64><len_b64>` to preserve
  printability when the input is ASCII text; binary-byte inputs may still
  contain a literal 'h' character which requires escape via `^h^` doubled
  prefix.

### 2.4 Placement axis (raw 156)

A33 = **post-A1 secondary-stacking** wrapper over the existing dispatcher. The
A33 path activates ONLY when:
- input is part of a multi-file A33 session (manifest declares ≥ 2 files), AND
- session is invoked via `live-fire-cross-repo` subcommand (not single-file
  CLI dispatcher), AND
- session aggregate raw bytes ≥ A33_MIN_SESSION_BYTES = 4096.

For single-file CLI invocation A33 reverts to identity passthrough (raw 142
D2 try-and-revert), matching the A19 v2 honest fallback behavior.

### 2.5 Decode reproducibility contract

Decoder requires THREE inputs:
1. **manifest** — ordered list of file identifiers (paths or hashes).
2. **seed buffer** — optional 256KB pre-state (if encoder used one).
3. **encoded byte stream** — concatenated wire bytes per manifest order.

Decoder reconstructs the ring buffer state byte-by-byte as it emits decoded
bytes. Byte-eq round-trip on (manifest, seed, stream) → original concatenated
corpus is the PRIMARY first-tick gate (F-A33-3).

---

## 3. PASS-by-PASS first-tick scope

### PASS 1 — design doc (THIS document)

Architecture spec: ring buffer + cross-file boundary semantics + manifest
reproducibility + sigil ^h justification + placement axis. Falsifier
preregister section 4 below.

### PASS 2 — skeleton module (~600 LoC)

`/Users/ghost/core/hexa-lang/self/stdlib/hxc_a33_cross_repo_dict.hexa`:
- ring buffer primitives: `_a33_ring_init`, `_a33_ring_push`,
  `_a33_ring_get_byte_at_offset_back`.
- match-find primitives: `_a33_find_longest_match` — at write-cursor
  position, scan back through ring (bounded distance) for longest matching
  substring of upcoming input bytes (length capped at MATCH_MAX).
- varint primitives: `_a33_varint_encode`, `_a33_varint_decode` (LEB128
  continuation-bit unsigned).
- session encode: `a33_session_encode(manifest, files_text, seed_buffer)`
  → returns (encoded_stream, byte_eq_witness).
- session decode: `a33_session_decode(manifest, stream, seed_buffer)`
  → returns reconstructed concatenated text.
- single-file CLI: `a33_encode_single` / `a33_decode_single` — raw 142 D2
  try-and-revert returns identity for single-file invocation.

### PASS 2.5 — seed buffer construction

`/Users/ghost/core/anima/state/format_witness/_a33_seed_buffer_2026-04-28.bin`:
- 256KB byte sequence built from concatenation of 5 representative files:
  - 2 anima JSONL audit files (mixed-real class, ~80KB).
  - 2 n6 stratified samples (text-heavy + json-heavy, ~120KB).
  - 1 hexa-lang stdlib module (synthetic-rep class, ~56KB).
- Total exact = 262144 bytes (truncated/padded to ring capacity).
- Hash recorded in design doc + first-tick witness; decoder MUST receive
  byte-identical seed for round-trip to hold.

The seed buffer is a HONEST in-sample bias: it is derived FROM the corpus
A33 will measure against. For the first-tick selftest this is acceptable
because we measure round-trip byte-eq, NOT saving% (in-sample saving
bound only, NOT wire saving claim per raw 91 honest C3). For PASS 4
LIVE FIRE the seed buffer must be either (a) shipped as wire overhead
(charged against saving) or (b) replaced with a held-out
representative buffer to validate cross-corpus generalization.

### PASS 3 — 5/5 fixture selftest (interp + AOT byte-identical)

5 selftest fixtures:
- **F1**: 3-file mini-session (12B + 64B + 128B). Cross-file back-reference
  expected on file 2 → file 1 prefix; round-trip byte-eq on concatenation.
- **F2**: ring-buffer primitive — push 300KB of distinct bytes, verify
  `_a33_ring_get_byte_at_offset_back(distance=N)` returns the correct byte
  for various N including ring-wrap boundary (N=262143, N=262144 should
  return invalid).
- **F3**: varint round-trip — encode/decode integers {0, 127, 128, 16383,
  16384, 262143, 262144, 65535} byte-identical.
- **F4**: match-find primitive — given a ring buffer with known content
  and a known upcoming-bytes prefix, verify the longest-match function
  returns the correct (distance, length) pair, bounded by MATCH_MAX.
- **F5**: short-input passthrough — single-file 24-byte input via
  `a33_encode_single` returns identity (raw 65/68; below MIN_SESSION_BYTES
  threshold).

PASS 3 verdict requires interp 5/5 + AOT 5/5 + interp_stdout_sha256 ==
aot_stdout_sha256 (raw 18 self-host fixpoint).

### PASS 4 — DEFERRED

LIVE FIRE 6-repo concatenated-corpus measurement DEFERRED to subsequent
tick. F-A33-1, F-A33-2, F-A33-5 gates DEFERRED. raw 91 honest C3 STRICT:
no aggregate saving claim at first tick.

### PASS 5 — DEFERRED

6-repo sweep + manifest reproducibility validation across 6 repo sub-corpora.
A28 TRANSCEND-FORBIDDEN: must be MEASURED on real corpus, not projection.

---

## 4. Falsifier preregister (raw 71)

| ID       | spec                                                                                              | retire condition                                |
|----------|---------------------------------------------------------------------------------------------------|-------------------------------------------------|
| F-A33-1  | text-heavy class lift on 5MB stratified concatenated corpus < +5pp vs A29 v3 standalone           | reject A33 text-heavy lever; first-tick DEFERRED|
| F-A33-2  | aggregate 6-repo MEASURED < 70% (A29 v3 baseline 66.22% + projected +5pp floor)                   | reject A33 cross-repo hypothesis; DEFERRED      |
| F-A33-3  | round-trip byte-eq fails on any 5/5 selftest fixture                                              | reject A33 first-tick (raw 65/68 violation)     |
| F-A33-4  | seed buffer overhead amortized < 0pp on 6-repo (i.e., raw 142 D2 always reverts to identity)      | retract seed-buffer model; DEFERRED             |
| F-A33-5  | dict context buffer state cannot be reproduced from manifest alone (decode irreproducibility)     | retract decode contract; structurally guarded   |
| F-A33-6  | session memory peak > 50MB on 6-repo concatenated corpus (raw 42 jetsam violation)                | reject A33 256KB ring buffer; DEFERRED          |

F-A33-3 is the PRIMARY first-tick gate. F-A33-1/2/4/6 are LIVE FIRE gates
(subsequent-tick). F-A33-5 is structurally guarded by the encoder/decoder
ring buffer mirror invariant (verified inside selftest F1 round-trip).

---

## 5. raw 91 honest C3 STRICT disclosure

A33 first-tick scope is INTENTIONALLY narrow:
- design doc + skeleton + 5/5 selftest only.
- in-sample saving estimator only; NO wire saving claim.
- design projection (text-heavy +5..15pp aggregate) is PROJECTED, NOT
  MEASURED.
- seed buffer is in-sample biased (derived from anima + n6); generalization
  gate deferred to PASS 4 with held-out buffer.
- NO 80% verdict claim on any axis.
- NO raw 137 cmix-ban strengthening.
- NO commit if any selftest fails.

A33 is a CANDIDATE algorithm-class shift on entropy path #1. First-tick
landing establishes the architectural skeleton; whether A33 actually
closes the 13.78pp gap from A29 v3 standalone (66.22%) to the 80% Pareto
target is a SUBSEQUENT-TICK MEASURED question.

---

## 6. raw 137 cmix-ban compliance

A33 = LZ77 deterministic match-find (greedy longest-match, byte-equality
test, integer compare) + LEB128 varint integer encoding + ring buffer
modulo arithmetic. NO fp ops. NO neural mixer. NO non-deterministic
similarity. Encode + decode both deterministic (raw 65/68 idempotent:
same (manifest, seed, files) → byte-identical encoded stream).

---

## 7. raw 47 cross-repo compliance

A33 module lives in `hexa-lang` (algorithm implementation). Design doc +
witness ledger + seed buffer artifacts live in `anima` (byte-corpus
authority). No cross-repo write inversion; pattern mirrors A19, A30, A32
companion-document pattern.

---

## 8. References

- entropy verdict witness: `/Users/ghost/core/anima/state/format_witness/2026-04-28_anima_n6_entropy_floor_measurement.jsonl`
- A19 v2 sibling: `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a19_cross_file_dict.hexa`
- A29 v3 deflate baseline: `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a29_deflate.hexa`
- A18 v6 LZ-PPM 32KB window: `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a18_lz_ppm_order4.hexa`
- A30 BWT companion landing: `/Users/ghost/core/anima/state/format_witness/2026-04-28_a30_bwt_mtf_first_tick.jsonl`
- A32 static Huffman companion landing: `/Users/ghost/core/anima/state/format_witness/2026-04-28_a32_static_huffman_first_tick.jsonl`
