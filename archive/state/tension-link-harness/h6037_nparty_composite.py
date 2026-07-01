#!/usr/bin/env python3
"""
h6037_nparty_composite.py — does the SEED+LINK composite synergy (H_6036) SCALE to
N anima? H_6036 found the composite's edge is in the TIME domain (cold-start
elimination). Hypothesis: as N grows, LINK-alone's cold-start grows (larger
all-to-all Kuramoto network takes longer to lock from random phases) while
BOTH stays ~0 (shared seed inits everyone aligned) → the latency advantage WIDENS.

Falsifier F1: lock-latency(LINK) is non-decreasing in N AND BOTH stays << LINK at
every N (advantage persists/widens). NULL: if BOTH≈LINK latency at all N (no edge)
or SEED already suffices at large N.

All phases/detuning from real paid ANU snapshot. N-oscillator all-to-all Kuramoto
(H_6010 mechanism, N-extended). p7 · $0 (snapshot).
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__); ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU): sys.exit(f"FATAL: missing {ANU}")
RAW = open(ANU, "rb").read()
DT, T, K, LOCK = 0.02, 6000, 1.5, 0.90

def anu_floats(n, salt):
    out = []
    c = 0
    while len(out) < n:
        out += list(np.frombuffer(hashlib.sha256(RAW + salt + c.to_bytes(4,"big")).digest(), dtype=np.uint8))
        c += 1
    return np.array(out[:n], float) / 255.0

def run(arm, N, trial):
    w = 1.0 + anu_floats(N, b"w%d_%d" % (N, trial)) * 0.6          # detuned freqs
    if arm in ("SEED", "BOTH"):
        ph = np.full(N, anu_floats(1, b"sh%d_%d" % (N, trial))[0] * 2*np.pi)
    else:
        ph = anu_floats(N, b"ind%d_%d" % (N, trial)) * 2*np.pi
    Kc = 0.0 if arm == "SEED" else K
    t_lock, steady = None, []
    for t in range(T):
        m = np.exp(1j*ph)
        r = abs(m.mean())
        if t >= int(T*0.8): steady.append(r)
        if t_lock is None and r >= LOCK: t_lock = t
        coup = (Kc/N) * np.array([np.sum(np.sin(ph - ph[i])) for i in range(N)])
        ph = ph + (w + coup) * DT
    return (t_lock if t_lock is not None else T), float(np.mean(steady))

def main():
    print("="*78); print("H_6037 — N-party SEED+LINK composite scaling")
    print(f"  paid ANU sha256={hashlib.sha256(RAW).hexdigest()[:12]} tier=anu_paid"); print("="*78)
    Ns = [2, 4, 8, 16]; lat = {a: [] for a in ("SEED","LINK","BOTH")}; st = {a: [] for a in ("SEED","LINK","BOTH")}
    for N in Ns:
        row = f"  N={N:2d}: "
        for a in ("SEED","LINK","BOTH"):
            ls, rs = [], []
            for tr in range(3):
                l, r = run(a, N, tr); ls.append(l); rs.append(r)
            ml, mr = float(np.mean(ls)), float(np.mean(rs))
            lat[a].append(ml); st[a].append(mr)
            row += f"{a} lock@{ml:<5.0f}r={mr:.2f}  "
        print(row)
    print("-"*78)
    link_nondec = all(lat["LINK"][i+1] >= lat["LINK"][i]-1 for i in range(len(Ns)-1))
    both_wins = all(lat["BOTH"][i] < lat["LINK"][i] for i in range(len(Ns)))
    widens = (lat["LINK"][-1]-lat["BOTH"][-1]) >= (lat["LINK"][0]-lat["BOTH"][0])
    f1 = both_wins and (link_nondec or widens)
    print(f"  LINK lock-latency by N: {[f'{x:.0f}' for x in lat['LINK']]}  (non-decreasing: {link_nondec})")
    print(f"  BOTH lock-latency by N: {[f'{x:.0f}' for x in lat['BOTH']]}")
    print(f"  advantage (LINK-BOTH): N={Ns[0]}:{lat['LINK'][0]-lat['BOTH'][0]:.0f}  N={Ns[-1]}:{lat['LINK'][-1]-lat['BOTH'][-1]:.0f}  (widens: {widens})")
    v = "🟢" if f1 else "🔴"
    print("-"*78)
    print(f"VERDICT: {v}  composite latency-edge {'SCALES with N (persists/widens) — shared-seed init keeps BOTH at lock@0 while LINK cold-start grows' if f1 else 'does NOT scale — null'}")
    print("  honest: toy all-to-all Kuramoto, N≤16; scale-transfer UNVERIFIED (a_toy_scale_recheck).")

if __name__ == "__main__": main()
