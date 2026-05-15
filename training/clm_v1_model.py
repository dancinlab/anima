"""training/clm_v1_model.py — .clm v1 from-scratch model (P2 path).

ARCH (spec_frozen.json v0.1 + W8 amendment 2026-05-15):
  - 12-layer base transformer (d=768, n_head=8, ffn=3072) — n_layers=12 satisfied
  - Mitosis branch (64 cells max, MLP per cell) at TOP after base
  - Shared token_emb + pos_emb + final_ln + lm_head (tied)
  - Total target ~180M params

W8 amendment carry (deviations from spec_frozen.json):
  - GQA kv_heads=4 → MHA kv_heads=n_head=8 (cleaner impl, GQA optional)
  - readout_mode "a_only" (Engine G 폐기, single-stack carry)
  - ctx 1024 retained but cost-gated to 256 in initial fire (envelope $25-35)

Mitosis logic (REBORN §88 / PSCC §44 carry):
  - per-cell tension = L2 norm of residual update (MLP output)
  - split if max-tension cell persistently above threshold (split_patience)
  - merge if min-pair-distance cells below threshold (merge_patience)
  - weighted residual sum via softmax(tensions)

References:
  - training/mitosis_model_v5.py (v5 cond.5 cotrain $1.26 H100 SXM, n_layer=1 cells=64)
  - state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain.py (trainer template)
  - state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json (W1 anchor sha256 972e9987...)
"""
from __future__ import annotations
import copy
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─── Config ──────────────────────────────────────────────────────────
@dataclass
class ClmV1Config:
    # Embedding + vocab
    vocab_size: int = 256
    d_model: int = 768
    max_seq: int = 256  # ctx, cost-gated initial fire

    # Base transformer
    n_layers_base: int = 12
    n_head: int = 8
    ffn_dim: int = 3072  # 4 × d_model
    dropout: float = 0.0
    weight_tied_lm_head: bool = True

    # Mitosis branch
    initial_cells: int = 2
    max_cells: int = 64
    min_cells: int = 2
    cell_ffn_dim: int = 1024  # smaller cell FFN to control param count
    split_threshold: float = 0.3
    split_patience: int = 3
    merge_threshold: float = 0.005
    merge_patience: int = 30
    noise_scale: float = 0.10
    adaptive_window: int = 100

    # Init
    seed: int = 42


# ─── Base transformer block ──────────────────────────────────────────
class TransformerBlock(nn.Module):
    """Standard pre-LN transformer block (multi-head attn + FFN)."""
    def __init__(self, cfg: ClmV1Config):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.d_model)
        self.attn = nn.MultiheadAttention(
            cfg.d_model, cfg.n_head, dropout=cfg.dropout, batch_first=True
        )
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.ffn = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.ffn_dim),
            nn.GELU(),
            nn.Linear(cfg.ffn_dim, cfg.d_model),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, _ = x.shape
        mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        h = self.ln2(x)
        x = x + self.ffn(h)
        return x


# ─── Mitosis cell (MLP) ──────────────────────────────────────────────
class MitosisCell(nn.Module):
    """One mitosis cell — pre-LN MLP producing residual update.
    Tension = L2 norm of update (per cell, mean over batch×seq)."""
    def __init__(self, cfg: ClmV1Config):
        super().__init__()
        self.ln = nn.LayerNorm(cfg.d_model)
        self.fc1 = nn.Linear(cfg.d_model, cfg.cell_ffn_dim)
        self.fc2 = nn.Linear(cfg.cell_ffn_dim, cfg.d_model)
        self.cell_id: int = -1
        self.creation_step: int = 0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(F.gelu(self.fc1(self.ln(x))))

    def own_parameters(self):
        for n, p in self.named_parameters():
            yield n, p


# ─── Full model ──────────────────────────────────────────────────────
class ClmV1Model(nn.Module):
    """12L base transformer + mitosis branch (64 cells max).

    Forward returns (logits, info) where info contains:
      - weights:   (n_cells,) softmax of tensions
      - tensions:  (n_cells,) per-cell L2 norm
      - n_cells:   current cell count
    """
    def __init__(self, cfg: ClmV1Config):
        super().__init__()
        self.cfg = cfg
        torch.manual_seed(cfg.seed)

        # Shared embeddings + final_ln + lm_head
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.max_seq, cfg.d_model)
        self.base_blocks = nn.ModuleList([TransformerBlock(cfg) for _ in range(cfg.n_layers_base)])
        self.final_ln = nn.LayerNorm(cfg.d_model)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        if cfg.weight_tied_lm_head:
            self.lm_head.weight = self.tok_emb.weight

        # Mitosis cells branch
        cells = []
        for i in range(cfg.initial_cells):
            c = MitosisCell(cfg)
            c.cell_id = i
            c.creation_step = 0
            cells.append(c)
        self.cells = nn.ModuleList(cells)
        self._next_id: int = cfg.initial_cells

        # Mitosis state
        self.step_count: int = 0
        self._global_tension_history: List[float] = []
        self._per_cell_tension_history: List[List[float]] = [[] for _ in range(cfg.initial_cells)]
        self._merge_pair_history: Dict[Tuple[int, int], List[float]] = {}
        self.phi: float = 0.0
        self.phi_per_cell: float = 0.0
        self.phi_history: List[float] = []
        self.event_log: List[Dict] = []
        self._optimizer_rebuild_callbacks: List = []

    @property
    def n_cells(self) -> int:
        return len(self.cells)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict]:
        """x: (B, T) long. Returns (logits (B,T,vocab), info dict)."""
        B, T = x.shape
        device = x.device
        pos = torch.arange(T, device=device).unsqueeze(0).expand(B, T)
        h = self.tok_emb(x) + self.pos_emb(pos)
        for block in self.base_blocks:
            h = block(h)

        # Mitosis branch — each cell produces (B,T,d), weighted residual sum
        n_cells = len(self.cells)
        cell_outs: List[torch.Tensor] = []
        tensions_grad: List[torch.Tensor] = []  # for graph
        for cell in self.cells:
            out = cell(h)
            cell_outs.append(out)
            # tension = mean L2 norm over batch×seq, with grad
            t = out.norm(dim=-1).mean()
            tensions_grad.append(t)

        # softmax weights (with grad for training)
        tensions_tensor = torch.stack(tensions_grad)
        weights = torch.softmax(tensions_tensor, dim=0)

        # Weighted sum
        stacked = torch.stack(cell_outs, dim=0)  # (n_cells, B, T, d)
        weighted = (weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)  # (B, T, d)
        h = h + weighted

        h = self.final_ln(h)
        logits = self.lm_head(h)

        info = {
            "weights": weights,
            "tensions": tensions_tensor,
            "n_cells": n_cells,
        }
        return logits, info

    def _record_tensions(self, info: Dict) -> None:
        """Update per-cell + global tension history (detached, for mitosis decisions)."""
        tensions = info["tensions"].detach().cpu().tolist()
        global_t = sum(tensions) / max(len(tensions), 1)
        self._global_tension_history.append(global_t)
        while len(self._per_cell_tension_history) < len(tensions):
            self._per_cell_tension_history.append([])
        for i, t in enumerate(tensions):
            self._per_cell_tension_history[i].append(t)
            # cap history length
            if len(self._per_cell_tension_history[i]) > self.cfg.adaptive_window * 2:
                self._per_cell_tension_history[i] = self._per_cell_tension_history[i][-self.cfg.adaptive_window:]

    def _split_cell(self, parent_idx: int) -> Dict:
        """Split parent cell — create a new child by deep-copy + gaussian noise.
        Child params have grad_fn=None (fresh leaves, optimizer rebuilds lazily)."""
        if len(self.cells) >= self.cfg.max_cells:
            return {"type": "split", "skipped": True, "reason": "max_cells"}
        parent = self.cells[parent_idx]
        # Build new cell on parent's device/dtype
        device = next(parent.parameters()).device
        dtype = next(parent.parameters()).dtype
        child = MitosisCell(self.cfg)
        child.to(device=device, dtype=dtype)
        # Copy parent weights + add gaussian noise
        with torch.no_grad():
            for (pn, pp), (cn, cp) in zip(parent.own_parameters(), child.own_parameters()):
                cp.data.copy_(pp.data)
                cp.data.add_(torch.randn_like(cp.data) * self.cfg.noise_scale)
        child.cell_id = self._next_id
        child.creation_step = self.step_count
        self._next_id += 1
        self.cells.append(child)
        # Extend history
        self._per_cell_tension_history.append([])
        ev = {"type": "split", "parent_idx": parent_idx, "child_id": child.cell_id, "step": self.step_count}
        self.event_log.append(ev)
        self._rebuild_optimizer(ev)
        return ev

    def force_split(self, parent_idx: int = 0) -> Dict:
        """Public API for F-V5MIT-1 + F-V5MIT-3 probes."""
        return self._split_cell(parent_idx)

    def _merge_cells(self, idx_a: int, idx_b: int) -> Dict:
        """Merge cell b into a — average weights, keep a, remove b."""
        if len(self.cells) <= self.cfg.min_cells:
            return {"type": "merge", "skipped": True, "reason": "min_cells"}
        a, b = self.cells[idx_a], self.cells[idx_b]
        with torch.no_grad():
            for (an, ap), (bn, bp) in zip(a.own_parameters(), b.own_parameters()):
                ap.data.copy_((ap.data + bp.data) / 2.0)
        # remove b
        new_cells = nn.ModuleList([c for i, c in enumerate(self.cells) if i != idx_b])
        self.cells = new_cells
        # Adjust history
        if idx_b < len(self._per_cell_tension_history):
            del self._per_cell_tension_history[idx_b]
        ev = {"type": "merge", "keeper_idx": idx_a, "removed_idx": idx_b, "step": self.step_count}
        self.event_log.append(ev)
        self._rebuild_optimizer(ev)
        return ev

    def force_merge(self, idx_a: int = 0, idx_b: int = 1) -> Dict:
        """Public API for F-V5MIT-2 probe."""
        return self._merge_cells(idx_a, idx_b)

    def _rebuild_optimizer(self, event: Dict) -> None:
        for cb in self._optimizer_rebuild_callbacks:
            try:
                cb(event, self)
            except Exception:
                pass

    def register_optimizer_rebuild_callback(self, cb) -> None:
        self._optimizer_rebuild_callbacks.append(cb)

    def _compute_iit_phi(self) -> float:
        """Φ★ proxy: mean pairwise L2 distance between cell weight vectors + log(N+1).
        Mirrors anima Φ★ proxy (PSCC §40 + state/anima_d3_verify_2026_05_12 harness)."""
        N = len(self.cells)
        if N < 2:
            return 0.0
        # Concat each cell's params into a single vector
        vecs = []
        for c in self.cells:
            ps = [p.detach().flatten() for _, p in c.own_parameters()]
            vecs.append(torch.cat(ps))
        # Pairwise L2 distances
        total = 0.0
        cnt = 0
        for i in range(N):
            for j in range(i + 1, N):
                # Same length (cells share arch)
                d = (vecs[i] - vecs[j]).norm().item()
                total += d
                cnt += 1
        mpd = total / max(cnt, 1)
        # Normalize by sqrt(dim) for scale invariance
        d_norm = (vecs[0].numel()) ** 0.5
        return float(mpd / d_norm) + math.log(N + 1)

    def mitosis_step(self, info: Dict) -> Dict:
        """Decide split/merge based on tensions + per-cell history."""
        self.step_count += 1
        self._record_tensions(info)

        events: List[Dict] = []
        tensions = info["tensions"].detach().cpu().tolist()

        # Compute per-cell adaptive threshold (mean + 1.5σ)
        for i, t in enumerate(tensions):
            hist = self._per_cell_tension_history[i] if i < len(self._per_cell_tension_history) else []
            if len(hist) < self.cfg.split_patience + 1:
                continue
            recent = hist[-self.cfg.split_patience:]
            window = hist[-self.cfg.adaptive_window:] if len(hist) >= self.cfg.adaptive_window else hist
            if len(window) < 5:
                continue
            mean = sum(window) / len(window)
            var = sum((x - mean) ** 2 for x in window) / max(len(window) - 1, 1)
            std = var ** 0.5
            threshold = mean + 1.5 * std + self.cfg.split_threshold
            # Split if all recent tensions persistently above threshold
            if all(r >= threshold for r in recent) and len(self.cells) < self.cfg.max_cells:
                ev = self._split_cell(i)
                if not ev.get("skipped"):
                    events.append(ev)
                break  # one event per step

        # Merge check: pairs with persistently low pairwise output distance
        if len(self.cells) > self.cfg.min_cells and not events:
            # Use a quick proxy: pair cells with similar tension (low difference)
            sorted_cells = sorted(range(len(tensions)), key=lambda i: tensions[i])
            # Only consider adjacent ranks
            for k in range(len(sorted_cells) - 1):
                a, b = sorted_cells[k], sorted_cells[k + 1]
                pair_key = (min(a, b), max(a, b))
                diff = abs(tensions[a] - tensions[b])
                self._merge_pair_history.setdefault(pair_key, []).append(diff)
                hist = self._merge_pair_history[pair_key]
                if len(hist) > self.cfg.merge_patience:
                    hist[:] = hist[-self.cfg.merge_patience:]
                if (len(hist) >= self.cfg.merge_patience and
                        all(d < self.cfg.merge_threshold for d in hist[-self.cfg.merge_patience:])):
                    ev = self._merge_cells(a, b)
                    if not ev.get("skipped"):
                        events.append(ev)
                        self._merge_pair_history.pop(pair_key, None)
                        break

        # Update phi every adaptive_window steps
        if self.step_count % self.cfg.adaptive_window == 0:
            try:
                self.phi = self._compute_iit_phi()
                self.phi_per_cell = self.phi / max(self.n_cells, 1)
                self.phi_history.append(self.phi)
            except Exception:
                pass

        return {"events": events}


def count_parameters(model: ClmV1Model) -> int:
    return sum(p.numel() for p in model.parameters())


if __name__ == "__main__":
    # Mini smoke
    cfg = ClmV1Config(
        d_model=64, n_layers_base=2, n_head=2, ffn_dim=128, max_seq=16,
        initial_cells=2, max_cells=4, cell_ffn_dim=64,
    )
    m = ClmV1Model(cfg)
    print(f"params: {count_parameters(m):,}  cells: {m.n_cells}")
    x = torch.randint(0, cfg.vocab_size, (2, 16))
    logits, info = m(x)
    print(f"logits: {logits.shape}  weights: {info['weights'].shape}  n_cells: {info['n_cells']}")
    ev = m.force_split(0)
    print(f"after split: cells={m.n_cells} event={ev}")
    ev = m.force_merge(0, 1)
    print(f"after merge: cells={m.n_cells} event={ev}")
    phi = m._compute_iit_phi()
    print(f"phi: {phi:.4f}")
