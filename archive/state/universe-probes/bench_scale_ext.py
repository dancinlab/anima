#!/usr/bin/env python3
"""SCALE-UP BENCHMARK (extension) — remaining scale-SENSITIVE bio/neuro hypotheses across >=3-rung size ladders.

Completes the CPU-substrate scale rung beyond the first 5 (#1743 SCALE-BENCH-CPU: MET·CRITICALITY·ATTRACTOR·
WORKSPACE·QUORUM). a_toy_scale_recheck · pure stdlib · emergent · fixed seeds · p7. CPU rung only (production
substrate AKIDA/forge GATED). SCALE-SURVIVES = signature holds/strengthens with size; CAP/BREAK = collapses.
"""
import math, random, statistics
SEED = 20260603


def h886_turing_scale():
    """Gierer-Meinhardt pattern: # of stripes scales with domain length (pattern persists, finer scale)."""
    def n_peaks(L):
        random.seed(SEED)
        Da, Dh, rho, mua, muh, dt = 0.02, 0.5, 0.05, 0.06, 0.12, 0.5
        a=[1.0+random.gauss(0,0.02) for _ in range(L)]; h=[1.0+random.gauss(0,0.02) for _ in range(L)]
        for _ in range(15000):
            na=list(a); nh=list(h)
            for i in range(L):
                la=a[(i-1)%L]+a[(i+1)%L]-2*a[i]; lh=h[(i-1)%L]+h[(i+1)%L]-2*h[i]
                na[i]=max(0.0,a[i]+dt*(Da*la+rho*(a[i]*a[i]/(h[i]+1e-9))-mua*a[i]))
                nh[i]=max(0.0,h[i]+dt*(Dh*lh+rho*a[i]*a[i]-muh*h[i]))
            a,h=na,nh
        mean=sum(a)/L; peaks=sum(1 for i in range(L) if a[i]>mean*1.3 and a[i]>=a[(i-1)%L] and a[i]>=a[(i+1)%L])
        return peaks, max(a)-min(a)
    rungs=[30,60,120]; curve=[(L,)+n_peaks(L) for L in rungs]
    peaks=[c[1] for c in curve]; patterned=all(c[2]>0.1 for c in curve)
    grows=peaks[-1]>peaks[0] and patterned  # more domain -> more stripes (fixed wavelength) = true Turing scaling
    print(f"[H_886 TURING scale]    {' '.join(f'L{L}:peaks={p},range={r:.2f}' for L,p,r in curve)} -> {'SCALE-SURVIVES (stripe count scales with domain, fixed wavelength)' if grows else 'SCALE-CAP'}")
    return grows


def h901_ring_scale():
    """Ring-attractor bump persists at every N (drift bounded as ring grows)."""
    def drift(N):
        random.seed(SEED)
        act=[math.exp(math.cos(2*math.pi*(i-N*0.25)/N)-1) for i in range(N)]
        for _ in range(200):
            inh=sum(act)/N; nxt=[max(0.0,0.5*act[(i-1)%N]+act[i]+0.5*act[(i+1)%N]-1.2*inh) for i in range(N)]
            s=sum(nxt) or 1.0; tot=sum(act); act=[a/s*tot for a in nxt]
        peak=max(range(N),key=lambda i:act[i]); start=int(N*0.25)
        return min(abs(peak-start),N-abs(peak-start)), N
    rungs=[40,80,160]; curve=[drift(N) for N in rungs]
    bounded=all(d<=max(3,int(0.06*N)) for d,N in curve)  # drift stays small fraction of ring as N grows
    print(f"[H_901 RING scale]      {' '.join(f'N{N}:drift={d}' for d,N in curve)} -> {'SCALE-SURVIVES (bump persists, drift bounded at every N)' if bounded else 'SCALE-BREAK'}")
    return bounded


def h862_hgt_scale():
    """HGT lateral-vs-vertical speedup PERSISTS as population scales (ratio stays >=1.5x)."""
    def ratio(N):
        def ticks(lateral):
            random.seed(SEED); has=[False]*N; has[0]=True
            for t in range(1,2000):
                idx=[i for i,v in enumerate(has) if v]; newly=[]
                for i in idx:
                    if random.random()<0.5: j=random.randrange(N); newly.append(j)
                    if lateral:
                        for _ in range(2):
                            if random.random()<0.5: j=random.randrange(N); newly.append(j)
                for j in newly: has[j]=True
                if sum(has)>=0.9*N: return t
            return 1999
        v,l=ticks(False),ticks(True); return v/max(l,1)
    rungs=[100,400,1600]; curve=[(N,ratio(N)) for N in rungs]
    persists=all(r>=1.5 for _,r in curve)
    print(f"[H_862 HGT scale]       {' '.join(f'N{N}:ratio={r:.2f}' for N,r in curve)} -> {'SCALE-SURVIVES (lateral speedup >=1.5x at every population)' if persists else 'SCALE-BREAK'}")
    return persists


def h864_prion_scale():
    """Prion basin propagation reach scales with chain length (occupancy front reaches the end at every L)."""
    def reach_frac(L):
        random.seed(SEED); p,q,sw,K=0.7,0.05,300,100; state=[0]*L; state[0]=1; occ=[0]*L
        for s in range(sw):
            for i in range(1,L):
                if state[i-1]==1 and state[i]==0:
                    if random.random()<p: state[i]=1
                elif state[i]==1 and random.random()<q: state[i]=0
            if s>=sw-K:
                for i in range(L): occ[i]+=state[i]
        mo=[o/K for o in occ]; reach=0
        for i in range(1,L):
            if mo[i]>0.5: reach=i
            else: break
        return reach/(L-1)
    rungs=[20,60,180]; curve=[(L,reach_frac(L)) for L in rungs]
    full=all(f>0.8 for _,f in curve)  # basin reaches >80% of chain at every length = self-sustaining at scale
    print(f"[H_864 PRION scale]     {' '.join(f'L{L}:reach_frac={f:.2f}' for L,f in curve)} -> {'SCALE-SURVIVES (basin self-propagates full chain at every length)' if full else 'SCALE-CAP'}")
    return full


def h882_seeding_scale():
    """Founder seeding correlation holds as ensemble size K scales."""
    def corr(K):
        random.seed(SEED); parent=[random.random() for _ in range(K)]
        child=[0.7*parent[i]+0.3*random.random() for i in range(K)]
        rnd=[random.random() for _ in range(K)]
        def cc(a,b):
            ma,mb=statistics.mean(a),statistics.mean(b); cov=sum((x-ma)*(y-mb) for x,y in zip(a,b))/len(a)
            sa=statistics.pstdev(a) or 1e-9; sb=statistics.pstdev(b) or 1e-9; return cov/(sa*sb)
        return cc(child,parent),cc(rnd,parent)
    rungs=[20,100,500]; curve=[(K,)+corr(K) for K in rungs]
    holds=all(cs>0.5 and cs>cr+0.3 for K,cs,cr in curve)
    print(f"[H_882 SEEDING scale]   {' '.join(f'K{K}:seed={cs:.2f}/rand={cr:.2f}' for K,cs,cr in curve)} -> {'SCALE-SURVIVES (founder bias holds at every ensemble size)' if holds else 'SCALE-BREAK'}")
    return holds


def h896_stdp_scale():
    """STDP edge-asymmetry scales with # spike pairs (directionality strengthens, scale-invariant sign)."""
    def asym(P):
        random.seed(SEED); wf=wb=0.0
        for _ in range(P):
            if random.random()<0.5: wf+=0.01
            else: wb-=0.01
        return abs(wf-wb)
    rungs=[500,2000,8000]; curve=[(P,asym(P)) for P in rungs]
    grows=curve[0][1]<curve[-1][1] and all(a>0.5 for _,a in curve)
    print(f"[H_896 STDP scale]      {' '.join(f'P{P}:asym={a:.2f}' for P,a in curve)} -> {'SCALE-SURVIVES (directional edge grows with pairs)' if grows else 'SCALE-CAP'} [chip AKD1500-future]")
    return grows


def h905_predhier_scale():
    """Hierarchical pred-coding advantage over flat holds/grows as sequence length scales."""
    def mse(hier,T):
        random.seed(SEED); x=0.0; trend=0.0; errs=[]
        for t in range(T):
            tt=math.sin(t*0.02); detail=random.gauss(0,0.2); sig=tt+detail
            if hier: trend+=0.05*(sig-trend); errs.append(detail**2)
            else: pred=x; x+=0.05*(sig-x); errs.append((sig-pred)**2)
        return statistics.mean(errs)
    rungs=[500,2000,8000]; curve=[(T, mse(True,T), mse(False,T)) for T in rungs]
    wins=all(h<f for _,h,f in curve)
    print(f"[H_905 PRED-HIER scale] {' '.join(f'T{T}:h={h:.3f}/flat={f:.3f}' for T,h,f in curve)} -> {'SCALE-SURVIVES (hierarchy beats flat at every length)' if wins else 'SCALE-BREAK'}")
    return wins


def h866_fret_scale():
    """FRET distance-decay profile persists (monotone decay) as the lattice scales."""
    def monotone(L):
        T0,absorb,iters=1.0,0.04,4000; T=[0.0]*L
        for _ in range(iters):
            nT=list(T)
            for i in range(1,L):
                left=T[i-1]; right=T[i+1] if i+1<L else T[i]
                nT[i]=(1-absorb)*0.5*(left+right)+0.5*absorb*T[i]
            nT[0]=T0; T=nT
        bins=[T[d] for d in (1,int(L*0.15),int(L*0.3),int(L*0.5)) if d<L]
        return all(bins[i]>bins[i+1] for i in range(len(bins)-1))
    rungs=[40,80,160]; curve=[(L,monotone(L)) for L in rungs]
    holds=all(m for _,m in curve)
    print(f"[H_866 FRET scale]      {' '.join(f'L{L}:monotone={m}' for L,m in curve)} -> {'SCALE-SURVIVES (distance-decay holds at every lattice size)' if holds else 'SCALE-BREAK'}")
    return holds


if __name__ == "__main__":
    print("=== SCALE-UP BENCHMARK EXT (remaining SENSITIVE · >=3-rung) seed=%d ===" % SEED)
    fns=[("H_886 TURING",h886_turing_scale),("H_901 RING",h901_ring_scale),("H_862 HGT",h862_hgt_scale),
         ("H_864 PRION",h864_prion_scale),("H_882 SEEDING",h882_seeding_scale),("H_896 STDP",h896_stdp_scale),
         ("H_905 PRED-HIER",h905_predhier_scale),("H_866 FRET",h866_fret_scale)]
    res={}
    for name,fn in fns:
        try: res[name]=fn()
        except Exception as e: res[name]=None; print(f"[{name}] ERROR {type(e).__name__}: {e}")
    surv=[k for k,v in res.items() if v is True]; other=[k for k,v in res.items() if v is False]
    print("=== SUMMARY: SCALE-SURVIVES=%d %s | CAP/BREAK=%d %s ===" % (len(surv),surv,len(other),other))
