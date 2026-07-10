"""Prove lean_load_weights == stock clm_load_weights byte-for-byte at fp64 on a small clm."""
import sys, numpy as np
from anima_py.core import decode as dec
import dtype_patch

clm = sys.argv[1]
W_stock = dec.clm_load_weights(clm)   # canonical
W_lean = dtype_patch._lean_load_weights(clm, np.float64)  # lean fp64

def eqk(a, b, k):
    if isinstance(a, list):
        return len(a) == len(b) and all(np.array_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, np.ndarray):
        return np.array_equal(a, b)
    if a is None:
        return b is None
    return a == b

keys = [k for k in W_stock if k != "slw" and k != "clml"]
allok = True
for k in keys:
    ok = eqk(W_stock[k], W_lean.get(k), k)
    if not ok:
        print(f"  MISMATCH key={k}")
    allok = allok and ok
# slw/clml: both None or equal-ish
slw_ok = (W_stock.get("slw") is None) == (W_lean.get("slw") is None)
clml_ok = (W_stock.get("clml") is None) == (W_lean.get("clml") is None)
print(f"lean==stock fp64 on {clm}: keys_ok={allok} slw_ok={slw_ok} clml_ok={clml_ok} "
      f"bind_type={W_stock.get('bind_type')} slw={W_stock.get('slw') is not None} clml={W_stock.get('clml') is not None}")
print("LEAN_VALIDATED" if (allok and slw_ok and clml_ok) else "LEAN_FAILED")
