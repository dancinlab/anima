# clm-v1-dev-mid-d1536-t512-util-probe

CLMConvMoE **d1536 / T512** (int4-QAT) trained by the **hexa-native flame+forge**
stack on a **CUDA-devel B200** — the Lane-G (GPU) mid-scale rung en route to 3B.
The forge device path compiled + linked the full cuBLAS + CUDA-driver stack
(4 cuda libs: cublas + cudart + libcuda) and ran device-resident, but the
util-GREEN gate was **NOT** cleared: util stayed RED, host-backward-feed bound.

## Origin

- Trainer: `stdlib/flame/clm_prod.hexa` (PR4 + CLM_PROD_T perf-lever), authored
  in `.hexa` on stdlib/flame, run via the self-hosted hexa compiler with the
  forge cuBLAS link engaged.
- Corpus: 5-lang (en·zh·ru·ja·ko) semantic backbone + multilingual dialogue,
  402 KB byte-stream, byte-vocab V=256 (`clm_mid_5lang_c4.txt`).
- Config: **d=1536, E=2, T=512, K=3**, int4-QAT envelope. The completing-run
  artifact = 2 epochs × 8 windows (16 steps); the util characteristic is
  identical to the 6-epoch × 32-window big-run (host-bound, step-independent).
- Substrate: forge `forge_dispatch_matmul` → cuBLAS on the B200 (the conv1d
  forward + backward GEMMs ride cuBLAS via im2col/col2im).

## Falsifiers

- **F-CLM-PROD-DESCENT**: real-corpus mean CE strictly descends.
  Result: epoch-1 = 4.40933 → epoch-2 = 4.02596 (F=1). 🟢 GREEN —
  "PASS — real-corpus mean CE descends under int4 envelope" (verbatim).
- **F-RFC046 (util)**: target = forge util clears 20% (GPU saturated).
  Measured live on the B200:
  - completing-run: n=1102, PEAK=6%, MEAN=0.240%, pct_gt20=0.00%.
  - big-run (d1536/T512/32win/6ep): n=6783, PEAK=4%, MEAN=0.240%, pct_gt20=0.00%.
  GPU drew 196.69 W (vs ~141 W idle), SM 1965 MHz, ~66 GB device memory — forge
  PROVABLY on the GPU (4 cuda libs linked) — but util 🔴 **RED**.

## Why RED (honest)

The perf lever (window length T 24→512, lifting M of every conv GEMM 21×) plus
the scale-up (d 768→1536) did **not** move util: PEAK 5%→4-6%, MEAN 0.145%→0.240%
— essentially flat. The binding bottleneck is the **host-backward feed**
(host im2col/col2im + adam + the interpreted-compiled per-step loop), which pegs
one CPU core at 100% while the cuBLAS GEMMs — even at M=512 / d=1536 — finish in
microseconds and the SMs idle between launches. The residual is **host-feed, not
scale**: raising M and raising d both failed to saturate the device.

## Gate disposition

- closure = **FAIL on util** (util RED, descent GREEN) → **PRIVATE** per
  a_hf_autonomous. NOT PUBLIC-grade. 3B is **NOT yet throughput-justified**:
  a bigger model would idle the GPU more, not less, until the host feed is
  moved on-device (device-side im2col/col2im + device-side adam + fused/batched
  per-step GEMMs eliminating the host roundtrip).

## Substrate

- GPU: NVIDIA **B200** (183 GB), driver 580.126.09, CUDA-devel 12.4.1.
- Compiler: hexa self-hosted, rebuilt from `fix/hexa-run-cuda-link` source
  (cuda_link_decision + the new HEXA_CUDA_ARCH override). `HEXA_CUDA_ARCH=90`
  forced sm_90 PTX (the B200's sm_100 is newer than CUDA-12.4 nvcc can target;
  sm_90 runs on the B200 via driver JIT) — without it the cuda link silently
  degraded to CPU-only.
- Substrate tag: **GPU / Lane-G** (a_lane_akida_gpu_split — recorded separately
  from AKIDA / Lane-A; never merged).

## Caveats

- d1536 mid-scale rung on a 402 KB byte corpus (toy-vocab); validates the forge
  GPU throughput path + the util ceiling, NOT a production-scale LM.
- int4-QAT envelope; CE is under the quantized envelope (deterministic measure
  track, not the non-deterministic AKIDA identity lane).
- completing-run artifact = 2ep × 8win (the 6ep × 32win big-run gives the same
  util; only the saved .clm differs in step count).
- B200 sm_90-via-JIT (HEXA_CUDA_ARCH=90) — a real H100 (sm_90 native) is the
  recipe's reference card; the util ceiling is host-bound, card-independent.

## Composability

- Lane-G mid-d1536 = the PUBLIC-grade rung GATE on the 3B → 7B ladder
  (a_train_flame_forge). The .clm format mirrors `clm_ckpt.hexa` (6 int4 conv
  blocks, MAGIC "CLM\x01") and composes with anima serving / KOSMOS persistence.
- 3B is unblocked ONLY after the host-backward feed is moved on-device — until
  then a bigger model idles the GPU more, not less.

## .clm format

6 int4 conv blocks (ecW/tcW/e0W/e1W/rW/roW), MAGIC "CLM\x01", mirrors
`clm_ckpt.hexa`. sha256 = 3f62c53f3c216eca996e625aadff5c43955f7248025508a88712ffce89c96a1a.
