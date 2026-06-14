#!/usr/bin/env python3
"""H_9018 — entanglement swapping: Bell-measure (2,3) entangles never-met (1,4). p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def conc(rho):
    sy=np.kron(Y,Y); R=rho@sy@rho.conj()@sy
    ev=np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)),0,None)))[::-1]
    return max(0.0,ev[0]-ev[1]-ev[2]-ev[3])
phi=norm(np.array([1,0,0,1.0])); full=np.kron(phi,phi)
P23=np.zeros((16,16))
for q1 in range(2):
  for q4 in range(2):
    for (a,b) in [(0,0),(1,1)]:
      for (c,d) in [(0,0),(1,1)]:
        P23[8*q1+4*a+2*b+q4,8*q1+4*c+2*d+q4]+=0.5
v=P23@full; v=v/np.linalg.norm(v)
psi14=np.zeros((2,2),complex)
for q1 in range(2):
  for q4 in range(2):
    psi14[q1,q4]=sum(v[8*q1+4*a+2*b+q4] for (a,b) in [(0,0),(1,1)])
psi14=psi14.flatten(); psi14=psi14/np.linalg.norm(psi14)
c14=conc(np.outer(psi14,psi14.conj()))
print("H_9018 entanglement swapping: (1,4) concurrence =",round(float(c14),3),"→",("🟢" if c14>0.9 else "🔴"))
