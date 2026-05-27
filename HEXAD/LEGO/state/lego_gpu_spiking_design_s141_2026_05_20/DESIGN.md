# §141 LEGO GPU SPIKING PRIMITIVE DESIGN — large-N GPU LIF prerequisite

> **Verdict**: `GPU-SPIKING-DESIGN-CLOSE-DEVICE-KERNEL-GAP-NAMED` — large-N GPU
> LIF needs 3 GPU spiking primitives, and unlike §138's CPU primitives these
> require **device CUDA kernels** (`runtime_cuda.c`), a deeper upstream change
> than §138's pure-hexa stdlib composition. design-tier · $0 · B-S141 5/5 🔵 ·
> central c93e160a 0-diff.

## §0 Why §141

§140 ported `lego_engine.py` → `lego_engine.hexa` and noted in DESIGN §4: "A
GPU LIF (large-N) would need `farr_*_gpu` spiking variants = a further upstream
gap." The user directive sequence ("포팅후 GPU fire") makes the LEGO GPU fire
the next target. §141 specifies what that fire needs.

The honest finding §141 lands: **a LEGO GPU fire is NOT one-step-away.** The
GPU spiking primitives are a *deeper* upstream change than §138's CPU ones.

## §1 §138 (CPU) vs §141 (GPU) — the depth difference

§138's 3 CPU primitives (`flame_event_threshold` / `flame_refractory_step` /
`flame_stdp_pair`) landed as **pure-hexa stdlib composition** — element-wise
loops over `t_get`/`t_set`, NO `runtime.c` builtin, NO codegen change. PR #77
proved it: 4/4 PASS, `hexa build` clean, zero builtin edits.

The GPU versions cannot be pure-hexa. A GPU `farr` op is a **device CUDA
kernel** dispatched by `runtime_cuda.c` + wired in codegen. Existing
`farr_*_gpu` (matmul/rope/rmsnorm/silu/add) are each a hand-written CUDA
kernel. The 3 GPU spiking primitives would be 3 NEW CUDA kernels:

```
flame_event_threshold_gpu   — device kernel: per-element v >= v_th → 1.0/0.0
flame_refractory_step_gpu   — device kernel: per-element countdown + clamp
flame_stdp_pair_gpu         — device kernel: N×N outer-product ΔW + clip
                              (this one is the real GPU win — O(N²) parallel)
```

| axis            | §138 CPU primitives          | §141 GPU primitives             |
|-----------------|-------------------------------|----------------------------------|
| where it lives  | stdlib `.hexa` (spiking_lib)  | `runtime_cuda.c` device kernels  |
| change depth    | pure-hexa composition         | builtin + codegen wire           |
| `hexa build`    | no codegen change             | codegen_c2 must wire 3 new ops   |
| who can do it   | anima filed PR #77 directly   | hexa-lang upstream (CUDA + wire) |
| review weight   | stdlib lib (light)            | runtime kernel (heavy)           |

## §2 Why a GPU LIF is worth it (the §141 motivation)

The LEGO arc measured up to N=2048 — §126/§127 showed N=2048 already takes
~5 min/replicate on CPU. The interesting spiking regimes (§137 found the
n_stim-gradient *steepens* with N) live at larger N. A GPU LIF would unlock
N=16k–100k:

- `flame_stdp_pair` is O(N²) — at N=16k that is 256M weight updates per step.
  CPU: minutes/step. GPU: the outer-product + clip is embarrassingly parallel,
  ~milliseconds/step.
- The membrane/threshold/refractory ops are O(N) — cheap either way; the
  STDP O(N²) is the term that forces GPU at scale.

So the *one* primitive that genuinely needs GPU is `flame_stdp_pair_gpu`. The
other two (`event_threshold`, `refractory`) are O(N) and could stay CPU even
in a large-N GPU run — only the W matrix lives on device.

## §3 The honest LEGO GPU fire prerequisite chain

```
§138 CPU primitives ──→ PR #77 ──→ §140 lego_engine.hexa (CPU)   ✅ DONE
                                              │
§141 names: GPU LIF needs ↓
   flame_stdp_pair_gpu   (O(N²) CUDA kernel — runtime_cuda.c)     ← the gap
   [+ event_threshold/refractory can stay CPU, O(N) cheap]
                                              │
   inbox patch: flame-stdp-pair-gpu-kernel.md (a runtime_cuda.c
   request — heavier than §139's stdlib patch; hexa-lang upstream)
                                              │
   THEN: lego_engine_gpu.hexa + large-N (N≥16k) GPU LIF fire
```

A LEGO GPU fire is **2 upstream steps away**, not 1: (a) the
`flame_stdp_pair_gpu` CUDA kernel must land in `runtime_cuda.c`, (b) only
then is a `lego_engine_gpu.hexa` + GPU fire fire-ready. §141 names step (a)
precisely and files the request.

## §4 What §141 closes

✅ Names the GPU LIF prerequisite exactly — `flame_stdp_pair_gpu` is the one
   O(N²) primitive that genuinely needs a device kernel; the O(N) ops can
   stay CPU.
✅ Honestly distinguishes §141 from §138: GPU = `runtime_cuda.c` device
   kernel (builtin-tier), NOT pure-hexa stdlib (stdlib-tier). A heavier
   upstream change.
✅ Files the inbox patch `flame-stdp-pair-gpu-kernel.md` — the hexa-first
   PR-only path, like §139 (but flagged as a runtime-kernel change).
✅ Makes the honest call: a LEGO GPU fire is **2 upstream steps away**, NOT
   fire-ready now. Firing a "GPU LIF" today would either fail (no kernel)
   or be a CPU sim wrapped in GPU dispatch (meaningless). The fire-gate
   discipline forbids that.

## §5 What §141 does NOT do

❌ It does NOT implement the CUDA kernel — that is hexa-lang upstream CUDA
   work (runtime_cuda.c + codegen wire), heavier than anima's PR #77 stdlib
   contribution. anima files the request; does not write the kernel.
❌ It does NOT fire a GPU LIF — the prerequisite (`flame_stdp_pair_gpu`) is
   not met. Honest fire-gate: no fire on an unmet prerequisite.
❌ GOAL emergence — engine tooling, orthogonal (B-EMERGE-7).

## §6 Closed-form propositions

```
B-S141-1   GPU-PRIMITIVE-IS-DEVICE-KERNEL-NOT-STDLIB  (§138 CPU = pure-hexa;
                                                       §141 GPU = runtime_cuda.c)
B-S141-2   STDP-PAIR-IS-THE-O-N2-PRIMITIVE  (the one that genuinely needs GPU;
                                             event/refractory are O(N))
B-S141-3   LEGO-GPU-FIRE-IS-2-UPSTREAM-STEPS-AWAY  (kernel land → gpu engine →
                                                    fire; NOT fire-ready now)
B-S141-4   INBOX-PATCH-PATH-HEXA-FIRST-COMPLIANT  (flame-stdp-pair-gpu-kernel.md,
                                                   flagged runtime-kernel tier)
B-S141-5   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S141-NOTE  empirical carve-out — design names the GPU gap; kernel
            implementation + GPU fire = future, NOT counted 🔵
```

## §7 Honest C3 (8)

1. §141 is the honest answer to "GPU fire go" for LEGO: the GPU fire has a
   real, named, 2-step prerequisite — not a refusal, a precise map.
2. The §138/§141 depth difference is the substantive finding — CPU spiking
   primitives were pure-hexa (anima could PR directly); GPU ones are CUDA
   kernels (hexa-lang upstream, heavier review).
3. Only `flame_stdp_pair_gpu` genuinely needs GPU — the O(N) ops can stay
   CPU even in a large-N run. This narrows the upstream ask.
4. anima stays downstream-consumer — files the request, does not write the
   CUDA kernel.
5. A LEGO GPU fire today would be meaningless (no kernel, or CPU-wrapped) —
   the fire-gate discipline forbids firing on an unmet prerequisite.
6. The inbox patch is filed but flagged as runtime-kernel-tier — heavier
   than §139's stdlib patch; hexa-lang maintainers' call on priority.
7. g3: design ≠ implementation ≠ fire ≠ emergence; capability claim 0.
8. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
