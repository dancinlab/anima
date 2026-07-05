"""
S1_trained_parity — hardening stress on E1 GO ($0 numpy, frozen-first, no tune-to-green).

DPI worry: E1's slot>additive lift (7.6x) used a FROZEN closed-form ridge readout — the
easiest regime. The real DPI wall is about a fitted additive combine in a 303M regime. If a
fitted readout of equal (or greater) capacity lets ADDITIVE catch up to SLOT, then E1's frozen
advantage is a mirage and the structural claim collapses (survives=false -> GPU HOLD).

Test: reuse E1's slot vs additive setup (K orthogonal-ish concepts, d, ORDERED held-out
pairs) but swap the frozen closed-form ridge for a fitted (Adam-optimized) readout of matched
capacity on BOTH forms:
  (1) linear-SGD readout (Adam, many epochs)          -> parity w/ closed-form baseline
  (2) MLP readout (1 hidden ReLU, H), SAME H for both  -> capacity parity
  (3) MLP readout with 2x capacity given to ADDITIVE ONLY -> deck stacked FOR additive
Same optimizer/epochs/arch across forms = fair. slot_shuffle control retained.

Structural prior (stated, then tested honestly): additive = a+b is SYMMETRIC in (a,b), so
the ordered-role info is DESTROYED in the representation. No readout capacity can invert an
information-destroying map. Ceiling for additive both-acc ~ 0.5 * P(set recovered) because
role/filler ordering is a coin flip on a symmetric input. If the numbers confirm additive
stays far below slot even with MORE capacity, slot's advantage is STRUCTURAL, not a frozen
artifact -> survives=true. If additive catches up, survives=false. Honest either way.
"""
import numpy as np, json

rng = np.random.default_rng(0)
K, d = 16, 64

# ---- E1's atomic concept dictionary (random Gaussian, unit norm) ----
C = rng.standard_normal((K, d)); C /= np.linalg.norm(C, axis=1, keepdims=True)

# ---- E1's ordered pairs (role a, filler b), a != b, same 70/30 split ----
pairs = np.array([(a, b) for a in range(K) for b in range(K) if a != b])
pairs = pairs[rng.permutation(len(pairs))]
n = len(pairs); n_tr = int(0.70 * n)
train_pairs, held_pairs = pairs[:n_tr], pairs[n_tr:]
assert set(train_pairs[:,0].tolist())==set(range(K)) and set(train_pairs[:,1].tolist())==set(range(K)), "coverage gap"

def build_rep(prs, mode, swap_rng=None):
    a = C[prs[:,0]]; b = C[prs[:,1]]
    if mode == "additive": return a + b
    if mode == "slot":     return np.concatenate([a, b], axis=1)
    if mode == "slot_shuffle":
        m = swap_rng.random(len(prs)) < 0.5
        A=a.copy(); B=b.copy(); A[m],B[m]=b[m],a[m]
        return np.concatenate([A, B], axis=1)
    raise ValueError(mode)

def onehot(ids):
    Y=np.zeros((len(ids),K)); Y[np.arange(len(ids)),ids]=1.0; return Y

# ---------- fitted readouts (Adam, numpy) ----------
def softmax(Z):
    Z=Z-Z.max(1,keepdims=True); E=np.exp(Z); return E/E.sum(1,keepdims=True)

def fit_linear(X, y, K, epochs=4000, lr=5e-3, seed=0):
    r=np.random.default_rng(seed); Dw=X.shape[1]
    W=r.standard_normal((Dw,K))*0.01; b=np.zeros(K)
    mW=np.zeros_like(W); vW=np.zeros_like(W); mb=np.zeros_like(b); vb=np.zeros_like(b)
    Y=onehot(y); N=len(X); b1,b2,eps=0.9,0.999,1e-8
    for t in range(1,epochs+1):
        P=softmax(X@W+b); dZ=(P-Y)/N
        gW=X.T@dZ + 1e-4*W; gb=dZ.sum(0)
        mW=b1*mW+(1-b1)*gW; vW=b2*vW+(1-b2)*gW*gW
        mb=b1*mb+(1-b1)*gb; vb=b2*vb+(1-b2)*gb*gb
        W-=lr*(mW/(1-b1**t))/(np.sqrt(vW/(1-b2**t))+eps)
        b-=lr*(mb/(1-b1**t))/(np.sqrt(vb/(1-b2**t))+eps)
    return lambda Xt: (Xt@W+b)

def fit_mlp(X, y, K, H=256, epochs=4000, lr=3e-3, seed=0):
    r=np.random.default_rng(seed); Dw=X.shape[1]
    W1=r.standard_normal((Dw,H))*np.sqrt(2.0/Dw); b1_=np.zeros(H)
    W2=r.standard_normal((H,K))*np.sqrt(2.0/H); b2_=np.zeros(K)
    params=[W1,b1_,W2,b2_]; m=[np.zeros_like(p) for p in params]; v=[np.zeros_like(p) for p in params]
    Y=onehot(y); N=len(X); beta1,beta2,eps=0.9,0.999,1e-8
    for t in range(1,epochs+1):
        Z1=X@W1+b1_; A1=np.maximum(Z1,0); P=softmax(A1@W2+b2_)
        dZ2=(P-Y)/N
        gW2=A1.T@dZ2 + 1e-4*W2; gb2=dZ2.sum(0)
        dA1=dZ2@W2.T; dZ1=dA1*(Z1>0)
        gW1=X.T@dZ1 + 1e-4*W1; gb1=dZ1.sum(0)
        grads=[gW1,gb1,gW2,gb2]
        for i,g in enumerate(grads):
            m[i]=beta1*m[i]+(1-beta1)*g; v[i]=beta2*v[i]+(1-beta2)*g*g
            params[i]-=lr*(m[i]/(1-beta1**t))/(np.sqrt(v[i]/(1-beta2**t))+eps)
        W1,b1_,W2,b2_=params
    def f(Xt):
        A1=np.maximum(Xt@W1+b1_,0); return A1@W2+b2_
    return f

def both_reach(mode, fitter, **kw):
    sr=np.random.default_rng(1); Xtr=build_rep(train_pairs, mode, sr)
    sr2=np.random.default_rng(101); Xte=build_rep(held_pairs, mode, sr2)
    fr=fitter(Xtr, train_pairs[:,0], K, seed=7, **kw)
    ff=fitter(Xtr, train_pairs[:,1], K, seed=8, **kw)
    pr=fr(Xte).argmax(1); pf=ff(Xte).argmax(1)
    ptr_r=fr(Xtr).argmax(1); ptr_f=ff(Xtr).argmax(1)
    return dict(
        both=float(np.mean((pr==held_pairs[:,0])&(pf==held_pairs[:,1]))),
        role=float(np.mean(pr==held_pairs[:,0])),
        filler=float(np.mean(pf==held_pairs[:,1])),
        fit_both=float(np.mean((ptr_r==train_pairs[:,0])&(ptr_f==train_pairs[:,1]))),
    )

random_both=1.0/(K*K)
res={}
# (1) linear-SGD fitted readout — parity with closed-form
res["additive_linSGD"]      = both_reach("additive", fit_linear)
res["slot_linSGD"]          = both_reach("slot",     fit_linear)
res["slot_shuffle_linSGD"]  = both_reach("slot_shuffle", fit_linear)
# (2) MLP readout, SAME capacity H=256 for both
res["additive_mlpH256"]     = both_reach("additive", fit_mlp, H=256)
res["slot_mlpH256"]         = both_reach("slot",     fit_mlp, H=256)
res["slot_shuffle_mlpH256"] = both_reach("slot_shuffle", fit_mlp, H=256)
# (3) deck stacked FOR additive: give ADDITIVE 2x capacity, slot stays H=256
res["additive_mlpH512"]     = both_reach("additive", fit_mlp, H=512, epochs=6000)

add_best = max(res["additive_linSGD"]["both"], res["additive_mlpH256"]["both"], res["additive_mlpH512"]["both"])
slot_best= max(res["slot_linSGD"]["both"], res["slot_mlpH256"]["both"])
shuffle_best = min(res["slot_shuffle_linSGD"]["both"], res["slot_shuffle_mlpH256"]["both"])

slot_reach=float(slot_best); additive_reach=float(add_best); gap=float(slot_reach-additive_reach)
slot_beats_additive = slot_reach > additive_reach + 0.05
lift=slot_reach-additive_reach
shuffle_collapses=(shuffle_best-additive_reach) < 0.4*lift if lift>0 else False
survives = bool(slot_beats_additive and gap>0.30 and shuffle_collapses)

out={
  "condition":"S1_trained_parity",
  "params":{"K":K,"d":d,"n_pairs":int(n),"n_train":int(n_tr),"n_heldout":int(n-n_tr),
            "random_both_acc":random_both,
            "readouts":["linear-SGD Adam 4k ep","MLP H256 ReLU Adam 4k ep","MLP H512 (additive-only, 6k ep)"]},
  "results_both_role_filler_fitfit":res,
  "slot_reach":slot_reach,
  "additive_reach":additive_reach,
  "gap":gap,
  "shuffle_control_reach":float(shuffle_best),
  "slot_beats_additive":bool(slot_beats_additive),
  "shuffle_collapses":bool(shuffle_collapses),
  "survives":survives,
}
print(json.dumps(out, indent=2))
with open("/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk/hardening/S1_trained_parity.json","w") as f:
    json.dump(out, f, indent=2)
