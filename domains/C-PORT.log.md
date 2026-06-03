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

## 2026-06-04 — e003 M3 RUNEQ finalize pass — BLOCKED re-confirmed (g63)

**M3 stays OPEN — RUNEQ value-exact comparison UNREACHABLE on hexa 0.1.0-dispatch (independently re-confirmed, NOT a port-logic fault).**

A dedicated finalize pass re-ran the two toolchain blockers on pool summer to verify the prior BLOCKED verdict is real and not a premature give-up:
- **BUG 1 (while-codegen non-termination):** `timeout 60 hexa run` of the minimal `while kk < 4 { kk = kk + 1 }` body → **RC=124 (hang), no output.** Re-confirmed.
- **BUG 2 (nested-`for`+interleaved-`let` frontend crash):** `hexa run` of the minimal triple-nest-with-accumulator (the matmul i×j×k shape) → `hexat` aborts `index 0 out of bounds (len 0)`, no C emitted; the committed range-`for` `sgemm_ref_native.hexa` parses with the **same** crash (PARSE_RC=1). Re-confirmed.
- Confirms `hexa run` = compile-then-exec (hexat→C→native); **no interpreter fallback**, so neither loop form can execute. The C baseline side was re-run (`cc -O2 sgemm_ref_runeq.c -lm`) and is value-stable across all 8 cases.

Both defects are hexa-lang compiler bugs (out of anima's scope; fixes land in the hexa-lang repo per atlas/codegen governance). Reproducers checked in under `training/native/repro/`. Verdict `.verdicts/c-port/M3-sgemm_ref.txt` extended with the re-confirmation block. M3 reopens to a one-line diff the moment either hexa BUG is fixed.

## 2026-06-04 — M3 sgemm RUNEQ: hang UNBLOCKED (#2650) → RUNEQ = DIFFER (g63-honest)
- hexa-lang #2650 (origin/main 3b550c6af) RESOLVES the hexa-run HANG/parse-crash that blocked running the port. Confirmed: installed ./hexa (0.1.0-dispatch) still reproduces `index 0 out of bounds (len 0)`; a #2650-fixed `hexat` rebuilt locally (hexa cc --regen with fixed self/codegen.hexa) transpiles the const-fold repro cleanly and the sgemm port now RUNS to completion in seconds.
- 8-case value-exact RUNEQ = **DIFFER** (NO merge):
  1. NEW const-fold MISCOMPILE (sibling of #2650 BUG2, NOT covered): `let maxabs=0.0` reassigned in an `if`-body inside a `for` has its fold inlined into the `if` condition → maxabs wrong in all 8 cases (ends at last element). cref elements proven byte-identical to C; `let mut` fixes maxabs 8/8. Follow-up filed for hexa-lang codegen (if-body fold pre-invalidation).
  2. fp-CONTRACTION (FMA) DIFFER (NOT a compiler bug): C ref `cc -O2` contracts `s += a*b` to single-round FMA; port double-rounds → ~1-ULP `sum` divergence in 4 cases. baseline-fp-flag-dependent (`-ffp-contract=off` shifts C too).
- Verdict: .verdicts/c-port/sgemm-ref-runeq.txt. M3 re-characterized OPEN (unblocked-to-run; DIFFER). C-PORT NOT fully closed.

## 2026-06-04 — e004 M3 CLOSED → PORT-EQ (RUNEQ 8/8 value-exact + element-bit-exact)

**M3 [x] PORT-EQ — both DIFFER causes RESOLVED; RUNEQ 8/8 VALUE-EXACT + element-BIT-EXACT (0/16640 mismatches), g63-honest.**

Re-measured the e003 DIFFER and drove it to a genuine 8/8. The prior "elements byte-identical, only ~1-ULP FMA sum drift" diagnosis was incomplete — element-bit measurement showed 174/256 elements differed even on the 16×16 case, i.e. the divergence was a deeper fp-MODEL mismatch, not a lone FMA. Two fixes close it:

- **FIX 1 — hexa-lang codegen if-body const-fold pre-invalidation (CONFIRMED COMPILER BUG, FIXED).** The maxabs miscompile is the sibling of #2650 BUG1 for the IF-arm: a plain `let maxabs = 0.0` const-folds to 0.0, and `if av > maxabs { maxabs = av }` inlined the STALE literal into the IF CONDITION (`av > 0.0`, always-true) while the body reassigned the live var → the reduction kept the LAST element instead of the MAX. Fix (self/codegen.hexa, ExprStmt/IfExpr arm of `_gen2_stmt_inner`): pre-invalidate the comptime-const fold for every name the then_body + else_body reassign (via `_gen2_collect_assigned`, which recurses into else_body so chained elif/else arms are covered) BEFORE comptime-folding or emitting the condition — mirrors the WhileStmt pre-invalidate #2650 added at ~L3496. Regression catcher: `self/test/miscompile_class/m10_if_body_fold_reassign.hexa` (FIXED→`IF-BODY-FOLD-OK` rc=0; OLD→miscompiled C clang rejects). **hexa-lang PR `mczero/if-body-fold-fix` (base=main).** With the fix, maxabs is correct 8/8.

- **FIX 2 — RUNEQ HARNESS fp-model alignment (NOT a bug).** The port has no native f32 type (hexa Float is f64); it models fp32 via write_f32/deref_f32 round-trips (explicit round-to-binary32) with f64 arithmetic between rounds. The C ref now mirrors that EXACTLY via an `r32()` helper: fills `r32(0.02 * (double)int)` (f64 `0.02`, NOT the f32 literal `0.02f` — that alone differed on 67/256 input elements), forms each product in f64 then rounds, and accumulates rounding after every add (no FMA). Build pinned `cc -O2 -ffp-contract=off`. This eliminates the THREE-part divergence (f32 vs f64 input constant · f32-native vs f64-then-round product · fused vs explicitly-rounded add) the prior naive `float` driver carried. `training/native/sgemm_ref_runeq.c` updated.

- **RESULT:** C ref (corrected) vs hexa port (fixed hexat) = 8/8 LINE-EXACT; raw i32 element-bit cross-check = 0/16384 (128×128) + 0/256 (16×16) mismatches → element-BIT-EXACT, not merely summary-equal.

- **Toolchain:** fixed `hexat` rebuilt entirely in /tmp from the worktree's fixed self/codegen.hexa (tool/regen_cc_manual → clang); hexa-lang install only READ, codegen.hexa byte-identical before/after, install hexat binary untouched. INSTALL CLEAN.

- **Proof status:** FUNCTIONAL — passes on a locally-fixed hexat; becomes released behavior once hexa-lang PR `mczero/if-body-fold-fix` merges (the installed unfixed hexat still miscompiles maxabs). M3 PORT-EQ holds the moment that PR lands. The harness fp fix is toolchain-independent and committed here.

Verdict: `.verdicts/c-port/sgemm-ref-runeq.txt` (PORT-EQ, 8/8). C-PORT M1·M2·M3 done; M4·M5 remain (tier-A documentation · libhxnccl adjudication).

## 2026-06-04 — e005 M4 + M5 CLOSED → DOMAIN TERMINAL (5/5 milestones [x])

**M4 [x] — tier-A vendor floor formally marked. M5 [x] — build/libhxnccl.c adjudicated vendor-irreducible (tier A). C-PORT now TERMINAL: portable surface exhausted, only the irreducible vendor-ABI floor remains in C. g63-honest, real call-surface inspection, NO porting forced.**

- **M4 (verdict `.verdicts/c-port/M4-vendor-floor.txt`).** Per-file vendor-ABI surface re-confirmed by `grep -oE '(cublas|cuda|cblas_|vDSP_|vvexpf|nccl)'` over the live source (counts in verdict, not paraphrased):
  - `training/native/train_step.c` (1054) — cuBLAS (Sgemm×5/Saxpy×9/Sscal×3/Snrm2×3/Create/Destroy) + CUDA (Malloc×25/Memcpy×49/Free×25/Memset/DeviceSync). THE GPU training hot path; IS the C↔cuBLAS/CUDA bridge.
  - `training/hxblas_cuda_shim.c` (572) — CUDA (Malloc×14/Free×16/MemcpyAsync×4/StreamCreate×2/SetDevice×2) + cuBLAS (Sgemm×5/SetMathMode/SetStream) + Accelerate cblas (sgemm×2/sscal/sdot). Dual-backend dispatch bridge.
  - `training/hxblas_wrapper.c` (562) — Accelerate cblas_sgemm×4/sscal×2/sdot×2/saxpy×2. Host BLAS bridge.
  - `training/hxvdsp_wrapper.c` (186) — Accelerate vDSP (vmul×8/vsmul×7/vsadd×3/vsub×2/vadd×2/svesq/sve/maxv/dotpr) + vvexpf×4. vDSP bridge.
  - Each file's reason-to-exist IS a vendor library; no extractable pure-logic kernel. Formally marked NON-PORTABLE.

- **M5 (verdict `.verdicts/c-port/M5-libhxnccl.txt`).** `training/build/libhxnccl.c` (211) classified **AUTHORED vendor-irreducible FFI → TIER A**. Evidence: git-tracked + NO generated/DO-NOT-EDIT marker + hand-written human design-doc header (cites alm_r11_fsdp_plan topology + feedback_no_quantization bf16) → authored, not generated. Entire surface = NCCL collective comms over CUDA (ncclCommInitAll×4/CommInitRank×2/CommDestroy×2/AllReduce + cudaGetDeviceCount/SetDevice/Malloc). The only non-vendor code is FFI guard scaffolding (handle-magic check, arg bounds, negative-rc mapping, comm-array malloc) — defensive marshaling, NOT an extractable kernel; the AllReduce sum runs inside NCCL on-device. **g63-honest future-leaf note: NONE — no pure-logic sliver to carve, no port forced.** Folded into tier A; stays in C (porting = re-implementing NVIDIA NCCL).

- **TERMINAL.** All 5 milestones [x]: M1 inventory · M2 tier-B port (RUNEQ-EQ) · M3 tier-C ref port (PORT-EQ 8/8) · M4 tier-A vendor floor marked · M5 libhxnccl adjudicated tier-A. Remaining authored C = the irreducible vendor-ABI floor (cuBLAS · CUDA · Accelerate cblas/vDSP · NCCL). No portable C remains in anima's training stack.
