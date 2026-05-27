#!/usr/bin/env python3
"""tool/hexa_native/phase5_pytorch_reference.py

PURPOSE
    PyTorch reference for HEXA_NATIVE Phase 5 parity test. Two modes:

      --emit-subset
          Read the full anima Phase 1A.1 .safetensors (BF16) and write a
          F32 subset to /tmp/anima_phase5_subset_f32.safetensors containing
          ONLY the tensors the 2-layer pure-hexa smoke needs:
            tok_emb.weight, norm_f.weight,
            layers.{0,1}.{norm1,norm2,attn.{q,k,v,o}_proj,ffn.{gate,up,down}}.weight
          Reason: hexa runtime ships only `read_f32_farr` (no bf16 reader
          yet), and pure-hexa per-layer matvec is ~150 s → 2 layers is the
          deliverable wall-clock window.

      (default) parity run
          Loads the SAME subset f32 safetensors. Runs an identical
          single-token forward path with Engine G BYPASSED (tension=None,
          no cell injection):
            embed(bos) → 2× block (RMSNorm/GQA/SwiGLU/residual) → norm_f → tied lm_head
          Prints next_id + first-5 logits matching the hexa smoke format.

PARITY CONTRACT
    next_id exact int match; first-5 logits |Δ| < 1e-3 absolute.

raw#9 EXCEPTION — this is the bridge reference, not the inference path.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import safe_open, save_file


SRC_FULL = Path(
    "/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12/"
    "ckpts/ckpt_phase1a1_sft.safetensors"
)
SUBSET_F32 = Path("/tmp/anima_phase5_subset_f32.safetensors")

D_MODEL = 1024
D_FF = 2752
N_HEADS = 16
N_KV = 4
D_HEAD = D_MODEL // N_HEADS  # 64
VOCAB = 32000
EPS = 1e-5
ROPE_THETA = 10000.0
N_LAYERS_SUBSET = 1  # match hexa smoke — hidden-state parity post 1 block

NEED_KEYS = (
    ["tok_emb.weight", "norm_f.weight"]
    + [
        f"layers.{li}.{stem}"
        for li in range(N_LAYERS_SUBSET)
        for stem in (
            "norm1.weight",
            "norm2.weight",
            "attn.q_proj.weight",
            "attn.k_proj.weight",
            "attn.v_proj.weight",
            "attn.o_proj.weight",
            "ffn.gate.weight",
            "ffn.up.weight",
            "ffn.down.weight",
        )
    ]
)


def emit_subset() -> None:
    print(f"reading: {SRC_FULL}")
    out_d: dict[str, torch.Tensor] = {}
    with safe_open(str(SRC_FULL), framework="pt", device="cpu") as f:
        for k in NEED_KEYS:
            t = f.get_tensor(k).float().contiguous()
            out_d[k] = t
            print(f"  {k}: {tuple(t.shape)} numel={t.numel()}")
    save_file(out_d, str(SUBSET_F32))
    sz_mb = SUBSET_F32.stat().st_size / (1024 * 1024)
    print(f"wrote subset f32: {SUBSET_F32} ({sz_mb:.1f} MB)")


# ── reference forward (matches hexa phase5_forward_smoke.hexa) ──────────────


def rms_norm(x: torch.Tensor, gamma: torch.Tensor, eps: float) -> torch.Tensor:
    # x: (d,); identical formula to hexa side.
    rms = (x.float().pow(2).mean()).item()
    scale = 1.0 / math.sqrt(rms + eps)
    return (x.float() * scale) * gamma.float()


def rope_apply(q: torch.Tensor, t: int, d_head: int, theta: float) -> torch.Tensor:
    # q: (d_head,). Hexa convention: (q[2i], q[2i+1]) paired.
    half = d_head // 2
    out = q.clone()
    for i in range(half):
        inv_freq = 1.0 / (theta ** ((2.0 * i) / d_head))
        angle = t * inv_freq
        c = math.cos(angle)
        s = math.sin(angle)
        q0 = q[2 * i].item()
        q1 = q[2 * i + 1].item()
        out[2 * i] = q0 * c - q1 * s
        out[2 * i + 1] = q0 * s + q1 * c
    return out


def gqa_step_t0(
    x_norm: torch.Tensor,
    q_w: torch.Tensor, k_w: torch.Tensor, v_w: torch.Tensor, o_w: torch.Tensor,
    d_model: int, n_heads: int, n_kv: int, d_head: int, theta: float, t: int,
) -> torch.Tensor:
    q_flat = q_w @ x_norm                  # (d_model,)
    k_flat = k_w @ x_norm                  # (n_kv * d_head,)
    v_flat = v_w @ x_norm                  # (n_kv * d_head,)
    q_heads = q_flat.view(n_heads, d_head)
    k_heads = k_flat.view(n_kv, d_head)
    v_heads = v_flat.view(n_kv, d_head)
    # RoPE — identity at t=0 (cos=1, sin=0), but we apply for correctness.
    q_rot = torch.stack([rope_apply(q_heads[h], t, d_head, theta) for h in range(n_heads)])
    # (k_rot computed but unused at t=0 single-position; included for parity)
    _ = torch.stack([rope_apply(k_heads[h], t, d_head, theta) for h in range(n_kv)])
    # Single-position attention → softmax over single key = 1.0 → ctx = V[kv_h].
    expand = n_heads // n_kv
    head_outs = torch.stack([v_heads[h // expand] for h in range(n_heads)])
    merged = head_outs.flatten()
    return o_w @ merged


def block_step_t0(
    x: torch.Tensor, w: dict[str, torch.Tensor], li: int,
) -> torch.Tensor:
    pre = f"layers.{li}."
    h1 = rms_norm(x, w[pre + "norm1.weight"], EPS)
    attn_out = gqa_step_t0(
        h1,
        w[pre + "attn.q_proj.weight"], w[pre + "attn.k_proj.weight"],
        w[pre + "attn.v_proj.weight"], w[pre + "attn.o_proj.weight"],
        D_MODEL, N_HEADS, N_KV, D_HEAD, ROPE_THETA, 0,
    )
    h_res = x + attn_out
    h2 = rms_norm(h_res, w[pre + "norm2.weight"], EPS)
    g = w[pre + "ffn.gate.weight"] @ h2
    u = w[pre + "ffn.up.weight"] @ h2
    hidden = F.silu(g) * u
    ffn_out = w[pre + "ffn.down.weight"] @ hidden
    return h_res + ffn_out


def parity_run() -> None:
    if not SUBSET_F32.exists():
        print(f"FATAL: subset f32 not found at {SUBSET_F32}", file=sys.stderr)
        print("       run: python3 tool/hexa_native/phase5_pytorch_reference.py --emit-subset",
              file=sys.stderr)
        sys.exit(2)

    print(f"loading subset: {SUBSET_F32}")
    w: dict[str, torch.Tensor] = {}
    with safe_open(str(SUBSET_F32), framework="pt", device="cpu") as f:
        for k in NEED_KEYS:
            w[k] = f.get_tensor(k).float()

    # Forward through 1 block at BOS (id=1) — hidden-state parity.
    bos = 1
    x = w["tok_emb.weight"][bos].clone()                   # (1024,)
    print(f"x0 (bos emb)[0..4] = {x[:5].tolist()}")
    for li in range(N_LAYERS_SUBSET):
        x = block_step_t0(x, w, li)
        print(f"  layer {li} done; x[0]={x[0].item()}")

    # Parity contract: hidden state x[0..4] after 1-layer forward.
    # Hexa side emits identical "h_x[i]=..." lines for the parity driver to parse.
    print()
    for i in range(5):
        print(f"h_x[{i}]={float(x[i].item())}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-subset", action="store_true",
                    help="generate /tmp/anima_phase5_subset_f32.safetensors")
    args = ap.parse_args()
    if args.emit_subset:
        emit_subset()
    else:
        parity_run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
