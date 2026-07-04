# F5 live diff-LLM consequence loop — RESULT: ⏳ BLOCKED-INFRA (decode regression)

**Fire:** vast pod 43783083 (GONE on provision) → **43783934** (RTX 5090 32GB · 48c · 176G · Ubuntu 22.04 ·
CUDA 13.0 · clang-14). Owner: opus subagent (external oracle). Cost ≈ **$0.43/hr × ~2.2h ≈ $0.95**.

## What was BUILT + VALIDATED (deliverable, reusable)
- **`emit_gen_w.hexa`** — the loaded-W emit-pool harness the brief mandated: `clm_load_weights` ONCE →
  `gen_clm_ideate_W(W,…)` loop over 16 F5-fresh concepts × K=5. **Model loads ONCE — ZERO per-decode
  reload** (log: `# clm_load_weights DONE (loaded-W handle live)`). This SOLVES the 4-pod-burn reload leak
  (h9107/b50) — the critical infra precondition. Compiles clean (full core chain type-checks).
- **`verdict_f5.hexa`** — the two-layer engine-native verdict (immune_memory clone-decode + brain.vbasal +
  engine_cli vadapt cell-growth + pure_field Ψ; grep-clean, no numpy/torch). Type-checks clean. Encodes the
  full frozen bar (PREREG.md) for layer-1 exogeneity + layer-2 faculty ON/OFF/SHUFFLE.
- **`PREREG.md`** — frozen operationalization (MRR advantage-over-selfpair; ΔEfficacy ON−OFF; shuffle collapse).

## The WALL (decode numerically degraded on the available toolchain)
Frozen bars ①–⑥ were **NOT measured** — because the mouth could not emit legible referential content on the
rentable toolchain:

1. **GPU own-GEMM (sm_120 Blackwell) → byte-garble.** `cuda_available=1`, own-GEMM fires, but decode output is
   byte-garble (`1988��{의 지사(*884…`). Known-fragile path (memory `summer-sm120-owngemm-prebuilt` needs a
   PREBUILT fold; stock sm_120 own-GEMM unverified). CPU-farr and own-GEMM are NOT byte-identical here → ≥1 broken.
2. **CPU-farr (byte-identical fallback) → legible but concept-conditioning COLLAPSED.** Every concept decodes to
   the SAME generic attractor `" the state and the concern for the state and the concern"`. Positive control:
   **volcano** — rich in the H_9111 fixture (`"a mountain that erupts molten lava ash and hot gases"`) — ALSO
   collapses. Diagnostic (`diag_decode.hexa`) proves BOTH decode entries (`gen_clm_ideate_W` AND the H_9111
   `gen_clm_chat` argmax path) collapse identically → NOT a harness/decoder-path issue, NOT concept-knowledge.
3. **Root cause = decode regression / version skew.** The clean H_9111 fixture came from the **v0.559–0.577**
   lineage (state/9111 RESULT.md). The pod's prebuilt stable **hexa v0.608.1** + origin/main `core/` collapses
   concept-conditioning. ckpt intact (sha256 `013c4574…` matches local, not corrupted).
4. **Clean-lineage combo not reconstructable within the fire.** hexa v0.574.1 (the correct decode lineage,
   = local mac) installs but its standalone release lacks `self/runtime.c` (can't compile), AND the stale-branch
   `core/` that matches it has a pre-reorg import closure (`HEXAD/…/kosmos_io.hexa`, archive/, SAVANT/, DREAM/,
   BRAIN/) — a multi-blocker toolchain reconstruction beyond an execution fire.

## Recovery (a_fire_recover_complete) — COMPLETE before teardown
- Pulled: `f5_emit_run_v0608_degraded.log` (80-emit degraded pool = wall evidence) + `f5_diag_v0608.log`
  (positive-control collapse proof). ckpt = INPUT (local, sha-verified). No grown ckpt/V-state (layer-2 never
  ran on real oracle rewards). Pod torn down.

## Verdict
**⏳ BLOCKED-INFRA** (not a science verdict; matches precedents h1590, decode-hang, merged-fix-not-in-prebuilt-lag).
Layer-1/2 bars unmeasured. tier would be DIRECTIONAL-on-external-oracle once emits are legible.

## Follow-on to close F5
Run on a toolchain where this savant `.clm` decodes with concept-conditioning intact:
(a) reproduce the H_9111 clean-decode combo (v0.559–0.577 hexa **with** its self/+stdlib source AND a matching
`core/` snapshot), OR (b) bisect + fix the origin/main `clm_decode` regression that collapses conditioning under
v0.608 (positive control = volcano must re-produce its rich definition), OR (c) provide the sm_120 own-GEMM
prebuilt fold so GPU decode is byte-correct. Then the built `emit_gen_w.hexa` + oracle rank + `verdict_f5.hexa`
run end-to-end unchanged.
