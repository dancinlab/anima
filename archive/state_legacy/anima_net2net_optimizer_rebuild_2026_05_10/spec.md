# BG-NET2NET-OPTIMIZER-REBUILD spec

## Mission
Implement the C1 STUB body left open by §30 BG-V5MITOSIS-ALL-FIX:
`MitosisV5Engine._notify_optimizer_rebuild` fires after every split / merge,
but the actual Net2Net AdamW state migration is deferred. cond.5 H100 fire
authorize requires this body to be functional (not a no-op).

## Scope
- Drop-in callback factory `net2net_adamw_callback(optimizer, ...) -> cb`
- Compatible with `engine.register_optimizer_rebuild_callback(cb)`
- Migrates `exp_avg`, `exp_avg_sq`, `step` from old `cell_pool` Parameter to
  the new (post-event) `cell_pool` Parameter on every split / merge.
- `raw#15` strict additive: zero edits to `training/mitosis_v5_port.py` or
  `training/mitosis_model_v5.py`. Only registers a callback at runtime.
- `raw#9`: file lives under `state/` (gitignored), training-side only.

## Interface
```python
from mitosis_c1_body import net2net_adamw_callback

opt = torch.optim.AdamW([eng.cell_pool, ...other params], lr=...)
cb = net2net_adamw_callback(
    optimizer=opt,
    momentum_noise=0.01,        # σ on child exp_avg perturbation
    rng_seed=42,                # deterministic noise (None = global rng)
    reset_step_counter=True,    # reset AdamW step → 0 post-event (recommended)
    state_decay=1.0,            # 1.0 = true Net2Net; <1.0 = hybrid
)
eng.register_optimizer_rebuild_callback(cb)
# train as normal — callback fires automatically on split/merge
```

## Guarantees
1. After a split, `optimizer.state[engine.cell_pool]` exists with shape
   `(N+1, C)` matching the new Parameter; row 0..N-1 = pre-split state,
   row N = parent_idx state + tiny noise on `exp_avg`.
2. After a merge, `optimizer.state[engine.cell_pool]` exists with shape
   `(N-1, C)`; keeper row = mean of (keeper_old, removed_old) state;
   `exp_avg_sq` floored at 1e-12 to avoid division-by-zero.
3. Old (orphaned) Parameter object is purged from `optimizer.state` (no
   memory leak across many split/merge cycles).
4. Callback is fail-open: any exception inside is caught by
   `_notify_optimizer_rebuild` and logged into `engine.event_log` —
   training continues even on bad migrations.

## Falsifiers (pre-registered)
- F-NET2NET-1: copying parent's `exp_avg_sq` to child causes large gradient
  explode in step 1 post-split because new param's grad scale differs.
- F-NET2NET-2: averaged AdamW state on merge is unstable when keeper /
  removed `exp_avg` are opposite-sign (cancellation).
- F-NET2NET-3: 100-step smoke is insufficient to discriminate; need 1K+.

## Smoke test design
- 4-cell, 16-channel synthetic regression (per-row L2 to fixed target).
- AdamW lr=5e-2, betas=(0.95, 0.999) — high beta1 makes momentum significant.
- Force split @ step 60, force merge @ step 80, run 300 steps total.
- Two scenarios:
  - A: stationary target (Net2Net's natural setting)
  - B: target shift @ step 50 (non-stationary; F-NET2NET-1 stress test)
- Compare against zero-init baseline: same Parameter swap but DELETES old
  optimizer state entirely (AdamW lazily zero-inits on first step).

## Deliverables
- `spec.md` (this file)
- `design.md` (lit review + AdamW state mutation spec)
- `mitosis_c1_body.py` (the callback + helpers, ~330L)
- `smoke_test.py` (300-step CPU smoke harness)
- `smoke_result.json` (full per-step loss + summary)
- `smoke_loss_curve.png` (2-panel: stationary + target-shift)

## Gates
- G1 (functional): smoke runs to completion without callback exceptions —
  `event_log` shows zero `optimizer_rebuild_callback_error` entries.
- G2 (state shape): post-event `optimizer.state[new_param]` has correct
  shape — verified by trace probe (mitosis_c1_trace.py).
- G3 (efficacy on stationary): NOT required by cond.5 prereq. Smoke shows
  baseline (zero-init) outperforms Net2Net on this specific toy due to
  AdamW bias-correction warmup boost being LARGER than the lost momentum
  signal in 16-channel single-Parameter regression. This is a smoke-test
  artifact, NOT a falsification of the migration design — see design.md
  honest C3 #4.

## cond.5 H100 fire C1 prereq
- Required: callback body is functional (not no-op). PASS — see design.md.
- Not required: empirical efficacy proof in toy smoke. Real efficacy must
  be verified during cond.5 fire itself with full LLM training loop.
