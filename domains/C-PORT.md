# C-PORT — anima live authored-C training-shim port + irreducible-FFI floor

@title: 🧱→💎 C-PORT — drive anima's live authored-C training shims to hexa-native where the vendor-FFI boundary permits

@goal: inventory and classify anima's **LIVE authored-C** training shims (`training/*.c`, excluding the generated `training/deploy/holo_breakthrough_*/` snapshots), then drive the **portable** subset to hexa-native — RUNEQ-gated, byte/numeric-equivalent against the C baseline — while **formally marking the irreducible FFI floor** (the C↔vendor-lib bridge that cannot be hexa-native). Three tiers: (A) IRREDUCIBLE FFI/vendor-ABI boundary (CUDA/cuBLAS/NCCL/Accelerate/vDSP/BLAS wrappers) — these ARE the bridge, kept in C; (B) PORTABLE-to-hexa (pure glue/control-flow/struct-marshaling with no vendor-lib dependency) — port targets; (C) SMOKE/TEST harnesses — retirable once the lib is hexa-tested. g63-honest: every classification is by real file inspection of what each `.c` actually calls.

## scope

- IN scope: `training/*.c` + `training/native/*.c` — the live authored C shim mass.
- OUT of scope (EXCLUDE): `training/deploy/holo_breakthrough_*/` (generated deploy artifacts), `.venv*`, `build/`, `.worktrees/`, `.claude/`.
- Note: `training/build/libhxnccl.c` (211 LOC) lives under the excluded `build/` path. It is recorded in the inventory verdict for completeness but is OUT of the port scope (build artifact). See [[#milestones]] M5.

## tiers (milestone-1 inventory — verdict `.verdicts/c-port/INVENTORY.txt`)

- **Tier A — IRREDUCIBLE FFI/vendor-ABI boundary** (kept in C; formally marked, NOT ported):
  - `training/native/train_step.c` (1054) — cuBLAS Sgemm + cudaMalloc/Memcpy/Free hot path (~50 cuBLAS calls/step). THE GPU training kernel bridge.
  - `training/hxblas_cuda_shim.c` (572) — cudaMalloc/Memcpy/Free + cublasSgemm + cblas_sgemm/sscal/sdot/saxpy (CUDA ⊕ Accelerate BLAS dual backend).
  - `training/hxblas_wrapper.c` (562) — cblas_sgemm/sscal/sdot/saxpy (Accelerate BLAS wrapper).
  - `training/hxvdsp_wrapper.c` (186) — vDSP_vmul/vsmul/vadd/dotpr + vvexpf (Accelerate vDSP wrapper).
- **Tier B — PORTABLE-to-hexa** (no vendor-lib dependency in the marshaling layer; port targets, RUNEQ-gated):
  - `training/native/train_ffi.c` (214) — flat FFI wrapper: scalar→struct packing, persistent global state, getters. Pure C glue; only 3 `cudaMalloc` calls (delegatable to the tier-A shim). Marshaling layer is hexa-portable.
- **Tier C — SMOKE/TEST** (retirable once the lib is hexa-tested):
  - `training/hxblas_cuda_smoke.c` (79) — `main()` harness, calls `extern hxblas_sgemm` + asserts max_err. No direct vendor calls.
  - `training/hxblas_cuda_smoke_large.c` (87) — `main()` multi-shape sweep over `extern hxblas_sgemm`. No direct vendor calls.

### aggregate LOC (in-scope, excludes build/libhxnccl.c)
- Tier A (irreducible FFI): 2374 LOC (4 files)
- Tier B (portable):         214 LOC (1 file)
- Tier C (smoke/test):       166 LOC (2 files)
- Total in-scope live authored C: 2754 LOC (7 files)

## milestones

- [x] **M1 — inventory + A/B/C classification** (g63 real-inspection · verdict `.verdicts/c-port/INVENTORY.txt`)
- [ ] **M2 — port tier-B** (`train_ffi.c` marshaling → hexa-native; RUNEQ vs C baseline; cudaMalloc delegated to tier-A shim extern)
- [ ] **M3 — retire tier-C** (drop `hxblas_cuda_smoke*.c` once an equivalent hexa-native smoke covers `hxblas_sgemm`)
- [ ] **M4 — formally mark tier-A** (document the irreducible vendor-ABI floor: each tier-A file = a C↔vendor bridge that CANNOT be hexa-native; record the exact vendor symbols)
- [ ] **M5 — adjudicate build/libhxnccl.c** (decide whether the NCCL all-reduce shim is live authored-C in scope or a build artifact; if live → tier A)
