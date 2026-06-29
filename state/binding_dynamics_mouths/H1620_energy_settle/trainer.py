#!/usr/bin/env python3
"""H_1620 — Energy-settle attractor mouth (Hopfield / predictive-coding relaxation).

MECHANISM (card): the penultimate representation is NOT read out feedforward; it
is the attractor z* of a K-step gradient relaxation on a scalar energy
  E(z; a) = 1/2 z^T W z - z^T (U_a a)
with SYMMETRIC W (modern-Hopfield / free-energy).  leg_a = the trunk penultimate
state (clamp / boundary condition); a SECOND leg is the trunk state shifted by one
role-offset (leg_b) so the settled minimum is a JOINT basin deep only when both
clamps are consistent.  z does dz/dt = -dE/dz for K steps from a 2-leg init; the
attractor z* is residually written back into the d-stream before the PRODUCTION
readout.  aux = the residual energy at z* (MONITOR-ONLY): a 'failed-to-settle'
signal driven toward 0.

ABLATION (card): K=1 -> the operator collapses to ONE feedforward layer (= conv/
attn baseline).  arm=ablate forces K_eff=1, isolating the settling dynamics.

The binding op writes a RESIDUAL d->d transform, so base.readout (Conv1d d->V)
stays intact -> .clm-serializable (the binding shapes the trunk objective).
"""
import os, sys
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bind_base import run


class EnergySettleBind(nn.Module):
    """K-step symmetric-energy relaxation on a k-dim hidden, 2-leg clamp init."""

    def __init__(self, d: int, k: int, bind_steps: int = 8, dt: float = 0.3,
                 role_offset: int = 1):
        super().__init__()
        self.d, self.k, self.K, self.dt = d, k, max(1, bind_steps), dt
        self.role_offset = role_offset
        # symmetric coupling W = M + M^T (built from a free param M); clamp maps.
        self.M = nn.Parameter(torch.randn(k, k) * (1.0 / (k ** 0.5)))
        self.Ua = nn.Conv1d(d, k, 1)        # leg_a clamp (penultimate)
        self.Ub = nn.Conv1d(d, k, 1)        # leg_b clamp (role-shifted)
        self.Wout = nn.Conv1d(k, d, 1)      # attractor -> residual d-stream
        self.gate = nn.Parameter(torch.zeros(1))   # residual gate (init 0 = identity-safe)

    def _Wsym(self):
        return 0.5 * (self.M + self.M.t())

    def forward(self, x, ablate: bool = False):
        # x: (B, d, T).  leg_a = x ; leg_b = role-shifted x (causal, pad left).
        B, d, T = x.shape
        a = self.Ua(x)                                  # (B, k, T)
        xb = F.pad(x, (self.role_offset, 0))[:, :, :T]  # shift-right by role_offset
        b = self.Ub(xb)                                 # (B, k, T)
        Wsym = self._Wsym()                             # (k, k)
        K = 1 if ablate else self.K
        # PSD-ify the coupling so the relaxation is contractive (modern-Hopfield /
        # predictive-coding free-energy is a DESCENT — an indefinite W diverges).
        # Wpsd = Wsym^T Wsym / k (>=0); gradient step z <- z - dt*(Wpsd z - drive)
        # then per-step normalize z so the fixed point is bounded (no blow-up).
        Wpsd = (Wsym @ Wsym) / self.k
        drive = a + b                                   # (B, k, T) joint-basin seed
        z = drive
        for _ in range(K):
            Wz = torch.einsum('ij,bjt->bit', Wpsd, z)   # (B, k, T)
            z = z - self.dt * (Wz - drive)
            z = z / (z.norm(dim=1, keepdim=True) / (self.k ** 0.5) + 1e-6)  # stabilize
        # residual energy at z* (MONITOR, normalized): E = 1/2 z^T Wpsd z - z^T drive
        Wz = torch.einsum('ij,bjt->bit', Wpsd, z)
        e = (0.5 * (z * Wz).sum(dim=1) - (z * drive).sum(dim=1)) / self.k
        aux = e.mean().clamp(-1e3, 1e3)                 # bounded monitor scalar
        # residual write-back into d-stream (gate init 0 -> starts as pure trunk)
        x_bound = x + torch.tanh(self.gate) * self.Wout(z)
        return x_bound, aux


def build_bind(d, V, k, bind_steps):
    # aux MONITOR-only (0.0): the settle DYNAMICS shapes the trunk via the residual
    # write-back; the energy aux is a readable 'failed-to-settle' signal, not a loss.
    return EnergySettleBind(d=d, k=k, bind_steps=bind_steps), 0.0


if __name__ == "__main__":
    run("H_1620 energy-settle attractor", build_bind)
