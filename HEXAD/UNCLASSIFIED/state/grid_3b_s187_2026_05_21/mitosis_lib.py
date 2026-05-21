"""mitosis_lib.py — training-time cell-pool with optional aux-loss term.

Clean module factored from `eval3_mitosis.py::CellPool` for use INSIDE the
training step (post-forward, pre-backward). The eval-time CellPool is a
POST-HOC observer of `model.tensions`; this module exposes the same dynamics
but ALSO returns a *differentiable* `aux_loss` tensor so the substrate can
co-adapt to its own mitosis behaviour.

Spec carry: `mitosis_hook_lib.hexa::cell_pool_init` defaults
    MIN_CELLS=2, MAX_CELLS=128, SPLIT_PATIENCE=3, MERGE_THRESHOLD=0.005,
    MERGE_PATIENCE=30, NOISE_SCALE=0.1, adaptive_threshold=mean_w*0.8
    on window=20 of global tension history.

Aux loss design (S187-G hypothesis):
    when a split fires at step s with avg_tension > threshold, we add a
        REWARD term to the substrate proportional to (mean_tension - threshold).
        Concretely:
            L_mitosis = -lambda_mitosis * mean(stacked_tensions[split_cells])
        This is a gentle pull-up on per-layer tension: tensions that JUSTIFIED
        a split get reinforced. If NO split fired this step, L_mitosis = 0.
    Equivalent intuition: "if you decided to specialise, commit to it" —
        the substrate is rewarded for producing decisive tension signals.

S187-G falsifier: 2 pods (vA-ctrl mitosis-active=false vs vA-mit mitosis-active=true).
    Compare final cell count under SAME post-hoc Eval 3 — if active training
    INCREASES splits (substrate co-adapted), hypothesis CONFIRMED. If splits
    are unchanged, mitosis is substrate-emergent, NOT training-dependent.

Failure modes:
    - bnb PagedAdamW8bit can drift on int8 m/v when aux loss is small + noisy.
        S187-G fallback: --mitosis-bnb-disable forces torch.optim.AdamW for the
        mitosis-active pod (carry the option, default off).
    - aux loss can dominate CE if lambda_mitosis too large. Default 0.05
        keeps it < 1% of CE (~3.8) typically.
"""
import math
import random
import torch


MIN_CELLS = 2
MAX_CELLS = 128
SPLIT_PATIENCE = 3
MERGE_THRESHOLD = 0.005
MERGE_PATIENCE = 30
NOISE_SCALE = 0.1
WINDOW = 20
ADAPTIVE_FACTOR = 0.8


class CellPool:
    """Training-time cell pool.

    Cells = light bags of (cell_id, hidden vector, tension_history).
    Hidden vectors are simulated random vectors (not gradient-coupled
    parameters) — they exist so the merge/split topology + Φ computation
    can run. Only the AUX LOSS produced by .step() carries gradient.

    Usage:
        pool = CellPool(d_model=3072, initial_cells=2, seed=1337)
        # inside training step, after forward:
        layer_tensions_tensor = torch.stack([t.mean() for t in tensions])  # (L,)
        aux_loss, info = pool.step(layer_tensions_tensor, step_idx)
        L_total = L_ce + ... + lambda_mitosis * aux_loss
        L_total.backward()
    """
    def __init__(self, d_model, initial_cells=2, seed=1337,
                 min_cells=MIN_CELLS, max_cells=MAX_CELLS,
                 split_patience=SPLIT_PATIENCE,
                 merge_threshold=MERGE_THRESHOLD,
                 merge_patience=MERGE_PATIENCE,
                 noise_scale=NOISE_SCALE,
                 window=WINDOW,
                 adaptive_factor=ADAPTIVE_FACTOR):
        self.rng = random.Random(seed)
        self.d_model = d_model
        self.min_cells = min_cells
        self.max_cells = max_cells
        self.split_patience = split_patience
        self.merge_threshold = merge_threshold
        self.merge_patience = merge_patience
        self.noise_scale = noise_scale
        self.window = window
        self.adaptive_factor = adaptive_factor
        self.next_id = 0
        self.cells = []
        for _ in range(initial_cells):
            self.cells.append(self._make_cell(parent_id=-1, hidden_seed=None, step=0))
        self.event_log = []
        self.tension_history = []
        self.phi_history = []
        self.phi = 0.0
        self.adaptive_threshold = 0.0
        self.split_threshold_eff = 0.0
        self.split_count = 0
        self.merge_count = 0

    def _gauss(self, n, sigma):
        return [self.rng.gauss(0.0, sigma) for _ in range(n)]

    def _make_cell(self, parent_id, hidden_seed, step):
        sigma_init = 1.0 / math.sqrt(self.d_model)
        if hidden_seed is None:
            hidden = self._gauss(self.d_model, sigma_init)
        else:
            hidden = [h + self.rng.gauss(0.0, self.noise_scale) for h in hidden_seed]
        cell = dict(
            cell_id=self.next_id,
            hidden=hidden,
            tension_history=[],
            parent_id=parent_id,
            creation_step=step,
            process_count=0,
        )
        self.next_id += 1
        return cell

    def step(self, layer_tensions_tensor, step_idx):
        """Update cell pool from per-layer tensions; return (aux_loss, info).

        layer_tensions_tensor: torch.Tensor of shape (L,) — per-layer
            mean-tensions, REQUIRED differentiable (do NOT .detach() before
            passing). The aux_loss returned is a tensor with grad fn so the
            substrate co-adapts.

        info: dict with diagnostics (split_fired, n_split_this_step,
            mean_tension_scalar, threshold, pool_size_after, phi).
        """
        device = layer_tensions_tensor.device
        dtype = layer_tensions_tensor.dtype
        L = int(layer_tensions_tensor.shape[0])

        # Float view for scalar-side bookkeeping (NO grad path here).
        with torch.no_grad():
            layer_t_float = layer_tensions_tensor.detach().float().tolist()

        # Per-cell tension assignment: cycle layer tensions across cells.
        n_cells = len(self.cells)
        per_cell_t = [layer_t_float[c_idx % L] for c_idx in range(n_cells)]
        for c_idx, cell in enumerate(self.cells):
            cell["tension_history"].append(per_cell_t[c_idx])
            cell["process_count"] += 1

        # Global pool tension = mean of per-cell-latest
        global_t = sum(per_cell_t) / max(1, n_cells)
        self.tension_history.append(global_t)

        # Adaptive split_threshold (window mean × 0.8)
        win = self.tension_history[-self.window:]
        if len(win) >= 3:
            mean_w = sum(win) / len(win)
            self.adaptive_threshold = mean_w * self.adaptive_factor
            self.split_threshold_eff = self.adaptive_threshold

        # Phi proxy = log(1 + mean pairwise cos dist on hidden vectors)
        self.phi = self._compute_phi()
        self.phi_history.append(self.phi)

        # Split check: collect cell indices that would split this step.
        split_cell_indices = []   # indices into self.cells AT TIME OF CHECK
        split_cell_layer_idx = [] # corresponding layer index (for grad path)
        if len(self.cells) < self.max_cells:
            for ci in range(len(self.cells)):
                cell = self.cells[ci]
                hist = cell["tension_history"]
                if len(hist) < self.split_patience:
                    continue
                recent = hist[-self.split_patience:]
                avg = sum(recent) / len(recent)
                if avg > self.split_threshold_eff and self.split_threshold_eff > 0:
                    split_cell_indices.append(ci)
                    split_cell_layer_idx.append(ci % L)
                    if len(self.cells) + len(split_cell_indices) >= self.max_cells:
                        break

        # Execute splits (bookkeeping side).
        n_split_fired = 0
        for ci in split_cell_indices:
            cell = self.cells[ci]
            child = self._make_cell(
                parent_id=cell["cell_id"],
                hidden_seed=cell["hidden"],
                step=step_idx,
            )
            self.cells.append(child)
            cell["tension_history"] = cell["tension_history"][-3:]  # reset
            self.event_log.append(dict(
                type="split", step=step_idx,
                parent_id=cell["cell_id"], child_id=child["cell_id"],
                avg_tension=sum(cell["tension_history"]) / max(1, len(cell["tension_history"])),
                threshold=self.split_threshold_eff,
                pool_size=len(self.cells),
            ))
            n_split_fired += 1
            self.split_count += 1
            if len(self.cells) >= self.max_cells:
                break

        # Merge check (no grad path — purely bookkeeping)
        if (len(self.cells) > self.min_cells
                and step_idx > 0
                and (step_idx % self.merge_patience == 0)):
            best_pair = None
            best_sim = -1.0
            for i in range(len(self.cells)):
                for j in range(i + 1, len(self.cells)):
                    sim = self._cosine(self.cells[i]["hidden"], self.cells[j]["hidden"])
                    if sim > best_sim:
                        best_sim = sim
                        best_pair = (i, j)
            if best_pair is not None and (1.0 - best_sim) < self.merge_threshold:
                i, j = best_pair
                a, b = self.cells[i], self.cells[j]
                merged = [(a["hidden"][k] + b["hidden"][k]) * 0.5
                          for k in range(self.d_model)]
                older = a if a["creation_step"] <= b["creation_step"] else b
                younger = b if older is a else a
                older["hidden"] = merged
                older["tension_history"].extend(younger["tension_history"][-5:])
                self.cells.remove(younger)
                self.event_log.append(dict(
                    type="merge", step=step_idx,
                    keeper_id=older["cell_id"], removed_id=younger["cell_id"],
                    sim=best_sim, pool_size=len(self.cells),
                ))
                self.merge_count += 1

        # ---- Aux loss (differentiable) ------------------------------------
        # L_mitosis = -mean(layer_tensions[split_layers])   if any split fired
        #           = 0                                     otherwise
        # The NEGATIVE sign means "reward tension that triggered a split".
        # When multiplied by + lambda_mitosis the substrate is pulled to
        # produce HIGHER tension on layers that justified a split.
        if n_split_fired > 0:
            # Pick the layer-tensions that triggered (indices into L).
            # Use torch.index_select to keep grad path live.
            idx_tensor = torch.tensor(
                list(set(split_cell_layer_idx)),
                device=device, dtype=torch.long,
            )
            picked = torch.index_select(layer_tensions_tensor, 0, idx_tensor)
            aux_loss = -picked.mean()
        else:
            # Zero tensor that still depends on layer_tensions (preserves
            # graph; backward through tiny scaled zero is harmless).
            aux_loss = layer_tensions_tensor.sum() * 0.0

        info = dict(
            split_fired=n_split_fired > 0,
            n_split_this_step=n_split_fired,
            mean_tension=float(global_t),
            threshold=float(self.split_threshold_eff),
            pool_size=len(self.cells),
            phi=float(self.phi),
            split_total=self.split_count,
            merge_total=self.merge_count,
        )
        return aux_loss, info

    def _compute_phi(self):
        n = len(self.cells)
        if n < 2:
            return 0.0
        total = 0.0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                total += (1.0 - self._cosine(
                    self.cells[i]["hidden"], self.cells[j]["hidden"]))
                count += 1
        mean_d = total / max(1, count)
        return math.log1p(mean_d)

    @staticmethod
    def _cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) + 1e-10
        nb = math.sqrt(sum(y * y for y in b)) + 1e-10
        return dot / (na * nb)

    def summary(self):
        return dict(
            initial_cells=self.min_cells,
            final_cells=len(self.cells),
            splits=self.split_count,
            merges=self.merge_count,
            next_id=self.next_id,
            phi_initial=self.phi_history[0] if self.phi_history else 0.0,
            phi_final=self.phi_history[-1] if self.phi_history else 0.0,
            n_events=len(self.event_log),
            event_log_head=self.event_log[:30],
            event_log_tail=self.event_log[-30:] if len(self.event_log) > 30 else [],
        )
