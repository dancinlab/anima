# anima train DDP (multi-GPU data-parallel) 설계 — Fable 5 위임 산출

> 위임 지시서: state/train_ddp_design/PROMPT.md · cli/train.py(SLW variant) 대상 · 구현=별건 follow-on(N==1 byte-identity gate 선행)

I read `cli/train.py` end-to-end (both this branch's and the `e1-303m` worktree's SLW variant), `core/slw.py::SLWModule`, the `MitosisMoE`/router-mask machinery, and checked forge/flame for multi-device primitives. Three load-bearing findings shape the whole design: **(1) experts are already pre-allocated at Emax and masked** — mitosis never changes parameter shapes, so DDP survives the split with no rebuild; **(2) the SLW module is parameter-only** (its slot state `S` is re-zeroed every forward, no buffers) — no cross-rank state hazard, but its 1024-iteration per-timestep Python loop is a real linear-scaling risk; **(3) forge/flame has zero collective-communication primitives** — hexa parity now would be fake.

Here is the spec.

---

# DDP design spec — `anima train --py --gpus …` (data-parallel, frozen-recipe-faithful)

**Scope**: `cli/train.py` (the e1-303m variant with `--slw` is the target text; everything below applies identically to the non-SLW branch — the delta is only the SLW trailer block). `cli/train.hexa`: follow-on only (§8). Invariant preserved: **global batch, LR, schedule, corpus mix, val stream, and serialize output format are unchanged vs the 1-GPU recipe**. DDP is an execution strategy, not a recipe change; the gate stays held-out DESCENT + engine-native `anima evaluate --py`.

## 0. Architecture decision (one paragraph)

Wrap a **composite "train-shell" module** (model + objective heads + jamo head) in `DistributedDataParallel`, one process per GPU via **torchrun self-re-exec**. Keep **global batch = `--batch-size`** (per-rank `B/N`), keep LR. Data sampling uses a **shared-stream global-replay sampler**: every rank replays the identical RNG stream for the *global* batch and materializes only its slice — the global batch is *byte-identical* to what the 1-GPU run would draw. Mitosis needs **no DDP rebuild** because the model is already allocated at Emax (mask-gated). Validation, DBES, gauges, checkpoints, and serialize are **rank-0 only** on the unwrapped inner model. `world_size==1` short-circuits every DDP branch → byte-identical to today.

## 1. Mitosis expert-split under DDP — **mechanism: pre-allocated-Emax masking (already implemented), split runs identically on all ranks, no rebuild**

The prompt's hardest problem is already solved by the existing code shape: `MitosisMoE` allocates experts + router at Emax from step 0 and masks dormant slots with a `-1e9` router-logit bias (`install_router_mask`). `MitosisMoE.split()` / `tlora_aware_split()` only `copy_`s into pre-existing tensors, flips `active_mask`, and zeroes Adam moments — **no parameter materializes, no optimizer param-group changes, no DDP wrapper rebuild needed**. Justification for keeping this over the alternatives: rebuild-DDP-after-split is pure risk (bucket re-registration, optimizer-state remap) for zero benefit; deterministic-growth would be a rewrite of working code.

What must hold, and why it does:

- **Deterministic split, no RNG**: the child perturbation is the fixed alternating `±1e-4` pattern (`eps[1::2] = -1e-4`), parent is hardcoded `0`, `rb[parent].item()` reads a parameter. Parameters are bitwise-identical across ranks after every step (NCCL allreduce returns the identical result on all ranks; same optimizer math on identical grads ⇒ identical params and identical Adam state). So the split at `split_step` produces bitwise-identical children and mask flips on every rank. **No code change to `split()` itself.**
- **Trigger**: `step == split_step` — step counter is trivially identical across ranks. No change.
- **Dormant experts and DDP's reducer**: dormant experts still run forward (`ex_out = stack([e(x) …])`) and are multiplied by an exactly-zero gate (softmax of `-1e9` underflows to 0.0; `hard_top_k` scatter writes 0) — autograd still reaches their params and delivers exact-zero grads, so **every param's grad hook fires every step** ⇒ `find_unused_parameters=False` is safe both before and after the split (§4).
- **`active_mask` / `e_active`**: deliberately *not* a registered buffer — per-rank plain tensor + int, kept in sync purely by determinism. Keep it that way (a registered buffer + `broadcast_buffers=True` would be an alternative sync mechanism, but §4 sets `broadcast_buffers=False`).
- **Belt-and-braces (cheap, do it)**: immediately after the split, `dist.broadcast` the six touched tensors (parent/child conv weight+bias, router weight+bias — and the TLoRA factor set in the tlora arm) from rank 0, plus `dist.all_reduce(MAX)` on a 1-element tensor holding `float(mito.e_active)` with an assert it equals the local value. Cost: one-time, microseconds. This converts "provably in sync" into "mechanically in sync" and catches any future nondeterminism (e.g., someone adds RNG to the split) at the split instead of as a silent divergence.
- Add a `--ddp-verify-sync` debug flag: every `val_every` steps, all-reduce a param-checksum (sum of `p.sum()` over params) and assert max-min < tolerance. Off by default (costs one collective).

## 2. SAVANT anneal under DDP — **confirmed pure-function-of-step; one required RNG change (per-rank dropout streams)**

- `savant_inhibition(step, …)` is a pure linear function of `step` with a deterministic latch dict (`latch["on"]/"at"` update depends only on `inh`, which depends only on `step`). `inhibition_to_wd`/`inhibition_to_dropout` are pure. **No schedule value is drawn from any generator** — confirmed by reading the function bodies. Each rank computes identical `wd`/`dp` per step; the per-step mutation of `opt.param_groups[…]["weight_decay"]` and `m.p` on `nn.Dropout` modules is per-rank-local and identical. No change needed.
- **The one flag**: dropout *masks* come from the default CUDA RNG, and every rank runs `torch.manual_seed(a.seed)` (needed for identical init). Without intervention, sample *i* on rank 0 and sample *i* on rank 1 get **the same dropout mask** — a correlation the 1-GPU run does not have (there, all B samples draw from one stream). Fix: **after** model construction + DDP wrap, reseed the default RNGs per rank: `torch.manual_seed(a.seed + 100003*(rank+1)); torch.cuda.manual_seed_all(same)`. Only under DDP (`world_size>1`); the N==1 path never reseeds (byte-identity). Order is critical — reseed *before* construction would diverge init (DDP's param broadcast at wrap would paper over it for the shell's params, but don't rely on that).

## 3. Corpus sampler + held-out val — **mechanism: shared-stream global-replay sampler (identical `gen` on all ranks, slice by global index) + rank-0-only full val**

This is the piece that makes the frozen-recipe comparison strongest, and it's *cheaper* than a DistributedSampler port because windows are mmap slices.

**Train sampling** — refactor `get_batch(step)` into two phases:

1. **Spec phase (all ranks, identical)**: keep `gen = torch.Generator().manual_seed(42)` **identical on all ranks** (deliberately *not* rank-offset — this is the inversion vs. the naive per-rank-seed advice). For `b_global in range(B_global)` draw the window spec exactly as today, in today's interleaved order: proportional → one `multinomial(_samp_w,1,generator=gen)` then one `randint(lo,hi,…,generator=gen)`; roundrobin → `cells[(step-1 + b_global) % len(cells)]` then the randint. Replicate the existing edge cases *exactly*: `_window_in` returns None (region `< seq_len+2`) **before** consuming the randint — the spec phase must likewise skip the draw and record the synthetic-fallback spec, or RNG streams desync. Implementation: add `ByteCell.window_spec(seq_len, gen) -> (start|None)` containing only the bounds check + randint (no mmap read), and have `window()` delegate to it (so the N==1 path consumes RNG in the identical order it does today — this keeps N==1 byte-identical).
2. **Materialize phase (per rank)**: rank r materializes only specs `[r*B_local, (r+1)*B_local)` into tensors (mmap slice + `frombuffer`).

**Consequences**: the *global* batch (union over ranks, in global order) is **byte-identical to the 1-GPU batch** for the same seed, for both proportional and roundrobin; the proportional cell weighting is globally exact (not just in expectation); the mean-loss gradient after DDP's average equals the 1-GPU global-batch gradient up to fp reduction order (equal shard sizes ⇒ mean-of-means = global mean; `F.cross_entropy` mean over `B_local·T` with fixed T divides evenly). Spec-phase overhead: `B_global` extra scalar RNG draws per rank per step — nil.

**Batch divisibility (hard part #5 edge)**: require `a.batch_size % world_size == 0`; hard-error at startup otherwise ("`--batch-size 8` with `--gpus` of N∈{2,4,8}; adjust one"). Do **not** pad or round — silent effective-batch change is exactly the frozen-recipe corruption we must refuse.

**Held-out val (the DESCENT gate)** — **rank-0 only, unchanged estimator**: `cell_val_ce`/`val_per_cell` run only on rank 0, on the **inner** model, with the same `val_gen` (seed 1234) and the same cadence (`step==1 / %val_every / final`). Because only rank 0 ever advances `val_gen` and the cadence matches, the val-window stream is **identical to the 1-GPU run's** — the descent trajectory is compared on the same held-out windows, which is what makes the §9 equivalence gate meaningful. Do **not** shard val across ranks or all-reduce a sharded val CE: it changes the estimator, saves seconds, and weakens comparability; val is 4 batches × cells, trivially cheap next to a 3.3 s step. Non-zero ranks skip val entirely and simply wait at the next allreduce (seconds; far under any NCCL timeout). The per-cell weighting/`train_end` boundaries are per-rank-computed but pure functions of file size + `val_frac` — identical everywhere.

**Train-CE metadata (`loss0`/`lossF`, log lines, summary json, `.bin` `val_ce` field)**: per-rank `out["ce_loss"]` is now a shard statistic. All-reduce (AVG) the detached CE each step (one scalar collective, negligible vs 3.3 s) so `loss0`/`lossF`/logs equal the global-batch CE; rank 0 prints.

## 4. Aux trunk-objectives under DDP — **mechanism: one composite shell module wraps model + objfn + jamo_head; `find_unused_parameters=False`**

Problem: `PredictiveInfoObjective` / `ConstructiveBindObjective` (and `JamoHead`) hold learnable params that live *outside* `model` — DDP-wrapping only `model` would silently **never allreduce their grads** (each rank's aux heads drift apart, sculpting different penultimate pressure per rank). Also, the per-step loss composition spans `model(x,y)` *plus* a second trunk pass (`trunk_penultimate(x)`) *plus* head losses; DDP wants one `forward()` producing the backward graph.

**Mechanism** — add:

```python
class TrainShell(nn.Module):
    def __init__(self, model, objfn, jamo_head, …flags):
        super().__init__()
        self.model = model
        self.objfn = objfn if isinstance(objfn, nn.Module) else None
        self._objfn_fn = None if isinstance(objfn, nn.Module) else objfn
        self.jamo_head = jamo_head            # None when jamo off
    def forward(self, x, y, obj_gen, dict_lambda, jamo_lambda):
        # verbatim relocation of the existing per-step block:
        # out = model(x,y); h = trunk_penultimate(x) if need_pen;
        # obj_loss, oaux = objfn(...); + moe aux_loss + dict L1 + jamo CE
        return loss, out["ce_loss"].detach(), aux
```

- Move the *existing* loss-composition block (both the bf16-autocast and fp32 variants — keep the callsite `autocast` context wrapping the DDP call; DDP supports it) into `TrainShell.forward` verbatim, including `trunk_penultimate` (make it a method reading `self.model`). Registering `objfn`/`jamo_head` as submodules puts their params in the DDP bucket set; the double trunk pass is fine (params used twice per iteration accumulate before the grad hook fires — standard DDP behavior).
- Wrap: `ddp = DDP(shell, device_ids=[local_rank], broadcast_buffers=False, find_unused_parameters=False)`.
  - **`find_unused_parameters=False`** — justified statically per run: the objective is fixed for the whole run; `need_pen` is constant; predinfo heads always fire (T=1024 ≫ horizons 1–3); cbind heads always fire; jamo head fires every step when on; `composed_nce`/`infonce`/`ce_marginal` have no params; dormant experts + dormant router rows receive exact-zero-but-present grads (§1); SLW (when `--slw`) is in the main path every step. There is no step-conditional head in the current code. Add `--ddp-find-unused` as an escape hatch and a startup assert comment: any *future* objective that gates a head per-step must flip it (silent alternative = DDP hang/error, which is loud, not silent — acceptable).
  - **`broadcast_buffers=False`** — CLMConvMoE/ByteGPT have no batch-stat buffers (GN/LN + conv; SLW is param-only with per-forward local slot state `S = x.new_zeros(...)`), and `mito.active_mask` is intentionally an unregistered per-rank tensor. Default `True` would add a per-step broadcast of nothing useful and could someday silently stomp a rank-local tensor if one gets registered. Add a startup assert: `len(list(shell.buffers())) == 0` (fail loudly if the model grows a buffer later).
- **`constructive_bind` + fft**: unchanged. The existing code already feeds `.float()` inputs, and sweep.py already drops `--bf16` for cbind; grads and params are fp32, so NCCL allreduce sees fp32 — nothing DDP-specific.
- **Optimizer/clip**: the existing `params` list (model + jamo + objfn) is the same tensor set as `shell.parameters()`; keep building `opt` and `clip_grad_norm_(params, 1.0)` from it. Clipping runs *after* backward, when DDP has already averaged grads — so every rank computes the identical global-gradient norm and identical clip scale, matching the 1-GPU semantics exactly. No change.
- **`obj_gen`**: reseed per rank (`20260628 + a.seed + 7919*rank`) — negatives/permutations are drawn per local shard; identical streams across ranks would correlate negatives across shards in a way the 1-GPU run doesn't. (Exact 1-GPU negative reproduction is impossible anyway — the 1-GPU run draws `(B·T, K)` in one call; this is accepted stochastic-equivalence, covered by the DESCENT gate.)
- **All rank-0 probes** (`dbes_specialization`, `gauge_lib`, `cell_val_ce`, `materialize_experts_into_state`, `_write_clm`) must run on **`shell.model` (the inner module)**, never through the DDP wrapper — keep a `core_model` reference and use it everywhere outside the train step. This also keeps `model.state_dict()` keys prefix-free (no `module.` remapping in serialize).

## 5. Effective batch + LR — **decision: GLOBAL batch preserved, LR untouched**

- Per-rank `B_local = a.batch_size // world_size`; the optimizer sees the same global batch (byte-identical content per §3), same LR, same clip, same wd schedule as the 1-GPU run. **No linear LR scaling, no `--per-rank-batch` option** — offering one invites exactly the silent recipe change we're guarding against. If someone wants a bigger global batch, that's a new recipe and a new frozen bar, not a DDP flag.
- Non-divisible N: hard error (§3). Document in `--gpus` help text.
- Known residual deviations from the 1-GPU loss surface (accepted, listed in §10): MoE load-balance/entropy aux and jamo's `ignore_index` mean are nonlinear batch statistics computed per-shard-then-averaged; with T=1024 the per-shard token counts (≥2048) keep these tight. These are noise-level and covered by the DESCENT gate — do *not* all-gather router probs to fix them (adds comm + code risk for nothing).

## 6. Checkpoint / serialize — **rank-0 only, inner model, barriers around writes**

- `_write_clm` / `_write_bin` / `--ckpt-out` full_sd / `--gauges-out` summary: guard with `rank == 0`, operate on `core_model` (unwrapped — no `model.module` string surgery needed since we keep the reference). `mito.e_active` used by `_write_clm` is identical on all ranks (§1), and the SLW trailer path (`S.append_slw_trailer(out_path, core_model.slw)`) reads `core_model.slw` params — allreduce-synced, so the rank-0 trailer is the global model. Unchanged semantics.
- `--ckpt-every` intermediate writes: same rank-0 guard; add `dist.barrier()` **after** the write (not before — nothing to protect before) so non-zero ranks don't run ahead into the next step's allreduce while rank 0 serializes a 303M `.clm` (correct either way — they'd just block on the collective — but the barrier keeps step wall-times honest in logs and keeps any future collective inserted into the loop from deadlocking against a mid-write rank). Same barrier after the final serialize, then `dist.destroy_process_group()`.
- Final `val_per_cell`, DBES final, gauges, summary print block: rank-0 only. `lossF` written into `.bin` metadata is the all-reduced CE (§3).

## 7. Launch surface — **`--gpus` with torchrun self-re-exec; N==1 short-circuit**

**Contract**: `anima train --py … --gpus 0,1,2,3` (mirrors `anima sweep`'s `--gpus`). Also accepts direct `torchrun --standalone --nproc_per_node=N cli/train.py …` (detected via env), but the anima-canonical path is the flag.

**Mechanism** (top of `main()`, immediately after `parse_args`):

1. `gpu_ids = parse(a.gpus)`; `under_torchrun = "RANK" in os.environ`.
2. **Re-exec branch**: if `len(gpu_ids) > 1 and not under_torchrun`: set `CUDA_VISIBLE_DEVICES=",".join(gpu_ids)`, then `os.execvpe("torchrun", ["torchrun", "--standalone", f"--nproc_per_node={len(gpu_ids)}", os.path.abspath(__file__), *sys.argv[1:]], env)`. exec preserves fds, so the launcher's `> rf 2>&1` result-file redirect keeps working; workers inherit it and only rank 0 prints. `--gpus` stays in argv (workers see `RANK` set, skip the branch, use the flag only for validation). torchrun (vs `mp.spawn`): standard failure propagation, clean per-rank env, no parent CUDA-context pitfalls, and it composes with the launcher's existing "shell-out + second-exec cat" pattern. Single-entry discipline is intact — this is an internal shell-out from the canonical entry, the same pattern `sweep.py`/`train.hexa` already use (pre_bash hooks only agent top-level).
3. **Worker init**: if `under_torchrun` and `WORLD_SIZE > 1`: `local_rank = int(os.environ["LOCAL_RANK"])`; `torch.cuda.set_device(local_rank)`; `device = f"cuda:{local_rank}"`; `dist.init_process_group("nccl")`; `ddp_on = True`; define `rank`, `world`, and `p0(*args)` (rank-0 print; route every existing `print` through it — the mitosis-split line, corpus-cell lines, step logs).
4. **N==1 no-regression short-circuit**: if `--gpus` absent, or one id, or `WORLD_SIZE==1`: `ddp_on = False` and **every** DDP branch is skipped — no process group, no shell wrap (or wrap-and-alias: skip the wrap entirely; the shell class refactor of §4 must itself preserve op order — relocating the loss block into `TrainShell.forward` and calling `shell(x, y, …)` un-wrapped is the same graph, and `ByteCell.window()` delegating to `window_spec()` is the same RNG order), no reseeding, no collectives, no barriers, sampler materializes all `B_global` specs locally. **Acceptance test for the refactor**: 60-step `--canon`-off toy A/B — pre-change vs post-change at N==1, same argv/seed → `sha256(.clm)` must be identical. That's the regression gate before any multi-GPU run.
5. `--gpus` with N>1 but `torch.cuda.device_count() < N`, or N ∤ batch-size: hard error before any allocation.

**Order-of-operations in `main()`** (the sequence matters):
`parse → re-exec/init (7) → torch.manual_seed(a.seed) [all ranks] → build model (+tlora install, +slw via cfg) → MitosisMoE + install_router_mask → warm-start → build objfn/jamo → build TrainShell → DDP wrap (if ddp_on) → per-rank reseed of default RNG + obj_gen (if ddp_on) (§2/§4) → build opt over params → data gens (gen=42 shared, val_gen=1234) → loop`.

## 8. hexa (`cli/train.hexa`) parity — **verdict: py-ONLY now; hexa multi-GPU = follow-on, and honestly a large separate lift**

- I checked: there is **no collective-communication or device-mesh primitive anywhere in forge/flame** (no allreduce/NCCL/multi-device references in the hexa runtime surface in this repo), and `cli/train.hexa` is currently **single-thread CPU-scalar-bound mid-fix** (#2598/#2600) — it does not yet saturate *one* GPU. Multi-GPU hexa would require (a) a collective primitive in the forge runtime (NCCL binding or a hand-rolled ring over CUDA IPC), (b) a multi-process or multi-device execution model in hexa-lang, and (c) the single-GPU util fix landing first. That is a runtime-engineering program, not a trainer patch.
- **Do not fake parity.** Label the hexa side as a scoped follow-on (ING entry: "train.hexa multi-GPU — blocked on forge collective primitive + single-GPU util fix; design mirror = this spec's §1–§6 semantics"), not `구현됨·미배선` (nothing is implemented on the hexa side — that label would be false).
- **Why this doesn't break the byte-parity pair**: the lockstep contract is on the *recipe* — loss arithmetic, SAVANT schedule, mitosis semantics, corpus/held-out layout, `.clm` byte grammar. This design deliberately holds all of those fixed (global batch preserved, LR untouched, same serializer). DDP is an execution strategy of the *same* recipe; `train.hexa` continues to implement that recipe single-GPU. Parity checks (component byte-match fixtures) remain against the N==1 path, which is byte-identical to today.

## 9. DESCENT-gate validation plan (learning-equivalence, not bit-identity)

1. **N==1 byte-identity gate** (refactor regression): toy 60-step A/B, `sha256(.clm)` pre-change vs post-change — must match exactly. Blocks everything else.
2. **Toy DDP equivalence**: same toy config, `--gpus` N=2 vs N=1, same seed, `--val-every` small. Compare the per-cell val_CE trajectory (identical val windows by construction, §3): every val point within noise (bound established by a 1-GPU seed-pair — run seeds 7/8 at N=1, take the max per-point |Δval_CE| as the noise envelope; the N=2 run must sit inside it). Also assert: mitosis split fires at the same step with the same `E` transition; savant `latched_at` identical; final `registers_DESCENT` count identical.
3. **Split-sync assert run**: toy N=4 with `--ddp-verify-sync` — param-checksum agreement across ranks at every val step, especially the first val after `split_step`.
4. **303M dress rehearsal** (short, e.g. 2000 steps on the target pod): N=4 vs the recorded 1-GPU trajectory of the same recipe prefix — val_CE curves overlaid within the seed-noise envelope; wall-time per step reported (expect <N× if SLW latency-bound, §10).
5. **Terminal**: full run's `.clm` through `anima evaluate --py` on the frozen bars — the only tier-eligible verdict, per `a_eval_py_canonical`. Torch-side curve agreement is DIRECTIONAL support only.

## 10. Silent-corruption risks for the frozen-recipe / E1 SLW comparison (the checklist to hold the line on)

1. **Aux-head grads not allreduced** (wrapping only `model`, not the shell) — ranks' objective heads drift; the trunk still trains and DESCENT can still pass, so nothing crashes and the E1 comparison is silently contaminated. The shell wrap (§4) is the defense; assert at startup that `set(shell params) == set(opt params)`.
2. **Global-batch drift** — any per-rank-B-kept default, padding on non-divisible N, or a "helpful" LR autoscale changes the optimizer trajectory vs the frozen bar. Defenses: hard error on N ∤ B; no LR flag; log `global_batch=B (per-rank B/N)` in the header line so the run record proves it.
3. **Sampler seed-offset per rank** (the standard DDP recipe!) — would change the global batch *content and cell mix* vs 1-GPU. This design deliberately shares `gen` and slices (§3); a future "fix" that per-rank-offsets seed 42 would silently break the equivalence — comment the generator line accordingly.
4. **RNG-order drift in the spec/materialize refactor** (e.g., skipping the multinomial for an undersized cell where today's code still draws it, or vice versa) — desyncs ranks *and* breaks N==1 byte-identity. Defense: gate 9.1.
5. **Dropout-mask correlation across ranks** (shared default RNG) or, worse, **reseeding before model construction** (divergent init on non-shell tensors). Defense: strict ordering in §7, reseed only under `ddp_on`.
6. **Val estimator change** (sharded val + allreduce, or non-rank-0 `val_gen` consumption) — DESCENT numbers no longer comparable to the 1-GPU record. Rank-0-only val is the contract.
7. **`lossF`/summary from a shard** — `.bin` metadata and gauges json would carry a 1/N-batch CE; all-reduce before recording.
8. **`broadcast_buffers=True` with a future registered buffer** (or someone registering `active_mask`) — rank-0 state stomps per-rank state mid-run. Defense: `broadcast_buffers=False` + zero-buffer assert.
9. **Serialize through the wrapper** (`module.`-prefixed keys silently passed to `serialize_v3`'s else-branch) — a malformed-but-written `.clm`. Defense: all serialize/probe paths use the `core_model` reference; `clm_decodable` print already runs post-write as a tripwire.
10. **SLW scaling honesty** (`a_wall_first` caveat, not corruption): `SLWModule.forward` is a Python loop of 1024 sequential small GEMMs over `(B_local, d)`; shrinking `B_local` from 8 to 2 barely shrinks that latency term, so with `--slw` the per-step wall has a constant floor and DDP speedup will saturate below N×. Measure s/step at N=1 vs N=4 in gate 9.4 and report honestly; if SLW dominates, the wall-time lever is an SLW batched/scan rewrite (follow-on), **not** growing the global batch.

---

**Change plan for `cli/train.py`, in implementation order**: ① `ByteCell.window_spec()` + `window()` delegation → ② `TrainShell` (relocate loss block + `trunk_penultimate`) with N==1 behavior identical → **run gate 9.1** → ③ `--gpus` + re-exec/init/short-circuit block (§7) → ④ global-replay `get_batch` (spec/materialize split, §3) + divisibility guard → ⑤ DDP wrap + per-rank reseeds (§2/§4) → ⑥ rank-0 guards (`p0`, val/DBES/gauges/serialize/ckpt) + CE allreduce + post-split broadcast/assert (§1) + barriers (§6) → ⑦ `--ddp-verify-sync` → gates 9.2–9.5. Nothing in the `.clm` byte grammar, the SAVANT/mitosis arithmetic, or the eval path changes.