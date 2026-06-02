# clm-v1-dev-d768-devfeed-rc3-util-probe

Lane-G (substrate=GPU) d768 forge-cuBLAS fire with BOTH device-feed levers active
(`CLM_PROD_DEVFEED=1` lever-a + `CLM_PROD_BATCHED=1` lever-b) on a from-scratch
CLMConvMoE d768/int4-QAT model. This is the run that closed the THIRD Lane-G
util-RED root cause (the `runtime_cuda.c` emit fork-bomb recursion + large-content
write failure). **PRIVATE** — closure-FAIL on util (util-RED persists).

## §1 What

- model: from-scratch CLMConvMoE, d=768, int4-QAT (LCG init), 6 int4 blocks (`CLM\x01`)
- corpus: c4 5-lang backbone (`clm_mid_5lang_c4.txt`, 402270 B, V=256), 16 windows
- trainer: hexa-native `stdlib/flame/clm_prod.hexa` (PR4) — flame+forge, no PyTorch/ATen
- artifact: `d768_5lang_c4.clm` (3,651,389 B), sha256 `98094a5d47b701b407b70adc86b983bfd33c9cf33a2fa1e48c55a4813b631ffb`

## §2 Gates

- **F-CLM-PROD-DESCENT: PASS** 🟢 — epoch-1 mean CE = 4.88733 → epoch-3 = 4.87688
  ("PASS — real-corpus mean CE descends under int4 envelope", verbatim). d=768 E=2 epochs=3 nwin=16.
- **F-RFC046 util: RED** 🔴 — n=388 samples, PEAK=5% MEAN=0.784% pct_ge20=0.00%, peak dev-mem 3952 MiB.
  GPU provably LIVE (87W vs ~70W idle, ~3.7 GB device-resident) but SM-starved.

## §3 Substrate

- substrate: 1× NVIDIA RTX PRO 6000 Blackwell Workstation Edition (97887 MiB), CUDA 12.4 / nvcc 12.4 / cuBLAS, gcc 11.4, clang 14
- link: clm_prod links cublas + cudart + **libcuda** + cublasLt (4 cuda libs); `forge_dispatch_matmul_batched` + `forge_dispatch_adamw` present; CUDA-link-ENGAGED=1
- build: self-host rebuild of hexa from `laneg/devfeed-cudalink-integrated` (cuda_link_decision + lever-a/-b + nvcc fwd-decl #2506 + emit recursion/write fixes #3a/#3b), glibc-2.39 shim, HEXA_CUDA_ARCH=90, `-lcuda` relink
- pod: vast 39062745, wall ~few-min/run, cost ~$ (rent-cap #2507)

## §4 Finding

util-RED is NOT a link/compile/emit defect (all three fixed and verified). The
bottleneck is the host-side per-step orchestration: the trainer pegs ONE CPU core
at ~100% while the GPU idles (the F-RFC046 host-backward feed). The device-feed
levers made buffers device-resident (mem up to ~3.7–14.8 GB across configs) but did
NOT lift SM util above ~5–6% — confirming the residual is host-feed, not memory
residency or scale. The 3B/7B forge fire stays throughput-blocked.

## §5 Lineage

- lineage: Lane-G forge-GPU util campaign; supersedes-attempt `clm-v1-dev-d768-forge-gpu`
  (root cause #3 now fixed; same util-RED verdict re-confirmed with both levers + RC#3 fix)
- substrate split: GPU / Lane-G — NEVER merged with any AKIDA / Lane-A number (a_lane_akida_gpu_split)
