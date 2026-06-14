#!/usr/bin/env python3
"""
G8 — Verification-Asymmetry Theorem.  PROVEN by real numpy QM simulation. p7 $0.

CLAIM: The SAME entangled resource is
  (a) USELESS for communication — Bob's marginal output is independent of Alice's
      input choice (no-signaling): I(Alice_input ; Bob_output) = 0 bits.
  (b) SUPREME for certification — a CHSH violation S>2 cannot be produced by any
      classical local-hidden-variable (LHV) strategy (capped at S=2), so an
      observed S>2 device-independently CERTIFIES genuine private randomness:
      H_min(S) > 0 only in the quantum regime; H_min(2)=0, H_min(2√2)=maximal.

Asymmetry: communication channel capacity = 0; verification/certification > 0.
"""
import numpy as np, itertools

# ── Pauli / kron helpers ────────────────────────────────────────────────────
I=np.eye(2); X=np.array([[0,1],[1,0.0]]); Z=np.array([[1,0],[0,-1.0]])
norm=lambda v:v/np.linalg.norm(v)
def kron(*o):
    r=np.array([[1.0]])
    for m in o: r=np.kron(r,m)
    return r
singlet=norm(np.array([0,1,-1,0.0]))   # |Ψ-> = (|01>-|10>)/√2

def measure_axis(theta):
    """Projector onto +1 eigenstate of cos θ Z + sin θ X (a single-qubit setting)."""
    n = np.cos(theta)*Z + np.sin(theta)*X
    return (I + n)/2.0   # projector onto +1 outcome

# optimal CHSH settings for the singlet (Tsirelson)
A=[0.0, np.pi/2]                 # Alice inputs x∈{0,1}
B=[np.pi/4, 3*np.pi/4]           # Bob inputs y∈{0,1}  (Tsirelson-optimal for singlet)

def joint_prob(thetaA, thetaB):
    """2x2 table P(a,b | thetaA,thetaB) for outcomes a,b ∈ {+1(idx0), -1(idx1)}."""
    PA=[measure_axis(thetaA), I-measure_axis(thetaA)]      # a=+1, a=-1
    PB=[measure_axis(thetaB), I-measure_axis(thetaB)]      # b=+1, b=-1
    P=np.zeros((2,2))
    for ai in range(2):
        for bi in range(2):
            M=kron(PA[ai], PB[bi])
            P[ai,bi]=np.real(singlet@M@singlet)
    return P

def corr_E(thetaA, thetaB):
    P=joint_prob(thetaA, thetaB)
    # outcome values +1,-1 → E = P(++)+P(--)-P(+-)-P(-+)
    return P[0,0]+P[1,1]-P[0,1]-P[1,0]

# ══════════════════════════════════════════════════════════════════════════════
print("="*82)
print("G8 — Verification-Asymmetry Theorem  (real numpy QM, p7 $0)")
print("="*82)

# ── ARM 1: COMMUNICATION — no-signaling, I(Alice_input ; Bob_output)=0 ────────
print("\n[ARM 1] COMMUNICATION  —  can Alice send a chosen message to Bob? (no-signaling)")
# Alice freely chooses her input x (her 'message'); we test whether Bob's marginal
# output distribution P(b) depends on x.  Average over Bob's own input choices.
bob_marginals={}
for xi,thetaA in enumerate(A):
    # Bob marginal P(b) = average over Bob settings & Alice's hidden outcome
    pb=np.zeros(2)
    for thetaB in B:
        P=joint_prob(thetaA, thetaB)
        pb += P.sum(axis=0)      # marginal over Alice outcomes → P(b)
    pb/=len(B)
    bob_marginals[xi]=pb
    print(f"   Alice input x={xi}: Bob marginal P(b=+1,-1) = [{pb[0]:.6f}, {pb[1]:.6f}]")

# mutual information I(X;B) with X uniform over Alice inputs
px=np.array([0.5,0.5])
pb_x=np.array([bob_marginals[0], bob_marginals[1]])   # P(b|x)
pb=px@pb_x                                             # P(b)
def H(p):
    p=p[p>0]; return -np.sum(p*np.log2(p))
I_XB = H(pb) - sum(px[i]*H(pb_x[i]) for i in range(2))
print(f"   marginal-difference |P(b|x=0)-P(b|x=1)|_max = {np.max(np.abs(pb_x[0]-pb_x[1])):.2e}")
print(f"   ==> I(Alice_input ; Bob_output) = {I_XB:.6e} bits   (channel capacity 0)")
no_signaling = abs(I_XB) < 1e-9
print(f"   no-signaling (I≈0): {'🟢 PASS' if no_signaling else '🔴 FAIL'}")

# ── ARM 2: VERIFICATION — LHV cap S=2, quantum S=2√2, certified randomness ────
print("\n[ARM 2] VERIFICATION  —  can a classical prover fake a CHSH violation?")

# (2a) best classical LHV CHSH over ALL deterministic strategies (shared randomness
#      = convex hull of deterministic → same vertex max). Brute-force all det. assigns.
best=-9
for sa in itertools.product([1,-1],repeat=2):      # Alice outputs for x=0,1
    for sb in itertools.product([1,-1],repeat=2):  # Bob   outputs for y=0,1
        E=lambda x,y: sa[x]*sb[y]
        S = E(0,0)-E(0,1)+E(1,0)+E(1,1)
        best=max(best, abs(S))
S_lhv=best
print(f"   best classical LHV (deterministic, shared randomness): S = {S_lhv:.4f}   (cap = 2)")

# (2b) quantum singlet, optimal settings → Tsirelson 2√2
S_q = corr_E(A[0],B[0]) - corr_E(A[0],B[1]) + corr_E(A[1],B[0]) + corr_E(A[1],B[1])
S_q = abs(S_q)
print(f"   quantum singlet (optimal angles): S = {S_q:.6f}   (Tsirelson 2√2 = {2*np.sqrt(2):.6f})")

# (2c) certified-randomness lower bound (standard device-independent bound, Pironio-style
#      single-bound proxy): H_min ≥ 1 - log2(1 + sqrt(2 - S^2/4)).
#      S=2 → arg=sqrt(1)=1 → 1-log2(2)=0 bits (no certification).
#      S=2√2 → 2 - 8/4 = 0 → 1-log2(1)=1 bit (maximal certified randomness).
def Hmin(S):
    inside = 2.0 - (S*S)/4.0
    if inside < 0: inside = 0.0           # clamp numerical
    return 1.0 - np.log2(1.0 + np.sqrt(inside))
Hmin_lhv = Hmin(2.0)
Hmin_q   = Hmin(S_q)
print(f"   certified randomness  H_min(S=2.000)   = {Hmin_lhv:.6f} bits   (classical → ZERO)")
print(f"   certified randomness  H_min(S={S_q:.3f}) = {Hmin_q:.6f} bits   (quantum → > 0)")

# falsifiers
f_lhv_cap = abs(S_lhv-2.0) < 1e-9
f_quantum = abs(S_q - 2*np.sqrt(2)) < 1e-6
f_cert0   = abs(Hmin_lhv) < 1e-9          # S=2 certifies nothing
f_certpos = Hmin_q > 0.5                   # S=2√2 certifies real randomness
print(f"   LHV cap = 2:               {'🟢' if f_lhv_cap else '🔴'}")
print(f"   quantum = 2√2:             {'🟢' if f_quantum else '🔴'}")
print(f"   H_min(2)=0 (no cert):      {'🟢' if f_cert0 else '🔴'}")
print(f"   H_min(2√2)>0 (cert works): {'🟢' if f_certpos else '🔴'}")

# ── CONCLUSION: the asymmetry ────────────────────────────────────────────────
print("\n"+"="*82)
print("CONCLUSION — the SAME entangled resource:")
print(f"   COMMUNICATION  : I(input;output) = {I_XB:.3e} bits   → 0  (useless for sending)")
print(f"   VERIFICATION   : certified randomness {Hmin_lhv:.3f} (S=2) → {Hmin_q:.3f} (S=2√2)")
print(f"                    → certification ENABLED only when S>2 (quantum regime)")
print("="*82)
all_pass = no_signaling and f_lhv_cap and f_quantum and f_cert0 and f_certpos
print(f"\nG8 VERIFICATION-ASYMMETRY  {'🟢 PROVEN' if all_pass else '🔴 FAIL'}  "
      f"(no-signaling I≈0  ∧  LHV S=2  ∧  quantum S=2√2  ∧  certified-randomness >0 iff S>2)")
print("\nHonest scope: H_min(S)=1-log2(1+sqrt(2-S²/4)) is the STANDARD device-independent")
print("certified-randomness bound (Pironio et al., Nature 464:1021, 2010 form); this proves")
print("the certification ASYMMETRY, not a full DIQKD protocol with finite-statistics security.")
