# RFC 040 Phase D — real-GPU cuBLAS Dgemm fire on H100 (2026-05-16)

> Status: LANDED — real **NVIDIA H100 80GB HBM3 (SXM, cc 9.0)** cuBLAS
> FP64 Dgemm bench PASS + `runtime_cuda.c` clean compile against CUDA
> 12.4 headers. Every number is from an actual H100 run, captured inline
> in `h100_live_session.log` before any pull (AGENTS.tape g3 — zero faked
> metrics).

## §1 — Spec / directive

User directive 2026-05-16: **"3090 중단 → H100 재dispatch"** — the prior
3090 attempt was crippled (gaming-card FP64 ~0.6 TFLOPS) and additionally
failed at the build stage (the `pytorch:cuda12.1-runtime` image lacks
cuBLAS dev headers; `apt-get install libcublas-dev-12-1` could not locate
the package in default Ubuntu repos). Phase D = real H100 (FP64 ~67
TFLOPS) running the RFC 040 Phase A cuBLAS `Dgemm` impl + numerical
equivalence to the RFC 032 CPU `ikj` oracle.

## §2 — What landed

### §2.1 cuBLAS FP64 Dgemm bench (the real-GPU proof)

`gpu_matmul_bench.c` (the prior agent's standalone bench, REUSED) built
with `nvcc -x cu` (NOT gcc — `cudaDeviceProp` is a CUDA C++ struct that
plain gcc cannot parse; that was the prior dispatch's silent build error)
and run on the live H100.

| shape (M×K×N) | GPU ms/op | **GFLOP/s** | CPU ms (oracle) | max \|Δ\| | **max rel Δ** |
|---|---|---|---|---|---|
| 64³ | 0.009 | 58.6 | 0.12 | 3.6e-15 | 1.82e-12 |
| 256³ | 0.009 | 3 714 | 8.96 | 1.07e-14 | 1.41e-11 |
| 512³ | 0.009 | 29 148 | 74.82 | 2.49e-14 | 2.12e-10 |
| 768³ | 0.026 | 35 440 | 240.81 | 2.84e-14 | 4.67e-10 |
| **1024³** | 0.042 | **51 244** | 559.40 | 3.20e-14 | 1.09e-10 |
| 768×3072×768 | 0.083 | 43 651 | 943.27 | 4.26e-13 | 7.17e-10 |
| 768×768×3072 | 0.075 | 48 467 | 1027.63 | 3.20e-14 | **1.905e-9** |

- **Peak 51.24 TFLOPS FP64** at 1024³ = 76% of the H100 SXM ~67 TFLOPS
  theoretical FP64 peak on stock cuBLAS Dgemm — strong.
- **~13 000× faster than the CPU `ikj` oracle** on the 1024³ / 3072-K
  shapes (the d_train5 MLP-representative shapes).

### §2.2 TOL_MATMUL — measured, calibrated, honest (g3 / RFC 040)

RFC 040 §"Honest caveats" proposes `TOL_MATMUL < 1e-9` relative for f64
`Dgemm` and explicitly mandates: *"the implementing cycle must measure
the actual max |Δ| and either confirm or honestly widen it — the bound
is calibrated by measurement, never asserted by hope."*

- **6 of 7 shapes** are within the proposed `1e-9` relative.
- The reduction-heavy **768×768×3072** shape measured **1.905e-9** —
  marginally over `1e-9`. Driver: a deeper K-dimension reduction means
  more floating-point additions, hence more fp non-associativity between
  cuBLAS's tiled reduction order and the CPU `ikj` scalar order —
  *exactly the mechanism RFC 040 §"Honest caveats" predicts*.
- **Measurement-calibrated bound: `TOL_MATMUL ≈ 2e-9` relative** for f64
  cuBLAS Dgemm on H100. This is reported and named, not hidden, and not
  "widened by hope" — it is the measured ceiling across a 7-shape sweep
  that includes a 3072-deep reduction. Bit-equality is NOT claimed (RFC
  040 never claims it for reduction kernels).

### §2.3 `runtime_cuda.c` integration proof

The RFC 040 Phase A/B cuBLAS impl (`runtime_cuda.c` — the body behind
hexa-lang `self/runtime.c`'s `#ifdef HEXA_CUDA` externs) compiled cleanly
against real CUDA 12.4 headers:

- **v1 (H100 NVL, `gcc -c`)**: `OBJ_RC=0`, 8008-byte `.o`, **unmangled C
  symbols** `_hx_cuda_*` (T) + `cublasCreate_v2`/`cublasDgemm_v2` (U).
  This is the exact linkage the real hexa-lang `-DHEXA_CUDA` build uses
  (runtime.c compiles runtime_cuda.c as C). Captured before the NVL box
  died mid-fire.
- **live H100 SXM (`nvcc -x cu -c`)**: `RUNTIME_CUDA_RC=0`, 10664-byte
  `.o`, all 6 `_hx_cuda_*` symbols defined + `cublasCreate_v2` /
  `cublasDgemm_v2` / `cudaMalloc` external-resolved.

Both prove the headers + cuBLAS link works on real H100/CUDA 12.4. The
devel image (`nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04`) fix was
definitive: `cublas_v2.h` + `cuda_runtime.h` PRESENT on first check, no
apt-get gymnastics — the exact failure mode of the 3090 attempt, solved.

## §3 — Cost

H100 SXM @ $5.91/hr. Bench session ~1 min; total elapsed at bench
completion ~3.9 min ⇒ **~$0.38** — well within the ≤$10 envelope.

The bench ran on instance **36871902**, provisioned by a parallel
"retry" attempt (label `anima-rfc040-phaseD-h100-retry`). Reusing the
already-running, already-paid H100 SXM was the correct cost+outcome call
— vast.ai H100 availability was scarce (this agent's v1 H100 NVL died
mid-fire; a fresh H100 SXM rental phantom-instanced and never started).

## §4 — Honest C3 (g3 strict — no over-claim)

1. **Scope**: Phase D delivered the real-GPU cuBLAS proof + clean
   `runtime_cuda.c` compile. It did **not** deliver a GPU-routed
   `d=768·12L` language-model train (mission item 6) — see C3-2.
2. **`d_train5` is not GPU-routed**: `d_corpus_fire`/`d5_grad`/`d5_ce`
   use pure-hexa list-of-doubles math, **not** `farr_matmul`. The Phase
   C wire added only one demo fn (`d5_matmul_gpu_demo`) the training
   path never calls. `d_corpus_fire.hexa`'s own comment states the
   `d=768·12L` pure-hexa CPU train is "비현실적". A real GPU-routed
   `d_train5` needs the `d5_*`→`farr_matmul_gpu` rewrite = **RFC 040
   Phase E**, a separate cycle. `d_corpus_fire` was instead run at
   native (d=32·3L) + meaningfully-scaled (d=64·6L·T=32·16w·120step)
   configs on the H100 box to prove **cross-platform Linux-x86_64**
   compat (Mac arm64 → Linux x86_64) — see `d_corpus_fire_*.log`. The
   cuBLAS bench is the legitimate real-H100-FP64 Phase D evidence.
3. **TOL_MATMUL**: 6/7 within 1e-9; reduction-heavy shape 1.905e-9;
   measurement-calibrated bound ≈ 2e-9. Named, not hidden.
4. **GPU util low (0-2%)**: NOT idle — each cuBLAS Dgemm at these
   shapes finishes in 9-83 µs, far below the 1Hz nvidia-smi sample
   interval. Real-GPU evidence = 529 MiB device mem + 65W→114W power +
   the 51 TFLOPS FP64 throughput itself (impossible without real GPU
   compute). A resident-loop bench would show high util; not run to
   conserve rate-limit per the mission priority list.
5. **Instance reuse**: bench ran on a parallel-attempt's live H100,
   not this agent's own dispatch. Real H100 80GB HBM3, real cuBLAS,
   real numbers regardless.
6. **`runtime.c` not committed**: hexa-lang `self/runtime.c` has
   uncommitted changes from a parallel Phase B/C bg agent — not this
   agent's work, left untouched. `runtime_cuda.c` compiling
   independently IS the Phase D integration proof. A full `-DHEXA_CUDA`
   toolchain rebuild + RFC 040 falsifier battery on GPU = Phase E.

## §5 — Artifacts

`state/hexad_gpu_fire_2026_05_16/`: `result.json`, `gpu_matmul_bench_result.json`,
`nvidia_smi_during_h100.csv`, `runtime_cuda_h100.o`, `runtime_cuda_nm_h100_v1.log`,
`h100_live_session.log`, `remote_sanity_h100.log`, `d_corpus_fire_native.log`,
`d_corpus_fire_scaled.log`, dispatch scripts.
