#!/usr/bin/env python3
"""G1 LEVER B1 = V1(sigma-inf) x V2(kappa) x V12(M/G2) — STEP-0 ABC-ABLATION KILL-GATE.

Real-G1-isomorphic toy (mirrors state/g1_gamma_engine_native/step0_gamma_bind_kill.py
and state/g1_lever_step0/{V2_micro_trace,V12_grammar_selfgen}): N concepts split into
two TYPES A x B; every composed sample entangles ONE type-A + ONE type-B constituent
(two-axis entanglement per sample -- recomb bar = emit BOTH, else best_distinct
collapses to log(max)=1). LOSS is reconstruction/next-token (NOT recomb-rigged). Shared
additive-unbind trunk across ALL arms; arms differ only in which of the 3 levers are ON.

  THE 3 LEVERS (toggles on the SAME trunk):
   A = V1 (sigma-inf skeleton-bind): add unbind-SKELETON examples -- each concept
       superposed with MANY distinct opposite-type partners, target = extract the single
       concept. Drives sigma (rule-partner diversity) toward ceiling so the trunk must
       learn a partner-agnostic unbind (sigma=1 => pair-binding FAIL; sigma->inf => general).
   B = V2 (kappa micro-trace): autoregressive COPY-prev-set + exactly-1-local-edit decode
       (set-addressed emit head Wemit, hard-copy dedup). kappa = local-copy ratio maximal.
   C = V12 (M/G2 self-gen): periodic grammar-VERIFIED self-generation (non-STaR) of
       CORPUS-ABSENT A x B pairs, self-labelled by model top-2, folded into train.

  CONTROLS: ADD = 000 baseline (FLOOR). DERIV = echo channel h += Ei+Ej (deriv_margin bar).
  ABLATION 7-arm: A B C AB AC BC ABC (+ ADD DERIV) x 3 seeds.
  SYNERGY (AND hypothesis) = margin(AB) > margin(A)+margin(B) (super-additive).

FROZEN BAR (set BEFORE measuring; c9/p7): N=24 D=64 HELDOUT=0.45 STEPS=4000 LR=3e-3
  seeds {7,4302,4303}. per arm on HELD-OUT pairs: best_distinct{0,1,2}, max_single(=1),
  recomb_rate. margin(X)=recomb(X)-recomb(ADD). deriv_margin=recomb(DERIV)-recomb(ADD).
  PASS iff ABC.bd>=2 AND ABC.bd>max_single AND margin(ABC)>deriv_margin AND super-additive.
  KILL iff ABC.bd<=max_single OR margin(ABC)<=deriv_margin OR no synergy (sub-additive).
JUDGMENT rho/sigma/kappa/M pre-registered; base predicted=(rho~0 AND sigma>1).
SCOPE: TOY numpy = DIRECTIONAL pre-screen (NOT 303M engine-native, NOT terminal).
"""
import numpy as np, json, time, os

N=24; D=64; HELDOUT=0.45; STEPS=4000; LR=3e-3; SEEDS=[7,4302,4303]
TYPE_A=set(range(0,N//2)); TYPE_B=set(range(N//2,N))
def ctype(i): return 0 if i in TYPE_A else 1
SKEL_K=8
WARMUP=800; GEN_EVERY=200; GEN_BATCH=24; AUG_CAP=60
b1a,b2a,eps=0.9,0.999,1e-8

ARMS=[  # (name, skeleton A, trace B, selfgen C, echo)
    ("ADD",  False,False,False,False),
    ("DERIV",False,False,False,True ),
    ("A",    True ,False,False,False),
    ("B",    False,True ,False,False),
    ("C",    False,False,True ,False),
    ("AB",   True ,True ,False,False),
    ("AC",   True ,False,True ,False),
    ("BC",   False,True ,True ,False),
    ("ABC",  True ,True ,True ,False),
]

def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))
def softmax(z): z=z-z.max(1,keepdims=True); e=np.exp(z); return e/e.sum(1,keepdims=True)

def make_data(rng):
    pairs=[(i,j) for i in TYPE_A for j in TYPE_B]
    rng.shuffle(pairs); ncut=int(len(pairs)*(1-HELDOUT))
    return pairs[:ncut], pairs[ncut:]

def sigma_of(pairs):
    part={}
    for (i,j) in pairs:
        part.setdefault(i,set()).add(j); part.setdefault(j,set()).add(i)
    return float(np.mean([len(v) for v in part.values()])) if part else 0.0

def grammar_ok(pred):
    if len(pred)!=2: return False
    a,b=pred; return (a!=b) and (ctype(a)!=ctype(b))

class Model:
    def __init__(self,rng,trace):
        s=1.0/np.sqrt(D); self.trace=trace
        self.P={"E":rng.standard_normal((N,D))*s,
                "Wa":np.eye(D)+rng.standard_normal((D,D))*0.05,
                "Wb":np.eye(D)+rng.standard_normal((D,D))*0.05,
                "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
                "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}
        if trace: self.P["Wemit"]=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.mom={k:np.zeros_like(v) for k,v in self.P.items()}
        self.vel={k:np.zeros_like(v) for k,v in self.P.items()}
    def adam(self,grads,step):
        for k in self.P:
            g=grads[k]; self.mom[k]=b1a*self.mom[k]+(1-b1a)*g; self.vel[k]=b2a*self.vel[k]+(1-b2a)*(g*g)
            mh=self.mom[k]/(1-b1a**step); vh=self.vel[k]/(1-b2a**step); self.P[k]-=LR*mh/(np.sqrt(vh)+eps)
    def fwd_shot(self,I,J,echo):
        P=self.P; a=P["E"][I]; b=P["E"][J]; pa=a@P["Wa"].T; pb=b@P["Wb"].T
        h=pa+pb
        if echo: h=h+a+b
        z1=h@P["W1"].T+P["b1"]; z=gelu(z1); logits=z@P["W2"].T+P["b2"]
        return logits,(I,J,a,b,pa,pb,h,z1,z,echo)
    def bwd_shot(self,cache,Y):
        P=self.P; I,J,a,b,pa,pb,h,z1,z,echo=cache; B=len(I)
        dlogits=(sigmoid(z@P["W2"].T+P["b2"])-Y)/N
        g={k:np.zeros_like(v) for k,v in P.items()}
        g["W2"]=dlogits.T@z; g["b2"]=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        g["W1"]=dz1.T@h; g["b1"]=dz1.sum(0)
        dh=dz1@P["W1"]; dpa=dh; dpb=dh
        g["Wa"]=dpa.T@a; g["Wb"]=dpb.T@b
        dEi=dpa@P["Wa"]; dEj=dpb@P["Wb"]
        if echo: dEi=dEi+dh; dEj=dEj+dh
        np.add.at(g["E"],I,dEi); np.add.at(g["E"],J,dEj)
        return {k:v/B for k,v in g.items()}
    def fwd_trace(self,I,J,Mem):
        P=self.P; a=P["E"][I]; b=P["E"][J]; pa=a@P["Wa"].T; pb=b@P["Wb"].T
        pemE=Mem@P["E"]; pem=pemE@P["Wemit"].T; ctx=pa+pb+pem
        z1=ctx@P["W1"].T+P["b1"]; z=gelu(z1); logits=z@P["W2"].T+P["b2"]
        return logits,(I,J,a,b,pemE,ctx,z1,z,Mem)
    def bwd_trace(self,cache,tgt):
        P=self.P; I,J,a,b,pemE,ctx,z1,z,Mem=cache; B=len(I)
        oh=np.zeros((B,N)); oh[np.arange(B),tgt]=1.0
        pr=softmax(z@P["W2"].T+P["b2"]); dlogits=(pr-oh)/B
        g={k:np.zeros_like(v) for k,v in P.items()}
        g["W2"]=dlogits.T@z; g["b2"]=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        g["W1"]=dz1.T@ctx; g["b1"]=dz1.sum(0)
        dctx=dz1@P["W1"]; dpa=dctx; dpb=dctx; dpem=dctx
        g["Wa"]=dpa.T@a; g["Wb"]=dpb.T@b
        g["Wemit"]=dpem.T@pemE
        dEi=dpa@P["Wa"]; dEj=dpb@P["Wb"]; dEmem=dpem@P["Wemit"]
        np.add.at(g["E"],I,dEi); np.add.at(g["E"],J,dEj)
        g["E"]=g["E"]+Mem.T@dEmem
        return {k:v/B for k,v in g.items()}
    def decode_shot(self,i,j,echo):
        logits,_=self.fwd_shot(np.array([i]),np.array([j]),echo)
        return set(np.argsort(logits[0])[-2:].tolist())
    def decode_trace(self,i,j):
        emitted=[]
        for t in range(2):
            Mem=np.zeros((1,N))
            for e in emitted: Mem[0,e]=1.0
            logits,_=self.fwd_trace(np.array([i]),np.array([j]),Mem)
            order=np.argsort(logits[0])[::-1]
            nxt=next((int(k) for k in order if int(k) not in emitted),int(order[0]))
            emitted.append(nxt)
        return set(emitted)

def skeleton_shot(rng):
    I=[];J=[];TGT=[]
    for c in range(N):
        opp=list(TYPE_B) if c in TYPE_A else list(TYPE_A)
        parts=rng.choice(opp,size=min(SKEL_K,len(opp)),replace=False)
        for p in parts:
            if c in TYPE_A: I.append(c); J.append(int(p)); TGT.append(c)
            else:           I.append(int(p)); J.append(c); TGT.append(c)
    return I,J,TGT

def base_shot(trp):
    I=[i for i in range(N)]; J=[i for i in range(N)]; TGT=[[i] for i in range(N)]
    for (i,j) in trp: I.append(i); J.append(j); TGT.append([i,j])
    return I,J,TGT

def base_trace(trp):
    I=[];J=[];MEM=[];TGT=[]
    for i in range(N):
        I.append(i);J.append(i);MEM.append([]);TGT.append(i)
    for (i,j) in trp:
        st=sorted([i,j])
        for t in range(2):
            I.append(i);J.append(j);MEM.append(st[:t]);TGT.append(st[t])
    return I,J,MEM,TGT

def to_Y(tgtlists):
    Y=np.zeros((len(tgtlists),N))
    for r,t in enumerate(tgtlists): Y[r,np.array(t)]=1.0
    return Y

def to_Mem(memlists):
    M=np.zeros((len(memlists),N))
    for r,e in enumerate(memlists):
        if len(e): M[r,np.array(e,dtype=int)]=1.0
    return M

def train_arm(cfg,seed):
    name,A,B,C,echo=cfg
    rng=np.random.default_rng(seed); m=Model(rng,trace=B)
    trp,tep=make_data(rng); trp_set=set(trp)
    accepted=[]; proposed=rejected=0
    if A: skI,skJ,skT=skeleton_shot(rng)
    if not B: bI,bJ,bTGT=base_shot(trp)
    else: bI,bJ,bMEM,bTGT=base_trace(trp)
    aug=[]
    for step in range(1,STEPS+1):
        if C and step>WARMUP and step%GEN_EVERY==0:
            new=[]
            for _ in range(GEN_BATCH):
                i=int(rng.integers(0,N//2)); j=int(rng.integers(N//2,N))
                if (i,j) in trp_set: continue
                pred=(m.decode_trace(i,j) if B else m.decode_shot(i,j,echo)); proposed+=1
                if not grammar_ok(sorted(pred)): rejected+=1; continue
                lab=sorted(pred); accepted.append(tuple(lab)); new.append((i,j,lab))
            aug.extend(new); aug=aug[-AUG_CAP:]
        if not B:
            I=list(bI); J=list(bJ); TG=[list(t) for t in bTGT]
            if A: I+=skI; J+=skJ; TG+=[[t] for t in skT]
            for (i,j,lab) in aug: I+=[i];J+=[j];TG+=[list(lab)]
            I=np.array(I);J=np.array(J);Y=to_Y(TG)
            logits,cache=m.fwd_shot(I,J,echo); grads=m.bwd_shot(cache,Y)
        else:
            I=list(bI); J=list(bJ); MEM=[list(e) for e in bMEM]; TG=list(bTGT)
            if A: I+=skI; J+=skJ; MEM+=[[] for _ in skT]; TG+=list(skT)
            for (i,j,lab) in aug:
                st=sorted(lab)
                for t in range(2): I+=[i];J+=[j];MEM+=[st[:t]];TG+=[st[t]]
            I=np.array(I);J=np.array(J);Mem=to_Mem(MEM);TG=np.array(TG)
            logits,cache=m.fwd_trace(I,J,Mem); grads=m.bwd_trace(cache,TG)
        m.adam(grads,step)
    per=[]
    for (i,j) in tep:
        em=(m.decode_trace(i,j) if B else m.decode_shot(i,j,echo))
        per.append((1 if i in em else 0)+(1 if j in em else 0))
    per=np.array(per)
    ms=max((1 if i in (m.decode_trace(i,i) if B else m.decode_shot(i,i,echo)) else 0) for i in range(N))
    info={"best_distinct":int(per.max()),"recomb_rate":float(np.mean(per==2)),
          "mean_bd":float(per.mean()),"max_single":int(ms),
          "gen_sigma":sigma_of(accepted),"n_accepted":len(accepted),
          "n_rejected":rejected,"sigma_train":sigma_of(trp)}
    return m,trp,tep,info

def predictors(trp,tep,arm_has_skel):
    train_singles=set(range(N)); tot=miss=0
    for (i,j) in tep:
        for k in (i,j):
            tot+=1
            if k not in train_singles: miss+=1
    rho=miss/max(1,tot); sig=sigma_of(trp)
    sig_skel=sig+(SKEL_K if arm_has_skel else 0.0)
    kappa_trace=float(np.mean([t/(t+1) for t in range(2)]))
    full=len(trp)+len(tep); tau=2; glen=2; M=(len(tep)/full)*(tau/glen)
    return {"rho_echo_residual":round(rho,4),"sigma_train":round(sig,3),
            "sigma_eff_with_skeleton":round(sig_skel,3),
            "kappa_local_copy_trace":round(kappa_trace,4),"delta_copy_vs_RF":1.0,
            "M_memo_disadvantage":round(M,4),"tau":tau,"grammar_len":glen}

def main():
    t0=time.time(); res={c[0]:{"bd":[],"rr":[],"mbd":[],"ms":[],"gs":[],"nacc":[],"nrej":[]} for c in ARMS}
    preds=None; preds_skel=None
    for seed in SEEDS:
        for cfg in ARMS:
            name=cfg[0]; m,trp,tep,info=train_arm(cfg,seed)
            if preds is None: preds=predictors(trp,tep,False); preds_skel=predictors(trp,tep,True)
            r=res[name]
            r["bd"].append(info["best_distinct"]); r["rr"].append(info["recomb_rate"])
            r["mbd"].append(info["mean_bd"]); r["ms"].append(info["max_single"])
            r["gs"].append(info["gen_sigma"]); r["nacc"].append(info["n_accepted"]); r["nrej"].append(info["n_rejected"])
            print(f"[seed {seed}] {name:5s} bd={info['best_distinct']} recomb={info['recomb_rate']:.3f} "
                  f"mean_bd={info['mean_bd']:.3f} max_single={info['max_single']} "
                  f"gen_sigma={info['gen_sigma']:.2f} nacc={info['n_accepted']}",flush=True)
    summ={}
    for c in ARMS:
        a=c[0]
        summ[a]={"best_distinct_max":int(max(res[a]["bd"])),"best_distinct_seeds":res[a]["bd"],
                 "recomb_rate_mean":float(np.mean(res[a]["rr"])),
                 "recomb_rate_seeds":[round(x,3) for x in res[a]["rr"]],
                 "mean_bd_mean":float(np.mean(res[a]["mbd"])),"max_single":int(max(res[a]["ms"])),
                 "gen_sigma_mean":float(np.mean(res[a]["gs"])),
                 "n_accepted_mean":float(np.mean(res[a]["nacc"]))}
    add=summ["ADD"]["recomb_rate_mean"]
    def marg(a): return summ[a]["recomb_rate_mean"]-add
    deriv_margin=marg("DERIV")
    mA,mB,mC=marg("A"),marg("B"),marg("C")
    mAB,mAC,mBC,mABC=marg("AB"),marg("AC"),marg("BC"),marg("ABC")
    synergy={"AB_vs_A+B":round(mAB-(mA+mB),4),"AC_vs_A+C":round(mAC-(mA+mC),4),
             "BC_vs_B+C":round(mBC-(mB+mC),4),"ABC_vs_A+B+C":round(mABC-(mA+mB+mC),4)}
    any_synergy=any(v>1e-6 for v in synergy.values())
    abc_bd=summ["ABC"]["best_distinct_max"]; max_single=summ["ABC"]["max_single"]
    passed=(abc_bd>=2) and (abc_bd>max_single) and (mABC>deriv_margin) and (synergy["ABC_vs_A+B+C"]>1e-6)
    predicted_base=(preds["rho_echo_residual"]<=0.05) and (preds["sigma_train"]>1.0)
    verdict=("PRE-SELECT PASS (ABC super-additive AND beats deriv margin AND bd>=2 => GPU escalation candidate)"
             if passed else
             "KILL (ABC sub-additive OR margin<=deriv_margin OR bd<=max_single => AND-stack FALSIFIED DIRECTIONAL, NO GPU rent)")
    out={"experiment":"G1 lever B1 V1(sigma-inf)xV2(kappa)xV12(M/G2) STEP-0 ABC-ablation cheap kill",
         "scope":"TOY numpy DIRECTIONAL pre-screen (NOT 303M engine-native, NOT terminal)",
         "config":{"N":N,"D":D,"HELDOUT":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS,
                   "SKEL_K":SKEL_K,"WARMUP":WARMUP,"GEN_EVERY":GEN_EVERY,"GEN_BATCH":GEN_BATCH,"AUG_CAP":AUG_CAP},
         "frozen_bar":("held-out recomb_rate per arm; margin(X)=recomb(X)-recomb(ADD); "
                       "PASS iff ABC.bd>=2 AND ABC.bd>max_single AND margin(ABC)>deriv_margin AND super-additive"),
         "predictors_base":preds,"predictors_with_skeleton":preds_skel,"arms":summ,
         "margins":{"A":round(mA,4),"B":round(mB,4),"C":round(mC,4),
                    "AB":round(mAB,4),"AC":round(mAC,4),"BC":round(mBC,4),"ABC":round(mABC,4),
                    "DERIV":round(deriv_margin,4)},
         "synergy_superadditive":synergy,"any_synergy":bool(any_synergy),
         "ADD_recomb":add,"DERIV_recomb":summ["DERIV"]["recomb_rate_mean"],"ABC_recomb":summ["ABC"]["recomb_rate_mean"],
         "ABC_best_distinct":abc_bd,"max_single":max_single,
         "deriv_margin":round(deriv_margin,4),"lever_margin_ABC":round(mABC,4),
         "PASS":bool(passed),"predicted_base_criterion":bool(predicted_base),
         "VERDICT":verdict,"wall_sec":round(time.time()-t0,1)}
    d=os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(d,"result.json"),"w").write(json.dumps(out,indent=2))
    print(json.dumps({"margins":out["margins"],"synergy":synergy,"PASS":passed,"VERDICT":verdict},indent=2))
if __name__=="__main__": main()
