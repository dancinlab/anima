#!/usr/bin/env python3
"""_decode_selftest.py — byte-exact HARD GATE for the unified core/decode.py.

Builds a TINY synthetic ByteGPT .bin + a TINY synthetic CLM .clm (seeded random
weights, exact serialize layouts) and asserts:

  (A) ByteGPT KV-cache decode ids == full-forward decode ids, TOKEN-FOR-TOKEN,
      for argmax AND top-k sampled, at gen = 20/80/120 and several seeds. The
      window-slide regime (gen 80/120 > block=64) exercises the cache REBUILD.
  (B) decode.py's merged functions produce byte-identical token ids to the
      ORIGINAL clm_decode.py / bytegpt_decode.py for the same inputs.
  (C) KV-cache vs full-forward wall-time speedup on the tiny model.

Pure numpy, no torch — runs anywhere. Lives in state/ (not core/) so it never
ships in the self-contained core/ package. Run: python3 _decode_selftest.py
"""
import os
import sys
import struct
import time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.abspath(os.path.join(_HERE, "..", "..", "core"))
sys.path.insert(0, _CORE)

import decode                      # the NEW unified module (under test)
import clm_decode as clm_old       # ORIGINAL conv mouth
import bytegpt_decode as bg_old    # ORIGINAL byte mouth


# ════════════════════════════════════════════════════════════════════════
# tiny synthetic serializers (exact byte layouts bg_load / clm_load_weights read)
# ════════════════════════════════════════════════════════════════════════

def write_tiny_bin(path, seed, vocab=256, d=32, nlay=2, nh=4, block=64):
    """5xu32 ByteGPT header + f32 LE weights (exact bg_load layout)."""
    rng = np.random.default_rng(seed)

    def f32(a):
        return np.asarray(a, dtype=np.float32).astype('<f4').tobytes()

    out = bytearray()
    out += struct.pack("<5I", vocab, d, nlay, nh, block)
    out += f32(rng.standard_normal((vocab, d)) * 0.02)   # tok
    out += f32(rng.standard_normal((block, d)) * 0.02)   # pos
    for _ in range(nlay):
        out += f32(np.ones(d) + rng.standard_normal(d) * 0.05)  # ln1.w
        out += f32(rng.standard_normal(d) * 0.01)               # ln1.b
        out += f32(rng.standard_normal((3 * d, d)) * 0.05)      # in_proj.w
        out += f32(rng.standard_normal(3 * d) * 0.01)           # in_proj.b
        out += f32(rng.standard_normal((d, d)) * 0.05)          # out_proj.w
        out += f32(rng.standard_normal(d) * 0.01)               # out_proj.b
        out += f32(np.ones(d) + rng.standard_normal(d) * 0.05)  # ln2.w
        out += f32(rng.standard_normal(d) * 0.01)               # ln2.b
        out += f32(rng.standard_normal((4 * d, d)) * 0.05)      # mlp0.w
        out += f32(rng.standard_normal(4 * d) * 0.01)           # mlp0.b
        out += f32(rng.standard_normal((d, 4 * d)) * 0.05)      # mlp2.w
        out += f32(rng.standard_normal(d) * 0.01)               # mlp2.b
    out += f32(np.ones(d) + rng.standard_normal(d) * 0.05)      # ln_f.w
    out += f32(rng.standard_normal(d) * 0.01)                   # ln_f.b
    out += f32(rng.standard_normal((vocab, d)) * 0.02)          # head
    open(path, "wb").write(out)
    return {"vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block}


def write_tiny_clm(path, seed, d=16, K=3, E=2, L=2, V=256):
    """CLM\\x01 + int4-sym conv blocks + CLMX + f32 ext arrays (exact
    clm_load_weights layout)."""
    rng = np.random.default_rng(seed)
    out = bytearray()
    out += bytes([67, 76, 77, 1])          # CLM\x01
    nblk = L + E + 3
    out += bytes([nblk])

    def block(cout, rest, scale=0.05):
        n = cout * rest
        codes = rng.integers(-8, 8, size=n)          # int4 range [-8,7]
        packed = bytearray((n + 1) // 2)
        for i in range(0, n, 2):
            lo = (int(codes[i]) + 8) & 0xF
            hi = (int(codes[i + 1]) + 8) & 0xF if i + 1 < n else 0
            packed[i // 2] = lo | (hi << 4)
        b = bytearray()
        b += struct.pack("<II", cout, rest)
        b += bytes(packed)
        scales = (rng.random(cout).astype(np.float32) * scale)
        b += scales.astype('<f4').tobytes()
        return b

    out += block(d, d * K)                 # ec
    for _ in range(L):
        out += block(d, d * K)             # tc[L]
    for _ in range(E):
        out += block(d, d * K)             # eW[E]
    out += block(E, d)                     # rW (K=1)
    out += block(V, d)                     # roW (K=1)
    out += bytes([67, 76, 77, 88])         # CLMX
    out += bytes([0])                      # n_ext (ignored by loader)

    def ext(vals):
        vals = np.asarray(vals, dtype=np.float32)
        return struct.pack("<I", vals.size) + vals.astype('<f4').tobytes()

    out += ext(rng.standard_normal(V * d) * 0.02)   # embed
    out += ext(rng.standard_normal(d) * 0.01)        # ecB
    for _ in range(L):
        out += ext(rng.standard_normal(d) * 0.01)    # tcB
    for _ in range(E):
        out += ext(rng.standard_normal(d) * 0.01)    # eB
    out += ext(rng.standard_normal(E) * 0.01)        # rB
    out += ext(rng.standard_normal(V) * 0.01)        # roB
    for _ in range(L):
        out += ext(np.ones(d) + rng.standard_normal(d) * 0.05)  # tgG
    for _ in range(L):
        out += ext(rng.standard_normal(d) * 0.01)                # tgB
    out += ext(np.ones(d) + rng.standard_normal(d) * 0.05)       # noG
    out += ext(rng.standard_normal(d) * 0.01)                    # noB
    open(path, "wb").write(out)


# ════════════════════════════════════════════════════════════════════════
# gates
# ════════════════════════════════════════════════════════════════════════

def _first_div(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return i, a[i], b[i]
    if len(a) != len(b):
        return min(len(a), len(b)), "len=%d" % len(a), "len=%d" % len(b)
    return None


def gate_A(binpath):
    print("\n=== GATE A: ByteGPT KV-cache == full-forward (token-for-token) ===")
    W = decode.bg_load(binpath)
    print("  hdr:", {k: W[k] for k in ("vocab", "d", "nlay", "nh", "block")})
    seeds = ["The capital of France is", "consciousness: ", "x", "hello world"]
    rngs = [7, 42, 1234]
    gens = [20, 80, 120]
    ok = True
    n = 0
    for seed in seeds:
        for gen in gens:
            # argmax
            kv = decode._decode_argmax_W(W, seed, gen)["ids"]
            full = decode._decode_argmax_W_full(W, seed, gen)["ids"]
            n += 1
            fd = _first_div(kv, full)
            if fd is not None:
                ok = False
                print("  ✗ ARGMAX DIVERGE seed=%r gen=%d @pos %s  kv=%s full=%s"
                      % (seed, gen, fd[0], fd[1], fd[2]))
            # sampled (several rng seeds)
            for sr in rngs:
                kv = decode.bytegpt_decode_topk_sampled_W(W, seed, gen, 40, 0.7, sr)["ids"]
                full = decode.bytegpt_decode_topk_sampled_W_full(W, seed, gen, 40, 0.7, sr)["ids"]
                n += 1
                fd = _first_div(kv, full)
                if fd is not None:
                    ok = False
                    print("  ✗ SAMPLE DIVERGE seed=%r gen=%d rng=%d @pos %s  kv=%s full=%s"
                          % (seed, gen, sr, fd[0], fd[1], fd[2]))
    print("  %d decode-pairs compared, %s" % (n, "ALL TOKEN-IDENTICAL ✓" if ok else "MISMATCH ✗"))
    return ok


def gate_B(binpath, clmpath):
    print("\n=== GATE B: merged decode.py == ORIGINAL modules (token-identical) ===")
    ok = True

    # ---- ByteGPT ----
    Wn = decode.bg_load(binpath)
    Wo = bg_old.bg_load(binpath)
    seeds = ["The capital of France is", "z", "abcdef"]
    for seed in seeds:
        for gen in [20, 80, 120]:
            # new _full must be EXACTLY the old full-forward loop
            a = decode._decode_argmax_W_full(Wn, seed, gen)["ids"]
            b = bg_old._decode_argmax_W(Wo, seed, gen)["ids"]
            fd = _first_div(a, b)
            if fd is not None:
                ok = False
                print("  ✗ BYTE argmax _full!=old seed=%r gen=%d @%s %s/%s" % (seed, gen, *fd))
            # new KV public must be token-identical to old full-forward public
            a = decode.bytegpt_decode_argmax(binpath, seed, gen)["ids"]
            b = bg_old.bytegpt_decode_argmax(binpath, seed, gen)["ids"]
            fd = _first_div(a, b)
            if fd is not None:
                ok = False
                print("  ✗ BYTE argmax KV!=old seed=%r gen=%d @%s %s/%s" % (seed, gen, *fd))
            for sr in [7, 99]:
                a = decode.bytegpt_decode_topk_sampled_W(Wn, seed, gen, 40, 0.7, sr)["ids"]
                b = bg_old.bytegpt_decode_topk_sampled_W(Wo, seed, gen, 40, 0.7, sr)["ids"]
                fd = _first_div(a, b)
                if fd is not None:
                    ok = False
                    print("  ✗ BYTE sample KV!=old seed=%r gen=%d rng=%d @%s %s/%s"
                          % (seed, gen, sr, *fd))

    # ---- CLM (verbatim port → must be byte-exact) ----
    Wn = decode.clm_load_weights(clmpath)
    Wo = clm_old.clm_load_weights(clmpath)
    print("  clm cfg:", decode.clm_config(clmpath))
    for seed in ["consciousness: ", "tension: ", "q"]:
        for gen in [20, 60]:
            a = decode.clm_decode_argmax(clmpath, seed, gen)["text"]
            b = clm_old.clm_decode_argmax(clmpath, seed, gen)["text"]
            if a != b:
                ok = False
                print("  ✗ CLM argmax new!=old seed=%r gen=%d" % (seed, gen))
            for sr in [7, 99]:
                a = decode.clm_decode_topk_sampled_W(Wn, seed, gen, 40, 0.7, sr)["text"]
                b = clm_old.clm_decode_topk_sampled_W(Wo, seed, gen, 40, 0.7, sr)["text"]
                if a != b:
                    ok = False
                    print("  ✗ CLM sample new!=old seed=%r gen=%d rng=%d" % (seed, gen, sr))
    # dispatch sanity
    assert decode.decode_mouth_kind(binpath) == "bytegpt", "mouth sniff .bin"
    assert decode.decode_mouth_kind(clmpath) == "clm", "mouth sniff .clm"
    print("  merged==original + mouth-dispatch: %s" % ("ALL IDENTICAL ✓" if ok else "MISMATCH ✗"))
    return ok


def gate_C(binpath):
    print("\n=== GATE C: KV-cache speedup vs full-forward ===")
    # tiny model (d=32,L=2): the pure-python sampler loop (vocab=256) is a fixed
    # per-token cost that masks the forward-pass savings → modest ratio.
    W = decode.bg_load(binpath)
    seed = "The capital of France is"
    gen = 80
    t = time.time(); decode.bytegpt_decode_topk_sampled_W_full(W, seed, gen, 40, 0.7, 7); t_full = time.time() - t
    t = time.time(); decode.bytegpt_decode_topk_sampled_W(W, seed, gen, 40, 0.7, 7); t_kv = time.time() - t
    ratio = t_full / t_kv if t_kv > 0 else float('inf')
    print("  [tiny d=32 L=2 sampled] gen=%d  full=%.3fs  kv=%.3fs  speedup=%.2fx"
          % (gen, t_full, t_kv, ratio))
    # realistic depth (d=128,L=6): forward cost dominates → true asymptotic speedup
    # in the growing-window eval regime (seed+gen < block, the 303M eval path).
    bigp = os.path.join(os.path.dirname(binpath), "_selftest_big.bin")
    write_tiny_bin(bigp, seed=1, vocab=256, d=128, nlay=6, nh=8, block=256)
    Wb = decode.bg_load(bigp)
    big_ratio = ratio
    for gen in (60, 120, 200):
        t = time.time(); f = decode._decode_argmax_W_full(Wb, seed, gen)["ids"]; tf = time.time() - t
        t = time.time(); k = decode._decode_argmax_W(Wb, seed, gen)["ids"]; tk = time.time() - t
        big_ratio = tf / tk if tk > 0 else float('inf')
        print("  [d=128 L=6 argmax]    gen=%3d  full=%.2fs  kv=%.2fs  speedup=%.2fx  ident=%s"
              % (gen, tf, tk, big_ratio, f == k))
    try:
        os.remove(bigp)
    except OSError:
        pass
    return big_ratio


def main():
    binp = os.path.join(_HERE, "_selftest_tiny.bin")
    clmp = os.path.join(_HERE, "_selftest_tiny.clm")
    write_tiny_bin(binp, seed=123)
    write_tiny_clm(clmp, seed=456)
    a = gate_A(binp)
    b = gate_B(binp, clmp)
    c = gate_C(binp)
    print("\n" + "=" * 60)
    print("SUMMARY: (A) KV==full: %s | (B) merged==old: %s | (C) speedup=%.2fx"
          % ("PASS" if a else "FAIL", "PASS" if b else "FAIL", c))
    print("RESULT:", "SUCCESS ✓" if (a and b) else "FAILURE ✗")
    for p in (binp, clmp):
        try:
            os.remove(p)
        except OSError:
            pass
    return 0 if (a and b) else 1


if __name__ == "__main__":
    sys.exit(main())
