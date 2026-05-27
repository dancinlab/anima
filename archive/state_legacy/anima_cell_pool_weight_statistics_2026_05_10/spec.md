# BG-CELL-POOL-WEIGHT-STATISTICS — spec

## Mission
Phase 2 cotrain-exercise hypothesis (§47): chat-loss backward pass during cotrain
exercises `engine_g.cell_pool_init` / `engine_g.c_to_h` / `engine_g.h_to_c`
projections. Detect statistically distinguishable weight signature vs. random_init
and vs. pre-cotrain substrate.

## 5 ckpts audited
| Code | Path | Arch | Substrate origin |
|---|---|---|---|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | engine_a_g_dual 350M (24L 1024d, n_cells=16, c_dim=64) | BG-LB step 8000 → cotrain 6000 steps (w=0.3→0.5) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | same | BG-LA scratch pretrain 12000 steps |
| C | `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt` | v2 6L 384d, dual-FFN (engine_a + engine_g), max_cells=64 | scratch step 50000 |
| D | `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells128_step_35000.pt` | v2 6L 384d, dual-FFN, max_cells=128 | scratch step 35000 |
| E | `state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt` | v2 same as C | C-style scratch + convo_5k extended FT |

## Key insight on architecture
- **350M (A,B)** has explicit `engine_g.cell_pool_init` (16,64), `h_to_c` (64,1024), `c_to_h` (1024,64) — physics-style cell pool.
- **v2 (C,D,E)** has NO cell_pool / c_to_h / h_to_c at the weight tensor level. `engine_g` in v2 is a **dual-FFN twin** (two parallel SwiGLU FFN paths, no cell-state pool). This is a paradigm difference; v2 cannot directly test cotrain-exercise hypothesis on cell_pool — only A vs B can.

## Bonus ckpt (substrate isolation)
| Code | Path | Role |
|---|---|---|
| S | `~/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt` | A's pre-cotrain substrate (BG-LB) |

S→A delta = pure cotrain effect; S→B delta = independent BG-LA pretrain control on shared seed=42 init.

## Metrics (per-tensor)
1. norms: L2, L∞, Frobenius
2. sparsity at 1e-3 and 1e-2
3. magnitude distribution: mean, std, skew, excess kurtosis
4. SVD: top-10 singular values, cumulative variance, spectral norm
5. effective rank (entropy of normalized σ²)
6. stable rank (||W||²_F / σ₁²)
7. Marchenko-Pastur deviation (spectral / σ_emp·(1+√c)·√max(m,k))
8. cosine similarity to random_init (seed=42, init_std matched to layer)
9. per-row cosine similarity (mean, std, median)

## Cross-substrate
- A vs B alignment: global cosine, per-row cosine, Hungarian matching, cell-pool entropy, gram off-diagonal
- S→A vs S→B fro-normalized delta (cotrain effect isolation)

## Falsifiers
- F-WEIGHT-1: A vs B weight statistics 차이 부재
- F-WEIGHT-2: random_init vs all trained 차이 부재
- F-WEIGHT-3: cell_pool effective_rank 모든 substrate 동일
