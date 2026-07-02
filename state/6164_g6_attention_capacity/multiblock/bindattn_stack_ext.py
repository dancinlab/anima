#!/usr/bin/env python3
"""G6 FALS BindAttn-STACK — multi-block extension of H_1449 (③ 안전, minimal blast radius).

DESIGN-ONLY scaffold. NOT wired to prod, NOT committed, NOT trained here.
Extends H_1449's ONE BindAttn block to N∈{2,3,4} FRESH-INIT blocks stacked AFTER the
frozen L24 ByteGPT trunk, BEFORE ln_f. Everything else (FROZEN h1305 detector, g6_common
5-bar + c4 ABLATE + SHUF-CORP, 3 seeds, corpus) is REUSED VERBATIM — the ONLY changed
variable is stack DEPTH N (width→depth of the injected binding head).

torch-side train = DIRECTIONAL (a_engine_native_learning). Terminal read = engine-native
`anima evaluate --py <clm>` on live core/ decode.

The torch class below MIRRORS g6_common.BindAttnByteGPT (gate-init-0 identity load, c4
ablate_off) but with a ModuleList of N Block()s each with its own scalar gate. c4 ABLATE
zeroes ALL N gates -> exact base regression (mechanism isolation intact).

This file carries ONLY the numpy forward-shape smoke (<30s, torch-free) so the N-block
stack shape is validated WITHOUT importing torch or touching weights. The real torch class
(commented ref) is spliced into g6_common at fire time under owner explicit-go.
"""
import numpy as np


# ── numpy MIRROR of ONE BindAttn Block forward (shape-only, random weights) ──
def _ln(x):
    m = x.mean(-1, keepdims=True); v = x.var(-1, keepdims=True)
    return (x - m) / np.sqrt(v + 1e-5)


def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z); return e / e.sum(-1, keepdims=True)


def _block_forward(x, d, h, mask, rng):
    """Single causal self-attn + MLP block, residual, gated by `gate`. Mirrors trunk Block."""
    B, T, _ = x.shape
    hd = d // h
    Wq, Wk, Wv, Wo = (rng.standard_normal((d, d)).astype(np.float32) * 0.02 for _ in range(4))
    hh = _ln(x)
    q = (hh @ Wq).reshape(B, T, h, hd).transpose(0, 2, 1, 3)
    k = (hh @ Wk).reshape(B, T, h, hd).transpose(0, 2, 1, 3)
    v = (hh @ Wv).reshape(B, T, h, hd).transpose(0, 2, 1, 3)
    att = (q @ k.transpose(0, 1, 3, 2)) / np.sqrt(hd) + mask
    a = (_softmax(att) @ v).transpose(0, 2, 1, 3).reshape(B, T, d) @ Wo
    x = x + a
    W1 = rng.standard_normal((d, 4 * d)).astype(np.float32) * 0.02
    W2 = rng.standard_normal((4 * d, d)).astype(np.float32) * 0.02
    hh2 = _ln(x)
    mlp = np.maximum(hh2 @ W1, 0) @ W2   # relu stand-in for gelu (shape only)
    return x + mlp


def stack_forward(trunk_out, d, h, N, gates, rng):
    """Apply N stacked BindAttn blocks with per-block scalar gate on the DELTA.
    gate=0 -> identity (byte-equivalent base load / c4 ablate). Returns [B,T,d]."""
    B, T, _ = trunk_out.shape
    mask = np.triu(np.full((T, T), -1e9, dtype=np.float32), 1)[None, None]
    x = trunk_out
    for n in range(N):
        delta = _block_forward(x, d, h, mask, rng) - x
        x = x + gates[n] * delta
    return x


def _smoke():
    rng = np.random.default_rng(0)
    d, h, B, T = 1024, 16, 2, 32   # h1129 303M ByteGPT geometry (d=1024,H=16,block=512→T subset)
    trunk_out = rng.standard_normal((B, T, d)).astype(np.float32)
    ok = True
    for N in (2, 3, 4):
        # gates all 0 => c4 ablate / identity load: output MUST equal trunk_out exactly
        y0 = stack_forward(trunk_out, d, h, N, gates=[0.0] * N, rng=np.random.default_rng(1))
        ident_ok = np.allclose(y0, trunk_out, atol=1e-6)
        # gates opened => shape preserved, output differs from trunk
        yg = stack_forward(trunk_out, d, h, N, gates=[1.0] * N, rng=np.random.default_rng(1))
        shape_ok = (yg.shape == trunk_out.shape)
        diff_ok = not np.allclose(yg, trunk_out, atol=1e-3)
        row = f"N={N}: identity(gate0)={ident_ok}  shape={yg.shape}={shape_ok}  gated!=trunk={diff_ok}"
        print(row)
        ok = ok and ident_ok and shape_ok and diff_ok
    # extra param-count sanity: N blocks each ~= one trunk Block (12*d^2 attn+mlp approx)
    per_block = 4 * d * d + 2 * (d * 4 * d)   # 4 attn proj + 2 mlp
    for N in (2, 3, 4):
        print(f"N={N}: added params ≈ {N * per_block / 1e6:.1f}M (base 303M frozen)")
    print("SMOKE_OK" if ok else "SMOKE_FAIL")


if __name__ == "__main__":
    _smoke()
