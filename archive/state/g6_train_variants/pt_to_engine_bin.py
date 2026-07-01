#!/usr/bin/env python3
"""pt_to_engine_bin.py — h1129 ByteGPT ckpt(.pt) → engine .bin (chat_full.bin format).

The G6 training-variant verdicts MUST be engine-native (a_engine_native_learning): the
trained torch ckpt has to be RE-MEASURED on the live CORE/bytegpt_decode mouth, NOT a torch
probe (the 1435/36/37 DIRECTIONAL mistake). This converts a trained .pt into the exact byte
layout CORE/bytegpt_decode.hexa::bg_load reads — the INVERSE of the parity-verify
torch_bin_layerdump.py (which READS chat_full.bin back into torch).

layout (CORE/bytegpt_decode.hexa header comment, VERBATIM):
  header  [vocab,d,n_layer,n_head,block]  5× u32 little-endian
  tok.weight[vocab*d] · pos.weight[block*d]
  per layer L: ln1.w[d] ln1.b[d] attn.in_proj_weight[3d*d] attn.in_proj_bias[3d]
               attn.out_proj.weight[d*d] attn.out_proj.bias[d] ln2.w[d] ln2.b[d]
               mlp.0.w[4d*d] mlp.0.b[4d] mlp.2.w[d*4d] mlp.2.b[d]
  ln_f.w[d] ln_f.b[d] head[vocab*d]   (head tied to tok)

usage: python3 pt_to_engine_bin.py <ckpt.pt> <out.bin>
VALIDATE: convert h1129c_chat.pt and assert byte-identical to the known chat_full.bin BEFORE
trusting any trained-variant .bin (catches a layout/key mismatch — c2).
"""
import struct, sys, numpy as np, torch

def export(ckpt_path, out_path):
    d_ = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = d_["model"] if isinstance(d_, dict) and "model" in d_ else d_
    cfg = d_.get("config", {}) if isinstance(d_, dict) else {}
    vocab = cfg.get("vocab", 256)
    d = cfg["d"]; nlay = cfg["n_layer"]; nh = cfg["n_head"]; block = cfg["block"]
    f = open(out_path, "wb")
    f.write(struct.pack("<5I", vocab, d, nlay, nh, block))
    def wr(key, shape=None):
        t = sd[key]
        if shape is not None:
            assert tuple(t.shape) == shape, f"{key} shape {tuple(t.shape)} != {shape}"
        # .float() FIRST — BFloat16/f16 tensors have no .numpy(); cast to f32 before export.
        # (root cause of chat_full.bin corruption: BFloat16 ckpt → broken/garbled .bin bytes)
        f.write(np.ascontiguousarray(t.detach().cpu().float().numpy(), dtype="<f4").tobytes())
    wr("tok.weight", (vocab, d))
    wr("pos.weight", (block, d))
    for L in range(nlay):
        p = f"blocks.{L}."
        wr(p + "ln1.weight", (d,));            wr(p + "ln1.bias", (d,))
        wr(p + "attn.in_proj_weight", (3*d, d)); wr(p + "attn.in_proj_bias", (3*d,))
        wr(p + "attn.out_proj.weight", (d, d));  wr(p + "attn.out_proj.bias", (d,))
        wr(p + "ln2.weight", (d,));            wr(p + "ln2.bias", (d,))
        wr(p + "mlp.0.weight", (4*d, d));      wr(p + "mlp.0.bias", (4*d,))
        wr(p + "mlp.2.weight", (d, 4*d));      wr(p + "mlp.2.bias", (d,))
    wr("ln_f.weight", (d,)); wr("ln_f.bias", (d,))
    # head tied to tok → state_dict may store head.weight or reuse tok.weight
    hk = "head.weight" if "head.weight" in sd else "tok.weight"
    wr(hk, (vocab, d))
    f.close()
    sz = struct.calcsize("<5I") + (vocab*d + block*d + nlay*(2*d + 3*d*d + 3*d + d*d + d + 2*d + 4*d*d + 4*d + d*4*d + d) + 2*d + vocab*d) * 4
    print(f"WROTE {out_path} cfg=(vocab={vocab} d={d} L={nlay} H={nh} block={block}) expected_bytes={sz}")

if __name__ == "__main__":
    export(sys.argv[1], sys.argv[2])
