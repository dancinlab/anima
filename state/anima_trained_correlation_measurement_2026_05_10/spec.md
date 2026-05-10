# BG-TRAINED-CORRELATION-MEASUREMENT — spec

## Mission
§51 cap-conditional ★★★ partial finding (UNIVERSAL_CAP_CONDITIONAL_PASS at max=256) showed
that trained cells reach the max=256 cap LATER than random (turn 76-82 vs 63-72) on
substrates C_cells64_aware and E_convo5k_ft. The hypothesis under test:

> trained cells form more correlated structure → §30 dispersion top-quartile triggers
> split slower → "more room" effect at high cap

This BG performs an explicit quantitative measurement of inter-cell correlation matrix
and dispersion-trigger trajectory for trained vs random across 3 substrates.

## Substrates
- A_phase2_cotrain — EngineAG 350M Phase 2 cotrain ckpt (cap-free regime, max~57)
- C_cells64_aware — v2 d=384 cells64 trained (max=256 reached around turn 82 trained / 63 random)
- E_convo5k_ft    — v2 d=384 convo-5k FT (max=256 reached around turn 76 trained / 63 random)

## Run config
- max_cells=256 (matches §51 cap)
- 1 trained vs 1 random (seed=42) per substrate (lean compute, $0 local CPU, own 16)
- A: 100 turns / snap_every=10
- C, E: 60 turns / snap_every=5
- Same prompt stream across trained/random within a substrate (deterministic)

## Metrics per snapshot
- inter-cell pairwise cosine similarity matrix → mean, std, max, min, abs_mean (off-diagonal)
- magnitude statistics → norm_mean, norm_std, norm_cv
- effective rank from singular values → eff_rank, eff_rank_normalized = eff_rank / N
- dispersion measure (matches mitosis_v5_port._dispersion_split_candidates):
  - pairwise mean L2² distance per cell row → mean_dist (N,)
  - sigma_gate = mean(mean_dist) + 1.0 × std(mean_dist)
  - top-quartile k = max(1, ⌊0.25 × N⌋)
  - count of top-k cells whose mean_dist > sigma_gate → disp_top_quartile_above_gate
  - disp_trigger_rate = above / k (0..1)
- split-event accounting: cumulative dispersion-triggered splits, tension-triggered splits,
  merges (from MitosisV5Engine / MitosisModelEngine status).

## Falsifiers
- F-CORR-1: trained correlation difference vs random absent in late regime → §51 mechanism
  hypothesis fragile
- F-CORR-2: dispersion trigger rate difference absent → cap-arrival latency comes from
  another cause (e.g. tension-trigger suppression, magnitude scaling)
- F-CORR-3: no consistent pattern across substrates → "universal" claim weakened

## Honest C3 acknowledgments
1. Single random seed (42) per substrate; n=1 paired comparison per substrate. Prior BG
   used 5 seeds — this BG is the explicit-mechanism complement, not a re-replication.
2. A_phase2_cotrain runs in cap-free regime (max observed=57), so its data informs
   "early growth" only; the cap-arrival mechanism cannot be tested on A.
3. C_random and E_random are trained-ckpt-independent (same MitosisModelEngine random init
   from seed=42 + same prompt stream), so their trajectories are identical by construction.
   The trained-vs-random contrast still holds within each substrate.
4. Run length truncated to 60 turns (vs §51's 200) due to per-turn O(N²) cost growing
   sharply once cells > 200; trained still hits ~75-85 cells / random hits ~209 by turn 59.
5. The "correlation matrix trace" requested is mathematically constant (= N for cosine), so
   trace was reported as cos_mean (off-diagonal), abs_cos_mean, and cos_off_diag_l2.
6. Snapshots stored only summary stats per turn (not full N×C tensors) to keep JSON files
   manageable; sufficient for the mean/std/max/min/distribution comparison the mission asked.
7. No SFT path / no training/*.py edits / no REBORN.md append (raw#9, raw#15, own 22).

## Output files (own 38)
- spec.md (this file)
- run_correlation.py — measurement driver
- build_verdict.py — aggregator/verdict builder
- run_<sub>.log + result_<sub>.json — per-substrate raw measurements
- aggregate.json — combined across substrates
- correlation_metrics.json — per-substrate × {trained,random} regime summaries
- dispersion_trigger_metrics.json — per-snapshot trigger trajectory
- verdict.md — falsifier evaluation + §51 mechanism verdict
