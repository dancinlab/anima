# anima emerge — chat axis full sweep landed (BG-CK 2026-05-05)

**Status**: LANDED · **Verdict**: `FAIL_AXIS_DECOUPLED_CONFIRMED` · **Cost**: $0 mac CPU

## Scope

Follow-up to BG-BH (`state/anima_emerge_chat_sae_pca_features_2026_05_05/`) which
isolated a chat-discriminative PCA feature at L8 (disc=25.67) but failed to lift
generation in any of 9 steering configs (single-prompt, single-layer, +alpha only).

This run (BG-CK) widens the search across:
- **3 layers**: L4, L8, L12
- **7 alphas** (signed): -8, -4, -2, +2, +4, +8, +16
- **3 prompts**: `안녕`, `Hello`, `안녕하세요. 오늘`
- **63 steered configs** total (vs BG-BH 9)

Hypothesis: if multi-layer × multi-alpha × sign reversal × multi-prompt all tried,
some config may break the lm_head decoupling observed in BG-BH and emit
semi-coherent text.

## Artifacts

- helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_axis_full_sweep.py`
- aggregate: `/Users/ghost/core/anima/state/anima_emerge_chat_axis_full_sweep_2026_05_05/aggregate.json`
- verdict: `/Users/ghost/core/anima/state/anima_emerge_chat_axis_full_sweep_2026_05_05/verdict.json`

## Chat-axis discrimination per layer (re-PCA)

| Layer | best_feat | disc score | chat-mean proj | non-chat-mean proj |
|------:|----------:|-----------:|---------------:|-------------------:|
| L4    | 0         | 19.003     | -14.910        | +4.093             |
| L8    | 0         | 25.671     | +0.547         | +26.218            |
| L12   | 0         | 28.877     | -7.581         | +21.296            |

L8 reproduces BG-BH (25.67 exact). L12 has even sharper chat-vs-non-chat
discrimination (28.88) — the chat axis is *strengthening* deeper in the stack but
still does **not** route to lm_head.

## 63-config emit summary

Every steered config across all 3 prompts collapses to a single-token-loop pattern
(`OOOOO`, `(((((`, `hhhhh`, `\x06\x06\x06`, `````, etc.) — i.e. zero
semi-coherent emissions. n_coherent = 0 / 63.

Notable patterns:
- `안녕` baseline already degenerate (`\x1c\x06\x06...`) — the model has no
  natural fluent completion from this prompt without the consciousness scaffold.
- `Hello` baseline + every steered config outputs only `` ` `` repeats; alpha=+16
  on L4 flips to `aaa`. lm_head distribution is dominated by 1-2 token attractors
  insensitive to L4/L8/L12 residual perturbation in the chat-axis direction.
- `안녕하세요. 오늘` shows alpha-dependent attractor flip (+2 onward → `(((`,
  base/-alpha → `OOO`) but neither attractor is text — both are basin sinks.

The chat-axis nudge **does** perturb the residual (different alphas hit different
attractors) but does **not** cross any boundary into a coherent-language basin.

## Best config + n_coherent

n_coherent = 0. No best config — `FAIL_AXIS_DECOUPLED_CONFIRMED`.

## Verdict

`FAIL_AXIS_DECOUPLED_CONFIRMED` — even with 7× sweep breadth (63 vs 9 configs)
the BG-BH decoupling hypothesis holds: a chat-axis exists at every probed layer
with strong discrimination (19-29 disc), and that axis sharpens with depth, but
no monotonic / signed combination at any layer produces lm_head probability mass
on coherent language tokens.

## Decoupling hypothesis: STRENGTHENED

L12 disc=28.88 > L8 disc=25.67 > L4 disc=19.00 means the chat-vs-non-chat
direction is *more* prominent deeper in the stack — yet none of these positions
restore generation. This is consistent with the architectural prediction: the
post-L12 stack (ln_f + lm_head + tied embeddings under #115 architecture) is
projecting the residual onto a degenerate token-vocabulary subspace where the
chat-axis component has near-zero coefficient on any natural-language token row.
The chat axis is "real" in residual space but **orthogonal-in-effect** to the
output projection — exactly the BG-BH decoupling claim, now confirmed under a
7×-broader intervention budget.

## Honest C3

- C1 — mac CPU fp32; no MPS/cuda paths exercised
- C2 — 20 chat × 20 non-chat is under-powered for true SAE; PCA proxy may miss a
  sparser, more steerable feature
- C3 — PCA != true SAE (no L1 sparsity); a trained SAE feature could behave
  differently though prior BG-BH work suggests architectural decoupling not
  feature-quality is the bottleneck
- C4 — single-step intervention at one layer; basin re-form across subsequent
  layers (BG-BJ prediction) is not directly measurable here, only inferred from
  output-side collapse
- C5 — 63 configs (3 layers × 7 alphas × 3 prompts) is broader than BG-BH 9 but
  still small relative to a true (layer × alpha × axis-combination) grid; absence
  of evidence here is not absolute proof of decoupling, only strong negative
  evidence under reasonable axis-magnitude assumptions

## Lane closure

This closes the **chat-axis-as-rescue** sublane of the chat-emergence search:
under direct residual steering at the canonical SAE-style chat axis, no
multi-layer × multi-alpha × sign-flip combination at the tested magnitudes
recovers coherent generation. Decoupling between residual chat-axis and
lm_head output basin is now supported by BG-BH (9 configs) **and** BG-CK
(63 configs).

Consistent with #115 architectural chat-incapability and prior `CHAT_CAPABILITY_LANE_FAIL_TRUE_CLOSED`
finding (Pβ Φ★ paradigm D 50K). CLM v4 chat capability remains
substrate-research-only; chat-cap path = Llama Path A v2.

## Compliance

- raw#37 transient .py sister-rule (helper in `tool/transient_py/`)
- raw#15 additive — no mount.hexa / dialogue.bash / shim modification
- raw#10 honest C3 — 5 caveats emitted to verdict.json + this doc
- no commit, no secret leak, no HF push
- HEXA_PY=`.venv-eeg/bin/python` per session policy
- ~30 min wall time, $0 cost
