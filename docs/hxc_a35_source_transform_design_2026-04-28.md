# HXC A35 — Source-Transform Schema Delta + Tokenizer (First Tick)

**Date**: 2026-04-28
**Phase**: Post-A29/A33 byte-stream ceiling (entropy verdict commit `4cd8e62da`)
**Sigil**: `^o` (lowercase, raw 92 sigil-line, distinct from `^A..^Z` and `^c/^v/^w`)
**Scope**: PASS 1+2+3 selftest only. PASS 4 LIVE FIRE DEFERRED.
**Compliance**: raw 9 hexa-only, raw 18 self-host fixpoint, raw 42 mac jetsam (RSS <100MB),
raw 65/68 idempotent, raw 71 falsifier-preregister, raw 91 honest C3 STRICT,
raw 92 sigil-line, raw 137 cmix-ban, raw 142 D2 try-revert, raw 156 placement-axis (pre-A1-raw).

---

## 0. Honest framing (raw 91 C3 STRICT)

A35 is **NOT another byte-stream compressor**. A19/A33 sit AFTER the bytes have been
emitted and squeeze the resulting byte stream. A35 sits **BEFORE** byte-emit and
**rewrites the source representation itself**, with the goal of **reducing H_n of the
input** that the downstream byte-stream stack (A1 → A19 → A33 → A29) will see.

Per entropy verdict commit `4cd8e62da`:

> "Per-file H_4 must drop to ~1.6 bits/byte equivalent; achievable on highly
>  schemaful jsonl where field names repeat 100x+ via column-oriented reordering"

A19 v2 (sigil `^Z`) per-corpus shared dict measured **+0.15pp slice / 0.00pp
scale-out** — diminishing return at the byte-stream layer. A35 changes the layer:
schema-aware delta + tokenization at the source level can collapse the field-name
repetition surface BEFORE entropy coding sees it, which is the **only path #3** in
the entropy verdict's 80% list (`source_transform_then_compress`).

**Honest scope disclosure (in-sample estimator only)**:

- A35 saving is achievable **only on the schemaful_jsonl subset** of the corpus.
- The ratio of schemaful jsonl vs schemafree text/non-jsonl in anima/n6 is **not
  yet measured at corpus scale**. This first-tick deliverable includes a 10-file
  random sample (§7) but does NOT extrapolate to corpus-wide saving.
- For schemafree input, A35 MUST be a **try-and-revert identity passthrough**
  (raw 142 D2). No spurious transform, no harm to non-schemaful inputs.

---

## 1. Placement axis (raw 156)

```
[input bytes]
     │
     ▼
┌─────────────────────────────────────────┐
│ A35 source-transform (sigil ^o)         │  ← pre-A1-raw (NEW PLACEMENT)
│  schema_detect →                        │
│   if schemaful: column_reorder + delta  │
│                 + dictionary tokenize    │
│   else:        identity passthrough     │
└─────────────────────────────────────────┘
     │
     ▼
[A1 raw byte canonicalization]            ← existing chain head
     │
     ▼
[A19 cross-file dict / A33 / A29]         ← existing byte-stream stack
     │
     ▼
[wire output]
```

A35 occupies a **strictly NEW axis**: source-level vs byte-stream. It does NOT
overlap A19 (cross-file byte dict), A29 (deflate), A33 (zstd-class), A8 (column
stat post-A1), A11 (cross-row delta post-A1), or A20 (schema-aware BPE post-A1).
The axis distinction: A35 emits a **DIFFERENT byte stream** for the downstream
chain to see; A8/A11/A20 emit the **SAME byte stream** in restructured form.

**raw 142 D2 try-and-revert contract**: `a35_encode(x)` returns
`a35_v1_wire` only if `len(wire) < len(x)`; otherwise returns `x` unchanged
(identity passthrough — no header overhead, no harm). Guarantees A35 never
inflates schemafree input beyond a constant detection cost (one schema-detect pass).

---

## 2. Four transform stages (encoder spec)

### Stage 1 — JSON column-oriented reordering

**Trigger**: `schema_detect(input) == SCHEMAFUL_JSONL`.

**Mechanism**: jsonl input has shape `{ "k1": v1_a, "k2": v2_a, ... }\n
                                       { "k1": v1_b, "k2": v2_b, ... }\n
                                       …`

Field names `"k1"`, `"k2"`, … repeat once per row. After column-reorder:

```
header: keys=[k1, k2, …]
column k1: [v1_a, v1_b, v1_c, …]
column k2: [v2_a, v2_b, v2_c, …]
…
```

Each field name appears **once** instead of N times. The row-order delimiter
becomes implicit (column index). For 100-row × 5-field jsonl with 8-char keys,
this saves `(100−1) × 5 × ~10 bytes ≈ 5KB` of pure field-name repetition.

**raw 91 honest projection**: schemaful jsonl with 5+ fields and 50+ rows →
projected H_n reduction of 30-50pp on the field-name surface. Untested at
corpus scale; F-A35-1 round-trip + first-tick fixture saving will validate the
mechanism but NOT extrapolate. See §6 disclosure.

### Stage 2 — Integer delta encoding

**Trigger**: column[i] is detected as numeric (all rows parse as int or float).

**Mechanism**: replace `[v1, v2, v3, …]` with `[v1, v2−v1, v3−v2, …]` then
varint-encode each delta. For monotonic timestamps, sequence IDs, or
slowly-changing counters, deltas are 1-2 bytes vs 6-12 byte raw integers.

**Reverse**: cumulative sum of varints reconstructs the original column.

**Honest scope**: only applied when `monotonic_or_small_delta_ratio > 70%`
of column entries qualify (heuristic, validated against F-A35-2 schemafree
revert path).

### Stage 3 — Dictionary tokenization (enum-like fields)

**Trigger**: column[i] has fewer than `A35_TOKEN_DICT_MAX = 64` distinct values
across all rows AND distinct value count ≤ 10% of row count.

**Mechanism**: assign each distinct value a small integer token (1-byte if
≤256 distinct, 2-byte varint otherwise). Emit dictionary as header,
column body becomes a token stream.

**Reverse**: dictionary lookup per token reconstructs string column.

### Stage 4 — Idempotent reverse transform (raw 65/68 mandatory)

**Reverse pipeline** (executed by `a35_decode`):

1. Read header (`# a35:s1 v=src-xform-v1 n=<bytes> mode=<schemaful|identity>`)
2. If `mode == identity`: emit body bytes unchanged.
3. Else: parse column dictionary header → for each column:
   - Stage 3 reverse: token → string lookup
   - Stage 2 reverse: varint cumulative sum (if numeric column)
4. Stage 1 reverse: re-emit row-oriented jsonl with original field order
   preserved (header keys[] determines reorder back to row form).

**Byte-eq invariant (raw 65/68)**: `decode(encode(x)) == x` for all x.
The header MUST carry `field_order_hash` (FNV-1a of original field-name
concatenation per row) to detect any field-order variance and FORCE
schemafree fallback (F-A35-2 graceful revert path).

---

## 3. Schema detector (PASS 2.5 validation)

Heuristic decision tree (cheap, one pass):

```
schema_detect(input):
    1. Split input on '\n'. Filter empty lines. Need ≥ 2 lines.
    2. For each non-empty line: try parse as JSON object.
       If any line fails to parse OR is non-dict → SCHEMAFREE.
    3. Compute keyset(line[0]) and keyset(line[N//2]) and keyset(line[-1]).
       If all three match → SCHEMAFUL_JSONL.
       If ≥ 2 of 3 match → SCHEMAFUL_JSONL (graceful, allows tail-row drift).
       Else → SCHEMAFREE_VARIABLE (Stage 1+2+3 not safe; identity passthrough).
```

**False-positive risk** (F-A35-6): random text that happens to begin with `{`
and `\n`-separated JSON-shaped lines. Two-line minimum + JSON-strict parse +
explicit keyset comparison eliminates the easy false positives.

**False-negative risk**: schemaful jsonl with optional fields (key drift across
rows). Mitigated by 2-of-3 keyset majority rule. Documented as "graceful — A35
identity-reverts on row 142 D2 try-revert at the encoder boundary if the
column-reorder produces a wire larger than the input".

**Selftest coverage** (PASS 2.5):
- random ASCII text → SCHEMAFREE detected ✓
- 5-line jsonl shared schema → SCHEMAFUL detected ✓
- 1-line jsonl → SCHEMAFREE detected (line minimum) ✓
- 5-line jsonl with field-order variance row-1 → SCHEMAFUL detected, but Stage 1
  reorder fails byte-eq round-trip → encoder identity-reverts (raw 142 D2)

---

## 4. Wire format

```
# a35:s1 v=src-xform-v1 n=<input_bytes> mode=<schemaful|identity> cols=<N> rows=<R>
# a35:dict <colname>=<base64url-token-table>     (one line per tokenized column)
# a35:hdr  keys=<base64url-of-keys-list> order_hash=<hex32>
^o<base64url-payload>
```

Header overhead: ~80-200 bytes for schemaful path; **0 bytes** for identity
path (raw 142 D2 try-revert short-circuits header emit).

`^o` sigil is raw 92 sigil-line compliant, lowercase distinct from `^A..^Z` and
existing lowercase sigils `^c` (A32), `^v/^w` (A23), `^Z` (A19 v2 — uppercase).
Sigil-distinct verified against `<repo-root>/../hexa-lang/self/stdlib/hxc_a*.hexa`.

---

## 5. Falsifier preregister (raw 71)

| ID | Spec | Retire condition | First-tick status |
|---|---|---|---|
| F-A35-1 | Round-trip byte-eq fails on any 5/5 fixture | reject A35 (raw 65/68) | gated PASS 3 selftest |
| F-A35-2 | Schemafree input → not identity passthrough (no harm contract) | reject A35 | gated PASS 3 fixture F4 |
| F-A35-3 | Encoder peak RSS > 100MB | reject A35 (raw 42 mac jetsam) | DEFERRED PASS 4 measurement |
| F-A35-4 | Encoder latency > 500ms per 1KB | reject A35 (production budget) | DEFERRED PASS 4 measurement |
| F-A35-5 | raw 18 self-host AOT byte-identical fail (interp ≠ AOT stdout) | reject A35 | gated PASS 3 AOT |
| F-A35-6 | Schema detector false-positive on random text fixture | reject schema_detect heuristic | gated PASS 2.5 (rate ≤ 5%) |

---

## 6. raw 91 honest C3 STRICT disclosure

**In-sample estimator only**: this design doc and first-tick selftest measure
the A35 mechanism on **synthetic fixtures** (5/5). No corpus-scale saving claim
is made. Specifically:

- **NOT MEASURED** at first tick: anima 6-repo aggregate, n6 aggregate, schemaful
  ratio per-corpus contribution.
- **NOT EXTRAPOLATED**: A35 saving on schemaful subset → corpus-wide. The
  schemafree subset will identity-passthrough (0pp contribution); corpus-wide
  saving = (schemaful_ratio × A35_schemaful_saving) − header_overhead. Both
  factors require PASS 4 LIVE FIRE measurement.
- **PROJECTED ONLY**: 30-50pp on the field-name surface for 5-field × 50-row
  schemaful jsonl. Synthetic projection — entropy verdict's "100x+ field
  repetition" requires very specific corpus shape.

NO 80% verdict in this document. NO raw 137 v8 strengthening claim.

---

## 7. anima/n6 schemaful_jsonl_ratio sample (10 files each)

Sample method: `random.seed(42)`, glob `*.jsonl` in
`<repo-root>/state` and `<repo-root>/../nexus/n6`, filter
size > 50B, take first 10 after shuffle. Schemaful = ≥70% of first 10 lines
share line[0] keyset (parse all as JSON dict).

### anima/state (29 candidate files)

| verdict | match% | size (B) | filename |
|---|---|---|---|
| schemaful | 1.00 | 1960 | anima_eeg_core_phase4_paradigms_integration_audit.jsonl |
| schemaful | 1.00 | 2419 | alm_r14_corpus_skeleton.jsonl |
| schemaful | 1.00 | 4111 | serve_alm_persona_log.jsonl |
| schemaful | 1.00 | 1150 | phi_cpu_synthetic_4path.jsonl |
| schemafree_variable | 0.20 | 2090 | cross_repo_sync_log.jsonl |
| schemaful | 1.00 | 960 | anima_eeg_behavioral_correlates_selftest.jsonl |
| schemaful | 0.75 | 675 | h100_weight_precache_progress.jsonl |
| schemaful | 1.00 | 33913 | asset_archive_log.jsonl |
| schemaful | 1.00 | 885 | cross_repo_links.jsonl |
| schemaful | 1.00 | 3024 | anima_eeg_impedance_ledger.jsonl |

**anima schemaful_jsonl_ratio = 9/10 = 90%** (1/10 schemafree_variable due to
heterogeneous keysets row-to-row in `cross_repo_sync_log.jsonl`).

### nexus/n6 (17 candidate files)

| verdict | match% | size (B) | filename |
|---|---|---|---|
| schemaful | 1.00 | 53913 | periodic_table_118.jsonl |
| schemaful | 1.00 | 60419 | atlas_phase6_crossscale.jsonl |
| not_json | — | 35300 | atlas_phase47_canonical_bridges.jsonl |
| schemafree_variable | 0.50 | 17435609 | atlas.blowup.jsonl |
| schemaful | 1.00 | 1245 | n6_physics.jsonl |
| schemaful | 1.00 | 10844 | atlas.blowup.events.jsonl |
| not_json | — | 122894 | atlas_phase48_approx_expr_bridges.jsonl |
| schemaful | 1.00 | 64814 | cross_engine_bus.candidates.jsonl |
| not_json | — | 428533 | atlas_phase45_symmetry.jsonl |
| too_short | 1 line | 397 | discovery_rate.jsonl |

**n6 schemaful_jsonl_ratio = 5/10 = 50%** (3/10 are non-JSON despite `.jsonl`
extension; 1/10 schemafree_variable; 1/10 single-line file too short).

### Honest interpretation (raw 91 C3 STRICT)

- **anima 90% / n6 50%** is a 10-file in-sample point estimate with seed=42;
  90% confidence interval (binomial) for n6 is roughly **[24%, 76%]** at n=10.
- The n6 corpus has a substantial **non-JSON-but-named-`.jsonl`** subset
  (atlas_phase47/48/45) that A35 schema_detect MUST identity-revert on.
  This is a real-world false-positive risk for any heuristic that ignores the
  JSON-parse step; the proposed detector parses each line strict-JSON, so
  these files will correctly route to identity passthrough.
- **NOT a corpus-wide saving claim**. A35 saving on n6 will be bounded above
  by `~50% × A35_schemaful_saving`, with measurement-pending wide CI.

---

## 8. First-tick selftest plan (PASS 1+2+3 + 5 fixtures)

| Fixture | Input shape | Expected schema_detect | Expected encode behavior | Validates |
|---|---|---|---|---|
| F1 | 5-line jsonl, 3-field shared schema | SCHEMAFUL | column_reorder + delta + token, target ≥70% size reduction in body | Stage 1+2+3 mechanism |
| F2 | 5-line jsonl, field-order variance row-1 | SCHEMAFUL detected | encode tries reorder, byte-eq round-trip fails OR wire > input → identity revert | F-A35-2 graceful revert |
| F3 | 1-line jsonl | SCHEMAFREE (line minimum) | identity passthrough | F-A35-2 short-input |
| F4 | 200B random ASCII text | SCHEMAFREE | identity passthrough, header NOT emitted | F-A35-6 false-positive guard |
| F5 | F1+F2+F3+F4 round-trip | n/a | `decode(encode(x)) == x` byte-eq for all 4 | F-A35-1 (raw 65/68) |

**Pass criteria**: all 5/5 byte-eq + interp output sha256 == AOT output sha256
(F-A35-5 raw 18 self-host fixpoint).

---

## 9. PASS 4 LIVE FIRE (DEFERRED — next tick)

Out of scope at first tick:
- 6-repo aggregate byte-eq saving% measurement
- schemaful_ratio precise estimate at corpus scale (current 10-file sample → CI too wide)
- F-A35-3 RSS measurement on largest schemaful jsonl
- F-A35-4 latency measurement on 1MB+ schemaful corpus
- A35 stacking with A1 + A19 + A33 + A29 chain (composite saving)
- chain-amortize delta (does A35 still help after A19/A33 saw the byte stream? expected NO — A35 must be pre-A1-raw)

---

## 10. References

- Entropy verdict: commit `4cd8e62da` —
  `<repo-root>/.hxc_aot/hxc_a25` history line; verdict text
  archived in commit message body.
- A29 v3 baseline: anima 50.83% / n6 60.62% (commit `4cd8e62da` body).
- A19 v2 sigil ^Z scale-out result: +0.15pp slice / 0.00pp scale-out.
- Skeleton module (this tick):
  `<repo-root>/../hexa-lang/self/stdlib/hxc_a35_source_transform.hexa`
  (~600 LoC target, sigil `^o`).
- Witness ledger (this tick):
  `<repo-root>/state/format_witness/2026-04-28_a35_first_tick.jsonl`.
