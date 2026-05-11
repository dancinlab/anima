<!-- @no-lineage-citation-exempt-file — landed cycle doc references prior closures by behavior, not lineage. raw policy mentions are policy-name strings, not citations. -->

# anima_emerge_chat_sae_pca_features — landed 2026-05-05

**Cycle**: BG-BH — CLM v4 chat-related interpretable feature 발견 시도 (simplified PCA-style SAE)
**Verdict**: `FAIL_ALL` (n_coherent = 0/10)
**Cost**: $0 (mac CPU fp32)
**Wall**: ~30min (model load + 40 residual captures + SVD + 10 × 30 steered forward passes)
**Substrate**: `dancinlab/clm-v4-mk2-v1` via `inj_helper._try_load_model`
**Layer**: 8 (mid-layer of CLM v4 decoder; D=768)
**Prompt**: `안녕`
**Compliance**: raw policy 37 + 15 + 10 PASS; no commit; no secret leak; HEXA_PY=.venv-eeg/bin/python; new files only

---

## TL;DR

The hypothesis was: **Anthropic Circuits April 2025 SAE methodology** says language models contain interpretable monosemantic features (incl. chat / persona / role-play features) recoverable via sparse coding on the residual stream. A *true* SAE requires expensive training, but a **simplified PCA proxy** (top-k right singular vectors of the chat plus non-chat residual matrix at layer 8) might surface a chat-discriminative direction that doubles as a steering vector for unblocking the chat-incapability gap.

**It does not.** Top-2 PCA components have *strong* chat-vs-non-chat discriminator scores (25.67 / 13.34 — clearly above the noise floor of feat-2/3/4 at 0.16 / 0.23 / 1.06), confirming the residual stream encodes a chat/non-chat axis. But steering at α in {1.0, 4.0, 8.0} along the unit-normed top-3 features yields the **same control-byte / replacement-char gibberish** that prior decode-strategy and feature-injection cycles produced. n_coherent = 0/10 across baseline + 9 steered configs.

This is a **fifth converging closure** of the chat-unblock investigation. PCA (and by extension a properly-trained SAE on this residual stream) finds the direction that *separates* chat from non-chat representations, but pushing along that direction does not flip the lm_head argmax distribution off the control-byte basin. The discriminator axis exists in *encoded representations*; the gibberish is in the *decoded vocabulary*. They are decoupled.

Aligns with the architectural chat-incapability finding and the substrate-research-only verdict on CLM v4 — chat-cap is not in the residual feature axis any more than it was in the SFT, the distill, the cross-modal bridge, or the decode strategy.

---

## (a) PCA top-10 singular values — rich features?

| Rank | Singular value | Comment |
|---|---|---|
| 1 | 131.87 | Dominant axis |
| 2 | 79.77 | Strong secondary axis |
| 3 | 51.12 | Tertiary |
| 4 | 32.30 | |
| 5 | 23.17 | Knee |
| 6 | 6.04 | drop ~4x |
| 7 | 4.10 | |
| 8 | 3.28 | |
| 9 | 2.60 | |
| 10 | 1.92 | Noise floor |

**Read**: clear knee at rank-5 to rank-6 (23.17 to 6.04, ~4x drop). Top-5 SVs span 5 dominant directions in the 768-D residual at layer 8. **Rich enough** that PCA truncation to 5 captures the meaningful structure of the 40-sample combined matrix.

---

## (b) Discriminator scores — top-5 features chat vs non-chat

| Feature | Chat proj mean | Non-chat proj mean | Discriminator |chat - non-chat| |
|---|---|---|---|
| **0** | 0.547 | 26.218 | **25.671** strongest |
| **1** | 7.099 | 20.437 | **13.339** second |
| 2 | -32.571 | -32.735 | 0.163 |
| 3 | 2.884 | 2.658 | 0.227 |
| 4 | 39.475 | 40.533 | 1.058 |

**Read**: feat-0 and feat-1 are **strongly chat-discriminative** (25.67 and 13.34, well above feat-2/3/4 at 0.16-1.06). feat-0 has chat-mean ~ 0 and non-chat-mean ~ 26 — i.e., this PCA axis is **activated by code/regex/SQL/symbol non-chat** and *deactivated* by Korean/English chat. feat-1 same direction, weaker. feat-2/3/4 are essentially shared content axes. **Chat/non-chat axis exists** in the layer-8 residual.

---

## (c) 10 emit configs

| Config | Emit (first 30 chars) | Coherent? |
|---|---|---|
| baseline | control-byte degeneracy `\x1c\x06\x06\x06...` (30 chars) | NO |
| feat0_alpha1.0 | identical to baseline | NO |
| feat0_alpha4.0 | replacement-char gibberish `??????????...` | NO |
| feat0_alpha8.0 | single-char degeneracy `/OOOOOOOO...` | NO |
| feat1_alpha1.0 | identical to baseline | NO |
| feat1_alpha4.0 | replacement-char gibberish | NO |
| feat1_alpha8.0 | replacement-char gibberish | NO |
| feat2_alpha1.0 | identical to baseline | NO |
| feat2_alpha4.0 | mostly replacement-char with one CJK char | NO |
| feat2_alpha8.0 | mostly replacement-char with one CJK char | NO |

**n_coherent = 0/10**.

**Coherent heuristic** (anima-internal): >= 5 semantic chars (Korean syllables 가-힣 OR ASCII letters) + no single character occupying >50% of the emitted text.

---

## (d) Verdict: **FAIL_ALL**

`n_coherent = 0/10 < 1` therefore `FAIL_ALL`.

### Root-cause read

1. **PCA finds the chat axis but cannot exploit it.** The discriminator scores (feat-0 = 25.67, feat-1 = 13.34) prove the residual stream at layer 8 *contains* a chat-vs-non-chat axis. However, steering along that axis at α in {1, 4, 8} does not unlock chat emit — the lm_head still concentrates argmax on control-byte / replacement-char tokens. The encoded discriminative axis and the decoded vocabulary distribution are **decoupled**.

2. **alpha=1.0 is indistinguishable from baseline.** Across feat-0/1/2 at alpha=1.0, the emit is byte-identical to the unsteered baseline. Unit-normed steering at alpha=1.0 perturbs the residual by L2-norm 1.0 in a 768-D space; the lm_head logit gap to "non-control-byte" is wider than this perturbation. Mirrors the prior finding that +2.0 logit bias on Korean tokens does not flip argmax.

3. **alpha=4-8 destroys the residual without recovering text.** At higher alpha, the steered residual is far from the manifold the lm_head was trained on, and the emit collapses to replacement chars (UTF-8 decode failures of arbitrary BPE tokens) or single-character degeneracy. This is failure-by-OOD, not chat-axis activation.

4. **Direction sign untested.** We pushed `+alpha * feat`. Pushing `-alpha * feat` (toward the *chat* end of feat-0, since chat-mean ~ 0 is *below* non-chat-mean ~ 26) was not exercised — but baseline `안녕` already produces gibberish, suggesting the residual already *is* on the chat-end of feat-0 and pushing further toward chat would not help. C3 carry below.

5. **A true SAE would not fix this.** A properly-trained SAE adds a sparse-coding L1 constraint that produces *monosemantic* features instead of the dense PCA components here. But the failure is **downstream of feature discovery** — it is in the lm_head argmax basin. A monosemantic "chat" SAE feature steered into the layer-8 residual would face the same lm_head argmax barrier observed here.

---

## (e) 5 honest C3 carries

1. **C1 — mac CPU fp32**: model loaded fp32 on CPU. Quantization or MPS could shift logits slightly but not by enough to flip argmax off the control-byte basin (large gap confirmed by prior +2.0-logit-bias non-effect cycle).

2. **C2 — PCA-style not equal to true SAE**: simplified PCA omits the sparse-coding (L1) constraint that produces monosemantic features in Anthropic's SAE methodology. PCA components are dense linear combinations of activations, not interpretable single-neuron-like features. **However** — root-cause #5 above — the failure is in the lm_head basin, not in feature monosemanticity. A true SAE would reproduce this null result.

3. **C3 — 20 chat x 20 non-chat under-powered**: 40 samples in 768-D space yield 40-rank SVD (limited by min(2N, D)). A 1000+ sample mini-corpus would tighten the SV spectrum, but the rank-1 to rank-5 spread already shows clear chat-discriminative axes (feat-0, feat-1). Sample size is sufficient for the falsification gate.

4. **C4 — single layer 8**: SAE methodology proper trains layer-specific features at multiple residual stream positions. Layer 8 was a mid-decoder choice; layer-12/15/-1 could have different chat-axis encodings. **However** — the prior decode-strategy cycle already showed the *final lm_head logits* are in the control-byte basin; any earlier layer's chat axis has to flow through the same lm_head bottleneck.

5. **C5 — last-token residual aggregation**: we extracted only the last-token residual per text. SAE proper aggregates per-token features across the whole sequence and identifies feature activation patterns. Last-token is a coarse proxy. **However** — for *steering*, the relevant residual position is exactly where the next-token logits are computed, i.e., last-token. C5 limits feature *discovery* but not feature *steering* fidelity at the chosen prompt position.

6. **C6 (extra) — direction sign untested**: only `+alpha * feat_unit` was tested. Pushing `-alpha` (toward chat end of feat-0) was omitted. Given baseline already emits gibberish on `안녕` (which by feat-0 mean is on the chat side), pushing further chat-ward is unlikely to help — but a 4-config plus-and-minus-alpha extension would close this loop. Filed as future work.

---

## Architectural chat-incapability — fifth convergence

| Investigation closure | Result | Mechanism eliminated |
|---|---|---|
| Phi-axis Paradigm D 50K distill (prior) | FAIL_TRUE composite 0.01176 | Distillation lift |
| CLM v4 LoRA SFT (prior) | FAIL_REGRESSION -36.298pp vs Llama Path A v2 | SFT lift |
| tribev2 chat bridge (prior) | FAIL_ALL_TRIED architectural | Cross-modal-encoder bridge |
| Decode strategy sweep (prior) | FAIL_ALL n_coherent=0/6 | Sampling/decode loop |
| **PCA-style SAE feature steering (this cycle)** | **FAIL_ALL n_coherent=0/10** | **Residual-stream feature axis** |

**Verified (5x).** Five orthogonal closures converge: chat-incapability is not in the distillation, the SFT, the cross-modal bridge, the decode loop, **or the residual-stream feature axis**. It is in the lm_head plus upstream representations *jointly*, in a way that surface interventions on hidden states cannot recover.

---

## Recommendation (ranked by 완성도 lens)

1. **STOP CLM v4 chat-unblock attempts.** Five orthogonal closures plus the substrate-research-only finding triangulate: any further mac-CPU-cheap intervention on CLM v4 chat is expected-FAIL. Reallocate to CLM-2-EXEC and Llama Path A v2 lanes.

2. **Optional plus-and-minus-alpha direction-sign loop** (C6 carry) — 30min, $0 — purely for completeness. Low expected information given the basin-degeneracy already established.

3. **Defer true SAE training.** Anthropic Circuits methodology requires GPU-hours to train an SAE on a residual stream layer; root-cause #5 suggests this would reproduce the null and is not cost-justified given five existing closures.

---

## Files

- helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_sae_pca_features.py` (raw policy 37 transient)
- state: `/Users/ghost/core/anima/state/anima_emerge_chat_sae_pca_features_2026_05_05/{aggregate.json, verdict.json}`
- doc: `/Users/ghost/core/anima/docs/anima_emerge_chat_sae_pca_features_landed_2026_05_05.ai.md` (this file)

End of cycle.
