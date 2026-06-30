# M4b longtrain — step-rate measurement + transfer-gap finding (2026-05-28)

Measured on RunPod H100 SXM `4q2rab8ds2zhsr` (and verified CPU-only on same node).

## measured: ~0.6–1.5 s/step (< 1.7 steps/s)
print-every-200 probe: in a 119 s window the trainer never reached step 200
(only step=1 printed). → rate < 200/119 ≈ 1.7 steps/s; realistically ~1 step/s.

Per-step cost is dominated by CPU-side dense loops, NOT the matmul:
- zero dMg: 29.16M `farr_set`/step
- Adam update: 29.16M params/step (sqrt + div + decay each)
- V=151643-wide softmax: ~3×V `farr_get`/step
GPU util was 0% (the d=64,T=4 matmuls are transfer-bound/tiny); CPU-only and
GPU builds have the SAME rate (matmul is not the bottleneck).

## the toy→production transfer GAP (quantified)
- dec_undertrain (toy #1314) predicted escape needs ~"tens × vocab" presentations
  = ≥3M presentations = ~750K steps.
- At ~1 step/s that is **~9 GPU-DAYS** — computationally INFEASIBLE in a fire.
- The toy's per-step cost (V=64 routing-free) is ~38,000× cheaper than this
  production trainer (V=151643 + dense 29M-param Adam). The "tens × vocab" budget
  does NOT transfer to a runnable production wall-time.

## the leak (separate, GPU-path only — a_runpod_inbox)
GPU build (`-DHEXA_CUDA`) leaks host RSS ~60 MB/s (OOM ~70 min). CPU build
(no -DHEXA_CUDA) has FLAT RSS (3088→3092 KB over 60s). → the leak is in
hexa-lang `runtime_cuda.c` device-buffer management, NOT the .hexa trainer.
The .hexa mm-leak fix (hoisted per-step backward buffers) is correct (CPU-flat).
→ FIRE RUNS CPU-ONLY (no leak, unbounded wall; matmul not the bottleneck anyway).

## decision: max-feasible budget probe
Added M4B_MAX_STEPS cap. Fire at 20,000 steps (CPU-only, flat RSS) =
80,000 token-presentations ≈ 0.53× V = **100× the prior fires' ≤200 steps**.
This is the largest honest budget; tests whether collapse persists at 100× budget.
