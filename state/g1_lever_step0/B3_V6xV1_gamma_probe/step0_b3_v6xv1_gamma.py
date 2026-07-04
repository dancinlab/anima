#!/usr/bin/env python3
"""G1 LEVER B3 = V6 x V1  gamma-via-DATA-channel probe — STEP-0 CHEAP ENGINE-NATIVE KILL.

Real-G1-homomorphic toy (mirrors state/g1_gamma_engine_native/step0_gamma_bind_kill.py
and the sibling state/g1_lever_step0/V2_micro_trace/step0_v2_micro_trace.py harness):
N concepts, held-out d-tuples, recombination = emit ALL d constituent keywords
(best_distinct = # distinct constituents emitted within budget d). LOSS is next-token /
reconstruction (NOT recomb-rigged). Arms differ ONLY in the TARGET-FORMAT / data channel.

  ADD    (additive control)  : additive sum-pool -> one-shot multi-label top-d readout.
  DERIV  (derivtrace base)   : positional autoregressive trace over SUM-pool, single path.
                               bd~baseline reference margin  (2x2 factorial (0,0) cell).
  V1     (skeleton-bind)     : structure/content factorized. Input pool is HRR-BOUND
                               S = SUM_k cconv(role_k, E[c_k]); slot t decoded by UNBIND
                               probe_t = ccorr(role_k, S). roles = FIXED random keys
                               (content-free skeleton, sigma_eff decoupled). Single path.
                               = gamma constructive-bind injected via the DATA channel.
  V6     (multi-path)        : SUM-pool, set-addressed emit (emitted-set feedback) trained
                               over ALL derivation orderings (confluence) + dedup decode.
                               paraphrase/order-invariance, NO binding.
  V6xV1  (B3 combined)       : BOUND-pool (V1) + multipath training + dedup decode (V6).
                               tests SYNERGY: does bind-in-data x multipath > sum of each.

FROZEN BAR (pre-registered, no post-hoc move -- c9/p7):
  N=24, D=64, HELDOUT=0.45, STEPS=4000, seeds {7,4302,4303}, depths {2,3}.
  metric = held-out best_distinct.
  LEVER PASS  = bd>=2 AND bd>max_single AND margin(arm-ADD) > margin(DERIV-ADD).
  SYNERGY     = bd(V6xV1) > bd(V1)+bd(V6)-bd(DERIV)  (2x2 interaction, DERIV=(0,0) cell).
  gamma-data GPU-ESCALATE iff V6xV1 PASSES the lever bar (beats ADD & DERIV-margin).
Predictors rho/sigma/kappa/M computed per-arm; each arm carries a pre-registered
predicted pass (PASS <=> rho~0 AND sigma_eff>1 AND delta_copy<=RF AND margin ~ log M).

DIRECTIONAL: toy numpy, NOT 303M engine-native (a_engine_native_learning). Pre-screen
only -- gates GPU spend, terminal verdict forbidden.
"""
import numpy as np, json, time, itertools

N = 24; D = 64; HELDOUT = 0.45; STEPS = 4000; LR = 3e-3
SEEDS = [7, 4302, 4303]; DEPTHS = [2, 3]; MAXT = 200; MAXPERM = 6
b1a, b2a, eps = 0.9, 0.999, 1e-8

# fixed content-free role keys (the skeleton) -- part of the frozen data format, shared
# across arms & seeds so V1/V6xV1 differ from DERIV/V6 ONLY by the bind channel.
_role_rng = np.random.default_rng(12345)
ROLES = _role_rng.standard_normal((max(DEPTHS), D))
ROLES = ROLES / np.linalg.norm(ROLES, axis=1, keepdims=True)

def gelu(x): return 0.5*x*(1.0+np.tanh(0.7978845608*(x+0.044715*x**3)))
def dgelu(x):
    c=0.7978845608; u=c*(x+0.044715*x**3); t=np.tanh(u); du=c*(1.0+3*0.044715*x**2)
    return 0.5*(1.0+t)+0.5*x*(1.0-t**2)*du
def sigmoid(x): return 1.0/(1.0+np.exp(-np.clip(x,-30,30)))
def softmax(z):
    z=z-z.max(1,keepdims=True); e=np.exp(z); return e/e.sum(1,keepdims=True)
# HRR circular conv/corr over last axis (batched)
def cconv(a,b): return np.real(np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)))
def ccorr(a,b): return np.real(np.fft.ifft(np.conj(np.fft.fft(a))*np.fft.fft(b)))

def make_tuples(rng, d):
    combos=list(itertools.combinations(range(N), d)); rng.shuffle(combos)
    combos=combos[:MAXT]
    ncut=int(len(combos)*(1-HELDOUT))
    return [np.array(c) for c in combos[:ncut]], [np.array(c) for c in combos[ncut:]]

def adam_step(P, mom, vel, grads, step):
    for k in P:
        g=grads[k]; mom[k]=b1a*mom[k]+(1-b1a)*g; vel[k]=b2a*vel[k]+(1-b2a)*(g*g)
        mh=mom[k]/(1-b1a**step); vh=vel[k]/(1-b2a**step); P[k]-=LR*mh/(np.sqrt(vh)+eps)

# ================= ADD: additive one-shot multi-label =================
def init_add(rng):
    s=1.0/np.sqrt(D)
    return {"E":rng.standard_normal((N,D))*s,
            "Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
            "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
            "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}
def train_add(P, tuples, d, rng):
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    idx=np.array([list(t) for t in tuples]); Y=np.zeros((len(tuples),N))
    for r,t in enumerate(tuples): Y[r, t]=1.0
    anc_idx=np.stack([np.full(d,i) for i in range(N)]); anc_Y=np.eye(N)
    IDX=np.concatenate([idx,anc_idx],0); YY=np.concatenate([Y,anc_Y],0); B=len(IDX)
    for step in range(1,STEPS+1):
        emb=P["E"][IDX]; proj=emb@P["Win"].T; p=proj.sum(1)
        z1=p@P["W1"].T+P["b1"]; z=gelu(z1); logits=z@P["W2"].T+P["b2"]
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
    bd=[]
    for t in pairs:
        idx=np.array(list(t))[None,:]; emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist()); bd.append(len(set(t.tolist()) & topd))
    return float(np.mean(bd))
def maxsingle_add(P, d):
    m=[]
    for i in range(N):
        idx=np.full((1,d),i); emb=P["E"][idx]; p=(emb@P["Win"].T).sum(1)
        z=gelu(p@P["W1"].T+P["b1"]); logits=(z@P["W2"].T+P["b2"])[0]
        topd=set(np.argsort(logits)[-d:].tolist()); m.append(len({i}&topd))
    return float(np.mean(m))

# ============ SUM-pool trace arms (DERIV positional / V6 set+multipath) ============
def init_sum(rng, mode, d):
    s=1.0/np.sqrt(D)
    P={"E":rng.standard_normal((N,D))*s,"Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
       "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
       "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N)}
    if mode=="DERIV": P["Wpos"]=rng.standard_normal((d,D))*s
    else:             P["Wemit"]=np.eye(D)+rng.standard_normal((D,D))*0.05
    return P
def build_sum_examples(tuples, d, multipath):
    """DERIV: single sorted path, positional target. V6: ALL orderings, set-addressed."""
    inp=[]; emit=[]; pos=[]; tgt=[]
    def add_path(seq):
        for t in range(len(seq)):
            inp.append(list(seq)); emit.append(list(seq[:t])); pos.append(t); tgt.append(seq[t])
    for tp in tuples:
        base=tp.tolist()
        if multipath:
            perms=list(itertools.permutations(base))[:MAXPERM]
            for pm in perms: add_path(list(pm))
        else:
            add_path(sorted(base))
    for i in range(N): add_path([i])
    return inp, emit, pos, tgt
def train_sum(P, tuples, mode, d, rng):
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    multipath=(mode=="V6")
    inp,emit,pos,tgt=build_sum_examples(tuples,d,multipath); B=len(tgt)
    tgt=np.array(tgt); posA=np.array(pos)
    Minp=np.zeros((B,N)); Mem=np.zeros((B,N))
    for r,x in enumerate(inp): Minp[r, np.array(x,dtype=int)]=1.0
    for r,x in enumerate(emit):
        if len(x): Mem[r, np.array(x,dtype=int)]=1.0
    oh=np.zeros((B,N)); oh[np.arange(B),tgt]=1.0
    for step in range(1,STEPS+1):
        pin=Minp@P["E"]; proj_in=pin@P["Win"].T
        if mode=="DERIV": ctx=proj_in+P["Wpos"][posA]
        else:            pem=Mem@P["E"]; ctx=proj_in+pem@P["Wemit"].T
        z1=ctx@P["W1"].T+P["b1"]; z=gelu(z1); logits=z@P["W2"].T+P["b2"]
        pr=softmax(logits); dlogits=(pr-oh)/B
        gW2=dlogits.T@z; gb2=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        gW1=dz1.T@ctx; gb1=dz1.sum(0); dctx=dz1@P["W1"]
        gWin=dctx.T@pin; dpin=dctx@P["Win"]; gE=Minp.T@dpin
        grads={"Win":gWin,"W1":gW1,"b1":gb1,"W2":gW2,"b2":gb2}
        if mode=="DERIV":
            gWpos=np.zeros_like(P["Wpos"]); np.add.at(gWpos, posA, dctx); grads["Wpos"]=gWpos
        else:
            gWemit=dctx.T@pem; grads["Wemit"]=gWemit; gE=gE+Mem.T@(dctx@P["Wemit"])
        grads["E"]=gE; adam_step(P,mom,vel,grads,step)
    return P
def eval_sum(P, pairs, mode, d):
    bd=[]
    for tp in pairs:
        tset=set(tp.tolist()); emitted=[]; pin=P["E"][tp].sum(0); proj_in=pin@P["Win"].T
        for t in range(d):
            if mode=="DERIV": ctx=proj_in+P["Wpos"][t]
            else:
                pem=(P["E"][emitted].sum(0) if emitted else np.zeros(D)); ctx=proj_in+pem@P["Wemit"].T
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if mode=="V6":
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else: nxt=int(np.argmax(logits))
            emitted.append(nxt)
        bd.append(len(set(emitted) & tset))
    return float(np.mean(bd))
def maxsingle_sum(P, mode, d):
    m=[]
    for i in range(N):
        emitted=[]; pin=P["E"][i]; proj_in=pin@P["Win"].T
        for t in range(d):
            if mode=="DERIV": ctx=proj_in+P["Wpos"][t]
            else:
                pem=(P["E"][emitted].sum(0) if emitted else np.zeros(D)); ctx=proj_in+pem@P["Wemit"].T
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if mode=="V6":
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else: nxt=int(np.argmax(logits))
            emitted.append(nxt)
        m.append(len(set(emitted)&{i}))
    return float(np.mean(m))

# ============ BOUND-pool trace arms (V1 skeleton / V6xV1 bind x multipath) ============
def init_bound(rng, d):
    s=1.0/np.sqrt(D)
    return {"E":rng.standard_normal((N,D))*s,"Win":np.eye(D)+rng.standard_normal((D,D))*0.05,
            "W1":rng.standard_normal((D,D))*s,"b1":np.zeros(D),
            "W2":rng.standard_normal((N,D))*s,"b2":np.zeros(N),
            "Wslot":rng.standard_normal((d,D))*s}   # per-slot decode bias (learned skeleton head)
def build_bound_paths(tuples, d, multipath):
    """each path = an assignment of the tuple's concepts to roles 0..d-1.
    returns list of concept_seq where concept_seq[k] binds to ROLE k."""
    paths=[]
    for tp in tuples:
        base=tp.tolist()
        if multipath:
            for pm in list(itertools.permutations(base))[:MAXPERM]: paths.append(list(pm))
        else:
            paths.append(sorted(base))
    for i in range(N): paths.append([i]*d)   # singleton anchors (concept i in every role)
    return paths
def train_bound(P, tuples, d, multipath, rng):
    """S = sum_k cconv(role_k, E[c_k]); slot t: probe = ccorr(role_k, S); target c_k.
    roles FIXED. grads: dS=cconv(role,dprobe); dE[c_k]=ccorr(role_k,dS)."""
    mom={k:np.zeros_like(v) for k,v in P.items()}; vel={k:np.zeros_like(v) for k,v in P.items()}
    R=ROLES[:d]
    paths=build_bound_paths(tuples,d,multipath)
    seqs=np.array([p for p in paths]); NP=len(seqs)
    tgt=seqs.reshape(-1); slot=np.tile(np.arange(d), NP); pidx=np.repeat(np.arange(NP), d)
    oh=np.zeros((NP*d, N)); oh[np.arange(NP*d), tgt]=1.0
    for step in range(1,STEPS+1):
        Ec=P["E"][seqs]                           # P,d,D
        bound=cconv(R[None,:,:], Ec)              # P,d,D
        S=bound.sum(1)                            # P,D
        probe=ccorr(R[slot], S[pidx])            # P*d,D
        ctx=probe@P["Win"].T + P["Wslot"][slot]  # P*d,D
        z1=ctx@P["W1"].T+P["b1"]; z=gelu(z1); logits=z@P["W2"].T+P["b2"]
        pr=softmax(logits); dlogits=(pr-oh)/(NP*d)
        gW2=dlogits.T@z; gb2=dlogits.sum(0)
        dz=dlogits@P["W2"]; dz1=dz*dgelu(z1)
        gW1=dz1.T@ctx; gb1=dz1.sum(0); dctx=dz1@P["W1"]
        gWin=dctx.T@probe; dprobe=dctx@P["Win"]
        gWslot=np.zeros_like(P["Wslot"]); np.add.at(gWslot, slot, dctx)
        dS_ex=cconv(R[slot], dprobe)             # P*d,D
        dS=np.zeros((NP,D)); np.add.at(dS, pidx, dS_ex)
        dbound=ccorr(R[None,:,:], dS[:,None,:])  # P,d,D
        gE=np.zeros_like(P["E"])
        for k in range(d): np.add.at(gE, seqs[:,k], dbound[:,k,:])
        grads={"E":gE,"Win":gWin,"W1":gW1,"b1":gb1,"W2":gW2,"b2":gb2,"Wslot":gWslot}
        adam_step(P,mom,vel,grads,step)
    return P
def eval_bound(P, pairs, d, dedup):
    R=ROLES[:d]; bd=[]
    for tp in pairs:
        tset=set(tp.tolist()); c=sorted(tp.tolist())
        S=cconv(R, P["E"][np.array(c)]).sum(0); emitted=[]
        for t in range(d):
            probe=ccorr(R[t], S); ctx=probe@P["Win"].T+P["Wslot"][t]
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if dedup:
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else: nxt=int(np.argmax(logits))
            emitted.append(nxt)
        bd.append(len(set(emitted)&tset))
    return float(np.mean(bd))
def maxsingle_bound(P, d, dedup):
    R=ROLES[:d]; m=[]
    for i in range(N):
        S=cconv(R, P["E"][np.array([i]*d)]).sum(0); emitted=[]
        for t in range(d):
            probe=ccorr(R[t], S); ctx=probe@P["Win"].T+P["Wslot"][t]
            z=gelu(ctx@P["W1"].T+P["b1"]); logits=z@P["W2"].T+P["b2"]
            if dedup:
                order=np.argsort(logits)[::-1]
                nxt=next((int(k) for k in order if int(k) not in emitted), int(order[0]))
            else: nxt=int(np.argmax(logits))
            emitted.append(nxt)
        m.append(len(set(emitted)&{i}))
    return float(np.mean(m))

# ==================== predictors rho / sigma / kappa / M ====================
def predictors(train_tuples, d, arm):
    partners={i:set() for i in range(N)}
    for tp in train_tuples:
        for a in tp:
            for b in tp:
                if a!=b: partners[int(a)].add(int(b))
    sigma_raw=float(np.mean([len(partners[i]) for i in range(N)])) if train_tuples else 0.0
    covered=set()
    for tp in train_tuples: covered.update(int(x) for x in tp)
    covered.update(range(N)); rho=1.0-len(covered)/N
    if arm in ("V6","V6xV1"): kappa=float(np.mean([t/(t+1) for t in range(d)]))
    else: kappa=0.0
    if arm=="ADD": M=1.0
    elif arm in ("V1","V6xV1"): M=float(d)
    else: M=float(np.mean([t+1 for t in range(d)]))
    if arm=="V6xV1": sig_eff=1e9
    elif arm=="V1": sig_eff=float(d)
    else: sig_eff=sigma_raw
    return {"rho":round(rho,4),"sigma_raw":round(sigma_raw,3),
            "sigma_eff":("inf" if sig_eff>=1e8 else round(sig_eff,3)),
            "kappa":round(kappa,4),"M":round(M,3)}
def predicted_pass(arm, pr):
    if arm=="ADD": return None
    rho0 = pr["rho"] < 1e-6
    seff = 1e9 if pr["sigma_eff"]=="inf" else pr["sigma_eff"]
    return bool(rho0 and seff>1.0 and pr["M"]>=2.0)

def main():
    t0=time.time(); ARMS=["ADD","DERIV","V1","V6","V6xV1"]
    out={"lever":"B3_V6xV1_gamma_probe","depths":{}}
    for d in DEPTHS:
        res={a:{"bd":[],"ms":[]} for a in ARMS}; preds={a:predictors([], d, a) for a in ARMS}
        for seed in SEEDS:
            rng=np.random.default_rng(seed); tr,te=make_tuples(rng,d)
            preds={a:predictors(tr, d, a) for a in ARMS}
            Pa=train_add(init_add(rng),tr,d,rng)
            res["ADD"]["bd"].append(eval_add(Pa,te,d)); res["ADD"]["ms"].append(maxsingle_add(Pa,d))
            Pd=train_sum(init_sum(rng,"DERIV",d),tr,"DERIV",d,rng)
            res["DERIV"]["bd"].append(eval_sum(Pd,te,"DERIV",d)); res["DERIV"]["ms"].append(maxsingle_sum(Pd,"DERIV",d))
            P1=train_bound(init_bound(rng,d),tr,d,False,rng)
            res["V1"]["bd"].append(eval_bound(P1,te,d,False)); res["V1"]["ms"].append(maxsingle_bound(P1,d,False))
            P6=train_sum(init_sum(rng,"V6",d),tr,"V6",d,rng)
            res["V6"]["bd"].append(eval_sum(P6,te,"V6",d)); res["V6"]["ms"].append(maxsingle_sum(P6,"V6",d))
            Pc=train_bound(init_bound(rng,d),tr,d,True,rng)
            res["V6xV1"]["bd"].append(eval_bound(Pc,te,d,True)); res["V6xV1"]["ms"].append(maxsingle_bound(Pc,d,True))
            print(f"[d{d} seed{seed}] "+" ".join(f"{a}={res[a]['bd'][-1]:.3f}" for a in ARMS),flush=True)
        summ={a:{"best_distinct_mean":float(np.mean(res[a]["bd"])),
                 "best_distinct_seeds":[round(x,3) for x in res[a]["bd"]],
                 "max_single_mean":float(np.mean(res[a]["ms"]))} for a in ARMS}
        bd={a:summ[a]["best_distinct_mean"] for a in ARMS}
        margins={a:round(bd[a]-bd["ADD"],4) for a in ARMS}
        deriv_margin=margins["DERIV"]
        synergy_lift=round(bd["V6xV1"] - (bd["V1"]+bd["V6"]-bd["DERIV"]), 4)
        out["depths"][d]={"arms":summ,"predictors":preds,"margins_vs_ADD":margins,
                          "deriv_margin":deriv_margin,"synergy_lift":synergy_lift,
                          "predicted_pass":{a:predicted_pass(a,preds[a]) for a in ARMS if a!="ADD"}}
    def cell(dd):
        x=out["depths"][dd]; b=x["arms"]
        return (b["V6xV1"]["best_distinct_mean"], b["V6xV1"]["max_single_mean"],
                x["margins_vs_ADD"]["V6xV1"], x["deriv_margin"], x["synergy_lift"])
    c2=cell(2); c3=cell(3)
    def passq(c): return (c[0]>=2.0) and (c[0]>c[1]) and (c[2]>0.0) and (c[2]>c[3])
    pass2=passq(c2); pass3=passq(c3); syn2=c2[4]>0.0; syn3=c3[4]>0.0
    escalate = pass2 or pass3
    out["summary"]={
        "V6xV1_bd_d2":c2[0],"V6xV1_bd_d3":c3[0],
        "margin_vs_ADD_d2":c2[2],"deriv_margin_d2":c2[3],
        "margin_vs_ADD_d3":c3[2],"deriv_margin_d3":c3[3],
        "synergy_lift_d2":c2[4],"synergy_lift_d3":c3[4],
        "synergy_d2":bool(syn2),"synergy_d3":bool(syn3),
        "pass_depth2":bool(pass2),"pass_depth3":bool(pass3),
        "PASS":bool(escalate),
        "VERDICT":("ESCALATE (gamma-via-DATA-channel V6xV1 beats ADD & DERIV-margin on held-out "
                   "recombination => STEP-1 303M gamma-data candidate)" if escalate else
                   "KILL (V6xV1 <= ADD additive ceiling OR <= DERIV baseline margin; "
                   "constructive-bind injected via data channel floors like the gamma OPERATOR "
                   "(H_1840) -- NO GPU rent for gamma)")}
    out["wall_sec"]=round(time.time()-t0,1)
    open("/Users/mini/dancinlab/anima/state/g1_lever_step0/B3_V6xV1_gamma_probe/result.json","w").write(json.dumps(out,indent=2))
    print(json.dumps(out["summary"],indent=2))
    for dd in DEPTHS: print(f"PRED d{dd}:", out["depths"][dd]["predicted_pass"], "| synergy_lift", out["depths"][dd]["synergy_lift"])
if __name__=="__main__": main()
