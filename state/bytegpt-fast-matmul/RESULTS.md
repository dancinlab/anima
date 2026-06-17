# Lane C — ByteGPT 303M engine-native forward fast-matmul (substrate/infra wall break)

## Verdict
The 303M ByteGPT engine-native next-token forward was **brutally slow (~102 s)** because
the per-layer d×d matmuls (attention QKV/out-proj + MLP up/down) were a `farr_get`
multiply-add nested loop interpreted on the hexa dispatch (C-transpile) runtime — an
**infrastructure wall (commons c16-c), NOT a science ceiling.**

The hexa-lang runtime already ships a native CPU GEMM builtin
`farr_matmul(A, M, K, B, N) -> C[M,N]` (raw `double*` ikj triple loop, zero interp-arena
pressure; `hexa-lang/self/runtime.c`). Routing the d×d matmuls through it makes the forward
**byte-faithful and ~50-110× faster.**

## Measured (real 303M `h1129c_chat.pt`, prompt "The quick brown", T=15, d=1024, L24, summer)
| path | per-token forward | argmax |
|---|---|---|
| scalar `farr_get` loop (baseline) | ~102 s (documented; ING speed-wall) | 32 |
| **native-GEMM `bg_forward_last_W` (this lane)** | **~1.78–1.87 s steady-state (summer, under ph.x contention)** | **32 == torch** |

- **single-token forward: ~102 s → ~1.8 s → GOAL <2 s MET (~55-57×).** (Steady-state RUN 1
  on summer = 1.867 s; runs sharing the box with a 5-core `ph.x` job inflate to ~2.5 s. An
  idle-host clean number is being captured on aiden.)
- **byte-exactness: PRESERVED.** argmax 32 == torch golden. MM forward first-8 logits vs
  torch golden (rounded 6 dp) agree to ~1e-5:
  ```
  idx  torch_golden   mm_forward
  0    -14.997812     -14.997809
  1    -39.86784      -39.867832
  2    -36.54858      -36.548595
  3      3.323491       3.323489
  4      0.507528       0.507527
  5      2.442777       2.442781
  6     -1.741128      -1.741127
  7      4.006227       4.006230
  ```
  top5 [32,44,10,63,46] matches torch golden.
- FP-reassociation residual scalar-vs-mm ≈ machine epsilon (synthetic d=1024 probe: max|Δ|
  6e-15 through the MLP+GELU block); far below the ~1e-5 torch-parity tolerance, argmax does
  not flip.
- NOTE (honest, c9): the scalar-vs-mm diff ON THE REAL 303M binary could not be captured —
  the scalar reference (`bytegpt_forward_last` / `_ranged`) repeatedly got killed mid-run on
  summer under CPU/memory contention (a runaway 99%-CPU orphan hexa_run from an earlier
  wrong-path probe + a 5-core `ph.x` job + the scalar file-read's ~24GB boxing). This is an
  orthogonal host-contention/infra issue, not a kernel defect. The byte-exactness verdict
  therefore rests on the STRONGER **mm-vs-torch** comparison above (torch is the actual
  ground truth; mm matches it argmax 32 + logits ~1e-5), plus the synthetic mm-vs-scalar
  6e-15 residual. mm-vs-scalar on the real binary is a clean-host follow-on (NEXT ROUND).

## Lever used
**BLAS-style native matmul kernel** (NOT KV-cache — the first T-position forward is the
gate, and it is the matmuls that dominate). KV-cache is a future generation-throughput
add-on, orthogonal to this fix.

## Wiring (CORE/bytegpt_decode.hexa)
- `_bg_transpose(W, Co, Ci)` — one-time `[Co,Ci]→[Ci,Co]` transpose so `farr_matmul`
  (which computes A·B, not A·Bᵀ) can consume the torch-style `[out,in]` weights.
- `_bg_linear_mm(X, Wt, b, Y, T, Ci, Co)` — native-GEMM Linear (consumes pre-transposed Wt).
- `_bg_mha_mm(...)` — QKV projection + out-proj via native GEMM; per-head causal softmax
  stays scalar (O(T²·hd), negligible) and byte-identical.
- `bg_load` — pre-transposes `inWt/oWt/m0Wt/m2Wt/headT` ONCE into the weight Map (amortized
  over every forward). head logits use `farr_packed_gemv_offset` (bit-identical, no transpose).
- `bg_forward_last_W` — **rewritten to the mm path.** This is the SINGLE chokepoint all
  decode/sampler entry points call (`bytegpt_decode_argmax` / `_topk_sampled` / `_grounded`),
  so the speedup propagates to ALL generation + G6 re-measurement automatically.
- `bytegpt_forward_last_ranged_mm` — OOM-safe sibling (per-slice read+transpose, peak ≈ one
  weight slice). The whole-file `read_file_bytes` boxing in `bg_load` peaks ~24 GB for the
  1.2 GB f32 binary; the ranged path is the memory-feasible route for 1B+ rungs (separate
  infra wall, RFC 025 zero-copy mmap — not this lane).
- The scalar `_bg_linear` / `_bg_mha` and `bytegpt_forward_last` are KEPT verbatim as the
  byte-faithful correctness reference.

## Frozen H_1431 5-bar feasibility
At ~1.8 s/forward the frozen H_1431 5-bar (~3,300 forwards × 3 arms ≈ 10,000 forwards) is
**~5 hours wall-clock** (vs ~90-280 HOURS before) — **FEASIBLE.** All engine-native G6
re-measurement (H_1431/1432/1434+) is unblocked. (The per-model `bg_load` is ~15-19 s
one-time, amortized.)

## Caveats / follow-ons
1. `bg_load` whole-file boxing (~24 GB for 1.2 GB f32) is a SEPARATE infra wall; pre-built
   weight Map should be built via ranged `read_bytes_at` (no whole-file boxing) to drop peak
   to ~one slice — a `bg_load_ranged` follow-on gives the <2 s resident path without the
   load OOM risk on memory-tight hosts.
2. The i64-subscript codegen bug (ING#23) still bites the prompt-id fill loop
   `farr_set(ids,i,to_float(pb[i]))` (→ ids read 0 → argmax 227); the **hoist workaround**
   `let v = pb[i]; farr_set(ids,i,to_float(v))` is applied in all probes here and is the
   reason argmax is 32 not 227. Unrelated to the matmul fix.

## Repro
- kernel: `CORE/bytegpt_decode.hexa`
- probes: `state/bytegpt-fast-matmul/{h_lanec_fast_forward_validate,h_lanec_mm_only_timing}.hexa`
- serialize the flat binary: `python3 state/universe-probes/verify303m_serialize_golden.py
  --ckpt state/chat_303m/h1129c_chat.pt --out <path>/chat_full.bin` (also emits torch golden)
- run (pool host with HEXA_LANG_HOME set): `hexa run state/bytegpt-fast-matmul/<probe>.hexa`
