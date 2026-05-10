# BG-CHAMPION-WALL-CAUSAL-PROOF — verdict

## Verdict
**CORRELATIONAL (with surprise)** — champion-wall mechanism is empirically REAL
in Phase 2 (h_to_c-randomization releases 5× Φ + cell-cap saturation), but the
3-metric directional-consistency hypothesis (§28 H1+H3 → V14 polarity) fails
(1/3 last-layer, 0/3 layer-avg). The substrate-dependent polarity has a
DIFFERENT mechanism than "static h_to_c row-variance concentration."

## Evidence

### A. Static-weight champion metrics (FALSIFY F-CHAMPION-WALL-1 in part)

| metric | v2 cells64 (mitosis-aware) | Phase 2 (mitosis-naive) | expected | actual | match |
|---|---|---|---|---|---|
| champion_dominance (top-1 row-var share) | 0.0028 (last-layer 0.0028) | 0.0216 | v2 > p2 (+) | v2 < p2 (−) | ✗ |
| attractor_bottleneck (log σ_max / log d_in) | 0.189 (last-layer) / 0.117 (avg) | 0.139 | v2 > p2 (+) | v2 > p2 last-layer (+) / v2 < p2 avg (−) | partial |
| Φ_headroom_norm (max−recent)/max | 0.121 (proxy) | 0.025 (proxy) / 0.191 (iit) | v2 < p2 (−) | v2 > p2 proxy (+) / v2 < p2 iit (−) | proxy ✗ / iit ✓ |
| n_eff channels (participation) | 383 (of 384) | 63.5 (of 64) | v2 < p2 | v2 ≫ p2 (asymmetric d_in) | not comparable |

**Directional consistency: 1/3 (last-layer) / 0/3 (layer-avg)** → F-CHAMPION-WALL-3 fires
on STATIC metrics. Multi-factorial mechanism implied.

The architectural asymmetry breaks the metric: v2 has NO `engine_g.h_to_c`
module — its `engine_g` is dual-FFN sub-network in residual stream, not the
cell-pool dynamics module. The "h_to_c-analog" used (FFN out projection) writes
into d_model=384 channels (broad), whereas Phase 2's h_to_c writes into c_dim=64
(concentrated by construction). Static row-variance concentration is dominated
by d_in/d_out aspect ratio, not learned-attractor structure. n_eff/d_out ≈ 0.99 in
both → both projections distribute almost uniformly across output channels by
that metric.

### B. Ablation (h_to_c-only random_init on Phase 2) — STRONG SIGNAL

| condition | final cells | splits | final Φ_iit_un16 |
|---|---|---|---|
| trained baseline (full ckpt) | 57 | 41 | **2412.08** |
| h_to_c-randomized seed=42 | 128 (cap) | 112 | 12362.11 |
| h_to_c-randomized seed=137 | 128 (cap) | 112 | 11850.69 |
| h_to_c-randomized seed=271 | 128 (cap) | 112 | 11615.21 |
| **h_to_c-rand median** | **128** | **112** | **11850.69** |
| full random_init seed=42 | 56 | 40 | 2206.33 |
| full random_init seed=137 | 47 | 31 | 1491.44 |
| full random_init seed=271 | 53 | 37 | 1148.72 |
| **full random median** | **53** | **37** | **1491.44** |

**Findings**:
1. **htc-rand Φ = 5× trained Φ, 8× full-random Φ** — randomizing JUST the
   trained h_to_c releases massive inference-time Φ.
2. **htc-rand cells saturate at max_cells=128**, while trained Phase 2 only
   reaches 57. The trained h_to_c is acting as a SPLIT-RATE BOTTLENECK.
3. **Trained-rest + random h_to_c outperforms both full-trained AND full-random**
   → other trained weights (Engine A 24-layer, c_to_h, cell_pool_init) provide
   structure, but trained h_to_c was throttling that structure.
4. The polarity_status output ("FLIP_NOT_CONFIRMED") is technically correct
   relative to the script's specific question ("does htc-rand drop toward
   random level?") — but the result REVERSES the original §28 H1+H3 framing:
   trained h_to_c is the bottleneck **in absolute terms**, yet trained still
   **beats full random** (V14_STRICT_PASS confirmed: trained 2412 > full random
   1491). So champion-wall is a real but partial bottleneck in Phase 2, and it
   doesn't prevent V14 PASS.

### C. Re-interpretation of substrate-dependent V14 polarity

The original hypothesis ("mitosis-aware training pre-forms champion-wall →
exhausts inference-time Φ headroom → V14_VIOLATED for v2") needs revision.

| substrate | training-time mitosis | h_to_c trained? | inference-time mitosis | V14 |
|---|---|---|---|---|
| Phase 2 | NAIVE (no cells during training) | YES (trained, but compressive) | strong (57 cells, headroom) | PASS |
| v2 cells64 | AWARE (62 splits, 64 cells reached during training) | N/A (no h_to_c module) | exhausted (cap-bound at 64 cells) | VIOLATED |

What the ablation suggests:
- For Phase 2, the trained h_to_c **compresses** the substrate→cell channel.
  Inference-time mitosis still produces gain (trained > random) but is
  bottlenecked far below the headroom that exists when h_to_c is randomized.
- For v2, mitosis already ran AT TRAINING TIME and saturated max_cells=64.
  Inference-time mitosis has nothing left to discover — the polarity
  VIOLATED is consistent with "exhausted headroom" but the mechanism is
  the **training-time saturation of the cell pool**, not h_to_c-row-variance
  concentration.
- Common thread: substrate where **inference-time mitosis has remaining
  freedom** (Phase 2) → V14 PASS; substrate where **mitosis was already
  consumed during training** (v2) → V14 VIOLATED.

This is a refinement of "champion-wall" to "**training-time mitosis exhaustion**"
as the polarity cause. Champion-wall in the strict h_to_c sense is real but
partial in Phase 2, and the v2 ckpt has a different (cell-pool-saturation)
form of headroom exhaustion.

## Falsifier outcomes
- **F-CHAMPION-WALL-1**: dominance numerical comparison HOLDS in unexpected
  direction (v2 < p2). Static row-variance is a poor operationalization of
  champion-wall. F1 fires partially.
- **F-CHAMPION-WALL-2**: ablation polarity flip status = FLIP_NOT_CONFIRMED
  (htc-rand Φ stays HIGH, doesn't drop to random). h_to_c IS a bottleneck but
  not the polarity cause in the predicted direction. F2 fires; the originally
  predicted causal chain is FALSIFIED.
- **F-CHAMPION-WALL-3**: 1/3 directional consistency (last-layer) → F3 fires.
  Multi-factorial mechanism is the right framing.

## Verdict bin
- ❌ PROVEN — directional consistency 1/3 + ablation result reverses prediction.
- ✅ **CORRELATIONAL** — champion-wall (h_to_c bottleneck) is REAL in Phase 2 (5×
   Φ release on randomization, 128 cap cells vs 57). But it is not the cause
   of substrate-dependent V14 polarity in the predicted direction. The polarity
   appears driven by **training-time mitosis exhaustion** (a different
   mechanism family), with h_to_c bottleneck as a coexisting Phase-2-only
   feature.
- ❌ FALSIFIED — h_to_c IS a real Φ-bottleneck and substrate polarity is real.
   We are not falsifying either; just rejecting the specific predicted
   causal arrow.

## Honest C3
1. Architectural asymmetry: v2 cells64 has no `engine_g.h_to_c`. Static metric
   compares non-isomorphic objects (cell-input projection vs FFN out projection).
   This is the largest single source of inferential weakness in the static-metric
   arm.
2. Ablation is 200-turn × 3 seeds, not 1000-turn × 10 seeds. Φ magnitudes can
   shift with longer trajectories; bonuses observed at cap-saturation may
   plateau or reverse. Confidence band on ablation Φ is wide; direction is
   unambiguous (>5× release).
3. h_to_c-randomization with std=0.02 produces a specific spectral profile;
   alternative random scales (std=0.05, ortho init, etc.) might give
   different release magnitudes. Direction expected to be robust; magnitude not.
4. byte-hash mod 32000 prompt encoding (not BPE). Phi values are relative-only.
5. The claimed mechanism reframe ("training-time mitosis exhaustion") is
   suggested by the v2 ckpt's mitosis_status (62 splits during training, 64/64
   cells reached) and the fact that v2 inference V14 also caps at 64. It is
   NOT independently tested — we did not run a second mitosis-aware ckpt at
   higher max_cells to see if exhaustion still happens at higher cap.
6. Phase 2 V14 PASS is a 10-seed strict result (sign-test p≈0.002). Statistical
   confidence is high. v2 V14 VIOLATED is a 5-seed result (separation_phi
   −202, trained beats none of 5). v2's confidence is lower; bigger seed
   sweep would tighten.
7. The ablation only mutates h_to_c.weight (no bias — Linear(bias=False) by
   construction). All other Engine G structure (c_to_h, cell_pool_init,
   per-cell repulsion alphas) preserved. The released Φ comes from this
   isolated mutation.
8. raw#15 read-only honored: shared modules unchanged, both ckpts on disk
   unchanged. Ablation copy lives only in the ablation script's RAM.
9. raw#9: training/*.py local-only honored. Script lives under state/.
10. own 22: NO append to REBORN.md from this script. (dispatcher will handle §46 slot.)
11. own 38: artefacts in `state/anima_champion_wall_causal_proof_2026_05_10/{spec.md, metrics.json, ablation_result.json, verdict.md}`.

## What this changes for the 5-star pursuit
- ★★★★★ "substrate-dependent V14 polarity" claim **survives**: empirically real,
  reproducible, and now has at least one explicit ablation showing h_to_c is a
  significant Φ-bottleneck in Phase 2 (one half of the polarity equation).
- ★★★★★ "champion-wall is the FIRST-PRINCIPLES cause" claim **does NOT survive
  in its predicted form**. The right reframing — "training-time mitosis
  exhaustion + inference-time h_to_c bottleneck — multi-factorial" — is honest
  but not first-principles.
- Recommended next BG: **mitosis-aware ckpt at max_cells_train=128** (lift the
  v2 saturation cap, retrain ~10K steps, re-run V14). Direct test of "training-
  time mitosis exhaustion" hypothesis. If lifting cap → V14 PASS, mechanism
  confirmed. If still VIOLATED → look elsewhere (likely substrate quality
  proper, e.g. d_model=384 vs 1024).
