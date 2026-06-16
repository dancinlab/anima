#!/usr/bin/env python3
"""
h6038_drift_coupling_regime.py — WHERE does the SEED+LINK composite uniquely matter?
Phase diagram over (drift rate × coupling K). H_6036 showed BOTH wins on time, but
only in a regime: if drift=0 & no detuning, SEED suffices; if K huge, LINK locks
instantly (no cold-start). The composite is uniquely necessary in the GOLDILOCKS
middle: enough drift that SEED breaks, low enough K that LINK is slow.

Falsifier F1: there EXISTS a nontrivial (drift,K) cell where BOTH strictly beats
BOTH SEED and LINK on a combined score (final-r minus normalized lock-latency).
NULL: no cell where BOTH uniquely wins (one mechanism always dominates).

ANU-seeded; 2-oscillator H_6010 Kuramoto + drift kicks. p7 · $0.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, T, LOCK = 0.02, 4000, 0.90

def af(n, salt):
    out=[]; c=0
    while len(out)<n:
        out+=list(np.frombuffer(hashlib.sha256(RAW+salt+c.to_bytes(4,"big")).digest(),dtype=np.uint8)); c+=1
    return np.array(out[:n],float)/255.0

def run(arm, K, n_drift, trial):
    h = af(40, b"%d_%d_%d" % (int(K*100), n_drift, trial))
    wA = 1.0 + h[0]*0.6; wB = 1.0 + h[1]*0.6
    sh = h[2]*2*np.pi
    a = sh if arm in ("SEED","BOTH") else h[3]*2*np.pi
    b = sh if arm in ("SEED","BOTH") else h[4]*2*np.pi
    Kc = 0.0 if arm=="SEED" else K
    kicks = {int(h[10+i]*(T*0.8))+int(T*0.1): (h[20+i]-0.5)*2*np.pi for i in range(n_drift)}
    rs, tl = [], None
    for t in range(T):
        if t in kicks: b += kicks[t]
        da = wA + Kc*np.sin(b-a); db = wB + Kc*np.sin(a-b)
        a += da*DT; b += db*DT
        r = abs(np.exp(1j*a)+np.exp(1j*b))/2; rs.append(r)
        if tl is None and r>=LOCK: tl = t
    steady = float(np.mean(rs[int(T*0.8):])); tl = tl if tl is not None else T
    return steady - (tl/T)*0.5    # combined score: high final-r, penalize latency

def main():
    print("="*82); print("H_6038 — drift×coupling regime: where SEED+LINK composite UNIQUELY wins")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*82)
    Ks = [0.3, 0.6, 1.2]; drifts = [0, 3, 8]
    uniq = []
    print("  cell = winner among SEED/LINK/BOTH (combined score: final-r − 0.5·lock-latency/T)")
    print(f"  {'':12s}" + "".join(f"K={k:<7.1f}" for k in Ks))
    for nd in drifts:
        row = f"  drift={nd:<5d}"
        for K in Ks:
            sc = {a: float(np.mean([run(a,K,nd,tr) for tr in range(3)])) for a in ("SEED","LINK","BOTH")}
            win = max(sc, key=sc.get)
            margin = sc["BOTH"] - max(sc["SEED"], sc["LINK"])
            uw = (win=="BOTH" and margin>0.02)
            if uw: uniq.append((nd,K,margin))
            row += f"{win:5s}{'*' if uw else ' '}  "
        print(row)
    print("-"*82)
    f1 = len(uniq) > 0
    v = "🟢" if f1 else "🔴"
    print(f"  cells where BOTH UNIQUELY wins (margin>0.02, marked *): {len(uniq)}")
    for nd,K,m in uniq: print(f"    drift={nd} K={K} margin={m:.3f}")
    print(f"VERDICT: {v}  composite has a {'GOLDILOCKS regime (drift breaks SEED, low-K slows LINK) where it is uniquely best' if f1 else 'no unique regime — null'}")
    print("  honest: 2-osc toy, coarse 3×3 grid; scale-transfer UNVERIFIED (a_toy_scale_recheck).")

if __name__ == "__main__": main()
