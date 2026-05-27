# BG-CHAMPION-WALL-CAUSAL-PROOF — §28 H1+H3 mechanism × §37 substrate-dependent V14 polarity causal evidence

## ts
2026-05-10 (cycle 2026-05-10 — 5-star pursuit)

## Mission
§28 BG-PHASE2-SPLIT-RATE-DIAG identified champion-wall: EngineG.h_to_c collapses
hidden_mean onto 1-2 cell-pool dims (champion attractor bottleneck).
§37 observed substrate-dependent V14 polarity:
  - Phase 2 (mitosis-naive cotrain @ d=1024)        → V14_STRICT_PASS  (10/10 trained > random)
  - v2 cells64 (mitosis-aware @ d=384, 62 splits)   → V14_VIOLATED     (trained < random_mean)

Hypothesis (champion-wall causal): mitosis-aware training pre-forms
champion-wall during the training step itself, exhausting the inference-time
mitosis Φ headroom. mitosis-naive training leaves the EngineG.h_to_c
projection un-specialised → inference-time mitosis can still build novel
attractor structure → V14 PASS.

## Methods (this BG)

### Metric definitions
1. **champion_dominance** = top-1 row-variance share over output channels
   of the cell-input projection (h_to_c-analog).
   - Phase 2: `engine_g.h_to_c.weight` (64, 1024) — variance per c_dim row.
   - v2 cells64: `blocks.{0..5}.ffn.engine_g.3.weight` (384, 1536) — last-layer
     and layer-mean. Engine_g here is dual-FFN sub-network (no cell-pool inside
     model_state); the FFN output projection that writes back into residual
     stream is the closest in-model proxy.
2. **attractor_bottleneck** = log(spectral_radius(W)) / log(d_inner).
   - SVD top-1 singular value → log-ratio against input dim.
3. **phi_headroom_remaining** = max_phi_observed − mean_phi_recent.
   - v2: 200-sample `phi_history` from ckpt; recent_window=100.
   - Phase 2: `proxy_phi` and `iit_phi_unnorm_b16` from anima_v14_strict_resolution
     trained-run snapshots (9 snapshots, 1000 turns); recent_window=2.
4. **v14_polarity** (orthogonal): from prior reports, immutable on this run.

### Ablation (h_to_c-only random_init)
Phase 2 ckpt loaded → ONLY `engine_g.h_to_c.weight` overwritten with
N(0, 0.02²) per seed in {42, 137, 271}. Everything else stays trained.
200-turn V14 mirror, max_cells=128, side-by-side with:
  - trained baseline (full ckpt)
  - 3-seed full random_init mirror

If champion-wall causes V14 polarity, h_to_c-randomized Φ should drop
toward random-mirror Φ.

If h_to_c-randomized Φ stays at trained level → champion-wall NOT polarity cause.

### Data sources
- `/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
- `/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt`
- `/Users/ghost/core/anima/state/anima_v14_strict_resolution_2026_05_10/result_10seed.json`
- `/Users/ghost/core/anima/state/anima_v5mitosis_d384_sweep_2026_05_10/result.json`

## Falsifiers
- F-CHAMPION-WALL-1: |champion_dominance(v2) − champion_dominance(p2)| < ε → polarity not driven by dominance.
- F-CHAMPION-WALL-2: ablation Φ ≈ trained Φ within noise band → h_to_c not polarity cause.
- F-CHAMPION-WALL-3: 3 metric directional consistency < 3/3 → multi-factorial mechanism, not pure champion-wall.

## Honest C3 (≥7)
1. v2 cells64 architecture has NO `engine_g.h_to_c` module — its `engine_g` is a
   dual-FFN GELU/Linear sub-network, not the cell-pool dynamics module.
   Direct apples-to-apples comparison of "h_to_c row variance" is impossible;
   v2 metric uses last-layer FFN output projection as a structural proxy
   (the residual-stream-writer). This is honest but architectural asymmetry.
2. Phase 2 phi_headroom uses 9 snapshots from a 1000-turn V14 trained run,
   not training-step phi history (Phase 2 ckpt's meta.json has no phi log).
   v2's phi_headroom uses 200-sample training-step phi history. Sampling
   density and source differ — the comparison is qualitative.
3. Spectral radius is a global linear scalar; champion attractor is a non-linear
   per-step phenomenon. Spectral radius is a proxy for "how strongly W amplifies
   one direction"; not a proof of dynamic attractor formation.
4. Only Phase 2 supports the h_to_c-only ablation (the v2 ckpt has no h_to_c
   in its state_dict). Ablation tests "is h_to_c the V14 PASS substrate cause?"
   not "is the absence of h_to_c the V14 VIOLATED cause for v2?". Ablation
   thus probes one direction of the polarity claim.
5. Ablation is 200-turn × 3 seeds, not the 1000-turn × 10 seeds of §V14-STRICT.
   $0 envelope dictates this; verdict bands are looser.
6. byte-hash mod 32000 prompt encoding (not real BPE) — relative-trained-vs-
   random comparison only, no semantic Φ magnitude claim.
7. h_to_c-randomization preserves c_to_h, cell_pool_init, and the upstream
   24-layer Engine A. Not a full reset — measures the marginal contribution
   of the trained h_to_c only.
8. raw#15 read-only honored: ckpts on disk untouched. In-memory weight copy
   mutated for ablation only.
9. : NO appending REBORN.md from this script.
10. : artefacts under
    `state/anima_champion_wall_causal_proof_2026_05_10/{spec.md, metrics.json, ablation_result.json, verdict.md}`.
