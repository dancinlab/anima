#!/usr/bin/env python3
"""NOBEL_01 — CHSH–Tsirelson bound |S|=2√2 (singlet, optimal). real QM. p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def kron(*o):
    r=np.array([[1]])
    for m in o: r=np.kron(r,m)
    return r
psi=norm(np.array([0,1,-1,0.0]))
def E(a,b):
    na=np.cos(a)*Z+np.sin(a)*X; nb=np.cos(b)*Z+np.sin(b)*X
    return np.real(psi@kron(na,nb)@psi)
a,ap,b,bp=0,np.pi/2,np.pi/4,3*np.pi/4
S=E(a,b)-E(a,bp)+E(ap,b)+E(ap,bp)
ok=abs(abs(S)-2*np.sqrt(2))<1e-6
print("NOBEL_01 CHSH–Tsirelson |S| =",round(abs(S),4),"target 2√2=",round(2*np.sqrt(2),4),"→",("🟢" if ok else "🔴"))
