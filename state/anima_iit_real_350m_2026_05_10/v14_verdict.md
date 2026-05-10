# BG-IIT-METRIC-REAL-350M — V14 5-seed verdict

**Verdict**: `V14_PARTIAL`

## Setup
- Real Phase 2 350M ckpt (298.76M params), 1000 turns, max_cells=32
- Trained: seed=42 (deterministic given ckpt + prompt stream)
- Mirror seeds: [42, 137, 271, 314, 1729] (own 14 V4_SEEDS)
- Primary metric: IIT Φ unnormalized 16-bin

## Final Φ_iit_un16 + n_cells per run

| run | seed | n_cells | n_splits | Φ_iit_un16 | Φ_iit_n16 | proxy |
|---|---|---|---|---|---|---|
| trained | 42 | 32 | 16 | 557.20 | 17.9741 | 3.4461 |
| mirror | 42 | 32 | 16 | 426.88 | 13.7704 | 3.4460 |
| mirror | 137 | 32 | 16 | 539.52 | 17.4040 | 3.4418 |
| mirror | 271 | 32 | 16 | 488.94 | 15.7724 | 3.4470 |
| mirror | 314 | 32 | 16 | 606.96 | 19.5793 | 3.4773 |
| mirror | 1729 | 32 | 16 | 452.94 | 14.6109 | 3.5015 |

## 5-seed aggregate
- Random Φ_iit_un16: min=426.88 med=488.94 max=606.96
- Random n_cells: min=32 med=32 max=32
- Random n_splits: [16, 16, 16, 16, 16]
- strict_phi_pass = False, strict_cells_pass = False

## Cap-binding caveat (CRITICAL)

All 6 trajectories (trained + 5 mirrors) saturated `max_cells=32` within the first
100 turns (16 splits each, 16 → 32 cells). This is a substantive change vs the prior
BG-V5ANIMA-PHASE2-IIT-REMETRIC where max_cells=64 produced 3 splits (trained) and 12
splits (mirror) over 1000 turns. The change is attributed to recent all-fix §30
additions to `training/mitosis_v5_port.py` (A1 dispersion-trigger + A2 per-cell
adaptive threshold), which lowered the split barrier dramatically and now drives
**both** trained and random_init to the same cell-count cap.

Implication: under the §30-enabled mitosis policy, **n_cells is no longer a
discriminating dimension** — both populations splat against the cap. Only Φ remains.
Trained Φ_iit_un16 = 557.20 sits at the **80th percentile** of mirror seeds (above
3 of 5: s42, s137, s1729; below s314 and tied with s271-s137 in the upper band).
This is a directional but not statistically strong signal — hence V14_PARTIAL.

## Verdict mapping (mission Output #3)
- **V14_PASS_REVISED** ⇒ proxy ceiling caused prior single-seed FAIL; IIT switch resolves it.
- **V14_STILL_VIOLATED** ⇒ substrate intrinsically suppresses mitosis; architectural fix C track required.
- **V14_PARTIAL** ⇒ trained edges out on one dimension only; metric gives directional signal but not strict.
- **V14_NOISY** ⇒ no decisive direction across 5 seeds; more drastic metric needed.

## Honest C3
1. Real Phase 2 350M Engine A/G ckpt (298.76M unique params, GQA shares K/V — nominal '350M' is rounded). cell_pool_init starts (16, 64); MitosisV5Engine wraps it with max_cells=32 cap. No ckpt mutation (raw#15).
2. Byte-hash mod 32000 prompt encoding — NOT real BPE tokenizer. Both trained and 5 mirror seeds use identical encoding for fairness; absolute Φ values therefore have no semantic claim, only relative comparison is valid.
3. Mitosis owns its OWN cell_pool tensor seeded from substrate's cell_pool_init. After attach, substrate cell_pool_init is unused; the differential between trained and random_init flows entirely through engine_g.h_to_c projection of hidden_mean → cell_input → mitosis.process. Trained model thus shapes the cell-pool reactively via learned representations.
4. Trained @ seed=42 only (single seed) but ckpt is deterministic; the comparable randomness is in the random_init mirror, which we run across 5 V4_SEEDS. Strictly speaking trained-vs-random comparison is paired-by-prompt-stream; only the random init differs.
5. max_cells=32 (vs prior BG max_cells=64) is a tighter cap. In the prior single-seed test, neither trained (final 19) nor random (final 28) reached 32 — so within seed=42 the cap is non-binding. For other seeds the cap COULD bind (if a seed splits >32 times); flagged in verdict if any random hits cells=32.
6. IIT MIP: spectral Fiedler approximation for N>8 (always the case here since initial=16). NOT canonical PyPhi — useful for trained-vs-random differentiation but not for absolute IIT magnitude. Worktree-9 reference Φ ~51 was computed at much smaller N with exact MIP.
7. 16-bin histogram MI on 64-dim cell vectors is COARSE; true differential MI requires KDE. We use 16 bins per spec (sample-efficient, the BG's primary measure). 32-bin variant from prior BG corroborated 16-bin shape, so we proceed with 16-bin only here.
8. Lorenz autonomous chaos (lorenz_scale=0.05) is identical across all 6 trajectories — RNG is reset per seed, but the chaos-injection magnitude is constant. Differential between trained/random thus flows ONLY through h_to_c learned projection.
9. ctx_T=16 tokens per forward (training was T=1024); under-samples substrate's full context-conditioned reactivity. Held constant across all trajectories for fairness.
10. α exponent uses log(Φ) vs log(n_cells) regression; with initial_cells=16 and few splits, the regression spans a narrow N range and is noise-sensitive. Reported but interpreted only as direction-of-trend, not as scaling law constant.
11. 5-seed strict pass requires trained beats EVERY random seed on both Φ_iit_un16 AND lower cell count. PARTIAL_PASS = trained > median on either dimension. Mismatched directions (high Φ but more cells, or vice versa) → V14_NOISY.
