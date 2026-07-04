#!/usr/bin/env python3
"""G1 LEVER B2 = L2 x V2 FACTORIAL — STEP-0 CHEAP ENGINE-NATIVE KILL-GATE (H_9127).

B2 coverage x granularity factorial. Cloned + fused from the two sibling STEP-0
harnesses:
  state/g1_lever_step0/L2_coverage_density/l2_coverage_density.py  (L2 = corpus DENSITY)
  state/g1_lever_step0/V2_micro_trace/step0_v2_micro_trace.py      (V2 = micro-trace decode)
Both floored individually (L2 KILL: margin 0.243<=DERIV 0.307; V2 KILL: MICRO<=ADD).
B2 question: does COMBINING them yield SYNERGY (superadditive, AB > A+B) that
neither lever alone showed?

Real-G1-isomorphic toy: N concepts, held-out d-tuples, recombination = emit ALL d
constituent keywords under next-token/reconstruction (BCE/CE) loss (NOT recomb-rigged).

TWO ORTHOGONAL FACTORS (2x2):
  L2 (corpus DENSITY, training-data axis):
     off = SPARSE  (degree cap k=1: each concept co-occurs with ~1 partner)
     on  = DENSE   (full train pool: component-dense, combination-sparse)
  V2 (target-format / decode GRANULARITY, readout axis):
     off = additive one-shot multi-label top-d readout (H_1819-shape pooling)
     on  = micro-trace: per-line copy-prev-set + exactly 1 SET-ADDRESSED local edit,
           hard-copy dedup decode (kappa maximal, M~depth)

4 factorial cells:
  C00 = L2off x V2off  (sparse additive)
  C10 = L2on  x V2off  (dense  additive)   == ADD control (additive ceiling @dense)
  C01 = L2off x V2on   (sparse micro-trace)
  C11 = L2on  x V2on   (dense  micro-trace) == the COMBINED lever
+ 2 required controls (common frozen bar):
  ADD   = C10 (additive one-shot @dense pool = additive-control ceiling, matched density)
  DERIV = derivtrace positional baseline @dense pool (bd~2 reference margin)

INTERACTION (synergy) = C11 - C10 - C01 + C00.  Superadditive iff interaction > 0.
  main effect L2 (under additive) = C10 - C00
  main effect V2 (under additive) = C01 - C00
  predicted-interaction magnitude = P_basin x kappa  (density basin-entry prob x copy ratio)

FROZEN BAR (pre-registered, no post-hoc move — c9/p7):
  N=24 · D=64 · HELDOUT eval frac 0.45 (fixed disjoint set/seed) · 4000 steps ·
  seeds {7,4302,4303}. Metric currency = held-out MEAN best_distinct (# distinct
  constituents emitted, budget=d). Depth 2 primary + depth 3 secondary robustness.
  COMBINED LEVER (C11) PASS iff:
    bd(C11)>=2 AND bd(C11)>max_single AND lever_margin(C11-ADD)>0
    AND lever_margin > deriv_margin(DERIV-ADD) AND synergy(interaction)>0.
  KILL otherwise. Pre-registered predictor test: synergy>0 predicted iff P_basin>0.5
  AND kappa>0.2 (both levers active).

DIRECTIONAL: toy numpy, NOT 303M engine-native (a_engine_native_learning). Pre-screen
only — gates GPU spend, terminal verdict forbidden. Numbers verbatim, no tune-to-green.
"""
import numpy as np, json, time, itertools, os

N = 24; D = 64; HELDOUT = 0.45; STEPS = 4000; LR = 3e-3
SEEDS = [7, 4302, 4303]; DEPTHS = [2, 3]; MAXT = 200
K_SPARSE = 1            # L2 off: degree cap = 1 partner per concept
b1a, b2a, eps = 0.9, 0.999, 1e-8

def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))
def softmax(z):
    z=z-z.max(1,keepdims=True); e=np.exp(z); return e/e.sum(1,keepdims=True)

def make_tuples(rng, d):
    combos=list(itertools.combinations(range(N), d)); rng.shuffle(combos)
    combos=combos[:MAXT]
    ncut=int(len(combos)*(1-HELDOUT))
    return [np.array(c) for c in combos[:ncut]], [np.array(c) for c in combos[ncut:]]

def degree_capped(tuples, k, rng):
    """L2 density: keep subset so every concept appears in <= k training tuples."""
    order=list(range(len(tuples))); rng.shuffle(order)
    deg=np.zeros(N,dtype=int); sel=[]
    for idx in order:
        t=tuples[idx]
        if all(deg[c]<k for c in t):
            sel.append(t)
            for c in t: deg[c]+=1
    return sel

def adam_step(P, mom, vel, grads, step):
    for k in P:
        g=grads[k]; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
        mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)

# ---------------- V2off: additive one-shot multi-label ----------------
def init_add(rng):
    s=1.0/np.sqrt(D)
    return {"E":rng.standard_normal((N,D))*s,
            "Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
            "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
            "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}

def train_add(P, tuples, d, rng):
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    idx=np.array([list(t) for t in tuples])                       # B,d
    Y=np.zeros((len(tuples),N))
    for r,t in enumerate(tuples): Y[r, t]=1.0
    anc_idx=np.stack([np.full(d,i) for i in range(N)])            # N,d
    anc_Y=np.eye(N)
    IDX=np.concatenate([idx,anc_idx],0); YY=np.concatenate([Y,anc_Y],0); B=len(IDX)
    for step in range(1,STEPS+1):
        emb=P["E"][IDX]; proj=emb@P["Win"].T; p=proj.sum(1)
        z1=p@P["W1"].T+P["b1"]; z=gelu(z1)
        logits=z@P["W2"].T+P["b2"]
        dlogits=(sigmoid(logits)-YY)/N
        gW2=dlogits.T@z; gb2=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        gW1=dz1.T@p; gb1=dz1.sum(0)
        dp=dz1@P["W1"]; gWin=dp.T@emb.sum(1); demb=dp@P["Win"]
        gE=np.zeros_like(P["E"])
        for k in range(d): np.add.at(gE, IDX[:,k], demb)
        grads={"E":gE/B,"Win":gWin/B,"W1":gW1/B,"b1":gb1/B,"W2":gW2/B,"b2":gb2/B}
        adam_step(P,mom,vel,grads,step)
    return P

def eval_add(P, pairs, d):
    """returns (mean_bd, recomb_rate) : recomb_rate = frac with ALL d in top-d."""
    bd=[]; full=[]
    for t in pairs:
        idx=np.array(list(t))[None,:]
        emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist())
        hit=len(set(t.tolist()) & topd)
        bd.append(hit); full.append(1.0 if hit==d else 0.0)
    return float(np.mean(bd)), float(np.mean(full))

def maxsingle_add(P, d):
    m=[]
    for i in range(N):
        idx=np.full((1,d),i); emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist()); m.append(len({i}&topd))
    return float(np.mean(m))

# ------------- V2on/DERIV: trace arms (MICRO set-addressed / DERIV positional) -------------
def init_trace(rng, mode, d):
    s=1.0/np.sqrt(D)
    P={"E":rng.standard_normal((N,D))*s,
       "Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
       "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
       "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}
    if mode=="DERIV": P["Wpos"]=rng.standard_normal((d,D))*s
    else:             P["Wemit"]=np.eye(D)+rng.standard_normal((D,D))*0.05
    return P

def build_trace_examples(tuples, d):
    ex_inp=[]; ex_emit=[]; ex_pos=[]; ex_tgt=[]
    def add(sorted_t):
        for t in range(len(sorted_t)):
            ex_inp.append(list(sorted_t)); ex_emit.append(list(sorted_t[:t]))
            ex_pos.append(t); ex_tgt.append(sorted_t[t])
    for tp in tuples: add(sorted(tp.tolist()))
    for i in range(N): add([i])
    return ex_inp, ex_emit, ex_pos, ex_tgt

def pool(E, idx_list):
    if len(idx_list)==0: return np.zeros(E.shape[1])
    return E[np.array(idx_list,dtype=int)].sum(0)

def train_trace(P, tuples, mode, d, rng):
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    inp,emit,pos,tgt=build_trace_examples(tuples,d); B=len(tgt)
    tgt=np.array(tgt); posA=np.array(pos)
    Minp=np.zeros((B,N)); Mem=np.zeros((B,N))
    for r,x in enumerate(inp): Minp[r, np.array(x,dtype=int)]=1.0
    for r,x in enumerate(emit):
        if len(x): Mem[r, np.array(x,dtype=int)]=1.0
    oh=np.zeros((B,N)); oh[np.arange(B),tgt]=1.0
    for step in range(1,STEPS+1):
        pin=Minp@P["E"]; proj_in=pin@P["Win"].T
        if mode=="DERIV":
            ctx=proj_in+P["Wpos"][posA]
        else:
            pem=Mem@P["E"]; ctx=proj_in+pem@P["Wemit"].T
        z1=ctx@P["W1"].T+P["b1"]; z=gelu(z1)
        logits=z@P["W2"].T+P["b2"]
        pr=softmax(logits); dlogits=(pr-oh)/B
        gW2=dlogits.T@z; gb2=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        gW1=dz1.T@ctx; gb1=dz1.sum(0)
        dctx=dz1@P["W1"]
        gWin=dctx.T@pin; dpin=dctx@P["Win"]; gE=Minp.T@dpin
        grads={"Win":gWin,"W1":gW1,"b1":gb1,"W2":gW2,"b2":gb2}
        if mode=="DERIV":
            gWpos=np.zeros_like(P["Wpos"]); np.add.at(gWpos, posA, dctx); grads["Wpos"]=gWpos
        else:
            gWemit=dctx.T@pem; grads["Wemit"]=gWemit
            dpem=dctx@P["Wemit"]; gE=gE+Mem.T@dpem
        grads["E"]=gE
        adam_step(P,mom,vel,grads,step)
    return P

def eval_trace(P, pairs, mode, d):
    bd=[]; full=[]
    for tp in pairs:
        tset=set(tp.tolist()); emitted=[]
        pin=pool(P["E"], list(tp)); proj_in=pin@P["Win"].T
        for t in range(d):
            if mode=="DERIV":
                ctx=proj_in+P["Wpos"][t]
            else:
                pem=pool(P["E"], emitted); ctx=proj_in+pem@P["Wemit"].T
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if mode=="MICRO":
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else:
                nxt=int(np.argmax(logits))
            emitted.append(nxt)
        hit=len(set(emitted) & tset)
        bd.append(hit); full.append(1.0 if hit==d else 0.0)
    return float(np.mean(bd)), float(np.mean(full))

def maxsingle_trace(P, mode, d):
    m=[]
    for i in range(N):
        emitted=[]; pin=pool(P["E"],[i]); proj_in=pin@P["Win"].T
        for t in range(d):
            if mode=="DERIV": ctx=proj_in+P["Wpos"][t]
            else: ctx=proj_in+pool(P["E"],emitted)@P["Wemit"].T
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if mode=="MICRO":
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else: nxt=int(np.argmax(logits))
            emitted.append(nxt)
        m.append(len(set(emitted)&{i}))
    return float(np.mean(m))

# ---------------- predictors rho / sigma / kappa / M ----------------
def sigma_of(tuples):
    partners={i:set() for i in range(N)}
    for tp in tuples:
        for a in tp:
            for b in tp:
                if a!=b: partners[int(a)].add(int(b))
    return float(np.mean([len(partners[i]) for i in range(N)]))

def predictors(dense_tuples, sparse_tuples, d):
    covered=set()
    for tp in dense_tuples: covered.update(int(x) for x in tp)
    covered.update(range(N))          # singleton anchors
    rho=1.0-len(covered)/N
    sig_dense=sigma_of(dense_tuples); sig_sparse=sigma_of(sparse_tuples)
    kappa=float(np.mean([ t/(t+1) for t in range(d) ]))
    M=float(np.mean([t+1 for t in range(d)]))
    return {"rho":round(rho,4),"sigma_dense":round(sig_dense,3),
            "sigma_sparse":round(sig_sparse,3),"kappa":round(kappa,4),"M":round(M,3)}

def run_depth(d):
    cells={c:{"bd":[]} for c in ["C00","C10","C01","C11"]}
    add_recomb=[]; add_ms=[]; c11_ms=[]
    deriv={"bd":[]}; preds=None
    for seed in SEEDS:
        rng=np.random.default_rng(seed)
        tr,te=make_tuples(rng,d)
        dense=tr                                   # L2 on: full train pool
        sparse=degree_capped(tr,K_SPARSE,rng)      # L2 off: degree-1
        if preds is None: preds=predictors(dense,sparse,d)
        # C00 sparse additive
        P=train_add(init_add(rng),sparse,d,rng); bd,_=eval_add(P,te,d); cells["C00"]["bd"].append(bd)
        # C10 dense additive == ADD control
        P=train_add(init_add(rng),dense,d,rng); bd,rr=eval_add(P,te,d)
        cells["C10"]["bd"].append(bd); add_recomb.append(rr); add_ms.append(maxsingle_add(P,d))
        # C01 sparse micro-trace
        P=train_trace(init_trace(rng,"MICRO",d),sparse,"MICRO",d,rng); bd,_=eval_trace(P,te,"MICRO",d)
        cells["C01"]["bd"].append(bd)
        # C11 dense micro-trace == combined lever
        P=train_trace(init_trace(rng,"MICRO",d),dense,"MICRO",d,rng); bd,_=eval_trace(P,te,"MICRO",d)
        cells["C11"]["bd"].append(bd); c11_ms.append(maxsingle_trace(P,"MICRO",d))
        # DERIV positional baseline @dense
        P=train_trace(init_trace(rng,"DERIV",d),dense,"DERIV",d,rng); bd,_=eval_trace(P,te,"DERIV",d)
        deriv["bd"].append(bd)
        print(f"[d{d} seed{seed}] C00={cells['C00']['bd'][-1]:.3f} C10/ADD={cells['C10']['bd'][-1]:.3f} "
              f"C01={cells['C01']['bd'][-1]:.3f} C11={cells['C11']['bd'][-1]:.3f} DERIV={deriv['bd'][-1]:.3f}",flush=True)
    def m(v): return float(np.mean(v))
    C00=m(cells["C00"]["bd"]); C10=m(cells["C10"]["bd"]); C01=m(cells["C01"]["bd"]); C11=m(cells["C11"]["bd"])
    DER=m(deriv["bd"]); ADD=C10
    interaction=C11 - C10 - C01 + C00
    eff_L2=C10 - C00; eff_V2=C01 - C00
    lever_margin=C11 - ADD; deriv_margin=DER - ADD
    P_basin=m(add_recomb)                          # dense additive both-in recomb rate
    kappa=preds["kappa"]
    max_single=m(c11_ms)
    pred_interaction=P_basin*kappa
    predicted_synergy=(P_basin>0.5) and (kappa>0.2)
    synergy=interaction>1e-6
    lever_pass=(C11>=2.0) and (C11>max_single) and (lever_margin>0) and (lever_margin>deriv_margin) and synergy
    return {
      "cells_mean":{"C00_sparse_add":round(C00,4),"C10_dense_add(ADD)":round(C10,4),
                    "C01_sparse_micro":round(C01,4),"C11_dense_micro(LEVER)":round(C11,4)},
      "cells_seeds":{c:[round(x,3) for x in cells[c]["bd"]] for c in cells},
      "DERIV_mean":round(DER,4),"DERIV_seeds":[round(x,3) for x in deriv["bd"]],
      "ADD_control":round(ADD,4),"max_single":round(max_single,4),
      "main_effect_L2(C10-C00)":round(eff_L2,4),"main_effect_V2(C01-C00)":round(eff_V2,4),
      "sum_main_effects":round(eff_L2+eff_V2,4),
      "combined_lift(C11-C00)":round(C11-C00,4),
      "INTERACTION(C11-C10-C01+C00)":round(interaction,4),
      "synergy_superadditive":bool(synergy),
      "lever_margin(C11-ADD)":round(lever_margin,4),
      "deriv_margin(DERIV-ADD)":round(deriv_margin,4),
      "predictors":preds,
      "P_basin(dense_add_recomb)":round(P_basin,4),
      "pred_interaction(P_basin*kappa)":round(pred_interaction,4),
      "predicted_synergy(P_basin>0.5 & kappa>0.2)":bool(predicted_synergy),
      "LEVER_PASS":bool(lever_pass),
    }

def main():
    t0=time.time(); out={"experiment":"G1 lever B2 = L2 x V2 FACTORIAL STEP-0 cheap kill (H_9127)",
        "harness":"fused clone of L2_coverage_density + V2_micro_trace step0 harnesses",
        "config":{"N":N,"D":D,"HELDOUT_eval_frac":HELDOUT,"STEPS":STEPS,"LR":LR,"seeds":SEEDS,
                  "K_SPARSE":K_SPARSE,"depths":DEPTHS,"MAXT":MAXT},
        "frozen_bar":("held-out MEAN best_distinct; 2x2 {L2 on/off}x{V2 on/off}+ADD+DERIV; "
                      "COMBINED LEVER C11 PASS iff bd>=2 AND >max_single AND lever_margin>0 "
                      "AND lever_margin>deriv_margin AND synergy(interaction)>0"),
        "depths":{}}
    for d in DEPTHS:
        out["depths"][str(d)]=run_depth(d)
    d2=out["depths"]["2"]; d3=out["depths"]["3"]
    inter2=d2["INTERACTION(C11-C10-C01+C00)"]; inter3=d3["INTERACTION(C11-C10-C01+C00)"]
    syn2=d2["synergy_superadditive"]; pass2=d2["LEVER_PASS"]
    interaction_grows=inter3>inter2
    verdict=("ESCALATE (B2 factorial: C11 dense-micro beats ADD & DERIV margin AND positive "
             "L2xV2 synergy (interaction>0) => superadditive coverage x granularity, STEP-1 303M)"
             if pass2 else
             "KILL (B2 factorial: no superadditive synergy (interaction<=0) or C11<=ADD/DERIV "
             "margin or bd<2/<=max_single => coverage x granularity does NOT combine, "
             "FALSIFIED-DIRECTIONAL, NO GPU rent)")
    out["summary"]={
        "primary_depth":2,
        "INTERACTION_d2":inter2,"INTERACTION_d3":inter3,
        "synergy_d2":bool(syn2),"synergy_d3":bool(d3["synergy_superadditive"]),
        "interaction_grows_with_depth":bool(interaction_grows),
        "LEVER_PASS_d2":bool(pass2),"LEVER_PASS_d3":bool(d3["LEVER_PASS"]),
        "predicted_synergy_d2":d2["predicted_synergy(P_basin>0.5 & kappa>0.2)"],
        "PASS":bool(pass2),"VERDICT":verdict}
    out["wall_sec"]=round(time.time()-t0,1)
    outp=os.path.join(os.path.dirname(os.path.abspath(__file__)),"result.json")
    open(outp,"w").write(json.dumps(out,indent=2))
    print("\n=== B2 L2xV2 FACTORIAL RESULT ===")
    print(json.dumps(out,indent=2))
    print("\nwrote",outp)

if __name__=="__main__": main()
