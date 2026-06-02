---
license: other
tags:
  - clm
  - clmconvmoe
  - lane-g
  - forge-gpu
  - util-probe
  - negative-result
library_name: hexa-flame
---

# clm-v1-dev-d1536-lever3-util-probe

CLMConvMoE (d=1536 / T=512, int4-QAT, LCG init, from-scratch) trained by the
**hexa-native flame+forge** trainer (`stdlib/flame/clm_prod.hexa`) on the H100
forge GPU substrate (**Lane-G**, `a_lane_akida_gpu_split` — NEVER merged with the
AKIDA on-chip Lane-A). NOT a PyTorch/ATen model — compiler-only NN, cuBLAS
`Dgemm`/`DgemmStridedBatched` on `nvcc -x cu`-compiled device kernels.

## Status: PRIVATE — closure-FAIL on util (descent GREEN / util RED)

This is the **lever-3** rung of the FORGE-UTILGREEN campaign (drop the dominant
65% batched-expert host repack via batched transpose-aware GEMM-feed,
`cublasDgemmStridedBatched` `CUBLAS_OP_T`).

| metric | verdict |
|---|---|
| `F-CLM-PROD-DESCENT` | **1 🟢 GREEN** — CE 4.05535 → 3.45564 (2 epochs × 32 windows, c4 5-lang corpus 402270 B, V=256, T=512) |
| `F-RFC046-GPU-UTILIZATION` | **🔴 RED** — PEAK=35% MEAN=0.4879% n=6868 busy_mean=5.3445% pct_ge20=0.1019% |
| byte-eq (all gates) | **max\|Δ\|=0.0** PRESERVED — `F-RFC046-GEMMFEED-EQ` · `F-RFC046-BATCHED-GEMMFEED-EQ` · `F-CLM-DEVFEED-*` · `F-CLM-CONV2-BATCHED-*` |

**util-GREEN (≥20% PEAK+MEAN) NOT reached.** lever progression (all on H100 sm_90,
forge provably on GPU — 4 cuda libs, power 115W vs 70W idle):

```
lever-1 (im2col→device)      MEAN 0.811%
lever-2 (bt/atb GEMM)         MEAN 0.4999%  PEAK 19%
lever-3 (batched bt/atb)      MEAN 0.4879%  PEAK 35%   ← this rung
```

PEAK rose (19→35%) but **MEAN essentially flat** — the device-feed lever chain
(a+b+2+3) is **necessary but insufficient**. The util-RED residual is NOT the GEMM
repack (now fully on device, byte-eq). It is the **interpreted per-step driver
loop** (the `clm_prod` host orchestration `while step<=steps` + 20× separate
`_adam` calls + glue) — the lever-4 target (fused on-device per-step driver,
~30→~2 host↔device boundary crossings/step). Closed-negative: scale/link/kernel/
emit/GEMM-feed all ruled out; the bottleneck is the host driver loop.

## Build (reproducible)

- H100 80GB HBM3 sm_90 · `nvidia/cuda:12.4.1-devel-ubuntu22.04` · nvcc 12.4 · gcc/clang
- hexa-lang `lane-g/rfc046-lever3-batched-gemmfeed` (`a5d01f37f`)
- self-host rebuild (`tool/stage_build_hexa`) → `cuda_link_decision` baked in
- seeds + spliced `self/runtime.c` (levers a+b+2+3) · pre-emit `runtime_cuda.c` (bt/atb/batched GPU kernels + fwd-decls) · `HEXA_CUDA_LINK=1` build · `-lcuda` relink (driver API)
- `HEXA_CUDA_ARCH=90` · `CUDA_VISIBLE_DEVICES=0` (single driver)
- fire: `CLM_PROD_D=1536 CLM_PROD_T=512 CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1`

## Files
- `lever3_d1536_t512.clm` — 6 int4 blocks, `CLM\x01`, 14379581 B, sha256 `06e2dcf44c15b6df582e1f33f1be9accdde034007272715398c2cb307347470e`
- `util_samples.csv` · `train_lever3.log` · `build_cuda_link.log`

substrate=GPU · Lane-G · pod vast 39126604 (torn down post-recovery).
