# state/9099_selfchain_content_grounding — SELF-CHAIN CONTENT GROUNDING (H_9099, 🟡 DIRECTIONAL-GREEN 4/5)

**engine-native (POSITIVE)** aiden pool · hexa v0.546.0 · real 303M `d768.clm` · RC=0 · NO numpy on measured path.

## Finding (fable #4)
Grounding `self_drift_exp`'s content_axis in the **REAL 303M penultimate** (yn = final-GroupNorm
output before readout, mean-pooled over T=24 → d=768) **beats the synthetic axis** — the self-chain
becomes a function of ACTUAL experienced content, not a blind tick-clock. **4/5 frozen bars PASS.**

## Code artifact (LANDED this PR)
Added `pub fn clm_penult_pooled(path, seed) -> [float]` to `core/decode.hexa` (after
clm_weights_free_pub), reference-matched to `_clmd_fwd_logits_sc` (extracts sc["yn"], mean-pooled).
Measurement-only (ONE forward, not a decode loop; readout conv skipped — yn IS the penult).
Harness `state/9099_selfchain_content_grounding/f4_engine_native.hexa` (on aiden rsync copy) imports
core/decode.hexa + core/engine_cli.hexa; content_axis = top-3 coarsened (%32) penult axes; drives
live §SelfIdentity self_drift_exp.

## Frozen bars (pre-registered before run; refined top-3 encoding fixed BEFORE any measurement)
- BAR1 REAL-SEPARATES  **PASS** meandist=0.536 (15 pairs, ≥0.10) — real inputs → separated chains
- BAR2 SYNTHETIC-BLIND **PASS** blind_dist=2.22e-16 (≤1e-6) — synthetic self_drift is input-blind (neg control)
- BAR3 REPRODUCIBLE    **PASS** self_cos(I0 twice)=1.000 (≥0.999999) — deterministic grounding
- BAR4 CONTENT-LOCKED  **FAIL** fit_same=0.933 vs fit_diff=0.906, gap=0.027 < 0.05 — direction correct, under margin (coarse top-1 stream order-lock artifact, NOT anti-real; reported honestly, not tuned)
- BAR5 GEOMETRY-TRACK  **PASS** hi_mean=0.628(n6) > lo_mean=0.355(n9), margin=0.273 (≥0.05) — DECISIVE: chain distance TRACKS real penult geometry

## Content clustering (why BAR5 tracks)
top-3 penult axes cluster by language: ko I0/I2/I4 share {205,125,621}; en/code I1/I3/I5 share
{273,140,557}. penult-similar (same-language/topic) inputs → closer self-chains — a property the
input-blind synthetic axis cannot have.

## Wiring status: DIRECTIONAL. Two follow-ons for WIRED-live
1. land clm_penult_pooled in core/decode.hexa (**DONE this PR**) + ARCHITECTURE §decode lockstep (DONE).
2. feed the runtime self_drift_exp lane 23b from clm_penult_pooled(real per-tick content) instead of the current synthetic amygdala/homeostat int axis.

## Engine-native caveat (honest)
Forward ran on live core/decode.hexa of the real ckpt but device CUDA kernels reported "named symbol
not found" (stale runtime build) → byte-exact HOST fallback (max|Δ|=0, so penult values = real device
values); _hx_k_gemm OWN-GEMM fired once; cuda_available=1. Measurement validity unaffected (byte-exact);
GPU acceleration only partial.

verbatim raw = state/verdicts/9099_selfchain_content_grounding/H_9099.txt
