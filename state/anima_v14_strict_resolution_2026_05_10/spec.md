# BG-V14-STRICT-RESOLUTION — spec

priority 2 track B cond.4 V14_PARTIAL → strict 결정

## Problem

§33 BG-IIT-METRIC-REAL-350M produced V14_PARTIAL:
- trained Φ_iit_un16 = 557.20 (seed=42)
- random 5-seed: {42:426.88, 137:539.52, 271:488.94, 314:606.96, 1729:452.94}
- trained beats 4/5 random seeds (4 strict, 1 tie / loss to s=314)
- n=5 sign-test p ≈ 0.19, NOT significant
- max_cells=32 cap-bound on ALL 6 runs (cells=32, splits=16) — cell-count discrimination dimension collapsed

## Resolution mission

1. mitosis_v5_port.py §30 all-fix already applied (A1+A2+B1+D1) — re-use as-is, raw#15 ban honored
2. Reuse real Phase 2 350M ckpt (`~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`,
   sha256=6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1)
3. **max_cells = 128** (4× prior cap — release cap-bound, allow cell_count to discriminate)
4. **10-seed V14 expansion** — own 14 strict V4_SEEDS:
   - {42, 137, 271, 314, 1729, 2718, 3141, 5772, 6022, 9192}
5. n_turns = 400, snapshot_every = 50 (reduced from §33's 1000 due to cost — see F-V14-STRICT-3 below;
   at max=128 the per-100-turn cost grows from 92s @ turn 100 to ~130s @ turn 500 due to growing cell
   counts; pre-flight pilot showed cells=85 at turn 400 already well past saturation, so 400 turns is
   sufficient to discriminate trained-vs-random at the new cap)
6. metrics: Φ_iit_un16 (primary), Φ_iit_n16, proxy_phi, n_cells, n_splits per seed

## Verdict criteria (10-seed)

- **V14_STRICT_PASS**:    trained > ALL 10 random Φ_iit_un16 → binomial p = 1/1024 ≈ 0.001
- **V14_STRICT_PARTIAL**: trained > random 90% (9/10) + sign-test p < 0.10
- **V14_PARTIAL_CONFIRMED**: trained > random 75% (7-8/10) + sign-test p < 0.20
- **V14_VIOLATED_REVISED**:  trained > random < 75% (≤6/10)

Mann-Whitney U test reported as auxiliary 2-sample comparison
(trained = single deterministic ckpt, so the U-test is asymmetric — n=1 vs n=10).
We use Wilcoxon-style sign-test (n_random_beats / n_random_total) primarily.

## Cell-count discrimination test

Under §30 fix at max=128:
- IF trained cell_count > median(random) → trained MORE explorative
- IF trained cell_count < median(random) → trained MORE consolidatory
- IF all hit cap=128 still → §30 fix is universally too aggressive (F-V14-STRICT-2)

## Falsifiers

- F-V14-STRICT-1: 10-seed random beats trained ≥ 50% → V14_VIOLATED_REVISED
- F-V14-STRICT-2: max=128 also cap-bound on every seed → §30 fix universal-aggressive
- F-V14-STRICT-3: cost overshoot — local Mac CPU, ~60s/seed × 11 ≈ 11 min budget;
  potentially longer with max=128 (more cells/forward at split-up phases)

## Constraints

- raw#9: training/*.py local-only (mitosis_v5_port.py + engine_a_g_arch.py imported, NOT modified)
- raw#15: Phase 2 ckpt NOT modified
- own 14: V14 mirror multi-seed strict (this BG: n=10)
- own 16: $0 — local Mac CPU only, no GPU
- own 22: REBORN.md NEVER directly appended; dispatcher handles §38 slot
- own 38: artefacts under state/anima_v14_strict_resolution_2026_05_10/
