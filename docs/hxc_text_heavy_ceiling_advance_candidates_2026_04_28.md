% HXC Text-Heavy / Mixed CEILING Advance — Algorithm Candidate Survey
% Date: 2026-04-28
% Status: DESIGN-ONLY — first-tick scout, NO IMPLEMENTATION, NO COMMIT this turn
% Author: agent (Opus 4.7 1M, ω-cycle text-heavy ceiling-advance scout)
% Phase: 13 P0 (post-Phase-12 closure attempt)
%
% Compliance: raw 9 hexa-only · raw 18 self-host fixpoint · raw 33 NL English ·
% raw 42 jetsam (≤200MB on 79KB) · raw 47 cross-repo · raw 65+68 idempotent ·
% raw 71 falsifier-preregistered · raw 91 honest C3 (DESIGN-ONLY, NO MEASURED
% claims) · raw 137 80% Pareto + cmix-ban + A28 TRANSCEND-FORBIDDEN ·
% raw 142 D2 try-and-revert (design-only = no try, no revert) · raw 156
% algorithm-placement-orthogonality.

---

## 0. Honest framing (raw 91 C3, STRICT)

This document is **DESIGN-ONLY scout**. Per the user mission brief, scope is:

- Survey lossless compression algorithms NOT in current catalog with text-heavy /
  mixed-class strength.
- Apply constraint filter (raw 9, raw 18, raw 137 cmix-ban, raw 42 jetsam).
- Compare against existing A1-A26 catalog.
- Recommend 1-2 candidates for next-cycle dispatch (NOT this turn).
- Pre-register falsifiers per recommendation.

The following are NOT delivered this turn (deferred):

- Any implementation `.hexa` source.
- Any `.hxc_aot` rebuild.
- Any LIVE FIRE measurement on text-heavy / mixed corpora.
- Any catalog promotion.
- Any commit (raw 142 D2 conservative).

The following ARE measured (cite-backed prior witnesses, not produced this turn):

| metric                            | value     | source ledger                                                   |
|-----------------------------------|-----------|-----------------------------------------------------------------|
| 6-repo aggregate (post A25 v2)    | 78.05%    | `2026-04-28_a25_v2_full_deployment_6repo_80pct_measured.jsonl` (53c711eb) |
| 5MB stratified composite          | 76.24%    | `2026-04-28_a18_v3o2_text_heavy_ceiling_final.jsonl` (post-d631a902 dispatch) |
| Text-heavy class (5MB sample)     | 49.09%    | same ledger, +0.78pp over A25-only 48.31%                       |
| Mixed class (5MB sample)          | 58.49%    | same ledger, +0.17pp over A25-only 58.32%                       |
| JSON-heavy class                  | 94.38%    | same ledger (saturated, +0.03pp from A18 disp)                  |
| Small-file class                  | 0.00%     | same ledger (passthrough; routed to A23 via A25 but null saving) |
| 80% target gap                    | 3.76pp    | aggregate 76.24% / target 80%                                   |
| raw 137 v8 strengthen threshold   | 78.65%    | DEFERRED HARD per 16ff3e55                                      |
| Shannon H_4 lower bound           | 0.813 b/B | n6 verdict a201a6cc → 90% saving asymptote                      |

**Bottleneck class arithmetic**:

- text-heavy contribution at 23.99% byte share: gap to 80% on class = 80 - 49.09 = 30.91pp;
  full-class hypothetical lift to 80% would deliver 30.91 × 0.2399 = +7.41pp aggregate
  (more than enough alone to reach 80% target).
- mixed contribution at ~30% byte share: gap = 80 - 58.49 = 21.51pp;
  full-class lift to 80% = 21.51 × 0.30 = +6.45pp aggregate.
- json-heavy at 94.38% saturated — no further lever.
- small-file at 0% — passthrough class, separate problem.

**Therefore**: any +5pp on text-heavy class alone closes ~+1.2pp aggregate;
+5pp on mixed alone closes ~+1.5pp aggregate. **Combined +5pp on both** ≈ +2.7pp
aggregate, sufficient to clear 78.65% v8 strengthening gate (currently -2.41pp)
with margin, and approaches 80% within ~1pp.

**This is the lever the present scout targets**: text-heavy + mixed combined
+5-10pp class lift via NEW entropy-coder paradigm currently absent from catalog.

---

<!-- [Hc_675 hxc-text-heavy-mixed-5pp-combined-lever-clear-80pct — moved to hypotheses_candidates/Hc_675_hxc_text_heavy_mixed_5pp_combined_lever.md on 2026-05-11] -->

## 1. Current catalog audit (saturation evidence)

### 1.1 Entropy-coder family in catalog (LIVE)

| algo | type                          | LoC   | order  | text-heavy verdict              |
|------|-------------------------------|------:|-------:|----------------------------------|
| A16  | order-0 byte arithmetic coder | 1,133 | 0      | declared 28% saving floor (Shannon H_0) |
| A17  | PPM order-3 context mixer     |   ~600 (in hexa-lang stdlib `hxc_a17_ppm_order3.hexa`) | 3 | partial — multibyte fix landed b85 |
| A18  | LZ77 + PPM order-4 (v1-v6)    | 2,485 | 4      | v3-o2 `49.09%` text-heavy ceiling final / +0.78pp lift over A25 |
| A23  | sparse PPM order-5            |   ~500 | 5      | small-file class winner (passthrough corner) |
| A26  | sparse PPM-D (Howard 1993)    |   697 (v3 inline) | 5    | RETIRED — memory floor 91MB on 79KB exceeded raw 42 |

### 1.2 LZ family in catalog (LIVE)

| algo | type                          | LoC   | window | text-heavy verdict              |
|------|-------------------------------|------:|-------:|----------------------------------|
| A18 v1 | LZ77 baseline               | (in 2485) | 32K | covered                          |
| A18 v2 | LZ77 + PPM order-4 hybrid   | (in 2485) | 32K | A25 internal default for text-heavy |
| A18 v3-o2 | LZ77 + 2-byte byte-context | (in 2485) | 32K | -4.97pp WORSE alone, +0.78pp via dispatch |
| A18 v4-w64 | LZ77 + 64K window          | (in 2485) | 64K | dispatch candidate              |
| A18 v6-optimal | LZ77 + lazy match optimal parsing | (in 2485) | 32K | dispatch candidate (O(n²) latency >1MB) |
| A19 v2 | cross-file shared dict       | (in `hxc_a19_cross_file_fed.hexa`) | dict-cap 65536 | scale-out 0.00pp (small-file class) |

### 1.3 Grammar / structural / type-aware family (LIVE)

| algo | type                          | LoC   | strength                       |
|------|-------------------------------|------:|---------------------------------|
| A24 v1 | PCFG grammar induction      | (a24 v1) | 0/216 wins on production corpora |
| A24 v2 | bounded grammar (estimator)  | (a24_v2_bounded) | build-only, no wire             |
| A25 v2 | type-aware classifier        | 951   | primary routing 76% standalone   |

### 1.4 Saturation observation

The catalog is **dense in the LZ-PPM family** (A16/A17/A18/A23/A26 all PPM /
arithmetic-coder territory). The **only entropy-coder paradigm currently present**
is **arithmetic / range coding**. Specifically absent (raw 91 honest enumeration
verified by `grep -niE "(huffman|burrows|bwt|deflate|rans|asymmetric|move-to-front)"`
across `/Users/ghost/core/hexa-lang/self/stdlib/hxc_*.hexa`):

- ✗ **Huffman coder** — symbol-level prefix codes, deterministic, integer-only.
  Only a `deflate-compatible` reference comment exists in A18 line 190 (
  `MAX_MATCH = 258`); no Huffman implementation.
- ✗ **Burrows-Wheeler Transform (BWT)** — block-sorting transform, prerequisite
  for bzip2-class compression. Strong on natural-language text via local
  context concentration.
- ✗ **Move-To-Front (MTF) transform** — symbol-rank transform, classical BWT
  post-processor.
- ✗ **rANS (range Asymmetric Numeral Systems) — Duda 2014** — modern
  deterministic entropy coder, alternative to arithmetic coding with
  table-driven encoding (faster on small alphabets).
- ✗ **Static Huffman with corpus-specific frequency tables** — sub-paradigm of
  Huffman with offline-trained codebooks (bounded memory, no per-file adaption).
- ✗ **Tunstall coder** (variable-to-fixed entropy coder, dual to Huffman) —
  niche, not surveyed here.

The mission brief enumerates DEFLATE, BWT+MTF+RLE, rANS, Static Huffman,
Arithmetic coder. Arithmetic coder is **already A16** — coverage assessment in §3.5.
The remaining 4 are NEW to catalog and form the candidate pool.

---

## 2. Constraint filter (raw 9 / raw 18 / raw 42 / raw 137)

Each candidate evaluated on 4 binary admissibility constraints. Any FAIL = candidate
ineligible for HXC catalog promotion (no implementation budget allocated).

| candidate                   | raw 9 hexa-only | raw 18 self-host | raw 42 mem ≤200MB on 79KB | raw 137 cmix-ban |
|-----------------------------|:----------------:|:-----------------:|:-------------------------:|:-----------------:|
| DEFLATE (LZ77 + Huffman)    | ✓ pure-hexa LoC ~700 | ✓ integer-only Huffman tree build | ✓ 32K window + 256-leaf Huffman tree ≪ 200MB | ✓ deterministic, no neural |
| BWT + MTF + RLE             | ✓ pure-hexa LoC ~600 | ✓ integer-only suffix array via SAIS or naive-sort | ⚠ block size 79KB → suffix array 79K × 4B = 316KB (safe); LARGER blocks risk | ✓ deterministic |
| rANS (Duda 2014)            | ✓ pure-hexa LoC ~500 | ✓ integer-only state machine (32-bit) | ✓ 256-symbol freq table ~1KB | ✓ deterministic |
| Static Huffman (corpus tab) | ✓ pure-hexa LoC ~400 | ✓ integer-only Huffman build + freeze | ✓ frozen codebook ~512B per class | ✓ deterministic, no on-line learning |
| Arithmetic coder            | **already A16** | already A16 | already A16 | already A16 |

All 4 NEW candidates pass all 4 constraints. Pre-implementation eligibility:
**4/4 admissible** for further analysis.

### 2.1 Critical raw 137 boundary check

**raw 137 cmix-ban scope**: bans neural-mixer (cmix / PAQ8 / NNCP class) entropy
coders that require floating-point, training corpora, or non-deterministic
sampling. Does NOT ban:

- Static frequency tables (Huffman / Static Huffman / Arithmetic with frozen freq).
- Integer-state coders (rANS / range-coder / arithmetic-coder all-integer).
- Block transforms (BWT / MTF / RLE — pure permutations, no learning).

**Verdict**: all 4 candidates are CLEARLY within raw 137 charter. None approach
the cmix boundary.

---

## 3. Candidate-by-candidate technical evaluation

### 3.1 DEFLATE (LZ77 + canonical Huffman)

**Algorithm spec** (RFC 1951, Deutsch 1996):
- LZ77 pre-stage with sliding window — already covered by A18 v1-v6 (32K window).
- Huffman post-stage — variable-length prefix codes for both literals (256 alphabet)
  and length-distance pairs (288-symbol alphabet for length, 30 distance codes).
- Canonical Huffman: deterministic code construction from code-length sequence
  alone (no tree shape transmission) — RFC 1951 §3.2.2.

**Comparison vs current A18**:
- A18 v1-v6 use LZ77 with **byte-emitting** literal encoding (1 byte per literal).
- DEFLATE replaces byte-emitting with **bit-packed Huffman** — high-frequency
  bytes (e.g., space, lowercase letters in English text) emit as 4-5 bits;
  low-frequency bytes emit as 8-12 bits.
- **Theoretical lift on English text**: H_0 = 5.75 bit/byte → Huffman achieves
  ~5.75/8 = 72% literal-stream saving from the entropy term alone (vs current
  byte-emit 0% literal-stream saving). A18 v6 provides match-pair compression;
  DEFLATE adds the literal-stream entropy term that A18 leaves on the table.

**raw 156 placement axis**: post-LZ77 (A18 v1 ⊂ DEFLATE pipeline). NOT
orthogonal to A18 — DEFLATE **subsumes** A18 v1's literal output. Deployment
options:

- (a) DEFLATE replaces A18 v2 entirely on text-heavy / mixed (high disruption).
- (b) DEFLATE = NEW algorithm A29, gated by A25 dispatcher to text-heavy / mixed
  classes only; A18 v2 retained for json-heavy / struct-audit (low disruption,
  preferred).

**Projected lift** (post-A25 baseline 78.05%):
- text-heavy class: 49.09% → **62-72%** (+13-23pp). Rationale: literal stream
  dominates text-heavy compressed output (current A18 v3-o2 leaves bit-packed
  entropy unrealized). This is the primary upside.
- mixed class: 58.49% → **66-72%** (+7-13pp). Rationale: mixed = English text
  + structured header markers; literal stream is ~70% of bytes and benefits
  from same Huffman lever.
- json-heavy: 94.38% → **94.5-95%** (+0.1-0.6pp). Saturated.
- aggregate (post-Phase-12 76.24% baseline): **+2.5-5.5pp** → 78.7-81.7%.

**Memory budget**: 32K window + 286-leaf literal/length tree + 30-leaf distance
tree + 19-leaf code-length tree = ~36KB resident. Hexa interpreter overhead
~10MB. Total ≤ 50MB on 79KB input. **Easily within raw 42 200MB cap**.

**Latency budget**: O(n × log(286)) ≈ O(8.2n). On 79KB: 79K × 8 cycles ≈ 0.6ms
ideal arithmetic; hexa interpreter 50-100x slower → 30-60ms. **Within A18's
80-160ms / 1KB Phase-8-P5 ceiling** (per `hxc_phase11_design_post_a18` §6.4).

**LoC budget**: ~700 pure-hexa (Huffman build ~250 + canonical-encode ~150 +
canonical-decode ~150 + LZ77 reuse-from-A18 ~50 + selftest ~100). Reuses A18
v1 LZ77 tokenizer to avoid duplication.

**Falsifiers (preregistered for future implementation, NOT this turn)**:

| ID | spec | retire condition |
|---|---|---|
| F-A29-1 | text-heavy class lift < +5pp on 5MB stratified | reject DEFLATE-replacing-A18 on text class |
| F-A29-2 | mixed class lift < +3pp on 5MB stratified | reject DEFLATE on mixed class |
| F-A29-3 | round-trip byte-eq fails on any class | reject (raw 65/68 idempotency) |
| F-A29-4 | encode latency > 200ms / 1KB hexa interp | reject (raw 42 perf budget) |
| F-A29-5 | aggregate < 78.65% MEASURED on 6-repo full sweep | reject raw 137 v8 strengthening |
| F-A29-6 | DEFLATE+A18 chain regression > 1pp vs DEFLATE-only | reject chained deployment (raw 156 orthogonality) |

**raw 69 verdict**: **CIRCUMVENT** — paradigm-shift class. DEFLATE adds the
entropy-coding axis that A18 v1-v6 explicitly lacks (LZ77 with byte literals).
This is NOT an APPROACH-class refinement of A18; it is an orthogonal pipeline
stage, identical to gzip/zlib's contribution over raw LZ77.

**Strengths (mission §3 priority)**:
- DEFLATE is the only candidate that directly attacks the **literal-stream
  entropy** that all A18 variants leave unaddressed.
- Implementation risk LOW — RFC 1951 is fully specified in 30 pages, multiple
  textbook hexa-portable references (e.g., zlib `trees.c` ~1500 LoC C, of which
  ~700 LoC is fundamentally portable to hexa integer ops).
- Reuses A18 v1 LZ77 tokenizer — no duplication.
- Deterministic across machines (raw 18 self-host fixpoint preserved).

**Weaknesses**:
- Literal-stream entropy coder OVERLAPS conceptually with A16 order-0 arithmetic
  coder. Hypothetical A16 + A18 v1 chain might achieve similar results — but
  A16 has known overhead (~20% bit-stream → byte-canonical wire expansion via
  base64url) that DEFLATE's bit-packing avoids natively.
- Bit-packing requires careful byte-alignment + padding flush — failure mode is
  off-by-one in tail handling. Requires rigorous round-trip selftest.

---

### 3.2 BWT + MTF + RLE (bzip2-style block-sort)

**Algorithm spec** (Burrows-Wheeler 1994 + Bentley-McIlroy 1986 MTF + RLE):
- **Pass 1 (BWT)**: take input block (e.g., 79KB), construct all rotations, sort
  lexicographically, output last column. Requires suffix-array construction
  (SAIS algorithm O(n) integer-only, or naive O(n² log n) suffix-sort).
- **Pass 2 (MTF)**: replace each byte with its position in a 256-element
  rank-list, then move that byte to position 0. Output is rank stream where
  high-frequency-after-BWT bytes cluster near 0.
- **Pass 3 (RLE on MTF zeros)**: run-length-encode the predominant 0s.
- **Pass 4 (Huffman or arithmetic coder)**: entropy-code the RLE+MTF stream.

**Comparison vs current A18**:
- A18 = forward-context-prediction (LZ77 + PPM order-4); cannot exploit
  the full document's symbol distribution.
- BWT + MTF = **block-context-clustering** — long-range repetitions across
  the entire block surface as local clusters in the BWT output. Particularly
  strong on natural English (40-50% saving floor on bzip2 vs gzip on text).

**raw 156 placement axis**: pre-A1 raw OR post-A18 (BWT can be applied directly
on raw bytes OR on A18 v1 output as a post-stage). Recommended placement:
**pre-A1 raw**, gated by A25 dispatcher to text-heavy class only.

**Projected lift** (post-A25 baseline):
- text-heavy class: 49.09% → **65-78%** (+16-29pp). Rationale: bzip2 routinely
  beats gzip by +10-20% on English text via block-sort context concentration.
- mixed class: 58.49% → **65-72%** (+7-13pp). Rationale: bzip2 advantage shrinks
  on mixed corpora where structure-markers limit BWT block coherence.
- aggregate: **+3-7pp** → 79-83%.

**Memory budget**: 79KB block × suffix-array 4 bytes = 316KB; SAIS auxiliary
arrays ~3× = 1MB. Plus MTF rank-list 256B; Huffman tree ~36KB. Total ~5MB
hexa interpreter overhead ~10MB = 15MB. **Within raw 42**.

**CRITICAL caveat**: bzip2's standard 900KB block size would exceed memory
budget (3.6MB suffix array on 900KB block). **Must cap block at 79KB** (or
smaller) to honor raw 42 on the worst-case corpus n6_atlas 79KB. This caps
the BWT context window — partial mitigation.

**Latency budget**: SAIS O(n) integer-only is fast in C (~10ns/byte on 79KB =
0.79ms). Hexa interpreter 50-100x slower → 40-80ms. Naive O(n² log n) suffix
sort: 79K × log(79K) × 79K = 1.6 × 10¹⁰ ops → minutes (UNACCEPTABLE).
**Critical implementation requirement**: must use SAIS (Nong-Zhang-Chan 2009)
or DC3 (Karkkainen-Sanders 2003), NOT naive sort.

**LoC budget**: ~600 pure-hexa (SAIS ~250 + MTF ~50 + RLE ~50 + Huffman ~150
or rANS ~100 + selftest ~100). SAIS is the dominant complexity; reference
implementation `sais-lite.c` is 350 LoC of well-tested portable C.

**Falsifiers**:

| ID | spec | retire condition |
|---|---|---|
| F-A30-1 | text-heavy class lift < +8pp on 5MB stratified | reject (BWT advantage minimal) |
| F-A30-2 | mixed class lift < +3pp on 5MB stratified | reject |
| F-A30-3 | round-trip byte-eq fails on any block size | reject (raw 65/68) |
| F-A30-4 | SAIS construction memory > 50MB on 79KB | reject (raw 42 worst-case violation) |
| F-A30-5 | SAIS construction time > 500ms / 79KB hexa interp | reject (raw 42 perf budget) |
| F-A30-6 | aggregate < 78.65% MEASURED on 6-repo full sweep | reject raw 137 v8 strengthening |
| F-A30-7 | block size > 79KB chosen → memory blowup | reject (must enforce ≤79KB cap) |

**raw 69 verdict**: **CIRCUMVENT** — different paradigm class (block-sort vs
forward-prediction). Strongest theoretical text-heavy candidate but with
HIGHEST implementation complexity (SAIS is non-trivial).

**Strengths**:
- Highest projected text-heavy lift (+16-29pp).
- bzip2's empirical advantage on English text is well-documented (40+ years
  of literature).
- BWT block-sort is **complementary** to A18 forward-context — no direct overlap.

**Weaknesses**:
- SAIS implementation is the costliest LoC budget item (~250 LoC of careful
  index manipulation; bug-prone).
- Block size cap at 79KB partially defeats BWT's long-range advantage. Larger
  blocks would extend the lift but violate raw 42 worst-case.
- BWT requires 1-byte sentinel + EOF marker handling — round-trip byte-eq
  is fragile.

---

### 3.3 rANS (range Asymmetric Numeral Systems)

**Algorithm spec** (Duda 2014):
- State machine: integer state s ∈ [L, bL), where L = 2^k for some normalization
  constant k (typically k=12 or 16).
- Encode symbol x with frequency f[x] and cumulative cum[x]:
  s' = floor(s / f[x]) × M + cum[x] + (s mod f[x]),
  where M = total frequency.
- Renormalize: while s ≥ bL, emit low byte / 16-bit word and shift right.
- Decode: reverse the operation, reading from end-of-stream.

**Comparison vs current A16**:
- A16 = arithmetic / range coder, identical theoretical compression ratio
  to rANS (both reach H_0 entropy floor).
- rANS advantages over A16:
  - **Table-driven encoding** with precomputed reciprocal tables → 2-3× faster
    encoding on small alphabets (256-byte symbol set is ideal).
  - **No carry propagation** → simpler implementation (A16 has carry-handling
    in `a16_encode` lines ~250-300 per `hxc_a16_arithmetic_coder.hexa`).
- rANS disadvantages:
  - Encodes in REVERSE order (encode last-symbol-first), requiring buffering
    or reverse-iteration.
  - Slightly larger state space than range coder (typically 32-bit state vs
    range coder's flexible 16-bit-renormalized).

**Comparison vs current A18**:
- Identical to A16 comparison: rANS provides the entropy-coder backend that
  A18 currently lacks. Could plug into A18's literal stream (replacing
  byte-emit) for similar effect to DEFLATE-as-Huffman, except using rANS
  tables instead of canonical Huffman codebook.

**raw 156 placement axis**: post-A18-tokenize (rANS replaces byte-emit on
literal stream of A18 v1+) OR replaces A16 wholesale.

**Projected lift**:
- IF rANS replaces A16 (drop-in entropy coder swap): saving ratio identical
  (both reach H_0); difference is purely encode/decode speed (rANS 2-3× faster).
  Wire output may differ by ~0.5% due to rounding tail handling.
- IF rANS plugs into A18 literal stream (parallel to DEFLATE option but with
  rANS instead of Huffman): equivalent compression to DEFLATE but at lower
  latency (table-driven). **Same +13-23pp text-heavy projection** as DEFLATE.

**Memory budget**: 256-symbol freq table 1KB + 256-symbol reciprocal table 1KB
+ state register 32-bit. Total <5KB. **Easily within raw 42**.

**Latency budget**: ~10-20ns/byte on optimized C; hexa interp 50-100x slower →
~500ns-2µs/byte; on 79KB = 40-160ms. Faster than A16 (~3× per Duda 2014 bench),
faster than DEFLATE Huffman.

**LoC budget**: ~500 pure-hexa (rANS encode ~150 + rANS decode ~150 + freq table
build ~50 + selftest ~150). Significantly simpler than DEFLATE (no canonical
code-length transmission).

**Falsifiers**:

| ID | spec | retire condition |
|---|---|---|
| F-A31-1 | rANS saving ratio differs from A16 by > 0.5% on identical input | reject (numeric error) |
| F-A31-2 | rANS encode latency NOT 2× faster than A16 on hexa interp | reject (no-gain swap) |
| F-A31-3 | round-trip byte-eq fails | reject (raw 65/68) |
| F-A31-4 | rANS plug-into-A18-literal-stream lift < +5pp text-heavy | reject (no entropy gain over A18 byte-emit) |
| F-A31-5 | rANS state register overflow on 32-bit ops | reject (precision violation) |
| F-A31-6 | aggregate < 78.65% MEASURED 6-repo | reject raw 137 v8 strengthening |

**raw 69 verdict**: **APPROACH** if used as drop-in A16 replacement (purely
faster, not higher-compression); **CIRCUMVENT** if used to add entropy-coding
to A18 literal stream (paradigm-shift identical to DEFLATE).

**Strengths**:
- Lowest LoC budget (~500) of all candidates.
- Faster encode/decode than A16 (~2-3×).
- Modern algorithm; cleaner spec than RFC 1951 Huffman.

**Weaknesses**:
- If used purely as A16 replacement, **no compression-ratio gain** (just speed).
  This violates the mission objective which requires ceiling ADVANCE not just
  speed.
- If used to add entropy-coding to A18 literal stream, becomes effectively
  identical to DEFLATE-with-rANS-instead-of-Huffman; design decision is
  Huffman vs rANS, not whether to add entropy coder.
- Encode in reverse order is implementation gotcha — requires buffering (extra
  memory) or reverse-iteration helper (hexa interp may not natively support
  efficient reverse iteration).

---

### 3.4 Static Huffman with corpus-specific frozen frequency tables

**Algorithm spec**:
- **Offline phase** (one-time, NOT per-file):
  - Sample representative corpus per class (text-heavy / mixed / json-heavy).
  - Compute byte frequency table per class (256-entry).
  - Build canonical Huffman codebook per class; freeze as a constant table
    in stdlib source (`hxc_a32_static_huffman.hexa` literal const).
- **Online phase** (per-file encode):
  - Look up class-specific codebook (no per-file frequency analysis).
  - Encode bytes using frozen codebook.
  - Header includes class-tag (1 byte) + lzz length.
  - Decode: identical lookup.

**Comparison vs DEFLATE**:
- DEFLATE = adaptive Huffman per-block (transmits codebook per file).
- Static Huffman = pre-computed frozen codebook (no codebook transmission).
- Static Huffman saves the codebook-transmission overhead (~40-100B per file)
  but loses adaptation to per-file outliers.

**Comparison vs A19 cross-file shared dict**:
- A19 = LZ77 dictionary shared across files (cross-file dedup).
- Static Huffman = entropy-coder codebook shared across files.
- **Orthogonal axes** — both can coexist (LZ77 cross-file dict + Huffman
  cross-file codebook).

**raw 156 placement axis**: post-LZ77 OR pre-A1 raw. Best placement:
post-A18 v1 tokenize → static Huffman literal stream.

**Projected lift** (post-A25 baseline):
- Small files (<2KB) — biggest beneficiary because per-file codebook
  transmission overhead would dominate; static eliminates it. text-heavy
  small-file (<2KB): A25 currently routes to A23 (passthrough 0%); static
  Huffman would lift to **20-40%** (+20-40pp).
- Medium-large text-heavy: same projection as DEFLATE (+13-23pp class lift)
  minus the codebook-transmission saving (~+0.1-0.5pp marginal).

**Memory budget**: 256-entry codebook × 4 classes × 4 bytes = 4KB frozen in
source. Decode tree 256-leaf binary tree ~4KB. Total <10KB. **Trivially within
raw 42**.

**Latency budget**: identical to DEFLATE Huffman (~30-60ms / 79KB hexa interp).

**LoC budget**: ~400 pure-hexa (codebook lookup ~50 + canonical encode ~150 +
canonical decode ~150 + selftest ~50). **Smallest of all candidates**.

**Falsifiers**:

| ID | spec | retire condition |
|---|---|---|
| F-A32-1 | text-heavy class lift < +5pp on 5MB stratified | reject |
| F-A32-2 | small-file class lift < +10pp (passthrough → encoded) | reject (key small-file lever) |
| F-A32-3 | round-trip byte-eq fails | reject (raw 65/68) |
| F-A32-4 | per-class codebook drift > 5% over 30 days corpus update | mandate retraining cycle (NOT a hard reject) |
| F-A32-5 | aggregate < 78.65% MEASURED 6-repo | reject raw 137 v8 strengthening |

**raw 69 verdict**: **CIRCUMVENT** — paradigm-shift class on small-file (currently
passthrough). On medium-large, equivalent to DEFLATE + 0.1-0.5pp.

**Strengths**:
- Smallest LoC budget (~400).
- Targets the **small-file class** that DEFLATE's adaptive Huffman cannot
  beat (codebook transmission overhead dominates for <2KB).
- Frozen codebook = trivially deterministic, no per-file frequency-pass.

**Weaknesses**:
- Codebook drift over time as corpus distribution shifts (text-heavy English
  prose vs Korean prose vs source code drift). Requires corpus re-sampling
  cycle (e.g., quarterly) to keep codebook representative.
- Loses to DEFLATE on per-file outliers (e.g., a text file dominated by
  single-character runs that aren't represented in the global codebook).
- Codebook transmission saving (~40B per file) is irrelevant for files >10KB.

---

### 3.5 Arithmetic coder coverage assessment (mission §3.5)

The mission brief asks: "Arithmetic coder (already A16) — assess current coverage".

**A16 status** (per `hxc_a16_arithmetic_coder.hexa` and witness ledgers):

| dimension                            | coverage / status                         |
|--------------------------------------|-------------------------------------------|
| Order-0 byte-arithmetic              | ✓ LIVE, 1133 LoC                          |
| Order-N (N≥1) context arithmetic     | ✗ NOT in A16; covered by A17/A18 PPM      |
| Wire format                          | base64url ^A sigil + base94 ^C (raw 157) |
| Standalone text-heavy class lift     | ~28% theoretical (H_0 floor), unverified at scale on text class alone |
| Composite chain placement            | A16 currently NOT in A25 dispatch table for text-heavy (A18 v2 wins on 49% measurement) |
| Selftest                             | 5/5 PASS                                   |
| Latency                              | ~80-160ms / 1KB hexa interp (Phase 8 P5)  |
| Round-trip byte-eq                   | preserved on selftest                      |

**A16 GAP analysis vs candidates**:

- A16 standalone reaches H_0 = 28% literal saving floor only when applied to
  RAW BYTES. Applied to A18 v2 OUTPUT (which is mostly LZ77 tokens), the H_0
  floor is much lower because the token alphabet is already entropy-coded by
  A18's range pass. A16 + A18 chain = NOT measured to deliver the +13-23pp
  text-heavy lift.
- A16's literal-stream applicability would require **plugging A16 INTO the
  A18 v1 LZ77 literal output channel** (replacing byte-emit), which is
  architecturally identical to DEFLATE-with-arithmetic-instead-of-Huffman.
  This deployment **has not been built or measured** in the catalog.

**Implication**: A16 standalone is NOT a substitute for the proposed A29-A32
candidates. The proposed candidates target **A18 v1 LZ77 literal-stream
entropy coding**, which is architecturally orthogonal to A16's standalone
order-0 application.

---

## 4. Comparison matrix

### 4.1 Projected text-heavy / mixed class lift (raw 91 PROJECTED, NOT MEASURED)

| candidate                | text-heavy class lift | mixed class lift | aggregate lift | LoC  | raw 69 verdict |
|--------------------------|----------------------:|-----------------:|---------------:|-----:|----------------|
| A29 DEFLATE (LZ77+Huff)  | **+13 to +23pp**      | +7 to +13pp      | +2.5 to +5.5pp | 700  | CIRCUMVENT     |
| A30 BWT+MTF+RLE+entropy  | **+16 to +29pp**      | +7 to +13pp      | +3 to +7pp     | 600  | CIRCUMVENT     |
| A31 rANS (drop-in A16)   | +0 to +0.5pp          | +0 to +0.3pp     | +0pp           | 500  | APPROACH       |
| A31 rANS (A18 lit-stream) | **+13 to +23pp** (~= A29) | +7 to +13pp | +2.5 to +5.5pp | 500  | CIRCUMVENT     |
| A32 Static Huffman frozen| +5 to +12pp           | +2 to +6pp       | +1 to +2.5pp   | 400  | CIRCUMVENT     |
| A32 Static Huffman SMALL-FILE only | passthrough class lift +20-40pp | n/a | +1 to +2pp (small share) | 400 | CIRCUMVENT |

**Note on A31 dual interpretation**: rANS as drop-in A16 replacement = APPROACH
(speed only, no compression gain). rANS as A18 literal-stream entropy coder =
CIRCUMVENT (paradigm shift identical to DEFLATE). The mission objective demands
ceiling ADVANCE, so the second interpretation is the active candidate.

### 4.2 Memory + latency budget summary

| candidate                       | memory on 79KB | latency on 79KB hexa interp | LoC   |
|---------------------------------|---------------:|----------------------------:|------:|
| A29 DEFLATE                     | ≤50MB          | 30-60ms                     | 700   |
| A30 BWT+MTF+RLE                 | ≤15MB          | 40-80ms (with SAIS)         | 600   |
| A31 rANS                        | ≤10MB          | 40-80ms                     | 500   |
| A32 Static Huffman              | ≤10MB          | 30-60ms                     | 400   |

All within raw 42 jetsam 200MB cap. All within Phase 8 P5 80-160ms / 1KB
historical envelope.

### 4.3 LoC vs lift Pareto

| candidate                | LoC/pp aggregate ratio        |
|--------------------------|------------------------------:|
| A29 DEFLATE              | 700 / 4pp = **175 LoC/pp**    |
| A30 BWT+MTF+RLE          | 600 / 5pp = **120 LoC/pp**    |
| A31 rANS (lit-stream)    | 500 / 4pp = **125 LoC/pp**    |
| A32 Static Huffman       | 400 / 1.7pp = **235 LoC/pp**  |

(Per-pp ratios use mid-range projection.) A30 BWT and A31 rANS are
Pareto-optimal on LoC/pp.

---

## 5. Top-2 recommendations (mission §6)

### 5.1 Recommendation #1: **A29 DEFLATE (LZ77 + canonical Huffman)**

**Rationale**:

- **Highest single-axis lift on the binding bottleneck**. Text-heavy class
  is 23.99% byte share with 30.91pp gap to 80%; +13-23pp class lift via
  Huffman literal-stream entropy is the **largest measurable lever
  available within charter**.
- **Implementation risk LOW**: RFC 1951 is the most-implemented compression
  spec in software history (~50+ open-source impls). Hexa port has clear
  path: reuse A18 v1 LZ77 tokenizer + add canonical Huffman tree builder
  (~250 LoC) + canonical encode/decode (~300 LoC).
- **Reuses A18**: no duplication; A29 = A18 v1 tokenizer + new entropy coder.
  Composes orthogonally with A25 dispatcher (gated to text-heavy + mixed
  classes only; json-heavy retains A18 v2 since 94.38% saturated).
- **Falsifier preregister**: 6 falsifiers in §3.1, conservative threshold
  (+5pp text-heavy required to declare success).

**Pre-implementation deliverables for next-cycle dispatch**:

1. Algorithm-design doc `hxc_a29_deflate_design_2026_04_29.md`
   (refines this section §3.1 to per-PASS spec).
2. First-tick `hxc_a29_deflate.hexa` skeleton:
   - PASS 1: byte-frequency analysis (single forward pass).
   - PASS 2: canonical Huffman tree build (priority queue O(n log n)
     integer-only).
   - PASS 2.5: in-sample entropy estimator (NOT wire coder yet).
   - PASS 3: 5 selftest fixtures (round-trip, short-input, JSON,
     Korean text, English text).
   - PASS 4: explicit "LIVE FIRE deferred" disclosure.
3. Witness ledger `2026-04-29_a29_deflate_first_tick.jsonl`.
4. Raw 71 falsifier preregister F-A29-1..6.
5. Cycle 2 = LIVE FIRE on 5MB stratified text-heavy corpus.
6. Cycle 3 (conditional on F-A29-1 NOT_TRIPPED) = full 6-repo sweep +
   raw 137 v8 strengthening verdict.

**Pre-registration commit count**: 0 this turn; ~3 commits across 3 cycles.

### 5.2 Recommendation #2: **A30 BWT + MTF + RLE + entropy** (HIGHER-RISK / HIGHER-REWARD alternative)

**Rationale**:

- **Strongest theoretical text-heavy ceiling** of the candidate set
  (+16-29pp class lift). bzip2's 30+ year track record on natural language
  text is empirically the strongest non-neural compression for English prose.
- **Orthogonal paradigm to LZ-PPM family** — unlike DEFLATE which extends
  A18, BWT operates on a fundamentally different transform-then-encode model.
  This means A30 + A29 chained could potentially yield additional lift
  (block-sort context concentration + Huffman entropy), at higher
  implementation cost.
- **Higher implementation risk than A29**: SAIS suffix-array construction is
  the dominant LoC contribution (~250 LoC of careful index manipulation).
  Bug surface is larger than A29's well-known canonical Huffman.

**Why #2 not #1**:
- Risk-adjusted lift: A29 is +2.5-5.5pp aggregate at LOW implementation risk;
  A30 is +3-7pp aggregate at MEDIUM-HIGH implementation risk (SAIS bug surface
  + sentinel/EOF handling).
- A29 compositionally matures to A30 (DEFLATE entropy coder is a prerequisite
  for any BWT pipeline that needs Huffman/rANS post-stage); building A29
  first means A30's entropy stage is already validated.

**Pre-implementation deliverables for next-cycle dispatch** (after A29 lands):

1. Design doc `hxc_a30_bwt_mtf_rle_design_2026_04_30.md`.
2. First-tick `hxc_a30_bwt_mtf_rle.hexa` skeleton (~300 LoC PASS 1+2+selftest).
3. 7 falsifiers F-A30-1..7 (per §3.2).

### 5.3 Why NOT recommending A31 / A32 as primary

- **A31 rANS**: as drop-in A16 replacement, no compression gain (only speed);
  as A18 literal-stream entropy coder, it duplicates A29's compression effect
  with different entropy-coder implementation. **A29 first** because Huffman
  is more battle-tested in pure-hexa integer-only context; rANS state-machine
  reverse-encoding is more error-prone in initial port.
- **A32 Static Huffman**: smallest LoC but smallest lift on aggregate (+1-2.5pp).
  Most attractive subset is the **small-file class** (passthrough → +20-40pp
  on tiny files), but small-file is only ~5% byte share so contribution is
  ~+1-2pp aggregate. RECOMMENDED as **A32 small-file-class-only deployment
  in cycle 2 of A29**, NOT as primary text-heavy lever.

---

## 6. Falsifier preregister consolidated table

All falsifiers below are pre-registered for **future implementation**. None
are tripped this turn (no implementation, no measurement).

| ID         | candidate | spec                                                         | retire condition |
|------------|-----------|--------------------------------------------------------------|------------------|
| F-A29-1    | DEFLATE   | text-heavy lift < +5pp on 5MB stratified                     | reject A29       |
| F-A29-2    | DEFLATE   | mixed lift < +3pp on 5MB stratified                          | reject A29 mixed |
| F-A29-3    | DEFLATE   | round-trip byte-eq fails                                     | reject A29       |
| F-A29-4    | DEFLATE   | encode latency > 200ms / 1KB hexa interp                     | reject A29       |
| F-A29-5    | DEFLATE   | aggregate < 78.65% on 6-repo                                 | reject raw 137 v8 |
| F-A29-6    | DEFLATE   | DEFLATE+A18 chain regression > 1pp vs DEFLATE-only           | reject chain     |
| F-A30-1    | BWT+MTF   | text-heavy lift < +8pp on 5MB stratified                     | reject A30       |
| F-A30-2    | BWT+MTF   | mixed lift < +3pp on 5MB stratified                          | reject A30 mixed |
| F-A30-3    | BWT+MTF   | round-trip byte-eq fails                                     | reject A30       |
| F-A30-4    | BWT+MTF   | SAIS memory > 50MB on 79KB                                   | reject A30       |
| F-A30-5    | BWT+MTF   | SAIS time > 500ms / 79KB hexa interp                         | reject A30       |
| F-A30-6    | BWT+MTF   | aggregate < 78.65% on 6-repo                                 | reject raw 137 v8 |
| F-A30-7    | BWT+MTF   | block size > 79KB chosen → memory blowup                     | enforce ≤79KB cap |
| F-A31-1    | rANS      | rANS saving differs from A16 by > 0.5% (drop-in mode)        | reject A31       |
| F-A31-2    | rANS      | rANS encode NOT 2× faster than A16                           | reject A31 speed |
| F-A31-3    | rANS      | round-trip byte-eq fails                                     | reject A31       |
| F-A31-4    | rANS      | A18-lit-stream lift < +5pp text-heavy                        | reject A31 entropy|
| F-A31-5    | rANS      | rANS state register overflow on 32-bit                       | reject A31       |
| F-A31-6    | rANS      | aggregate < 78.65% on 6-repo                                 | reject raw 137 v8 |
| F-A32-1    | StaticHuff| text-heavy lift < +5pp                                       | reject A32       |
| F-A32-2    | StaticHuff| small-file lift < +10pp (passthrough → encoded)              | reject A32 small |
| F-A32-3    | StaticHuff| round-trip byte-eq fails                                     | reject A32       |
| F-A32-4    | StaticHuff| codebook drift > 5% over 30 days                             | mandate retrain  |
| F-A32-5    | StaticHuff| aggregate < 78.65% on 6-repo                                 | reject raw 137 v8 |

Total: **24 falsifiers** preregistered across 4 candidates.

---

## 7. Non-overlap with prior work (raw 47 sibling-coordination)

The mission brief flags two prior commits to avoid overlap:

- **aa6b3cfe** — A25 source patch. This scout does NOT modify
  `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a25_type_aware.hexa`; A25
  remains as the dispatcher SSOT. The proposed A29-A32 candidates are NEW
  algorithm files (`hxc_a29_*.hexa`, etc.) that A25 dispatch table would
  optionally route to in cycle 3+ AFTER per-class lift is MEASURED.
- **a6ef2d5e** — Size gating. This scout does NOT introduce new size guards;
  any size-class behavior of the candidates is delegated to A25's existing
  `A25_SMALL_FILE_THRESH = 500` and `A25_LARGE_FILE_THRESH = 16384`
  thresholds (per `hxc_a25_type_aware.hexa` lines 135-136).

**Verdict**: Non-overlap CLEAN. This scout is **strictly additive** —
candidate-discovery + design-doc + falsifier preregister; zero modifications
to existing source.

---

## 8. References

- Witten-Neal-Cleary 1987, "Arithmetic coding for data compression",
  CACM 30(6) — basis for A16.
- Howard 1993, "The design and analysis of efficient lossless data
  compression systems" — basis for A26 PPM-D escape mechanism.
- Burrows-Wheeler 1994, "A block-sorting lossless data compression algorithm",
  DEC SRC Research Report 124 — basis for A30 candidate.
- Bentley-McIlroy 1986, "A locally adaptive data compression scheme",
  CACM 29(4) — basis for A30 MTF stage.
- Deutsch 1996, "DEFLATE Compressed Data Format Specification version 1.3",
  IETF RFC 1951 — basis for A29 candidate.
- Duda 2014, "Asymmetric numeral systems: entropy coding combining speed of
  Huffman coding with compression rate of arithmetic coding", arXiv 1311.2540 —
  basis for A31 candidate.
- Nong-Zhang-Chan 2009, "Linear suffix array construction by almost pure
  induced-sorting" — basis for A30 SAIS suffix array.
- n6 verdict a201a6cc: H_0 = 5.755, H_3 = 1.294, H_4 = 0.813 bit/byte —
  text-heavy upper-bound saving anchor.
- Phase 12 forward design (this repo):
  `/Users/ghost/core/anima/docs/hxc_phase12_forward_design_20260428.md`.
- A18 v3-o2 text-heavy ceiling final witness:
  `/Users/ghost/core/anima/state/format_witness/2026-04-28_a18_v3o2_text_heavy_ceiling_final.jsonl`.
- A25 v2 6-repo 78.05% measurement:
  `/Users/ghost/core/anima/state/format_witness/2026-04-28_a25_v2_full_deployment_6repo_80pct_measured.jsonl`.

---

## 9. Compliance summary

- **raw 9 hexa-only**: ✓ all 4 candidates spec'd as pure-hexa integer-only.
- **raw 18 self-host fixpoint**: ✓ all candidates avoid floating-point;
  deterministic across machines.
- **raw 33 NL English fields**: ✓ all design tables + falsifiers in English;
  Korean only in summary narrative per user request.
- **raw 42 jetsam ≤200MB on 79KB**: ✓ memory budgets ≤50MB worst-case (A29).
- **raw 47 cross-repo**: ✓ §7 non-overlap statement; sibling commits
  aa6b3cfe + a6ef2d5e respected.
- **raw 65+68 idempotent**: ✓ all candidates require round-trip byte-eq
  in falsifiers (F-A29-3, F-A30-3, F-A31-3, F-A32-3).
- **raw 71 falsifier-preregistered**: ✓ 24 falsifiers in §6.
- **raw 91 honest C3 STRICT**: ✓ all numbers labelled PROJECTED in §3 and
  §4; only §0 cite-backed metrics labelled MEASURED with witness paths.
- **raw 137 80% Pareto + cmix-ban + A28 forbidden**: ✓ all candidates within
  raw 137 charter; none approach cmix neural-mixer boundary; A28 semantic
  embedding NOT proposed.
- **raw 142 D2 try-and-revert**: ✓ DESIGN-ONLY, no try, no revert; future
  implementation cycles will follow D2 cadence per-candidate.
- **raw 156 algorithm-placement-orthogonality**: ✓ each candidate declares
  placement axis (post-A18-tokenize / pre-A1-raw / drop-in-A16).

---

## 10. Korean summary (사용자 요청 보존)

- **임무**: text-heavy 49% / mixed 58% bottleneck class CEILING advance —
  catalog 미존재 알고리즘 후보 식별 + first-tick 설계 문서.
- **현재 catalog 포화**: A1-A26 모두 LZ-PPM family 또는 type-aware
  dispatcher. **Huffman / BWT / rANS / Static Huffman 부재**. (raw 91
  honest enumeration via grep verified.)
- **gap 산수**: text-heavy class 49.09% → 80% lift = 30.91pp class-local
  → 23.99% byte share × 30.91pp = +7.41pp aggregate. mixed 58.49% → 80% =
  21.51pp × 0.30 share = +6.45pp aggregate. **Combined +5pp on each class**
  ≈ +2.7pp aggregate (78.65% v8 strengthening 게이트 통과 + 80% target ~1pp
  근접).
- **Top 2 추천**:
  1. **A29 DEFLATE (LZ77 + canonical Huffman)** — RFC 1951 표준, LoC ~700,
     text-heavy +13-23pp class lift PROJECTED, aggregate +2.5-5.5pp,
     **CIRCUMVENT** verdict, A18 v1 LZ77 tokenizer 재사용, implementation
     risk LOW. **PRIMARY 추천**.
  2. **A30 BWT+MTF+RLE+entropy (bzip2-class)** — Burrows-Wheeler 1994 + SAIS
     suffix array, LoC ~600, text-heavy +16-29pp PROJECTED (가장 강력),
     aggregate +3-7pp, **CIRCUMVENT** verdict, SAIS implementation 위험 MEDIUM-HIGH,
     A29 다음 사이클 권장.
- **A31 rANS + A32 Static Huffman**: secondary 후보. A31 = A29와 동일
  paradigm 다른 entropy coder; A32 = small-file class 보조 lever (passthrough
  → +20-40pp small-file) — A29 cycle 2 동반 배치 권장.
- **이번 turn deliverable**: 이 design 문서 1개 + 24-falsifier preregister.
  **NO 구현 / NO 커밋 / NO LIVE FIRE** (raw 142 D2 conservative).
- **다음 cycle 진입 게이트**: A29 first-tick `hxc_a29_deflate.hexa` skeleton
  + 5-fixture selftest + witness ledger + 디자인 문서 `hxc_a29_deflate_design_2026_04_29.md`.

---

**End of survey. Design-only. NO MEASURED claims. NO commit this turn.**
