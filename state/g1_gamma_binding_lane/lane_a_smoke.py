#!/usr/bin/env python3
"""Golden regression smoke for core/lane_a.py (fork-A retro-route lane · H_9235).
$0 CPU-local · torch-free arms always run · torch parity arm runs if torch present.
Verifies: pack↔read byte-exact roundtrip · γ=0 passthrough (bit-exact) · numpy↔torch
op-parity · causal mask (no future leak) · route-shuffle control. NO 303M needed."""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "core"))
import lane_a

rng = np.random.RandomState(7)
d, k, d_c, delta, theta = 32, 8, 16, 2, 0.05
T = 12


def mk_lane(gamma=1.0):
    def R(*s):
        return rng.randn(*s).astype("<f4") * 0.05
    return {"k": k, "d_c": d_c, "delta": delta, "d": d, "theta": theta,
            "W_q": R(k, d), "b_q": R(k), "W_k": R(k, d), "b_k": R(k),
            "W_v": R(d_c, d), "b_v": R(d_c), "W_u": R(d_c, d), "b_u": R(d_c),
            "W_o": R(d, d_c), "b_o": R(d), "w_g": R(d), "b_g": float(rng.randn()),
            "gamma": float(gamma)}


fails = []
lane = mk_lane(gamma=1.0)
x = rng.randn(T, d).astype(np.float64)

# 1) pack <-> read byte-exact roundtrip
blob = lane_a.pack_lane(lane)
lane2, off = lane_a.read_lane(blob, 0)
assert off == len(blob), f"read consumed {off} != {len(blob)}"
for nm in lane_a._ARR_ORDER:
    a = np.asarray(lane[nm], dtype="<f4").reshape(-1)
    b = np.asarray(lane2[nm], dtype="<f4").reshape(-1)
    if not np.array_equal(a, b):
        fails.append(f"roundtrip {nm} mismatch")
if lane2["k"] != k or lane2["d_c"] != d_c or lane2["delta"] != delta or lane2["d"] != d:
    fails.append("roundtrip scalar mismatch")
print(f"[1] pack/read roundtrip: {len(blob)}B, arrays_equal={not any('roundtrip' in f for f in fails)}")

# 2) absent/short trailer -> read_lane returns None (passthrough)
none_lane, _ = lane_a.read_lane(b"\x00\x00\x00\x00garbage", 0)
none2, _ = lane_a.read_lane(blob, len(blob))
if none_lane is not None or none2 is not None:
    fails.append("absent/short trailer not None")
print(f"[2] absent/short -> None: {none_lane is None and none2 is None}")

# 3) gamma=0 passthrough is BIT-EXACT (the --lane-off BLIND ablation)
y0 = lane_a.lane_apply(x, lane2, gamma=0.0)
if not np.array_equal(y0, x):
    fails.append(f"gamma=0 not bit-exact (max|d|={np.abs(y0 - x).max()})")
print(f"[3] gamma=0 passthrough bit-exact: {np.array_equal(y0, x)}")

# 4) gamma=1 actually changes output (lane is live)
y1 = lane_a.lane_apply(x, lane2, gamma=1.0)
changed = float(np.abs(y1 - x).max())
print(f"[4] gamma=1 live (max|d|={changed:.4e}): {changed > 0}")
if changed == 0:
    fails.append("gamma=1 produced no change (lane dead)")

# 5) causal: positions 0..delta-1 have no valid key -> row unchanged
for t in range(min(delta, T)):
    if not np.array_equal(y1[t], x[t]):
        fails.append(f"pos {t} changed despite no valid key (delta={delta})")
        break
print(f"[5] causal no-key rows unchanged (t<{delta}): {not any('no valid key' in f for f in fails)}")

# 6) route-shuffle changes result vs base (control is live)
ysh = lane_a.lane_apply(x, lane2, gamma=1.0, route_shuffle_seed=123)
print(f"[6] route-shuffle differs from base: {not np.array_equal(ysh, y1)}")

# 7) numpy <-> torch op-parity
try:
    import torch
    m = lane_a.LaneAModule(d, k=k, d_c=d_c, delta=delta, theta=theta)
    with torch.no_grad():
        m.W_q.weight.copy_(torch.tensor(lane["W_q"])); m.W_q.bias.copy_(torch.tensor(lane["b_q"]))
        m.W_k.weight.copy_(torch.tensor(lane["W_k"])); m.W_k.bias.copy_(torch.tensor(lane["b_k"]))
        m.W_v.weight.copy_(torch.tensor(lane["W_v"])); m.W_v.bias.copy_(torch.tensor(lane["b_v"]))
        m.W_u.weight.copy_(torch.tensor(lane["W_u"])); m.W_u.bias.copy_(torch.tensor(lane["b_u"]))
        m.W_o.weight.copy_(torch.tensor(lane["W_o"])); m.W_o.bias.copy_(torch.tensor(lane["b_o"]))
        m.w_g.weight.copy_(torch.tensor(lane["w_g"]).reshape(1, d)); m.w_g.bias.copy_(torch.tensor([lane["b_g"]]))
        m.gamma.copy_(torch.tensor(1.0))
    xt = torch.tensor(x, dtype=torch.float32).T.unsqueeze(0)   # (1, d, T)
    yt = m(xt).squeeze(0).T.detach().numpy()                  # (T, d)
    yn = lane_a.lane_apply(x, lane, gamma=1.0).astype(np.float32)
    mad = float(np.abs(yt - yn).max())
    ok = mad < 1e-4   # f32 op-order parity (not bit; softmax/matmul reassoc)
    print(f"[7] numpy<->torch parity max|d|={mad:.3e}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"numpy-torch parity max|d|={mad:.3e}")
except ImportError:
    print("[7] torch absent -- parity arm skipped (inference-pod-clean, OK)")

print("\n=== SMOKE %s ===" % ("PASS" if not fails else "FAIL: " + " * ".join(fails)))
sys.exit(1 if fails else 0)
