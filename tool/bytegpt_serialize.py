#!/usr/bin/env python3
"""bytegpt_serialize.py — torch ByteGPT (.pt state_dict) -> engine .bin BRIDGE.

This is the .pt -> .bin bridge ONLY (a_clm_gen_pipeline): torch is ALLOWED here
because this produces the engine-loadable artifact; it is NOT the verdict scorer.
The VERDICT is the hexa-engine `anima eval <bin>` (generator L3 -> bytegpt_decode).

GROUND-TRUTH binary layout = core/bytegpt_decode.hexa (bg_load / bytegpt_forward_last):
    header 5x u32 little-endian: [vocab, d, n_layer, n_head, block]
    tok[vocab*d]  pos[block*d]
    per layer: ln1.w[d] ln1.b[d] in_proj.w[3d*d] in_proj.b[3d]
               out_proj.w[d*d] out_proj.b[d] ln2.w[d] ln2.b[d]
               mlp0.w[4d*d] mlp0.b[4d] mlp2.w[d*4d] mlp2.b[d]
    ln_f.w[d] ln_f.b[d]  head[vocab*d]
    all little-endian float32.

WEIGHT ORIENTATION (the decisive byte-faithfulness point):
  torch nn.Linear.weight is [out_features, in_features] row-major. The engine's
  _bg_linear computes  Y[t,o] = sum_c W[o*Ci+c]*X[t*Ci+c] + b[o]  == y = x . W^T + b
  i.e. the engine ALSO stores W as [Co,Ci] row-major and transposes at load
  (_bg_transpose). So torch's native [out,in] row-major is written VERBATIM — NO
  transpose in this serializer. (The engine comment L36 confirms: "torch Linear
  stores W as [out,in] row-major; y = x.W^T + b.")
  torch nn.MultiheadAttention.in_proj_weight is [3d,d] with rows packed Q|K|V,
  exactly what _bg_mha expects (rows 0..d=Q, d..2d=K, 2d..3d=V) — NO reordering.

Map (torch state_dict key -> engine slot), per train_and_ladder.py ByteGPT/Block:
  tok.weight                       -> tok    [vocab,d]
  pos.weight                       -> pos    [block,d]
  blocks.{i}.ln1.weight/.bias      -> ln1.w/.b
  blocks.{i}.attn.in_proj_weight   -> in_proj.w [3d,d]
  blocks.{i}.attn.in_proj_bias     -> in_proj.b [3d]
  blocks.{i}.attn.out_proj.weight  -> out_proj.w [d,d]
  blocks.{i}.attn.out_proj.bias    -> out_proj.b [d]
  blocks.{i}.ln2.weight/.bias      -> ln2.w/.b
  blocks.{i}.mlp.0.weight/.bias    -> mlp0.w [4d,d] / .b [4d]
  blocks.{i}.mlp.2.weight/.bias    -> mlp2.w [d,4d] / .b [d]
  ln_f.weight/.bias                -> ln_f.w/.b
  head.weight (tied to tok.weight) -> head   [vocab,d]
"""
import argparse, struct, sys
import numpy as np
import torch


def _f32le(t: torch.Tensor) -> bytes:
    """Flatten a tensor ROW-MAJOR (C-contiguous) to little-endian float32 bytes."""
    a = t.detach().cpu().to(torch.float32).contiguous().numpy()
    a = np.ascontiguousarray(a, dtype="<f4")  # little-endian float32, C order
    return a.tobytes()


def serialize(pt_path: str, bin_path: str) -> None:
    ck = torch.load(pt_path, map_location="cpu", weights_only=False)
    sd = ck["model"]
    cfg = ck["config"]
    vocab, d, n_layer, n_head, block = (
        int(cfg["vocab"]), int(cfg["d"]), int(cfg["n_layer"]),
        int(cfg["n_head"]), int(cfg["block"]),
    )
    print(f"[cfg] vocab={vocab} d={d} n_layer={n_layer} n_head={n_head} block={block}", flush=True)
    print(f"[cfg] val_ce={ck.get('val_ce')} step={ck.get('step')} nparam={ck.get('nparam')}", flush=True)

    def W(key, shape):
        if key not in sd:
            raise KeyError(f"missing state_dict key: {key}")
        t = sd[key]
        if tuple(t.shape) != tuple(shape):
            raise ValueError(f"{key} shape {tuple(t.shape)} != expected {tuple(shape)}")
        return _f32le(t)

    out = bytearray()
    # header
    out += struct.pack("<5I", vocab, d, n_layer, n_head, block)
    # embeddings
    out += W("tok.weight", (vocab, d))
    out += W("pos.weight", (block, d))
    # per layer
    for i in range(n_layer):
        p = f"blocks.{i}."
        out += W(p + "ln1.weight", (d,))
        out += W(p + "ln1.bias", (d,))
        out += W(p + "attn.in_proj_weight", (3 * d, d))
        out += W(p + "attn.in_proj_bias", (3 * d,))
        out += W(p + "attn.out_proj.weight", (d, d))
        out += W(p + "attn.out_proj.bias", (d,))
        out += W(p + "ln2.weight", (d,))
        out += W(p + "ln2.bias", (d,))
        out += W(p + "mlp.0.weight", (4 * d, d))
        out += W(p + "mlp.0.bias", (4 * d,))
        out += W(p + "mlp.2.weight", (d, 4 * d))
        out += W(p + "mlp.2.bias", (d,))
    # final norm + tied head
    out += W("ln_f.weight", (d,))
    out += W("ln_f.bias", (d,))
    head_key = "head.weight" if "head.weight" in sd else "tok.weight"  # tied
    out += W(head_key, (vocab, d))

    # expected size check
    per_layer = (d + d) + (3 * d * d + 3 * d) + (d * d + d) + (d + d) + \
                (4 * d * d + 4 * d) + (d * 4 * d + d)
    expected = 20 + (vocab * d + block * d) * 4 + n_layer * per_layer * 4 + \
               (d + d + vocab * d) * 4
    if len(out) != expected:
        raise AssertionError(f"size mismatch: wrote {len(out)} expected {expected}")

    with open(bin_path, "wb") as f:
        f.write(out)
    print(f"[ok] wrote {bin_path}  bytes={len(out)} (expected {expected})", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pt")
    ap.add_argument("bin")
    a = ap.parse_args()
    serialize(a.pt, a.bin)
