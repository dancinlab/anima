#!/usr/bin/env python3
"""H_9012 — Peres–Mermin magic square (rows +I, ∏cols -1). real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
O=[[kron(X,I),kron(I,X),kron(X,X)],[kron(I,Z),kron(Z,I),kron(Z,Z)],[kron(X,Z),kron(Z,X),kron(Y,Y)]]
def prod(ms):
    r=np.eye(4)
    for m in ms: r=r@m
    return r
rows_ok=all(np.allclose(prod(O[i]),np.eye(4)) for i in range(3))
csign=[(1 if np.allclose(prod([O[0][j],O[1][j],O[2][j]]),np.eye(4)) else -1) for j in range(3)]
contr=rows_ok and (int(np.prod(csign))==-1)
print("H_9012 Peres-Mermin: rows=+I",rows_ok,"∏cols=",int(np.prod(csign)),"contradiction →",("🟢" if contr else "🔴"))
