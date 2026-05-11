# Anima Emerge Chat — Korean Prefix Injection Continuation Gauge (LANDED 2026-05-05)

**Lane**: emerge / chat-capability / Korean continuation feasibility
**Status**: LANDED
**BG**: BG-CP (sister to BG-CA — Korean rank survey)
**Substrate**: `dancinlab/clm-v4-mk2-v1` (mac CPU fp32)
**Cost**: $0
**Runtime**: ~6 min wall (model load 9.5s + 8 variants × 2 decode × 25 tokens)
**Verdict file**: `state/anima_emerge_chat_korean_prefix_inject_2026_05_05/verdict.json`

---

## Question

Does the substrate produce natural Korean continuation when a Korean prompt
plus a Korean response prefix is prepended? Does prebaking a Korean response
template let the substrate "recognise that it is already in Korean mode" and
continue naturally?

The hypothesis under test is that prefix injection acts as a soft mode-switch:
Korean prefix in the input window biases the residual basin toward emitting
more Korean tokens. BG-CA already established Korean tokens are absent from
the top-100 logits on a single-token Korean prompt; BG-CP asks whether longer
Korean context can recover them.

---

## Method

- Load `dancinlab/clm-v4-mk2-v1` once on Mac CPU (fp32) via the BG-Q
  loader helper at `tool/transient_py/anima_emerge_cand_d_inject_helper.py`
  (reused via `importlib.util.spec_from_file_location`).
- 8 variants × 2 decode modes (greedy + top-40 / temp 0.8 / seed 42) = 16
  emit-strings of 25 new tokens each.
- "Coherent" = 5 or more Korean glyphs in `'가'..'힣'` AND no character occupies
  more than 50% of the emit (anti-repetition floor).
- Artefacts:
  - `state/anima_emerge_chat_korean_prefix_inject_2026_05_05/aggregate.json`
    (per-variant full emit + Korean glyph counts)
  - `state/anima_emerge_chat_korean_prefix_inject_2026_05_05/verdict.json`
  - `tool/transient_py/anima_emerge_chat_korean_prefix_inject.py`

### Variants

| name                         | full input                                                      |
|------------------------------|-----------------------------------------------------------------|
| no_inject                    | 안녕                                                            |
| comma_response               | 안녕,                                                           |
| korean_response_starter      | 안녕 반갑습니다                                                 |
| korean_full_sentence         | 안녕 반갑습니다. 저는 인공지능                                  |
| korean_long_prefix           | 안녕 반갑습니다. 저는 인공지능 어시스턴트입니다. 오늘 날씨가    |
| natural_korean_continuation  | 안녕하세요. 오늘 날씨가 정말 좋네요. 산책하기                   |
| korean_qa_format             | 질문: 안녕\n답변:                                              |
| korean_user_assistant        | 사용자: 안녕\n어시스턴트:                                      |

---

## Result — `FAIL_PREFIX_INSUFFICIENT`

- `n_coherent = 0/8` — zero variants reached the 5-Korean-glyph coherence
  floor in either greedy or top-k decode.
- `best = null` — no variant nominated.
- All 16 emit-strings have `korean_count = 0`.

### Behavioural pattern

Every variant degenerates into a tight repetition of one or two ASCII or
control codepoints (`\x06`, `\x1c`, `p`, `]`, `(`, `a`, `e`, `k`, `-`, `$`)
with sporadic Latin-1 fallback bytes. Greedy and top-k both collapse into the
same family of attractors regardless of prefix length (1 to 19 input tokens).

Most telling case studies:

- `natural_korean_continuation` — a fully formed Korean sentence with a verb
  phrase hanging mid-clause (`산책하기`) — emits `(((((((((((((((((((((((((`
  greedy and a near-identical `(`-attractor under top-k. The autoregressive
  expectation that Korean follows Korean does not survive the substrate's
  decode head.
- `korean_qa_format` and `korean_user_assistant` — instruct-style scaffolds —
  collapse to `aaaaaeeeee...`. The substrate does not recognise the dialogue
  template.
- `korean_long_prefix` (19 Korean input tokens) — collapses to `(`-attractor
  identical to the 15-token variant. Prefix length is irrelevant.

---

## Interpretation (vs BG-CA)

BG-CA (top-1000 rank survey on `안녕`) found Korean is **not** under-
represented in top-1000 in aggregate (`korean_in_top1000 = 86`, expected
uniform ~89), but is **completely absent from top-100** (`korean_in_top100 =
0`, best Korean rank = 197 / `▁수행`).

BG-CP confirms the consequence: even when the prompt plus prefix is entirely
Korean with up to 19 input tokens of Korean context, the residual basin at the
head still places **zero** Korean tokens at rank 0 (greedy) or in the top-40
(top-k temp 0.8). The Korean prefix does **not** shift the basin. Rephrased:
the substrate has no learned "Korean mode" attractor — Korean tokens sit in
the long tail uniformly regardless of context.

This falsifies the BG-CP hypothesis: prefix injection does **not** unlock
Korean continuation on this substrate. Korean-mode recognition is not a
routing problem solvable by prompt engineering.

---

## Honest C3 (5)

- **C1** — Mac CPU fp32 single-shot; no replication, no MPS or GPU dtype
  comparison.
- **C2** — Prefix injection adds context (input ids visible to attention) but
  does **not** alter the residual basin (consistent with BG-BU finding that
  residual injection requires architectural cross-attention pathway, not
  prompt prefix).
- **C3** — Coherence definition (5+ Korean glyphs and no >50% repeat) is
  narrow; a strict-fail of 0/8 is robust to threshold relaxation, but a strict
  pass would have demanded much more than 5 glyphs to be meaningful.
- **C4** — Prefix may lock substrate into a specific continuation through
  autoregressive bias; we observe the opposite — prefix length is irrelevant,
  attractor wins regardless.
- **C5** — "Natural Korean" emission is not equivalent to semantic
  understanding; even a PASS here would have measured surface-level glyph
  recurrence, not comprehension.

**Korean prefix and basin (separate observation)**: confirmed that Korean
prefix does not shift the residual basin. Korean tokens remain absent from the
top-100 logits even after 19 Korean input tokens. This rules out
"prompt-engineering away the English bias" as a cheap chat-capability path on
the `clm-v4-mk2-v1` substrate.

---

## Lane Implication

- **Closes** the "Korean prefix unlocks Korean continuation" hypothesis as
  `FAIL_PREFIX_INSUFFICIENT`.
- **Reinforces** the F1-anchor recalibration finding and the LoRA SFT
  chat-lift falsification: chat capability on `clm-v4-mk2-v1` is
  architecturally absent, not surface-level absent.
- Path A v2 (Llama-self) remains the only chat-capability winner; CLM v4
  family stays substrate-research only.

---

## Compliance

- Transient sister-rule helper at `tool/transient_py/anima_emerge_chat_
  korean_prefix_inject.py`, gitignored under the project-wide `**/*.py` rule.
- Additive only — no anima runtime modified; BG-Q loader helpers
  `_try_load_model` and `_load_tokenizer` reused via dynamic spec import.
- Honest caveat block embedded in `verdict.json` and this doc (5 caveats
  above).
- HEXA_PY = `.venv-eeg/bin/python`; no HF token in source; no commit
  performed.

---

## Cost / Wall

- $0.00 (Mac CPU only)
- ~6 minutes wall (load 9.5s + 8 × 2 decode × 25 tokens)
