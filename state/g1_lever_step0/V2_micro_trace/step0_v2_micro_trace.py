#!/usr/bin/env python3
"""G1 LEVER V2_micro_trace — STEP-0 CHEAP ENGINE-NATIVE KILL-GATE (torch-free numpy).

Real-G1-homomorphic toy (mirrors state/g1_gamma_engine_native/step0_gamma_bind_kill.py):
N concepts, held-out d-tuples, recombination = emit ALL d constituent keywords.
Extends the pair task to depth d in {2,3} so the micro-trace lever's depth curve is
measurable. LOSS is next-token/reconstruction (NOT recomb-rigged). Arms differ in the
TARGET FORMAT / trunk decoding structure only.

  ADD   (additive control) : additive pool -> one-shot multi-label readout, top-d.
                             (reference gamma toy showed this ~solves depth-2.)
  DERIV (derivtrace base)  : autoregressive POSITIONAL trace -- predict the t-th sorted
                             constituent from full-tuple pool + learned position bias.
                             bd~2 baseline reference margin.
  MICRO (V2 lever)         : micro-trace -- each line = COPY previous emitted set + exactly
                             1 local edit. Edit head is SET-ADDRESSED (full-tuple pool +
                             emitted-set pool, order-invariant); decode enforces hard copy
                             (dedup: pick best UN-emitted). kappa maximal, M ~ depth.

FROZEN BAR (pre-registered, no post-hoc move -- c9/p7):
  N=24, D=64, HELDOUT=0.45, STEPS=4000, seeds {7,4302,4303}.
  metric = held-out best_distinct (# distinct constituents the arm emits within budget=d).
  LEVER PASS = held_out best_distinct>=2 AND >max_single AND
               margin(MICRO-ADD) > margin(DERIV-ADD).  KILL otherwise.
  Depth curve: measure at d=2 and d=3; pre-registered prediction margin ~ depth.

DIRECTIONAL: toy numpy, NOT 303M engine-native (a_engine_native_learning). Pre-screen
only -- gates GPU spend, terminal verdict forbidden.
"""
import numpy as np, json, time, itertools

N = 24; D = 64; HELDOUT = 0.45; STEPS = 4000; LR = 3e-3
SEEDS = [7, 4302, 4303]; DEPTHS = [2, 3]; MAXT = 200
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

def adam_step(P, mom, vel, grads, step):
    for k in P:
        g=grads[k]; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
        mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)

# ---------------- ADD: additive one-shot multi-label ----------------
def init_add(rng):
    s=1.0/np.sqrt(D)
    return {"E":rng.standard_normal((N,D))*s,
            "Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
            "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
            "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}

def train_add(P, tuples, d, rng):
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    # anchors: each concept singleton -> emit itself
    idx=np.array([list(t) for t in tuples])                       # B,d
    Y=np.zeros((len(tuples),N))
    for r,t in enumerate(tuples): Y[r, t]=1.0
    anc_idx=np.stack([np.full(d,i) for i in range(N)])            # N,d
    anc_Y=np.eye(N)
    IDX=np.concatenate([idx,anc_idx],0); YY=np.concatenate([Y,anc_Y],0); B=len(IDX)
    for step in range(1,STEPS+1):
        emb=P["E"][IDX]                        # B,d,D
        proj=emb@P["Win"].T                    # B,d,D
        p=proj.sum(1)                          # B,D
        z1=p@P["W1"].T+P["b1"]; z=gelu(z1)
        logits=z@P["W2"].T+P["b2"]             # B,N
        dlogits=(sigmoid(logits)-YY)/N         # B,N
        gW2=dlogits.T@z; gb2=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        gW1=dz1.T@p; gb1=dz1.sum(0)
        dp=dz1@P["W1"]                          # B,D
        gWin=dp.T@emb.sum(1)                    # D,D
        demb=dp@P["Win"]                        # B,D (same for each of d slots)
        gE=np.zeros_like(P["E"])
        for k in range(d): np.add.at(gE, IDX[:,k], demb)
        grads={"E":gE/B,"Win":gWin/B,"W1":gW1/B,"b1":gb1/B,"W2":gW2/B,"b2":gb2/B}
        adam_step(P,mom,vel,grads,step)
    return P

def eval_add(P, pairs, d):
    bd=[]
    for t in pairs:
        idx=np.array(list(t))[None,:]
        emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist())
        bd.append(len(set(t.tolist()) & topd))
    return float(np.mean(bd))

def maxsingle_add(P, d):
    m=[]
    for i in range(N):
        idx=np.full((1,d),i); emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist()); m.append(len({i}&topd))
    return float(np.mean(m))

# ------------- TRACE arms (DERIV positional / MICRO set-addressed) -------------
def init_trace(rng, mode, d):
    s=1.0/np.sqrt(D)
    P={"E":rng.standard_normal((N,D))*s,
       "Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
       "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
       "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}
    if mode=="DERIV": P["Wpos"]=rng.standard_normal((d,D))*s   # per-step position bias
    else:             P["Wemit"]=np.eye(D)+rng.standard_normal((D,D))*0.05
    return P

def build_trace_examples(tuples, d):
    """Per-line teacher-forced examples (stop-grad state feedback).
    target = t-th sorted constituent (canonical order); emitted = sorted prefix."""
    ex_inp=[]; ex_emit=[]; ex_pos=[]; ex_tgt=[]
    def add(sorted_t):
        for t in range(len(sorted_t)):
            ex_inp.append(list(sorted_t)); ex_emit.append(list(sorted_t[:t]))
            ex_pos.append(t); ex_tgt.append(sorted_t[t])
    for tp in tuples: add(sorted(tp.tolist()))
    for i in range(N): add([i])                             # singleton anchors
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
    """Decode d lines. DERIV: positional argmax (may repeat). MICRO: hard copy+dedup edit."""
    bd=[]
    for tp in pairs:
        tset=set(tp.tolist()); emitted=[]
        pin=pool(P["E"], list(tp))
        proj_in=pin@P["Win"].T
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
        bd.append(len(set(emitted) & tset))
    return float(np.mean(bd))

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
def predictors(train_tuples, d):
    # sigma: mean distinct partners per concept in training tuples
    partners={i:set() for i in range(N)}
    for tp in train_tuples:
        for a in tp:
            for b in tp:
                if a!=b: partners[int(a)].add(int(b))
    sigma=float(np.mean([len(partners[i]) for i in range(N)]))
    # rho: echo-residual = frac of held-out local rules (constituent-in-set) NOT covered
    # in training. Every concept appears in training tuples+anchors -> local rule covered.
    covered=set()
    for tp in train_tuples: covered.update(int(x) for x in tp)
    covered.update(range(N))  # anchors
    rho=1.0-len(covered)/N
    # kappa: micro-trace mean local-copy ratio across the d lines
    kappa=float(np.mean([ (t)/(t+1) for t in range(d) ]))
    # M: memorization-disadvantage = |trace|/grammar-length = mean cumulative-line-size
    M=float(np.mean([t+1 for t in range(d)]))/1.0
    return {"rho":round(rho,4),"sigma":round(sigma,3),"kappa":round(kappa,4),"M":round(M,3)}

def main():
    t0=time.time(); out={"lever":"V2_micro_trace","depths":{}}
    for d in DEPTHS:
        res={a:{"bd":[],"ms":[]} for a in ["ADD","DERIV","MICRO"]}; preds=None
        for seed in SEEDS:
            rng=np.random.default_rng(seed)
            tr,te=make_tuples(rng,d)
            if preds is None: preds=predictors(tr,d)
            # ADD
            Pa=train_add(init_add(rng),tr,d,rng)
            res["ADD"]["bd"].append(eval_add(Pa,te,d)); res["ADD"]["ms"].append(maxsingle_add(Pa,d))
            # DERIV
            Pd=train_trace(init_trace(rng,"DERIV",d),tr,"DERIV",d,rng)
            res["DERIV"]["bd"].append(eval_trace(Pd,te,"DERIV",d)); res["DERIV"]["ms"].append(maxsingle_trace(Pd,"DERIV",d))
            # MICRO
            Pm=train_trace(init_trace(rng,"MICRO",d),tr,"MICRO",d,rng)
            res["MICRO"]["bd"].append(eval_trace(Pm,te,"MICRO",d)); res["MICRO"]["ms"].append(maxsingle_trace(Pm,"MICRO",d))
            print(f"[d{d} seed{seed}] ADD bd={res['ADD']['bd'][-1]:.3f} DERIV bd={res['DERIV']['bd'][-1]:.3f} MICRO bd={res['MICRO']['bd'][-1]:.3f}",flush=True)
        summ={a:{"best_distinct_mean":float(np.mean(res[a]["bd"])),
                 "best_distinct_seeds":[round(x,3) for x in res[a]["bd"]],
                 "max_single_mean":float(np.mean(res[a]["ms"]))} for a in res}
        add_bd=summ["ADD"]["best_distinct_mean"]; der_bd=summ["DERIV"]["best_distinct_mean"]; mic_bd=summ["MICRO"]["best_distinct_mean"]
        lever_margin=mic_bd-add_bd; deriv_margin=der_bd-add_bd
        out["depths"][d]={"arms":summ,"predictors":preds,
                          "lever_margin":round(lever_margin,4),"deriv_margin":round(deriv_margin,4)}
    # verdict on depth-2 primary + depth curve
    d2=out["depths"][2]; d3=out["depths"][3]
    mic2=d2["arms"]["MICRO"]["best_distinct_mean"]; ms2=d2["arms"]["MICRO"]["max_single_mean"]
    lm2,dm2=d2["lever_margin"],d2["deriv_margin"]; lm3=d3["lever_margin"]; dm3=d3["deriv_margin"]
    mic3=d3["arms"]["MICRO"]["best_distinct_mean"]; ms3=d3["arms"]["MICRO"]["max_single_mean"]
    add2=d2["arms"]["ADD"]["best_distinct_mean"]; add3=d3["arms"]["ADD"]["best_distinct_mean"]
    # task frozen bar: PASS = bd>=2 AND bd>max_single AND lever>ADD(margin>0) AND lever_margin>deriv_margin
    # KILL = lever<=ADD OR lever_margin<=deriv_margin
    pass_d2=(mic2>=2.0) and (mic2>ms2) and (mic2>add2) and (lm2>dm2)
    pass_d3=(mic3>=2.0) and (mic3>ms3) and (mic3>add3) and (lm3>dm3)
    margin_grows=lm3>lm2
    out["summary"]={
        "pass_depth2":bool(pass_d2),"pass_depth3":bool(pass_d3),
        "ADD_bd_d2":add2,"MICRO_bd_d2":mic2,"ADD_bd_d3":add3,"MICRO_bd_d3":mic3,
        "lever_margin_d2":lm2,"deriv_margin_d2":dm2,"lever_margin_d3":lm3,"deriv_margin_d3":dm3,
        "margin_grows_with_depth":bool(margin_grows),
        "PASS":bool(pass_d2 or pass_d3),
        "VERDICT":("ESCALATE (micro-trace beats ADD & DERIV-baseline margin on held-out; "
                   "STEP-1 303M candidate)" if (pass_d2 or pass_d3) else
                   "KILL (micro-trace <= ADD (additive control is ceiling) or <= DERIV baseline "
                   "margin; target-format/decode lever floors, no GPU rent)")}
    out["wall_sec"]=round(time.time()-t0,1)
    open("/Users/mini/dancinlab/anima/state/g1_lever_step0/V2_micro_trace/result.json","w").write(json.dumps(out,indent=2))
    print(json.dumps(out["summary"],indent=2)); print("PREDICTORS d2:",out["depths"][2]["predictors"],"d3:",out["depths"][3]["predictors"])
if __name__=="__main__": main()
