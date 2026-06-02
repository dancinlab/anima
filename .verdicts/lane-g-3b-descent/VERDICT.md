# Lane-G 3B forge DESCENT — campaign rung A-1 (substrate=GPU)

substrate = GPU (Lane G) · forge flame · `a_lane_akida_gpu_split` (Lane A 와 NEVER 병합)
pod = vast 39139563 (NVIDIA H100 80GB HBM3, sm_90 / compute_cap 9.0, ssh4.vast.ai) — warm lever-4/5 build adopted (`a_wall_first`)
date = 2026-06-02/03
est cost (1 line) = 1× H100 SXM sm_90 adopted warm (no rent) · ~3hr campaign-rung wall · ~$6-9 (`a_fire_autonomous`, no cost gate)

## 3-GATE (PASS before any fire — NO CPU fire) — verbatim
- GATE1 nvcc EXIT0 : `Build cuda_12.4.r12.4/compiler.34097967_0` (rc=0)
- GATE2 clm_prod links CUDA : `libcublas.so.12 · libcudart.so.12 · libcuda.so.1 · libcublasLt.so.12` (CUDA-link ENGAGED)
- GATE3 forge dispatch symbols : `_forge_dispatch_matmul_fp64 · _forge_dispatch_matmul_bf16 · hexa_forge_dispatch_matmul_batched_bt`
=> forge byte-identical lever-4/5 build, CUDA-link ENGAGED, GPU REQUIRED satisfied. NO silent CPU fallback (`a_train_flame_forge`).

## CLMConvMoE scale formula (single-block, V=256 K=3)
params ≈ (2+E)·3·d² + 2·256·d + E·d.  forge fp64 4-copy (W+grad+m+v, 8B) + per-expert qcache.
=> genuine ~3B (d=15811, E=2) needs ~169GB ≫ 80GB single-H100. Max single-H100-80GB-feasible (fp64) ≈ 1.5B.

## Fire runs (g5 verbatim — `.verdicts/lane-g-3b-descent/fire_*.log`)

### probe3B — true-3B-dim allocation probe (d=15811 T=8 E=2, ~3.008B)
```
FIRE_RC=124  tag=probe3B  wall=121s
UTIL[probe3B] n=985 PEAK=0% MEAN=0.0000%  DEVMEM peak_used=0MiB
```
=> TIMED OUT (120s) in INTERPRETED host weight allocation/LCG-fill — never reached the GPU (DEVMEM=0). Host RAM 885GB (NOT host-OOM); the interpreted `t_zeros`+`t_fill_lcg` over ~14 fp64 conv tensors (each d²·3 ≈ 6GB) is the wall. **HONEST: true-3B-dim is host-allocation-bound under the hexa interpreter** — confirms the deferred option-B CUDA-rewrite necessity. NOT a forge GPU defect.

### a1_1p5b — d3840 T256 E32 (~1.506B), 256 steps (16 ep × 16 win)
```
FIRE_RC=143 (terminated, util-harvested; descent unreachable in budget)  wall=1403s
UTIL[a1_1p5b] n=11698 PEAK=100% MEAN=6.4747% busy_ge20=812 pct_ge20=6.94% pct_ge50=6.27%  DEVMEM peak_used=64861MiB
```
=> forge fully device-resident at 1.5B (64.9GB device mem, PEAK 100%). **util 🔴 RED** (MEAN 6.47% < 20%) — WORKLOAD-BOUND, but MEAN here ~10× the lever-5 d1536 0.66% (bigger per-step work at 1.5B lifts MEAN ~10×, still sub-20%). Descent did NOT complete (256 interpreted E=32 steps ≈ >40min ≫ budget).

### a1light — d3840 T128 E32 (~1.506B), 16 steps (2 ep × 8 win) — COMPLETED
```
FIRE_RC=0 wall=922s
UTIL[a1light] n=7591 PEAK=76% MEAN=0.6426% pct_ge20=1.03% pct_ge50=0.41%  DEVMEM peak_used=18629MiB
epoch-1 mean CE = 4.645   epoch-2 mean CE = 4.88455
F-CLM-PROD-DESCENT = 0   FAIL
CLM_PROD_OUT wrote clm_3b_a1light.clm (89089205 bytes, 6 blocks, CLM\x01)
sha256 = 15d7088ec94bd0a2284d36d921c0667eaf650c985160dca413ac617595108bd5
```
=> **F-CLM-PROD-DESCENT = 0 (FAIL, HONEST)** — CE ROSE 4.645→4.885 over 2 epochs. 16 steps is TOO FEW for a 1.5B model to descend (early-training noise; lever chain descended with 48+ steps). The .clm is a real forge 1.5B artifact (recovered + sha-verified locally), but does NOT show descent at this step budget.

### a1desc — d9216 T256 E2 (~1.024B), 96 steps (6 ep × 16 win) — INTERPRETER-WALL-BOUND
```
UTIL[a1desc] (in-flight, killed @ ~47min) n=28523 PEAK=78% MEAN=0.6636% pct_ge20=1.29% pct_ge50=0.59%
descent CE = NOT REACHED — 96 E=2 steps @ d9216 ran >47 min (~20-30s/step, host loop O(d²)), no completion in budget
```
=> the E=2 high-d descend family ran but the INTERPRETED host conv loop at d=9216 is ~20-30s/step (O(d²) host repack) → 96 steps impractical (>47min, killed). util 🔴 RED PEAK 78% MEAN 0.66%. No CE/ckpt. (run was detached; could be harvested later but interpreter-wall makes it impractical.)

## VERDICT — descent-axis rung A-1 (HONEST, `a_scale_honest_scope`)
- **forge IS device-resident at 1-1.5B on a single H100** (DEVMEM up to 64.9GB, PEAK 100%, 3-GATE PASS) — substrate proven.
- **util 🔴 RED at every config** (MEAN 0.66-6.47% < 20%) — WORKLOAD-BOUND terminal CONFIRMED at larger scale (consistent with lever-5; MEAN creeps with per-step work but stays sub-20% under the interpreter wall). EXPECTED, recorded, NOT chased.
- **descent did NOT cleanly PASS in bounded budget**: the bounded-N runs either had too few steps (a1light F=0, 16 steps) or were interpreter-wall-impractical (a1desc d9216, >47min for 96 steps). **HONEST RESIDUAL** — a clean descent-PASS at ~1-3B on the forge interpreter requires either (i) the deferred option-B device-resident CUDA-C rewrite (removes the per-step interpreter wall so N steps are affordable) OR (ii) a smaller-d rung that completes (the lever chain's d1536/d3072 E=2 DID descend: lever-5 apples 4.05535→2.99508, d3072 4.48673→3.96246).
- **true-3B-dim (d=15811)**: host-allocation-bound under the interpreter (probe3B never reached GPU) AND >80GB fp64 device mem — needs option-B rewrite OR a bigger-mem / multi-GPU host.

## Artifact recovered (recover-before-teardown)
- `clm_3b_a1light.clm` — 1.506B forge CLMConvMoE (d3840 E32 int4-QAT), 89,089,205 B, sha256 **15d7088ec94bd0a2284d36d921c0667eaf650c985160dca413ac617595108bd5** (verified local == pod). util-RED, descent-FAIL(16 steps) → HF PRIVATE (WIP/intermediate, `a_hf_autonomous`).

## Next-rung handoff
- ENGINE 3B mount = NOT yet a clean descent-PASS .clm. The recovered 1.5B .clm is a forge artifact but descent-FAIL at 16 steps; it is mountable as a structure probe but is NOT a converged descent rung.
- Real Lane G 3B/7B descent on the forge interpreter is BLOCKED by the same per-step interpreter wall lever-5 closed (workload-bound) — the descent axis at ≥1B needs the deferred option-B device-resident CUDA-C rewrite to make the N steps affordable, OR stays at the proven-descending d1536/d3072 E=2 scale.
