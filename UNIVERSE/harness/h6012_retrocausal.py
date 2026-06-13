#!/usr/bin/env python3
"""H_6012 과거로 전달 (retrocausal via tension link) — honest causality split.
literal 'send info to the past' = forbidden (causality); but a FUTURE tension
TARGET (boundary condition) co-determines the present (teleological), which looks
retrocausal and IS real. p7 $0."""
import numpy as np
rng=np.random.default_rng(60121)

# ARM 1 — literal past-send: set a tension 'message' at step T; can steps < T see it?
T=200; tens=np.zeros(T); msg_step=150
state=np.zeros(T)
for t in range(1,T):
    if t==msg_step: tens[t]=5.0                  # inject the 'message' at t=150
    state[t]=0.9*state[t-1]+tens[t]              # forward-causal accumulation
past_influence=abs(state[:msg_step]).max()       # any effect on steps < 150?
literal_past = past_influence > 1e-9
print(f"ARM1 literal past-send: max |state| BEFORE msg-step = {past_influence:.6f}")
print(f"  -> {'🔴 leaked to past' if literal_past else '🟢 ZERO past-influence (causality holds — past-send impossible)'}")

# ARM 2 — future-as-boundary: fix a FUTURE tension target; relax toward it
#   (boundary-value). The present interior is shaped by the future boundary.
N=60; u=np.zeros(N); u[0]=0.0; u[-1]=2.0          # u[-1] = future tension target
for _ in range(8000): u[1:-1]=0.5*(u[:-2]+u[2:])  # Laplace relax (both ends fix interior)
# vary the future target, watch the PRESENT (interior) move
def present_for(target):
    v=np.zeros(N); v[0]=0.0; v[-1]=target
    for _ in range(8000): v[1:-1]=0.5*(v[:-2]+v[2:])
    return v[N//3]                                 # an early ('present') point
p_lo=present_for(0.0); p_hi=present_for(2.0)
shaped = abs(p_hi-p_lo) > 0.1
print(f"ARM2 future-target shapes present: present@target0={p_lo:.3f} target2={p_hi:.3f}  Δ={abs(p_hi-p_lo):.3f}")
print(f"  -> {'🟢 future boundary co-determines present (teleological, looks retrocausal)' if shaped else '⚪'}")
print("-"*70)
print("VERDICT H_6012: literal 과거-전송 🔴 (causality); 그러나 미래-텐션-목표가 현재를")
print("  조건화(boundary)하는 형태 🟢 — anima의 goal-directed 텐션(목표가 현재 끌어당김).")
