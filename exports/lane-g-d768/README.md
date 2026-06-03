# anima-clm-d768-forge-gpu

CLMConvMoE d768 (int4-QAT) trained by the **hexa-native flame+forge** stack on a
CUDA-devel H100_SXM — the first Lane-G (GPU) checkpoint where forge's device path
actually compiled and linked the cuBLAS + CUDA-driver stack (vs the prior
bare-image fire that silently fell back to CPU at util 0%).

## Origin

- Trainer: `stdlib/flame/clm_prod.hexa` (PR4, CLMConvMoE + int4 QAT envelope),
  authored in `.hexa` on stdlib/flame, run via the self-hosted hexa compiler.
- Corpus: c4 5-lang parallel-semantic backbone (en · zh · ru · ja · ko),
  `stdlib/flame/testdata/clm_semantic_parallel.txt`, byte-vocab V=256.
- Config: d=768, E=2, 3 epochs × 8 windows, T=24, K=3 (the 12×16 variant is
  identical in the GPU-link path but host-bound-slow; the util finding is the
  same at any step count).
- Substrate: forge `forge_dispatch_matmul` → cuBLAS on the H100 (the conv1d
  forward + backward GEMMs ride cuBLAS via im2col/col2im).

## Falsifiers

- **F-CLM-PROD-DESCENT**: real-corpus mean CE strictly descends.
  Result: epoch-1 = 4.69893 → epoch-3 = 3.32540 (F=1). 🟢 GREEN — "PASS — real-corpus mean CE descends under int4 envelope" (verbatim).
- **F-RFC046 (util)**: target = forge util clears 0% / meaningfully busy (>20%).
  Measured on the live H100 during d768 training: PEAK=5% MEAN=0.145% over 352
  nvidia-smi samples (pct_gt20 = 0.00%). 🔴 RED.
  - NEW EVIDENCE vs the prior fire: forge IS on the GPU this time — the binary
    links cuBLAS+cudart+**libcuda** (driver API), GPU power = 132W (vs ~67W idle),
    SM clock = 1980 MHz, ~2 GB device memory allocated. The prior verdict
    ("forge=cuBLAS does NOT route the GEMM onto the GPU") is REFUTED.
  - True bottleneck (isolated): host-backward feed. The trainer pegs ONE CPU core
    at ~98% while the GPU idles — the d768/T=24 conv→im2col→cuBLAS GEMMs are
    microsecond-scale and latency-bound; host im2col/col2im + adam + the
    interpreted-compiled per-step loop dominate. F-RFC046 host-bound, confirmed.

## Substrate

- GPU: NVIDIA H100 80GB HBM3 (vast pod 39000300), driver 555.58.02.
- Image: `nvidia/cuda:12.4.1-devel-ubuntu22.04` (nvcc 12.4 + cuBLAS + clang 14).
- Compiler: hexa self-hosted, **rebuilt from source** (`tool/stage_build_hexa`)
  so `cuda_link_decision` (the forge GPU link path) is in the binary — it is
  absent from the prebuilt release. Links runtime_cuda.o (nvcc sm_90) + cuBLAS +
  cudart + cuda (driver API).
- Substrate tag: **GPU / Lane-G** (a_lane_akida_gpu_split — recorded separately
  from the AKIDA / Lane-A on-chip track; never merged).

## Caveats

- d768 single-block CLMConvMoE on the c4 5-lang fixture (toy-vocab byte corpus);
  this validates the forge GPU *throughput path*, not a production-scale LM.
- int4-QAT envelope; CE is under the quantized envelope (deterministic measure
  track, not the non-deterministic AKIDA identity lane).
- Util is the d768 measurement only; transfer to 3B/7B is the next ladder rung.

## Composability

- Lane-G d768 forge-GPU PASS is the throughput gate for the 3B → 7B ladder
  (a_train_flame_forge). Same `.hexa` trainer scales by raising CLM_PROD_D.
- The .clm format mirrors `clm_ckpt.hexa` (6 int4 conv blocks, MAGIC "CLM\x01");
  composes with the anima serving / KOSMOS persistence path.
