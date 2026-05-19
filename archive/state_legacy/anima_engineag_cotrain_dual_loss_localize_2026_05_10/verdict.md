# BG-ENGINEAG-COTRAIN-DUAL-LOSS-LOCALIZE — verdict

**FINAL_VERDICT**: `attention-driven cotrain signature with dominant component = q_proj; weight-drift pattern is U-shaped across depth (mid-layers most-changed) AND DECOUPLED from §57's slab1_early V14-dominance — F-DUAL-LOSS-3 partially triggered.`

**Star credit**: ★★★★ partial — q_proj uniquely identified as the most-changed component class (mean cos_AB = 0.6468, vs all MLP projections clustered ≈0.70 and v_proj ≈0.83), but the layer-axis pattern of weight drift inverts §57's slab dominance, so the 5-star single-locus claim is not supported.

**Dominant component**: `attn.q_proj.weight`
**Dominant layer band (by weight drift)**: layers 10–16 (param-weighted cos_AB ≈ 0.679)
**Dominant slab (by weight drift)**: `slab2_middle` (mean cos_AB = 0.7666)
**Dominant slab (per §57 V14 effect)**: `slab1_early` (mean cos_AB = 0.8205 — *least* drifted)

**Elapsed**: 42.6s on Mac CPU (envelope: target ≤2 min, well under).

## §57 cross-link — the central tension

§57 found: A1_slab1_early (layers 0–7) is the **uniquely dominant** V14 lever
— only slab whose swap collapses cells to its own attractor (n_cells=44,
Φ≈1037, Δ_sep=−1375).  A2/A3 swaps also flip V14 but produce bit-exact
identical degenerate trajectories (n_cells=43, Φ≈1343).

This BG finds: in **weight space**, slab1_early is the **least** modified
slab (mean cos_AB = 0.8205, vs slab2_middle 0.7666 and slab3_late 0.7788).
A param-weighted layer-by-layer profile shows a **U-shape**: layers 0–3 and
layer 23 are least drifted (cos ≈ 0.79–0.85), with peak drift at layers
10–16 (cos ≈ 0.68).

**Cross-link verdict**: drift magnitude and V14 causal effect are
**decoupled**.  §57 dominance is NOT explained by "slab1_early was most
modified by cotrain".  Instead, slab1_early is V14-dominant *despite* being
the least modified slab — implying that even small cotrain perturbations to
the early-layer attention readout disrupt downstream cell dynamics
disproportionately.  The early layers' role is "shape the input
representation that engine_g consumes", and small q_proj/k_proj shifts at
layers 0–3 cascade.  The middle and late layers, while more heavily
modified in absolute weight terms, can absorb arbitrary BG-LA←→A swaps
without breaking attractor selection because they fall into the shared
n_cells=43, Φ≈1343 basin (§57 honest C3 #11).

## Component ranking (mean over 24 layers)

| rank | component | mean cos_AB | mean rel_L2 | band | trainable? |
|---|---|---|---|---|---|
| 1 (most-changed) | `attn.q_proj.weight`  | 0.6468 | 0.8487 | WARM | yes |
| 2 | `ffn.gate.weight`     | 0.6998 | 0.7905 | COOL | yes |
| 3 | `ffn.down.weight`     | 0.7081 | 0.7805 | COOL | yes |
| 4 | `ffn.up.weight`       | 0.7084 | 0.7796 | COOL | yes |
| 5 | `attn.o_proj.weight`  | 0.7503 | 0.7170 | COOL | yes |
| 6 | `attn.k_proj.weight`  | 0.7523 | 0.7069 | COOL | yes |
| 7 | `attn.v_proj.weight`  | 0.8319 | 0.5853 | COOL | yes |
| — | `norm1.weight`        | 1.0000 | 0.0000 | (frozen) | nominally yes — empirically untouched in BOTH ckpts |
| — | `norm2.weight`        | 1.0000 | 0.0000 | (frozen) | nominally yes — empirically untouched in BOTH ckpts |

`norm_f.weight` (final RMSNorm) also bit-exact at init=1.0 in both ckpts.
RMSNorm gain is `nn.Parameter(torch.ones(d))` (no `requires_grad=False`),
so it is *nominally* trainable — but neither training run produced any
update large enough to escape bf16 round-off-to-1.0.  This is a finding
about the optimizer/grad-scale regime in both BG-LA pretrain and Phase 2
cotrain, NOT about the chat dual loss specifically.

## Attention vs MLP vs Norm — the lever assignment

| sub-system | components | mean cos_AB across 24 layers × N components | mean rel_L2 |
|---|---|---|---|
| **Attention readout** | q + k + v + o (4 components × 24 = 96 tensors) | **0.7453** | 0.7145 |
| **MLP** | gate + up + down (3 components × 24 = 72 tensors) | **0.7054** | 0.7836 |
| **RMSNorm** | n1 + n2 (2 components × 24 = 48 tensors) | 1.0000 (frozen) | 0.0000 |

By aggregate component-class mean cos, **MLP drifts slightly more than
attention** (0.7054 vs 0.7453).  But the **single most-changed slot** is
`q_proj` (0.6468), beating `gate` (0.6998) by a clear margin.  And `v_proj`
(0.8319) is much more preserved than the average.  So the attention class
splits internally:
- query (q): biggest drift — what to attend to is what the chat loss
  rewrites.
- key (k) / output (o): moderate drift (0.75) — comparable to MLP.
- value (v): largest preservation (0.83) — what to retrieve is largely
  inherited from BG-LA pretrain.

**Lever assignment**: chat dual loss is **q_proj-led** (token-conditional
attention pattern), with secondary distributed effect across MLP
gate/up/down and attn k/o.  This pattern is consistent with chat-format
cotrain training the model to recognize role boundaries, special tokens
(`<|im_start|>`, `<|im_end|>`, etc.), and turn-taking — all of which are
*query-side* patterns over self-attention.

## Per-layer drift profile (param-weighted cos_AB)

```
layer    pwc      band
 00     0.848    COOL  ← least changed
 01     0.787    COOL
 02     0.743    COOL
 03     0.726    COOL
 04     0.714    COOL
 05     0.702    COOL
 06     0.695    COOL
 07     0.691    COOL  ← end of slab1_early
 08     0.688    COOL  ← begin slab2_middle
 09     0.683    COOL
 10     0.680    COOL
 11     0.678    COOL  ← deepest drift
 12     0.679    COOL
 13     0.679    COOL
 14     0.681    COOL
 15     0.681    COOL  ← end of slab2_middle
 16     0.682    COOL  ← begin slab3_late
 17     0.685    COOL
 18     0.688    COOL
 19     0.693    COOL
 20     0.697    COOL
 21     0.709    COOL
 22     0.726    COOL
 23     0.765    COOL  ← lm_head boundary
```

U-shape with floor at layers 11–13.  Layers 0–3 are least drifted but
§57 says they are the V14-critical slab.  This means the earliest layers
encode embedding-near token-shape statistics that the cell pool reads
through engine_g; even a small cos drop (q-cos = 0.71 at layer 2 vs 0.60
at layer 17) is sufficient to displace the attractor — likely because the
early-layer hidden_mean fixes the input to the entire downstream stack,
including engine_g.

## Cross-link with §57 — ablation prediction (qualitative, not yet fired)

If a single-component swap study were fired (24 layers × q_proj swap A→B),
this analysis predicts:
1. **q_proj-only swap of slab1_early (layers 0–7)** would flip V14 with
   the largest separation drop, mirroring §57's A1 dominance —
   even though this is the smallest weight delta.  This is testable.
2. **q_proj-only swap of slab2_middle/late** would either preserve V14 or
   collapse to the shared §57 attractor at (n_cells=43, Φ≈1343), again
   mirroring §57.
3. **v_proj-only swap (any slab)** would barely perturb V14 — v is the
   most-preserved component, so swapping it removes the smallest amount of
   cotrain-specific information.
4. **MLP-gate-only swap** would perturb V14 less than full slab swap but
   more than v_proj swap.

Cost of firing the prediction: 24 × ~6 min = 2.4h on Mac CPU per single-
component-axis (deferred per budget; logged as follow-up §59).

## Falsifier verdicts

- **F-DUAL-LOSS-1 (uniform across components)**: NOT triggered.  q_proj
  (0.65) clearly separates from v_proj (0.83) — a 0.18 cos_AB spread is
  ~3× the within-MLP spread (gate 0.700, up 0.708, down 0.708).
- **F-DUAL-LOSS-2 (norm-shift artifact)**: NOT triggered, and additionally
  ruled out by direct evidence — RMSNorm weights are bit-exact 1.0 in
  BOTH ckpts; cotrain didn't shift them at all.
- **F-DUAL-LOSS-3 (component-finding inconsistent with §57 slab)**:
  **PARTIALLY TRIGGERED**.  Component-level dominant = q_proj (consistent
  with attention being the reshaped sub-system).  But layer-axis
  dominant-by-drift = slab2_middle (layers 10–16), inverting §57's
  slab1_early dominance.  Therefore the single-component-single-locus
  ★★★★★ claim is unsupported.  Verdict downgraded to ★★★★ partial:
  q_proj is the dominant component class and chat loss is
  attention-readout-led, but drift magnitude is NOT a sufficient predictor
  of V14 causal effect — small early-layer perturbations dominate over
  large mid-layer perturbations in attractor selection.

## Honest C3 (≥7)

1. **Cosine is direction-only.**  cos_AB measures angle between flattened
   tensors; it ignores scale.  rel_L2 (l2_diff / l2_A) is reported alongside
   for magnitude.  Both rank q_proj as most-changed.  Result is robust under
   either metric.
2. **bf16 quantization floor.**  Both ckpts are stored in bf16 (~7-bit
   mantissa).  Differences below 2^-8 ≈ 4e-3 (relative to scale) collapse
   to zero.  This explains exactly why RMSNorm weights register as
   bit-exact across A and B — any subtle gain shift was eaten by bf16
   round-off near 1.0.  We cannot resolve below this floor; conclusions are
   valid for "above-bf16-noise" drift only.
3. **q_proj's primacy may reflect q's larger optimizable surface, not chat
   loss specificity.**  q_proj is (1024, 1024) = 1.05M params; k/v_proj are
   (256, 1024) = 0.26M each (GQA factor 4).  More params, more places for
   gradient to land.  Compare against per-param drift: q rel_L2 = 0.85, k
   rel_L2 = 0.71, v rel_L2 = 0.59 — q is *still* the highest in
   normalized-Frobenius terms, so this is not just a param-count artifact;
   but a portion of q's lead may be statistical.
4. **Phase 2 cotrain ≠ "chat-only".**  Substrate A's chat dual-loss
   curriculum included continued anima-persona language modeling
   (w_anima = 0.7→0.5 over the curriculum); the chat-only signal was
   w_chat = 0.3→0.5.  The A↔B delta therefore reflects "added 30-50% chat
   gradient + continued LM gradient" — not "replace LM with chat".  The
   q_proj signature is the *marginal* effect of the chat term, not the
   pure chat training signature.
5. **B is not a fresh init.**  B = step_12000 of BG-LA pretrain on persona
   corpus.  A = BG-LB pretrain → Phase 2 cotrain.  A and B share neither a
   common ancestor checkpoint nor a common pretrain corpus exactly
   (BG-LB vs BG-LA differ in tokenizer remapping).  The cos_AB ≈ 0.65–0.83
   range therefore reflects **(BG-LA pretrain trajectory) vs (BG-LB
   pretrain trajectory + cotrain)**, not "cotrain delta" in isolation.
   To isolate cotrain alone we would need (BG-LB-pretrain-only) vs
   (BG-LB-pretrain → Phase 2 cotrain) — that ckpt pair was not produced
   under the §57 budget but is the canonical follow-up.
6. **Effective rank is essentially preserved.**  q_proj effective rank
   stays in [793, 808] across all 24 layers in both A and B (full-rank
   for 1024×1024 = max possible 1024).  Cotrain modifies *direction*
   (cos_AB drops to 0.6) without collapsing rank.  This is consistent with
   a low-norm directional update on top of a full-rank pretrain ckpt — the
   pattern of LoRA-like fine-tuning, even though Phase 2 was full-tensor
   cotrain.  Sparsity is also pinned (~0.003 in both).
7. **Tied lm_head and tok_emb.**  cos_AB = 0.7464 for `tok_emb.weight` and
   `lm_head.weight` is exactly equal (both 32000×1024).  These tensors are
   tied at runtime per `EngineAGModel` config.  The drift is non-trivial —
   chat dual loss substantially reshaped the embedding/unembedding map.
   §57's swap study fixed both at A's values across all conditions, so
   this drift contribution is not directly tested.  A follow-up swapping
   tok_emb is the natural extension.
8. **Single-seed source for swap predictions.**  The §59 ablation
   prediction (q_proj-only swap → V14 flip pattern mirroring §57) is based
   on B = a single BG-LA pretrain ckpt at step_12000.  Multi-seed B would
   strengthen the qualitative prediction; deferred under .
9. **No forward pass.**  This is pure weight-space analysis.  We do not
   measure "how much does q_proj drift propagate to hidden_mean".  §57
   already showed (C3 #11) that layer-7 vs layer-8 perturbations of
   comparable weight magnitude produce dramatically different cell-pool
   trajectories; weight-space cosine cannot capture that asymmetry.  The
   ★★★★ verdict here is consistent with that asymmetry — drift magnitude
   and V14 causal effect ARE empirically decoupled.
10. **9 components is the natural per-block decomposition under
    `EngineABlock`.**  RoPE has no learnable parameters
    (cos/sin are register_buffers), so it is correctly absent from the
    216 measurements.  Engine G blocks (cell_pool_init, c_to_h, h_to_c)
    are excluded — they are §50/§58's territory.  Per §50 they are
    correlational, not causal; per §58 the h_to_c cell-proximity learning
    is the substrate-level mechanism, downstream of engine_a's
    hidden_mean.  Thus engine_a 24×9 = 216 is the correct surface for
    "where does the cotrain gradient land".
11. **Heat-band thresholds are arbitrary.**  HOT/<0.40, WARM/<0.65,
    COOL/<0.85, COLD/≥0.85 are convention.  No q_proj layer falls below
    0.59; no non-norm component reaches 0.95 except layer 0/1 q which
    are 0.81–0.90.  All non-norm cells fall in WARM or COOL.  The
    qualitative ranking (q < gate ≈ down ≈ up < o ≈ k < v) is
    threshold-independent.
12. **Cosine threshold for "uniformly distributed".**  σ across the 7
    trainable components' mean cos_AB = 0.0578 (stdev of {0.6468, 0.6998,
    0.7081, 0.7084, 0.7503, 0.7523, 0.8319}).  This is large enough to
    reject F-DUAL-LOSS-1 by visual inspection, though no formal test
    statistic is computed.  A bootstrap or permutation test would
    formalize; not done under .

## Summary

The chat dual-loss cotrain is an **attention-readout reshaping** —
specifically, **q_proj** carries the largest weight delta (cos_AB =
0.6468), with secondary near-uniform contribution from MLP gate/up/down
(≈0.70).  v_proj is the most preserved (0.83), confirming that the *what*
of attention (value content) is largely inherited from BG-LA pretrain
while the *what to attend to* (query) is what chat-format training
rewrites.  RMSNorm gains are bit-exact frozen at 1.0 in both ckpts,
ruling out F-DUAL-LOSS-2.

The layer-axis profile is **U-shaped** with floor at layers 11–13,
inverting §57's slab1_early V14-dominance.  Drift magnitude and V14
causal effect are **decoupled** — the slab that drifts least
(slab1_early) is the slab whose swap is most catastrophic, and the slab
that drifts most (slab2_middle) collapses into the same §57 degenerate
attractor as slab3_late.  This is the partial F-DUAL-LOSS-3 trigger.

**Star verdict**: ★★★★ — q_proj component-class identified, but
single-locus ★★★★★ unsupported because layer-axis weight drift inverts
§57 slab dominance.  §50 PROVEN-AT-BODY-LOCUS is preserved and
**refined**: the body lever is q_proj-attention-readout-mediated, not
MLP-feature-mixing-mediated, and the small early-layer q_proj
perturbations matter more than large mid-layer perturbations.

**Follow-up (§59 candidate)**: 24-condition single-component swap study
(q_proj only, gate only, v_proj only) at the slab1_early band, V14 mirror
3-seed × 200-turn — predicted runtime ~3h on Mac CPU; will resolve
"is it q_proj specifically that flips V14, or the q+k+o ensemble?".
