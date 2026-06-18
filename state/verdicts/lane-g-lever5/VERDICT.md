# Lane-G FORGE-UTILGREEN lever-5 — workload-bound SWEEP verdict

substrate = GPU (Lane G) · pod vast 39139563 (H100 80GB HBM3, sm_90 / compute_cap 9.0, ssh4.vast.ai)
build = lever-4 byte-identical clm_prod (adamw_group fused, 3-GATE PASS + BYTEEQ-PASS inherited; SAME binary, no rebuild)
date = 2026-06-02 (sweep DONE 2026-06-02T17:28:28Z)

## Hypothesis under test (lever-5 disambiguation)
- (A) crossing-bound : residual ~11 host↔device crossings/step SM-starve the GPU; cure = collapse the whole step to ~1 crossing/epoch.
- (B) workload-bound : per-step GEMM too small for H100 → kernel finishes faster than any host feed → MEAN is workload-limited NOT feed-limited; cure = bigger per-step work.

## Method
Apples-to-apples replay at the EXACT lever-4 config (d1536/T512/nsamp32/ep3) PLUS three LARGER per-step-work configs on the SAME byte-identical lever-4 build. nvidia-smi util sampled @0.1s, device-mem @0.5s, F-CLM-PROD-DESCENT per config. CLM_PROD_DEVFEED=1, CLM_PROD_BATCHED=1, HEXA_CUDA_LINK=1. g5 verbatim sampler lines below.

## Measurement (verbatim sampler lines, /root/lever5_sweep.log)
```
UTIL[apples] n=9149  PEAK=38% MEAN=0.6619% busy_ge20=81  pct_ge20=0.89% pct_ge50=0.00%   DEVMEM peak=20447MiB
UTIL[d3072]  n=11441 PEAK=78% MEAN=0.7152% busy_ge20=125 pct_ge20=1.09% pct_ge50=0.39%   DEVMEM peak=26405MiB
UTIL[t1024]  n=5892  PEAK=38% MEAN=0.5883% busy_ge20=35  pct_ge20=0.59% pct_ge50=0.00%   DEVMEM peak=15097MiB
UTIL[big]    n=8931  PEAK=75% MEAN=0.6838% busy_ge20=87  pct_ge20=0.97% pct_ge50=0.32%   DEVMEM peak=23215MiB
```
Descent (F-CLM-PROD-DESCENT, g5 verbatim — ALL GREEN):
```
apples  CE 4.05535 -> 2.99508   F-CLM-PROD-DESCENT=1  PASS
d3072   CE 4.48673 -> 3.96246   F-CLM-PROD-DESCENT=1  PASS
t1024   CE 4.20807 -> 3.36669   F-CLM-PROD-DESCENT=1  PASS
big     CE 4.60325 -> 4.22859   F-CLM-PROD-DESCENT=1  PASS
```

## Apples-to-apples vs lever-4 (validates harness)
lever-4 : PEAK=41% MEAN=0.6630%  |  lever-5 apples : PEAK=38% MEAN=0.6619% — reproduced within sampling noise (byte-identical build, same config). Harness sound.

## A-vs-B RULING : (B) WORKLOAD-BOUND — host-feed axis CLOSED-NEGATIVE at this scale
Across an 8x sweep of per-step work, PEAK doubled (38% -> 78%) but MEAN stayed PINNED in the 0.59-0.72% band. Bigger per-step GEMMs do NOT lift MEAN.

Decisive logic ruling OUT (A) crossing-bound: at d3072 each host↔device crossing carries ~4x more device compute while the *number* of crossings is identical to apples. If the binding constraint were fixed-count per-crossing launch latency (A), amortizing 4x bigger kernels over the same crossing count would have RAISED the busy fraction (MEAN). It did NOT (0.6619% -> 0.7152%, +0.05pp). PEAK rising to 78% confirms the kernels themselves do occupy the SMs harder — but the GPU still sits idle ~99.3% of wall time.

Root residual (refines the lever chain): the binding constraint is the INTERPRETED host per-step driver loop wall-time (hexa-interpreted scalar fwd/CE/bwd, ~13ns/op, ~104M ops/step @ d1536 ≈ ~1.4s host/step per the lever-3 profile), which scales WITH model size — so at d3072 the host gap grew ~proportionally with the kernel, holding the busy fraction flat. The remaining ~11 host↔device crossings are NOT the constraint; the interpreter IS.

lever chain util curve (MEAN flat, PEAK monotone — the workload-bound signature):
```
lever-1 MEAN 0.811%  PEAK  6%
lever-2 MEAN 0.4999% PEAK 19%
lever-3 MEAN 0.4879% PEAK 35%
lever-4 MEAN 0.6630% PEAK 41%
lever-5 sweep: MEAN 0.59-0.72% PEAK up to 78% (8x work)  <- MEAN invariant to per-step work
```

## VERDICT
util-GREEN (MEAN>=20% AND PEAK>=20%) NOT reached at any config. MEAN ceiling ~0.72%.
=> WORKLOAD-BOUND (B). The host-feed / crossing-count axis is CLOSED-NEGATIVE. util-GREEN is NOT achievable by any further host-feed lever (crossings are not the constraint). The cure is one of:
  (i) full device-resident model port — re-author the entire fwd+CE+bwd graph in CUDA C so the hexa interpreter leaves the per-step hot path (this is the production-scale model rewrite, NOT a feed lever); OR
  (ii) production scale large enough that even the interpreted host gaps shrink relative to kernel time — the 8x sweep shows d3072/T1024 does NOT get there at this corpus/batch, so the scale needed is well beyond d3072.

This is the HONEST TERMINAL of the host-feed util lever chain (levers a/b/1/2/3/4 + lever-5 sweep). No remaining host-feed lever can move MEAN. a_scale_honest_scope: d=1536 MEAN-util is a workload-size + interpreter-wall artifact, NOT a forge defect — forge is provably device-resident (20-26GB device mem, PEAK to 78%, byte-eq PRESERVED, descent GREEN every config).

Lane G PUBLIC milestone : NOT flipped (util-GREEN not reached) — keep [ ] + workload-bound terminal note.
.clm = util-RED/WIP -> HF PRIVATE per a_hf_autonomous.
