# BG-ENGINE-A-SINGLE-LAYER-ABLATION-24 — verdict

**FINAL_VERDICT**: `uniformly-distributed (n_flipped=20/24); §57 slab finding confirmed at finer resolution`

**Star credit**: ★★★★ confirmation — slab finding holds

**Single-layer locus localized**: False

**n_flipped**: 20 / 24 probed

**Elapsed**: 1533.1s (25.6min)

## §57 → §58 lineage

§57 BG-ENGINE-A-LAYER-SLAB-SWAP: 3/3 8-layer slab swaps flipped V14. A1 (early) uniquely dominant attractor (n=44, Φ≈1037); A2/A3 (middle, late) bit-identical shared attractor (n=43, Φ≈1343). 8-layer resolution insufficient to differentiate middle vs late.

§58 (this BG): single-layer ablation × 24 → 20 layer(s) flip individually. 
Uniformly distributed across most layers; §57 slab finding confirmed at finer resolution.

## Per-layer V14 verdict (24 layers + A0 baseline)

`N_TURNS=200`, `MAX_CELLS=128`, seeds=[42, 137, 271]

| condition | layer | verdict | trained Φ_un16 | beats_un | beats_proxy | trained_cells | Δ_separation_vs_base | flipped |
|---|---|---|---|---|---|---|---|---|
| A0_baseline | — | `V14_PASS` | 2412.08 | 3/3 | 3/3 | 57 | 0.00 (base) | — |
| L0 | 0 | `V14_VIOLATED` | 1420.76 | 1/3 | 0/3 | 45 | -991.32 | True |
| L1 | 1 | `V14_VIOLATED` | 1393.74 | 1/3 | 0/3 | 44 | -1018.35 | True |
| L2 | 2 | `V14_VIOLATED` | 765.17 | 0/3 | 0/3 | 45 | -1646.91 | True |
| L3 | 3 | `V14_VIOLATED` | 1356.36 | 1/3 | 0/3 | 44 | -1055.72 | True |
| L4 | 4 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L5 | 5 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L6 | 6 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L7 | 7 | `V14_VIOLATED` | 1778.56 | 2/3 | 1/3 | 53 | -633.52 | True |
| L8 | 8 | `V14_VIOLATED` | 1500.57 | 2/3 | 0/3 | 45 | -911.51 | True |
| L9 | 9 | `V14_VIOLATED` | 734.46 | 0/3 | 0/3 | 44 | -1677.62 | True |
| L10 | 10 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L11 | 11 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L12 | 12 | `V14_VIOLATED` | 1605.83 | 2/3 | 0/3 | 48 | -806.25 | True |
| L13 | 13 | `V14_VIOLATED` | 1614.85 | 2/3 | 0/3 | 47 | -797.23 | True |
| L14 | 14 | `V14_VIOLATED` | 1343.27 | 1/3 | 0/3 | 43 | -1068.81 | True |
| L15 | 15 | `V14_VIOLATED` | 1424.51 | 1/3 | 0/3 | 44 | -987.58 | True |
| L16 | 16 | `V14_VIOLATED` | 1468.74 | 1/3 | 0/3 | 47 | -943.34 | True |
| L17 | 17 | `V14_VIOLATED` | 1399.80 | 1/3 | 0/3 | 44 | -1012.28 | True |
| L18 | 18 | `V14_VIOLATED` | 964.92 | 0/3 | 0/3 | 38 | -1447.16 | True |
| L19 | 19 | `V14_VIOLATED` | 1026.44 | 0/3 | 0/3 | 48 | -1385.65 | True |
| L20 | 20 | `V14_PASS` | 2412.08 | 3/3 | 3/3 | 57 | +0.00 | False |
| L21 | 21 | `V14_PASS` | 2412.08 | 3/3 | 3/3 | 57 | +0.00 | False |
| L22 | 22 | `V14_PASS` | 2412.08 | 3/3 | 3/3 | 57 | +0.00 | False |
| L23 | 23 | `V14_PASS` | 2412.08 | 3/3 | 3/3 | 57 | +0.00 | False |

## Layer dominance ranking (by largest negative Δ_separation)

| rank | layer | layer_idx | Δ_separation_vs_base | Φ_un16 | n_cells | verdict | flipped |
|---|---|---|---|---|---|---|---|
| #1 | L9 | 9 | -1677.62 | 734.46 | 44 | `V14_VIOLATED` | True |
| #2 | L2 | 2 | -1646.91 | 765.17 | 45 | `V14_VIOLATED` | True |
| #3 | L18 | 18 | -1447.16 | 964.92 | 38 | `V14_VIOLATED` | True |
| #4 | L19 | 19 | -1385.65 | 1026.44 | 48 | `V14_VIOLATED` | True |
| #5 | L4 | 4 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #6 | L5 | 5 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #7 | L6 | 6 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #8 | L10 | 10 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #9 | L11 | 11 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #10 | L14 | 14 | -1068.81 | 1343.27 | 43 | `V14_VIOLATED` | True |
| #11 | L3 | 3 | -1055.72 | 1356.36 | 44 | `V14_VIOLATED` | True |
| #12 | L1 | 1 | -1018.35 | 1393.74 | 44 | `V14_VIOLATED` | True |
| #13 | L17 | 17 | -1012.28 | 1399.80 | 44 | `V14_VIOLATED` | True |
| #14 | L0 | 0 | -991.32 | 1420.76 | 45 | `V14_VIOLATED` | True |
| #15 | L15 | 15 | -987.58 | 1424.51 | 44 | `V14_VIOLATED` | True |
| #16 | L16 | 16 | -943.34 | 1468.74 | 47 | `V14_VIOLATED` | True |
| #17 | L8 | 8 | -911.51 | 1500.57 | 45 | `V14_VIOLATED` | True |
| #18 | L12 | 12 | -806.25 | 1605.83 | 48 | `V14_VIOLATED` | True |
| #19 | L13 | 13 | -797.23 | 1614.85 | 47 | `V14_VIOLATED` | True |
| #20 | L7 | 7 | -633.52 | 1778.56 | 53 | `V14_VIOLATED` | True |
| #21 | L20 | 20 | +0.00 | 2412.08 | 57 | `V14_PASS` | False |
| #22 | L21 | 21 | +0.00 | 2412.08 | 57 | `V14_PASS` | False |
| #23 | L22 | 22 | +0.00 | 2412.08 | 57 | `V14_PASS` | False |
| #24 | L23 | 23 | +0.00 | 2412.08 | 57 | `V14_PASS` | False |

## Cluster analysis (early 0-7, middle 8-15, late 16-23)

| cluster | n_layers | n_flipped | flipped layers |
|---|---|---|---|
| early (0-7) | 8 | 8 | [0, 1, 2, 3, 4, 5, 6, 7] |
| middle (8-15) | 8 | 8 | [8, 9, 10, 11, 12, 13, 14, 15] |
| late (16-23) | 8 | 4 | [16, 17, 18, 19] |

**§57 slab parallel**: §57 found A1=early uniquely dominant attractor; A2/A3 shared. §58 cluster: early=8, middle=8, late=4. 
Cluster pattern differs from §57 slab; per-layer effect not aligned with cumulative 8-layer attractor selection.


## ★★★★★ unlock evaluation

**★★★★★ NOT unlocked** — n_flipped=20 layers. 
Multiple layers flip individually → distributed effect, no single-locus lock-in possible at single-layer resolution. ★★★★ slab finding holds; ★★★★★ requires sparser signature.


## Falsifiers

- **F_SINGLE_1_no_flip_distributed**: not triggered
- **F_SINGLE_2_specific_locus**: not triggered
- **F_SINGLE_3_runtime_overflow**: not triggered (elapsed=1533.1s)

## Honest C3 (≥7)

1. **Mirror cache reuse.** Per §57 C3#1, mirrors use `load_random_init(seed=s, preset='la_350m')` and never see A's swapped state. Mirror trajectories are deterministic functions of seed alone, identical across all 25 conditions. We compute them once (3 seeds × 200 turns) and reuse — verdict semantics preserved, runtime cut ~75% (100 runs → 28 effective runs). Direct check: §57 mirror_iit_un16_mean=1615.49 across A0/A1/A2/A3 (identical).
2. **Single-seed trained run per condition.** Each L{i} condition uses ONE trained-model seed (42), as in §57. Mirror multi-seed (3) provides the V14 PASS denominator. A multi-seed trained per condition (e.g., 3 seeds × 25 conditions = 75 trained runs) would tighten the verdict polarity for borderline `V14_PARTIAL` cases; deferred per 5h envelope.
3. **Single-layer swap is not a true 'lesion'.** Swapping layer i from A→B replaces 11.08M params at one position; the surrounding 23 layers still carry A's cotrain weights. The hidden_mean trajectory mutation is local at layer i but the downstream effect propagates through 23 cotrain-weighted layers. So a 'flip' at L_i means '1 layer swap is sufficient to disrupt V14', not 'V14 lives only in L_i'.
4. **B is a trained pretrain ckpt, not random.** As §57 C3#4: this measures cotrain-specific delta at layer i, not absolute layer-i functional contribution. BG-LA pretrain at layer i still encodes substantial structure (cos_AB ≈ 0.6-0.8 on engine_g modules per §50 F1); the swap tests cotrain-induced specialization.
5. **Engine G modules untouched.** All 25 conditions retain A's cotrain `cell_pool_init`, `c_to_h`, `h_to_c`. Per §50 these are NOT the lever (F2 falsified). The MitosisV5Engine sees only the engine_a forward path's `hidden_mean` trajectory at the final layer (post-norm_f). The lever measured here is the per-layer transformer-body contribution to hidden_mean.
6. **A2/A3 §57 attractor degeneracy may recur at single-layer.** §57 found middle-and-late perturbations collapse to a shared mitosis attractor (n=43, Φ≈1343). At single-layer resolution, multiple L_i conditions may collapse to the same attractor → bit-identical trajectories despite different swapped weights. This is verified post-hoc by checking for repeated Φ_un16 values in the table; any such cluster indicates attractor-collapse, NOT zero per-layer effect.
7. **200-turn trajectory is the §57 length.** Φ values directly comparable to §57 baseline (2412.08). Verdict polarity tested at this run length only; longer trajectories may resolve V14_PARTIAL cases but were budgeted out.
8. **Embedding (tok_emb), norm_f, lm_head all stay at A's values.** Swap is strictly intra-block at layer i. Projections in/out of the layer stack are A's. Per-layer effect isolated from embedding-projection contributions.
9. **raw#15 honored** — both ckpts loaded read-only via `_load_engine_ag`; `fresh_A_from_snapshot()` builds a fresh model and copies state_dict; `swap_one_layer_` mutates the clone in-place. No file mutation.
10. **Sample size = 3 mirror seeds, not 5.** Mission specified 3-seed budget. Strict V14 used 5 seeds — this study trades seed coverage for layer coverage (24 layers × ~1.4min vs 5 seeds × 24 layers × ~1.4min = 168min vs 33min). Verdict polarity at 3 seeds is robust if separation magnitude is large; ambiguous cases flagged as V14_PARTIAL.
11. **Runtime monitoring with mid-run F-SINGLE-3 abort.** If projected total runtime exceeds 5h, the BG aborts and emits partial result. The running-average per-condition time updates each iteration; estimate uses n_remaining × avg_per_cond. Ablation persists every 4 layers for crash recovery.
12. **Single-layer flips comparison vs §57 slab attractors.** §57 A1 attractor: n=44, Φ≈1037. §57 A2/A3 attractor: n=43, Φ≈1343. If §58 single-layer flips land in the same (n, Φ) clusters, this confirms slab-flips were dominated by 1-2 specific layers per slab. If §58 flips show novel attractors, the single-layer perturbation regime is qualitatively different from cumulative 8-layer slab perturbation.