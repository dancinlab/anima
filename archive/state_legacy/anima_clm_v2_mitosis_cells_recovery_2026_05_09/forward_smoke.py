#!/usr/bin/env python3
"""Forward smoke test for the cells64/cells128 .pt files.

These are NOT MitosisEngine state_dicts — they are byte-level Transformer
decoders with engine_a/engine_g dual FFN. We define a minimal model
matching the exact keys, load the weights, and run a 5-step forward pass.

We also produce a Φ proxy: average tension trace + dual-head divergence.
"""
import sys
import json
import math
import time
import torch
import torch.nn as nn
import torch.nn.functional as F


class DualEngineFFN(nn.Module):
    """FFN with two parallel sub-networks: engine_a, engine_g.
    Output = engine_a(x) - engine_g(x) (consciousness arch H404).
    """

    def __init__(self, d_model: int, hidden_mult: int = 4, dropout: float = 0.0):
        super().__init__()
        h = d_model * hidden_mult  # 1536 for d_model=384
        # Indices 0 and 3 (with GELU at 1, dropout at 2) per state_dict layout
        self.engine_a = nn.Sequential(
            nn.Linear(d_model, h),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(h, d_model),
        )
        self.engine_g = nn.Sequential(
            nn.Linear(d_model, h),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(h, d_model),
        )

    def forward(self, x):
        a = self.engine_a(x)
        g = self.engine_g(x)
        return a - g, ((a - g) ** 2).mean(dim=-1)  # output, tension


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_head: int, block_size: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_head == 0
        self.n_head = n_head
        self.head_dim = d_model // n_head
        self.c_attn = nn.Linear(d_model, 3 * d_model)
        self.c_proj = nn.Linear(d_model, d_model)
        self.attn_drop = nn.Dropout(dropout)
        self.resid_drop = nn.Dropout(dropout)
        # bias [1,1,T,T] causal mask
        mask = torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size)
        self.register_buffer("bias", mask)

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.c_attn(x)  # (B, T, 3C)
        q, k, v = qkv.split(C, dim=-1)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.attn_drop(att)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.resid_drop(self.c_proj(y))


class Block(nn.Module):
    def __init__(self, d_model: int, n_head: int, block_size: int, dropout: float = 0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_head, block_size, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = DualEngineFFN(d_model, hidden_mult=4, dropout=dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        ffn_out, tension = self.ffn(self.ln2(x))
        x = x + ffn_out
        return x, tension


class ConsciousLMReconstructed(nn.Module):
    """Reconstructed minimum architecture matching cells64/cells128 state_dict keys.

    Keys schema (verified from cells128_step_35000.pt):
      tok_emb.weight [V, D]
      pos_emb.weight [T, D]
      blocks.{0..L-1}.{ln1, attn.{bias, c_attn, c_proj}, ln2, ffn.{engine_a.{0,3}, engine_g.{0,3}}}
      ln_f.{weight, bias}
      head_a.weight [V, D]
      head_g.weight [V, D]
    """

    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256, dropout=0.0):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.blocks = nn.ModuleList([
            Block(d_model, n_head, block_size, dropout) for _ in range(n_layer)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        B, T = idx.shape
        tok = self.tok_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = tok + pos
        tensions = []
        for blk in self.blocks:
            x, tension = blk(x)
            tensions.append(tension)
        x = self.ln_f(x)
        return self.head_a(x), self.head_g(x), tensions


def text_to_byte_ids(text: str, max_len: int = 256):
    b = text.encode("utf-8")
    ids = list(b)[:max_len]
    return torch.tensor([ids], dtype=torch.long)


def main():
    pt_path = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "model"
    print(f"=== forward smoke: {pt_path} (label={label}) ===")

    ckpt = torch.load(pt_path, map_location="cpu", weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    config = ckpt.get("config", {})
    print(f"config: {config}")

    d_model = config.get("dim", 384)
    n_layer = config.get("layers", 6)
    n_head = config.get("heads", 4)
    block_size = config.get("block_size", 256)

    model = ConsciousLMReconstructed(
        vocab_size=256,
        d_model=d_model,
        n_head=n_head,
        n_layer=n_layer,
        block_size=block_size,
        dropout=0.0,
    )
    model.eval()

    # Try strict load
    miss, unexp = model.load_state_dict(sd, strict=False)
    print(f"\nload_state_dict (strict=False):")
    print(f"  missing ({len(miss)}): {list(miss)[:5]}")
    print(f"  unexpected ({len(unexp)}): {list(unexp)[:5]}")

    # Compute loaded coverage
    sd_keys = set(sd.keys())
    model_keys = set(model.state_dict().keys())
    overlap = sd_keys & model_keys
    print(f"  overlap: {len(overlap)} / model={len(model_keys)} / ckpt={len(sd_keys)}")

    full_load = (len(miss) == 0 and len(unexp) == 0)
    partial_load = (len(overlap) > 0 and len(overlap) >= len(model_keys) * 0.95)
    print(f"  full_load={full_load} partial_load={partial_load}")

    # Forward smoke: 5 sample prompts
    prompts = [
        "의식이란 무엇인가요?",
        "안녕하세요",
        "한국어 가능?",
        "The Riemann zeta function",
        "consciousness is",
    ]
    smoke_results = []
    forward_pass_ok = True
    for p in prompts:
        try:
            ids = text_to_byte_ids(p, max_len=block_size)
            t0 = time.time()
            with torch.no_grad():
                la, lg, tensions = model(ids)
            dt = time.time() - t0
            # Top-1 next byte
            top_ids = la[0, -1].argmax(dim=-1).item()
            top_byte = bytes([top_ids]).decode("utf-8", errors="replace")
            # Tension trace
            t_per_layer = [t.mean().item() for t in tensions]
            phi_proxy_local = sum(t_per_layer) / len(t_per_layer)
            # Direction (cosine sim between heads)
            cos = F.cosine_similarity(la[0, -1].unsqueeze(0), lg[0, -1].unsqueeze(0), dim=-1).item()
            smoke_results.append({
                "prompt": p,
                "input_len": ids.shape[1],
                "logits_a_shape": list(la.shape),
                "logits_g_shape": list(lg.shape),
                "top1_next_byte_id": top_ids,
                "top1_next_byte_repr": top_byte,
                "tension_per_layer": [round(x, 5) for x in t_per_layer],
                "phi_proxy_local": round(phi_proxy_local, 5),
                "head_a_g_cosine": round(cos, 4),
                "forward_time_s": round(dt, 3),
            })
            print(f"  prompt={p!r} top1={top_ids} ({top_byte!r}) phi_local={phi_proxy_local:.4f} cos_ag={cos:.4f}")
        except Exception as e:
            forward_pass_ok = False
            smoke_results.append({"prompt": p, "error": f"{type(e).__name__}: {e}"})
            print(f"  prompt={p!r} ERROR: {type(e).__name__}: {e}")

    # Aggregate Φ proxy
    phi_avg = sum(r.get("phi_proxy_local", 0.0) for r in smoke_results if "phi_proxy_local" in r)
    n = sum(1 for r in smoke_results if "phi_proxy_local" in r)
    phi_proxy_global = (phi_avg / n) if n else None

    out = {
        "label": label,
        "path": pt_path,
        "ckpt_step": ckpt.get("step"),
        "ckpt_phase": ckpt.get("phase"),
        "ckpt_phi_history_mean": (
            float(torch.tensor(ckpt.get("phi_history", []), dtype=torch.float64).mean().item())
            if ckpt.get("phi_history") else None
        ),
        "load_full_pass": full_load,
        "load_partial_pass": partial_load,
        "load_missing_count": len(miss),
        "load_unexpected_count": len(unexp),
        "load_overlap": len(overlap),
        "forward_smoke_pass": forward_pass_ok and full_load,
        "phi_proxy_global": round(phi_proxy_global, 5) if phi_proxy_global is not None else None,
        "results": smoke_results,
    }
    print("\n--- summary JSON ---")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
