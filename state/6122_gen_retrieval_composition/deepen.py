# H_6122 ADVERSARIAL DEEPEN — retrieval-composition (numpy DIRECTIONAL screen was 0->2.0 REACHABLE)
# Precedent: H_6112 meiosis numpy REACHABLE(0->1.0) COLLAPSED on real CLMConvMoE (0->0.022). numpy overstates.
# a_break_the_wall: a REACHABLE is NOT confident until controls kill the alternatives. Default ARTIFACT if uncertain.
#
# ORIGINAL operator (probe.py): trunk emits a COMBINATION INDEX = (argmax match to color-tension,
#   argmax match to shape-tension) over a non-parametric anchor pool of SINGLE-feature anchors,
#   then ASSEMBLES = concatenates the two retrieved words. composed_distinct = # target feats in output.
#   Result: additive-top1 readout = 1.0 (floor), retrieval-composition = 2.0, margin 1.0 -> GREEN-DIRECTIONAL.
#
# ADVERSARIAL HYPOTHESIS: the 1.0 margin is a METRIC ARTIFACT of READOUT ARITY (1-slot argmax vs
#   2-slot retrieval), NOT of the proposed "retrieve-two-from-pool" mechanism. Retrieval == concat
#   == pure juxtaposition (probe's own deep_bind=0 confirms no fused/interaction token).
#
# FROZEN BAR (declared BEFORE run): operator SURVIVES only if ALL THREE hold:
#   (C1) generic-nonlinearity control: a GENERIC operator (same 2-slot arity: additive-top2,
#        tanh-top2, mult-top2, randMLP-top2) does NOT reach retrieval's composed_distinct.
#        PASS-C1 iff  retrieval - max(generic_top2 family) >= 0.5   (generic must NOT match)
#   (C2) bind-recoverability BEATS additive: fit linear readout C->parentA and C->parentB on TRAIN
#        pairs, held-out(LOO) recovery. distinctness is necessary-not-sufficient; binding requires
#        recovery to EXCEED the additive-superposition floor.
#        PASS-C2 iff  recover(retrieval) - recover(additive-sum) >= 0.20
#   (C3) ablation collapses: retrieval with its key ingredient OFF (emit ONE index, arity=1) must
#        fall to the additive-top1 floor.  PASS-C3 iff  ablated <= additive_top1 + 0.25
#   SURVIVE = C1 and C2 and C3 ; else ARTIFACT.
import os
os.environ.setdefault("OMP_NUM_THREADS","4")
import numpy as np

D=64
COLORS=["red","blue","green"]     # concept axis A
SHAPES=["circle","square","tri"]  # concept axis B  (independent of A)
PAIRS=[(c,s) for c in COLORS for s in SHAPES]   # 9 novel (never co-stored) pairs
SEEDS=[7,11,23,42,101]

def seeded(seed):
    rng=np.random.default_rng(seed)
    code={}
    for w in COLORS+SHAPES:
        v=rng.standard_normal(D); v/=np.linalg.norm(v); code[w]=v
    pool=[(w,code[w],w) for w in COLORS+SHAPES]   # (feature, tension-vec, text)
    return rng,code,pool

def feats(text): return set(text.split())

def topk_words(q,pool,k):
    sims=np.array([q@v for (_,v,_) in pool])
    idx=np.argsort(-sims)[:k]
    return " ".join(pool[i][2] for i in idx)

def score(out_text,c,s): return len(feats(out_text)&{c,s})

# ---------- C1: generic-nonlinearity / arity family ----------
def op_additive_top1(code,pool,c,s):            # ORIGINAL floor (walled class, 1 slot)
    q=code[c]+code[s]; q/=np.linalg.norm(q)
    return score(topk_words(q,pool,1),c,s)
def op_retrieval(code,pool,c,s):                 # ORIGINAL H_6122 operator
    sims_c=np.array([code[c]@v for (_,v,_) in pool]); a=pool[int(np.argmax(sims_c))][2]
    sims_s=np.array([code[s]@v for (_,v,_) in pool]); b=pool[int(np.argmax(sims_s))][2]
    return score(a+" "+b,c,s)
def op_additive_top2(code,pool,c,s):             # GENERIC: same additive blend, arity=2
    q=code[c]+code[s]; q/=np.linalg.norm(q)
    return score(topk_words(q,pool,2),c,s)
def op_tanh_top2(code,pool,c,s):                 # GENERIC nonlinearity tanh(A+B), arity=2
    q=np.tanh(code[c]+code[s]); q/=np.linalg.norm(q)
    return score(topk_words(q,pool,2),c,s)
def op_mult_top2(code,pool,c,s):                 # GENERIC elementwise A*B, arity=2
    q=code[c]*code[s]; n=np.linalg.norm(q); q=q/n if n>0 else q
    return score(topk_words(q,pool,2),c,s)
def make_randmlp(rng):
    W1=rng.standard_normal((D,2*D))/np.sqrt(2*D); W2=rng.standard_normal((D,D))/np.sqrt(D)
    def f(A,B):
        h=np.maximum(0.0,W1@np.concatenate([A,B])); q=W2@h; n=np.linalg.norm(q); return q/n if n>0 else q
    return f
def op_ablate_arity1(code,pool,c,s):             # C3: retrieval ingredient OFF -> emit ONE index only
    # trunk can pick only a single anchor (arity=1) -> the dominant tension match
    q=code[c]+code[s]; q/=np.linalg.norm(q)
    return score(topk_words(q,pool,1),c,s)

def mean_over(op,extra=None):
    per=[]
    for seed in SEEDS:
        rng,code,pool=seeded(seed)
        f=make_randmlp(rng) if extra=="mlp" else None
        vs=[]
        for c,s in PAIRS:
            if extra=="mlp":
                vs.append(score(topk_words(f(code[c],code[s]),pool,2),c,s))
            else:
                vs.append(op(code,pool,c,s))
        per.append(np.mean(vs))
    return float(np.mean(per))

# ---------- C2: bind-recoverability (vector rep + linear readout, LOO held-out) ----------
def ridge_fit(X,Y,lam=1e-2):
    A=X.T@X+lam*np.eye(X.shape[1]); return np.linalg.solve(A, X.T@Y)
def recover_acc(compose):
    # compose(A,B)->C vector; recover parent color-idx & shape-idx via linear readout, LOO over 9 pairs
    accs=[]
    for seed in SEEDS:
        rng,code,pool=seeded(seed)
        Cs=[]; yc=[]; ys=[]
        for (c,s) in PAIRS:
            Cs.append(compose(code[c],code[s]))
            yc.append(COLORS.index(c)); ys.append(SHAPES.index(s))
        X=np.array(Cs)
        Yc=np.eye(3)[yc]; Ys=np.eye(3)[ys]
        n=len(PAIRS); hitc=0; hits=0
        for i in range(n):                       # leave-one-pair-out
            tr=[j for j in range(n) if j!=i]
            Wc=ridge_fit(X[tr],Yc[tr]); Ws=ridge_fit(X[tr],Ys[tr])
            if int(np.argmax(X[i]@Wc))==yc[i]: hitc+=1
            if int(np.argmax(X[i]@Ws))==ys[i]: hits+=1
        accs.append(0.5*(hitc/n)+0.5*(hits/n))   # avg of color & shape held-out recovery
    return float(np.mean(accs))
comp_retrieval=lambda A,B: np.concatenate([A,B])          # retrieval "assembly" == concat (juxtaposition)
comp_additive =lambda A,B: A+B                            # additive superposition floor

def run():
    add1=mean_over(op_additive_top1)
    ret =mean_over(op_retrieval)
    a2  =mean_over(op_additive_top2)
    tanh=mean_over(op_tanh_top2)
    mult=mean_over(op_mult_top2)
    mlp =mean_over(None,extra="mlp")
    abl =mean_over(op_ablate_arity1)
    generic_max=max(a2,tanh,mult,mlp)

    rec_ret=recover_acc(comp_retrieval)
    rec_add=recover_acc(comp_additive)

    print("[H_6122 ADVERSARIAL DEEPEN] D=64, 9 novel pairs x 5 seeds; chance recovery=0.333")
    print("--- baseline (from probe.py) ---")
    print(f"  additive-top1 (walled floor) composed_distinct = {add1:.3f}")
    print(f"  retrieval-composition        composed_distinct = {ret:.3f}   (original REACHABLE, margin {ret-add1:+.3f})")
    print("--- C1 GENERIC-NONLINEARITY control (all arity=2, same 2-slot readout) ---")
    print(f"  additive-top2  = {a2:.3f}")
    print(f"  tanh(A+B)-top2 = {tanh:.3f}")
    print(f"  mult(A*B)-top2 = {mult:.3f}")
    print(f"  randMLP-top2   = {mlp:.3f}")
    print(f"  generic-family MAX = {generic_max:.3f}   retrieval - generic_max = {ret-generic_max:+.3f}")
    c1_pass = (ret-generic_max) >= 0.5
    print(f"  PASS-C1 (retrieval - generic_max >= 0.5, i.e. generic does NOT match): {c1_pass}")
    print("--- C2 BIND-RECOVERABILITY (linear readout C->parents, LOO held-out) ---")
    print(f"  recover(retrieval=concat)   = {rec_ret:.3f}")
    print(f"  recover(additive-sum floor) = {rec_add:.3f}   retrieval - additive = {rec_ret-rec_add:+.3f}")
    c2_pass = (rec_ret-rec_add) >= 0.20
    print(f"  PASS-C2 (recovery beats additive by >=0.20): {c2_pass}")
    print("  (note: both parents trivially recoverable from EITHER -> juxtaposition, NOT binding;")
    print("   deep_bind fused-token = 0.0 from probe.py -> conjunction/interaction UNREACHABLE)")
    print("--- C3 ABLATION (retrieval ingredient OFF: emit ONE index, arity=1) ---")
    print(f"  ablated(arity=1) = {abl:.3f}   additive-top1 floor = {add1:.3f}")
    c3_pass = abl <= add1 + 0.25
    print(f"  PASS-C3 (ablation collapses to floor): {c3_pass}")
    print("--- FROZEN VERDICT ---")
    survive = c1_pass and c2_pass and c3_pass
    print(f"  SURVIVE = C1({c1_pass}) AND C2({c2_pass}) AND C3({c3_pass}) = {survive}")
    print(f"  VERDICT: {'CONFIRMED (real composition signal - flag real-trunk rung)' if survive else 'ARTIFACT (numpy REACHABLE = readout-arity/juxtaposition artifact, NOT the proposed mechanism)'}")
    print("  H_6112 transfer caveat: even were controls passed, numpy REACHABLE overstates real CLMConvMoE (0->1.0 became 0->0.022). numpy=DIRECTIONAL by construction, terminal 아님.")

if __name__=='__main__':
    run()
