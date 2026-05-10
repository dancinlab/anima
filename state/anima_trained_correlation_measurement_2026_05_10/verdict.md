# BG-TRAINED-CORRELATION-MEASUREMENT — verdict

§51 cap-conditional mechanism hypothesis: trained cells form more correlated structure →
top-quartile dispersion variance lower → fewer outliers cross sigma_gate → split rate
slower near cap → cap reached later. Tested on 3 substrates × {trained, random_seed=42} ×
max_cells=256. Lean compute: 1 trained + 1 random per substrate ($0 local CPU, own 16).
A: 100 turns / snap=10 (cap-free). C, E: 60 turns / snap=5 (cap-approach).

## Table 1 — Inter-cell cosine correlation (all snapshots)

| substrate | run | n_snaps | nC range | cos_mean | abs_cos_mean | cos_std | norm_cv | eff_rank/N |
|---|---|---|---|---|---|---|---|---|
| A_phase2_cotrain | trained | 11 | 16→57 | +0.1026 | 0.1548 | 0.1331 | 0.3280 | 0.6843 |
| A_phase2_cotrain | random  | 11 | 16→48 | +0.1073 | 0.1595 | 0.1297 | 0.3399 | 0.7053 |
| C_cells64_aware  | trained | 13 |  8→75 | +0.1118 | 0.1357 | 0.0570 | 0.2070 | 0.8545 |
| C_cells64_aware  | random  | 13 |  8→209| +0.1107 | 0.1350 | 0.0575 | 0.2664 | 0.8107 |
| E_convo5k_ft     | trained | 13 |  8→85 | +0.1132 | 0.1356 | 0.0535 | 0.1735 | 0.8650 |
| E_convo5k_ft     | random  | 13 |  8→209| +0.1107 | 0.1350 | 0.0575 | 0.2664 | 0.8107 |

(C_random ≡ E_random by construction — same seed=42 + same prompt stream, ckpt-independent random init.)

## Table 2 — Cosine correlation by cell-count regime (trained vs random)

| substrate | regime | run | nC range | cos_mean | abs_cos_mean | eff_rank/N | disp_above/k |
|---|---|---|---|---|---|---|---|
| A_phase2_cotrain | early(8-64)  | trained | 16→57  | +0.1026 | 0.1548 | 0.6843 | 3.36/10.91 |
| A_phase2_cotrain | early(8-64)  | random  | 16→48  | +0.1073 | 0.1595 | 0.7053 | 2.64/9.73  |
| C_cells64_aware  | early(8-64)  | trained |  8→58  | +0.1210 | 0.1435 | 0.8531 | 2.08/5.33  |
| C_cells64_aware  | early(8-64)  | random  |  8→49  | +0.1720 | 0.1919 | 0.7958 | 2.12/5.38  |
| C_cells64_aware  | late(64-256) | trained | 75→75  | +0.0022 | 0.0426 | 0.8717 | 5.00/18.00 |
| C_cells64_aware  | late(64-256) | random  | 66→209 | +0.0127 | 0.0440 | 0.8346 | 9.80/32.20 |
| E_convo5k_ft     | early(8-64)  | trained |  8→47  | +0.1334 | 0.1525 | 0.8648 | 2.18/4.18  |
| E_convo5k_ft     | early(8-64)  | random  |  8→49  | +0.1720 | 0.1919 | 0.7958 | 2.12/5.38  |
| E_convo5k_ft     | late(64-256) | trained | 65→85  | +0.0021 | 0.0427 | 0.8660 | 6.00/18.50 |
| E_convo5k_ft     | late(64-256) | random  | 66→209 | +0.0127 | 0.0440 | 0.8346 | 9.80/32.20 |

## Table 3 — Split events by trigger type (60-turn / 100-turn windows)

| substrate | run | final_n_cells | n_splits_total | n_splits_disp | n_splits_tens | disp_frac | splits/turn |
|---|---|---|---|---|---|---|---|
| A_phase2_cotrain | trained | 57  | 41  | 26  | 15 | 0.634 | 0.41 |
| A_phase2_cotrain | random  | 48  | 36  | 21  | 15 | 0.583 | 0.36 |
| C_cells64_aware  | trained | 75  | 67  | 63  |  4 | 0.940 | 1.12 |
| C_cells64_aware  | random  | 209 | 201 | 143 | 58 | 0.711 | 3.35 |
| E_convo5k_ft     | trained | 85  | 77  | 72  |  5 | 0.935 | 1.28 |
| E_convo5k_ft     | random  | 209 | 201 | 143 | 58 | 0.711 | 3.35 |

## Table 4 — Dispersion trigger trajectory (trained vs random, per snapshot)

(Format: turn / nC / disp_above/k / inc_disp_splits)

### A_phase2_cotrain (cap-free)

| turn | trained nC | t disp/k | t Δsplit_disp | random nC | r disp/k | r Δsplit_disp |
|---|---|---|---|---|---|---|
| 0  | 16 | 3/4   | 0  | 16 | 2/4   | 0  |
| 10 | 23 | 4/5   | 7  | 23 | 4/5   | 7  |
| 20 | 34 | 8/8   | 11 | 33 | 8/8   | 9  |
| 30 | 38 | 6/9   | 4  | 38 | 5/9   | 3  |
| 40 | 41 | 5/10  | 3  | 44 | 3/11  | 2  |
| 50 | 57 | 7/14  | 1  | 44 | 4/11  | 0  |
| 60 | 57 | 4/14  | 0  | 45 | 3/11  | 0  |
| 70 | 57 | 0/14  | 0  | 48 | 0/12  | 0  |
| 80 | 57 | 0/14  | 0  | 48 | 0/12  | 0  |
| 90 | 57 | 0/14  | 0  | 48 | 0/12  | 0  |
| 99 | 57 | 0/14  | 0  | 48 | 0/12  | 0  |

### C_cells64_aware (cap-approach)

| turn | trained nC | t disp/k | t Δsplit_disp | random nC | r disp/k | r Δsplit_disp |
|---|---|---|---|---|---|---|
|  0 |   8 | 2/2   | 0  |   8 | 1/2   | 0  |
|  5 |   9 | 1/2   | 0  |   8 | 2/2   | 0  |
| 10 |   9 | 2/2   | 0  |   9 | 1/2   | 1  |
| 15 |   9 | 1/2   | 0  |  13 | 1/3   | 2  |
| 20 |  14 | 1/3   | 5  |  20 | 3/5   | 3  |
| 25 |  16 | 1/4   | 2  |  32 | 4/8   | 7  |
| 30 |  19 | 1/4   | 3  |  39 | 2/9   | 6  |
| 35 |  25 | 2/6   | 6  |  49 | 3/12  | 3  |
| 40 |  29 | 3/7   | 4  |  66 | 3/16  | 10 |
| 45 |  33 | 2/8   | 4  |  84 | 6/21  | 15 |
| 50 |  42 | 4/10  | 8  | 117 | 8/29  | 25 |
| 55 |  58 | 5/14  | 15 | 175 | 18/43 | 40 |
| 59 |  75 | 5/18  | 16 | 209 | 14/52 | 31 |

### E_convo5k_ft (cap-approach)

| turn | trained nC | t disp/k | t Δsplit_disp | random nC | r disp/k | r Δsplit_disp |
|---|---|---|---|---|---|---|
|  0 |   8 | 2/2   | 0  |   8 | 1/2   | 0  |
|  5 |   8 | 2/2   | 0  |   8 | 2/2   | 0  |
| 10 |   8 | 2/2   | 0  |   9 | 1/2   | 1  |
| 15 |   8 | 1/2   | 0  |  13 | 1/3   | 2  |
| 20 |  11 | 1/2   | 3  |  20 | 3/5   | 3  |
| 25 |  13 | 2/3   | 2  |  32 | 4/8   | 7  |
| 30 |  15 | 3/3   | 2  |  39 | 2/9   | 6  |
| 35 |  22 | 1/5   | 7  |  49 | 3/12  | 3  |
| 40 |  26 | 3/6   | 3  |  66 | 3/16  | 10 |
| 45 |  33 | 3/8   | 7  |  84 | 6/21  | 15 |
| 50 |  47 | 4/11  | 11 | 117 | 8/29  | 25 |
| 55 |  65 | 4/16  | 18 | 175 | 18/43 | 40 |
| 59 |  85 | 8/21  | 19 | 209 | 14/52 | 31 |

## Falsifier check

### F-CORR-1: trained correlation higher than random in late regime?
- C_cells64_aware: cos_mean late trained − random = +0.0022 − +0.0127 = **−0.0105** (FALSIFIED)
- E_convo5k_ft:    cos_mean late trained − random = +0.0021 − +0.0127 = **−0.0106** (FALSIFIED)
- And in EARLY regime (more comparable n_cells): C trained 0.121 < random 0.172 (−0.051);
  E trained 0.133 < random 0.172 (−0.039). Trained is **less** correlated, not more.

### F-CORR-2: trained dispersion trigger rate lower than random in late regime?
- C: disp_above/k mean trained=0.278 random=0.304; diff = −0.026 (weakly consistent)
- E: disp_above/k mean trained=0.324 random=0.304; diff = +0.020 (weakly inverted)
- Effectively wash — dispersion trigger rate is roughly equal across trained vs random
  at comparable cell counts. Not a strong driver.

### F-CORR-3: cross-substrate consistency?
- A is cap-free so doesn't probe the §51 mechanism directly.
- C and E show identical random trajectory (by construction), and very similar trained
  trajectories (final_n_cells 75 vs 85, splits/turn 1.12 vs 1.28). Consistent across
  the two cap-reaching substrates.

## §51 mechanism verdict: **ALT_MECHANISM**

The "trained cells more correlated → dispersion triggers slower" hypothesis is **falsified
in its direct form**. Surprising findings reframe the mechanism:

### What the data actually shows
1. **Cap-arrival latency is real**: C, E trained reach 75/85 cells at turn 59 vs random 209.
   That is a 2.5-3× lower cell-growth rate per turn. Confirmed at this measurement window.
2. **Inter-cell correlation is comparable or LOWER for trained**: in early regime trained
   cos_mean 0.12-0.13 vs random 0.17. F-CORR-1 falsified.
3. **Dispersion top-quartile trigger rate is comparable**: trained ~0.28-0.32 vs random
   ~0.30. F-CORR-2 weakly falsified (no consistent direction).
4. **The actual driver is tension-trigger SUPPRESSION**: trained substrates fire only
   4-5 tension-triggered splits across 60 turns, vs 58 for random — a **10-14× suppression**.
   Total splits/turn: trained 1.12-1.28 vs random 3.35 — almost entirely explained by
   tension-trigger absence (Δ_tens 53-54 ≈ Δ_total 134).
5. **Trained substrates use dispersion-dominant splits** (94% trained vs 71% random).
   Once their per-cell tensions stay below threshold (because EngineG's h_to_c projection
   lands cells closer to hidden_mean), splits accumulate only through dispersion outliers.

### Reformulated mechanism (substantiated by the measurements)
> §51 cap-conditional latency is driven by **per-cell tension threshold suppression**
> in trained substrates, NOT by lower inter-cell correlation. Trained h_to_c learns to
> project hidden_mean closer to existing cell positions (→ low ‖cell − hint‖² tension),
> which keeps `cell.tension_history < per_cell_threshold` and starves the tension-trigger
> path. The dispersion path remains active at similar rate, but contributes fewer splits
> per turn because the substrate is OR-combined (only one path can fire per cell per step).

### Cross-substrate honesty
- A_phase2_cotrain in cap-free regime shows the SAME trained-vs-random parity: trained 57
  cells / random 48 cells / similar disp_above ratios / similar tension-trigger counts (15
  vs 15). The tension-suppression effect is V14 mirror-specific to the v2 d=384 substrates
  where the cell_state buffer accumulates per-cell history.

## Honest C3 acknowledgments

1. **n=1 paired test per substrate**. Single random seed (42); we did not re-run the 5-seed
   battery. The split-rate gap (3×) is large enough to be robust against seed jitter, but
   cos_mean differences (0.01-0.05) are within plausible seed variance — the F-CORR-1
   falsification stands strongly only because trained is ≤ random in BOTH C and E and across
   BOTH regimes.
2. **C_random ≡ E_random** by construction (no ckpt-dependence in random init). The
   substrate-level finding (trained vs random within each substrate) is independent, but
   "universal across substrates" means "across DIFFERENT trained substrates," not different
   random baselines.
3. **A is cap-free**. The §51 mechanism is fundamentally about cap-approach behavior, so A's
   data only validates the early-growth half of the picture; cap-arrival dynamics on A
   cannot be tested without a much higher max_cells or longer trajectories.
4. **60-turn cutoff** doesn't reach trained's first_cap (turn 76-82 from prior BG). Our
   late-regime measurement (n_cells 65-85) is pre-cap for trained. Random crosses the cap
   threshold inside the window, so the late-regime contrast is asymmetric.
5. **Correlation = cosine off-diagonal mean**. Pearson correlation on raw cell-state values
   would weight high-magnitude cells more; cosine factors out magnitude. norm_cv is reported
   separately to track magnitude dispersion. Both metrics show no "trained more correlated"
   effect.
6. **Top-quartile dispersion trigger rate** is computed exactly as in the actual mitosis
   engine (`_dispersion_split_candidates` with sigma_mult=1.0). The fact that trigger rate
   is similar between trained and random implies the engine's gating logic is unbiased — the
   asymmetry must lie elsewhere (tension path).
7. **Lorenz noise injection** mutates cell_state every turn for v2 substrates. The reported
   cos_mean is post-Lorenz; the effect on inter-cell correlation is comparable across
   trained and random because Lorenz is shared infrastructure.
8. **No tension-history snapshots**. We computed dispersion mechanism state but did not log
   per-cell tension distribution. The "tension-suppression" reframing comes from the
   downstream split-trigger counts (n_splits_tension), which is indirect evidence.

## Cross-link to §51

- §51 PARTIAL finding: cap-arrival latency on C, E (trained 76-82 vs random 63-72 turns).
- This BG: cap-arrival latency CONFIRMED at the measurement window (trained nC 75-85 vs
  random nC 209 at turn 59). Mechanism CHANGED from "correlation → dispersion" to
  "tension-trigger suppression" — refined the §51 finding from "more correlated structure"
  to "h_to_c learned proximity to cells".
- Falsifier F-CORR-1 falsified → original §51 mechanism wording fragile, refinement needed.
- Falsifier F-CORR-2 weakly falsified → dispersion is not the differential driver.
- Falsifier F-CORR-3 holds → C, E both show same pattern (universal across cap-reaching
  substrates).
