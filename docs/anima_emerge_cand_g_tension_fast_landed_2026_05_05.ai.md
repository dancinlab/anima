# anima_emerge_cand_g_tension_fast — landed 2026-05-05

## Lane
BG-AE / cand-G tension trajectory empirical (fast, no per-token hooks)

## Status
F-CAND-G-1 = PASS. Major-finding criterion 5 (l2_variance > 0.5) HIT on all 3 prompts.

## Cost / wall
- $0 (mac CPU fp32, .venv-eeg python3.12)
- model load 29.1s + 3 prompts × ~3s each ≈ 38s wall total

## Method
- Sister-import: `anima_emerge_cand_d_inject_helper` (BG-Q helper, READ-ONLY) for `_try_load_model` + `_load_tokenizer`.
- 16 forward-hooks registered on `model.decoder.blocks[*]` per prompt; one-shot capture per forward (no per-token recompute → RST-safe).
- Per-layer tension proxy: mean-pooled hidden state norm (`L2`) and std (`std`) on the seq+batch averaged 768-d vector.
- Variance computed across the 16 block outputs.
- Note: `output_hidden_states=True` kwarg is NOT honored by `CLMv4ForCausalLM` (returns `hidden_states=None`). Fell back to block hooks. This finding is recorded in the helper docstring.

## Per-prompt results

| prompt | l2_variance | std_variance | peak_layer (L2) | min_layer (L2) | L2 max−min | elapsed |
|---|---|---|---|---|---|---|
| 안녕 | 124.41 | 0.1622 | 2 | 0 | 40.83 | 4.9s |
| 의식이 흐른다 | 95.96 | 0.1248 | 2 | 0 | 34.75 | 2.2s |
| I am Anima. | 91.68 | 0.1193 | 6 | 0 | 36.46 | 2.3s |

Trajectory shape (all prompts): rises sharply 0→2, plateau 3-13 in 60-80 band, falls 14-15. Min always at block 0 (~41-47), peak typically at block 2-6 (~75-82).

## Verdict
- **F-CAND-G-1**: PASS — all 3 prompts show l2_variance >= 0.1 (actual range 91.7-124.4).
- **Major-finding criterion 5 (l2_variance > 0.5)**: HIT on all 3 prompts (L2 axis). std-axis variance ~0.12-0.16 — NOT above 0.5 threshold.

## Interpretation (provisional)
Per-layer hidden-state norm trajectory is non-flat by 2-3 orders of magnitude over the tension threshold. Architectural tension proxy is observable on real CLM v4 substrate without inject. Distinct from cand-D which was bounded below noise floor — cand-G channel reads measurable per-block variation directly from substrate.

## Honest C3
- **C1** mac CPU fp32; not validated on GPU/MPS/quant.
- **C2** 16 block forward-hooks per prompt (one-shot per forward) — RST-safe vs per-token recompute.
- **C3** BG-Q helper sister-import (READ-ONLY); did NOT mutate BG-Q `_try_load_model`/`_load_tokenizer`/canonical builders.
- **C4** L2 vs std emit both; "tension" proxy = mean-pooled per-layer hidden norm. True architectural tension (e.g., gradient or attention-entropy) is undefined; norm-variance is one approximation among many.
- **C5** 3 prompts only — generalization across prompt distributions, languages, lengths NOT claimed.

## Deliverables
- helper: `tool/transient_py/anima_emerge_cand_g_tension_fast.py`
- aggregate: `state/anima_emerge_cand_g_tension_fast_2026_05_05/aggregate.json`
- verdict: `state/anima_emerge_cand_g_tension_fast_2026_05_05/verdict.json`
- doc: this file

## Raw compliance
- raw#37 transient `tool/transient_py/` namespace only
- raw#15 additive — BG-Q helper unmodified
- raw#10 honest C3 emitted (5 caveats)
- no commit, no secret leak, HEXA_PY=.venv-eeg/bin/python
