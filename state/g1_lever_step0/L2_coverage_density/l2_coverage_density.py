#!/usr/bin/env python3
"""G1 LEVER L2 combination-coverage DENSITY — STEP-0 CHEAP ENGINE-NATIVE KILL (H_9127).

Real-G1-isomorphic readout toy (cloned from state/g1_gamma_engine_native/
step0_gamma_bind_kill.py). Two concepts -> emit BOTH keywords = held-out
recombination, under next-token/reconstruction (BCE) loss (NOT recomb-rigged).

L2 lever (F3 held-out-as-interpolation): target stays FLAT (=the answer: emit
both concept keywords, additive combiner — CE=echo is NOT broken). The lever is
the CORPUS DENSITY: tile the (concept x concept) space so each concept co-occurs
with k DISTINCT partners in training (component-dense, combination-sparse). Sweep
k = 1 -> full pool and plot held-out best_distinct(k) -> look for a
phase-transition k* (density enters the interpolation basin).

3 arms per FROZEN BAR (measure-frozen, no post-hoc move c9/p7):
  ADD   : additive FLAT decode, SPARSE k=1 model  (additive-control floor)
  DERIV : derivtrace baseline = decompose-and-echo decode (2-step single-concept
          trace: read i, read j) on the dense model -> bd~2 reference margin
  LEVER : additive FLAT decode swept over density k in {1,2,3,4,6,8,12}
          headline = densest k point.

FROZEN BAR: N=24, D=64, held-out EVAL frac 0.45 (fixed disjoint set per seed,
identical across all k), 4000 steps, seeds {7,4302,4303}.
Metric currency = held-out recomb_rate (mean [both i,j in top-2]); best_distinct
= max over held-out pairs of |top2 cap {i,j}|; max_single = single-concept floor.
LEVER PASS iff best_distinct(k_max) >= 2 AND > max_single AND
  margin_lever(recomb_rate(k_max) - recomb_rate(ADD)) > margin_DERIV
  AND a phase-transition k* exists. KILL otherwise. Torch-free numpy = DIRECTIONAL.
"""
import numpy as np, json, time, itertools

N=24; D=64; HELDOUT=0.45; STEPS=4000; LR=3e-3; SEEDS=[7,4302,4303]
KS=[1,2,3,4,6,8,12]           # density sweep (partners-per-concept)
K_ADD=1                        # additive-control floor = sparsest
K_MAX=KS[-1]                   # lever headline = densest

def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))

class Model:
    """additive FLAT combiner (L2 keeps CE=echo, operator unchanged)."""
    def __init__(self,rng):
        s=1.0/np.sqrt(D)
        self.E=rng.standard_normal((N,D))*s
        self.Wa=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.Wb=np.eye(D)+rng.standard_normal((D,D))*0.05
        self.W1=rng.standard_normal((D,D))*s; self.b1=np.zeros(D)
        self.W2=rng.standard_normal((N,D))*s; self.b2=np.zeros(N)
    def params(self):
        return {"E":self.E,"Wa":self.Wa,"Wb":self.Wb,"W1":self.W1,"b1":self.b1,"W2":self.W2,"b2":self.b2}
    def fwd(self,I,J):
        A=self.E[I]; Bv=self.E[J]
        PA=A@self.Wa.T; PB=Bv@self.Wb.T
        H=PA+PB
        Z1=H@self.W1.T+self.b1; Z=gelu(Z1)
        logits=Z@self.W2.T+self.b2
        return logits,(I,J,A,Bv,PA,PB,H,Z1,Z)

def degree_capped(pool,k,rng):
    """select subset of pool so each concept has degree <= k (most == k)."""
    order=list(range(len(pool))); rng.shuffle(order)
    deg=np.zeros(N,dtype=int); sel=[]
    for idx in order:
        a,b=pool[idx]
        if deg[a]<k and deg[b]<k:
            sel.append((a,b)); deg[a]+=1; deg[b]+=1
    return sel,float(deg.mean()),int(deg.min()),int(deg.max())

def make_split(rng):
    pairs=[(i,j) for i in range(N) for j in range(i+1,N)]; rng.shuffle(pairs)
    ncut=int(len(pairs)*(1-HELDOUT))
    return pairs[:ncut],pairs[ncut:]   # pool(train-eligible), held-out(fixed eval)

def train_model(data,seed):
    rng=np.random.default_rng(seed*97+1); m=Model(rng)
    I=np.array([d[0] for d in data]); J=np.array([d[1] for d in data])
    T=np.zeros((len(data),N))
    for r,(i,j) in enumerate(data):
        T[r,i]=1.0; T[r,j]=1.0
    P=m.params(); mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    b1a,b2a,eps=0.9,0.999,1e-8; B=len(data)
    for step in range(1,STEPS+1):
        logits,(Ii,Jj,A,Bv,PA,PB,H,Z1,Z)=m.fwd(I,J)
        p=sigmoid(logits); dlogits=(p-T)/(N*B)
        gW2=dlogits.T@Z; gb2=dlogits.sum(0)
        dZ=dlogits@m.W2; dZ1=dZ*dgelu(Z1)
        gW1=dZ1.T@H; gb1=dZ1.sum(0)
        dH=dZ1@m.W1
        gWa=dH.T@A; gWb=dH.T@Bv
        dA=dH@m.Wa; dBv=dH@m.Wb
        gE=np.zeros_like(m.E); np.add.at(gE,I,dA); np.add.at(gE,J,dBv)
        grads={"E":gE,"Wa":gWa,"Wb":gWb,"W1":gW1,"b1":gb1,"W2":gW2,"b2":gb2}
        for k in P:
            g=grads[k]; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
            mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)
    return m

def eval_flat(m,held):
    I=np.array([p[0] for p in held]); J=np.array([p[1] for p in held])
    logits,_=m.fwd(I,J)
    top2=np.argsort(logits,axis=1)[:,-2:]
    dist=np.zeros(len(held),dtype=int); both=np.zeros(len(held),dtype=bool)
    for r,(i,j) in enumerate(held):
        s=set(top2[r].tolist()); d=(1 if i in s else 0)+(1 if j in s else 0)
        dist[r]=d; both[r]=(i in s and j in s)
    return {"recomb_rate":float(both.mean()),"best_distinct":int(dist.max()),
            "mean_distinct":float(dist.mean())}

def eval_deriv(m,held):
    """derivtrace baseline: decompose composed query into two single-concept echo
    steps (read i via forward(i,i), read j via forward(j,j)); distinct = coverage
    of the two argmax echoes. sigma=inf by construction (no partner in step ctx)."""
    idx=np.arange(N)
    slog,_=m.fwd(idx,idx)          # single grounding: forward(i,i)
    sarg=np.argmax(slog,axis=1)    # per-concept single-echo argmax
    dist=np.zeros(len(held),dtype=int); both=np.zeros(len(held),dtype=bool)
    for r,(i,j) in enumerate(held):
        s={int(sarg[i]),int(sarg[j])}
        d=(1 if i in s else 0)+(1 if j in s else 0)
        dist[r]=d; both[r]=(i in s and j in s)
    return {"recomb_rate":float(both.mean()),"best_distinct":int(dist.max()),
            "mean_distinct":float(dist.mean())}

def eval_single(m):
    idx=np.arange(N); slog,_=m.fwd(idx,idx)
    return float((np.argmax(slog,axis=1)==idx).mean())

def max_single_floor(m,held):
    """single-concept floor: emit only top-1 concept -> distinct per held pair."""
    I=np.array([p[0] for p in held]); J=np.array([p[1] for p in held])
    logits,_=m.fwd(I,J); top1=np.argmax(logits,axis=1)
    dist=np.array([(1 if int(top1[r]) in (held[r][0],held[r][1]) else 0) for r in range(len(held))])
    return int(dist.max())

def main():
    t0=time.time()
    per_k={k:{"recomb":[],"bd":[],"meand":[],"deg":[]} for k in KS}
    deriv={"recomb":[],"bd":[],"meand":[]}
    singacc=[]; msingle=[]
    for seed in SEEDS:
        rng=np.random.default_rng(seed)
        pool,held=make_split(rng)
        singles=[(i,i) for i in range(N)]
        dense_model=None
        for k in KS:
            sel,md,mn,mx=degree_capped(pool,k,rng)
            data=singles+sel
            m=train_model(data,seed*1000+k)
            ef=eval_flat(m,held)
            per_k[k]["recomb"].append(ef["recomb_rate"]); per_k[k]["bd"].append(ef["best_distinct"])
            per_k[k]["meand"].append(ef["mean_distinct"]); per_k[k]["deg"].append(md)
            print(f"[seed {seed}] k={k:2d} deg~{md:.1f}({mn}-{mx}) n_train={len(sel)} "
                  f"HELDOUT recomb={ef['recomb_rate']:.3f} bd={ef['best_distinct']} "
                  f"meand={ef['mean_distinct']:.3f}",flush=True)
            if k==K_MAX: dense_model=m
        ed=eval_deriv(dense_model,held)
        deriv["recomb"].append(ed["recomb_rate"]); deriv["bd"].append(ed["best_distinct"]); deriv["meand"].append(ed["mean_distinct"])
        singacc.append(eval_single(dense_model)); msingle.append(max_single_floor(dense_model,held))
        print(f"[seed {seed}] DERIV(single-echo trace) HELDOUT recomb={ed['recomb_rate']:.3f} "
              f"bd={ed['best_distinct']} meand={ed['mean_distinct']:.3f} | single_acc={singacc[-1]:.3f} max_single_bd={msingle[-1]}",flush=True)

    def summ(d): return {"recomb_rate_mean":float(np.mean(d["recomb"])),
                         "recomb_rate_seeds":[round(x,3) for x in d["recomb"]],
                         "best_distinct_max":int(np.max(d["bd"])),
                         "best_distinct_seeds":[int(x) for x in d["bd"]],
                         "mean_distinct_mean":float(np.mean(d["meand"]))}
    curve={str(k):summ(per_k[k]) for k in KS}
    add_s=summ(per_k[K_ADD]); lev_s=summ(per_k[K_MAX]); der_s=summ(deriv)
    add_r=add_s["recomb_rate_mean"]; lev_r=lev_s["recomb_rate_mean"]; der_r=der_s["recomb_rate_mean"]
    margin_lever=lev_r-add_r; margin_deriv=der_r-add_r
    max_single=int(np.max(msingle))

    means=[float(np.mean(per_k[k]["recomb"])) for k in KS]
    rises=[(KS[i+1],means[i+1]-means[i]) for i in range(len(KS)-1)]
    kstar=None; best_rise=0.0
    for (kk,rr) in rises:
        if rr>best_rise: best_rise=rr; kstar=kk
    transition=(best_rise>=0.05) and (means[-1]-means[0]>=0.10)

    bd_lever=lev_s["best_distinct_max"]
    lever_pass=(bd_lever>=2) and (bd_lever>max_single) and (margin_lever>margin_deriv) and transition
    verdict=("ESCALATE (density lever: held-out recomb rises with k, k*=%s exists, "
             "margin_lever %.3f > margin_DERIV %.3f => STEP-1 clm303/ByteGPT --py)"%(str(kstar),margin_lever,margin_deriv)
             if lever_pass else
             "KILL (L2 density additive-FLAT floor: margin_lever %.3f <= margin_DERIV %.3f "
             "OR no phase-transition (best_rise=%.3f,trans=%s) OR bd_lever %d < 2/max_single "
             "=> FALSIFIED-DIRECTIONAL, NO GPU rent)"%(margin_lever,margin_deriv,best_rise,transition,bd_lever))

    predictors={
      "rho_echo_residual":0.0,
      "rho_note":"both target concepts seen (singles+combos) => min-suff-ctx present => rho~0 (F3 interpolation)",
      "sigma_partner_diversity_ADD(k1)":1,
      "sigma_partner_diversity_LEVER(kmax)":K_MAX,
      "sigma_DERIV":"inf (single-echo, no partner in step context)",
      "sigma_note":"sigma == training density k; k=1 => pair-binding FAIL predicted; k=%d => sigma>1 OK"%K_MAX,
      "kappa_copy_locality":1.0, "delta_copy":0, "RF":"prompt-local (delta<RF)",
      "kappa_note":"FLAT prompt names (i,j); target {i,j} = direct in-prompt copy => kappa=1, delta<RF (favorable)",
      "M_memorization_disadv_L2":2.0,
      "M_note":"FLAT target short (|tau|=2) => M small => margin ~ log M weak (UNfavorable; derivtrace M larger via long structured trace)",
      "predicted_pass_naive_rule":True,
      "predicted_pass_caveat":"M small (short FLAT target) caps absolute margin; density may lift held-out only to interpolation floor, not beat DERIV structured-target margin"
    }

    out={"experiment":"G1 lever L2 combination-coverage DENSITY STEP-0 cheap kill (H_9127)",
         "harness":"cloned from state/g1_gamma_engine_native/step0_gamma_bind_kill.py",
         "config":{"N":N,"D":D,"HELDOUT_eval_frac":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS,"k_sweep":KS},
         "frozen_bar":("held-out recomb_rate (both i,j in top-2) per arm; LEVER PASS iff "
                       "bd(kmax)>=2 AND >max_single AND margin_lever>margin_DERIV AND phase-transition k* exists"),
         "arms":{"ADD_flat_k1":add_s,"DERIV_single_echo_trace":der_s,"LEVER_flat_kmax":lev_s},
         "density_curve_recomb_by_k":curve,
         "max_single_floor":max_single,
         "single_acc_mean":float(np.mean(singacc)),
         "phase_transition":{"k_star":kstar,"best_single_step_rise":round(best_rise,4),
                             "recomb_start_k%d"%KS[0]:round(means[0],4),"recomb_end_k%d"%KS[-1]:round(means[-1],4),
                             "transition_detected":transition},
         "margins":{"margin_lever_kmax_minus_ADD":round(margin_lever,4),
                    "margin_DERIV_minus_ADD":round(margin_deriv,4)},
         "predictors_rho_sigma_kappa_M":predictors,
         "LEVER_PASS":bool(lever_pass),"VERDICT":verdict,
         "wall_sec":round(time.time()-t0,1)}
    print("\n=== L2 STEP-0 RESULT ===")
    print(json.dumps(out,indent=2))
    import os
    outp=os.path.join(os.path.dirname(os.path.abspath(__file__)),"result.json")
    open(outp,"w").write(json.dumps(out,indent=2))
    print("\nwrote",outp)

if __name__=="__main__": main()
