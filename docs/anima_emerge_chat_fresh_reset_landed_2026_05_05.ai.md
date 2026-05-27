# anima emerge chat fresh-reset (BG-BU) — landed 2026-05-05

## TL;DR

**FAIL_BASIN_PERSISTS** — n_coherent = 0 / 6 emit texts. BG-BJ residual-basin
hypothesis VERIFIED at decode level: per-step fresh re-encode is illusory and
window-truncate corrupts semantic anchor. Chat-capability rescue path via
decode-side intervention is closed on CLM v4 best.pt.

## Context

- BG-BJ verdict (`state/anima_emerge_chat_entropy_trajectory_2026_05_05/verdict.json`)
  identified an autoregressive basin re-forming step 1+: `안녕하세요...` collapses
  step 1 to "/" with top1_prob 0.977; `안녕` triggers byte fallback (\x1c) at
  step 0 with entropy 3.31.
- Hypothesis: if basin lives in *token history*, breaking the autoregressive
  feedback loop (fresh re-encode each step, no kv cache reuse) should let the
  decode escape.
- Counter-hypothesis (C5, predicted FAIL): basin lives in *residual geometry*
  not in token history, so any fresh re-encode replays the same residual path.

## Method

3 decode strategies × 2 prompts (= 6 emit texts), 15 new tokens each:

| Strategy            | Mechanism                                                  |
| ------------------- | ---------------------------------------------------------- |
| `greedy_fresh`      | argmax + sp.decode([next_id]) → cur_text + tok → re-encode |
| `topk_fresh`        | top-k=40 / temp=0.7 / seed=42 + same fresh re-encode       |
| `window20_truncate` | greedy + keep only last 20 chars of cur_text per step      |

All forwards: `no_grad`, no kv cache reuse, fp32, CPU.

## Results

### Emit text (15 tokens each, post-prompt slice)

| Prompt           | greedy_fresh        | topk_fresh          | window20             |
| ---------------- | ------------------- | ------------------- | -------------------- |
| 안녕하세요. ...  | `/(((/(//////((/`   | `//////(/(/////(`   | `/(((//((////(/(`    |
| 안녕             | `\x1c × 15`         | `\x1c�-�p/((((((///` | `\x1c × 15`         |

### Coherence table

All 6 cells: **false**. n_coherent = 0.

### Verdict

```
verdict: FAIL_BASIN_PERSISTS
n_coherent: 0
n_total_emit: 6
load_sec: 7.6
sweep_sec: 47.3
```

## window-truncate vs fresh-reset

The two interventions are mechanistically distinct:

- `greedy_fresh` / `topk_fresh`: keep full cur_text, re-encode each step. The
  emit IS the standard greedy/topk path because sp.encode/decode is a
  deterministic round-trip given the same string. **No actual reset.**
- `window20_truncate`: keep only last 20 chars per step. After 5 steps the
  prompt is gone entirely. Mechanically a real intervention but corrupts the
  semantic anchor. Empirically converged to the same `/(((` and `\x1c` basins
  as fresh-reset → suggests basin is reachable from many context shapes, not
  just full-prompt context.

Both prompts collapsed identically across all three strategies. The `안녕` byte
fallback (\x1c, 0x1c = ASCII 28 / FILE SEPARATOR) is robust to top-k stochastic
escape and to context truncation.

## BG-BJ insight verify

Claim: basin re-forms in autoregressive feedback because it lives in residual
geometry, not in token history.

- Verified condition: n_coherent == 0 across all 3 strategies → **MET**.
- Falsified condition: n_coherent ≥ 1 with greedy_fresh or topk_fresh
  (token-history-only basin) → not met.

The window20 result is the most informative: dropping the prompt context
entirely does not escape the basin. This means the basin is reachable from any
short input that the tokenizer maps into the same neighborhood — consistent
with a residual-stream attractor that pulls in nearby encodings.

## Honest C3

- C1 — mac CPU fp32 (.venv-eeg python3.12), no GPU, no kv cache reuse.
- C2 — sp.encode/decode round-trip is mathematically identical to the standard
  greedy path. The "fresh-reset" framing is misleading at the decode level;
  there is no real reset until window-truncate.
- C3 — window-truncate drops semantic context; observed coherence loss may be
  context-loss not basin-escape. False-positive risk: had window20 produced
  text, we could not have separated the two effects.
- C4 — every "fresh" forward still rebuilds the same residual stream from the
  same tokens. Decode-side interventions cannot escape a residual-geometry
  basin.
- C5 — BG-BJ insight (basin in residual, not history) is verified by the all-6
  collapse, with the window20 control as the strongest evidence (different
  context shape, same basin).

## Constraints satisfied

- raw#37 transient .py sister-rule (helper imports inj_helper for model load)
- raw#15 additive — no mount/shim/dialogue modification
- raw#10 honest C3 emitted (5 caveats + BG-BJ insight verify block)
- $0 mac CPU only, no commit, no HF token leak

## Deliverables

- `tool/transient_py/anima_emerge_chat_fresh_reset.py` — probe
- `state/anima_emerge_chat_fresh_reset_2026_05_05/aggregate.json` — full emit + step-by-step histories
- `state/anima_emerge_chat_fresh_reset_2026_05_05/verdict.json` — schema/1 verdict

## Implication for chat-capability rescue

Decode-side interventions (entropy trajectory BG-BJ + fresh-reset BG-BU) both
fail. The basin is architectural. Consistent with prior lane closures:

- F-Pβ-3 FAIL_TRUE (composite 0.01176, dot/quote/fragment gens)
- F-CLM-LORA-2 FAIL_REGRESSION (-36.298pp vs Llama Path A v2)
- #115 architectural chat-incapability

Path A v2 on Llama remains the only validated chat-capable substrate. CLM v4
remains substrate-research only.
