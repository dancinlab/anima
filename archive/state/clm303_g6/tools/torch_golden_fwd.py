# Numpy reimpl of train/clm/model/model.py CLMConvMoE forward using RAW fp32 torch weights (NOT the .clm) via ptload.py. The torch GOLDEN that the .clm int4 mirror is checked against (agreed to 4 decimals -> serialize is faithful). Built 2026-06-24, H_1579.
# Provenance: anima H_1579 clm303 root-cause (overfit, NOT serialize defect).
#   See HYPOTHESES/cards/H_1579_clm303_serialization_defect.md + CORRECTION_overfit_not_serialize.md.
#   Torch-free (no torch import) — runs on any host with numpy.

# Numpy reimpl of model.py CLMConvMoE forward using the RAW torch fp32 weights
# (NOT the .clm) — this is the torch GOLDEN forward, no int4 quant, no .clm layout.
# If THIS gives garbage too => the torch ckpt itself never learned (training defect).
import sys, math
sys.path.insert(0,'/private/tmp/claude-501/-Users-mini-dancinlab-anima/2f2f8df3-5c44-48e3-acaa-7ece60efa6a7/scratchpad')
import numpy as np, ptload

PT=sys.argv[1]; CORPUS=sys.argv[2]
sd=ptload.load_pt(PT)
d=sd['embed.weight'].shape[1]; V=sd['embed.weight'].shape[0]
L=sum(1 for k in sd if k.startswith('trunk.') and k.endswith('.conv.conv.weight'))
E=sum(1 for k in sd if k.startswith('moe.experts.') and k.endswith('.conv.conv.weight'))
K=sd['embed_conv.conv.weight'].shape[2]
print(f"GOLDEN torch fwd: d={d} V={V} L={L} E={E} K={K}",flush=True)

def gelu_erf(x):  # torch nn.GELU default = exact erf
    from math import erf
    vec=np.vectorize(lambda t: 0.5*t*(1.0+erf(t/np.sqrt(2.0))))
    return vec(x)
def gelu_erf_fast(x):
    # exact erf via scipy-free: use math.erf vectorized is slow; use tanh-free erf approx? 
    # Use numpy: erf not in numpy. Implement Abramowitz-Stegun 7.1.26 (err<1.5e-7).
    s=np.sign(x); ax=np.abs(x)/np.sqrt(2.0)
    t=1.0/(1.0+0.3275911*ax)
    y=1.0-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*np.exp(-ax*ax)
    erf=s*y
    return 0.5*x*(1.0+erf)
def conv1d_torch(x, w, b, dil, K):
    # x:(T,Cin); w:(Cout,Cin,K) torch; causal left pad (K-1)*dil
    T,Cin=x.shape; Cout=w.shape[0]
    pad=(K-1)*dil
    xp=np.concatenate([np.zeros((pad,Cin)),x],0)  # (T+pad,Cin)
    y=np.zeros((T,Cout))
    # build via taps
    for k in range(K):
        # tap k uses xp[t + k*dil : ...]; output position t reads xp[t + k*dil]
        seg=xp[k*dil : k*dil+T]    # (T,Cin)
        y += seg @ w[:,:,k].T       # (T,Cout)
    return y + b[None,:]
def gn1(x,g,b):
    mu=x.mean(1,keepdims=True); var=x.var(1,keepdims=True)
    return (x-mu)/np.sqrt(var+1e-5)*g[None,:]+b[None,:]
def fwd(tok):
    T=len(tok)
    x=sd['embed.weight'][tok]   # (T,d)
    x=conv1d_torch(x, sd['embed_conv.conv.weight'], sd['embed_conv.conv.bias'],1,K)
    dil=1
    for i in range(L):
        de=min(dil,512)
        h=conv1d_torch(x, sd[f'trunk.{i}.conv.conv.weight'], sd[f'trunk.{i}.conv.conv.bias'],de,K)
        h=gn1(h, sd[f'trunk.{i}.norm.weight'], sd[f'trunk.{i}.norm.bias'])
        h=gelu_erf_fast(h)
        x=x+h; dil*=2
    lr=conv1d_torch(x, sd['moe.router.weight'], sd['moe.router.bias'],1,1)  # (T,E)
    exo=[gelu_erf_fast(conv1d_torch(x, sd[f'moe.experts.{j}.conv.conv.weight'], sd[f'moe.experts.{j}.conv.conv.bias'],1,K)) for j in range(E)]
    p=np.exp(lr-lr.max(1,keepdims=True)); p/=p.sum(1,keepdims=True)
    y=sum(p[:,j:j+1]*exo[j] for j in range(E))
    y=gn1(y, sd['norm_out.weight'], sd['norm_out.bias'])
    out=conv1d_torch(y, sd['readout.weight'], sd['readout.bias'],1,1)
    return out
def ce(lg,tgt):
    z=lg-lg.max(1,keepdims=True); lse=np.log(np.exp(z).sum(1))
    return float((-(z[np.arange(len(tgt)),tgt.astype(int)]-lse)).sum()/len(tgt))
rb=open(CORPUS,'rb').read(); n=len(rb); T=24; nwin=24; stride=max(1,(n-T-1)//nwin)
sm=ss=0.0;cnt=0
for s in range(nwin):
    base=s*stride
    if base+T+1<=n:
        tok=np.frombuffer(rb,np.uint8,T,base).astype(int); tgt=np.frombuffer(rb,np.uint8,T,base+1).astype(float)
        lg=fwd(tok); sm+=ce(lg,tgt); ss+=ce(lg,tgt[::-1].copy()); cnt+=1
print(f"GOLDEN model_ce={sm/cnt:.5f} shuffle={ss/cnt:.5f} uniform={math.log(V):.5f} -> {'DESCENT' if sm/cnt<math.log(V) else 'NO-DESCENT'}",flush=True)
