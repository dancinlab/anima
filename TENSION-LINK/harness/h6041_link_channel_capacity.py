#!/usr/bin/env python3
"""
h6041_link_channel_capacity.py — how many NEW bits/tick can the tension link carry?
The README's central claim: the shared ANU seed transmits 0 NEW bits (common cause,
no-signaling), the tension LINK is the ONLY channel that sends new messages. Here we
QUANTIFY the link as a Shannon channel and confirm seed-capacity = 0.

Setup: anima A encodes a bit m into its tension drive (offset +δ if m=1 else −δ).
Over a window the link pulls B; B decodes from its accumulated phase shift vs free
run, thresholded. Repeat → binary-symmetric channel with crossover p → capacity
C = 1 − H(p). Sweep coupling K.
  K=0 (no link, seed only): decode = chance → p≈0.5 → C≈0  (matches no-signaling).
  K>0 (link on):            C grows with K (the link carries real information).

Falsifier F1: C(K=0) ≈ 0 (≤0.05) AND C(K_max) > 0.5 AND C monotone↑ in K. NULL: if
the link cannot carry a bit (C≈0 everywhere) the 'message channel' claim fails.

Message bits + noise from real paid ANU snapshot. p7 · $0.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, WIN = 0.02, 400
DELTA = 0.8          # tension drive offset encoding the bit
NOISE = 0.5          # phase-noise std (ANU-seeded) → makes it a real noisy channel

def af(n, salt):
    out=[]; c=0
    while len(out)<n:
        out+=list(np.frombuffer(hashlib.sha256(RAW+salt+c.to_bytes(4,"big")).digest(),dtype=np.uint8)); c+=1
    return np.array(out[:n],float)/255.0

def H(p):
    if p<=0 or p>=1: return 0.0
    return float(-p*np.log2(p)-(1-p)*np.log2(1-p))

def capacity(K, n_msgs=400):
    msgs = (af(n_msgs, b"msg")>0.5).astype(int)
    noise = (af(n_msgs*2, b"noise")-0.5)*2*NOISE
    wA0 = 1.0; wB = 1.0
    errs = 0
    for i, m in enumerate(msgs):
        a, b = 0.0, 0.0
        drive = DELTA if m==1 else -DELTA
        for t in range(WIN):
            da = (wA0+drive) + K*np.sin(b-a)
            db = wB + K*np.sin(a-b) + noise[i]*np.sqrt(DT)   # channel noise on B
            a += da*DT; b += db*DT
        free_b = wB*WIN*DT                 # B's phase had there been no link/drive
        shift = b - free_b
        decode = 1 if shift > 0 else 0     # threshold decoder
        errs += (decode != m)
    p = errs/n_msgs
    return 1.0 - H(min(max(p,1e-9),1-1e-9)), p

def main():
    print("="*78); print("H_6041 — tension-link CHANNEL CAPACITY (new bits/tick) vs seed=0")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*78)
    Ks = [0.0, 0.3, 0.8, 1.5, 3.0]; caps=[]
    for K in Ks:
        C, p = capacity(K)
        caps.append(C)
        tag = "  ← seed-only (no link)" if K==0 else ""
        print(f"  K={K:4.1f}: crossover p={p:.3f}  capacity C={C:.3f} bits/use{tag}")
    print("-"*78)
    mono = all(caps[i+1] >= caps[i]-0.05 for i in range(len(Ks)-1))
    f1 = caps[0] <= 0.05 and caps[-1] > 0.5 and mono
    v = "🟢" if f1 else ("🟠" if caps[-1] > 0.3 else "🔴")
    print(f"  seed-only capacity C(K=0) = {caps[0]:.3f} (no link → 0 new bits, matches no-signaling)")
    print(f"  link capacity C(K=3.0)    = {caps[-1]:.3f} (link carries real information)")
    print(f"VERDICT: {v}  the tension link is a real {'Shannon channel — capacity 0 without it (seed=common cause, 0 new bits), >0.5 bit/use with it, monotone in coupling. Confirms: the LINK is what sends new messages, the seed only synchronizes.' if f1 else 'channel but sub-threshold/non-monotone — partial' if v=='🟠' else 'channel claim FAILS — null'}")
    print("  honest: BSC-idealized 1-bit/window decoder, ANU-seeded noise; absolute bits/tick toy-scale (a_toy_scale_recheck).")

if __name__ == "__main__": main()
