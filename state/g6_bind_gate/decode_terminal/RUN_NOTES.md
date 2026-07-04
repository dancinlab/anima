# H_6186 G6-bind DECODE-axis engine-native — RESOLVED on dedicated vast L40S pod (2026-07-03)

> Supersedes the prior aiden BLOCKED-INFRA note. Authoritative result = `engine_native_verdict.json`
> (+ `engine_native_fals_bound.json`, `engine_native_frame_out/` 108 files, `frame_run.log`,
> `gpu_util_timeline.txt`). Prior aiden `status.json` kept as historical record.

## 1. own-GEMM ignition — ACHIEVED (the repeated session wall, BROKEN)
Rented vast L40S (48GB, sm_89), id 43686128. CUDA-enabled hexa v0.587.0 via `HEXA_CUDA=1 sh install.sh`
+ apt build-essential/clang + symlink pip-nvidia cuda_runtime/cublas `.so.12`->`.so` and LIBRARY_PATH/
LD_LIBRARY_PATH to those dirs (bare ubuntu22.04 has no /usr/local/cuda toolkit). cuda_available()=1.
ALL 54 decode processes emitted `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path (no cuBLAS)` +
`[EAGER-DEVGLUE-FIRED] _hx_k_gelu device CUDA-erf GELU`; GPU util 81-86% during decode; peak ~9.96 GB/frame.
Contrast: aiden = CPU-scalar farr (no marker, util 0%, host wedge). L40S own-GEMM fires.

## 2. h9107 GPU-mem leak + process-isolation wall-break
gen_auto_ideate per-candidate mouth-reload leaks GPU device memory. 3-seed whole-arm (54 decodes) AND
1-seed (18 decodes) both OOM rc=137 at ~41/48 GB BEFORE any RESULT (own-GEMM non-rescuing, per h9107).
WALL-BREAK: fals_bound is FRAME-INDEPENDENT -> run each (arm,seed,frame) as a SEPARATE hexa-run process
(k=3 decodes ~9.96 GB) that EXITS to free the GPU. 54 processes, ALL rc=0, zero OOM. Decode + per-frame
scoring UNCHANGED engine-native CORE ops (`g6_decode_best_of_k_auto` + frozen predicates via additive pub
glue g6_kwr_pub/g6_falstb_pub/g6_dict_load_pub); base_seed+i + k-offsets[0,101,202] + frames/pairs
byte-faithful to g6_score_arm_auto_bound. Frozen ops UNTOUCHED. External step = arithmetic sum only.

## 3. Engine-native fals_bound (seeds 7,4302,4303)
- BASE     [0,0,0]  mean 0.0     (py-mirror [0,0,0] — byte-parity MATCH)
- TARGETED [3,3,5]  mean 3.6667  (py-mirror [5,6,6]=5.667 — byte-parity FAIL, mirror overstated)
- SHUF     [0,0,0]  mean 0.0     (py-mirror [1,0,0]=0.333 — byte-parity FAIL, engine cleaner)

## 4. Verdict (honest, c9, frozen-first, tune-to-green forbidden)
- TARGETED >> SHUF engine-native (separation 3.667 >= 3.0) -> form-priming BLOCK CONFIRMED on-engine.
- P1(base=0)✓ P3(shuf reject)✓ P4(separation)✓ — BUT **P2 (targeted majority fals_bound>=4 in >=2 seeds)
  FAILS engine-native**: [3,3,5] has only 1/3 seeds >=4 (mirror had 3/3). Frozen prereg OVERALL = FAIL.
- byte-parity with numpy mirror FAILS (own-GEMM decode != numpy decode).
- **TERMINAL DECISION: NOT a clean terminal PASS.** Engine-native REFINES the py-mirror DIRECTIONAL —
  the qualitative bind effect holds on-engine, but the mirror was optimistic; the true own-GEMM signal is
  weaker and does not clear the frozen P2 bar. (a_engine_native_learning working as intended.)

## 5. Recovery / teardown
Frame outputs + logs PULLED to this dir (a_fire_recover_complete). Ckpts remain staged & sha-verified on
mac (/tmp/g6tc_*.bin + ~/anima-weights/.../h1129.bin: 5cf07a36/919c1360/8c3af81b). Pod 43686128 torn down
(hexa cloud down, status GONE). No bookkeeping/commit/HYPOTHESES/CHANGELOG/ARCHITECTURE touched (task scope).
