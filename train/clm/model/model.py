"""CLM conv-MoE model skeleton (toy scale).

Implements the CLM P0 architecture (CLM/P0_ARCHITECTURE.md):

    byte text (V=256)
      -> dilated conv embed
      -> dilated conv trunk (no attention)
      -> MoE conv layer (router picks among N small conv experts = mitosis cells)
      -> byte readout (next-byte prediction)

Three router variants are exposed via a flag (see RouterConfig.variant):

    "A"   : entropy-regularized routing      (content axis)
    "B"   : top-k routing + load-balance aux (routing axis)
    "AB"  : both A and B combined            (dual-axis, untried in prior art)

This is a CPU/Mac toy-scale skeleton. It is intentionally small
(d=64, 2 layers, 4 experts) so the load-balance probe runs at $0 on a laptop.
Per the design's Q4, toy-scale results are INTUITION ONLY (non-gate); the real
F-CLM-MONO judgment is the full-scale multi-rung fire (H_847 §3).

No attention is used anywhere: every operator is conv / linear, which keeps the
inference path inside the AKIDA primitive envelope (P0 §2, F-CLM-AKIDA-MAP).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint as _grad_checkpoint


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
@dataclass
class CLMConfig:
    """Tiny CLM config. Defaults are the P0 `tiny` rung (d64/L2/E4)."""

    vocab_size: int = 256          # byte vocabulary (V=256), P0 Q3 monopoly lever
    d_model: int = 64              # channel width
    n_trunk_layers: int = 2        # dilated conv trunk depth
    n_experts: int = 4             # MoE conv experts (= mitosis cells)
    kernel_size: int = 3           # conv kernel (causal)
    expert_kernel_size: int = 3    # per-expert conv kernel
    dilation_base: int = 2         # trunk dilation grows as base**layer
    max_dilation: int = 512        # CAP on trunk dilation (= dilation = min(base**i, max_dilation)).
                                   # A dilation >= seq_len pads the sequence with ~base**i zeros and
                                   # sees no real taps, so an uncapped base**i at deep L (e.g. L=30 ->
                                   # 2**29) explodes the causal-pad buffer (OOM) for ZERO modeling gain.
                                   # Capping at 512 keeps the receptive field >= a 512-token window and
                                   # is byte-eq-neutral for the L=1 golden (min(2**0,512)=1, unchanged).
    top_k: int = 1                 # experts selected per position (variant B/AB)
    grad_checkpoint: bool = False  # RUNTIME-only activation recompute (torch.utils.checkpoint).
                                   # When True, each trunk layer is recomputed in backward instead of
                                   # retained, cutting peak activation memory ~n_trunk_layers-fold so a
                                   # 7B d6208/L30/E30 rung fits one 80GB H100 (the reserved
                                   # --grad-checkpoint flag, now WIRED). Touches NO serialized weight
                                   # bytes -> byte-eq PRESERVED (like the dilation cap): a checkpointed
                                   # forward computes the IDENTICAL output; only the autograd tape's
                                   # activation retention changes. Default False keeps golden/3B unchanged.

    # router-variant knobs (see RouterConfig)
    variant: str = "AB"            # "A" | "B" | "AB"
    entropy_coef: float = 0.01     # arm A: entropy-regularization weight
    load_balance_coef: float = 0.01  # arm B: load-balance aux-loss weight

    dropout: float = 0.0

    def router_config(self) -> "RouterConfig":
        v = self.variant.upper()
        if v not in ("A", "B", "AB"):
            raise ValueError(f"variant must be A|B|AB, got {self.variant!r}")
        return RouterConfig(
            variant=v,
            n_experts=self.n_experts,
            top_k=self.top_k,
            entropy_coef=self.entropy_coef if v in ("A", "AB") else 0.0,
            load_balance_coef=self.load_balance_coef if v in ("B", "AB") else 0.0,
            hard_top_k=v in ("B", "AB"),
        )


@dataclass
class RouterConfig:
    variant: str
    n_experts: int
    top_k: int
    entropy_coef: float
    load_balance_coef: float
    hard_top_k: bool


# --------------------------------------------------------------------------- #
# Causal dilated conv block (trunk)
# --------------------------------------------------------------------------- #
class CausalDilatedConv1d(nn.Module):
    """1D causal conv with left-padding so position t never sees t+1.

    Causality matters for a next-byte LM: the readout at t must depend only on
    bytes <= t. We left-pad by (kernel_size - 1) * dilation and drop the right
    overhang.
    """

    def __init__(self, channels: int, kernel_size: int, dilation: int):
        super().__init__()
        self.kernel_size = kernel_size
        self.dilation = dilation
        self.pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(channels, channels, kernel_size, dilation=dilation)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, C, T)
        x = F.pad(x, (self.pad, 0))
        return self.conv(x)


class TrunkLayer(nn.Module):
    """Residual gated dilated-conv trunk layer (no attention)."""

    def __init__(self, cfg: CLMConfig, dilation: int):
        super().__init__()
        self.conv = CausalDilatedConv1d(cfg.d_model, cfg.kernel_size, dilation)
        self.norm = nn.GroupNorm(1, cfg.d_model)  # layernorm over channels
        self.act = nn.GELU()
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.conv(x)
        h = self.norm(h)
        h = self.act(h)
        h = self.drop(h)
        return x + h


# --------------------------------------------------------------------------- #
# MoE conv layer
# --------------------------------------------------------------------------- #
class ConvExpert(nn.Module):
    """A small causal conv expert = one mitosis cell (P0 Q2)."""

    def __init__(self, cfg: CLMConfig):
        super().__init__()
        self.conv = CausalDilatedConv1d(cfg.d_model, cfg.expert_kernel_size, dilation=1)
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.act(self.conv(x))


@dataclass
class MoEStats:
    """Per-forward routing diagnostics (filled by MoEConvLayer.forward)."""

    # mean router probability mass assigned to each expert over the batch*time
    usage: torch.Tensor                 # (n_experts,)
    aux_loss: torch.Tensor              # scalar (load-balance + entropy terms)
    entropy: torch.Tensor               # scalar mean per-token routing entropy


class MoEConvLayer(nn.Module):
    """Mixture of conv experts with a per-position softmax router.

    Router operates per (batch, time) position. Variants:

      A  (entropy-reg)      : soft mix of all experts; entropy bonus encourages
                              the router to keep its per-token distribution from
                              collapsing onto one expert (subtracted from loss).
      B  (top-k + lb)       : hard top-k gating; a load-balance aux loss
                              (Switch-Transformer style) penalizes uneven usage.
      AB (both)             : top-k routing + load-balance + entropy bonus.
    """

    def __init__(self, cfg: CLMConfig):
        super().__init__()
        self.rc = cfg.router_config()
        self.experts = nn.ModuleList(ConvExpert(cfg) for _ in range(cfg.n_experts))
        # router: per-position linear over channels -> expert logits
        self.router = nn.Conv1d(cfg.d_model, cfg.n_experts, kernel_size=1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, MoEStats]:
        # x: (B, C, T)
        B, C, T = x.shape
        n_e = self.rc.n_experts

        logits = self.router(x)                       # (B, n_e, T)
        probs = F.softmax(logits, dim=1)              # per-position dist

        # per-token routing entropy (nats), averaged
        ent_tok = -(probs * torch.log(probs + 1e-9)).sum(dim=1)  # (B, T)
        entropy = ent_tok.mean()

        # stack expert outputs: (B, n_e, C, T)
        ex_out = torch.stack([e(x) for e in self.experts], dim=1)

        if self.rc.hard_top_k:
            # hard top-k gate (variant B / AB)
            k = min(self.rc.top_k, n_e)
            topv, topi = probs.topk(k, dim=1)         # (B, k, T)
            # renormalize the kept gate weights
            gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)  # (B, k, T)
            mask = torch.zeros_like(probs).scatter_(1, topi, gate)  # (B, n_e, T)
        else:
            # soft mixture over all experts (variant A)
            mask = probs                              # (B, n_e, T)

        # weighted combine: (B, n_e, 1, T) * (B, n_e, C, T) -> sum over experts
        y = (mask.unsqueeze(2) * ex_out).sum(dim=1)   # (B, C, T)

        # ----- usage stats + aux losses ----------------------------------- #
        # "usage" = fraction of routing mass each expert receives (soft probs,
        # the importance signal). Used by the load-balance loss and by the
        # offline balance probe.
        usage = probs.mean(dim=(0, 2))                # (n_e,)

        aux = x.new_zeros(())
        if self.rc.load_balance_coef > 0.0:
            # Switch-Transformer load-balance: n_e * sum_i (f_i * P_i)
            # f_i = fraction of tokens dispatched to expert i (top-1 routing
            #       fraction), P_i = mean router prob for expert i.
            # VECTORIZED: a Python `[(top1==i).mean() for i in range(n_e)]` loop
            # launches n_e separate reductions + GPU syncs per forward (the
            # per-step bottleneck at n_e=30). one_hot+mean is a single fused op,
            # mathematically identical (per-class fraction == one-hot mean).
            top1 = probs.argmax(dim=1)                            # (B, T)
            f_i = F.one_hot(top1, n_e).to(probs.dtype).mean(dim=(0, 1))  # (n_e,)
            p_i = usage
            lb = n_e * (f_i * p_i).sum()
            aux = aux + self.rc.load_balance_coef * lb
        if self.rc.entropy_coef > 0.0:
            # entropy bonus: maximize routing entropy -> subtract from loss
            aux = aux - self.rc.entropy_coef * entropy

        return y, MoEStats(usage=usage, aux_loss=aux, entropy=entropy)


# --------------------------------------------------------------------------- #
# Full model
# --------------------------------------------------------------------------- #
class CLMConvMoE(nn.Module):
    """Conv-native byte LM with a single MoE conv layer (toy skeleton)."""

    def __init__(self, cfg: CLMConfig):
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.d_model)
        # dilated conv embed (P0 §0: "dilated conv embed")
        self.embed_conv = CausalDilatedConv1d(cfg.d_model, cfg.kernel_size, dilation=1)

        # CAP dilation at cfg.max_dilation (WaveNet/TCN-style saturation). An
        # uncapped base**i at deep L explodes the causal pad (L=30 -> 2**29 ~5e8
        # left-pad) for no modeling benefit beyond a seq-length receptive field.
        # min(2**0, cap)=1 so the L=1 golden is byte-eq-unchanged.
        dils = [min(cfg.dilation_base ** i, cfg.max_dilation) for i in range(cfg.n_trunk_layers)]
        self.trunk = nn.ModuleList(TrunkLayer(cfg, d) for d in dils)
        self.moe = MoEConvLayer(cfg)
        self.norm_out = nn.GroupNorm(1, cfg.d_model)
        self.readout = nn.Conv1d(cfg.d_model, cfg.vocab_size, kernel_size=1)

    def forward(
        self, tokens: torch.Tensor, targets: Optional[torch.Tensor] = None
    ) -> dict:
        # tokens: (B, T) long
        x = self.embed(tokens)                  # (B, T, C)
        x = x.transpose(1, 2)                   # (B, C, T)
        x = self.embed_conv(x)
        # Gradient checkpointing (runtime-only, byte-eq-neutral): when enabled and
        # training, recompute each trunk layer's activations in backward instead of
        # retaining them. At L30/d6208 the retained-activation chain is what OOMs an
        # 80GB H100 (28GB fp32 weights + 8bit-optim state leave too little for 30
        # layers of (B,6208,512) activations); checkpointing trades ~1 extra forward
        # for ~L-fold less activation memory. use_reentrant=False = the modern
        # non-reentrant autograd path (handles no-input-grad embeds cleanly).
        ckpt = getattr(self.cfg, "grad_checkpoint", False) and self.training and x.requires_grad
        for layer in self.trunk:
            if ckpt:
                x = _grad_checkpoint(layer, x, use_reentrant=False)
            else:
                x = layer(x)
        x, stats = self.moe(x)
        x = self.norm_out(x)
        logits = self.readout(x)                # (B, V, T)

        out = {
            "logits": logits,
            "usage": stats.usage,
            "aux_loss": stats.aux_loss,
            "routing_entropy": stats.entropy,
        }
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.cfg.vocab_size),
                targets.reshape(-1),
            )
            out["ce_loss"] = ce
            out["loss"] = ce + stats.aux_loss
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


def build_model(variant: str = "AB", **overrides) -> CLMConvMoE:
    """Convenience factory. `variant` in {A, B, AB}."""
    cfg = CLMConfig(variant=variant, **overrides)
    return CLMConvMoE(cfg)
