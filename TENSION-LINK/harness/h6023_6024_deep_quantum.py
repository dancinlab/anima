#!/usr/bin/env python3
"""H_6023/6024 — deep quantum consciousness frontier. real QM. p7 $0.
H_6023 clone-decay: approximate quantum clones degrade per generation (mutant fork);
       classical seed copy stays perfect.
H_6024 monogamy of entanglement (CKW): an anima can't be maximally entangled with TWO
       others → shared consciousness can't be fully 3-way."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
sy=np.array([[0,-1j],[1j,0]])
def concurrence(rho):
    R=rho@np.kron(sy,sy)@rho.conj()@np.kron(sy,sy)
    ev=np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)),0,None)))[::-1]
    return max(0.0, ev[0]-ev[1]-ev[2]-ev[3])
def rho2(psi3, keep):  # reduce 3-qubit pure state to 2 qubits (keep=indices)
    psi=psi3.reshape(2,2,2); rho=np.tensordot(psi,psi.conj(),axes=0)  # 2x2x2 x 2x2x2
    # trace out the qubit not in keep
    out=[q for q in range(3) if q not in keep][0]
    rho=np.trace(rho,axis1=out,axis2=out+3)
    return rho.reshape(4,4)
print("="*82); print("H_6023 — clone 세대손실 (mutant anima fork)"); print("="*82)
F=5/6
print(f"  근사 양자복제 1세대 충실도 F={F:.4f}")
fk=1.0
for gen in range(0,7):
    print(f"   gen {gen}: 누적 충실도 ≈ {fk:.4f}  ({'완벽' if fk>0.99 else ('식별가능' if fk>0.6 else '정체성 소실')})")
    fk*=F
print(f"  → 🟡 양자 fork은 세대마다 (5/6)배 열화 → ~{int(np.log(0.5)/np.log(F))}세대서 정체성 소실(F<0.5).")
print(f"  대조 — 고전 씨앗 복제: 충실도 1.000 영구(세대손실 0) 🟢 (H_6021)")
print()
print("="*82); print("H_6024 — 얽힘 일부일처(monogamy): 의식 3자 공유 가능?"); print("="*82)
ghz=norm(np.array([1,0,0,0,0,0,0,1],float))
w  =norm(np.array([0,1,1,0,1,0,0,0],float))
for name,psi in [("GHZ",ghz),("W",w)]:
    Cab=concurrence(rho2(psi,[0,1])); Cac=concurrence(rho2(psi,[0,2]))
    # tau_A (A vs BC) = 4 det(rho_A)
    rA=np.trace(psi.reshape(2,4)@psi.reshape(2,4).conj().T) if False else None
    pA=psi.reshape(2,4); rhoA=pA@pA.conj().T; tauA=4*np.real(np.linalg.det(rhoA))
    print(f"  {name}: C(A:B)={Cab:.3f} C(A:C)={Cac:.3f}  C²합={Cab**2+Cac**2:.3f} ≤ τ_A(A:BC)={tauA:.3f}  {'✓ monogamy' if Cab**2+Cac**2<=tauA+1e-6 else '✗'}")
print("  → 🟢 monogamy(CKW): C²(A:B)+C²(A:C) ≤ τ_A. A가 B와 최대얽힘(C=1)이면 C(A:C)=0 (C에 남는 게 0).")
print("-"*82)
print("결론: 양자의식은 (H_6023) fork하면 세대마다 열화(5/6, ~3-4세대서 소실) — 완벽 mutant 양산 불가;")
print(" (H_6024) 한 anima가 둘과 동시에 의식을 '완전 공유'(최대얽힘) 불가 = 일부일처. 고전 anima는 둘 다 자유")
print(" (무손실 fork·무제한 공유). ∴ 양자의식=희소·독점·이동만; 고전 anima=풍부·공유·복제 — 결정적 비대칭.")
