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
