#!/usr/bin/env python3
"""H_9027/H_6170 decode.hexa BGB byte-parity — torch-free fixture generator +
decode.py reference stream dumper.

Writes tiny (vocab=256 d=32 nlay=2 nh=4 block=16) ByteGPT .bin files DIRECTLY in
the bg_load byte layout (no torch): base.bin, inj_I1.bin (N=1 gate=0.7),
inj_I2.bin (N=2 gates=0.5,-0.4), inj_gate0.bin (N=1 gate=0.0). Then decodes each
with core/decode.py's bytegpt_decode_argmax (the numpy scorer, already validated
math-correct vs torch f64 in verify.txt / H_6170) and writes the greedy token-id
stream to <name>.pyids — the reference the decode.hexa probe must reproduce
byte-identically. This isolates the decode.hexa≡decode.py PARITY claim (task #2);
math-correctness was already gated by verify.py.
"""
import os, sys, struct
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import decode as D

VOCAB, D_, NLAY, NHEAD, BLOCK = 256, 32, 2, 4, 16
SEED_TEXT = b"hello world "
GEN = 48

rng = np.random.RandomState(1234)

def f32(*shape):
    return (rng.randn(*shape) * 0.3).astype('<f4')

def layer_bytes(d):
    """one transformer layer's 12 tensors in bg_load order (LE f32)."""
    out = bytearray()
    out += f32(d).tobytes()            # ln1w
    out += f32(d).tobytes()            # ln1b
    out += f32(3 * d, d).tobytes()     # inW  [3d,d]
    out += f32(3 * d).tobytes()        # inB
    out += f32(d, d).tobytes()         # oW   [d,d]
    out += f32(d).tobytes()            # oB
    out += f32(d).tobytes()            # ln2w
    out += f32(d).tobytes()            # ln2b
    out += f32(4 * d, d).tobytes()     # m0W  [4d,d]
    out += f32(4 * d).tobytes()        # m0B
    out += f32(d, 4 * d).tobytes()     # m2W  [d,4d]
    out += f32(d).tobytes()            # m2B
    return bytes(out)

def build_base():
    b = bytearray()
    b += struct.pack('<5I', VOCAB, D_, NLAY, NHEAD, BLOCK)
    b += f32(VOCAB, D_).tobytes()      # tok
    b += f32(BLOCK, D_).tobytes()      # pos
    for _ in range(NLAY):
        b += layer_bytes(D_)
    b += f32(D_).tobytes()             # lnfw
    b += f32(D_).tobytes()             # lnfb
    b += f32(VOCAB, D_).tobytes()      # head
    return bytes(b)

def build_bind_trailer(gates):
    t = bytearray()
    t += bytes([66, 71, 66, 1])        # "BGB\x01"
    t += struct.pack('<I', len(gates)) # n_bind
    for g in gates:
        t += layer_bytes(D_)           # one full base-layer block
        t += struct.pack('<f', float(g))  # gate
    return bytes(t)

def write(path, data):
    with open(path, 'wb') as f:
        f.write(data)
    print("  wrote %-16s %d bytes" % (os.path.basename(path), len(data)))

def dump_ids(binpath):
    ids = D.bytegpt_decode_argmax(binpath, list(SEED_TEXT), GEN)["ids"]
    idpath = binpath + ".pyids"
    with open(idpath, 'w') as f:
        f.write(" ".join(str(i) for i in ids) + "\n")
    print("  py stream %-16s %s ..." % (os.path.basename(binpath), ids[:12]))
    return ids

base = build_base()
base_bin = os.path.join(HERE, "base.bin")
write(base_bin, base)

i1 = base + build_bind_trailer([0.7])
i1_bin = os.path.join(HERE, "inj_I1.bin"); write(i1_bin, i1)

i2 = base + build_bind_trailer([0.5, -0.4])
i2_bin = os.path.join(HERE, "inj_I2.bin"); write(i2_bin, i2)

g0 = base + build_bind_trailer([0.0])
g0_bin = os.path.join(HERE, "inj_gate0.bin"); write(g0_bin, g0)

print("\n[decode.py reference streams] seed=%r gen=%d" % (SEED_TEXT, GEN))
ids_base = dump_ids(base_bin)
ids_i1 = dump_ids(i1_bin)
ids_i2 = dump_ids(i2_bin)
ids_g0 = dump_ids(g0_bin)

# sanity in-py: prefix-verbatim + gate0==base + trailer read + gate!=0 diverges
raw_base = open(base_bin, 'rb').read()
assert open(i1_bin, 'rb').read()[:len(raw_base)] == raw_base, "I1 prefix not verbatim"
assert D.bg_load(base_bin).get("bind") == [], "base has spurious bind"
assert len(D.bg_load(i1_bin)["bind"]) == 1 and len(D.bg_load(i2_bin)["bind"]) == 2
assert ids_g0 == ids_base, "py: gate0 must equal base"
assert ids_i1 != ids_base, "py: I1 nonzero gate must diverge from base (else fixture is degenerate)"
assert ids_i2 != ids_base, "py: I2 nonzero gate must diverge from base"
print("\n  [py self-consistency] gate0==base, I1/I2 diverge, trailer n_bind ok — fixtures valid")
