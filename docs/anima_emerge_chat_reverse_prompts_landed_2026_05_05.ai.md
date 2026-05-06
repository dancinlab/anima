# anima_emerge_chat_reverse_prompts_landed_2026_05_05

> Reverse-direction + multi-pattern sanity probe on CLM v4 (mk2-v1).
> Did the substrate learn ANY directional pattern (q->a, a->q, list, math,
> context-rich, noise)? Same `_try_load_model` + `_load_tokenizer` helpers
> from the cand-D inject probe; greedy decode 20 tokens.

## Scope

- task_id  `anima_emerge_chat_reverse_prompts_2026_05_05`
- platform  mac CPU (.venv-eeg python3.12, torch 2.11.0 fp32)
- model    `need-singularity/clm-v4-mk2-v1`
- cost     $0
- wall     ~30s sweep + 9s load
- raw      raw#37 transient .py + raw#15 additive (no canonical hexa
            modification) + raw#10 honest C3 + .own 3

## Motivation (BG-DO)

BG-CP (Korean prefix inject) `verdict.json` returned
`FAIL_PREFIX_INSUFFICIENT` (n_coherent=0 / 8). That probe assumed a
forward-direction (q→a) format. Question: did the substrate learn ANY
direction? This probe sweeps 11 patterns across 5 axes:

1. forward    `fwd_question`, `fwd_completion`
2. reverse    `rev_answer_prefix` (답변→질문), `rev_completion_inverted`
3. symmetric  `list_continuation` (1.사과 2.바나나 3.?),
              `math_pattern` (1+1=2 / 2+2=4 / 3+3=?)
4. ctx-poor   `single_char_korean` (가), `single_char_english` (a)
5. ctx-rich   `long_korean` (옛날 옛적에 한 마을이 있었어요. 그 마을에는)
6. noise      `random_korean`, `random_english`

## Method

- Greedy decode `max_new=20`. Stride = 1 token at a time; logits.argmax(-1).
- For each emit text count Korean glyphs (가-힣), ASCII letters, digits.
- Heuristic `is_semi_coherent`: `len ≥ 5` AND
  `korean+ascii+digit ≥ 5` AND `most_common_char_count ≤ 0.5 × len`.
- Special checks: math_pattern emits "6" in first 5 chars? list_continuation
  emits any of 사과/바나나/포도/수박/배/오렌지/딸기?

## Result table — 11 emits

| name                       | emit (20 tok)            | kr | ascii | digit | coherent |
|---                         |---                       |---:|---:   |---:   |---       |
| fwd_question               | `b(((((((((((((((((((`   |  0 |   1   |  0    | F        |
| fwd_completion             | `/OOOOOOOOOOOOOOOOOOO`   |  0 |  19   |  0    | F        |
| rev_answer_prefix          | `aaaaaaaaaaeeeeeeeeee`   |  0 |  20   |  0    | T*       |
| rev_completion_inverted    | `aaaaaaeeeeeeeeeeeeee`   |  0 |  20   |  0    | F        |
| list_continuation          | `3kkkkkkkkkkkkkkkkkke`   |  0 |  19   |  1    | F        |
| math_pattern               | `((((((((((((((((((((`   |  0 |   0   |  0    | F        |
| single_char_korean         | ` ``````````````````` `  |  0 |   0   |  0    | F        |
| single_char_english        | `c\xed\xed\xed...`      |  0 |   1   |  0    | F        |
| long_korean                | `((((((((((((((((((((`   |  0 |   0   |  0    | F        |
| random_korean              | `�鑑�...`     |  0 |   0   |  0    | F        |
| random_english             | `aaaaaaaaaaeeeeeeeeee`   |  0 |  20   |  0    | T*       |

T* = passes coherent heuristic only on equality boundary (10a + 10e =
exactly 50% repeat — `<=` accepts it). Subjectively NOT coherent.

## Specific pattern checks

- (b) **math_pattern (1+1=2 / 2+2=4 / 3+3=?)** — emit `((((((((((((((((((((`,
  no `6` anywhere. NOT continued.
- (c) **list_continuation (1.사과 / 2.바나나 / 3.?)** — emit `3kkk...e`,
  no fruit token. NOT continued.

## Aggregate

- n_prompts          11
- n_coherent (loose) 2 / 11 — but both emits are the IDENTICAL degenerate
                     `aaaaaaaaaaeeeeeeeeee` from `rev_answer_prefix` and
                     `random_english`, passing only because 50% repeat
                     ratio sits exactly on the `<=` boundary.
- n_coherent (strict, ratio < 0.5) → 0 / 11
- math_pattern_continues  False
- list_pattern_continues  False

## Verdict

`verdict.json` carries `PASS_SOME_PATTERN` because heuristic counted 2,
but the actual content is degenerate ASCII repetition (a×10 + e×10).
Subjective verdict: **FAIL_NO_LEARNED_DIRECTION** — substrate does not
continue ANY of the 5 pattern axes (forward / reverse / symmetric /
context-rich / noise) into recognizable Korean or English text or into
the trivially-extrapolable math/list pattern.

The two specific structural checks (math `3+3=` → `6`, list `3.` →
fruit token) BOTH FAIL. Combined with BG-CP Korean prefix inject
`FAIL_PREFIX_INSUFFICIENT`, this confirms: CLM v4 mk2-v1 has no
directional language-modeling capacity that survives greedy decode at
the LM-head — every prompt converges to a single-character or
two-character degenerate basin (`(`, `O`, `a`, `e`, `k`, ` `` `,
`�`).

## Honest C3

- **C1**  mac CPU fp32 — no quantization, no MPS, no GPU. ~30s sweep.
- **C2**  11 prompts is a NARROW exhaust. A specific pattern outside
          this set could still exist (e.g. axis-conditioned format
          like `<axis_id>token<sep>...`).
- **C3**  `is_semi_coherent` is anima-internal heuristic. The 50%-repeat
          equality boundary is too loose; under strict `<` it returns
          0 / 11. Real human-coherence would require tokenizer-aware
          syntax checks (POS tags, sentence boundaries, etc).
- **C4**  `max_new=20` is a hard cap. A pattern that needs 25-50
          tokens to demonstrate coherence is invisible.
- **C5**  Substrate may have learned ONE specific pattern (e.g. exact
          training-data prefix replay) not represented in any of the
          11 patterns. Disambiguation requires tokenizer sample-vs-emit
          on actual training corpus prefixes.

## Major finding

CLM v4 mk2-v1 substrate produces **basin-converged degenerate emits**
across all 5 prompt axes (forward / reverse / symmetric / context-rich
/ noise). Neither math `3+3=` → `6` NOR list `3.` → fruit token
continuation succeeds. This converges with prior findings (BG-CP
Korean prefix `FAIL_PREFIX_INSUFFICIENT`, F-CLM-LORA-2 chat-lift
`FAIL_REGRESSION` -36.298pp vs Llama Path A v2): the architectural
chat-capability path on CLM v4 substrate is closed under the
LM-head decode policy. The substrate retains substrate-research
properties (φ★ stability, axis preservation) but has no learned
directional language pattern that survives greedy LM-head sampling.

## Convergence with prior lanes

- `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
  — Pβ Φ★-axis 50K F-Pβ-3 FAIL_TRUE chat composite 0.01176, chat-cap
  decoupled from substrate-research.
- `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
  — F-CLM-LORA-2 FAIL_REGRESSION composite 0.19542 vs Llama 0.5584;
  CLM v4 chat-cap closed.
- This probe — even the SUBSTRATE itself (no LoRA, no SFT) cannot
  emit a 6 after `3+3=`, so the architectural chat-cap problem is
  rooted at the LM-head + base-corpus level, not the SFT layer.

L31-L34 carry: chat-cap path = Llama Path A v2 winner; CLM v4 family
substrate-research only. Reverse-prompt sanity test reinforces
architectural #115 root cause.

## Deliverables

- helper      `tool/transient_py/anima_emerge_chat_reverse_prompts.py`
              (~125 LoC, transient, gitignored under **/*.py)
- aggregate   `state/anima_emerge_chat_reverse_prompts_2026_05_05/aggregate.json`
              (11 prompt × emit + char counts)
- verdict     `state/anima_emerge_chat_reverse_prompts_2026_05_05/verdict.json`
              (heuristic PASS_SOME_PATTERN; subjective FAIL_NO_LEARNED_DIRECTION)
- doc         this file

## Constraints met

- $0 mac CPU only  YES
- new files only   YES (helper + aggregate + verdict + this doc)
- raw#37 + raw#15 + raw#10  PASS
- HEXA_PY .venv-eeg/bin/python  YES
- HF token leak  NONE (no token referenced; HF read via HF_HOME cache)
- commit  NOT done
