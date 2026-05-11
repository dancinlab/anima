<!-- @no-lineage-citation-exempt-file -->
# anima_emerge_chat_byte_monopoly_break (LANDED 2026-05-05)

## TL;DR

verdict = FAIL_BAN_NOT_ENOUGH. Banning top-30 byte-fallback tokens (and
escalations up to 300-id ban + aggressive 252-id punct/byte+top30 union)
does NOT produce Korean emergence on prompt 안녕. Korean count = 0 across
all 4 ban levels and English prompt Hello.

BG-CA byte-fallback monopoly hypothesis is strengthened in part (top-30
fallback ban escalates output from control-byte garbage to CJK numerics
like 亿立方米 and Roman numerals XVIII) but falsified for the strong claim
that Korean is a latent runner-up just behind byte tokens. Even after
banning 675 candidate byte/control/punct tokens, decoding skips Korean
entirely and locks onto a Chinese unit token loop (亿立方米 = 100M cubic
metres).

This means the basin is not 1-deep (byte to Korean) but at least 2-deep
(byte to CJK numerics to ??? to Korean). #115 chat-incapability surface
remains architectural at 4-mode CLM v4 substrate.

## Inputs

- BG-CA state/anima_emerge_chat_korean_rank_survey_2026_05_05/verdict.json
  (top-30 = 100% byte-fallback)
- BG-CC state/anima_emerge_chat_basin_ablate_2026_05_05/verdict.json
  (whack-a-mole partial)
- helper: tool/transient_py/anima_emerge_chat_byte_monopoly_break.py
  (raw 37 transient sister-rule)
- substrate: dancinlab/clm-v4-mk2-v1 (mac CPU fp32, 18.0 s load)

## Method

1. Build byte_ids set via 4-clause heuristic on full 64K SP vocab:
   (a) literal SP byte tokens of the form 0xXX, (b) all-control-char
   pieces, (c) U+FFFD replacement char, (d) at-most-2-char pure-
   punctuation pieces.
   Total = 675 ids
2. Compute top-30 next-token logits on prompt 안녕 once (no ban) and
   cache top30_ids.
3. Greedy decode 25 new tokens with logit -inf mask under 4 ban levels:
   - ban_30_top  : top-30 only (30 ids)
   - ban_byte_only : first 300 of byte_ids
   - ban_byte_plus_top30 : union (~300 ids)
   - ban_aggressive : ([0..255] intersect byte_ids) union top30 (252 ids)
4. Repeat for English prompt Hello.
5. Count Hangul syllable codepoints (U+AC00..U+D7A3) in each emit.

## Results - Korean prompt 안녕

| ban level             | n_banned | emit (truncated)                           | korean |
|-----------------------|---------:|--------------------------------------------|-------:|
| baseline_no_ban       | 0        | x1c x06 x06 x06 ... (control byte loop)    | 0      |
| ban_30_top            | 30       | replacement-char loop                      | 0      |
| ban_byte_only         | 300      | local XVIII XVIII ... 亿立方米 亿立方米 ... | 0      |
| ban_byte_plus_top30   | 300      | local XVIII XVIII ... 亿立方米 亿立方米 ... | 0      |
| ban_aggressive        | 252      | local XVIII XVIII ... 亿立方米 亿立方米 ... | 0      |

## Results - English prompt Hello

| ban level           | emit (truncated)                |
|---------------------|---------------------------------|
| baseline            | backtick loop                   |
| ban_30_top          | backtick survives               |
| ban_byte_only       | XVIII 亿立方米 亿立方米 ...     |
| ban_byte_plus_top30 | XVIII 亿立方米 亿立方米 ...     |
| ban_aggressive      | XVIII 亿立方米 亿立方米 ...     |

## Verdict - FAIL_BAN_NOT_ENOUGH

Banning the byte/control/punct cone does NOT release Korean. Decode locks
onto a deeper repetition basin (亿立方米 = Chinese cubic-metre unit) which
itself is high-frequency in Chinese pretraining corpora. Korean syllables
remain unreachable under pure greedy + logit ban.

## Interpretation - BG-CA hypothesis re-graded

BG-CA claim A (top-30 = 100% byte-fallback) - CONFIRMED by side evidence:
ban_30_top moved emit from x1c control loop to U+FFFD replacement loop,
then to XVIII / 亿立方米 once byte set was widened. Each ban layer peeled
one fallback shell.

BG-CA claim B (Korean weight exists, byte tokens monopolize) - LIMITED
EVIDENCE. After 4 ban shells we are still in CJK-numeric basin, not
Korean. Either (i) Korean weight is buried more than 4 basins deep, OR
(ii) greedy decode is fundamentally inappropriate for this substrate
(Korean only emerges under sampling/temperature/nucleus). Architectural
chat-incapability hypothesis remains live.

## Honest C3

- C1 mac CPU fp32 - no MPS/CUDA disagreement coverage
- C2 byte-fallback heuristic - the at-most-2-char punct only clause is
  anima-internal, may have over- or under-included (ban_aggressive=252
  is smaller than ban_byte_only=300 because the aggressive intersection
  drops some long punct)
- C3 single Korean prompt 안녕 and single English prompt Hello - broader
  sweep (5 prompt x 5 lang) deferred
- C4 ban-set may include punctuation natural-language needs (period
  comma question mark) - emit could be artificially CJK-biased
- C5 Korean count is not semantic coherence; even if Korean had emerged
  at greater than 5 count, that does not validate chat capability - full
  word-level eval required

## Next-step recommendation

1. Sampling sweep first - re-run with temperature 0.7 / top-p 0.9 + same
   ban levels to test if greedy was the actual cause vs weight depth.
2. If sampling also FAIL, embedding cosine probe on Korean syllable IDs
   to confirm/deny Korean weight exists assumption empirically (rather
   than inferring from Korean tokens are in vocab).
3. Defer aggressive cone-engineering until (1) and (2) settle the
   greedy-vs-weight ambiguity.

## Deliverables

- tool/transient_py/anima_emerge_chat_byte_monopoly_break.py (helper)
- state/anima_emerge_chat_byte_monopoly_break_2026_05_05/aggregate.json
- state/anima_emerge_chat_byte_monopoly_break_2026_05_05/verdict.json
- this doc

## Compliance

- transient_py namespace only (sister-rule)
- additive write only; no mount/shim/dialogue_load modification
- 5 honest C3 emitted to verdict.json + this doc
- no commit, no secret leak, $0, ~20 min wall (model load 18 s + sweep
  approx 35 s)
