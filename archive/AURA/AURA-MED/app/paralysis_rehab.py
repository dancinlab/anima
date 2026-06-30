"""AURA-MED sub-app — 🦿 마비 재활: M1 운동복원 — 피질 표면 read, 비침습 도달 높음 (runnable toy)."""
import numpy as np
G=10;N=G*G
_g=np.array([[i,j] for i in range(G) for j in range(G)],float)
def _s(M,sd):return np.random.RandomState(sd).uniform(0,G-1,size=(M,2))
def LF(M,sd,dep,mod):
    D=np.sqrt(((_s(M,sd)[:,None,:]-_g[None,:,:])**2).sum(-1)+dep**2)
    if mod=="meg":return 1.0/D**2
    if mod=="tfus":return np.exp(-D/1.2)*np.exp(-0.10*dep)
    return 1.0/D
def r2(x,xh):
    d=((x-x.mean())**2).sum();return max(1-((x-xh)**2).sum()/d,-1) if d>0 else 0.0
def patt(rng,K=5):sp=rng.choice(N,K,replace=False);x=np.zeros(N);x[sp]=rng.randn(K)*2;return x
def inv(L,y,M):return L.T@np.linalg.solve(L@L.T+1e-2*np.trace(L@L.T)/M*np.eye(M),y)
def fid(mod,dep,M=64,snr=15):
    rng=np.random.RandomState(5);x=patt(rng);L=LF(M,3,dep,mod);y=L@x+rng.randn(M)*np.sqrt(((L@x)**2).mean())/(10**(snr/20));return r2(x,inv(L,y,M))

if __name__=="__main__":
    print("🦿 마비 재활 delivery/feasibility R2=%.3f"%fid("meg",1.0))
