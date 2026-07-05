#!/usr/bin/env python3
"""
Transfer-mechanism sweep — MECHANISM = recurrent_trained (E7, TRAINED GRU).

SHARED SYNTHETIC TASK (corrected BINDING-DOMINANT target; identical across sweep agents,
only the mechanism differs). 2nd-run task fixing the 1st-run additive-dominant artifact.

  - K=256 concepts, d=32 fixed random vectors: np.random.RandomState(0).randn(256,32).
  - DISJOINT split: TRAIN concepts 0-191 (192), TEST concepts 192-255 (64). overlap 0.
  - PURE BILINEAR non-commutative target (NO linear a/b terms):
        T = np.random.RandomState(1).randn(16,16,16)          # (k,i,j), asymmetric in (i,j)
        t(a,b) = tanh( einsum("kij,i,j->k", T, vec[a][:16], vec[b][:16]) )   # (16,)
    additive(Wa@a+Wb@b) cannot represent a bilinear form -> additive cross R2 ~0.
    T asymmetric -> t(a,b)!=t(b,a). Bilinear with T fixed -> transfers to unseen concepts.
  - Mechanisms receive full 32-d vectors; target reads first 16 dims (shared distractor dims).
  - TRAIN pairs 3000 (a!=b, TRAIN concepts, seed2); TEST 3000 (a!=b, TEST concepts, seed2)
    = CROSS-DISTRIBUTION (held-out concepts).
  - Mechanism params + linear head trained END-TO-END (numpy Adam, ~3000 epochs) on TRAIN MSE.
  - Metric: cross-distribution R2 on TEST. Controls: ADDITIVE baseline (jointly trained),
    ORDER-SHUFFLE (swap a,b at test -> R2 collapses).
  - Verdict TRANSFER-EARNING iff cross_R2(mech)-cross_R2(add)>=0.15 AND shuffle drops>=0.15.
  - ANCHOR: slot_gated_write (E1) must clear cross>=add+0.15 on THIS target else INCONCLUSIVE.

MECHANISM recurrent_trained: small GRU over [vec[a],vec[b]] (h0=0), final hidden=rep; exact
  2-step BPTT (analytic, gradient-checked). Multiplicative gates can express order-dependent
  bilinear interaction. Q: does TRAINED recurrence earn cross-distribution transfer?
"""
import numpy as np, json, os, shutil

K, D = 256, 32
DT = 16
vec = np.random.RandomState(0).randn(K, D).astype(np.float64)
TRAIN_C = np.arange(0, 192); TEST_C = np.arange(192, 256)
T = np.random.RandomState(1).randn(DT, DT, DT).astype(np.float64)

def target(a_idx, b_idx):
    va = vec[a_idx][:, :DT]; vb = vec[b_idx][:, :DT]
    return np.tanh(np.einsum("kij,ni,nj->nk", T, va, vb))

def sample_pairs(concepts, n, seed):
    rng = np.random.RandomState(seed)
    a = concepts[rng.randint(0, len(concepts), size=n*3)]
    b = concepts[rng.randint(0, len(concepts), size=n*3)]
    mask = a != b; a, b = a[mask][:n], b[mask][:n]
    assert len(a) == n
    return a, b

tr_a, tr_b = sample_pairs(TRAIN_C, 3000, 2)
te_a, te_b = sample_pairs(TEST_C, 3000, 2)
Ttr = target(tr_a, tr_b); Tte = target(te_a, te_b)

class Adam:
    def __init__(s, params, lr=3e-3, b1=0.9, b2=0.999, eps=1e-8):
        s.p=params; s.lr=lr; s.b1=b1; s.b2=b2; s.eps=eps
        s.m={k:np.zeros_like(v) for k,v in params.items()}
        s.v={k:np.zeros_like(v) for k,v in params.items()}; s.t=0
    def step(s, grads):
        s.t+=1
        for k in s.p:
            s.m[k]=s.b1*s.m[k]+(1-s.b1)*grads[k]
            s.v[k]=s.b2*s.v[k]+(1-s.b2)*(grads[k]**2)
            mh=s.m[k]/(1-s.b1**s.t); vh=s.v[k]/(1-s.b2**s.t)
            s.p[k]-=s.lr*mh/(np.sqrt(vh)+s.eps)

def r2_score(pred, true):
    return 1.0 - np.sum((pred-true)**2)/np.sum((true-true.mean(axis=0))**2)

def sigmoid(x):
    return np.where(x>=0, 1.0/(1.0+np.exp(-x)), np.exp(x)/(1.0+np.exp(x)))

# ---------------- GRU ----------------
def gru_params(H, rng):
    return {'Wz':rng.randn(D,H)/np.sqrt(D),'Uz':rng.randn(H,H)/np.sqrt(H),'bz':np.zeros(H),
            'Wr':rng.randn(D,H)/np.sqrt(D),'Ur':rng.randn(H,H)/np.sqrt(H),'br':np.zeros(H),
            'Wh':rng.randn(D,H)/np.sqrt(D),'Uh':rng.randn(H,H)/np.sqrt(H),'bh':np.zeros(H),
            'V':rng.randn(H,DT)/np.sqrt(H),'c':np.zeros(DT)}

def gru_step(x, hp, P):
    z=sigmoid(x@P['Wz']+hp@P['Uz']+P['bz'])
    r=sigmoid(x@P['Wr']+hp@P['Ur']+P['br'])
    rhp=r*hp
    hh=np.tanh(x@P['Wh']+rhp@P['Uh']+P['bh'])
    hn=(1-z)*hp+z*hh
    return hn, (x,hp,z,r,rhp,hh,hn)

def gru_step_back(dhn, cache, P, g):
    x,hp,z,r,rhp,hh,hn=cache
    dz=dhn*(hh-hp); dhh=dhn*z; dhp=dhn*(1-z)
    dah=dhh*(1-hh**2)
    g['Wh']+=x.T@dah; g['Uh']+=rhp.T@dah; g['bh']+=dah.sum(0)
    drhp=dah@P['Uh'].T; dr=drhp*hp; dhp+=drhp*r
    dar=dr*r*(1-r)
    g['Wr']+=x.T@dar; g['Ur']+=hp.T@dar; g['br']+=dar.sum(0); dhp+=dar@P['Ur'].T
    daz=dz*z*(1-z)
    g['Wz']+=x.T@daz; g['Uz']+=hp.T@daz; g['bz']+=daz.sum(0); dhp+=daz@P['Uz'].T
    return dhp

def gru_forward(a_idx, b_idx, P):
    va=vec[a_idx]; vb=vec[b_idx]; n=va.shape[0]; H=P['bz'].shape[0]
    h1,c1=gru_step(va, np.zeros((n,H)), P)
    h2,c2=gru_step(vb, h1, P)
    return h2@P['V']+P['c'], (c1,c2)

def gru_grads(a_idx, b_idx, P, Y):
    pred,(c1,c2)=gru_forward(a_idx,b_idx,P); n=pred.shape[0]
    err=pred-Y; dpred=(2.0/(n*DT))*err
    g={k:np.zeros_like(v) for k,v in P.items()}
    g['V']+=c2[6].T@dpred; g['c']+=dpred.sum(0)
    dh1=gru_step_back(dpred@P['V'].T, c2, P, g)
    gru_step_back(dh1, c1, P, g)
    return g

def gradcheck_gru():
    rng=np.random.RandomState(9); P=gru_params(6,rng)
    a=np.array([3,5,7,11]); b=np.array([4,6,8,12]); Y=target(a,b)
    g=gru_grads(a,b,P,Y); eps=1e-6; worst=0.0
    for k in ['Wz','Uz','bz','Wr','Ur','br','Wh','Uh','bh','V','c']:
        arr=P[k]; cnt=0
        for idx in np.ndindex(arr.shape):
            if cnt>=4: break
            cnt+=1; old=arr[idx]
            arr[idx]=old+eps; p1,_=gru_forward(a,b,P); l1=np.mean((p1-Y)**2)
            arr[idx]=old-eps; p2,_=gru_forward(a,b,P); l2=np.mean((p2-Y)**2)
            arr[idx]=old
            num=(l1-l2)/(2*eps); ana=g[k][idx]
            worst=max(worst, abs(num-ana)/max(1e-8,abs(num)+abs(ana)))
    return worst

def train_gru(seed=7, H=48, epochs=3000, lr=3e-3, shuffle_test=False):
    rng=np.random.RandomState(seed); P=gru_params(H,rng); opt=Adam(P,lr=lr)
    for ep in range(epochs): opt.step(gru_grads(tr_a,tr_b,P,Ttr))
    ea,eb=te_a.copy(),te_b.copy()
    if shuffle_test:
        rs=np.random.RandomState(123); sw=rs.rand(len(ea))<0.5
        ea2,eb2=ea.copy(),eb.copy(); ea2[sw],eb2[sw]=eb[sw],ea[sw]; ea,eb=ea2,eb2
    pte,_=gru_forward(ea,eb,P); ptr,_=gru_forward(tr_a,tr_b,P)
    return r2_score(ptr,Ttr), r2_score(pte,Tte)

# ---------------- ADDITIVE ----------------
def train_additive(seed=7, H=48, epochs=3000, lr=3e-3, shuffle_test=False):
    rng=np.random.RandomState(seed)
    P={'Wa':rng.randn(D,H)/np.sqrt(D),'Wb':rng.randn(D,H)/np.sqrt(D),
       'V':rng.randn(H,DT)/np.sqrt(H),'c':np.zeros(DT)}
    opt=Adam(P,lr=lr)
    def fwd(a,b,P):
        va=vec[a]; vb=vec[b]; r=va@P['Wa']+vb@P['Wb']
        return r@P['V']+P['c'], (va,vb,r)
    n=len(tr_a)
    for ep in range(epochs):
        pred,(va,vb,r)=fwd(tr_a,tr_b,P)
        dpred=(2.0/(n*DT))*(pred-Ttr)
        dr=dpred@P['V'].T
        opt.step({'Wa':va.T@dr,'Wb':vb.T@dr,'V':r.T@dpred,'c':dpred.sum(0)})
    ea,eb=te_a.copy(),te_b.copy()
    if shuffle_test:
        rs=np.random.RandomState(123); sw=rs.rand(len(ea))<0.5
        ea2,eb2=ea.copy(),eb.copy(); ea2[sw],eb2[sw]=eb[sw],ea[sw]; ea,eb=ea2,eb2
    pte,_=fwd(ea,eb,P); ptr,_=fwd(tr_a,tr_b,P)
    return r2_score(ptr,Ttr), r2_score(pte,Tte)

# ---------------- ANCHOR slot_gated_write ----------------
def train_slot(seed=7, N=8, H=32, Vd=32, Lr=32, Lf=32, epochs=3000, lr=3e-3, shuffle_test=False):
    rng=np.random.RandomState(seed)
    P={'Wq':rng.randn(H,D)/np.sqrt(D),'Sk':rng.randn(N,H)/np.sqrt(H),
       'Wv':rng.randn(Vd,D)/np.sqrt(D),'Wrl':rng.randn(Lr,D)/np.sqrt(D),
       'Wfl':rng.randn(Lf,D)/np.sqrt(D),'Wh':rng.randn(DT,N*Vd+Lr+Lf)/np.sqrt(N*Vd+Lr+Lf),
       'bh':np.zeros(DT)}
    opt=Adam(P,lr=lr)
    def fwd(a,b,P):
        va=vec[a]; vb=vec[b]; rq=va@P['Wq'].T
        logits=rq@P['Sk'].T; logits-=logits.max(1,keepdims=True)
        e=np.exp(logits); g=e/e.sum(1,keepdims=True)
        val=vb@P['Wv'].T
        M=g[:,:,None]*val[:,None,:]; mflat=M.reshape(M.shape[0],-1)
        rl=va@P['Wrl'].T; fl=vb@P['Wfl'].T
        r=np.concatenate([mflat,rl,fl],1)
        return r@P['Wh'].T+P['bh'], (va,vb,rq,g,val,M,mflat,rl,fl,r)
    n=len(tr_a)
    for ep in range(epochs):
        pred,(va,vb,rq,g,val,M,mflat,rl,fl,r)=fwd(tr_a,tr_b,P)
        dpred=(2.0/(n*DT))*(pred-Ttr)
        gWh=dpred.T@r; gbh=dpred.sum(0); dr=dpred@P['Wh']
        dmflat=dr[:,:N*Vd]; drl=dr[:,N*Vd:N*Vd+Lr]; dfl=dr[:,N*Vd+Lr:]
        gWrl=drl.T@va; gWfl=dfl.T@vb
        dM=dmflat.reshape(M.shape)
        dg=(dM*val[:,None,:]).sum(2); dval=(dM*g[:,:,None]).sum(1)
        dlog=g*(dg-(dg*g).sum(1,keepdims=True))
        gSk=dlog.T@rq; drq=dlog@P['Sk']; gWq=drq.T@va; gWv=dval.T@vb
        opt.step({'Wq':gWq,'Sk':gSk,'Wv':gWv,'Wrl':gWrl,'Wfl':gWfl,'Wh':gWh,'bh':gbh})
    ea,eb=te_a.copy(),te_b.copy()
    if shuffle_test:
        rs=np.random.RandomState(123); sw=rs.rand(len(ea))<0.5
        ea2,eb2=ea.copy(),eb.copy(); ea2[sw],eb2[sw]=eb[sw],ea[sw]; ea,eb=ea2,eb2
    pte,_=fwd(ea,eb,P); ptr,_=fwd(tr_a,tr_b,P)
    return r2_score(ptr,Ttr), r2_score(pte,Tte)

if __name__=='__main__':
    gc=gradcheck_gru()
    assert gc<1e-4, f"GRU gradcheck failed {gc}"
    tr_mech,cross_mech=train_gru(shuffle_test=False)
    _,cross_shuf=train_gru(shuffle_test=True)
    tr_add,cross_add=train_additive(shuffle_test=False)
    tr_slot,cross_slot=train_slot(shuffle_test=False)
    _,cross_slot_shuf=train_slot(shuffle_test=True)
    anchor_delta=cross_slot-cross_add; anchor_valid=anchor_delta>=0.15
    delta_add=cross_mech-cross_add; shuffle_drop=cross_mech-cross_shuf
    transfer=(delta_add>=0.15) and (shuffle_drop>=0.15)
    verdict=("INCONCLUSIVE-task-artifact" if not anchor_valid
             else ("TRANSFER-EARNING" if transfer else "NO-TRANSFER"))
    out={"mechanism":"recurrent_trained",
         "spec":"small GRU over [vec[a],vec[b]] (h0=0), final hidden=rep; exact 2-step BPTT, Adam",
         "task":"PURE-BILINEAR non-commutative binding, cross-distribution (disjoint concept split)",
         "config":{"K":K,"d":D,"target_dims":DT,"train_concepts":[0,191],"test_concepts":[192,255],
                   "n_train_pairs":len(tr_a),"n_test_pairs":len(te_a),
                   "gru_H":48,"epochs":3000,"opt":"adam","lr":3e-3},
         "gradcheck_worst_rel_err":float(gc),
         "train_r2_mech":round(float(tr_mech),4),
         "cross_r2_mech":round(float(cross_mech),4),
         "cross_r2_shuffle":round(float(cross_shuf),4),
         "train_r2_additive":round(float(tr_add),4),
         "cross_r2_additive":round(float(cross_add),4),
         "delta_vs_additive":round(float(delta_add),4),
         "shuffle_drop":round(float(shuffle_drop),4),
         "anchor_slot_gated_write":{"train_r2":round(float(tr_slot),4),
                                    "cross_r2":round(float(cross_slot),4),
                                    "cross_r2_shuffle":round(float(cross_slot_shuf),4),
                                    "delta_vs_additive":round(float(anchor_delta),4),
                                    "clears_+0.15":bool(anchor_valid)},
         "thresholds":{"delta_add>=":0.15,"shuffle_drop>=":0.15,"anchor_delta>=":0.15},
         "verdict":verdict}
    print(json.dumps(out,indent=2))
    dest="/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/recurrent_trained"
    os.makedirs(dest,exist_ok=True)
    with open(os.path.join(dest,"RESULT.json"),"w") as f: json.dump(out,f,indent=2)
    shutil.copy(os.path.abspath(__file__), os.path.join(dest,"reproduce.py"))
    print("WROTE", dest)
