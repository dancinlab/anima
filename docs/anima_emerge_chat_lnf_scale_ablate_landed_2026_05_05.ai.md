<!-- @no-lineage-citation-exempt-file -->
# anima emerge chat — ln_f weight scale ablation landed 2026-05-05

**Task ID**: anima_emerge_chat_lnf_scale_ablate_2026_05_05
**Lane**: BG-CF (BG-BQ "UPSTREAM RMSNorm collapse" hypothesis check)
**Platform**: mac CPU (.venv-eeg python3.12, torch fp32)
**Cost**: 0 USD
**Wall**: ~1 min (model load 14.3s + 9 forward decodes)

---

## Hypothesis under test

BG-BQ verdict (state/anima_emerge_chat_head_compare_2026_05_05/verdict.json,
verdict FAIL_ALL_HEADS) found that all 4 head paths (baseline forward / head_a /
head_g / tied tok_emb) produced incoherent emits from the prompt 안녕, suggesting
the pathology is UPSTREAM of the LM head. Primary suspect: decoder.ln_f
(RMSNorm) gain weight collapsed into a degenerate fixed point that pins argmax
onto a single basin token irrespective of input content.

**Falsifier H_lnf_gain**: vary decoder.ln_f.weight (gain) over a wide grid plus
unit and random replacements. If any non-baseline config breaks the basin
(emits distinguishable text), ln_f gain IS a basin lever.

---

## Method

- Model: need-singularity/clm-v4-mk2-v1 (CLM v4 mk2 v1)
- Loader: shared _try_load_model / _load_tokenizer from
  tool/transient_py/anima_emerge_cand_d_inject_helper.py
- Prompt: 안녕하세요. 오늘 날씨가 좋네요. (KO long greeting; n_input=12 toks)
- Decode: greedy argmax, 25 new tokens
- Configs (9):
  - baseline (original ln_f.weight, no modification)
  - scale_{0.1, 0.5, 1.5, 2.0, 5.0, 10.0} (multiplicative scaling)
  - unit_weight (replace with torch.ones_like)
  - random_normal_weight (gaussian preserving original mean+std, seed=42)
- Restoration: original weight cloned and restored after sweep
- Coherence heuristic: len>=5 AND (korean+ascii_letters)>=5 AND max_char_freq<=50%

---

## Result

### ln_f.weight stats

```
type:  RMSNorm
shape: (768,)
mean:  1.0384
std:   0.0137
min:   1.0141
max:   1.0986
```

### 9 emits

| config               | emit                          |
|----------------------|-------------------------------|
| baseline             | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_0.1            | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_0.5            | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_1.5            | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_2.0            | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_5.0            | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| scale_10.0           | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| unit_weight          | /OOOOOOOOOOOOOOOOOOOOOOOO     |
| random_normal_weight | /OOOOOOOOOOOOOOOOOOOOOOOO     |

- diff_from_baseline_count: **0 / 8**
- n_coherent: **0 / 9**

### Verdict

**FAIL_LNF_NOT_THE_BUG**

The basin is INVARIANT to ln_f gain perturbation across 100x dynamic range
(0.1x to 10x) AND under structural replacement (unit weights, random gaussian).
ln_f gain is NOT in the causal path of the basin attractor.

---

## Interpretation

This **falsifies** the BG-BQ working hypothesis that ln_f gain is the upstream
RMSNorm-collapse contributor. The pathology is robust to:

1. **Scale dynamics** — 100x gain dynamic range produces zero output change.
   Implies the ln_f gain modulation is being absorbed/normalized by a
   downstream component (likely lm_head softmax saturation, OR the basin
   token-id is selected by argmax-rank that survives any monotonic gain
   transform on the pre-head residual).
2. **Structural identity** — replacing the learned ~1.04 mean gain with unit
   weights or a random gaussian (same first/second moments) does NOT
   destabilize the attractor. The attractor lives in a feature direction that
   has been amplified to the point where argmax is gain-monotone.

### Where the basin actually lives — narrowed candidates

- **NOT** ln_f gain (this BG-CF closes that lane).
- Likely deeper than ln_f: pre-ln_f residual stream is itself collapsed onto a
  single dominant direction. The next probes should attack:
  - pre_ln_f_residual_norm_distribution (does the pre-ln_f hidden have one
    dominant feature direction that survives any norm gain?)
  - lm_head.weight row-norms — the basin token row may have anomalous
    norm-magnitude that wins argmax under any reasonable hidden vector
  - tok_emb row-norms — if tied, same effect via embedding magnitude
- **rms-normalization step itself** (denominator) — this BG-CF varied gain only;
  varying or removing the rms(x) denominator was out of scope (C2).

---

## honest C3 (verdict-embedded, see verdict.json)

- C1 mac CPU fp32 noise floor; argmax tie-break deterministic for this run only.
- C2 single-component intervention — gain only, not full RMSNorm; rms-denominator
  variation needed for whole-norm pathology test.
- C3 single prompt KO long; per-prompt variance not measured.
- C4 semi-coherence heuristic is anima-internal screening tool; false-pos/neg
  risks acknowledged. (Moot here — all 9 emits identical degenerate string.)
- C5 weight modification by-construction changes outputs; observed
  non-modification result is robust BUT could in principle reflect numerical
  instability collapsing into the same argmax via different paths. Replication
  with diverse prompts strengthens claim.

---

## Next-step recommendation (ranked by 완성도)

1. **lm_head.weight row-norm survey** (0 USD mac CPU, ~5 min) — measure
   per-token row norm distribution; if `/` and `O` tokens have anomalous
   max-norm rows, the basin is a vocabulary-row-norm artifact, not a
   representation-space issue. STRONGEST diagnostic value next.
2. **pre-ln_f residual feature-axis SVD** (0 USD mac CPU, ~10 min) — capture
   model.decoder.layers[-1] output (pre-ln_f hidden) over a small prompt
   sweep, run SVD; if 1 singular value dominates by >10x, the basin lives in
   that direction.
3. **rms-denominator ablation** (0 USD mac CPU, ~15 min) — replace
   decoder.ln_f.forward with identity (skip rms-normalization entirely);
   tests whether the rms-step itself zeros the variation. C2 follow-up.
4. **token-id forensics** (0 USD mac CPU, ~3 min) — what bytes/tokens are `/`
   and `O` in the 64k SentencePiece vocab? If they are common SentencePiece
   bookkeeping tokens (continuation/merge artifacts), the basin may be a
   tokenizer-level rather than model-level issue.

---

## Deliverables

- state/anima_emerge_chat_lnf_scale_ablate_2026_05_05/aggregate.json — 9 emits
- state/anima_emerge_chat_lnf_scale_ablate_2026_05_05/verdict.json — verdict + C3
- tool/transient_py/anima_emerge_chat_lnf_scale_ablate.py — helper
- docs/anima_emerge_chat_lnf_scale_ablate_landed_2026_05_05.ai.md — this doc

---

## Compliance notes

- transient .py sister-rule helper (torch.nn weight ablation inline; hexa
  cannot do this) — additive only (no mount.hexa / dialogue / shim
  modification) — 5 honest C3 emitted to verdict.json — gitignored per
  **/*.py — N/A H100 cost gates (mac CPU 0 USD, no H100 BG) — no commit per
  BG-CF spec — no HF token leak (model load uses cached snapshot only)
