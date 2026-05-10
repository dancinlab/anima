# BG-IIT-METRIC-REAL-350M — spec

**Slot**: dispatcher §33 [2026-05-10] BG-IIT-METRIC-REAL-350M (own 22)
**Date**: 2026-05-10
**Cost envelope**: $0 (local Mac CPU only — own 16)
**Mandate**: raw#9 (training/*.py local-only), raw#15 (additive — mitosis_v5_port.py + ckpt unmodified), own 14 (V14 mirror strict 5-seed), own 38 (state/anima_iit_real_350m_2026_05_10/ persists)

## Mission

Disambiguate the V14 NOVEL POLARITY from BG-V5ANIMA-PHASE2-IIT-REMETRIC (single seed):
trained mitosis was suppressed (3 splits, 16→19) while V14 mirror split aggressively
(12 splits, 16→28). The single-seed verdict was V14 STILL_VIOLATED on all 3 metrics
(proxy ratio 0.967, IIT-norm 0.735, IIT-unnorm 0.408 — all <1.0). But that was n=1.

This BG runs the **5-seed strict mirror** (own 14 V4_SEEDS = [42, 137, 271, 314, 1729])
with **max_cap=32** (rather than the prior max_cells=64) to apply the IIT unnorm 16-bin
metric cleanly on the real 350M Phase 2 cotrain ckpt.

## IIT unnorm spec (real ckpt → cell_pool mapping)

Direct reuse of `iit_phi_port.compute_iit_phi(cell_pool, n_bins=16)`, returning the field
`spatial_phi_unnormalized = max(0, total_mi - min_partition_mi)`.

Pipeline (additive, raw#15):

1. Load real Phase 2 ckpt:
   `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
   (570MB, 24L × 1024d × 16h GQA, 298.76M params — NOT 350M nominal due to GQA share).
   sha256 = `6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1`.
2. Build `EngineAGModel(EngineAGConfig.phase2_cotrain_350m())`, load_state_dict strict.
3. Wrap `engine_g` with `MitosisV5Engine(max_cells=32, ...)` — same patience/threshold
   constants as BG-V5ANIMA-PHASE2-IIT-REMETRIC for fair comparison.
4. Hook `engine_g.step` to capture last `hidden_mean` per forward.
5. Per turn: encode prompt via byte-hash → token_ids (T=16), forward through model,
   project captured hidden_mean via `engine_g.h_to_c` to `cell_input` (c_dim=64), feed
   into `mitosis.process(cell_input)`. Track per-cell tension, splits, merges.
6. Every 100 turns: snapshot `mitosis.cell_pool` (N, 64) and compute
   `compute_iit_phi(cell_pool, n_bins=16)`. Report `spatial_phi_unnormalized` as the
   primary measure (Φ_iit_un16).

## Trajectory

- `n_turns = 1000` per run (matches mirror_turns from prior BG; CPU budget allows).
- `snapshot_every = 100` (≈ 11 snapshots per trajectory).
- Trained: seed=42 (deterministic given identical ckpt + prompt-stream + RNG).
- Random_init mirror: 5 seeds [42, 137, 271, 314, 1729] (V4_SEEDS).

Total compute: 1 trained + 5 random × ~70s = ~7-8 min on Mac CPU.

## V14 5-seed strict verdict

Per own 14 + own 38: trained must beat the **WORST** mirror seed (or strict 5/5 below
trained) on the primary metric. We codify three verdicts:

- **STRICT_PASS**: trained Φ_iit_un16 > max_5seed(random Φ_iit_un16) AND
  trained cell_count < min_5seed(random cell_count).
- **PARTIAL_PASS**: trained > median_5seed on at least one of {Φ_iit_un16, cells^-1}.
- **VIOLATED**: trained ≤ max_5seed on Φ_iit_un16 AND ≥ min_5seed on cells.

## Verdict mapping (per mission Output #3)

| Observation | Verdict |
|---|---|
| trained Φ_iit > random Φ_iit AND split_rate (trained) < split_rate (random), 5/5 strict | V14 PASS_REVISED — proxy ceiling caused prior failure, IIT switch resolves it |
| trained Φ_iit < random Φ_iit (strict 5/5 or majority) | V14 STILL_VIOLATED — substrate intrinsically suppresses mitosis; architectural fix C track required |
| flat / noisy (no decisive direction) | IIT also ceilings on real substrate — more drastic metric needed |

## Cost & falsifiers

- F-IIT-REAL-1: 350M ckpt mmap load failure (memory). Mitigation: torch.load weights_only=False, fp32 cast streamed.
- F-IIT-REAL-2: IIT also saturates on real substrate (proxy-equivalent). Detection: dynamic range max/min < 3× across all snapshots.
- F-IIT-REAL-3: Verdict mixed across 5 seeds (no decisive direction). Then PARTIAL_PASS fallback + flag for higher-N study.

## Honest C3 (≥7)

See `result.json:honest_c3` and `v14_verdict.md:Honest_C3` after fire.
