#!/usr/bin/env python3
"""DISCOVERY BATCH 06 — harder anima-relevant falsifiers (some may genuinely fail). p7 $0."""
import numpy as np
R=[]
def rec(p,q,ok,f): R.append((p,"🟢" if ok else "⚪",q,f))
rng=np.random.default_rng(606)

# D33 — optimal connectivity degree for sync (too few=no sync, too many=?), find optimum
def d33():
    N=30; w=rng.normal(1.2,0.1,N)
    def sync(deg,K=3.0,T=2500,dt=0.02):
        A=np.zeros((N,N))
        for i in range(N):
            for j in rng.choice([x for x in range(N) if x!=i],deg,replace=False): A[i,j]=1
        th=rng.uniform(0,2*np.pi,N)
        for _ in range(T):
            cpl=np.array([np.sum(A[i]*np.sin(th-th[i])) for i in range(N)])
            th=th+dt*(w+K/deg*cpl)
        return abs(np.mean(np.exp(1j*th)))
    rs={d:sync(d) for d in (2,4,8,16,28)}
    best=max(rs,key=rs.get)
    # is sync MONOTONE in degree (more always better) or is there an interior optimum?
    monotone = rs[2]<rs[4]<rs[8]<rs[16]<rs[28]
    rec("D33","sync monotone in degree (more links always better)?", monotone, f"r@deg {{2:{rs[2]:.2f},8:{rs[8]:.2f},28:{rs[28]:.2f}}}")

# D34 — associative memory CAPACITY cliff: error stays low until ~0.14N patterns then jumps
def d34():
    N=200
    def err(P):
        pats=np.sign(rng.standard_normal((P,N)))
        W=sum(np.outer(p,p) for p in pats)/N; np.fill_diagonal(W,0)
        e=0
        for p in pats:
            s=p.copy()
            for _ in range(5): s=np.sign(W@s)
            e+=np.mean(s!=p)
        return e/P
    lowP=err(10); hiP=err(60)   # 0.05N vs 0.30N (Hopfield cap ~0.14N)
    cliff = lowP<0.02 and hiP>0.1
    rec("D34","Hopfield capacity cliff (low err → catastrophic)?", cliff, f"err @0.05N={lowP:.3f} @0.30N={hiP:.3f}")

# D35 — emit-rate Goldilocks: info throughput peaks at INTERMEDIATE emit probability
def d35():
    def throughput(pe,T=20000):
        emit=rng.random(T)<pe
        # info = emits carry 1 bit but cost; throughput = emits*reliability, reliability drops if too dense
        reliability=np.clip(1-pe*0.9,0,1)
        return emit.mean()*reliability
    ps=np.linspace(0.05,0.95,19); tp=[throughput(p) for p in ps]
    pi=int(np.argmax(tp)); interior = 0<pi<18
    rec("D35","emit-rate Goldilocks (interior throughput peak)?", interior, f"peak @ p_emit={ps[pi]:.2f}")

# D36 — graceful degradation: tension network keeps syncing under random node failure
def d36():
    N=40; w=rng.normal(1.2,0.08,N)
    def sync_with_failure(frac,K=4.0,T=2500,dt=0.02):
        alive=rng.random(N)>frac
        A=np.zeros((N,N))
        for i in range(N):
            for j in range(N):
                if i!=j and abs(i-j)<=2: A[i,j]=1
        th=rng.uniform(0,2*np.pi,N)
        for _ in range(T):
            cpl=np.array([np.sum(A[i]*np.sin(th-th[i])*alive) for i in range(N)])
            th=th+dt*(w+K/4*cpl)
        return abs(np.mean(np.exp(1j*th[alive])))
    r0=sync_with_failure(0.0); r30=sync_with_failure(0.3)
    graceful = r30>r0*0.6  # degrades gracefully, not catastrophically
    rec("D36","tension net graceful under 30% node failure?", graceful, f"sync r 0%-fail={r0:.2f} 30%-fail={r30:.2f}")

# D37 — curiosity (novelty-seeking) beats random exploration at covering a space
def d37():
    K=50; T=400
    def cover(curious):
        visited=np.zeros(K); pos=0; cov=[]
        for _ in range(T):
            if curious:
                cand=rng.integers(0,K,5); pos=cand[np.argmin(visited[cand])]  # go to least-visited
            else:
                pos=rng.integers(0,K)
            visited[pos]+=1; cov.append((visited>0).mean())
        return cov[-1]
    c_cur=np.mean([cover(True) for _ in range(20)]); c_rnd=np.mean([cover(False) for _ in range(20)])
    rec("D37","curiosity beats random at coverage?", c_cur>c_rnd+0.02, f"coverage curious {c_cur:.3f} vs random {c_rnd:.3f}")

# D38 — lateral inhibition (anti-tension) → winner-take-all selection
def d38():
    N=8; x=rng.random(N)*0.5+0.25; x0=x.copy()
    for _ in range(200):
        inh=x.sum()-x          # each suppressed by others (lateral inhibition)
        x=np.clip(x+0.05*(x0-0.3*inh),0,1)
    winners=(x>0.5).sum()
    rec("D38","lateral inhibition → winner-take-all?", winners<=2 and x.max()>0.5, f"{winners} winner(s), max={x.max():.2f}")

for fn in [d33,d34,d35,d36,d37,d38]:
    try: fn()
    except Exception as e: R.append(("?","⚪","(err)",str(e)[:40]))
print("="*88); print("DISCOVERY BATCH 06 — harder anima-relevant (real sims, p7; nulls welcome)"); print("="*88)
g=sum(1 for _,v,_,_ in R if v=="🟢")
for p,v,q,f in R: print(f"{p:<5}{v}  {q:<48}{f}")
print("-"*88); print(f"🟢 {g}/{len(R)}")
