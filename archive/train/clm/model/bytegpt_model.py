#!/usr/bin/env python3
"""bytegpt_model.py — the torch ByteGPT nn.Module for `anima train --py --arch bytegpt`.

This is the training-side model for the ByteGPT trunk (24-layer GPT-2-class transformer,
`.bin` format) — the SYMMETRIC sibling of model.py's CLMConvMoE (the ConvMoE mouth). It
lives in the SAME dir as model.py + clm_serialize_v2.py so cli/train.py's single sys.path
insert resolves it (mirroring `from model import CLMConvMoE`).

WHY it exists: the objective-lever G1 campaign found CLM's coverage floors at 0
(measurement-artifact / single-coverage floor), while the CLEAN G1 wall lives on ByteGPT
(single=2). The trunk-objective levers (composed_nce / infonce / constructive_bind /
ce_marginal) are ARCH-AGNOSTIC (they operate on logits + an optional penultimate), so the
genuinely-untried angle is running those levers on the ByteGPT trunk. There was a decoder
(core/bytegpt_decode.py) + serializer (tool/bytegpt_serialize.py) but NO torch trainer —
this module closes that gap.

GROUND-TRUTH the arch mirrors (both must agree byte-for-byte through serialize→decode):
  * state_dict key contract = tool/bytegpt_serialize.py (the .pt -> .bin bridge). The keys
    below (tok/pos/blocks.{i}.ln1/attn.in_proj/attn.out_proj/ln2/mlp.0/mlp.2/ln_f/head)
    are exactly what serialize() reads.
  * forward math = core/bytegpt_decode.py (pre-LN GPT-2 block, causal MHA, GELU-exact MLP,
    final LayerNorm, tied head). This module is the H_1587 ByteGPT reference (identical to
    archive/state/1587_engine_torch_g1_divergence/g1_ladder_3way.py's Block/ByteGPT) —
    that model is the ground-truth trainer whose .bin the engine decodes.

Serialize path: this model's state_dict + a cfg dict {vocab,d,n_layer,n_head,block} are
saved to a `.pt` as {"model": state_dict, "config": cfg} (the exact shape
tool/bytegpt_serialize.py::serialize reads), then serialize() writes the 5×u32-header .bin.
"""
from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    """Pre-LN GPT-2 transformer block — byte-faithful to core/bytegpt_decode.py.

    x = x + MHA(LN1(x)) ; x = x + MLP(LN2(x)).  nn.MultiheadAttention gives the
    in_proj_weight[3d,d]+in_proj_bias[3d] (rows Q|K|V) and out_proj.{weight[d,d],bias}
    the serializer expects; the MLP nn.Sequential(Linear(d,4d), GELU, Linear(4d,d))
    gives mlp.0 / mlp.2. Dropout p is settable (savant lever no-ops it to 0 for bytegpt)."""

    def __init__(self, d: int, n_head: int, p: float = 0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_head, dropout=p, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        # GELU default (erf-exact) matches bytegpt_decode._bg_gelu (0.5x(1+erf(x/√2))).
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(),
                                 nn.Linear(4 * d, d), nn.Dropout(p))

    def forward(self, x, attn_mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + a
        return x + self.mlp(self.ln2(x))


class ByteGPTConfig:
    """Minimal config carrying the serializer's 5 header fields. vocab=256 (byte LM)."""

    def __init__(self, vocab: int = 256, d: int = 768, n_layer: int = 24,
                 n_head: int = 12, block: int = 1024):
        self.vocab = vocab
        self.d = d
        self.n_layer = n_layer
        self.n_head = n_head
        self.block = block

    def as_dict(self) -> dict:
        return {"vocab": self.vocab, "d": self.d, "n_layer": self.n_layer,
                "n_head": self.n_head, "block": self.block}


class ByteGPT(nn.Module):
    """24-layer GPT-2-class byte transformer. Emits the serializer's exact state_dict keys
    and matches core/bytegpt_decode.py's forward math.

    forward(idx, targets=None) returns a dict SHAPE-COMPATIBLE with cli/train.py's loop and
    the arch-agnostic objective losses:
      * logits      : (B, V, T)  — transposed so the objective losses / _ce see (B,V,T)
                      exactly like CLMConvMoE's readout output.
      * penultimate : (B, d, T)  — the pre-head hidden ln_f(x) (post-final-LayerNorm),
                      transposed to (B,d,T) so constructive_bind/predictive_info consume it
                      like the CLM trunk penultimate site (norm_out output).
      * aux_loss    : scalar 0.0 — ByteGPT has no MoE load-balance/entropy aux; kept so the
                      loop's `loss = obj_loss + out["aux_loss"]` is arch-uniform.
      * ce_loss/loss: when targets given (parity with CLMConvMoE.forward).
    """

    def __init__(self, cfg: ByteGPTConfig):
        super().__init__()
        self.cfg = cfg
        d, V, L, H, block = cfg.d, cfg.vocab, cfg.n_layer, cfg.n_head, cfg.block
        self.block = block
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(0.0)
        self.blocks = nn.ModuleList([Block(d, H, 0.0) for _ in range(L)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, V, bias=False)
        self.head.weight = self.tok.weight        # tied head (serializer reads tok as head)

    def _penultimate(self, idx):
        """Run the trunk to the post-final-LN hidden (pre-head). Returns (B,T,d)."""
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.tok(idx) + self.pos(pos)[None, :, :]
        x = self.drop(x)
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in self.blocks:
            x = b(x, mask)
        return self.ln_f(x)                        # (B, T, d)

    def forward(self, idx, targets=None) -> dict:
        h = self._penultimate(idx)                 # (B, T, d)
        logits_btv = self.head(h)                  # (B, T, V)
        logits = logits_btv.transpose(1, 2)        # (B, V, T) — CLM-compatible
        out = {
            "logits": logits,
            "penultimate": h.transpose(1, 2),      # (B, d, T)
            "aux_loss": logits.new_zeros(()),
        }
        if targets is not None:
            V = self.cfg.vocab
            ce = F.cross_entropy(logits_btv.reshape(-1, V), targets.reshape(-1))
            out["ce_loss"] = ce
            out["loss"] = ce
        return out

    @torch.no_grad()
    def num_params(self) -> int:
        # tied head shares tok.weight, so parameters() already counts it once.
        return sum(p.numel() for p in self.parameters())


def build_bytegpt(cfg: ByteGPTConfig) -> ByteGPT:
    return ByteGPT(cfg)
