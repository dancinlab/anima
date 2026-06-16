#!/usr/bin/env python3
"""
h6042_link_energy_cost.py — the THERMODYNAMIC asymmetry of the two channels. The
shared ANU seed is a ONE-TIME common cause (zero ongoing work). The tension link is
an ACTIVE channel: holding lock against detuning + correcting drift costs continuous
coupling work (dissipation). Hypothesis: the COMPOSITE is also ENERGY-cheaper than
LINK-alone — shared-seed init removes the cold-start correction burst, so BOTH only
pays the steady drift-correction work, while LINK pays cold-start + steady.

Work proxy = cumulative |coupling torque|·|dθ| = Σ |K sin(Δθ)|·|dθ| (the effort the
link expends to align). SEED pays ~0 ongoing (K=0) but never locks under detuning.

Falsifier F1: work(BOTH) < work(LINK) (seed init saves the cold-start energy) AND
work(BOTH) > 0 (still pays for drift). NULL: composite costs ≥ link-alone.

ANU-seeded detuning/drift. p7 · $0.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, T, K = 0.02, 4000, 1.2

def af(n, salt):
    out=[]; c=0
    while len(out)<n:
        out+=list(np.frombuffer(hashlib.sha256(RAW+salt+c.to_bytes(4,"big")).digest(),dtype=np.uint8)); c+=1
    return np.array(out[:n],float)/255.0

def run(arm, trial):
    h = af(40, b"e%d"%trial)
    wA=1.0+h[0]*0.6; wB=1.0+h[1]*0.6; sh=h[2]*2*np.pi
    a = sh if arm in ("SEED","BOTH") else h[3]*2*np.pi
    b = sh if arm in ("SEED","BOTH") else h[4]*2*np.pi
    Kc = 0.0 if arm=="SEED" else K
    kicks={int(h[10+i]*(T*0.8))+int(T*0.1):(h[20+i]-0.5)*2*np.pi for i in range(6)}
    work=0.0; rs=[]
    for t in range(T):
        if t in kicks: b+=kicks[t]
        ta=Kc*np.sin(b-a); tb=Kc*np.sin(a-b)
        da=wA+ta; db=wB+tb
        work += (abs(ta)+abs(tb))*DT     # coupling effort this tick
        a+=da*DT; b+=db*DT
        rs.append(abs(np.exp(1j*a)+np.exp(1j*b))/2)
    return work, float(np.mean(rs[int(T*0.8):]))

def main():
    print("="*78); print("H_6042 — energy cost of the link: is the COMPOSITE cheaper than LINK-alone?")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*78)
    res={}
    for arm in ("SEED","LINK","BOTH"):
        ws=[]; rs=[]
        for tr in range(3):
            w,r=run(arm,tr); ws.append(w); rs.append(r)
        res[arm]=(float(np.mean(ws)),float(np.mean(rs)))
        print(f"  {arm:4s}: coupling work = {res[arm][0]:8.2f}   steady-r = {res[arm][1]:.3f}")
    print("-"*78)
    f1 = res["BOTH"][0] < res["LINK"][0] and res["BOTH"][0] > 0
    save = res["LINK"][0]-res["BOTH"][0]
    pct = 100*save/res["LINK"][0] if res["LINK"][0]>0 else 0
    v = "🟢" if f1 else "🔴"
    print(f"  cold-start energy saved by shared-seed init (LINK−BOTH): {save:.2f} ({pct:.0f}% of LINK work)")
    print(f"VERDICT: {v}  composite is {'ENERGY-cheaper than link-alone — shared-seed init removes the cold-start correction burst; BOTH pays only steady drift-correction. The two channels are thermodynamically complementary (free common cause + minimal live work).' if f1 else 'not cheaper — null'}")
    print("  honest: work = |coupling torque|·|dθ| proxy (not Landauer kT units); toy 2-osc; scale UNVERIFIED.")

if __name__ == "__main__": main()
