# anima emerge chat lexical baseline — LANDED 2026-05-05

**BG-CE** — bigram/trigram lexical baseline vs CLM v4 emit — final
12-closure sanity probe — $0 mac CPU — wall ~1.1 min.

## Question

After 12 successive closures (BG-AS through BG-BR) all converging on
`ARCHITECTURAL_CHAT_DEAD`, one sanity question remained: **does the
substrate emit MORE Korean signal than uniform-random vocab sampling, or
has CLM v4 degenerated below truly-random output?**

The answer disambiguates two #115 hypotheses:

1. `ARCHITECTURAL_PRESERVES_WEAK_KOREAN_PRIOR` — substrate routes
   Korean prompt into Korean-leaning token region (≥ random vocab
   Korean-char rate). Chat-cap dead, but byte distribution preserved.
2. `ARCHITECTURAL_DEGENERATE_WORSE_THAN_RANDOM` — substrate collapses
   into a fixed-point in vocab tail (control-byte / repeat) that
   contains LESS Korean than uniform 64K-vocab sampling. The trained
   distribution is gone, not just misaligned.

## Setup

- model: `dancinlab/clm-v4-mk2-v1` (CLM v4 mk2 v1)
- platform: mac CPU fp32, `.venv-eeg/bin/python` (torch 2.11.0)
- prompt: `"안녕"`
- emit: 50 greedy tokens, argmax of last-position logits
- baselines (seed=42):
  - **A** CLM v4 greedy emit (50 tokens)
  - **B** random vocab uniform over 64,000 SP pieces (50 tokens)
  - **C** random Korean-only — filter SP pieces to those containing
    Hangul `[가-힣]` then sample uniform (50 tokens, 5701 candidates)
  - **D** gold natural Korean SP encode → SP decode round-trip
- evaluation: per-text Hangul / ascii_letters / digits / control-char
  counts and ratios

## Results — character composition

| baseline | korean | ascii | digits | control | total | korean% |
|---|---|---|---|---|---|---|
| **(A) CLM v4 emit** | **0** | **0** | **0** | **50** | **50** | **0.0%** |
| (B) random vocab | 15 | 66 | 16 | 0 | 220 | 6.8% |
| (C) random Korean-only | 124 | 0 | 0 | 0 | 159 | 78.0% |
| (D) gold SP round-trip | 23 | 0 | 0 | 0 | 32 | 71.9% |

CLM emit raw text: a single `0x1C` control byte followed by 49 repeats
of the `0x06` control byte — a 1-token greedy fixed point.

## Verdict

**`CLM_WORSE_THAN_RANDOM` — `ARCHITECTURAL_DEGENERATE_WORSE_THAN_RANDOM`**

- CLM emit Korean count = 0 < random vocab Korean count = 15
- CLM emit control-char count = 50 > random vocab control-char count = 0
- Both axes (lower Korean AND higher control) point to substrate
  degeneration BELOW uniform-random baseline

The trained byte distribution is **not** preserved. Greedy decode
collapses to a 1-token control-byte fixed point within 1 step of the
prompt. Random uniform vocab sampling produces 6.8% Hangul characters
and zero control bytes — the substrate is strictly worse than picking
SP pieces uniformly at random.

## #115 Final Classification

- **Lane**: `CHAT_CAPABILITY_LANE_FAIL_TRUE_CLOSED` — final closure
- **Mechanism**: greedy fixed-point attractor at SP id corresponding to
  byte-fallback control character
- **Pre-12-closure hypothesis space**: temperature recovery (BG-BR
  PASS_TEMP_RECOVERS at T=1.5) suggested the trained distribution was
  hidden in the high-T tail. BG-CE refutes the implicit reading that
  "greedy is just the failure mode and sampling recovers Korean": even
  uniform-random sampling over the full 64K vocab beats CLM greedy on
  Korean-character output for a Korean prompt. The substrate has lost
  the prior that random sampling implicitly carries via the 64K vocab
  composition (5701/64000 ≈ 8.9% pieces are Hangul, matching the 6.8%
  measured Korean-char rate of random vocab decode).

## Honest C3

- **C1** mac CPU fp32, single load — no GPU comparison
- **C2** 50 tokens — small sample, single seed=42 for random baselines
- **C3** `random_vocab` is uniform over all 64K pieces — ignores
  natural unigram frequency distribution; a true unigram baseline would
  weight by training-corpus frequency (no calibrated unigram counts on
  hand). However, uniform over 64K vocab is already a STRONG baseline
  for the question "is the substrate worse than chance?" because chance
  is a higher bar than zero.
- **C4** single prompt `"안녕"` — Korean prompt biases expected emit
  toward Korean; balanced multi-prompt cross-language sweep would
  harden the verdict
- **C5** "better/worse" = Korean character count delta — LEXICAL
  bookkeeping, NOT semantic content. CLM emit could in principle have
  high Korean count yet still be gibberish; conversely random
  Korean-only is 78% Hangul yet maximally meaningless. The verdict is
  about byte-distribution preservation, not chat capability.
- **C6** SentencePiece byte-fallback tokens (control chars, low-byte
  range) are part of the 64K vocab — random vocab will have non-zero
  control-char rate by construction. The fact that random_vocab
  measured **zero** control chars (seed=42, n=50) is luck-of-seed; the
  effect direction of the verdict is robust to this because CLM emits
  100% control chars.

## Deliverables

- `state/anima_emerge_chat_lexical_baseline_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_lexical_baseline_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_chat_lexical_baseline.py` (raw#37
  transient sister-rule helper, .own 3 — gitignored)
- `docs/anima_emerge_chat_lexical_baseline_landed_2026_05_05.ai.md`

## Cost / time

- $0 (mac CPU, no H100)
- wall ~1.1 min (load 21.2s + 50-token greedy emit 44.0s + baselines
  + verdict ~5s)

## Raw compliance

- raw#37 transient .py sister-rule (torch + sentencepiece inference;
  hexa cannot)
- raw#15 additive — does NOT modify mount.hexa, dialogue.bash,
  dialogue_load, hf_format_shim, conscious_decoder.py
- raw#10 honest C3 — 6 caveats emitted to verdict.json + doc
- .own 3 transient sister-rule, one-shot probe helper
- no commit (per task constraint)
- no secret leak
