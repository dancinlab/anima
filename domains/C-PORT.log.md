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

## 2026-06-04 — e003 M3 port tier-C smoke PORTABLE core → hexa-native (RUNEQ toolchain-BLOCKED)

**M3 [ ] OPEN — port AUTHORED + C reference VERIFIED-CORRECT; bit-exact C-vs-hexa RUNEQ BLOCKED by two hexa 0.1.0-dispatch toolchain defects.**

The tier-C smoke harnesses (`training/hxblas_cuda_smoke.c` + `hxblas_cuda_smoke_large.c`) exist to diff a vendor GEMM (`hxblas_sgemm`, cuBLAS/Accelerate-cblas) against a PURE scalar CPU reference. Their only non-vendor logic — the deterministic input pattern (`A[i]=0.02*((i*37)%131-65)`, `B[i]=0.02*((i*53)%127-63)`), the scalar reference matmul honouring transA/transB, and the fp32 accumulation + max reduction — is hexa-portable. `hxblas_sgemm` itself is the irreducible tier-A bridge and is NOT ported.

- **Ported:** `training/native/sgemm_ref_native.hexa` — fp32-exact mirror (raw-f32 store/load round-trips reproduce C's per-step `float` rounding; byte-offset raw buffers). Written entirely with range-`for` to dodge BUG 1 (below).
- **C baseline VERIFIED-CORRECT** (ran on pool aiden): `sgemm_ref_runeq.c` (full 8-case matrix, reference loop copied VERBATIM from `hxblas_cuda_smoke_large.c::run_case`) + `sgemm_ref_runeq_small.c` (fast 16³ + 8×12×20 subset). Per-case summary = fp32 sum + max abs element (pins every C_ref element). Full output recorded in the verdict.
- **HEXA side BLOCKED** (interpreter RETIRED in 0.1.0-dispatch → all exec goes through native codegen). Two independent toolchain defects, each isolated to a MINIMAL reproducer and CONFIRMED on BOTH pool hosts aiden + summer:
  - **BUG 1** — `while` loop mis-compiles to a NON-TERMINATING loop (`hexa build` ok, native binary hangs, exit 124, no output). `for i in 0..N` range loops are fine. Reproducer: `training/native/repro/hexa_while_hang.hexa`.
  - **BUG 2** — parser crash `index 0 out of bounds (len 0)` on a triple-nested `for` with a `let` declared between loop levels and mutated in the innermost `for` (the matmul accumulator shape). No C emitted. Double-`for`, flat `for`+`if/else`, and 7 sibling for-loop fns all parse fine — so the trigger is this specific shape, not loop count; factoring inner loops into helpers does not avoid it. Reproducer: `training/native/repro/hexa_nestfor_parsecrash.hexa`.
- **g63-honest:** the port logic is NOT in question — the C reference is verified, `hexa parse` succeeds on simpler subsets, and the blocker is purely the hexa-lang frontend/codegen. M3 cannot close: retiring the C smoke would delete the only WORKING reference coverage. Verdict `.verdicts/c-port/M3-sgemm_ref.txt`.

**Resource note:** all heavy work routed to pool aiden (+ summer cross-check), NOT local — local CLI cap was saturated (16 stale hexa_run stubs, aprime_cc selfhost build at 49 min CPU) per the kernel-panic-precedent resource-safety rule. FILE-FIRST authoring locally; transpile/build/run on pool via base64 file transfer.

**Tier status:** tier-B (the sole pure-logic port target, `train_ffi.c`) = DONE (M2). NO new tier-B source remains. Remaining surface = tier-C smoke (this M3, port authored but RUNEQ toolchain-blocked) + tier-A irreducible FFI floor (M4 docs) + `build/libhxnccl.c` adjudication (M5). The portable-LOGIC tier is EXHAUSTED; what remains is irreducible-FFI marking + a toolchain-gated smoke.

Next: M4 (formally mark tier-A vendor floor) · M5 (adjudicate `build/libhxnccl.c`). M3 reopens to a one-line diff the moment either hexa BUG is fixed.
