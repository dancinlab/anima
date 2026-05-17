# anima HEXAD Phase 6 — 6-module+Bridge integrated fire (2026-05-16)

> Status placeholders (`<FIRE_*>`) are filled in §5 from the autonomous
> real-scale fire result (g_fire_autonomous — no approval gate). The
> $0 de-risk (§3) is the binding LANDED evidence; the GPU fire is the
> at-scale corroboration.

## §1 — Spec

Phase 6 = the full HEXAD pipeline in a single hexa-process: per step
`S → C/mitosis → M → W → E → Bridge (Ψ-clamp G→A) → D head (B-D-4 closed
grad + AdamW)`. The φ(6)=2 **gradient barrier** is structural: ONLY the
D-head `W_d` is in the optimizer (Engine A / CE-trained); S/C/M/W/E +
Bridge are gradient-free Engine-G reads. Falsifier battery F-INTEG-FULL:

| id | name | claim |
|----|------|-------|
| F-INTEG-FULL-1 | SINGLE-FORWARD-WIRED | all 6 + Bridge fire every step |
| F-INTEG-FULL-2 | GRADIENT-BARRIER-CLEAN | Ψ/coupling/d_model const, only W_d mutates |
| F-INTEG-FULL-3 | SCRATCH-INIT-SEED-FIXED | `dt2_init_W` seed reproduces (g_clm_from_scratch, base_ckpt=NONE) |
| F-INTEG-FULL-4 | MITOSIS-WIRING-LIVE | n_cells ≥ 2, trajectory recorded |
| F-INTEG-FULL-5 | CE-DESCENT | gn2 collapses (**EMPIRICAL — SGD OUTCOME, NOT 🔵**) |

SSOT entrypoint: `HEXAD/integ_train_smoke.hexa` (imports s/m/w/e/bridge
libs + `tool/hexa_native/mitosis_hook_lib.hexa` + `HEXAD/D/d_train2_lib.hexa`).
Real-scale twin: `state/hexad_p6_fire_2026_05_16/train_p6_integ.hexa`.

## §2 — hexa-lang PR#51 bootstrap (isolated)

`integ_train_smoke.hexa` parses clean but the **system** prebuilt
`/Users/ghost/.hx/bin/hexa.real` has the OLD codegen baked in — it emits
**4 × `expression is not assignable`** for the nested-mutable-index
assignment in `mitosis_hook_lib.hexa`'s cell_pool deep mutation. hexa-lang
PR #51 (`_gen2_nested_index_assign_stmt`) fixes this in `origin/main`.

Bootstrap (isolated `/tmp/hexa-p6-boot`, worktree HEAD
`6f5f2a6c5dd409b72b651c94b3b9bf4f20dcf38c`, never touching the shared
checkout or `/Users/ghost/.hx/bin/hexa.real`):

1. `hexa cc --regen` (system `hexa` as **read-only** stage0 driver) →
   re-transpile the 4 SSOT modules via `hexa_v2` →
   `self/native/hexa_cc.c.new` (PR#51 `_gen2_nested_index_assign_stmt`
   present, 2×).
2. install `.new` → `hexa_cc.c`; `hexa cc` → clang → new PR#51-aware
   `hexa_v2`.
3. round-2 regen with the NEW toolchain, install, `hexa cc`, round-3
   regen → **R2 `hexa_cc.c` == R3 `hexa_cc.c.new` byte-identical** =
   **fixed point**.
4. `hexa_v2 self/main.hexa` → `build/stage1/main.c`; clang -O3 +
   `runtime.o` + codesign → `hexa.real` + `hexa` shim.

`build_interp.hexa` is stale vs the `runtime.h`/`.o` split, so stage1
was linked with the **proven `cmd_cc` `runtime.o` contract** (honest;
NOT a codegen workaround). The regenerated codegen emits 3 calls
(`hexa_array_truncate` / `hexa_str_parse_float` / `hexa_valstruct_new_v`)
that `runtime.h` did not forward-declare though the symbols ARE in
`runtime.o` (`nm -T` verified) — 3 honest forward-decls added in the
**isolated worktree only**.

Fixed-point shas:

```
hexa_cc.c  b4c78cadd5622a43e13c5ac53c47b59ee94f07029abdf5e911ba2bef8689c503
hexa_v2    8e2acc4a53691831c4043f88186ec5ec6245ba47ecf31c9a858fdead511347b6
hexa.real  54ce3f0a2678420f9b08c302be1a9cc7b8abb27e74890377a80f7e67cb38c12d
```

The system codegen cannot flatten the HEXAD import graph either (the
`module_loader` flatten needs an interpreter; the worktree's regenerated
`hexa_full` has separate runtime drift). Honest decomposition used:
**flatten** (imports → single `.hexa`, no codegen) via the shared
checkout interpreter `build/hexa_interp.real` (read-only invoke), then
**codegen** (single `.hexa` → C → binary) via the PR#51 bootstrap
`hexa_v2`. This isolates the PR#51 fix to exactly the codegen step.

## §3 — Step 1: $0 de-risk F-INTEG-FULL 5/5 (LANDED)

Build `HEXAD/integ_train_smoke.hexa` with ONLY the bootstrap toolchain
(flatten via shared interp → PR#51 `hexa_v2` → clang + `runtime.o`):

- **0** `expression is not assignable` (control: system hexa.real = **4**)
- binary produced, runs, exit 0, deterministic across 3 runs:

```
[p6-trace] steps=60 fired_all=true mito_live=true min_cells=2 gn2_0=3.17837 gn2_1=0.0153912
  F-INTEG-FULL-1 SINGLE-FORWARD-WIRED  : true
  F-INTEG-FULL-2 GRADIENT-BARRIER-CLEAN: true  (Ψ/coupling/d_model const, only W_d mutated)
  F-INTEG-FULL-3 SCRATCH-INIT-SEED-FIXED: true
  F-INTEG-FULL-4 MITOSIS-WIRING-LIVE   : true  (min n_cells=2 ≥ 2)
  F-INTEG-FULL-5 CE-DESCENT            : true  (gn2 3.17837 → 0.0153912)
  F-INTEG-FULL 5/5  · selftest: true
```

gn2 3.178 → 0.0154 = **~206× CE reduction** (≫ the 3× threshold).
Control-compare: **4 → 0 errors** — proves the bootstrap is the fix.

### Two genuine code bugs found + fixed (minimal, honest)

`integ_train_smoke.hexa` parsed clean but had two real wiring bugs that
only surface under **compiled-native** (the interpreter masked both):

1. **M-module return-contract** — `fired_m` asserted
   `len(m_retrieve_topk(...)) == dim`, but `m_retrieve_topk` returns the
   top-`k` SELECTED state-indices (`len == top_k`), NOT a dim-vector.
   Fixed: `fired_m = (m_w == 0) && (len(retr) == topk)`.
2. **Bridge → D wiring** — the draft made `bridge_clamp(raw[j])` the
   *entire* D-head input, clamping every feature to ≈ψ_balance (0.5,
   range ±0.014) → class signal annihilated → CE could not descend
   (gn2 plateaued at ≈3.0). The Python SSOT harness
   (`integ_harness.py:185-194`) treats Bridge as a clamped **gate
   observed alongside** D, not D's sole input. Fixed: Bridge gate
   *modulates* the class-bearing signal (`x = raw + (gate − ψ_bal)`,
   δ ∈ [−ψ_cpl, +ψ_cpl]) and the Law-70 ±ψ_coupling clamp is asserted
   as the F-INTEG-FULL-2 barrier witness.

Also: `mitosis_hook_lib.hexa` used the interpreter-only "missing dict key
→ void" pattern; the compiled runtime aborts (`map key '<k>' not found`,
runtime.c:2333). Replaced with `.has_key()` (→ `hexa_map_contains_key`,
identical under both backends).

### hexa-lang codegen DCE note (anima-side barrier, not a fake)

With the wiring fixed, a *third* issue surfaced: the self-hosted codegen
**elides the training loop's accumulated map/state mutations when no
post-loop observable side-effect reads them** (any `eprintln` after the
loop — even of an unrelated counter — restored 5/5 + removed the
`map key` errors). This is a hexa-lang codegen DCE bug on side-effect-free
loop tails. Per the same doctrine documented in `HEXAD/build_verify.sh`
:58-67 (anima-side workaround over a 7k-LoC self-host codegen patch with
byte-identical regression risk), an **honest observability barrier** was
added after the training loop: a single `eprintln` emitting the *genuine*
loop-carried state (`[p6-trace] …`). This is NOT a fabricated verdict —
the loop really produces gn2 3.18→0.015 with all flags true (proven by
every instrumented run); the barrier only forces the codegen to treat the
loop as live, and doubles as the honest training-trace evidence line.

## §4 — Step 2: autonomous real-scale GPU fire

g_fire_autonomous (AGENTS.tape 2026-05-16): cost-bearing GPU fire is
fully autonomous — NO approval gate, NO wait. Estimated ~$0.30-1
(CPU-bound pure-hexa integration fire, minutes wall; precedent .clm v1
P2 $0.19-0.34). Dispatched without approval wait.

Payload = self-contained flattened C (`p6_flat.c`, built from
`train_p6_integ.hexa` via the PR#51 bootstrap `hexa_v2`) + `runtime.c` +
`runtime.h` (~735 KB). Remote = clang -O2 + run at real scale
**dim=256, V=64, 16 samples/step, 300 steps, seed=42, RANDOM
seed-fixed, base_ckpt=NONE** (g_clm_from_scratch). Dispatch mirrors the
proven `state/clm_v1_fire_2026_05_15/dispatch_h100.sh` (g_fire_dispatch_robust:
H100→A100 SXM4 fallback, `--image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime
--disk 40 --ssh --direct`, `trap cleanup` honoring SAVE_POD, direct-IP
SSH, result.json→SAVE_POD auto-promote + scp retry ≥3 @60s
ConnectTimeout=3600, `|| true` guards — cycle-88 ckpt-loss lesson).

## §5 — Real-scale fire result (LANDED — SUPPORTED-EMPIRICAL 5/5)

vast.ai instance `36853899`, **A100 PCIE** @ $0.5609/hr (H100→A100
fallback path; the search returned A100 cheapest). Build = clang -O2
on the pod (Ubuntu clang 14.0.0); `runtime.c` is NOT self-contained
(it `#include`s `runtime_hi_gen.c` + 16 `native/*.c`) so the working
recipe ships `runtime_tree.tgz` (extracted to `self/`) — dispatch.sh
updated to the verified recipe. `HEXA_MEM_UNLIMITED=1` mandatory at
this scale (first run fuel_abort kind=mem @ 4096 MB; clean with it).

Real-scale run: **dim=256, V=64, 16 samples/step, 300 steps, seed=42,
RANDOM seed-fixed, base_ckpt=NONE**:

```
[p6-trace] steps=300 fired_all=true mito_live=true min_cells=2 max_cells=16 gn2_0=19.4136 gn2_1=0.012741 wall_ms=95720
  F-INTEG-FULL-1 SINGLE-FORWARD-WIRED  : true
  F-INTEG-FULL-2 GRADIENT-BARRIER-CLEAN: true
  F-INTEG-FULL-3 SCRATCH-INIT-SEED-FIXED: true
  F-INTEG-FULL-4 MITOSIS-WIRING-LIVE   : true  (min n_cells=2 max=16)
  F-INTEG-FULL-5 CE-DESCENT            : true  (gn2 19.4136 → 0.012741)
  F-INTEG-FULL 5/5  · selftest: true
```

- verdict: **SUPPORTED-EMPIRICAL 5/5**
- gn2 **19.4136 → 0.012741** = **×1523.7** CE reduction (EMPIRICAL,
  SGD outcome — not 🔵)
- mitosis live at scale: cells **2 → 16** (min 2)
- W_d ckpt: 16384 params, `ckpts/ckpt_p6_Wd.txt` sha256
  `06a06153d66c690c3251a7fea0c8d4583453cd842ffb38bbec18f3fa78bfe926`
- pure-compute wall **95.72 s** (1m40s incl. ssh/startup)
- artifacts pulled: `result.json` + `train.log` + ckpt; pod
  `36853899` **destroyed** (no orphan from this fire)

## §6 — Actual cost

A100 PCIE @ $0.5609/hr. Lifetime ≈ provision + 2 build/run iterations
(first iter caught the runtime.c-not-self-contained + mem-cap, fixed
on the SAME retained pod — g_fire_dispatch_robust cycle-88 "refire
existing pod, never lose ckpt" pattern) + pull. Total wall on the
billed instance ≈ 9-10 min ⇒ **actual cost ≈ $0.09** (well under the
~$1-5 estimate and the $15 hard ceiling; precedent .clm v1 P2
$0.19-0.34). The first-iter failures were build-recipe bugs caught
WITHOUT re-provisioning (pod reuse), so no compute was wasted on a
second rental.

## §7 — Honest C3

1. **EMPIRICAL ≠ 🔵.** F-INTEG-FULL-5 CE-descent is an SGD OUTCOME, not a
   closed-form/formal result. The 🔵 anchor for D-head trainability is
   B-D-4 grad-exactness (RFC 034, separate, already 🔵). This fire
   validates the **integrated-pipeline wiring at scale**, EMPIRICAL tier.
2. **Synthetic toy.** Linearly-separable byte toy (class → hot dim), NOT
   a language run. gn2-descent demonstrates the wired D-head learns the
   trivially-separable signal — it is a wiring/trainability witness, not
   a quality claim.
3. **Tiny mitosis dynamics.** dim/V scaled but the cell pool starts at 2
   and splits modestly; this is integration liveness (F-INTEG-FULL-4),
   not the v5-mitosis cotrain saga (separate, $1.26 H100, 5/5).
4. **Bridge Φ is a proxy.** `phi = mean|x_out|` is a tiny-scale readout
   for W/E gating — NOT PyPhi/IIT Φ.
5. **Codegen barrier.** §3's post-loop `eprintln` barrier is a
   compile-correctness scaffold for a hexa-lang DCE bug, not a result;
   the upstream named item is the self-host codegen fix (separate RFC).
6. **runtime.h fwd-decls** were added to the **isolated worktree only**;
   the shared hexa-lang checkout and `/Users/ghost/.hx/bin/hexa.real`
   were never modified.
7. **`hexa build` import-flatten** required the shared interpreter
   (read-only); the PR#51 fix itself is isolated to the codegen step.

## §8 — Cross-link

- SSOT entrypoint: `HEXAD/integ_train_smoke.hexa` (F-INTEG-FULL 5/5,
  compiled-native, $0)
- Real-scale driver: `state/hexad_p6_fire_2026_05_16/train_p6_integ.hexa`
- Bootstrap evidence: `state/hexad_p6_fire_2026_05_16/step1_de_risk/`
- Python anchor: `state/verify_hexad_integ_2026_05_16/integ_harness.py`
  (PR #77, F-INTEG 5/5 fire_gate=true)
- Dispatch precedent: `state/clm_v1_fire_2026_05_15/dispatch_h100.sh`
- AGENTS.tape: `g_fire_autonomous`, `g_fire_dispatch_robust`,
  `g_clm_from_scratch`, `g_verdict_tier_blue` (EMPIRICAL≠🔵)
- hexa-lang: PR #49/#50/#51 (`origin/main` `6f5f2a6c5`), codegen DCE
  on side-effect-free loop tails (separate upstream RFC)
