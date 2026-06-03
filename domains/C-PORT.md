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

**DOMAIN TERMINAL** (2026-06-04) — all 5 milestones `[x]`. Portable surface exhausted: tier-B `train_ffi.c` ported RUNEQ-EQ (M2), tier-C smoke-ref logic ported (M3), tier-A vendor floor formally marked (M4) + `build/libhxnccl.c` adjudicated tier-A irreducible NCCL FFI (M5). Remaining C = the irreducible vendor-ABI floor (cuBLAS · CUDA · Accelerate cblas/vDSP · NCCL); no pure-logic sliver left to carve. g63-honest.

- [x] **M1 — inventory + A/B/C classification** (g63 real-inspection · verdict `.verdicts/c-port/INVENTORY.txt`)
- [x] **M2 — port tier-B** (`train_ffi.c` marshaling → hexa-native; RUNEQ vs C baseline = PORT-EQ bit-identical on interp + compiled path; cudaMalloc/cuBLAS stay in tier-A shim — verdict `.verdicts/c-port/M2-train_ffi.txt`)
- [x] **M3 — retire tier-C** (drop `hxblas_cuda_smoke*.c` once an equivalent hexa-native smoke covers `hxblas_sgemm`) — **PORT-EQ · RUNEQ 8/8 VALUE-EXACT + element-BIT-EXACT (g63-honest); proven-pending the hexa-lang if-body-fold PR merge.** The smoke harnesses' only portable logic (the scalar CPU reference matmul + deterministic pattern + max_err) is ported to hexa-native (`training/native/sgemm_ref_native.hexa`); the 8-case RUNEQ is now value-exact AND element-bit-exact (0/16640 mismatches) against the C reference after TWO fixes: **(1) a CONFIRMED hexa-lang codegen bug, FIXED** — a plain `let maxabs = 0.0` reassigned inside an `if`-body within a `for`-loop had its comptime-const fold inlined into the `if` CONDITION (`av > 0.0`, always-true) so `maxabs` ended at the LAST element, not the max (sibling of #2650 BUG1, NOT covered by the while-only fix); the fix pre-invalidates the fold for names the then/elif/else bodies reassign before folding/emitting the condition (hexa-lang PR `mczero/if-body-fold-fix`, base=main, + regression catcher `m10_if_body_fold_reassign.hexa`). **(2) a RUNEQ HARNESS fp fix** (not a bug) — the port models fp32 with f64 intermediates + round-to-f32 per op (no native f32 type); the C ref now mirrors that model EXACTLY (f64 `0.02` constant, f64 product rounded to f32, accumulate rounded after every add) and builds `cc -O2 -ffp-contract=off`, eliminating the f32-const / f32-product / FMA-contraction triple divergence the prior naive `float` driver had. PROOF is FUNCTIONAL (passes on a locally-rebuilt hexat carrying the codegen fix); it becomes the released behavior the moment the hexa-lang PR merges (the currently-installed unfixed hexat still miscompiles maxabs). Verdict `.verdicts/c-port/sgemm-ref-runeq.txt` (PORT-EQ, 8/8). [[C-PORT.log.md]]
- [x] **M4 — formally mark tier-A** (irreducible vendor-ABI floor documented: 4 in-scope files = C↔vendor bridges that CANNOT be hexa-native; exact vendor symbols + per-file why-irreducible recorded by g63 call-surface inspection. `train_step.c`=cuBLAS/CUDA · `hxblas_cuda_shim.c`=CUDA⊕cuBLAS⊕cblas · `hxblas_wrapper.c`=Accelerate cblas · `hxvdsp_wrapper.c`=Accelerate vDSP. No pure-logic sliver remains in any tier-A file. Verdict `.verdicts/c-port/M4-vendor-floor.txt`)
- [x] **M5 — adjudicate build/libhxnccl.c** — **AUTHORED vendor-irreducible FFI → TIER A.** git-tracked hand-authored C (no generated marker; human design-doc header citing alm_r11_fsdp_plan), but its entire reason-to-exist is the NCCL collective-comms ABI over CUDA (ncclCommInitAll/AllReduce/CommDestroy + cuda*). The only non-vendor code is FFI guard scaffolding (handle-magic + bounds + rc-mapping) — NO extractable pure-logic kernel, NO future leaf. Folded into tier A; stays in C (porting = re-implementing NVIDIA NCCL). Verdict `.verdicts/c-port/M5-libhxnccl.txt`
