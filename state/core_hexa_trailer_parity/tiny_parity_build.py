"""tiny-synthetic SLW+CLML parity harness (LOCAL byte-parity gate for the hexa
decode trailer port). Builds a tiny CLMConvMoE .clm, appends SLW + CLML trailers,
computes the numpy (decode.py) LAST-position logits golden, and writes a fixed
byte-seq the hexa smoke replays. Diff the two logit vectors = max|Δ| parity.

Run from core/ on sys.path (this script inserts it). Emits into the CWD outdir.
"""
import os, sys, struct
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.abspath(os.path.join(HERE, "..", "..", "core"))
sys.path.insert(0, CORE)

import serialize as S            # core/serialize.py
import verify_clm_v2 as VC       # core/verify_clm_v2.py (_build_synthetic_general)
from slw import pack_slw
from clml import pack_clml
import decode as D               # core/decode.py

OUT = os.environ.get("PARITY_OUT", HERE)
os.makedirs(OUT, exist_ok=True)

d, L, E, V, K = 16, 1, 2, 256, 3
n_slot, k, d_s, r, tau = 4, 8, 16, 8, 8.0
rng = np.random.default_rng(7)
def rf(*shape):
    return (rng.standard_normal(shape) * 0.1).astype("<f4")

# 1) tiny base .clm
sd, _ = VC._build_synthetic_general(d=d, L=L, E=E, K=K, V=V, seed=2026)
base = os.path.join(OUT, "tiny_base.clm")
S.serialize_v3(sd, L, E, base)

# 2) SLW trailer (weights match core/slw.py:_ARR_ORDER / slot_apply shapes)
slw = {"n_slot": n_slot, "k": k, "d_s": d_s,
       "K_slots": rf(n_slot, k),
       "W_r": rf(k, d), "b_r": rf(k), "W_q": rf(k, d), "b_q": rf(k),
       "W_v": rf(d_s, d), "b_v": rf(d_s), "W_o": rf(d, d_s), "b_o": rf(d),
       "w_g": rf(d), "b_g": rf(1), "gamma": np.asarray([0.6], "<f4")}
# 3) CLML trailer (core/clml.py:_ARR_ORDER / lane_apply shapes)
clml = {"lane_type": 1, "r": r, "tau": tau,
        "W1": rf(d, r), "b1": rf(r), "W2": rf(r, V),
        "w_g": rf(2 * d), "b_g": rf(1)}

trailered = os.path.join(OUT, "tiny_trailered.clm")
with open(base, "rb") as f:
    blob = f.read()
with open(trailered, "wb") as f:
    f.write(blob + pack_slw(slw) + pack_clml(clml))

# 4) fixed byte-seq (token ids = bytes) for both engines
T = 12
seq = (rng.integers(0, V, size=T)).astype(np.int64)
with open(os.path.join(OUT, "tiny_seed.bin"), "wb") as f:
    f.write(bytes(int(x) for x in seq))

def last_logits(clm_path):
    W = D.clm_load_weights(clm_path)
    lg = D._fwd_logits(W, seq.astype(np.float64), T)   # [T,V]
    return np.asarray(lg[T - 1], dtype=np.float64)

py_base = last_logits(base)
py_trail = last_logits(trailered)
# sanity: the trailers MUST change the output (else the wiring is a no-op)
d_bt = float(np.max(np.abs(py_trail - py_base)))
np.save(os.path.join(OUT, "py_last_logits.npy"), py_trail)
with open(os.path.join(OUT, "py_last_logits.txt"), "w") as f:
    for x in py_trail:
        f.write(repr(float(x)) + "\n")

print(f"[PY] base!=trailered max|Δ| = {d_bt:.6e}  (must be >0 = trailers active)")
print(f"[PY] trailered last-logits: V={py_trail.size} "
      f"min={py_trail.min():.6f} max={py_trail.max():.6f}")
print(f"[PY] wrote {trailered} + tiny_seed.bin + py_last_logits.{{npy,txt}}")
print(f"[CFG] d={d} L={L} E={E} V={V} K={K} n_slot={n_slot} k={k} r={r} tau={tau} T={T} gamma=0.6")
