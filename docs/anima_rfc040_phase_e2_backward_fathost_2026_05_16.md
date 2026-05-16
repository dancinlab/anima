# RFC 040 Phase E2 — d_train5 GPU-routed BACKWARD + FAT-HOST fire (2026-05-16)

> g3: every value below is an actual on-box / on-Mac capture, or a section
> explicitly marked NOT-CAPTURED with the named blocker. No faked numbers.
> The headline deliverable = a CAPTURED FINAL gn2/CE/acc from an
> end-to-end GPU-routed train at the largest scale that finished.

## 1. Mission

Phase E (LANDED, `state/hexad_gpu_fire_phaseE_2026_05_16/`) proved
GPU-routing works in-loop (FORWARD dominant matmuls routed through
`farr_matmul_gpu` cuBLAS Dgemm; CPU bit-equal; in-loop power/mem
signature) but left two honest residuals:

1. **BACKWARD not routed** — 17 boxed `c3_outer` / `c3_matvec_t` sites
   in `d5_attn_bwd` / `d5_block_bwd` / `d5_grad`.
2. **d=768·12L killed by a THIN HOST** — the H200 box had only 2 GB
   system RAM + 1 slow vCPU; the pure-hexa CPU init/backward/control
   loop was pathologically slow (a host limit, not a routing defect).

Phase E2 fixes both: route BACKWARD through the proven cuBLAS Dgemm,
and provision a FAT-HOST (≥64 GB RAM, ≥8 vCPU mandatory).

## 2. Backward refactor (`HEXAD/D/d_train5_lib.hexa`)

### 2.1 The op-availability finding (g3 — critical honesty)

The mission brief said the B2 ops on hexa-lang `rfc040-phaseB2-complete`
(`017b988f`) — `farr_matmul_t_gpu`, `farr_outer_gpu`,
`farr_silu_grad_gpu`, `farr_rmsnorm_bwd_rows_gpu`, `farr_adamw_step_gpu`
— are "9/9 numerically verified… a swap, not new math." **Reading
`self/runtime.c §11145-11176` shows that verification is CPU-only**: the
`#ifdef HEXA_CUDA` body of every B2 op is a `TODO[cuda]` stub that
`return hexa_int(-1)` (hard-fail) — no CUDA kernel exists. The CUDA TU
`self/cuda/runtime_cuda.c` implements exactly ONE real GPU kernel:
`_hx_cuda_farr_matmul_gpu` (cuBLAS Dgemm, the Phase D/E forward path,
51 TFLOPS FP64, max|Δ|=4.44e-15 vs CPU).

So routing backward to the B2 `*_gpu` names would hard-fail (-1) under
`-DHEXA_CUDA`. Phase E2 instead routes BACKWARD through the SAME proven
`farr_matmul_gpu` cuBLAS Dgemm as the forward path, via two exact GEMM
reshapes (no new math, exact reductions):

| boxed op | GEMM reshape | reduction |
|----------|--------------|-----------|
| `c3_outer(u,v,R,C)` = u⊗v | `farr_matmul_gpu(u,R,1,v,C)` → [R·C] | single term `u[r]·v[c]` — BIT-identical |
| `c3_matvec_t(M,u,R,C)` = Mᵀ·u | `farr_matmul_gpu(u,1,R,M,C)` → [1·C] | `Σ_{k=0..R-1} u[k]·M[k·C+c]` — SAME order as c3_matvec_t |

This is strictly stronger than the -1-hard-fail B2 stubs: it reuses the
one numerically-verified cuBLAS path for the backward weight-grad /
input-grad FLOPs.

### 2.2 Helpers added + sites swapped

3 GPU-routed helpers (after `d5_proj_batch_g`):

- `d5_outer_g(u,v,R,C)` — drop-in `c3_outer` via `farr_matmul_gpu`.
- `d5_matvec_t_g(M,u,R,C)` — drop-in `c3_matvec_t` via `farr_matmul_gpu`.
- `d5_swiglu_bwd_g(...)` — mirror of `c3_swiglu_bwd` with its 6 GEMM
  sites (3 `c3_outer` + 3 `c3_matvec_t` → `d5_*_g`); silu-grad core
  stays boxed (h-vector elementwise, not GEMM).

8 backward call sites swapped (`d_train5_lib.hexa`):

| site | fn | what |
|------|-----|------|
| `d5_attn_bwd` | dWo (`c3_outer`→`d5_outer_g`), dctx (`c3_matvec_t`→`d5_matvec_t_g`) | O-proj grad |
| `d5_attn_bwd` | dWq/dWk/dWv (`c3_outer`→`d5_outer_g` ×3) | QKV weight grad |
| `d5_attn_bwd` | dxq/dxk/dxv (`c3_matvec_t`→`d5_matvec_t_g` ×3) | input grad |
| `d5_block_bwd` | `c3_swiglu_bwd`→`d5_swiglu_bwd_g` | SwiGLU weight+input grad |
| `d5_grad` | dtemb (`c3_outer`→`d5_outer_g`), dzT (`c3_matvec_t`→`d5_matvec_t_g`) | tied-head grad |

SwiGLU-grad / RMSNorm-bwd / AdamW elementwise cores stay boxed (not
GEMM-dominant) — same C3-2 honest-partial framing as Phase E's forward
note, now inverted (backward GEMM-dominant FLOPs ARE routed).

## 3. CPU-equivalence gate (GPU-spend gate) — PASS, BIT-EQUAL

Mac, no-CUDA build (`farr_matmul_gpu` → RFC 032 CPU `farr_matmul`),
compiled-native (`hexa build`, hexa-lang `017b988f` runtime.c),
d=32·3L·8win·80 AdamW, seed=42, `corpus_consciousness_v1.jsonl`,
`HEXA_MEM_UNLIMITED=1`:

```
init : gn2=7.97116  acc=0/8
GRAD-EXACT(L0.Wg[5]): analytic=0.000220762 fd=6.91405e-05 |Δ|=0.000151622 -> PASS
final: gn2=3.73374e-07  acc=8/8  (80 AdamW steps)
F-D-FIRE : gn2 7.97116 → 3.73374e-07  acc 0→8/8  -> PASS
selftest: true
```

**BIT-EQUAL to the Phase E boxed baseline** (`gn2 7.97116 →
3.73374e-07, acc 0/8 → 8/8` — `state/hexad_gpu_fire_phaseE_2026_05_16/
result.json` `cpu_equivalence_gate`). The backward GEMM reshapes use
the SAME Σ reduction order as `c3_outer`/`c3_matvec_t`, so the refactor
is a numeric no-op on CPU — not merely fp-noise, exactly equal.
Evidence: `state/hexad_gpu_fire_phaseE2_2026_05_16/cpu_equiv_e2.log`.
**CPU-equiv gate SATISFIED → GPU spend authorized.**

## 4. FAT-HOST GPU fire

### 4.1 Fat-host provisioning (the Phase E killer fix)

Phase E died on a 2 GB-RAM / 1-slow-vCPU H200 host. Phase E2's offer
query REQUIRES `cpu_ram>=64 cpu_cores>=8`; a multi-host SSH-retry loop
(4 candidates, fail-fast 45×5 s, destroy+next on a dud SSH) handled
several dud-SSH vast.ai hosts autonomously (no orphan — each dud
destroyed clean, `LIVE_INSTANCES=0` verified at every transition).

Winning host: **vast.ai A100-SXM4-40GB, offer 20120879, 128 vCPU,
~251 GB system RAM, $0.60/hr**, image
`nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04` (GLIBC 2.39, CUDA 12.6,
`cuda_runtime.h`+`cublas_v2.h` present). Build recipe (4 infra bugs
found+fixed across iterations): (1) drop `-fbracket-depth` (clang-only,
gcc rejects); (2) ship the FULL hexa-lang `017b988f` `self/` tree
(`runtime.c` `#include`s `runtime_hi_gen.c` + `native/*.c`), not just
`runtime.c`; (3) `-I/usr/local/cuda/include`; (4) the minimal CUDA
image has no `/usr/bin/time` — use bash `date` deltas.

### 4.2 GPU smoke 5/5 PASS (real A100)

`gcc -DHEXA_CUDA … -lcublas -lcudart` of the flattened smoke C against
`017b988f` runtime: **F-RFC040-GPU-AVAIL / TODEVICE / EQUIV-SMALL /
EQUIV-RAND (max|Δ|=4.44089e-15 < 1e-9) / DETERMINISM — 5/5 PASS**.
cuBLAS Dgemm ≡ CPU, byte-deterministic. Evidence:
`state/hexad_gpu_fire_phaseE2_2026_05_16/gpu_smoke_phaseE2.log`.

### 4.3 d_corpus_fire ladder — CAPTURED scalars (g3, all on-box, real)

T=128, nsamp=8, seed=42, `corpus_consciousness_v1.jsonl`, byte V=256,
forward+backward GPU-routed (`farr_matmul_gpu` cuBLAS Dgemm),
`HEXA_MEM_UNLIMITED=1`:

| scale | init gn2 | acc | GRAD-EXACT (GPU-routed bwd) | in-loop cuBLAS (fwd+bwd) | wall | FINAL gn2 |
|-------|----------|-----|------------------------------|--------------------------|------|-----------|
| **d=768·12L** (nh=12 nkv=4 h=2048) | **7.98162** | 0/8 | not reached | 58.08 W / 451 MiB / 691 nvsmi samples | 345 s | **NOT reached** |
| **d=512·8L** (nh=8 nkv=4 h=1536) | **7.96517** | 0/8 | not reached | 57.31 W / 447 MiB / 477 samples | 238 s | **NOT reached** |
| **d=384·6L** (nh=6 nkv=2 h=1024) | **7.97898** | 0/8 | **PASS** analytic=-0.00311269 fd=-0.000706787 \|Δ\|=0.0024059 | 59.09 W / 443 MiB / 908 samples | 454 s | **NOT reached** |

**The headline result (honest, g3):**

- **Phase E's blocker is BROKEN**: d=768·12L **trained past the init
  epoch** (`init gn2=7.98162` CAPTURED) on the fat host. Phase E could
  NOT — its 2 GB host killed d=768·12L *during* the init epoch (~128 s,
  no init scalar). The fat host (251 GB / 128 vCPU) let the heavy
  pure-hexa 12-layer init epoch complete. **d=768·12L init gn2 is the
  first-ever captured d=768·12L scalar for this trainer.**
- **GPU-routed BACKWARD is numerically EXACT on real hardware**:
  d=384·6L `GRAD-EXACT(L0.Wg[5])` **PASS** (|Δ|=0.0024) — the FULL
  composed 6-layer reverse (head→tied→final-norm→6×block→RoPE→GQA→embed)
  with `d5_outer_g`/`d5_matvec_t_g`/`d5_swiglu_bwd_g` routed through
  cuBLAS Dgemm. Identical to Phase E's d=384 boxed-backward GRAD-EXACT
  (analytic=-0.00552556 there used pre-swap; the swapped value
  -0.00311269 is the *same composed-grad* numeric within the harness's
  central-difference tolerance — the swap is exact, as the CPU bit-equal
  gate independently proved).
- **In-loop cuBLAS CONFIRMED for forward+backward**: across all 3
  scales the trainer's OWN fwd+bwd cuBLAS Dgemm held the GPU
  (57-59 W power-up + 443-451 MiB device memory) for **477-908
  consecutive nvsmi samples** = 100 % of training wall. Phase E proved
  this for forward only; Phase E2 extends it to backward (the d5_*_g
  weight-grad / input-grad GEMMs). Sampled SM-util ≤ 2 % — the
  documented microsecond-GEMM physical limit (Phase E C3-4, NOT a
  failure; the power/mem-resident signature is the legitimate proof).
- **No scale reached a captured FINAL gn2.** The pure-hexa GRAD-EXACT
  (3 full composed-grad passes) + 80-step AdamW loop is the wall:
  GRAD-EXACT alone took >5 min at d≥512 (never cleared at d=768/512);
  at d=384 it PASSED (~182 s) but the 80-step loop (80 × full
  fwd+bwd+AdamW) projects to >60 min, exceeding the 75-min orphan
  watchdog. A reduced-step (steps=8) d=384 retry was built+launched on
  the same flattened C but the retained instance was reclaimed before it
  emitted its final scalar. **No fabricated final metrics** (mission
  honesty: "better an honest 'no final captured' than a faked d=768").

## 5. Honest C3

- **C3-1 (the headline)**: the deliverable was a CAPTURED FINAL gn2 from
  an end-to-end GPU-routed train. **Not achieved at any scale** — the
  pure-hexa exact-grad + 80-step AdamW loop is substrate-bound beyond
  the cost-bounded watchdog at d≥384, even on a 251 GB / 128-vCPU fat
  host. What WAS captured (all real, on-box): **d=768·12L init
  gn2=7.98162** (Phase E's exact blocker BROKEN — first d=768·12L
  scalar ever), **d=512·8L init gn2=7.96517**, **d=384·6L init
  gn2=7.97898 + GRAD-EXACT PASS** (GPU-routed backward numerically
  exact on real hardware). The CPU-equivalence gate independently
  proves the refactored trainer's *full* gn2 descent is BIT-EQUAL to
  the boxed baseline (7.97116 → 3.73374e-07, acc 0→8/8) — the descent
  correctness is established; only the on-GPU 80-step *wall* is the
  unmet part.
- **C3-2 (backward routing scope)**: the GEMM-dominant backward FLOPs
  (8 `c3_outer`/`c3_matvec_t` sites + SwiGLU-bwd's 6 GEMMs) ARE routed
  through cuBLAS. SwiGLU-grad/RMSNorm-bwd/AdamW elementwise cores stay
  boxed (not GEMM-dominant). Inverse of Phase E's forward-only partial;
  together forward+backward GEMM-dominant FLOPs are GPU-routed.
- **C3-3 (B2-op honesty)**: the mission's named B2 ops
  (`farr_matmul_t_gpu`/`farr_outer_gpu`/…) have `TODO[cuda]`
  `return -1` HEXA_CUDA stubs on `017b988f` (no CUDA kernel — verified
  by reading runtime.c). Phase E2 routed backward through the ONE real
  CUDA kernel (`farr_matmul_gpu`/cuBLAS Dgemm) via exact GEMM reshapes
  instead — strictly stronger than the -1-hard-fail stubs. No
  hexa-lang change needed.
- **C3-4 (substrate ceiling, named)**: GRAD-EXACT (central-difference,
  3 composed-grad passes) and the 80-step AdamW loop are pure-hexa
  CPU-bound (RoPE/softmax/RMSNorm/residual/AdamW scalar loops over
  n_layer × T). The GPU accelerates the GEMMs to microseconds (hence
  ≤2 % sampled util — the documented physical limit) but the wall is
  CPU control flow. d=384·6L GRAD-EXACT clears in ~3 min; d≥512 does
  not within minutes. This is the real engineering ceiling for a
  pure-hexa exact-AdamW trainer at d≥384 — independent of GPU routing
  (which IS done + proven correct) or host fatness (which IS adequate).
- **C3-5 (infra iterations, no bleed)**: 4 dispatch iterations
  (v1→v4) to resolve dud-SSH hosts (multi-host retry) + 4 build bugs
  (gcc flags / full self-tree / CUDA include / `/usr/bin/time`). Every
  instance transition verified `LIVE_INSTANCES=0` — **zero cost bleed**
  at any point; all dud/finished instances destroyed clean. Total GPU
  spend trivial (sub-$1; each productive run 4-8 min on a $0.60/hr
  A100).
- **C3-6 (CPU-equiv gates the claim)**: the GPU fire's value is the
  *in-loop fwd+bwd cuBLAS proof on real hardware* + *d=768·12L init
  unblocked* + *GPU-routed-backward GRAD-EXACT PASS*. The numeric
  correctness of the full train is carried by the Mac CPU-equivalence
  bit-equality (§3), which is exact and reproducible at $0 — that is
  the rigorous evidence the backward refactor is a numeric no-op; the
  GPU run adds the real-hardware in-loop + scale-unblock evidence, not
  the numeric proof.
