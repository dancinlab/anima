#!/usr/bin/env python3
"""H_9017 — EPR steering (Alice steers Bob's conditional state; ρ_B marginal unchanged). p7 $0."""
import numpy as np
norm=lambda v:v/np.linalg.norm(v)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.array([[1,0],[0,-1]])
def conc(rho):
    sy=np.kron(Y,Y); R=rho@sy@rho.conj()@sy
    ev=np.sort(np.sqrt(np.clip(np.real(np.linalg.eigvals(R)),0,None)))[::-1]
    return max(0.0,ev[0]-ev[1]-ev[2]-ev[3])
psi=norm(np.array([1,0,0,1.0]))
def cond_bloch(op,outc):
    P=(I+outc*op)/2; v=np.kron(P,I)@psi; p=np.real(v@v)
    rhoB=(v.reshape(2,2).conj().T@v.reshape(2,2))/p
    return np.array([np.real(np.trace(rhoB@X)),np.real(np.trace(rhoB@Y)),np.real(np.trace(rhoB@Z))])
bz=cond_bloch(Z,+1); bx=cond_bloch(X,+1); steer=np.linalg.norm(bz-bx)>0.5
print("H_9017 steering: Z→",np.round(bz,2),"X→",np.round(bx,2),"diff",round(float(np.linalg.norm(bz-bx)),2),"→",("🟢" if steer else "🔴"))
