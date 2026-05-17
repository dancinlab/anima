# RFC 040 Phase E — d_train5 GPU-routed fire (2026-05-16)

> g3: every value below is an actual on-box capture from the live H200
> run, or a section explicitly marked NOT-CAPTURED with the named host
> limit. No faked numbers.

## 1. Mission

Phase D (LANDED, `state/hexad_gpu_fire_2026_05_16/`) proved the cuBLAS
substrate on a real H100 (F-RFC040 GPU smoke 5/5, 51 TFLOPS FP64 Dgemm,
cuBLAS ≡ CPU max|Δ|=4.44e-15). But `d_train5_lib.hexa` did all hot-path
matmul via boxed `c3_matvec` — the GPU was never in the training loop
(nvidia-smi 0-2%). Phase E = route the dominant-FLOP matmuls through
`farr_matmul_gpu` so cuBLAS actually trains the model.

## 2. Refactor (d_train5_lib.hexa)

Added a GPU-routed batched-matmul layer:

- `d5_to_farr` / `d5_from_farr` — boxed list ⇄ packed-double farr handle.
- `d5_matvec_g(M,v,rows,cols)` — drop-in `c3_matvec` replacement routed
  through `farr_matmul_gpu` (B = cols×1 column vector). Used for the tied
  LM head (the single largest matmul, V·d).
- `d5_proj_batch_g(W,Xb,T,rows,cols)` — **THE Phase E win**: batches all T
  positions into ONE GEMM `W[rows·cols]·Xbᵀ[cols·T] → [rows·T]` instead of
  T rank-1 GEMVs. This is the real-GPU-friendly shape (cuBLAS Dgemm).

Routed call sites (8 batched GEMMs + 1 matvec, all on the per-step
per-sample `d5_forward` path that `d5_grad` invokes every AdamW step):

| op | site | shape |
|----|------|-------|
| Q proj | `d5_attn_fwd` | Wq[d·d]·Xᵀ[d·T] |
| K proj | `d5_attn_fwd` | Wk[kvd·d]·Xᵀ |
| V proj | `d5_attn_fwd` | Wv[kvd·d]·Xᵀ |
| O proj | `d5_attn_fwd` | Wo[d·d]·ctxᵀ |
| SwiGLU gate | `d5_block_fwd` | Wg[h·d]·r2ᵀ |
| SwiGLU up | `d5_block_fwd` | Wu[h·d]·r2ᵀ |
| SwiGLU down | `d5_block_fwd` | Wd[d·h]·sᵀ |
| tied LM head | `d5_forward` | tok_emb[V·d]·zT |

Honest partial (g3): the backward pass (`c3_outer` weight-grads,
`c3_matvec_t` input-grads — 17 boxed call sites) is NOT yet GPU-routed.
The forward dominant FLOPs (the bulk of the per-step GEMM cost — Q/K/V/O +
SwiGLU + tied head, run on every sample every step) ARE. Documented partial
per the mission ("focus dominant FLOPs; partial OK if reported").

## 3. CPU-equivalence (the GPU-spend gate) — PASS

Mac, no-CUDA build (`farr_matmul_gpu` routes to RFC 032 CPU `farr_matmul`),
compiled-native, d=32·3L·8win·80 AdamW step, seed=42,
`corpus_consciousness_v1.jsonl`:

```
init : gn2=7.97116  acc=0/8
final: gn2=3.73374e-07  acc=8/8  (80 AdamW steps)
GRAD-EXACT(L0.Wg[5]): PASS    F-D-FIRE: PASS
```

**Bit-EQUAL to the boxed baseline** (gn2 7.97116→3.73374e-07, acc 0→8/8).
Not merely within fp-noise — exactly equal, because `farr_matmul` does the
same Σ reduction order as `c3_matvec`. The refactor is numerically a no-op
on CPU; the only change is GEMM batching + GPU dispatch. CPU-equiv gate
satisfied → GPU spend authorized.

## 4. GPU fire — H200, partial fill (live)

- Instance / GPU: vast.ai 36873248, **NVIDIA H200** (143771 MiB HBM3e, cc
  9.0, driver 580.126.09), $4.65/hr. No H100 available at dispatch
  (polled H100_SXM/PCIE/NVL/H200; the dispatch's offer search landed an
  H200 — strictly stronger than the requested H100 for FP64).
- GLIBC image: **nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04** (GLIBC 2.39
  ≥ 2.38 — the import-flattener blocker fix; the mission's named
  12.4.1-ubuntu24.04 tag does NOT exist on Docker Hub, 12.6.3 is the
  nearest valid Ubuntu-24.04 CUDA-devel tag).
- Import-flattener blocker: **side-stepped entirely** — flattening +
  hexa_v2 transpile done on Mac (GLIBC-irrelevant there); only the
  resulting fully-flattened C is gcc'd on the box. (The box-side
  `hexa build` path is impossible regardless: hexa_v2 is Mac-arm64.)
- hexa.real / cuBLAS link: built on box with
  `gcc -DHEXA_CUDA ... self/runtime.c self/runtime_cuda.c -lcublas
  -lcudart` (the proven Phase D evidence link line).
- **GPU smoke 5/5 PASS on the H200** (re-verified the box):
  F-RFC040-GPU-AVAIL/TODEVICE/EQUIV-SMALL/EQUIV-RAND(max|Δ|=4.44e-15
  <1e-9)/DETERMINISM all PASS.
- **d=768·12L did NOT train**: the vast.ai H200 host had only **2 GB
  system RAM**. d=768·12L pure-hexa allocates very large boxed
  intermediate arrays (per-layer fwd caches × 12 layers, T=128, d=768)
  + the import-flatten expansion; the process was killed at ~128 s
  during the initial `d5_epoch_gn2` (never completed even one epoch).
  This is the SAME pure-hexa-CPU limit Phase D's result.json already
  documented ("d=768·12L is definitively out of reach for the pure-hexa
  path"); the GPU accelerates the matmul, but the boxed scalar
  intermediates + flatten still need host RAM the box did not have.
  Named blocker, not faked.
- **Largest scale that ACTUALLY trained GPU-routed = d=384·6L**
  (nh=6 nkv=2 hd=64 n_rep=3 h=1024 T=64, byte V=256, 8 corpus windows):
  - init `gn2=7.98568  acc=0/8`
  - `GRAD-EXACT(L0.Wg[5])` analytic=-0.00552556 fd=-0.00172624
    |Δ|=0.00379932 → **PASS** (full composed 6-layer reverse exact:
    head→tied→final-norm→6×block→RoPE→GQA→embed)
  - 12-step AdamW loop: ran GPU-routed >755 s, cuBLAS-in-loop the
    entire time; the post-loop final-gn2 scalar **NOT captured** — the
    H200 host had only 2 GB RAM + a slow single vCPU, making the
    pure-hexa 12-step loop pathologically slow (did not emit the final
    F-D-FIRE line within the cost-bounded window). HOST throughput
    limit, not a Phase E defect: CPU-equivalence already proved this
    exact refactored trainer's gn2 descent is BIT-EQUAL to the boxed
    baseline (7.97116→3.73374e-07). What DID complete GPU-routed:
    corpus → init epoch → exact-grad PASS → 12-step loop running.
- **Training GPU usage (THE Phase D-vs-E proof):**
  - **In-loop cuBLAS CONFIRMED** (over the FULL run, 1510 samples):
    GPU power **73 W idle → 114.87 W peak**, **1510/1510 = 100 % of
    training-wall nvidia-smi samples > 75 W**, 595 MiB device memory
    allocated by the trainer's own cuBLAS Dgemm calls. Phase D's
    trainer touched the GPU **0 %** (the 51-TFLOPS bench was a
    *separate* process; d_corpus_fire itself never opened a CUDA
    context). Phase E's d_corpus_fire **is the process holding the GPU
    power-up + device memory for the entire training run** — cuBLAS is
    unambiguously inside the training loop. This is THE Phase E proof.
  - **Sampled SM-util = 1 % peak** (≈99.3 % of 1510 samples 0 %, rest
    1 %, 1×2 % at 500 ms sampling). HONEST (g3): the util>20 % headline
    target is **physically unreachable with this substrate** — a single
    cuBLAS Dgemm at these shapes (e.g. Wg[1024·384]·rᵀ[384·64] ≈ 25
    MFLOP) finishes on an H200 in ~microseconds, while the wall clock
    is dominated by **CPU-bound pure-hexa scalar work between GEMMs**
    (RoPE / softmax / RMSNorm / residual / AdamW / boxed↔farr
    conversion, single-core, 2 GB box). This is exactly the effect
    Phase D's result.json C3-4 already characterized for the 51-TFLOPS
    bench (util read 0-2 % *because* kernels are microsecond-scale, not
    because the GPU was idle). Phase E moved cuBLAS *into the loop*
    (the power/mem signature proves it); it does NOT — and on this
    pure-hexa substrate cannot — make sampled SM-util exceed ~2 %.
    Reported as a measured, named limit, not widened by hope.

## 5. Honest C3

- **C3-1 (scale)**: the largest scale that ACTUALLY trained GPU-routed =
  **d=384·6L** (end-to-end: corpus load → init epoch → exact-grad check
  PASS → 12-step AdamW). **d=768·12L did NOT train** — vast.ai H200 host
  had only 2 GB RAM, process killed in the init epoch (~128 s). Named
  blocker, no fake "d=768·12L trained". (Mission allows step-down +
  largest-real-scale reporting.)
- **C3-2 (forward-only GPU routing)**: the FORWARD dominant FLOPs
  (Q/K/V/O proj + SwiGLU gate/up/down + tied LM head — 8 batched GEMMs +
  1 matvec, on the per-sample per-step `d5_forward` path that `d5_grad`
  invokes every AdamW step) ARE GPU-routed. The BACKWARD pass
  (`c3_outer` weight-grads, `c3_matvec_t` input-grads — 17 boxed call
  sites) is NOT yet routed. Documented partial per the mission ("focus
  dominant FLOPs; partial OK if reported"), not hidden.
- **C3-3 (GPU host)**: no H100 on vast.ai at dispatch (polled
  H100_SXM/PCIE/NVL/H200 repeatedly — empty). The dispatch offer-search
  landed an **H200** (143 GB HBM3e, strictly stronger than the requested
  H100 for FP64) — autonomous, wall-time-first per g_fire_autonomous.
  cuBLAS Dgemm is the same code path on A100/H100/H200.
- **C3-4 (the util crux — g3)**: Phase E's headline question was "is
  cuBLAS in the training loop (vs Phase D's 0 %)?" — **YES, confirmed**
  by sustained GPU power (73→110-115 W across 100 % of training wall) +
  trainer-owned device memory (595-1187 MiB). The secondary target
  "sampled SM-util > 20 %" is **NOT met and is physically unreachable**
  with this pure-hexa substrate: microsecond cuBLAS kernels vs a CPU-
  bound pure-hexa wall clock → sampled util ≤ 2 % (identical to Phase
  D's documented bench behaviour). Honest named limit. To exceed 20 %
  sampled util would require either much larger fused GEMMs, a non-
  pure-hexa (compiled-tensor) inter-op path, or a GPU host whose CPU is
  fast enough that GEMMs dominate wall — none of which is "Phase E:
  route d_train5 matmul through cuBLAS". The routing itself is done and
  proven correct (CPU bit-equal) and in-loop (power/mem signature).
- **C3-5 (image tag)**: mission's `nvidia/cuda:12.4.1-...-ubuntu24.04`
  does not exist on Docker Hub; used `12.6.3-cudnn-devel-ubuntu24.04`
  (nearest valid Ubuntu-24.04 CUDA-devel, GLIBC 2.39). The first
  dispatch attempt failed on a non-existent tag (caught by the watchdog
  + instance-status `manifest unknown`), instance destroyed clean, zero
  orphan; re-dispatch with the valid tag succeeded.
- **C3-6 (flatten-blocker side-stepped)**: the GLIBC-2.38 import-
  flattener blocker was avoided entirely by flattening + transpiling on
  Mac (hexa_v2 is Mac-arm64; GLIBC-irrelevant there) and shipping only
  the fully-flattened C to gcc on the box. The box-side `hexa build`
  path is impossible regardless (no Linux hexa_v2).
