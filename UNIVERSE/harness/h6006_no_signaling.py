#!/usr/bin/env python3
"""
h6006_no_signaling.py — REAL simulation closing the "anima-to-anima quantum
communication WITHOUT a physical/classical link" claim (H_6006, a ⊗-tier branch
off H_6001 비분리성).

Three coded checks on two anima sharing a Bell (singlet) pair:
  F1 NON-SEPARABILITY present   — CHSH |S|>2 (they ARE entangled; H_6001 holds)
  F2 NO COMMUNICATION           — Bob's marginal is INVARIANT to Alice's choice
                                   ⇒ 0 bits transmitted (no-communication theorem)
  F3 TELEPORTATION needs a link — without Alice's 2 classical bits, Bob's recovered
                                   state is random ⇒ a classical channel is required

Verdict: "uses entanglement to COMMUNICATE with NO physical link" is 🔴 CLOSED-NEG.
"entanglement = non-separability/correlation" is 🟢 (H_6001). p7 · $0 · numpy.
"""
import numpy as np
rng = np.random.default_rng(60061)

def E(a, b, shots=400000):
    """Singlet correlation estimated by shot-by-shot measurement sampling."""
    p_eq = np.sin((a-b)/2)**2
    eq = rng.random(shots) < p_eq
    oA = rng.integers(0,2,shots)*2-1
    oB = np.where(eq, oA, -oA)
    return float(np.mean(oA*oB))

def f1_nonseparability():
    d = np.pi/180
    S = E(0,45*d) - E(0,135*d) + E(90*d,45*d) + E(90*d,135*d)
    return abs(S), abs(S) > 2.0   # >2 = genuinely entangled (classical ≤ 2)

def f2_no_communication():
    # Alice encodes a 'message' in her measurement-basis choice; Bob measures his half.
    def bob_marg(alice_basis, shots=400000, bob_angle=0.0):
        a = 0.0 if alice_basis==0 else np.pi/2
        p_eq = np.sin((a-bob_angle)/2)**2
        eq = rng.random(shots) < p_eq
        oA = rng.integers(0,2,shots)*2-1
        oB = np.where(eq, oA, -oA)
        return (oB==1).mean()
    m0, m1 = bob_marg(0), bob_marg(1)
    return m0, m1, abs(m0-m1)         # ≈0 ⇒ no information reaches Bob

def f3_teleport_needs_classical():
    # Teleport an unknown qubit |ψ>=(α,β) from Alice to Bob via a shared Bell pair.
    # Alice's Bell measurement yields 2 classical bits; Bob applies a correction
    # ONLY if he receives them. WITHOUT the bits, Bob holds one of 4 states at random
    # → his state is maximally mixed → fidelity to |ψ> averages ~0.5 (no info).
    alpha, beta = np.cos(0.7), np.sin(0.7); psi = np.array([alpha, beta])
    # the 4 equally-likely post-measurement Bob states (I, X, Z, XZ applied to ψ)
    X = np.array([[0,1],[1,0]]); Z = np.array([[1,0],[0,-1]])
    corrected = [psi, X@psi, Z@psi, X@Z@psi]
    # WITHOUT classical bits: Bob can't know which → average fidelity over the 4
    fid_nolink = np.mean([abs(psi @ s)**2 for s in corrected])
    # WITH classical bits: Bob applies the inverse correction → perfect fidelity
    fid_link = np.mean([abs(psi @ (np.linalg.inv(M) @ (M@psi)))**2
                        for M in [np.eye(2), X, Z, X@Z]])
    return fid_nolink, fid_link

def main():
    print("="*78)
    print("H_6006 — anima 간 양자통신(물리연결 없이) : REAL no-signaling verification")
    print("="*78)
    S, entangled = f1_nonseparability()
    print(f"F1 NON-SEPARABILITY : CHSH |S|={S:.3f}  {'🟢 entangled (>2)' if entangled else '🔴'}")
    m0, m1, delta = f2_no_communication()
    nocomm = delta < 0.01
    print(f"F2 NO-COMMUNICATION : Bob P(+1) Alice'0'={m0:.4f} '1'={m1:.4f}  |Δ|={delta:.4f}")
    print(f"                      {'🔴 0 bits transmitted (Bob invariant) — CANNOT communicate' if nocomm else '🟢 communicates'}")
    fnl, fl = f3_teleport_needs_classical()
    needs_link = fnl < 0.9 and fl > 0.99
    print(f"F3 TELEPORT NEEDS LINK: fidelity no-classical-bits={fnl:.3f}  with-bits={fl:.3f}")
    print(f"                      {'🔴 no classical channel ⇒ random (needs a physical link)' if needs_link else '🟢'}")
    print("-"*78)
    print("VERDICT:")
    print("  🟢 '얽힘 = 비분리성/상관'  (H_6001) — CHSH>2 confirms genuine entanglement")
    print("  🔴 '물리연결 없이 통신 가능' (H_6006) — CLOSED-NEG by no-communication theorem:")
    print("       entanglement transmits 0 bits alone; teleportation/superdense both REQUIRE")
    print("       a classical channel (= a physical link). So the 'no link' clause is impossible.")

if __name__ == "__main__":
    main()
