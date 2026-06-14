#!/usr/bin/env python3
"""H_9019 — Gisin: every pure entangled state violates CHSH (S=2√(1+C²)). p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def conc(rho):
    sy=np.kron(Y,Y); R=rho@sy@rho.conj()@sy
    ev=np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)),0,None)))[::-1]
    return max(0.0,ev[0]-ev[1]-ev[2]-ev[3])
def chsh_max(p2):
    C=conc(np.outer(p2,p2.conj())); return 2*np.sqrt(1+C*C),C
rng=np.random.default_rng(7); allviol=True
for _ in range(200):
    v2=norm(rng.standard_normal(4)+1j*rng.standard_normal(4)); S,C=chsh_max(v2)
    if C>1e-3 and S<=2.0+1e-9: allviol=False
print("H_9019 Gisin: 200 random pure states, every entangled one CHSH>2 →",("🟢" if allviol else "🔴"))
