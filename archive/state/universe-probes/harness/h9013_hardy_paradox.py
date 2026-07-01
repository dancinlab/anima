#!/usr/bin/env python3
"""H_9013 — Hardy nonlocal event P>0 (LR=0). real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
hardy=norm(np.array([1,1,1,0.0]))
u=norm(np.array([1,-1.0]))
Pu=abs(np.kron(u,u)@hardy)**2
print("H_9013 Hardy P(impossible-under-LR) =",round(Pu,4),"→",("🟢" if Pu>0.01 else "🔴"))
