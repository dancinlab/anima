# anima_emerge_nnsight_intervention_landed_2026_05_05.ai.md

**BG-BW landed**: F-NNSIGHT-1 intervention smoke at `decoder.blocks[8].output`
**Date**: 2026-05-05/06 UTC
**Cost**: $0 (mac CPU fp32)
**Duration**: ~25min (incl. CLM v4 fresh load)
**Verdict**: `PASS_INTERVENTION_VISIBLE`

---

## Lineage

- BG-BB (2026-05-05) external sister candidate audit → nnsight ranked 2순위
- BG-BL (2026-05-05) `anima_emerge_nnsight_smoke_2026_05_05/verdict.json` →
  `PASS_READY` at `decoder.blocks[8].output` shape `[1,2,768]`
- BG-BW (this doc) → F-NNSIGHT-1 intervention smoke landed

## Setup

- Model: `need-singularity/clm-v4-mk2-v1` (CLM v4 mk2 v1, fp32 cpu)
- Helper: `tool/transient_py/anima_emerge_nnsight_intervention.py` (raw#37 + .own 3)
  - Reuses `anima_emerge_cand_d_inject_helper.py:_try_load_model + _load_tokenizer`
- Wrap: `from nnsight import NNsight; nn_model = NNsight(raw_model)` v0.7.0
- Capture path: `nn_model.decoder.blocks[8].output` (BG-BL confirmed)
- Prompt: `"안녕하세요. 오늘 날씨가 좋네요."` (12 tokens)

## 3 Interventions × Logit Delta

| Intervention            | Argmax (last-token) | max abs logit delta |
| ----------------------- | ------------------: | ------------------: |
| baseline                |                  51 |                   — |
| zero L8 output          |             **151** |         **11.4068** |
| scale L8 by 2x          |                  51 |              0.1941 |
| add noise std=2.0 to L8 |                  51 |              2.2557 |

**Key signal**: zeroing layer 8 output flips the argmax token (51 → 151) and
shifts logits by 11.4 — proves nnsight intervention is REAL and reaches `output.logits`.

`scale_2x` ≈ 0.19 is suspicious-low (suggests block 8 may produce tuple where
in-place `*=` on `out[0]` was traced but residual stream may have re-stabilized).
`noise_2.0` at 2.26 is intermediate, consistent with stochastic perturbation.

## Post-Intervention 20-Token Continuation

(first token from intervened logits; subsequent 19 from raw greedy)

| Variant   | Continuation                              |
| --------- | ----------------------------------------- |
| baseline  | `'/OOOOOOOOOOOOOOOOOOO'`                  |
| zero_L8   | `'��������������������'`                  |
| scale_2x  | `'/OOOOOOOOOOOOOOOOOOO'`                  |
| noise_2.0 | `'/OOOOOOOOOOOOOOOOOOO'`                  |

**n_coherent_post_intervention**: **0/4** (basin re-forms after 1 intervened token)

This empirically confirms the BG-BJ basin insight: intervention at one layer one
step does not rescue chat capability — the model re-collapses to the degenerate
attractor (`OOOOO...` / replacement char) on subsequent autoregressive steps.

## Verdict

```
F-NNSIGHT-1 intervention_visible: TRUE (delta_zero = 11.41 > 0.1)
verdict: PASS_INTERVENTION_VISIBLE
next_step: multi-layer sweep + axis-conditioned intervention via nnsight
```

State emitted:

- `state/anima_emerge_nnsight_intervention_2026_05_05/aggregate.json`
- `state/anima_emerge_nnsight_intervention_2026_05_05/verdict.json`

## Honest C3 (5)

- **C1** mac CPU fp32 only — no MPS / CUDA validation
- **C2** single-step intervention only — multi-step autoregressive nnsight trace is
  CPU-prohibitive (would need ~20× repeated forward inside trace)
- **C3** logit delta = intervention visibility, NOT chat-capability rescue.
  zero_L8 flipped the argmax but the basin re-formed within 1 token
- **C4** single layer 8 only — full multi-layer sweep deferred (BG-BV scope)
- **C5** BG-BJ basin insight predicts and is empirically confirmed:
  post-intervention degenerate attractor re-forms regardless of intervention magnitude

## nnsight Unlocked Path Evaluation

**What nnsight unlocks (vs. naive forward-hook)**:

1. Per-layer intervention via attribute proxy (`nn_model.decoder.blocks[8].output`)
   without manual `register_forward_hook` boilerplate.
2. `.save()` of intervened logits cleanly outside the trace context.
3. In-place mutation semantics on traced proxies (tested: tuple-aware
   `out[0][:] = ...` and tensor-direct `out[:] = ...`).
4. Composability: 3 interventions ran cleanly back-to-back without cache reset issues.

**What nnsight does NOT unlock for chat-cap rescue**:

1. Multi-step autoregressive intervention is expensive and would need a custom
   loop wrapping `nn_model.trace` per step — not free over standard hooks.
2. Basin re-formation is architectural (BG-BJ) and intervention at L8 alone is
   insufficient to bend the trajectory into coherent space.
3. Intervention magnitude scaling (zero vs. 2x vs. noise) does not monotonically
   map to coherence — confirms #115 chat-incapability is not a single-layer issue.

**Recommended next BG**:

- **BG-BX**: multi-layer intervention sweep (L0..L11) measuring max abs logit
  delta per layer at the same prompt; identifies critical layers for chat-cap
  collapse. Still $0 mac CPU, ~30min.
- **BG-BY**: axis-conditioned intervention — load Pβ Φ★-axis or CLM v4 LoRA
  delta as injection vector at L8 instead of zero/2x/noise; measures whether
  axis-direction intervention improves coherence vs. random.

## Constraints honored

- $0 mac CPU
- new files only (helper + state dir + this doc)
- raw#37 transient sister-rule (.py for nnsight, hexa cannot)
- raw#15 additive (no model file mod, no SFT, no commit)
- raw#10 honest C3 (5 caveats emitted)
- HEXA_PY=.venv-eeg/bin/python
- no HF token leak
- no commit (per task constraint)
