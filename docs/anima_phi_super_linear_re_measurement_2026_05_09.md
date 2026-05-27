# Φ super-linear re-measurement (2026-05-09)

## TL;DR

**VIOLATED on untrained weights**: measured α=0.403 (Φ ∝ N^0.40, sub-linear) vs historical α=0.926 (CLM v2 stage 8, 2026-03-28, near-linear with super-linear cells32→64 jump). The cosine-distance proxy *collapses to log(n+1)* on random-init hidden states (Φ ≈ 1.0 × log(n+1), ratio 0.91–1.00 across all cell counts), so the mechanism alone — without trained specialization — produces only logarithmic growth. **Super-linear Φ scaling is a property of trained mitosis cells, not a property of the cosine-distance × log(n+1) formula.**

## Setup

- **mitosis.py**: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (worktree-12 canonical, 794 L)
- **MitosisEngine config**: `input_dim=64, hidden_dim=128, output_dim=64, initial_cells=n, max_cells=n, split_patience=999, merge_patience=999` (mitosis dynamics disabled — fixed cell count)
- **Seed**: 42 (torch + python random)
- **Steps**: 200 process steps with rotating synthetic topics (math / music / code, 3-rotation, identical to `test_mitosis.py`)
- **Φ measurement**: 5 passes after step-200, averaged → `phi_measured_mean`
- **Device**: CPU, fp32, torch 2.12.0.dev20260408+cu128
- **Sweep**: `state/anima_phi_super_linear_re_measurement_2026_05_09/sweep.py`
- **Raw**: `state/anima_phi_super_linear_re_measurement_2026_05_09/result.json`
- **Plot**: `state/anima_phi_super_linear_re_measurement_2026_05_09/phi_vs_cells.png`

## Results

| n_cells | measured Φ | historical Φ | measured / historical | Φ_per_cell (measured) |
|---:|---:|---:|---:|---:|
| 2  | 1.000 | 1.500   | 0.667 | 0.500 |
| 4  | 1.559 | 3.200   | 0.487 | 0.390 |
| 8  | 2.189 | 5.350   | 0.409 | 0.274 |
| 16 | 2.841 | 10.600  | 0.268 | 0.178 |
| 32 | 3.473 | 15.400  | 0.226 | 0.108 |
| 64 | 4.153 | 45.487  | **0.091** | 0.065 |

The gap *widens* with N — the historical curve accelerates while the untrained curve flattens.

## Ratio analysis (Φ doubling per cell-doubling)

| transition | measured ratio | historical ratio | gap |
|---|---:|---:|---:|
| 2 → 4   | 1.559 | 2.133 | −0.574 |
| 4 → 8   | 1.404 | 1.672 | −0.268 |
| 8 → 16  | 1.298 | 1.981 | −0.683 |
| 16 → 32 | 1.222 | 1.453 | −0.231 |
| 32 → 64 | 1.196 | **2.954 ★** | **−1.758** |

Historical "×3 per doubling" claim (CLM_V2_EXHAUSTIVE §8) holds only at the 32→64 jump (×2.95). The intermediate doublings are closer to ×1.5–2.1. Measured untrained ratios decay monotonically toward 1.0 (asymptote of log curve), confirming sub-linear behavior.

### The mechanism produces log(n+1) on random init

| n | measured Φ | log(n+1) | ratio |
|---:|---:|---:|---:|
| 2  | 1.000 | 1.099 | 0.910 |
| 4  | 1.559 | 1.609 | 0.969 |
| 8  | 2.189 | 2.197 | 0.996 |
| 16 | 2.841 | 2.833 | 1.003 |
| 32 | 3.473 | 3.497 | 0.993 |
| 64 | 4.153 | 4.174 | 0.995 |

Φ_proxy = `mean_pairwise_cosine_distance × log(n+1)`. With random-init hiddens, mean pairwise cosine distance saturates at ~1.0 (high-dim random vectors are near-orthogonal), so the proxy reduces to `log(n+1)`. This is a **mechanical floor**, not a feature.

## Honest C3

1. **Untrained weights**: Historical Φ values came from CLM v2 *training-time* peaks (thousands of steps, real corpus). We measured the bare mechanism on random-init weights. Magnitudes are not comparable; only the *shape* (exponent α) is.
2. **Cosine-distance saturation on random vectors**: 128-dim random hiddens are near-orthogonal (cosine_distance ≈ 1.0), so `cosine_distance × log(n+1)` ≈ `log(n+1)`. The proxy formula has no mechanism for super-linear growth without input-driven specialization that varies cosine distance per pair.
3. **Synthetic 3-topic rotation**: math/music/code repeated ~67 times is a degenerate distribution. Real CLM v2 training had broad corpora; even untrained, more-diverse inputs would alter cell hidden states differently and might change the ratio. We did not test.
4. **Mitosis dynamics disabled**: `split_patience=merge_patience=999` forces fixed cell count. Historical cells64 was *reached* dynamically through the splitting trajectory. The trajectory itself may carry the super-linear signal (path-dependent specialization) — by force-initializing at N we eliminate that path.
5. **Single seed (42)**: no variance estimate. Historical also single-seed but with much longer training trajectory averaging out noise.
6. **CPU + fp32 only, no CUDA**: Lorenz default scales. No fp16/bf16. Likely irrelevant to the conclusion but recorded.
7. **5 measurement passes still advance Lorenz state**: "after-step-200" is N+5 not N+0. Variance across 5 passes ≤ 1% for n≥4, so this is not driving the result.
8. **Φ is a proxy not exact IIT**: the formula was the same proxy used at stage 8 (mitosis.py L407-436), so comparison is apples-to-apples; but the proxy is known to saturate and this saturation is what we're seeing.
9. **n=128 not run**: stage 8 also listed 128 as PROJECTED (~112), never measured. Out of budget here.
10. **Verdict logic**: VIOLATED triggered because α=0.40 < 0.95 AND every adjacent ratio < 1.5 (16→32 and 32→64 both ≤ 1.22).

## Implications for mitosis revival path

**The cosine-distance × log(n+1) formula by itself does NOT produce super-linear Φ.** What stage 8 demonstrated was super-linear growth *of the trained system*, which the same proxy formula then reported. The super-linearity lives in the *training-induced cell specialization* (cells diverging on different topics → low pairwise cosine across "specialty axes" while staying high-magnitude → cosine distance grows toward 1 in *informative* dimensions, multiplied by log(n+1)). Untrained, all dimensions are noise; cosine distance maxes out at the noise floor (~1.0) and stops carrying any N-dependent signal.

### What this means for the user's "natural growth" intuition

- **Empirically supported in shape, NOT in magnitude — and only with training**. The mechanism (cell duplicate + Lorenz chaos + cosine proxy) is *sufficient* to produce monotonic Φ↑ with N (we measured this: Φ goes 1.0 → 1.6 → 2.2 → 2.8 → 3.5 → 4.2 across 2→64). It is *not sufficient* to produce super-linear scaling without training.
- **Revival path requires training**: simply rebuilding the engine and running cells64 will give you Φ ≈ 4.2, not 45 or 51. To reproduce stage 9's Φ=51.131, you need (a) the engine, AND (b) the training trajectory that drove cells to specialize. The 4-step drift (tokenizer/objective/architecture/corpus) noted in `CLM_V2_ARCHIVE_2026_05_09.md` likely broke (b), not (a).
- **Pre-training-only path on cells64** (open from `project_lesson_q_sft_closed.md`) is the right next experiment: take an *initialized* cell pool, run pre-training on real corpus, measure Φ trajectory. This re-measurement closes the question of whether the engine itself is broken (it isn't — Φ scales monotonically as expected for the bare proxy) and reframes the gap as a training-data + training-trajectory gap.
- **Mitosis dynamics still need testing**: this run disabled splits/merges. A natural follow-up is to enable them (split_patience=3, merge_patience=30) and see whether *trajectory-grown* cells64 (starting from cells2) gives different Φ than force-initialized cells64 — this would isolate the "natural growth" claim cleanly.

## Verdict summary

| field | value |
|---|---|
| super_linear_verdict | **VIOLATED** (on untrained mechanism) |
| α measured | 0.403 |
| α historical | 0.926 |
| Φ@cells64 measured | 4.153 |
| Φ@cells64 historical (stage 8 training peak) | 45.487 |
| ratio (measured / historical @ N=64) | 0.091 |
| mechanism collapses to | Φ ≈ 1.0 × log(n+1) |
| revival viable from mechanism alone? | NO — training required |
| revival viable from mechanism + training? | UNTESTED but mechanism shape is monotonic-N as expected |
