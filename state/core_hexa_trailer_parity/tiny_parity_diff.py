"""Diff hexa last-logits (stdin or arg file, one f64/line) vs the numpy golden
(py_last_logits.npy). PASS if max|Δ| <= tol. Reports the worst position."""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
gold = np.load(os.path.join(HERE, "py_last_logits.npy"))

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hexa_parity_out.txt"
vals = []
with open(src) as f:
    for line in f:
        s = line.strip()
        if not s:
            continue
        try:
            vals.append(float(s))
        except ValueError:
            pass  # skip non-numeric log lines
hexa = np.asarray(vals, dtype=np.float64)

if hexa.size != gold.size:
    print(f"[FAIL] size mismatch: hexa={hexa.size} golden={gold.size} "
          f"(hexa output likely truncated / has log noise)")
    sys.exit(2)

delta = np.abs(hexa - gold)
i = int(np.argmax(delta))
tol = 1e-4   # to_string precision-limited; a real wiring bug => O(0.01-1.0)
print(f"[PARITY] V={gold.size}  max|Δ|={delta.max():.3e} @v={i} "
      f"(hexa={hexa[i]:.6f} py={gold[i]:.6f})  mean|Δ|={delta.mean():.3e}")
if delta.max() <= tol:
    print(f"[PASS] hexa SLW+CLML forward == numpy within {tol:.0e} "
          f"(to_string-precision-bounded; 303M pool = definitive f64 gate)")
    sys.exit(0)
print(f"[FAIL] max|Δ|={delta.max():.3e} > {tol:.0e} — wiring/order/index bug")
sys.exit(1)
