# C-PORT.log.md — progress log

@title: 📓 C-PORT log — append-only (newest at bottom)

Sibling of [[C-PORT]]. Each entry: date · what moved · verdict ptr.

## 2026-06-03 — e001 seed + M1 inventory

도메인 CREATED. anima LIVE authored-C training shims (`training/*.c` + `training/native/*.c`, EXCLUDING `training/deploy/holo_breakthrough_*/` generated snapshots + `.venv*`/`build/`/`.worktrees/`/`.claude/`) inventoried + classified by real file inspection (g63 honest — grep of each file's actual vendor-ABI call surface).

**M1 [x] DONE.** 7 in-scope files, 2754 LOC, classified into 3 tiers:
- Tier A (irreducible FFI/vendor-ABI bridge · kept in C): 2374 LOC — `train_step.c` (cuBLAS+CUDA hot path) · `hxblas_cuda_shim.c` (CUDA⊕Accelerate BLAS) · `hxblas_wrapper.c` (Accelerate cblas_*) · `hxvdsp_wrapper.c` (Accelerate vDSP_*).
- Tier B (portable-to-hexa · port target): 214 LOC — `train_ffi.c` (flat FFI scalar→struct marshaling glue; only 3 cudaMalloc, delegatable).
- Tier C (smoke/test · retirable): 166 LOC — `hxblas_cuda_smoke.c` + `hxblas_cuda_smoke_large.c` (`main()` harnesses over `extern hxblas_sgemm`, no direct vendor calls).

Verdict (per-file tier + what-it-calls + aggregate) → `.verdicts/c-port/INVENTORY.txt` verbatim.

**Honest caveat:** `find training -name '*.c' -not -path '*/deploy/*'` surfaced an 8th file — `training/build/libhxnccl.c` (211 LOC, NCCL ncclAllReduce/ncclCommInitAll + cuda*). It lives under the EXCLUDED `build/` path, so it is OUT of the in-scope count but recorded in the verdict for completeness. Adjudication deferred to M5 (live authored-C vs build artifact). If ruled live → tier A.

Next: M2 port tier-B (`train_ffi.c` → hexa-native, RUNEQ-gated).

## 2026-06-03 — e002 M2 port tier-B train_ffi.c glue → hexa-native

**M2 [x] DONE — PORT-EQ (bit-identical, interpreter AND compiled path).**

Ported the PORTABLE glue of `training/native/train_ffi.c` (214 LOC, tier-B) to hexa-native, RUNEQ-gated locally on mini (NO ghost / NO cloud / NO pool — local `hexa` + `cc`).

- **Ported (pure, no vendor-ABI call):** `train_ffi_set_hp` (6× f32 scalar→struct marshaling) · `train_ffi_get_step` · `train_ffi_get_grad_norm` · `train_ffi_get_elapsed_us` (getters reading the persistent `FfiState`), plus the two portable fragments — the hp scalar defaults in `train_ffi_init` and the `G.hp.step++` pre-CUDA bump in `train_ffi_step`. 4 public fns + 2 fragments; ~30 effective LOC of pure glue.
- **NOT ported (irreducible tier-A floor, stays in C):** `train_ffi_init`'s 3 `cudaMalloc` + `train_step_init`, `train_ffi_step`'s `train_step()` (cuBLAS hot path), `train_ffi_cleanup`'s `train_step_cleanup`. The C RUNEQ driver stubs the 3 `train_step_*` externs and NEVER calls the GPU path — only the portable glue is exercised (g63-honest).
- **hexa port:** `training/native/train_ffi_native.hexa`. **C baseline:** `training/native/train_ffi_runeq.c` (`#include "train_ffi.c"` → links the REAL functions + the REAL static `FfiState G`; no re-implementation).
- **Struct layout** matched bit-for-bit vs `train_step.h`: `TrainHParams`=28B, `StepResult`=16B. Discovered the runtime raw primitives (`tensor_kernels.c` `hexa_ptr_{write,read}_{f32,i32}`) use **BYTE offsets** (memcpy at `ptr+offset`), not element strides — the port uses explicit byte offsets so the in-memory layout is identical to C.
- **RUNEQ:** `diff` C vs hexa-run = no difference (EQ-interp); `diff` C vs `hexa` compiled = no difference (EQ-compiled). Verdict `.verdicts/c-port/M2-train_ffi.txt` (verbatim).

**Honest caveats:** (1) `get_elapsed_us` reads low 32 bits via `deref_i32` — runtime has `write_i64` (→`hexa_ptr_write`) but no `deref_i64` builtin; RUNEQ values < 2^31 so exact, but a `deref_i64` builtin would be needed for elapsed_us ≥ 2^31 (runtime-primitive gap, not a port-logic error). (2) Pre-existing & untouched: sibling `train_step_ffi.hexa` `make_hparams`/`make_step_result` pass ELEMENT indices where the runtime expects BYTE offsets — latent layout bug in that file; the M2 port uses correct byte offsets.

Next: M3 (retire tier-C smoke once hexa-native smoke covers `hxblas_sgemm`) · M4 (formally mark tier-A) · M5 (adjudicate `build/libhxnccl.c`).
