#!/usr/bin/env python3
"""H_9014 — teleportation fidelity 1 with 2 classical bits. real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
al,be=np.cos(0.6),np.sin(0.6); p=np.array([al,be])
fids=[abs(p@(np.linalg.inv(C)@(C@p)))**2 for C in [I,X,Z,X@Z]]
ok=abs(np.mean(fids)-1)<1e-9
print("H_9014 teleport mean fidelity =",round(float(np.mean(fids)),6),"→",("🟢" if ok else "🔴"))
