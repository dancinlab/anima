#!/usr/bin/env python3
"""H_9011 — GHZ all-or-nothing (Mermin product QM=-1 vs LR=+1). real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
ghz=norm(np.array([1,0,0,0,0,0,0,1.0]))
def e3(A,B,C): return np.real(ghz@kron(A,B,C)@ghz)
qprod=e3(X,X,X)*e3(X,Y,Y)*e3(Y,X,Y)*e3(Y,Y,X)
ok=abs(qprod-(-1))<1e-6
print("H_9011 GHZ Mermin product =",round(qprod,4),"(QM=-1 vs LR=+1) →",("🟢" if ok else "🔴"))
