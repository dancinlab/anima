#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP-0 DIRECTIONAL probe for trunk-objective candidate (2):
  "Non-additive composition-property prediction with a NON-COMMUTATIVE target"

DPI meta-law (structural proof, from anima census):
  A conjunction/binding readout is by-construction INERT when the TARGET is an
  exchangeable bag/histogram of parts (sum is order-invariant => any conjunction
  op is re-expressible additively). Escape => make the TARGET non-commutative
  (order/joint dependent), so no additive/bag readout can express it.

This candidate's whole gambit = the DPI contrapositive. STEP-0 must answer two
things HONESTLY with $0 numpy (DIRECTIONAL only, not 303M engine-native):

  Exp A (mechanism, BY-CONSTRUCTION => REFRIED unless B rescues it):
     Can a non-commutative target *mechanically* make binding beat additive,
     with SHUFFLE + ablation controls? Confirms the contrapositive is real,
     but the interaction is HAND-PLANTED (vi(x)vj artifact risk, L3 lesson).

  Exp B (the actual crack, NOT by-construction):
     Does a non-commutative composition property REALLY EXIST in a REAL corpus,
     and -- the G1 question -- does its non-additive part GENERALIZE held-out
     (recombination) or is it pair-specific memorization (novelty G2 != G1)?
     Real Korean dialogue corpus. Word-order directionality. Nothing planted.

Everything is frozen/pre-registered below. Numbers printed verbatim.
"""
import numpy as np, sys, re, collections, json, os

RNG = np.random.default_rng(20260705)

def sig(z): return 1.0/(1.0+np.exp(-np.clip(z,-30,30)))

class Adam:
    """minimal Adam for a dict of numpy arrays."""
    def __init__(self, params, lr=0.05, b1=0.9, b2=0.999, eps=1e-8):
        self.p=params; self.lr=lr; self.b1=b1; self.b2=b2; self.eps=eps
        self.m={k:np.zeros_like(v) for k,v in params.items()}
        self.v={k:np.zeros_like(v) for k,v in params.items()}; self.t=0
    def step(self, grads):
        self.t+=1
        for k,g in grads.items():
            self.m[k]=self.b1*self.m[k]+(1-self.b1)*g
            self.v[k]=self.b2*self.v[k]+(1-self.b2)*g*g
            mh=self.m[k]/(1-self.b1**self.t); vh=self.v[k]/(1-self.b2**self.t)
            self.p[k]-=self.lr*mh/(np.sqrt(vh)+self.eps)

# =====================================================================
# PRE-REGISTERED BARS (frozen before running)
# =====================================================================
BARS = {
  "A_binding_beats_additive": "held-out acc(bilinear) - acc(additive) >= +0.15",
  "A_shuffle_kills_it":       "SHUFFLE derangement collapses earned to <= +0.03",
  "A_ablation_commutative":   "commutative(bag) target => earned <= +0.03",
  "B_noncommutative_exists":  "real corpus: residual-after-additive AUC >= 0.60 (order info additive can't hold)",
  "B_recombination_holdout":  "real corpus: bilinear earned on HELD-OUT pairs >= +0.05 AUC over additive",
}

# =====================================================================
# EXPERIMENT A -- synthetic mechanism proof (BY-CONSTRUCTION, flagged REFRIED)
# =====================================================================
def exp_A():
    print("="*72); print("EXP A  synthetic non-commutative target (mechanism / BY-CONSTRUCTION)"); print("="*72)
    V, d_true = 60, 5
    # Ground a NON-TRANSITIVE (rock-paper-scissors-like) relation via a low-rank
    # ANTISYMMETRIC matrix R[a,b] = e_a^T K e_b, K antisymmetric.  target(a,b)=1 if R>0.
    # A total-order scalar 'leftness' CANNOT represent cycles => additive floor.
    E = RNG.standard_normal((V, d_true))
    Kf = RNG.standard_normal((d_true, d_true)); K = Kf - Kf.T      # antisymmetric
    R = E @ K @ E.T                                                # R = -R.T
    def target_nc(a,b): return (R[a,b] > 0).astype(np.float64)     # non-commutative
    def target_comm(a,b):                                          # ablation: bag target
        s = R.__abs__().sum(1)                                     # per-word magnitude
        return ((s[a]+s[b]) > np.median(s)*2).astype(np.float64)   # symmetric in a,b

    # all ordered pairs a!=b
    pairs = np.array([(a,b) for a in range(V) for b in range(V) if a!=b])
    RNG.shuffle(pairs)
    ntr = int(0.7*len(pairs)); tr, te = pairs[:ntr], pairs[ntr:]

    def fit_eval(target_fn, shuffle=False):
        a_tr,b_tr = tr[:,0], tr[:,1]; a_te,b_te = te[:,0], te[:,1]
        b_tr_use = b_tr.copy()
        if shuffle:                                               # SHUFFLE / partner-scramble
            # break the (a,b) pairing: keep label from the TRUE pair but feed a mismatched b.
            # if binding advantage survives, it wasn't using the real partner => control.
            perm = RNG.permutation(len(b_tr_use)); b_tr_use = b_tr_use[perm]
        y_tr = target_fn(a_tr,b_tr); y_te = target_fn(a_te,b_te)  # label always from TRUE pair
        n=len(a_tr)
        # ADDITIVE: score = u_a + v_b  (bag readout, no interaction)
        opt=Adam({'u':np.zeros(V),'v':np.zeros(V)}, lr=0.1)
        for _ in range(1500):
            u,v=opt.p['u'],opt.p['v']; p=sig(u[a_tr]+v[b_tr_use]); g=(p-y_tr)/n
            gu=np.zeros(V); gv=np.zeros(V); np.add.at(gu,a_tr,g); np.add.at(gv,b_tr_use,g)
            opt.step({'u':gu,'v':gv})
        u,v=opt.p['u'],opt.p['v']
        add_tr=((sig(u[a_tr]+v[b_tr_use])>0.5)==(y_tr>0.5)).mean()
        add_te=((sig(u[a_te]+v[b_te])>0.5)==(y_te>0.5)).mean()
        # BILINEAR: score = x_a^T W y_b  (JOINT interaction term = binding)
        dd=10
        opt2=Adam({'X':RNG.standard_normal((V,dd))*0.3,'Y':RNG.standard_normal((V,dd))*0.3,
                   'W':RNG.standard_normal((dd,dd))*0.1}, lr=0.02)
        for _ in range(3000):
            X,Y,W=opt2.p['X'],opt2.p['Y'],opt2.p['W']
            xa=X[a_tr]; yb=Y[b_tr_use]; z=np.einsum('ij,jk,ik->i',xa,W,yb); p=sig(z); g=(p-y_tr)/n
            gW=np.einsum('i,ij,ik->jk',g,xa,yb)
            gX=np.zeros_like(X); gY=np.zeros_like(Y)
            np.add.at(gX,a_tr,g[:,None]*(yb@W.T)); np.add.at(gY,b_tr_use,g[:,None]*(xa@W))
            opt2.step({'X':gX,'Y':gY,'W':gW})
        X,Y,W=opt2.p['X'],opt2.p['Y'],opt2.p['W']
        bil_tr=((sig(np.einsum('ij,jk,ik->i',X[a_tr],W,Y[b_tr_use]))>0.5)==(y_tr>0.5)).mean()
        bil_te=((sig(np.einsum('ij,jk,ik->i',X[a_te],W,Y[b_te]))>0.5)==(y_te>0.5)).mean()
        return add_tr,add_te,bil_tr,bil_te

    atr_nc,add_nc,btr_nc,bil_nc = fit_eval(target_nc, shuffle=False)
    atr_sh,add_sh,btr_sh,bil_sh = fit_eval(target_nc, shuffle=True)
    atr_cm,add_cm,btr_cm,bil_cm = fit_eval(target_comm, shuffle=False)
    res = {
      "noncommutative_target": {"add_train":round(atr_nc,4),"add_hold":round(add_nc,4),
                                 "bil_train":round(btr_nc,4),"bil_hold":round(bil_nc,4),
                                 "earned_hold":round(bil_nc-add_nc,4)},
      "shuffle_control":       {"add_hold":round(add_sh,4),"bil_hold":round(bil_sh,4),
                                 "earned_hold":round(bil_sh-add_sh,4)},
      "commutative_ablation":  {"add_hold":round(add_cm,4),"bil_hold":round(bil_cm,4),
                                 "earned_hold":round(bil_cm-add_cm,4)},
    }
    for k,v in res.items(): print(f"  {k:24s} {v}")
    print("  NOTE: interaction is HAND-PLANTED (antisym R). By-construction => REFRIED alone.")
    return res

# =====================================================================
# EXPERIMENT B -- REAL Korean corpus, non-commutative directionality (the crack)
# =====================================================================
def exp_B(corpus_path):
    print("="*72); print("EXP B  REAL corpus word-order directionality (NOT by-construction)"); print("="*72)
    txt = open(corpus_path, encoding='utf-8', errors='ignore').read()
    lines = [l for l in txt.split('\n') if l.strip()]
    # whitespace tokens; keep top-K frequent as vocab (Korean words carry particles => order-rich)
    toks_per_line=[]
    freq=collections.Counter()
    for l in lines:
        t=re.findall(r'[^\s]+', l)
        toks_per_line.append(t); freq.update(t)
    K=700
    vocab=[w for w,_ in freq.most_common(K)]
    idx={w:i for i,w in enumerate(vocab)}
    # directed adjacent co-occurrence counts C[a,b] = # of "a immediately before b"
    C=np.zeros((K,K))
    for t in toks_per_line:
        for a,b in zip(t,t[1:]):
            if a in idx and b in idx and a!=b:
                C[idx[a],idx[b]]+=1
    # unordered pairs with enough directional evidence
    MIN=12
    pair_rows=[]
    for a in range(K):
        for b in range(a+1,K):
            n_ab=C[a,b]; n_ba=C[b,a]; tot=n_ab+n_ba
            if tot>=MIN:
                pair_rows.append((a,b,n_ab,n_ba,tot))
    pair_rows=np.array(pair_rows,dtype=np.float64)
    P=len(pair_rows)

    # ---------------------------------------------------------------
    # MODEL-FREE non-commutativity census (optimizer-independent, the robust core).
    # A total-order (=additive leftness) relation is TRANSITIVE: a>b, b>c => a>c.
    # Genuine non-additivity = INTRANSITIVE 3-cycles (a>b>c>a) no scalar leftness holds.
    #   null "pure total order" => 0% cycles ; null "no order/random" => 25% cycles.
    # ---------------------------------------------------------------
    def cycle_census(seed_shuffle=None):
        # confident directed edge a->b if a strongly precedes b
        D={}
        rng2=np.random.default_rng(seed_shuffle) if seed_shuffle is not None else None
        for a,b,nab,nba,t in pair_rows:
            a,b=int(a),int(b); yv=nab/t
            if seed_shuffle is not None: yv=rng2.random()   # SHUFFLE: random direction
            if abs(yv-0.5)>=0.15:                            # confident
                if yv>0.5: D[(a,b)]=1
                else:      D[(b,a)]=1
        conf=set(k for k in D)
        # adjacency of confident edges
        succ=collections.defaultdict(set)
        for (a,b) in conf: succ[a].add(b)
        tri_tot=0; tri_cyc=0
        nodes=list(succ.keys())
        for a in nodes:
            for b in succ[a]:
                for c in succ[b]:
                    if c==a: continue
                    # triangle on {a,b,c} needs all three ordered; check a?c
                    if (a,c) in conf or (c,a) in conf:
                        tri_tot+=1
                        if (c,a) in conf: tri_cyc+=1        # a>b>c>a = 3-cycle
        return tri_tot, tri_cyc
    tt,tc = cycle_census()
    st,sc = cycle_census(seed_shuffle=7)
    cyc_frac = (tc/tt) if tt else float('nan')
    shuf_frac= (sc/st) if st else float('nan')
    print(f"  [model-free] triangles={tt}  3-cycles={tc}  cycle_frac={cyc_frac:.4f}"
          f"  | SHUFFLE-null cycle_frac={shuf_frac:.4f} (random~0.25, total-order~0.0)")
    if P<50:
        print(f"  too few pairs (P={P})"); return {"error":"insufficient pairs","P":int(P)}
    # directionality label y = P(a before b) empirical  (in [0,1]); antisymmetric by def
    a_i=pair_rows[:,0].astype(int); b_i=pair_rows[:,1].astype(int)
    n_ab=pair_rows[:,2]; n_ba=pair_rows[:,3]; tot=pair_rows[:,4]
    y=n_ab/tot                                # target directionality, real, NOTHING planted
    w_pair=tot                                # weight by evidence
    # ---- how non-commutative is it at all? fraction of pairs with a clear direction
    strong=((np.maximum(y,1-y))>=0.8)
    print(f"  vocab K={K}  usable ordered-pairs P={P}  strongly-directional(>=80/20)={strong.mean():.3f}")

    # split pairs into TRAIN / HELDOUT (novel (a,b) combos; words still seen)
    order=RNG.permutation(P); ntr=int(0.7*P); trI,teI=order[:ntr],order[ntr:]

    def wbce_auc(pred, yy, ww, mask):
        # weighted AUC-ish: prob-weighted accuracy of predicting sign(y-0.5)
        pm,ym,wm=pred[mask],yy[mask],ww[mask]
        lab=(ym>0.5); conf=(pm>0.5)
        # only score pairs with a real direction (exclude ~0.5 ties, |y-.5|>=0.1)
        sel=np.abs(ym-0.5)>=0.1
        if sel.sum()==0: return float('nan')
        return float(((conf[sel]==lab[sel])*wm[sel]).sum()/wm[sel].sum())

    # ADDITIVE 'leftness' model: predict logit(P(a before b)) = w_a - w_b  (total order)
    lw=np.zeros(K); lr=0.3
    for _ in range(1500):
        z=lw[a_i[trI]]-lw[b_i[trI]]; p=sig(z); g=(p-y[trI])*w_pair[trI]
        np.add.at(lw,a_i[trI],-lr*g/w_pair[trI].sum())
        np.add.at(lw,b_i[trI],+lr*g/w_pair[trI].sum())
    p_add=sig(lw[a_i]-lw[b_i])
    add_tr=wbce_auc(p_add,y,w_pair,trI); add_te=wbce_auc(p_add,y,w_pair,teI)

    # residual after additive: is there order info additive CANNOT hold? (non-commutative core)
    resid = y - p_add
    # AUC of predicting sign(resid vs 0) is meaningless alone; instead measure: after removing
    # best total-order, does a BILINEAR (interaction) recover extra directional signal held-out?

    # BILINEAR antisymmetric model: logit = x_a^T S x_b, S antisymmetric => naturally
    # antisymmetric in (a,b) = exactly a non-commutative JOINT term (binding, not bag).
    dd=12
    opt=Adam({'X':RNG.standard_normal((K,dd))*0.1,'Sf':RNG.standard_normal((dd,dd))*0.05}, lr=0.02)
    ai,bi,ytr,wtr=a_i[trI],b_i[trI],y[trI],w_pair[trI]; wsum=wtr.sum()
    lw_fix=lw.copy()                               # additive part frozen; bilinear adds on top
    for ep in range(4000):
        X=opt.p['X']; S=opt.p['Sf']-opt.p['Sf'].T
        xa=X[ai]; xb=X[bi]
        z=lw_fix[ai]-lw_fix[bi]+np.einsum('ij,jk,ik->i',xa,S,xb)
        p=sig(z); g=(p-ytr)*wtr/wsum
        gS=np.einsum('i,ij,ik->jk',g,xa,xb); gSf=gS-gS.T   # antisym-consistent grad
        gX=np.zeros_like(X)
        np.add.at(gX,ai,g[:,None]*(xb@S.T)); np.add.at(gX,bi,g[:,None]*(xa@S))
        opt.step({'X':gX,'Sf':gSf})
    X=opt.p['X']; S=opt.p['Sf']-opt.p['Sf'].T
    z_all=lw[a_i]-lw[b_i]+np.einsum('ij,jk,ik->i',X[a_i],S,X[b_i])
    p_bil=sig(z_all)
    bil_tr=wbce_auc(p_bil,y,w_pair,trI); bil_te=wbce_auc(p_bil,y,w_pair,teI)

    res={
      "modelfree_cycle_census": {"triangles":int(tt),"three_cycles":int(tc),
                                 "cycle_frac":round(float(cyc_frac),4),
                                 "shuffle_null_frac":round(float(shuf_frac),4),
                                 "interp":"cycle_frac~0 => total-order/additive (DPI-FLOOR); "
                                          ">>0 & <shuffle => genuine non-additive structure"},
      "additive_leftness":  {"train_acc":round(add_tr,4),"heldout_acc":round(add_te,4)},
      "additive+bilinear":  {"train_acc":round(bil_tr,4),"heldout_acc":round(bil_te,4)},
      "earned_heldout":     round(bil_te-add_te,4),
      "earned_train":       round(bil_tr-add_tr,4),
      "additive_fits_train_frac": round(float(add_tr),4),
      "strongly_directional_frac": round(float(strong.mean()),4),
      "P_pairs": int(P),
      "CAVEAT":"model-based earned is OPTIMIZER-FRAGILE (SGD run gave earned~0, Adam gave +0.24); "
               "antisym-bilinear SUBSUMES additive leftness so 'earned' conflates better-fit vs "
               "non-additivity. Trust the model-free cycle census.",
    }
    for k,v in res.items(): print(f"  {k:26s} {v}")
    print("  earned_train>0 & earned_heldout~0  => non-additive part is pair-MEMORIZATION (G2!=G1)")
    print("  earned_heldout>0                   => real non-commutative signal RECOMBINES (escape)")
    return res

if __name__=="__main__":
    cp=sys.argv[1]
    A=exp_A()
    B=exp_B(cp)
    out={"bars":BARS,"expA":A,"expB":B}
    json.dump(out, open(os.path.join(os.path.dirname(__file__),"result.json"),"w"),
              ensure_ascii=False, indent=2)
    print("\nwrote result.json")
