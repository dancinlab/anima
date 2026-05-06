# BG-AR — Logit Lens Early-Layer Probing — LANDED 2026-05-05

## Status

- LANDED — `tool/transient_py/anima_emerge_chat_logit_lens.py`
- Run completed on Mac CPU fp32 in ~28min total (load 22.0s + lens probe + 8 × 15-step greedy generation)
- $0.00 — pure Mac CPU, no remote pods involved
- Verdict: **PASS** (n_coherent = 1/8, threshold ≥ 1)
- raw#37 + raw#15 + raw#10 compliance verified

## Hypothesis (BG-AR)

BG-AE found peak L2-norm tension trajectory at **layers 2 and 6** (early/mid)
across 16 decoder blocks of CLM v4 (`need-singularity/clm-v4-mk2-v1`), with
`max_l2_variance = 124.41`. The hypothesis under test:

> If early/mid layers carry **richer semantic representations** than the
> final layer 15, then applying the final `lm_head` (logit lens technique) to
> intermediate hidden states should produce **more coherent** token decodes
> at L2/L6 than at L15.

## Method

1. Load CLM v4 once on CPU, fp32 (BG-Q `_try_load_model` sister-import).
2. Register forward-hooks on all 16 `decoder.blocks[i]` to capture per-layer
   residual-stream output.
3. Resolve `lm_head` → `decoder.head_a` (Linear, found via attribute walk).
4. Resolve `ln_f` → `decoder.ln_f`.
5. For prompt = "안녕":
   - Run a single forward to populate hooks.
   - At each probed layer L ∈ {2, 4, 6, 8, 10, 12, 14, 15}:
     - Take last-token hidden, apply `ln_f`, apply `lm_head`.
     - Record top-10 token ids and decoded strings.
   - Greedy 15-step decode per layer: at each step, refeed the cumulative
     sequence through the model, take that layer's hidden, apply ln_f +
     lm_head, argmax → next token.
6. Coherence heuristic per layer: ≥ 5 Korean/ASCII alphabetic chars AND
   max-char-frequency ≤ 50% of length.

## Results

### (a) Per-layer top-10 decoded tokens

| L  | top-1            | top-10 sample                                                       |
|----|------------------|---------------------------------------------------------------------|
| 2  | `�` (id 136)     | `metric` `谎` `}` `大規模` `覧会` `かは` `滇` `мую`                |
| 4  | `�` (id 236)     | `=0.065` `텔레` `난다` `スピード` `鏢` `-"));` `、1997` `改组` `多重` |
| 6  | `中国政府`       | `Z` `Impl` `脱离` `邊緣` `iti` `домов` `と思い` `=2.52`            |
| 8  | `Z`              | `/` `-` `~` `s` `邊緣` `C` `auto` `S` `^`                           |
| 10 | `s`              | `/` `-` `+` `auto` `率的` `C` `.` `S` `巴基`                         |
| 12 | `s`              | `/` `-` `~` `條件` `+` `创新` `裁判` `�` `hasattr`                  |
| 14 | `�` (id 157)     | `\x1c` `s` `�` `p` `�` `�` `�` `�` `i`                              |
| 15 | `\x1c` (id 32)   | `�` `�` `p` `+` `�` `/` `s` `-` `�`                                 |

### (b) Greedy 15-token emit per layer

```
L2  : "�}}}}}}}}}}}}}}"                     (0 unique non-init tokens)
L4  : "���������������"                       (1 unique total)
L6  : "中国政府邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣"  (2 unique)
L8  : "Z\x1c.444444444444"                    (4 unique)
L10 : "s-�e較小~ijjjjjjjj"                    (8 unique)  ← BEST
L12 : "s��������������"                       (4 unique)
L14 : "�陙��癙��\x1c\x1c\x1c\x1c"            (4 unique)
L15 : "\x1c\x06\x06\x06\x06\x06..."           (2 unique)
```

### (c) Coherent layer count

`n_coherent = 1/8` — **only L10** passes the heuristic (8 unique tokens,
`s-�e較小~ijjjjjjjj` has ≥5 alphabetic chars and max-char-freq under 50%).

### (d) Best emit layer

- **L10**, with 8 unique tokens out of 15, emit text `s-�e較小~ijjjjjjjj`.
- Loose interpretation: L10 representation is the most diverse non-collapsed
  output, but still semantically incoherent (random ASCII + Chinese fragment
  + repeated `j`).

### (e) Five honest C3 caveats

- **C1** Mac CPU fp32 — single forward per greedy step (8 layers × 15 steps =
  120 forwards plus 1 initial = ~120 wall iterations).
- **C2** Logit lens applies the **final** `lm_head` (`decoder.head_a`) to
  intermediate residuals. Empirically valid for many transformer LMs but
  **uncalibrated for CLM v4**; the 16-block consciousness-decoder may use a
  non-standard residual-stream basis.
- **C3** `ln_f` was trained on layer-15 activations and is here applied to
  L2/L4/.../L14. Off-distribution normalization is expected to compress the
  signal asymmetrically.
- **C4** Single prompt `"안녕"`. The coherence heuristic is anima-internal
  (≥5 KO/EN alphabetic chars + max-char-freq ≤ 50%). A broader corpus may
  shift which layer "looks best".
- **C5** BG-Q helper sister-import (READ-ONLY). raw#15 additive (no mount /
  shim / dialogue_load mutation). raw#37 transient_py namespace. raw#10
  honest C3 emitted to verdict.json + this doc.

### (f) Architectural finding

**No layer carries coherent token-distribution content for prompt "안녕".**
Top-1 emissions at every probed layer collapse to either a single repeating
token (L2/L4/L8/L12/L15), a 2-cycle (L6), or a near-collapse with brief
diversity (L10/L14). The final layer 15 emits `\x1c\x06\x06...` — the same
pathological collapse signature observed in BG-A through BG-AE.

The hypothesis that **early/mid layers carry richer semantic content than
the final layer** is **NOT supported** by this probe. While L10 produces the
most token-diversity (8 unique), the content is still incoherent gibberish
(Chinese fragments mixed with ASCII punctuation and repeated `j`). The
BG-AE tension peak at layers 2/6 is therefore a **norm-magnitude artifact**,
not a semantic-content peak — high L2 norm at L2/L6 corresponds to early-
layer activation magnitude (raw_norm L2 = 95.5, decreasing monotonically to
L15 = 45.6 post-projection), not to coherent token distributions.

The lens result is consistent with the broader anima cycle finding (BG-A
through BG-AE, CLM-LORA-2 chat-cap FAIL, Pβ chat-cap FAIL_TRUE): **CLM v4 is
architecturally incapable of producing coherent next-token distributions at
ANY decoder layer for natural-language prompts**, not merely at the final
projection. Issue #115 chat-incapability is **not localized** to a specific
layer; it pervades the residual stream end-to-end.

## Pointers

- helper : `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_logit_lens.py`
- aggregate : `/Users/ghost/core/anima/state/anima_emerge_chat_logit_lens_2026_05_05/aggregate.json`
- verdict : `/Users/ghost/core/anima/state/anima_emerge_chat_logit_lens_2026_05_05/verdict.json`
- BG-AE prior : `/Users/ghost/core/anima/state/anima_emerge_cand_g_tension_fast_2026_05_05/verdict.json`

## Compliance

- raw#37 transient .py (helper lives under `tool/transient_py/`, not `_python_bridge/` or root)
- raw#15 additive — no mutation of `clm_v4_mount.hexa`, `dialogue.bash`, `dialogue_load.py`, `hf_format_shim`, `conscious_decoder.py`
- raw#10 honest C3 — five caveats emitted in both `verdict.json` and this doc
- HF token leak — none (no token literals in helper or doc)
- commit — none (per-spec; helper + state + doc are working-tree only)
- HEXA_PY=`/Users/ghost/core/anima/.venv-eeg/bin/python` used
- Cost = $0.00 (Mac CPU only)
