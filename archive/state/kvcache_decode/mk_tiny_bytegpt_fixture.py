#!/usr/bin/env python3
# Fixture generator (NOT a verdict path — produces a tiny random-weight ByteGPT
# binary in the exact bytegpt_decode.hexa layout for the byte-exact KV-cache smoke).
# Random weights are fine: the smoke proves two HEXA decode paths agree byte-for-byte
# on the SAME weights, which is weight-value-independent.
import struct, sys, random

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h1156_mount/bytegpt_tiny.bin"
    vocab, d, nlay, nh, block = 256, 64, 2, 4, 64
    random.seed(1234)
    def rnd(n):  # small magnitude so attention/gelu stay well-conditioned
        return [random.uniform(-0.08, 0.08) for _ in range(n)]
    buf = bytearray()
    buf += struct.pack("<5I", vocab, d, nlay, nh, block)
    def wf(vals):
        for v in vals:
            buf.extend(struct.pack("<f", v))
    wf(rnd(vocab * d))      # tok
    wf(rnd(block * d))      # pos
    for _ in range(nlay):
        wf([1.0] * d)               # ln1.w (init 1)
        wf([0.0] * d)               # ln1.b
        wf(rnd(3 * d * d))          # in_proj.w [3d,d]
        wf([0.0] * (3 * d))         # in_proj.b
        wf(rnd(d * d))              # out_proj.w [d,d]
        wf([0.0] * d)               # out_proj.b
        wf([1.0] * d)               # ln2.w
        wf([0.0] * d)               # ln2.b
        wf(rnd(4 * d * d))          # mlp0.w [4d,d]
        wf([0.0] * (4 * d))         # mlp0.b
        wf(rnd(d * 4 * d))          # mlp2.w [d,4d]
        wf([0.0] * d)               # mlp2.b
    wf([1.0] * d)                   # ln_f.w
    wf([0.0] * d)                   # ln_f.b
    wf(rnd(vocab * d))              # head
    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(buf)
    print(f"wrote {out}  ({len(buf)} bytes)  vocab={vocab} d={d} nlay={nlay} nh={nh} block={block}")

if __name__ == "__main__":
    main()
