#!/usr/bin/env python3
"""
h6036b_hexa_crosscheck.py — numpy reference for the .hexa engine lift
(engine_seed_link_composite.hexa). Uses the IDENTICAL byte/255 param map (NOT the
sha256 map of the original H_6036 harness) so the two implementations MUST match
numerically → proves the .hexa engine reproduces the composite mechanism, not a
mirror (H_1199 precedent). Reads the same committed paid ANU ints snapshot.
p7 · $0.
"""
import os, sys, math

_D = os.path.dirname(__file__)
INTS = os.path.join(_D, "..", "anu_seed_512.ints.txt")
if not os.path.exists(INTS): sys.exit(f"FATAL: missing {INTS}")
B = [float(x) for x in open(INTS).read().split()]
PI2, DT, T, K, LOCK = 2*math.pi, 0.02, 4000, 1.2, 0.90

def order2(a, b):
    cr = math.cos(a)+math.cos(b); ci = math.sin(a)+math.sin(b)
    return math.sqrt(cr*cr+ci*ci)/2.0

def run(arm, wA, wB, sh, iA, iB, kt, km):
    a = iA if arm == 1 else sh
    b = iB if arm == 1 else sh
    Kc = 0.0 if arm == 0 else K
    tl, acc, cnt = -1, 0.0, 0
    warm = int(T*0.8)
    for t in range(T):
        for i, kk in enumerate(kt):
            if kk == t: b += km[i]
        da = wA + Kc*math.sin(b-a); db = wB + Kc*math.sin(a-b)
        a += da*DT; b += db*DT
        r = order2(a, b)
        if tl < 0 and r >= LOCK: tl = t
        if t >= warm: acc += r; cnt += 1
    return acc/cnt, (T if tl < 0 else tl)

def main():
    print("numpy crosscheck (byte/255 map, same paid ANU ints):")
    sumR = [0.0,0.0,0.0]; sumL = [0.0,0.0,0.0]
    for ti, o in enumerate((0,160,320)):
        wA = 1.0+(B[o]/255.0)*0.6; wB = 1.0+(B[o+1]/255.0)*0.6
        sh = (B[o+2]/255.0)*PI2; iA = (B[o+3]/255.0)*PI2; iB = (B[o+4]/255.0)*PI2
        kt = [int((B[o+5+i]/255.0)*(T*0.8))+int(T*0.1) for i in range(6)]
        km = [((B[o+20+i]/255.0)-0.5)*PI2 for i in range(6)]
        line = f"  trial{ti+1}: "
        for arm,nm in ((0,"SEED"),(1,"LINK"),(2,"BOTH")):
            r,l = run(arm,wA,wB,sh,iA,iB,kt,km)
            sumR[arm]+=r; sumL[arm]+=l
            line += f"{nm} r={r:.3f} lock@{l}  "
        print(line)
    for arm,nm in ((0,"SEED"),(1,"LINK"),(2,"BOTH")):
        print(f"  {nm}: mean steady-r = {sumR[arm]/3:.3f}   mean ticks-to-lock = {sumL[arm]/3:.3f}")

if __name__ == "__main__": main()
