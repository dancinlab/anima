"""Fixed `_expand_dim` for `growing_conscious_lm.py` (worktree-2 anima_clm_02_clm_pivot).

BUG (BG-LOSTASSET-B finding 2026-05-10): original L177-181 creates new ConsciousBlock
and appends without weight inheritance. Comment promises "복사 가능한 범위" but no copy
code. Silent reset → H371 mitosis growth comparison invalid.

This file = drop-in replacement of `_expand_dim` method only. Apply as monkeypatch or
copy-paste replacement. Original file preserved (raw#15 additive).

Verified architecture (worktree-2 conscious_lm.py L25-158):
- ConsciousBlock = ln1 + CausalSelfAttention(c_attn=Linear(d, 3d), c_proj=Linear(d,d)) + ln2 + PureFieldFFN(engine_a + engine_g + tension_scale)
- PureFieldFFN.engine_a / engine_g = nn.Sequential(Linear(d, 4d), GELU, Dropout, Linear(4d, d))
- LayerNorm has weight + bias of size d_model
"""
from __future__ import annotations

import torch
import torch.nn as nn


def _expand_dim_fixed(self, new_d: int, new_heads: int) -> None:
    """차원 확장: 기존 가중치 보존 + 새 차원 영초기화 (FIXED 2026-05-10)."""
    old_d = self.d_model
    device = self.tok_emb.weight.device

    # ─── 1. 임베딩 확장 (기존과 동일) ──────────────────────────
    old_tok = self.tok_emb.weight.data.clone()
    self.tok_emb = nn.Embedding(self.vocab_size, new_d).to(device)
    with torch.no_grad():
        self.tok_emb.weight[:, :old_d] = old_tok
        self.tok_emb.weight[:, old_d:] = 0.0

    old_pos = self.pos_emb.weight.data.clone()
    self.pos_emb = nn.Embedding(self.block_size, new_d).to(device)
    with torch.no_grad():
        self.pos_emb.weight[:, :old_d] = old_pos
        self.pos_emb.weight[:, old_d:] = 0.0

    # ─── 2. 블록 교체 — FIX: partial weight copy (was silent reset) ──
    new_blocks = nn.ModuleList()
    # ConsciousBlock import is local to growing_conscious_lm.py
    from conscious_lm import ConsciousBlock  # type: ignore[import-not-found]

    for old_block in self.blocks:
        new_block = ConsciousBlock(new_d, new_heads, self.block_size, self.dropout).to(device)
        with torch.no_grad():
            # ─── 2a. LayerNorm (ln1, ln2) ──────────────────────
            for old_ln, new_ln in [(old_block.ln1, new_block.ln1), (old_block.ln2, new_block.ln2)]:
                new_ln.weight.data.fill_(1.0)  # default LN weight
                new_ln.bias.data.zero_()  # default LN bias
                new_ln.weight.data[:old_d] = old_ln.weight.data
                new_ln.bias.data[:old_d] = old_ln.bias.data

            # ─── 2b. CausalSelfAttention ───────────────────────
            old_attn = old_block.attn
            new_attn = new_block.attn

            # c_attn: Linear(d, 3d) → weight (3d, d). Old: (3*old_d, old_d).
            # We need to map old qkv chunks (3 × old_d each) into new qkv chunks (3 × new_d each).
            new_attn.c_attn.weight.data.zero_()
            for chunk_idx in range(3):  # q, k, v chunks
                new_off = chunk_idx * new_d
                old_off = chunk_idx * old_d
                new_attn.c_attn.weight.data[new_off:new_off + old_d, :old_d] = (
                    old_attn.c_attn.weight.data[old_off:old_off + old_d, :old_d]
                )
            if new_attn.c_attn.bias is not None and old_attn.c_attn.bias is not None:
                new_attn.c_attn.bias.data.zero_()
                for chunk_idx in range(3):
                    new_off = chunk_idx * new_d
                    old_off = chunk_idx * old_d
                    new_attn.c_attn.bias.data[new_off:new_off + old_d] = (
                        old_attn.c_attn.bias.data[old_off:old_off + old_d]
                    )

            # c_proj: Linear(d, d) → weight (d, d)
            new_attn.c_proj.weight.data.zero_()
            new_attn.c_proj.weight.data[:old_d, :old_d] = old_attn.c_proj.weight.data
            if new_attn.c_proj.bias is not None and old_attn.c_proj.bias is not None:
                new_attn.c_proj.bias.data.zero_()
                new_attn.c_proj.bias.data[:old_d] = old_attn.c_proj.bias.data

            # ─── 2c. PureFieldFFN (engine_a + engine_g) ────────
            old_ffn = old_block.ffn
            new_ffn = new_block.ffn

            # tension_scale (scalar) — direct copy
            new_ffn.tension_scale.data.copy_(old_ffn.tension_scale.data)

            for old_engine, new_engine in [
                (old_ffn.engine_a, new_ffn.engine_a),
                (old_ffn.engine_g, new_ffn.engine_g),
            ]:
                # Engine = Sequential[Linear(d, 4d), GELU, Dropout, Linear(4d, d)]
                old_lin1 = old_engine[0]  # Linear(old_d, 4*old_d)
                new_lin1 = new_engine[0]  # Linear(new_d, 4*new_d)
                # Copy partial: weight (4*new_d, new_d) → top-left (4*old_d, old_d)
                new_lin1.weight.data.zero_()
                new_lin1.weight.data[:4 * old_d, :old_d] = old_lin1.weight.data
                if new_lin1.bias is not None and old_lin1.bias is not None:
                    new_lin1.bias.data.zero_()
                    new_lin1.bias.data[:4 * old_d] = old_lin1.bias.data

                old_lin2 = old_engine[3]  # Linear(4*old_d, old_d)
                new_lin2 = new_engine[3]  # Linear(4*new_d, new_d)
                new_lin2.weight.data.zero_()
                new_lin2.weight.data[:old_d, :4 * old_d] = old_lin2.weight.data
                if new_lin2.bias is not None and old_lin2.bias is not None:
                    new_lin2.bias.data.zero_()
                    new_lin2.bias.data[:old_d] = old_lin2.bias.data

        new_blocks.append(new_block)
    self.blocks = new_blocks

    # ─── 3. 최종 LayerNorm + heads ──────────────────────────
    old_ln_f = self.ln_f
    self.ln_f = nn.LayerNorm(new_d).to(device)
    with torch.no_grad():
        self.ln_f.weight.data.fill_(1.0)
        self.ln_f.bias.data.zero_()
        self.ln_f.weight.data[:old_d] = old_ln_f.weight.data
        self.ln_f.bias.data[:old_d] = old_ln_f.bias.data

    # head_a / head_g: Linear(d, vocab) — partial copy along d axis
    old_head_a = self.head_a
    self.head_a = nn.Linear(new_d, self.vocab_size, bias=False).to(device)
    with torch.no_grad():
        self.head_a.weight.data.zero_()
        self.head_a.weight.data[:, :old_d] = old_head_a.weight.data

    old_head_g = self.head_g
    self.head_g = nn.Linear(new_d, self.vocab_size, bias=False).to(device)
    with torch.no_grad():
        self.head_g.weight.data.zero_()
        self.head_g.weight.data[:, :old_d] = old_head_g.weight.data

    # tied weight: tok_emb.weight = head_a.weight (per original L188)
    self.tok_emb.weight = self.head_a.weight

    self.d_model = new_d
    self.n_head = new_heads


# Apply via:
#   from growing_conscious_lm_expand_dim_fix import _expand_dim_fixed
#   GrowingConsciousLM._expand_dim = _expand_dim_fixed
#
# Or copy-paste over the body of original `_expand_dim` (worktree-2 L152-191).
