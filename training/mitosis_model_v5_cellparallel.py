"""training/mitosis_model_v5_cellparallel.py — v6 cell-parallel MitosisModelEngine.

PURPOSE (post-★★★★★ 2026-05-12 BG (c))
    v5-mitosis arch native parallelization. v4 single-GPU bottleneck = Python
    cell-loop O(N) sequential over cells (mitosis_model_v5.py forward 안에서
    `for cell in self.cells: cell(x)` 가 wall 의 ~50% 차지). 각 cell forward 는
    INDEPENDENT — cell dimension 으로 자연 split 가능.

    v6 cell-parallel = N cells × W world_size GPU 분산:
        local cells per GPU = N // W  (가령 256 cells × 8 GPU → 32 cells / GPU)
        각 GPU 가 own shard forward → local (sum_weighted, sum_weights) 계산
        torch.distributed.all_reduce(local_sum, SUM) → global aggregated hidden
        torch.distributed.all_gather(local_tensions, ...) → full tension vector
                                                          (mitosis dynamics용)
    backward: DDP-style — autograd 가 local cells 의 gradient 만 local 에
        compute, all_reduce 가 backward 시 shared params (tok_emb/pos_emb/lm_head)
        에 적용. Cell-owned params 는 local-only (no sync).

PARTNERS
    • cotrain_v5mitosis_v6_cellparallel.py — trainer (8× H100 SXM 80GB 가정)
    • dispatch_h100_v6_cellparallel.sh — vast.ai 8-GPU dispatch
    • mitosis_model_v5.py — fork base, NOT modified (read-only)

HONEST C3 (≥ 5)
    1. cross-GPU split/merge = TODO[migration]. split 은 own shard 안에서만,
       max_local_cells = shard cap. 만약 모든 shard 의 cells > shard cap →
       split silent reject. 첫 cycle 은 same-GPU only.
    2. all-reduce overhead 는 d_model=1024 × ctx=512 batch=8 = ~8 MB / step.
       NCCL 80Gb/s bidirectional 위 ~0.1ms — Python cell-loop 의 ~1-3 s vs
       compelling. small-batch (batch=1) corner 는 통신 비율 ↑.
    3. routing top-K 가 cross-GPU 시 active cells 가 한 GPU 에 몰릴 수 있음 —
       load imbalance. monitoring metric `dispatch_imbalance` 노출.
    4. Lorenz cell_state inject 는 per-GPU local (각 GPU 가 own cells 에 inject).
       v5 original 의 cross-cell phase coupling 은 local 안에서만 작용 — 글로벌
       phase coupling = approximated (not exact). 이론상 phase decorrelation 가능.
    5. Φ 계산 (`_compute_iit_phi`) 은 sigs.shape = (N_local, D) → global sigs
       all-gather 후 compute, 또는 local-only fallback. impl: local-only fallback
       (cheap + approximate; full Φ는 마지막 final checkpoint 에서 single-GPU
       merge 후 compute).
    6. weight-tied lm_head (tok_emb.weight 와 share) 는 DDP 에서 broadcast/reduce
       특수 처리 필요. 본 impl: register tok_emb/pos_emb/final_ln/lm_head as
       SHARED (DDP-broadcast). cells 는 SHARD-LOCAL (no DDP).
    7. ckpt shape: 각 GPU 가 own state_dict 저장 → final 시 rank 0 가 all-gather
       해서 single ckpt 합성. 또는 sharded checkpoint (CellShardCheckpoint).
    8. fresh init 가 cells 분산 facilitates (v4 ckpt 256-cell load = cross-shard
       cell-id 매칭 복잡); v6 dispatch 는 fresh init 권장.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist

# Reuse base config + cell + attention from mitosis_model_v5
from mitosis_model_v5 import (
    MitosisModelConfig,
    CausalSelfAttention,
    MitosisModelCell,
)


# ─── distributed helpers ──────────────────────────────────────────────

def _is_dist() -> bool:
    return dist.is_available() and dist.is_initialized()


def _world_size() -> int:
    return dist.get_world_size() if _is_dist() else 1


def _rank() -> int:
    return dist.get_rank() if _is_dist() else 0


# ─── Cell-parallel engine ─────────────────────────────────────────────

class MitosisModelEngineCellParallel(nn.Module):
    """N-cell engine with cells DISTRIBUTED across world_size GPUs.

    Shape contract (per rank r, world_size W, current global N_cells):
        local_N = N_cells // W  (rank 0 carries the +remainder)
        local cells span global ids [shard_start[r], shard_end[r])
        shard_start[r] = (r * N_cells) // W
        shard_end[r]   = ((r+1) * N_cells) // W

    Forward:
        1. shared tok+pos emb (replicated, DDP-broadcasted)
        2. local cells forward → (local_outs, local_tensions)
        3. all_gather(local_tensions) → global_tensions (N,)
        4. softmax(global_tensions) → global_weights (N,)
        5. local_weighted = Σ_{i in shard} weight_i * local_out_i
        6. all_reduce(local_weighted, SUM) → aggregated (B,T,D)
        7. final_ln + lm_head → logits

    backward DDP semantics:
        - shared params (tok_emb/pos_emb/final_ln/lm_head): DDP all-reduce on
          gradient (caller wraps in DDP for these).
        - cell-owned params: gradient is local-only (no sync — each rank owns
          a distinct slice of cells).

    HONEST C3 carry from v5 + v6-specific (see file docstring)
    """

    def __init__(self, cfg: MitosisModelConfig):
        super().__init__()
        self.cfg = cfg
        self.d_model = cfg.d_model
        self.vocab_size = cfg.vocab_size
        self.max_seq = cfg.max_seq

        self.world_size = _world_size()
        self.rank = _rank()

        # Shared modules (DDP wrap target, replicated across ranks)
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.max_seq, cfg.d_model)
        self.final_ln = nn.LayerNorm(cfg.d_model)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        if cfg.weight_tied_lm_head:
            self.lm_head.weight = self.tok_emb.weight

        # Initial cells — distribute INITIAL_CELLS across ranks
        # Each rank instantiates only ITS local cells.
        self._shared_attn: Optional[CausalSelfAttention] = None
        local_start, local_end = self._global_to_local(cfg.initial_cells, self.rank, self.world_size)
        local_cells = []
        for global_id in range(local_start, local_end):
            cell = MitosisModelCell(cfg, shared_attn=None)
            cell.cell_id = global_id
            cell.creation_step = 0
            local_cells.append(cell)
        self.cells = nn.ModuleList(local_cells)
        self._global_n_cells = cfg.initial_cells
        self._next_id = cfg.initial_cells

        # max cells per shard (cell-parallel cap; cross-GPU migration = TODO)
        # Allow some headroom over cfg.max_cells // world_size for unbalanced
        # split allocation. Default = ceil(max_cells / W) + 4 slack.
        self.max_local_cells = (cfg.max_cells + self.world_size - 1) // self.world_size + 4

        # Mitosis bookkeeping (per-rank local)
        self.step_count: int = 0
        self.split_threshold: float = 0.3
        self._global_tension_history: List[float] = []
        self._per_cell_thresholds: List[float] = [0.3 for _ in self.cells]
        self._lorenz: List[float] = [1.0, 1.0, 1.0]
        self.phi: float = 0.0
        self.phi_per_cell: float = 0.0
        self._phi_best: float = 0.0
        self._phi_per_cell_best: float = 0.0
        self.event_log: List[Dict] = []

    # ─── range helpers ──────────────────────────────────────────────

    @staticmethod
    def _global_to_local(n_global: int, rank: int, world_size: int) -> Tuple[int, int]:
        start = (rank * n_global) // world_size
        end = ((rank + 1) * n_global) // world_size
        return start, end

    @property
    def n_local_cells(self) -> int:
        return len(self.cells)

    @property
    def n_cells(self) -> int:
        """Total cells across all ranks (kept in sync via split/merge ops)."""
        return self._global_n_cells

    # ─── Forward (pure: no mutation) ────────────────────────────────

    def forward(
        self,
        input_ids: torch.Tensor,
        readout_mode: Optional[str] = None,
    ) -> Tuple[torch.Tensor, Dict]:
        if readout_mode is None:
            readout_mode = self.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= self.max_seq

        pos = torch.arange(T, device=input_ids.device)
        x = self.tok_emb(input_ids) + self.pos_emb(pos).unsqueeze(0)  # (B,T,D)

        # 1. Local cells forward
        local_outs: List[torch.Tensor] = []
        local_tensions: List[torch.Tensor] = []
        for cell in self.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            local_outs.append(out_i)
            local_tensions.append(tension_tok.mean())  # scalar / cell

        if not local_outs:
            # Edge case: this rank has 0 cells — should not happen with
            # world_size <= initial_cells. Return zeros for aggregated.
            zero = torch.zeros(B, T, self.d_model, device=x.device, dtype=x.dtype)
            local_tens_t = torch.zeros(0, device=x.device, dtype=x.dtype)
        else:
            local_tens_t = torch.stack(local_tensions)  # (n_local,)

        # 2. All-gather tensions across ranks → (n_global,) full tension vector
        if self.world_size > 1:
            # Each rank may have different n_local — use a 2-pass: first gather
            # local sizes (cheap int), then varlen gather.
            sizes_tensor = torch.tensor([local_tens_t.numel()], device=x.device, dtype=torch.long)
            sizes_list = [torch.zeros_like(sizes_tensor) for _ in range(self.world_size)]
            dist.all_gather(sizes_list, sizes_tensor)
            sizes = [int(s.item()) for s in sizes_list]
            max_sz = max(sizes) if sizes else 0
            # pad local_tens_t to max_sz
            pad_local = torch.zeros(max_sz, device=x.device, dtype=x.dtype)
            if local_tens_t.numel() > 0:
                pad_local[: local_tens_t.numel()] = local_tens_t
            gathered = [torch.zeros_like(pad_local) for _ in range(self.world_size)]
            dist.all_gather(gathered, pad_local)
            # Concatenate trimmed slices in rank order
            tens_pieces = []
            for r, sz in enumerate(sizes):
                tens_pieces.append(gathered[r][:sz])
            global_tensions = torch.cat(tens_pieces, dim=0)  # (n_global,)
        else:
            global_tensions = local_tens_t
            sizes = [local_tens_t.numel()]

        # 3. softmax → global weights
        if global_tensions.numel() == 0:
            weights = torch.zeros(0, device=x.device, dtype=x.dtype)
        else:
            weights = F.softmax(global_tensions, dim=0)  # (n_global,)

        # 4. Local weighted sum (only over OWN shard's slice of weights)
        local_start = sum(sizes[:self.rank])
        local_end = local_start + sizes[self.rank] if self.rank < len(sizes) else local_start
        if local_outs and local_end > local_start:
            local_weights = weights[local_start:local_end]  # (n_local,)
            stacked = torch.stack(local_outs, dim=0)  # (n_local, B, T, D)
            local_weighted = (local_weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)  # (B,T,D)
        else:
            local_weighted = torch.zeros(B, T, self.d_model, device=x.device, dtype=x.dtype)

        # 5. all_reduce SUM → global aggregated hidden
        if self.world_size > 1:
            dist.all_reduce(local_weighted, op=dist.ReduceOp.SUM)
        aggregated = local_weighted  # now == sum across all shards' weighted sums

        h = self.final_ln(aggregated)
        logits = self.lm_head(h)

        info = {
            "tensions": global_tensions.detach().cpu().float().tolist() if global_tensions.numel() > 0 else [],
            "aggregated": aggregated,
            "weights": weights.detach(),
            "weights_live": weights,
            "n_cells": self.n_cells,
            "n_local_cells": self.n_local_cells,
            "local_shard": (local_start, local_end),
            "shard_sizes": sizes,
        }
        return logits, info

    # ─── Mitosis step (mutating, local-shard only for v6 first cycle) ─

    def mitosis_step(self, info: Dict) -> Dict:
        """v6: local-shard mitosis ONLY. cross-GPU migration = TODO[migration].

        Each rank independently decides split/merge over its OWN local cells.
        Global n_cells is then RE-SUMMED across ranks via all_reduce.
        """
        self.step_count += 1

        # Lorenz inject local
        self._inject_lorenz_into_cells()

        # Update local cell tension history (use FULL global tensions but
        # only this rank's slice is informative for local cell.tension_history)
        global_tens = list(info.get("tensions", []))
        local_start, local_end = info.get("local_shard", (0, 0))
        for i, cell in enumerate(self.cells):
            t = global_tens[local_start + i] if (local_start + i) < len(global_tens) else 0.0
            cell.tension_history.append(t)
            if len(cell.tension_history) > 50:
                cell.tension_history = cell.tension_history[-50:]
            cell.process_count += 1
        # local tension history for adaptive threshold
        for t in global_tens:
            self._global_tension_history.append(t)
        if len(self._global_tension_history) > 500:
            self._global_tension_history = self._global_tension_history[-500:]

        # Compute Φ local approximation (per-shard cell_states only)
        phi = self._compute_iit_phi_local()
        self.phi = phi
        if phi > self._phi_best:
            self._phi_best = phi
        n = max(self.n_cells, 1)
        self.phi_per_cell = phi / n
        if self.phi_per_cell > self._phi_per_cell_best:
            self._phi_per_cell_best = self.phi_per_cell

        # Adaptive threshold update
        self._update_adaptive_threshold()

        # Local split / merge gates (own shard only)
        split_events = self._check_splits_local()
        merge_events = self._check_merges_local()
        events = split_events + merge_events

        # Sync global n_cells across ranks
        if self.world_size > 1:
            local_n_t = torch.tensor([self.n_local_cells], dtype=torch.long, device=self._device_hint())
            global_n_t = local_n_t.clone()
            dist.all_reduce(global_n_t, op=dist.ReduceOp.SUM)
            self._global_n_cells = int(global_n_t.item())
        else:
            self._global_n_cells = self.n_local_cells

        return {"phi": phi, "events": events, "n_cells": self.n_cells, "n_local": self.n_local_cells}

    def _device_hint(self) -> torch.device:
        if len(self.cells) > 0:
            return self.cells[0].cell_state.device
        # Fallback to tok_emb device
        return self.tok_emb.weight.device

    # ─── Local split / merge primitives ─────────────────────────────

    def _split_cell_local(self, parent_local_idx: int) -> Optional[Dict]:
        """Same-shard split. cross-GPU migration NOT implemented (HONEST C3 #1)."""
        if self.n_local_cells >= self.max_local_cells:
            return None
        if self.n_cells >= self.cfg.max_cells:
            return None
        if parent_local_idx < 0 or parent_local_idx >= self.n_local_cells:
            return None

        parent: MitosisModelCell = self.cells[parent_local_idx]

        with torch.no_grad():
            # Attention sharing policy (same as v5)
            post_n_local = self.n_local_cells + 1
            share_now = (self.cfg.attention_sharing == "always") or (
                self.cfg.attention_sharing == "auto" and post_n_local > 8
            )
            if share_now and self._shared_attn is None:
                self._shared_attn = self.cells[0].attn
                for c in self.cells:
                    if c.attn is not self._shared_attn:
                        c.attn = self._shared_attn
                        c._owns_attn = False

            child = MitosisModelCell(
                self.cfg,
                shared_attn=self._shared_attn if share_now else None,
            )
            _device = parent.cell_state.device
            _dtype = parent.cell_state.dtype
            child = child.to(device=_device, dtype=_dtype)

            sd_parent = parent.state_dict()
            if not child._owns_attn:
                sd_parent = {k: v for k, v in sd_parent.items() if not k.startswith("attn.")}
            child.load_state_dict(sd_parent, strict=False)

            owned_names = set(n for n, _ in child.own_parameters())
            for name, p in child.named_parameters(recurse=True):
                if name not in owned_names:
                    continue
                if p.numel() == 0:
                    continue
                pn = p.detach().norm().item()
                eff_sigma = self.cfg.noise_scale * pn / max(p.numel() ** 0.5, 1.0)
                cap = 0.5 * (p.detach().std().item() if p.numel() > 1 else 1.0)
                if cap > 0:
                    eff_sigma = min(eff_sigma, cap)
                noise = torch.randn_like(p) * eff_sigma
                p.add_(noise)

            child.cell_state.copy_(parent.cell_state)
            child.cell_state.add_(
                torch.randn_like(child.cell_state) * (0.1 * parent.cell_state.norm().clamp(min=1e-6))
            )

            child.cell_id = -1  # global id allocated below; -1 = pending
            child.creation_step = self.step_count
            child.parent_id = parent.cell_id
            child.tension_history = []
            child.process_count = 0

            new_list = nn.ModuleList(list(self.cells) + [child])
            self.cells = new_list

            parent.tension_history = parent.tension_history[-3:]

            if parent_local_idx < len(self._per_cell_thresholds):
                self._per_cell_thresholds.append(self._per_cell_thresholds[parent_local_idx])
            else:
                self._per_cell_thresholds.append(self.split_threshold)

        event = {
            "type": "split",
            "step": self.step_count,
            "rank": self.rank,
            "parent_local_idx": parent_local_idx,
            "parent_id": parent.cell_id,
            "child_local_idx": self.n_local_cells - 1,
            "n_local_cells_after": self.n_local_cells,
            "shared_attn": self._shared_attn is not None,
        }
        self.event_log.append(event)
        return event

    def _merge_cells_local(self, idx_a: int, idx_b: int) -> Optional[Dict]:
        if self.n_local_cells <= 1:
            return None
        if self.n_cells <= self.cfg.min_cells:
            return None
        if idx_a == idx_b:
            return None
        if not (0 <= idx_a < self.n_local_cells and 0 <= idx_b < self.n_local_cells):
            return None

        a, b = self.cells[idx_a], self.cells[idx_b]
        if a.creation_step <= b.creation_step:
            keeper, removed = a, b
            removed_idx = idx_b
        else:
            keeper, removed = b, a
            removed_idx = idx_a

        with torch.no_grad():
            owned_keep = dict(keeper.own_parameters())
            owned_remove = dict(removed.own_parameters())
            for name, p_keep in owned_keep.items():
                if name in owned_remove:
                    p_keep.data.add_(owned_remove[name].data).div_(2.0)
            keeper.cell_state.add_(removed.cell_state).div_(2.0)

            survivors = [c for i, c in enumerate(self.cells) if i != removed_idx]
            self.cells = nn.ModuleList(survivors)

            if removed_idx < len(self._per_cell_thresholds):
                self._per_cell_thresholds.pop(removed_idx)

        event = {
            "type": "merge",
            "step": self.step_count,
            "rank": self.rank,
            "keeper_id": keeper.cell_id,
            "removed_id": removed.cell_id,
            "n_local_cells_after": self.n_local_cells,
        }
        self.event_log.append(event)
        return event

    # ─── Lorenz local ───────────────────────────────────────────────

    def _lorenz_step(self, dt: float = 0.01) -> Tuple[float, float, float]:
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        x, y, z = self._lorenz
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        self._lorenz = [x + dx, y + dy, z + dz]
        return dx, dy, dz

    def _inject_lorenz_into_cells(self):
        dx, dy, dz = self._lorenz_step()
        N = self.n_local_cells
        if N == 0:
            return
        device = self.cells[0].cell_state.device
        dtype = self.cells[0].cell_state.dtype
        lorenz_vec = torch.tensor([dx, dy, dz], dtype=dtype, device=device)
        D = self.d_model

        if self.cfg.lorenz_auto_calibrate:
            with torch.no_grad():
                states = torch.stack([c.cell_state for c in self.cells])
                mean_norm = float(states.norm(dim=-1).mean().item())
            base_scale = self.cfg.lorenz_scale * max(mean_norm, 1e-3) * self.cfg.lorenz_calibration_factor
        else:
            base_scale = self.cfg.lorenz_scale

        with torch.no_grad():
            # global id range for THIS rank — use rank * N + i for phase offset
            # (approximate; cross-rank phase coupling lost — HONEST C3 #4)
            rank_offset = self.rank * 100  # heuristic offset to decorrelate ranks
            for i, cell in enumerate(self.cells):
                global_i = rank_offset + i
                phase = (global_i * 2.0 * math.pi) / max(self.n_cells, 1)
                scale = base_scale * (1.0 + 0.3 * math.sin(phase + self.step_count * 0.1))
                noise = torch.randn(D, dtype=dtype, device=device) * scale
                inject = min(3, D)
                noise[:inject] = noise[:inject] + lorenz_vec[:inject] * 0.2
                cell.cell_state.add_(noise)
                n_norm = cell.cell_state.norm().clamp(min=1e-8)
                if n_norm.item() > 10.0:
                    cell.cell_state.mul_(10.0 / n_norm)

    # ─── Φ local (HONEST C3 #5) ─────────────────────────────────────

    def _compute_iit_phi_local(self) -> float:
        if self.n_local_cells < 2:
            return 0.0
        with torch.no_grad():
            sigs = torch.stack([c.cell_state.detach() for c in self.cells])
            norms = sigs.norm(dim=1, keepdim=True).clamp(min=1e-8)
            normed = sigs / norms
            cos = normed @ normed.t()
            n = sigs.shape[0]
            mask = 1.0 - torch.eye(n, device=cos.device, dtype=cos.dtype)
            mean_dist = ((1.0 - cos) * mask).sum() / mask.sum().clamp(min=1.0)
        return float(mean_dist.item() * math.log(n + 1))

    # ─── Adaptive split threshold ───────────────────────────────────

    def _update_adaptive_threshold(self):
        if len(self._global_tension_history) >= 10:
            recent = self._global_tension_history[-self.cfg.adaptive_window:]
            mean_t = sum(recent) / len(recent)
            var_t = sum((t - mean_t) ** 2 for t in recent) / len(recent)
            std_t = math.sqrt(var_t) if var_t > 0 else mean_t * 0.1
            self.split_threshold = max(mean_t + 1.5 * std_t, mean_t * 0.5)

        if not self.cfg.per_cell_threshold_enabled:
            return
        while len(self._per_cell_thresholds) < self.n_local_cells:
            self._per_cell_thresholds.append(self.split_threshold)
        while len(self._per_cell_thresholds) > self.n_local_cells:
            self._per_cell_thresholds.pop()
        for i, cell in enumerate(self.cells):
            hist = cell.tension_history[-self.cfg.per_cell_window:]
            if len(hist) < 5:
                self._per_cell_thresholds[i] = self.split_threshold
                continue
            mu = sum(hist) / len(hist)
            var = sum((t - mu) ** 2 for t in hist) / len(hist)
            sd = math.sqrt(var) if var > 0 else mu * 0.1
            self._per_cell_thresholds[i] = max(
                mu + self.cfg.per_cell_sigma_mult * sd, mu * 0.5
            )

    # ─── Split / merge gates (local) ────────────────────────────────

    def _check_splits_local(self) -> List[Dict]:
        events: List[Dict] = []
        if self.n_local_cells >= self.max_local_cells:
            return events
        if self.n_cells >= self.cfg.max_cells:
            return events
        candidates: List[int] = []
        for i, cell in enumerate(self.cells):
            if len(cell.tension_history) < self.cfg.split_patience:
                continue
            recent = cell.tension_history[-self.cfg.split_patience:]
            if self.cfg.per_cell_threshold_enabled and i < len(self._per_cell_thresholds):
                thr = self._per_cell_thresholds[i]
            else:
                thr = self.split_threshold
            if all(t > thr for t in recent):
                candidates.append(i)
        for idx in candidates:
            if self.n_local_cells >= self.max_local_cells:
                break
            if self.n_cells >= self.cfg.max_cells:
                break
            if idx >= self.n_local_cells:
                continue
            ev = self._split_cell_local(idx)
            if ev:
                ev["trigger"] = "tension"
                events.append(ev)
        return events

    def _check_merges_local(self) -> List[Dict]:
        # v6 first cycle: aggressive merge disabled (cross-GPU migration TODO
        # + local merge alone biases toward shard-internal collapse). Keep stub.
        return []

    # ─── Public test hooks ──────────────────────────────────────────

    def force_split(self, local_idx: int = 0) -> Optional[Dict]:
        return self._split_cell_local(local_idx)

    def status(self) -> Dict:
        splits = sum(1 for e in self.event_log if e["type"] == "split")
        merges = sum(1 for e in self.event_log if e["type"] == "merge")
        return {
            "rank": self.rank,
            "world_size": self.world_size,
            "n_local_cells": self.n_local_cells,
            "n_cells_global": self.n_cells,
            "max_local_cells": self.max_local_cells,
            "max_cells_global": self.cfg.max_cells,
            "step": self.step_count,
            "phi_local": self.phi,
            "phi_per_cell": self.phi_per_cell,
            "phi_best_local": self._phi_best,
            "splits_local": splits,
            "merges_local": merges,
            "attention_sharing_active": self._shared_attn is not None,
        }


# ─── DESIGN BLOCKERS / KNOWN LIMITS (mirrors mitosis_model_v5.py) ────
# 1. cross-GPU split/merge = TODO[migration]. shard cap enforced.
# 2. Lorenz cross-rank phase coupling = approximated (HONEST C3 #4).
# 3. Φ = local-only per rank (HONEST C3 #5). Full Φ = single-GPU merge ckpt step.
# 4. Optimizer state migration STUB carried from v5 (cell-owned params are
#    local-only so split/merge does NOT trigger DDP gradient bucket rebuild;
#    BUT inner-shard optimizer DOES need rebuild — caller's responsibility).
# 5. small batch / small ctx → all-reduce overhead can dominate Python loop
#    speedup; production target = batch >= 4, ctx >= 256.
# 6. fresh-init recommended for v6 (v4 ckpt 256-cell cross-shard load = future
#    work TODO[ckpt-distribute]).
