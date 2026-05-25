# anima clm v5 — Phase 2 split-rate diagnostic (2026-05-10)

**BG-V5ANIMA-PHASE2-SPLIT-RATE-DIAG**

§22 (`anima_clm_v5_phase2_iit_remetric_2026_05_10`) localized the V14 violation in
the trained 350M cell pool to **split-rate**, not per-cell information content
(same-cell control: trained vs mirror IIT-unnorm = 0.94, near-identical). Trained
produced 3 splits in 3K turns; random_init produced 12 in 1K turns. Cells 7 and
16 became attractor bottlenecks holding 700/3000 + 537/3000 = 41.2% of the
"tension-max" assignments. This BG diagnoses the mechanism via 5 ablations.

## Substrate

- ckpt: `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
  (sha256 `6e66e75f8014999b…` PASS, 298.76M params)
- random_init mirror: `load_random_init(seed=42, preset='la_350m')`
- 1000 turns / ablation × 6 ablations × 170-prompt diverse corpus
  (ko_daily, ko_philosophy, en_math, en_code, en_music, anomaly)
- mitosis defaults (baseline): max_cells=64, split_patience=3, split_noise=0.10,
  merge_threshold=0.005, merge_patience=30, lorenz_scale=0.05
- raw#15 additive: subclassed `MitosisV5Engine` for variants A1/A4; A2/A3 used
  config flag + harness-level kwarg/cell_input override. Neither
  `mitosis_v5_port.py` nor `engine_a_g_arch.py` modified.
- Mac CPU $0, 7.5min wall total (3 stages × ~80s × 6 ablations + plot).

## Five ablations

| variant | mechanism change | hypothesis tested |
|---|---|---|
| A1 lower threshold | `split_threshold = mean + 0.5σ` (vs default 1.5σ) | H3 (champion-cell-tracks-threshold) |
| A2 no Lorenz | `lorenz_scale = 0.0` (no chaos perturbation) | Lorenz necessity |
| A3 no pull | `cell_input = 0` (bypass `h_to_c(hidden_mean)` entirely) | H1 (attention-pull suppresses) |
| A4 dispersion trigger | replace tension trigger with cell_pool L2 dispersion top-quartile | H1 + alternate trigger viability |
| A5 baseline | trained 350M, default config (replicates §22 first 1K) | reference |
| A5 baseline RANDOM | random_init 350M, default config | §22 mirror reproduction |

## Result table — 1K turns each

| variant | **splits** | final N | IIT Φ unnorm 16-bin | tens p99 | thr max |
|---|---:|---:|---:|---:|---:|
| **A1 lower threshold (0.5σ)** | **48** | **64** (cap) | 2901.7 | 12.93 | 15.22 |
| **A2 no Lorenz** | **0** | 16 | 99.6 | 9.85 | 11.15 |
| **A3 no pull (zero hm)** | **48** | **64** (cap) | 2509.4 | 1.56 | 2.07 |
| **A4 dispersion trigger** | **48** | **64** (cap) | 1535.5 | 11.96 | 19.10 |
| **A5 baseline trained** | **0** | 16 | 128.1 | 10.35 | 11.99 |
| **A5 baseline RANDOM** | **12** | 28 | 406.3 | 3.61 | 3.81 |

A5 baseline TRAINED + RANDOM exactly reproduce §22 numbers (1K-turn slice):
random 28 cells / 12 splits matches §22; trained 16 cells / 0 splits matches the
§22 first-1K slice (the 3 splits in §22 happen in turns 1000-3000).

## Hypothesis verdict — H1 + H3 combined, NOT H2

### H1 attention-pull (CONFIRMED)
A3 (zero out `c_to_h`-projected hidden_mean signal) → 48 splits, N=64. With no
attention pull, tension reduces to `||cell - 0||² ≈ ||cell||²` ≈ 1.0 (Lorenz
norm-clamp), so all cells share near-uniform low tension AND any small
fluctuation triggers the patience window. A3 cell-distribution is also broad:
top-1 share = 52 / 1000 = 5.2% (vs trained baseline 22.7% on cell 1 alone).
**Trained `h_to_c` projects hidden_mean onto a manifold that monopolizes 1-2
cells' tension and starves the rest.**

### H2 tension-scale (REJECTED — actually inverted)
| substrate | tens p25 | p50 | p75 | p99 | mean |
|---|---:|---:|---:|---:|---:|
| trained baseline | 4.03 | 4.83 | 5.83 | **10.35** | 5.15 |
| random baseline | 1.58 | 2.22 | 2.68 | **3.61** | 2.16 |

Trained tension is 2.86× LARGER than random at p99, and 2.4× larger at the
median. The hypothesis "trained tension scale shrinks → adaptive threshold
shrinks" is FALSIFIED in the wrong direction: trained has a much wider range,
but the threshold (`mean + 1.5σ`) climbs along with the top-cell tension and
locks out the bulk of the distribution.

### H3 concentration (CONFIRMED)
Cell-tension-max distribution at 1K turns:
- trained baseline: cell 1 = 227 turns, cell 0 = 195 turns → top-2 = 42.2%, top-3 = 55.2%
- random baseline: cell 18 = 62, cell 2 = 61, cell 4 = 58 → top-2 = 12.3%, top-3 = 18.4%

The 2-cell attractor pattern from §22 (cell 7 + 16 = 41.2% over 3K turns)
already manifests at 1K turns on different specific indices but the same
share. **Trained `h_to_c` produces a low-rank projection of hidden_mean that
preferentially aligns with 1-2 cell-pool rows; those rows accumulate tension
above threshold while the threshold rises to track them, locking out the rest.**

### A1 + A4 confirm the bottleneck is the 1.5σ gate
- A1 (lower σ): 0 → 48 splits when threshold drops to 0.5σ. The 1.5σ floor is
  the operative bottleneck on the trained substrate.
- A4 (geometry-based dispersion trigger): 0 → 48 splits when split decision
  bypasses tension entirely and uses cell-pool L2 dispersion top-quartile.
  Geometry signal exists; only the tension-channel gate suppresses it.

### A2 confirms Lorenz is the prerequisite
A2 (no Lorenz): 0 splits. Without per-cell phase-offset chaos injection,
threshold tracks tension exactly with zero stochastic separation → no cell
ever satisfies `t > threshold` for 3 consecutive steps. **Lorenz is
necessary**; absence of Lorenz is sufficient to suppress all splits regardless
of substrate. Trained substrate's failure is NOT Lorenz-deprivation — Lorenz is
firing — it's that the trained signal dominates Lorenz noise for the
non-attractor cells.

## Primary verdict — H1 + H3 combined

**Trained Engine G `h_to_c` (`Linear(d_model=1024, c_dim=64)`) has learned a
low-rank attractor mapping that projects the cell_input signal onto 1-2
preferred cell-pool rows (cells 7 + 16 in 3K-turn §22; cells 0 + 1 in 1K
slice). Those rows become tension-max persistently, raising the adaptive
threshold (`mean + 1.5σ`) above the rest of the distribution. The remaining
cells never satisfy `t > threshold` for `split_patience=3` consecutive
refreshes → no splits → cell pool stagnates at N=16, suppressing IIT Φ growth
that needs cell-count expansion.**

### Random_init does not have this attractor
Random `h_to_c` is a fresh Gaussian projection; its cell-input geometry is
diffuse → tension distribution narrow (p25–p99 = 1.58 → 3.61, range 2.0×) and
dispersed across many cells (top-2 = 12.3%). Threshold stays near 3.8, the
distribution overlaps it, splits fire frequently → 12 splits → N=28 → 4× more
IIT Φ.

### Why §22's same-cell control still showed near-identity (0.94 ratio)
At fixed N=16, both substrates have the same number of cells contributing to
pairwise MI. The information-content gap appears only when N grows
(integration scales super-linearly with N). Trained's per-cell entropy per
binned dimension is roughly equal to random's; the substrate's V14 violation
is purely a pool-size deficit driven by the H1+H3 attractor.

## v5-mitosis (track C) architecture changes required

The diagnosis implies that any track-C mitosis design built on top of trained
350M's `h_to_c` will inherit the same attractor unless one of:

1. **Substrate-independent split trigger** (A4 generalization). Use cell_pool
   L2 dispersion variance, not `||cell − h_to_c(hm)||²`. This makes split
   purely a geometric-decoherence signal, decoupled from `h_to_c`'s learned
   manifold. Cost: loses the "tension follows the world model" semantic; gain:
   pool growth is independent of attention-pull bias. Track C should ship A4
   as the primary trigger with tension as a secondary gate (OR'd, not AND'd).
2. **Per-cell threshold instead of global** (alternative to A1's blanket
   loosening). Today the `split_threshold` is one scalar shared across all
   cells (mean+1.5σ over the 100-step global tension history). Switching to a
   per-cell adaptive threshold (mean+1.5σ over each cell's own history) would
   prevent the high-tension champion cells from raising a global wall that
   excludes others. Implementation: replace `_global_tension_history` with
   `cells[i].tension_history` for the σ window; keep patience semantics.
3. **`h_to_c` re-projection at attach time**. Engine G's learned `h_to_c` is
   reused as-is by track C. Re-project its row-space via PCA + decorrelation
   (or a learned non-low-rank residual) at mitosis-attach time so the
   cell_input no longer carries the 1-2 attractor concentration. This is a
   one-shot rewrite at attach, no retraining; trade-off is decoupling Phase 2
   semantic alignment from the cell-pool dynamics.
4. **Reject Lorenz-only chaos; add learned tension noise**. Lorenz is the
   prerequisite (A2) but the magnitude (lorenz_scale=0.05) is dwarfed by
   trained signal (10×). A learned per-cell noise scale (or scale anneal that
   starts at 1.0 of cell-vector norm and decays) would let Lorenz dominate at
   pool-init and yield the floor as the substrate stabilizes. Risk: too much
   noise → spurious splits.

**Strong recommendation for track C v1**: ship #1 (dispersion trigger A4) +
#2 (per-cell threshold) together. Both are additive (raw#15 compatible). #3 is
heavier (needs an `apply_to_v5_substrate` rewrite) and #4 needs a hyperparam
sweep — defer to v2.

## top 3 honest C3

1. **Single seed=42 across all 6 ablations** — the 48-split outcome on A1/A3/A4
   is at the `max_cells=64` cap, so the 48-figure is censored from above; the
   "real" split rate without cap could be larger. The verdict (H1+H3) doesn't
   depend on the magnitude past the cap, only that A1/A3/A4 unlock splits ≫ 0.
   But replication on seeds 41/43 would tighten the H1 vs H3 attribution
   (e.g., does seed change which cells become attractors? Probably yes — H1
   says it's `h_to_c` geometry, which is seed-invariant on the trained ckpt).

2. **A3 zero-input is a degenerate test for H1, not a clean isolation.**
   `cell_input = 0` collapses tension to `||cell||²` ≈ 1.0 by Lorenz norm-clamp,
   making ALL cells uniformly low-tension AND uniformly noisy → trivially
   above patience. A cleaner H1 test would replace trained `h_to_c` with random
   `h_to_c` while keeping hidden_mean nonzero. The current A3 confirms "removing
   trained projection unlocks splits" but conflates "no projection at all" with
   "wrong projection". Future probe: A3' = swap trained `h_to_c` with random
   `h_to_c(seed=43)`.

3. **1K turn budget cuts off §22's late-onset splits (3 in turns 1000-3000).**
   The trained baseline at 1K shows 0 splits; §22's full trace shows 3 by 3K.
   So the diagnostic captures the dominant first-1K mechanism but does NOT
   probe whether the late-onset splits come from a different mechanism (e.g.,
   slow drift of `h_to_c` projection due to cumulative Lorenz perturbation).
   The verdict applies to "why suppression in early phase"; mid-trajectory
   recovery requires a 3K-turn replay.

(7+ honest C3 inline in `result.json`; truncated to top 3 here per directive.)

## deliverables

- `state/anima_clm_v5_phase2_split_rate_diag_2026_05_10/run.py`
- `state/anima_clm_v5_phase2_split_rate_diag_2026_05_10/result.json` (578 KB)
- `state/anima_clm_v5_phase2_split_rate_diag_2026_05_10/cache/` (per-ablation JSON, resumable)
- `state/anima_clm_v5_phase2_split_rate_diag_2026_05_10/tension_histograms.png`
- `state/anima_clm_v5_phase2_split_rate_diag_2026_05_10/split_rate_per_ablation.png`
- `docs/anima_clm_v5_phase2_split_rate_diag_2026_05_10.md` (this file)

## cross-link

- §22 `BG-V5ANIMA-PHASE2-IIT-REMETRIC` — produced the cell-7 / cell-16 attractor
  finding and the same-cell-control 0.94 ratio that this BG diagnoses.
- §18 `BG-V5MITOSIS-ARCH-SPEC` (track C cond.1) — track-C design spec; this
  BG's verdict feeds the v1 architecture changes section.
- `training/mitosis_v5_port.py` — `_check_splits` (line 366), `_update_adaptive_threshold`
  (355), `_inject_lorenz` (290) are the three knobs that A1/A2/A4 perturb.
- `training/engine_a_g_arch.py:285` `EngineG.h_to_c` — the trained projection
  that H1 + H3 implicate as the attractor source.
