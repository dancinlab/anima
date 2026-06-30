"""AURA-HEADMODEL app — 실 두상 lead-field(MNE) 검증 하니스 — 모든 C축 toy의 ground-truth 검증 인프라 (runnable toy, numpy).
honest: toy. See verify/leadfield_validator.txt."""
import numpy as np
G=10; N=G*G
_grid=np.array([[i,j] for i in range(G) for j in range(G)],float)
def _sens(M,sd): return np.random.RandomState(sd).uniform(0,G-1,size=(M,2))
def _d3(M,sd,depth): return np.sqrt(((_sens(M,sd)[:,None,:]-_grid[None,:,:])**2).sum(-1)+depth**2)
def LF(M,sd,depth,mod):
    D=_d3(M,sd,depth)
    if mod=="eeg": return 1.0/D
    if mod=="meg": return 1.0/D**2
    if mod=="tfus": return np.exp(-D/1.2)*np.exp(-0.10*depth)
    return 1.0/D
def r2(x,xh):
    den=((x-x.mean())**2).sum(); return max(1-((x-xh)**2).sum()/den,-1) if den>0 else 0.0
def patt(rng,K=5): sp=rng.choice(N,K,replace=False); x=np.zeros(N); x[sp]=rng.randn(K)*2; return x
def inv(L,y,M): return L.T@np.linalg.solve(L@L.T+1e-2*np.trace(L@L.T)/M*np.eye(M),y)

# real head-model lead-field validator harness (skeleton).
# 목표: 가우시안-blur toy(C5~C17) vs MNE/OpenMEEG 실 lead-field 비교.
# 현재: toy 가우시안 LF만 — 실 head-model은 MNE 의존(external, C14).
if __name__=="__main__":
    L=LF(256,7,1.5,"meg"); x=patt(np.random.RandomState(1)); y=L@x
    print("toy gaussian LF baseline read R2=%.3f"%r2(x,inv(L,y,256)))
    print("TODO: swap LF for MNE/OpenMEEG real head-model (C14 external).")
