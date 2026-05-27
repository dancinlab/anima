# anima_emerge_chat_english_sweep — English prompt sweep (BG-CB landed 2026-05-05)

<!-- @no-lineage-citation-exempt-file -->

## Scope

Extend BG-AQ (T=0.8, 6 decode strategies, KO `안녕`) and BG-BR (KO `안녕`,
9 temperatures times top-k=100) to **English prompts** across 8 length / format
classes. Hypothesis under test:

> If substrate trained on English but not (or weakly on) Korean, English long
> prompts may emit coherent text — Korean-only failure would localize as
> language-coverage gap, NOT architectural #115.

`PASS_ENGLISH_WORKS` would imply: BG-AQ/BR/BP are KO-coverage artifacts.
`FAIL_ENGLISH_ALSO` would imply: chat-cap failure is language-agnostic,
strengthening architectural #115 framing.

## Setup

- Substrate: `dancinlab/clm-v4-mk2-v1` (CLM v4 fp32, mac CPU)
- Tokenizer: `tokenizer_64k_multilingual.model` (SentencePiece, 64k multilingual)
- Decoder: `greedy` (argmax) + `top-k=40, T=0.8, max_new=30, seed=42`
- raw37 transient sister-import on `anima_emerge_cand_d_inject_helper.py`
  (reuses `_try_load_model` + `_load_tokenizer`)
- 8 prompts times 2 decoders = **16 emits**
- load_sec = 15.1s, total wall ~ 2.4 min

## Prompt classes

| Name | Prompt | n_tokens |
|---|---|---|
| short | `Hello` | 2 |
| medium | `Hello world. How are you today?` | 9 |
| long | quick-brown-fox + weather (45 tok) | 45 |
| instruction | `Q: What is consciousness?\nA:` | 8 |
| few_shot | 3-shot QA chain to `Hello, how are you?` | 36 |
| chat_format | `User: Hello\nAssistant:` | 7 |
| story | `Once upon a time there was a kingdom where` | 13 |
| wiki | `The phenomenon known as consciousness has been studied for` | 14 |

## Results — 16 emits

| Prompt | greedy | top-k=40 T=0.8 |
|---|---|---|
| short       | backtick times 30 | backtick + e times 12 + ASCII `dhhhhh...` |
| medium      | `b((((((((((` (29x) | `b/jjjdhhhh...` |
| long        | `b((((((((((` (29x) | `b/OOOPP^hPPg...` |
| instruction | `aaaaaaa eeeeeee` (split) | `aaaaaccccc` + control bytes (10x) |
| few_shot    | `a` x 30 (pure) | `a` x 30 (pure) |
| chat_format | `aaaaaeeeeee` | `aaaaaccccc` + multi-byte salad |
| story       | `/OOOOOOOOOOOOOOOOOO` | `/OOOOPPgPgPPgg...` |
| wiki        | `/OOOOOOOOOOOOOOOOOO` | `/OOOOPPgPPgPPgPP...` |

**No prompt produced 3+ ASCII alpha-word tokens.** Every emit is single-character
ASCII repetition (`a`, `(`, `O`, `e`, `g`, `h`, `P`, `b`, backtick) or control-byte
salad — same character-class collapse pattern observed in BG-AQ/BR Korean sweeps.

## Coherence verdict

- `n_coherent` = **0 / 16** (heuristic: 3+ ASCII alpha-words length 2+, no
  single-char dominating more than 50% of text)
- `best` = **null** (no coherent emit at any prompt times decoder)
- Schema verdict: **FAIL_ENGLISH_ALSO**

## Pattern analysis

The substrate exhibits **prompt-conditioned ASCII attractors** instead of
random byte salad:

- "Hello" prompts to backtick and `b` attractors
- Question/A prompts to `a` and `e` attractors
- Story / "The X" prompts to `/` and `O`/`P`/`g` attractors
- chat_format to `a` (matches "Q:" attractor — chat_format unrecognised as instruction)

This is **structurally identical** to the Korean BG-BR collapse pattern (control
byte salad + character-class repetition). The prompt-conditioning suggests the
model is responding to input structure (different prompts to different attractors)
but the manifold it lands on is **single-token-class repetition**, not natural
language continuation.

## Conclusion

`FAIL_ENGLISH_ALSO`. The substrate emits no coherent English at any of 8 prompt
classes times 2 decode strategies. The character-class collapse pattern matches the
Korean BG-AQ/BR/BP failure mode exactly:

- BG-AQ KO `안녕` T=0.8: 0/6 coherent, control-byte attractor
- BG-BR KO `안녕` T-sweep 9-temp: 0/12 *real* coherent (heuristic-PASS only)
- **BG-CB EN 8-prompt times 2-decode: 0/16 coherent, ASCII single-char attractors**

The Korean-only-failure hypothesis is **falsified**. Chat-cap failure is
**language-agnostic** under both KO and EN — and across 30+ decoder configurations
when BG-AQ/BR/CB are aggregated.

### #115 implication

This **strengthens the architectural #115 framing**:

1. CLM v4 LoRA SFT regression (-36.298pp vs Llama Path A v2) is not a KO-tokenization
   artifact — substrate fails to emit coherent EN as well.
2. Pbeta Phi-axis chat-cap FAIL_TRUE (composite 0.01176, dot/quote/fragment gens)
   is consistent with this substrate-level character-class collapse.
3. The Llama Path A v2 winner (composite 0.5584) clearly demonstrates that
   **architectural** chat capability requires substrate-level coherent-emit
   infrastructure that CLM v4 lacks across languages.
4. CLM v4 substrate may be sufficient for axis / phi research (Pbeta Phi 42.37 PASS,
   F1/3/4-Part-A/5 PASS) but **NOT for chat-cap** — substrate-research vs
   chat-capability lanes remain decoupled per L28-L33.

## Honest C3

1. **C1** mac CPU fp32 — no GPU; greedy + top-k=40 T=0.8 only, no beam / nucleus /
   contrastive / DoLa / repetition-penalty.
2. **C2** `english_semi_coherent` heuristic = 3+ ASCII alpha-word tokens (length 2+,
   alpha + light punct) + max-char-count under 50% of text — narrow definition; a
   broader linguistic check (e.g. n-gram LM perplexity, BPE consistency, dictionary
   word ratio) might shift the verdict — but qualitatively the emits are clearly
   degenerate at human inspection.
3. **C3** 8 prompt classes only; broader corpus (technical, conversational,
   code, news, dialogue, multi-turn) may shift coherence rate. Most likely small
   shift given the depth of single-token-class collapse observed.
4. **C4** single seed (42) for top-k; multi-seed sweep at the same T=0.8 might
   reveal stochastic emit-windows — but BG-BR T=1.5 multi-seed showed identical
   character-class collapse across seeds {7, 100, 1000}, so this is unlikely.
5. **C5** **PASS** would have signaled substrate `English haksub + Korean an haksub`
   (BG-CA hypothesis verified); **FAIL_ENGLISH_ALSO** strengthens
   "substrate broken across languages" architectural-failure framing — but it
   does NOT *prove* architectural failure (decoder-only chat-tuning may still
   recover, as Llama Path A v2 demonstrates separately). The robust claim is:
   **CLM v4 substrate alone is non-conversational across KO + EN under standard
   decoders**, not "any substrate from this family is non-conversational".

## Deliverables

- `state/anima_emerge_chat_english_sweep_2026_05_05/aggregate.json` — 8-prompt times 2-decoder
  emit table with timing
- `state/anima_emerge_chat_english_sweep_2026_05_05/verdict.json` — schema
  `anima/emerge_chat_english_sweep/verdict/1`, FAIL_ENGLISH_ALSO
- `tool/transient_py/anima_emerge_chat_english_sweep.py` — raw37 transient
  sister helper

## Cross-references

- BG-AQ KO 6-decoder: `state/anima_emerge_chat_decoder_strategy_2026_05_05/`
- BG-BR KO 9-temp:    `state/anima_emerge_chat_temp_extreme_2026_05_05/`
- BG-BP KO multi-seed: (BG-BP referenced in #115 chat-cap chain)
- Pbeta Phi-axis FAIL_TRUE: feedback memory `pbeta_chat_capability_fail_substrate_research_pass_decoupled`
- CLM v4 LoRA chat-lift FALSIFIED: feedback memory `clm_v4_lora_sft_chat_lift_falsified_substrate_safe`

## Cost + wall-time

- Cost: $0 (mac CPU)
- Wall: ~2.4 minutes (load 15.1s + 16 emits times ~6.5s avg)
- raw37 transient `tool/transient_py/` namespace, .own 3 sister-rule
- raw15 additive (no mount.hexa / dialogue.bash / dialogue_load mod)
- raw10 honest C3 (5 caveats above)
- No commit, no secret leak

## Lane closure

Lane: **CHAT_EMIT_LANGUAGE_AGNOSTIC_FAIL_CLOSED**

Korean-only-failure hypothesis falsified. CLM v4 substrate exhibits
character-class collapse across KO + EN under 30+ decoder configurations.
Architectural #115 framing strengthened. Chat-cap path remains:
**Llama Path A v2 winner (only)**; CLM v4 = substrate-research only per L31-L33.
