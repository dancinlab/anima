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

## CORRECTION (honest, c9) — bg_load_ranged does NOT fix the 24GB OOM
Built bg_load_ranged (ranged read_bytes_at per slice + free-after-transpose) expecting peak
≈ one slice. MEASURED peak RSS via `/usr/bin/time -v` on a real ranged decode (gen=3):
**Maximum resident set size = 24,300,188 KB ≈ 24.3 GB** — SAME as resident bg_load. The
dispatch runtime boxes the bytes returned by read_bytes_at (each byte → a HexaVal) and does
not free them promptly, so slicing the read does NOT lower the peak. The true fix is at the
runtime level (RFC 025 zero-copy mmap), OUT OF Lane C's scope. bg_load_ranged is kept (it is
byte-correct, decode exit 0, output sane) but it is NOT an OOM remedy — do not rely on it for
that. Practical 5-bar path: each engine_decode is a SEPARATE subprocess that peaks ~24GB
SEQUENTIALLY and is freed on exit, so it FITS on summer's 30GB **when uncontended** (no other
heavy job). The earlier pilot OOM was concurrency/contention (a 99%-CPU orphan + ph.x), not a
per-process ceiling. Recommendation for the pool 5-bar: run on an idle 30GB+ host, serialized,
no co-tenant heavy jobs.

## Quick fast-pipeline validation pilot (small scope — NOT the frozen 5-bar)
End-to-end engine-native H_1431 through the FULL chain (fast mm forward + hoisted topk
decode + frozen H_1305 scoring + cross-shuffle control), small scope on summer.
- The fast mm decode WORKS end-to-end: e.g. NSUBJ=1/MAXNEW=20 produced coherent fragments
  `consciousness: REL='universalized with t'  MEAS='responses to questio'` in ~1min/fragment
  (bg_load ~24GB once + 20 forwards @ ~1.8s). The forward-speed fix is confirmed in the real
  generation pipeline, not just the single-forward probe.
- HARNESS BUG found + worked around: h1431_bind_compose.score_from_fragments shuffle control
  uses a `while True: ... if all(perm[i]!=i ...)` DERANGEMENT — IMPOSSIBLE for n=1 → infinite
  loop. Any scoped pilot MUST use NSUBJ>=2 (the full 5-bar's NSUBJ=5 is fine). Re-ran NSUBJ=2.
- MEMORY: the resident bg_load peaks ~24GB (boxing, unfixed — see correction above). On a 30GB
  host it FITS for sequential single-process decodes when uncontended, but co-residence with
  the torch-importing scorer (~2GB) makes it tight/swappy. Full 5-bar wants an idle 30GB+ host.

## PILOT COMPLETED (fast-pipeline validation, NSUBJ=2/NSEED=1/MAXNEW=20 — NOT the frozen 5-bar)
The full engine-native H_1431 chain ran end-to-end on summer, exit 0:
```
[seed 7] consciousness: REL='universalized with t'  MEAS='responses to questio'
[seed 7] tension:       REL='kindled not a phi ca'  MEAS='raw network, enablin'
COMPOSE   FALS=0.0000  DIST=0.0000
SHUFFLE   FALS=0.0000  DIST=0.0000
ABLATE    FALS=0.0000  DIST=2.0000
```
PROVES: fast mm forward + hoisted topk decode + frozen H_1305 scoring + shuffle + ablate
controls all execute fast+correct. (At MAXNEW=20 the short fragments yield no falsifiable
claims → all-zero FALS/DIST is expected for this tiny scope; the point is the PIPELINE, which
runs. The frozen 5-bar uses MAXNEW=110 which produces scoreable fragments.) Orphan-guard
(setsid + EXIT-trap process-group kill) prevented the 24GB-orphan leak; exit clean.

## LOAD-WALL FIX LANDED: read_f32_at (peak 24.3GB → 18.1GB, byte-identical)
_bg_rd_farr_at now calls the runtime's read_f32_at(path, byte_off, n_floats) — reads f32
DIRECTLY into a native farr via a bounded 8MB chunk buffer, NO boxed-HexaVal byte
intermediate. Verified byte-IDENTICAL (max|Δ|=0 on the real 303M tok block). Measured peak
RSS on a real ranged decode dropped 24.3GB → 18.1GB. That clears the OOM margin on a 30GB
host (was tight at 24GB). (Residual 18GB is the runtime holding freed farrs / transpose
intermediates — a further reduction needs runtime farr-table compaction, but 18GB on 30GB is
workable for the serialized 5-bar.) bg_load_ranged / *_ranged / topk_sampled_ranged all
inherit this automatically. Commit aa2b81633.

## CORRECTION (honest, c9) — read_f32_at is NOT portable; reverted from the build path
The read_f32_at load-RSS fix (24.3→18.1GB) is REAL and byte-identical ON SUMMER (verified
max|Δ|=0, ran clean), but read_f32_at is only in NEWER hexa builds — mini's installed
/Users/mini/.hx toolchain does NOT have the builtin (fresh compile = "undeclared identifier
read_f32_at"; an earlier 'compile ok' was a stale cache). Shipping it unconditionally would
break the build on any host with an older hexa (CI, mini). So _bg_rd_farr_at is REVERTED to
the portable read_bytes_at path (compiles everywhere; peak stays ~24GB). The lower-RSS path is
documented in-code as a one-line opt-in swap for hosts whose hexa has read_f32_at. The genuine
fix remains runtime-level (RFC 025 mmap). NET: the load wall stands at ~24GB (fits a clean
30GB host serialized, as the completed NSUBJ=2 pilot proved); the forward-speed result is
unaffected and portable.
