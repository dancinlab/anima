#!/usr/bin/env python3
"""G1 LEVER V12 — grammar-verified self-gen (non-STaR) — STEP-0 CHEAP KILL-GATE.

Replicates the real-G1-isomorphic toy of state/g1_gamma_engine_native/
step0_gamma_bind_kill.py (N concepts, held-out composed pairs, two-keyword
recombination best_distinct, manual-grad, torch-free numpy). TARGET-FORMAT is
swapped: arms differ in the TRAINING-DATA pipeline (V12 is a data-manufacture
lever, not a combiner-op lever). All arms share ONE additive unbinding trunk +
learned projections + nonlinear multi-hot readout.

  ADD   : additive-control (MATCHED to V12) — superposed input h=Wa@Ei+Wb@Ej, must
          UNBIND both constituents; train on singles + seen composed pairs ONLY.
          No augmentation. = FLOOR.
  DERIV : derivtrace baseline (bd=2 reference margin; the campaign's only surviving
          G1 lift). derivation-trace target-format = echo channel h += Ei+Ej so
          emitting both constituents becomes an ECHO/copy (echo=composition, CE=echo
          broken). Positive control; its held-out margin over ADD = the deriv_margin
          bar a NEW lever must clear to be worth GPU.
  V12   : the LEVER — grammar-VERIFIED self-gen. Same trunk as ADD (must genuinely
          unbind, NO echo). Periodically self-generates CORPUS-ABSENT pairs, takes
          its own top-2 derivation, keeps ONLY grammar-passing ones (2 distinct
          constituents of DIFFERENT type A x B), self-labels (non-STaR: grammar
          filter, NOT ground-truth answer) and adds them to train. Manufactures
          corpus-absent combinations (targets G2 novelty).

GENERATOR sigma-collapse GATE (crux for this lever): measure sigma (rule-partner
diversity) of the ACCEPTED self-gen corpus. sigma->1 (each concept self-gens with
only one partner) => generator degenerate => G2 invalid. Predicted: sigma
maintained (>1) => G2 novelty up.

FROZEN BAR (set BEFORE measuring; no post-hoc move — c9/p7):
  real-G1-isomorphic toy: N=24, D=64, heldout~=0.45, 4000 step, seeds {7,4302,4303}.
  per arm on HELD-OUT composed pairs:
    best_distinct = max over held-out prompts of (#target constituents in top-2)  {0,1,2}
    max_single    = max over single prompts of (#target in top-2)                  (=1)
    recomb_rate   = fraction of held-out prompts with both constituents in top-2   (margin score)
  deriv_margin = DERIV.recomb_rate - ADD.recomb_rate
  lever_margin = V12.recomb_rate   - ADD.recomb_rate
  PASS (pre-select, GPU-escalation candidate) iff
     V12.best_distinct >= 2  AND  V12.best_distinct > max_single  AND  lever_margin > deriv_margin.
  KILL iff  V12.best_distinct <= max_single  OR  lever_margin <= deriv_margin.

PRE-REGISTERED PREDICTION (rho/sigma/kappa/M judgment criterion; before run):
  base rule `predicted` field = (rho~=0 AND sigma_train>1) => recomb-eligible.
  V12-specific refinement (reported in notes, NOT the field): grammar-only self-
  labels tend to COLLAPSE generator sigma (confirmation loop on the model's own
  wrong labels) => V12 unlikely to beat the strong derivtrace-echo margin; a MISS
  of the base criterion here => generator-sigma is the better predictor.

SCOPE: TOY numpy = DIRECTIONAL pre-screen (a_engine_native_learning: NOT 303M
engine-native, NOT terminal). Purpose = gate GPU spend. Numbers verbatim, no tune-to-green.
"""
import numpy as np, json, time, os

# ---- FROZEN BAR ----
N=24; D=64; HELDOUT=0.45; STEPS=4000; LR=3e-3; SEEDS=[7,4302,4303]
ARMS=["ADD","DERIV","V12"]
TYPE_A=set(range(0,N//2)); TYPE_B=set(range(N//2,N))   # toy grammar: A x B compositions
def ctype(i): return 0 if i in TYPE_A else 1
WARMUP=800; GEN_EVERY=200; GEN_BATCH=24; AUG_CAP=60     # self-gen schedule

def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))

class Model:
    def __init__(self,rng):
        s=1.0/np.sqrt(D)
        self.E=rng.standard_normal((N,D))*s
        self.Wa=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.Wb=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.W1=rng.standard_normal((D,D))*s; self.b1=np.zeros(D)
        self.W2=rng.standard_normal((N,D))*s; self.b2=np.zeros(N)
    def forward(self,i,j,echo=False):
        a=self.E[i]; b=self.E[j]; pa=self.Wa@a; pb=self.Wb@b
        h=pa+pb
        if echo: h=h+a+b                     # derivtrace echo channel (DERIV only)
        z1=self.W1@h+self.b1; z=gelu(z1)
        logits=self.W2@z+self.b2
        return logits,(i,j,a,b,pa,pb,h,z1,z,logits,echo)
    def backward(self,cache,target,grads):
        i,j,a,b,pa,pb,h,z1,z,logits,echo=cache
        p=sigmoid(logits); dlogits=(p-target)/N
        grads["W2"]+=np.outer(dlogits,z); grads["b2"]+=dlogits
        dz=self.W2.T@dlogits; dz1=dz*dgelu(z1)
        grads["W1"]+=np.outer(dz1,h); grads["b1"]+=dz1
        dh=self.W1.T@dz1; dpa=dh; dpb=dh
        grads["Wa"]+=np.outer(dpa,a); grads["Wb"]+=np.outer(dpb,b)
        gEi=self.Wa.T@dpa; gEj=self.Wb.T@dpb
        if echo: gEi=gEi+dh; gEj=gEj+dh      # echo path grad to raw embeddings
        grads["E"][i]+=gEi; grads["E"][j]+=gEj
    def params(self):
        return {"E":self.E,"Wa":self.Wa,"Wb":self.Wb,"W1":self.W1,"b1":self.b1,"W2":self.W2,"b2":self.b2}
    def top2(self,i,j,echo=False):
        logits,_=self.forward(i,j,echo); return np.argsort(logits)[-2:].tolist()

def make_data(rng):
    pairs=[(i,j) for i in TYPE_A for j in TYPE_B]      # valid space = A x B = 144
    rng.shuffle(pairs); ncut=int(len(pairs)*(1-HELDOUT))
    return pairs[:ncut], pairs[ncut:]

def tvec(idxs):
    y=np.zeros(N)
    for k in idxs: y[k]=1.0
    return y

def grammar_ok(pred):
    if len(pred)!=2: return False
    a,b=pred
    if a==b: return False
    return ctype(a)!=ctype(b)                          # DIFFERENT type = well-typed derivation

def sigma_of(pairs):
    part={}
    for (i,j) in pairs:
        part.setdefault(i,set()).add(j); part.setdefault(j,set()).add(i)
    return float(np.mean([len(v) for v in part.values()])) if part else 0.0

def train_arm(arm,seed):
    rng=np.random.default_rng(seed); m=Model(rng)
    trp,tep=make_data(rng)
    trp_set=set(trp)|set((j,i) for (i,j) in trp)
    echo=(arm=="DERIV")
    base=[(i,i,(i,)) for i in range(N)]+[(i,j,(i,j)) for (i,j) in trp]
    P=m.params(); mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    b1a,b2a,eps=0.9,0.999,1e-8
    aug=[]; accepted=[]; proposed=rejected=0
    for step in range(1,STEPS+1):
        if arm=="V12" and step>WARMUP and step%GEN_EVERY==0:
            new=[]
            for _ in range(GEN_BATCH):
                i=int(rng.integers(0,N//2)); j=int(rng.integers(N//2,N))
                if (i,j) in trp_set: continue
                pred=m.top2(i,j); proposed+=1
                if not grammar_ok(pred): rejected+=1; continue      # GRAMMAR filter (non-STaR)
                lab=tuple(sorted(set(pred)))                        # self-label = model's own top-2
                new.append((i,j,lab)); accepted.append(lab)
            aug.extend(new); aug=aug[-AUG_CAP:]
        data=base+[(i,j,tgt) for (i,j,tgt) in aug]
        grads={k:np.zeros_like(v) for k,v in P.items()}; rng.shuffle(data)
        for (i,j,tgt) in data:
            _,cache=m.forward(i,j,echo); m.backward(cache,tvec(tgt),grads)
        inv=1.0/len(data)
        for k in P:
            g=grads[k]*inv; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
            mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)
    info={"gen_sigma":sigma_of(accepted),"n_accepted":len(accepted),
          "n_proposed":proposed,"n_rejected":rejected,"sigma_train":sigma_of(trp),"echo":echo}
    return m,trp,tep,info

def eval_heldout(m,pairs,echo=False):
    per=[]
    for (i,j) in pairs:
        t2=set(m.top2(i,j,echo)); c=(1 if i in t2 else 0)+(1 if j in t2 else 0); per.append(c)
    per=np.array(per)
    return int(per.max()), float(np.mean(per==2)), float(per.mean())

def eval_single(m,echo=False):
    return int(max(1 if i in set(m.top2(i,i,echo)) else 0 for i in range(N)))

def compute_predictors(trp,tep):
    train_singles=set(range(N))                        # every (k,k) present in train
    tot=miss=0
    for (i,j) in tep:
        for k in (i,j):
            tot+=1
            if k not in train_singles: miss+=1
    rho=miss/max(1,tot)
    sig=sigma_of(trp)
    kappa=0.0; delta_copy_rf=1.0                        # summed input: no local copy, RF must span both slots
    full=len(trp)+len(tep); tau=2; grammar_len=2
    M=(len(tep)/full)*(tau/grammar_len)
    return {"rho_echo_residual":round(rho,4),"sigma_train_partner_div":round(sig,3),
            "kappa_local_copy":round(kappa,3),"delta_copy_vs_RF":round(delta_copy_rf,3),
            "M_memo_disadvantage":round(M,4),"tau":tau,"grammar_len":grammar_len}

def main():
    t0=time.time()
    res={a:{"bd":[],"rr":[],"mbd":[],"ms":[],"gs":[],"nacc":[],"nrej":[]} for a in ARMS}
    preds=None
    for seed in SEEDS:
        for arm in ARMS:
            m,trp,tep,info=train_arm(arm,seed)
            if preds is None: preds=compute_predictors(trp,tep)
            e=info["echo"]
            bd,rr,mbd=eval_heldout(m,tep,e); ms=eval_single(m,e)
            res[arm]["bd"].append(bd); res[arm]["rr"].append(rr); res[arm]["mbd"].append(mbd)
            res[arm]["ms"].append(ms); res[arm]["gs"].append(info["gen_sigma"])
            res[arm]["nacc"].append(info["n_accepted"]); res[arm]["nrej"].append(info["n_rejected"])
            print(f"[seed {seed}] {arm:5s} best_distinct={bd} recomb_rate={rr:.3f} mean_bd={mbd:.3f} "
                  f"max_single={ms} gen_sigma={info['gen_sigma']:.2f} nacc={info['n_accepted']} "
                  f"nrej={info['n_rejected']}",flush=True)
    summ={}
    for a in ARMS:
        summ[a]={"best_distinct_max":int(max(res[a]["bd"])),"best_distinct_seeds":res[a]["bd"],
                 "recomb_rate_mean":float(np.mean(res[a]["rr"])),
                 "recomb_rate_seeds":[round(x,3) for x in res[a]["rr"]],
                 "mean_bd_mean":float(np.mean(res[a]["mbd"])),"max_single":int(max(res[a]["ms"])),
                 "gen_sigma_mean":float(np.mean(res[a]["gs"])),
                 "n_accepted_mean":float(np.mean(res[a]["nacc"])),
                 "n_rejected_mean":float(np.mean(res[a]["nrej"]))}
    add_rr=summ["ADD"]["recomb_rate_mean"]
    deriv_margin=summ["DERIV"]["recomb_rate_mean"]-add_rr
    lever_margin=summ["V12"]["recomb_rate_mean"]-add_rr
    v12_bd=summ["V12"]["best_distinct_max"]; max_single=summ["V12"]["max_single"]
    passed=(v12_bd>=2) and (v12_bd>max_single) and (lever_margin>deriv_margin)
    predicted_base=(preds["rho_echo_residual"]<=0.05) and (preds["sigma_train_partner_div"]>1.0)
    verdict=("PRE-SELECT PASS (grammar-filtered self-gen beats deriv margin & bd>=2 => GPU escalation candidate)"
             if passed else
             "KILL (lever_margin <= deriv_margin OR bd<=max_single => DIRECTIONAL FALSIFIED, NO GPU rent)")
    out={"experiment":"G1 lever V12 grammar-verified self-gen (non-STaR) STEP-0 cheap kill",
         "scope":"TOY numpy DIRECTIONAL pre-screen (a_engine_native_learning: NOT 303M engine-native, NOT terminal)",
         "config":{"N":N,"D":D,"HELDOUT":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS,
                   "WARMUP":WARMUP,"GEN_EVERY":GEN_EVERY,"GEN_BATCH":GEN_BATCH,"AUG_CAP":AUG_CAP},
         "frozen_bar":("held-out best_distinct(both constituents top-2), max_single, recomb_rate per arm; "
                       "PASS iff V12.bd>=2 AND V12.bd>max_single AND (V12-ADD margin)>(DERIV-ADD margin)"),
         "predictors_rho_sigma_kappa_M":preds,"arms":summ,
         "ADD_recomb_rate":add_rr,"DERIV_recomb_rate":summ["DERIV"]["recomb_rate_mean"],
         "V12_recomb_rate":summ["V12"]["recomb_rate_mean"],
         "deriv_margin":deriv_margin,"lever_margin":lever_margin,
         "V12_best_distinct":v12_bd,"max_single":max_single,
         "V12_gen_sigma":summ["V12"]["gen_sigma_mean"],
         "PASS":bool(passed),"predicted_base_criterion":bool(predicted_base),
         "VERDICT":verdict,"wall_sec":round(time.time()-t0,1)}
    print(json.dumps(out,indent=2))
    d=os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(d,"result.json"),"w").write(json.dumps(out,indent=2))
if __name__=="__main__": main()
