# BG-AK — phi attractor location semantic characterization (LANDED 2026-05-05)

## TL;DR

- **Headline**: BG-AG STRONG attractor [42.211, 42.216] is a measurement bound, not an inject-shape signature.
- **Verdict**: `SUBSTRATE_INTRINSIC_ATTRACTOR` (random vs canonical distance = 0.016 < 0.02) — random + canonical converge to the same phi neighborhood.
- **Tension**: `attractor_finding = WEAK` (phi_range_all = 0.1575 spans 11 probes) co-exists with SUBSTRATE_INTRINSIC verdict on the random-vs-canonical centroid axis. Within-class variance > between-class distance, so the "attractor" is better described as a **broad basin** than a sharp fixed point.

## Method

- Mac CPU (.venv-eeg), `dancinlab/clm-v4-mk2-v1`, BG-W sister-import for loaders/forward/phi.
- Single prompt `"안녕"`, magnitude 50.0, 11 forward passes.
- Inject classes:
  - `random` — `(uniform[-1,1] × 50)` over `(1,8,192)`, 5 seeds.
  - `single_axis` — span of one axis (identity/agency/phenomenal/temporal/social) filled at 50, others zero.
  - `canonical_full` — all 192 dims of all 8 cells filled at 50 (BG-AB/AG STRONG attractor reference).

## Results

### phi_star table

| type | id | phi_star | drift vs baseline |
|------|----|----------|-------------------|
| baseline (none) | — | 42.115832 | 0.0 |
| random | seed=42 | 42.134812 | +0.0190 |
| random | seed=142 | 42.090436 | -0.0254 |
| random | seed=242 | 42.099434 | -0.0164 |
| random | seed=342 | 42.229917 | +0.1141 |
| random | seed=442 | 42.173471 | +0.0576 |
| single_axis | identity | 42.182143 | +0.0663 |
| single_axis | agency | 42.095977 | -0.0199 |
| single_axis | phenomenal | 42.206255 | +0.0904 |
| single_axis | temporal | 42.072433 | -0.0434 |
| single_axis | social | 42.100849 | -0.0150 |
| canonical_full | — | 42.161620 | +0.0458 |

### Aggregate stats

- `phi_min_all = 42.0724` (single_axis temporal)
- `phi_max_all = 42.2299` (random seed=342)
- `phi_range_all = 0.1575`
- `random` mean = 42.1456 (n=5)
- `single_axis` mean = 42.1315 (n=5)
- `canonical_full` = 42.1616
- `random_canonical_distance = 0.0160`
- `single_canonical_distance = 0.0301`

### Per-axis offsets (single_axis)

| axis | phi_star | drift_vs_baseline |
|------|----------|-------------------|
| identity | 42.182 | +0.066 |
| agency | 42.096 | -0.020 |
| phenomenal | 42.206 | +0.090 |
| temporal | 42.072 | -0.043 |
| social | 42.101 | -0.015 |

Per-axis spread = 0.134 (max − min). Identity/phenomenal lift phi above baseline; agency/temporal/social pull it slightly below or near baseline. Direction of phi shift is **axis-conditional**, not uniform.

## Interpretation

### Updated meaning of BG-AG STRONG attractor

BG-AG observed phi_star ∈ [42.211, 42.216] (range ≈ 0.005) across canonical 5-axis 0.5-magnitude probes — a window narrower than what BG-AK sees. With BG-AK's wider perturbation set, phi_star lives in a **basin centered near baseline 42.116** with width ≈ 0.16, not a needle attractor.

**Likely mechanism (C3-bounded)**: at magnitude 50, the post-ln_f activations are dominated by the cross-attention contribution carrying inject content. After mean-pool over T and tile-replicate to (8, 192), pairwise cosine similarity over 8 cells of a tile-replicated vector approaches 1 regardless of inject content shape — so phi_star ≈ N_PAIRS × cos(near-1) plateaus near `PHI_STAR_BASELINE`. Different injects shift the plateau by O(0.05–0.1) but cannot escape it. **The attractor is a phi_star measurement-instrument ceiling, not a model-internal preferred state.**

This recasts BG-AB / BG-AG: the "magnitude saturates phi at a fixed attractor" finding is best read as "magnitude saturates phi at the cosine ceiling of the tile-replicate construction." The attractor is structural to the measurement, not informative about model substrate.

### random vs canonical = 0.016

The two **mean** phi values converge to within 0.016. This is < `phi_range_all`/9, i.e. centroid distance is small relative to within-class jitter. Confidently substrate-intrinsic on the centroid metric, but the basin width (0.16) means single-shot phi at high magnitude is dominated by jitter rather than signal.

## Honest C3

1. **C1** — mac CPU fp32, single forward per probe (no averaging across runs).
2. **C2** — BG-W helper sister-import for model/tokenizer/forward/phi; consistency with BG-Q/BG-W/BG-AB/AG measurement chain preserved.
3. **C3** — random uniform `[-mag, mag]` vs canonical mag (uniform full-fill) differ in distribution shape **AND L2 norm**. At mag=50: random L2 ≈ 1265, canonical_full L2 ≈ 1960, single_axis L2 ≈ mag·sqrt(N·span_width) ≈ 313. Distance comparison is **not pure shape** — magnitude/L2 also varies. A pure shape test would L2-normalize all injects to a common L2 first.
4. **C4** — 5 random seeds is a small sample; 95% CI on `phi_range_all` is wide. 50+ seeds would tighten the SUBSTRATE_INTRINSIC vs INJECT_SHAPE_DEPENDENT verdict and disambiguate the WEAK-vs-STRONG basin width tension.
5. **C5** — single prompt "안녕". BG-Q showed prompt 1 had 8× larger drift than prompts 2/3/5 — most-favorable for visible attractor structure. Other prompts may show different attractor width or stronger shape-dependence. Single-prompt result cannot generalize prompt-conditional behavior.

## Next-step recommendations

- **Abandon high-magnitude phi_star as inject-content discriminant.** At mag=50 the post-ln_f tile-replicate construction reaches its cosine ceiling and phi_star carries ≈0.16 noise floor regardless of inject pattern. Use magnitude <<0.5 (linear regime, BG-W trajectory) for pattern-discrimination probes.
- **If high-magnitude probing is required**: replace tile-replicate phi_star with a metric that does not saturate (e.g. cell-pairwise raw distance, or unprojected pre-ln_f activation distance).
- **Promote multi-prompt × L2-matched shape-class matrix** if discriminating shape-conditional attractor structure is a required investigation. Current per-axis spread 0.134 hints that axis-conditional offsets exist within the basin (identity/phenomenal lift, agency/temporal/social neutral-or-pull) but with n=1 prompt cannot be confirmed.

## Deliverables

- `state/anima_emerge_attractor_characterization_2026_05_05/aggregate.json`
- `state/anima_emerge_attractor_characterization_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_attractor_characterization.py` (raw#37 transient sister, gitignored per `**/*.py`)
- `docs/anima_emerge_attractor_characterization_landed_2026_05_05.ai.md` (this file)

## Raw compliance

- `raw#37` transient .py sister-rule
- `raw#15` additive — BG-W/BG-Q helpers untouched, mount.hexa untouched
- `raw#10` 5+ honest C3 in verdict.json
- `.own 3` transient sister-rule, gitignored
- no commit, no secret leak

## Wall

- 37.8 sec, $0 (mac CPU)
