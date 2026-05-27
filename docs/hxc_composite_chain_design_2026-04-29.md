# HXC Composite Chain Design — A33 + A34 + A35 Stack (3-Path Entropy-Verdict Integration)

**Date**: 2026-04-29
**Phase**: Post-N6-entropy-floor verdict commit `4cd8e62da` (witness
`state/format_witness/2026-04-28_anima_n6_entropy_floor_measurement.jsonl`).
**Author tick**: design doc only — NO module file modifications, NO commit
to `tool/hxc_composite_chain.hexa`, NO LIVE FIRE, NO witness ledger entry.
**Scope**: 5-stage chain SPECIFICATION + 3 chain options + decode manifest +
F-CHAIN-1..8 falsifier preregistration + implementation roadmap (PASS 1
design only).
**Compliance**: raw 9 hexa-only · raw 18 self-host fixpoint · raw 33
commit-msg English · raw 42 mac jetsam (RSS<100MB) · raw 47 cross-repo ·
raw 65 + 68 idempotent byte-eq · raw 71 falsifier-preregister · raw 91
honest C3 STRICT · raw 92 sigil-line · raw 137 cmix-ban · raw 142 D2
try-revert · raw 156 placement-axis (3 axes orthogonal).
**Non-overlap**: prior `hxc_composite_chain_design_2026_04_28.md` covered
A29+A30+A23 (deprecated chain candidates). This document is a **NEW chain
proposal** over A33 (sigil `^h`, in-flight) + A34 v1 (sigil `^l`, 5/5 PASS) +
A35 (sigil `^o`, 6/6 PASS Stage 1). All three modules read-only consumed.

---

## 0. Honest framing (raw 91 C3 STRICT)

This design is the **fifth turn** in the entropy-verdict chain: prior turns
landed A33 first-tick (cross-repo dictionary LZ77, sigil `^h`, in-flight), A34
v1 sub-byte arithmetic coder skeleton (5/5 PASS, AOT byte-identical, F1 +5%
F2 +8% F3 -4%), A35 source-transform v1 Stage 1 column-reorder (6/6 PASS,
F1 -2% header overhead dominated). This turn is the **composite chain
specification** that integrates all three paths into one decode manifest +
one chain dispatcher.

**Honest disclosures**:

1. **No saving claim**. The 80% target reachability remains FALSE per the
   `4cd8e62da` global verdict on per-file byte-canonical encoding. This
   document specifies the COMPOSITE CHAIN as the design hypothesis for
   reaching the 80% target via the **simultaneous union** of the three
   verdict-listed paths, NOT a measurement that 80% is reached.
2. **Per-stage saving estimates are PROJECTION**, not measured. A33 first-tick
   in-flight; A34 v1 measured F1 +5% / F2 +8% / F3 -4% (in-sample, 4KB
   fixtures); A35 Stage 1 measured F1 -2% (header-overhead-dominated on
   small fixtures). The composite saving is hypothetical.
3. **Stage interaction unknown**. Each stage was measured in isolation. A35
   then A33 then A34 may exhibit destructive interference — e.g., A35
   column-reorder rewrites byte distribution such that A33's 256KB ring
   buffer fingerprints become useless. **Cross-stage correlations are
   pre-registered F-CHAIN falsifiers**, not assumed-positive.
4. **PASS 1 design only this turn**. PASS 2 skeleton implementation in
   `tool/hxc_composite_chain.hexa` is deferred to a separate turn under raw
   91 C3 strict. PASS 3 selftest 9-fixture is deferred to PASS 2 follow-on.
   PASS 4 LIVE FIRE on n6/anima 6-repo sweep is deferred indefinitely until
   PASS 1+2+3 land.
5. **cmix-ban (raw 137) compatibility is structural, not empirical**. A34
   = single deterministic order-3 PPM-D with NO context mixer. A33 LZ77 +
   A29 v3 Huffman are deterministic single-stage. A composite of
   deterministic stages is itself deterministic — but the F-CHAIN-8
   falsifier guards against the chain dispatcher being mis-classified as
   a mixer if it inspects multiple per-stage outputs and selects.

---

## 1. Motivation — entropy verdict path integration

### 1.1 The 4cd8e62da verdict

```
{"global_verdict":"80%_REACHABILITY_FALSE_PER_FILE_BYTE_CANONICAL — Per-file
Shannon entropy floor (H_0..H_4) is 27-50% across both repos, all <80%.
Reaching 80% requires (a) corpus-spanning shared dictionary OR (b) sub-byte
coding (arithmetic/range coder operating on bits) OR (c) source-level
transformation reducing source H_n itself."}
```

The verdict enumerates THREE algorithmic axes. Each prior tick attacked one:

| Path | Module | Sigil | First-tick status (current) |
|------|--------|-------|------------------------------|
| #1 cross-repo dictionary LZ77 (256KB rolling, cross-file boundary) | A33 | `^h` | in-flight |
| #2 corpus-aware arithmetic coder (sub-byte order-3 PPM-D) | A34 v1 | `^l` | 5/5 PASS, F1 +5% / F2 +8% / F3 -4% |
| #3 source-level transformation (schema delta + tokenizer) | A35 v1 | `^o` | 6/6 PASS Stage 1 column-reorder, F1 -2% |

**Per-axis ceiling hypothesis**: each axis on its own caps short of 80%.
A35 (path #3) lifts only on schemaful jsonl. A34 (path #2) gains 3.3
bit/byte on text-heavy via fractional-bit but cannot exploit cross-file
context. A33 (path #1) gains cross-file LZ77 within a 256KB window but
cannot drop H_n itself.

**Composite hypothesis**: simultaneous integration of all three axes into
one chain may reach ~80% on text-heavy + json-heavy + mixed by combining
their orthogonal saving sources (raw 156 placement-axis 3-axis orthogonal).

### 1.2 Placement-axis orthogonality (raw 156)

The three modules attack DIFFERENT pipeline placements:

```
        ┌──────────────────────────────────────────┐
        │ A35 source-transform (^o)                │  ← pre-A1-raw
        │   schema_detect → column_reorder + delta  │     (axis #3: H_n itself)
        └──────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────┐
        │ A1..A15 structural strip (existing)      │  ← raw byte canonical
        └──────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────┐
        │ A18 v6 / A19 v2 / A33 (^h)               │  ← post-A1 byte-stream
        │   text-heavy LZ77 / per-corpus dict /     │     (axis #1: cross-file
        │   cross-repo 256KB rolling                │      LZ77 context)
        └──────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────┐
        │ A29 v3 length-codes Huffman (existing)   │  ← post-LZ77 entropy
        └──────────────────────────────────────────┘
                          │
                          ▼
        ┌──────────────────────────────────────────┐
        │ A34 sub-byte arithmetic coder (^l)       │  ← post-Huffman OR
        │   replacing or layered with A29           │     replacing Huffman
        │   (order-3 PPM-D, bit-stream)             │     (axis #2: sub-byte)
        └──────────────────────────────────────────┘
                          │
                          ▼
                [composite wire bytes]
```

The **3 axes are orthogonal** because:

- A35 modifies *what the bytes mean* (source representation). H_n of the
  input drops because schema redundancy is collapsed at the source.
- A33 exploits *what bytes have appeared elsewhere* (cross-file context).
  Saving comes from references into the rolling buffer — INDEPENDENT of
  the per-file H_n.
- A34 exploits *fractional bits* (sub-byte coding). Saving comes from
  bypassing the 8-bit-per-symbol envelope — INDEPENDENT of byte-level
  context model order.

Because the three axes are orthogonal, their savings are MULTIPLICATIVE
rather than additive: if A35 reduces input by `s_35`, A33 reduces the
post-A35 stream by `s_33`, and A34 reduces the post-A33 stream by `s_34`,
the composite saving is `1 - (1 - s_35)(1 - s_33)(1 - s_34)`. This is the
**central design hypothesis** that the chain may reach 80%.

---

## 2. Five-stage chain specification

The composite chain is a **5-stage pipeline**, each stage with its own
sigil + decode manifest entry:

| Stage | Module | Sigil | Placement | Operation |
|-------|--------|-------|-----------|-----------|
| 1 | **A35** | `^o` | pre-A1-raw | source-transform (column-reorder + delta + tokenize) on schemaful inputs; identity passthrough on schemafree |
| 2 | **A1..A15** | (no new sigil; existing structural family) | raw byte canonicalization | structural strip / unicode normalization / line-end normalization |
| 3 | **A18 v6 / A19 v2 / A33** | `^h` (A33), `^Z` (A19), existing (A18) | post-A1 LZ77 family | best-of-N dispatcher: A18 v6 text-heavy LZ77 / A19 v2 per-corpus dict / A33 cross-repo 256KB rolling |
| 4 | **A29 v3** | existing | post-LZ77 entropy | length-codes Huffman |
| 5 | **A34** | `^l` | post-Huffman OR replacing Huffman | sub-byte arithmetic coder, order-3 PPM-D |

### 2.1 Stage-1 A35 source-transform (pre-A1-raw)

- Input: raw file bytes (no prior canonicalization).
- Operation: A35 schema-detect; if schemaful jsonl → column-reorder +
  delta-encode shared field-names + tokenize repeated values → emit
  transformed source bytes. If schemafree → identity passthrough (raw 142
  D2 try-revert applies if transformed > original).
- Output: transformed source bytes (still text-domain, NOT compressed).
- Wire prefix on chain manifest: `^o` if active; else absent.

### 2.2 Stage-2 A1..A15 structural strip (existing)

- Input: stage-1 output bytes.
- Operation: existing structural family (line-end normalization, unicode
  NFC, BOM strip, …) — unchanged behavior. **No new module.**
- Output: canonical raw bytes ready for byte-stream compression.
- Wire prefix on chain manifest: existing structural-family declarations.

### 2.3 Stage-3 LZ77 best-of-N (post-A1)

- Input: stage-2 output bytes.
- Operation: dispatcher chooses among:
  - A18 v6 (text-heavy LZ77 — proven +2.09pp on text-heavy class).
  - A19 v2 (per-corpus shared dict 256-entry top-N, sigil `^Z`).
  - A33 (cross-repo 256KB rolling LZ77, sigil `^h`, in-flight).
  - Choice is per-file or per-stream by min-byte-length wins.
- Output: byte-canonical LZ77 wire (header + sigil + b64url body).
- Wire prefix on chain manifest: `lz_choice=a18|a19|a33` field.

### 2.4 Stage-4 A29 v3 length-codes Huffman (post-LZ77)

- Input: stage-3 output bytes.
- Operation: A29 v3 length-codes Huffman entropy stage (post-LZ77 backref
  length distribution → canonical Huffman). Existing module, unchanged.
- Output: byte-canonical entropy wire.
- Wire prefix on chain manifest: `huff=a29v3`.

### 2.5 Stage-5 A34 sub-byte arithmetic coder

- Input: stage-4 output bytes (or stage-3 bytes if A29 is bypassed).
- Operation: A34 v1 single-deterministic order-3 PPM-D bit-stream. Two
  sub-modes:
  - **Mode L (layered)**: A34 entropy-codes A29's Huffman bitstream byte
    projection. Saving comes from sub-byte residual on Huffman codewords.
  - **Mode R (replacing)**: A34 entropy-codes stage-3 output directly,
    skipping A29. Saving comes from sub-byte coding of LZ77 literal +
    backref token stream.
  - Choice per-file or per-class (text-heavy → Mode R, json-heavy → Mode L
    per A35 schema delta interaction).
- Output: byte-canonical wire (final composite output).
- Wire prefix on chain manifest: `ac_mode=L|R, ac_model=ppm3`.

### 2.6 Round-trip identity (raw 65 + 68)

For all input `s`:
```
decode_chain(encode_chain(s)) == s
```
Decode runs stages in reverse: 5 → 4 (or skip if Mode R) → 3 → 2 → 1.
Each decode stage is the inverse of its encode counterpart and is
unchanged from the per-module decoder. **No new decode logic** is
required at the chain dispatcher level — the dispatcher reads the
manifest, then calls the per-module decoders in reverse order.

---

## 3. Three chain options compared

### 3.1 Option A — linear chain (fixed)

**Specification**: `A35 → A1..A15 → (LZ77 dispatcher) → A29 v3 → A34 Mode L`.
Every input takes every stage. raw 142 D2 try-revert applies AT EACH STAGE
INDIVIDUALLY: if A35 inflates schemafree input, A35 emits identity for that
file but the chain continues. A34 Mode L vs Mode R is fixed at the option
level (Option A picks Mode L).

**Pros**:
- Simplest decode manifest (5 stages always present).
- Minimum dispatcher logic.
- Composite saving = product of per-stage savings (clean math).

**Cons**:
- Mode-L vs Mode-R choice is class-specific; Option A loses the +2..3pp
  Mode-R gain on text-heavy.
- A35 pays header overhead on every schemafree file (mitigated by Stage-1
  D2 revert).
- LZ77 dispatcher within Stage-3 is itself a best-of-N — Option A inherits
  but does not exploit.

### 3.2 Option B — best-of-N dispatch with try-revert at each junction

**Specification**: at each stage boundary (1→2, 2→3, 3→4, 4→5), run
`stage_encode` and `identity_passthrough` in parallel; emit whichever is
shorter. **Per-junction raw 142 D2 try-revert.** This is the strongest
saving guarantee but requires 2× encode CPU per junction.

```
def encode_chain_optionB(s):
    s1_t = A35_encode(s);  s1 = min_len(s1_t, s)
    s2_t = A1_15_encode(s1); s2 = min_len(s2_t, s1)
    # Stage-3 has internal best-of-N (A18/A19/A33)
    s3_t = LZ77_dispatch(s2); s3 = min_len(s3_t, s2)
    s4_t = A29v3_encode(s3); s4 = min_len(s4_t, s3)
    # Stage-5 mode L vs Mode R within best-of-N
    s5_L = A34_encode_modeL(s4)
    s5_R = A34_encode_modeR(s3)  # replacing A29
    s5 = min_len(s5_L, s5_R, s4, s3)
    return s5
```

**Pros**:
- Strict raw 142 D2 protection — chain saving ≥ best single stage.
- Mode-L vs Mode-R chosen per-file empirically.
- Worst-case = identity revert at every junction.

**Cons**:
- 2× encode CPU per junction = ~5× total CPU vs Option A.
- Decode manifest must record which stages were active per-file (more
  complex schema).
- F-CHAIN-7 try-revert ordering bug risk (see §5).

### 3.3 Option C — A25-style type-aware top-level routing

**Specification**: an A25-style top-level type classifier inspects the input
and routes to one of three pre-defined chain paths:

| Class | Route | Stages |
|-------|-------|--------|
| text-heavy (.md, .txt) | TEXT | A1..A15 → A18 v6 LZ77 → A34 Mode R |
| json-heavy (.jsonl, schemaful) | JSON | A35 → A1..A15 → A19 v2 dict → A29 v3 → A34 Mode L |
| mixed (.hexa, .py) | MIXED | A1..A15 → A33 cross-repo LZ77 → A29 v3 → A34 Mode L |

**Pros**:
- Fast dispatch (single classifier read, then linear chain per class).
- Each route is hand-tuned for its class — A35 only invoked where it can
  win (json-heavy).
- A25 dispatcher is already proven (76.24% aggregate baseline).

**Cons**:
- Class boundaries can mis-route (e.g., a `.md` with embedded jsonl block).
- Chain path is FIXED per class — no per-file fallback if a particular
  schemaful jsonl file is short and A35 hurts.
- Adding a new chain route requires re-training A25 classifier.

### 3.4 Placement-axis matrix (raw 156 declaration)

For each stage, placement is declared per raw 156:

| Stage | Module | Placement axis (raw 156) | Orthogonal? |
|-------|--------|-------------------------|-------------|
| 1 | A35 | pre-A1-raw (axis #3 source H_n) | yes |
| 2 | A1..A15 | byte canonicalization (existing axis) | yes (independent of #1#2#3) |
| 3 | A18 v6 / A19 v2 / A33 | post-A1 byte-stream LZ77 (axis #1 cross-file context) | yes |
| 4 | A29 v3 | post-LZ77 byte entropy (axis #4 byte-Huffman, NOT one of verdict's 3 paths but existing baseline) | yes (orthogonal to #1#2#3) |
| 5 | A34 | post-Huffman OR replacing Huffman (axis #2 sub-byte) | yes |

**3-axis orthogonality verified**: stages 1, 3, 5 attack the three verdict
paths #3, #1, #2 respectively. Stages 2, 4 are existing pipeline (not new
verdict paths). The 3 attack axes are pairwise orthogonal: stage 1 changes
the source, stage 3 references prior bytes, stage 5 escapes the byte
envelope.

### 3.5 Try-revert ordering (raw 142 D2 fallback locations)

Per chain option, D2 fallback can fire at:

| Junction | Option A | Option B | Option C |
|----------|----------|----------|----------|
| 1→2 (post-A35) | identity if A35 inflates | min_len gate | per-class only |
| 2→3 (post-A1..A15) | n/a (existing always-shorter) | min_len gate | n/a |
| 3→4 (post-LZ77) | n/a | min_len gate | n/a |
| 4→5 (post-A29 vs A34 Mode-R bypass) | fixed Mode L | min_len gate (L vs R vs A29) | per-class fixed |
| Final wire vs identity raw | n/a (chain composite assumed shorter) | top-level min_len gate | top-level min_len gate |

**F-CHAIN-7 risk**: in Option B, junction `i→i+1` may revert AFTER stage `i+1`
already consumed the stage-`i` output. Mitigation: each junction must
fix the choice BEFORE calling the next stage. Specifically:

```
s_i_choice = min_len(stage_i_encode(s_{i-1}), s_{i-1})  # revert HERE
s_{i+1}_input = s_i_choice                              # NEXT stage sees it
```

Implementation must NOT pipeline the encodes or the choice can lag.

---

## 4. Decode manifest schema

### 4.1 Per-stage manifest entry

The composite wire begins with a manifest header followed by the stage-5
output. Manifest schema (line-delimited, header-only, raw 92 sigil-line):

```
# cc:s2 v=composite-v2 chain=<A|B|C> n=<input_bytes> stages=<5>
# cc:stage1 mode=<active|identity> sigil=^o param=<json>
# cc:stage2 mode=<active|identity> family=A1..A15 param=<json>
# cc:stage3 mode=<active|identity> sigil=<^h|^Z|^a18|identity> param=<json>
# cc:stage4 mode=<active|identity> family=A29v3 param=<json>
# cc:stage5 mode=<active|identity> sigil=^l param=<json> ac_mode=<L|R>
^d<base64url-stage5-payload>
```

Sigil `^d` (lowercase, raw 92 sigil-line, disjoint from `^a/^b/^c/^h/^l/^o/^Z`).
The `chain=` field is mandatory: `A` / `B` / `C` per option choice.

### 4.2 Per-stage parameter blob

Each `param=<json>` is a small JSON object recording stage-specific
hyperparameters needed for decode. Examples:

- Stage 1 A35 param: `{"schema_id": "anima_n6_entropy_floor/1",
  "column_order": [...], "tokenize_dict_idx": 7}`.
- Stage 3 A33 param: `{"ring_cap": 262144, "manifest_file_order": [...],
  "ring_state_seed": "..."}` (CRITICAL — see §4.3).
- Stage 5 A34 param: `{"order": 3, "carry_byte_count": 3,
  "ppm_state_init": "zero"}`.

Decode reads each param to instantiate the per-stage decoder. Param
ambiguity → F-CHAIN-3 falsifier.

### 4.3 File-order invariance (A33 ring buffer dependency)

A33 is the first stage (in chain stage 3) to depend on **previous file
bytes** within the rolling 256KB window. This breaks the per-file
independence assumption of stages 1, 2, 4, 5. The composite manifest
MUST record the file order:

```
{"manifest_file_order": ["file_a.md", "file_b.md", ...]}
```

Decode order MUST exactly match encode order. If A33 is active in stage 3,
decode of file `i` requires the ring buffer state AFTER decoding files
`0..i-1`. **Random-access decode** of any single file is not supported
when A33 is active.

**F-CHAIN-4 falsifier**: file-order-dependency breaks portability — if
the user wants random-access single-file decode, A33 MUST be disabled in
stage 3 (Option B falls back to A18 v6 or A19 v2 for that subset).

### 4.4 Byte-eq round-trip 5-stage chain test plan

PASS 3 selftest (deferred to follow-on tick) will verify byte-eq round-trip
on **9 fixtures** (3 classes × 3 sizes):

| Fixture | Class | Size | Expected dominant stage |
|---------|-------|------|-------------------------|
| F1: anima_milestone_excerpt.md | text-heavy | 4KB | A18 v6 + A34 Mode R |
| F2: n6_paper_excerpt.md | text-heavy | 8KB | A18 v6 + A34 Mode R |
| F3: anima_roadmap_excerpt.md | text-heavy | 16KB | A33 + A34 Mode L |
| F4: atlas_signals_jsonl.jsonl | json-heavy | 4KB | A35 + A19 v2 + A29 v3 + A34 Mode L |
| F5: clay_iter_065.jsonl | json-heavy | 4KB (small) | A35 + A19 v2 + A34 Mode L |
| F6: anima_witness_jsonl.jsonl | json-heavy | 16KB | A35 + A33 + A34 Mode L |
| F7: anima_n6_entropy_measure.hexa | mixed | 24KB | A33 + A29 v3 + A34 Mode L |
| F8: small_eeg_state.json | json-heavy | 1.3KB | identity-revert dominant |
| F9: korean_paper_excerpt.md | text-heavy korean | 4KB | A18 v6 + A34 Mode R |

PASS 3 gate = 9/9 byte-eq round-trip (F-CHAIN-1 falsifier).

---

## 5. 80% close path analysis (PROJECTION, NOT MEASURED)

### 5.1 Per-stage saving estimate (raw 91 honest C3 in-sample only)

The following table is **PROJECTION based on prior-tick in-sample
estimators**. NONE of these are MEASURED on the composite chain.

| Stage | Saving estimator | Source |
|-------|------------------|--------|
| Stage 1 A35 (json-heavy) | +20..30% | A35 design doc Stage 1 column-reorder projection on 4..16KB schemaful jsonl |
| Stage 1 A35 (schemafree) | -2..0% | A35 v1 measured F1 -2% header-overhead on small schemafree |
| Stage 3 A18 v6 (text-heavy) | +40..47% | A18 v6 measured 47% saving on text-heavy 6-repo 2026-04-28 |
| Stage 3 A33 (mixed/cross-file) | +10..20% (in-sample) | A33 design projection on cross-repo 256KB rolling |
| Stage 3 A19 v2 (json-heavy) | +0..3% | A19 v2 measured +0.15pp slice / 0.00pp scale-out 2026-04-28 |
| Stage 4 A29 v3 (post-LZ77) | +5..10% | A29 v3 measured 66.22% standalone on text-heavy small |
| Stage 5 A34 Mode L (post-Huffman) | +3..6% | A34 v1 measured F1 +5% / F2 +8% / F3 -4% (4KB fixtures) |
| Stage 5 A34 Mode R (replacing Huffman, post-LZ77) | +6..12% | A34 PPM-D theoretical lift over single-Huffman, NOT MEASURED |

### 5.2 Additive vs multiplicative composite saving

For independent stages, composite saving is multiplicative:
```
s_total = 1 - product_i (1 - s_i)
```

If three orthogonal stages each save 30%:
```
s_total = 1 - (0.7)^3 = 1 - 0.343 = 65.7%
```

If they each save 40%:
```
s_total = 1 - (0.6)^3 = 1 - 0.216 = 78.4%
```

**80% requires either (a) all three stages averaging ≥ ~42% saving, OR
(b) one stage at 60%+ and other two at ~30%, OR (c) heavy class-specific
routing where the in-class composite product reaches 0.8.**

### 5.3 Per-class projection

| Class | Hypothesized chain | Projected composite saving (PROJECTION) |
|-------|-------------------|-----------------------------------------|
| text-heavy | A18 v6 (+47%) + A34 Mode R (+8%) on stage-3 LZ77 output | `1 - (0.53)(0.92) = 51.2%` (single A18 dominates) → +60-70% if A33 cross-file lifts another +10pp on top |
| json-heavy small | A35 (+25%) + A19 v2 (+2%) + A29 v3 (+8%) + A34 (+4%) | `1 - (0.75)(0.98)(0.92)(0.96) = 35%` (small files header-dominated) |
| json-heavy large schemaful | A35 (+30%) + A33 cross-file (+15%) + A29 v3 (+8%) + A34 Mode L (+5%) | `1 - (0.7)(0.85)(0.92)(0.95) = 48%` → reach 90%+ ONLY if A35 alone gives +60% on highly schemaful jsonl |
| mixed (.hexa, .py) | A33 cross-repo (+15%) + A29 v3 (+8%) + A34 Mode L (+5%) | `1 - (0.85)(0.92)(0.95) = 26%` (per-file H_4 floor on .hexa is ~4.7 bit/byte = 41% saving theoretical max via byte coder) |

**Honest projection summary**:
- text-heavy: **60-70% projection**, NOT 80%.
- json-heavy large schemaful: **48..90%+ projection** depending on A35 saving on highly schemaful
  long jsonl (the ONLY class where 80% is theoretically reachable).
- mixed: **70%+ projection requires sub-byte fractional gain on top of byte
  ceiling** — A34 Mode L lift on top of A29 v3 floor is the load-bearing
  axis.

### 5.4 80% reachability hypothesis

**Design hypothesis** (NOT a claim): the 80% target is achievable via
composite chain on the **json-heavy large schemaful subset only**, and is
NOT achievable on text-heavy or mixed with the proposed 5-stage chain.

**Honest reservation (raw 91)**: the in-sample saving estimates may be
optimistic by 5..15pp under PASS 4 LIVE FIRE. Stage interaction is
unmeasured. The chain may fail to advance the 76.24% A25 dispatcher
baseline by even 1pp. **No promotion claim is made by this design.**

---

## 6. F-CHAIN-1..8 falsifier preregistration (raw 71)

The composite chain experiment is pre-registered with EIGHT falsifiers.
Each falsifier is a measurable condition that, if observed, falsifies a
load-bearing assumption.

### 6.1 F-CHAIN-1 — chain round-trip byte-eq fail

**Condition**: any of the 9 selftest fixtures fails byte-eq round-trip
(`decode(encode(s)) != s`).

**Severity**: BLOCKING. PASS 3 selftest cannot pass; chain is rejected
at PASS 1 design level if any predicate-level analysis shows an unrecoverable
information loss path.

### 6.2 F-CHAIN-2 — chain saving < single-stage best (composite hurts)

**Condition**: composite encoded length (final wire) is LARGER than the
best single-stage encoded length on the same input. I.e., the 5-stage
chain inflates relative to the best of {A18, A29, A33, A34, A35} alone.

**Severity**: HIGH. Triggers raw 142 D2 top-level identity revert. Composite
chain is catalogued as "anti-lever, do not promote" per `2026-04-28
composite chain skeleton precedent.

### 6.3 F-CHAIN-3 — manifest decode-side ambiguity

**Condition**: composite header parses ambiguously (e.g., two stages claim
the same sigil; param JSON missing required key for decode).

**Severity**: BLOCKING. Header schema MUST be unambiguous by construction.
Sigil `^d` is reserved disjoint; per-stage sigils are chained inside the
manifest (`^o`, `^h`/`^Z`, `^l`) but the ENVELOPE sigil is `^d`.

### 6.4 F-CHAIN-4 — file-order dependency breaks portability

**Condition**: a user attempts random-access single-file decode when A33
was active in stage 3, and decode produces non-byte-eq output because the
ring buffer state cannot be reconstructed.

**Severity**: MEDIUM. Mitigation: chain manifest declares
`random_access=false` when A33 is active; tools that need random-access
disable A33 at encode time.

### 6.5 F-CHAIN-5 — chain RSS > 300MB cumulative

**Condition**: cumulative resident set size during encode of a 4KB fixture
exceeds 300MB (raw 42 mac jetsam triggers at 100MB per stage; cumulative
budget is 5 stages × 60MB = 300MB).

**Severity**: HIGH on macOS targets. A33 ring buffer alone is 256KB but
LZ77 hash table can balloon to 16MB+. A34 PPM-D state can grow to ~20MB.
A35 schema dictionary ~5MB. Cumulative budget is plausible but not yet
measured.

### 6.6 F-CHAIN-6 — chain latency > 2000ms/KB

**Condition**: encode latency exceeds 2 seconds per KB of input.

**Severity**: MEDIUM. Composite chain is 5× single-stage CPU at minimum,
2× more in Option B. On 4KB fixtures, target latency budget = 8 seconds
total. PASS 4 LIVE FIRE will measure.

### 6.7 F-CHAIN-7 — raw 142 D2 try-revert ordering bug

**Condition**: in Option B (best-of-N), stage `i` reverts to identity AFTER
stage `i+1` has already consumed stage `i`'s output, leading to decode
mismatch (decode reads manifest indicating identity at stage `i` but
stage `i+1` decoded a non-identity input).

**Severity**: BLOCKING. Implementation MUST fix the choice at junction
`i` BEFORE invoking stage `i+1` encode. Pipelined encodes are forbidden.

### 6.8 F-CHAIN-8 — raw 137 cmix-ban violation (composition mis-classified as mixer)

**Condition**: composite chain dispatcher inspects multiple per-stage
candidate outputs (Option B best-of-N) and a third party classifies the
chain as "context mixer" because the dispatcher selects among models on a
per-input basis.

**Severity**: HIGH. Defense:
- A34 internally is a SINGLE deterministic order-3 PPM-D — no internal
  context mixing.
- The chain dispatcher selects AMONG STAGES (different placements), not
  AMONG MODELS at the same placement. This is **multi-stage cascade**, not
  context mixing in the cmix sense.
- The min_len-revert at each junction is a BYTE-LENGTH GATE, not a
  probability mixer.
- raw 137 cmix-ban applies to the HEAVY out-of-band coder class (CMIX,
  paq8) NOT to multi-stage deterministic cascades. DEFLATE itself is a
  2-stage cascade (LZ77 → Huffman) and is universally classified as a
  single algorithm, not a mixer.

**F-CHAIN-8 mitigation pre-registration**: chain dispatcher specification
explicitly forbids per-bit probability blending. Each stage outputs a
complete byte stream that the next stage consumes byte-aligned. No
per-symbol probability arithmetic crosses stage boundaries.

---

## 7. Implementation roadmap

### 7.1 PASS structure (4 passes)

| Pass | Scope | Status |
|------|-------|--------|
| **PASS 1** | Design doc (this document, `~600 LoC`) | THIS TURN |
| **PASS 2** | Skeleton `tool/hxc_composite_chain.hexa` (~700 LoC), Option A linear chain only, sigil `^d`, encode/decode wire, manifest reader/writer | NEXT TURN, NOT this turn |
| **PASS 3** | Selftest 9 fixtures byte-eq round-trip; raw 142 D2 try-revert at top-level only (Option A); pre-register F-CHAIN-1..8 in falsifier ledger | PASS 2 follow-on |
| **PASS 4** | LIVE FIRE on n6/anima 6-repo sweep, Option A only, MEASURED composite saving, F-CHAIN-2 / F-CHAIN-5 / F-CHAIN-6 measurement | DEFERRED INDEFINITELY |
| **PASS 5** | Option B best-of-N upgrade if PASS 4 yields > 0pp aggregate; F-CHAIN-7 stress test | DEFERRED, conditional on PASS 4 |
| **PASS 6** | Option C A25-aware routing if PASS 4 + 5 yield class-specific advantage; A25 classifier extension | DEFERRED, conditional |

### 7.2 Pre-conditions for PASS 2

PASS 2 (skeleton) cannot start until ALL of the following are true:

1. **A33 first-tick PASS 3 selftest 5/5 byte-eq round-trip MEASURED**
   (currently in-flight). Without A33 round-trip correctness, stage 3
   cannot be wired in.
2. **A34 v2 wire stabilization**: A34 v1 is 5/5 PASS but `^l` sigil and
   wire format may evolve in v2 (carry-byte budget, PPM-D state init).
   PASS 2 of composite chain pins `^l` at v1 freeze point.
3. **A35 v2 release-or-freeze decision**: A35 v1 Stage 1 (column-reorder)
   is 6/6 PASS. v2 Stage 2 (delta + tokenizer) design exists but is not
   skeleton-landed. PASS 2 of composite chain pins `^o` at v1 freeze.

### 7.3 Non-overlap with prior composite chain doc

The prior `hxc_composite_chain_design_2026_04_28.md` (yesterday) covered
A29+A30+A23. **This document is NOT a revision of that doc.** Both docs
coexist:

- 2026-04-28 doc: A29+A30+A23 chain — "internal-byte composition" axis on
  EXISTING modules (A29 / A30 / A23). Skeleton landed under sigil `^d`.
- **2026-04-29 doc (this)**: A33+A34+A35 chain — three NEW modules from
  the entropy verdict's enumerated 80% paths. Sigil `^d` is **REUSED**
  for the chain envelope (multi-version capable via `v=composite-v2`
  in the manifest header).

The `^d` sigil reuse is intentional: the chain envelope is the same
abstract concept (multi-stage cascade with manifest header), and the
`v=composite-v1` vs `v=composite-v2` field disambiguates parsers. **F-CHAIN-3
manifest ambiguity does NOT fire** because v1 manifest references chains
{C1, C3} and v2 manifest references chain {A, B, C} — disjoint chain tag
sets.

---

## 8. Cumulative caveats (raw 91 explicit)

1. This is a **PASS 1 design doc only**. NO module implementation, NO
   commit to `tool/hxc_composite_chain.hexa`, NO LIVE FIRE, NO witness
   ledger entry, NO promotion claim.
2. All saving estimates are PROJECTION — A33 is in-flight, A34 v1 5/5
   PASS in-sample on 4KB fixtures only, A35 v1 6/6 PASS Stage 1
   header-dominated on small. **Composite measurement requires all three
   to land + PASS 4 LIVE FIRE.**
3. Stage interaction is UNMEASURED. A35 column-reorder may DESTROY A33
   ring buffer fingerprints. A34 Mode R replacing A29 may LOSE A29's
   length-code lift. **F-CHAIN-2 falsifier guards against composite < best
   single stage.**
4. The 80% close hypothesis is **class-specific**: text-heavy projected
   60-70%, json-heavy large schemaful projected 48..90%+, mixed projected
   70%+. **None reach 80% with high confidence; only json-heavy large
   schemaful has theoretical headroom.**
5. raw 142 D2 try-revert is pre-registered at every junction in Option B
   and at the top level in Option A. Implementation order matters
   (F-CHAIN-7).
6. raw 137 cmix-ban: composite chain is a multi-stage deterministic
   cascade, NOT a context mixer. F-CHAIN-8 falsifier explicitly guards
   the boundary.
7. raw 156 placement-axis: 3 axes orthogonal (source H_n / cross-file
   context / sub-byte fractional). Each stage's placement is declared
   per stage in the manifest.
8. raw 47 cross-repo: A33 ring buffer is concatenated-corpus over n6 +
   anima + hexa-lang + airgenome + hive + nexus per A33 design. Composite
   chain manifest records the cross-repo file order.
9. raw 18 self-host fixpoint: composite chain itself must be self-host
   compressible — when applied to its own source `tool/hxc_composite_chain.hexa`,
   composite must round-trip byte-eq. This is a PASS 3 selftest fixture.
10. raw 9 hexa-only: PASS 2 implementation will be in hexa only;
    `/tmp/composite_chain_helper.py` carve-outs are forbidden under raw 9
    unless reduced to scratch-only (raw 37).

---

## 9. Cross-references

- A33 design: `anima/docs/hxc_a33_cross_repo_dict_design_2026-04-28.md`.
- A34 design: `anima/docs/hxc_a34_sub_byte_arithmetic_design_2026-04-28.md`.
- A35 design: `anima/docs/hxc_a35_source_transform_design_2026-04-28.md`.
- N6 entropy floor witness: `anima/state/format_witness/2026-04-28_anima_n6_entropy_floor_measurement.jsonl` (commit 4cd8e62da).
- N6 entropy floor design: `anima/docs/hxc_anima_n6_entropy_floor_2026_04_28.md`.
- Prior composite chain (A29+A30+A23, deprecated): `anima/docs/hxc_composite_chain_design_2026_04_28.md`.
- A25 dispatcher: `tool/hxc_a25_type_aware.hexa`.
- A18 v6 LZ77: `anima/docs/hxc_phase10_a18_design_20260428.md`.
- A19 v2 per-corpus dict: `anima/docs/hxc_phase9_p4_a19_cross_file_shared_dict_design.md`.
- A29 v3 length-codes Huffman: `anima/docs/hxc_phase13_p0_a29_deflate_design_*.md`.
- Falsification ledger v2: `anima/docs/hxc_falsification_ledger_v2_20260428.md` — F-CHAIN-1..8 to be appended at PASS 3.
- raw 156 placement-axis specification: `anima/docs/hxc_phase11_a22_design_20260428.md` (placement matrix precedent).
- raw 142 D2 try-revert specification: `anima/docs/hxc_falsification_ledger_v2_20260428.md` §D2.
- raw 137 cmix-ban specification: `anima/docs/hxc_wire_encoding_decision_20260428.md` §cmix-ban.

---

## 10. End of design — PASS 1 mandate

This tick:
- Land `anima/docs/hxc_composite_chain_design_2026-04-29.md` design doc.
- NO module file modifications (A33/A34/A35 modules untouched).
- NO commit to `tool/hxc_composite_chain.hexa` (skeleton is PASS 2, next turn).
- NO witness ledger entry (this design doc IS the deliverable).
- NO LIVE FIRE / NO 6-repo sweep / NO catalog promotion / NO A25 dispatcher integration.

Follow-on ticks (separate decision-gates):
- (T+1) PASS 2 skeleton land — Option A linear chain only, sigil `^d`,
  v=composite-v2 manifest, encode/decode wire on top of A33/A34/A35 (each
  read-only consumed). Pre-condition: A33 first-tick PASS 3 5/5 byte-eq.
- (T+2) PASS 3 selftest 9-fixture byte-eq round-trip; F-CHAIN-1..8
  pre-registered in falsifier ledger.
- (T+3) PASS 4 LIVE FIRE on n6/anima 6-repo sweep, Option A only — MEASURED
  composite saving, F-CHAIN-2 and F-CHAIN-5 and F-CHAIN-6 verdicts.
- (T+4 conditional) PASS 5 Option B upgrade if PASS 4 yields > 0pp.
- (T+5 conditional) PASS 6 Option C A25-aware routing if class-specific
  PASS 4/5 advantage exists.

raw 91 honest C3 lock: this design IS the deliverable. NO measured saving
claim. NO 80% reachability claim. The composite chain hypothesis remains
**design hypothesis ONLY** until PASS 4 LIVE FIRE measures it. Per the
4cd8e62da global verdict, 80% reachability on per-file byte-canonical
remains FALSE; the composite chain proposes a path BEYOND per-file
byte-canonical (cross-file LZ77 + sub-byte coding + source transform), but
empirical reachability is post-PASS-4 unknown.
