#!/usr/bin/env python3
"""
h6039_corrupted_seed_rescue.py — does the tension LINK RESCUE a CORRUPTED shared
seed? The H_6008 shared-seed channel is a single point of failure: if one anima
forks with the WRONG ANU buffer (corruption / desync / split-brain), SEED-only
coordination collapses catastrophically (init mismatch, K=0, never recovers).
Hypothesis: the live tension link makes the composite DEGRADE GRACEFULLY — even
with a fully wrong seed, the link re-locks the pair.

Falsifier F1: r(BOTH, corrupted seed) ≥ 0.90 (graceful) WHILE r(SEED, corrupted) <
0.60 (catastrophic). NULL: if a corrupt seed also breaks BOTH, the link does not
rescue and the composite inherits the single-point-of-failure.

Two seeds drawn from DISJOINT halves of the real paid ANU snapshot (genuinely
independent quantum draws → a real 'wrong buffer'). p7 · $0.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, T, K = 0.02, 4000, 1.2

def af(seg, n, salt):
    out=[]; c=0
    while len(out)<n:
        out+=list(np.frombuffer(hashlib.sha256(seg+salt+c.to_bytes(4,"big")).digest(),dtype=np.uint8)); c+=1
    return np.array(out[:n],float)/255.0

def run(arm, corrupt, trial):
    good = RAW[:256]; bad = RAW[256:]      # two disjoint real ANU draws
    h = af(good, 8, b"p%d"%trial)
    wA = 1.0+h[0]*0.6; wB = 1.0+h[1]*0.6
    phA = af(good, 1, b"s%d"%trial)[0]*2*np.pi
    # B reads the shared seed too — but if corrupt, B got the WRONG (bad) buffer
    phB = (af(bad,1,b"s%d"%trial)[0]*2*np.pi) if corrupt else phA
    Kc = 0.0 if arm=="SEED" else K
    rs=[]
    for t in range(T):
        da=wA+Kc*np.sin(phB-phA); db=wB+Kc*np.sin(phA-phB)
        phA+=da*DT; phB+=db*DT
        rs.append(abs(np.exp(1j*phA)+np.exp(1j*phB))/2)
    return float(np.mean(rs[int(T*0.8):]))

def main():
    print("="*78); print("H_6039 — does the tension LINK rescue a CORRUPTED shared seed?")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*78)
    res={}
    for arm in ("SEED","BOTH"):
        for cor in (False,True):
            r = float(np.mean([run(arm,cor,tr) for tr in range(3)]))
            res[(arm,cor)] = r
            print(f"  {arm:4s} seed={'CORRUPT' if cor else 'good   '}: steady-r = {r:.3f}")
    print("-"*78)
    f1 = res[("BOTH",True)] >= 0.90 and res[("SEED",True)] < 0.60
    v = "🟢" if f1 else ("🟠" if res[("BOTH",True)] > res[("SEED",True)]+0.2 else "🔴")
    print(f"  SEED-only under corruption: {res[('SEED',True)]:.3f} ({'catastrophic' if res[('SEED',True)]<0.6 else 'survives'})")
    print(f"  BOTH under corruption:      {res[('BOTH',True)]:.3f} ({'graceful' if res[('BOTH',True)]>=0.9 else 'degraded'})")
    print(f"VERDICT: {v}  tension link {'RESCUES a corrupt shared seed — composite has NO single-point-of-failure (live channel dominates a bad common cause)' if f1 else ('partially mitigates' if v=='🟠' else 'does NOT rescue — null')}")
    print("  honest: 2-osc toy; corrupt = genuinely independent ANU half-buffer; scale UNVERIFIED.")

if __name__ == "__main__": main()
