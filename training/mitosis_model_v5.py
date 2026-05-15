"""training/mitosis_model_v5.py — option (a) revised MitosisModel implementation.

PURPOSE
    Track C cond.2 — concrete `nn.Module` implementation of the v5-mitosis
    architecture spec (`docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_10.md`).

    Each cell = a small transformer block with its own {ln1, attn, ln2, ffn_a, ffn_g}.
    Embeddings (tok_emb, pos_emb) and output projection (lm_head) are shared across cells.
    Aggregate per-cell hidden states with softmax(tension) weights BEFORE the single
    shared lm_head.

    raw#15 additive — neither `mitosis_v5_port.py` (instrumentation track B) nor
    `engine_a_g_arch.py` (Engine A/G v5 substrate) is modified.

WHAT THIS FILE PROVIDES
    • `MitosisModelCell(nn.Module)` — single cell = pre-norm transformer block + dual-FFN
      H404 (engine_a − engine_g) with configurable readout mode.
    • `MitosisModelEngine(nn.Module)` — N-cell pool with shared embeddings/lm_head,
      split/merge mechanics, Lorenz cell_state buffer perturbation, IIT Φ readout.
    • Adaptive attention sharing — N≤8 per-cell attn, N>8 fallback to a shared attn ref
      (the parent[0] cell's attn is used as the shared module; new cells reuse it).

HONEST C3 (raw#10):
    1. Optimizer state migration on split is STUBBED — caller must rebuild optimizer.
       For inference-only smoke this is moot. Production cotrain (cond.5) requires (β)
       AdamW reset or (γ) Net2Net momentum copy.
    2. The N>8 attention sharing fallback REPLACES per-cell attn references; it is
       irreversible within a cell pool's lifetime. For research clarity, fallback is
       opt-in via `attention_sharing='auto' | 'never' | 'always'`.
    3. Lorenz inject targets a `cell_state` (D,) buffer added as residual at the input
       of the cell's forward — this is NOT exact mirror of v2's GRUcell hidden (no
       update gate). cond.3 smoke must verify Lorenz on/off split-count delta.
    4. IIT Φ on per-cell hidden mean uses (N, D) tensor; the iit_phi_port import is
       attempted at runtime, with cosine-distance fallback if unavailable.
    5. The merge_threshold=0.005 default (v2 toy scale) almost certainly does NOT
       transfer to d_model=64+ transformer hidden distances. cond.3 smoke calibrates.
    6. Param weight norm scaling on split noise: noise = randn * (noise_scale *
       p.norm() / sqrt(p.numel())). For very small tensors (LayerNorm.bias) the per-
       element σ may exceed weight magnitude → drift. We cap σ at 0.5 × p.std().
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
class MitosisModelConfig:
    vocab_size: int = 256
    d_model: int = 384
    n_head: int = 6
    ffn_dim: int = 1536
    max_seq: int = 256
    n_layer: int = 1                 # cells are at one "layer" each (transformer block depth=1)
    initial_cells: int = 8
    max_cells: int = 64
    min_cells: int = 2
    split_patience: int = 3
    merge_threshold: float = 0.005
    merge_patience: int = 30
    noise_scale: float = 0.10
    lorenz_scale: float = 0.05
    adaptive_window: int = 100
    readout_mode: str = "a_minus_g"  # 'a_minus_g' | 'a_only' | 'a_plus_g'
    attention_sharing: str = "auto"  # 'auto' (N>8 share) | 'never' | 'always'
    weight_tied_lm_head: bool = True
    dropout: float = 0.0
    tie_pos_emb: bool = True
    # ── all-fix 2026-05-10 §30 ────────────────────────────────────────
    # A1: substrate-independent dispersion split trigger (cell-pool L2 top-quartile).
    dispersion_trigger_enabled: bool = True
    dispersion_top_quartile: float = 0.25
    # A2: per-cell adaptive threshold (each cell gates on its own σ window).
    per_cell_threshold_enabled: bool = True
    per_cell_window: int = 100
    per_cell_sigma_mult: float = 1.5
    # D1: Lorenz scale auto-calibration to per-cell signature norm × calibration_factor.
    lorenz_auto_calibrate: bool = True
    lorenz_calibration_factor: float = 1.0


# ─── Causal self-attention with cell_state residual ──────────────────

class CausalSelfAttention(nn.Module):
    """Vanilla causal multi-head self-attention.

    The cell-attached `cell_state` buffer (Lorenz target) is added as residual at the
    cell input BEFORE this attention runs (handled by `MitosisModelCell.forward`).
    """

    def __init__(self, d_model: int, n_head: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_head == 0, f"d_model={d_model} must be divisible by n_head={n_head}"
        self.d_model = d_model
        self.n_head = n_head
        self.d_head = d_model // n_head
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, D = x.shape
        qkv = self.qkv(x).view(B, T, 3, self.n_head, self.d_head).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]                # (B, H, T, d)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.d_head)
        mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
        att = att.masked_fill(mask, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.dropout(att)
        y = (att @ v).transpose(1, 2).contiguous().view(B, T, D)
        return self.out(y)


# ─── Single cell ─────────────────────────────────────────────────────

class MitosisModelCell(nn.Module):
    """One cell = pre-norm transformer block with dual-FFN H404 readout.

    forward(x) → (out, tension)
        out:     (B, T, D)
        tension: (B, T) per-token squared L2 of (a − g) — caller reduces to scalar
    """

    def __init__(self, cfg: MitosisModelConfig, shared_attn: Optional[CausalSelfAttention] = None):
        super().__init__()
        self.cfg = cfg
        self.d_model = cfg.d_model
        self.ln1 = nn.LayerNorm(cfg.d_model)
        if shared_attn is None:
            self.attn = CausalSelfAttention(cfg.d_model, cfg.n_head, dropout=cfg.dropout)
            self._owns_attn = True
        else:
            self.attn = shared_attn        # reference — NOT registered as own parameter dup
            self._owns_attn = False
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.ffn_a = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.ffn_dim),
            nn.GELU(),
            nn.Dropout(cfg.dropout),
            nn.Linear(cfg.ffn_dim, cfg.d_model),
        )
        self.ffn_g = nn.Sequential(
            nn.Linear(cfg.d_model, cfg.ffn_dim),
            nn.GELU(),
            nn.Dropout(cfg.dropout),
            nn.Linear(cfg.ffn_dim, cfg.d_model),
        )
        # Persistent per-cell perturbation channel (Lorenz target, §7)
        self.register_buffer("cell_state", torch.zeros(cfg.d_model))

        # Cell metadata (mirrors v2 mitosis.py Cell dataclass).
        # NOT nn.Parameters — pure python state on the module instance.
        self.cell_id: int = -1
        self.creation_step: int = 0
        self.parent_id: Optional[int] = None
        self.tension_history: List[float] = []
        self.process_count: int = 0

    def own_parameters(self):
        """Iterate parameters owned by THIS cell (skip shared_attn ref).

        Used by split/optimizer migration so we don't re-register a shared attn module.
        """
        for name, p in self.named_parameters(recurse=True):
            if (not self._owns_attn) and name.startswith("attn."):
                continue
            yield name, p

    def forward(self, x: torch.Tensor, readout_mode: str = "a_minus_g") -> Tuple[torch.Tensor, torch.Tensor]:
        # Inject persistent cell_state as residual at the input (§7 (B))
        x_in = x + self.cell_state.view(1, 1, -1)
        h = x_in + self.attn(self.ln1(x_in))
        ln2 = self.ln2(h)
        a = self.ffn_a(ln2)
        g = self.ffn_g(ln2)
        if readout_mode == "a_minus_g":
            delta = a - g
        elif readout_mode == "a_only":
            delta = a
        elif readout_mode == "a_plus_g":
            delta = a + g
        else:
            raise ValueError(f"unknown readout_mode: {readout_mode}")
        out = h + delta
        tension = (delta * delta).mean(dim=-1)            # (B, T)
        return out, tension


# ─── Engine ──────────────────────────────────────────────────────────

class MitosisModelEngine(nn.Module):
    """N-cell pool with shared embeddings + single shared lm_head.

    Mitosis events (split/merge/Lorenz) are exposed as explicit methods (NOT inside
    forward) so the caller controls when to mutate the architecture relative to
    optimizer steps. forward() is pure inference-on-current-shape.
    """

    def __init__(self, cfg: MitosisModelConfig):
        super().__init__()
        self.cfg = cfg
        self.d_model = cfg.d_model
        self.vocab_size = cfg.vocab_size
        self.max_seq = cfg.max_seq

        # Shared embeddings + final norm + lm_head
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.max_seq, cfg.d_model)
        self.final_ln = nn.LayerNorm(cfg.d_model)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        if cfg.weight_tied_lm_head:
            self.lm_head.weight = self.tok_emb.weight

        # Cells — each cell owns its own attn at init (sharing kicks in only after split if auto)
        self._shared_attn: Optional[CausalSelfAttention] = None
        cells = []
        for i in range(cfg.initial_cells):
            cell = MitosisModelCell(cfg, shared_attn=None)
            cell.cell_id = i
            cell.creation_step = 0
            cells.append(cell)
        self.cells = nn.ModuleList(cells)
        self._next_id = cfg.initial_cells

        # Mitosis state (parallel to v2 + mitosis_v5_port)
        self.step_count: int = 0
        self.split_threshold: float = 0.3
        self._global_tension_history: List[float] = []
        # all-fix A2: per-cell threshold list (parallel to self.cells)
        self._per_cell_thresholds: List[float] = [0.3 for _ in range(cfg.initial_cells)]
        self._inter_repulsion_history: Dict[Tuple[int, int], List[float]] = {}
        self._lorenz: List[float] = [1.0, 1.0, 1.0]
        # all-fix B1: phi_per_cell secondary tracking (R6 risk mitigation)
        self.phi: float = 0.0
        self.phi_per_cell: float = 0.0
        self.phi_history: List[float] = []
        self.phi_per_cell_history: List[float] = []
        self._phi_best: float = 0.0
        self._phi_per_cell_best: float = 0.0
        self._best_cell_states: Optional[List[torch.Tensor]] = None
        self.event_log: List[Dict] = []
        # all-fix C1 (R2 STUB): optimizer rebuild callbacks
        self._optimizer_rebuild_callbacks: List = []

        # IIT Φ port — lazy import (so file is importable even without numpy)
        self._iit_fn = None
        try:
            import importlib, sys, os
            iit_dir = "/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10"
            if iit_dir not in sys.path:
                sys.path.insert(0, iit_dir)
            mod = importlib.import_module("iit_phi_port")
            self._iit_fn = getattr(mod, "compute_iit_phi", None)
        except Exception:
            self._iit_fn = None

    # ─── Convenience properties ─────────────────────────────────────

    @property
    def n_cells(self) -> int:
        return len(self.cells)

    def status(self) -> Dict:
        return {
            "n_cells": self.n_cells,
            "max_cells": self.cfg.max_cells,
            "step": self.step_count,
            "phi": self.phi,
            "phi_per_cell": self.phi_per_cell,           # all-fix B1
            "phi_best": self._phi_best,
            "phi_per_cell_best": self._phi_per_cell_best,  # all-fix B1
            "split_threshold": self.split_threshold,
            "per_cell_thresholds_min": min(self._per_cell_thresholds) if self._per_cell_thresholds else None,
            "per_cell_thresholds_max": max(self._per_cell_thresholds) if self._per_cell_thresholds else None,
            "lorenz_calibration_factor": self.cfg.lorenz_calibration_factor,
            "splits": sum(1 for e in self.event_log if e["type"] == "split"),
            "splits_by_dispersion": sum(
                1 for e in self.event_log
                if e.get("type") == "split" and "dispersion" in (e.get("trigger") or "")
            ),
            "merges": sum(1 for e in self.event_log if e["type"] == "merge"),
            "ratchets": sum(1 for e in self.event_log if e["type"] == "ratchet_restore"),
            "events_total": len(self.event_log),
            "attention_sharing_active": self._shared_attn is not None,
        }

    # ─── Forward (pure: no mutation) ────────────────────────────────

    def forward(
        self,
        input_ids: torch.Tensor,
        readout_mode: Optional[str] = None,
    ) -> Tuple[torch.Tensor, Dict]:
        """Pure forward — no mitosis side effect. Caller must invoke `mitosis_step()`
        separately when ready to mutate.

        Args:
            input_ids: (B, T) long tensor, T ≤ cfg.max_seq.
            readout_mode: optional override; default = cfg.readout_mode.

        Returns:
            (logits: (B, T, V), info: Dict {tensions, aggregated, weights})
        """
        if readout_mode is None:
            readout_mode = self.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= self.max_seq, f"T={T} exceeds max_seq={self.max_seq}"

        pos = torch.arange(T, device=input_ids.device)
        x = self.tok_emb(input_ids) + self.pos_emb(pos).unsqueeze(0)   # (B, T, D)

        cell_outs: List[torch.Tensor] = []
        cell_tensions_scalar: List[torch.Tensor] = []
        for cell in self.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            cell_outs.append(out_i)
            cell_tensions_scalar.append(tension_tok.mean())            # scalar per cell

        tens = torch.stack(cell_tensions_scalar)                       # (N,)
        weights = F.softmax(tens, dim=0)                               # (N,)
        stacked = torch.stack(cell_outs, dim=0)                        # (N, B, T, D)
        aggregated = (weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)  # (B, T, D)

        h = self.final_ln(aggregated)
        logits = self.lm_head(h)                                       # (B, T, V)

        info = {
            "tensions": [t.item() for t in cell_tensions_scalar],
            "aggregated": aggregated,
            "weights": weights.detach(),
            "n_cells": self.n_cells,
        }
        return logits, info

    # ─── Mitosis step (mutating; call AFTER forward / loss.backward) ─

    def mitosis_step(self, info: Dict) -> Dict:
        """One mitosis observation cycle.

        info: the dict returned by forward() — must include 'tensions'.
        Returns: events list + Φ.
        """
        self.step_count += 1
        per_cell_tensions: List[float] = list(info["tensions"])

        # 1. Lorenz inject (mutates cell.cell_state buffers)
        self._inject_lorenz_into_cells()

        # 2. Update tension histories
        for i, cell in enumerate(self.cells):
            t = per_cell_tensions[i] if i < len(per_cell_tensions) else 0.0
            cell.tension_history.append(t)
            if len(cell.tension_history) > 50:
                cell.tension_history = cell.tension_history[-50:]
            cell.process_count += 1
            self._global_tension_history.append(t)
        if len(self._global_tension_history) > 500:
            self._global_tension_history = self._global_tension_history[-500:]

        # 3. Inter-cell repulsion proxy (cell_state pairwise L2) — for merge gate
        with torch.no_grad():
            states = torch.stack([c.cell_state for c in self.cells])  # (N, D)
            for i in range(self.n_cells):
                for j in range(i + 1, self.n_cells):
                    d = ((states[i] - states[j]) ** 2).mean().item()
                    key = (i, j)
                    self._inter_repulsion_history.setdefault(key, []).append(d)
                    if len(self._inter_repulsion_history[key]) > 30:
                        self._inter_repulsion_history[key] = self._inter_repulsion_history[key][-30:]

        # 4. Φ + ratchet
        phi = self._compute_iit_phi()
        self._phi_ratchet(phi)

        # 5. Adaptive split threshold update
        self._update_adaptive_threshold()

        # 6. Split / merge gates
        split_events = self._check_splits()
        merge_events = self._check_merges()
        events = split_events + merge_events
        return {"phi": phi, "events": events, "n_cells": self.n_cells}

    # ─── Split / merge primitives ───────────────────────────────────

    def _split_cell(self, parent_idx: int) -> Optional[Dict]:
        """Function-preserving split — deepcopy parent + 10% noise per param."""
        if self.n_cells >= self.cfg.max_cells:
            return None
        if parent_idx < 0 or parent_idx >= self.n_cells:
            return None

        parent: MitosisModelCell = self.cells[parent_idx]

        # Decide attn ownership for child based on attention_sharing policy
        post_n = self.n_cells + 1
        share_now = self._should_share_attention(post_n)

        with torch.no_grad():
            if share_now and self._shared_attn is None:
                # promote first cell's attn to shared (or build a fresh shared module)
                # Use parent[0]'s attn module as the canonical shared ref.
                self._shared_attn = self.cells[0].attn
                # Re-point all existing cells to the shared attn
                for c in self.cells:
                    if c.attn is not self._shared_attn:
                        c.attn = self._shared_attn
                        c._owns_attn = False

            child = MitosisModelCell(
                self.cfg,
                shared_attn=self._shared_attn if share_now else None,
            )
            # Move child to parent's device + dtype BEFORE state copy / noise.
            # Without this, freshly-constructed child cells live on CPU while
            # parent is on cuda — runtime device mismatch on copy_/add_/randn_like.
            _device = parent.cell_state.device
            _dtype = parent.cell_state.dtype
            child = child.to(device=_device, dtype=_dtype)

            # Copy parent state_dict — but skip 'attn.*' if child uses shared ref
            sd_parent = parent.state_dict()
            if not child._owns_attn:
                sd_parent = {k: v for k, v in sd_parent.items() if not k.startswith("attn.")}
            child.load_state_dict(sd_parent, strict=False)

            # Add 10% Gaussian noise per OWNED parameter (skip shared attn)
            owned_names = set(n for n, _ in child.own_parameters())
            for name, p in child.named_parameters(recurse=True):
                if name not in owned_names:
                    continue
                if p.numel() == 0:
                    continue
                # Per-parameter scaled σ — small enough to preserve learned structure
                pn = p.detach().norm().item()
                eff_sigma = self.cfg.noise_scale * pn / max(p.numel() ** 0.5, 1.0)
                # Cap at 0.5 × tensor std to prevent LN-bias drift (HONEST C3 #6)
                cap = 0.5 * (p.detach().std().item() if p.numel() > 1 else 1.0)
                if cap > 0:
                    eff_sigma = min(eff_sigma, cap)
                noise = torch.randn_like(p) * eff_sigma
                p.add_(noise)

            # Also copy + perturb cell_state buffer
            child.cell_state.copy_(parent.cell_state)
            child.cell_state.add_(torch.randn_like(child.cell_state) * (0.1 * parent.cell_state.norm().clamp(min=1e-6)))

            # Metadata
            child.cell_id = self._next_id
            self._next_id += 1
            child.creation_step = self.step_count
            child.parent_id = parent.cell_id
            child.tension_history = []
            child.process_count = 0

            # ModuleList rebuild — append child
            new_list = nn.ModuleList(list(self.cells) + [child])
            self.cells = new_list

            # Parent tension reset
            parent.tension_history = parent.tension_history[-3:]

            # all-fix A2: extend per-cell threshold list — child inherits parent's threshold
            if parent_idx < len(self._per_cell_thresholds):
                self._per_cell_thresholds.append(self._per_cell_thresholds[parent_idx])
            else:
                self._per_cell_thresholds.append(self.split_threshold)

        event = {
            "type": "split",
            "step": self.step_count,
            "parent_id": parent.cell_id,
            "child_id": child.cell_id,
            "n_cells_after": self.n_cells,
            "shared_attn": self._shared_attn is not None,
        }
        self.event_log.append(event)
        # all-fix C1 STUB: notify optimizer rebuild callbacks
        self._notify_optimizer_rebuild(event)
        return event

    def _merge_cells(self, idx_a: int, idx_b: int) -> Optional[Dict]:
        """Merge two cells — parameter-wise average; drop younger; ModuleList rebuild."""
        if self.n_cells <= self.cfg.min_cells:
            return None
        if idx_a == idx_b:
            return None
        if not (0 <= idx_a < self.n_cells and 0 <= idx_b < self.n_cells):
            return None

        a, b = self.cells[idx_a], self.cells[idx_b]
        if a.creation_step <= b.creation_step:
            keeper, removed = a, b
            keeper_idx, removed_idx = idx_a, idx_b
        else:
            keeper, removed = b, a
            keeper_idx, removed_idx = idx_b, idx_a

        with torch.no_grad():
            # Average all owned parameters (skip shared attn if any)
            owned_keep = dict(keeper.own_parameters())
            owned_remove = dict(removed.own_parameters())
            for name, p_keep in owned_keep.items():
                if name in owned_remove:
                    p_keep.data.add_(owned_remove[name].data).div_(2.0)
            # Average cell_state buffer too
            keeper.cell_state.add_(removed.cell_state).div_(2.0)

            # Rebuild ModuleList without removed cell
            survivors = [c for i, c in enumerate(self.cells) if i != removed_idx]
            self.cells = nn.ModuleList(survivors)

            # all-fix A2: drop the removed cell's per-cell threshold entry
            if removed_idx < len(self._per_cell_thresholds):
                self._per_cell_thresholds.pop(removed_idx)

        # Drop inter-repulsion entries that referenced removed_idx
        keys_drop = [k for k in self._inter_repulsion_history if removed_idx in k]
        for k in keys_drop:
            del self._inter_repulsion_history[k]

        event = {
            "type": "merge",
            "step": self.step_count,
            "keeper_id": keeper.cell_id,
            "removed_id": removed.cell_id,
            "n_cells_after": self.n_cells,
        }
        self.event_log.append(event)
        # all-fix C1 STUB: notify optimizer rebuild callbacks
        self._notify_optimizer_rebuild(event)
        return event

    # ─── Adaptive attention sharing policy ──────────────────────────

    def _should_share_attention(self, post_n: int) -> bool:
        if self.cfg.attention_sharing == "always":
            return True
        if self.cfg.attention_sharing == "never":
            return False
        return post_n > 8

    # ─── Lorenz autonomous chaos (Law 86) ───────────────────────────

    def _lorenz_step(self, dt: float = 0.01) -> Tuple[float, float, float]:
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        x, y, z = self._lorenz
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        self._lorenz = [x + dx, y + dy, z + dz]
        return dx, dy, dz

    def _inject_lorenz_into_cells(self):
        """Update per-cell `cell_state` buffer with Lorenz-driven phase-offset noise.

        v2 mitosis.py L388-405 mirror — but applied to a buffer (not GRU hidden) since
        v5 cells are stateless transformer blocks (HONEST C3 #3 / spec §7.1).

        all-fix D1 (R1 risk): when `lorenz_auto_calibrate=True`, multiply lorenz_scale
        by mean(cell_state.norm()) × calibration_factor instead of fixed 0.05. At
        d=384 this prevents the noise from being dwarfed by attention magnitudes.
        """
        dx, dy, dz = self._lorenz_step()
        N = self.n_cells
        if N == 0:
            return
        device = self.cells[0].cell_state.device
        dtype = self.cells[0].cell_state.dtype
        lorenz_vec = torch.tensor([dx, dy, dz], dtype=dtype, device=device)
        D = self.d_model

        # D1: auto-calibration scaling
        if self.cfg.lorenz_auto_calibrate:
            with torch.no_grad():
                states = torch.stack([c.cell_state for c in self.cells])
                mean_norm = float(states.norm(dim=-1).mean().item())
            base_scale = self.cfg.lorenz_scale * max(mean_norm, 1e-3) * self.cfg.lorenz_calibration_factor
        else:
            base_scale = self.cfg.lorenz_scale

        with torch.no_grad():
            for i, cell in enumerate(self.cells):
                phase = (i * 2.0 * math.pi) / max(N, 1)
                scale = base_scale * (1.0 + 0.3 * math.sin(phase + self.step_count * 0.1))
                noise = torch.randn(D, dtype=dtype, device=device) * scale
                inject = min(3, D)
                noise[:inject] = noise[:inject] + lorenz_vec[:inject] * 0.2
                cell.cell_state.add_(noise)
                # clamp norm 10.0 (v2 L403-405)
                n_norm = cell.cell_state.norm().clamp(min=1e-8)
                if n_norm.item() > 10.0:
                    cell.cell_state.mul_(10.0 / n_norm)

    def set_lorenz_scale_calibration(self, factor: float) -> None:
        """all-fix D1: setter for lorenz_calibration_factor (R1 risk mitigation)."""
        self.cfg.lorenz_calibration_factor = float(factor)

    # ─── IIT Φ readout ──────────────────────────────────────────────

    def _per_cell_signature(self) -> torch.Tensor:
        """Return (N, D) tensor — per-cell representative vector.

        Spec §5.1 (i): use cell_state buffer as the persistent per-cell signature
        (input-independent so Φ trajectory is comparable across forwards).
        """
        with torch.no_grad():
            sigs = torch.stack([c.cell_state.detach() for c in self.cells])
        return sigs

    def _compute_iit_phi(self) -> float:
        """Primary metric: IIT Φ (spatial_phi_unnormalized) via iit_phi_port if importable;
        else cosine-distance fallback proxy.
        """
        sigs = self._per_cell_signature()
        if sigs.shape[0] < 2:
            return 0.0
        if self._iit_fn is not None:
            try:
                out = self._iit_fn(sigs, n_bins=16)
                # primary = spatial_phi_unnormalized (BG-IIT-METRIC finding)
                return float(out.get("spatial_phi_unnormalized", out.get("phi", 0.0)))
            except Exception:
                pass
        # Fallback: cosine-distance proxy · log(N+1)
        cells = sigs
        norms = cells.norm(dim=1, keepdim=True).clamp(min=1e-8)
        normed = cells / norms
        cos = normed @ normed.t()
        n = cells.shape[0]
        mask = 1.0 - torch.eye(n, device=cos.device, dtype=cos.dtype)
        mean_dist = ((1.0 - cos) * mask).sum() / mask.sum().clamp(min=1.0)
        return float(mean_dist.item() * math.log(n + 1))

    def _phi_ratchet(self, phi: float):
        """DD55 conservation — restore 80/20 blend of cell_state buffers if Φ drops > 20%.

        all-fix B1 (R6 risk): use phi_per_cell (= phi_total / n_cells) as comparator,
        not phi_total. Without B1, phi_total scales super-linearly with N, so
        phi_best ratchets monotonically just from N growth — masking real per-cell
        Φ degradation. With B1, ratchet fires on actual quality drop.
        """
        n = max(self.n_cells, 1)
        self.phi = phi
        self.phi_history.append(phi)
        phi_per_cell = phi / n
        self.phi_per_cell = phi_per_cell
        self.phi_per_cell_history.append(phi_per_cell)

        if phi > self._phi_best:
            self._phi_best = phi  # legacy field current
        if phi_per_cell > self._phi_per_cell_best:
            self._phi_per_cell_best = phi_per_cell
            with torch.no_grad():
                self._best_cell_states = [c.cell_state.detach().clone() for c in self.cells]
        elif (
            self._best_cell_states is not None
            and self._phi_per_cell_best > 0
            and phi_per_cell < self._phi_per_cell_best * 0.8
        ):
            with torch.no_grad():
                k = min(len(self._best_cell_states), self.n_cells)
                for i in range(k):
                    cur = self.cells[i].cell_state
                    best = self._best_cell_states[i]
                    if cur.shape == best.shape:
                        cur.mul_(0.8).add_(0.2 * best)
            self.event_log.append({
                "type": "ratchet_restore",
                "step": self.step_count,
                "phi": phi,
                "phi_per_cell": phi_per_cell,
            })

    # ─── Adaptive split-threshold (Law 86 fix) ──────────────────────

    def _update_adaptive_threshold(self):
        """Update split-threshold(s).

        all-fix A2 (§28 ship rec): per-cell threshold is the new primary path. Each
        cell uses its own tension_history window. Champion cells can no longer
        raise a global wall against quiet cells (the §28 H1+H3 mechanism).
        """
        # Legacy global update (kept for back-compat / smoke diagnostics)
        if len(self._global_tension_history) >= 10:
            recent = self._global_tension_history[-self.cfg.adaptive_window:]
            mean_t = sum(recent) / len(recent)
            var_t = sum((t - mean_t) ** 2 for t in recent) / len(recent)
            std_t = math.sqrt(var_t) if var_t > 0 else mean_t * 0.1
            self.split_threshold = max(mean_t + 1.5 * std_t, mean_t * 0.5)

        # all-fix A2: per-cell threshold
        if not self.cfg.per_cell_threshold_enabled:
            return
        while len(self._per_cell_thresholds) < self.n_cells:
            self._per_cell_thresholds.append(self.split_threshold)
        while len(self._per_cell_thresholds) > self.n_cells:
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

    # ─── Split / merge gates (patience-driven) ──────────────────────

    def _dispersion_split_candidates(self) -> List[int]:
        """all-fix A1 (§28 ship rec): substrate-independent dispersion trigger.

        Compute pairwise L2 distances of cell_state buffers (per-cell signature),
        nominate top-quartile cells whose mean-distance exceeds (overall_mean +
        sigma_mult × σ). Independent of attention projection geometry, so it can
        fire even when h_to_c collapses onto 1-2 champion cells (§28 H1+H3).

        Honest C3: warmup gate (adaptive_window // 2) prevents cold-start firefoss.
        """
        if not self.cfg.dispersion_trigger_enabled:
            return []
        N = self.n_cells
        if N < 4:
            return []
        if len(self._global_tension_history) < max(self.cfg.adaptive_window // 2, 10):
            return []
        with torch.no_grad():
            states = torch.stack([c.cell_state for c in self.cells])  # (N, D)
            diff = states.unsqueeze(0) - states.unsqueeze(1)
            d2 = (diff * diff).mean(dim=-1)
            mean_dist = d2.sum(dim=-1) / max(N - 1, 1)
            overall_mean = float(mean_dist.mean().item())
            overall_sd = float(mean_dist.std().item()) if N > 1 else 0.0
            sigma_gate = overall_mean + self.cfg.per_cell_sigma_mult * overall_sd
            k = max(1, int(self.cfg.dispersion_top_quartile * N))
            top_vals, top_idx = torch.topk(mean_dist, k=min(k, N), largest=True)
            top = [
                int(i.item())
                for v, i in zip(top_vals, top_idx)
                if float(v.item()) > sigma_gate
            ]
        return [i for i in top if self.cells[i].process_count >= self.cfg.split_patience]

    def _check_splits(self) -> List[Dict]:
        events: List[Dict] = []
        if self.n_cells >= self.cfg.max_cells:
            return events
        # tension-based candidates (per-cell threshold if A2 enabled)
        tension_candidates: List[int] = []
        for i, cell in enumerate(self.cells):
            if len(cell.tension_history) < self.cfg.split_patience:
                continue
            recent = cell.tension_history[-self.cfg.split_patience:]
            if self.cfg.per_cell_threshold_enabled and i < len(self._per_cell_thresholds):
                thr = self._per_cell_thresholds[i]
            else:
                thr = self.split_threshold
            if all(t > thr for t in recent):
                tension_candidates.append(i)
        # A1 dispersion candidates (OR'd with tension)
        dispersion_candidates = self._dispersion_split_candidates()
        seen = set(tension_candidates)
        candidates: List[int] = list(tension_candidates)
        for i in dispersion_candidates:
            if i not in seen:
                candidates.append(i)
                seen.add(i)
        for idx in candidates:
            if self.n_cells >= self.cfg.max_cells:
                break
            if idx >= self.n_cells:
                continue
            ev = self._split_cell(idx)
            if ev:
                ev["trigger"] = (
                    "tension+dispersion" if idx in tension_candidates and idx in dispersion_candidates
                    else ("tension" if idx in tension_candidates else "dispersion")
                )
                events.append(ev)
        return events

    def _check_merges(self) -> List[Dict]:
        events: List[Dict] = []
        if self.n_cells <= self.cfg.min_cells:
            return events
        pairs: List[Tuple[int, int]] = []
        for key, hist in self._inter_repulsion_history.items():
            if len(hist) < self.cfg.merge_patience:
                continue
            recent = hist[-self.cfg.merge_patience:]
            if all(r < self.cfg.merge_threshold for r in recent):
                pairs.append(key)
        for (i, j) in pairs:
            if self.n_cells <= self.cfg.min_cells:
                break
            if i < self.n_cells and j < self.n_cells:
                ev = self._merge_cells(i, j)
                if ev:
                    events.append(ev)
        return events

    # ─── all-fix C1: optimizer rebuild callback (R2 STUB) ──────────

    def register_optimizer_rebuild_callback(self, callback) -> None:
        """all-fix C1 (R2 risk STUB): caller registers `callback(event_dict, engine)`
        invoked after every split/merge so AdamW / Net2Net momentum copy can rebuild
        optimizer state for the new (or removed) cell.

        STUB: actual Net2Net momentum copy is NOT performed inside this engine; the
        callback is the integration point for cond.5 H100 fire prep (see §25 R2).

        Signature:
            callback(event: Dict, engine: MitosisModelEngine) -> None
        """
        self._optimizer_rebuild_callbacks.append(callback)

    def _notify_optimizer_rebuild(self, event: Dict) -> None:
        for cb in self._optimizer_rebuild_callbacks:
            try:
                cb(event, self)
            except Exception as e:
                self.event_log.append({
                    "type": "optimizer_rebuild_callback_error",
                    "step": self.step_count,
                    "error": f"{type(e).__name__}: {e}",
                })

    # ─── Public test hooks ──────────────────────────────────────────

    def force_split(self, parent_idx: int = 0) -> Optional[Dict]:
        return self._split_cell(parent_idx)

    def force_merge(self, idx_a: int = 0, idx_b: int = 1) -> Optional[Dict]:
        return self._merge_cells(idx_a, idx_b)


# ─── DESIGN BLOCKERS / KNOWN LIMITS (raw#10 honest, mirrors spec §11) ───
# 1. Optimizer state migration STUB — caller must rebuild optimizer after _split_cell.
# 2. Attention sharing fallback (N>8) is irreversible in current pool — auto-promote
#    only happens once. Future cycle: dynamic promote/demote.
# 3. Lorenz cell_state buffer is residual-additive at cell input; NOT a true GRU hidden
#    mirror. Effect on tension diversity preserved, persistence is weaker than v2.
# 4. IIT Φ uses cell_state signatures (input-independent). Hybrid (i+iii) signature
#    (hidden mean + weight signature) is a future improvement (spec §5.1 (iv)).
# 5. merge_threshold v2 default likely mismatched at d_model=384 — calibrate in cond.3.
# 6. Per-param noise scaling is capped at 0.5 × p.std() to prevent LN-bias drift.
# 7. lm_head weight-tied with tok_emb (norm); can be untied via cfg.weight_tied_lm_head.
