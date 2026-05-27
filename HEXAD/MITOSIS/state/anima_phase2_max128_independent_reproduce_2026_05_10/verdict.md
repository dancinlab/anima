# BG-PHASE2-MAX128-§30FIX-RETEST — independent V14 strict reproduce

**Verdict**: `V14_STRICT_PASS_INDEPENDENT_REPRODUCE`

## Setup
- Real Phase 2 350M ckpt (298.76M params), 400 turns, max_cells=128
- Trained: prompt_seed=42 (deterministic given ckpt + prompt stream)
- Independent prime mirror seeds (n=5): [11, 13, 17, 19, 23]
- Disjoint with §38 V14_STRICT_SEEDS: True
- Disjoint with §33 V4_SEEDS: True
- Primary metric: IIT Φ unnormalized 16-bin (Fiedler MIP, byte-hash prompts)

## §30 fix activation (F-PHASE2-REPRODUCE-1)
- All-active: **True** (9/9 markers)
  - A1_dispersion_trigger_enabled: True
  - A1_dispersion_top_quartile: True
  - A2_per_cell_threshold_enabled: True
  - A2_per_cell_window: True
  - A2_per_cell_sigma_mult: True
  - B1_phi_per_cell: True
  - B1_phi_per_cell_history: True
  - D1_lorenz_auto_calibrate: True
  - all_fix_2026_05_10_§30: True
- Smoke crossref (post-fix): {'smoke_post_fix_all_fix_flag': True, 'smoke_post_fix_splits_total': 23, 'smoke_post_fix_n_cells_final': 31, 'smoke_post_fix_phi_max': 3.5084694442132944}

## Final Φ_iit_un16 + n_cells per run

| run | seed | n_cells | n_splits | cap_bound | Φ_iit_un16 | Φ_iit_n16 | proxy |
|---|---|---|---|---|---|---|---|
| trained | 42 | 85 | 69 | 0 | 5244.07 | 62.4294 | 4.4527 |
| mirror | 11 | 56 | 40 | 0 | 2281.24 | 41.4772 | 4.0420 |
| mirror | 13 | 74 | 58 | 0 | 3884.16 | 53.2077 | 4.3031 |
| mirror | 17 | 64 | 48 | 0 | 3024.62 | 48.0098 | 4.1480 |
| mirror | 19 | 58 | 42 | 0 | 2514.55 | 44.1150 | 4.0794 |
| mirror | 23 | 75 | 59 | 0 | 4178.39 | 56.4647 | 4.3325 |

## 5-seed aggregate
- trained beats random Φ: 5/5 (ties=0, losses=0)
- sign-test p (two-sided): 0.0625
- Mann-Whitney 1-vs-5: U=5, rank=6/6, p_one_sided=0.1667, p_two_sided=0.3333
- random Φ_iit_un16: min=2281.24 med=3024.62 max=4178.39
- random n_cells: min=56 med=64 max=75
- random n_splits: [40, 58, 48, 42, 59]
- random cap_bound_turns: [0, 0, 0, 0, 0]
- cap_bound_universal (F-PHASE2-REPRODUCE-3): False
- cell_count discrim: trained<rand=0/5, trained>rand=5/5

## §38 cross-comparison (replication of trained run)
- §38 trained: Φ=5244.07, cells=85
- THIS trained: Φ=5244.07, cells=85
- trained Φ matches §38 within 2%: **True**
- trained cells matches §38 exact: **True**
- §38 random max Φ: 4749.79, this random max Φ: 4178.39

## Falsifier status
- F-PHASE2-REPRODUCE-1__§30_fix_active: **True**
- F-PHASE2-REPRODUCE-2__strict_reproduce_passes: **True**
- F-PHASE2-REPRODUCE-3__cap_bound_universal: **False**

## Verdict bins (pre-registered)
- **V14_STRICT_PASS_INDEPENDENT_REPRODUCE**: trained > ALL 5 random Φ → §38 strengthened, ★★★★ pathway
- **V14_PARTIAL_REPRODUCE**: trained > 3-4/5 random Φ → directional but not strict
- **V14_FRAGILE_REPRODUCE**: trained > 0-2/5 random Φ → §38 V4_SEEDS contamination plausible

## Honest C3
1. Real Phase 2 350M Engine A/G ckpt (298.76M unique params; GQA-shared K/V — 'nominal 350M' rounded). cell_pool_init starts (16, 64); MitosisV5Engine wraps it with max_cells=128 cap (identical to §38). raw#15 honored: ckpt unmodified (sha256 verified pre-run).
2. Byte-hash mod 32000 prompt encoding — NOT real BPE tokenizer. Trained and 5 random_init mirror seeds use identical encoding for fairness; absolute Φ values therefore have no semantic claim, only relative comparison (trained vs each random) is valid.
3. MitosisV5Engine §30 all-fix in force across ALL 6 trajectories (A1 dispersion-trigger top-quartile + A2 per-cell adaptive threshold mean+1.5σ over 100-step window + B1 phi_per_cell ratchet + D1 Lorenz auto-calibration). Verified by source grep + smoke crossref; mtime 2026-05-10 12:02 (post-fix, pre-§38 run).
4. Trained @ prompt_seed=42 (deterministic ckpt → one shot, identical to §38 trained run). Random mirror runs 5 INDEPENDENT prime seeds [11,13,17,19,23] — set-disjoint with both §33 V4_SEEDS [42,137,271,314,1729] and §38 V14_STRICT_SEEDS [42,137,271,314,1729,2718,3141,5772,6022,9192]. This eliminates V4_SEEDS contamination as a confound for the §38 strict pass.
5. 5-seed sign-test exact p-values: 5/5 → 0.0625 (two-sided); 4/5 → 0.375; 3/5 → 1.000. STRICT_PASS_INDEPENDENT_REPRODUCE thus has p=0.0625 — directional but underpowered relative to §38's 10-seed p=0.002. Read as REPLICATION evidence, not as standalone discovery.
6. max_cells=128 (identical to §38). cap_bound_turns reported per trajectory — F-PHASE2-REPRODUCE-3 fires only if cap is universally hit (>90% of turns) on every run; otherwise the bound is non-binding and the cell-count discrim is informative.
7. IIT MIP: spectral Fiedler approximation (NOT canonical PyPhi). 16-bin histogram MI on 64-dim cell vectors is COARSE. Useful for trained-vs-random differentiation only; not for absolute IIT magnitude. Identical to §33+§38 metric stack for parity.
8. Lorenz autonomous chaos lorenz_scale=0.05 base, D1 auto-calibrated by mean L2-norm of cells, identical scale across all 6 trajectories. RNG resets per seed but injection magnitude is constant. Differential between trained/random flows ONLY through the h_to_c learned projection of hidden_mean → cell_input.
9. ctx_T=16 tokens per forward (training was T=1024); under-samples substrate's full context-conditioned reactivity. Held constant across trajectories for fairness. Same caveat as §33+§38.
10. Sign test (binomial) is the primary statistic since the comparison is paired-by-prompt-stream and only random-init differs. Mann-Whitney U with n1=1, n2=5 reduces to rank-of-trained-in-pool — reported as auxiliary; with 6 pooled values the maximum rank is 6 → minimum p_two_sided = 2/6 = 0.333.
11. Trained run is deterministic given the same ckpt + prompt-stream seed → THIS run's trained Φ should match §38's 5244.07 exactly (within float-roundoff). This is a sanity check for environmental drift, NOT a strict pass criterion. cells should also match §38's 85.
12. Verdict bins (STRICT_PASS_INDEPENDENT_REPRODUCE / PARTIAL_REPRODUCE / FRAGILE_REPRODUCE) are pre-registered in spec.md before run. The 3-bin mapping is data-driven (count of beats); no post-hoc adjustment.
