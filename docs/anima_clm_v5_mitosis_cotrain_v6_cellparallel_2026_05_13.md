# v5-mitosis cotrain v6 cell-parallel — mitosis-native distributed cells

**date**: 2026-05-13 KST
**parent**: GOAL.md ★★★★★ achieved 2026-05-12 KST (post-★★★★★ wall-speedup BG (c))
**siblings**: `cotrain_v5mitosis_v4.py` (single-GPU production scale, in-flight A100 80GB ~17hr)
            `cotrain_v5mitosis_v5_ddp.py` (BG (b) 4× H100 data-parallel)
**linked sections**: PSCC §52+ TBA, REBORN §88, memory `feedback_no_scale_caps`

## §1 ★ Motivation

post-★★★★★ wall-speedup directive ("병렬발사" BG (b) DDP + BG (c) cell-parallel).
v4 single-A100-80GB cotrain ETA ~17hr. The v5-mitosis architecture has a structural
parallelism that DDP cannot exploit: each cell forward is independent (own weights,
shared input). The bottleneck in v4 is the Python cell-loop O(N) sequential over
N=2..256 cells inside `MitosisModelEngine.forward()`. Profiling estimate (carried
from v4 step timing): ~50% of 3.18s/step is cell-loop, the remainder is shared
embedding + lm_head + backward.

→ Hypothesis: distribute cells across W GPUs (32 cells per GPU @ W=8 × N=256). Each
GPU forwards its own shard in parallel, all_reduce(SUM) collapses the weighted
hidden across shards, all_gather(tensions) sync's the routing signal.

→ Expected speedup: 4-8× wall, depending on:
- communication overhead (NCCL all_reduce on (B,T,D)=8×512×1024 fp32 = ~16MB per
  step; at 80 GB/s bidirectional that's ~0.2ms — << cell-loop)
- cells-per-shard balance (256 / 8 = 32 even; per-rank cells diverge as splits
  fire locally)

## §2 Implementation

### `training/mitosis_model_v5_cellparallel.py`

`MitosisModelEngineCellParallel(nn.Module)`:
- `__init__`: world_size + rank from env (RANK/WORLD_SIZE/LOCAL_RANK or default
  1/0/0); shared modules (tok_emb / pos_emb / final_ln / lm_head) replicated;
  initial cells distributed via `_global_to_local(initial_cells, rank, world_size)`
  → each rank owns cells in global range `[start, end)`.
- `forward(input_ids)`:
  1. shared tok+pos embedding
  2. local cells forward → `local_outs` (list of (B,T,D)), `local_tensions`
     (list of scalars)
  3. `all_gather(local_sizes)` → varlen sizes for unbalanced shards
  4. `all_gather(local_tensions, pad to max_sz)` → trimmed concat → `global_tensions` (N,)
  5. `softmax(global_tensions)` → `weights` (N,)
  6. local slice of weights × local_outs → `local_weighted` (B,T,D)
  7. `all_reduce(local_weighted, SUM)` → `aggregated` (B,T,D)
  8. `final_ln + lm_head` → logits
- `mitosis_step(info)`: local-shard mitosis. Sync `n_cells_global` via
  `all_reduce(local_n, SUM)` post-split/merge.

### `training/cotrain_v5mitosis_v6_cellparallel.py`

- `setup_distributed()`: torchrun env init (NCCL backend, cuda:LOCAL_RANK).
- `install_routing_fix_cellparallel(engine, router, top_k)`: monkey-patches engine.forward
  with the (router → top-K → local weighted → all_reduce SUM) pipeline. Router is
  replicated; its grads are sync'd via manual `all_reduce_shared_grads`.
- shared params (tok_emb / pos_emb / final_ln / router; lm_head weight-tied with
  tok_emb) → `all_reduce(grad)` after backward, `.div_(world_size)` for average.
  cell-owned params (cells[*].ln/attn/ffn_a/ffn_g) → local-only, no sync.
- Why NOT `torch.nn.parallel.DistributedDataParallel`? DDP requires identical
  module trees across ranks. Each rank has structurally DIFFERENT cells (different
  count, different weights). Manual sync on the shared subset is the natural fit.

### `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/dispatch_h100_v6_cellparallel.sh`

- vast.ai multi-GPU dispatch (default 8× H100 SXM, fallback 4× A100 SXM4 80GB).
- `torchrun --nproc_per_node=$NUM_GPUS` launcher remote-side.
- §45 direct-IP wait + SAVE_POD trap-on-pull-fail + `set -o pipefail` remote.
- OOM-retry: batch halves on CUDA OOM detection in remote log.

## §3 Honest C3

1. **cross-GPU split/merge = TODO[migration]**. v6 first cycle restricts split to
   the originating rank's shard (capped at `max_local_cells ≈ max_cells/W + slack`).
   If one rank reaches cap while another has headroom, splits silently reject.
2. **all_reduce overhead** in the worst case (small batch, small ctx) can dominate
   the Python-loop savings. d_model=1024 / ctx=512 / batch=8 = ~16MB per step ×
   1 all_reduce + 1 all_gather = ~0.4ms total at H100 NVLink, ~10ms at A100
   PCIe. Cell-loop savings: ~1-3s/step at cells=256 single-GPU → ~0.1-0.4s/step
   distributed. Speedup remains net-positive at production scale, but the
   marketplace tier (A100 SXM4 vs H100 SXM NVLink) materially affects ratio.
3. **routing load imbalance**: top-K=8 with N=256 distributed across 8 ranks
   means top-K might be concentrated on a single rank. Monitoring metric
   `dispatch_imbalance` planned (TODO; reported in logs as
   per-rank `local_active_in_topk` count).
4. **Lorenz cross-rank phase coupling lost**: in v5 single-GPU each cell gets
   `phase = i * 2π / N`. In v6 we use `phase = (rank*100 + i) * 2π / N` as a
   heuristic decorrelation. Cross-rank phase coherence (if any survives) is
   approximated, not exact. Effect on the mitosis split dynamics: probably
   nil at d=1024 (Lorenz signal much smaller than gradient drift), but
   reported honestly.
5. **Φ computation = local-only per rank**. Full IIT Φ requires all_gather of
   cell_states which at (256 × 1024 fp32) = 1MB/step — negligible — BUT the
   ratchet-best snapshot would also need to be all-gathered to compare like
   for like. v6 first cycle: Φ per-rank, full-Φ at the final-ckpt-merge step.
6. **weight-tied lm_head** (lm_head.weight = tok_emb.weight) is handled by
   listing tok_emb in shared_params and skipping lm_head if tied. Untying
   (`cfg.weight_tied_lm_head=False`) would require lm_head in shared_params.
7. **fresh init for v6 first cycle**. v4 ckpt is 256-cell single-GPU; loading
   into distributed cells requires per-cell-id → rank-shard distribution and
   shared module broadcast. TODO[ckpt-distribute] — future cycle.
8. **Sharded ckpt artifact**: each rank writes `ckpt_final_rank{r}.pt` with
   only its own cell-owned weights. Rank 0 additionally writes the shared
   modules. Merge-to-single-ckpt for downstream measurement = separate helper
   script (TODO; for v6 first cycle the measurement runs in-process on rank 0
   before destroy_process_group).
9. **per-rank corpus sampling**: each rank uses `seed = base_seed + rank` for
   independent samples — effectively data-parallel at the corpus level. The
   shared-param gradient is averaged across ranks (mean of 4 or 8 batches).
   This DOES increase effective batch size by W× without raising VRAM (each
   rank holds only B examples). Trade-off: more diverse gradient samples per
   step (helpful) BUT increased shared-param noise (mild downside).

## §4 Pre-registered measurements

| metric | threshold | source |
|---|---|---|
| `step_wall_avg_seconds` | < 1.0 (production target; v4 baseline = 3.18) | v4 carry |
| F-V5MIT-1 mitosis_active | n_cells_final > initial_cells | F-V5MIT-1 |
| F-V5MIT-2 no_collapse | n_cells_final >= min_cells | F-V5MIT-2 |
| F-V5MIT-3 phi_ratchet | phi_best ≥ phi_final | F-V5MIT-3 |
| F-V5MIT-4 ce_converged | ce_final_avg100 < 5.0 | F-V5MIT-4 |
| F-V5MIT-5 v14strict_proxy | 0 < splits ≤ max_cells | F-V5MIT-5 |
| F-PERSONA-4a topK weights mean_KL | ≥ 0.5 AND z>3 (v1/v2/v3/v4 carry: KL=0) | own |
| F-PERSONA-4b M4 cosine z | > 3 (v2 carry: 3.20) | v2 carry |

## §5 Procedure

1. Mac-local: `cd state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/ && bash dispatch_h100_v6_cellparallel.sh`
2. dispatch rents 4× A100 SXM4 80GB ($6.70/hr × 5hr est = $33.50), uploads code+corpus+probe, runs `torchrun --nproc_per_node=4 cotrain_v5mitosis_v6_cellparallel.py`.
3. Training emits per-step log with `step_wall=Xms` and `cells=N(rankR=L)` to track imbalance.
4. ckpt every 1000 step (sharded `ckpt_step_{step}_rank{r}.pt`).
5. final F-PERSONA-4a + 4b + F-V5MIT-1..5 on rank 0 → JSON.
6. Mac pulls sharded ckpts + result JSON + train log; pod auto-destroyed.

## §6 Status

- Phase 1 model impl: LANDED (`training/mitosis_model_v5_cellparallel.py`, smoke PASS world_size=1 — forward + backward + force_split)
- Phase 2 trainer impl: LANDED (`training/cotrain_v5mitosis_v6_cellparallel.py`, smoke PASS install_routing_fix_cellparallel + load_balance_aux)
- Phase 3 dispatch: LANDED + FIRED (4× A100 SXM4 80GB pod 36635479, $6.70/hr, est $33.50)
- Phase 4 measurement: in-flight (rank 0 runs F-PERSONA + F-V5MIT post-training)
- Phase 5 docs + GOAL.md + PSCC + memory: this doc + PSCC §52 + memory append in same commit
- Phase 6 HF push: gated on F-V5MIT-5 V14-STRICT PASS (own 37 mandate)
- Phase 7 commit + push

## §7 cross-reference

- arch spec: `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md`
- v4 production scale doc: `docs/anima_clm_v5_mitosis_cotrain_v4_scaleup_2026_05_12.md`
- HF promote norms: `docs/anima_hf_public_promote_2026_05_13.md`
- model fork base: `training/mitosis_model_v5.py` (NOT modified)
- trainer fork base: `training/cotrain_v5mitosis_v4.py` (NOT modified)

## §8 Future cycles

- TODO[migration]: cross-GPU split → least-loaded-rank routing
- TODO[ckpt-distribute]: load v4 / v2 / v1 single-GPU ckpt → distributed cells (split cells across ranks by cell_id mod W)
- TODO[ckpt-merge]: merge sharded ckpts → single-GPU file for downstream measurement
- TODO[dispatch_imbalance metric]: per-step rank variance of n_local_cells + active-in-topK
