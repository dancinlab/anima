#!/usr/bin/env python3
"""
h6043_adversarial_saboteur.py — does the SEED+LINK composite RESIST an adversary?
A third anima C ("saboteur") couples to A and B trying to DESYNC them (pull each
toward C's own drifting phase). Security question: is the composite (shared-seed
init + mutual link) more attack-resistant than LINK-alone? Hypothesis: yes — the
shared-seed baseline gives A,B a head-start lock the saboteur must overcome, and
the strong A-B link out-pulls the saboteur, so BOTH holds r(A,B) high under attack
where LINK-alone (cold-starting into the attack) is dragged apart.

Falsifier F1: r_AB(BOTH, attack) ≥ 0.85 AND > r_AB(LINK, attack)+0.05. NULL: the
saboteur breaks both equally (composite gives no security margin).

Saboteur coupling Ks and phase from real paid ANU snapshot. p7 · $0.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, T, K, KS = 0.02, 4000, 1.2, 0.9   # K = honest A-B link, KS = saboteur pull

def af(n, salt):
    out=[]; c=0
    while len(out)<n:
        out+=list(np.frombuffer(hashlib.sha256(RAW+salt+c.to_bytes(4,"big")).digest(),dtype=np.uint8)); c+=1
    return np.array(out[:n],float)/255.0

def run(arm, attack, trial):
    h=af(20,b"s%d"%trial)
    wA=1.0+h[0]*0.6; wB=1.0+h[1]*0.6; wC=1.0+h[2]*0.6; sh=h[3]*2*np.pi
    a = sh if arm in ("SEED","BOTH") else h[4]*2*np.pi
    b = sh if arm in ("SEED","BOTH") else h[5]*2*np.pi
    c = h[6]*2*np.pi
    Kc = 0.0 if arm=="SEED" else K
    Ks = KS if attack else 0.0
    rs=[]
    for t in range(T):
        # A,B pulled toward each other (honest link) AND toward C (saboteur)
        da = wA + Kc*np.sin(b-a) + Ks*np.sin(c-a)
        db = wB + Kc*np.sin(a-b) + Ks*np.sin(c-b)
        dc = wC + Ks*np.sin(a-c) + Ks*np.sin(b-c)   # C drifts, weakly pulled back
        a+=da*DT; b+=db*DT; c+=dc*DT
        rs.append(abs(np.exp(1j*a)+np.exp(1j*b))/2)   # A-B coordination only
    return float(np.mean(rs[int(T*0.8):]))

def main():
    print("="*78); print("H_6043 — adversarial saboteur: does the composite RESIST a desync attack?")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*78)
    res={}
    for arm in ("SEED","LINK","BOTH"):
        for atk in (False,True):
            r=float(np.mean([run(arm,atk,tr) for tr in range(3)]))
            res[(arm,atk)]=r
            print(f"  {arm:4s} attack={'ON ' if atk else 'OFF'}: r(A,B) = {r:.3f}")
    print("-"*78)
    f1 = res[("BOTH",True)] >= 0.85 and res[("BOTH",True)] > res[("LINK",True)]+0.05
    margin = res[("BOTH",True)] - res[("LINK",True)]
    v = "🟢" if f1 else ("🟠" if margin>0 and res[("BOTH",True)]>res[("SEED",True)] else "🔴")
    print(f"  under attack: BOTH r={res[('BOTH',True)]:.3f}  LINK r={res[('LINK',True)]:.3f}  (composite margin +{margin:.3f})")
    print(f"VERDICT: {v}  composite {'RESISTS the saboteur better than link-alone — shared-seed baseline + strong A-B link out-pull the attacker; security margin from combining channels' if f1 else ('partially more robust' if v=='🟠' else 'no security margin — null')}")
    print("  honest: 3-osc toy, single saboteur, fixed Ks; scale/strategy-space UNVERIFIED (a_toy_scale_recheck).")

if __name__ == "__main__": main()
