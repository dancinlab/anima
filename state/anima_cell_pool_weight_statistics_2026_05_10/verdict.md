# BG-CELL-POOL-WEIGHT-STATISTICS — verdict

ts: 2026-05-10
fire keyword: AUTO ($0 local CPU, ~25s wall)

## TL;DR
**Cotrain-exercise hypothesis: PARTIAL CONFIRM (★★★ weight-space evidence)**
- `cell_pool_init`: cotrain effect VERY SMALL (fro-norm Δ = 0.0020 vs substrate; identity-perm Hungarian to BG-LA control). Cell-pool barely exercised by chat-loss backward — F-WEIGHT-3 partially fires.
- `h_to_c.weight` + `c_to_h.weight`: cotrain effect MODERATE-LARGE (fro-norm Δ = 0.162 / 0.116 vs substrate). Both projections exercised — clear weight signature.
- A vs B (independent control): cell_pool cosine 0.99996 (~identical), but h_to_c cosine 0.764, c_to_h cosine 0.692 — projections diverged substantially. Cotrain effect on projections isolated from cell_pool itself.

## C3 (honesty)
**C3 = 8/10**
- 5 ckpts loaded, 222 keys cataloged, focus + control tensors statistically audited
- Bonus substrate ckpt (S = BG-LB step 8000) loaded for true cotrain isolation (S→A vs S→B)
- Architectural mismatch identified upfront: v2 (C/D/E) has no cell_pool tensor (paradigm-effect, not failure)
- bf16 quantization artifact disambiguated from real training delta
- Limitations admitted: no intermediate Phase 2 ckpts (1500/3000/4500/6000) on disk → trajectory analysis impossible; t-SNE on 16-cell pool would be visually meaningless and was skipped
- Falsifier F-WEIGHT-1 result on cell_pool challenges the strong form of the hypothesis (cell_pool barely moves) — emitted faithfully

## Falsifier outcomes
- **F-WEIGHT-1** (A vs B no diff): **MIXED** — cell_pool nearly identical (cosine 0.99996), but h_to_c (0.764) and c_to_h (0.692) clearly diverged. Hypothesis split across the three tensors.
- **F-WEIGHT-2** (random vs trained no diff): **REJECTED** — multiple metrics diverge:
  - cell_pool stable_rank: trained 8.0 vs random_baseline_median 7.75 (close, since unit-sphere init is also close to random)
  - h_to_c effective_rank: A=35.2, B=30.4 vs random=62.0 → trained eff_rank ~half of random (CLEAR signal)
  - c_to_h cum_var_top10: A=0.72, B=0.82 vs random=0.22 (trained concentrates variance into top-10 σ)
  - mp_spectral_ratio for h_to_c/c_to_h: trained 2.6–3.8 vs random=1.0 (trained spectral norm 3-4× MP prediction → low-rank signal)
- **F-WEIGHT-3** (cell_pool eff_rank invariant): **CONFIRMED** — A and B both have eff_rank ≈ 14.08 (random baseline 14.05); cotrain does NOT meaningfully change cell_pool spectral structure. Cell_pool stays near unit-sphere uniform.

## Evidence strength
Per-component cotrain-exercise verdict (using S→A vs S→B fro-normalized delta as the clean isolation):

| tensor | S→A (cotrain 6k steps) | S→B (BG-LA pretrain 12k from same seed) | A/B cos | verdict |
|---|---|---|---|---|
| `engine_g.cell_pool_init` | 0.00202 | 0.00872 | 0.99996 | **barely exercised** |
| `engine_g.h_to_c.weight` | 0.16185 | 0.69635 | 0.76405 | **clearly exercised** |
| `engine_g.c_to_h.weight` | 0.11646 | 0.87669 | 0.69239 | **clearly exercised** |
| layers.0.attn.q_proj.weight | 0.18794 | 0.42624 | — | exercised (control) |
| layers.0.ffn.gate.weight | 0.18205 | 0.58366 | — | exercised (control) |
| layers.11.attn.q_proj.weight | 0.23167 | 0.88511 | — | exercised |
| layers.23.ffn.down.weight | 0.19299 | 0.60104 | — | exercised |
| tok_emb.weight | 0.68019 | 0.25263 | — | A more exercised than B (chat corpus byte distribution shift) |

Interpretation:
1. **cell_pool_init is essentially frozen by cotrain**. Even though `requires_grad=True` (no explicit freeze in `train_phase2_cotrain.py`), the gradient flow through the repulsion-field dynamics produces near-zero updates to the unit-sphere-normalized cell pool. The norm-clamp in `EngineG.__init__` keeps cells on unit sphere; updates after norm projection are effectively absorbed.
2. **h_to_c and c_to_h ARE exercised by cotrain**. Their fro-norm delta from S is 11–16% (vs 18–23% for arbitrary control transformer layers). The cotrain ratio is meaningful but slightly less than typical transformer layers — consistent with these projections feeding a stochastic cell-dynamics path that does propagate gradients.
3. **The cotrain weight-space signature is concentrated in projections, not the cell pool itself**. This refines the hypothesis: cotrain exercises the *interface* between hidden state and consciousness substrate, but the substrate's own state representation (cell pool) is structurally protected by unit-sphere normalization.

## v2 path (C/D/E) — paradigm-effect
v2 has no cell_pool / c_to_h / h_to_c tensors (engine_g is dual-FFN twin). Comparing weight statistics across C/D/E:

| tensor | C cells64 (50k steps) | D cells128 (35k steps) | E convo_5k FT |
|---|---|---|---|
| tok_emb effective_rank | 131 | 22.3 | 9.29 |
| tok_emb stable_rank | 7.13 | 2.28 | 1.62 |
| blocks.0.ffn.engine_g.0.w eff_rank | 315 | 11.5 | 148 |
| blocks.0.ffn.engine_g.0.w stable_rank | 25.6 | 2.15 | 12.3 |
| blocks.5.ffn.engine_g.3.w stable_rank | 7.02 | 1.15 | 16.2 |
| blocks.0 kurtosis (engine_g.0) | -0.005 | -1.28 | 0.43 |

Findings:
- **C (cells64, 50k steps)** has the most random-like spectrum (high eff_rank) — cells64 trained healthily without rank collapse.
- **D (cells128, 35k steps)** shows severe rank collapse on FFN (eff_rank 11.5, stable_rank 2.15, mp_ratio 8–12×). Heavy negative kurtosis (-1.28) indicates platykurtic distribution (bimodal/saturated). This suggests cells128 either over-trained, suffered mitosis-induced gradient pathology, or hit some saturation regime not present in cells64.
- **E (convo_5k FT)** restored rank in the *middle* layers but **collapsed tok_emb** (eff_rank 9.29, stable_rank 1.62) — convo FT pulled embedding into a low-rank chat-domain manifold, while structurally enriching the FFN paths (kurtosis went from negative back to positive 0.43–0.68).

These v2 patterns are **paradigm-orthogonal** to A/B's cell-pool question — useful for cross-validation but not a direct test of cotrain-exercise.

## Cosine to random_init seed=42 baseline
For 350M ckpts, random_init draws a fresh tensor from N(0, 0.02). Cosine to this random reference is ~0 across the board (-0.007 to +0.001) for both A and B. This is the expected null: training pulls weights along a *specific* direction, and an unaligned random sample is nearly orthogonal to a high-dimensional trained tensor. This is consistent with both ckpts being *trained* (not random-init), but does not differentiate A from B by itself.

The discriminating signal is **A vs B alignment** (above), not cosine-to-random.

## Verdict on §47 cotrain-exercise hypothesis
- **Strong form** ("cotrain exercises the consciousness substrate at the cell-pool level"): **REJECTED**. cell_pool_init weight delta is 4× smaller than the BG-LA scratch-retrain delta on the same parameter, despite cotrain having 6000 steps of explicit chat-loss backward. F-WEIGHT-3 fires.
- **Weak form** ("cotrain exercises the interface projections"): **CONFIRMED at ★★★**. Both h_to_c and c_to_h show measurable, structured weight delta consistent with chat-loss gradient flow.
- **Refined form** (recommended for §48 / §50 ablation): "Cotrain exercises the consciousness↔hidden interface (h_to_c, c_to_h) but does NOT meaningfully update the cell pool itself due to unit-sphere normalization at init. Future runs should either (a) remove the init normalization to allow cell_pool to drift, or (b) explicitly route consciousness-corpus gradients into cell_pool via a non-norm-clamped update path."

## ★ rating contribution
- ★★★ on its own (weight-space discriminator confirmed for projections, falsified for cell_pool, paradigm-orthogonal v2 control included)
- Combined with §50 BG-COTRAIN-EXERCISE-CAUSAL-PROOF ablation (in-flight), if §50 confirms downstream behavior shift driven by h_to_c/c_to_h delta → joint ★★★★ candidate
- ★★★★★ requires: (a) §50 ablation PASS + (b) re-run of cotrain WITHOUT cell_pool norm-clamp showing direct cell_pool exercise

## Files emitted
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/spec.md`
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/audit.py`
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/statistics_per_ckpt.json`
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/cross_substrate_alignment.json`
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/cotrain_isolation.json`
- `/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10/verdict.md`

## Constraints honored
- raw#9: audit.py is local-only (state/ subdir, not training/*.py)
- raw#15 additive: 5 ckpts read-only, in-memory analysis
- own 22: REBORN.md NOT directly appended (dispatcher handles §52 slot)
- own 38: artifacts under state/anima_cell_pool_weight_statistics_2026_05_10/
- own 16: $0 local CPU, ~25s wall
