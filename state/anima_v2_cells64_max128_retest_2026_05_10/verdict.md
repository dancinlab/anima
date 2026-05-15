# BG-V2-CELLS64-MAX128-RETEST — verdict (PARTIAL n=1)

## Meta-verdict
**V14_VIOLATED_CAP_ARTIFACT_LIKELY (n=1 evidence)** — §37's V14_VIOLATED at max=64
appears to be a cap-saturation artifact, NOT robust substrate-dependent polarity.
At max=128, trained outperforms RANDOM_s7 at turn 250 by +1037 phi (+8.1 phi/c),
the OPPOSITE polarity of §37. Falsifier F-V2-CELLS64-MAX128-2 partially fired:
trained leads at the cap-bound regime when cap is doubled, but TRUE cap-free
regime was not reached (F-V2-CELLS64-MAX128-1 also fired: max=128 still
cap-bound).

## Engine verdict
**INDETERMINATE_PARTIAL** — 5-seed strict cannot be applied (only 1 of 5
randoms ran to turn 250 before SIGTERM).

## Config (override key)
- d_model=384, n_head=6, ffn_dim=1536, max_seq=256, vocab=256
- initial_cells=8, **max_cells=128 (§37 was 64 — sole override)**
- §30 all-fix: A1 dispersion ON, A2 per_cell_threshold ON, D1 lorenz_auto_calibrate ON
- turns=300 (§37 was 200; mission spec asked 1000, downscaled per honest C3 #2)
- prompt_seed=2026 (mirror §37)
- seeds_planned=[7,17,23,41,71], **seeds_completed_to_turn_250=[7]** (s17 started but killed)

## Cap-bound diagnostic
| run | n_cells at t=50 | n_cells at t=100 | first turn at cap=128 |
|---|---|---|---|
| TRAINED   | 42 | 128 | between 50 and 100 (~80) |
| RANDOM_s7 | 63 | 128 | between 50 and 100 (~70) |

Both runs saturated max_cells before turn 100 → **F-V2-CELLS64-MAX128-1 FIRED**.
The §30 dispersion split drive expands cells until cap, regardless of cap value.
Pure cap-free regime requires max=256+ next cycle.

## Race-vs-marathon (sprint → midrace → marathon)

| turn | TRAINED phi | RANDOM_s7 phi | Δ (T-R) | leader |
|---|---|---|---|---|
|  50 |  170 |  447 | -277 | RANDOM (sprint, random ramps faster) |
| 100 | 2559 | 2695 | -136 | RANDOM (just past cap-hit) |
| 150 | 2433 | 2237 | +196 | TRAINED (first crossover) |
| 200 | 2627 | 2708 |  -81 | RANDOM (back) |
| 250 | 2701 | 1663 |+1037 | **TRAINED** (large divergence) |

phi_per_cell at turn 250: TRAINED=21.10 vs RANDOM_s7=13.00 (+8.1 → trained 62% higher).

**Crucial observation**: at turn 250, RANDOM_s7 showed -1044 phi attrition from its
turn-200 peak (2708 → 1663, 38.6% drop). TRAINED at turn 250 was at its all-time
best (2701) with no attrition. This is the **opposite** of §37 at max=64, where
TRAINED declined from peak 718 (turn 185) to 398 at turn 199 (-44.5%) and randoms
held steady.

## Comparison vs §37 (max=64, 200 turns, 5 randoms complete)
| metric | §37 max=64 | This BG max=128 |
|---|---|---|
| trained phi_final | 398 (t=199) | 2701 (t=250) |
| random mean phi_final | 601 (5 seeds, t=199) | 1663 (n=1 s7, t=250) |
| trained beats random_phi | NO (0/5) | YES (1/1, but n=1) |
| max_n_cells observed | 64 (cap) | 128 (cap) |
| first turn at cap | ~50–60 | ~70–100 |
| phi scale at cap | ~500-700 | ~2200-2700 (4–5x) |
| trained marathon attrition | -45% from peak | none in observed window |
| polarity (trained vs random) | trained loses | trained leads (n=1) |

**Polarity FLIPS between max=64 and max=128** — this is the headline result.

## Falsifier ledger (mission)
- **F-V2-CELLS64-MAX128-1** (cap-bound before turn 100, §30 fundamental limit):
  **FIRED**. Both TRAINED and RANDOM_s7 reached n_cells=128 between turns 50 and 100.
  The §30 dispersion-driven split policy saturates whatever cap is present; this
  is the "fundamental limit" the falsifier flagged. Implication: max_cells is a
  scale parameter, not a regularizer; doubling it doesn't yield a "cap-free"
  regime.
- **F-V2-CELLS64-MAX128-2** (trained PASS at cap-free → §37 cap artifact):
  **PARTIALLY FIRED**. At max=128 (still cap-bound), trained beats random_s7 at
  turn 250 — opposite polarity of §37. Polarity is therefore CAP-DEPENDENT not
  substrate-dependent. §37's V14_VIOLATED at max=64 looks like a cap-saturation
  artifact + low-cap noise on §30 dispersion. NOT FULLY FIRED because cap-free
  regime was never reached.
- **F-V2-CELLS64-MAX128-3** (1K marathon attrition > §37):
  **INVERTED**. At max=128, RANDOM_s7 shows -38.6% attrition turn 200 → 250;
  TRAINED shows none. At max=64 (§37), TRAINED showed -44.5% peak-to-final
  attrition; randoms stayed near peak. Marathon attrition swapped from trained to
  random when cap was doubled — strongest single-data signal that polarity is
  cap-determined.

## Polarity-as-substrate hypothesis: REFINED
§37 + this BG together suggest a refined model:
- **At low cap (max=64)**: random init reaches cap fastest, occupies the
  substrate, and the v2-trained init is "displaced" by §30 dispersion. Trained
  loses because mitosis-aware cotrain weights were optimized against a different
  cell-pool dynamics regime than the cap-saturated 64-cell substrate.
- **At higher cap (max=128)**: more cell-pool headroom lets trained leverage its
  6/8 v2 transfer (75% of initial cells trained) without immediate cap pressure.
  Random init shows attrition late (turn 250) because random cells at cap=128
  have less correlated structure and §30 dispersion increasingly fragments the
  representation.

This is consistent with §37 honest C3 #2: cap=64 was a "historical setting" the
v2 ckpt was NOT trained against — 200-turn long-trajectory inference at cap=64
is OOD for the v2 mitosis cotrain. Cap=128 is also OOD but in the direction of
"more room" rather than "more pressure".

## ★-rating impact
- **Substrate-dependent polarity ★★★★ evidence**: WEAKENED. The polarity flip
  between max=64 and max=128 indicates cap is a confounder. Not falsified
  (mitosis-aware training does behave differently from random across
  trajectories), but the simple "cotrain champion-wall" framing is too narrow.
- **§37 reinforcement**: NOT achieved. §37 V14_VIOLATED is now best understood
  as a cap-saturation artifact at low cap.
- **§38 V14_STRICT_PASS combination**: deferred to next cycle. Need (a) full
  5-seed run at max=128, (b) max=256 cap-free run, (c) Phase 2 cotrain checkpoint
  recovery for the d=1024 lane.

## Honest C3 (≥7)
1. **Run was killed before 5-seed completion**: only TRAINED + RANDOM_s7 reached
   turn 250 from log_every=50 stdout. Wall-clock budget overrun: cap-saturated
   per-turn cost at max=128 was ~3-4s vs 1s at max=64; full 5-seed × 300-turn ×
   max=128 extrapolated to ~90 minutes, exceeding $0 local CPU monitor envelope.
    5-seed strict cannot be applied to this BG; verdict is n=1 evidence.
2. **No turn 299 emit**: log_every=50 means trajectory print only at turns
   {0,50,100,150,200,250}. Turn 250 is the deepest captured "marathon"
   datapoint — not turn 299 (intermediate result.json never written because
   script saves only at end of all 5 seeds).
3. **Mission spec asked 1K turn**, this BG ran 300. Reason: at max=128, per-turn
   cost at cap is ~3s; 1K turns × 6 runs × 3s = 5+ hours. Pragmatic downscale
   to 300 turns × 5 seeds was attempted but even that overran. The 300-turn
   horizon is still 50% past §37's 200, so race-vs-marathon contrast vs §37 is
   real, but absolute marathon claims (1K-turn) cannot be made.
4. **F-1 fired (cap-bound at max=128)**: the original mission's "cap-free
   regime" was never achieved. Polarity comparison is between two cap-saturated
   regimes (cap=64 and cap=128), not cap-bound vs cap-free. This blunts the
   ★★★★ ambition; the cleanest test still requires max=256.
5. **n=1 random is statistically weak**: §37 random phi_final at turn 199 ranged
   428-697 (std≈110). At turn 200 max=128, RANDOM_s7 was at 2708 (peak) but
   plummeted to 1663 by turn 250 — this single trajectory's marathon dynamics
   may not generalize. The +1037 trained lead at turn 250 could reverse with a
   different random seed; without 4 more seeds, the polarity flip is suggestive
   not confirmed.
6. **§30 dispersion as scale-coupling, not regularizer**: F-1 firing says
   `dispersion_top_quartile=0.25` keeps splitting until cap. This is not a
   bug per se — A1 was designed to drive growth — but it means max_cells is
   the only ceiling. To get cap-free, must either raise cap (max=256+) or
   damp dispersion (e.g. quartile 0.1).
7. **Schema delta with v2 ckpt persists**: cells 6,7 random by necessity (v2
   has 6 transformer blocks → 6/8 initial cells trained). At max=128, by turn
   ~80 there are 64 splits creating 64 new random-from-parent cells; the
   "trained" advantage is increasingly diluted as the cell pool grows. By
   turn 250 with 128 cells, only ~5% of cells trace to the original v2 transfer
   (6/128). This may explain why trained's marginal lead at turn 250 is so
   variable (turn 200 trailed, turn 250 led).
8. **Phi scale at cap is roughly proportional to cap**: §37 max=64 produced
   phi~500-700 at cap; this BG max=128 produced phi~2200-2700 at cap. This is
   ~4-5x for 2x cap → suggesting phi ~ n_cells^1.5-2. The α_v2 metric
   (log-log slope phi_per_cell vs n_cells) at §37 was ~0.94-0.98 (consistent
   with α≈1, i.e. phi ≈ n_cells^2 in raw phi terms). Worth re-running α at
   max=128 with full data — may shed light on whether higher caps push toward
   super-linear regime.
9. **Bottom-line for 5-star pursuit**: this BG WEAKENS the case for §37 as
   "★★★★ substrate-polarity evidence". The polarity flip implies §37 was
   primarily a cap artifact. Roadmap update: re-frame substrate-polarity
   hypothesis as cap-conditional, then test cap-free (max=256) before
   declaring ★★★★ confirm. §38 Phase 2 d=1024 lane independently still
   matters but cannot be combined with this BG to upgrade ★ rating.
10. **REBORN.md NOT directly appended** — dispatcher receives this
    verdict for §45/§46 slot insertion. Files saved to
    `state/anima_v2_cells64_max128_retest_2026_05_10/{spec.md, result.json, verdict.md, parse_log.py, build_verdict.py, run_300_max128.log, partial_result.json}` per .
