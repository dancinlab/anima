# BG-V14-STRICT-RESOLUTION — V14 strict 10-seed verdict

**Verdict**: `V14_STRICT_PASS`

## Setup
- Real Phase 2 350M ckpt (298.76M params), 400 turns, max_cells=128 (4× §33)
- Trained: prompt_seed=42 (deterministic given ckpt + prompt stream)
- Mirror seeds (n=10): [42, 137, 271, 314, 1729, 2718, 3141, 5772, 6022, 9192]
- Primary metric: IIT Φ unnormalized 16-bin (Fiedler MIP, byte-hash prompts)

## Final Φ_iit_un16 + n_cells per run

| run | seed | n_cells | n_splits | cap_bound | Φ_iit_un16 | Φ_iit_n16 | proxy |
|---|---|---|---|---|---|---|---|
| trained | 42 | 85 | 69 | 0 | 5244.07 | 62.4294 | 4.4527 |
| mirror | 42 | 80 | 64 | 0 | 4749.79 | 60.1240 | 4.3908 |
| mirror | 137 | 55 | 39 | 0 | 2002.94 | 37.0915 | 4.0423 |
| mirror | 271 | 69 | 53 | 0 | 3569.75 | 52.4963 | 4.2364 |
| mirror | 314 | 68 | 52 | 0 | 3412.37 | 50.9309 | 4.2265 |
| mirror | 1729 | 65 | 49 | 0 | 2113.97 | 33.0308 | 4.1867 |
| mirror | 2718 | 66 | 50 | 0 | 3235.07 | 49.7703 | 4.2067 |
| mirror | 3141 | 78 | 62 | 0 | 4399.14 | 57.1316 | 4.3666 |
| mirror | 5772 | 65 | 49 | 0 | 2750.09 | 42.9702 | 4.2160 |
| mirror | 6022 | 71 | 55 | 0 | 3593.50 | 51.3357 | 4.2832 |
| mirror | 9192 | 54 | 38 | 0 | 1226.88 | 23.1487 | 4.0131 |

## 10-seed aggregate
- trained beats random Φ: 10/10 (100%) (ties=0, losses=0)
- sign-test p (two-sided): 0.0020
- Mann-Whitney 1-vs-10: U=10, rank=11/11, p_one_sided=0.0909, p_two_sided=0.1818
- random Φ_iit_un16: min=1226.88 med=3412.37 max=4749.79
- random n_cells: min=54 med=68 max=80
- random n_splits: [64, 39, 53, 52, 49, 50, 62, 49, 55, 38]
- random cap_bound_turns: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
- cap_bound_universal (F-V14-STRICT-2): False
- cell_count discrim: trained<rand=0/10, trained>rand=10/10

## Verdict bins
- **V14_STRICT_PASS**:        trained > ALL 10 random Φ → binomial p≈0.001
- **V14_STRICT_PARTIAL**:     trained > 9/10 random + sign-test p<0.10
- **V14_PARTIAL_CONFIRMED**:  trained > 7-8/10 random + sign-test p<0.20
- **V14_VIOLATED_REVISED**:   trained > random < 75%

## Honest C3
1. Real Phase 2 350M Engine A/G ckpt (298.76M unique params; GQA-shared K/V — 'nominal 350M' rounded). cell_pool_init starts (16, 64); MitosisV5Engine wraps it with max_cells=128 cap (4× §33). raw#15 honored: ckpt unmodified.
2. Byte-hash mod 32000 prompt encoding — NOT real BPE tokenizer. trained and 10 random_init mirror seeds use identical encoding for fairness; absolute Φ values therefore have no semantic claim, only relative comparison is valid.
3. MitosisV5Engine §30 all-fix in force (A1 dispersion-trigger top-quartile; A2 per-cell adaptive threshold mean+1.5σ over 100-step window; B1 phi_per_cell ratchet; D1 Lorenz auto-calibration). All 11 trajectories use these unchanged. raw#9 + own 38: not edited here.
4. Trained @ prompt_seed=42 only (single deterministic ckpt → one shot). Random mirror runs n=10 seeds {42,137,271,314,1729,2718,3141,5772,6022,9192}. The 10-seed extension permits binomial bound: 10/10 → p≈0.001; 9/10 → p≈0.022; 7/10 → p≈0.34 (two-sided).
5. max_cells=128 vs §33's 32 explicitly diagnoses F-V14-STRICT-2: if cap_bound_turns ≈ n_turns on every seed, §30 fix is universally too aggressive (NOT trained-vs-random differentiated). cap_bound_turns reported per-trajectory.
6. IIT MIP: spectral Fiedler approximation for N>8 (always). NOT canonical PyPhi. Useful for trained-vs-random direction, NOT for absolute IIT magnitude. 16-bin histogram MI on 64-dim cell vectors is COARSE; true differential MI requires KDE.
7. Lorenz autonomous chaos (lorenz_scale=0.05 base, D1 auto-calibrated by mean L2-norm of cells) is identical scale across all 11 trajectories — RNG resets per seed, but the chaos-injection magnitude is constant. Differential between trained/random flows ONLY through the h_to_c learned projection of hidden_mean → cell_input.
8. ctx_T=16 tokens per forward (training was T=1024); under-samples substrate's full context-conditioned reactivity. Held constant across all trajectories for fairness.
9. Sign test (binomial) is the primary statistic since the comparison is paired-by-prompt-stream and only random-init differs. Mann-Whitney U with n1=1, n2=10 reduces to rank-of-trained-in-pool — reported as auxiliary.
10. α exponent (log-log Φ vs n_cells) regression spans wider N range here (max=128 vs §33's 32) — interpretation should still be treated as direction-of-trend rather than scaling-law constant; few-snapshot regression remains noise-sensitive.
11. Verdict bins (strict/strict_partial/partial_confirmed/violated_revised) are pre-registered before run (own 22 honest emit). The transition between bins is determined by the data; no post-hoc adjustment.
