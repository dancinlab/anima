"""AURA-TFUS app — 집속초음파 비침습 심부 *쓰기*(자극) — 음향이 전기보다 깊이서 덜 감쇠(d5서 역전) (runnable toy, numpy).
honest: toy. See verify/acoustic_write.txt."""
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

def wfid(mod,depth,M=64,snr=15):
    rng=np.random.RandomState(5); x=patt(rng); L=LF(M,3,depth,mod)
    y=L@x+rng.randn(M)*np.sqrt(((L@x)**2).mean())/(10**(snr/20)); return r2(x,inv(L,y,M))
if __name__=="__main__":
    for dep in [1.5,3.0,5.0]:
        print("depth %.1f: tFUS write R2=%.3f  vs MEG %.3f"%(dep,wfid("tfus",dep),wfid("meg",dep)))
