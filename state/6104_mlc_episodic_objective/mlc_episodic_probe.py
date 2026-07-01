#!/usr/bin/env python3
# H_1835 MLC episodic-objective toy probe — numpy from-scratch, torch/gauge_lib FORBIDDEN.
# DIRECTIONAL-only mirror (a_engine_native_learning). Manual reverse-mode autograd + Adam,
# finite-diff gradcheck PASS. Tests whether objective-as-TASK-STRUCTURE (Lake&Baroni MLC,
# Nature 2023) — episodic grammar permutation + in-context study examples — lifts a toy
# compositional-generalization metric above the plain-next-byte-CE floor (H_1602/H_1816 area,
# additive-aux collapse). Canonical MLC "novel primitive in composition" (SCAN dax) test:
# each primitive is DEMONSTRATED in isolation, one primitive is HELD OUT of composition during
# training and must be composed at test.
import numpy as np, sys, time

# ---------------- minimal reverse-mode autograd on numpy arrays ----------------
class T:
    __slots__=('data','grad','_parents','_backward')
    def __init__(self,data,parents=(),backward=None):
        self.data=np.asarray(data,dtype=np.float64)
        self.grad=np.zeros_like(self.data)
        self._parents=parents; self._backward=backward

def backward(root):
    topo=[]; seen=set()
    def build(v):
        if id(v) in seen: return
        seen.add(id(v))
        for p in v._parents: build(p)
        topo.append(v)
    build(root)
    root.grad=np.ones_like(root.data)
    for v in reversed(topo):
        if v._backward: v._backward()

def reduce_to(g,shape):
    while g.ndim>len(shape): g=g.sum(0)
    for i,s in enumerate(shape):
        if s==1 and g.shape[i]!=1: g=g.sum(i,keepdims=True)
    return g

def matmul(a,b):
    out=T(a.data@b.data,(a,b))
    def bw():
        a.grad+=reduce_to(out.grad@np.swapaxes(b.data,-1,-2),a.data.shape)
        b.grad+=reduce_to(np.swapaxes(a.data,-1,-2)@out.grad,b.data.shape)
    out._backward=bw; return out

def add(a,b):
    out=T(a.data+b.data,(a,b))
    def bw():
        a.grad+=reduce_to(out.grad,a.data.shape)
        b.grad+=reduce_to(out.grad,b.data.shape)
    out._backward=bw; return out

def mul(a,s):
    out=T(a.data*s,(a,))
    def bw(): a.grad+=out.grad*s
    out._backward=bw; return out

def relu(a):
    out=T(np.maximum(a.data,0.0),(a,))
    def bw(): a.grad+=out.grad*(a.data>0)
    out._backward=bw; return out

def softmax(a):
    x=a.data-a.data.max(-1,keepdims=True)
    e=np.exp(x); y=e/e.sum(-1,keepdims=True)
    out=T(y,(a,))
    def bw():
        g=out.grad
        a.grad+=y*(g-(g*y).sum(-1,keepdims=True))
    out._backward=bw; return out

def reshape(a,shape):
    out=T(a.data.reshape(shape),(a,))
    def bw(): a.grad+=out.grad.reshape(a.data.shape)
    out._backward=bw; return out

def swap(a,i,j):
    out=T(np.swapaxes(a.data,i,j),(a,))
    def bw(): a.grad+=np.swapaxes(out.grad,i,j)
    out._backward=bw; return out

def layernorm(a,gamma,beta,eps=1e-5):
    x=a.data; D=x.shape[-1]
    mu=x.mean(-1,keepdims=True); xc=x-mu
    var=(xc*xc).mean(-1,keepdims=True); inv=1.0/np.sqrt(var+eps)
    xn=xc*inv
    out=T(xn*gamma.data+beta.data,(a,gamma,beta))
    def bw():
        dy=out.grad
        gamma.grad+=reduce_to(dy*xn,gamma.data.shape)
        beta.grad+=reduce_to(dy,beta.data.shape)
        dxn=dy*gamma.data
        s1=dxn.sum(-1,keepdims=True); s2=(dxn*xn).sum(-1,keepdims=True)
        a.grad+=inv/D*(D*dxn-s1-xn*s2)
    out._backward=bw; return out

def embed(E,idx):
    out=T(E.data[idx],(E,))
    def bw(): np.add.at(E.grad,idx,out.grad)
    out._backward=bw; return out

def cross_entropy(logits,targets,mask):
    x=logits.data; x=x-x.max(-1,keepdims=True)
    e=np.exp(x); p=e/e.sum(-1,keepdims=True)
    B,Tt,V=x.shape
    bi=np.arange(B)[:,None]; ti=np.arange(Tt)[None,:]
    nll=-np.log(p[bi,ti,targets]+1e-12)
    m=mask; denom=m.sum()+1e-9
    loss=(nll*m).sum()/denom
    out=T(loss,(logits,))
    def bw():
        d=p.copy(); d[bi,ti,targets]-=1.0
        d=d*(m[...,None])/denom
        logits.grad+=d*out.grad
    out._backward=bw; return out

# ---------------- model ----------------
def make_params(rng,V,D,H,ff,nblock,ctx):
    def rn(*s,sc): return T(rng.standard_normal(s)*sc)
    P={}
    P['tok']=rn(V,D,sc=0.02); P['pos']=rn(ctx,D,sc=0.02)
    for b in range(nblock):
        pf=f'b{b}_'
        P[pf+'ln1g']=T(np.ones(D)); P[pf+'ln1b']=T(np.zeros(D))
        P[pf+'Wq']=rn(D,D,sc=1/np.sqrt(D)); P[pf+'bq']=T(np.zeros(D))
        P[pf+'Wk']=rn(D,D,sc=1/np.sqrt(D)); P[pf+'bk']=T(np.zeros(D))
        P[pf+'Wv']=rn(D,D,sc=1/np.sqrt(D)); P[pf+'bv']=T(np.zeros(D))
        P[pf+'Wo']=rn(D,D,sc=1/np.sqrt(D)); P[pf+'bo']=T(np.zeros(D))
        P[pf+'ln2g']=T(np.ones(D)); P[pf+'ln2b']=T(np.zeros(D))
        P[pf+'W1']=rn(D,ff,sc=1/np.sqrt(D)); P[pf+'b1']=T(np.zeros(ff))
        P[pf+'W2']=rn(ff,D,sc=1/np.sqrt(ff)); P[pf+'b2']=T(np.zeros(D))
    P['lng']=T(np.ones(D)); P['lnb']=T(np.zeros(D))
    P['out']=rn(D,V,sc=0.02); P['outb']=T(np.zeros(V))
    return P

def linear(x,W,b): return add(matmul(x,W),b)

def forward(P,idx,cfg):
    B,Tt=idx.shape; D=cfg['D']; H=cfg['H']; dh=D//H; nb=cfg['nblock']
    x=add(embed(P['tok'],idx),embed(P['pos'],np.arange(Tt)))
    m=np.triu(np.ones((Tt,Tt)),1)*-1e9
    maskT=T(m.reshape(1,1,Tt,Tt))
    for b in range(nb):
        pf=f'b{b}_'
        h=layernorm(x,P[pf+'ln1g'],P[pf+'ln1b'])
        q=linear(h,P[pf+'Wq'],P[pf+'bq']); k=linear(h,P[pf+'Wk'],P[pf+'bk']); v=linear(h,P[pf+'Wv'],P[pf+'bv'])
        def heads(t): return swap(reshape(t,(B,Tt,H,dh)),1,2)
        q=heads(q); k=heads(k); v=heads(v)
        sc=matmul(q,swap(k,-1,-2)); sc=mul(sc,1.0/np.sqrt(dh)); sc=add(sc,maskT)
        att=softmax(sc)
        ctx=matmul(att,v)
        ctx=reshape(swap(ctx,1,2),(B,Tt,D))
        x=add(x,linear(ctx,P[pf+'Wo'],P[pf+'bo']))
        h2=layernorm(x,P[pf+'ln2g'],P[pf+'ln2b'])
        ff=linear(relu(linear(h2,P[pf+'W1'],P[pf+'b1'])),P[pf+'W2'],P[pf+'b2'])
        x=add(x,ff)
    x=layernorm(x,P['lng'],P['lnb'])
    return linear(x,P['out'],P['outb'])

def forward_np(P,idx,cfg): return forward(P,idx,cfg).data

class Adam:
    def __init__(s,P,lr,b1=.9,b2=.98,eps=1e-9):
        s.P=P;s.lr=lr;s.b1=b1;s.b2=b2;s.eps=eps;s.t=0
        s.m={k:np.zeros_like(v.data) for k,v in P.items()}
        s.v={k:np.zeros_like(v.data) for k,v in P.items()}
    def step(s):
        s.t+=1
        for k,p in s.P.items():
            g=p.grad
            s.m[k]=s.b1*s.m[k]+(1-s.b1)*g
            s.v[k]=s.b2*s.v[k]+(1-s.b2)*g*g
            mh=s.m[k]/(1-s.b1**s.t); vh=s.v[k]/(1-s.b2**s.t)
            p.data-=s.lr*mh/(np.sqrt(vh)+s.eps)
    def zero(s):
        for p in s.P.values(): p.grad=np.zeros_like(p.data)

# ---------------- MLC compositional grammar (novel-primitive / SCAN-dax) ----------------
# 4 colors x 4 shapes. output(i,j)=(pc[i],ps[j]).  NOVEL primitives = color 3 & shape 3:
# demonstrated in ISOLATION but never COMPOSED during training; must be composed at test.
ID_CW=lambda i:i        # 0..3 color word
ID_SW=lambda j:4+j      # 4..7 shape word
ID_CO=lambda o:8+o      # 8..11 color output
ID_SO=lambda o:12+o     # 12..15 shape output
EQ,SEMI,BAR,END,PAD=16,17,18,19,20
V=21
NC,NS=3,3                                  # novel color, novel shape indices
SEEN=[(i,j) for i in range(3) for j in range(3)]           # 9 composed combos in training
HELD=[(3,0),(0,3),(3,1),(3,3)]             # 4 held-out compositions touching a novel primitive
FIXED_PC=[2,0,3,1]; FIXED_PS=[1,3,0,2]     # ARM A static non-identity grammar
LEN_A=6                                     # padded len of an ARM-A sequence (max = composed)

def rand_perm(rng): return list(rng.permutation(4))

# ---- ARM A base sequences: plain next-byte CE, static grammar, NO in-context study ----
def armA_base(pc,ps):
    seqs=[]
    for i in range(4): seqs.append([ID_CW(i),EQ,ID_CO(pc[i]),END])          # color isolation
    for j in range(4): seqs.append([ID_SW(j),EQ,ID_SO(ps[j]),END])          # shape isolation
    for (i,j) in SEEN:                                                       # seen compositions
        seqs.append([ID_CW(i),ID_SW(j),EQ,ID_CO(pc[i]),ID_SO(ps[j]),END])
    return seqs  # 17 sequences

def pad_seq(s,L): return s+[PAD]*(L-len(s))

def make_batch_A(rng,B,base):
    idxs=rng.integers(0,len(base),size=B)
    arr=np.array([pad_seq(base[t],LEN_A) for t in idxs],dtype=np.int64)
    x=arr[:,:-1]; y=arr[:,1:]
    mask=(y!=PAD).astype(np.float64)
    return x,y,mask

# ---- ARM B episodic: fresh grammar per episode + in-context isolation study ----
def armB_study(rng,pc,ps):
    lessons=[]
    for i in range(4): lessons.append([ID_CW(i),EQ,ID_CO(pc[i]),SEMI])
    for j in range(4): lessons.append([ID_SW(j),EQ,ID_SO(ps[j]),SEMI])
    rng.shuffle(lessons)
    flat=[]; [flat.extend(l) for l in lessons]
    return flat+[BAR]  # 8*4+1 = 33 tokens

def armB_episode(rng,query,pc,ps):
    st=armB_study(rng,pc,ps)
    qi,qj=query
    q=[ID_CW(qi),ID_SW(qj),EQ,ID_CO(pc[qi]),ID_SO(ps[qj]),END]
    return np.array(st+q,dtype=np.int64)  # 33+6 = 39

LEN_B=33+6
EQPOS_B=33+2   # index of query '=' in ARM-B sequence (prefix = 0..EQPOS_B)

def make_batch_B(rng,B):
    arr=np.empty((B,LEN_B),dtype=np.int64)
    for b in range(B):
        q=SEEN[rng.integers(len(SEEN))]
        arr[b]=armB_episode(rng,q,rand_perm(rng),rand_perm(rng))
    x=arr[:,:-1]; y=arr[:,1:]
    mask=np.ones_like(y,dtype=np.float64)
    return x,y,mask

# ---------------- decode + metric ----------------
def greedy2(P,prefix,cfg):
    toks=list(prefix); outs=[]
    for _ in range(2):
        lg=forward_np(P,np.array(toks,dtype=np.int64)[None,:],cfg)[0,-1]
        nt=int(lg.argmax()); outs.append(nt); toks.append(nt)
    return outs

def composed_distinct(P,arm,cfg,eval_rng,R=5):
    solved=set()
    for (qi,qj) in HELD:
        hits=0
        for _ in range(R):
            if arm=='A':
                pc,ps=FIXED_PC,FIXED_PS
                prefix=[ID_CW(qi),ID_SW(qj),EQ]
            else:
                pc,ps=rand_perm(eval_rng),rand_perm(eval_rng)
                seq=armB_episode(eval_rng,(qi,qj),pc,ps)
                prefix=list(seq[:EQPOS_B+1])
            want=[ID_CO(pc[qi]),ID_SO(ps[qj])]
            if greedy2(P,prefix,cfg)==want: hits+=1
        if hits>=3: solved.add((qi,qj))
    return len(solved)

# ---------------- gradcheck ----------------
def gradcheck():
    rng=np.random.default_rng(0)
    cfg=dict(D=8,H=2,nblock=1,ff=16,ctx=32)
    P=make_params(rng,V,cfg['D'],cfg['H'],cfg['ff'],cfg['nblock'],cfg['ctx'])
    B,Tt=2,10
    idx=rng.integers(0,V,size=(B,Tt)); y=rng.integers(0,V,size=(B,Tt)); m=np.ones((B,Tt))
    def loss_of(): return cross_entropy(forward(P,idx,cfg),y,m)
    backward(loss_of())
    keys=['tok','pos','b0_Wq','b0_ln1g','b0_W1','b0_b2','out','lng']
    worst=0.0
    ga_cache={k:P[k].grad.ravel().copy() for k in keys}
    for k in keys:
        flat=P[k].data.ravel(); ga=ga_cache[k]
        for _ in range(6):
            i=rng.integers(flat.size); old=flat[i]; h=1e-6
            flat[i]=old+h; lp=loss_of().data
            flat[i]=old-h; lm=loss_of().data
            flat[i]=old
            num=(lp-lm)/(2*h); ana=ga[i]
            worst=max(worst,abs(num-ana)/(max(abs(num),abs(ana))+1e-12))
    return worst

# ---------------- train + evaluate one arm/seed ----------------
def run(arm,seed,cfg,steps,B,lr):
    rng=np.random.default_rng(seed)
    P=make_params(rng,V,cfg['D'],cfg['H'],cfg['ff'],cfg['nblock'],cfg['ctx'])
    opt=Adam(P,lr)
    base=armA_base(FIXED_PC,FIXED_PS)
    train_acc_num=0
    for s in range(steps):
        x,y,m=(make_batch_A(rng,B,base) if arm=='A' else make_batch_B(rng,B))
        opt.zero()
        L=cross_entropy(forward(P,x,cfg),y,m)
        backward(L); opt.step()
    eval_rng=np.random.default_rng(10_000+seed)
    cd=composed_distinct(P,arm,cfg,eval_rng)
    # sanity: seen-composition accuracy (should be high => training worked)
    if arm=='A':
        seen_ok=sum(greedy2(P,[ID_CW(i),ID_SW(j),EQ],cfg)==[ID_CO(FIXED_PC[i]),ID_SO(FIXED_PS[j])] for (i,j) in SEEN)
    else:
        er=np.random.default_rng(20_000+seed); seen_ok=0
        for (i,j) in SEEN:
            pc,ps=rand_perm(er),rand_perm(er); sq=armB_episode(er,(i,j),pc,ps)
            seen_ok+=greedy2(P,list(sq[:EQPOS_B+1]),cfg)==[ID_CO(pc[i]),ID_SO(ps[j])]
    return cd,float(L.data),seen_ok

if __name__=='__main__':
    t0=time.time()
    worst=gradcheck()
    print(f"[gradcheck] max rel err = {worst:.3e}  ->  {'PASS' if worst<1e-4 else 'FAIL'}",flush=True)
    assert worst<1e-4,"gradcheck FAILED"
    # FROZEN hyperparams (pre-registered; generic toy-transformer defaults, not tuned to metric)
    cfg=dict(D=64,H=4,nblock=2,ff=128,ctx=64)
    STEPS=int(sys.argv[1]) if len(sys.argv)>1 else 4000
    B=32; LR=1.5e-3; SEEDS=[7,4302,4303]
    print(f"cfg={cfg} steps={STEPS} B={B} lr={LR}  SEEN={len(SEEN)} HELD={HELD}",flush=True)
    res={}
    for seed in SEEDS:
        for arm in ('A','B'):
            cd,fl,seen=run(arm,seed,cfg,STEPS,B,LR)
            res[(arm,seed)]=cd
            print(f"  seed={seed} ARM {arm}: composed_distinct={cd}/4  seen_acc={seen}/{len(SEEN)}  (final CE={fl:.3f})  t={time.time()-t0:.0f}s",flush=True)
    print("\n=== composed_distinct (held-out novel-primitive comps /4) ===")
    print("seed  |  A(plain-CE static)  |  B(MLC episodic)")
    for seed in SEEDS:
        print(f"{seed:>5} |         {res[('A',seed)]}            |        {res[('B',seed)]}")
    Bok=all(res[('B',s)]>=3 for s in SEEDS)
    BgtA=all(res[('B',s)]>res[('A',s)] for s in SEEDS)
    verdict="🟢 DIRECTIONAL-GREEN" if (Bok and BgtA) else "🧱 WALL"
    print(f"\nfrozen bar: B>=3 all seeds={Bok} ; B>A all seeds={BgtA}  ->  {verdict}")
