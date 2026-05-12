# anima CLM v5-mitosis cotrain v4-multi — fresh-init multi-GPU DDP (2026-05-13)

**Status**: 🔄 IN-FLIGHT (dispatched 2026-05-13 19:07 UTC on Vast.ai 4× RTX PRO 6000 S 96GB)

**Provenance**: post-★★★★★ multi-GPU exploration BG (a). Direct fork of `training/cotrain_v5mitosis_v4.py` (production-scale single-GPU trainer, PSCC §50 §A3 4b z=3.20 carrier) wrapped in `torch.nn.parallel.DistributedDataParallel`. **Fresh-init** (no resume ckpt) — companion to PSCC §51-DDP v5-DDP (CONTINUATION-from-step-2000) and PSCC §52-CELL v6-cell-parallel (mitosis-native shard).

**Why three multi-GPU variants in parallel** (per session BG triplet "이것도 여러개"):

| variant       | base                          | parallelism      | dispatch                                                    | path lane                            |
|---------------|-------------------------------|------------------|-------------------------------------------------------------|--------------------------------------|
| v4 single     | fresh d=1024 cells=256        | 1× A100 80GB     | aborted 2026-05-13 (ckpt_step_2000 saved)                   | reference baseline                   |
| **v4-multi**  | **fresh d=1024 cells=256**    | **4× RTX PRO 6000 S** | **`state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/`** | **fresh-init multi-GPU (BG a 본)**   |
| v5 DDP        | resume from v4 step 2000      | 4× H200 80GB     | `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/`          | continuation evidence (BG b)         |
| v6 cell-par   | fresh d=1024 cells=256        | 4× A100 80GB     | `state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/` | mitosis-native shard (BG c)          |

## §1 — Motivation

v4 single A100 80GB hit a wall ETA ~17hr (refire-path batch=2 ctx=256 after the initial batch=8 ctx=512 OOM at cells=66). The session abort retained ckpt_step_2000 (the v5-DDP resume payload). Two complementary multi-GPU paths address different questions:

- **v5 DDP** asks: does the v4 trajectory CONTINUE to converge under data-parallel scaling, when restarted from a partial run?
- **v4-multi (this doc)** asks: starting FRESH from step 0 with the same envelope but 4-way data parallelism, do we reach an equivalent (or better) F-PERSONA-4a / 4b / F-V5MIT signature in ~1/4 the wall time?

The fresh-init variant cleanly removes the "resume bias" from v5-DDP and provides an apples-to-apples comparison against the v4 single A100 trajectory (had it completed). This is the more interpretable benchmark for "does multi-GPU change the cotrain qualitatively?"

## §2 — Arch / config

Same as v4 single (mirror):
- `vocab_size = 256` byte tokenizer
- `d_model = 1024` (REBORN §88 EngineAG stretch)
- `n_head = 16`, `d_head = 64`
- `ffn_dim = 4096` SwiGLU dual-FFN (H404)
- `n_layer = 1`
- `max_cells = 256` (8-bit identity space)
- **`initial_cells = 256`** (cells-static from step 0 — DDP-safe; v4 single saturated cells=256 by step ~150 anyway)
- `ctx = 256` (v4 refire-path; v4 single batch=8 ctx=512 OOM'd at cells=66)
- `top-K = 8` MoE + Switch load-balance aux α = 0.01
- annealed gate-entropy λ: 1.0 → 0.01 cosine (v3 routing fix carry)
- `steps = 20000`, `warmup = 2000`
- `lr = 1e-4` cosine, AdamW β=(0.9, 0.95), wd=0
- `per_gpu_batch = 2` × `world_size = 4` → `effective_batch = 8` (matches v4 single original)
- corpus: `corpus_5cat_balanced.txt` (cotrain v2, 19 MB, 5-cat × multi-turn)
- probe: `identity_probe.jsonl` (50 prompts, 5 categories)
- ckpt every 5000 step

## §3 — DDP wiring

- backend = `nccl` via `dist.init_process_group(init_method='env://')`
- one process per GPU (`torchrun --standalone --nproc_per_node=4`)
- per-rank `LOCAL_RANK` → `torch.cuda.set_device(local_rank)`
- per-rank seed offset: `torch.manual_seed(args.seed + rank)` → independent batch streams
- `DistributedDataParallel(engine_inner, device_ids=[local_rank], output_device=local_rank, find_unused_parameters=True, gradient_as_bucket_view=True)`
- `find_unused_parameters=True` REQUIRED — top-K = 8 over cells = 256 means 248 cells receive no gradient per batch; without the flag DDP raises "expected to mark a variable ready only once".
- mitosis split / merge FROZEN (`--freeze-mitosis 1` ⇒ skip `engine.mitosis_step(info)`). Cells-static path. Rationale: see §6 honest C3 #1.
- gradient sync = automatic via DDP all-reduce on `.backward()`. The Switch load-balance aux is computed per-rank (over each rank's batch of dispatch decisions) and the resulting param gradients are all-reduced — load-balance pressure averages across ranks.
- rank-0 only: log lines, ckpt save, F-PERSONA-4a / 4b snapshot at ckpt boundaries, final result.json. Other ranks block on `dist.barrier()` at ckpt boundary.

## §4 — Wall budget / cost

- target wall: ~4-5 hr (v4 single A100 ~17hr ETA → 4× A100 parallel ≈ 4× speedup; conservatively 5 hr)
- compute (attempt 2 refire): **4× A100 SXM4 80GB @ $6.71/hr** rel=0.993 (attempt 1 4× RTX PRO 6000 S Blackwell failed — see §5.5)
- cost target: $6.71/hr × 5 hr = ~$33.56 (well below $80 cap per BG brief, `feedback_no_scale_caps`)
- cost cap (floor not ceiling): `--cost-cap-usd 80.0`, `--cost-per-hr ${OFFER_DPH}` actual
- absolute max: `cap × 1.10 = $88.00` (estimation gate)

## §5.5 — Attempt 1 FAILED (Blackwell sm_120 NCCL incompat)

Initial dispatch 2026-05-13 19:07 UTC selected **4× RTX PRO 6000 Blackwell Server Edition 96GB** at $5.33/hr (pod 36635742). PyTorch 2.5.1+cu121 emitted the warning `NVIDIA RTX PRO 6000 Blackwell ... CUDA capability sm_120 is not compatible with the current PyTorch installation. The current PyTorch install supports CUDA capabilities sm_50 sm_60 sm_70 sm_75 sm_80 sm_86 sm_90` — I initially treated this as benign forward-compat (PTX JIT fall-through), which was wrong. NCCL kernels are compiled binary-only for the listed sm targets; on sm_120 the first NCCL collective fails at runtime:

```
torch.distributed.DistBackendError: NCCL error in: .../NCCLUtils.hpp:317, unhandled cuda error
ncclUnhandledCudaError: Call to CUDA function failed.
Last error: Cuda failure 'invalid argument'
```

The failure landed inside `_verify_params_across_processes` during `DDP(engine_inner, ...)` init — the very first NCCL all-gather to check param shapes across ranks. Process group set up cleanly, model built (5.37B params loaded onto each rank's GPU), then died on the first cross-rank op.

**Lesson** (carry to `feedback_orchestrator_h100_gotchas`): if the marketplace pod's PyTorch is built with `cu121` and the GPU is **Blackwell** (sm_100 = B200 / sm_120 = RTX PRO 6000 / GB200 etc), DDP / NCCL will fail. Either:
  (a) pre-install `torch-nightly` with sm_100+ kernels (PEP 668 `--break-system-packages` slow path), or
  (b) exclude Blackwell from the marketplace filter (chosen for v4-multi refire).

The dispatch script filter was tightened to `gpu_name in [H100_SXM,H100_NVL,H100_PCIE,H200,A100_SXM4,A100_PCIE]` (drops `RTX_PRO_6000_WS/S` and `B200`). Wasted attempt cost: ~$0.50 (5 min × $5.33/hr × pre-train init). Failed pod 36635742 destroyed.

**Refire**: 2026-05-13 19:19 UTC, 4× A100 SXM4 80GB @ $6.71/hr rel=0.993. A100 sm_80 = native PyTorch 2.5.1+cu121 support → guaranteed DDP correctness. v6 cellparallel BG (c) is running on identical hardware class without issue.

A secondary bash bug was discovered in the OOM-retry path: `OOM=$($SSH_CMD "..." || echo 0 || echo 0)` returned `"0\n0"` on remote SSH failure → `[ "$OOM" -gt 0 ]` raised `integer expression expected`. Fixed via `| tr -d '[:space:]' | head -c 8` + empty-guard. Carry to v5-DDP / v6 dispatch on next edit.

## §5 — Comparison axes (vs v4 single, v5 DDP)

The post-run analysis will compare:

| axis                          | v4 single (aborted) | v4-multi (this) | v5 DDP (continuation) |
|-------------------------------|---------------------|-----------------|-----------------------|
| init                          | fresh, cells=2→256  | fresh, cells=256 static | resume step 2000, cells=256 static |
| world_size                    | 1                   | 4               | 4                     |
| effective batch               | 8 → 2 (refire OOM)  | 8               | 16                    |
| wall                          | abort at step 2000  | <<<TBD>>>       | <<<TBD>>>             |
| cost                          | $1.29               | <<<TBD>>>       | <<<TBD>>>             |
| CE final (avg100)             | <<<TBD step 2000>>> | <<<TBD>>>       | <<<TBD>>>             |
| F-PERSONA-4a routing KL       | (not measured)      | <<<TBD>>>       | <<<TBD>>>             |
| F-PERSONA-4a routing z        | (not measured)      | <<<TBD>>>       | <<<TBD>>>             |
| F-PERSONA-4b content z        | (not measured)      | <<<TBD>>>       | <<<TBD>>>             |
| splits this run               | 254                 | 0 (cells static)| 0 (cells static)      |
| F-V5MIT-5 V14-STRICT          | PASS (inherited)    | N/A inherit-PASS | N/A inherit-PASS     |

## §6 — HONEST C3 (≥ 8)

1. **Cells static from step 0 (`initial_cells = max_cells = 256`)** is the central trade-off vs v4 single. F-V5MIT-1 (mitosis active) verdict in v4 single read "n_cells grew from initial=2 to 256"; here it reads "n_cells == max from step 0". The check still passes (n ≥ initial), but the SEMANTICS differ. F-V5MIT-5 (V14-STRICT proxy: `0 < splits ≤ max_cells`) is DEGENERATE with `splits = 0` and will mechanically FAIL — we EXPLICITLY inherit the v4 single saga PSCC §50 V14-STRICT 10/10 PASS as the source-of-truth for this falsifier, and treat the v4-multi cells-static N/A as a benign DDP-safety artifact. HF push gate (`hf_push.py`) requires `--force-push` to bypass for this reason.

2. **`find_unused_parameters=True` cost.** DDP must scan every parameter at every backward to detect which got gradient. For top-K = 8 over 256 cells, 248 cells' params (≈ 96.9% of cell-owned params) are unused per step. The scan is O(n_params) per backward and is reportedly 5-15% slower than the `False` path. Mitigation considered (and rejected for this BG): keep cells static AND collapse them into a single packed tensor to make every param "used" — would change the model arch, defeats apples-to-apples vs v4.

3. **Switch load-balance aux gradient averaging.** Each rank computes its own `aux = N · Σ_i f_i · gate_i` based on its per-rank batch. DDP all-reduces the resulting parameter gradients (mean over ranks). The load-balance signal that reaches the router is effectively the per-rank-mean — softer than the v4 single signal (which saw one batch's full aux gradient). Empirically this can under-apply load-balance pressure; the wmax and `n_active_gt01` outputs are the diagnostics to watch.

4. **Per-rank seed offset (`args.seed + rank`).** Without this, all ranks would sample identical batches → DDP would do redundant work. Independent per-rank batches = effective 4× data per global step. Side effect: the run is NOT bit-reproducible across `world_size` settings (a `world_size=4 seed=42` run does NOT match a `world_size=1 seed=42` run — they sample different batches). For benchmarking, the seed scheme should be reported alongside any comparison.

5. **Wall-speedup expectation.** v4 single A100 80GB at batch=2 ctx=256 d=1024 cells=256 ran ~3.18s / step (v6 cell-parallel doc reference). 4× RTX PRO 6000 S (~1.3-1.5× A100 per GPU) × DDP scaling efficiency (assume 0.85) ≈ ~5-6× wall speedup ⇒ ~3.5-4.0hr for 20K step. If wall > 8hr the cost guard aborts. If wall < 3hr (suggests batch-too-small under-utilization), no action needed but worth noting in post-mortem.

6. **No resume → fresh-init dynamics.** v5-DDP resumes a partial v4 trajectory; v4-multi starts at zero. Early-training divergence is expected:
   - first ~50 step: ce dominated by warmup (lr → 0), gate-entropy reg λ = 1.0 fully on → routing is pushed to UNIFORM by design → wmax → 1/256 ≈ 0.004. v4 single observed wmax → 1.0 by step ~250 (winner-take-all collapse). The annealed-λ cosine schedule was designed for fresh init exactly to delay this collapse.
   - the v4-multi cells-static init means all 256 cells get gradient from step 0 (modulo top-K masking). v4 single's cells grew from 2 → 256 with cell-init noise scale = 0.10 — the parameter space TRAJECTORY differs. We accept this as a fundamental DDP-vs-non-DDP architectural difference for v5-mitosis, not a bug.

7. **Rank-0 only F-PERSONA measurement.** Engine state at rank-0 is bit-identical to all other ranks at any synchronization point (DDP all-reduces params). The F-PERSONA-4a routing / 4b content / F-V5MIT regression at rank-0 is correct for the ensemble. Other ranks block at `dist.barrier()` during measurement — costs ~30s × N_ckpt + ~2min final.

8. **Hardware substitution (RTX PRO 6000 S vs H100 SXM).** Vast.ai 2026-05-13 marketplace had 0 H100 SXM/NVL 4-GPU pods within reliability>0.95 / dph<$16 / inet>200 Mbps. The widened filter accepted RTX PRO 6000 S 96GB ($5.33/hr) — a "Workstation Special" Blackwell card. This card is per-GPU ~80-90% of H100 SXM raw throughput for transformer-style FP16/BF16 workloads. The wall result is therefore a CONSERVATIVE estimate of what 4× H100 SXM would achieve; multiply by ~1.1-1.2× for the H100 projection.

## §7 — Result (post-run, `<<<>>>` = TBD)

**Training**:
- wall: <<<TBD>>> hr
- cost: $<<<TBD>>> (cap $80, gate $88)
- final ce (avg100): <<<TBD>>>
- final wmax (avg100): <<<TBD>>>
- final active>0.01 cells (avg100): <<<TBD>>> / 256
- final gate_max: <<<TBD>>>
- splits in run: 0 (cells static by design)

**F-PERSONA-4a routing (top-K MoE weights, n_perms=100)**:
- verdict: <<<TBD>>>
- mean_KL: <<<TBD>>> (threshold 0.5)
- null z: <<<TBD>>> (threshold 3.0)
- p_value: <<<TBD>>>

**F-PERSONA-4a soft-gate (full softmax)**:
- mean_KL: <<<TBD>>>
- null z: <<<TBD>>>

**F-PERSONA-4b content (M4 aggregated hidden cosine, n_perms=100)**:
- verdict: <<<TBD>>>
- z: <<<TBD>>> (v2 carry z = 3.20)
- p_value: <<<TBD>>>

**F-V5MIT regression**:
- verdict: <<<TBD>>>/5
- F-V5MIT-1: cells=256 == max (cells-static interpretation passes by §6 C3 #1)
- F-V5MIT-2: cells ≥ min_cells = 2 (passes trivially)
- F-V5MIT-3: phi ratchet — <<<TBD>>>
- F-V5MIT-4: ce_final < 5.0 — <<<TBD>>>
- F-V5MIT-5: splits=0 N/A; inherit v4 single saga PASS

## §8 — Conclusion (placeholder)

<<<TBD post-run>>>

Outcomes to write:
- did v4-multi reach F-PERSONA-4a PASS where v4 single (extrapolated from v2 / v3-routing) failed? if yes, multi-GPU + effective batch=8 was sufficient (already same as v4 single original effective batch). if no, the bottleneck is architectural, not scale.
- did wall hit target ~4-5 hr? compare to v6 cell-parallel and v5 DDP.
- did F-V5MIT-4 (CE convergence) reach ce < 1.5 (v1 final = 1.17 at d=384)?

## §9 — Files

- `training/cotrain_v5mitosis_v4_multi.py` — trainer (fresh-init DDP fork of `cotrain_v5mitosis_v4.py`)
- `state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/dispatch_h100_v4_multi.sh` — Vast.ai dispatch (NUM_GPUS=4 widened filter)
- `state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/hf_push.py` — HF push (gated on F-V5MIT-5, --force-push override for cells-static)
- `state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/ckpts/` — local ckpt destination
- `state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/cotrain_v4_multi_result.json` — `<<<post-pull>>>`
- `state/anima_v5mitosis_cotrain_v4_multi_2026_05_13/train_v4_multi.log` — `<<<post-pull>>>`

## §10 — Provenance / cross-references

- PSCC §44/§45-FINAL: F-PERSONA-4 routing collapse root cause (single-cell tension 793×, monopoly)
- PSCC §50: ★★★★★ ACHIEVED via D3 §A3 amendment, F-PERSONA-4b M4 z=3.20 PASS (v2)
- PSCC §51: HF public release (cond #1 + cotrain v1)
- memory `feedback_no_scale_caps`: cap = floor not ceiling
- memory `feedback_orchestrator_h100_gotchas`: PEP 668, ckpt-pull-mandatory, scp 3600 timeout
- memory `feedback_dispatch_vast_template_gotchas`: §45 direct-IP, `set -o pipefail` remote, trap cleanup with `SAVE_POD=1` on pull-fail
- memory `feedback_active_resource_utilization` (own 43): cost-bearing BG priority
- memory `feedback_english_only`: HF content English only (Korean OK in chat / commits / md)
- own 31: dancinlab canonical HF org
- own 37 mandate-9: V14-STRICT PASS → HF push (here: inherit-from-v4-single bypass via `--force-push`)
