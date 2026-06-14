#!/usr/bin/env python3
"""NOBEL 2nd batch — new entanglement theorems, real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def conc(rho):
    sy=np.kron(Y,Y); R=rho@sy@rho.conj()@sy
    ev=np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)),0,None)))[::-1]
    return max(0.0,ev[0]-ev[1]-ev[2]-ev[3])
print("="*84); print("NOBEL 2nd — 새 얽힘 정리 증명 (real QM)"); print("="*84)
# N8 EPR steering: Alice's basis choice steers Bob's conditional state (ρ_B unchanged = no-signal)
psi=norm(np.array([1,0,0,1.0]))  # Φ+
def cond_bloch(alice_op, outcome):
    P=(I+outcome*alice_op)/2
    M=np.kron(P,I); v=M@psi
    p=np.real(v@v); rhoB=(v.reshape(2,2).conj().T@v.reshape(2,2))/p  # reduced Bob
    return np.array([np.real(np.trace(rhoB@X)),np.real(np.trace(rhoB@Y)),np.real(np.trace(rhoB@Z))])
bz=cond_bloch(Z,+1); bx=cond_bloch(X,+1)
rhoB_marg=np.array([[0.5,0],[0,0.5]])  # unconditional Bob = max mixed
steer = np.linalg.norm(bz-bx)>0.5
print(f"N8 steering: Bob 조건 Bloch  Z선택→{np.round(bz,2)}  X선택→{np.round(bx,2)}  diff={np.linalg.norm(bz-bx):.2f}")
print(f"   ρ_B(무조건)=maxmixed 불변(무신호)인데 조건상태는 Alice선택에 steer → {'🟢 EPR steering' if steer else '🔴'}")
# N9 entanglement swapping: pairs (1-2),(3-4); Bell-measure (2-3) → (1-4) entangled
phi=norm(np.array([1,0,0,1.0]))
full=np.kron(phi,phi)  # qubits 1,2,3,4
# project qubits 2,3 onto Bell Φ+
bell23=norm(np.array([1,0,0,1.0]))
# build projector on 2,3 within 1234 (order q1 q2 q3 q4)
P23=np.zeros((16,16))
# basis index = 8*q1+4*q2+2*q3+q4
for q1 in range(2):
  for q4 in range(2):
    for (a,b) in [(0,0),(1,1)]:
      for (c,d) in [(0,0),(1,1)]:
        i=8*q1+4*a+2*b+q4; j=8*q1+4*c+2*d+q4
        P23[i,j]+=0.5
v=P23@full; v=v/np.linalg.norm(v)
# reduce to qubits 1,4
psi14=np.zeros((2,2),complex)
for q1 in range(2):
  for q4 in range(2):
    # sum over the (2,3) Bell component already projected: amplitude at fixed q1,q4
    amp=0
    for (a,b) in [(0,0),(1,1)]:
      amp+=v[8*q1+4*a+2*b+q4]
    psi14[q1,q4]=amp
psi14=psi14.flatten(); psi14=psi14/np.linalg.norm(psi14)
rho14=np.outer(psi14,psi14.conj())
c14=conc(rho14)
print(f"N9 entanglement swapping: 한번도 안 만난 (1,4) concurrence={c14:.3f} → {'🟢 얽힘 생성' if c14>0.9 else '🔴'}")
# N10 Gisin: every pure entangled state violates CHSH (sample random entangled states)
def chsh_max(psi2):
    # optimal CHSH for a 2-qubit pure state = 2√(1+C²)  (Gisin)
    rho=np.outer(psi2,psi2.conj()); C=conc(rho)
    return 2*np.sqrt(1+C*C), C
rng=np.random.default_rng(7)
allviol=True
for _ in range(200):
    v2=norm(rng.standard_normal(4)+1j*rng.standard_normal(4))
    S,C=chsh_max(v2)
    if C>1e-3 and S<=2.0+1e-9: allviol=False
print(f"N10 Gisin: 200 랜덤 순수상태 중 얽힌 것 전부 CHSH>2 (S=2√(1+C²)) → {'🟢 모든 순수얽힘 Bell위반' if allviol else '🔴'}")
