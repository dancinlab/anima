#!/usr/bin/env python3
"""H_1630 — Tropical (max-plus) semiring binding mouth.

MECHANISM (card): replace the (+,x) ring with the tropical (max,+) semiring.
Per position form a role x filler score S[r,f] = role_proj + filler_proj, and the
bound rep per role is the tropical matvec b[r] = max_f (S[r,f] + value[f]) — an
argmax that routes exactly ONE filler to each role (Viterbi-style, idempotent, no
superposition crosstalk).  Temperature-annealable: softmax-weighted at T=1, hard
max as T->0.  Here roles/fillers are R/Ft latent slots projected from the
penultimate stream; the bound role vectors are scattered back residually into the
d-stream before the PRODUCTION readout.

ABLATION (card): a single continuous knob T.  arm=ablate sets T=1 (log-sum-exp /
softmax = ordinary attention pooling).  bind anneals T toward 0 (hard max-plus).
If the lift vanishes as T->1, max-plus selectivity is load-bearing.

base.readout (Conv1d d->V) stays intact -> .clm-serializable.
"""
import os, sys
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bind_base import run


class TropicalBind(nn.Module):
    def __init__(self, d: int, k: int, n_roles: int = 8, n_fillers: int = 16,
                 t_hard: float = 0.1):
        super().__init__()
        self.d, self.k = d, k
        self.R, self.Fn = n_roles, n_fillers
        self.t_hard = t_hard
        # project penultimate -> role scores (R), filler scores (Fn), filler values
        self.role_proj = nn.Conv1d(d, n_roles, 1)
        self.fill_proj = nn.Conv1d(d, n_fillers, 1)
        self.val_proj = nn.Conv1d(d, n_fillers * k, 1)   # value[f] in R^k per pos
        self.Wout = nn.Conv1d(n_roles * k, d, 1)          # bound roles -> d-stream
        self.gate = nn.Parameter(torch.zeros(1))

    def forward(self, x, ablate: bool = False):
        B, d, T = x.shape
        rs = self.role_proj(x)                            # (B, R, T)
        fs = self.fill_proj(x)                            # (B, Fn, T)
        vals = self.val_proj(x).view(B, self.Fn, self.k, T)   # (B, Fn, k, T)
        # score S[r,f] = role[r] + filler[f]  -> (B, R, Fn, T)
        S = rs.unsqueeze(2) + fs.unsqueeze(1)
        # tropical contraction: b[r] = max_f (S[r,f] + value[f])
        # combine S with each value channel: (B,R,Fn,k,T)
        comb = S.unsqueeze(3) + vals.unsqueeze(1)         # (B, R, Fn, k, T)
        T_temp = 1.0 if ablate else self.t_hard
        # softmax over filler axis at temperature T (T->0 = hard max-plus)
        w = torch.softmax(comb / T_temp, dim=2)           # (B, R, Fn, k, T)
        b = (w * comb).sum(dim=2)                         # (B, R, k, T) tropical matvec
        # crosstalk monitor: entropy of the assignment (low = selective bind)
        ent = -(w.clamp_min(1e-9) * w.clamp_min(1e-9).log()).sum(dim=2).mean()
        bound = b.reshape(B, self.R * self.k, T)
        x_bound = x + torch.tanh(self.gate) * self.Wout(bound)
        return x_bound, ent                               # aux = assignment entropy


def build_bind(d, V, k, bind_steps):
    # k here = per-filler value width; keep modest so param budget ~ production.
    kw = max(8, k // 8)
    return TropicalBind(d=d, k=kw), 0.0                   # aux MONITOR-only (no loss add)


if __name__ == "__main__":
    run("H_1630 tropical max-plus", build_bind)
