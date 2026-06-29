#!/usr/bin/env python3
"""H_1632 — Galois-closure concept-lattice binding mouth (FCA meet/join).

MECHANISM (card): Formal Concept Analysis.  One leg projects to an object/extent
indicator set, the other to an attribute/intent indicator set (sparse sigmoid
gates).  The bind = Galois closure: intent = attributes shared by ALL gated
objects (soft AND-pool over objects), extent = objects having ALL gated
attributes (soft AND-pool over attributes); iterate the two derivation operators
to a fixpoint = a formal concept (closed extent,intent).  Composition = lattice
meet (intersection of intents), idempotent.  The closed concept indicators are
scattered back residually into the d-stream before the PRODUCTION readout.

ABLATION (card): replace the AND-pool (min / log-product of gates) with the
OR-pool (sum / softmax) used by attention.  arm=ablate uses OR-pool, isolating the
meet (conjunction) as load-bearing.

soft AND over a set = product of gates = exp(sum log g); soft OR = 1 - prod(1-g).
base.readout (Conv1d d->V) stays intact -> .clm-serializable.
"""
import os, sys
import torch
import torch.nn as nn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bind_base import run


class GaloisLatticeBind(nn.Module):
    def __init__(self, d: int, k: int, n_obj: int = 32, n_attr: int = 32,
                 bind_steps: int = 2):
        super().__init__()
        self.d, self.k = d, k
        self.no, self.na = n_obj, n_attr
        self.K = max(1, bind_steps)
        self.obj_gate = nn.Conv1d(d, n_obj, 1)             # extent indicator logits
        self.attr_gate = nn.Conv1d(d, n_attr, 1)           # intent indicator logits
        # formal context (object x attribute incidence), learned.
        self.context = nn.Parameter(torch.randn(n_obj, n_attr) * 0.1)
        self.Wout = nn.Conv1d(n_obj + n_attr, d, 1)        # closed concept -> d
        self.gate = nn.Parameter(torch.zeros(1))

    @staticmethod
    def _and_pool(weights, gates_logits, ablate):
        # weights: (B, S, T) soft membership; gates_logits incidence per (S, S2).
        # soft AND over the gated S set of the incidence column for each S2.
        # ablate -> OR pool (softmax-weighted sum); else AND (log-product).
        g = torch.sigmoid(gates_logits)                    # (S, S2)
        # broadcast incidence over batch/time via weighted aggregation
        # log-AND: for each S2, prod over S of (g[s,s2]) ^ weight[s]
        # = exp( sum_s weight[s] * log g[s,s2] )
        lw = torch.log(g.clamp_min(1e-6))                  # (S, S2)
        if ablate:
            # OR-pool: softmax-weighted sum of incidence (attention-like)
            return torch.einsum('bst,su->but', torch.softmax(weights, dim=1), g)
        # soft AND = exp( sum_s weight[s] * log g[s,u] ); clamp to avoid overflow
        return torch.exp(torch.einsum('bst,su->but', weights, lw).clamp(-30, 30))

    def forward(self, x, ablate: bool = False):
        B, d, T = x.shape
        ext = torch.sigmoid(self.obj_gate(x))              # (B, no, T) extent
        intent = torch.sigmoid(self.attr_gate(x))          # (B, na, T) intent
        K = 1 if ablate else self.K
        for _ in range(K):
            # intent' = attributes shared by ALL gated objects (AND over objects)
            intent = self._and_pool(ext, self.context, ablate)         # (B, na, T)
            # extent' = objects having ALL gated attributes (AND over attrs)
            ext = self._and_pool(intent, self.context.t(), ablate)     # (B, no, T)
        # idempotence monitor: re-derive once more, measure drift
        intent2 = self._and_pool(ext, self.context, ablate)
        idem = (intent2 - intent).pow(2).mean()
        concept = torch.cat([ext, intent], dim=1)          # (B, no+na, T)
        x_bound = x + torch.tanh(self.gate) * self.Wout(concept)
        return x_bound, idem


def build_bind(d, V, k, bind_steps):
    return GaloisLatticeBind(d=d, k=k, bind_steps=max(2, bind_steps // 4)), 0.0  # monitor-only


if __name__ == "__main__":
    run("H_1632 galois-lattice meet", build_bind)
