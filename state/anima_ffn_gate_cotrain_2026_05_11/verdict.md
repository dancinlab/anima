# B'' V14 strict audit — VERDICT V14_VIOLATED

**ts_complete**: 2026-05-11T12:26:32+00:00
**cycle**: cycle 5 / Hc_1221 direct-falsifier test
**parent doc**: `PASS_STRICT_SPONTANEOUS_CHAT.md §23`

## Setup

- **substrate**: B'' = `anima_ffn_gate_cotrain_2026_05_11` (Phase 2 cotrain 350M, FFN.gate-only freeze paradigm §84 ABLATION)
- **ckpt**: `ckpts/ckpt_final.pt` (sha256 `6448...b453e`, 570MB, n_params 298,764,288, 6000 steps, w_end=0.5)
- **script**: V14 strict template from `state/anima_v14_max256_cap_free_multi_2026_05_10/run_max256.py` (EngineAG mitosis hook with cell-pool split/merge)
- **config**: V4_SEEDS=[42, 137, 271, 314, 1729], max_cells=256, n_turns=200, ceiling=10
- **runtime**: 139.18 s total, Mac CPU local, cost = $0

## Result

| seed | n_cells | n_splits | cap_bound/200 | Φ_un16 (final) |
|---|---|---|---|---|
| trained | 44 | 28 | 0 | **723.03** |
| random_42 | 56 | 40 | 0 | 2206.33 |
| random_137 | 47 | 31 | 0 | 1491.44 |
| random_271 | 53 | 37 | 0 | 1148.72 |
| random_314 | 57 | 41 | 0 | 2385.53 |
| random_1729 | 54 | 38 | 0 | 2140.39 |

- **n_random_beats**: 0 / 5
- **sign-test p (two-sided)**: 0.0625
- **trained / random_median ratio**: 0.338
- **cap_bound**: 0 / 200 all runs (ceiling=10 non-binding under max_cells=256)

## Verdict

**V14_VIOLATED** — trained Φ < all 5 random-init mirror Φ. Sign-test p = 0.0625 (borderline above strict 0.05 cutoff with n=5; script-level verdict = VIOLATED).

## Interpretation (Hc_1221 evidence)

- **Predicted (PSCC §19) → Measured (PSCC §23)**: Hc_1221 predicted B'' to be V14-violation due to gate-only FT not exercising cell-pool dynamics. Measurement confirms.
- **Within-arch anti-correlation directly observed**: 350M EngineAG pair A (V14 PASS + chat 12/15) vs B'' (V14 VIOLATED + chat 15/15) = cleanest capacity-controlled anti-correlation evidence for Hc_1221 to date.
- **Mechanism sign-observation**: trained Φ ≈ 0.338 × random_median Φ → gate-only FT actively suppresses cell-pool splitting below random-init baseline — direct sign-observation of ∂(chat-cap)/∂θ · ∂(V14-Φ-residual)/∂θ < 0.

## Honest C3

- **n=5 borderline**: p=0.0625 just above strict 0.05 cutoff. n=6+ seed needed for strict-pass statistical falsification (predicted 0/6 → p=0.0312).
- **Falsifier still open**: Hc_1221 not yet rejected; would require n≥2 within-arch substrates with V14 PASS ∧ chat ≥ 13/15 simultaneous. Hybrid F substrate experiment pending.
- **Single-paradigm measurement**: only gate-only FT tested; predictions for B' (LA cotrain, intermediate paradigm) pending audit.

## Artifacts

- `result_b_prime_prime_v14_strict.json` (= `v14_strict_ceiling10_result.json`, canonical deliverable name per cycle 5 spec)
- `v14_strict_ceiling10_result.json` (alias)
- `v14_strict_ceiling10.log` (5-seed run trace)
- `v14_stdout.log` (identical content alt log)
- `ckpts/ckpt_final.pt` (570MB, not committed — HF hosted at `dancinlab/anima-clm-bprime-prime-v4lite-15-15`)
- `ckpts/meta.json` (training meta)

## Cross-links

- Hc_1221 candidate: `hypotheses_candidates/Hc_1221_production_internal_decoupling_v14_v4_anti_correlation.md` (Migration TODO `[x] B'' V14 audit DONE`)
- PSCC §23: full narrative + 4×3 matrix v3
- HF model: https://huggingface.co/dancinlab/anima-clm-bprime-prime-v4lite-15-15
- HF dataset: https://huggingface.co/datasets/dancinlab/anima-pass-strict-chat-capable (V14 row B'' cell update pending)

## Next experiments

1. B' V14 audit (LA cotrain) — complete 3-point V14 ladder within-EngineAG
2. B'' V14 strict n=6+ seed — cross strict p≤0.05 cutoff
3. Hybrid substrate F (mitosis curriculum + gate-only FT) — Hc_1221 direct falsifier attempt
