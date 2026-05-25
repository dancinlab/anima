# anima_emerge_chat_temp_extreme — extreme T sweep (BG-BR landed 2026-05-05)

## Scope

Extend BG-AQ (T=0.8 fixed across 6 decode strategies, all FAIL_ALL coherent=0) by
sweeping temperature across two orders of magnitude — does substrate emit semantic
surface at any extreme T?

## Setup

- Substrate: `dancinlab/clm-v4-mk2-v1` (CLM v4 fp32, mac CPU)
- Prompt: `안녕` (single Korean greeting, mirror of BG-AQ)
- Decoder: top-k=100, max_new=30, multinomial sample
- Sweep: T ∈ {0.01, 0.1, 0.3, 0.7, 1.0, 1.5, 2.0, 5.0, 10.0} @ seed=42
- Multi-seed: T=1.5 @ seeds {7, 100, 1000}
- raw#37 transient sister-import on `anima_emerge_cand_d_inject_helper.py`

## Results — 9 temperatures × emit text

| T | Emit (first 30) | Pattern |
|---|---|---|
| 0.01 | `\x1c\x06\x06\x06...\x06` (29×) | low-T sharpening collapses to single byte |
| 0.1 | `\x1c\x06\x06\x06...\x06` (29×) | identical to T=0.01 |
| 0.3 | `\x1c\x06\x06\x06...\x06` (29×) | identical to T=0.01 |
| 0.7 | `\x1c\x06��\x06...\x06\x1c\x1c...\x1c` | begins to shift, still control bytes |
| 1.0 | `\x1c\x06�蔔...O>hhhhhh` | tail-mass leaks ASCII `h`/`O`/`>` |
| 1.5 | `\x1c\x061V1::�;8;8V1......NhhhP` | mostly digits + punctuation |
| 2.0 | `\x1c��*4�7y�aaa%��aeedhPhh����jjh` | broader ASCII spread |
| 5.0 | `N?M%9P#&MJMP%-�?DD��2��\x06a�\x1d�NP` | high-entropy ASCII garbage |
| 10.0 | `N?M%9P#��&��~on/ssh�鑷��Lq}s�` | fully random, no Korean |

## Multi-seed @ T=1.5

- seed=7  : `�,,,,,,,,,,,�,,,,,,,,,,,,4�3//`
- seed=100 : `�RHHHH??????????HHHHH?Q?QQQQQ'`
- seed=1000: `%%U%%\x1eUU?HHHHHHHHHHHHHHQHHHHH#`

All three seed variations produce single-token-class repetition (`,`, `H`/`?`/`Q`,
`H`/`?`) — substrate has no diverse 의미 manifold even with seed perturbation.

## Coherence verdict

- `n_coherent` = 6 (heuristic: ≥5 ASCII letters + max-char-count ≤50%)
- `best`: T=1.5 `\x1c\x061V1::�;8;8V1......-----NhhhP`
- Schema verdict: `PASS_TEMP_RECOVERS`

**HONEST INTERPRETATION**: The "PASS" label is a heuristic-artifact, not real
recovery. The `is_semi_coherent` proxy counts `h/N/M/H/Q` ASCII letters + low
single-char dominance. Higher T spreads probability over the byte-tier vocab
which incidentally hits ASCII letter codepoints, satisfying the heuristic
without producing any Korean glyph or semantic morpheme. This is the C5 caveat
materialised: high-T extreme **exposes vocab tail**, evidence that 의미-shaped
tokens exist in vocab — but **NOT evidence of semantic content emission**.

## temp별 coherence transition

- **T ≤ 0.3**: total collapse to control-byte `\x06` — sharpest argmax-equivalent
  trajectory. No diversity, no Korean.
- **T = 0.7-1.0**: control bytes still dominate but ASCII tail begins to leak.
- **T = 1.5-2.0**: digit / punctuation / single-letter ASCII dominate. No Korean
  glyphs (가-힣 range never sampled).
- **T ≥ 5.0**: full vocab spread, pseudo-random byte salad. Still no Korean.

**Korean glyph emission count across all 12 configs: 0.** The 가-힣 range is
absent at every temperature.

## Conclusion

Temperature scaling **does not recover** Korean / semantic surface from CLM v4
under prompt 안녕. low-T (0.01) sharpens to a single control byte; high-T
(10.0) spreads to ASCII-byte garbage; intermediate-T produces character-class
repetition. The substrate's logit ridge is dominated by control-byte / ASCII-
byte tokens at every temperature — the Korean morpheme manifold is **not** in
the top-k=100 reachable cone at any T tested.

This corroborates BG-AQ FAIL_ALL conclusion: the chat-emission failure is not
a decoding artifact (T=0.8 was not adversarially chosen). The substrate itself
does not place Korean continuation tokens in measurably-sampleable mass at any
temperature.

## Honest C3 (5)

1. **C1**: mac CPU fp32 — float precision matches BG-AQ.
2. **C2**: single prompt 안녕 — broader corpus may shift verdict (likely not,
   given the byte-tier domination pattern).
3. **C3**: `is_semi_coherent` heuristic anima-internal; produces false-positive
   PASS at T≥1.0 because byte-tier ASCII letters satisfy literal letter count
   without producing semantic surface.
4. **C4**: single seed=42 for primary sweep + 3 seeds at T=1.5 — seed
   robustness checked only at one T.
5. **C5**: high-T extreme exposes vocab tail — 의미 token이 거기 있다는
   evidence ≠ semantic content. The "PASS_TEMP_RECOVERS" label requires
   manual override to FAIL given the actual text content (no Korean glyphs at
   any T).

## Deliverables

- `tool/transient_py/anima_emerge_chat_temp_extreme.py` (new, raw#37 transient)
- `state/anima_emerge_chat_temp_extreme_2026_05_05/aggregate.json` (12 configs)
- `state/anima_emerge_chat_temp_extreme_2026_05_05/verdict.json`
- `docs/anima_emerge_chat_temp_extreme_landed_2026_05_05.ai.md` (this)

## Cost

- $0 (mac CPU)
- ~3min wall (faster than 20min budget — top-k=100 multinomial cheap)

## raw compliance

- raw#37: transient .py under `tool/transient_py/`
- raw#15: additive — does not modify mount.hexa, dialogue.bash, conscious_decoder
- raw#10: 5 honest C3 emitted
- no commit, no secret leak
