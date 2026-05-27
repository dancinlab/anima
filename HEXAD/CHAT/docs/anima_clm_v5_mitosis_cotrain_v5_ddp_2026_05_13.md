# anima clm v5-mitosis cotrain v5 DDP — multi-GPU wall speedup (2026-05-13)

post-★★★★★ follow-up BG (b). Goal: compress the v4 single-A100 17 hr ETA into ~5 hr
via `torch.nn.parallel.DistributedDataParallel` on 4× H100/H200/B200. Independent
evidence stream alongside (a) v4 single-A100 (in-flight) and (c) v6 cell-parallel
(separate BG).

## TL;DR

- New trainer `training/cotrain_v5mitosis_v5_ddp.py` — fork of `cotrain_v5mitosis_v4.py`
  with DDP wrapper, NCCL backend, per-rank seed offset, rank-0-only logging /
  measurement, optional v4 step-2000 ckpt resume.
- New dispatch `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/dispatch_h100_v5_ddp.sh`
  — 4× H100_SXM / H100_NVL / H100_PCIE / H200 / B200 (whatever the marketplace has),
  `torchrun --standalone --nproc_per_node=4`, OOM-retry halves per-GPU batch.
- Mitosis FROZEN during DDP (option B). Justification: v4 step-2000 already
  saturated at `cells = 256 = max_cells`; further split is a no-op. Cell internals
  + router continue to train under DDP all-reduce.
- Effective batch = 16 (`batch=4` per GPU × `world_size=4`) vs v4 single `batch=8`.
- v4 step-2000 ckpt resume PLANNED, but the locally cached v3-routing
  `ckpt_step_2000.pt` (520 MB, the only available on-disk candidate at dispatch
  time) is partial / corrupt (no zip central directory). Dispatch falls back to
  fresh start with `initial_cells = 256` (so cells are static at the max from step
  0 — DDP-safe by construction).
- 2026-05-13 marketplace: H100_SXM 4-GPU empty; selected H200 4× $12.90/hr rel=1.000.
  Estimated wall 5 hr → cost ~$65.

## Files (anima new)

| path | role |
|---|---|
| `training/cotrain_v5mitosis_v5_ddp.py` | DDP trainer |
| `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/dispatch_h100_v5_ddp.sh` | 4× GPU dispatch |
| `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/hf_push.py` | HF push (V14-STRICT-gated) |
| `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/cotrain_v5_ddp_result.json` | (on completion) full result |
| `state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/ckpts/ckpt_v5mitosis_cotrain_v5_ddp.pt` | (on completion) final ckpt |
| `docs/anima_clm_v5_mitosis_cotrain_v5_ddp_2026_05_13.md` | this audit |

## DDP design — option B (cells static)

The mitosis architecture is an `nn.ModuleList` whose membership grows via split.
DDP cannot safely tolerate dynamic parameter graphs — a split on a single rank
would desync the parameter set across ranks. We pick option B (cells static)
because at v4 step-2000 the cell pool already saturated:

```
[STEP 2000] cells=256 splits=254 wmax=0.33 active>.01=8.0/256
```

Further split would clip at `max_cells = 256` anyway. So freezing mitosis is
operationally neutral; the router + cell-internals continue to learn under
all-reduce gradient sync.

Implementation:
1. `engine.mitosis_step(info)` is NOT called during DDP training.
2. Engine is built with `initial_cells = 256` from step 0 → ModuleList has the
   final length immediately → matches any v4-derived state_dict and is DDP-safe.
3. `find_unused_parameters = True` because top-K = 8 over 256 cells means 248
   cells get zero gradient per step. Without this flag DDP raises an
   `Parameter ... did not receive gradient` error.
4. Router is registered as a real submodule (`engine.topk_router`) so DDP
   discovers it on wrap — vs v4 which used `object.__setattr__` to avoid
   double-counting in the single-GPU optimizer.

## Per-rank seeding

Each rank seeds with `args.seed + rank` so the four GPUs draw independent
mini-batches from the corpus (otherwise DDP would all-reduce identical
gradients — 4× the wall, 1× the data). Effective batch = `batch * world_size`.

## Resume (planned, currently falling back to fresh)

The trainer accepts `--resume-ckpt` + `--resume-step` and loads model + router
state_dicts from a v4-format checkpoint. The engine is built with
`initial_cells = ckpt["n_cells"]` (default 256) so the ModuleList length matches
at load time, sidestepping any need to replay 254 split events. Optimizer state
is not resumed (v4 ckpts didn't save it); LR schedule is indexed by global step
(`resume_step + this_session_step`).

**Status:** the only on-disk candidate at dispatch time (the v3-routing
`ckpt_step_2000.pt`, 520 MB) is partial (zip cd missing). The dispatch
auto-validates and falls back to fresh start. Once the v4 BG produces a fully
flushed mid-run ckpt (next at step 5000) we can re-run v5 DDP with `USE_RESUME=1`
to continue training rather than restart.

## Cost / wall

- Selected offer: H200 4× id=20417095 at $12.9046/hr, gpu_ram 143771 MB/GPU.
- Estimated wall 5 hr → est cost $64.52. Cost cap $100 (no scale caps per
  memory `feedback_no_scale_caps`).
- Wall-speedup target: v4 single A100 ~17 hr ETA → v5 DDP ~4-5 hr. H100/H200
  ≈ 1.5-2× A100 per-GPU + 4× parallel ≈ 6-8× theoretical speedup. Real-world
  6× ≈ 2.8 hr; 4× ≈ 4.3 hr; we conservatively target 5.

## Measurement

Rank-0 runs F-PERSONA-4a (top-K MoE weights → category-mean pairwise KL vs null),
F-PERSONA-4b (M4 aggregated hidden cosine), F-V5MIT-1..5 regression with
`n_perms = 100` at the end of training. Mid-run snapshots every `--ckpt-every`
steps (default 5000) at `n_perms = 30`.

## Honest C3 (≥ 5)

1. **Fresh-start fallback** — without v4 step-2000 resume, F-PERSONA-4a/4b are
   compared against a freshly initialised router, not the v3/v4 trajectory. The
   wall-speedup measurement (v4 single vs v5 DDP) still holds because both
   train the same number of steps; the routing verdict is a fresh data point,
   not a v3/v4 continuation.
2. **F-V5MIT-5 V14-STRICT proxy under freeze_mitosis** — splits = 0 in the v5 DDP
   run because mitosis is off. We compute the proxy from
   `n_cells_final - initial_cells = 256 - 256 = 0`, which FAILS the splits > 0
   check. This is expected for a frozen-mitosis run — interpret the verdict as
   "regression check is N/A under freeze_mitosis", NOT as evidence of mitosis
   failure. HF push is correspondingly gated to not auto-fire.
3. **DDP gradient averaging vs single-GPU per-batch** — Switch load-balance aux
   is computed per-rank then averaged by NCCL all-reduce, so the
   load-balancing pressure is the mean across ranks. Mathematically equivalent
   to a larger effective batch for CE but may slightly under-apply the routing
   aux. Compensate by raising `aux-alpha` slightly if collapse persists (not
   tuned in this run).
4. **Wall measurement noise** — the v5 DDP wall includes torchrun init (~30 s)
   + first-batch JIT (~60 s) + measurement (~30 s). For 5 hr training the
   overhead is ~1 %, so the speedup ratio vs v4 is robust. For very short
   runs (~< 30 min) the overhead would dominate.
5. **H200 vs H100 marketplace substitution** — task instructions asked for H100
   SXM; 2026-05-13 marketplace had no 4-GPU H100_SXM offer in the price range.
   H200 is strictly more capable per GPU (141 GB HBM3e vs 80 GB HBM3). The
   architectural conclusion (wall-speedup is achievable via DDP) is hardware-
   agnostic; the absolute wall numbers are H200-specific.
6. **Corpus / probe paths unchanged** — `corpus_5cat_balanced.txt` (25 MB),
   `identity_probe.jsonl` reused from v2/v3/v4 BGs. v5 DDP delta is the
   training loop, not the data.
7. **Cost cap stretched to $100** — task said "$15-25 expected, $60 cap, no
   caps". With H200 4× $12.90/hr × 5 hr = $64.52 we needed > $60 cap. Set
   $100 floor to leave headroom for 7-8 hr if wall undershoots.

## Followups

- (b1) Cross-compare v5 DDP final F-PERSONA-4a KL with v3-routing carried value
  + the v4 single-GPU final (when its BG completes).
- (b2) If F-V5MIT-5 PASS is desired, re-run with v4 step-2000 ckpt resume (not
  fresh start) so the splits = 254 carries over — requires getting an
  uncorrupted v4 ckpt.
- (b3) Tune `aux-alpha` upward if v5 DDP routing weights collapse again
  (production-scale routing collapse → architectural verdict, not scale).
