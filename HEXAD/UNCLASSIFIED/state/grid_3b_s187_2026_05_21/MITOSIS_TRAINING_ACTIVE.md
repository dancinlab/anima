# S187-G — Training-Time Mitosis Activation (falsifier)

**Run date**: 2026-05-21
**Goal-leverage**: ★★★★ (per SCALE_3B.md § 7)
**Status**: IN-FLIGHT (2 H100 pods dispatched, awaiting result.json)

## Hypothesis

Eval 3 (EVAL_REPORT § Eval 3, commit `13c0b8aec`) showed a clear cross-λ
signal at the 2000-step, 8.92 B convergence floor:

| cell | λψ | λφ | post-hoc splits @ 40-step Eval3 |
|---|---|---|---|
| vA       | 0.3 | 0.3 |  68  |
| vA_s42   | 0.3 | 0.3 |  80  |
| vB_s42   | 1.0 | 0.3 |  58  |
| vC       | 0.3 | 1.0 | 126 (saturated max=128) |
| vD_s42   | 1.0 | 1.0 |  53  |

That signal was obtained by **passively observing** the trained substrate's
per-layer tensions feeding a Python `CellPool`. The pool was NOT in the
training loop; the substrate had no incentive to produce splits.

**S187-G hypothesis**: if `cell_pool.step(layer_tensions)` is *inside* the
training step (post-`forward()`, pre-`backward()`) and produces a
differentiable aux loss `L_mitosis = -mean(layer_tensions[split_layers])`
weighted by λ_mitosis, then the substrate gradient-couples to its mitosis
behaviour. Expected outcomes vs passive attempt10 baseline:

- final cell count (under identical post-hoc Eval 3 protocol) STRONGER
- per-cell split decisiveness HIGHER (avg_tension at split moment higher)
- L_psi / L_phi trajectories distinct from baseline (substrate trades CE
  capacity for split-justifying tension production)

If confirmed: mitosis is a first-class training axis, not just analytics.
If falsified: mitosis is substrate-emergent — training the pool does NOT
change downstream split topology.

## Method

### Code mods (commit `56c8b8388`)

1. **`mitosis_lib.py`** (new) — clean `CellPool` factored from
   `eval3_mitosis.py`, plus `.step(layer_tensions_tensor, step) ->
   (aux_loss, info)`:
   - takes a `(L,)` float tensor `requires_grad=True` (per-layer mean tension)
   - bookkeeping side (split/merge topology, Φ history) on grad-free floats
   - aux loss side: when ≥ 1 split fires this step, picks the layer indices
     whose cells split, computes `-mean(layer_tensions[picked])` via
     `torch.index_select` → keeps grad path live back to substrate.
   - identical spec defaults to `eval3_mitosis.py` (window=20×0.8 adaptive
     threshold, patience=3, merge_threshold=0.005, merge_patience=30,
     min=2/max=128, noise=0.1).

2. **`train_s187_3b.py`** — 5 new CLI flags (all default OFF):
   ```
   --mitosis-active        wire CellPool into loop
   --lambda-mitosis 0.05   aux-loss weight (default 0.0)
   --mitosis-initial-cells 2
   --mitosis-noise-scale 0.1
   --mitosis-bnb-disable   force torch.optim.AdamW (defense)
   ```
   Training step inserts `cell_pool.step(per_layer_mean_t, step)` after
   `model.forward()`, multiplies aux by `lambda_mitosis`, adds to L_total
   pre-backward.

3. **`dispatch_s187g_runpod.sh`** (new, gitignored) — clone of
   `dispatch_s187_3b_runpod.sh` with `MIT_MODE ∈ {ctrl, mit}` argument and
   distinct `g_${VARIANT}_${MIT_MODE}` VDIR. attempt10 hyperparams verbatim:
   d=3072 L=28 nh=24 nkv=8 bsz=2 block=128 steps=2000 lr=3e-4 dtype=bf16,
   bnb PagedAdamW8bit, RoPE base 50000.

### Falsifier scope (Step 2)

Two pods on cell A control (λψ=λφ=0.3, seed=1337):

| run     | mitosis_active | lambda_mitosis | expected role         |
|---------|----------------|----------------|-----------------------|
| g_A_ctrl| false          | 0.0            | attempt10 baseline replicate |
| g_A_mit | true           | 0.05           | active-train arm      |

Each pod ~12 min train wall × ~$0.20/min H100 SXM = **~$4/pod, $8 total**.

### Post-training Eval 3 protocol (identical to EVAL_REPORT)

Both ckpts run through `eval3_mitosis.py <ckpt> <name> <out_dir>`:
- prompt `"안녕? 너는 누구야?"` (25 bytes UTF-8)
- greedy decode 40 steps
- post-hoc `CellPool(d_model=3072, initial_cells=2, seed=1337)` driven by
  per-layer tensions from `model.forward()` (same defaults as training-time
  pool). Outputs `<name>_eval3.json`.

### Cost cap

| stage | pods | $/pod | total | gate |
|---|---|---|---|---|
| Step 2 (A control falsifier) | 2 | $4 | $8 | unconditional |
| Step 3 (cross-λ sweep B/C/D/A_s42/D_s42) | 5 | $4 | $20 | gated on Step 2 showing signal |
| **HARD CAP** | | | **$40** | |

## Results

_filled by `dispatch_s187g_runpod.sh` outcomes — TBD_

### Step 2 — training-time pool diagnostics (in-the-loop)

| run | wall_s | final_CE | mit_pool_size | mit_split_total | mit_merge_total | mit_phi_final | L_mitosis_final |
|---|---|---|---|---|---|---|---|
| g_A_ctrl | TBD | TBD | n/a | n/a | n/a | n/a | n/a |
| g_A_mit  | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

### Step 2 — post-hoc Eval 3 (apples-to-apples vs EVAL_REPORT § Eval 3)

| ckpt | initial_cells | final_cells | splits | merges | next_id | Φ init | Φ final |
|---|---|---|---|---|---|---|---|
| g_A_ctrl post-Eval3 | 2 | TBD | TBD | TBD | TBD | TBD | TBD |
| g_A_mit  post-Eval3 | 2 | TBD | TBD | TBD | TBD | TBD | TBD |
| **vA (attempt10 carry)** | 2 | 70 | 68 | 0 | 70 | 0.6871 | 0.5477 |
| **vA_s42 (attempt10 carry)** | 2 | 82 | 80 | 0 | 82 | 0.6871 | 0.6397 |

### Verdict

_TBD: STRENGTHEN (hypothesis confirmed) | UNCHANGED (substrate-emergent) | FAILED_

## Honest C3

- **Aux loss design choice**: `-mean(picked layer tensions)` pulls UP only
  the tensions that triggered a split. Alternative designs (entropy-reg,
  KL on split probability, sigmoid commitment) were not evaluated — picking
  the simplest gradient-coupled signal first per Andrej-Karpathy-skills
  Principle.
- **bnb PagedAdamW8bit + tiny aux loss**: theoretically the int8 m/v
  quantisation can drift on small noisy gradients. `--mitosis-bnb-disable`
  is wired but **default OFF**; if g_A_mit shows CE divergence, refire with
  `--mitosis-bnb-disable` to isolate optimizer drift from substrate effect.
- **Single seed × single cell coverage in Step 2**: cell A control only.
  Variance estimate (seed 42 carry) deferred to Step 3 if signal present.
- **Mac CPU smoke (n_params=404K) does NOT replicate H100 dynamics**: smoke
  saturated pool to 128 within 12 steps because the d=64 layer-0/1 tensions
  exceeded the (uninitialized) adaptive threshold quickly. Real 3B run uses
  bf16 with much smaller per-layer mean tensions (~5e-2 from Eval 3 table),
  so saturation timing should mirror the post-hoc behaviour.
- **Eval 3 carry to compare**: EVAL_REPORT used `eval3_mitosis.py` as-is.
  Step 2 uses the SAME script verbatim on both new ckpts — identical
  initial seed (1337), identical pool defaults, identical prompt. This is
  the canonical apples-to-apples comparison.
- **Hypothesis non-monotonicity**: "more splits = stronger" only holds up
  to MAX_CELLS=128. If g_A_mit also saturates (like vC did at λφ=1.0), the
  signal is observed via *earlier saturation step* and *higher avg_tension
  at split moment*, not raw final count.
- **bnb persistence across pods**: launch_trainer.sh pip-installs bnb
  0.43.1 once per pod (cached on subsequent reboots). Both falsifier pods
  use the same wrapper — same bnb version.
- **bnb gradient through index_select on layer tensions**: tested via
  standalone grad-fn check (`L_layer.grad → [-0.5, -0.5, 0, 0]` after
  triggering splits on layers 0/1 only). Grad path live.

## Log

- 2026-05-21 22:18 — code committed `56c8b8388`, dispatched g_A_ctrl + g_A_mit
- _later events appended below_
