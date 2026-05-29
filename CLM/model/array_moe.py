"""Sparse-MoE expert-array forward + inter-expert dispatch entropy (DISSOLVE).

This module is the MITOSIS-ARRAY measurement harness (CLM/P0_ARCHITECTURE.md §11,
CLM/CLM.breakthrough.mining.md DISSOLVE). It EXTENDS the landed conv-MoE skeleton
(CLM/model/model.py) by reframing *scale* from `d_model` to `expert-COUNT` (@L2):

    scale axis = number of experts E (each expert is chip-fit, <= ~1.2M params)
    big model  = sum over E chip-fit experts (top-k sparse activation)
    routing-diversity = inter-expert dispatch entropy, MEASURED across an
                        expert-count sweep E in {4, 8, 16, 32, 64}.

Each expert is one mitosis cell = one AKD1000 chip (@L3). Only the TOP-K experts
are active per token (sparse dispatch, Switch/GShard style), so the GPU/CPU
forward cost stays cheap while E (and therefore effective capacity) scales.

HONEST (@L6, p7): physical multi-AKD1000 is currently just pi5 (1 chip). The
inter-CHIP dispatch entropy is therefore measured here via its SW/GPU surrogate
= inter-EXPERT dispatch entropy (top-1 hard-dispatch counts over experts). The
expert<->chip 1:1 mapping makes the surrogate == target for the dispatch
distribution; physical chip-to-chip DMA latency is the only un-measured axis
(hardware follow-up). This is a CPU/Mac toy harness ($0); toy != scale (H_666).

The dispatch entropy is reported in two equivalent units:
  * nats              : H = -sum_i p_i ln p_i   (max = ln E)
  * normalized        : H / ln E in [0, 1]      (1 = perfectly balanced)
A uniform-null z-score (vs the Dirichlet(1) uniform-simplex dispatch null) is
computed by the sweep runner (run_array_sweep.py), not here -- this module only
produces the raw per-expert dispatch counts + entropy for one forward.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

# import the landed skeleton pieces (CLM/model/model.py)
import os
import sys
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from model import CLMConfig, CausalDilatedConv1d, TrunkLayer, ConvExpert  # noqa: E402


# AKD1000 node budget per chip (P0 §11 / breakthrough.mining "~1.2M nodes").
# An expert whose param count exceeds this is NOT chip-fit (sweep flags it).
AKD1000_NODE_BUDGET = 1_200_000


@dataclass
class ArrayConfig:
    """Sparse-MoE expert-array config. Scale axis = `n_experts` (@L2)."""
    vocab_size: int = 256
    d_model: int = 64
    n_trunk_layers: int = 2
    n_experts: int = 8          # THE scale axis (swept 4..64)
    kernel_size: int = 3
    expert_kernel_size: int = 3
    dilation_base: int = 2
    top_k: int = 2              # sparse: only top-k experts active per token

    def to_clmconfig(self) -> CLMConfig:
        # reuse the skeleton config for the shared conv pieces
        return CLMConfig(
            vocab_size=self.vocab_size, d_model=self.d_model,
            n_trunk_layers=self.n_trunk_layers, n_experts=self.n_experts,
            kernel_size=self.kernel_size, expert_kernel_size=self.expert_kernel_size,
            dilation_base=self.dilation_base, top_k=self.top_k, variant="B",
        )


@dataclass
class DispatchStats:
    """Inter-expert dispatch diagnostics for one sparse forward."""
    dispatch_counts: torch.Tensor   # (n_experts,) top-1 hard dispatch counts
    dispatch_frac: torch.Tensor     # (n_experts,) normalized to sum 1
    entropy_nats: float             # H = -sum p ln p
    max_entropy_nats: float         # ln(n_experts)
    norm_entropy: float             # H / ln(n_experts) in [0,1]
    n_active_experts: int           # experts with count > 0


def _dispatch_entropy(counts: torch.Tensor) -> DispatchStats:
    total = counts.sum().clamp_min(1.0)
    frac = counts / total
    nz = frac[frac > 0]
    H = float(-(nz * torch.log(nz)).sum())
    ne = counts.numel()
    Hmax = math.log(ne) if ne > 1 else 0.0
    return DispatchStats(
        dispatch_counts=counts,
        dispatch_frac=frac,
        entropy_nats=H,
        max_entropy_nats=Hmax,
        norm_entropy=(H / Hmax) if Hmax > 0 else 0.0,
        n_active_experts=int((counts > 0).sum()),
    )


class SparseMoEArray(nn.Module):
    """Top-k sparse mixture of chip-fit conv experts (= mitosis cells = chips).

    Unlike the skeleton MoEConvLayer (which stacks ALL experts every forward),
    this layer DISPATCHES each (batch, time) position to only its top-k experts.
    That keeps per-token cost ~constant as E (the scale axis) grows -- the
    DISSOLVE property: big effective capacity, chip-fit per-unit footprint.

    The returned DispatchStats.dispatch_counts are the inter-expert (= inter-
    chip surrogate) hard dispatch counts used to compute dispatch entropy.
    """

    def __init__(self, cfg: ArrayConfig):
        super().__init__()
        self.cfg = cfg
        clm = cfg.to_clmconfig()
        self.experts = nn.ModuleList(ConvExpert(clm) for _ in range(cfg.n_experts))
        self.router = nn.Conv1d(cfg.d_model, cfg.n_experts, kernel_size=1)

    def expert_param_count(self) -> int:
        return sum(p.numel() for p in self.experts[0].parameters())

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, DispatchStats]:
        # x: (B, C, T)
        B, C, T = x.shape
        n_e = self.cfg.n_experts
        k = min(self.cfg.top_k, n_e)

        logits = self.router(x)                          # (B, n_e, T)
        probs = F.softmax(logits, dim=1)
        topv, topi = probs.topk(k, dim=1)                # (B, k, T)
        gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)

        # sparse combine: only the k selected experts contribute per position.
        # (toy harness: we still evaluate experts densely on CPU for simplicity,
        #  then mask -- the DISPATCH (counts) is what is genuinely sparse/top-k,
        #  which is the measured quantity. A real chip runs only the routed expert.)
        ex_out = torch.stack([e(x) for e in self.experts], dim=1)  # (B,n_e,C,T)
        mask = torch.zeros_like(probs).scatter_(1, topi, gate)     # (B,n_e,T)
        y = (mask.unsqueeze(2) * ex_out).sum(dim=1)                # (B,C,T)

        # inter-expert dispatch counts = top-1 routed expert per position
        top1 = probs.argmax(dim=1)                       # (B, T)
        counts = torch.bincount(top1.reshape(-1), minlength=n_e).float()
        stats = _dispatch_entropy(counts)
        return y, stats


class CLMArray(nn.Module):
    """Conv-native byte LM with a sparse expert-ARRAY MoE layer (DISSOLVE).

    Identical trunk/embed/readout to the skeleton; the MoE layer is the sparse
    top-k expert array whose expert-COUNT is the scale axis.
    """

    def __init__(self, cfg: ArrayConfig):
        super().__init__()
        self.cfg = cfg
        clm = cfg.to_clmconfig()
        self.embed = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.embed_conv = CausalDilatedConv1d(cfg.d_model, cfg.kernel_size, 1)
        dils = [cfg.dilation_base ** i for i in range(cfg.n_trunk_layers)]
        self.trunk = nn.ModuleList(TrunkLayer(clm, d) for d in dils)
        self.moe = SparseMoEArray(cfg)
        self.norm_out = nn.GroupNorm(1, cfg.d_model)
        self.readout = nn.Conv1d(cfg.d_model, cfg.vocab_size, kernel_size=1)

    def forward(self, tokens: torch.Tensor,
                targets: Optional[torch.Tensor] = None) -> dict:
        x = self.embed(tokens).transpose(1, 2)           # (B,C,T)
        x = self.embed_conv(x)
        for layer in self.trunk:
            x = layer(x)
        x, stats = self.moe(x)
        x = self.norm_out(x)
        logits = self.readout(x)                         # (B,V,T)
        out = {
            "logits": logits,
            "dispatch_counts": stats.dispatch_counts,
            "dispatch_entropy_nats": stats.entropy_nats,
            "dispatch_norm_entropy": stats.norm_entropy,
            "n_active_experts": stats.n_active_experts,
        }
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1),
            )
            out["ce_loss"] = ce
            out["loss"] = ce
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def expert_chip_fit(self) -> bool:
        """True iff a single expert fits the AKD1000 node budget (@L3)."""
        return self.moe.expert_param_count() <= AKD1000_NODE_BUDGET


# expert-count sweep axis (P0 §11.2 / @L7). Each entry keeps every expert
# chip-fit; the runner verifies expert_param_count <= AKD1000_NODE_BUDGET.
SWEEP_EXPERT_COUNTS: List[int] = [4, 8, 16, 32, 64]


def build_array(n_experts: int = 8, **overrides) -> CLMArray:
    cfg = ArrayConfig(n_experts=n_experts, **overrides)
    return CLMArray(cfg)
