#!/usr/bin/env python3
# make_tiny_ckpt.py — a TINY synthetic ByteGPT .bin (vocab=256,d=32,nlay=2,nh=4,block=256)
# purely to SMOKE the bytegpt_hidden_pool_ranged code path + the falsifier harness on mini
# (CPU, seconds). NOT a real model — weights are deterministic-pseudo so pooled != constant.
# The GROUNDING verdict is measured only on the real h1129 303M (pool). numpy only.
import os, struct
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tiny_bytegpt.bin")
V, D, L, H, B = 256, 32, 2, 4, 256
rng = np.random.default_rng(7)


def f32(n, scale=0.02):
    return (rng.standard_normal(n).astype(np.float32) * scale)


def main():
    parts = [struct.pack("<5I", V, D, L, H, B)]
    parts.append(f32(V * D).tobytes())      # tok
    parts.append(f32(B * D).tobytes())      # pos
    for _ in range(L):
        parts.append((np.ones(D, np.float32)).tobytes())   # ln1w
        parts.append(f32(D).tobytes())                     # ln1b
        parts.append(f32(3 * D * D).tobytes())             # in_proj.w
        parts.append(f32(3 * D).tobytes())                 # in_proj.b
        parts.append(f32(D * D).tobytes())                 # out_proj.w
        parts.append(f32(D).tobytes())                     # out_proj.b
        parts.append((np.ones(D, np.float32)).tobytes())   # ln2w
        parts.append(f32(D).tobytes())                     # ln2b
        parts.append(f32(4 * D * D).tobytes())             # mlp0.w
        parts.append(f32(4 * D).tobytes())                 # mlp0.b
        parts.append(f32(D * 4 * D).tobytes())             # mlp2.w
        parts.append(f32(D).tobytes())                     # mlp2.b
    parts.append((np.ones(D, np.float32)).tobytes())       # ln_f.w
    parts.append(f32(D).tobytes())                         # ln_f.b
    parts.append(f32(V * D).tobytes())                     # head
    with open(OUT, "wb") as w:
        w.write(b"".join(parts))
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes) V={V} d={D} L={L} H={H} block={B}")


if __name__ == "__main__":
    main()
