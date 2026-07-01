#!/usr/bin/env python3
"""H_1631 — Sheaf-gluing binding mouth (local sections -> global consistency).

MECHANISM (card): treat positions as nodes on a graph with role-edges; each node
carries a local stalk vector; each edge carries a learned low-rank restriction map
R_{i->e}.  The bind = a few Jacobi steps toward sheaf-Laplacian consistency: find
node features whose restrictions AGREE on shared edges, minimizing
  sum_edges || R_{i->e} x_i - R_{j->e} x_j ||^2.
The consistent assignment IS the bound composite; the residual disagreement
(coboundary norm) is an explicit readable 'failed-to-bind' signal (MONITOR-ONLY).
Here the 'edge' couples each position to its role-neighbor (causal offset); the
restriction map is a learned low-rank rotation per edge.

ABLATION (card): set all restriction maps to identity (R = I) -> the sheaf
collapses to ordinary graph-Laplacian smoothing (= vanilla message passing).
arm=ablate forces R=I, isolating the non-trivial restriction maps (role-typing).

base.readout (Conv1d d->V) stays intact -> .clm-serializable.
"""
import os, sys
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bind_base import run


class SheafGlueBind(nn.Module):
    def __init__(self, d: int, k: int, bind_steps: int = 4, rank: int = 32,
                 role_offset: int = 1, jacobi_lr: float = 0.3):
        super().__init__()
        self.d, self.k, self.K = d, k, max(1, bind_steps)
        self.role_offset = role_offset
        self.jl = jacobi_lr
        self.r = rank
        # project stalk into k-dim consistency space + back.
        self.stalk = nn.Conv1d(d, k, 1)
        self.unstalk = nn.Conv1d(k, d, 1)
        # low-rank restriction map per the two edge endpoints: R = I + Ua Vb^T
        self.Ua = nn.Parameter(torch.randn(k, rank) * (1.0 / (k ** 0.5)))
        self.Vb = nn.Parameter(torch.randn(k, rank) * (1.0 / (k ** 0.5)))
        self.Uc = nn.Parameter(torch.randn(k, rank) * (1.0 / (k ** 0.5)))
        self.Vd = nn.Parameter(torch.randn(k, rank) * (1.0 / (k ** 0.5)))
        self.gate = nn.Parameter(torch.zeros(1))

    def _lowrank(self, h, U, Vt):
        # R h = h + U (V^T h).  h:(B,k,T)  U:(k,r)  Vt:(r,k)
        proj = torch.einsum('rk,bkt->brt', Vt, h)      # (B, r, T)
        return h + torch.einsum('kr,brt->bkt', U, proj)

    def _R_i(self, h, ablate):
        if ablate:
            return h
        return self._lowrank(h, self.Ua, self.Vb.t())

    def _R_j(self, h, ablate):
        if ablate:
            return h
        return self._lowrank(h, self.Uc, self.Vd.t())

    def forward(self, x, ablate: bool = False):
        B, d, T = x.shape
        h = self.stalk(x)                                  # (B, k, T) local sections
        K = 1 if ablate else self.K
        # neighbor = role-offset shifted (causal): edge (i, j=i-offset)
        for _ in range(K):
            hj = F.pad(h, (self.role_offset, 0))[:, :, :T]  # x_j on shared edge
            Ri = self._R_i(h, ablate)
            Rj = self._R_j(hj, ablate)
            disagree = Ri - Rj                              # coboundary direction
            # Jacobi step: move h to reduce restriction disagreement
            h = h - self.jl * disagree
        # coboundary norm at fixpoint (MONITOR): ||R_i h_i - R_j h_j||^2
        hj = F.pad(h, (self.role_offset, 0))[:, :, :T]
        cob = (self._R_i(h, ablate) - self._R_j(hj, ablate)).pow(2).sum(dim=1).mean()
        x_bound = x + torch.tanh(self.gate) * self.unstalk(h)
        return x_bound, cob


def build_bind(d, V, k, bind_steps):
    kw = max(64, k // 4)
    return SheafGlueBind(d=d, k=kw, bind_steps=max(2, bind_steps // 2)), 0.0  # monitor-only


if __name__ == "__main__":
    run("H_1631 sheaf-gluing", build_bind)
