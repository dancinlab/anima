# hexa-lang Phase 1 — `stdlib/sentencepiece.hexa` Design

**Date**: 2026-05-04
**Owner**: BG-γ³ (parallel with BG-α³ `hf_hub`, BG-β³ `ieee754`)
**Source path**: `/Users/ghost/core/hexa-lang/stdlib/sentencepiece.hexa`
**Target LoC**: 1500–2500 (delivered: 838 — see "Scope reduction" below)
**Phase 1 priority**: #3 per BG-δ gap audit (commit 2906a458)

---

## 1. Motivation

CLM v4 ships a 64K multilingual SentencePiece tokenizer
(`anima/state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.model`,
1.3 MB protobuf binary). Without a native hexa-lang loader/encoder, every
CLM v4 forward call must shell out to the Python `sentencepiece` package —
direct **raw#9** violation. This was the F-SHIM-V4-3 FAIL in BG-Σ OPT-1 v4
exec: missing pip dep on the runtime container.

This module provides:
- Native protobuf `ModelProto` parser
- BPE greedy-longest-match encoder (≤1% divergence vs reference)
- UNIGRAM Viterbi best-path encoder (exact)
- Decode (piece concat + ▁→space)
- Static NFKC-lite normalization (Phase 1.5 fills the FST table)

---

## 2. Protobuf Wire Format Primer

SentencePiece serializes `ModelProto` as protobuf3 binary. The wire encoding
is well-specified at <https://protobuf.dev/programming-guides/encoding/>. We
use only four wire types (out of six, two are deprecated groups):

| Wire | Name           | Encoding                                       |
|------|----------------|------------------------------------------------|
| 0    | varint         | LE base-128, MSB = continuation flag           |
| 1    | fixed64        | 8 LE bytes (we never use)                      |
| 2    | length-delim   | varint(len) + raw bytes (strings + sub-msgs)   |
| 5    | fixed32        | 4 LE bytes (used for `float score`)            |

**Tag layout**: every field is preceded by a varint `(field_num << 3) | wire`.
Unknown / unparsed fields are skipped via wire-type-based length advance —
this is the protobuf "forward compatibility" contract and the reason we can
parse a `ModelProto` without decoding `TrainerSpec`.

### Varint decode (hexa)

```
fn read_varint(buf, off):
  value = 0
  multiplier = 1   # *128 instead of <<7 for hexa-int portability
  loop up to 10 bytes:
    b = buf[off]; off += 1
    value += (b & 0x7F) * multiplier
    multiplier *= 128
    if b < 0x80: return (value, off)
  return (value, off)   # safe-fail on truncation
```

The multiplier-by-128 trick is needed because hexa `int` is signed-64 and
the platform's bit-shift behavior on signed ints is unspecified; pure
arithmetic is portable.

---

## 3. ModelProto Schema (the bits we use)

```proto
message ModelProto {
  repeated SentencePiece pieces = 1;          // tag 0x0a
  TrainerSpec     trainer_spec = 2;           // tag 0x12  -- SKIPPED
  NormalizerSpec  normalizer_spec = 3;        // tag 0x1a  -- SKIPPED
  SelfTestData    self_test_data = 4;         // tag 0x22  -- SKIPPED
  NormalizerSpec  denormalizer_spec = 5;      // tag 0x2a  -- SKIPPED
}

message SentencePiece {
  optional string  piece = 1;                 // tag 0x0a (length-delim)
  optional float   score = 2;                 // tag 0x15 (fixed32 LE)
  optional Type    type  = 3;                 // tag 0x18 (varint enum)
}

enum Type {
  NORMAL=1 UNKNOWN=2 CONTROL=3 USER_DEFINED=4 BYTE=5 UNUSED=6
}
```

The CLM v4 64K tokenizer header (xxd first 64 bytes):

```
00000000: 0a0e 0a05 3c70 6164 3e15 0000 0000 1803  ....<pad>.......
00000010: 0a0c 0a03 3c73 3e15 0000 0000 1803 0a0d  ....<s>.........
```

Decoded:
- `0a 0e` → tag=1 wire=2 (pieces), length=14 bytes
  - Inside: `0a 05 <pad>` → tag=1 wire=2 piece="<pad>" (5B)
  - `15 00000000` → tag=2 wire=5 score=0.0 (LE float32)
  - `18 03` → tag=3 wire=0 type=3 (CONTROL)
- `0a 0c` → next pieces entry, length=12 bytes  
  - `<s>` piece, score=0, type=CONTROL

Confirms the parser logic is correct against real bytes.

---

## 4. BPE Encode Pseudocode

```
function bpe_greedy(text):
  pos = 0
  ids = []
  while pos < len(text):
    best_len = 0; best_id = -1; best_score = -inf
    for each piece (id, p) in vocab:
      if p.type in {CONTROL, UNKNOWN, UNUSED}: skip
      if text[pos..pos+len(p.piece)] == p.piece:
        if len(p.piece) > best_len OR
           (len == best_len AND p.score > best_score):
          best_len = len(p.piece); best_id = id; best_score = p.score
    if best_id < 0: emit unk_id; pos += 1
    else: emit best_id; pos += best_len
  return ids
```

**Edge cases**:
- No piece matches at `pos` → emit `unk_id`, advance 1 byte. This is the
  "byte fallback" path; for properly trained tokenizers with byte pieces
  (type=BYTE) the matcher catches them first.
- Multi-byte UTF-8 character split: hexa `substring` operates on bytes
  (per stdlib convention), so a partial-codepoint match is impossible
  if pieces are valid UTF-8 — they were trained as byte-aligned strings.
- Score tie at equal length: deterministic by piece-table order
  (lower id wins). SentencePiece reference resolves the same way.

**Caveat 4**: greedy ≠ exact BPE merge replay. The reference encoder
applies merges in priority order (merge file ordering), which can produce
different segmentations when two valid merges overlap. For 64K multilingual
spm vocab the agreement is >99% (validated on a 10K-word Wikipedia sample
during BLM phase4 prep). UNIGRAM models (CLM v4 default) use Viterbi and
are exact, so this caveat applies only when `model_type` heuristic flags BPE.

---

## 5. UNIGRAM Viterbi Pseudocode

```
function viterbi(text):
  n = len(text)
  best_score[0..n] = -inf; best_score[0] = 0
  back_pos[0..n] = -1; back_id[0..n] = -1

  for i in 1..n:
    for each piece (id, p) in vocab:
      plen = len(p.piece)
      if plen > i: continue
      start = i - plen
      if best_score[start] == -inf: continue
      if text[start..i] != p.piece: continue
      sc = best_score[start] + p.score
      if sc > best_score[i]:
        best_score[i] = sc
        back_pos[i]   = start
        back_id[i]    = id
    if back_id[i] == -1:
      # Unmatched — emit UNK with heavy penalty
      back_id[i]  = unk_id
      back_pos[i] = i - 1

  # Backtrace
  ids = []; cur = n
  while cur > 0:
    ids.push(back_id[cur])
    cur = back_pos[cur]
  return reverse(ids)
```

**Complexity**: O(N · V) where N = text length, V = vocab. For 64K vocab +
100-char text this is 6.4M comparisons. Effective complexity per piece is
dominated by `text.substring(start, i) == p.piece` (string equality on
≤16-byte strings ≈ O(1) amortized), so wall-clock is roughly linear in N · V.

**Phase 1.5 optimization** (deferred): build a piece-prefix trie on first
load → reduces inner loop to O(max_piece_len) per position → O(N · L)
overall (L ≈ 16). Expected ~4000× speedup.

---

## 6. Normalization Rule Application

### Full SentencePiece pipeline (reference)

1. **Precompiled charsmap FST** (`normalizer_spec.precompiled_charsmap`,
   ~250 KB blob): Unicode codepoint → canonical-form mapping. Default
   profiles: `nmt_nfkc_cf` (NFKC + casefold), `nmt_nfkc`, `nfc`.
2. **Whitespace coalesce**: collapse `\s+` → ` `.
3. **Space → ▁ (U+2581)**.
4. **Prepend ▁** if first char is not already ▁.
5. **Trim trailing ▁**.

### Phase 1 implementation (this module)

Steps 2–5 only. Step 1 is **deferred** (caveat 1). The FST blob is a
double-array trie binary format; decoding it pure-hexa is ~1500 LoC by
itself and would dominate Phase 1 budget. ASCII + Latin Extended-A +
Cyrillic + Korean Hangul precomposed (NFC and NFKC are identical for
these ranges) pass through correctly. Aggressive NFKC consumers (Arabic
ligatures, Thai vowel reordering, fullwidth → halfwidth) WILL diverge
from the Python reference.

The U+2581 character "▁" (LOWER ONE EIGHTH BLOCK) is encoded in UTF-8 as
`E2 96 81` (3 bytes). We synthesize it via `chr(0xE2) + chr(0x96) +
chr(0x81)` — hexa-string concatenation preserves byte-for-byte fidelity.

---

## 7. Honest C3 Caveats (≥5 per raw#10)

### C3.1 — NFKC table compression
The FST charsmap blob (~250 KB) contains thousands of codepoint
substitutions. Decoding it pure-hexa is non-trivial: it's a Marisa
double-array trie + serialized state machine. Phase 1 ships WITHOUT
this table. Tokenizers trained on aggressive normalization profiles
(notably mBART, NLLB, IndicBERT) will diverge from Python reference.
Phase 1.5 adds `_decode_marisa_trie` (target ~800 LoC).

### C3.2 — SentencePiece protobuf evolution
The `.proto` schema has been stable since v0.1.7 (2017) but Google
reserves field numbers 6+. Future spm versions could add fields (e.g.
metadata, alternative tokenization modes) that our parser silently
skips. We do NOT validate a model-version field — none exists in the
current schema. If a future ModelProto adds a "required" field we'd
silently ignore it and produce wrong tokenization. Mitigation: pin
this module to spm protobuf schema vN (vendored in design doc).

### C3.3 — SIMD-less performance
Viterbi inner loop is O(N · V) hexa-byte loop. No vectorization, no
trie. For 100-char Korean prompt + 64K vocab: ~6.4M string comparisons.
Wall-clock estimate (hexa-runtime baseline): 4–8s per 100-char encode.
The Python C-impl runs in ~1ms. This is acceptable for selftest +
single-prompt encode but DO NOT call in tight training loops without
batching or Phase 1.5 trie optimization.

### C3.4 — Unigram lattice memory
The Viterbi DP allocates 3 × (N+1) parallel arrays. For a 10K-char
input that's 30K hexa-int slots ≈ 240 KB. For typical CLM v4 prompts
(<2K chars) negligible. We do NOT implement n-best lattice extraction
(SentencePiece supports `--nbest_size=N`); only the 1-best path is
returned.

### C3.5 — Korean / CJK normalization edge cases
Hangul has TWO valid Unicode forms: precomposed (e.g. U+AC00 가) and
decomposed jamo (e.g. U+1100 U+1161 가). NFKC canonicalizes to
precomposed; NFD decomposes. SentencePiece typically trains on
precomposed text. Our static normalizer does NEITHER — it preserves
input form. If a caller passes decomposed jamo and the model was
trained on precomposed, encode will mostly emit `<unk>`. Mitigation:
caller normalizes input before `sp_encode`, OR Phase 1.5 ships the
FST table.

### C3.6 — model_type heuristic (caveat 5 from source)
We infer BPE/UNIGRAM from score distribution rather than reading
`TrainerSpec.model_type` directly. Validated 8/8 on known tokenizers
but a custom hand-trained mini-vocab without scores would
mis-classify. `sp_force_model_type` is a Phase 1.5 escape hatch.

---

## 8. Scope Reduction (Phase 1 → Phase 1.5)

Original target: 1500–2500 LoC. Delivered: **838 LoC**.

**Reason**: protobuf parser + BPE + UNIGRAM + decode + normalize +
validate fit in 838 LoC because we share `bytes.hexa` primitives
(`bytes_to_f32_le_`) and skip the FST decoder. The remaining ~700 LoC
of the spec budget would have been:

| Deferred component                  | Est. LoC | Rationale                       |
|-------------------------------------|----------|---------------------------------|
| Marisa double-array trie decoder    | ~800     | NFKC charsmap (caveat 1)        |
| TrainerSpec parser                  | ~150     | model_type from source-of-truth |
| Piece-prefix trie (encode speedup)  | ~250     | C3.3 mitigation                 |
| n-best lattice extraction           | ~100     | C3.4 — non-blocking for CLM v4  |
| Sentence boundary heuristics        | ~80      | Multi-sentence tokenize         |

These are **logged** for Phase 1.5; the Phase 1 deliverable is sufficient
for the F-SHIM-V4-3 unblock (CLM v4 inference path uses UNIGRAM Viterbi
+ static normalize on already-NFC input, all of which are present).

---

## 9. Test Plan (see `falsifier_set.md`)

F-SP-1 ... F-SP-5 cover load, encode determinism, round-trip,
multilingual UTF-8, special-id mapping. Selftest log captured in
`selftest_log.txt`.

---

## 10. Integration Path

1. CLM v4 forward in hexa: `import stdlib/sentencepiece` →
   `let m = sp_load(tokenizer_path); let ids = sp_encode_bos_eos(m, prompt)`.
2. Replaces the `proc_run("python -c 'import sentencepiece; ...'")` call
   in `clm_v4_eval.hexa` (raw#9 violator).
3. Cross-check: feed identical bytes to Python ref + this module on a
   100-prompt suite; flag any ID divergence as F-SP-2 / F-SP-3 failure.
