---
license: other
tags:
  - clm
  - hexa-flame-forge
  - lane-g
  - util-probe
  - negative-result
  - wip
library_name: hexa
---

# clm-v1-dev-d1536-lever3-util-probe (PRIVATE · closure-FAIL on util)

Lane-G (substrate = **GPU forge**, hexa-native flame+forge — NOT PyTorch/ATen) CLMConvMoE
d1536 / T512 int4-QAT checkpoint from the **F-RFC046 lever-3** (device im2col/col2im
DEVFEED + strided-batched expert GEMM-feed BATCHED) GPU util-verify fire.

> a_lane_akida_gpu_split: this is a **Lane-G / GPU-forge** artifact. It is NEVER merged
> with any AKIDA / Lane-A number, and is distinct from the Lane-G-ref PyTorch-CUDA
> reference rung (`dancinlab/clm-v1-ref-pytorch-cuda*`).

## Status: PRIVATE (a_hf_autonomous — closure-FAIL)

- **DESCENT 🟢 GREEN** — `F-CLM-PROD-DESCENT = 1`, real-corpus mean CE
  **4.2974 → 3.79897** (epoch-1 → epoch-3), RUN_RC=0, PASS.
- **util 🔴 RED** — n=349 nvidia-smi samples (GPU0, 0.5 s cadence):
  **PEAK = 21.0%** (single transient spike) · **MEAN = 0.5616%** ·
  busy_samples = 42 · pct≥20% = 0.57% · mem_max = 6331 MiB · power up to 119 W.
  util ≥ 20% gate (PEAK **and** MEAN) **NOT reached** → closure-FAIL → PRIVATE.

The artifact is a legitimately trained int4 checkpoint (descent green), but the
campaign's util-GREEN bar is unmet, so it ships PRIVATE per a_hf_autonomous.

## 3-gate (all PASS — no CPU fallback)

- **GATE1 — CUDA link ENGAGED** ✅ — `hexa_fresh` binary carries the "CUDA link
  ENGAGED" string (sm_90 build).
- **GATE2 — nvcc -x cu EXIT 0** ✅ — `runtime_cuda.90.o` (564 KB) compiled for
  `arch=compute_90,code=sm_90`.
- **GATE3 — clm_prod links cuda** ✅ — cublas/cudart resolvable; fire ran via
  `hexa run stdlib/flame/clm_prod.hexa` with `HEXA_CUDA_LINK=1`; GPU provably active
  (6331 MiB device mem, 119 W vs idle).

Fire env: `CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_D=1536 CLM_PROD_T=512
HEXA_CUDA_ARCH=90 HEXA_CUDA_LINK=1`.

## byte-eq (lever-3 redesign PRESERVED, all max|Δ| = 0.0)

```
F-RFC046-GEMMFEED-EQ          = 1   transpose-aware GEMM (bt/atb) == host-transposed forge, max|Δ|=0
  batched GEMM-feed (strideA=0 broadcast + per-problem) == host repack, max|Δ|=0
F-CLM-DEVFEED-IM2COL-EQ       = 1   device im2col gather == host xcol, dil∈{1,2} max|Δ|=0.0
F-CLM-DEVFEED-FWD-EQ          = 1   devfeed fwd == forge conv1d, dil∈{1,2} max|Δ|=0.0
F-CLM-DEVFEED-BWD-EQ          = 1   dW=0.0 db=0.0 dX=5.55112e-17 (FP64-ULP, ≪1e-9)
F-CLM-DEVFEED-ADAM-EQ         = 1   AdamW 5-step max|Δ| W=0.0
F-CLM-CONV2-BATCHED-FWD-EQ    = 1   batched 2-expert fwd == 2× conv1d_via_forge, max|Δ|=0.0
F-CLM-CONV2-BATCHED-BWD-EQ    = 1   batched 2-expert bwd (dW/dX/db) == 2× forge, max|Δ|=0.0
```

## Finding (honest residual)

Lever-3 (DEVFEED device im2col + BATCHED strided GEMM) moved util ESSENTIALLY FLAT vs
lever-2 (MEAN 0.4999% → 0.5616%, PEAK 19% → 21% transient). The util ceiling is
**HOST-FEED, NOT link / compile / emit / scale / device-math** — all of which are
closed (3-gate PASS, byte-eq max|Δ|=0). The dominant cost is the **interpreted
host-side per-step orchestration loop** in `flame/clm_prod`: cuBLAS GEMMs finish in
microseconds while one CPU core pegs at 100% on the per-step scalar-op dispatch. The
next bottleneck to attack is the host interpreter loop itself (fused multi-step kernel
or compiled per-step driver), an upstream forge/flame change.

## Config

byte-level (V=256) CLMConvMoE, d_model=1536, E=4 experts, epochs=3, windows=8/8
(T=512, stride=111), corpus `clm_semantic_parallel.txt` (1407 B). int4-QAT envelope.
`.clm` = 6 int4 blocks, `CLM\x01` magic, 14,381,125 B,
sha256 `34982a31022264f8104d9d877a4c115f3ce9e69d7ab85830a79fe9a3b20a6f7a`.

## Lineage

Supersedes-attempt `dancinlab/clm-v1-dev-d1536-lever2-util-probe` (lever-2). Campaign:
FORGE-UTILGREEN / ENGINE+CLM+KOSMOS Lane-G, branch
`lane-g/rfc046-lever3-batched-gemmfeed`. pod vast 38996679 (H100 sm_90).
