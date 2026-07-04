#!/usr/bin/env python3
"""G1 LEVER V13 resolution-ladder — STEP-0 CHEAP ENGINE-NATIVE KILL (torch-free numpy).

Real-G1-isomorphic controlled toy (clone of state/g1_gamma_engine_native/step0_gamma_
bind_kill.py pattern) — two concepts -> emit BOTH constituents' keywords = held-out
recombination, under next-token/reconstruction loss (NOT recomb-rigged). ALL arms share
the SAME ADDITIVE trunk combiner (h = pa + pb); arms differ ONLY in the OBJECTIVE/target-
FORMAT axis via a resolution-ladder schedule p_full(step) that decides, per pair per step,
whether the example is emitted at FULL resolution (answer head + two derivation-trace heads
supervised: dA->i, dB->j) or FLAT resolution (answer head only).

  ADD    : p_full = 0 constant           (additive-control; FLAT-only; NO derivation)
  DERIV  : p_full = 1 constant           (derivtrace baseline; derivation ALWAYS on)
  LADDER : p_full anneals 1.0 -> 0.0      (V13 resolution ladder: start FULL, descend to
                                           FLAT -> tests whether emitting FULL derivation
                                           INDUCES FLAT internalization = the lever premise)

Frozen metric (identical all arms): held-out FLAT recombination = ans-head top-2 contains
BOTH {i,j}, evaluated WITHOUT emitting derivation (internalized path). emit-derivation-vs-
internalization discriminator.

FROZEN BAR (set before measuring; no post-hoc move — c9/p7):
  N=24, D=64, HELDOUT=0.45, STEPS=4000, seeds {7,4302,4303}. 3 arms = ADD + DERIV + LADDER.
  PASS(lever) = held-out best_distinct>=2 (count) AND best_distinct>max_single (count)
                AND margin(LADDER-ADD) > margin(DERIV-ADD).
  KILL        = LADDER <= ADD  OR  LADDER margin <= DERIV margin.

Predictors (measured $0, pre-registered): rho echo-residual, sigma partner-diversity,
kappa local-copy-ratio + delta_copy vs RF, M memorization-disadvantage.

DIRECTIONAL only (a_engine_native_learning): toy numpy, NOT 303M engine-native, NOT terminal.
"""
import numpy as np, json, time
N=24; D=64; HELDOUT=0.45; STEPS=4000; LR=3e-3; SEEDS=[7,4302,4303]
ARMS=["ADD","DERIV","LADDER"]
OUT="/Users/mini/dancinlab/anima/state/g1_lever_step0/V13_resolution_ladder/result.json"

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
        self.Wans=rng.standard_normal((N,D))*s; self.bans=np.zeros(N)
        self.Wda =rng.standard_normal((N,D))*s; self.bda =np.zeros(N)
        self.Wdb =rng.standard_normal((N,D))*s; self.bdb =np.zeros(N)
    def forward(self,i,j):
        a=self.E[i]; b=self.E[j]; pa=self.Wa@a; pb=self.Wb@b
        h=pa+pb
        z1=self.W1@h+self.b1; z=gelu(z1)
        ans=self.Wans@z+self.bans; da=self.Wda@z+self.bda; db=self.Wdb@z+self.bdb
        return ans,(i,j,a,b,pa,pb,h,z1,z,ans,da,db)
    def backward(self,cache,tgt_ans,tgt_da,tgt_db,full,grads):
        i,j,a,b,pa,pb,h,z1,z,ans,da,db=cache
        dz=np.zeros(D)
        pA=sigmoid(ans); dans=(pA-tgt_ans)/N
        grads["Wans"]+=np.outer(dans,z); grads["bans"]+=dans; dz+=self.Wans.T@dans
        if full:
            pDA=sigmoid(da); dda=(pDA-tgt_da)/N
            grads["Wda"]+=np.outer(dda,z); grads["bda"]+=dda; dz+=self.Wda.T@dda
            pDB=sigmoid(db); ddb=(pDB-tgt_db)/N
            grads["Wdb"]+=np.outer(ddb,z); grads["bdb"]+=ddb; dz+=self.Wdb.T@ddb
        dz1=dz*dgelu(z1)
        grads["W1"]+=np.outer(dz1,h); grads["b1"]+=dz1
        dh=self.W1.T@dz1; dpa=dh; dpb=dh
        grads["Wa"]+=np.outer(dpa,a); grads["Wb"]+=np.outer(dpb,b)
        grads["E"][i]+=self.Wa.T@dpa; grads["E"][j]+=self.Wb.T@dpb
    def params(self):
        return {k:getattr(self,k) for k in
                ["E","Wa","Wb","W1","b1","Wans","bans","Wda","bda","Wdb","bdb"]}

def make_data(rng):
    pairs=[(i,j) for i in range(N) for j in range(i+1,N)]; rng.shuffle(pairs)
    ncut=int(len(pairs)*(1-HELDOUT)); return pairs[:ncut],pairs[ncut:]
def onehot(k):
    y=np.zeros(N); y[k]=1.0; return y
def multihot(idxs):
    y=np.zeros(N)
    for k in idxs: y[k]=1.0
    return y
def p_full_of(arm,step):
    if arm=="ADD":   return 0.0
    if arm=="DERIV": return 1.0
    return max(0.0, 1.0 - (step-1)/(STEPS-1))

def train_arm(arm,seed):
    rng=np.random.default_rng(seed); m=Model(rng)
    trp,tep=make_data(rng)
    data=[(i,i,(i,)) for i in range(N)]+[(i,j,(i,j)) for (i,j) in trp]
    P=m.params(); mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    b1a,b2a,eps=0.9,0.999,1e-8
    for step in range(1,STEPS+1):
        pf=p_full_of(arm,step)
        grads={k:np.zeros_like(v) for k,v in P.items()}; rng.shuffle(data)
        for (i,j,tgt) in data:
            _,cache=m.forward(i,j)
            full=(rng.random()<pf)
            m.backward(cache, multihot(tgt), onehot(i), onehot(j), full, grads)
        inv=1.0/len(data)
        for k in P:
            g=grads[k]*inv; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
            mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)
    return m,trp,tep

def eval_flat(m,pairs):
    both=0; single=0
    for (i,j) in pairs:
        ans,_=m.forward(i,j); top2=set(np.argsort(ans)[-2:].tolist())
        nhit=len({i,j}&top2)
        if nhit==2: both+=1
        elif nhit==1: single+=1
    n=max(1,len(pairs))
    return both/n, both, single, n
def eval_single_acc(m):
    ok=0
    for i in range(N):
        ans,_=m.forward(i,i)
        if int(np.argmax(ans))==i: ok+=1
    return ok/N

def compute_predictors(seed):
    rng=np.random.default_rng(seed); trp,tep=make_data(rng)
    seen=set(range(N))
    for (i,j) in trp: seen.add(i); seen.add(j)
    tot=0; miss=0
    for (i,j) in tep:
        for k in (i,j):
            tot+=1
            if k not in seen: miss+=1
    rho=miss/max(1,tot)
    partners={k:set() for k in range(N)}
    for (i,j) in trp: partners[i].add(j); partners[j].add(i)
    sig=float(np.mean([len(partners[k]) for k in range(N)]))
    delta_copy=1; kappa=1.0
    M=len(tep)/float(N)
    return dict(rho=round(rho,4), sigma=round(sig,3), kappa=kappa,
                delta_copy=delta_copy, RF="inf(global)", M=round(M,3),
                n_train=len(trp), n_heldout=len(tep))

def main():
    t0=time.time(); res={a:{"rate":[],"bd":[],"ms":[],"n":[],"sa":[]} for a in ARMS}
    for seed in SEEDS:
        for arm in ARMS:
            m,trp,tep=train_arm(arm,seed)
            rate,both,single,n=eval_flat(m,tep); sa=eval_single_acc(m)
            res[arm]["rate"].append(rate); res[arm]["bd"].append(both)
            res[arm]["ms"].append(single); res[arm]["n"].append(n); res[arm]["sa"].append(sa)
            print(f"[seed {seed}] {arm:7s} FLAT_recomb={rate:.3f} best_distinct(both)={both} "
                  f"single_only={single}/{n} single_acc={sa:.3f}",flush=True)
    def mean(a,k): return float(np.mean(res[a][k]))
    summ={a:{"flat_recomb_mean":round(mean(a,"rate"),4),
             "flat_recomb_seeds":[round(x,3) for x in res[a]["rate"]],
             "best_distinct_count_seeds":res[a]["bd"],
             "best_distinct_count_mean":round(mean(a,"bd"),2),
             "max_single_count_seeds":res[a]["ms"],
             "max_single_count_mean":round(mean(a,"ms"),2),
             "single_acc_mean":round(mean(a,"sa"),3)} for a in ARMS}
    add=summ["ADD"]["flat_recomb_mean"]; drv=summ["DERIV"]["flat_recomb_mean"]; lad=summ["LADDER"]["flat_recomb_mean"]
    lever_margin=round(lad-add,4); deriv_margin=round(drv-add,4)
    bd_lever=summ["LADDER"]["best_distinct_count_mean"]; ms_lever=summ["LADDER"]["max_single_count_mean"]
    bd_ge2=bd_lever>=2; bd_gt_ms=bd_lever>ms_lever
    passed=(lever_margin>deriv_margin) and bd_ge2 and (lad>add)
    kill=(lad<=add) or (lever_margin<=deriv_margin)
    preds=compute_predictors(SEEDS[0])
    predicted=(preds["rho"]<=0.02) and (preds["sigma"]>1.0)
    verdict=("KILL — resolution-ladder does NOT beat derivtrace-baseline margin on held-out "
             "FLAT internalization; FULL derivation does NOT induce FLAT recombination beyond "
             "always-on derivtrace (or beyond additive). Objective-format axis INERT on additive "
             "trunk. NO GPU escalation." if kill else
             "ESCALATE — ladder margin > derivtrace margin AND bd>=2 => STEP-1 full 303M candidate.")
    out={"experiment":"G1 lever V13 resolution-ladder STEP-0 cheap kill",
         "scope":"DIRECTIONAL toy numpy (torch-free); NOT 303M engine-native; NOT terminal",
         "config":{"N":N,"D":D,"HELDOUT":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS,
                   "arms":ARMS,"combiner":"additive(fixed all arms)",
                   "ladder_schedule":"p_full 1.0->0.0 linear (LADDER); ADD=0; DERIV=1"},
         "frozen_bar":("held-out FLAT recomb (ans-head top-2 has BOTH i,j; no derivation emit). "
                       "PASS iff bd>=2 AND bd>max_single AND (LADDER-ADD)>(DERIV-ADD); "
                       "KILL iff LADDER<=ADD OR LADDER_margin<=DERIV_margin"),
         "arms":summ,
         "ADD_flat_recomb":add,"DERIV_flat_recomb":drv,"LADDER_flat_recomb":lad,
         "lever_margin_LADDER_minus_ADD":lever_margin,
         "deriv_margin_DERIV_minus_ADD":deriv_margin,
         "bd_lever_mean":bd_lever,"max_single_lever_mean":ms_lever,
         "bd_ge2":bool(bd_ge2),"bd_gt_max_single":bool(bd_gt_ms),
         "PASS":bool(passed),"KILL":bool(kill),
         "predictors":preds,
         "predicted_pass_rule":"rho<=0.02 AND sigma>1",
         "predicted_pass":bool(predicted),
         "predicted_vs_actual":("MATCH" if predicted==passed else "MISMATCH(predictor over/under-optimistic)"),
         "VERDICT":verdict,"wall_sec":round(time.time()-t0,1)}
    print(json.dumps(out,indent=2))
    open(OUT,"w").write(json.dumps(out,indent=2))
if __name__=="__main__": main()
