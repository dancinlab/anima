#!/usr/bin/env python3
"""TPR with bias-augmented encoders (fair strong version): input [vec;1] so outer product
spans constant+linear+bilinear -> can represent the full target family, not just pure 2nd-order."""
import json, os, numpy as np
d, K = 32, 256
P_ROLE, Q_FILL = 20, 20
N_PAIRS, EPOCHS, LR = 3000, 2000, 3e-3
OUTDIR = "/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/tensor_product"
vec = np.random.RandomState(0).randn(K, d)
TRAIN_IDX = np.arange(0, 192); TEST_IDX = np.arange(192, 256)
rs1 = np.random.RandomState(1)
Wr = rs1.randn(d, d)/np.sqrt(d); Wf = rs1.randn(d, d)/np.sqrt(d); ROLL = int(rs1.randint(1, d))
def target(ai, bi):
    va, vb = vec[ai], vec[bi]
    return np.tanh(va@Wr.T + vb@Wf.T + va*np.roll(vb, ROLL, axis=-1))
def sample_pairs(g, n, seed):
    rs = np.random.RandomState(seed); a = rs.choice(g, n); b = rs.choice(g, n); m = a==b
    while m.any(): b[m] = rs.choice(g, int(m.sum())); m = a==b
    return a, b
tr_a, tr_b = sample_pairs(TRAIN_IDX, N_PAIRS, 2); te_a, te_b = sample_pairs(TEST_IDX, N_PAIRS, 2)
one = np.ones((N_PAIRS, 1))
Xa_tr = np.hstack([vec[tr_a], one]); Xb_tr = np.hstack([vec[tr_b], one])
Xa_te = np.hstack([vec[te_a], one]); Xb_te = np.hstack([vec[te_b], one])
T_tr, T_te = target(tr_a, tr_b), target(te_a, te_b)
di = d+1
def r2(p, t): return 1.0 - np.sum((p-t)**2)/np.sum((t-t.mean(0))**2)
class Adam:
    def __init__(s, p, lr): s.p, s.lr = p, lr; s.m=[np.zeros_like(x) for x in p]; s.v=[np.zeros_like(x) for x in p]; s.t=0
    def step(s, g):
        s.t+=1; b1,b2,e=0.9,0.999,1e-8
        for i,gi in enumerate(g):
            s.m[i]=b1*s.m[i]+(1-b1)*gi; s.v[i]=b2*s.v[i]+(1-b2)*gi*gi
            s.p[i]-=s.lr*(s.m[i]/(1-b1**s.t))/(np.sqrt(s.v[i]/(1-b2**s.t))+e)
def shuf(xa, xb, do):
    if not do: return xa, xb
    rs=np.random.RandomState(99); sw=rs.rand(len(xa))<0.5; xa2,xb2=xa.copy(),xb.copy()
    xa2[sw],xb2[sw]=xb[sw],xa[sw]; return xa2,xb2
def train_tpr(do_shuf=False):
    rs=np.random.RandomState(10)
    Ra=rs.randn(P_ROLE,di)/np.sqrt(di); Fb=rs.randn(Q_FILL,di)/np.sqrt(di)
    W=rs.randn(d,P_ROLE*Q_FILL)/np.sqrt(P_ROLE*Q_FILL); opt=Adam([Ra,Fb,W],LR); N=N_PAIRS; sc=1.0/(N*d)
    for _ in range(EPOCHS):
        role=Xa_tr@Ra.T; fill=Xb_tr@Fb.T
        Ff=(role[:,:,None]*fill[:,None,:]).reshape(N,-1); pred=Ff@W.T
        dp=2.0*(pred-T_tr)*sc; gW=dp.T@Ff; dF=(dp@W).reshape(N,P_ROLE,Q_FILL)
        gRa=(dF*fill[:,None,:]).sum(2).T@Xa_tr; gFb=(dF*role[:,:,None]).sum(1).T@Xb_tr
        opt.step([gRa,gFb,gW])
    xa,xb=shuf(Xa_te,Xb_te,do_shuf); role=xa@Ra.T; fill=xb@Fb.T
    Ff=(role[:,:,None]*fill[:,None,:]).reshape(len(xa),-1); return r2(Ff@W.T,T_te)
def train_add(do_shuf=False):
    rs=np.random.RandomState(20); M=32
    Wa=rs.randn(M,di)/np.sqrt(di); Wb=rs.randn(M,di)/np.sqrt(di); W=rs.randn(d,M)/np.sqrt(M)
    opt=Adam([Wa,Wb,W],LR); N=N_PAIRS; sc=1.0/(N*d)
    for _ in range(EPOCHS):
        r=Xa_tr@Wa.T+Xb_tr@Wb.T; pred=r@W.T; dp=2.0*(pred-T_tr)*sc
        gW=dp.T@r; dr=dp@W; opt.step([dr.T@Xa_tr, dr.T@Xb_tr, gW])
    xa,xb=shuf(Xa_te,Xb_te,do_shuf); return r2((xa@Wa.T+xb@Wb.T)@W.T,T_te)
m=train_tpr(False); ms=train_tpr(True); a=train_add(False); as_=train_add(True)
margin=m-a; drop=m-ms; tr=(margin>=0.15)and(drop>=0.15)
out={"mechanism":"tensor_product","spec":"Smolensky TPR/bilinear, bias-augmented encoders [vec;1] -> spans const+linear+bilinear (fair strong TPR), linear head, end-to-end Adam (E4)",
 "params":{"d":d,"K":K,"p_role":P_ROLE,"q_fill":Q_FILL,"n_pairs":N_PAIRS,"epochs":EPOCHS,"lr":LR,"roll":ROLL,"encoder_bias":True,"train_concepts":"0-191","test_concepts":"192-255"},
 "cross_dist_r2_mech":float(m),"cross_dist_r2_additive":float(a),
 "order_shuffle_r2_mech":float(ms),"order_shuffle_r2_additive":float(as_),
 "margin_mech_minus_additive":float(margin),"shuffle_drop_mech":float(drop),
 "criteria":"TRANSFER-EARNING iff margin>=0.15 AND shuffle_drop>=0.15",
 "verdict":"TRANSFER-EARNING" if tr else "NO-TRANSFER"}
os.makedirs(OUTDIR,exist_ok=True)
with open(OUTDIR+"/RESULT.json","w") as f: json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
