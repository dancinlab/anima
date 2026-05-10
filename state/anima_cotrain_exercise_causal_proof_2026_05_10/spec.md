# BG-COTRAIN-EXERCISE-CAUSAL-PROOF — spec

> own 14 — V14 mirror multi-seed ablation
> own 16 — $0 local Mac CPU only
> raw#15 additive — both ckpts loaded read-only; in-memory mutation only
> own 22 — REBORN.md direct append BLOCKED (dispatcher §50 slot)
> own 38 — artifacts under state/anima_cotrain_exercise_causal_proof_2026_05_10/

## §0 mission

§47 V14_POLARITY_FALSIFIED post-hoc hypothesis: **cotrain-exercise** —
Phase 2 chat-cotrain (w=0.3→0.5 KO chat dual loss) over 6K steps *exercises*
the engine_g cell-pool / c_to_h / h_to_c projections, producing a richer
mitosis substrate than naive BG-LA pretrain. Test via 3 evidence streams:

1. weight-space statistics (L2 / rank / sparsity / cos-sim)
2. forward-pass diversity (variance / pairwise cos / eff-dim of c_to_h(hidden_mean))
3. ablation — replace c_to_h, h_to_c, cell_pool_init with random_init and re-run V14

## §1 substrates

| sym | role | ckpt | source |
|---|---|---|---|
| A  | Phase 2 cotrain (V14_PASS) | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | §38 (anima_phase_2_cotrain_2026_05_09) 597.6 MB / 298.76 M |
| B  | BG-LA pretrain (V14_VIOLATED) | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | §47 BG-LA 12K-step pretrain pod 4wxx2wvcvgjp88 |
| R  | random_init seed=42 (preset la_350m) | in-memory `load_random_init` | engine_a_g_arch.py |

Same arch (engine_a_g_dual_350m_v1, d=1024, 24L, GQA, c_dim=64, n_cells=16) — only weights differ.

## §2 verdict criteria

- **PROVEN** ★★★★★ → F1 PASS (weight stats differ) AND F2 PASS (ablation V14 polarity flips)
- **CORRELATIONAL** ★★★★ → F1 PASS (weight stats differ) BUT F2 FALSIFIED (no polarity flip)
- **FALSIFIED** → F1 FALSIFIED (no weight differences)

## §3 falsifiers (pre-registered)

- F-COTRAIN-EXERCISE-1: weight stats — A vs B fail to differ on ≥2 of 3 targets
  (rel_l2 ≤ 1% AND cos(A,B) ≥ 0.99 on all)
- F-COTRAIN-EXERCISE-2: ablation — none of {ABL1 c_to_h-rand, ABL2 h_to_c-rand,
  ABL3 both-rand, ABL4 pool-rand} flips V14 verdict from baseline
- F-COTRAIN-EXERCISE-3: fwd diversity — A's c_to_h(hm) effective_dim ≤ B's AND
  A's avg pairwise cos ≥ B's

## §4 fire keyword

AUTO ($0 local CPU)
