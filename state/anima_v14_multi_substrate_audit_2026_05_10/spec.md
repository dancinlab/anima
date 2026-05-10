# BG-V14-MULTI-SUBSTRATE-AUDIT — spec

priority §47 (cycle 2026-05-10) — substrate-dependent V14 polarity 가설을 4+ substrate
cross-comparison 으로 일반화 검증.

## Hypothesis under test

**Polarity hypothesis** (born from §37 vs §38 split):
> Mitosis-AWARE training (cells co-evolved with LM via mitosis instrumentation during
> backward pass) produces ckpts where downstream V14 mirror trajectory has trained Φ
> ≤ random Φ (V14_VIOLATED), while mitosis-NAIVE training (cells instrumented only
> at inference time over a static LM ckpt) produces ckpts where trained Φ > random Φ
> (V14_PASS).

**Generalization claim**: this polarity is universal (substrate-independent given
the awareness binary), not artefactual.

## Substrate inventory (5 candidates)

| ID | ckpt | arch | params | mitosis paradigm | prior V14 |
|----|------|------|--------|------------------|-----------|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | EngineAG d=1024 GQA, 24L | 298.76M | naive (cotrain on KO chat, NOT mitosis-step) | V14_STRICT_PASS @ 1000-turn 10-seed (§38) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | EngineAG d=1024 GQA, 24L | 331.53M | naive (pretrain only, never cotrained) | NEW (this BG) |
| C | `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt` | v2 6L transformer d=384 | 18.52M | aware (mitosis-step in training loop, max_cells=64 saturated) | V14_VIOLATED @ 200-turn 5-seed (§37, seeds=[7,17,23,41,71]) |
| D | `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells128_step_35000.pt` | v2 6L transformer d=384, heads=4 | 18.52M | aware (max_cells=128, step=35K, 70% of 50K planned) | NEW (this BG) |
| E | `state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt` | v2 6L transformer d=384 | 18.52M | naive (FT continuation of byte-level v2 base, NO mitosis instrumentation) | NEW (this BG) |

Note: substrate E is byte-level 18M whereas C/D are 218M — direct paired comparison
of E with C/D conflates capacity AND paradigm. E is included as a "small mitosis-naive
d=384" to triangulate whether polarity persists below the 218M scale. A/B are nearly
identical capacity (298M / 332M) so A vs B is a clean within-paradigm replication.
C vs D is a clean within-paradigm replication (both mitosis-aware, both d=384).

## Method

For each new substrate (B, D, E) — and for paired comparison consistency, **ALSO rerun
C with V4_SEEDS** (since §37 used different seeds [7,17,23,41,71]):

- 5-seed V14 mirror: V4_SEEDS = `[42, 137, 271, 314, 1729]`
- max_cells = 128 (release cap for cell-count discrimination; matches §38)
- n_turns = 500, snapshot_every = 50 (constrained by 5-substrate cost budget)
- prompt stream: deterministic per (substrate-schema, seed=42) for trained,
  per-seed for random mirrors
- §30 all-fix: A1+A2+B1+D1 active for v2-schema substrates; for EngineAG substrates
  use the §38 mitosis_v5_port pipeline (same fix set)
- Φ_iit_unnormalized 16-bin (Fiedler MIP) as primary metric for EngineAG path;
  v2-schema path reports Φ + Φ_per_cell + α_v2 (the §37 metric set)

For substrate A, **reuse §38 V14_STRICT_PASS result directly** (1000-turn 10-seed,
already at greater statistical strength than what this BG can fire under cost).

## Verdict bins

For each substrate: V14_PASS / V14_PARTIAL / V14_VIOLATED.

Cross-substrate aggregate:
- **V14_POLARITY_GENERALIZED**: 4/4 substrate consistent with polarity hypothesis
  (mitosis-aware → VIOLATED, mitosis-naive → PASS)
- **V14_POLARITY_LIKELY**: 3/4 consistent
- **V14_POLARITY_FRAGILE**: 2/4 consistent
- **V14_POLARITY_FALSIFIED**: 0-1/4 consistent

The 4/4 count is over substrates {A, B, C, D}. Substrate E provides triangulation
context but its 18M capacity vs 218-330M of A-D introduces a confounder (capacity
collapses below threshold may cause spurious VIOLATED), so E is NOT counted in the
core 4/4 verdict, only reported as supplementary.

## Constraints

- raw#9: training/*.py local-only (mitosis_v5_port.py + engine_a_g_arch.py + iit_phi_port.py + mitosis_model_v5.py imported, NOT modified)
- raw#15: additive — all ckpts unmodified
- own 14: V14 5-seed strict per substrate
- own 16: $0 envelope — local Mac CPU only
- own 22: REBORN.md 직접 append 안함; dispatcher가 §47 slot에 receive 후 append
- own 38: artefact persisted under state/anima_v14_multi_substrate_audit_2026_05_10/

## Falsifiers

- F-MULTI-1: substrate inventory < 3 → cross-comparison weak, ABORT.  [PASSED — 5 candidates]
- F-MULTI-2: ALL substrates cap-bound at max=128 → cell-count comparison dimension collapsed.
- F-MULTI-3: mitosis-aware substrate (C or D) → V14_PASS → polarity hypothesis falsified.
- F-MULTI-4: mitosis-naive substrate (B or E) → V14_VIOLATED → polarity hypothesis falsified.
- F-MULTI-5: 500-turn budget too short → trajectory in transient regime, verdict noisy.

## Cost envelope

EngineAG d=1024 max=128 5-seed × 500-turn ≈ 80 min (extrapolated from §38 130s/100t)
v2 d=384 max=128 5-seed × 500-turn ≈ 50 min (extrapolated from §37 with cap-release)
- B: ~80 min
- D: ~50 min (using cells128 ckpt)
- E: ~30 min (smaller per-forward due to byte vocab and same arch)
- C re-run with V4_SEEDS: ~50 min
Total: ~3.5 h
