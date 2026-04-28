# HXC A35 v2 — Stage 2 + Stage 3 Activation (Design Delta)

**Date**: 2026-04-29
**Predecessor**: `hxc_a35_source_transform_design_2026-04-28.md` (first tick — Stage 1 only)
**Sigil**: `^o` (UNCHANGED — same module, in-place modification)
**Module**: `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a35_source_transform.hexa`
**Scope**: PASS 1+2+3 selftest only. PASS 4 LIVE FIRE DEFERRED.
**Compliance**: raw 9 hexa-only, raw 18 self-host fixpoint, raw 33 English commit/witness,
raw 42 mac jetsam (RSS <100MB), raw 65/68 idempotent, raw 71 falsifier-preregister,
raw 91 honest C3 STRICT, raw 92 sigil-line, raw 137 cmix-ban, raw 142 D2 try-revert,
raw 156 placement-axis (pre-A1-raw).

---

## 0. Honest framing (raw 91 C3 STRICT)

A35 first tick (commit `7b79b9ff` hexa-lang + `7957bf0f` anima) shipped Stage 1
column reorder ACTIVE; Stage 2 (integer delta varint) and Stage 3 (dictionary
tokenize) were SCAFFOLDING-ONLY no-ops. Rationale at first tick: locale int
parse risk + round-trip safety preferred over saving lift; activation deferred
to PASS 4 LIVE FIRE.

**This v2 turn activates Stage 2 + Stage 3 in-place** within the SAME module
(no new module, sigil `^o` unchanged). Wire format header bumped to
`v=src-xform-v2` to disambiguate v1 readers from v2 wires; v1 readers MUST
identity-revert on `v=src-xform-v2` headers (forward-incompat by design —
first-tick selftest never persisted v1 wires to disk, so no migration burden).

**F1 baseline**: 5-line jsonl shared schema 300B input → 308B v1 wire (-2%
saving, header overhead ~80B dominates). v2 target: lift to net positive
saving on schemaful corpus by combining Stage 2 (delta) + Stage 3 (dict).

**raw 91 honest scope** (UNCHANGED from v1):
- in-sample estimator on 9-fixture selftest only
- corpus-scale measurement DEFERRED to PASS 4 LIVE FIRE
- schemaful_jsonl_ratio: anima 90%, n6 50% (n=10 each, seed=42, v1 baseline)

---

## 1. Stage 2 — Integer delta varint (ACTIVATION SPEC)

### Trigger heuristic

A column is **delta-eligible** iff:
1. All `n_rows` row values parse as ASCII-digit-only integers (signed `-` allowed
   on first character only).
2. NO decimal point `.`, NO scientific notation `e`/`E`, NO locale-thousand-sep
   (`,`/`'`/space).
3. `n_rows ≥ 2` (delta requires at least one prior value).

Locale safety is the critical raw 91 prudence point: real-world jsonl from
non-en-US locales may use `,` as decimal separator. Restricting Stage 2 to
strict ASCII-digit-only with optional leading `-` rejects every locale-formatted
float and avoids round-trip drift.

### Wire format (per column)

```
C<idx>=DELTA:<base_varint>;<delta_1_varint>;<delta_2_varint>;...
```

- `base_varint`: signed varint of `column[0]` absolute value
- `delta_i_varint`: signed varint of `column[i] - column[i-1]` for i ≥ 1
- Separator `;` chosen because ASCII-digit + `-` column never contains it.

### Signed varint encoding (zigzag)

Standard zigzag mapping `n → (n << 1) ^ (n >> 63)`, encoded as 7-bit groups
with continuation MSB. Implementation reuses existing utility patterns from
A34 sub-byte arith module (raw 9 hexa-only).

For first-tick activation simplicity we encode varint as **decimal-string
repr** rather than raw 7-bit bytes — this trades binary compactness for
round-trip determinism on the wire (avoids embedded NUL/control bytes that
the existing `\x1F` separator scheme cannot tolerate). Saving lift on F1
comes from `,`-elimination across 5 rows, not from raw byte savings of varint.

**Saving math** for F1 timestamp+saving columns:
- v1 column `2026-04-28T00:00:00Z` × 5 + sep × 4 = 100B → unchanged (string column)
- v1 saving column `97`,`96`,`95`,`94`,`93` × 5 chars + 4 seps = 14B
- v2 saving column `DELTA:97;-1;-1;-1;-1` = 21B (LARGER on tiny columns)

Honest projection: Stage 2 saving on F1 is **negative** for the saving column
(7B inflation) because monotonic delta on a short 5-row column cannot beat
the literal stringification. Stage 2 try-revert per-column (see §3) routes
the saving column back to literal Stage-1-only encoding.

Stage 2 lift comes from **Stage 3 enum tokenization** (string columns with
low cardinality), not from delta on tiny integer columns. F1 `ev` column
(5 rows of `"first_tick"`) is the actual saving target.

### Decode reverse

1. Detect `DELTA:` prefix on column body.
2. Split on `;`, decode each token as signed varint.
3. Cumulative sum: `column[0] = base; column[i] = column[i-1] + delta_i`.
4. Stringify each integer back to decimal ASCII (locale-independent).

---

## 2. Stage 3 — Dictionary tokenize (ACTIVATION SPEC)

### Trigger heuristic

A column is **token-eligible** iff:
1. `distinct_count(column) < n_rows / 2` (cardinality strictly less than half).
2. `distinct_count ≤ A35_TOKEN_DICT_MAX = 64`.
3. Column is NOT delta-eligible (Stage 2 wins priority on integer columns).
4. `n_rows ≥ 4` — below 4 the dict header overhead dominates.

The `< n_rows / 2` threshold is intentionally loose at first activation
(stricter than v1 design's `≤ 10%` rule which would require 50+ rows).
For F1 (5 rows × `ev:"first_tick"`), distinct=1, threshold=2 → triggers.

### Wire format (per column)

```
C<idx>=DICT:<token_table>;<row_tokens>
```

- `token_table`: distinct values joined by `\x1E` (Record Separator, distinct
  from `\x1F` Unit Separator already in use)
- `row_tokens`: per-row decimal index into token_table, joined by `;`

Bail conditions (revert to literal column):
- Any column value contains `\x1E` or `;` or `\x1F` → bail.
- Any column value contains `:` followed by a literal that could collide with
  `DELTA:`/`DICT:` prefix → resolved by always quoting whole column body when
  prefix sigil is reserved (encoder reads first 6 chars to detect prefix on
  decode).

### F1 projection

`ev` column: 5 rows of `"first_tick"` (12 bytes each with quotes).
- v1 literal: `"first_tick"\x1F"first_tick"\x1F"first_tick"\x1F"first_tick"\x1F"first_tick"` = 60+4 = 64B
- v3 dict: `DICT:"first_tick";0;0;0;0;0` = 5 (prefix) + 12 (tok) + 1 (sep) + 9 (5 indices + 4 seps) = 27B
- Saving: 37B per column (~12% of F1 input 300B).

Combined F1 v2 wire estimate:
- header: 80B (unchanged)
- K + R lines: ~30B (unchanged)
- ts column: ~104B (literal — Stage 2 reject because `:` and `T`/`Z` chars)
- ev column: ~27B (Stage 3 dict)
- saving column: ~14B (Stage 1 literal — Stage 2 reject due to negative saving)
- Total: ~255B vs v1 308B → **+15-17% saving lift** on F1.

If integer stringification of saving column proves favorable (delta encoding
of monotonic descending sequence) Stage 2 may activate; per §1 try-revert
the encoder picks min(literal, delta) per column.

### Decode reverse

1. Detect `DICT:` prefix on column body.
2. Split on first `;` after `DICT:` to separate token table from row indices.
3. Split token table on `\x1E`.
4. Map each row token (decimal int) → token_table[idx] string.

---

## 3. Per-column try-revert (raw 142 D2 graceful)

Stage 2 + Stage 3 are evaluated **per column independently**, not per file.
Each column emits the SHORTEST of:
- literal (Stage-1-only, current v1 wire)
- DELTA varint (Stage 2, if eligible)
- DICT tokenize (Stage 3, if eligible)

Whole-file try-revert (raw 142 D2): if total v2 wire ≥ input length → identity
passthrough (no header, no harm). Same contract as v1.

**Schema detector false-positive guard (F-A35-V2-4)**: Stage 2/3 detection runs
ONLY after Stage 1 build succeeds. Random text never reaches Stage 2/3 (schema
detector identity-routes at the encoder boundary). F1 + F4 fixtures cover
positive + negative paths.

---

## 4. Falsifier preregister (raw 71)

| ID | Spec | Retire condition |
|---|---|---|
| F-A35-V2-1 | Round-trip byte-eq fail on any 9/9 fixture (5 v1 + 4 new) | reject A35 v2 (raw 65/68) |
| F-A35-V2-2 | v2 < v1 saving on schemaful F1 (must lift over -2%) | reject Stage 2/3 activation |
| F-A35-V2-3 | Encoder peak RSS > 100MB on 79KB | reject A35 v2 (raw 42 mac jetsam) |
| F-A35-V2-4 | Schema detector false-positive on random text (Stage 2/3 spurious activation) | reject detector |
| F-A35-V2-5 | encode(encode(x)) ≠ encode(x) — idempotency loss (raw 65/68) | reject A35 v2 |
| F-A35-V2-6 | raw 18 self-host AOT byte-identical fail | reject A35 v2 OR honest C3 if sandbox blocker recurs |

---

## 5. Fixture matrix (PASS 3 selftest, 9 fixtures)

| Fixture | Shape | Detector | Encode behavior | Validates |
|---|---|---|---|---|
| F1 | 5-line jsonl shared schema | SCHEMAFUL | Stage 1+2+3 (saving > v1's -2%) | F-A35-V2-2 lift |
| F2 | 5-line jsonl field-order variance | SCHEMAFUL detected, Stage 1 build bails | identity revert | F-A35-V2-1 graceful |
| F3 | 1-line jsonl | SCHEMAFREE | identity passthrough | F-A35-V2-4 false-pos guard |
| F4 | random ASCII text | SCHEMAFREE | identity passthrough | F-A35-V2-4 false-pos guard |
| F5 | aggregate round-trip on F1..F4 | n/a | byte-eq 4/4 | F-A35-V2-1 (raw 65/68) |
| F6 | 10-line jsonl with monotonic int column | SCHEMAFUL | Stage 2 trigger, delta wire | Stage 2 mechanism |
| F7 | 10-line jsonl with enum field (3 distinct in 10 rows) | SCHEMAFUL | Stage 3 trigger, dict wire | Stage 3 mechanism |
| F8 | 10-line jsonl with `"1.5"` non-int string | SCHEMAFUL, Stage 2 reject | Stage 1 literal, no delta | Locale safety |
| F9 | aggregate round-trip on F6..F8 | n/a | byte-eq 3/3 | F-A35-V2-1 + F-A35-V2-5 |

**Pass criteria**: 9/9 byte-eq + F1 saving > -2% (lift over v1 baseline) +
no schema detector false-positive on F4 + locale safety hold on F8.

---

## 6. raw 91 honest C3 STRICT mandates

- v1 → v2 saving comparison is **in-sample only** (9-fixture synthetic).
- Corpus-scale projection: anima 90% × A35_v2_schemaful_saving / n6 50% ×
  A35_v2_schemaful_saving — both factors require PASS 4 LIVE FIRE.
- AOT byte-identical fixpoint attempted (PASS 3 closure); if sandbox blocker
  recurs (silent rc=0 no-artifact, A32-pattern), **honest C3 disclosure** is
  the deliverable — not a synthetic byte-identical claim.
- NO commit if any of: 9/9 selftest fail, locale safety fail (F8), schema
  detector false-positive (F4).

NO 80% verdict in this document. NO raw 137 v8 strengthening claim.

---

## 7. PASS 4 LIVE FIRE (DEFERRED — next tick)

Out of scope at this v2 activation tick:
- 6-repo aggregate byte-eq saving% measurement
- schemaful_ratio precise estimate at corpus scale
- F-A35-V2-3 RSS measurement on largest schemaful jsonl
- Latency measurement on 1MB+ schemaful corpus
- A35 v2 stacking with A1 + A19 + A33 + A29 chain

---

## 8. References

- v1 design: `/Users/ghost/core/anima/docs/hxc_a35_source_transform_design_2026-04-28.md`
- v1 commit: hexa-lang `7b79b9ff` + anima `7957bf0f`
- Module (modified in-place this tick):
  `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a35_source_transform.hexa`
- Witness ledger (this tick):
  `/Users/ghost/core/anima/state/format_witness/2026-04-29_a35_v2_stage_2_3.jsonl`
- Sister modules in-flight: A33 (sigil ^h), A34 v2 (sigil ^l) — DO NOT modify.
