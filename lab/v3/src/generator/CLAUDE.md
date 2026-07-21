# src/generator — the synthetic drill language (H_003)

The rig's corpus (`ARCHITECTURE.json` -> `rig-corpus`). Deterministic, stdlib-only,
$0. Nothing here trains anything: it emits the streams, probes and eval items that
the H_003 gate measures and the H_004 pilot would train on.

## Key files

- `lang.py` — jamo composition (Hangul's algorithmic syllable block supplies the
  COMPOSITION RULE; the vocabulary is invented, not Korean). `render`/`parse` are
  asserted inverses; `to_jamo`/`from_jamo` likewise.
- `spec.py` — the frozen `GenSpec`: 512 stems, 128 held-out, 64 phase-1 affixes
  (4 NEG), phase 2 = 52 carried + 12 NOVEL NEG allomorphs, Zipf collocations with
  a phase-2 shift. Everything is STORED, not regenerated. `spec_hash()` is the
  sha256 that goes in the card.
- `stream.py` — `stream`/`stream_sample`/`probes`/`eval_items`.
- `codec.py` — `fit_bpe_jamo`/`Codec.boundaries`/`boundary_delta_matrix`/
  `boundary_shift_rate`/`atomicity_audit`.
- `audit.py` — `leak_scan`/`heldout_neg_cooccurrence` (parse-based, mark-keyed).
- `materialize.py` — `vocab`/`encode_ids`/`stream_ids`/`eval_encoded`: encode phase streams
  and eval items to token ids under a given codec, so codec-fairness (each arm scored under
  its OWN tokenization) is established once for every training path.

## Rules

- **One entropy source** — every draw descends from `random.Random(spec["seed"])`.
  No clock, no `os.urandom`, no set-iteration order (sort before returning).
- **BPE ties are frozen** as (count desc, pair lexicographic asc). Unfrozen ties are
  silent nondeterminism: two fits disagree on the merge list and therefore on every
  boundary downstream.
- **Explicit flip supervision is mandatory**, not stylistic. Per v1's NAT-ATOM law
  atomicity AMPLIFIES a taught signal and cannot source one; a stream with only
  shifted collocation statistics reads chance even in the oracle arm.
- **Held-out stems never meet a NEG affix** in either phase — they appear with PLAIN
  affixes, so only the COMPOSITION is novel. Otherwise the eval measures coverage.
- **Probe framing == stream framing** (sentinel-delimited). v1's instrumentation bug
  #3 was exactly this mismatch and it made four arms look dead.

## Gotcha

- Boundaries are indexed in **jamo positions, not bytes** — a deliberate deviation
  from the design's "64 bytes". Each conjoining jamo is exactly 3 UTF-8 bytes, so a
  byte-indexed matrix would have 2/3 of its columns identically zero and deflate the
  boundary-shift rate ~3x. Probes are still exactly rectangular (256 x 64 jamo =
  256 x 192 bytes). Jamo is the codec's base alphabet, so the index is still
  codec-independent — which was the actual requirement.
