import numpy as np
def mi_bits(x,y):
    x=np.asarray(x); y=np.asarray(y); T=len(x); mi=0.0
    for xv in (0,1):
        for yv in (0,1):
            n=np.sum((x==xv)&(y==yv))
            if n==0: continue
            pxy=n/T; px=np.sum(x==xv)/T; py=np.sum(y==yv)/T
            mi+=pxy*np.log2(pxy/(px*py))
    return mi
def channel_mi(amp,thr,sigma,period,T,mode,shuffle,seed):
    rng=np.random.default_rng(seed)
    t=np.arange(T); sig=amp*np.sin(2*np.pi*t/period)
    ethr=0.0 if mode==1 else thr
    noise=sigma*rng.standard_normal(T)
    x=(sig>=0).astype(int); y=((sig+noise)>=ethr).astype(int)
    if shuffle==1: x=rng.permutation(x)
    return mi_bits(x,y)
amp,thr,period,T=0.8,1.0,40,4000
sigmas=[0.0,0.1,0.2,0.3,0.5,0.7,1.0,1.5,2.0,3.0]
print("NONLINEAR (subthreshold amp<thr):")
mis=[channel_mi(amp,thr,s,period,T,0,0,7) for s in sigmas]
for s,m in zip(sigmas,mis): print(f"  sigma={s:.2f}  MI={m:.4f}")
peak_i=int(np.argmax(mis))
print(f"  MI(0)={mis[0]:.4f}  peak MI={mis[peak_i]:.4f} @sigma={sigmas[peak_i]}  invU={mis[peak_i]>mis[0] and mis[peak_i]>mis[-1]}")
print("SHUFFLE control (phase-randomized labels):")
mish=[channel_mi(amp,thr,s,period,T,0,1,7) for s in sigmas]
print(f"  max shuffled MI={max(mish):.4f}")
print("ABLATION linearized (threshold->mean, barrier removed):")
mial=[channel_mi(amp,thr,s,period,T,1,0,7) for s in sigmas]
for s,m in zip(sigmas,mial): print(f"  sigma={s:.2f}  MI={m:.4f}")
pk=int(np.argmax(mial)); print(f"  MI(0)={mial[0]:.4f} peak@{sigmas[pk]} monotonic_dec_peak_at_0={pk==0}")
