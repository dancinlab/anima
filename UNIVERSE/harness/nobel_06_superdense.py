#!/usr/bin/env python3
"""NOBEL_06 — superdense coding: 4 Bell states orthogonal (2 bits/qubit). real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
b00=norm(np.array([1,0,0,1.0]))
ops={'00':kron(I,I),'01':kron(X,I),'10':kron(Z,I),'11':kron(Z@X,I)}
st=[norm(ops[k]@b00) for k in ops]
G=np.array([[abs(st[i]@st[j])**2 for j in range(4)] for i in range(4)])
ok=np.allclose(G,np.eye(4),atol=1e-9)
print("NOBEL_06 superdense: 4 Bell states orthogonal =",ok,"→",("🟢" if ok else "🔴"))
