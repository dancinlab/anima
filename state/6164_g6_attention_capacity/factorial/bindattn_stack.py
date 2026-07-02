#!/usr/bin/env python3
"""bindattn_stack.py — H_6164 CAP×REG factorial: n_blocks extension of H_1449 BindAttn.

DESIGN-ONLY SCAFFOLD (pre-registration). DO NOT run heavy training from this file yet —
GPU is cost-gated behind explicit owner go (rung1 pool-first / rung2 explicit-go).

Extends archive/state/1449_g6_attention_injection/g6_common.py::BindAttnByteGPT (which
splices ONE trainable binding self-attention Block after the L24 trunk, gated so gate=0 is
byte-identical to base) to a STACK of `n_blocks` such blocks — FACTOR CAP:
    rung0 = n_blocks=1   (== H_1449, the DEAD anchor; DO NOT re-fire, cite only)
    rung1 = n_blocks∈{2,4}  @303M base   (depth-capacity lever, NEW)
    rung2 = n_blocks stack on a 7B-class trunk   (scale lever, explicit-go)

The stack is HOMOGENEOUS ByteGPT Blocks appended before ln_f, so the serialized ckpt is
just a deeper ByteGPT (.bin header n_layer bumped by n_blocks) → mounts through the SAME
generator L3 ByteGPT slot (a_core_engine_map) for the engine-native terminal read
(`anima evaluate --py`). No 2nd decode path is introduced.

c4 ABLATE (isolation): every injected block's residual gate forced to 0 → identity
passthrough → exact base regression. If FALS stays lifted with the whole stack ablated,
the lift is training-exposure (REGISTER), not the attention capacity → INERT (== H_1449).

torch import is LAZY (inside build_stack_model) so this module imports torch-free for the
numpy smoke of the plumbing + the register builder.
"""
import os

# CAP-factor rung → n_blocks map (frozen).
CAP_RUNGS = {"rung0": 1, "rung1_2": 2, "rung1_4": 4, "rung2": 2}  # rung2 depth on 7B trunk
# rung2 also swaps the trunk (d/n_layer) — the n_blocks stack rides on top; see PREREG.


def build_stack_model(base, n_head, n_blocks, ablate_off=False):
    """Splice `n_blocks` gated binding Blocks after base.blocks, before ln_f.

    Each block starts as identity (per-block scalar gate init 0) so the model loads
    byte-equivalent to base; training opens the gates. `ablate_off` zeroes ALL gates
    (the c4 control). Mirrors g6_common.BindAttnByteGPT for n_blocks=1 EXACTLY.
    """
    import torch  # lazy
    import torch.nn as nn
    import torch.nn.functional as F

    # Reuse the frozen base Block class from the H_1449 harness (h1129 arch, VERBATIM).
    Block = type(base.blocks[0])
    d = base.tok.embedding_dim

    class BindStackByteGPT(nn.Module):
        def __init__(self):
            super().__init__()
            self.base = base
            self.bind = nn.ModuleList([Block(d, n_head, 0.0) for _ in range(n_blocks)])
            self.gates = nn.ParameterList(
                [nn.Parameter(torch.zeros(1)) for _ in range(n_blocks)])
            self.ablate_off = ablate_off
            self.block = base.block

        def forward(self, idx, targets=None):
            b = self.base
            B, T = idx.shape
            pos = torch.arange(T, device=idx.device)
            x = b.drop(b.tok(idx) + b.pos(pos)[None, :, :])
            mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device),
                              diagonal=1)
            for blk in b.blocks:
                x = blk(x, mask)
            for blk, g in zip(self.bind, self.gates):
                gate = torch.zeros_like(g) if self.ablate_off else g
                x = x + gate * (blk(x, mask) - x)   # gate=0 == identity (byte-equiv base)
            logits = b.head(b.ln_f(x))
            loss = (F.cross_entropy(logits.view(-1, 256), targets.view(-1))
                    if targets is not None else None)
            return logits, loss

    return BindStackByteGPT()


def freeze_base(m):
    """Train ONLY the injected stack + gates; freeze the base trunk (isolates the CAP
    variable to the attention stack, not full-weight drift) — same as g6_common.freeze_base
    but over the ModuleList."""
    for p in m.base.parameters():
        p.requires_grad_(False)
    for blk in m.bind:
        for p in blk.parameters():
            p.requires_grad_(True)
    for g in m.gates:
        g.requires_grad_(True)


# ── plumbing self-test (torch-free) ──────────────────────────────────────────
def _plumbing_selftest():
    """Assert the CAP-rung → n_blocks contract without importing torch."""
    assert CAP_RUNGS["rung0"] == 1, "rung0 MUST be the H_1449 1-block anchor"
    assert CAP_RUNGS["rung1_2"] == 2 and CAP_RUNGS["rung1_4"] == 4, "rung1 = 2/4-block stack"
    return {"cap_rungs": CAP_RUNGS, "n_blocks_ok": True}


if __name__ == "__main__":
    import json
    print(json.dumps(_plumbing_selftest()))
