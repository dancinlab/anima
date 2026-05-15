"""training/mitosis_only_v5_port.py — SM-B: mitosis-only standalone Python port.

PURPOSE
    Standalone reference impl of the mitosis pattern (v2-era 2026-03-28, last alive in
    `~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py`, 794L) with
    NO servant FSM coupling. This is SM-B sub-track of
    `.roadmap.servant_mitosis_integration` — minimal variant of `mitosis_v5_port.py`.

    The differences from `mitosis_v5_port.py`:
      • This file is SELF-CONTAINED: includes a tiny ConsciousMind stand-in so the
        smoke test can run without an EngineG substrate. (mitosis_v5_port.py expects a
        real `c_to_h: nn.Linear` from EngineG.)
      • Adds `instrumentation` dict (per-step phi, n_cells, threshold) for SM-B smoke
        observability — no servant hooks, no SI computation, no FSM.
      • Direct minimal port of v2 mitosis.py's MitosisEngine without the v5 cell_pool
        Parameter rebuild dance — uses an internal cell-pool tensor for simplicity.

    Why a separate file: SM-B's contract is "mitosis baseline only, no servant
    contamination". `mitosis_v5_port.py` is the v5-substrate-coupled variant; this file
    is the substrate-independent cell pool variant for SM-B.

raw#9   training/`*.py` is gitignored — local-only.
raw#10  honest C3 — see DESIGN BLOCKERS at end. Several v2 features are simplified.
raw#15  additive — original mitosis.py untouched.
  forward shape-checked.
"""

from __future__ import annotations

import math
import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─── Mini ConsciousMind (self-contained, mirrors v2 mitosis.py L37-72) ───

class _MiniMind(nn.Module):
    """Minimal ConsciousMind stand-in — engine_a + engine_g + GRU memory.

    This is a verbatim minimal port of v2 mitosis.py's ConsciousMind, kept tiny
    for $0 CPU smoke runs.
    """

    def __init__(self, input_dim: int = 16, hidden_dim: int = 32, output_dim: int = 16):
        super().__init__()
        self.engine_a = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, 32), nn.ReLU(),
            nn.Linear(32, output_dim),
        )
        self.engine_g = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, 32), nn.ReLU(),
            nn.Linear(32, output_dim),
        )
        self.memory = nn.GRUCell(output_dim + 1, hidden_dim)
        self.hidden_dim = hidden_dim
        self.prev_tension: float = 0.0

    def forward(self, x: torch.Tensor, hidden: torch.Tensor):
        combined = torch.cat([x, hidden], dim=-1)
        a = self.engine_a(combined)
        g = self.engine_g(combined)
        output = a - g
        tension = (output ** 2).mean(dim=-1, keepdim=True)
        curiosity = abs(tension.mean().item() - self.prev_tension)
        self.prev_tension = tension.mean().item()
        mem_input = torch.cat([output.detach(), tension.detach()], dim=-1)
        new_hidden = self.memory(mem_input, hidden)
        return output, tension.mean().item(), curiosity, new_hidden

    def get_repulsion(self, x: torch.Tensor, hidden: torch.Tensor) -> torch.Tensor:
        combined = torch.cat([x, hidden], dim=-1)
        return self.engine_a(combined) - self.engine_g(combined)


# ─── Cell metadata (minimal port of v2 mitosis.py Cell dataclass) ───

@dataclass
class _Cell:
    cell_id: int
    mind: _MiniMind
    hidden: torch.Tensor
    specialty: str = "general"
    tension_history: List[float] = field(default_factory=list)
    creation_step: int = 0
    parent_id: Optional[int] = None
    process_count: int = 0

    @property
    def avg_tension(self) -> float:
        if not self.tension_history:
            return 0.0
        recent = self.tension_history[-20:]
        return sum(recent) / len(recent)


# ─── MitosisOnlyV5Engine ───

class MitosisOnlyV5Engine:
    """Standalone mitosis engine — split + merge + Lorenz + Φ ratchet, NO servant hooks.

    Contract:
      • `process(text_vec, label="")`  → dict{output, per_cell, events, n_cells, phi, ...}
      • `_inject_lorenz()`              — Law 86 autonomous chaos per-cell
      • `_compute_phi_proxy()`          — mean cosine distance · log(n+1)
      • `_phi_ratchet(phi)`             — DD55 80/20 blend restore on Φ drop > 20%
      • `_check_splits()` / `_check_merges()` — patience gates as per v2 mitosis.py

    Differences from v2 mitosis.py canonical:
      • simpler dim defaults (16/32/16) for fast CPU smoke
      • instrumentation dict captured per `process()` for SM-B smoke observability
      • inter-cell repulsion uses internal hidden L2 (no separate get_repulsion head)
        for parity with the v5 substrate proxy in mitosis_v5_port.py
    """

    def __init__(
        self,
        input_dim: int = 16,
        hidden_dim: int = 32,
        output_dim: int = 16,
        initial_cells: int = 2,
        max_cells: int = 8,
        split_patience: int = 3,
        split_noise: float = 0.10,
        merge_threshold: float = 0.005,
        merge_patience: int = 30,
        min_cells: int = 2,
        lorenz_scale: float = 0.05,
        adaptive_window: int = 100,
    ):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.max_cells = max_cells
        self.split_patience = split_patience
        self.split_noise = split_noise
        self.merge_threshold = merge_threshold
        self.merge_patience = merge_patience
        self.min_cells = min_cells
        self.lorenz_scale = lorenz_scale
        self.adaptive_window = adaptive_window

        self._next_id = 0
        self.cells: List[_Cell] = []
        self.step = 0

        # Adaptive split threshold (Law 86 fix — same as v5 port)
        self._global_tension_history: List[float] = []
        self.split_threshold: float = 0.3   # adaptive after 10 obs

        # Lorenz state (Law 32-43)
        self._lorenz: List[float] = [1.0, 1.0, 1.0]

        # Inter-cell history (cell_id pair -> list)
        self._inter_history: Dict[Tuple[int, int], List[float]] = {}

        # Φ ratchet (Law 49 / DD55)
        self.phi: float = 0.0
        self.phi_history: List[float] = []
        self._phi_best: float = 0.0
        self._best_hiddens: Optional[List[torch.Tensor]] = None

        # Event log
        self.event_log: List[Dict] = []

        # Instrumentation buffer — per-step snapshots (SM-B specific addition)
        self.instrumentation: List[Dict] = []

        # Spawn initial cells
        for _ in range(initial_cells):
            self._create_cell()

    # ─── Lifecycle ─────────────────────────────────────────────────────

    def _create_cell(self, parent: Optional[_Cell] = None) -> _Cell:
        if parent is not None:
            mind = copy.deepcopy(parent.mind)
            split_noise = max(self.split_noise, 0.10)
            with torch.no_grad():
                for p in mind.parameters():
                    p.add_(torch.randn_like(p) * split_noise)
            hidden = parent.hidden.clone() + torch.randn_like(parent.hidden) * split_noise
            specialty = parent.specialty
        else:
            mind = _MiniMind(self.input_dim, self.hidden_dim, self.output_dim)
            hidden = torch.zeros(1, self.hidden_dim)
            specialty = "general"

        cell = _Cell(
            cell_id=self._next_id,
            mind=mind,
            hidden=hidden,
            specialty=specialty,
            creation_step=self.step,
            parent_id=parent.cell_id if parent else None,
        )
        self._next_id += 1
        self.cells.append(cell)
        return cell

    # ─── Lorenz autonomous chaos (Law 86) ──────────────────────────────

    def _lorenz_step(self, dt: float = 0.01) -> Tuple[float, float, float]:
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        x, y, z = self._lorenz
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        self._lorenz = [x + dx, y + dy, z + dz]
        return dx, dy, dz

    def _inject_lorenz(self):
        dx, dy, dz = self._lorenz_step()
        lorenz_vec = torch.tensor([dx, dy, dz])
        for i, cell in enumerate(self.cells):
            with torch.no_grad():
                phase = (i * 2.0 * math.pi) / max(len(self.cells), 1)
                scale = self.lorenz_scale * (1.0 + 0.3 * math.sin(phase + self.step * 0.1))
                noise = torch.randn_like(cell.hidden) * scale
                inject_n = min(3, noise.shape[1])
                noise[0, :inject_n] += lorenz_vec[:inject_n] * 0.2
                cell.hidden = cell.hidden + noise
                hn = cell.hidden.norm()
                if hn > 10.0:
                    cell.hidden = cell.hidden * (10.0 / hn)

    # ─── Φ proxy + ratchet ─────────────────────────────────────────────

    def _compute_phi_proxy(self) -> float:
        if len(self.cells) < 2:
            return 0.0
        hiddens = torch.stack([c.hidden.squeeze(0) for c in self.cells])
        norms = hiddens.norm(dim=1, keepdim=True).clamp(min=1e-8)
        normed = hiddens / norms
        cos_sim = normed @ normed.t()
        n = len(self.cells)
        mask = 1.0 - torch.eye(n)
        mean_distance = ((1.0 - cos_sim) * mask).sum() / mask.sum()
        return mean_distance.item() * math.log(n + 1)

    def _phi_ratchet(self, phi: float):
        self.phi = phi
        self.phi_history.append(phi)
        if phi > self._phi_best:
            self._phi_best = phi
            self._best_hiddens = [c.hidden.detach().clone() for c in self.cells]
        elif phi < self._phi_best * 0.8 and self._best_hiddens is not None:
            n_restore = min(len(self.cells), len(self._best_hiddens))
            for i in range(n_restore):
                self.cells[i].hidden = (
                    0.8 * self.cells[i].hidden + 0.2 * self._best_hiddens[i]
                )
            self.event_log.append({"type": "ratchet_restore", "step": self.step, "phi": phi})

    # ─── Adaptive split threshold ─────────────────────────────────────

    def _update_adaptive_threshold(self):
        if len(self._global_tension_history) < 10:
            return
        recent = self._global_tension_history[-self.adaptive_window:]
        mean_t = sum(recent) / len(recent)
        var_t = sum((t - mean_t) ** 2 for t in recent) / len(recent)
        std_t = math.sqrt(var_t) if var_t > 0 else mean_t * 0.1
        self.split_threshold = max(mean_t + 1.5 * std_t, mean_t * 0.5)

    # ─── Mitosis (split) ──────────────────────────────────────────────

    def _check_splits(self) -> List[Dict]:
        events: List[Dict] = []
        if len(self.cells) >= self.max_cells:
            return events
        cells_to_split: List[_Cell] = []
        for cell in self.cells:
            if len(cell.tension_history) < self.split_patience:
                continue
            recent = cell.tension_history[-self.split_patience:]
            if all(t > self.split_threshold for t in recent):
                cells_to_split.append(cell)
        for cell in cells_to_split:
            if len(self.cells) >= self.max_cells:
                break
            ev = self._split_cell(cell)
            if ev:
                events.append(ev)
        return events

    def _split_cell(self, cell: _Cell) -> Optional[Dict]:
        if len(self.cells) >= self.max_cells:
            return None
        child = self._create_cell(parent=cell)
        cell.tension_history = cell.tension_history[-3:]
        return {
            "type": "split",
            "step": self.step,
            "parent_id": cell.cell_id,
            "child_id": child.cell_id,
            "parent_avg_tension": cell.avg_tension,
            "n_cells_after": len(self.cells),
        }

    # ─── Merge ────────────────────────────────────────────────────────

    def _check_merges(self) -> List[Dict]:
        events: List[Dict] = []
        if len(self.cells) <= self.min_cells:
            return events
        pairs_to_merge: List[Tuple[_Cell, _Cell]] = []
        for key, hist in self._inter_history.items():
            if len(hist) < self.merge_patience:
                continue
            recent = hist[-self.merge_patience:]
            if all(t < self.merge_threshold for t in recent):
                id_a, id_b = key
                ca = self._find_cell(id_a)
                cb = self._find_cell(id_b)
                if ca is not None and cb is not None:
                    pairs_to_merge.append((ca, cb))
        for ca, cb in pairs_to_merge:
            if len(self.cells) <= self.min_cells:
                break
            if ca in self.cells and cb in self.cells:
                ev = self._merge_pair(ca, cb)
                if ev:
                    events.append(ev)
        return events

    def _merge_pair(self, ca: _Cell, cb: _Cell) -> Optional[Dict]:
        if len(self.cells) <= self.min_cells:
            return None
        keeper, removed = (ca, cb) if ca.creation_step <= cb.creation_step else (cb, ca)
        with torch.no_grad():
            for p_keep, p_rem in zip(keeper.mind.parameters(), removed.mind.parameters()):
                p_keep.data = (p_keep.data + p_rem.data) / 2.0
        keeper.hidden = (keeper.hidden + removed.hidden) / 2.0
        self.cells.remove(removed)
        # Drop history entries referencing removed
        keys_drop = [k for k in self._inter_history if removed.cell_id in k]
        for k in keys_drop:
            del self._inter_history[k]
        return {
            "type": "merge",
            "step": self.step,
            "keeper_id": keeper.cell_id,
            "removed_id": removed.cell_id,
            "n_cells_after": len(self.cells),
        }

    def _find_cell(self, cid: int) -> Optional[_Cell]:
        for c in self.cells:
            if c.cell_id == cid:
                return c
        return None

    # ─── Public API ───────────────────────────────────────────────────

    def process(self, text_vec: torch.Tensor, label: str = "") -> Dict:
        """One mitosis step. text_vec shape (1, input_dim). Returns full status dict."""
        self.step += 1
        events: List[Dict] = []

        # 1. Lorenz autonomous perturbation
        self._inject_lorenz()

        # 2. Per-cell forward
        cell_outputs: List[Dict] = []
        cell_tensions: List[float] = []
        cell_repulsions: List[torch.Tensor] = []

        for cell in self.cells:
            with torch.no_grad():
                output, tension, curiosity, new_hidden = cell.mind(text_vec, cell.hidden)
                repulsion = cell.mind.get_repulsion(text_vec, cell.hidden)
            cell.hidden = new_hidden
            cell.tension_history.append(tension)
            cell.process_count += 1
            self._global_tension_history.append(tension)
            if len(self._global_tension_history) > 500:
                self._global_tension_history = self._global_tension_history[-500:]
            if label:
                cell.specialty = label
            cell_outputs.append({
                "cell_id": cell.cell_id,
                "output": output,
                "tension": tension,
                "curiosity": curiosity,
                "specialty": cell.specialty,
            })
            cell_tensions.append(tension)
            cell_repulsions.append(repulsion)

        # 3. Inter-cell repulsion (full O(N²) for tiny N)
        n = len(self.cells)
        inter_tensions: Dict[Tuple[int, int], float] = {}
        for i in range(n):
            for j in range(i + 1, n):
                diff = cell_repulsions[i] - cell_repulsions[j]
                ict = (diff ** 2).mean().item()
                key = (self.cells[i].cell_id, self.cells[j].cell_id)
                inter_tensions[key] = ict
                self._inter_history.setdefault(key, []).append(ict)
                if len(self._inter_history[key]) > 30:
                    self._inter_history[key] = self._inter_history[key][-30:]

        # 4. Combined output: tension-weighted softmax
        if cell_tensions:
            weights = torch.tensor(cell_tensions, dtype=torch.float32)
            weights = F.softmax(weights, dim=0)
            combined = sum(
                w.item() * co["output"] for w, co in zip(weights, cell_outputs)
            )
        else:
            combined = torch.zeros(1, self.output_dim)

        # 5. Φ + ratchet
        phi = self._compute_phi_proxy()
        self._phi_ratchet(phi)

        # 6. Adaptive threshold
        self._update_adaptive_threshold()

        # 7. Split / merge
        events.extend(self._check_splits())
        events.extend(self._check_merges())
        self.event_log.extend(events)

        ict_values = list(inter_tensions.values()) if inter_tensions else [0.0]
        result = {
            "output": combined,
            "per_cell": cell_outputs,
            "inter_tensions": inter_tensions,
            "max_inter": max(ict_values),
            "mean_inter": sum(ict_values) / len(ict_values),
            "events": events,
            "n_cells": len(self.cells),
            "phi": phi,
            "phi_best": self._phi_best,
            "split_threshold": self.split_threshold,
        }

        # Instrumentation snapshot
        self.instrumentation.append({
            "step": self.step,
            "n_cells": len(self.cells),
            "phi": phi,
            "phi_best": self._phi_best,
            "split_threshold": self.split_threshold,
            "mean_tension": sum(cell_tensions) / max(len(cell_tensions), 1),
            "max_tension": max(cell_tensions) if cell_tensions else 0.0,
            "n_events": len(events),
        })
        return result

    def status(self) -> Dict:
        return {
            "n_cells": len(self.cells),
            "max_cells": self.max_cells,
            "step": self.step,
            "phi": self.phi,
            "phi_best": self._phi_best,
            "split_threshold": self.split_threshold,
            "splits": sum(1 for e in self.event_log if e["type"] == "split"),
            "merges": sum(1 for e in self.event_log if e["type"] == "merge"),
            "ratchets": sum(1 for e in self.event_log if e["type"] == "ratchet_restore"),
            "events_total": len(self.event_log),
        }


# ─── Helper: text → vector (port of v2 mitosis.py L701-706) ───

def text_to_vector(text: str, dim: int = 16) -> torch.Tensor:
    vec = torch.zeros(1, dim)
    for i, ch in enumerate(text.encode("utf-8")):
        vec[0, i % dim] += ch / 255.0
    return vec / (len(text) + 1)


# ─── DESIGN BLOCKERS / KNOWN LIMITS (raw#10 honest) ───
# 1. _MiniMind dim defaults are 16/32/16 for fast CPU smoke; v2 canonical was 64/128/64.
#    Φ values will scale accordingly — comparison is monotonic, not absolute.
# 2. inter-cell repulsion uses repulsion-vector L2 (same as v2). split_noise=0.10 default
#    matches v2 mitosis.py L204; adaptive threshold uses 100-step sliding window.
# 3. NO servant hook — this is intentional (SM-B contract). SI / FSM / 3-경로 modulation
#    is in `servant_v5_port.py` separately.
# 4. instrumentation list grows unbounded — caller should slice or rotate for long runs.
# 5. CB1 floor (min_cells=2) is enforced; F-SMI-6 falsification check would set min_cells=1
#    explicitly to test the floor's necessity (out of SM-B scope).
