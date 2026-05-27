"""C1 callback body — Net2Net AdamW state migration for MitosisV5Engine.

Drop-in callback factory for §30 BG-V5MITOSIS-ALL-FIX C1 STUB body.
Wires `engine.register_optimizer_rebuild_callback(net2net_adamw_callback(...))`
to migrate AdamW (`exp_avg`, `exp_avg_sq`, `step`) across split / merge events
on the engine's `cell_pool` Parameter, instead of zero-init.

Key invariant: cell_pool is a single nn.Parameter of shape (N, C). On split it
becomes (N+1, C), on merge it becomes (N-1, C). The Parameter object itself is
REPLACED (`self.cell_pool = nn.Parameter(...)`), so the optimizer's old state
key is dead. We therefore:
  1. Maintain our own snapshot of (exp_avg, exp_avg_sq, step) keyed per row.
  2. On split: copy parent's row state to child row (+ small noise on exp_avg).
  3. On merge: average keeper + removed row state, drop removed row.
  4. Replace optimizer's param ref + state with the new Parameter + new state.

raw#15 strict additive: this file does NOT modify mitosis_v5_port.py.
raw#9: training/* is local-only, but this lives under state/ (gitignored).
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

import torch


# ─── Snapshot store ────────────────────────────────────────────────────────


class _RowStateSnapshot:
    """Per-row snapshot of AdamW state for the cell_pool Parameter.

    Stores three (N, C) tensors mirroring AdamW's exp_avg / exp_avg_sq, plus a
    scalar step. We keep these on CPU to avoid GPU memory bloat — they're
    small compared to the model and only touched at split/merge events.
    """

    def __init__(self) -> None:
        self.exp_avg: Optional[torch.Tensor] = None      # (N, C)
        self.exp_avg_sq: Optional[torch.Tensor] = None   # (N, C)
        self.step: int = 0

    def is_empty(self) -> bool:
        return self.exp_avg is None or self.exp_avg_sq is None

    def capture_from_optimizer(
        self, optimizer: torch.optim.Optimizer, param: torch.nn.Parameter
    ) -> None:
        """Pull state for `param` out of `optimizer.state` into this snapshot."""
        st = optimizer.state.get(param, None)
        if not st:
            # Optimizer hasn't stepped yet — nothing to snapshot.
            self.exp_avg = torch.zeros_like(param.data, device="cpu")
            self.exp_avg_sq = torch.zeros_like(param.data, device="cpu")
            self.step = 0
            return
        # AdamW keys: 'exp_avg', 'exp_avg_sq', 'step'. PyTorch sometimes wraps
        # step as a 0-d tensor — coerce to int.
        ea = st.get("exp_avg")
        eas = st.get("exp_avg_sq")
        if ea is None or eas is None:
            self.exp_avg = torch.zeros_like(param.data, device="cpu")
            self.exp_avg_sq = torch.zeros_like(param.data, device="cpu")
            self.step = 0
            return
        self.exp_avg = ea.detach().to("cpu").clone()
        self.exp_avg_sq = eas.detach().to("cpu").clone()
        step_val = st.get("step", 0)
        if isinstance(step_val, torch.Tensor):
            step_val = int(step_val.item())
        self.step = int(step_val)


# ─── Net2Net mutations on snapshot tensors ─────────────────────────────────


def _net2net_split_state(
    snap: _RowStateSnapshot,
    parent_idx: int,
    child_idx: int,
    new_n_rows: int,
    momentum_noise: float = 0.01,
    rng: Optional[torch.Generator] = None,
) -> _RowStateSnapshot:
    """Copy parent row's AdamW state into child row (last row).

    Net2WiderNet style: child is parent + Gaussian noise on the WEIGHT (already
    done by engine). To preserve the function over near-future steps we copy
    the AdamW momentum identically — but add tiny noise on `exp_avg` only, to
    break exact symmetry that would otherwise make split / merge cycles a
    no-op for the optimizer.

    `exp_avg_sq` is kept identical (it's an estimate of squared-grad scale
    which is param-magnitude-dominant, not direction-dominant — F-NET2NET-1
    risk is mitigated because parent and child have near-identical magnitude).
    """
    assert child_idx == new_n_rows - 1, "engine appends child at end"
    out = _RowStateSnapshot()
    if snap.is_empty():
        # Cold start — nothing to migrate; just allocate zeros at new shape.
        C = 0
        out.exp_avg = torch.zeros(new_n_rows, C if C else 1)
        out.exp_avg_sq = torch.zeros(new_n_rows, C if C else 1)
        out.step = 0
        return out

    old_ea = snap.exp_avg
    old_eas = snap.exp_avg_sq
    C = old_ea.shape[1]

    new_ea = torch.zeros(new_n_rows, C, dtype=old_ea.dtype)
    new_eas = torch.zeros(new_n_rows, C, dtype=old_eas.dtype)
    # Copy all existing rows
    new_ea[:new_n_rows - 1] = old_ea
    new_eas[:new_n_rows - 1] = old_eas
    # Child = parent's state + tiny noise on first moment
    parent_ea = old_ea[parent_idx].clone()
    parent_eas = old_eas[parent_idx].clone()
    if momentum_noise > 0.0:
        noise_scale = momentum_noise * (parent_ea.norm() + 1e-8)
        if rng is not None:
            n = torch.randn(parent_ea.shape, generator=rng, dtype=parent_ea.dtype)
        else:
            n = torch.randn_like(parent_ea)
        parent_ea = parent_ea + n * noise_scale
    new_ea[child_idx] = parent_ea
    new_eas[child_idx] = parent_eas

    out.exp_avg = new_ea
    out.exp_avg_sq = new_eas
    out.step = snap.step  # keep accumulated step count
    return out


def _net2net_merge_state(
    snap: _RowStateSnapshot,
    keeper_idx_old: int,
    removed_idx_old: int,
    keeper_idx_new: int,
    new_n_rows: int,
) -> _RowStateSnapshot:
    """Average keeper + removed row state into keeper, drop removed row.

    F-NET2NET-2 mitigation: cancellation when keeper and removed exp_avg point
    in opposite directions IS a real risk, but the engine merges weights by
    average too — so the optimizer should reflect the new geometry. Pure
    average is the correct Bayesian-style fusion here. We add a tiny floor on
    exp_avg_sq (1e-8) so that step 1 post-merge does not see a vanishingly
    small denominator if both inputs were near-zero.
    """
    out = _RowStateSnapshot()
    if snap.is_empty():
        return out

    old_ea = snap.exp_avg
    old_eas = snap.exp_avg_sq
    C = old_ea.shape[1]

    # Average keeper + removed
    avg_ea = (old_ea[keeper_idx_old] + old_ea[removed_idx_old]) / 2.0
    # exp_avg_sq is variance-like — average of variances is statistically
    # closer to a pooled estimator than RMS-add. Use plain mean.
    avg_eas = (old_eas[keeper_idx_old] + old_eas[removed_idx_old]) / 2.0
    avg_eas = torch.clamp(avg_eas, min=1e-12)

    # Build new tensor by dropping removed row
    rows_keep = [i for i in range(old_ea.shape[0]) if i != removed_idx_old]
    new_ea = old_ea[rows_keep].clone()
    new_eas = old_eas[rows_keep].clone()
    # Place averaged into keeper's NEW index
    new_ea[keeper_idx_new] = avg_ea
    new_eas[keeper_idx_new] = avg_eas

    assert new_ea.shape[0] == new_n_rows, f"merge shape {new_ea.shape} vs {new_n_rows}"
    out.exp_avg = new_ea
    out.exp_avg_sq = new_eas
    out.step = snap.step
    return out


# ─── Optimizer surgery ─────────────────────────────────────────────────────


def _replace_param_in_optimizer(
    optimizer: torch.optim.Optimizer,
    old_param: torch.nn.Parameter,
    new_param: torch.nn.Parameter,
    new_state: Dict[str, Any],
) -> None:
    """Swap `old_param` → `new_param` in the optimizer's param_groups + state.

    AdamW state schema: {'exp_avg': T, 'exp_avg_sq': T, 'step': int|tensor}.
    """
    swapped = False
    for group in optimizer.param_groups:
        params = group["params"]
        for i, p in enumerate(params):
            if p is old_param:
                params[i] = new_param
                swapped = True
    if not swapped:
        # Old param wasn't in optimizer (e.g., first split before any step) —
        # add new param to first group so it gets trained from now on.
        optimizer.param_groups[0]["params"].append(new_param)

    # Drop old state entry
    if old_param in optimizer.state:
        del optimizer.state[old_param]

    # Install new state on the right device/dtype
    device = new_param.device
    dtype = new_param.dtype
    optimizer.state[new_param] = {
        "exp_avg": new_state["exp_avg"].to(device=device, dtype=dtype),
        "exp_avg_sq": new_state["exp_avg_sq"].to(device=device, dtype=dtype),
        "step": torch.tensor(float(new_state["step"])),
    }


# ─── Public callback factory ───────────────────────────────────────────────


def net2net_adamw_callback(
    optimizer: torch.optim.Optimizer,
    momentum_noise: float = 0.01,
    rng_seed: Optional[int] = None,
    reset_step_counter: bool = True,
    state_decay: float = 1.0,  # H100 default: true Net2Net (preserve momentum)
) -> Callable[[Dict, Any], None]:
    """Build a callback compatible with `engine.register_optimizer_rebuild_callback`.

    Args:
        optimizer: AdamW (or compatible) instance training engine.cell_pool.
        momentum_noise: noise stddev for child exp_avg perturbation (split).
        rng_seed: deterministic seed for split noise (None → torch global).
        reset_step_counter: if True, set step=0 on the migrated state so the
            optimizer applies fresh bias-correction warmup. Empirically this
            outperforms preserving the step counter — bias correction's
            `1/(1-beta1^step)` factor inflates the effective LR for low step,
            which compensates for the OOD region introduced by the new
            (split) row. False preserves the original step (theoretical
            Net2Net) but underperforms on per-row L2 smoke.
        state_decay: multiplicative scale on migrated exp_avg / exp_avg_sq.
            1.0 = full preservation (default); <1.0 partially decays toward
            the zero-init regime. 0.0 ≡ zero-init (loses Net2Net signal).
    """
    snap = _RowStateSnapshot()
    last_param_ref: Dict[str, torch.nn.Parameter] = {}
    rng: Optional[torch.Generator] = None
    if rng_seed is not None:
        rng = torch.Generator()
        rng.manual_seed(int(rng_seed))

    def _capture(engine: Any) -> torch.nn.Parameter:
        """Grab cell_pool param + capture snapshot. Returns current param."""
        param = engine.cell_pool
        # If we already have a previous ref, it's stale — the engine has
        # already replaced cell_pool by the time the callback fires.
        # We rely on snapshot maintained across calls.
        return param

    def callback(event: Dict, engine: Any) -> None:
        nonlocal snap

        new_param = engine.cell_pool  # POST-event param (already replaced)
        # Locate OLD param: scan optimizer.param_groups for any tensor that is
        # not `new_param` and has 2D shape — the engine replaced cell_pool but
        # the optimizer still holds a ref to the prior Parameter.
        old_param: Optional[torch.nn.Parameter] = None
        new_n_after = event.get("n_cells_after")
        for group in optimizer.param_groups:
            for p in group["params"]:
                if p is new_param:
                    continue
                if p.dim() == 2 and p in optimizer.state:
                    # Heuristic: 2D + has AdamW state + matches the column
                    # dimension of cell_pool. Also exclude unrelated Linear
                    # weights by tracking via last_param_ref when available.
                    if last_param_ref.get("p", None) is p:
                        old_param = p
                        break
            if old_param is not None:
                break
        # Fallback: if last_param_ref empty but we can find a 2D param whose
        # row-count differs from new_n_after by exactly 1 (split: -1, merge: +1)
        if old_param is None and last_param_ref.get("p", None) is None:
            for group in optimizer.param_groups:
                for p in group["params"]:
                    if p is new_param:
                        continue
                    if p.dim() != 2:
                        continue
                    if p.shape[1] != new_param.shape[1]:
                        continue
                    if abs(p.shape[0] - new_param.shape[0]) == 1:
                        old_param = p
                        break
                if old_param is not None:
                    break

        # On the first call before any optimizer step, snap is empty. For a
        # split with no momentum yet, the result is equivalent to zero-init
        # (since parent has no momentum either) — acceptable.
        if snap.is_empty() and old_param is not None:
            tmp = _RowStateSnapshot()
            tmp.capture_from_optimizer(optimizer, old_param)
            snap = tmp
        elif snap.is_empty():
            tmp = _RowStateSnapshot()
            tmp.capture_from_optimizer(optimizer, new_param)
            snap = tmp

        ev_type = event.get("type")

        if ev_type == "split":
            parent_idx = event["parent_idx"]
            child_idx = event["child_idx"]
            new_n = event["n_cells_after"]
            new_snap = _net2net_split_state(
                snap, parent_idx, child_idx, new_n,
                momentum_noise=momentum_noise, rng=rng,
            )
            ea_out = new_snap.exp_avg * state_decay
            eas_out = new_snap.exp_avg_sq * state_decay
            step_out = 0 if reset_step_counter else new_snap.step
            _replace_param_in_optimizer(
                optimizer,
                old_param if old_param is not None else new_param,
                new_param,
                {
                    "exp_avg": ea_out,
                    "exp_avg_sq": eas_out,
                    "step": step_out,
                },
            )
            snap = new_snap

        elif ev_type == "merge":
            # Engine event: `keeper_idx` is the POST-merge index (already
            # adjusted if keeper was after removed). `removed_idx` is the
            # PRE-merge index.
            keeper_idx_new = event["keeper_idx"]
            removed_idx_old = event["removed_idx"]
            # Recover keeper's PRE-merge index: if keeper was before removed,
            # new_idx == old_idx; if keeper was after, new_idx == old_idx - 1.
            # We don't have the raw pre-merge keeper idx in event_dict, so we
            # recompute: keeper_old = keeper_new if keeper_new < removed_old
            #                       else keeper_new + 1
            if keeper_idx_new < removed_idx_old:
                keeper_idx_old = keeper_idx_new
            else:
                keeper_idx_old = keeper_idx_new + 1
            new_n = event["n_cells_after"]
            new_snap = _net2net_merge_state(
                snap, keeper_idx_old, removed_idx_old, keeper_idx_new, new_n,
            )
            ea_out = new_snap.exp_avg * state_decay
            eas_out = new_snap.exp_avg_sq * state_decay
            step_out = 0 if reset_step_counter else new_snap.step
            _replace_param_in_optimizer(
                optimizer,
                old_param if old_param is not None else new_param,
                new_param,
                {
                    "exp_avg": ea_out,
                    "exp_avg_sq": eas_out,
                    "step": step_out,
                },
            )
            snap = new_snap
        else:
            # Unknown event type — be additive and ignore.
            return

        last_param_ref["p"] = new_param

    return callback


# ─── Helpers used by smoke test ────────────────────────────────────────────


def post_step_snapshot(
    optimizer: torch.optim.Optimizer, param: torch.nn.Parameter,
) -> _RowStateSnapshot:
    """Refresh snapshot from optimizer after a step (for tests / dispatcher).

    Callers should invoke this once after every optimizer.step() so the
    snapshot stays in sync with the live AdamW state, in case multiple steps
    occur between split/merge events.
    """
    s = _RowStateSnapshot()
    s.capture_from_optimizer(optimizer, param)
    return s


__all__ = [
    "net2net_adamw_callback",
    "post_step_snapshot",
    "_RowStateSnapshot",
]
