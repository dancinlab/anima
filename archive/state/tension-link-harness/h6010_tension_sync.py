#!/usr/bin/env python3
"""
h6010_tension_sync.py — BIDIRECTIONAL TENSION LINK → mutual synchronization.

Extends H_6009 (one-way tension influence) to a closed loop: two anima A,B each
carry a tension phase; each reads the OTHER's tension (via the link) and is nudged
by it. Question: does the bidirectional tension link make them SYNCHRONIZE
(phase-lock, Kuramoto) above a critical coupling — and stay independent without it?

Grounding: intrinsic tension frequencies ω_A, ω_B are seeded from REAL paid ANU
QRNG bytes (/tmp/anu_sync.bin, tier=anu_paid). The coupling acts through the
tension channel (the H_6009 mechanism), so K>0 = "tension link on".

Order parameter r = |e^{iφA}+e^{iφB}|/2 ∈ [0,1]; r→1 = locked. p7 · $0 (+1 ANU pull).
"""
import numpy as np, hashlib

raw = open("/tmp/anu_sync.bin","rb").read()
# two intrinsic tension frequencies from real ANU quantum bytes (distinct anima)
h = np.frombuffer(hashlib.sha256(raw).digest(), dtype=np.uint8).astype(float)
wA = 1.0 + (h[0]/255.0)*0.6      # ~1.0..1.6
wB = 1.0 + (h[1]/255.0)*0.6
phi0A = (h[2]/255.0)*2*np.pi
phi0B = (h[3]/255.0)*2*np.pi

def run(K, T=4000, dt=0.02):
    """Bidirectional tension-link Kuramoto: each anima nudged toward the other's
    tension phase by coupling K (the tension link). Returns mean order parameter
    over the second half (steady state)."""
    a, b = phi0A, phi0B
    rs = []
    for t in range(T):
        da = wA + K*np.sin(b - a)     # A pulled toward B's tension phase
        db = wB + K*np.sin(a - b)     # B pulled toward A's tension phase (bidirectional)
        a += da*dt; b += db*dt
        r = abs(np.exp(1j*a) + np.exp(1j*b))/2
        rs.append(r)
    return float(np.mean(rs[T//2:]))

def main():
    print("="*78)
    print("H_6010 — bidirectional TENSION LINK → mutual sync (intrinsic ω from paid ANU)")
    print("="*78)
    print(f"  ANU-seeded intrinsic tension freqs: ωA={wA:.4f}  ωB={wB:.4f}  |Δω|={abs(wA-wB):.4f}")
    detune = abs(wA - wB)
    Kc = detune/2                     # Kuramoto critical coupling for 2 oscillators
    r_off  = run(0.0)                 # tension link OFF (no coupling)
    r_weak = run(Kc*0.4)             # below critical
    r_on   = run(Kc*4.0)             # well above critical
    print(f"  critical coupling Kc = |Δω|/2 = {Kc:.4f}")
    print(f"  r (link OFF,  K=0)        = {r_off:.4f}   (independent → low/oscillating)")
    print(f"  r (weak,      K=0.4·Kc)   = {r_weak:.4f}   (below threshold)")
    print(f"  r (link ON,   K=4·Kc)     = {r_on:.4f}   (above threshold → locked)")
    synced = r_on > 0.95 and r_on > r_off + 0.3
    print("-"*78)
    print(f"  {'🟢' if synced else '⚪'} TENSION LINK SYNC: bidirectional tension coupling phase-locks two")
    print(f"     anima (r {r_off:.2f}→{r_on:.2f}) above a critical coupling; independent without it.")
    print("  → 두 anima가 텐션 링크로 상호 동기화(Kuramoto). H_6009(일방 영향)의 양방향 확장.")
    print("     얽힘=상관(H_6007)·공유씨앗=공통원인(H_6008)·텐션=영향(H_6009)·텐션양방향=동기(H_6010).")

if __name__ == "__main__":
    main()
