# BG-ENGINEAG-COTRAIN-DUAL-LOSS-LOCALIZE — spec

**Date**: 2026-05-10
**Lineage**: §50 → §57 (slab-locus) → §58 (correlation/h_to_c) → THIS BG (component-locus).
**Predecessor verdict**: §57 PROMOTED §50 to PROVEN-AT-BODY-LOCUS — engine_a's
24-layer transformer body collectively carries the V14 PASS lever; A1/A2/A3
swaps all flip V14_PASS → V14_VIOLATED, with A1_slab1_early dominant in
attractor selection.
**Mission**: drill one level deeper than §57 — at the (layer × component)
granularity of 24 × 9 = 216 parameter sub-tensors, which slot was most
reshaped by Phase 2 chat dual-loss cotrain (substrate A) relative to
BG-LA persona-only pretrain (substrate B)?

## Hypothesis

H-COMP: cotrain w=0.3→0.5 chat dual loss does not modify all 9 per-layer
components equally.  One of {RMSNorm, GQA q/k/v/o, SwiGLU gate/up/down}
takes the brunt of the gradient.  Component-level localization will tell us
**which sub-system the chat loss actually trains** — attention readout
(q/k/v/o), feature mixing (gate/up/down), or normalization (n1/n2).

## Substrates

Identical to §57.

| Substrate | path | params | training |
|---|---|---|---|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | 350M bf16 | BG-LB pretrain → Phase 2 chat-template cotrain (curriculum w=0.3→0.5) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | 350M bf16 | BG-LA persona-only pretrain (no chat dual loss) |

Both share `EngineAGConfig` (24 layers, d=1024, GQA 16/4, SwiGLU 2.6875,
Engine G dim=64, n_cells=16).  Identical architecture; only training regime
differs.

## Method

For each fully-qualified parameter `layers.{i}.{c}.weight` with i ∈ [0,24),
c ∈ {norm1, attn.q_proj, attn.k_proj, attn.v_proj, attn.o_proj, norm2,
ffn.gate, ffn.up, ffn.down}, compute:

| metric | definition |
|---|---|
| `cos_AB` | `cos(vec(A), vec(B))` after fp32 cast |
| `l2_A`, `l2_B` | Frobenius norm of A, B |
| `l2_diff` | Frobenius norm of (A − B) |
| `relative_l2_diff` | `l2_diff / l2_A` |
| `effective_rank_A`, `_B` | `exp(H(p))` where p = svals/Σsvals |
| `sparsity_A`, `_B` | fraction of |w| < 1e-4 |
| `singular_value_l1_diff` | `Σ_i |σ_i(A) − σ_i(B)|` |

Plus aggregate roll-ups: per-component (mean over 24 layers), per-layer
(mean over 9 components), per-slab (cross-link with §57's 3-slab grouping).
Also: tok_emb, norm_f, lm_head as global-extras.

## Output deliverables (own 38)

| file | content |
|---|---|
| `spec.md` (this) | hypothesis + method + falsifier table |
| `component_metrics.json` | all 216 per-pair scalars + aggregates |
| `heatmap_table.md` | 24×9 cos_AB matrix + per-band classification |
| `verdict.md` | dominant-component decision + §57 cross-link + C3 ≥7 |
| `run.py` | the executable (raw#9, state-local, gitignored) |
| `run.log` | timestamped run-log |

## Verdict logic

| Outcome | Interpretation | Star credit |
|---|---|---|
| All 9 components ≈ uniform cos | F-DUAL-LOSS-1 distributed at component-level | ★★★★ §50 strengthened |
| `norm1`/`norm2` uniquely most-changed | F-DUAL-LOSS-2 normalization-shift artifact | (architectural reduction effort) |
| Single attn proj uniquely most-changed | attention-driven cotrain signature | ★★★★ specific |
| q+k+v+o together most-changed > MLP | attention readout dominant | ★★★★ specific |
| gate+up+down together most-changed > attn | MLP-driven cotrain signature | ★★★★ specific |
| Component-level finding inconsistent with §57 slab dominance | F-DUAL-LOSS-3 cross-link broken | reframe required |

★★★★★ candidate iff a single component class dominates AND its layer
pattern matches §57 slab1_early dominance (i.e., the same 8 layers carry
both the largest weight drift and the largest V14 effect).

## Falsifiers

- **F-DUAL-LOSS-1**: distributed across all 9 components (cos_AB σ < 0.05
  across components).  Interpretation: chat loss diffuses across the whole
  block uniformly.  ★★★★ partial.
- **F-DUAL-LOSS-2**: norm1/norm2 most-changed.  Indicates that gain/scale
  is the only thing the chat loss adjusted, suggesting an architectural
  redundancy (chat loss could equivalently be replaced by per-layer scalar
  scaling).
- **F-DUAL-LOSS-3**: dominant component identified but its layer pattern
  inverts §57 (e.g., max drift in slab3_late while §57 dominance is
  slab1_early).  Cross-link broken — drift magnitude and V14 effect are
  decoupled.

## Constraints (own/raw)

- **raw#9** — `training/*.py` local-only; this script lives under `state/`
  (gitignored).
- **raw#15 additive** — A and B ckpts loaded read-only via `torch.load`;
  all tensor ops are out-of-place; no file mutation.
- **own 16** — $0 local Mac CPU; weight-only analysis (no model forward,
  no GPU).  Wall-clock target ≤2 min.  Achieved: 42.6s.
- **own 22** — every metric scalar emit; verdict.md SSOT.  REBORN.md
  appendage handled by dispatcher §62.
- **own 38** — artefacts under
  `state/anima_engineag_cotrain_dual_loss_localize_2026_05_10/`.

## Time budget

- 24 layers × 9 tensors × (cos + L2 + SVD) on bf16 → ~1-2 min on Mac CPU.
- Actual elapsed: **42.6s**.
