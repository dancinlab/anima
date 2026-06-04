# Lane G 3B forge — HEXA-FUSION util-unblock PREFLIGHT — 🔴 STOP (CLOSED-NEGATIVE)

date = 2026-06-05 · Lane G / GPU (a_lane_akida_gpu_split) · substrate = hexa-lang `clm_prod` device-resident forge
gate = the ⛔ HARD PREFLIGHT GATE: "is the HEXA-FUSION device-resident CUDA-graph train-step WIRED INTO / pullable into anima's forge trainer?"

## VERDICT: STOP. Did NOT rent a GPU. The named util fix is ALREADY a measured CLOSED-NEGATIVE on the same binary.

### The integration gap (precise, like the Lane P serializer-gap STOP)
- **anima's Lane G forge trainer IS the hexa-lang `clm_prod` binary.** The rung A-1 fire script
  (`.verdicts/lane-g-3b-descent/fire_3b_descent.sh` L17-18) runs `CLM=$REPO/clm_prod` with
  `REPO=/root/hexa-lang`. anima invokes hexa-lang's `clm_prod` directly over env-config; it has
  **no independent forge train-step driver** (grep for `forge_dispatch_train_step` / `clm_lever` /
  `HEXA_CUDA_GRAPH` / `forge_graph` across anima = 0 hits; anima has no `stdlib/flame/` tree).
- Therefore there is **nothing anima-side to integrate HEXA_CUDA_GRAPH into**. The CUDA-graph lever
  lives in hexa-lang's `clm_prod` / `runtime_cuda.c` and is env-gated there. anima inherits whatever
  `clm_prod` does. The gate's "wired or pullable → integrate" branch does NOT apply because there is
  no anima boundary to wire across — anima already runs the exact program the lever was measured on.

### The lever was ALREADY measured against this exact binary → CLOSED-NEGATIVE
The HEXA-FUSION CUDA-graph train-step (HEXA-FUSION ④/⑤, `a_cuda_graph_train`) was built + measured
in the sibling kit `~/hexa-fusion-cuda-kit/` (PR #2658), AFTER rung A-1. Verbatim verdicts:

| lever | run | util MEAN | PEAK | median | CE ep1→ep4 | byte-eq |
|---|---|---|---|---|---|---|
| eager baseline | g0 GRAPH=0 | **14.87%** | 77% | 2% | 4.46624→3.64669 | — |
| ④ fwd/bwd graph | g1 GRAPH=1 | **13.19%** | 77% | 2% | 4.46624→3.64669 | ✅ bit-identical |
| ⑤ whole-step graph (AdamW in graph) | g1ws WHOLESTEP=1 | **13.54%** | 77% | 2% | 4.46624→3.64669 | ✅ bit-identical |

(config DEVRESIDENT=1 DEVFEED=1 BATCHED=1 D=1536 T=512 E=2 NSAMP=8 EPOCHS=4; clean idle H100, baseline 0.00%.)

**PRE-REGISTERED FALSIFIER** "whole-step capture raises util MEAN to >=20%" → **FALSIFIED. 13.54%.**
The whole-step probe (13.54%) is statistically indistinguishable from the ④ fwd/bwd-only graph
(13.19%, +0.35pp) — adding the entire 16-launch AdamW sweep to the captured graph moved util by
essentially nothing. Median pinned at 2% across all three conditions. PEAK identical (77%). The eager
baseline (14.87%) was HIGHER than both graph variants this run → the graph lever's signal is within
the noise floor.

### Root cause (honest, post-falsification — verbatim from F-FUSION-GRAPH-WHOLESTEP-AB.txt)
Host launch overhead is **NOT** the util ceiling on H100. Taking the host fully off the per-step
critical path (fwd+bwd+AdamW all in one replayed graph) does NOT lift utilization. The median-2%
floor that survives whole-step capture = the GPU is idle BETWEEN kernels because the per-kernel work
at D=1536/T=512 is sub-millisecond and the SERIAL fine-grained kernel DAG (each op waits on the prior
op's output) leaves SMs idle waiting on the next kernel's dependency. **The graph removes LAUNCH
latency, not the kernel-to-kernel DEPENDENCY chain.** This is the SAME workload-bound residual that
rung A-1 (VERDICT.md) and lever-5 (WORKLOAD-BOUND TERMINAL) already found.

**CLOSED-NEGATIVE on the >=20% falsifier.** Ruled-out axis = "host launch overhead is the util
ceiling on H100" — FALSIFIED across the full lever family (② async 10-12%, ④ fwd/bwd graph 13.17%,
⑤ whole-step graph 13.54%; all bottom out at median 2% / MEAN ~12-15%). The util wall is the
fine-grained serial kernel DAG, not the host.

### The real remaining unblock (NOT a capture env flag — codegen work, hexa-lang-OWNED)
Kernel **FUSION** (collapse the dependency chain into fewer, bigger kernels so each saturates SMs
longer). Upstream hexa-lang fusion line, measured in the same kit, is INCREMENTAL + sub-GREEN:
- **L3-a** (GN→GELU fused) 🟢 CONFIRMED byte-eq, **+3.26pp** MEAN (10.31→13.57%).
- **L3-b** (dual-GELU fused) 🟢 +1.01pp stacked on L3-a (byte-eq).
- **L3-c / L3-d / P2a** (triple fusion / glue-block + cooperative megakernel) build-ready, **UNMEASURED**,
  with the authors' own HONEST ceiling note: "pairwise incremental, will NOT reach >=20% alone."
- cublasLt-GELU-epilogue ruled out (FP64 has no GELU epilogue); the FULL whole-step megakernel is
  design-CLOSED (a persistent kernel can't call cuBLAS → hand FP64 GEMM breaks byte-eq + roofline).

This is upstream codegen/kernel-authoring inside hexa-lang's `clm_prod`, not an anima env-gate
integration. It is also still sub-GREEN as measured. So it is NOT an available util-GREEN unblock for
the 3B/7B fire today.

## Consequence for the campaign
- 3B ladder NOT fired beyond rung A-1. The fire's stated dependency ("HEXA_CUDA_GRAPH on → util unblock
  → util-GREEN closure gate") is FALSIFIED — the unblock does not exist; it is a measured closed-neg.
- 7B NOT proceeded. The 3B closure gate (util-GREEN MEAN>=20% AND descent-GREEN) is **not met by
  FALSIFICATION**, not by skipped measurement. `a_paper_negative_ok` applies: this is a publishable
  closed-negative ruling out host-removal as the util lever for the forge `clm_prod` substrate.
- No GPU rented, no util-GREEN fabricated (p7/g5: verdicts verbatim, zero fabrication).
- DO-NOT-TOUCH pods untouched (rented none).

## Honest util number WITH fusion (verbatim — do NOT claim GREEN)
**MEAN 13.54%** (whole-step CUDA-graph capture, PEAK 77%, median 2%). FAR under the 20% GREEN bar.

## Upstream handoff
The remaining unblock is hexa-lang codegen-owned (kernel fusion past L3-b, or the deferred option-B
device-resident CUDA-C full-step rewrite). Filed to hexa-lang inbox per `a_runpod_inbox` /
`a_runpod_inbox`-adjacent handoff. For anima's descent axis, the proven-descending path stays the
d1536/d3072 E=2 scale (lever-5 CE 4.05535→2.99508).
